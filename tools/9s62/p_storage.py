"""9s62 · STORAGE ON THIS DEVICE: a meter, a limit of her own with warnings, tidying of the earlier copies, Clean the library."""
CARD = r'''<div class="panel card" id="storageCard">
          <h3 data-st-h>Storage on this device</h3>
          <p data-st-lede>What the Forge keeps here, how much room it takes, and how much the device still offers. Set a limit of your own if you like; the Forge warns you before it is reached and, if you ask it to, tidies the earlier copies first.</p>
          <div class="st-meter" id="stMeter" role="meter" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-label="Storage used"><div class="st-fill" id="stFill"></div></div>
          <div class="muted" id="stSum" style="font-size:12.5px;margin:6px 0 8px"></div>
          <div id="stLines" class="st-lines"></div>
          <div class="row" style="margin-top:10px;align-items:center;flex-wrap:wrap;gap:8px"><label class="row" style="gap:6px;align-items:center"><span data-st-limit>Keep the Forge under</span><input type="number" id="stLimit" min="50" step="50" inputmode="numeric" style="width:6.5em"> <span>MB</span></label><button type="button" class="solid" id="stLimitSave">Keep this limit</button><button type="button" class="solid" id="stLimitNone">No limit</button></div>
          <label class="row" style="gap:8px;align-items:center;margin-top:6px"><input type="checkbox" id="stAuto"> <span data-st-auto>Tidy by itself when the limit is near: the earlier copies of the apps go first, newest work never</span></label>
          <div class="row" style="margin-top:10px"><button type="button" class="stone solid" id="stClean">🧹 Clean the library</button><button type="button" class="solid" id="stRefresh">Measure again</button></div>
          <div id="stReport" class="muted" role="status" aria-live="polite" style="font-size:12.5px;margin-top:6px"></div>
          <span class="tip" data-tip="The meter reads what the browser reports for this app, and the lines underneath count what the Forge itself keeps: the copies of your apps (two per app at most), the files in Files, the new apps and edits of the Studio, and the small notes in localStorage. Clean the library removes only the earlier copy of each app, the one kept one step back; your newest copies and your files stay."></span>
        </div>
        '''
CSS = r'''<style id="cd-9s62-storage-css">
/* 9s62 · the Storage card (Settings, Backup): a meter, its lines, its warnings */
#storageCard .st-meter{height:12px;border-radius:999px;background:var(--well,rgba(27,107,147,.08));border:1px solid var(--line,rgba(27,107,147,.25));overflow:hidden;margin-top:6px}
#storageCard .st-fill{height:100%;width:0;border-radius:999px;background:var(--accent,#1B6B93);transition:width .4s ease}
#storageCard[data-st-level="warn"] .st-fill{background:#c07a1a}
#storageCard[data-st-level="full"] .st-fill{background:#9c2a2a}
#storageCard .st-lines{display:grid;grid-template-columns:auto 1fr auto;gap:3px 12px;font-size:12.5px;align-items:center}
#storageCard .st-lines .st-k{font-weight:600;white-space:nowrap}
#storageCard .st-lines .st-d{color:var(--ink2,#4a5563);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#storageCard .st-lines .st-v{font-family:var(--cd-mono,ui-monospace,monospace);white-space:nowrap}
#storageCard[data-st-level="warn"] #stSum{color:#8a4b10;font-weight:600}
#storageCard[data-st-level="full"] #stSum{color:#9c2a2a;font-weight:600}
body[data-theme="night"] #storageCard[data-st-level="warn"] #stSum{color:#f0c08a}
body[data-theme="night"] #storageCard[data-st-level="full"] #stSum{color:#f0a0a0}
#storageCard input[type=number]{padding:4px 8px;border-radius:8px;border:1px solid var(--line,rgba(27,107,147,.3));background:var(--panel,#fff);color:inherit}
</style>
'''
JS = r'''<script id="cd-9s62-storage-js">
/* 9s62 · STORAGE MANAGEMENT. Her ask: storage policies that evict old app versions as the limit nears, a limit of her own
   with warnings before it is reached, and a "clean library" that frees space. The measure: navigator.storage.estimate for
   the browser's own reading of this origin, and the Forge's own count of what it keeps (the app library's two copies per app,
   Files, the Studio's new apps and edits, localStorage). The policy: the earlier copies go first, oldest first, and never a
   newest copy, never a file she brought in, never a new app of hers; those she removes herself, by name. Every removal is
   said in plain words, in the card and in the diary. Nothing is sent anywhere. */
(function(){
  function $(id){ return document.getElementById(id); }
  function fr(){ return document.documentElement.lang==='fr'; }
  function T(en,f){ return fr()?f:en; }
  function esc(t){ return String(t==null?'':t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function MB(n){ n=+n||0; return n<1048576 ? (n<1024? n+' B' : (n/1024).toFixed(0)+' KB') : (n/1048576).toFixed(1)+' MB'; }
  function rec(k,v){ try{ if(v===undefined) return localStorage.getItem('forge:storage:'+k); if(v===null) localStorage.removeItem('forge:storage:'+k); else localStorage.setItem('forge:storage:'+k,v); }catch(e){ return null; } }
  var NAMES={cd:'Carpe Diem', forge:'The Forge', inkwell:'Inkwell', ingenium:'Ingenium'};
  function studioSizes(){ return new Promise(function(res){ var out={apps:0, edits:0, list:[]}; try{ if(!window.indexedDB) return res(out); var r=indexedDB.open('forge-studio',2);
      r.onupgradeneeded=function(){ try{ var db=r.result; if(!db.objectStoreNames.contains('apps')) db.createObjectStore('apps',{keyPath:'id'}); if(!db.objectStoreNames.contains('edits')) db.createObjectStore('edits',{keyPath:'id'}); }catch(e){} };
      r.onsuccess=function(){ var d=r.result; try{ var t=d.transaction(['apps','edits'],'readonly'); var c=t.objectStore('apps').openCursor(); c.onsuccess=function(){ var k=c.result; if(k){ var n=(k.value.code||'').length; out.apps+=n; out.list.push({id:k.value.id,name:k.value.name,size:n}); k.continue(); } };
          var c2=t.objectStore('edits').openCursor(); c2.onsuccess=function(){ var k=c2.result; if(k){ try{ out.edits+=JSON.stringify(k.value).length; }catch(e){} k.continue(); } };
          t.oncomplete=function(){ try{ d.close(); }catch(e){} res(out); }; t.onerror=t.onabort=function(){ try{ d.close(); }catch(e){} res(out); }; }catch(e){ try{ d.close(); }catch(x){} res(out); } };
      r.onerror=function(){ res(out); }; r.onblocked=function(){ res(out); }; }catch(e){ res(out); } }); }
  function localSize(){ var n=0; try{ for(var i=0;i<localStorage.length;i++){ var k=localStorage.key(i); n+=(k.length+(localStorage.getItem(k)||'').length)*2; } }catch(e){} return n; }
  function filesSizes(){ try{ return window.__forgeBackup.files().then(function(l){ return l.map(function(r){ return {id:r.id,name:r.name,size:r.size||0}; }); }, function(){ return []; }); }catch(e){ return Promise.resolve([]); } }
  function libSizes(){ try{ return window.__forgeLib.sizes(); }catch(e){ return Promise.resolve({}); } }
  function estimate(){ try{ if(navigator.storage&&navigator.storage.estimate) return navigator.storage.estimate().then(function(e){ return e||{}; }, function(){ return {}; }); }catch(e){} return Promise.resolve({}); }
  var LAST=null, busy=false;
  function measure(quiet){ if(busy) return Promise.resolve(LAST); busy=true;
    return Promise.all([estimate(), libSizes(), filesSizes(), studioSizes()]).then(function(r){ busy=false;
      var est=r[0], lib=r[1], files=r[2], st=r[3], libN=0, libList=[];
      Object.keys(lib).forEach(function(k){ libN+=lib[k].size||0; libList.push(lib[k]); });
      var filesN=files.reduce(function(a,b){ return a+(b.size||0); },0), ls=localSize();
      var own=libN+filesN+st.apps+st.edits+ls;
      LAST={est:est, lib:libList, libN:libN, files:files, filesN:filesN, studio:st, ls:ls, own:own, at:Date.now()};
      paint(); policy(quiet); return LAST; }, function(){ busy=false; return LAST; }); }
  function limitBytes(){ var m=parseInt(rec('limitMB')||'',10); return (m>0)?m*1048576:0; }
  function level(){ if(!LAST) return ''; var lim=limitBytes(), used=LAST.own, quota=(LAST.est&&LAST.est.quota)||0, usage=(LAST.est&&LAST.est.usage)||0;
    var ratio = lim ? used/lim : (quota ? Math.max(usage,used)/quota : 0);
    return ratio>=0.95?'full':(ratio>=0.8?'warn':''); }
  function paint(){ var card=$('storageCard'); if(!card||!LAST) return; var lim=limitBytes(), quota=(LAST.est&&LAST.est.quota)||0, usage=(LAST.est&&LAST.est.usage)||0, used=LAST.own;
    var base=lim||quota||0, pct=base?Math.min(100,Math.round((lim?used:Math.max(usage,used))/base*100)):0, lv=level();
    card.setAttribute('data-st-level', lv); $('stFill').style.width=pct+'%'; var m=$('stMeter'); m.setAttribute('aria-valuenow',String(pct));
    var sum = T('The Forge keeps ','La Forge garde ')+MB(used)+T(' here',' ici')
      +(lim?T(' of the ',' sur les ')+MB(lim)+T(' you allow',' que vous autorisez'):'')
      +(quota?T('. The browser reports ','. Le navigateur annonce ')+MB(usage)+T(' used of about ',' utilisés sur environ ')+MB(quota)+T(' it offers this app.',' offerts à cette app.'):'.')
      +(lv==='full'?T(' Nearly full: clean the library, or raise the limit.',' Presque plein : nettoyez la bibliothèque, ou relevez la limite.'):(lv==='warn'?T(' Getting close: a good moment to clean the library.',' Ça se remplit : bon moment pour nettoyer la bibliothèque.'):''));
    $('stSum').textContent=sum;
    var L=$('stLines'); L.innerHTML='';
    function line(k,d,v){ L.insertAdjacentHTML('beforeend','<span class="st-k">'+esc(k)+'</span><span class="st-d">'+esc(d)+'</span><span class="st-v">'+esc(v)+'</span>'); }
    var byApp={}; LAST.lib.forEach(function(x){ (byApp[x.app]=byApp[x.app]||[]).push(x); });
    var apps=Object.keys(byApp); if(!apps.length) line(T('App copies','Copies des apps'), T('no copy kept yet','aucune copie gardée'), MB(0));
    apps.forEach(function(a){ var l=byApp[a], n=l.filter(function(x){ return x.slot==='newest'; })[0], e=l.filter(function(x){ return x.slot==='earlier'; })[0];
      line(NAMES[a]||a, (n?T('newest ','la plus récente ')+(n.version||'')+(n.source==='made'?T(' (your version)',' (votre version)'):''):'')+(e?T(' · earlier ',' · précédente ')+(e.version||''):''), MB(l.reduce(function(s,x){ return s+(x.size||0); },0))); });
    line(T('Files','Fichiers'), LAST.files.length+T(' kept in Files',' gardés dans Fichiers'), MB(LAST.filesN));
    line(T('New apps','Nouvelles apps'), LAST.studio.list.length+T(' made in the Studio',' faites dans le Studio')+(LAST.studio.edits?T(', and their edits',', et leurs modifications'):''), MB(LAST.studio.apps+LAST.studio.edits));
    line(T('Settings and notes','Réglages et notes'), T('the small store (localStorage)','la petite mémoire (localStorage)'), MB(LAST.ls));
    var li=$('stLimit'); if(li&&document.activeElement!==li) li.value=lim?String(Math.round(lim/1048576)):'';
    var au=$('stAuto'); if(au) au.checked=rec('auto')==='1';
    var h=card.querySelector('[data-st-h]'); if(h) h.textContent=T('Storage on this device','Stockage sur cet appareil');
    var ld=card.querySelector('[data-st-lede]'); if(ld) ld.textContent=T('What the Forge keeps here, how much room it takes, and how much the device still offers. Set a limit of your own if you like; the Forge warns you before it is reached and, if you ask it to, tidies the earlier copies first.','Ce que la Forge garde ici, la place que cela prend, et ce que l’appareil offre encore. Fixez une limite à vous si vous voulez ; la Forge prévient avant qu’elle soit atteinte et, si vous le demandez, range d’abord les copies précédentes.');
    var ll=card.querySelector('[data-st-limit]'); if(ll) ll.textContent=T('Keep the Forge under','Garder la Forge sous');
    var la=card.querySelector('[data-st-auto]'); if(la) la.textContent=T('Tidy by itself when the limit is near: the earlier copies of the apps go first, newest work never','Ranger seule quand la limite approche : les copies précédentes des apps partent d’abord, jamais le travail le plus récent');
    $('stLimitSave').textContent=T('Keep this limit','Garder cette limite'); $('stLimitNone').textContent=T('No limit','Sans limite'); $('stClean').textContent=T('🧹 Clean the library','🧹 Nettoyer la bibliothèque'); $('stRefresh').textContent=T('Measure again','Mesurer de nouveau'); }
  function report(t,warn){ var r=$('stReport'); if(r){ r.textContent=t; r.style.color=warn?'#9c2a2a':''; } }
  function diary(t){ try{ if(window.FORGE&&FORGE.diary) FORGE.diary('storage',t); }catch(e){} }
  /* the earlier copies, oldest first; none of the newest */
  function earlierCopies(){ return (LAST?LAST.lib:[]).filter(function(x){ return x.slot==='earlier'; }).sort(function(a,b){ return (a.at||0)-(b.at||0); }); }
  function dropList(list, why){ var freed=0, names=[], p=Promise.resolve();
    list.forEach(function(x){ p=p.then(function(){ return window.__forgeLib.drop(x.app,'earlier').then(function(){ freed+=x.size||0; names.push((NAMES[x.app]||x.app)+' '+(x.version||'')); }, function(){}); }); });
    return p.then(function(){ return {freed:freed, names:names}; }); }
  function clean(){ if(!LAST){ return measure().then(clean); } var list=earlierCopies();
    if(!list.length){ report(T('Nothing to clean: no earlier copy is kept. The newest copies, your files and your new apps are never removed here; remove one by name where it lives.','Rien à nettoyer : aucune copie précédente n’est gardée. Les copies les plus récentes, vos fichiers et vos nouvelles apps ne sont jamais retirés ici ; retirez-en un par son nom, là où il vit.')); return Promise.resolve(); }
    if(!confirm(T('Remove the earlier copy of '+list.map(function(x){ return NAMES[x.app]||x.app; }).join(', ')+'? The newest copy of each app stays. This frees about '+MB(list.reduce(function(s,x){ return s+(x.size||0); },0))+'.','Retirer la copie précédente de '+list.map(function(x){ return NAMES[x.app]||x.app; }).join(', ')+' ? La copie la plus récente de chaque app reste. Cela libère environ '+MB(list.reduce(function(s,x){ return s+(x.size||0); },0))+'.'))) return Promise.resolve();
    return dropList(list).then(function(r){ var t=T('Cleaned: ','Nettoyé : ')+(r.names.join(', ')||T('nothing','rien'))+T(' removed, about ',' retirée, environ ')+MB(r.freed)+T(' freed. The newest copies stay.',' libérés. Les copies les plus récentes restent.'); report(t); diary(t); return measure(true); }); }
  /* the policy: when she asked for it and the limit is near, the earlier copies go, oldest first, until there is room */
  var toldAt=0;
  function policy(quiet){ if(!LAST) return; var lim=limitBytes(), lv=level(); if(!lv) return;
    if(rec('auto')==='1' && lim){ var list=earlierCopies(), need=LAST.own-lim*0.8, take=[], sum=0;
      for(var i=0;i<list.length && sum<need;i++){ take.push(list[i]); sum+=list[i].size||0; }
      if(take.length){ dropList(take).then(function(r){ var t=T('The limit was near, so the Forge tidied by itself: the earlier copy of ','La limite approchait : la Forge a rangé seule la copie précédente de ')+r.names.join(', ')+T(' removed, about ',' retirée, environ ')+MB(r.freed)+T(' freed.',' libérés.'); report(t); diary(t); try{ if(window.__forgeLibPaint) window.__forgeLibPaint(); }catch(e){} measure(true); }); return; } }
    if(!quiet || Date.now()-toldAt>600000){ toldAt=Date.now(); report(lv==='full'?T('Storage is nearly full. Press Clean the library, remove files you no longer need in Files, or raise the limit.','Le stockage est presque plein. Appuyez sur Nettoyer la bibliothèque, retirez dans Fichiers ce dont vous n’avez plus besoin, ou relevez la limite.'):T('Storage is getting close to its limit.','Le stockage approche de sa limite.'), lv==='full'); } }
  function wire(){ var card=$('storageCard'); if(!card||card.__wired) return; card.__wired=true;
    $('stRefresh').onclick=function(){ report(T('Measuring…','Mesure…')); measure().then(function(){ if(!level()) report(T('Measured just now.','Mesuré à l’instant.')); }); };
    $('stClean').onclick=function(){ clean(); };
    $('stLimitSave').onclick=function(){ var v=parseInt($('stLimit').value,10); if(!(v>=50)){ report(T('A limit is a whole number of megabytes, 50 or more.','Une limite est un nombre entier de mégaoctets, 50 ou plus.'),true); return; } rec('limitMB',String(v)); report(T('Kept: the Forge will warn you as it nears ','Gardé : la Forge préviendra en approchant de ')+v+' MB.'); diary(T('limit set to ','limite fixée à ')+v+' MB'); measure(); };
    $('stLimitNone').onclick=function(){ rec('limitMB',null); $('stLimit').value=''; report(T('No limit of your own; the browser’s own room is the measure.','Pas de limite à vous ; la place du navigateur sert de mesure.')); measure(); };
    $('stAuto').onchange=function(){ rec('auto',this.checked?'1':'0'); report(this.checked?T('The Forge will tidy the earlier copies by itself when the limit is near.','La Forge rangera seule les copies précédentes quand la limite approchera.'):T('The Forge will only warn; nothing is removed unless you press Clean.','La Forge ne fera que prévenir ; rien n’est retiré sans que vous appuyiez sur Nettoyer.')); if(this.checked) measure(); }; }
  function seat(){ var rc=$('recoverCard'); if(!rc||$('storageCard')) return !!$('storageCard'); rc.insertAdjacentHTML('beforebegin', ''' + repr(CARD) + '''); wire(); return true; }
  function start(){ if(!seat()){ setTimeout(start,700); return; }
    setTimeout(function(){ measure(true); }, 2500);
    /* measured again when the library changes, when Settings opens, and every ten minutes while the Forge is open */
    try{ var old=window.__forgeLibPaint; window.__forgeLibPaint=function(){ try{ if(old) old.apply(this,arguments); }catch(e){} clearTimeout(start.t); start.t=setTimeout(function(){ measure(true); },1500); }; }catch(e){}
    document.addEventListener('click', function(e){ var b=e.target.closest&&e.target.closest('[data-room="settings"], .nav-btn'); if(b && /settings|réglages/i.test(b.textContent||'')) setTimeout(function(){ measure(true); },300); }, true);
    setInterval(function(){ measure(true); }, 600000);
    try{ new MutationObserver(function(){ paint(); }).observe(document.documentElement,{attributes:true,attributeFilter:['lang']}); }catch(e){} }
  window.__forgeStorage={ measure:measure, clean:clean, last:function(){ return LAST; }, level:level, limit:limitBytes };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
</script>
'''
def apply(P):
    P.insert_before('<script id="cd-9s61-studio">', CSS + JS, 'storage block')
    # the diary, reachable by name for the Storage card and the backup
    P.replace_once("remount:function(){ if(ED.shell){ mountShellPreview(); return true; } return false; }};",
                   "remount:function(){ if(ED.shell){ mountShellPreview(); return true; } return false; }, diary:function(k,t){ diary(k,t); }, showDoc:function(d,n,t,k){ showDoc(d,n,t,k); }};", 'FORGE diary/showDoc')
