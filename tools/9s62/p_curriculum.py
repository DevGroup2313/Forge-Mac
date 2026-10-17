"""9s62 · THE CURRICULUM, REWRITTEN FOR HER: the three years' data replaced whole, the ids kept, so what she has read stays read."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
def apply(P):
    parts = []
    for y in ('y1', 'y2', 'y3'):
        f = os.path.join(HERE, '..', 'curriculum', y + '.js')
        if not os.path.exists(f):
            f = os.path.join(HERE, 'curriculum', y + '.js')
        parts.append(open(f, encoding='utf-8').read().rstrip() + '\n')
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
