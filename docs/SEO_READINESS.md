# SEO readiness and launch plan

Updated 23 October 2026 for Kenya Travel Concierge.

The public site is already live at:
https://collinsiswerve.github.io/kenya-travel-concierge/

## Implemented

- Crawlable HTML for the homepage, services catalogue, ten service pages, contact and privacy.
- Unique search titles and descriptions, absolute canonical URLs, and a matching 14-page XML sitemap.
- Service titles describe the service and Kenya; the visible page design and service content are retained.
- Organization and WebSite structured data on the homepage; Service structured data on all ten service pages; breadcrumb data on service routes; a ContactPage for enquiries.
- Markup uses the existing name, phone, email, Instagram and Kenya service coverage. No address, reviews, ratings, awards or prices have been invented.
- Complete Open Graph and social image metadata with descriptive image text.
- The error page is marked noindex; published content pages remain indexable.
- Category and enquiry query parameters keep the clean page URL as canonical.
- The retained dist copy points to the same public canonical URLs. The sitemap lists the public root URLs.
- An AVIF hero with WebP fallback and early loading priority, lazy loading for supporting service images, and WOFF2 versions of the same nine fonts.
- Existing keyboard navigation, skip link, image alternatives, responsive CSS and deferred JavaScript retained.

### Measured asset sizes

| Asset | Before | After | Reduction |
| --- | ---: | ---: | ---: |
| Homepage hero, preferred | 2,590,686 bytes (PNG) | 168,005 bytes (AVIF) | 93.5% |
| Homepage hero, fallback | 2,590,686 bytes (PNG) | 319,504 bytes (WebP) | 87.7% |
| All nine font files | 1,837,460 bytes (TTF) | 444,780 bytes (WOFF2) | 75.8% |

These are asset byte reductions, not measured page-speed or ranking gains. A browser downloads the font weights it uses, not necessarily all nine. Font characters and horizontal metrics were compared after conversion. Original images and font files remain as editable sources; normal page loading references the optimized versions.

## Independent mobile audit

The first PageSpeed Insights run on 23 October 2026 reported SEO 100, Performance 83, Accessibility 97 and Best Practices 96. It used an emulated Moto G Power with slow 4G, and had no real-user field data. Its report is https://pagespeed.web.dev/analysis/https-collinsiswerve-github-io-kenya-travel-concierge/262511oxyp?form_factor=mobile.

The follow-up implementation removes the two render-blocking stylesheet requests by embedding the small shared CSS and font declarations, adds the AVIF variant, darkens muted text for legibility, and preserves supporting images' natural proportions. Font URLs inside embedded styles are checked for nested routes and the missing-page fallback. GitHub Pages controls response cache headers, so cache-lifetime findings may remain on this host. Scores are lab observations rather than ranking or field-performance guarantees.

### Final mobile lab check after the follow-up

PageSpeed Insights on 23 October 2026 at 16:07 (Africa/Nairobi), emulated Moto G Power and slow 4G:

| Category or metric | First run | Follow-up run |
| --- | ---: | ---: |
| Performance | 83 | 96 |
| Accessibility | 97 | 97 |
| Best Practices | 96 | 100 |
| SEO, basic automated checks | 100 | 100 |
| First Contentful Paint | 2.3 s | 0.8 s |
| Largest Contentful Paint | 4.2 s | 2.9 s |
| Total Blocking Time | 0 ms | 0 ms |
| Cumulative Layout Shift | 0.038 | 0.031 |

Report: https://pagespeed.web.dev/analysis/https-collinsiswerve-github-io-kenya-travel-concierge/ff0mjixb0n?form_factor=mobile

There was no field data. These are homepage lab measurements; they do not establish a field Core Web Vitals pass or a Google ranking. The remaining contrast flag is the faint, aria-hidden decorative KTC watermark. Readable body/footer text was darkened and the supporting-image aspect-ratio finding is resolved. A full manual accessibility review is not claimed.

## Next: permanent domain

Confirm the preferred domain and ownership before changing canonical URLs. A custom domain is useful for a consistent brand address; it does not guarantee higher rankings.

When ready, configure the domain and HTTPS in GitHub Pages and DNS, then change data/site.json > url to the public HTTPS base URL, rebuild and recheck. SITE_URL can override the configuration for a specific build. Keep old-to-new redirects where the hosting setup permits and update Google Search Console and business links.

## Next: Google Search Console

Ownership verification, sitemap submission and actual index status are still outstanding.

For the current GitHub project address:

1. Add a URL-prefix property for the complete public site address, including /kenya-travel-concierge/.
2. Choose HTML-tag verification in the Google account that will own the property.
3. Add only Google's verification tag content to google_site_verification in data/site.json. Rebuild and deploy; the homepage emits the verification meta tag only when configured.
4. Complete verification in Search Console.
5. Submit https://collinsiswerve.github.io/kenya-travel-concierge/sitemap.xml.
6. Inspect the homepage and priority service URLs. Check discovery, indexing and Google's selected canonical, then request indexing where appropriate.

The verification value is not supplied or invented in this repository. No Google account has been connected and no property is claimed verified.

A project-folder robots.txt is not the host-root robots.txt that Google reads. At this address Google looks at https://collinsiswerve.github.io/robots.txt, not /kenya-travel-concierge/robots.txt. The included file becomes effective when served at a domain root. Until then, do not rely on it to block URLs or advertise the sitemap; submit the sitemap directly through Search Console. Public pages use normal indexable HTML.

## Next: service and local search content

Confirm which customers and locations matter most before expanding the copy:

- International visitors and returning Kenyans: airport reception, chauffeur support and executive travel.
- Kenyans abroad: property care, construction monitoring and trusted representation.
- People moving to Kenya: relocation, settling in and practical local coordination.

Only add airports, towns, neighbourhoods and coverage claims that the business confirms. Build useful service information such as how enquiries work, what clients need to provide, inclusions and genuine answers to common questions. Use real project examples, photographs and customer feedback with permission. Do not create repetitive location pages or unsupported claims.

A Google Business Profile is appropriate only if the business meets Google's eligibility rules for a customer-facing location or in-person service-area work. Confirm the real name, service area, contact information and operating details before creating a profile or LocalBusiness schema.

## Measurement and remaining limits

- Deployment and source checks establish technical readiness, not Google indexing or a ranking promise.
- No Google Search Console property has been verified and no sitemap has been submitted from an account.
- Both mobile lab results are recorded above. A field Core Web Vitals pass is not claimed; no field data was available.
- Run PageSpeed Insights on the public homepage and a service page after deployment. Treat lab measurements separately from real-user field data.
- Review Search Console impressions, queries, clicks, indexed pages and mobile experience as data accumulates. Enquiry tracking can be added after its scope and privacy requirements are agreed; no analytics or marketing tags have been installed.
- A search results position and indexing date cannot be guaranteed.

## Maintaining these checks

- Business metadata and the future domain: data/site.json.
- Service content: data/services.json.
- Shared templates: scripts/build.py.
- Source styles, JavaScript and original assets: dist/assets/.

After normal edits:

    python3 scripts/build.py
    python3 scripts/check.py
    python3 scripts/check_seo.py
    node --check assets/app.js

Or use npm run check after building.

Optimized assets are committed and require no installation to host or rebuild the HTML. To regenerate them from the retained originals, use scripts/optimize_assets.py with Pillow, fonttools and brotli installed, then rebuild.

## Official references

- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/monitor-debug/search-console-start
- https://support.google.com/webmasters/answer/9008080
- https://developers.google.com/search/docs/appearance/structured-data/organization
- https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- https://developers.google.com/crawling/docs/robots-txt/create-robots-txt
- https://developers.google.com/search/docs/appearance/core-web-vitals
- https://support.google.com/business/answer/3038177
