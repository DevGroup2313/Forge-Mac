"""9s62 · the Studio: the baked applier in the head (Carpe Diem's own Studio no longer swallows the edits),
   a version kept from the Studio is 'your version' in the library, and the hand's applier is version 2."""
import os, json
from forgepatch import js_string

HERE = os.path.dirname(os.path.abspath(__file__))

BAKE = r"""function bakedIn(code){ var out=[], i=0, k; while((k=code.indexOf(T_ED,i))>=0){ var e=code.indexOf(T_END,k); if(e<0) break;
  var m=/__FORGE_STUDIO_EDITS\s*=\s*([\s\S]*?);?\s*$/.exec(code.slice(k+T_ED.length,e)); if(m){ try{ var l=JSON.parse(m[1]); if(l&&l.length) out=out.concat(l); }catch(x){} } i=e+T_END.length; } return out; }
function headSlot(html){ var hm=/<head(?:\s[^>]*)?>/i.exec(html); if(!hm) return -1; var at=hm.index+hm[0].length;
  var cm=/<meta\s[^>]*charset[^>]*>/i.exec(html.slice(at,at+4096)); if(cm) at+=cm.index+cm[0].length; return at; }
function bakeEdits(code,edits){ var had=bakedIn(code), html=strip(strip(code,T_ED),T_AP);
  /* 9s62: the edits already in the version's code stay in it, the new ones come after them (measured: a second Keep used to bake the
     new ones alone, and the first were lost from the new version) */
  var ids={}; edits.forEach(function(x){ ids[x.id]=1; }); var all=had.filter(function(x){ return x&&x.id!=null&&!ids[x.id]; }).concat(edits);
  if(!all.length) return html;
  var tag=T_ED+'window.__FORGE_STUDIO_EDITS='+JSON.stringify(all).replace(/<\//g,'<\\/')+';'+T_END+T_AP+APPLIER.replace(/<\//g,'<\\/')+T_END;
  /* in the head, after the charset when the app names one there (a charset must stand within the first 1024 bytes), so the baked
     applier is the first Studio in the page: an app with a Studio of its own (Carpe Diem) then steps aside or takes the edits over,
     instead of the baked copy stepping aside with its edits unread (measured on 9s61) */
  var ha=headSlot(html); if(ha>=0) return html.slice(0,ha)+tag+html.slice(ha);
  var at=html.lastIndexOf('</body>'); return at>=0?html.slice(0,at)+tag+html.slice(at):html+tag; }"""

HAND_OLD = r"""window.__forgeStudioAgentInto=function(html){ if(typeof html!=="string") return html; if(html.slice(-60000).indexOf("id=\"forge-studio-agent\"")>=0) return html;
  var i=html.lastIndexOf("</body>"); if(i<0) i=html.lastIndexOf("</html>"); if(i<0) return html;
  var tag="<scr"+"ipt id=\"forge-studio-applier\">"+A+"</scr"+"ipt><scr"+"ipt id=\"forge-studio-agent\">"+G+"</scr"+"ipt>";
  return html.slice(0,i)+tag+html.slice(i); };"""

HAND_NEW = r"""window.__forgeStudioAgentInto=function(html){ if(typeof html!=="string") return html; if(html.slice(-60000).indexOf("id=\"forge-studio-agent\"")>=0) return html;
  var i=html.lastIndexOf("</body>"); if(i<0) i=html.lastIndexOf("</html>"); if(i<0) return html;
  /* 9s62: a version kept earlier carries its edits and an applier of its own; the edits are read out, that applier is taken out, and
     this applier stands in the head with them (after the charset), so one Studio alone runs in the stage. Measured on versions kept
     under 9s61: the old applier at the foot of the body kept its own watch and wrote the shared style sheet over this one's, and the
     stage flapped between styled and plain. The hand stays at the foot, where the page is whole when it starts. */
  var ED="<scr"+"ipt id=\"forge-studio-edits\">", AP="<scr"+"ipt id=\"forge-studio-applier\">", END="</scr"+"ipt>", baked=[];
  function cut(h,tag,read){ var k; while((k=h.indexOf(tag))>=0){ var e=h.indexOf(END,k); if(e<0) break;
      if(read){ var m=/__FORGE_STUDIO_EDITS\s*=\s*([\s\S]*?);?\s*$/.exec(h.slice(k+tag.length,e)); if(m){ try{ var l=JSON.parse(m[1]); if(l&&l.length) baked=baked.concat(l); }catch(x){} } }
      h=h.slice(0,k)+h.slice(e+END.length); } return h; }
  html=cut(cut(html,ED,true),AP,false);
  var head=(baked.length?ED+"window.__FORGE_STUDIO_EDITS="+JSON.stringify(baked).replace(/<\//g,"<\\/")+";"+END:"")+AP+A+END, foot="<scr"+"ipt id=\"forge-studio-agent\">"+G+"</scr"+"ipt>";
  var hm=/<head(?:\s[^>]*)?>/i.exec(html), ha=-1; if(hm){ ha=hm.index+hm[0].length; var cm=/<meta\s[^>]*charset[^>]*>/i.exec(html.slice(ha,ha+4096)); if(cm) ha+=cm.index+cm[0].length; }
  if(ha>=0) html=html.slice(0,ha)+head+html.slice(ha); else foot=head+foot;
  i=html.lastIndexOf("</body>"); if(i<0) i=html.lastIndexOf("</html>");
  return html.slice(0,i)+foot+html.slice(i); };"""

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
    # 2. bakeEdits: the edits already in the version stay in it, the tag goes into the head after the charset
    start = "function bakeEdits(code,edits){ var html=strip(strip(code,T_ED),T_AP); if(!edits.length) return html;"
    tail = "  var at=html.lastIndexOf('</body>'); return at>=0?html.slice(0,at)+tag+html.slice(at):html+tag; }"
    P.must_once(start, 'bakeEdits'); i = P.t.index(start); j = P.t.index(tail, i) + len(tail)
    P.t = P.t[:i] + BAKE + P.t[j:]; P.log.append('replace: bakeEdits (edits kept, head after charset)')
    # 2b. the stage's copy: a version's own edits tag and older applier come out, this applier stands in the head with the edits
    P.replace_once(HAND_OLD, HAND_NEW, 'stage hand in the head, one Studio alone')
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
