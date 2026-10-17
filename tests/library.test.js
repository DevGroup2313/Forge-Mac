const { launch, open, openApp, check, skip } = require('./_lib');
(async () => {
  const browser = await launch(); const { page, errs } = await open(browser);
  if (process.env.INKWELL_HTML && require('fs').existsSync(process.env.INKWELL_HTML)) await openApp(page, process.env.INKWELL_HTML); else skip('no Inkwell file: the store test runs on an empty library');
  await page.evaluate(() => { FORGE.tab('editor', 'trouble'); document.getElementById('fold-storetest').open = true; });
  await page.evaluate(() => window.__forgeStoreTest.run());
  await page.waitForFunction(() => { var l = window.__forgeStoreTest.lines(); return l.length && /passed|failed|échec|réussi/.test(l[l.length - 1].text); }, null, { timeout: 60000 });
  const lines = await page.evaluate(() => window.__forgeStoreTest.lines());
  lines.forEach(l => console.log('   ', l.ok === true ? '✓' : (l.ok === false ? '✗' : '·'), l.text));
  check(!lines.some(l => l.ok === false), 'every store step passed');
  check(errs.length === 0, 'no page error');
  await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
