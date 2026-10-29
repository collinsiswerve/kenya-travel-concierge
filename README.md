# Kenya Travel Concierge

I use this repository to manage the Kenya Travel Concierge website. It is where people can find out what we offer, get in touch and arrange support in Kenya, whether they are visiting, relocating or handling things from abroad.

**[Visit the website](https://collinsiswerve.github.io/kenya-travel-concierge/)**

![Kenya Travel Concierge homepage](docs/website-preview.jpg)

## What is on the site

The site covers our ten services, from airport welcomes and chauffeur arrangements to relocation, property care and everyday errands. Each service has its own page with a short explanation and a way to enquire.

Visitors can prepare a WhatsApp or email message on the contact page. They review and send it themselves; the website does not store enquiries in a database or take payments online.

Our [Privacy Policy](https://collinsiswerve.github.io/kenya-travel-concierge/privacy/) and [Terms & Conditions](https://collinsiswerve.github.io/kenya-travel-concierge/terms/) are linked at the bottom of every page.

## Find us online

- [Instagram](https://www.instagram.com/kenyatravelconcierge/)
- [TikTok](https://www.tiktok.com/@kenyatravelconcie)
- [Facebook](https://www.facebook.com/share/1DoAB8zH6i/)

For enquiries, call **+254 717 762323** or email **info.kenyatravelconcierge@gmail.com**.

## Making changes

The site uses HTML, CSS and JavaScript, with a small Python script to keep the shared parts of the pages consistent. There is no framework or database to set up.

I keep the editable content in these files:

| What needs changing | Where to edit |
| --- | --- |
| Service descriptions and inclusions | `data/services.json` |
| Business metadata, social links and website address | `data/site.json` |
| Privacy policy and terms | `data/legal.json` |
| Shared layout, displayed contact details and general page copy | `scripts/build.py` |
| Colours, spacing and responsive styles | `dist/assets/styles.css` |
| Menus, service filters and enquiry form behaviour | `dist/assets/app.js` |

After editing, rebuild the pages and run the checks:

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 scripts/check_seo.py
node --check assets/app.js
```

The build updates both `dist/` and the public files at the top of the repository. Include both copies when committing a change so the next rebuild keeps the website in sync. Python 3.10 or newer is needed for rebuilding; Node is only needed for the JavaScript check.

To preview the site locally, run this from the repository folder and open `http://localhost:8080/`:

```sh
python3 -m http.server 8080
```

## Publishing

GitHub Pages publishes the files from **main → /(root)**. The homepage is the top-level `index.html`, and `.nojekyll` keeps publishing straightforward. After a change is committed to `main`, the deployment status appears in the repository’s **Actions** tab.

If the website address changes, update `data/site.json` and rebuild so the sitemap and page addresses match. More publishing notes are in [UPLOAD_GUIDE.txt](UPLOAD_GUIDE.txt).

## Images and fonts

The image sources and their notes are kept in `data/` and [docs/IMAGERY.md](docs/IMAGERY.md). The images are brand illustrations, rather than photographs documenting our actual team, clients or bookings. Public pages use smaller AVIF and WebP versions to keep loading times down.

The site uses Cormorant Garamond and Manrope. Their font licences are included with the assets. KTC branding and other content remain subject to their respective owners’ rights; this repository does not grant a general licence to reuse them.
