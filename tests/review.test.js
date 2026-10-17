/* the defects the 9s62 review found, each shown fixed in the browser:
   a second Keep keeps the first edits; two blocks on one part stay two; a version kept under 9s61 runs one Studio on the stage;
   Clean the library never hangs; Merge keeps this device's own copies; the library tells its listeners; the Editing panel fits a short
   window; the help and the French refusal name the right steps */
const { launch, open, openApp, frameOf, check, skip, OUT } = require('./_lib');
const fs = require('fs'), path = require('path');
const FORGE = process.env.FORGE_HTML || path.join(__dirname, '..', 'the_forge.html');
const APPLIER_V2 = fs.readFileSync(path.join(__dirname, '..', 'tools', '9s62', 'applier_v2.js'), 'utf8');
(async () => {
  const browser = await launch();
  const html = fs.readFileSync(FORGE, 'utf8');

  /* 1. the texts */
  const help = html.indexOf('var HELP = {"editor"');
  const i2 = html.indexOf('"In 2, The whole app', help), i3 = html.indexOf('"In 3, Pick a named surface', help), i4 = html.indexOf('"In 4, Change it', help);
  check(i2 > 0 && i2 < i3 && i3 < i4, 'the Editor help lists 2, 3, 4 in that order (English)');
  const f2 = html.indexOf('"En 2, L’app entière', help), f3 = html.indexOf('"En 3, Choisir une surface nommée', help);
  check(f2 > 0 && f2 < f3, 'the Editor help lists 2 before 3 (French)');
  check(html.indexOf('Ses surfaces (\\u00e9tape 3) et le CSS libre') > 0 && html.indexOf('Ses surfaces (\\u00e9tape 2)') < 0, 'the French Workshop refusal names step 3');
  check(html.indexOf('<p>Step 5 makes real files.') > 0 && html.indexOf('<p>Step 3 makes real files.') < 0, 'the Guidebook shipping article names step 5');

  /* 2. the applier alone: two blocks and a copy on one part stay two blocks and one copy over many passes */
  { const { ctx, page } = await open(browser);
    const counts = await page.evaluate(src => new Promise(res => {
      const f = document.createElement('iframe'); f.style.cssText = 'width:300px;height:200px'; document.body.appendChild(f);
      const d = f.contentDocument; d.open();
      d.write('<!doctype html><html><head><meta charset="utf-8"></head><body><div id="a">part</div><div id="c">third</div><div id="b">second</div><script>window.__FORGE_STUDIO_EDITS=' + JSON.stringify([
        { id: 'h1', k: 'k1', sel: '#a', kind: 'html', value: '<p class="b">one</p>' },
        { id: 'h2', k: 'k1', sel: '#a', kind: 'html', value: '<p class="b">two</p>' },
        { id: 'd1', k: 'k1', sel: '#a', kind: 'dup' },
        { id: 'm1', k: 'k2', sel: '#b', kind: 'move', where: 'after', ref: '#a', refk: 'k1' }]) + ';</scr' + 'ipt><script>' + src + '</scr' + 'ipt></body></html>'); d.close();
      setTimeout(() => { const w = f.contentWindow; for (let i = 0; i < 4; i++) w.__forgeStudio.pass();
        setTimeout(() => res({ html: d.querySelectorAll('[data-forge-html]').length, dup: d.querySelectorAll('[data-forge-dup]').length, kids: d.body.children.length, gen: w.__forgeStudio.gen, order: [].map.call(d.body.children, x => x.id || x.getAttribute('data-forge-html') || x.getAttribute('data-forge-dup') || x.tagName).join(',') }), 400); }, 300); }), APPLIER_V2);
    check(counts.gen === 2, 'the applier is generation 2');
    check(counts.html === 2 && counts.dup === 1, 'two blocks and one copy after five passes (' + counts.html + ' blocks, ' + counts.dup + ' copies)');
    check(/^a,.*,b,c$/.test(counts.order.replace(/,SCRIPT/g, '')) && counts.kids === 6 + 2, 'the moved part lands after the whole run (' + counts.order + ')');
    await ctx.close(); }

  /* 3. the Storage card: Clean asked for while the first measure is still running comes back, and never hangs the page */
  { const { ctx, page, errs } = await open(browser);
    await page.evaluate(() => FORGE.openRoom('settings')); await page.waitForTimeout(500);
    const r = await page.evaluate(() => { window.confirm = () => false; window.__forgeStorage.measure();
      return Promise.race([window.__forgeStorage.clean().then(() => 'done'), new Promise(res => setTimeout(() => res('timeout'), 8000))]).then(x => ({ x, last: !!window.__forgeStorage.last() })); });
    check(r.x === 'done' && r.last, 'Clean the library during a measure comes back (' + r.x + ')');
    check(await page.evaluate(() => typeof window.__forgeLib.metaCached === 'function'), 'the library offers its cached list');
    const told = await page.evaluate(() => new Promise(res => { window.addEventListener('forge:lib', () => res(true)); setTimeout(() => res(false), 4000);
      window.__forgeLib.keepRaw({ app: 'inkwell', title: 'Inkwell', version: '1', build: '', date: '', name: 'i.html', size: 5, sha256: 'abc', source: 'file' }, new TextEncoder().encode('hello'), 'newest'); }));
    check(told === true, 'the library says forge:lib when a copy is kept');
    const bad = await page.evaluate(() => window.__forgeLib.keepRaw({ app: 'nope' }, new TextEncoder().encode('x'), 'newest').then(() => 'kept', e => e && e.code));
    check(bad === 'bad', 'a record for an unknown app is refused (' + bad + ')');
    check(errs.length === 0, 'no page error' + (errs.length ? ': ' + errs.join(' | ') : ''));
    await ctx.close(); }

  /* 4. Merge keeps this device's own copies; Replace takes the zip's */
  { const { ctx, page, errs } = await open(browser);
    await page.evaluate(() => FORGE.openRoom('settings')); await page.waitForTimeout(500);
    const seed = await page.evaluate(async () => {
      const enc = new TextEncoder(), L = window.__forgeLib;
      const mk = t => '<!doctype html><html><head><meta charset="utf-8"><title>Carpe Diem</title></head><body>' + t + '</body></html>';
      const X = enc.encode(mk('X, made here')), Y = enc.encode(mk('Y, the copy before')), A = enc.encode(mk('A, from the other device')), B = enc.encode(mk('B, its copy before'));
      const [sx, sy, sa, sb] = await Promise.all([L.sha(X), L.sha(Y), L.sha(A), L.sha(B)]);
      await L.keepRaw({ app: 'cd', title: 'Carpe Diem', version: '1051', build: '', date: '', name: 'x.html', size: X.length, sha256: sx, source: 'made' }, X, 'newest');
      await L.keepRaw({ app: 'cd', title: 'Carpe Diem', version: '1050', build: '', date: '', name: 'y.html', size: Y.length, sha256: sy, source: 'file' }, Y, 'earlier');
      const man = { forge: 'backup', v: 4, zip: true, at: new Date().toISOString(), build: {}, keys: {}, store: {}, files: [], studio: [], library: [
        { id: 'cd:newest', app: 'cd', slot: 'newest', version: '1051', build: '', date: '', name: 'a.html', title: 'Carpe Diem', size: A.length, sha256: sa, source: 'file', path: 'library/cd__newest.html' },
        { id: 'cd:earlier', app: 'cd', slot: 'earlier', version: '1050', build: '', date: '', name: 'b.html', title: 'Carpe Diem', size: B.length, sha256: sb, source: 'file', path: 'library/cd__earlier.html' }] };
      const blob = await window.__forgeZip.make([{ name: 'forge-backup.json', text: JSON.stringify(man) }, { name: 'library/cd__newest.html', bytes: A }, { name: 'library/cd__earlier.html', bytes: B }]);
      const u8 = new Uint8Array(await blob.arrayBuffer()); window.__t = { u8, man };
      return { sx, sy, sa, sb, n: u8.length }; });
    const run = async merge => { await page.evaluate(m => { const Z = window.__forgeLib.zip, t = window.__t; return window.__forgeBackupZip.restore(t.u8, Z.entries(t.u8), t.man, m); }, merge);
      await page.waitForTimeout(4000); await page.waitForLoadState('load'); await page.waitForTimeout(3000);
      const door = page.locator('#demo-entry, #cd-door').locator('text=Open the Editor').first(); if (await door.count()) { await door.click(); await page.waitForTimeout(800); }
      return page.evaluate(() => window.__forgeLib.meta().then(M => ({ n: M['cd:newest'] && M['cd:newest'].sha256, e: M['cd:earlier'] && M['cd:earlier'].sha256 }))); };
    const m1 = await run(true);
    check(m1.n === seed.sx && m1.e === seed.sy, 'Merge: this device keeps its own newest and earlier copies');
    await page.evaluate(() => FORGE.openRoom('settings')); await page.waitForTimeout(500);
    await page.evaluate(async seed => { const enc = new TextEncoder(), L = window.__forgeLib, mk = t => '<!doctype html><html><head><meta charset="utf-8"><title>Carpe Diem</title></head><body>' + t + '</body></html>';
      const A = enc.encode(mk('A, from the other device')), B = enc.encode(mk('B, its copy before'));
      const man = { forge: 'backup', v: 4, zip: true, at: new Date().toISOString(), build: {}, keys: {}, store: {}, files: [], studio: [], library: [
        { id: 'cd:newest', app: 'cd', slot: 'newest', version: '1051', build: '', date: '', name: 'a.html', title: 'Carpe Diem', size: A.length, sha256: seed.sa, source: 'file', path: 'library/cd__newest.html' },
        { id: 'cd:earlier', app: 'cd', slot: 'earlier', version: '1050', build: '', date: '', name: 'b.html', title: 'Carpe Diem', size: B.length, sha256: seed.sb, source: 'file', path: 'library/cd__earlier.html' }] };
      const blob = await window.__forgeZip.make([{ name: 'forge-backup.json', text: JSON.stringify(man) }, { name: 'library/cd__newest.html', bytes: A }, { name: 'library/cd__earlier.html', bytes: B }]);
      window.__t = { u8: new Uint8Array(await blob.arrayBuffer()), man }; }, seed);
    const m2 = await run(false);
    check(m2.n === seed.sa && m2.e === seed.sb, 'Replace: the zip\'s newest and earlier copies take their places');
    check(errs.filter(e => !/reload|navigation/i.test(e)).length === 0, 'no page error' + (errs.length ? ': ' + errs.join(' | ') : ''));
    await ctx.close(); }

  /* 5. the Editing panel in a short window: inside it, and its last row reachable */
  { const { ctx, page } = await open(browser, { viewport: { width: 1100, height: 430 } });
    await page.locator('.hd-appkey').first().click(); await page.waitForTimeout(600);
    const r = await page.evaluate(() => { const p = document.querySelector('.hd-appkey-wrap > .hd-panel[data-open]'); if (!p) return null; const pr = p.getBoundingClientRect();
      const rows = p.querySelectorAll('#edAppSeg button'); const last = rows[rows.length - 1]; last.scrollIntoView({ block: 'nearest' }); const lr = last.getBoundingClientRect();
      return { top: pr.top, bottom: pr.bottom, h: innerHeight, rows: rows.length, lastTop: lr.top, lastBottom: lr.bottom, scrolls: p.scrollHeight > p.clientHeight }; });
    check(r && r.top >= 0 && r.bottom <= r.h + 0.5, 'the panel stays inside a 430 px window (' + (r && Math.round(r.top)) + '..' + (r && Math.round(r.bottom)) + ' of ' + (r && r.h) + ')');
    check(r && r.rows >= 5 && r.lastBottom <= r.bottom + 1 && r.lastTop >= r.top - 1, 'the last of ' + (r && r.rows) + ' rows can be scrolled into view');
    await ctx.close(); }

  /* 5b. a full device is heard in Files: the refusal is said, not swallowed */
  { const { ctx, page } = await open(browser);
    await page.evaluate(() => FORGE.openRoom('files')); await page.waitForTimeout(500);
    const cdp = await ctx.newCDPSession(page); await cdp.send('Storage.overrideQuotaForOrigin', { origin: 'http://127.0.0.1:' + (process.env.FORGE_PORT || 8765), quotaSize: 200 * 1024 });
    const big = OUT + '/bigapp.html'; fs.writeFileSync(big, '<!doctype html><title>big</title>' + 'x'.repeat(3000000));
    await page.setInputFiles('#filesIn', big);
    const said = await page.evaluate(() => new Promise(res => { const t0 = Date.now();
      const iv = setInterval(() => { const s = (document.getElementById('filesState') || {}).textContent || ''; if (/No room left|Plus de place/.test(s) || Date.now() - t0 > 9000) { clearInterval(iv); res(s); } }, 200); }));
    check(/No room left on this device to keep bigapp.html/.test(said), 'a full device is said in plain words (' + said.slice(0, 60) + ')');
    await cdp.send('Storage.overrideQuotaForOrigin', { origin: 'http://127.0.0.1:' + (process.env.FORGE_PORT || 8765), quotaSize: 2000000000 });
    await ctx.close(); }

  /* 5c. the comparison: the Forge against itself with two far edits in well under three seconds; the fold speaks French */
  { const { ctx, page } = await open(browser);
    const d = await page.evaluate(() => fetch('the_forge.html').then(r => r.text()).then(A => { const L = A.split('\n'); L[100] = L[100] + ' <!-- one -->'; L[L.length - 200] = L[L.length - 200] + ' <!-- two -->'; const r = window.__forgeCompare.diff(A, L.join('\n')); return { ms: r.ms, places: r.hunks.length, add: r.add, del: r.del }; }));
    check(d.places === 2 && d.add === 2 && d.del === 2, 'two far edits found as two places (' + d.places + ')');
    check(d.ms < 3000, 'the comparison took ' + d.ms + ' ms');
    const fr = await page.evaluate(() => { document.documentElement.lang = 'fr'; return new Promise(res => setTimeout(() => res({ go: (document.getElementById('cmpGo') || {}).textContent, a: (document.querySelector('#fold-compare [data-cmp="a"]') || {}).textContent }), 400)); });
    check(fr.go === '🔍 Comparer' && fr.a === 'Avant', 'the Compare fold speaks French (' + fr.go + ', ' + fr.a + ')');
    await ctx.close(); }

  /* 5d. the Studio's second copy of the edits travels in the zip and comes back */
  { const { ctx, page } = await open(browser);
    await page.evaluate(() => new Promise((res, rej) => { const r = indexedDB.open('forge-studio', 2); r.onupgradeneeded = () => { const db = r.result; if (!db.objectStoreNames.contains('apps')) db.createObjectStore('apps', { keyPath: 'id' }); if (!db.objectStoreNames.contains('edits')) db.createObjectStore('edits', { keyPath: 'id' }); };
      r.onsuccess = () => { const d = r.result, t = d.transaction('edits', 'readwrite'); t.objectStore('edits').put({ id: 'ingenium', edits: [{ id: 'e1', k: 'fs1', sel: '#homeTitle', kind: 'text', prop: '', value: 'from the second copy' }], seq: 2, t: Date.now() }); t.oncomplete = () => { d.close(); res(); }; t.onerror = () => rej(t.error); }; r.onerror = () => rej(r.error); }));
    await page.evaluate(() => FORGE.openRoom('settings')); await page.waitForTimeout(600);
    const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 120000 }), page.locator('#bkZipOut').click()]);
    const zipPath = OUT + '/edits.zip'; await dl.saveAs(zipPath); const bytes = Array.from(fs.readFileSync(zipPath));
    const names = await page.evaluate(b => Object.keys(window.__forgeLib.zip.entries(new Uint8Array(b))), bytes);
    check(names.indexOf('studio/edits.json') >= 0, 'the zip carries studio/edits.json (' + names.length + ' entries)');
    await ctx.close();
    const { ctx: c2, page: p2 } = await open(browser);
    await p2.evaluate(() => FORGE.openRoom('settings')); await p2.waitForTimeout(500);
    await p2.evaluate(b => { const u8 = new Uint8Array(b), Z = window.__forgeLib.zip, ents = Z.entries(u8); return Z.data(u8, ents['forge-backup.json']).then(mb => window.__forgeBackupZip.restore(u8, ents, JSON.parse(new TextDecoder().decode(mb)), false)); }, bytes);
    await p2.waitForTimeout(4000); await p2.waitForLoadState('load'); await p2.waitForTimeout(2500);
    const rec = await p2.evaluate(() => new Promise(res => { const r = indexedDB.open('forge-studio', 2); r.onsuccess = () => { const d = r.result; try { const q = d.transaction('edits', 'readonly').objectStore('edits').get('ingenium'); q.onsuccess = () => { d.close(); res(q.result || null); }; q.onerror = () => { d.close(); res(null); }; } catch (e) { d.close(); res(null); } }; r.onerror = () => res(null); }));
    check(rec && rec.edits && rec.edits[0] && rec.edits[0].value === 'from the second copy', 'the second copy of the edits came back on the fresh profile');
    await c2.close(); }

  /* 5e. two new apps with one name: Remove takes the row that was pressed, by id */
  { const { ctx, page, errs } = await open(browser);
    await page.evaluate(() => { document.getElementById('fsNewName').value = 'Twin'; window.__forgeStudioUI.newApp('blank'); }); await page.waitForTimeout(2500);
    await page.evaluate(() => { document.getElementById('fsNewName').value = 'Twin'; window.__forgeStudioUI.newApp('blank'); }); await page.waitForTimeout(2500);
    const before = await page.evaluate(() => window.__forgeStudioUI.newApps().then(l => l.sort((a, b) => b.at - a.at).map(x => x.id)));
    check(before.length === 2, 'two new apps named Twin (' + before.length + ')');
    await page.evaluate(() => { const rows = document.querySelectorAll('#fsNewList .fs-row'); const b = rows[0].querySelector('.fs-del'); b.click(); }); await page.waitForTimeout(2500);
    const after = await page.evaluate(() => window.__forgeStudioUI.newApps().then(l => l.map(x => x.id)));
    check(after.length === 1 && after[0] === before[1], 'the newer Twin (the row pressed) went; the older stays');
    check(errs.length === 0, 'no page error' + (errs.length ? ': ' + errs.join(' | ') : ''));
    await ctx.close(); }

  /* 5f. the curriculum: a checked prediction stays in view, the counts follow in place, and an answer in the questions room is not wiped */
  { const { ctx, page, errs } = await open(browser);
    await page.evaluate(() => { FORGE.openRoom('curriculum'); FORGE.tab('curriculum', 'py'); }); await page.waitForTimeout(500);
    await page.evaluate(() => { var pg = document.querySelector('#curricPages .page[data-page="py"]'); pg.querySelector('details.term').open = true; pg.querySelector('details.module').open = true; pg.querySelector('details.lesson').open = true;
      Array.from(pg.querySelectorAll('details.lesson button')).find(x => /Check my prediction/.test(x.textContent)).click(); });
    await page.waitForTimeout(3000);
    const r = await page.evaluate(() => { var pg = document.querySelector('#curricPages .page[data-page="py"]'); var l = pg.querySelector('details.lesson'); var a = l.querySelector('.cd-tip-line');
      return { shown: !!(a && a.style.display === 'block'), lessonOpen: l.open, read: /✔/.test(l.querySelector('summary').textContent), moduleLine: pg.querySelector('details.module summary .s').textContent, termLine: pg.querySelector('details.term summary .s').textContent, yearLine: pg.querySelector('.panel.card .muted').textContent, mag: (document.querySelector('#magUnits .unitcard:nth-child(2) .muted') || {}).textContent || '' }; });
    check(r.shown && r.lessonOpen, 'the checked prediction is still in view three seconds later');
    check(r.read && /^1 of 2 read/.test(r.moduleLine) && /^1 of 24 lessons read/.test(r.mag), 'the lesson, its module and the Magister count it as read, in place (' + r.moduleLine + '; ' + r.mag + ')');
    check(/· 1 of 8 read$/.test(r.termLine) && /24 lessons · 1 read/.test(r.yearLine), 'the term and the year count it too (' + r.termLine.slice(-14) + '; ' + r.yearLine.slice(0, 60) + ')');
    await page.evaluate(() => { FORGE.openRoom('assessments'); FORGE.tab('assessments', 'cpp'); }); await page.waitForTimeout(600);
    await page.evaluate(() => { var pg = document.querySelector('#assessPages .page[data-page="cpp"]'); pg.querySelector('details.term').open = true; pg.querySelector('details.module').open = true; pg.querySelectorAll('details.module .q .qa')[1].click(); });
    await page.waitForTimeout(3000);
    const tip = await page.evaluate(() => { var e = document.querySelector('#assessPages .page[data-page="cpp"] details.module .q .cd-tip-line'); return e ? e.textContent : ''; });
    check(/^Right\./.test(tip), 'the answer given in the questions room is still explained three seconds later');
    check(errs.length === 0, 'no page error' + (errs.length ? ': ' + errs.join(' | ') : ''));
    await ctx.close(); }

  /* 5g. accessibility: the Guidebook chapter is listed and found; the checker finds a nameless control on a closed page and an unlabelled field, keeps the scroll, speaks French; the handle's value follows the split */
  { const { ctx, page, errs } = await open(browser, { viewport: { width: 1400, height: 700 } });
    const g = await page.evaluate(() => { var arts = [].slice.call(document.querySelectorAll('#guide article')); var i = arts.findIndex(a => /Testing with a screen reader/.test((a.querySelector('h3') || {}).textContent || '')); var toc = document.getElementById('guideToc');
      var s = document.getElementById('guideSearch'); s.value = 'VoiceOver'; s.dispatchEvent(new Event('input', { bubbles: true })); return new Promise(res => setTimeout(() => res({ indexed: i >= 0, inToc: /Testing with a screen reader/.test(toc.textContent), found: toc.querySelectorAll('button').length }), 400)); });
    check(g.indexed && g.inToc && g.found >= 1, 'the Guidebook lists the screen reader chapter and finds it by "VoiceOver"');
    const a = await page.evaluate(() => { var fold = document.getElementById('fold-a11y'); fold.open = true; var n = fold, sc = null; while (n && n !== document.body) { var cs = getComputedStyle(n); if (/(auto|scroll)/.test(cs.overflowY) && n.scrollHeight > n.clientHeight + 10) { sc = n; break; } n = n.parentElement; } if (sc) sc.scrollTop = 500; var before = sc ? sc.scrollTop : 0;
      var ff = document.getElementById('fold-file'); var pg = ff.closest('.page'); var pages = pg ? pg.parentNode.querySelectorAll('.page') : []; pages.forEach(x => x.setAttribute('data-on', x === pg ? '0' : '1')); /* the Edit page closed, as when Troubleshoot is open */
      var b = document.createElement('button'); b.id = 'tmpNameless'; b.type = 'button'; b.innerHTML = '<span></span>'; (ff.querySelector('.fold-body') || ff).appendChild(b);
      var s = document.createElement('select'); s.id = 'tmpSel'; s.innerHTML = '<option>One</option>'; fold.querySelector('.fold-body').appendChild(s);
      window.__forgeA11y.run(); var found = window.__forgeA11y.last(); var after = sc ? sc.scrollTop : 0; b.remove(); s.remove(); pages.forEach(x => x.setAttribute('data-on', x === pg ? '1' : '0'));
      return { before, after, nameless: found.filter(x => /tmpNameless/.test(x.where)).length, sel: found.filter(x => x.kind === 'label' && /tmpSel/.test(x.where)).length, editOff: pg ? pg.getAttribute('data-on') : '?' }; });
    check(a.nameless === 1 && a.sel === 1, 'the checker finds a nameless control on a closed page and an unlabelled field (' + a.nameless + ', ' + a.sel + ')');
    check(a.before === 500 && a.after === 500, 'the room keeps its scroll through the check (' + a.before + ' -> ' + a.after + ')');
    const fr = await page.evaluate(() => { document.documentElement.lang = 'fr'; return new Promise(res => setTimeout(() => res({ go: document.getElementById('a11yGo').textContent, fn: document.getElementById('fnUnit').getAttribute('aria-label') }), 500)); });
    check(fr.go === '♿ Vérifier maintenant' && /^Unité/.test(fr.fn), 'the fold and the field names speak French');
    const hd = await page.evaluate(() => new Promise(res => { var t = document.getElementById('thread'), h = document.getElementById('handle'); t.style.setProperty('--room-w', Math.round(document.getElementById('main').clientWidth * 0.62) + 'px'); setTimeout(() => res({ now: +h.getAttribute('aria-valuenow'), min: +h.getAttribute('aria-valuemin'), max: +h.getAttribute('aria-valuemax') }), 600); }));
    check(hd.now >= 58 && hd.now <= 66 && hd.min <= hd.now && hd.now <= hd.max, 'the handle says its new value after the split moves (' + hd.now + ' in ' + hd.min + '..' + hd.max + ')');
    check(errs.length === 0, 'no page error' + (errs.length ? ': ' + errs.join(' | ') : ''));
    await ctx.close(); }

  /* 5h. how much help: the walkthrough's why on every step, twice over; the hidden tutor line stays hidden through boot; a store that refuses to write still keeps the level; the words follow the language */
  { const { ctx, page, errs } = await open(browser);
    const r = await page.evaluate(() => new Promise(async res => { const sleep = ms => new Promise(r => setTimeout(r, ms)); const whys = []; window.forgeWalkthrough(); await sleep(700); const p = document.getElementById('fg-walk');
      for (let i = 0; i < 5; i++) { whys.push(!!p.querySelector('.fg-why')); const nx = Array.from(p.querySelectorAll('button')).find(b => (b.getAttribute('data-fgw') || '') === 'next'); if (nx) nx.click(); await sleep(500); }
      window.forgeWalkthrough(); await sleep(700); const again = !!p.querySelector('.fg-why'); document.documentElement.lang = 'fr'; await sleep(500);
      res({ whys, again, h3: (document.querySelector('#fgLevelCard h3') || {}).textContent, why: ((p.querySelector('.fg-why') || {}).textContent || '').slice(0, 8) }); }));
    check(r.whys.every(Boolean) && r.again, 'the walkthrough carries its why on steps 1 to 5 and again on a second start');
    check(r.h3 === 'Combien la Forge explique' && r.why === 'Pourquoi', 'the Settings card and the why follow the language');
    check(errs.length === 0, 'no page error' + (errs.length ? ': ' + errs.join(' | ') : ''));
    await ctx.close(); }
  { const ctx = await browser.newContext({ viewport: { width: 1400, height: 800 } }); const page = await ctx.newPage(); await page.addInitScript(() => { try { localStorage.setItem('forge:tutor', '0'); } catch (e) {} });
    await page.goto(require('./_lib').URL, { waitUntil: 'load', timeout: 180000 }); await page.waitForTimeout(3500);
    const tut = await page.evaluate(() => document.getElementById('tutor').getAttribute('data-on'));
    check(tut === '0', 'the tutor line she hid stays hidden through boot');
    await ctx.close(); }
  { const ctx = await browser.newContext({ viewport: { width: 1400, height: 800 } }); const page = await ctx.newPage(); await page.addInitScript(() => { const o = Storage.prototype.setItem; Storage.prototype.setItem = function (k, v) { if (/^fg:/.test(k)) throw new Error('refused'); return o.call(this, k, v); }; });
    await page.goto(require('./_lib').URL, { waitUntil: 'load', timeout: 180000 }); await page.waitForTimeout(3000);
    const door = page.locator('#demo-entry, #cd-door').locator('text=Open the Editor').first(); if (await door.count()) await door.click(); await page.waitForTimeout(800);
    const r = await page.evaluate(() => new Promise(async res => { const sleep = ms => new Promise(r => setTimeout(r, ms)); document.querySelector('.fg-lv[data-fg-level="ease"]').click(); await sleep(400); const card = document.querySelector('#room-editor .fg-help'); const folded = !card.open; card.querySelector('summary').click(); await sleep(200); document.body.appendChild(document.createElement('div')); await sleep(600); res({ lv: document.documentElement.getAttribute('data-fg-level'), folded, stillOpen: card.open }); }));
    check(r.lv === 'ease' && r.folded && r.stillOpen, 'a store that refuses to write still keeps the level, and a card opened by hand stays open');
    await ctx.close(); }

  /* 6. with Ingenium: a second Keep keeps the first edit; a version kept under 9s61 runs one Studio on the stage */
  const ING = process.env.INGENIUM_HTML;
  if (ING && fs.existsSync(ING)) {
    { const { ctx, page, errs } = await open(browser);
      await openApp(page, ING);
      const pages = await page.evaluate(() => window.__forgeStudioUI.scan()); const first = pages.find(p => p.group === 'page'); if (first) { await page.evaluate(p => window.__forgeStudioUI.go(p), first); await page.waitForTimeout(1500); }
      await page.evaluate(() => window.__forgeStudioUI.selectSel('#homeTitle')); await page.evaluate(() => window.__forgeStudioUI.record('text', '', 'First keep')); await page.waitForTimeout(600);
      await page.evaluate(() => window.__forgeStudioUI.keep()); await page.waitForFunction(() => window.__forgeStudioUI.state().live, null, { timeout: 180000 }); await page.waitForTimeout(3000);
      await page.evaluate(() => window.__forgeStudioUI.selectSel('#homeTitle')); await page.evaluate(() => window.__forgeStudioUI.record('style', 'color', 'rgb(200, 0, 0)')); await page.waitForTimeout(600);
      await page.evaluate(() => window.__forgeStudioUI.keep()); await page.waitForFunction(() => window.__forgeStudioUI.state().live, null, { timeout: 180000 }); await page.waitForTimeout(3000);
      const after = await frameOf(page).evaluate(() => { const e = document.querySelector('#homeTitle'); const tag = document.getElementById('forge-studio-edits'), cs = document.querySelector('meta[charset]');
        return { t: e && e.textContent, c: e && getComputedStyle(e).color, baked: window.__forgeStudio.baked().length, inHead: !!(tag && tag.parentNode === document.head), afterCharset: !!(tag && cs && (cs.compareDocumentPosition(tag) & 4)) }; });
      check(after.baked >= 2 && /First keep/.test(after.t || '') && after.c === 'rgb(200, 0, 0)', 'the second Keep carries both edits (' + after.baked + ' baked; "' + after.t + '", ' + after.c + ')');
      check(after.inHead && after.afterCharset, 'the baked edits stand in the head, after the charset');
      check(errs.length === 0, 'no page error' + (errs.length ? ': ' + errs.join(' | ') : ''));
      await ctx.close(); }
    { const base = html; const lit = /var APPLIER="((?:[^"\\]|\\.)*)", AGENT=/.exec(base);
      /* a version as 9s61 kept it: the edits tag and the old applier at the foot of the body; the old applier is taken from the 9s61 literal if the base is beside the tests */
      let v1 = null; const b61 = process.env.FORGE_BASE_61; if (b61 && fs.existsSync(b61)) { const m = /var APPLIER="((?:[^"\\]|\\.)*)", AGENT=/.exec(fs.readFileSync(b61, 'utf8')); if (m) v1 = new Function('return "' + m[1] + '"')(); }
      if (!v1) skip('no 9s61 base given (FORGE_BASE_61): the old applier is stood in for by a copy of the new one');
      const ap = v1 || new Function('return "' + lit[1] + '"')();
      const src = fs.readFileSync(ING, 'utf8'); const at = src.lastIndexOf('</body>');
      const old = src.slice(0, at) + '<script id="forge-studio-edits">window.__FORGE_STUDIO_EDITS=[{"id":"t1","k":"fs1","sel":"#homeTitle","kind":"text","prop":"","value":"From the old version"}];</script><script id="forge-studio-applier">' + ap + '</script>' + src.slice(at);
      const file = path.join(OUT, 'ingenium_9s61_kept.html'); fs.writeFileSync(file, old);
      const { ctx, page, errs } = await open(browser);
      await openApp(page, file);
      const pages = await page.evaluate(() => window.__forgeStudioUI.scan()); const first = pages.find(p => p.group === 'page'); if (first) { await page.evaluate(p => window.__forgeStudioUI.go(p), first); await page.waitForTimeout(1500); }
      const st = await frameOf(page).evaluate(() => ({ appliers: document.querySelectorAll('script#forge-studio-applier').length, inBody: !!document.body.querySelector('script#forge-studio-applier'), gen: window.__forgeStudio.gen, baked: window.__forgeStudio.baked().length, t: (document.querySelector('#homeTitle') || {}).textContent }));
      check(st.appliers === 1 && !st.inBody && st.gen === 2, 'one Studio alone on the stage, in the head (' + st.appliers + ' applier, gen ' + st.gen + ')');
      check(st.baked === 1 && /From the old version/.test(st.t || ''), 'the old version\'s edit is baked and applied (' + st.baked + ' baked)');
      check(errs.length === 0, 'no page error' + (errs.length ? ': ' + errs.join(' | ') : ''));
      await ctx.close(); }
  } else skip('Ingenium: no file given');
  await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
