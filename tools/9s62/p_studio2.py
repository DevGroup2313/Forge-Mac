"""9s62 · THE STUDIO, FURTHER: a part carried from one app into another, a block of her own HTML, a new app removed by name,
   and a plain line when the hand inside the stage is not answering."""
AGENT_ADD = r'''      case 'outer': { if(!SEL) return null; var c=SEL.cloneNode(true); try{ c.removeAttribute('data-fs'); Array.prototype.forEach.call(c.querySelectorAll('[data-fs]'),function(x){ x.removeAttribute('data-fs'); }); var hl=c.querySelector('#forge-studio-hl'); if(hl) hl.remove(); }catch(e){} return {html:c.outerHTML.slice(0,200000), label:labelOf(SEL)}; }
'''
JS = r'''<script id="cd-9s62-studio2-js">
/* 9s62 · THE STUDIO, FURTHER. Her ask: to edit, customise, rearrange or build entirely new apps inside the Forge, and to make
   new apps from the code of her four. Three ways are added to the panel of step 2:
     · "📋 Copy this part" takes the part she pointed at (its HTML, as the running app has it) into the Forge's own pocket, on
       this device, and "📥 Paste the copied part after it" puts it into any app, after any part: a card from Carpe Diem can
       stand in Ingenium. Pasted HTML is data: the applier takes out scripts and handlers before it draws it, so nothing runs.
     · "➕ A block of my own" opens a small box for her own HTML (a heading, a paragraph, a list), placed after the part.
     · Every new app in the list of step 5 can be removed by name, with a question first; nothing else is touched.
   And the head of the panel says plainly when the hand inside the stage is not answering, and what to do. */
(function(){
  function $(id){ return document.getElementById(id); }
  function fr(){ return document.documentElement.lang==='fr'; }
  function T(en,f){ return fr()?f:en; }
  function esc(t){ return String(t==null?'':t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  function UI(){ return window.__forgeStudioUI||null; }
  function pocket(v){ try{ if(v===undefined) return JSON.parse(localStorage.getItem('forge:studio:pocket')||'null'); localStorage.setItem('forge:studio:pocket', JSON.stringify(v)); }catch(e){ return null; } }
  function cleanHtml(h){ var d=document.createElement('div'); d.innerHTML=String(h||''); Array.prototype.forEach.call(d.querySelectorAll('script,iframe,object,embed,link,meta,style'),function(x){ x.remove(); });
    Array.prototype.forEach.call(d.querySelectorAll('*'),function(x){ for(var i=x.attributes.length-1;i>=0;i--){ var a=x.attributes[i]; if(/^on/i.test(a.name)||/^\s*javascript:/i.test(a.value)||a.name==='id') x.removeAttribute(a.name); } }); return d.innerHTML; }
  function say(t,k){ var n=$('fsSay'); if(n){ n.textContent=t; n.className='fs-say'+(k?' '+k:''); } }
  function paintPocket(){ var p=pocket(), b=$('fsPaste'); if(!b) return; b.disabled=!p; b.title=p?(T('Paste: ','Coller : ')+p.label+T(' (from ',' (de ')+p.from+')'):T('Nothing copied yet','Rien de copié'); b.textContent=p?T('📥 Paste the copied part after it','📥 Coller la partie copiée après'):T('📥 Paste (nothing copied yet)','📥 Coller (rien de copié)'); }
  function addKeys(){ var acts=document.querySelector('#fsSel .fs-acts'); if(!acts||acts.querySelector('#fsCopyPart')) return;
    acts.insertAdjacentHTML('beforeend','<button type="button" class="solid" id="fsCopyPart">📋 '+T('Copy this part','Copier cette partie')+'</button><button type="button" class="solid" id="fsPaste"></button><button type="button" class="solid" id="fsOwnBlock">➕ '+T('A block of my own','Un bloc à moi')+'</button>');
    paintPocket();
    $('fsCopyPart').onclick=function(){ var ui=UI(); if(!ui||!ui.state().live||!ui.state().sel){ say(T('Point at a part first.','Montrez d’abord une partie.'),'warn'); return; }
      ui.rpc('outer').then(function(r){ if(!r||!r.html){ say(T('That part could not be copied.','Cette partie n’a pas pu être copiée.'),'warn'); return; } var from=(function(){ try{ return ui.state().newApp?ui.state().newApp.name:({cd:'Carpe Diem',forge:'The Forge',inkwell:'Inkwell',ingenium:'Ingenium'}[window.__forgeEd.app()]||T('the app','l’app')); }catch(e){ return ''; } })();
        pocket({html:cleanHtml(r.html), label:r.label, from:from, at:Date.now()}); paintPocket(); say(T('Copied: ','Copié : ')+r.label+T('. Open any app, point at a part, and paste it after that part.','. Ouvrez n’importe quelle app, montrez une partie, et collez après elle.'),'ok'); try{ window.__forgeEd.teach('fsCopied',{label:r.label}); }catch(e){} },function(){ say(T('That part could not be copied.','Cette partie n’a pas pu être copiée.'),'warn'); }); };
    $('fsPaste').onclick=function(){ var ui=UI(), p=pocket(); if(!p){ say(T('Nothing is copied yet.','Rien n’est copié.'),'warn'); return; } if(!ui||!ui.state().sel){ say(T('Point at the part to paste after.','Montrez la partie après laquelle coller.'),'warn'); return; }
      ui.record('html','',p.html,{label:p.label}); say(T('Pasted after it: ','Collé après : ')+p.label+T(', from ',', de ')+p.from+T('. It is data in this app now: words and looks, never its old script.','. C’est une donnée de cette app maintenant : des mots et un aspect, jamais son ancien script.'),'ok'); try{ window.__forgeEd.teach('fsPasted',{label:p.label, from:p.from}); }catch(e){} };
    $('fsOwnBlock').onclick=function(){ var ui=UI(); if(!ui||!ui.state().sel){ say(T('Point at the part to put the block after.','Montrez la partie après laquelle mettre le bloc.'),'warn'); return; }
      var box=$('fsOwnBox'); if(!box){ acts.insertAdjacentHTML('afterend','<div id="fsOwnBox" class="fs-acts" style="flex-direction:column;align-items:stretch"><textarea id="fsOwnHtml" rows="4" spellcheck="false" style="width:100%;box-sizing:border-box;font:12.5px/1.5 var(--cd-mono,ui-monospace,monospace);padding:8px 10px;border-radius:8px;border:1px solid var(--line,rgba(16,42,58,.2));background:var(--panel,#fff);color:inherit" placeholder="'+esc(T('<h3>My heading</h3>\n<p>My words.</p>','<h3>Mon titre</h3>\n<p>Mes mots.</p>'))+'"></textarea><div class="fs-acts"><button type="button" class="solid fs-prime" id="fsOwnGo">'+T('Put the block after it','Mettre le bloc après')+'</button><button type="button" class="fs-mini" id="fsOwnX">'+T('Close','Fermer')+'</button></div></div>'); box=$('fsOwnBox');
        $('fsOwnGo').onclick=function(){ var v=$('fsOwnHtml').value.trim(); if(!v){ $('fsOwnHtml').focus(); return; } var ui2=UI(); if(!ui2||!ui2.state().sel) return; ui2.record('html','',cleanHtml(v),{label:T('a block of your own','un bloc à vous')}); say(T('Your block stands after the part. Scripts and handlers, if any, were taken out: a block is data.','Votre bloc est après la partie. Les scripts et gestionnaires, s’il y en avait, ont été retirés : un bloc est une donnée.'),'ok'); try{ window.__forgeEd.teach('fsBlock',{}); }catch(e){} };
        $('fsOwnX').onclick=function(){ box.remove(); }; }
      $('fsOwnHtml').focus(); }; }
  /* the hand's silence, said */
  function hand(){ var ui=UI(), who=$('fsWho'); if(!ui||!who) return; var st=ui.state(), f=$('frame'), has=f&&(f.getAttribute('src')||f.hasAttribute('srcdoc')), line=$('fsHandLine');
    if(has && !st.live){ if(!line){ var say0=$('fsSay'); if(say0){ say0.insertAdjacentHTML('afterend','<div id="fsHandLine" class="fs-say warn" role="status"></div>'); line=$('fsHandLine'); } }
      if(line){ var w=T('The app on the stage is not answering the Studio yet. An app that is still starting answers in a moment; if this line stays, press ↻ Look for pages again, or choose the file again in step 1.','L’app sur la scène ne répond pas encore au Studio. Une app qui démarre répond dans un instant ; si cette ligne reste, appuyez sur ↻ Chercher de nouveau les pages, ou choisissez de nouveau le fichier à l’étape 1.'); if(line.textContent!==w) line.textContent=w; } }
    else if(line) line.remove(); }
  /* a new app removed by name */
  function newAppDel(id){ return new Promise(function(res,rej){ try{ var r=indexedDB.open('forge-studio',2); r.onsuccess=function(){ var d=r.result; var t=d.transaction(['apps','edits'],'readwrite'); t.objectStore('apps').delete(id); try{ t.objectStore('edits').delete('new:'+id); }catch(e){} t.oncomplete=function(){ d.close(); res(true); }; t.onerror=t.onabort=function(){ var e=t.error; d.close(); rej(e); }; }; r.onerror=function(){ rej(r.error); }; }catch(e){ rej(e); } }); }
  function removeKeys(){ var box=$('fsNewList'); if(!box) return; Array.prototype.forEach.call(box.querySelectorAll('.fs-row'), function(r){ if(r.querySelector('.fs-del')) return; var t=r.querySelector('.fs-row-t'); if(!t) return; var name=(t.textContent||'').replace(/\s·\s[\d.,]+\s*KB$/,'');
      var b=document.createElement('button'); b.type='button'; b.className='fs-mini fs-del'; b.textContent=T('Remove','Retirer'); b.title=T('Remove this new app from this device','Retirer cette nouvelle app de cet appareil');
      b.onclick=function(){ var ui=UI(); if(!ui) return; ui.newApps().then(function(list){ var a=list.filter(function(x){ return x.name===name; })[0]; if(!a){ say(T('That app is no longer in the list.','Cette app n’est plus dans la liste.'),'warn'); return; }
        if(!confirm(T('Remove the new app "'+a.name+'" from this device? Download it first if you want to keep a copy.','Retirer la nouvelle app « '+a.name+' » de cet appareil ? Téléchargez-la d’abord si vous voulez en garder une copie.'))) return;
        newAppDel(a.id).then(function(){ var st=ui.state(); if(st.newApp&&st.newApp.id===a.id){ try{ $('fsLeave').click(); }catch(e){} } say(T('Removed: ','Retirée : ')+a.name+'.','ok'); try{ FORGE.diary('studio', T('removed the new app ','a retiré la nouvelle app ')+a.name); }catch(e){} try{ var lv=$('fsLeave'); }catch(e){} refreshList(); try{ if(window.__forgeStorage) window.__forgeStorage.measure(true); }catch(e){} },function(e){ say(T('It could not be removed: ','Impossible de la retirer : ')+String(e&&e.message||e),'warn'); }); }); };
      r.appendChild(b); }); }
  function refreshList(){ var ui=UI(); if(!ui) return; try{ ui.newApps().then(function(list){ var box=$('fsNewList'); if(!box) return; /* repaint as the Studio does, then add the keys */ var ev=new Event('fs-refresh'); box.innerHTML=''; if(!list.length){ var q=document.createElement('div'); q.className='fs-quiet'; q.textContent=T('No new apps yet.','Pas encore de nouvelle app.'); box.appendChild(q); return; }
      list.sort(function(a,b){ return b.at-a.at; }).forEach(function(x){ var r=document.createElement('div'); r.className='fs-row'; var s=document.createElement('span'); s.className='fs-row-t'; s.textContent=x.name+' · '+Math.round(x.size/1024)+' KB'; r.appendChild(s);
        var o=document.createElement('button'); o.className='solid'; o.type='button'; o.textContent=T('Open','Ouvrir'); o.onclick=function(){ ui.newApps().then(function(){ /* the Studio's own opener */ try{ window.__forgeStudioOpenNew(x.id); }catch(e){} }); }; r.appendChild(o);
        var dl=document.createElement('button'); dl.className='solid'; dl.type='button'; dl.textContent=T('Download','Télécharger'); dl.onclick=function(){ try{ window.__forgeStudioDownloadNew(x.id); }catch(e){} }; r.appendChild(dl);
        box.appendChild(r); }); removeKeys(); }); }catch(e){} }
  /* the Studio's lessons for the new keys */
  function lessons(){ try{ var b=window.__forgeEd; if(!b||lessons.done) return; lessons.done=1;
    b.lesson('fsCopied', function(v){ return T('You copied ','Vous avez copié ')+esc(v.label)+T('. In the code a part is a run of HTML: its opening tag, everything inside, its closing tag. The Forge keeps that run in its pocket on this device until you paste it.','. Dans le code, une partie est un morceau de HTML : sa balise ouvrante, tout ce qui est dedans, sa balise fermante. La Forge garde ce morceau dans sa poche sur cet appareil jusqu’à ce que vous le colliez.'); });
    b.lesson('fsPasted', function(v){ return T('You pasted ','Vous avez collé ')+esc(v.label)+T(' from ',' de ')+esc(v.from)+T(' into this app. Its words and shape came with it; its old script did not, because a part pasted as data must never run. Its colours come from this app’s own CSS now.',' dans cette app. Ses mots et sa forme sont venus ; son ancien script non, car une partie collée comme donnée ne doit jamais s’exécuter. Ses couleurs viennent maintenant du CSS de cette app.'); });
    b.lesson('fsBlock', function(){ return T('A block of your own is HTML you wrote: a tag, words, a closing tag. The applier draws it after the part, every time the app opens.','Un bloc à vous est du HTML que vous avez écrit : une balise, des mots, une balise fermante. L’applicateur le dessine après la partie, chaque fois que l’app s’ouvre.'); }); }catch(e){} }
  function watch(){ var fold=$('fold-studio'); if(!fold){ setTimeout(watch,700); return; } lessons();
    try{ new MutationObserver(function(ms){ if(ms.every(function(m){ var t=m.target; return t&&t.closest&&t.closest('#fsHandLine,#fsOwnBox,.fs-del'); })) return; addKeys(); hand(); }).observe(fold,{childList:true,subtree:true}); }catch(e){}
    addKeys(); hand(); setInterval(hand, 2500);
    var nl=$('fsNewList'); if(nl){ try{ new MutationObserver(function(){ if(!nl.querySelector('.fs-del') && nl.querySelector('.fs-row')) removeKeys(); }).observe(nl,{childList:true}); }catch(e){} removeKeys(); } }
  window.__forgeStudio2={ pocket:pocket, refreshList:refreshList, clean:cleanHtml };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', watch); else watch();
})();
</script>
'''
def apply(P):
    # the hand answers 'outer': the part's HTML, for the pocket (both copies of the agent literal)
    old = "      case 'reload': setTimeout(function(){ try{ location.reload(); }catch(e){} },0); return true;\\n"
    new = old + "      case 'outer': { if(!SEL) return null; var c=SEL.cloneNode(true); try{ c.removeAttribute('data-fs'); Array.prototype.forEach.call(c.querySelectorAll('[data-fs]'),function(x){ x.removeAttribute('data-fs'); }); var hl=c.querySelector('#forge-studio-hl'); if(hl) hl.remove(); }catch(e){} return {html:c.outerHTML.slice(0,200000), label:labelOf(SEL)}; }\\n"
    P.replace_all(old, new, 'agent outer', expect=2)
    # the Studio describes an html edit and explains it
    P.replace_once("function describe(x){ var what={text:T('words','mots'),attr:x.prop,hide:x.value?T('hidden','caché'):T('shown','montré'),move:x.where==='before'?T('moved earlier','avancé'):T('moved later','reculé'),dup:T('a copy','une copie')}[x.kind];",
                   "function describe(x){ var what={text:T('words','mots'),attr:x.prop,hide:x.value?T('hidden','caché'):T('shown','montré'),move:x.where==='before'?T('moved earlier','avancé'):T('moved later','reculé'),dup:T('a copy','une copie'),html:T('a block after it','un bloc après')+(x.label?' ('+x.label+')':'')}[x.kind];", 'describe html')
    P.replace_once("  else if(kind==='dup'){ words=T('You made a copy. In HTML a copy is the same element written twice; the second one is yours to change.','Vous avez fait une copie. En HTML, c’est le même élément écrit deux fois ; la seconde est à vous.'); code=''; }",
                   "  else if(kind==='dup'){ words=T('You made a copy. In HTML a copy is the same element written twice; the second one is yours to change.','Vous avez fait une copie. En HTML, c’est le même élément écrit deux fois ; la seconde est à vous.'); code=''; }\n  else if(kind==='html'){ words=T('You put a block of HTML after the part. The applier draws it as data each time the app opens; a script inside it would be taken out, so it can only be words and shape.','Vous avez mis un bloc de HTML après la partie. L’applicateur le dessine comme donnée à chaque ouverture ; un script dedans serait retiré, il ne peut donc être que mots et forme.'); code=esc(String(value||'').slice(0,300)); }", 'explain html')
    # the Studio's own openers for a new app, by id, for the refreshed list
    P.replace_once("window.__forgeStudioUI={ state:function(){ return FS; },", "window.__forgeStudioOpenNew=function(id){ newAppGet(id).then(function(a){ if(a) openNewApp(a); }); }; window.__forgeStudioDownloadNew=function(id){ newAppGet(id).then(function(a){ if(a) download(a.name.replace(/[^\\w .-]+/g,'').trim().replace(/\\s+/g,'_')+'.html',a.code); }); };\nwindow.__forgeStudioUI={ state:function(){ return FS; },", 'studio openers')
    # the html edit kind is valid data, with its own label
    P.replace_once("  if(same) same.value=value; else { var ne={id:'e'+Date.now().toString(36)+(FS.seq++), k:s.k, sel:s.sel, kind:kind, prop:prop||'', value:value, label:s.label, at:Date.now()}; if(s.dup) ne.dup=s.dup; if(extra) for(var x in extra) ne[x]=extra[x]; FS.edits.push(ne); }",
                   "  if(same&&kind!=='html') same.value=value; else { var ne={id:'e'+Date.now().toString(36)+(FS.seq++), k:s.k, sel:s.sel, kind:kind, prop:prop||'', value:value, label:s.label, at:Date.now()}; if(s.dup) ne.dup=s.dup; if(extra) for(var x in extra) ne[x]=extra[x]; FS.edits.push(ne); }", 'record html kind')
    P.replace_once("  var same=FS.edits.filter(function(x){ return x.k===s.k&&x.kind===kind&&(x.prop||'')===(prop||'')&&kind!=='move'&&kind!=='dup'; })[0];",
                   "  var same=FS.edits.filter(function(x){ return x.k===s.k&&x.kind===kind&&(x.prop||'')===(prop||'')&&kind!=='move'&&kind!=='dup'&&kind!=='html'; })[0];", 'record html same')
    P.insert_before('<script id="cd-9s61-studio">', JS, 'studio2 block')
