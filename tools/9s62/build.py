"""Build the next Forge from the 9s61 base: every patch module in order, each anchored exactly once."""
import sys, os, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from forgepatch import Patcher
BASE = os.path.join(HERE, '..', 'base_9s61.html')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'www', 'the_forge.html')
ORDER = [m for m in os.environ.get('FORGE_PATCHES', 'p_studio,p_appseals').split(',') if m]
text = open(BASE, encoding='utf-8').read()
P = Patcher(text)
for name in ORDER:
    mod = importlib.import_module(name)
    mod.apply(P)
    print('applied', name)
open(OUT, 'w', encoding='utf-8').write(P.t)
print('\n'.join('  ' + l for l in P.log))
print('wrote', OUT, len(P.t), 'bytes')
