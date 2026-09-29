"""E5: capacity value functions on structured two-terminal networks.

v(u) = min sum_e phi_e(y_e) + P * (D - throughput)_+  over continuous flows
with y_e <= u_e on the capacitated arcs K and 0 <= y.  Elastic demand
(penalty P per unit of unmet demand) couples the stages.
Networks:
  P3   : three parallel arcs (pairwise substitutes; M-natural type)
  SP4  : series(parallel(a,b), parallel(c,d))  (substitute/complement
         relation is sign-unbalanced, so not L-natural up to sign flips)
  WB2/WB3 : Wheatstone bridge, capacities on 2 or 3 arcs.
"""
import itertools
import numpy as np
import cvxpy as cp
from dcheck import (ddm_violations, ic_violations, lnat_violations,
                    mnat_violations, ninf_false_local_minima, box, INF)

SOLVE = dict(solver=cp.CLARABEL, tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
rng = np.random.default_rng(11)

NETS = {
    "P3": (3, [(0, 1), (0, 1), (0, 1)], [0, 1, 2]),
    "SP4": (3, [(0, 1), (0, 1), (1, 2), (1, 2)], [0, 1, 2, 3]),
    "WB2": (4, [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)], [0, 4]),
    "WB3": (4, [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)], [0, 2, 4]),
    "WB3b": (4, [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)], [0, 1, 2]),
}


def instance(V, arcs, K, kind):
    E = len(arcs)
    up = cp.Parameter(len(K))
    y = cp.Variable(E, nonneg=True)
    t = cp.Variable(nonneg=True)  # throughput
    cons = []
    for v in range(V):
        out_ = sum(y[k] for k, (i, j) in enumerate(arcs) if i == v)
        in_ = sum(y[k] for k, (i, j) in enumerate(arcs) if j == v)
        rhs = t if v == 0 else (-t if v == V - 1 else 0)
        cons.append(out_ - in_ == rhs)
    for s, k in enumerate(K):
        cons.append(y[k] <= up[s])
    terms = []
    for k in range(E):
        a, b = rng.uniform(0.2, 1.5), rng.uniform(0, 1.5)
        if kind == "quad":
            terms.append(a * cp.square(y[k]) + b * y[k])
        else:
            c = rng.uniform(0.3, 2.7)
            terms.append(b * y[k] + 2 * a * cp.pos(y[k] - c))
    D = rng.uniform(2.0, 5.0)
    P = rng.uniform(3.0, 8.0)
    obj = sum(terms) + P * cp.pos(D - t) - 0.0 * t
    return cp.Problem(cp.Minimize(obj), cons), up


def lnat_upto_signs(f, n):
    return min(len(lnat_violations({tuple(s * a for s, a in zip(tau, p)): v for p, v in f.items()}))
               for tau in itertools.product((1, -1), repeat=n))


for name, (V, arcs, K) in [(k, v) for k, v in NETS.items() if k.startswith("WB")]:
    for kind in ("quad", "pl"):
        st = dict(inst=0, ddm=0, ic=0, lnat_signs=0, mnat=0, falselocal=0)
        ex = None
        for _ in range(12):
            prob, up = instance(V, arcs, K, kind)
            n = len(K)
            f = {}
            for p in box(0, 3, n):
                up.value = np.array(p, float)
                prob.solve(**SOLVE)
                f[p] = prob.value
            st["inst"] += 1
            dv = ddm_violations(f); iv = ic_violations(f)
            st["ddm"] += bool(dv); st["ic"] += bool(iv)
            st["lnat_signs"] += bool(lnat_upto_signs(f, n))
            st["mnat"] += bool(mnat_violations(f))
            st["falselocal"] += bool(ninf_false_local_minima(f))
            if iv and ex is None:
                ex = iv[0]
        print(f"{name:5s} {kind:4s} {st}  first IC violation: {ex}", flush=True)
