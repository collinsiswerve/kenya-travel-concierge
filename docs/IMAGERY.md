# Photorealistic brand imagery

Updated 23 October 2026. The existing page layout, typography, logo, service copy and enquiry flows are retained.

## Direction and provenance

Twelve original images were created using OpenAI's built-in image-generation tool, one standalone asset per prompt. The direction is natural-light luxury editorial photography in Kenya-inspired settings: discreet service, lush greenery, linen, timber and natural stone. These AI-generated illustrations do not document actual KTC staff, clients, vehicles, venues or properties. No Tully photographs, code, copy, awards or endorsements were reused.

The complete prompt set is saved in [data/imagery-prompts.json](../data/imagery-prompts.json). Image alternatives, source dimensions, focal positions and output sizes are in [data/imagery.json](../data/imagery.json). Masters are high-quality JPEG exports from the generated originals. The older supplied screenshots and savannah source are retained for history.

## Asset map

Paths below are relative to the repository root. All rendered AVIF files have WebP fallbacks. Supporting images also have a 640px version; larger outputs are 1280px wide (1024px for the portrait). The homepage hero uses its full generated 1672px width without artificial enlargement. Public assets are mirrored in dist/assets/images/ for the retained build.

| Image | Saved master | Largest preferred public image | Source dimensions |
| --- | --- | --- | --- |
| kenya-luxury-hero | `data/image-masters/kenya-luxury-hero.jpg` | `assets/images/kenya-luxury-hero-1672.avif` | 1672 × 941 |
| airport-welcome | `data/image-masters/airport-welcome.jpg` | `assets/images/airport-welcome-1280.avif` | 1536 × 1024 |
| private-chauffeur | `data/image-masters/private-chauffeur.jpg` | `assets/images/private-chauffeur-1280.avif` | 1536 × 1024 |
| executive-concierge | `data/image-masters/executive-concierge.jpg` | `assets/images/executive-concierge-1280.avif` | 1536 × 1024 |
| lifestyle-concierge | `data/image-masters/lifestyle-concierge.jpg` | `assets/images/lifestyle-concierge-1280.avif` | 1536 × 1024 |
| relocation-home | `data/image-masters/relocation-home.jpg` | `assets/images/relocation-home-1280.avif` | 1536 × 1024 |
| consultation-planning | `data/image-masters/consultation-planning.jpg` | `assets/images/consultation-planning-1280.avif` | 1536 × 1024 |
| property-stewardship | `data/image-masters/property-stewardship.jpg` | `assets/images/property-stewardship-1280.avif` | 1536 × 1024 |
| construction-oversight | `data/image-masters/construction-oversight.jpg` | `assets/images/construction-oversight-1280.avif` | 1536 × 1024 |
| trusted-representation | `data/image-masters/trusted-representation.jpg` | `assets/images/trusted-representation-1280.avif` | 1536 × 1024 |
| procurement-coordination | `data/image-masters/procurement-coordination.jpg` | `assets/images/procurement-coordination-1280.avif` | 1536 × 1024 |
| personal-concierge | `data/image-masters/personal-concierge.jpg` | `assets/images/personal-concierge-1024.avif` | 1024 × 1536 |

The homepage categories use airport-welcome, lifestyle-concierge and property-stewardship. About uses personal-concierge. Each service uses its corresponding distinct image.

## Loading and regeneration

The hero is preloaded with high fetch priority. Service-page lead images load eagerly; supporting homepage imagery loads lazily. Responsive candidates and intrinsic dimensions preserve the established image boxes and avoid downloading the largest supporting file unnecessarily. The new social preview is assets/images/kenya-luxury-social.jpg (1200 × 675).

With Pillow installed, run:

    python3 scripts/optimize_assets.py --images-only
    python3 scripts/build.py
    npm run check

Normal HTML rebuilding and hosting do not require Pillow. To regenerate the unchanged fonts too, omit --images-only and install fonttools and brotli.

The image collection is validated for source availability, portable responsive paths, dimensions in markup, alternatives, loading priority and individual AVIF/WebP byte budgets. Browser review covered the homepage hero, category imagery, About portrait and wide and tighter service crops. Desktop preview showed loaded images and fonts without horizontal overflow. Previous PageSpeed scores in SEO_READINESS.md predate this imagery refresh unless a newer result is explicitly recorded.
