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
| `support/` | Contact, subscriptions, restoring purchases, deleting data (`/support/#delete`) |
| `privacy/`, `terms/` | The legal pages, for the app as it is: offline, no accounts, Firebase and Amplitude for usage data and crash reports. Accounts or sync need them updated first (the 26 Oct accounts-ready versions are in git: `a643f52`) |
| `404.html` | Not found |
| `assets/site.css` | All styles (the app's Slate palette) |
| `assets/lang.js` | The footer's language picker: the one list of languages |
| `ro/`, … | The home page per App Store locale (see Adding a language) |
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
captured from the app's harness with `heynap/review/capture.py`, palette
Slate (`palette=slate`): `app tab=today now=2026-09-19T10:15`, `log log=addmore`,
`app tab=stats now=2026-09-19T20:30`). Needs `node`, `cwebp`, `pngquant`, `oxipng`.

## Adding a language

One folder per App Store locale (`storeLocales` in the app's
`lib/harness/store_shots.dart`), named by its id: `/ro/`, `/en-GB/`, … en-US stays at
the root. For each locale's home page:

1. Copy `ro/index.html`, translate it, and set `<html lang>`, `og:locale` and the
   canonical and `og:url`.
2. Screenshots: the first three of `../heynap/fastlane/ios/screenshots/<locale>/`
   (`1_iphone_ring`, `2_iphone_remind`, `3_iphone_add`) into `assets/img/store/<locale>/`
   as WebP at 300 and 600 wide (`cwebp -q 70`) and a 300-wide JPEG fallback (`sips`,
   quality 70); about 10–26 KB per WebP. No captions under them: each image's alt is
   its `storeCopy` headline and sub-line, taken from `store_shots.dart`, never read off
   the image.
3. The App Store badge in that language, from Apple's badge tool
   (`https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/<lang-region>?size=250x83`),
   as `assets/img/badge-app-store-<locale>.svg`, with Apple's own wording as its alt.
4. One `<link rel="alternate" hreflang="…">` per language plus `x-default` (the
   English page), the same set on every version of the page, and the same in
   `sitemap.xml` (`xhtml:link`, plus a `<url>` for the new page).
5. One line in `assets/lang.js`: the footer's language picker reads that list on every
   page (the pages carry only a fallback link to English).

The support, privacy and terms pages stay English for now.

With more than a handful of pages, move the shared header, footer and head into
Jekyll includes; GitHub Pages already builds with Jekyll.
