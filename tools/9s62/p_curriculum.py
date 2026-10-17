"""9s62 · THE CURRICULUM, REWRITTEN FOR HER: the three years' data replaced whole, the ids kept, so what she has read stays read."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
def apply(P):
    parts = []
    for y in ('y1', 'y2', 'y3'):
        f = os.path.join(HERE, '..', 'curriculum', y + '.js')
        if not os.path.exists(f):
            f = os.path.join(HERE, 'curriculum', y + '.js')
        src = open(f, encoding='utf-8').read().rstrip() + '\n'
        # a closing script tag inside a lesson's string would end the page's own script element: escaped, as the house does
        src = src.replace('</script>', '<\\/script>')
        assert '</script' not in src
        parts.append(src)
    start = 'var CURRICULUM_Y1={id:\'web\', year:1,'
    end = 'var CURRICULUM=[CURRICULUM_Y1,CURRICULUM_Y2,CURRICULUM_Y3];'
    P.must_once(start, 'curriculum start'); P.must_once(end, 'curriculum end')
    i = P.t.index(start); j = P.t.index(end)
    assert j > i
    P.t = P.t[:i] + ''.join(parts) + P.t[j:]
    P.log.append('replace: the three years of the curriculum (%d chars)' % sum(len(p) for p in parts))
    # the rooms' own words follow the rewrite
    P.replace_once('<div class="section-sub">Three units, each read and tried, one lesson at a time.</div>',
                   '<div class="section-sub">Three years, written for you: look, do, name, why it matters, done when. One lesson at a time, and a way to stop.</div>', 'curriculum sub')
    P.replace_once('<div class="section-sub">Four questions for each module, answers explained, nothing marked.</div>',
                   '<div class="section-sub">Four questions for each module, each answer explained; nothing is marked, and a wrong guess teaches as much as a right one.</div>', 'assessments sub')
    # a lesson marked read, or its prediction checked, is brought up to date in place; nothing is repainted under her
    P.replace_once("  if(l.reveal){ var rv=mk('button','stone solid','Check my prediction'); var ans=mk('div','cd-tip-line'); ans.style.display='none'; ans.innerHTML=l.reveal; rv.onclick=function(){ ans.style.display='block'; rv.disabled=true; MAG.done[u.id+':'+m.id+':'+i]=1; magSave(); setTimeout(function(){ magPaint(u.id, m.id, i); },1500); }; row.appendChild(rv); lb.appendChild(row); lb.appendChild(ans); }",
                   "  if(l.reveal){ var rv=mk('button','stone solid',done?'\\u2714 Checked':'Check my prediction'); var ans=mk('div','cd-tip-line'); ans.style.display=done?'block':'none'; ans.innerHTML=l.reveal; rv.disabled=done; rv.onclick=function(){ ans.style.display='block'; rv.disabled=true; rv.textContent='\\u2714 Checked'; MAG.done[u.id+':'+m.id+':'+i]=1; magSave(); magMark(ld,u,m,l,i); }; row.appendChild(rv); lb.appendChild(row); lb.appendChild(ans); }   /* 9s62: the answer stays in view (measured: a repaint 1.5 s later hid it) */", 'reveal stays')
    P.replace_once("  else { var rd=mk('button','solid','Mark as read'); rd.onclick=function(){ MAG.done[u.id+':'+m.id+':'+i]=1; magSave(); magPaint(u.id, m.id, i); }; row.appendChild(rd); lb.appendChild(row); }",
                   "  else { var rd=mk('button','solid',done?'\\u2714 Read':'Mark as read'); rd.disabled=done; rd.onclick=function(){ MAG.done[u.id+':'+m.id+':'+i]=1; magSave(); rd.disabled=true; rd.textContent='\\u2714 Read'; magMark(ld,u,m,l,i); }; row.appendChild(rd); lb.appendChild(row); }", 'mark as read in place')
    P.replace_once("magSave(); magPaint(u.id, m.id, i); teach('lessonTry'", "magSave(); magMark(ld,u,m,l,i); teach('lessonTry'", 'try it in place')
    s = P.t.index("  if(U!==__ghost){ U.innerHTML=''; CURRICULUM.forEach(function(u){\n    var c=yearCounts(u);")
    e_marker = "row.appendChild(a); row.appendChild(b); r.appendChild(row); U.appendChild(r); }); }\n"
    e = P.t.index(e_marker, s) + len(e_marker)
    block = P.t[s:e]
    P.t = P.t[:s] + "  magPaintUnits();\n" + P.t[e:]
    P.insert_before("function magPaint(unitId, moduleId, openLesson){",
        "/* 9s62: a lesson marked read, or its prediction checked, is brought up to date in place: its own line, its module's count, the\n"
        "   Magister's counts. Measured on 9s61: a repaint of the three rooms 1.5 s after \"Check my prediction\" hid the answer she was\n"
        "   reading and enabled the button again, so the answer came and went; and an answer given meanwhile in the questions room was\n"
        "   lost with it. */\n"
        "function magPaintUnits(){ var U=el('magUnits');\n" + block + "}\n"
        "function magMark(ld,u,m,l,i){ try{ var st=ld.querySelector('summary .t'), ss=ld.querySelector('summary .s'); if(st) st.textContent='\\u2714 '+l.t; if(ss) ss.textContent='read';\n"
        "    var md=el('module-'+m.id); if(md!==__ghost){ var n=readCount(u,m), ms=md.querySelector('summary .s'); if(ms){ ms.textContent=n+' of '+m.lessons.length+' read'+(MAG.asked[m.id]?' \\u00b7 questions answered':''); ms.className='s'+(n===m.lessons.length?' ok':''); } }\n"
        "    magPaintUnits(); if(typeof ascensusPaint==='function') ascensusPaint(); }catch(e){} }\n", 'magMark and magPaintUnits')
    P.log.append('replace: the Magister counts painted on their own')
