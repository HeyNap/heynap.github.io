// Renders a local HTML file to a PNG in headless Chrome for Testing: the icon
// (tools/icon.html) and the social card (tools/og.html).
//
//   node tools/render.mjs <file.html[?query]> <out.png> <width> <height> [transparent]
//
// The page is laid out at width × height CSS pixels and captured at 1×.
// `transparent` keeps the page's empty background see-through (icon corners).
import { spawn } from 'node:child_process';
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const CH = '/Applications/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const [input, out, w, h, transparent] = process.argv.slice(2);
const [file, query = ''] = input.split('?');
const url = pathToFileURL(resolve(file)).href + (query ? `?${query}` : '');
const port = 9400 + Math.floor(Math.random() * 400);
const prof = mkdtempSync(join(tmpdir(), 'heynap-render-'));
const chrome = spawn(CH, [
  '--headless=new', `--user-data-dir=${prof}`, '--no-first-run', '--hide-scrollbars',
  '--disable-background-networking', '--disable-component-update', '--disable-sync',
  '--disable-default-apps', '--no-default-browser-check', '--allow-file-access-from-files',
  '--force-color-profile=srgb',
  '--disable-features=MediaRouter,DialMediaRouteProvider,GlobalMediaControls',
  `--remote-debugging-port=${port}`, 'about:blank',
], { stdio: 'ignore' });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let targets;
for (let i = 0; i < 60 && !targets; i++) {
  try { targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); } catch { await sleep(200); }
}
const page = targets.find((t) => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0;
const pending = new Map();
const send = (method, params = {}) => {
  const i = ++id;
  ws.send(JSON.stringify({ id: i, method, params }));
  return new Promise((r) => pending.set(i, r));
};
ws.addEventListener('message', (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); }
});
await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', {
  width: Number(w), height: Number(h), deviceScaleFactor: 1, mobile: false,
});
if (transparent) {
  await send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });
}
await send('Page.navigate', { url });
// Fonts and images: wait until the page says it's ready (or a second).
for (let i = 0; i < 50; i++) {
  const r = await send('Runtime.evaluate', {
    expression: 'document.readyState === "complete" && document.fonts.status === "loaded"',
    returnByValue: true,
  });
  if (r?.result?.value) break;
  await sleep(100);
}
await sleep(300);
const shot = await send('Page.captureScreenshot', {
  format: 'png',
  clip: { x: 0, y: 0, width: Number(w), height: Number(h), scale: 1 },
  captureBeyondViewport: true,
});
writeFileSync(out, Buffer.from(shot.data, 'base64'));
ws.close();
const exited = new Promise((r) => chrome.once('exit', r));
chrome.kill();
await exited;
try { rmSync(prof, { recursive: true, force: true }); } catch {}
console.log(out);
process.exit(0);
