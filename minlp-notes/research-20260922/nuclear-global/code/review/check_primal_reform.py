"""Check (a) the author's stored primal points against every OSiL row in exact arithmetic,
(b) the power-variable map p = phi o k at those points (R1-R4, lam > 0, phi = G p / lam),
(c) the pattern's equilibrium with the reviewer's own simulator (float), and uniqueness spot checks.
usage: check_primal_reform.py names..."""
import sys, json, os
import numpy as np
from fractions import Fraction as F
from rv_common import D, equilibrium, eval_rows_exact, typ_from_x

HERE = os.path.dirname(os.path.abspath(__file__))
PV = json.load(open(os.path.join(HERE, "../../runs/primal_verified.json")))
rng = np.random.default_rng(12345)
for nm in sys.argv[1:]:
    d = D(nm); S = d.S
    x = [F(s) for s in PV[nm]["x"]]
    assert len(x) == len(S.M["vars"])
    rv, where, bv, obj = eval_rows_exact(S, x)
    typ = typ_from_x(S, x)
    # power variables
    N, T = S.N, S.T
    p = [[x[S.phi[i][t]] * x[S.k[i][t]] for i in range(N)] for t in range(T)]
    lam = [x[S.lam[t]] for t in range(T)]
    r1 = max(abs(x[S.k[i][t + 1]] - x[S.k[i][t]] + S.a * p[t][i]) for i in range(N) for t in range(T - 1))
    r2 = max(abs(sum(S.V[i] * p[t][i] for i in range(N)) - 1) for t in range(T))
    r3 = max(max(p[t][i] - S.c[i][t], 0) for i in range(N) for t in range(T))
    r4 = max(abs(lam[t] * p[t][i] - x[S.k[i][t]] * sum(S.G[i][j] * p[t][j] for j in range(N))) for i in range(N) for t in range(T))
    rinv = max(abs(x[S.phi[i][t]] - sum(S.G[i][j] * p[t][j] for j in range(N)) / lam[t]) for i in range(N) for t in range(T))
    print(f"{nm}: pattern(reviewer node order)={typ}")
    print(f"   exact OSiL check: max row viol {float(rv):.2e} ({where}), bound/int viol {float(bv):.1e}, objective {float(obj):.10f}")
    print(f"   power model at the point: R1 {float(r1):.1e} R2 {float(r2):.1e} R3 excess {float(r3):.1e} R4 {float(r4):.1e}; "
          f"min lam_t {float(min(lam)):.6f}; |phi - Gp/lam| {float(rinv):.1e}")
    e = equilibrium(d, typ)
    print(f"   reviewer simulator: lam_T {e['lam']:.10f} peak {e['peak']:.6f} (c={d.c:.6f}) residual {e['res']:.1e} iters {e['it']}")
    # uniqueness spot check: random starts in the (K+) box
    lo = d.KF - d.a * d.c * (T - 1) * d.maxage
    ends = []
    for s in range(10):
        k1 = rng.uniform(lo, d.KF, N)
        ends.append(equilibrium(d, typ, k1=k1)["k1"])
    spread = max(np.max(np.abs(z - e["k1"])) for z in ends)
    print(f"   10 random starts in [{lo:.4f}, {d.KF}]^N: max distance to the equilibrium {spread:.1e}")
