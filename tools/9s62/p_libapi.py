"""9s62 · the app library and the zip writer lend their hands to the Storage card, the backup and the comparison:
   nothing new runs here, the same functions are reachable by name."""
def apply(P):
    P.replace_once("window.__forgeLib={ meta:function(){ META=null; return metaAll(); }, open:openCopy, importFile:importLibrary, keep:keepText, paint:paint, file:LIB_FILE };",
        "window.__forgeLib={ meta:function(){ META=null; return metaAll(); }, open:openCopy, importFile:importLibrary, keep:keepText, paint:paint, file:LIB_FILE,\n"
        "  /* 9s62: the same store, reachable by the Storage card, the backup and the comparison tool */\n"
        "  bytes:bytesOf, keepRaw:function(m,u8,slot){ return keepCopy(m,u8,slot); }, sha:sha256, zip:{entries:zipEntries, data:zipData, canInflate:canInflate},\n"
        "  drop:function(a,slot){ var id=a+':'+slot; return dbOpen().then(function(d){ return new Promise(function(res,rej){ var t=d.transaction(['meta','bytes'],'readwrite'); t.objectStore('meta').delete(id); t.objectStore('bytes').delete(id);\n"
        "    t.oncomplete=function(){ if(META) delete META[id]; if(OPEN&&OPEN.app===a&&OPEN.slot===slot) OPEN.slot=null; paintSoon(); res(true); }; t.onerror=t.onabort=function(){ rej(t.error||err('refused')); }; }); }); },\n"
        "  sizes:function(){ return dbOpen().then(function(d){ return new Promise(function(res){ var out={}, t=d.transaction('meta','readonly'), c=t.objectStore('meta').openCursor(); c.onsuccess=function(){ var k=c.result; if(k){ out[k.value.id]={app:k.value.app, slot:k.value.slot, size:k.value.size||0, version:k.value.version||'', source:k.value.source||'', at:k.value.at||0, name:k.value.name||''}; k.continue(); } }; t.oncomplete=function(){ res(out); }; t.onerror=t.onabort=function(){ res(out); }; }); }).catch(function(){ return {}; }); } };",
        'applib api')
    P.insert_before("function zip(entries){\n  var enc=new TextEncoder(), chunks=[], central=[], off=0;",
        "/* 9s62: the zip writer and the checksum, reachable by the backup and the Storage card (the functions above, by name) */\nwindow.__forgeZip={ make:zipAsync, plain:zip, crc32:crc32 };\n", 'zip api')
