// Content collections config (Astro Content Layer API, Astro 5+/7).
// Defines the `work` collection: one Markdown file per case study, all
// validated against the same schema so the frontmatter can't silently drift.
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const work = defineCollection({
	// `glob` loads every .md file under src/content/work/ into the collection.
	loader: glob({ pattern: '**/*.md', base: './src/content/work' }),

	// `schema` validates each file's frontmatter at build time. `image` is the
	// helper that makes `cover` image-ready: when you add a screenshot later,
	// set `cover: ./foo.png` (relative to the .md file) and Astro optimizes it.
	schema: ({ image }) =>
		z
			.object({
				title: z.string(),
				label: z.string().optional(),          // short card label; falls back to title
				summary: z.string(),
				hook: z.string().optional(),           // short card summary (~3 lines); falls back to summary
				role: z.string(),
				timeframe: z.string(),
				team: z.string(),
				skills: z.array(z.string()),
				featured: z.boolean().default(false), // true = shown on the home page
				order: z.number(),                     // sort order (low = first)
				// Shown at the top of the case-study page (not on the cards).
				// Put the file in src/assets/work/ and reference it relative to
				// this .md file, e.g. cover: ../../assets/work/bet-tracker.webp
				cover: image().optional(),
				coverAlt: z.string().optional(),       // required whenever cover is set
				links: z
					.array(z.object({ label: z.string(), url: z.string().url() }))
					.default([]),
			})
			// An image with no alt text is invisible to screen readers and to anyone
			// whose image fails to load. Failing the build is kinder than shipping it:
			// the mistake surfaces now rather than never.
			.refine((data) => !data.cover || Boolean(data.coverAlt), {
				message: 'coverAlt is required when cover is set — describe what the image shows.',
				path: ['coverAlt'],
			}),
});

// The `press` collection: one Markdown file per callout. Each is a short pull
// quote from a press release or news article. `quote` is the only required
// field; `outlet`/`url`/`date` are optional but recommended — a quote reads as
// unsourced without at least an outlet, so keep the fields present even when a
// given entry leaves them blank.
const press = defineCollection({
	loader: glob({ pattern: '**/*.md', base: './src/content/press' }),
	schema: z.object({
		quote: z.string(),                 // the callout itself
		outlet: z.string().optional(),     // publication or source, e.g. "The Verge"
		url: z.string().url().optional(),  // link to the original article (build-time validated)
		date: z.string().optional(),       // display date, e.g. "March 2023"
		order: z.number(),                 // sort order (low = first)
	}),
});

export const collections = { work, press };
