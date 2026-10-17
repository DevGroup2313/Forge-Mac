"""9s62 · THE EDITING PANEL: each app under its own seal, one row each, never cut off."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))

def apply(P):
    _sp = [os.path.join(HERE, 'seals', 'seals.json'), os.path.join(HERE, '..', 'seals', 'seals.json')]
    seals = json.load(open([p for p in _sp if os.path.exists(p)][0], encoding='utf-8'))
    data = {'cd': {'day': seals['cd_day'], 'night': seals['cd_night']},
            'inkwell': {'day': seals['inkwell_day'], 'night': seals['inkwell_night']},
            'ingenium': {'day': seals['ingenium_day'], 'night': seals['ingenium_night']}}
    css = r'''<style id="cd-9s62-appseals-css">
/* 9s62 · THE EDITING PANEL, EACH APP UNDER ITS OWN SEAL. Measured on 9s61: the switch's five keys sat in a two-column grid with
   a small round crop of whatever icon the app's preview had last given (a flat PNG taken from its apple-touch-icon), so the
   seals were the wrong design and the wrong look by day and by night, and on a short screen the panel's foot, with its last
   keys, ran below the window. Now: one row per app, its own seal as the app itself draws it (Carpe Diem 1051's, Inkwell 7.42's,
   Ingenium 3.2's, each with a day face and a night face; the Forge's drawn live by its own seal), the name beside it, and a
   small line saying which copy this device keeps. The panel never runs past the window: it scrolls instead. */
html:not(#hd1):not(#hd2):not(#hd3):not(#hd4):not(#hd5):not(#hd6):not(#hd7) body.forge-app .hd-panel #edAppRow > #edAppSeg{display:flex !important;flex-direction:column !important;gap:4px !important;grid-template-columns:none !important;padding:4px !important;width:100% !important;max-width:100% !important;box-sizing:border-box !important}
html:not(#hd1):not(#hd2):not(#hd3):not(#hd4):not(#hd5):not(#hd6):not(#hd7) body.forge-app .hd-panel #edAppRow > #edAppSeg > button{display:flex !important;align-items:center !important;justify-content:flex-start !important;gap:10px !important;width:100% !important;min-height:42px !important;padding:5px 10px 5px 8px !important;border-radius:10px !important;text-align:left !important;white-space:nowrap !important;overflow:hidden !important;box-sizing:border-box !important}
#edAppSeg .edapp-seal{width:28px;height:28px;flex:0 0 28px;display:inline-block;object-fit:contain;border-radius:50%;background:transparent}
#edAppSeg .edapp-seal.night{display:none}
body[data-theme="night"] #edAppSeg .edapp-seal.day{display:none}
body[data-theme="night"] #edAppSeg .edapp-seal.night{display:inline-block}
#edAppSeg .edapp-fseal{width:28px;height:28px;flex:0 0 28px;display:inline-grid;place-items:center;line-height:0}
#edAppSeg .edapp-fseal svg{width:28px;height:28px;display:block}
#edAppSeg .edapp-any{width:28px;height:28px;flex:0 0 28px;display:inline-grid;place-items:center;line-height:0}
#edAppSeg .edapp-n{font-weight:600;font-size:13.5px;flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis}
#edAppSeg .edapp-s{font:400 11px/1.2 var(--cd-sans,system-ui,sans-serif);opacity:.72;white-space:nowrap;flex:0 0 auto;margin-left:6px}
#edAppSeg button[aria-pressed="true"] .edapp-s{opacity:.9}
#edAppSeg .edapp-logo{display:none !important}
html:not(#hd1):not(#hd2):not(#hd3):not(#hd4):not(#hd5):not(#hd6):not(#hd7) body.forge-app .hd-appkey-wrap > .hd-panel{max-height:calc(100vh - 56px) !important;overflow:auto !important;overscroll-behavior:contain;min-width:min(360px, calc(100vw - 24px)) !important}
@media (max-width:420px){ #edAppSeg .edapp-s{display:none} }
</style>
'''
    js = '''<script id="cd-9s62-appseals-js">
/* 9s62 · the seals of her apps, as the apps draw them (the reasons are in the sheet cd-9s62-appseals-css). Carpe Diem's,
   Inkwell's and Ingenium's were drawn by each app's own seal code on 17 October 2026 and kept here as two small pictures each,
   a day face and a night face; the Forge's is drawn live by its own seal (cdForgeSealSVG); Another app wears a plain page. */
(function(){
  var SEALS=''' + json.dumps(data) + ''';
  var ANY='<svg viewBox="0 0 28 28" width="28" height="28" aria-hidden="true"><circle cx="14" cy="14" r="13" fill="var(--accent,#1B6B93)"/><path d="M9.5 7.5h6l4 4v9a1 1 0 0 1-1 1h-9a1 1 0 0 1-1-1v-12a1 1 0 0 1 1-1z" fill="#fff"/><path d="M15.5 7.5v4h4" fill="none" stroke="var(--accent,#1B6B93)" stroke-width="1.2"/><path d="M11 14.5h6M11 17h6M11 19.5h4" stroke="var(--accent,#1B6B93)" stroke-width="1.2" stroke-linecap="round"/></svg>';
  function strip(svg){ return String(svg||'').replace(/<title>[\\s\\S]*?<\\/title>/g,'').replace(/<desc>[\\s\\S]*?<\\/desc>/g,'').replace(/<svg /,'<svg aria-hidden="true" focusable="false" '); }
  window.forgeAppSeal=function(app, size){ size=size||28; if(app==='other') app='any';
    if(app==='forge'){ try{ if(typeof window.cdForgeSealSVG==='function') return '<span class="edapp-fseal" aria-hidden="true">'+strip(window.cdForgeSealSVG(size))+'</span>'; }catch(e){} return '<span class="edapp-fseal" data-wait="1" aria-hidden="true"></span>'; }
    var s=SEALS[app]; if(s) return '<img class="edapp-seal day" alt="" aria-hidden="true" src="'+s.day+'"><img class="edapp-seal night" alt="" aria-hidden="true" src="'+s.night+'">';
    return '<span class="edapp-any" aria-hidden="true">'+ANY+'</span>'; };
  /* the Forge's own seal is drawn by a script that runs later than the switch's first paint: paint the switch again once it is there */
  var tries=0, iv=setInterval(function(){ tries++; if(typeof window.cdForgeSealSVG==='function' || tries>60){ clearInterval(iv); try{ if(typeof window.cdForgeSealSVG==='function' && document.querySelector('#edAppSeg [data-wait]') && window.__forgeEdAppWords) window.__forgeEdAppWords(); }catch(e){} } }, 250);
  /* the small line under each name: which copy of the app this device keeps */
  function T(en,fr){ return document.documentElement.lang==='fr'?fr:en; }
  var busy=false;
  function status(){ if(busy||!window.__forgeLib||!document.getElementById('edAppSeg')) return; busy=true;
    /* the cached list, not a fresh read: a fresh read empties the library's cache for a moment, and the switch then mounted the default file over a kept copy (measured) */
    (window.__forgeLib.metaCached||window.__forgeLib.meta)().then(function(M){ busy=false; M=M||{};
      [].forEach.call(document.querySelectorAll('#edAppSeg button[data-app]'), function(b){ var k=b.getAttribute('data-app'); if(k==='other') k='any';
        var s=b.querySelector('.edapp-s'); if(!s){ s=document.createElement('small'); s.className='edapp-s'; b.appendChild(s); }
        var m=M[k+':newest'], t;
        if(k==='any') t=T('any file of yours','un fichier à vous');
        else if(!m) t=T('no copy yet','pas encore de copie');
        else t=(m.version||'')+(m.source==='made'?T(' · your version',' · votre version'):T(' · kept here',' · gardée ici'));
        if(s.textContent!==t) s.textContent=t; });
      fitPanel();
    }, function(){ busy=false; }); }
  /* 9s62: the panel's room is taken from where its key stands, so its foot never runs past the window: below the key when there is
     room, above it when there is more room there, and it scrolls within that room (a fixed allowance left the last rows out of reach
     on a short screen, measured) */
  function fitPanel(){ var p=document.querySelector('body.forge-app .hd-appkey-wrap > .hd-panel[data-open]'); if(!p) return; var k=p.parentNode&&p.parentNode.querySelector('button[aria-controls="'+p.id+'"]'); if(!k) return;
    var kr=k.getBoundingClientRect(), below=Math.floor(window.innerHeight-kr.bottom-16), above=Math.floor(kr.top-16);
    p.style.removeProperty('max-height'); var need=p.scrollHeight+2, up=!(need<=below)&&(need<=above||above>below), room=up?above:below;
    if(up){ p.style.setProperty('top','auto','important'); p.style.setProperty('bottom','calc(100% + 6px)','important'); } else { p.style.removeProperty('top'); p.style.removeProperty('bottom'); }
    p.style.setProperty('max-height', Math.max(120, Math.min(room, need))+'px', 'important'); }
  function fitWatch(){ try{ new MutationObserver(function(ms){ for(var i=0;i<ms.length;i++){ var t=ms[i].target; if(t&&t.classList&&t.classList.contains('hd-panel')){ fitPanel(); return; } } }).observe(document.body,{attributes:true,attributeFilter:['data-open'],subtree:true}); }catch(e){}
    window.addEventListener('resize', fitPanel); }
  var t0=null; function soon(){ clearTimeout(t0); t0=setTimeout(status, 120); }
  function start(){ var seg=document.getElementById('edAppSeg'); if(!seg){ setTimeout(start, 500); return; }
    try{ new MutationObserver(soon).observe(seg,{childList:true,subtree:true}); }catch(e){}
    document.addEventListener('click', function(e){ var k=e.target.closest&&e.target.closest('.hd-appkey'); if(k) soon(); }, true);
    /* the library says 'forge:lib' on the window whenever a copy is kept, opened or dropped (measured: the paint hook alone was never called by the library itself) */
    window.addEventListener('forge:lib', soon); fitWatch();
    soon(); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
</script>
'''
    P.insert_before('<script id="cd-forge-js">', css + js, 'appseals block before cd-forge-js')
    # the switch paints each app under its seal; the old logo is retired
    P.replace_once("""if(Q){ var t=fr?Q.fr.name:Q.name, lg=edLogo(k), want=(lg?'<img class="edapp-logo" alt="" src="'+lg+'">':'')+'<span>'+edEsc(t)+'</span>'; if(b.__paint!==want){ b.__paint=want; b.innerHTML=want; } } });""",
                   """if(Q){ var t=fr?Q.fr.name:Q.name, want=(window.forgeAppSeal?window.forgeAppSeal(k,28):'')+'<span class="edapp-n">'+edEsc(t)+'</span>'; if(b.__paint!==want){ b.__paint=want; b.innerHTML=want; } } });""", 'edAppWords seals')
    P.replace_once("window.__forgeEdSay=edSay;", "window.__forgeEdSay=edSay; window.__forgeEdAppWords=edAppWords;   /* 9s62: the seals block repaints the switch once the Forge's own seal can be drawn */", 'expose edAppWords')
    # the key above the panel reads the app's name alone, never the seal's words
    P.replace_once("var L = lab ? lab.textContent.trim() : T('Editing', 'Modifié'), A = on ? on.textContent.trim() : '';",
                   "var L = lab ? lab.textContent.trim() : T('Editing', 'Modifié'), A = on ? ((on.querySelector('.edapp-n') || on).textContent.trim()) : '';", 'appKey reads the name')
