// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // Emits sitemap-index.xml + sitemap-0.xml at build time, listing every static
  // page. public/robots.txt points crawlers at it.
  integrations: [sitemap()],

  // `site` is your production URL. Astro uses it to build absolute URLs
  // (canonical links, Open Graph tags, sitemaps). For a `username.github.io`
  // root repo, this is exactly the Pages URL — no `base` path needed.
  site: 'https://trussell9.github.io',
});
