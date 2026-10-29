# heynap.app

The HeyNap website, served by GitHub Pages from this repo (`main`, root) at
https://heynap.app. Plain HTML and one stylesheet; no build step. GitHub Pages
runs Jekyll over it, which copies the pages as they are (`_config.yml` only adds
`.well-known` and leaves out `tools/` and the docs).

Setting up the domain, GitHub, the stores and the search consoles: [SETUP.md](SETUP.md).

## What's here

| Path | What |
|---|---|
| `index.html` | The home page (en-US): value, three store screenshots, questions, store badges |
| `support/` | Contact, subscriptions, restoring purchases, deleting data (`/support/#delete`) |
| `privacy/`, `terms/` | The legal pages, for the app as it is: offline, no accounts, Firebase and Amplitude for usage data and crash reports. Accounts or sync need them updated first (the 26 Oct accounts-ready versions are in git: `a643f52`) |
| `404.html` | Not found |
| `assets/site.css` | All styles (the app's Slate palette) |
| `assets/lang.js` | Closes the footer's language picker on a click elsewhere |
| `ro/`, `en-GB/`, … | The home page per App Store locale (see below) |
| `assets/fonts/` | Quicksand and Lato, subset to Latin + Latin Extended (Romanian and most European languages), WOFF2, self-hosted (no Google Fonts requests) |
| `assets/img/` | Icons, store screenshots per locale (`store/`), App Store badges per language, social cards |
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
`tools/og.html` (which uses `tools/screens/next-nap.png`; the screens there are 780 × 1768,
captured from the app's harness with `heynap/review/capture.py`, palette
Slate (`palette=slate`): `app tab=today now=2026-09-19T10:15`, `log log=addmore`,
`app tab=stats now=2026-09-19T20:30`). Needs `node`, `cwebp`, `pngquant`, `oxipng`.

## The home page per locale

One home page per App Store locale (`storeLocales` in the app's
`lib/harness/store_shots.dart`): en-US at the root, every other locale in a folder named
by its id (`/ro/`, `/en-GB/`, `/zh-Hant/`, …). They are all written by

```bash
python3 tools/build-locales.py
```

from `tools/site-i18n/<locale>.json` (the page's words; edit those, never the pages) and
`tools/site-i18n/_store.json` (each screenshot's alt text: its `storeCopy` headline and
sub-line, never read off the image). It also writes the footer's language picker into
every page, the hreflang links, and the home pages' entries in `sitemap.xml`.

- **The screenshots:** the first three of `../heynap/fastlane/ios/screenshots/<locale>/`
  (`1_iphone_ring`, `2_iphone_remind`, `3_iphone_add`) as WebP in
  `assets/img/store/<locale>/`: `<n>.webp` 300 wide (`cwebp -q 72`) and `<n>@2x.webp`
  600 wide (`cwebp -q 70`), resized with `sips -Z 650` / `-Z 1300`. Redo them after
  `review/store_export.py` changes the PNGs.
- **`_store.json`:** after `storeCopy` changes, re-export it with a throwaway Dart file in
  the app's `tool/` that prints `storeLine(locale, id)` for `ring`, `remind` and `add`
  of every `storeLocales` entry.
- **The badges:** `assets/img/badge-app-store-<locale>.svg` from Apple's badge tool
  (`https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/<lang-region>?size=250x83`,
  e.g. `ro-ro`, `nb-no`, `zh-tw`); English locales share `badge-app-store.svg`, fr-CA
  uses fr-FR's. Their alt text, Apple's wording, is `BADGE_ALT` in the script.
- **A new locale:** its entry in `LOCALES` (the script), its JSON, its screenshots and
  badge, then run the script.

The support, privacy and terms pages stay English for now.

With more than a handful of pages, move the shared header, footer and head into
Jekyll includes; GitHub Pages already builds with Jekyll.
