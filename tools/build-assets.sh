#!/bin/zsh
# Rebuilds every generated image on the site from its source:
#   the icon        tools/icon.html (from the Icon Composer layers in icon-layers/)
#   the social card tools/og.html (uses the icon and the hero screenshot)
#   (tools/screens/*.png, captured from the app's harness, feed only the social card;
#   the home pages' screenshots come from fastlane, see README)
# Needs Chrome for Testing, node, cwebp, pngquant and oxipng (brew install webp pngquant oxipng).
# Run from the repo root: tools/build-assets.sh
set -euo pipefail
cd "${0:A:h}/.."
TMP=$(mktemp -d)
IMG=assets/img
mkdir -p $IMG

squeeze() { pngquant --force --skip-if-larger --quality 80-95 --output "$1" "$1" 2>/dev/null || true; oxipng -q -o 4 --strip safe "$1"; }

# The icon, three shapes at 1024.
for shape in full rounded maskable; do
  node tools/render.mjs "tools/icon.html?shape=$shape" $TMP/icon-$shape.png 1024 1024 transparent >/dev/null
done

# iOS home screen (full bleed: iOS rounds it), Android/PWA (rounded on the page,
# maskable for the launcher), favicons.
sips -Z 180 $TMP/icon-full.png --out apple-touch-icon.png >/dev/null
for s in 192 512; do sips -Z $s $TMP/icon-rounded.png --out $IMG/icon-$s.png >/dev/null; done
sips -Z 512 $TMP/icon-maskable.png --out $IMG/icon-maskable-512.png >/dev/null
# The header logo (40 pt, at up to 3×).
sips -Z 128 $TMP/icon-rounded.png --out $IMG/logo-128.png >/dev/null
for s in 16 32 48; do sips -Z $s $TMP/icon-rounded.png --out $TMP/fav-$s.png >/dev/null; done
sips -Z 32 $TMP/icon-rounded.png --out favicon-32.png >/dev/null
node tools/ico.mjs favicon.ico $TMP/fav-16.png $TMP/fav-32.png $TMP/fav-48.png

# The social card (1200 × 630) and a square one for chat apps.
node tools/render.mjs tools/og.html $TMP/og.png 1200 630 >/dev/null
cp $TMP/og.png $IMG/og.png
node tools/render.mjs 'tools/og.html?square=1' $TMP/og-square.png 600 600 >/dev/null
cp $TMP/og-square.png $IMG/og-square.png

for f in apple-touch-icon.png favicon-32.png $IMG/icon-*.png $IMG/logo-*.png $IMG/og*.png; do squeeze $f; done
rm -rf $TMP
ls -la apple-touch-icon.png favicon.ico favicon-32.png $IMG
