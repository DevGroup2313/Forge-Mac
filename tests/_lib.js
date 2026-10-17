/* shared helpers: a browser, a page through the door, an app opened in the Editor */
const path = require('path');
let chromium; try { chromium = require('playwright').chromium; } catch (e) { chromium = require('/opt/node-tools/node_modules/playwright').chromium; }
const URL = 'http://127.0.0.1:' + (process.env.FORGE_PORT || 8765) + '/the_forge.html';
async function launch() { const opts = {}; if (process.env.PW_CHROME) opts.executablePath = process.env.PW_CHROME; else if (require('fs').existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome')) opts.executablePath = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'; return chromium.launch(opts); }
async function open(browser, ctxOpts) {
  const ctx = await browser.newContext(Object.assign({ viewport: { width: 1400, height: 900 }, acceptDownloads: true }, ctxOpts || {}));
  const page = await ctx.newPage(); const errs = [];
  page.on('pageerror', e => errs.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/404|net::ERR|permissions policy/i.test(m.text())) errs.push('console: ' + m.text().slice(0, 300)); });
  page.on('dialog', async d => { try { await d.accept(); } catch (e) {} });
  await page.goto(URL, { waitUntil: 'load', timeout: 180000 }); await page.waitForTimeout(2500);
  const door = page.locator('#demo-entry, #cd-door').locator('text=Open the Editor').first(); if (await door.count()) await door.click(); await page.waitForTimeout(900);
  return { ctx, page, errs };
}
async function openApp(page, file) {
  await page.setInputFiles('#edShell', file);
  await page.waitForFunction(() => window.__forgeStudioUI && window.__forgeStudioUI.state().live, null, { timeout: 180000 });
  await page.waitForTimeout(2500);
}
function frameOf(page) { return page.frames().find(f => f !== page.mainFrame() && f.parentFrame() === page.mainFrame()); }
function check(cond, what) { if (!cond) { throw new Error('FAILED: ' + what); } console.log('  ok  ' + what); }
function skip(what) { console.log('  skip ' + what); }
const OUT = path.join(__dirname, 'out');
module.exports = { launch, open, openApp, frameOf, check, skip, OUT, URL };
