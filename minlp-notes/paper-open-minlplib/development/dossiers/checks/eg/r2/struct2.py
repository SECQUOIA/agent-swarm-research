"""Own check: gamma ranges per coordinate, c_k range, side-row slacks at the saved points (mpmath iv)."""
import sys
sys.argv = [sys.argv[0]]
src = open('osil_iv.py').read().split("for name in sys.argv[1:]:")[0]
exec(src)
from fractions import Fraction as F
for name in ['eg_int_s', 'eg_disc_s', 'eg_disc2_s']:
    V, obj, C, lin, NL = load(name)
    rows = [terms(NL[k]) for k in range(28)]
    G = [[F(rows[k][1][0][1][i][1]) for i in range(7)] for k in range(28)]
    rng = [(float(min(G[k][i] for k in range(28))), float(max(G[k][i] for k in range(28)))) for i in range(7)]
    ck = [F(C[k][1]) for k in range(24)]
    vn = [v[0] for v in V]
    sol = dict(l.split() for l in open(f'{name}.retry.sol') if l.strip())
    x = [iv.mpf(sol[n]) for n in vn]
    sl = []
    for k in range(24, 28):
        g = ev(NL[k], x); cn, lb, ub = C[k]
        s = (g - iv.mpf(lb)) if lb is not None else (iv.mpf(ub) - g)
        sl.append((cn, mp.nstr(s.a, 4)))
    print(name, "gamma ranges (min,max over rows) per coordinate:", [(round(a, 4), round(b, 4)) for a, b in rng])
    print("   c_k range", float(min(ck)), float(max(ck)), "; side-row slacks at the point:", sl)
