"""camshape: rigorous dual bound by forward/backward bound propagation along the chain,
and a primal point (the bound's maximizer), checked against the OSIL.

Argument (details in the report). With u_j = 1/r_j (u_0 = 1), the convexity rows
g_1..g_{n-1} are the linear inequalities e_j = u_{j-1} - c u_j + u_{j+1} >= 0.
Let S solve S_{j+1} = c S_j - S_{j-1} with S_0 = 1, S_1 = 1/ub_1. Then
  u_j - S_j = sum_{k=1}^{j-1} U_{j-1-k}(c/2) e_k + U_{j-1}(c/2) (u_1 - 1/ub_1) >= 0
whenever the Chebyshev values U_m(c/2) (m = 0..n-1) are >= 0; this is checked in
interval arithmetic. Hence r_j <= R_j := 1/S_j (when S_j > 0). With the bounds
r_j <= ub_j and the slope rows |r_{j+1} - r_j| <= alpha (pairs j = 2..n-1), every
feasible r satisfies r_j <= E_j := min_k (B_k + alpha * dist(j, k)), B = min(R, ub),
dist = number of slope-constrained pairs between j and k. So sum r <= sum E and
objective = -c0 sum r >= -c0 sum E.
All quantities are computed in mpmath interval arithmetic (60 digits) from the
decimal constants of the OSIL.
"""
import json
import sys
import time

import mpmath as mp
import numpy as np

from camshape_model import extract
from osil_eval import check

iv = mp.iv
iv.dps = 60


def dec(x):
    """Interval enclosing the decimal constant printed in the OSIL (repr of the float
    parsed from it; the OSIL strings have at most 15-16 significant digits)."""
    return iv.mpf(repr(float(x)))


def bound(n):
    m = extract(n)
    # the three-term recurrences amplify interval widths by about (1 + sqrt 2) per step
    # (dependency effect), so the working precision grows with n
    iv.dps = int(0.4 * n) + 60
    c, c2, alpha, c0 = dec(m["c"]), dec(m["c2"]), dec(m["alpha"]), dec(m["c0"])
    ub = [dec(v) for v in m["ub"]]
    # Chebyshev U_m(c/2): U_0 = 1, U_1 = c, U_{m+1} = c U_m - U_{m-1}
    U = [iv.mpf(1), c]
    for k in range(2, n + 1):
        U.append(c * U[-1] - U[-2])
    cheb_ok = all(Um.a >= 0 for Um in U[:n])
    # S recurrence (index j = 0..n, 1-based r index j)
    S = [iv.mpf(1), 1 / ub[0]]
    for j in range(2, n + 1):
        S.append(c * S[-1] - S[-2])
    R = [None] + [(1 / S[j]) if S[j].a > 0 else None for j in range(1, n + 1)]
    # upper ends of B_j = min(R_j, ub_j); only upper ends are used below
    Bu = [min(mp.mpf(R[j].b), mp.mpf(ub[j - 1].b)) if R[j] is not None else mp.mpf(ub[j - 1].b)
          for j in range(1, n + 1)]
    # envelope: E_j = min_k (B_k + alpha*dist(j,k)); pair (j, j+1) constrained iff j >= 2 (1-based)
    au = mp.mpf(alpha.b)
    E = Bu[:]
    # upper ends only; each addition is done in interval arithmetic and its upper end kept,
    # so every E[j] is a rigorous upper bound of min_k (B_k + alpha * dist(j, k))
    def add_up(x, y):
        return mp.mpf((iv.mpf(x) + iv.mpf(y)).b)
    for j in range(1, n):  # forward: 0-based j; pair (j-1, j) is 1-based pair (j, j+1)
        if j >= 2:
            E[j] = min(E[j], add_up(E[j - 1], au))
    for j in range(n - 2, -1, -1):
        if j + 1 >= 2:
            E[j] = min(E[j], add_up(E[j + 1], au))
    sumE = iv.mpf(0)
    for e in E:
        sumE += iv.mpf(e)
    dual = -c0 * sumE
    return m, dict(cheb_nonneg=cheb_ok, sumE_upper=float(mp.mpf(sumE.b)), dual_bound=float(mp.mpf(dual.a)),
                   dual_interval=[mp.nstr(mp.mpf(dual.a), 20), mp.nstr(mp.mpf(dual.b), 20)], E=[float(e) for e in E],
                   S_min=float(min(mp.mpf(s.a) for s in S[1:n + 1])))


def primal_from_envelope(m, E):
    """Use the envelope as primal point (d_i = r_{i+1} - r_i) and check it in the OSIL."""
    n = m["n"]
    r = np.array(E, dtype=float)
    r = np.minimum(r, m["ub"])
    x = np.concatenate([r, np.diff(r)])
    return x, check(f"camshape{n}", x, m["I"])


def main(n):
    t0 = time.time()
    m, rec = bound(n)
    x, chk = primal_from_envelope(m, rec["E"])
    out = dict(name=f"camshape{n}", n=n, chebyshev_nonneg=rec["cheb_nonneg"], S_min=rec["S_min"],
               dual_bound=rec["dual_bound"], dual_interval=rec["dual_interval"],
               primal_obj=chk["obj"], primal_cons_viol=chk["cons_viol"], primal_bound_viol=chk["bound_viol"],
               worst_row=chk["worst_row"], seconds=time.time() - t0)
    print(json.dumps(out))
    with open(f"logs/camshape{n}_bound.json", "w") as f:
        json.dump(out, f, indent=1)
    np.save(f"logs/camshape{n}_envelope.npy", np.array(rec["E"]))
    return out


if __name__ == "__main__":
    for a in sys.argv[1:]:
        main(int(a))
