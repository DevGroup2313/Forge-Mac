"""9s62 · the Studio: the baked applier in the head (Carpe Diem's own Studio no longer swallows the edits),
   a version kept from the Studio is 'your version' in the library, and the hand's applier is version 2."""
import os, json
from forgepatch import js_string

HERE = os.path.dirname(os.path.abspath(__file__))

def apply(P):
    applier = open(os.path.join(HERE, 'applier_v2.js'), encoding='utf-8').read()
    lit = js_string(applier)   # a JS string literal, "..." with </ escaped
    # 1. the applier literal in the Studio (var APPLIER="...", AGENT=) and in the hand (var A="...", G=)
    for start, end, what in (('var APPLIER="/* THE FORGE STUDIO', '", AGENT="/* THE FORGE STUDIO', 'studio APPLIER'),
                             ('var A="/* THE FORGE STUDIO', '", G="/* THE FORGE STUDIO', 'hand A')):
        P.must_once(start, what); P.must_once(end, what)
        i = P.t.index(start); j = P.t.index(end)
        assert j > i
        head = start.split('"')[0] + '"'      # 'var APPLIER="' / 'var A="'
        P.t = P.t[:i] + head[:-1] + lit + P.t[j + 1:]   # replace the whole literal, keep ', AGENT=' / ', G='
        P.log.append('replace literal: ' + what)
    # 2. bakeEdits: the tag goes into the head
    P.replace_once("  var at=html.lastIndexOf('</body>'); return at>=0?html.slice(0,at)+tag+html.slice(at):html+tag; }",
        "  /* 9s62: in the head, so the baked applier is the first Studio in the page: an app with a Studio of its own (Carpe Diem) then\n"
        "     steps aside or takes the edits over, instead of the baked copy stepping aside with its edits unread (measured on 9s61) */\n"
        "  var hm=/<head(?:\\s[^>]*)?>/i.exec(html); if(hm){ var ha=hm.index+hm[0].length; return html.slice(0,ha)+tag+html.slice(ha); }\n"
        "  var at=html.lastIndexOf('</body>'); return at>=0?html.slice(0,at)+tag+html.slice(at):html+tag; }", 'bakeEdits head placement')
    # 3. a version kept from the Studio is her own version, not 'the file you chose'
    P.replace_once("try{ ed().open(baked,name,k); }catch(e){ say(T('It could not be kept: '",
                   "try{ ed().open(baked,name,k,{made:true}); }catch(e){ say(T('It could not be kept: '", 'keepVersion made')
    P.replace_once("var k=curKey(); FS.codeDirty=false; try{ ed().open(code,ed().shellName()||'app.html',k); }catch(e){}",
                   "var k=curKey(); FS.codeDirty=false; try{ ed().open(code,ed().shellName()||'app.html',k,{made:true}); }catch(e){}", 'keepCode made')
    P.replace_once("open:function(txt,name,a){ if(a && (ED.app||edApp())!==a) edSwitch(a,{noMount:true}); setEditorShell(txt,name); }",
                   "open:function(txt,name,a,opt){ if(a && (ED.app||edApp())!==a) edSwitch(a,{noMount:true}); setEditorShell(txt,name,opt); }", '__forgeEd.open opt')
    P.replace_once("function setEditorShell(txt,name){\n  ED.shell=txt; ED.shellName=name; clearShipDoc(); if(window.shellKeep) shellKeep(name,txt); try{ if(window.__forgeLibSeen) window.__forgeLibSeen(txt,name); }catch(e){}",
                   "function setEditorShell(txt,name,opt){\n  ED.shell=txt; ED.shellName=name; clearShipDoc(); if(window.shellKeep) shellKeep(name,txt); try{ if(window.__forgeLibSeen) window.__forgeLibSeen(txt,name,(opt&&opt.made)?'made':'file'); }catch(e){}", 'setEditorShell opt')
    P.replace_once("window.__forgeLibSeen=function(txt, name){ if(OPENING) return; var a='any'; try{ a=B().detect(txt); }catch(e){}\n  OPEN={app:a, slot:null, text:txt, name:name||''}; NOTE=null; paintSoon();\n  if(LIB_APPS.indexOf(a)>=0) later(function(){ if(shellNow()===txt) keepText(a, txt, name, 'file'); }); };",
                   "window.__forgeLibSeen=function(txt, name, how){ if(OPENING) return; var a='any'; try{ a=B().detect(txt); }catch(e){}\n  OPEN={app:a, slot:null, text:txt, name:name||''}; NOTE=null; paintSoon();\n  if(LIB_APPS.indexOf(a)>=0) later(function(){ if(shellNow()===txt) keepText(a, txt, name, how==='made'?'made':'file'); }); };", '__forgeLibSeen how')
