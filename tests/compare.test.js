const { launch, open, openApp, check, skip } = require('./_lib');
(async () => {
  const browser = await launch(); const { page, errs } = await open(browser);
  const INK = process.env.INKWELL_HTML; if (!INK || !require('fs').existsSync(INK)) { skip('no Inkwell file'); await browser.close(); return; }
  await openApp(page, INK); await page.evaluate(() => window.__forgeStudioUI.selectSel('header .brand b')); await page.evaluate(() => window.__forgeStudioUI.record('text', '', 'compared')); await page.waitForTimeout(500); await page.evaluate(() => window.__forgeStudioUI.keep()); await page.waitForFunction(() => window.__forgeStudioUI.state().live, null, { timeout: 180000 }); await page.waitForTimeout(2500);
  await page.evaluate(() => { FORGE.tab('editor', 'trouble'); document.getElementById('fold-compare').open = true; }); await page.waitForTimeout(1500);
  await page.selectOption('#cmpA', 'lib:inkwell:earlier'); await page.selectOption('#cmpB', 'lib:inkwell:newest'); await page.locator('#cmpGo').click(); await page.waitForTimeout(4000);
  const sum = await page.locator('#cmpSum').textContent();
  check(/lines added/.test(sum) && /place/.test(sum), 'earlier and newest differ, said in words: ' + sum.slice(0, 90));
  await page.selectOption('#cmpA', 'lib:inkwell:newest'); await page.selectOption('#cmpB', 'stage'); await page.locator('#cmpGo').click(); await page.waitForTimeout(3000);
  check(/the same|identiques/.test(await page.locator('#cmpSum').textContent()), 'the newest copy and the stage are the same');
  check(errs.length === 0, 'no page error'); await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
