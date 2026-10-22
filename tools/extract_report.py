#!/usr/bin/env python3
"""Extract approved DOCX blocks without rewriting. Private plan and audit stay outside repo."""
import argparse, copy, hashlib, io, json, re
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
from html import escape
from lxml import etree as E, html
from PIL import Image
from layout import SITE, SECTIONS, section_page, build_shell
NS={"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main","a":"http://schemas.openxmlformats.org/drawingml/2006/main","r":"http://schemas.openxmlformats.org/officeDocument/2006/relationships","mc":"http://schemas.openxmlformats.org/markup-compatibility/2006","c":"http://schemas.openxmlformats.org/drawingml/2006/chart","m":"http://schemas.openxmlformats.org/officeDocument/2006/math"}
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(s):return " ".join(s.split())
def clean_doc(z):
    root=E.fromstring(z.read("word/document.xml"))
    for ac in root.xpath("//mc:AlternateContent",namespaces=NS):
        chosen=ac.find("mc:Choice",NS)
        if chosen is None:chosen=ac.find("mc:Fallback",NS)
        if chosen is None:raise ValueError("Unsupported AlternateContent")
        parent=ac.getparent();pos=parent.index(ac)
        for child in list(chosen):
            parent.insert(pos,copy.deepcopy(child));pos+=1
        parent.remove(ac)
    if root.xpath("//w:ins|//w:del",namespaces=NS):raise ValueError("Resolve tracked changes before import")
    return list(root.find("w:body",NS))
def text_of(b):return "".join(b.xpath(".//w:t/text()",namespaces=NS))
def redact(s):
    s=re.sub(r"/Users/[^\n]+?(?= detect train)", "[LOCAL_YOLO_EXECUTABLE]", s)
    s=re.sub(r'"/Users/[^"]+/weights/best\.pt"', '"[LOCAL_MODEL_PATH]"', s)
    s=re.sub(r'"/Users/[^"]+/data\.yaml"', '"[LOCAL_DATA_YAML]"', s)
    s=re.sub(r'(?i)(?<=labelerLogin": ")[^"]+@[^"]+', "[LABELER_EMAIL_REMOVED]", s)
    return s
def strip_jpeg(data):
    # Preserve compressed image data and color profiles; remove EXIF, IPTC and comments.
    if data[:2]!=b"\xff\xd8":raise ValueError("Invalid JPEG")
    out=bytearray(data[:2]);pos=2
    while pos<len(data):
        if data[pos]!=255:raise ValueError("Invalid JPEG segment")
        marker=data[pos+1]
        if marker in (0xda,0xd9):out.extend(data[pos:]);break
        size=int.from_bytes(data[pos+2:pos+4],"big")
        segment=data[pos:pos+size+2]
        if marker not in (0xe1,0xed,0xfe):out.extend(segment)
        pos+=size+2
    return bytes(out)
def clean_image(data,extension):
    if extension.lower() in (".jpg",".jpeg"):
        cleaned=strip_jpeg(data)
        a,b=Image.open(io.BytesIO(data)),Image.open(io.BytesIO(cleaned))
        if a.tobytes()!=b.tobytes():raise ValueError("JPEG pixel data changed")
        if a.getexif().get(274,1)!=1:raise ValueError("Image orientation requires review")
        return cleaned
    im=Image.open(io.BytesIO(data))
    out=io.BytesIO();im.save(out,format="PNG")
    if Image.open(io.BytesIO(out.getvalue())).tobytes()!=im.tobytes():raise ValueError("PNG pixels changed")
    return out.getvalue()
def mathml(n):
    name=E.QName(n).localname
    if name in ("rPr","ctrlPr","lastRenderedPageBreak") or name.endswith("Pr"):return ""
    if name=="t":return "<mtext>"+escape(n.text or "")+"</mtext>"
    kids=lambda:"".join(mathml(c) for c in n)
    if name in ("oMath","oMathPara","e","num","den","sub","sup","r"):return "<mrow>"+kids()+"</mrow>"
    if name=="f":
        return "<mfrac>"+mathml(n.find("m:num",NS))+mathml(n.find("m:den",NS))+"</mfrac>"
    if name in ("sSub","sSup"):
        tag="msub" if name=="sSub" else "msup"; sub="sub" if name=="sSub" else "sup"
        return "<"+tag+">"+mathml(n.find("m:e",NS))+mathml(n.find("m:"+sub,NS))+"</"+tag+">"
    raise ValueError("Unimplemented math object: "+name)
def inline(p,rels):
    original=text_of(p);approved=redact(original)
    if approved!=original:return escape(approved)
    result=[]
    for t in p.xpath(".//w:t",namespaces=NS):
        value=escape(t.text or "");anc=list(t.iterancestors())
        run=next((a for a in anc if a.tag=="{"+NS["w"]+"}r"),None)
        if run is not None:
            if run.find("w:rPr/w:b",NS) is not None:value="<strong>"+value+"</strong>"
            if run.find("w:rPr/w:i",NS) is not None:value="<em>"+value+"</em>"
        h=next((a for a in anc if a.tag=="{"+NS["w"]+"}hyperlink"),None)
        if h is not None:
            target=rels.get(h.get("{"+NS["r"]+"}id"),"")
            if target.startswith(("https://","http://")):value=f'<a href="{escape(target,quote=True)}" rel="noopener">{value}</a>'
        result.append(value)
    return "".join(result)
def figure(path,alt):
    return f'<figure><a href="../assets/figures/{escape(path)}" target="_blank" rel="noopener" aria-label="Open figure at full size"><img src="../assets/figures/{escape(path)}" alt="{escape(alt,quote=True)}" loading="lazy" decoding="async"></a><div class="image-hint">Select figure to view at full size.</div></figure>'
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True);ap.add_argument("--plan",type=Path,required=True)
    ap.add_argument("--audit",type=Path,required=True);ap.add_argument("--verify-only",action="store_true")
    args=ap.parse_args()
    if args.audit.resolve().is_relative_to(SITE.parent.resolve()):raise SystemExit("Audit must be outside repository")
    plan=json.loads(args.plan.read_text());data=args.source.read_bytes()
    if sha(data)!=plan["source_sha256"]:raise SystemExit("Source changed: review and update the private content plan first")
    args.audit.mkdir(parents=True,exist_ok=True)
    with ZipFile(io.BytesIO(data)) as z:
        blocks=clean_doc(z)
        relxml=E.fromstring(z.read("word/_rels/document.xml.rels"))
        rels={r.get("Id"):r.get("Target") for r in relxml}
        heading="";locations={}
        for i,b in enumerate(blocks):
            st=b.xpath("./w:pPr/w:pStyle/@w:val",namespaces=NS)
            if st and st[0].startswith("Heading") and text_of(b).strip():heading=text_of(b).strip()
            locations[i]=heading
        record=[];assets={};verifications=[];titles=dict(SECTIONS);titles["references"]="REFERENCES"
        for slug,ranges in plan["sections"].items():
            ids=[i for start,end in ranges for i in range(start,end)]
            article=[];headings=[];inlist=False
            expected={}
            for i in ids:
                b=blocks[i];txt=text_of(b);approved=redact(txt);bid=f"b{i:04d}"
                if approved.strip():
                    expected[bid]=norm(approved)
                    record.append({"website_section":slug,"source_block":i,"source_heading":locations[i],"source_text_hash":sha(norm(txt).encode()),"website_text_hash":sha(norm(approved).encode()),"copied_unchanged":txt==approved,"reason":None if txt==approved else "Privacy: local file path or dataset labeler email replaced with a neutral placeholder"})
                st=b.xpath("./w:pPr/w:pStyle/@w:val",namespaces=NS)
                st=st[0] if st else ""
                islist=st=="ListParagraph"
                if inlist and not islist and approved.strip():article.append("</ul>");inlist=False
                if approved.strip():
                    if b.tag=="{"+NS["w"]+"}tbl":
                        table=f'<div class="table-scroll" role="region" aria-label="Report table; scroll horizontally if needed" tabindex="0"><table id="{bid}" data-source-id="{bid}">'
                        for rownum,tr in enumerate(b.findall("w:tr",NS)):
                            table+="<tr>"
                            for tc in tr.findall("w:tc",NS):
                                tag="th" if rownum==0 else "td";scope=' scope="col"' if rownum==0 else ""
                                table+=f"<{tag}{scope}>"
                                for p in tc.findall("w:p",NS):table+="<p>"+inline(p,rels)+"</p>"
                                table+=f"</{tag}>"
                            table+="</tr>"
                        article.append(table+"</table></div>")
                    elif st.startswith("Heading") and not txt.strip().startswith("Figure"):
                        level=min(4,int(st[-1])+1);prefix=plan.get("numbering",{}).get(str(i),"")
                        # Automatic numbering is presentation, not added report wording.
                        numbered=f'<span data-generated="number">{escape(prefix)}</span>' if prefix else ""
                        article.append(f'<h{level} id="{bid}">{numbered}<span data-source-id="{bid}">{inline(b,rels)}</span></h{level}>')
                        headings.append((bid,prefix+txt.strip()))
                    elif islist:
                        if not inlist:article.append("<ul>");inlist=True
                        article.append(f'<li id="{bid}" data-source-id="{bid}">{inline(b,rels)}</li>')
                    else:
                        caption=txt.strip().startswith("Figure")
                        code=i in plan.get("code_blocks",[1378,1387,1388,1389,1390,1397,1420,1421,*range(1426,1438),*range(1446,1453)])
                        tag="pre" if code else "p"
                        cls=' class="caption"' if caption else ""
                        content=inline(b,rels)
                        for phrase,target in plan.get("internal_links",[("Appendix A","#b1349"),("Appendix B","#b1380"),("appendix D","results.html#b1504")]):
                            if phrase in content:content=content.replace(phrase,f'<a href="{target}">{phrase}</a>')
                        article.append(f'<{tag} id="{bid}" data-source-id="{bid}"{cls}>{content}</{tag}>')
                for m in b.xpath(".//m:oMath",namespaces=NS):
                    article.append(f'<div class="formula" data-source-math="{bid}"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block">{mathml(m)}</math></div>')
                imgs=b.xpath(".//a:blip/@r:embed",namespaces=NS)
                for rid in imgs:
                    name=Path(rels[rid]).name
                    raw=z.read("word/"+rels[rid]);ext=Path(name).suffix
                    assets[name]={"source_sha256":sha(raw),"source_block":i}
                    if not args.verify_only:
                        dest=SITE/"assets/figures"/name;dest.parent.mkdir(parents=True,exist_ok=True)
                        dest.write_bytes(clean_image(raw,ext))
                    assets[name]["public_sha256"]=sha((SITE/"assets/figures"/name).read_bytes())
                    later=[text_of(blocks[j]).strip() for j in range(i,min(i+22,len(blocks))) if text_of(blocks[j]).strip().startswith("Figure")]
                    alt=later[0] if later else locations[i]+" — original report figure"
                    article.append(figure(name,alt))
                for chart in b.xpath(".//c:chart",namespaces=NS):
                    rid=chart.get("{"+NS["r"]+"}id");name=Path(rels[rid]).stem+".png"
                    if not (SITE/"assets/figures"/name).is_file():raise SystemExit("Extract original chart first: "+name)
                    article.append(figure(name,locations[i]+" — original report chart"))
                    assets[name]={"source_block":i,"source_chart_sha256":sha(z.read("word/"+rels[rid])),"public_sha256":sha((SITE/"assets/figures"/name).read_bytes())}
            if inlist:article.append("</ul>")
            notice=""
            if slug=="references":notice='<aside class="notice">The latest supplied report contains six bibliography entries, reproduced below. Some in-text citations still have no corresponding bibliography entry in the source report.</aside>'
            if not args.verify_only:section_page(slug,titles[slug],"".join(article),headings,notice)
            rendered=html.fromstring((SITE/"content"/(slug+".html")).read_text())
            actual={e.get("data-source-id"):norm(e.text_content()) for e in rendered.xpath("//*[@data-source-id]")}
            if actual!=expected:
                missing=[k for k in expected if k not in actual]
                extra=[k for k in actual if k not in expected]
                changed=[k for k in expected if k in actual and expected[k]!=actual[k]]
                raise SystemExit(f"CONTENT MISMATCH {slug}: missing={missing}, extra={extra}, changed={changed}")
            # Compare every original equation's textual tokens as well as its structural representation.
            for i in ids:
                for m in blocks[i].xpath(".//m:oMath",namespaces=NS):
                    target=rendered.xpath(f'//*[@data-source-math="b{i:04d}"]')
                    original="".join(m.xpath(".//m:t/text()",namespaces=NS))
                    if len(target)!=1 or target[0].text_content()!=original:raise SystemExit(f"MATH MISMATCH b{i:04d}")
            verifications.append({"page":slug,"matched_blocks":len(expected),"status":"PASS"})
        audit={"source_sha256":sha(data),"comparison":"Per-block exact text after documented privacy replacements; layout whitespace normalized. Equations compared separately.","pages":verifications,"blocks":record,"assets":assets}
        (args.audit/"content-audit.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2))
        lines=["# Report-to-website content mapping","","Source locations use zero-based body child indices in word/document.xml; they remain stable for the recorded source hash.","","All displayed text is copied unchanged except the explicitly marked privacy substitutions. Empty layout paragraphs and the unused OOXML compatibility fallback are presentation only.","","| Website | Original heading | Source block | Unchanged | Reason |","|---|---|---:|---|---|"]
        lines += [f'| {r["website_section"]} | {r["source_heading"]} | {r["source_block"]} | {"Yes" if r["copied_unchanged"] else "No"} | {r["reason"] or ""} |' for r in record]
        lines+=["","## Intentional exclusions",""]+["- "+x for x in plan["exclusions"]]
        (args.audit/"CONTENT_MAPPING.md").write_text("\n".join(lines))
        print(json.dumps({"status":"PASS","pages":verifications,"assets":len(assets),"privacy_modified_blocks":sum(not r["copied_unchanged"] for r in record)},indent=2))
    if not args.verify_only:build_shell()
if __name__=="__main__":main()
