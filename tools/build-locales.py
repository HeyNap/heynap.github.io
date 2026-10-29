#!/usr/bin/env python3
"""Writes the home page for every App Store locale: en-US at the root
(index.html), every other locale in its own folder (/ro/, /en-GB/, …), and
the home page's entries in sitemap.xml.

The words: tools/site-i18n/<locale>.json (the page) and _store.json (the
screenshots' alt text: each one's storeCopy headline and sub-line, exported
from the app's lib/harness/store_shots.dart; see README). The screenshots:
assets/img/store/<locale>/; the badges: assets/img/badge-app-store-<locale>.svg.

Run from the repo root: python3 tools/build-locales.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
I18N = ROOT / 'tools/site-i18n'
SITE = 'https://heynap.app'

# id: (html lang, og:locale, the name in its own language, Google Play hl)
LOCALES = {
    'en-US': ('en-US', 'en_US', 'English (US)', 'en'),
    'en-GB': ('en-GB', 'en_GB', 'English (UK)', 'en-GB'),
    'en-AU': ('en-AU', 'en_AU', 'English (Australia)', 'en-AU'),
    'en-CA': ('en-CA', 'en_CA', 'English (Canada)', 'en-CA'),
    'es-MX': ('es-MX', 'es_MX', 'Español (México)', 'es-419'),
    'es-ES': ('es-ES', 'es_ES', 'Español (España)', 'es'),
    'de-DE': ('de-DE', 'de_DE', 'Deutsch', 'de'),
    'fr-FR': ('fr-FR', 'fr_FR', 'Français', 'fr'),
    'fr-CA': ('fr-CA', 'fr_CA', 'Français (Canada)', 'fr-CA'),
    'it': ('it', 'it_IT', 'Italiano', 'it'),
    'nl-NL': ('nl-NL', 'nl_NL', 'Nederlands', 'nl'),
    'pt-BR': ('pt-BR', 'pt_BR', 'Português (Brasil)', 'pt-BR'),
    'pt-PT': ('pt-PT', 'pt_PT', 'Português (Portugal)', 'pt-PT'),
    'da': ('da', 'da_DK', 'Dansk', 'da'),
    'no': ('nb', 'nb_NO', 'Norsk', 'no'),
    'sv': ('sv', 'sv_SE', 'Svenska', 'sv'),
    'fi': ('fi', 'fi_FI', 'Suomi', 'fi'),
    'pl': ('pl', 'pl_PL', 'Polski', 'pl'),
    'cs': ('cs', 'cs_CZ', 'Čeština', 'cs'),
    'sk': ('sk', 'sk_SK', 'Slovenčina', 'sk'),
    'hu': ('hu', 'hu_HU', 'Magyar', 'hu'),
    'ro': ('ro', 'ro_RO', 'Română', 'ro'),
    'hr': ('hr', 'hr_HR', 'Hrvatski', 'hr'),
    'el': ('el', 'el_GR', 'Ελληνικά', 'el'),
    'ru': ('ru', 'ru_RU', 'Русский', 'ru'),
    'th': ('th', 'th_TH', 'ไทย', 'th'),
    'ja': ('ja', 'ja_JP', '日本語', 'ja'),
    'ko': ('ko', 'ko_KR', '한국어', 'ko'),
    'zh-Hant': ('zh-Hant', 'zh_TW', '繁體中文', 'zh-TW'),
}

# Apple's badge wording, the badge's alt text.
BADGE_ALT = {
    'en': 'Download on the App Store', 'es-MX': 'Descárgalo en el App Store',
    'es-ES': 'Consíguelo en el App Store', 'de-DE': 'Laden im App Store',
    'fr': "Télécharger dans l'App Store", 'it': 'Scarica su App Store',
    'nl-NL': 'Download in de App Store', 'pt-BR': 'Baixar na App Store',
    'pt-PT': 'Descarregar na App Store', 'da': 'Hent i App Store',
    'no': 'Last ned fra App Store', 'sv': 'Hämta i App Store', 'fi': 'Lataa App Storesta',
    'pl': 'Pobierz w App Store', 'cs': 'Stáhnout v App Store', 'sk': 'Stiahnuť na App Store',
    'hu': 'Letölthető az App Store-ból', 'ro': 'Descărcați de pe App Store',
    'hr': 'Preuzmi u App Storeu', 'el': 'Λήψη στο App Store', 'ru': 'Загрузите в App Store',
    'th': 'ดาวน์โหลดได้ที่ App Store', 'ja': 'App Storeからダウンロード',
    'ko': 'App Store에서 다운로드 하기', 'zh-Hant': '從 App Store 下載',
}

SHOTS = ['1-ring', '2-remind', '3-add']
GLOBE = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 '
         '3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>')


def path(loc):
    return '/' if loc == 'en-US' else f'/{loc}/'


def badge(loc):
    """The badge's file, width and height at 52 pt tall."""
    f = 'badge-app-store.svg' if loc.startswith('en-') else (
        'badge-app-store-fr-FR.svg' if loc == 'fr-CA' else f'badge-app-store-{loc}.svg')
    head = (ROOT / 'assets/img' / f).read_text()[:2000]
    _, _, w, h = map(float, re.search(r'viewBox="([^"]+)"', head).group(1).split())
    return f, round(52 * w / h), 52


def badge_alt(loc):
    return BADGE_ALT.get(loc) or BADGE_ALT[loc[:2]]


def e(s):
    return html.escape(s, quote=False).replace('"', "&quot;")


def j(s):
    return json.dumps(s, ensure_ascii=False)


def page(loc, t, store, order):
    lang, og, name, hl = LOCALES[loc]
    url = SITE + path(loc)
    en = loc.startswith('en-')
    legal_lang = '' if en else ' hreflang="en"'
    b, bw, bh = badge(loc)
    alts = []
    for shot in ('ring', 'remind', 'add'):
        head, sub = store[loc][shot]
        alts.append(head if not sub else f'{head} {sub}')

    alternates = '\n'.join(
        f'  <link rel="alternate" hreflang="{l}" href="{SITE}{path(l)}">' for l in order
    ) + f'\n  <link rel="alternate" hreflang="x-default" href="{SITE}/">'
    og_alts = '\n'.join(
        f'  <meta property="og:locale:alternate" content="{LOCALES[l][1]}">' for l in order if l != loc)

    shots = '\n'.join(f'''        <li>
          <div class="shot">
            <picture>
              <source type="image/webp" srcset="/assets/img/store/{loc}/{n}.webp 300w, /assets/img/store/{loc}/{n}@2x.webp 600w" sizes="300px">
              <img src="/assets/img/store/{loc}/{n}.webp" width="300" height="650" alt="{e(a)}" loading="lazy">
            </picture>
          </div>
        </li>''' for n, a in zip(SHOTS, alts))

    current = ' aria-current="page"'
    picker = '\n'.join(
        f'          <li><a href="{path(l)}" hreflang="{l}" lang="{LOCALES[l][0]}"'
        f'{current if l == loc else ""}>{e(LOCALES[l][2])}</a></li>'
        for l in sorted(order, key=lambda l: LOCALES[l][2].casefold()))

    faq = ',\n'.join(
        f'          {{ "@type": "Question", "name": {j(t[f"q{i}"])}, "acceptedAnswer": '
        f'{{ "@type": "Answer", "text": {j(t[f"a{i}"])} }} }}' for i in range(1, 5))

    details = '\n'.join(f'''      <details>
        <summary>{e(t[f"q{i}"])}</summary>
        <p>{e(t[f"a{i}"])}</p>
      </details>''' for i in range(1, 5))

    page_node = (f'''      {{
        "@type": "WebSite",
        "@id": "{SITE}/#site",
        "url": "{SITE}/",
        "name": "HeyNap",
        "inLanguage": "en-US",
        "publisher": {{ "@id": "{SITE}/#org" }}
      }},''' if loc == 'en-US' else f'''      {{
        "@type": "WebPage",
        "@id": "{url}#page",
        "url": "{url}",
        "name": {j(t["title"])},
        "inLanguage": "{lang}",
        "isPartOf": {{ "@id": "{SITE}/#site" }}
      }},''')

    def stores(lazy):
        lz = ' loading="lazy"' if lazy else ''
        return f'''      <div class="stores">
        <a class="apple" href="https://apps.apple.com/app/idAPP_STORE_ID"><img src="/assets/img/{b}" width="{bw}" height="{bh}" alt="{e(badge_alt(loc))}"{lz}></a>
        <!-- Android launch: uncomment. -->
        <!-- <a class="play" href="https://play.google.com/store/apps/details?id=app.heynap.mobile&amp;hl={hl}"><img src="/assets/img/badge-google-play.png" width="175" height="52" alt="{e(t["play_alt"])}"{lz}></a> -->
      </div>'''

    return f'''<!doctype html>
<!-- Written by tools/build-locales.py from tools/site-i18n/{loc}.json: edit those, not this. -->
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(t["title"])}</title>
  <meta name="description" content="{e(t["description"])}">
  <link rel="canonical" href="{url}">
{alternates}
  <meta name="theme-color" content="#0E0F13">
  <meta name="color-scheme" content="dark">

  <!-- Smart App Banner (Safari on iPhone): uncomment with the App Store id. -->
  <!-- <meta name="apple-itunes-app" content="app-id=APP_STORE_ID"> -->

  <!-- Sharing -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="HeyNap">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{e(t["share_title"])}">
  <meta property="og:description" content="{e(t["share_description"])}">
  <meta property="og:image" content="{SITE}/assets/img/og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{e(t["share_image_alt"])}">
  <meta property="og:locale" content="{og}">
{og_alts}
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(t["share_title"])}">
  <meta name="twitter:description" content="{e(t["share_description"])}">
  <meta name="twitter:image" content="{SITE}/assets/img/og.png">
  <meta name="twitter:image:alt" content="{e(t["share_image_alt"])}">

  <!-- Icons and install -->
  <link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48">
  <link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">

  <link rel="preload" href="/assets/fonts/Quicksand-Bold.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/Lato-Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/site.css">
  <script src="/assets/lang.js" defer></script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Organization",
        "@id": "{SITE}/#org",
        "name": "HeyNap",
        "legalName": "Diaconu Mobile Apps SRL",
        "url": "{SITE}/",
        "logo": "{SITE}/assets/img/icon-512.png",
        "email": "postmuseapp+heynap@gmail.com",
        "taxID": "38455506",
        "identifier": "ROONRC.J22/3376/2017",
        "address": {{ "@type": "PostalAddress", "streetAddress": "B-dul Tudor Vladimirescu 45A", "addressLocality": "Iasi", "postalCode": "707401", "addressCountry": "RO" }}
      }},
{page_node}
      {{
        "@type": "MobileApplication",
        "name": "HeyNap",
        "inLanguage": "{lang}",
        "description": {j(t["app_description"])},
        "operatingSystem": "iOS",
        "applicationCategory": "HealthApplication",
        "image": "{SITE}/assets/img/icon-512.png",
        "screenshot": [
{(","+chr(10)).join(f'          "{SITE}/assets/img/store/{loc}/{n}@2x.webp"' for n in SHOTS)}
        ],
        "offers": {{ "@type": "Offer", "price": "0" }},
        "publisher": {{ "@id": "{SITE}/#org" }}
      }},
      {{
        "@type": "FAQPage",
        "inLanguage": "{lang}",
        "mainEntity": [
{faq}
        ]
      }}
    ]
  }}
  </script>
</head>
<body>
  <a class="skip" href="#main">{e(t["skip"])}</a>

  <header class="top">
    <div class="wrap">
      <a class="brand" href="{path(loc)}" aria-label="{e(t["home_label"])}">
        <img src="/assets/img/logo-128.png" width="40" height="40" alt="">HeyNap
      </a>
      <nav aria-label="Site"><a href="/support/"{legal_lang}>{e(t["support"])}</a></nav>
    </div>
  </header>

  <main id="main">
    <section class="hero wrap">
      <img class="icon" src="/assets/img/icon-192.png" srcset="/assets/img/icon-192.png 1x, /assets/img/icon-512.png 3x" width="112" height="112" alt="{e(t["icon_alt"])}">
      <h1>{e(t["h1"])}</h1>
      <p class="lede">{e(t["lede"])}</p>
{stores(False)}
    </section>

    <section class="wrap" aria-label="{e(t["screens_label"])}">
      <ul class="screens">
{shots}
      </ul>
    </section>

    <section class="faq wrap" aria-labelledby="faq">
      <h2 id="faq">{e(t["faq"])}</h2>
{details}
    </section>

    <section class="cta wrap" aria-labelledby="get">
      <h2 id="get">{e(t["get"])}</h2>
      <p>{e(t["get_text"])}</p>
{stores(True)}
      <p class="note">{e(t["note"])}</p>
    </section>
  </main>

  <footer class="foot">
    <div class="wrap">
      <nav aria-label="{e(t["footer_label"])}">
        <a href="/support/"{legal_lang}>{e(t["support"])}</a>
        <a href="/privacy/"{legal_lang}>{e(t["privacy"])}</a>
        <a href="/terms/"{legal_lang}>{e(t["terms"])}</a>
        <a href="mailto:postmuseapp+heynap@gmail.com">postmuseapp+heynap@gmail.com</a>
      </nav>
      <span>© 2026 Diaconu Mobile Apps SRL · CUI 38455506 · J22/3376/2017</span>
      <details class="lang">
        <summary aria-label="{e(t["language_label"])}: {e(name)}">{GLOBE}{e(name)}</summary>
        <ul>
{picker}
        </ul>
      </details>
    </div>
  </footer>
</body>
</html>
'''


def sitemap(order, lastmod):
    """The home page's <url> per locale, in place of whatever home entries were there."""
    f = ROOT / 'sitemap.xml'
    s = f.read_text()
    links = '\n'.join(
        f'    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{path(l)}"/>' for l in order
    ) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>'
    urls = '\n'.join(f'''  <url>
    <loc>{SITE}{path(l)}</loc>
    <lastmod>{lastmod}</lastmod>
{links}
{chr(10).join(f"    <image:image><image:loc>{SITE}/assets/img/store/{l}/{n}@2x.webp</image:loc></image:image>" for n in SHOTS)}
  </url>''' for l in order)
    paths = '|'.join(re.escape(path(l)) for l in order)
    home = re.compile(r'  <url>\n    <loc>' + re.escape(SITE) + f'({paths})</loc>.*?</url>\n', re.S)
    first = home.search(s).start()
    s = home.sub('', s)
    s = s[:first] + urls + '\n' + s[first:]
    f.write_text(s)


def main():
    import datetime
    store = json.loads((I18N / '_store.json').read_text())
    order = list(LOCALES)
    for loc in order:
        t = json.loads((I18N / f'{loc}.json').read_text())
        out = ROOT / ('index.html' if loc == 'en-US' else f'{loc}/index.html')
        out.parent.mkdir(exist_ok=True)
        out.write_text(page(loc, t, store, order))
    sitemap(order, datetime.date.today().isoformat())
    print(f'{len(order)} pages')


main()
