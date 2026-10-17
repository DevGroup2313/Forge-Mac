"""9s62 · the app library and the zip writer lend their hands to the Storage card, the backup and the comparison:
   nothing new runs here, the same functions are reachable by name."""
def apply(P):
    P.replace_once("window.__forgeLib={ meta:function(){ META=null; return metaAll(); }, open:openCopy, importFile:importLibrary, keep:keepText, paint:paint, file:LIB_FILE };",
        "window.__forgeLib={ meta:function(){ META=null; return metaAll(); }, open:openCopy, importFile:importLibrary, keep:keepText, paint:paint, file:LIB_FILE,\n"
        "  /* 9s62: the same store, reachable by the Storage card, the backup and the comparison tool */\n"
        "  metaCached:metaAll, bytes:bytesOf, sha:sha256, zip:{entries:zipEntries, data:zipData, canInflate:canInflate},\n"
        "  keepRaw:function(m,u8,slot){ slot=slot||'newest'; if(!m||LIB_APPS.indexOf(m.app)<0||(slot!=='newest'&&slot!=='earlier')||!u8||!u8.length) return Promise.reject(err('bad',m&&m.app)); return keepCopy(m,u8,slot); },\n"
        "  drop:function(a,slot){ var id=a+':'+slot; return dbOpen().then(function(d){ return new Promise(function(res,rej){ var t=d.transaction(['meta','bytes'],'readwrite'); t.objectStore('meta').delete(id); t.objectStore('bytes').delete(id);\n"
        "    t.oncomplete=function(){ if(META) delete META[id]; if(OPEN&&OPEN.app===a&&OPEN.slot===slot) OPEN.slot=null; paintSoon(); res(true); }; t.onerror=t.onabort=function(){ rej(t.error||err('refused')); }; }); }); },\n"
        "  sizes:function(){ return dbOpen().then(function(d){ return new Promise(function(res){ var out={}, t=d.transaction('meta','readonly'), c=t.objectStore('meta').openCursor(); c.onsuccess=function(){ var k=c.result; if(k){ out[k.value.id]={app:k.value.app, slot:k.value.slot, size:k.value.size||0, version:k.value.version||'', source:k.value.source||'', at:k.value.at||0, name:k.value.name||''}; k.continue(); } }; t.oncomplete=function(){ res(out); }; t.onerror=t.onabort=function(){ res(out); }; }); }); } };",
        'applib api')
    # the library says so whenever a copy is kept, opened or dropped: the Storage card, the comparison and the Editing panel listen
    P.replace_once("var paintT=0; function paintSoon(){ clearTimeout(paintT); paintT=setTimeout(paint, 30); }",
        "var paintT=0; function paintSoon(){ clearTimeout(paintT); paintT=setTimeout(function(){ try{ paint(); }catch(e){} /* 9s62: 'forge:lib' on the window: a copy was kept, opened or dropped (measured: the paint hook alone was never reached from here) */ try{ var ev; try{ ev=new CustomEvent('forge:lib'); }catch(x){ ev=document.createEvent('Event'); ev.initEvent('forge:lib',false,false); } window.dispatchEvent(ev); }catch(e){} }, 30); }",
        'paintSoon says forge:lib')
    # a copy kept straight into the store (the backup's read-back, the self-test) repaints and tells the listeners too; keepText painted by itself and keepCopy never did
    P.replace_once("t.oncomplete=function(){ if(META){ META[put.id]=put; if(moved) META[eid]=moved; } res({moved:moved, meta:put}); };",
        "t.oncomplete=function(){ if(META){ META[put.id]=put; if(moved) META[eid]=moved; } paintSoon(); res({moved:moved, meta:put}); };", 'keepCopy paints')
    P.insert_before("function zip(entries){\n  var enc=new TextEncoder(), chunks=[], central=[], off=0;",
        "/* 9s62: the zip writer and the checksum, reachable by the backup and the Storage card (the functions above, by name) */\nwindow.__forgeZip={ make:zipAsync, plain:zip, crc32:crc32 };\n", 'zip api')
