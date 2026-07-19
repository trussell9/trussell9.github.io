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
		z.object({
			title: z.string(),
			label: z.string().optional(),          // short card label; falls back to title
			summary: z.string(),
			role: z.string(),
			timeframe: z.string(),
			team: z.string(),
			skills: z.array(z.string()),
			featured: z.boolean().default(false), // true = shown on the home page
			order: z.number(),                     // sort order (low = first)
			cover: image().optional(),             // omit until you have a screenshot
			links: z
				.array(z.object({ label: z.string(), url: z.string().url() }))
				.default([]),
		}),
});

export const collections = { work };
