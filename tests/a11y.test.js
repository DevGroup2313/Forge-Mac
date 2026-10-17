/* axe-core over the open rooms; put axe.min.js (from the axe-core package) in tests/ */
const { launch, open, check, skip } = require('./_lib');
const fs = require('fs'), path = require('path');
(async () => {
  const axe = path.join(__dirname, 'axe.min.js'); if (!fs.existsSync(axe)) { skip('tests/axe.min.js is not here'); return; }
  const browser = await launch(); const { page } = await open(browser);
  /* the colours are measured on the settled page: the rooms' entrance fades and the tutor line's rise are switched off for the measurement, since a frame sampled mid-fade reads as low contrast when the box is busy (measured as a flake) */
  await page.addStyleTag({ content: '#section-forge *, #section-forge { animation: none !important; transition: none !important; }' });
  await page.addScriptTag({ path: axe });
  let bad = 0;
  for (const room of ['editor', 'files', 'settings', 'magister', 'curriculum']) {
    await page.evaluate(r => FORGE.openRoom(r), room); await page.waitForTimeout(800);
    /* the tutor line fades up once after a room opens, later on a big room: axe reads the settled page, never a frame of the fade (measured: a sample mid-fade read as low contrast) */
    await page.waitForFunction(() => new Promise(res => { const e = document.getElementById('tutorLine'); let n = 0; const iv = setInterval(() => { const o = +getComputedStyle(e).opacity; n = o >= 0.9 ? n + 1 : 0; if (n >= 3) { clearInterval(iv); res(true); } }, 100); setTimeout(() => { clearInterval(iv); res(true); }, 4000); }), null, { timeout: 10000 });
    const r = await page.evaluate(() => axe.run(document.getElementById('section-forge'), { runOnly: ['wcag2a', 'wcag2aa'] }).then(x => x.violations.map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length, first: (v.nodes[0] && v.nodes[0].target[0]) || '' }))));
    const serious = r.filter(v => v.impact === 'serious' || v.impact === 'critical');
    console.log('  ' + room + ': ' + r.length + ' kinds, ' + serious.length + ' serious or critical'); serious.forEach(v => console.log('     ' + v.impact + ' ' + v.id + ' x' + v.n + ' e.g. ' + v.first));
    bad += serious.length;
  }
  check(bad === 0, 'no serious or critical violation in the open rooms'); await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
