"""9s62 · EVERYTHING IN ONE ZIP: the whole library and the app's state exported and read back; the way to another device."""
ROW = r'''<div class="row" id="bkZipRow" style="margin-top:8px;flex-wrap:wrap;gap:8px"><button type="button" class="stone solid" id="bkZipOut">🗄 Export everything as one zip</button><input id="bkZipIn" type="file" accept=".zip,application/zip,.json,application/json" style="display:none"><button type="button" class="solid" id="bkZipInBtn">📥 Read a zip back</button></div>
          <div class="muted" id="bkZipState" role="status" aria-live="polite" style="font-size:12.5px;margin-top:4px"></div>
          <span class="tip" data-tip="The zip holds the JSON backup and, beside it as plain files, the copies of your apps kept in the Forge (two per app at most), the files in Files and the new apps made in the Studio. It is the one file to carry to another device. Reading it back checks every file against its fingerprint first; a file that did not arrive whole is named and skipped, and nothing already here is lost."></span>'''
MOVE = r'''<div class="panel card" id="moveCard">
          <h3 data-mv="h">Move to another device</h3>
          <ol data-mv="list" style="margin:6px 0 8px 20px;line-height:1.55;font-size:13.5px"></ol>
          <p class="muted" data-mv="note" style="font-size:12.5px;margin:0"></p>
        </div>
        '''
JS = r'''<script id="cd-9s62-backup-js">
/* 9s62 · EVERYTHING IN ONE ZIP, AND THE WAY TO ANOTHER DEVICE. The JSON backup of 9s59 carried the settings, the edits, the
   diary and the files of Files, but not the copies of her apps kept in the app library, nor the new apps of the Studio: on a
   new device those had to be brought back by hand. The zip carries all of it: forge-backup.json (the same JSON, its files
   listed instead of embedded), files/ (the files of Files), library/ (each kept copy of each app, with its fingerprint in the
   manifest), studio/ (the new apps), and a READ ME. Reading it back: every entry is checked against the zip's own checksum
   and, for the apps, the SHA-256 the manifest gives; a broken one is named and skipped; a full device is said plainly, and
   what was read before it stays. Replace or Merge, as the JSON backup offers. Nothing is sent anywhere. */
(function(){
  function $(id){ return document.getElementById(id); }
  function fr(){ return document.documentElement.lang==='fr'; }
  function T(en,f){ return fr()?f:en; }
  function esc(t){ return String(t==null?'':t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function MB(n){ n=+n||0; return n<1048576 ? (n/1024).toFixed(0)+' KB' : (n/1048576).toFixed(1)+' MB'; }
  function say(t,warn){ var s=$('bkZipState'); if(!s) return; s.textContent=t; s.style.color=warn?'#9c2a2a':''; }
  function safe(n){ return String(n||'file').replace(/[\/\\:*?"<>|\u0000-\u001f]+/g,'_').slice(0,120); }
  function isFull(e){ var n=e&&(e.name||'')||''; return /Quota/i.test(n)||/quota|full|space/i.test(String(e&&e.message||'')); }
  var NAMES={cd:'Carpe Diem', forge:'The Forge', inkwell:'Inkwell', ingenium:'Ingenium'};
  function studioApps(){ return new Promise(function(res){ var out=[]; try{ if(!window.indexedDB) return res(out); var r=indexedDB.open('forge-studio',2);
      r.onupgradeneeded=function(){ try{ var db=r.result; if(!db.objectStoreNames.contains('apps')) db.createObjectStore('apps',{keyPath:'id'}); if(!db.objectStoreNames.contains('edits')) db.createObjectStore('edits',{keyPath:'id'}); }catch(e){} };
      r.onsuccess=function(){ var d=r.result; try{ var t=d.transaction('apps','readonly'), c=t.objectStore('apps').openCursor(); c.onsuccess=function(){ var k=c.result; if(k){ out.push(k.value); k.continue(); } }; t.oncomplete=function(){ try{ d.close(); }catch(e){} res(out); }; t.onerror=t.onabort=function(){ try{ d.close(); }catch(e){} res(out); }; }catch(e){ try{ d.close(); }catch(x){} res(out); } };
      r.onerror=function(){ res(out); }; r.onblocked=function(){ res(out); }; }catch(e){ res(out); } }); }
  function studioPut(a){ return new Promise(function(res,rej){ try{ var r=indexedDB.open('forge-studio',2);
      r.onupgradeneeded=function(){ try{ var db=r.result; if(!db.objectStoreNames.contains('apps')) db.createObjectStore('apps',{keyPath:'id'}); if(!db.objectStoreNames.contains('edits')) db.createObjectStore('edits',{keyPath:'id'}); }catch(e){} };
      r.onsuccess=function(){ var d=r.result; try{ var t=d.transaction('apps','readwrite'); t.objectStore('apps').put(a); t.oncomplete=function(){ try{ d.close(); }catch(e){} res(true); }; t.onerror=t.onabort=function(){ var e=t.error; try{ d.close(); }catch(x){} rej(e); }; }catch(e){ try{ d.close(); }catch(x){} rej(e); } };
      r.onerror=function(){ rej(r.error); }; }catch(e){ rej(e); } }); }
  function deliver(name, blob){ try{ if(window.cdSaveBytesToHost && blob.arrayBuffer){ blob.arrayBuffer().then(function(buf){ var done=false; try{ done=cdSaveBytesToHost(name, blob.type||'application/zip', new Uint8Array(buf)); }catch(e){} if(!done) anchor(name, blob); }); return; } }catch(e){} anchor(name, blob); }
  function anchor(name, blob){ var u=URL.createObjectURL(blob), a=document.createElement('a'); a.href=u; a.download=name; document.body.appendChild(a); a.click(); setTimeout(function(){ URL.revokeObjectURL(u); a.remove(); }, 4000); }
  var README_EN='THE FORGE · EVERYTHING, IN ONE ZIP\n\nThis zip holds all the Forge kept on one device:\n  forge-backup.json  the settings, the edits, the diary, the chat, the curriculum read, the sources kept\n  files/             the files brought into Files\n  library/           the copies of your apps kept in the Forge (the newest, and the one before it)\n  studio/            the new apps made in the Studio\n\nTO READ IT BACK ON ANY DEVICE\n  1. Install the Forge on that device (the device package for it) and open it.\n  2. Settings, then Backup, then "Read a zip back", and choose this file.\n  3. Choose Merge to lay it over what is there, or Replace to start from this file alone.\nEvery file is checked against its fingerprint before it is kept. Nothing is sent anywhere.\n';
  var README_FR='LA FORGE · TOUT, EN UN ZIP\n\nCe zip contient tout ce que la Forge gardait sur un appareil :\n  forge-backup.json  les réglages, les modifications, le journal, la discussion, le cursus lu, les sources gardées\n  files/             les fichiers apportés dans Fichiers\n  library/           les copies de vos apps gardées dans la Forge (la plus récente, et celle d’avant)\n  studio/            les nouvelles apps faites dans le Studio\n\nPOUR LE RELIRE SUR N’IMPORTE QUEL APPAREIL\n  1. Installez la Forge sur cet appareil (son paquet) et ouvrez-la.\n  2. Réglages, puis Sauvegarde, puis « Relire un zip », et choisissez ce fichier.\n  3. Choisissez Fusionner pour le poser sur ce qui est là, ou Remplacer pour repartir de ce seul fichier.\nChaque fichier est vérifié contre son empreinte avant d’être gardé. Rien n’est envoyé nulle part.\n';
  function exportZip(){ if(!window.__forgeZip||!window.__forgeBackup){ say(T('The zip writer is not ready yet; try again in a moment.','L’écriture du zip n’est pas encore prête ; réessayez dans un instant.'),true); return; }
    var b=$('bkZipOut'); b.disabled=true; say(T('Gathering…','Rassemblement…'));
    var man={forge:'backup', v:4, zip:true, at:new Date().toISOString(), build:(window.CD_BUILD||{}), keys:{}, store:{}, files:[], library:[], studio:[]}, entries=[];
    Promise.resolve().then(function(){ try{ var o=window.__forgeBackup.make(); man.keys=o.keys||{}; man.store=o.store||{}; }catch(e){} })
    .then(function(){ return window.__forgeBackup.files().then(function(list){ var p=Promise.resolve(); list.forEach(function(r){ p=p.then(function(){ var path='files/'+r.id+'__'+safe(r.name); return (r.blob.arrayBuffer?r.blob.arrayBuffer():new Response(r.blob).arrayBuffer()).then(function(buf){ entries.push({name:path, bytes:new Uint8Array(buf)}); man.files.push({id:r.id,name:r.name,size:r.size||buf.byteLength,at:r.at||0,kind:r.kind||'',type:r.type||'',path:path}); }, function(){}); }); }); return p; }, function(){}); })
    .then(function(){ if(!window.__forgeLib) return; return window.__forgeLib.sizes().then(function(M){ var ids=Object.keys(M), p=Promise.resolve(); ids.forEach(function(id){ p=p.then(function(){ var m=M[id]; say(T('Gathering ','Rassemblement de ')+(NAMES[m.app]||m.app)+' ('+m.slot+')…'); return window.__forgeLib.bytes(id).then(function(buf){ if(!buf) return; var path='library/'+m.app+'__'+m.slot+'.html'; entries.push({name:path, bytes:new Uint8Array(buf)}); return window.__forgeLib.meta().then(function(MM){ var full=MM[id]||m; man.library.push({id:id, app:m.app, slot:m.slot, version:full.version||'', build:full.build||'', date:full.date||'', name:full.name||'', title:full.title||'', size:buf.byteLength, sha256:full.sha256||'', source:full.source||'', at:full.at||0, path:path}); }); }, function(){}); }); }); return p; }); })
    .then(function(){ return studioApps().then(function(list){ list.forEach(function(a){ var path='studio/'+a.id+'__'+safe(a.name)+'.html'; entries.push({name:path, text:a.code||''}); man.studio.push({id:a.id,name:a.name,at:a.at||0,from:a.from||'',size:(a.code||'').length,path:path}); }); }); })
    .then(function(){ entries.unshift({name:'forge-backup.json', text:JSON.stringify(man,null,1)}); entries.push({name:'READ ME.txt', text:README_EN+'\n\n'+README_FR});
      say(T('Packing ','Emballage de ')+entries.length+T(' files…',' fichiers…')); return window.__forgeZip.make(entries); })
    .then(function(blob){ var name='the-forge-everything-'+new Date().toISOString().slice(0,10)+'.zip'; deliver(name, blob);
      var t=T('Exported ','Exporté ')+name+' · '+MB(blob.size)+' · '+Object.keys(man.store).length+T(' settings, ',' réglages, ')+man.files.length+T(' files, ',' fichiers, ')+man.library.length+T(' app copies, ',' copies d’apps, ')+man.studio.length+T(' new apps.',' nouvelles apps.'); say(t); try{ FORGE.diary('backup', t); }catch(e){} b.disabled=false; })
    .catch(function(e){ b.disabled=false; say(T('The zip could not be made: ','Le zip n’a pas pu être fait : ')+String(e&&e.message||e),true); }); }
  function readBuf(file){ if(file.arrayBuffer) return file.arrayBuffer(); return new Promise(function(res,rej){ var r=new FileReader(); r.onload=function(){ res(r.result); }; r.onerror=function(){ rej(r.error); }; r.readAsArrayBuffer(file); }); }
  function ask(man, go){ var night=document.body.getAttribute('data-theme')==='night';
    var back=document.createElement('div'); back.style.cssText='position:fixed;inset:0;z-index:2147483000;background:rgba(10,20,26,.45);display:flex;align-items:center;justify-content:center;padding:18px;';
    var panel=document.createElement('div'); panel.setAttribute('role','dialog'); panel.setAttribute('aria-modal','true'); panel.style.cssText='max-width:540px;width:100%;border-radius:14px;padding:18px 20px;box-shadow:0 18px 60px rgba(0,0,0,.35);font-family:Georgia,serif;'+(night?'background:#14212a;color:#dfe9ef;border:1px solid rgba(255,255,255,.14);':'background:#fff;color:#233;border:1px solid rgba(27,107,147,.25);');
    var h=document.createElement('div'); h.style.cssText='font-weight:700;font-size:17px;margin-bottom:6px;'; h.textContent=T('Read the zip back','Relire le zip'); panel.appendChild(h);
    var d=document.createElement('div'); d.style.cssText='opacity:.85;font-size:13px;margin-bottom:12px;line-height:1.5';
    d.textContent=T('This zip was made on '+String(man.at||'').slice(0,10)+(man.build&&man.build.stamp?' by the Forge '+man.build.stamp:'')+': '+Object.keys(man.store||{}).length+' settings, '+(man.files||[]).length+' files, '+(man.library||[]).length+' app copies and '+(man.studio||[]).length+' new apps. Replace overwrites what this device holds; Merge keeps the rest and lays the zip over it, keeping a newer app copy already here. Every file is checked first. The Forge reloads after.',
      'Ce zip a été fait le '+String(man.at||'').slice(0,10)+(man.build&&man.build.stamp?' par la Forge '+man.build.stamp:'')+' : '+Object.keys(man.store||{}).length+' réglages, '+(man.files||[]).length+' fichiers, '+(man.library||[]).length+' copies d’apps et '+(man.studio||[]).length+' nouvelles apps. Remplacer écrase ce que l’appareil garde ; Fusionner garde le reste et pose le zip dessus, en gardant une copie d’app déjà plus récente ici. Chaque fichier est vérifié d’abord. La Forge se recharge ensuite.'); panel.appendChild(d);
    var row=document.createElement('div'); row.style.cssText='display:flex;flex-wrap:wrap;gap:8px;'; panel.appendChild(row);
    function btn(label,primary,fn){ var b=document.createElement('button'); b.type='button'; b.textContent=label; b.style.cssText='padding:8px 14px;border-radius:9px;cursor:pointer;font-weight:600;font-family:inherit;'+(primary?'background:#1B6B93;color:#fff;border:1px solid #1B6B93;':(night?'background:transparent;color:#cfe3ee;border:1px solid rgba(255,255,255,.3);':'background:#fff;color:#1B6B93;border:1px solid rgba(27,107,147,.45);')); b.onclick=fn; row.appendChild(b); return b; }
    btn(T('Replace','Remplacer'),true,function(){ back.remove(); go(false); }); btn(T('Merge','Fusionner'),false,function(){ back.remove(); go(true); }); btn(T('Cancel','Annuler'),false,function(){ back.remove(); say(''); });
    back.appendChild(panel); document.body.appendChild(back); try{ row.firstChild.focus(); }catch(e){} }
  function vnum(v){ return (String(v||'').match(/\d+/g)||[]).slice(0,3).map(Number); }
  function cmpVer(a,b){ a=vnum(a); b=vnum(b); for(var i=0;i<Math.max(a.length,b.length);i++){ var x=a[i]||0, y=b[i]||0; if(x!==y) return x<y?-1:1; } return 0; }
  function readZip(file){ var L=window.__forgeLib, Z=L&&L.zip, B=window.__forgeBackup; if(!Z||!B){ say(T('The reader is not ready yet; try again in a moment.','Le lecteur n’est pas encore prêt ; réessayez dans un instant.'),true); return; }
    say(T('Reading ','Lecture de ')+file.name+'…');
    readBuf(file).then(function(buf){ var u8=new Uint8Array(buf);
      /* a JSON backup chosen here is read the old way */
      if(/\.json$/i.test(file.name)||u8[0]===123){ var txt=new TextDecoder().decode(u8); var m=B.read(txt); if(m!=='reading back') say(m,true); else say(''); return; }
      var ents=Z.entries(u8); if(!ents||!ents['forge-backup.json']) throw new Error('notzip');
      return Z.data(u8, ents['forge-backup.json']).then(function(mb){ var man; try{ man=JSON.parse(new TextDecoder().decode(mb)); }catch(e){ throw new Error('notzip'); } if(!man||man.forge!=='backup') throw new Error('notzip');
        ask(man, function(merge){ restore(u8, ents, man, merge); }); }); })
    .catch(function(e){ var c=String(e&&e.message||e);
      if(c==='notzip') say(T('This file is not a Forge backup zip (no forge-backup.json inside). Choose the file the Forge made: the-forge-everything-….zip, or a .json backup.','Ce fichier n’est pas un zip de sauvegarde de la Forge (pas de forge-backup.json dedans). Choisissez le fichier fait par la Forge : the-forge-everything-….zip, ou une sauvegarde .json.'),true);
      else if(c==='nostream') say(T('This browser cannot unpack a zip. Use the JSON backup instead, or open the zip on a computer and bring the files in one by one.','Ce navigateur ne sait pas déballer un zip. Utilisez plutôt la sauvegarde JSON, ou ouvrez le zip sur un ordinateur et apportez les fichiers un par un.'),true);
      else say(T('The zip could not be read: ','Le zip n’a pas pu être lu : ')+c,true); }); }
  function entryData(u8, ents, path, app){ var Z=window.__forgeLib.zip, e=ents[path]; if(!e) return Promise.reject(new Error('missing'));
    return Z.data(u8, e, app).then(function(d){ if(e.usz!=null && d.length!==e.usz) throw new Error('broken'); if(e.crc!=null && window.__forgeZip && window.__forgeZip.crc32){ var c=window.__forgeZip.crc32(d)>>>0; if(c!==(e.crc>>>0)) throw new Error('broken'); } return d; }); }
  function restore(u8, ents, man, merge){ var B=window.__forgeBackup, L=window.__forgeLib, done={keys:'',files:0,lib:0,apps:0}, skipped=[], full=false;
    say(T('Reading back the settings…','Relecture des réglages…'));
    B.apply({forge:'backup', keys:man.keys||{}, store:man.store||{}, files:[]}, merge).then(function(msg){ done.keys=msg; })
    .then(function(){ var p=Promise.resolve(); (man.files||[]).forEach(function(f){ p=p.then(function(){ if(full) return; say(T('Reading back ','Relecture de ')+f.name+'…');
        return entryData(u8, ents, f.path).then(function(d){ return B.put({id:f.id,name:f.name,size:f.size||d.length,at:f.at||Date.now(),kind:f.kind||'file',type:f.type||'',blob:new Blob([d],{type:f.type||'application/octet-stream'})}).then(function(){ done.files++; }); })
        .catch(function(e){ if(isFull(e)){ full=true; return; } skipped.push(f.name+' ('+T('did not arrive whole','n’est pas arrivé entier')+')'); }); }); }); return p; })
    .then(function(){ if(!L) return; return L.meta().then(function(M){ var list=(man.library||[]).slice().sort(function(a,b){ return (a.slot==='newest'?0:1)-(b.slot==='newest'?0:1); }), p=Promise.resolve();
        list.forEach(function(m){ p=p.then(function(){ if(full) return; var cur=M[m.app+':newest'];
            if(merge && cur && m.slot==='newest' && cmpVer(m.version, cur.version)<0){ skipped.push((NAMES[m.app]||m.app)+' '+m.version+' ('+T('an newer copy is already here','une copie plus récente est déjà ici')+')'); return; }
            if(cur && cur.sha256===m.sha256){ return; }
            say(T('Reading back ','Relecture de ')+(NAMES[m.app]||m.app)+' '+(m.version||'')+'…');
            return entryData(u8, ents, m.path, m.app).then(function(d){ return L.sha(d).then(function(h){ if(m.sha256 && h!==String(m.sha256).toLowerCase()) throw new Error('broken');
                return L.keepRaw({app:m.app,title:m.title||NAMES[m.app]||m.app,version:m.version||'',build:m.build||'',date:m.date||'',name:m.name||(m.app+'.html'),size:d.length,sha256:h,source:m.source||'file'}, d, m.slot).then(function(){ done.lib++; }); }); })
            .catch(function(e){ if(isFull(e)){ full=true; return; } skipped.push((NAMES[m.app]||m.app)+' '+(m.version||'')+' ('+(String(e&&e.message)==='broken'?T('did not arrive whole','n’est pas arrivée entière'):T('could not be kept','n’a pas pu être gardée'))+')'); }); }); });
        return p; }); })
    .then(function(){ var p=Promise.resolve(); (man.studio||[]).forEach(function(a){ p=p.then(function(){ if(full) return; return entryData(u8, ents, a.path).then(function(d){ return studioPut({id:a.id,name:a.name,code:new TextDecoder().decode(d),at:a.at||Date.now(),from:a.from||''}).then(function(){ done.apps++; }); }).catch(function(e){ if(isFull(e)){ full=true; return; } skipped.push(a.name+' ('+T('did not arrive whole','n’est pas arrivée entière')+')'); }); }); }); return p; })
    .then(function(){ var t=T('Read back: ','Relu : ')+done.keys+', '+done.files+T(' files, ',' fichiers, ')+done.lib+T(' app copies, ',' copies d’apps, ')+done.apps+T(' new apps.',' nouvelles apps.')
        +(skipped.length?' '+T('Skipped: ','Sauté : ')+skipped.join('; ')+'.':'')+(full?' '+T('This device ran out of room part way; what was read before that is kept. Free some space (Storage, below) and read the zip again.','L’appareil a manqué de place en route ; ce qui a été relu avant reste. Libérez de la place (Stockage, ci-dessous) et relisez le zip.'):'');
      say(t, full||skipped.length>0); try{ FORGE.diary('backup', t); }catch(e){}
      if(!full) setTimeout(function(){ location.reload(); }, 1800); })
    .catch(function(e){ say(T('Reading back stopped: ','La relecture s’est arrêtée : ')+String(e&&e.message||e)+T('. What was read before it stays.','. Ce qui a été relu avant reste.'),true); }); }
  function moveSteps(){ return fr() ? ['Ici : Réglages, Sauvegarde, puis « 🗄 Tout exporter en un zip ». Le fichier s’appelle the-forge-everything-(date).zip.',
      'Portez le zip sur l’autre appareil : AirDrop ou iCloud Drive entre un Mac, un iPhone et un iPad ; une clé USB ou un dossier partagé vers Windows ; un courriel à vous-même ou un lecteur en ligne pour la tablette Fire (il arrive dans Téléchargements).',
      'Sur l’autre appareil, installez la Forge pour cet appareil (le paquet de l’étape 5 de l’Éditeur, ou le fichier HTML seul) et ouvrez-la.',
      'Là : Réglages, Sauvegarde, « 📥 Relire un zip », choisissez le fichier, puis Fusionner (ou Remplacer sur un appareil neuf).',
      'Vos apps, vos fichiers, vos modifications et vos réglages sont là. Le zip reste une sauvegarde : gardez-le.']
    : ['Here: Settings, Backup, then "🗄 Export everything as one zip". The file is called the-forge-everything-(date).zip.',
      'Carry the zip to the other device: AirDrop or iCloud Drive between a Mac, an iPhone and an iPad; a USB stick or a shared folder to Windows; an email to yourself or an online drive for the Fire tablet (it lands in Downloads).',
      'On the other device, install the Forge for that device (the package from step 5 of the Editor, or the plain HTML file) and open it.',
      'There: Settings, Backup, "📥 Read a zip back", choose the file, then Merge (or Replace on a brand-new device).',
      'Your apps, files, edits and settings are there. The zip remains a backup: keep it.']; }
  function paintMove(){ var c=$('moveCard'); if(!c) return; c.querySelector('[data-mv="h"]').textContent=T('Move to another device','Passer à un autre appareil');
    c.querySelector('[data-mv="list"]').innerHTML=moveSteps().map(function(s){ return '<li>'+esc(s)+'</li>'; }).join('');
    c.querySelector('[data-mv="note"]').textContent=T('The Mac, Windows, iPhone, iPad and Fire builds all read the same zip, so one file serves every device. A zip made by an older Forge is read by a newer one.','Les versions Mac, Windows, iPhone, iPad et Fire lisent le même zip : un seul fichier sert tous les appareils. Un zip fait par une Forge plus ancienne est lu par une plus récente.'); }
  function seat(){ var inBtn=$('backupInBtn'); if(!inBtn||$('bkZipRow')) return !!$('bkZipRow'); var row=inBtn.closest('.row'); if(!row) return false;
    row.insertAdjacentHTML('afterend', ''' + repr(ROW) + ''');
    var rc=$('recoverCard'); if(rc) rc.insertAdjacentHTML('beforebegin', ''' + repr(MOVE) + ''');
    $('bkZipOut').onclick=exportZip; $('bkZipInBtn').onclick=function(){ $('bkZipIn').click(); };
    $('bkZipIn').onchange=function(){ var f=this.files&&this.files[0]; try{ this.value=''; }catch(e){} if(f) readZip(f); };
    paintMove(); try{ new MutationObserver(function(){ paintMove(); var o=$('bkZipOut'); if(o) o.textContent=T('🗄 Export everything as one zip','🗄 Tout exporter en un zip'); var i=$('bkZipInBtn'); if(i) i.textContent=T('📥 Read a zip back','📥 Relire un zip'); }).observe(document.documentElement,{attributes:true,attributeFilter:['lang']}); }catch(e){}
    return true; }
  function start(){ if(!seat()) setTimeout(start, 700); }
  window.__forgeBackupZip={ exportZip:exportZip, readZip:readZip };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
</script>
'''
def apply(P):
    P.insert_before('<script id="cd-9s61-studio">', JS, 'backup zip block')
    P.replace_once("try{ window.__forgeBackup={ gather:backupGather, read:function(t){ return backupRead(t); }, files:function(){ return filesAll(); }, del:function(id){ return filesDel(id); } }; }catch(e){}",
                   "try{ window.__forgeBackup={ gather:backupGather, read:function(t){ return backupRead(t); }, files:function(){ return filesAll(); }, del:function(id){ return filesDel(id); }, put:function(r){ return filesPut(r); }, apply:function(o,m){ return backupApply(o,m); }, make:function(){ return JSON.parse(backupMake()); } }; }catch(e){}   /* 9s62: the zip backup reads and writes through the same doors */", 'backup api')
    P.replace_once("out[dec.decode(u8.subarray(off+46,off+46+nl))]={meth:dv.getUint16(off+10,true), csz:dv.getUint32(off+20,true), usz:dv.getUint32(off+24,true), lho:dv.getUint32(off+42,true)};",
                   "out[dec.decode(u8.subarray(off+46,off+46+nl))]={meth:dv.getUint16(off+10,true), crc:dv.getUint32(off+16,true), csz:dv.getUint32(off+20,true), usz:dv.getUint32(off+24,true), lho:dv.getUint32(off+42,true)};   /* 9s62: the checksum travels too, so a backup can check each file */", 'zip entries crc')
