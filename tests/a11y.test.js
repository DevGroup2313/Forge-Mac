/* axe-core over the open rooms; put axe.min.js (from the axe-core package) in tests/ */
const { launch, open, check, skip } = require('./_lib');
const fs = require('fs'), path = require('path');
(async () => {
  const axe = path.join(__dirname, 'axe.min.js'); if (!fs.existsSync(axe)) { skip('tests/axe.min.js is not here'); return; }
  const browser = await launch(); const { page } = await open(browser);
  await page.addScriptTag({ path: axe });
  let bad = 0;
  for (const room of ['editor', 'files', 'settings', 'magister', 'curriculum']) {
    await page.evaluate(r => FORGE.openRoom(r), room); await page.waitForTimeout(800);
    const r = await page.evaluate(() => axe.run(document.getElementById('section-forge'), { runOnly: ['wcag2a', 'wcag2aa'] }).then(x => x.violations.map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length, first: (v.nodes[0] && v.nodes[0].target[0]) || '' }))));
    const serious = r.filter(v => v.impact === 'serious' || v.impact === 'critical');
    console.log('  ' + room + ': ' + r.length + ' kinds, ' + serious.length + ' serious or critical'); serious.forEach(v => console.log('     ' + v.impact + ' ' + v.id + ' x' + v.n + ' e.g. ' + v.first));
    bad += serious.length;
  }
  check(bad === 0, 'no serious or critical violation in the open rooms'); await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
