"""Review r2: replace the three rounded constants in the current ghg_3veh.gms by the exact products
of the old factored form; then every row must equal the 2010 text exactly."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import sys, re, sympy as sp
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import exactcmp as X
D = (_PUBLIC_REPO + '/research-20260929/publication/reviews/minlplib-status-r1/dl')
src = open(f'{D}/gms/ghg_3veh.gms').read()
rep = {'2715.7894736842': '2715.789473684205', '376.046780997472': '376.046780997472326',
       '28.341428570246': '28.3414285702460083441901635199'}
for a, b in rep.items():
    src = re.sub(re.escape(a) + r'(?!\d)', b, src)
open('/tmp/ghg_patched_r2.gms', 'w').write(src)
old, _, _ = X.read_gms(f'{D}/old/MINLPLib.ghg_3veh.gms')
pat, _, _ = X.read_gms('/tmp/ghg_patched_r2.gms')
bad = [k for k in old if sp.expand(old[k][0] - pat[k][0]) != 0 and sp.cancel(sp.together(old[k][0] - pat[k][0])) != 0]
print('rows differing after replacing the 3 constants by exact products:', bad)
