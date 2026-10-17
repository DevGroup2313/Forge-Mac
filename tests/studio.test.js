const { launch, open, openApp, frameOf, check, skip } = require('./_lib');
const APPS = [['ingenium', process.env.INGENIUM_HTML, '#homeTitle'], ['inkwell', process.env.INKWELL_HTML, 'header .brand b'], ['cd', process.env.CARPE_HTML, '#head-readings'], ['forge', process.env.FORGE_HTML, '#brand-offline']];
(async () => {
  const browser = await launch();
  for (const [key, file, sel] of APPS) {
    if (!file || !require('fs').existsSync(file)) { skip(key + ': no file given'); continue; }
    const { ctx, page, errs } = await open(browser);
    await openApp(page, file);
    const st = await page.evaluate(() => ({ app: window.__forgeEd.app(), live: window.__forgeStudioUI.state().live }));
    check(st.app === key, key + ': the Forge read the app from the file (' + st.app + ')');
    await page.waitForTimeout(2500);
    const pages = await page.evaluate(() => window.__forgeStudioUI.scan());
    check(pages.length >= 3, key + ': ' + pages.length + ' places found');
    const first = pages.find(p => p.group === 'page'); if (first) { await page.evaluate(p => window.__forgeStudioUI.go(p), first); await page.waitForTimeout(2000); }
    const info = await page.evaluate(s => window.__forgeStudioUI.selectSel(s), sel);
    check(info && info.sel, key + ': the part ' + sel + ' is chosen');
    await page.evaluate(() => window.__forgeStudioUI.record('text', '', 'Changed by the test'));
    await page.waitForTimeout(1000);
    const live = await frameOf(page).evaluate(s => (document.querySelector(s) || {}).textContent, sel);
    check(/Changed by the test/.test(live || ''), key + ': the preview followed the change');
    await page.evaluate(() => window.__forgeStudioUI.keep());
    await page.waitForFunction(() => window.__forgeStudioUI.state().live, null, { timeout: 180000 }); await page.waitForTimeout(3000);
    const after = await frameOf(page).evaluate(s => ({ t: (document.querySelector(s) || {}).textContent, baked: window.__forgeStudio.baked().length }), sel);
    check(/Changed by the test/.test(after.t || '') && after.baked >= 1, key + ': the kept version carries the edit (' + after.baked + ' baked)');
    const meta = await page.evaluate(() => window.__forgeLib.meta().then(m => Object.keys(m)));
    check(meta.indexOf(key + ':newest') >= 0 && meta.indexOf(key + ':earlier') >= 0, key + ': newest and earlier copies kept');
    check(errs.length === 0, key + ': no page error' + (errs.length ? ': ' + errs.join(' | ') : ''));
    await ctx.close();
  }
  await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
