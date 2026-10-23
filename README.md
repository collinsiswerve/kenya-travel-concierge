# Kenya Travel Concierge

A premium, responsive static website for Kenya Travel Concierge. Built with HTML, CSS, and vanilla JavaScript; no runtime framework or database required.

![KTC homepage preview](docs/website-preview.jpg)

## Website

- Homepage with original Kenyan landscape imagery and the supplied KTC identity.
- Service catalogue with three category filters and ten dedicated service pages.
- Visitor journeys for guests, people relocating, and Kenyans abroad.
- WhatsApp and email enquiry preparation, including service selection and browser validation.
- Mobile navigation, keyboard-accessible tabs, FAQ disclosures, reduced-motion support, metadata, sitemap, and privacy information.

## Run and edit

The ready-to-upload website starts at `index.html` in this folder. A parallel built copy remains in `dist/`. Serve the project folder to preview it. For example:

```sh
python3 -m http.server 8080
```

Edit service descriptions and inclusions in `data/services.json`. Shared page templates and general copy are in `scripts/build.py`; styles and interactions are in `dist/assets/styles.css` and `dist/assets/app.js`. Rebuilding also copies the updated website and assets to the project root for GitHub Pages.

Regenerate the HTML and check links:

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 scripts/check_seo.py
node --check dist/assets/app.js
```

Python 3.10+ is needed only for regeneration. Node is used only for the optional JavaScript syntax check. The published site needs neither.

## Hosting on GitHub Pages

This export is prepared for `collinsiswerve/kenya-travel-concierge`.

1. Extract the ZIP and upload all extracted files and folders directly into the repository on `main`. The repository must show `index.html` next to `README.md`, not inside an extra outer folder.
2. Open **Settings > Pages**.
3. Set **Source: Deploy from a branch**, **Branch: main**, and **Folder: /(root)**. Save if the settings changed.
4. After the Pages deployment succeeds, open **Visit site** or `https://collinsiswerve.github.io/kenya-travel-concierge/`.

See `UPLOAD_GUIDE.txt` for the complete browser upload steps. No custom Actions workflow or build command is required on GitHub. The included `.nojekyll` file selects static publishing. Navigation, stylesheets and font URLs support the GitHub project address; canonical and sitemap URLs use that address as well.

If publishing at a different URL, set `SITE_URL` to its complete public base URL when rebuilding. The `404.html` navigation uses this base URL so it also works at missing nested routes.

The `.openai/hosting.json` file retains the original connected Sites project identity and still points to `dist/`. Preserve it when updating that Site. GitHub Pages serves the ready copy at the repository root.

## Search visibility and performance

See [SEO readiness and launch plan](docs/SEO_READINESS.md) for implemented checks and the remaining Google account steps. Business details, the canonical base URL and an optional Search Console verification value are in `data/site.json`. The hero and service imagery use optimized AVIF with responsive WebP fallbacks and all active font URLs use WOFF2; the source assets and licences are retained. `scripts/optimize_assets.py --images-only` regenerates the optimized imagery using Pillow; omit the flag to also regenerate WOFF2 fonts using fonttools and brotli. HTML rebuilding and hosting require no extra packages.

## Enquiries

The form prepares a message locally and opens WhatsApp or the visitor's email app. It does not silently send messages or store requests in a site database. Visitors review and send their message themselves. Phone: +254 717 762323. Email: info.kenyatravelconcierge@gmail.com.

## Assets

The supplied KTC logo is retained. Twelve original photorealistic AI-generated brand images now cover the homepage hero, About section and all ten services. They are illustrative scenes, not photographs of actual KTC staff, clients, properties, vehicles or named venues. Tully Luxury Travel informed the photographic direction; none of its imagery was copied.

High-quality JPEG masters are in `data/image-masters/`. The full generation prompts, built-in tool provenance, descriptive alternatives and image dimensions are retained in `data/imagery-prompts.json` and `data/imagery.json`. See [imagery notes](docs/IMAGERY.md) for the asset map. Public pages load AVIF with responsive WebP fallbacks from `assets/images/`, mirrored in `dist/assets/images/`. Original supplied screenshots and the earlier savannah illustration remain as historical source material and are not used for service imagery.

Cormorant Garamond and Manrope are self-hosted Google Fonts. Their SIL Open Font License notices are included in `dist/assets/`. The reference website informed the spacious editorial presentation; its code, photographs, copy, awards, and testimonials have not been copied.

## Ownership

Brand content and supplied imagery remain subject to their respective owners' rights. This repository is intended for Kenya Travel Concierge's website. No broad open-source licence is asserted over the brand or supplied images.
