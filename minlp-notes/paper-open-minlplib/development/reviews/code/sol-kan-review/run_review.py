import os
import sys
import json
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parent
sys.path[:0] = [str(BASE/'tree/research-20260929/reviews/wave3-verification'),
                str(BASE/'tree/research-20260929/open-instances-wave3/kan')]
import kan_decode
kan_decode.OSIL = str(BASE/'osil')
import kan_bnb_rigexp as B
import kan_iv as K

original = K.iexp_pt_fast
stats = {'calls': 0, 'points': 0, 'lo': float('inf'), 'hi': -float('inf'), 'rmax': 0.0}
samples = []
def observed(x):
    x = np.asarray(x, dtype=np.float64)
    stats['calls'] += 1
    stats['points'] += x.size
    stats['lo'] = min(stats['lo'], float(x.min()))
    stats['hi'] = max(stats['hi'], float(x.max()))
    m = np.rint(x * (64 / 0.6931471805599453))
    r = K.NI(x) - K.NI(m) * K.LN2_64
    stats['rmax'] = max(stats['rmax'], float(np.maximum(abs(r.lo), abs(r.hi)).max()))
    if stats['calls'] % 31 == 1 and len(samples) < 20000:
        flat = x.ravel()
        samples.extend(float(flat[i]) for i in np.linspace(0, len(flat)-1, min(8, len(flat)), dtype=int))
    return original(x)
K.iexp_pt_fast = observed
original_quad = B.minquad
quad_stats = {'points': 0, 'half_nonexact': 0, 'displacement_wrong_sign': 0,
              'nonfinite_inputs': 0, 'max_abs_s': 0.0}
def observed_quad(gl, gh, m, sl, sh):
    quad_stats['points'] += m.size
    quad_stats['half_nonexact'] += int(np.count_nonzero((0.5*m)*2 != m))
    quad_stats['displacement_wrong_sign'] += int(np.count_nonzero((sl>0)|(sh<0)))
    quad_stats['nonfinite_inputs'] += sum(int(np.count_nonzero(~np.isfinite(a))) for a in (gl,gh,m,sl,sh))
    quad_stats['max_abs_s'] = max(quad_stats['max_abs_s'],float(np.maximum(abs(sl),abs(sh)).max()))
    return original_quad(gl, gh, m, sl, sh)
B.minquad = observed_quad
name = sys.argv[1]
result = B.bnb(name, 4e-11, 1800, 1024)
(BASE/'evidence'/f'{name}.result.json').write_text(json.dumps(result, indent=2)+'\n')
(BASE/'evidence'/f'{name}.args.json').write_text(json.dumps({'stats': stats, 'samples': samples}, indent=2)+'\n')
print('QUADRATIC_STATS', json.dumps(quad_stats))
print('ARGUMENT_STATS', json.dumps(stats))
print('IMPORTED_REPOSITORY_MODULES', json.dumps({n: m.__file__ for n, m in sys.modules.items()
    if n in ('kan_bnb_rigexp', 'kan_iv', 'kan_decode', 'osilx', 'ia')}))
