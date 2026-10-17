"""9s62 · HELP THAT FITS HER: how much the Forge explains, chosen once and remembered, with the help card, the walkthrough and a
   line of context as each step opens."""
JS = r'''<script id="cd-9s62-guidance-js">
/* 9s62 · HOW MUCH HELP. Her ask: the walkthrough and the help adapting to skill level, and contextual help. One choice, made
   on the help card of any room or in Settings and kept on this device: "First day" (everything said, and a line of context as
   each step opens), "Finding my way" (the lists, nothing more), "At ease" (the card folded to one line, the walkthrough
   terse). The walkthrough's cards carry a "why" at First day and lose it At ease. The context line is the teaching line
   under the rail, which already speaks as she works: at First day it also speaks when a step of the Editor opens, saying what
   the step is for and what to do first. Nothing is scored; the choice changes nothing but the words. */
(function(){
  function $(id){ return document.getElementById(id); }
  function fr(){ return document.documentElement.lang==='fr'; }
  function T(en,f){ return fr()?f:en; }
  function esc(t){ return String(t==null?'':t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function level(v){ try{ if(v===undefined) return localStorage.getItem('fg:level')||'first'; localStorage.setItem('fg:level', v); }catch(e){ return 'first'; } }
  var LEVELS=[['first', 'First day', 'Premier jour', 'Everything explained, and a line of context as each step opens.', 'Tout expliqué, et une ligne de contexte à l’ouverture de chaque étape.'],
              ['going', 'Finding my way', 'Je trouve mon chemin', 'The lists on each card, nothing more.', 'Les listes de chaque carte, rien de plus.'],
              ['ease', 'At ease', 'À l’aise', 'The cards folded to a line; the walkthrough terse.', 'Les cartes repliées en une ligne ; la visite brève.']];
  var WHY={ '#edAppRow':[ 'Why: the Forge keeps a copy of each of your apps on this device, so a press opens it with no file to find.', 'Pourquoi : la Forge garde une copie de chacune de vos apps sur cet appareil ; une pression l’ouvre sans fichier à chercher.'],
    '#fold-surface':['Why: a named surface is a part the app registered itself; it is the quickest way to rename, hide, reorder or colour. For anything else, step 2, the whole app, reaches every part.', 'Pourquoi : une surface nommée est une partie que l’app a elle-même déclarée ; c’est le chemin le plus court pour renommer, cacher, réordonner ou colorer. Pour le reste, l’étape 2, l’app entière, atteint chaque partie.'],
    '#fold-controls':['Why: an edit here is data, never code. The app reads it when it opens, so nothing can break, and Restore puts it back.', 'Pourquoi : une modification ici est une donnée, jamais du code. L’app la lit à l’ouverture, rien ne peut casser, et Rétablir remet comme avant.'],
    '#fold-ship':['Why: the HTML file is the whole app; the device packages wrap it with the installer each device wants, and GitHub builds the app from them.', 'Pourquoi : le fichier HTML est l’app entière ; les paquets l’enveloppent de l’installateur voulu par chaque appareil, et GitHub construit l’app à partir d’eux.'],
    '#shipAllBtn':['Why: one zip per device, each with its own READ ME FIRST, so no device’s steps are mixed with another’s.', 'Pourquoi : un zip par appareil, chacun avec son LISEZ-MOI, pour ne jamais mêler les étapes d’un appareil à celles d’un autre.'],
    '#zipAppsBtn':['Why: the Library is the memory of the session: everything made here can be downloaded again until the Forge is closed.', 'Pourquoi : la Bibliothèque est la mémoire de la séance : tout ce qui est fait ici se retélécharge jusqu’à la fermeture de la Forge.'],
    '#guideBody':['Why: the Guidebook is the Forge’s own book; its search finds any control by what it does.', 'Pourquoi : le Guide est le livre de la Forge ; sa recherche trouve toute commande par ce qu’elle fait.'] };
  var CTX={ 'fold-file':['Step 1 is the file: the app you are about to change. Choose one of your apps at the top (Editing), or press 📂 to pick any page. The Forge never writes to this file; it makes a new version when you keep one.', 'L’étape 1 est le fichier : l’app que vous allez changer. Choisissez une de vos apps en haut (Édition), ou appuyez sur 📂 pour prendre une page. La Forge n’écrit jamais dans ce fichier ; elle fait une nouvelle version quand vous la gardez.'],
    'fold-studio':['Step 2 is the whole app. Press a page to see it on the right, then ✋ Point at a part and click anything in the preview. Change its words or its look below; the preview follows you, and the Studio says what changed in the code.', 'L’étape 2 est l’app entière. Appuyez sur une page pour la voir à droite, puis ✋ Montrer une partie et cliquez n’importe quoi dans l’aperçu. Changez ses mots ou son aspect dessous ; l’aperçu vous suit, et le Studio dit ce qui a changé dans le code.'],
    'fold-surface':['Step 3 is the quick way: the parts the app named itself (its rail, its door, its top bar). Pick one to rename, hide, reorder or colour its controls in step 4.', 'L’étape 3 est le chemin rapide : les parties que l’app a nommées elle-même (son rail, sa porte, sa barre du haut). Choisissez-en une pour renommer, cacher, réordonner ou colorer ses commandes à l’étape 4.'],
    'fold-controls':['Step 4 changes the surface you picked: Show hides or shows, Words renames, Order moves, Colour paints. Each is one line of data the app reads when it opens.', 'L’étape 4 change la surface choisie : Montrer cache ou montre, Mots renomme, Ordre déplace, Couleur peint. Chacune est une ligne de donnée que l’app lit à l’ouverture.'],
    'fold-ship':['Step 5 is the way out: the edited app as one HTML file, or a zip per device with its installer and a READ ME FIRST. Your edits are already kept; this makes the thing you install.', 'L’étape 5 est la sortie : l’app modifiée en un fichier HTML, ou un zip par appareil avec son installateur et son LISEZ-MOI. Vos modifications sont déjà gardées ; ceci fait ce que vous installez.'],
    'fold-trouble':['Troubleshoot reads the file and the live preview and says what it found, line by line: a cross names the fault and where it stands.', 'Dépannage lit le fichier et l’aperçu vivant et dit ce qu’il a trouvé, ligne par ligne : une croix nomme la faute et où elle est.'],
    'fold-compare':['Compare shows what changed between two versions, in words first, then line by line: red as it was, green as it is.', 'Comparer montre ce qui a changé entre deux versions, en mots d’abord, puis ligne par ligne : rouge comme avant, vert comme maintenant.'],
    'fold-storetest':['Test the store writes to a scratch store and reads back, so a faulty device is named before it costs you work.', 'Tester le stockage écrit dans un stockage d’essai et relit, pour qu’un appareil fautif soit nommé avant qu’il vous coûte du travail.'],
    'fold-a11y':['The screen reader check measures names, pictures, headings, tabs, labels and contrast in every room, and names each fault.', 'La vérification lecteur d’écran mesure noms, images, titres, onglets, étiquettes et contraste dans chaque pièce, et nomme chaque faute.'] };
  function paintChooser(host){ if(!host) return; var lv=level(); host.innerHTML='<span class="fg-lv-l">'+T('How much help:','Combien d’aide :')+'</span>'+LEVELS.map(function(L){ return '<button type="button" class="fg-lv" data-fg-level="'+L[0]+'" aria-pressed="'+(lv===L[0]?'true':'false')+'" title="'+esc(fr()?L[4]:L[3])+'">'+esc(fr()?L[2]:L[1])+'</button>'; }).join(''); }
  function applyLevel(){ var lv=level(); document.documentElement.setAttribute('data-fg-level', lv);
    Array.prototype.forEach.call(document.querySelectorAll('.fg-help'), function(d){ var room=d.getAttribute('data-fg-room'); var ch=d.querySelector('.fg-lv-row'); if(!ch){ ch=document.createElement('div'); ch.className='fg-lv-row'; var body=d.querySelector('.fold-body'); if(body) body.insertBefore(ch, body.firstChild); } paintChooser(ch);
      var s=d.querySelector('summary .s'); if(s) s.textContent = lv==='ease' ? T('at ease','à l’aise') : (lv==='going' ? T('first, then next','d’abord, ensuite') : T('first day: everything said','premier jour : tout est dit'));
      try{ var closed=localStorage.getItem('fg:closed:'+room); if(closed==null){ d.open = lv!=='ease'; } }catch(e){} });
    Array.prototype.forEach.call(document.querySelectorAll('.fg-lv'), function(b){ b.setAttribute('aria-pressed', b.getAttribute('data-fg-level')===lv?'true':'false'); });
    var st=$('fgLevelSettings'); if(st) paintChooser(st); }
  document.addEventListener('click', function(e){ var b=e.target.closest&&e.target.closest('.fg-lv'); if(!b) return; e.preventDefault(); level(b.getAttribute('data-fg-level')); try{ Object.keys(localStorage).forEach(function(k){ if(k.indexOf('fg:closed:')===0) localStorage.removeItem(k); }); }catch(x){} applyLevel();
    var L=LEVELS.filter(function(x){ return x[0]===level(); })[0]; try{ window.__forgeEd.teach('fgLevel',{name:fr()?L[2]:L[1], about:fr()?L[4]:L[3]}); }catch(x){} }, true);
  /* the walkthrough's why, at First day; terse at ease */
  function dressWalk(){ var p=$('fg-walk'); if(!p||p.hidden) return; var lv=level(), body=p.children[1]; if(!body) return; var old=p.querySelector('.fg-why'); if(old) old.remove();
    if(lv==='first'){ var m=/data-fgw="there"/.test(p.innerHTML); var t=p.querySelector('.fg-w-h span'); var n=t?parseInt((t.textContent.match(/(\d+)\s*\//)||[])[1],10):0; var keys=['#edAppRow','#fold-surface','#fold-controls','#fold-ship','#shipAllBtn','#zipAppsBtn','#guideBody']; var w=WHY[keys[n-1]]; if(w){ var d=document.createElement('div'); d.className='fg-why'; d.textContent=fr()?w[1]:w[0]; body.insertAdjacentElement('afterend', d); } } }
  /* the context line: when a step of the Editor opens, at First day */
  function lessons(){ try{ var b=window.__forgeEd; if(!b||lessons.done) return; lessons.done=1;
    Object.keys(CTX).forEach(function(k){ b.lesson('ctx:'+k, function(){ return esc(fr()?CTX[k][1]:CTX[k][0]); }); });
    b.lesson('fgLevel', function(v){ return '<b>'+esc(v.name)+'</b>: '+esc(v.about)+' '+esc(T('Change it on any help card, or in Settings.','Changez-le sur toute carte d’aide, ou dans les Réglages.')); }); }catch(e){} }
  var lastCtx='';
  document.addEventListener('toggle', function(e){ var d=e.target; if(!d||d.tagName!=='DETAILS'||!d.open) return; if(level()!=='first') return; var k=d.id; if(!CTX[k]||lastCtx===k) return; lastCtx=k; try{ var tut=$('tutor'); if(tut && tut.getAttribute('data-on')!=='1'){ tut.setAttribute('data-on','1'); var tb=$('tutorBtn'); if(tb) tb.textContent=T('📘 Hide the line','📘 Masquer la ligne'); } window.__forgeEd.teach('ctx:'+k,{}); }catch(x){} }, true);
  function seatSettings(){ var lay=document.querySelector('#room-settings .page[data-page="layout"] .panel.card'); if(!lay||$('fgLevelCard')) return; lay.insertAdjacentHTML('afterend','<div class="panel card" id="fgLevelCard"><h3>'+T('How much the Forge explains','Combien la Forge explique')+'</h3><p class="muted" style="font-size:13px">'+T('Chosen once, kept on this device, changed any time here or on the help card of any room. Nothing is scored; only the words change.','Choisi une fois, gardé sur cet appareil, changé à tout moment ici ou sur la carte d’aide de toute pièce. Rien n’est noté ; seuls les mots changent.')+'</p><div class="fg-lv-row" id="fgLevelSettings"></div></div>'); paintChooser($('fgLevelSettings')); }
  function start(){ lessons(); applyLevel(); seatSettings();
    try{ new MutationObserver(function(){ clearTimeout(start.t); start.t=setTimeout(function(){ lessons(); applyLevel(); seatSettings(); dressWalk(); }, 150); }).observe(document.body,{childList:true,subtree:true}); }catch(e){}
    try{ new MutationObserver(function(){ applyLevel(); }).observe(document.documentElement,{attributes:true,attributeFilter:['lang']}); }catch(e){} }
  window.__forgeGuidance={ level:level, apply:applyLevel };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', start); else setTimeout(start, 50);
})();
</script>
<style id="cd-9s62-guidance-css">
/* 9s62 · the help level chooser and the walkthrough's why */
.fg-lv-row{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:0 0 10px}
.fg-lv-l{font:600 11px/1.2 var(--cd-sans,system-ui,sans-serif);letter-spacing:.08em;text-transform:uppercase;color:var(--accent,#1B6B93);margin-right:4px}
.fg-lv{font:600 12.5px/1.2 var(--cd-sans,system-ui,sans-serif);padding:5px 12px;border-radius:999px;border:1px solid rgba(23,87,122,.3);background:var(--panel,#fff);color:var(--ink,#1d1d1f);cursor:pointer}
.fg-lv[aria-pressed="true"]{background:var(--accent,#1B6B93);border-color:var(--accent,#1B6B93);color:#fff}
.fg-lv:focus-visible{outline:2px solid var(--accent,#1B6B93);outline-offset:2px}
html[data-fg-level="ease"] .fg-help .fg-cols{font-size:12.5px}
html[data-fg-level="first"] .fg-help .fg-cols li{margin-bottom:3px}
#fg-walk .fg-why{margin-top:8px;padding:6px 10px;border-left:3px solid var(--accent,#1B6B93);background:rgba(27,107,147,.07);border-radius:0 8px 8px 0;font-size:13px;line-height:1.45}
body[data-theme="night"] .fg-lv{background:#1b2027;border-color:rgba(255,255,255,.18);color:#e8e8ea}
body[data-theme="night"] .fg-lv[aria-pressed="true"]{background:#1d5a80;border-color:#1d5a80;color:#fff}
</style>
'''
def apply(P):
    P.insert_before('<script id="cd-9s61-studio">', JS, 'guidance block')
