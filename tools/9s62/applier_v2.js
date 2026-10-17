/* THE FORGE STUDIO'S EDITS, INSIDE THE APP (9s62). Copyright (c) 2026 Yannie D. Forest. All rights reserved.
   The edits made in the Forge's Studio, applied to the app as it runs: words, attributes, looks, hiding, moving and
   copying a part. Each edit names its part by a selector read from the live app when she pointed at it. The first
   time a part is found it is marked (data-fs), so a part keeps its edits after it moves; a part the app draws again
   is found again by its selector. Looks are written as CSS, everything else is done here and done again whenever the
   app redraws (a MutationObserver, quiet while it works). DECLARATIVE ONLY: no eval, nothing fetched.
   9s62: the baked copy stands in the head, so it is the first Studio in the page. An app that carries a Studio of its
   own (Carpe Diem 1051 does) finds it there and steps aside, or takes the baked edits over from it (they are read
   from window.__FORGE_STUDIO_EDITS, which stands just before this). Measured on 9s61: the baked copy stood at the foot
   of the body, Carpe Diem's own copy ran first with no edits to read, and the baked copy then stepped aside with the
   edits unread. Only the Studio that holds the window's name acts; a copy that was replaced stops its watch. */
(function(){
  var OLD=window.__forgeStudio;
  /* v stays 1: an app that carries a Studio of its own (Carpe Diem 1051) asks for v===1 and then hands this one its saved
     edits; any other value made it start a copy of its own over this one. gen 2 is what tells this Studio from the old. */
  if(OLD&&OLD.v===1&&OLD.gen>=2){ try{ if(OLD.addBaked) OLD.addBaked(window.__FORGE_STUDIO_EDITS||[]); }catch(e){} return; }
  /* two layers: what a kept version carries in its own code (BAKED), and what the Forge's Studio is changing now (LIVE, on top) */
  var BAKED=(window.__FORGE_STUDIO_EDITS||[]).slice(),LIVE=[],EDITS=BAKED.slice(),obs=null,busy=false,timer=null,SELF=null;
  /* an older Studio (v1) that ran before this one holds edits of its own as its live layer; they are kept as live here */
  try{ if(OLD&&OLD.v===1&&OLD.edits){ var had={}; BAKED.forEach(function(x){ had[x.id]=1; }); LIVE=OLD.edits().filter(function(x){ return x&&!had[x.id]; }); EDITS=BAKED.concat(LIVE); } }catch(e){}
  function mine(){ return window.__forgeStudio===SELF; }
  function q(sel){try{return document.querySelector(sel);}catch(e){return null;}}
  function mark(e,k){var v=(e.getAttribute('data-fs')||'').split(' ').filter(Boolean);if(v.indexOf(k)<0){v.push(k);e.setAttribute('data-fs',v.join(' '));}}
  function find(ed){var e=null;try{e=document.querySelector('[data-fs~="'+ed.k+'"]');}catch(x){}
    if(!e&&ed.dup)e=q('[data-forge-dup="'+ed.dup+'"]');
    if(!e&&ed.sel)e=q(ed.sel);
    if(e)mark(e,ed.k);return e;}
  function setWords(e,v){
    if(!e.children.length){if(e.textContent!==v)e.textContent=v;return;}
    for(var n=e.firstChild;n;n=n.nextSibling){if(n.nodeType===3&&n.nodeValue.trim()){var lead=/^\s*/.exec(n.nodeValue)[0],tail=/\s*$/.exec(n.nodeValue)[0];
      if(n.nodeValue!==lead+v+tail)n.nodeValue=lead+v+tail;return;}}}
  function cssOf(edits){var by={},order=[];
    edits.forEach(function(ed){if(ed.kind!=='style'&&ed.kind!=='hide')return;var key=ed.k;if(!by[key]){by[key]={};order.push(key);}
      if(ed.kind==='hide'){if(ed.value)by[key].display='none';}else by[key][ed.prop]=ed.value;});
    /* a background colour also clears a gradient painted on top of it, or the new colour would sit hidden underneath */
    order.forEach(function(k){var p=by[k];if(p['background-color'])p['background-image']='none';});
    return order.map(function(k){var p=by[k],body=Object.keys(p).filter(function(x){return p[x]!==''&&p[x]!=null;}).map(function(x){return x+':'+p[x]+' !important';}).join(';');
      return body?'[data-fs~="'+k+'"]{'+body+'}':'';}).join('\n');}
  function pass(){if(busy)return;if(!mine()){ if(obs){ try{ obs.disconnect(); }catch(e){} } return; }busy=true;try{if(obs)obs.disconnect();
      /* every part is found before anything moves, so one move never confuses the next */
      var found={};EDITS.forEach(function(ed){found[ed.id]=find(ed);});
      EDITS.forEach(function(ed){var e=found[ed.id];if(!e)return;
        if(ed.kind==='text')setWords(e,String(ed.value));
        else if(ed.kind==='attr'){if(ed.value==null||ed.value==='')e.removeAttribute(ed.prop);else if(e.getAttribute(ed.prop)!==String(ed.value))e.setAttribute(ed.prop,String(ed.value));}
        else if(ed.kind==='move'){var r=null;try{r=document.querySelector('[data-fs~="'+ed.refk+'"]')||q(ed.ref);}catch(x){}
          if(r&&r!==e&&r.parentNode&&e.parentNode===r.parentNode){if(ed.where==='before'&&e.nextElementSibling!==r)r.parentNode.insertBefore(e,r);
            else if(ed.where==='after'&&r.nextElementSibling!==e)r.parentNode.insertBefore(e,r.nextSibling);}}
        else if(ed.kind==='dup'){var nx=e.nextElementSibling;if(!(nx&&nx.getAttribute('data-forge-dup')===String(ed.id))){var c=e.cloneNode(true);
            c.setAttribute('data-forge-dup',String(ed.id));c.removeAttribute('id');c.removeAttribute('data-fs');
            Array.prototype.forEach.call(c.querySelectorAll('[id],[data-fs]'),function(x){x.removeAttribute('id');x.removeAttribute('data-fs');});
            e.parentNode.insertBefore(c,e.nextSibling);}}
        else if(ed.kind==='html'){ /* 9s62: a block of the owner's own HTML after the part, data never run: scripts and handlers are taken out */
          var ex=e.nextElementSibling;if(!(ex&&ex.getAttribute('data-forge-html')===String(ed.id))){var box=document.createElement('div');box.setAttribute('data-forge-html',String(ed.id));box.innerHTML=String(ed.value||'');
            Array.prototype.forEach.call(box.querySelectorAll('script,iframe,object,embed'),function(x){x.remove();});
            Array.prototype.forEach.call(box.querySelectorAll('*'),function(x){for(var i=x.attributes.length-1;i>=0;i--){var a=x.attributes[i];if(/^on/i.test(a.name)||/^\s*javascript:/i.test(a.value))x.removeAttribute(a.name);}});
            e.parentNode.insertBefore(box,e.nextSibling);}}});
      var st=document.getElementById('forge-studio-css');if(!st){st=document.createElement('style');st.id='forge-studio-css';(document.head||document.documentElement).appendChild(st);}
      var css=cssOf(EDITS);if(st.textContent!==css)st.textContent=css;
    }catch(e){}finally{busy=false;watch();}}
  function soon(){clearTimeout(timer);timer=setTimeout(pass,120);}
  function watch(){if(!document.body||!window.MutationObserver||!EDITS.length||!mine())return;if(!obs)obs=new MutationObserver(function(){if(!busy)soon();});
    try{obs.observe(document.body,{childList:true,subtree:true});}catch(e){}}
  function apply(list){LIVE=(list||[]).slice();EDITS=BAKED.concat(LIVE);pass();}
  function addBaked(list){var had={};BAKED.forEach(function(x){had[x.id]=1;});(list||[]).forEach(function(x){if(x&&!had[x.id]){BAKED.push(x);had[x.id]=1;}});EDITS=BAKED.concat(LIVE);pass();}
  SELF=window.__forgeStudio={v:1,gen:2,apply:apply,pass:pass,find:find,addBaked:addBaked,edits:function(){return EDITS.slice();},baked:function(){return BAKED.slice();}};
  if(EDITS.length){if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){pass();});else pass();
    window.addEventListener('load',function(){pass();});}
})();
