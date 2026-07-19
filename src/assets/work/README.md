# Case-study cover images

Drop cover images for `/work/[slug]` pages in this folder.

## How to add one

1. Save the image here, named after the case study, e.g. `bet-tracker.webp`.
2. In the matching file in `src/content/work/`, add two frontmatter fields:

```yaml
cover: ../../assets/work/bet-tracker.webp
coverAlt: "theScore matchup page showing a live bet trending against game state"
```

The path is relative to the `.md` file, not to the project root.

**`coverAlt` is required whenever `cover` is set** — the build fails without it.
That is deliberate. An image with no alt text is invisible to screen readers and
to anyone whose image does not load, and a failed build is a better reminder
than never noticing. Describe what the image *shows*, not what the project
achieved (the headline already does that).

## Specs

| | |
|---|---|
| Width | 1200–1600px |
| Aspect ratio | keep it **the same across all studies** (3:2 or 16:10) |
| Format | WebP preferred, PNG fine — Astro converts and resizes either way |
| File size | no hard limit; Astro optimizes on build |

Consistent aspect ratio matters more than resolution. Mixed ratios make the
pages look accidental even when each image is good on its own.

Astro's `<Image>` handles optimization, responsive sizes, and width/height
attributes (which stop the page jumping around as images load). Do not
pre-optimize beyond exporting at a sane size.

## What is safe to publish

Safe:
- App Store / Google Play screenshots (published marketing assets)
- Press coverage and official announcements
- Your own screenshots of the publicly released app, with **no real user data
  and no account balances**, including your own

Not safe:
- Internal Figma, roadmaps, analytics dashboards, internal tooling
- Unreleased or unshipped designs
- Anything showing another person's data

The bar is higher here than for most portfolios: these were regulated,
real-money products. When unsure, leave it out — the writing carries the
studies already.

Note on brands: Barstool Sportsbook and ESPN Bet marks illustrate factual work
history, which is normally fine, but heavy brand imagery on a personal site can
read as implied endorsement. Prefer product screenshots over logos.
