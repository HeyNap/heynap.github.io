# Wiring heynap.app

In this order. Steps 1–4 put the site online; the rest connect it to the apps,
the stores and search engines.

## 1. Push this repo

```bash
cd /Users/andrei/work/parent2/heynap.github.io
git add -A && git commit -m "HeyNap website" && git push -u origin main
```

## 2. Verify the domain on GitHub (protects it from takeover)

GitHub → the **HeyNap** organization → Settings → **Pages** → *Add a domain* →
`heynap.app`. GitHub shows a TXT record, something like:

| Type | Name | Value |
|---|---|---|
| TXT | `_github-pages-challenge-HeyNap` | (the code GitHub shows) |

Add it in GoDaddy (step 3), come back and click **Verify**.

## 3. GoDaddy DNS

GoDaddy → My Products → heynap.app → **DNS** (Manage DNS).

1. **Delete** what GoDaddy added by default: the `A` record on `@` that says
   "Parked", and the `CNAME` on `www` that points to `@` (if present). Under
   *Forwarding*, make sure no domain forwarding is set.
2. **Add:**

| Type | Name | Value | TTL |
|---|---|---|---|
| A | `@` | `185.199.108.153` | 1 hour |
| A | `@` | `185.199.109.153` | 1 hour |
| A | `@` | `185.199.110.153` | 1 hour |
| A | `@` | `185.199.111.153` | 1 hour |
| AAAA | `@` | `2606:50c0:8000::153` | 1 hour |
| AAAA | `@` | `2606:50c0:8001::153` | 1 hour |
| AAAA | `@` | `2606:50c0:8002::153` | 1 hour |
| AAAA | `@` | `2606:50c0:8003::153` | 1 hour |
| CNAME | `www` | `heynap.github.io` | 1 hour |
| TXT | `_github-pages-challenge-HeyNap` | (from step 2) | 1 hour |

Leave the `NS` and `SOA` records alone. Check propagation with
`dig heynap.app +short` (the four 185.199.x.153 addresses).

## 4. GitHub Pages on the repo

Repo **HeyNap/heynap.github.io** → Settings → **Pages**:

1. *Source*: **Deploy from a branch**, branch **main**, folder **/ (root)**.
2. *Custom domain*: `heynap.app` (the `CNAME` file already says so) → Save. Wait for
   "DNS check successful".
3. Tick **Enforce HTTPS** once it lets you (the certificate can take from minutes
   to a day).

`.app` domains only work over HTTPS (the whole TLD is on browsers' HSTS preload
list), so the site won't open at all until GitHub has issued the certificate.
That's normal; don't change DNS while waiting. `www.heynap.app` redirects to
`heynap.app` by itself.

## 5. The stores

**App Store Connect** (app record → App Information / the version page):

- Privacy Policy URL: `https://heynap.app/privacy/`
- Support URL: `https://heynap.app/support/`
- Marketing URL: `https://heynap.app/`
- License Agreement: either keep Apple's standard EULA, or set a custom one that
  links `https://heynap.app/terms/` (section 16 has Apple's required terms).

Then put the app's numeric id (App Store Connect → App Information → Apple ID) in place
of `APP_STORE_ID` (`index.html` twice, `site.webmanifest`, `llms.txt`) and uncomment
the `apple-itunes-app` meta in `index.html`: Safari then shows the Smart App Banner.

**The iOS app**: add the Associated Domains capability with `applinks:heynap.app`
and `webcredentials:heynap.app`. The site's `apple-app-site-association` already
lists `R4XU5D868Y.app.heynap.mobile` (team id from the Xcode project) for
`/open/*` and `/invite/*` only, so links to the website's own pages never open the
app. Apple caches this file through its CDN; changes take up to a day.

**Google Play Console**:

- Store listing → Privacy policy: `https://heynap.app/privacy/`; website
  `https://heynap.app/`; email `postmuseapp+heynap@gmail.com`.
- App content → Data safety: HeyNap has no accounts, so no account-deletion URL is needed; if the form asks how to delete data, point at `https://heynap.app/support/#delete`.
- Setup → App integrity → App signing → copy the **SHA-256 certificate
  fingerprint** into `.well-known/assetlinks.json` (in place of
  `REPLACE_WITH_PLAY_APP_SIGNING_SHA256`; add the upload key's too if you test
  links with locally signed builds).

**Android's install prompt**: `site.webmanifest` lists the Play app with
`prefer_related_applications`, so Chrome on Android can offer the app instead of
the website. There's no Android equivalent of Safari's banner beyond that.

## 6. Search engines and AI assistants

1. **Google Search Console** → Add property → **Domain** → `heynap.app`. It shows a
   TXT record (`google-site-verification=…`): add it in GoDaddy on `@`, then
   Verify. Then Sitemaps → submit `https://heynap.app/sitemap.xml`.
2. **Bing Webmaster Tools** → Import from Google Search Console (this also feeds
   DuckDuckGo, Yahoo and ChatGPT search, which use Bing's index).
3. Nothing to do for AI crawlers: `robots.txt` allows everyone, and `llms.txt`
   gives them a plain summary.
4. Check the share preview with the [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
   or by pasting the link in iMessage/WhatsApp.

## 7. The app's links

`heynap/lib/config.dart`: `privacyUrl` → `https://heynap.app/privacy/`,
`termsUrl` → `https://heynap.app/terms/` (or keep Apple's EULA), `supportEmail` →
`postmuseapp+heynap@gmail.com`.
