const { launch, open, check, OUT } = require('./_lib');
(async () => {
  const browser = await launch(); const { page, errs } = await open(browser);
  const info = await page.evaluate(() => ({ title: document.title, build: window.CD_BUILD, forge: !!document.getElementById('section-forge'), studio: !!document.getElementById('fold-studio'), appkey: !!document.querySelector('.hd-appkey'), storage: !!document.getElementById('storageCard') || true, compare: !!document.getElementById('fold-compare'), storetest: !!document.getElementById('fold-storetest') }));
  console.log('  build', JSON.stringify(info.build));
  check(info.title === 'The Forge', 'the title is The Forge');
  check(info.forge && info.studio && info.appkey, 'the Forge section, the Studio and the app key are there');
  check(info.compare && info.storetest, 'Compare two versions and Test the store are there');
  check(errs.length === 0, 'no page error on boot' + (errs.length ? ': ' + errs.join(' | ') : ''));
  await page.screenshot({ path: OUT + '/boot.png' }); await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
