# Local website review - 30 October 2026

Status: local validation complete. The owner initially requested a local report refresh and removal of Appendices A-D, then approved pushing the reviewed update to the existing GitHub website on 30 October 2026. This record describes validation before publication.

## Changes

- Updated the six research sections and bibliography from the supplied final PDF dated 30 October 2026. Its accompanying Word version was checked against the PDF before structured import.
- Removed Appendices A-D from Methodology, including all contents links, code, tables, equations and their exclusive dataset-structure image. Removed two obsolete unused report figure exports as well.
- Removed parenthetical pointers to A and B and standalone pointers to previously omitted photo, static-map and performance appendices.
- Preserved earlier exclusions of front matter, the Executive Summary, administrative Project Management material, schedules and report-only navigation.
- Retained the website numbering: Conclusion 5.0, Future Work 6.0 and Results Discussion 4.5.
- Replaced the workflow figure and correct-detection example with the revised report figures. All eight native chart sources remain identical.
- Expanded the bibliography to the final report's 18 entries and removed the obsolete six-entry notice.
- Remapped all 46 glossary source links to the revised report passages. Glossary definitions are unchanged.
- Updated public source hashes, maintenance guidance, source import checks and checksums. Original reports and private audit records remain outside the repository.

## Verification

- All 258 retained source blocks match the PDF after normalising layout whitespace and punctuation; two paragraphs contain intervening PDF chart labels, verified as insertions with no missing source text.
- A separate final verify-only import comparison passed for all seven report pages and their original equations after three website heading-number substitutions and two documented pointer removals.
- Static site validation passed: 13 HTML pages, ten homepage cards and 1,667 local references, with no errors.
- Browser review passed for Methodology contents, its final PDI section and navigation, Results numbering, the updated bibliography, and glossary search linking to the revised PDI passage.
- Desktop review used a 1280 x 900 browser viewport; the bibliography and glossary were also checked at 390 x 844 without horizontal page overflow. These were browser viewport checks, not a physical phone test.
- 2,655 protected website files remain byte-identical, including the interactive map, map assets and export, gallery cards and images, all three videos and posters, shared CSS/JavaScript, homepage, map and video wrappers, and the publication workflow.
- Both supplied report files retain their original hashes. The pre-publication Git HEAD was ae6ca29ff3d647cfd9f8d4464533c137a5a369f9.

## Local preview

Double-click Preview.command, or run python3 tools/preview.py from the repository. Only site/ is served, bound to this computer.
