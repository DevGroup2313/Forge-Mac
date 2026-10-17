"""9s62 · COMPARE TWO VERSIONS: what changed between any two copies of an app, said in plain words and shown line by line."""
FOLD = r'''<details class="fold panel" id="fold-compare">
          <summary><span class="n">7</span><span class="t">🔍 Compare two versions</span><span class="s" id="cmpState">which two</span></summary>
          <div class="fold-body">
            <p data-cmp="lede">See what changed between two versions of an app: the one on the stage, the copies the Forge keeps (the newest and the one before), a new app of yours, or any file from this device. The Forge says in words what differs, then shows each place, line by line, before and after.</p>
            <div class="row" style="flex-wrap:wrap;gap:8px;align-items:flex-end">
              <label class="field"><span data-cmp="a">Before</span><select id="cmpA"></select></label>
              <label class="field"><span data-cmp="b">After</span><select id="cmpB"></select></label>
              <input id="cmpFileA" type="file" style="display:none"><input id="cmpFileB" type="file" style="display:none">
              <button type="button" class="stone solid" id="cmpGo">🔍 Compare</button>
            </div>
            <div id="cmpSum" class="muted" role="status" aria-live="polite" style="margin-top:8px;font-size:13px;line-height:1.5"></div>
            <div id="cmpOut" class="cmp-out"></div>
            <div class="row" id="cmpActs" style="margin-top:8px" hidden><button type="button" class="solid" id="cmpShow">👁️ Show the report on the right</button><button type="button" class="solid" id="cmpCopy">Keep the report as a note</button></div>
            <span class="tip" data-tip="Lines that are the same are skipped; each place that differs is shown with three lines around it. Red is the line as it was, green as it is now. A picture or font folded into the code appears as one long line; it is compared like any other. Two identical files say so in one line."></span>
          </div>
        </details>
        '''
CSS = r'''<style id="cd-9s62-compare-css">
/* 9s62 · the comparison: before in red, after in green, line numbers in the margin, nothing moves */
#fold-compare .cmp-out{max-height:420px;overflow:auto;margin-top:8px;border:1px solid var(--line,rgba(27,107,147,.25));border-radius:10px;background:var(--panel,#fff);font:12px/1.5 var(--cd-mono,ui-monospace,monospace)}
#fold-compare .cmp-out:empty{display:none}
#fold-compare .cmp-h{padding:4px 10px;background:var(--well,rgba(27,107,147,.07));color:var(--accent,#1B6B93);font:600 11.5px/1.4 var(--cd-sans,system-ui,sans-serif);border-top:1px solid var(--line,rgba(27,107,147,.18));position:sticky;top:0}
#fold-compare .cmp-l{display:grid;grid-template-columns:4.5em 4.5em 1fr;gap:0 8px;padding:0 10px;white-space:pre-wrap;overflow-wrap:anywhere}
#fold-compare .cmp-l .n{color:var(--ink2,#6b7580);text-align:right;user-select:none}
#fold-compare .cmp-l.del{background:rgba(190,40,40,.10)} #fold-compare .cmp-l.del .t{color:#8e1d1d}
#fold-compare .cmp-l.add{background:rgba(30,140,70,.12)} #fold-compare .cmp-l.add .t{color:#15602f}
body[data-theme="night"] #fold-compare .cmp-l.del .t{color:#f0a0a0} body[data-theme="night"] #fold-compare .cmp-l.add .t{color:#9fe0b4}
#fold-compare .cmp-more{padding:6px 10px;color:var(--ink2,#6b7580);font:italic 12px var(--cd-serif,Georgia,serif)}
</style>
'''
JS = r'''<script id="cd-9s62-compare-js">
/* 9s62 · COMPARE TWO VERSIONS. Her ask: a version comparison tool, to understand changes between app versions. The two
   sides can be the file on the stage, a copy the library keeps (newest or earlier, for each app), a new app of the Studio,
   or any file from this device. The lines of each are compared: the same run at the head and the foot is skipped, then the
   lines that stand alone in both (patience: a line that appears once on each side anchors the two) pair the files up, and
   what lies between anchors is compared exactly when small, or shown whole as replaced when large. The result is said in
   words first (how many lines, how many places, where the first is), then shown place by place, before in red and after in
   green, three lines of context each. A file of twelve megabytes is seventy thousand lines; this takes well under a second
   for an ordinary edit. Nothing is run and nothing is sent. */
(function(){
  function $(id){ return document.getElementById(id); }
  function fr(){ return document.documentElement.lang==='fr'; }
  function T(en,f){ return fr()?f:en; }
  function esc(t){ return String(t==null?'':t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  var NAMES={cd:'Carpe Diem', forge:'The Forge', inkwell:'Inkwell', ingenium:'Ingenium'};
  /* ---------- the diff ---------- */
  function ids(linesA, linesB){ var map=new Map(), a=new Int32Array(linesA.length), b=new Int32Array(linesB.length), n=0;
    for(var i=0;i<linesA.length;i++){ var k=map.get(linesA[i]); if(k==null){ k=n++; map.set(linesA[i],k); } a[i]=k; }
    for(var j=0;j<linesB.length;j++){ var k2=map.get(linesB[j]); if(k2==null){ k2=n++; map.set(linesB[j],k2); } b[j]=k2; }
    return {a:a,b:b}; }
  /* exact LCS for a small region: returns pairs [i,j] of equal lines */
  function lcsPairs(a,a0,a1,b,b0,b1){ var n=a1-a0, m=b1-b0, L=new Int32Array((n+1)*(m+1)), W=m+1, i, j;
    for(i=n-1;i>=0;i--) for(j=m-1;j>=0;j--) L[i*W+j]= a[a0+i]===b[b0+j] ? L[(i+1)*W+j+1]+1 : Math.max(L[(i+1)*W+j], L[i*W+j+1]);
    var out=[]; i=0; j=0; while(i<n&&j<m){ if(a[a0+i]===b[b0+j]){ out.push([a0+i,b0+j]); i++; j++; } else if(L[(i+1)*W+j]>=L[i*W+j+1]) i++; else j++; }
    return out; }
  /* patience: lines unique on both sides anchor the region; between anchors recurse, exact when small */
  function pairs(a,a0,a1,b,b0,b1,depth){ var out=[];
    while(a0<a1&&b0<b1&&a[a0]===b[b0]){ out.push([a0,b0]); a0++; b0++; }
    var tail=[]; while(a1>a0&&b1>b0&&a[a1-1]===b[b1-1]){ a1--; b1--; tail.push([a1,b1]); }
    if(a0<a1&&b0<b1){ var n=a1-a0, m=b1-b0;
      if(n*m<=250000) out=out.concat(lcsPairs(a,a0,a1,b,b0,b1));
      else if(depth<40){ var ca=new Map(), cb=new Map(), i, k;
        for(i=a0;i<a1;i++){ k=a[i]; ca.set(k,(ca.get(k)||0)+1); }
        for(i=b0;i<b1;i++){ k=b[i]; cb.set(k,(cb.get(k)||0)+1); }
        var posA=new Map(); for(i=a0;i<a1;i++){ k=a[i]; if(ca.get(k)===1&&cb.get(k)===1) posA.set(k,i); }
        var seq=[]; for(i=b0;i<b1;i++){ k=b[i]; if(posA.has(k)) seq.push([posA.get(k),i]); }
        /* the longest run of anchors that keeps its order (an increasing subsequence on the a side) */
        var lis=[], pre=new Int32Array(seq.length), tailIdx=[]; for(i=0;i<seq.length;i++){ var x=seq[i][0], lo=0, hi=tailIdx.length; while(lo<hi){ var mid=(lo+hi)>>1; if(seq[tailIdx[mid]][0]<x) lo=mid+1; else hi=mid; } pre[i]=lo?tailIdx[lo-1]:-1; tailIdx[lo]=i; }
        for(var p=tailIdx.length?tailIdx[tailIdx.length-1]:-1; p>=0; p=pre[p]) lis.push(seq[p]); lis.reverse();
        /* pushed, never concatenated: with sixty thousand anchors a concat per anchor copied the whole list each time (measured: fifteen seconds for the Forge against itself with two edits; now a fraction of a second) */
        if(lis.length){ var pa=a0, pb=b0; lis.forEach(function(an){ var sub=pairs(a,pa,an[0],b,pb,an[1],depth+1); for(var s=0;s<sub.length;s++) out.push(sub[s]); out.push(an); pa=an[0]+1; pb=an[1]+1; }); var rest=pairs(a,pa,a1,b,pb,b1,depth+1); for(var s2=0;s2<rest.length;s2++) out.push(rest[s2]); }
        /* no anchor at all in a large region: shown as replaced whole */ } }
    tail.reverse(); return out.concat(tail); }
  function diff(textA, textB){ var la=textA.split('\n'), lb=textB.split('\n'), t0=Date.now();
    if(textA===textB) return {same:true, linesA:la.length, linesB:lb.length, hunks:[], add:0, del:0, ms:0};
    var id=ids(la,lb), pr=pairs(id.a,0,la.length,id.b,0,lb.length,0);
    /* the hunks: runs of unpaired lines, with three lines of context */
    var ops=[], i=0, j=0; pr.push([la.length, lb.length]);
    pr.forEach(function(p){ while(i<p[0]){ ops.push(['-',i,-1]); i++; } while(j<p[1]){ ops.push(['+',-1,j]); j++; } if(p[0]<la.length){ ops.push([' ',p[0],p[1]]); } i=p[0]+1; j=p[1]+1; });
    var hunks=[], cur=null, add=0, del=0, C=3;
    for(var k=0;k<ops.length;k++){ var o=ops[k]; if(o[0]!==' '){ if(o[0]==='+') add++; else del++; if(!cur){ cur={at:k, ops:[]}; for(var c=Math.max(0,k-C);c<k;c++) cur.ops.push(ops[c]); } cur.ops.push(o); cur.last=k; }
      else if(cur){ if(k-cur.last<=C*2){ cur.ops.push(o); } else { for(var c2=cur.last+1;c2<=Math.min(ops.length-1,cur.last+C);c2++){} hunks.push(cur); cur=null; } } }
    if(cur) hunks.push(cur);
    hunks.forEach(function(h){ while(h.ops.length && h.ops[h.ops.length-1][0]===' ' && h.ops.length>0){ var tailCtx=0; for(var q=h.ops.length-1;q>=0&&h.ops[q][0]===' ';q--) tailCtx++; if(tailCtx>C) h.ops.pop(); else break; } });
    return {same:false, linesA:la.length, linesB:lb.length, hunks:hunks, add:add, del:del, la:la, lb:lb, ms:Date.now()-t0}; }
  /* ---------- the sides ---------- */
  function sides(){ var out=[{k:'stage', t:T('the file on the stage','le fichier sur la scène')}];
    return (window.__forgeLib?(window.__forgeLib.metaCached||window.__forgeLib.meta)().catch(function(){ return {}; }):Promise.resolve({})).then(function(M){ Object.keys(M).sort().forEach(function(id){ var m=M[id]; out.push({k:'lib:'+id, t:(NAMES[m.app]||m.app)+' '+(m.version||'')+(m.slot==='newest'?T(' (newest copy)',' (copie la plus récente)'):T(' (the copy before)',' (la copie d’avant)'))+(m.source==='made'?T(', your version',', votre version'):'')}); });
      return (window.__forgeStudioUI?window.__forgeStudioUI.newApps().catch(function(){ return []; }):Promise.resolve([])); }).then(function(apps){ (apps||[]).forEach(function(a){ out.push({k:'new:'+a.id, t:T('new app: ','nouvelle app : ')+a.name}); }); out.push({k:'file', t:T('a file from this device…','un fichier de cet appareil…')}); return out; }); }
  function fill(){ return sides().then(function(list){ ['cmpA','cmpB'].forEach(function(id){ var s=$(id); if(!s) return; var was=s.value; s.innerHTML=''; list.forEach(function(x){ var o=document.createElement('option'); o.value=x.k; o.textContent=x.t; s.appendChild(o); }); if(was && list.some(function(x){ return x.k===was; })) s.value=was; });
      ['A','B'].forEach(function(s){ if(FILES[s]){ var o=$('cmp'+s).querySelector('option[value="file"]'); if(o) o.textContent=T('file: ','fichier : ')+FILES[s].name; } });
      /* the first pair offered is one app's two copies, never two apps */
      var b=$('cmpB'); if(b && b.value==='stage'){ var pick=null; list.forEach(function(x){ var m=/^lib:(.+):earlier$/.exec(x.k); if(m && !pick && list.some(function(y){ return y.k==='lib:'+m[1]+':newest'; })) pick=m[1]; }); if(pick){ $('cmpA').value='lib:'+pick+':earlier'; b.value='lib:'+pick+':newest'; } } }); }
  /* the fold's own words, in her language */
  function wordsOf(){ var f=$('fold-compare'); if(!f) return; function set(sel,en,fr2){ var e=f.querySelector(sel), v=T(en,fr2); if(e&&e.textContent!==v) e.textContent=v; }
    set('summary .t','🔍 Compare two versions','🔍 Comparer deux versions');
    set('[data-cmp="lede"]','See what changed between two versions of an app: the one on the stage, the copies the Forge keeps (the newest and the one before), a new app of yours, or any file from this device. The Forge says in words what differs, then shows each place, line by line, before and after.','Voyez ce qui a changé entre deux versions d’une app : celle sur la scène, les copies que la Forge garde (la plus récente et celle d’avant), une nouvelle app à vous, ou n’importe quel fichier de cet appareil. La Forge dit en mots ce qui diffère, puis montre chaque endroit, ligne par ligne, avant et après.');
    set('[data-cmp="a"]','Before','Avant'); set('[data-cmp="b"]','After','Après'); set('#cmpGo','🔍 Compare','🔍 Comparer'); set('#cmpShow','👁️ Show the report on the right','👁️ Montrer le rapport à droite'); set('#cmpCopy','Keep the report as a note','Garder le rapport comme note');
    var tip=f.querySelector('.tip'); if(tip) tip.setAttribute('data-tip', T('Lines that are the same are skipped; each place that differs is shown with three lines around it. Red is the line as it was, green as it is now. A picture or font folded into the code appears as one long line; it is compared like any other. Two identical files say so in one line.','Les lignes identiques sont sautées ; chaque endroit qui diffère est montré avec trois lignes autour. Rouge : la ligne telle qu’elle était ; vert : telle qu’elle est maintenant. Une image ou une police repliée dans le code apparaît comme une longue ligne ; elle est comparée comme les autres. Deux fichiers identiques le disent en une ligne.'));
    var st=$('cmpState'); if(st && /^(which two|lesquelles)$/.test(st.textContent.trim())) st.textContent=T('which two','lesquelles'); }
  var FILES={A:null,B:null};
  function textOf(side){ var sel=$('cmp'+side), v=sel.value;
    if(v==='stage'){ var FSu=null; try{ FSu=window.__forgeStudioUI&&window.__forgeStudioUI.state(); }catch(e){} if(FSu&&FSu.newApp&&FSu.newApp.code) return Promise.resolve({name:FSu.newApp.name, text:FSu.newApp.code}); /* a new app of hers on the stage is what the stage shows */
      var sh=window.FORGE&&FORGE.ED&&FORGE.ED.shell; return sh?Promise.resolve({name:(FORGE.ED.shellName||'stage'), text:sh}):Promise.reject(new Error(T('nothing is on the stage','rien n’est sur la scène'))); }
    if(v.indexOf('lib:')===0){ var id=v.slice(4); return window.__forgeLib.bytes(id).then(function(b){ if(!b) throw new Error(T('that copy is no longer kept','cette copie n’est plus gardée')); return {name:sel.options[sel.selectedIndex].textContent, text:new TextDecoder().decode(new Uint8Array(b))}; }); }
    if(v.indexOf('new:')===0){ return new Promise(function(res,rej){ var r=indexedDB.open('forge-studio',2); r.onsuccess=function(){ var d=r.result; var q=d.transaction('apps','readonly').objectStore('apps').get(v.slice(4)); q.onsuccess=function(){ d.close(); if(!q.result) rej(new Error('gone')); else res({name:q.result.name, text:q.result.code||''}); }; q.onerror=function(){ d.close(); rej(q.error); }; }; r.onerror=function(){ rej(r.error); }; }); }
    if(v==='file'){ var f=FILES[side]; if(!f) return Promise.reject(new Error(T('choose the file first','choisissez d’abord le fichier'))); return (f.text?f.text():new Response(f).text()).then(function(t){ return {name:f.name, text:t}; }); }
    return Promise.reject(new Error('?')); }
  var LAST=null;
  function words(r, na, nb){ if(r.same) return T('The two are the same, line for line: ','Les deux sont identiques, ligne pour ligne : ')+r.linesA.toLocaleString()+T(' lines.',' lignes.');
    var places=r.hunks.length, first=r.hunks[0], fl=first?first.ops.filter(function(o){ return o[0]!==' '; })[0]:null, where=fl?(fl[0]==='-'?fl[1]+1:fl[2]+1):0;
    return T('From ','De ')+esc(na)+T(' to ',' à ')+esc(nb)+': '+r.add.toLocaleString()+T(' lines added, ',' lignes ajoutées, ')+r.del.toLocaleString()+T(' removed, in ',' retirées, en ')+places+T(places===1?' place':' places',places===1?' endroit':' endroits')+'. '+T('The first is at line ','Le premier est à la ligne ')+where.toLocaleString()+(fl?': '+esc(String(fl[0]==='-'?r.la[fl[1]]:r.lb[fl[2]]).trim().slice(0,90)):'')+'. '+T('Before: ','Avant : ')+r.linesA.toLocaleString()+T(' lines; after: ',' lignes ; après : ')+r.linesB.toLocaleString()+'.'; }
  function clip(s){ s=String(s); return s.length>400 ? s.slice(0,400)+' …('+(s.length-400).toLocaleString()+T(' more characters',' caractères de plus')+')' : s; }
  function render(r){ var out=$('cmpOut'); out.innerHTML=''; if(r.same) return; var MAX=80, h='';
    r.hunks.slice(0,MAX).forEach(function(hk,i){ var f=hk.ops[0]; h+='<div class="cmp-h">'+T('Place ','Endroit ')+(i+1)+' · '+T('line ','ligne ')+((f[1]>=0?f[1]:f[2])+1).toLocaleString()+'</div>';
      hk.ops.forEach(function(o){ var cls=o[0]==='-'?'del':(o[0]==='+'?'add':'ctx'), t=o[0]==='-'?r.la[o[1]]:(o[0]==='+'?r.lb[o[2]]:r.la[o[1]]);
        h+='<div class="cmp-l '+cls+'"><span class="n">'+(o[1]>=0?o[1]+1:'')+'</span><span class="n">'+(o[2]>=0?o[2]+1:'')+'</span><span class="t">'+(o[0]===' '?'  ':(o[0]+' '))+esc(clip(t))+'</span></div>'; }); });
    if(r.hunks.length>MAX) h+='<div class="cmp-more">'+T('… and ','… et ')+(r.hunks.length-MAX)+T(' more places. Show the report on the right for all of them.',' endroits de plus. Montrez le rapport à droite pour les voir tous.')+'</div>';
    out.innerHTML=h; }
  function report(r, na, nb){ var lines=[T('COMPARISON','COMPARAISON')+' · '+new Date().toLocaleString(), words(r,na,nb).replace(/<[^>]+>/g,'').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&'), ''];
    r.hunks.forEach(function(hk,i){ var f=hk.ops[0]; lines.push('--- '+T('place ','endroit ')+(i+1)+' · '+T('line ','ligne ')+((f[1]>=0?f[1]:f[2])+1)); hk.ops.forEach(function(o){ var t=o[0]==='-'?r.la[o[1]]:(o[0]==='+'?r.lb[o[2]]:r.la[o[1]]); lines.push(o[0]+' '+clip(t)); }); lines.push(''); });
    return lines.join('\n'); }
  function go(){ var A=$('cmpA').value, B=$('cmpB').value; if(A===B && A!=='file'){ $('cmpSum').textContent=T('Choose two different versions.','Choisissez deux versions différentes.'); return; }
    $('cmpSum').textContent=T('Reading…','Lecture…'); $('cmpOut').innerHTML=''; $('cmpActs').hidden=true;
    Promise.all([textOf('A'), textOf('B')]).then(function(x){ $('cmpSum').textContent=T('Comparing…','Comparaison…');
      setTimeout(function(){ try{ var r=diff(x[0].text, x[1].text); LAST={r:r, na:x[0].name, nb:x[1].name}; $('cmpSum').innerHTML=words(r,x[0].name,x[1].name)+' <span class="muted">('+r.ms+' ms)</span>'; render(r); $('cmpActs').hidden=false; try{ FORGE.state('cmpState', r.same?T('the same','identiques'):(r.hunks.length+T(' places',' endroits')), 'ok'); }catch(e){} }catch(e){ $('cmpSum').textContent=T('The comparison could not be made: ','La comparaison n’a pas pu être faite : ')+String(e&&e.message||e); } }, 30); })
    .catch(function(e){ $('cmpSum').textContent=T('Not compared: ','Pas comparé : ')+String(e&&e.message||e); }); }
  function show(){ if(!LAST) return; var txt=report(LAST.r, LAST.na, LAST.nb); var doc='<!DOCTYPE html><meta charset="utf-8"><title>'+esc(T('Comparison','Comparaison'))+'</title><style>body{margin:0;padding:18px;font:13px/1.5 ui-monospace,Menlo,Consolas,monospace;color:#1d1d1f;background:#fff}h1{font:700 18px Georgia,serif;margin:0 0 10px}pre{white-space:pre-wrap;overflow-wrap:anywhere}.d{background:rgba(190,40,40,.10);color:#8e1d1d}.a{background:rgba(30,140,70,.12);color:#15602f}.h{color:#1B6B93;font-weight:600;margin-top:10px}</style><h1>'+esc(T('Comparison','Comparaison'))+'</h1><pre>'+txt.split('\n').map(function(l){ var c=l.indexOf('--- ')===0?'h':(l.charAt(0)==='-'?'d':(l.charAt(0)==='+'?'a':'')); return c?'<span class="'+c+'">'+esc(l)+'</span>':esc(l); }).join('\n')+'</pre>';
    try{ FORGE.showDoc(doc, T('Comparison','Comparaison'), txt, 'file'); }catch(e){} }
  function keep(){ if(!LAST) return; var txt=report(LAST.r, LAST.na, LAST.nb), kept=false; try{ if(window.FORGE&&FORGE.files){ FORGE.files.push({name:'comparison-'+new Date().toISOString().slice(0,10)+'.txt', doc:'<pre>'+esc(txt)+'</pre>', text:txt, kind:'text'}); FORGE.paint(); kept=true; } }catch(e){}
    var cp=(navigator.clipboard&&navigator.clipboard.writeText)?navigator.clipboard.writeText(txt).then(function(){ return true; },function(){ return false; }):Promise.resolve(false);
    cp.then(function(c){ $('cmpSum').insertAdjacentHTML('beforeend',' <b>'+(kept?T('Kept in the Library','Gardé dans la Bibliothèque'):T('Not kept in the Library','Pas gardé dans la Bibliothèque'))+(c?T(', and copied.',', et copié.'):T('. The clipboard was not available here.','. Le presse-papiers n’était pas disponible ici.'))+'</b>'); }); }
  function seat(){ var tr=$('fold-trouble'); if(!tr||$('fold-compare')) return !!$('fold-compare'); tr.insertAdjacentHTML('afterend', ''' + repr(FOLD) + ''');
    $('cmpGo').onclick=go; $('cmpShow').onclick=show; $('cmpCopy').onclick=keep;
    ['A','B'].forEach(function(s){ $('cmp'+s).addEventListener('change', function(){ if(this.value==='file') $('cmpFile'+s).click(); }); $('cmpFile'+s).onchange=function(){ FILES[s]=this.files&&this.files[0]||null; try{ this.value=''; }catch(e){} if(FILES[s]){ var sel=$('cmp'+s), o=sel.querySelector('option[value="file"]'); if(o) o.textContent=T('file: ','fichier : ')+FILES[s].name; } }; });
    $('fold-compare').addEventListener('toggle', function(){ if(this.open) fill(); }); fill(); wordsOf();
    try{ new MutationObserver(wordsOf).observe(document.documentElement,{attributes:true,attributeFilter:['lang']}); }catch(e){}
    window.addEventListener('forge:lib', function(){ if($('fold-compare')&&$('fold-compare').open) fill(); });
    return true; }
  function start(){ if(!seat()) setTimeout(start, 700); }
  window.__forgeCompare={ diff:diff, go:go, fill:fill, last:function(){ return LAST; } };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
</script>
'''
def apply(P):
    P.insert_before('<script id="cd-9s61-studio">', CSS + JS, 'compare block')
