const { launch, open, openApp, check, skip, OUT } = require('./_lib');
const fs = require('fs');
(async () => {
  const browser = await launch(); const { ctx, page, errs } = await open(browser);
  const INK = process.env.INKWELL_HTML;
  if (INK && fs.existsSync(INK)) { await openApp(page, INK); await page.evaluate(() => window.__forgeStudioUI.selectSel('header .brand b')); await page.evaluate(() => window.__forgeStudioUI.record('text', '', 'kept by the test')); await page.waitForTimeout(500); await page.evaluate(() => window.__forgeStudioUI.keep()); await page.waitForFunction(() => window.__forgeStudioUI.state().live, null, { timeout: 180000 }); await page.waitForTimeout(2500); } else skip('no Inkwell file: no app copies in this run');
  fs.writeFileSync(OUT + '/note.txt', 'A note kept in Files.\n');
  await page.evaluate(() => FORGE.openRoom('files')); await page.setInputFiles('#filesIn', OUT + '/note.txt'); await page.waitForTimeout(1200);
  await page.evaluate(() => FORGE.openRoom('settings')); await page.waitForTimeout(600);
  const m = await page.evaluate(() => window.__forgeStorage.measure().then(L => ({ files: L.files.length, lib: L.lib.map(x => x.app + ':' + x.slot), own: L.own })));
  check(m.files === 1, 'the Storage card counts the file in Files');
  await page.locator('#stLimit').fill('50'); await page.locator('#stLimitSave').click(); await page.waitForTimeout(600);
  check(/50 MB/.test(await page.locator('#stReport').textContent()), 'a 50 MB limit is kept');
  if (m.lib.indexOf('inkwell:earlier') >= 0) { await page.locator('#stClean').click(); await page.waitForTimeout(2500); const lib = await page.evaluate(() => window.__forgeStorage.last().lib.map(x => x.app + ':' + x.slot)); check(lib.indexOf('inkwell:earlier') < 0 && lib.indexOf('inkwell:newest') >= 0, 'Clean the library removed the earlier copy and kept the newest'); }
  const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 180000 }), page.locator('#bkZipOut').click()]);
  const zip = OUT + '/everything.zip'; await dl.saveAs(zip);
  check(fs.statSync(zip).size > 1000, 'the zip backup was made (' + fs.statSync(zip).size + ' bytes)');
  check(errs.length === 0, 'no page error while exporting'); await ctx.close();
  const { page: p2, errs: e2 } = await open(browser);
  await p2.evaluate(() => FORGE.openRoom('settings')); await p2.setInputFiles('#bkZipIn', zip); await p2.waitForTimeout(2500);
  await p2.locator('[role=dialog] button', { hasText: /Merge|Fusionner/ }).click(); await p2.waitForTimeout(6000); await p2.waitForLoadState('load'); await p2.waitForTimeout(3000);
  const after = await p2.evaluate(() => Promise.all([window.__forgeLib.meta().then(m => Object.keys(m)), window.__forgeBackup.files().then(l => l.map(f => f.name))]).then(r => ({ lib: r[0], files: r[1], limit: localStorage.getItem('forge:storage:limitMB') })));
  check(after.files.indexOf('note.txt') >= 0, 'the file came back in the fresh profile');
  check(after.limit === '50', 'the settings came back');
  if (m.lib.length) check(after.lib.indexOf('inkwell:newest') >= 0, 'the app copy came back');
  check(e2.length === 0, 'no page error while reading back');
  await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
