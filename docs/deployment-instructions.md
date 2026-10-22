# GitHub Pages deployment

Publication requires the project owner's explicit approval. Keep the source documents and the sibling private review folder outside Git. Confirm the privacy review and content checks before the first upload.

1. Create a repository under the intended GitHub account. Start private while reviewing. Use a stable repository name and keep it unchanged after a QR code is printed.
2. Upload or push the contents of this repository only. Never upload its parent project folder.
3. Before uploading, run python3 tools/check_site.py and inspect git status --short. Include site/, tools/, docs/, README.md, .gitignore, Preview.command and .github/workflows/pages.yml. Exclude all source reports, PowerPoint files, private audit files and local caches.
4. In repository Settings → Pages, select GitHub Actions as the source. GitHub Free supports Pages from public repositories; private repository Pages requires an eligible paid plan. Decide repository visibility explicitly before changing it.
5. After publication approval, run **Publish approved showcase** from the Actions tab on main, checking the publication approval input. The workflow deploys only site/.
6. Wait for a successful deployment. Use the exact HTTPS URL shown by the deployment. It normally follows https://OWNER.github.io/REPOSITORY/, but that pattern is not confirmation of a live URL.
7. Open that URL without signing in. Test all eight cards, each research page, figures, references, map layers and photo popups on desktop and a real phone.
8. Only after the permanent URL is confirmed, generate PNG and SVG QR assets pointing to the homepage. Test a printed proof with multiple phone cameras. No final QR is supplied before the URL is confirmed.

## Updates

Edit/import locally, run the checks, commit and push. Publishing remains a separate, explicit manual workflow run. Preserve the repository name and homepage URL.

The video can be stored at site/assets/video/project-demo.mp4. GitHub rejects ordinary Git files larger than 100 MiB; if the MP4 exceeds that limit, prepare an approved smaller encode or choose an approved direct video host. Do not put private footage in a public repository.

The current map HTML is about 30.6 MB and contains the original geographic data. The whole site is about 276 MB because full-resolution map photos are retained. The homepage and research text are lightweight; the map is requested only when its card is opened. Photo requests are made by the original popup code; verify mobile transfer performance with the final dataset. Confirm live mobile transfer performance after publication, including an uncached load.

## Official documentation

- [Custom Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- [Large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)

The website copy uses standard OpenStreetMap tiles because the original CARTO endpoint returned API-key-required tiles during browser testing. Keep visible attribution, normal browser caching and referrer headers; do not add bulk or offline tile downloads. See the [OSM tile usage policy](https://operations.osmfoundation.org/policies/tiles/).
