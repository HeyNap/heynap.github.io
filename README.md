# heynap.app

The HeyNap website, served by GitHub Pages from this repo (`main`, root) at
https://heynap.app. Plain HTML and one stylesheet; no build step. GitHub Pages
runs Jekyll over it, which copies the pages as they are (`_config.yml` only adds
`.well-known` and leaves out `tools/` and the docs).

Setting up the domain, GitHub, the stores and the search consoles: [SETUP.md](SETUP.md).

## What's here

| Path | What |
|---|---|
| `index.html` | The home page: value, three screenshots, questions, store badges |
| `support/` | Contact, subscriptions, download and delete data (Google Play's deletion URL is `/support/#delete`) |
| `privacy/`, `terms/` | The legal pages (written for accounts and sync already) |
| `404.html` | Not found |
| `assets/site.css` | All styles (the app's Slate palette) |
| `assets/fonts/` | Quicksand and Lato, subset to Latin + Latin Extended (Romanian and most European languages), WOFF2, self-hosted (no Google Fonts requests) |
| `assets/img/` | Icons, screenshots (WebP 1× and 2×, PNG fallback), store badges, social cards |
| `robots.txt`, `sitemap.xml`, `llms.txt` | For search engines and AI assistants |
| `site.webmanifest` | Icons, and `related_applications` for Android's install prompt |
| `.well-known/` | `apple-app-site-association` (universal links, password autofill), `assetlinks.json` (Android app links), `security.txt` |
| `CNAME` | The custom domain |
| `tools/` | Not published: the icon and social card sources and the asset build |

## Placeholders to fill

- `APP_STORE_ID` (in `index.html` twice, `site.webmanifest`, `llms.txt`): the App Store's
  numeric app id. Also uncomment the `apple-itunes-app` meta in `index.html`.
- `REPLACE_WITH_PLAY_APP_SIGNING_SHA256` in `.well-known/assetlinks.json`.

## Rebuilding the images

```bash
tools/build-assets.sh
```

It renders the icon from the Icon Composer layers (`tools/icon-layers/`, copied from
`../appicon/icon-composer.icon`) in Chrome for Testing, the social cards from
`tools/og.html`, and compresses the screenshots in `tools/screens/` (780 × 1768,
captured from the app's harness with `naplog_preview/review/capture.py`, palette
Slate (`palette=slate`): `app tab=today now=2026-09-19T10:15`, `log log=addmore`,
`app tab=stats now=2026-09-19T20:30`). Needs `node`, `cwebp`, `pngquant`, `oxipng`.

## Adding a language

Each language gets its own folder with the same pages (`/ro/`, `/ro/privacy/`, …),
English stays at the root. For each page, in every language:

1. `<html lang="ro">`, and `og:locale` (`ro_RO`).
2. One `<link rel="alternate" hreflang="…">` per language plus `x-default` (the
   English page), the same set on every version of the page.
3. The same alternates as `xhtml:link` entries in `sitemap.xml`, and a `<url>` per
   language page.
4. The store badges in that language (Apple's and Google's badge pages have each
   locale) and the screenshots captured in it.
5. A language link in the footer.

With more than a handful of pages, move the shared header, footer and head into
Jekyll includes; GitHub Pages already builds with Jekyll.
