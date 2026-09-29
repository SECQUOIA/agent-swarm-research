"""Round counts of fixed-point cutoff propagation at the root (Proposition 3.9
and Proposition 3.10 of the note).
Run: python3 rounds.py > logs/rounds.log"""
import math
import instances as I
from fbbt import hc4, Builder

# x^2 - 2x + 1 + r^4 with base r = x - 1: a stationary term (r^4) that carries
# no cancellation, next to a base (x) whose two terms cancel at x = 1
_b = Builder(1)
_r = _b.lin([0], [1.0], -1.0)
_b.lin([_b.pow(0, 2), 0, _b.pow(_r, 4)], [1.0, -2.0, 1.0], 1.0)
QUAD_R4 = dict(reps={'r4': _b.dag()})
ROT1 = I.make('rot1')
LINE3 = I.make('line3')

q, h, n1, n1s = I.make('quad1'), I.make('h1'), I.make('nondeg1'), I.make('nondeg1s')
print('eps | (s-1)^2 exp on [0.2,2.2]: rounds, rounds*sqrt(eps) | h1 exp on [0.2,2.2] | h1 exp on [-2,2.2] '
      '| nondeg1 u / mono on [-1/3,2/3] | nondeg1s exp on [0,1] | x^2-2x+1+(x-1)^4 on [0.2,2.2] '
      '| rot1 st root | line3 st root')
for eps in [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8]:
    out = []
    for inst, rep, box in ((q, 'exp', [(0.2, 2.2)]), (h, 'exp', [(0.2, 2.2)]), (h, 'exp', [(-2.0, 2.2)]),
                           (n1, 'u', [(-1 / 3, 2 / 3)]), (n1, 'mono', [(-1 / 3, 2 / 3)]),
                           (n1s, 'exp', [(0.0, 1.0)]), (QUAD_R4, 'r4', [(0.2, 2.2)]),
                           (ROT1, 'st', ROT1['box']), (LINE3, 'st', LINE3['box'])):
        st, _, r = hc4(inst['reps'][rep], box, -eps, max_rounds=10 ** 6)
        out.append(f'{st[0]} {r} ({r * math.sqrt(eps):.3f})')
    print(f'{eps:.0e} | ' + ' | '.join(out), flush=True)
