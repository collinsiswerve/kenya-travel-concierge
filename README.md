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

The ready-to-host website is in `dist/`. Serve that directory with any static web server. For example:

```sh
python3 -m http.server 8080 --directory dist
```

Edit service descriptions and inclusions in `data/services.json`. Shared page templates and general copy are in `scripts/build.py`; styles and interactions are in `dist/assets/styles.css` and `dist/assets/app.js`.

Regenerate the HTML and check links:

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check dist/assets/app.js
```

Python 3.10+ is needed only for regeneration. Node is used only for the optional JavaScript syntax check. The published site needs neither.

## Hosting

Deploy `dist/` as the static document root. Routes use root-relative links and work on a domain or subdomain. Configure the host to use `404.html` for missing routes. Set `SITE_URL=https://your-domain.example` when rebuilding to update canonical and social URLs and the sitemap.

For GitHub Pages, use a custom domain or a user-site repository to preserve root-relative routes. The complete website is committed, so static hosting does not require a build step.

The `.openai/hosting.json` file holds the connected Sites project identity. Preserve it when updating this specific Site. A separate deployment on another host does not need that file.

## Enquiries

The form prepares a message locally and opens WhatsApp or the visitor's email app. It does not silently send messages or store requests in a site database. Visitors review and send their message themselves. Phone: +254 717 762323. Email: info.kenyatravelconcierge@gmail.com.

## Assets

The logo and supporting brand imagery come from the owner's supplied WhatsApp catalogue screenshots. The original screenshot files remain unchanged; CSS presents only the relevant logo or image region. The photographs within the supplied brand artwork are used as promotional illustrations, not as verified staff or property photographs.

The savannah hero is an original AI-generated illustrative brand image, created with the built-in image-generation tool. The generation brief is in `data/hero-prompt.txt`. It is not a photograph of a named property or a specific offered itinerary.

Cormorant Garamond and Manrope are self-hosted Google Fonts. Their SIL Open Font License notices are included in `dist/assets/`. The reference website informed the spacious editorial presentation; its code, photographs, copy, awards, and testimonials have not been copied.

## Ownership

Brand content and supplied imagery remain subject to their respective owners' rights. This repository is intended for Kenya Travel Concierge's website. No broad open-source licence is asserted over the brand or supplied images.
