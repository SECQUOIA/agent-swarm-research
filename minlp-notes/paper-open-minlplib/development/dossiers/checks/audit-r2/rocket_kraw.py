"""Second, independent existence proof for an exactly feasible rocketN point below
LINDO's listed dual.  Setup written for this dossier; interval arithmetic, AD and
Krawczyk test from the first bound-audit verifier (ivl.py: rational endpoints,
outward rounding; kraw.py: own error analysis).  Not the wave-2 reviewer's code.
Layout (asserted): x2 = step; v_0..v_N; h_0..h_N; g_0..g_N; m_0..m_N; T_0..T_N; D_0..D_N.
"""
import sys, time, json
from fractions import Fraction as F
import numpy as np
import osil, kraw

N = int(sys.argv[1]); rhos = [float(s) for s in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1e-12, 1e-11, 1e-10]
LINDO = {100: F('-1.0128319'), 200: F('-1.01283563'), 400: F('-1.01283634')}[N]
M = osil.parse(f'data/rocket{N}.osil')
assert M.n == 6 * N + 7 and M.m == 5 * N + 2 and M.sense == 'min'
step = 0
v = list(range(1, N + 2)); h = list(range(N + 2, 2 * N + 3)); g = list(range(2 * N + 3, 3 * N + 4))
m = list(range(3 * N + 4, 4 * N + 5)); T = list(range(4 * N + 5, 5 * N + 6)); D = list(range(5 * N + 6, 6 * N + 7))
assert M.obj_lin == {h[-1]: F(-1)} and M.obj_const == 0 and M.obj_nl is None and not M.obj_quad
assert (M.lb[v[0]], M.ub[v[0]], M.lb[h[0]], M.ub[h[0]], M.lb[m[0]], M.ub[m[0]], M.lb[m[-1]], M.ub[m[-1]]) == (0, 0, 1, 1, 1, 1, F('0.6'), F('0.6'))
assert all(M.clb[i] == M.cub[i] == 0 for i in range(M.m))
pol = dict(l.split() for l in open(f'data/rocket{N}.conopt.polished.txt') if len(l.split()) == 2)
Tv = [F(pol[M.vname[j]]) for j in T]
# mass rows: m_{i+1} - m_i + c*step*(T_i + T_{i+1}) = 0, found from the model, not assumed
mass = {}
for i in range(M.m):
    if M.nl[i] is None and set(M.lin[i]) <= set(m) and len(M.lin[i]) == 2:
        (a, ca), (b, cb) = sorted(M.lin[i].items())
        assert (ca, cb) == (-1, 1) and b == a + 1
        q = sorted(M.quad[i]); assert len(q) == 2 and all(x[0] == step for x in q) and q[0][2] == q[1][2]
        assert [x[1] for x in q] == [T[m.index(a)], T[m.index(a) + 1]]
        mass[m.index(a)] = (i, q[0][2])
assert sorted(mass) == list(range(N))
S = [F(0)]
for k in range(N):
    S.append(S[-1] + mass[k][1] * (Tv[k] + Tv[k + 1]))
st = (F(1) - F('0.6')) / S[-1]          # m_N = m_0 - step*S_N
mv = [F(1) - st * S[k] for k in range(N + 1)]
assert mv[-1] == F('0.6') and st > 0
x = [F(0)] * M.n
x[step] = st
for k in range(N + 1):
    x[m[k]] = mv[k]; x[T[k]] = Tv[k]
x[v[0]], x[h[0]], x[g[0]], x[D[0]] = F(0), F(1), F(1), F(0)
U = v[1:] + h[1:] + g[1:] + D[1:]
for j in U:
    x[j] = F(pol[M.vname[j]])
fixedset = set(range(M.n)) - set(U)
Srows = [i for i in range(M.m) if osil.row_vars(M, i) - fixedset]
assert len(Srows) == len(U) == 4 * N, (len(Srows), len(U))
sysm = kraw.System(M, x, Srows, U)
t0 = time.time()
c = kraw.newton(sysm, [x[j] for j in U], log=lambda s: None)
res = dict(N=N, step=float(st), n=len(U), T_at_bounds=sum(1 for t in Tv if t in (0, F('3.5'))), masses_at_0p6=sum(1 for q in mv if q == F('0.6')))
for rho in rhos:
    r = rho * np.maximum(np.abs(c), 1.0)
    ok, X, info = kraw.krawczyk(sysm, c, r)
    res.update(rho=rho, krawczyk_ok=ok, **info)
    if ok:
        bok, fails, ob = kraw.box_check(M, sysm, X)
        res.update(box_ok=bok, fails=[str(f) for f in fails[:5]], obj_lo=float(ob.lo), obj_hi=float(ob.hi),
                   obj_hi_exact_below_lindo=bool(ob.hi < LINDO), margin=float(LINDO - ob.hi))
        k = 13
        lo = F((ob.lo.numerator * 10**k) // ob.lo.denominator, 10**k)
        hi = F(-((-ob.hi.numerator * 10**k) // ob.hi.denominator), 10**k)
        res['outward_13dec'] = ['%.13f' % lo, '%.13f' % hi]
        assert lo <= ob.lo and hi >= ob.hi and F('%.13f' % lo) == lo and F('%.13f' % hi) == hi
        break
res['sec'] = round(time.time() - t0, 1)
print(json.dumps(res, indent=1, default=str))
