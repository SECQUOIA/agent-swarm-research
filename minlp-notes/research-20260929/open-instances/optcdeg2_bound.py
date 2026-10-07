"""optcdeg2: pattern check, rigorous state bounds by interval propagation along the chain,
and a rigorous Lagrangian dual bound.

Model (asserted from the OSIL in pattern_check):
  min (h/2) sum_{t=0}^{N} y_t^2
  s.t. y_{t+1} - y_t - h v_t = 0                                   (mu_t)
       v_{t+1} - v_t - h u_t + 0.02h y_t + 0.2h v_t^2 = 0            (lam_t),  t = 0..N-1
       y_0 = 10, v_0 = 0, v_N = 0, v_t >= -1 (1 <= t <= N-1), |u_t| <= 0.2,
  h = 4e-4 (OSIL coefficients 0.0004, 8e-06 = 0.02h, 8e-05 = 0.2h, 0.0002 = h/2).

Dual function: for any (mu, lam), minimizing the Lagrangian separately over
  y_t in R (convex quadratic), u_t in [-0.2, 0.2] (linear), and v_t in V_t (quadratic;
  V_t = [-1, inf) intersected with rigorous reachability bounds)
gives a valid lower bound. Where lam_t < 0 the v_t-term is concave and the finite
reachability bounds V_t are needed; they come from forward-backward interval
propagation of the dynamics (a DP over interval-valued states).
"""
import json
import sys
import time

import mpmath as mp
import numpy as np

from optcdeg2_common import N, costates, load_minlplib, to_osil
from osil_eval import check, load

iv = mp.iv


def pattern_check(I):
    lb, ub = I["lb"], I["ub"]
    ui = list(range(0, N - 1)) + [N]
    yi = list(range(N + 1, 2 * N + 2))
    vi = list(range(2 * N + 2, 3 * N + 2)) + [N - 1]
    assert len(lb) == 3 * N + 2 and I["ncons"] == 2 * N
    for j in ui:
        assert lb[j] == -0.2 and ub[j] == 0.2
    assert lb[yi[0]] == ub[yi[0]] == 10.0 and all(np.isinf(lb[j]) and np.isinf(ub[j]) for j in yi[1:])
    assert lb[vi[0]] == ub[vi[0]] == 0.0 and lb[vi[N]] == ub[vi[N]] == 0.0
    assert all(lb[j] == -1.0 and np.isinf(ub[j]) for j in vi[1:N])
    obj = I["rows"][-1]
    assert obj["lin"] == {} and obj["nl"] is None and sorted(obj["quad"]) == sorted((j, j, 0.0002) for j in yi)
    for t in range(N):
        r = I["rows"][t]
        assert r["lin"] == {yi[t]: -1.0, yi[t + 1]: 1.0, vi[t]: -0.0004} and r["quad"] == [] and r["lb"] == r["ub"] == 0.0
        r = I["rows"][N + t]
        assert r["lin"] == {ui[t]: -0.0004, yi[t]: 8e-06, vi[t]: -1.0, vi[t + 1]: 1.0}, (t, r["lin"])
        assert r["quad"] == [(vi[t], vi[t], 8e-05)] and r["lb"] == r["ub"] == 0.0


def state_bounds(passes=2):
    """Forward/backward interval propagation. Returns lists of (lo, hi) mpf for y_t and v_t.
    g(v) = v - 0.2 h v^2 is increasing for v < 1/(0.4h) = 6250, which is asserted."""
    iv.dps = 25
    h = iv.mpf("0.0004")
    Ulo, Uhi = iv.mpf("-0.2"), iv.mpf("0.2")
    Y = [None] * (N + 1)
    V = [None] * (N + 1)
    Y[0] = iv.mpf(10)
    V[0] = iv.mpf(0)
    INF = mp.mpf("1e6")
    for t in range(1, N + 1):  # initial wide boxes
        Y[t] = iv.mpf([-INF, INF])
        V[t] = iv.mpf([-1, INF]) if t < N else iv.mpf(0)

    def g(x):  # x: point interval endpoint
        return x - iv.mpf("0.2") * h * x * x

    def inter(a, b):
        lo = max(mp.mpf(a.a), mp.mpf(b.a))
        hi = min(mp.mpf(a.b), mp.mpf(b.b))
        assert lo <= hi, "empty intersection: infeasible box"
        return iv.mpf([lo, hi])

    for p in range(passes):
        for t in range(N):  # forward
            vlo, vhi = mp.mpf(V[t].a), mp.mpf(V[t].b)
            assert vhi < 6000
            gv = iv.mpf([mp.mpf(g(iv.mpf(vlo)).a), mp.mpf(g(iv.mpf(vhi)).b)])
            vn = gv + h * iv.mpf([Ulo.a, Uhi.b]) - iv.mpf("0.02") * h * Y[t]
            V[t + 1] = inter(V[t + 1], vn)
            Y[t + 1] = inter(Y[t + 1], Y[t] + h * V[t])
        for t in range(N - 1, -1, -1):  # backward
            # y_t = y_{t+1} - h v_t
            Y[t] = inter(Y[t], Y[t + 1] - h * V[t])
            # g(v_t) = v_{t+1} - h u_t + 0.02 h y_t ; invert the increasing g on v < 6250
            rhs = V[t + 1] - h * iv.mpf([Ulo.a, Uhi.b]) + iv.mpf("0.02") * h * Y[t]
            lo, hi = mp.mpf(rhs.a), mp.mpf(rhs.b)
            # g^{-1}(z) = (1 - sqrt(1 - 0.8 h z)) / (0.4 h); increasing in z
            def ginv(z, up):
                zi = iv.mpf(z)
                r = (1 - iv.sqrt(1 - iv.mpf("0.8") * h * zi)) / (iv.mpf("0.4") * h)
                return mp.mpf(r.b) if up else mp.mpf(r.a)
            V[t] = inter(V[t], iv.mpf([ginv(lo, False), ginv(hi, True)]))
    return Y, V


def dual_value(mu, lam, V, exact=True):
    """Interval evaluation of the dual function (see module docstring)."""
    iv.dps = 30
    h = iv.mpf("0.0004")
    M = [iv.mpf(float(x)) for x in mu]
    L = [iv.mpf(float(x)) for x in lam]
    tot = h / 2 * 100 - M[0] * 10 + L[0] * iv.mpf("0.02") * h * 10  # y_0 = 10 terms
    # y_t, 1..N-1
    for t in range(1, N):
        b = M[t - 1] - M[t] + iv.mpf("0.02") * h * L[t]
        tot -= b * b / (2 * h)
    tot -= M[N - 1] * M[N - 1] / (2 * h)  # y_N
    # u_t
    for t in range(N):
        tot -= iv.mpf("0.2") * h * abs(L[t])
    # v_t, 1..N-1 : a v^2 + b v over V_t
    worst = []
    for t in range(1, N):
        a = iv.mpf("0.2") * h * L[t]
        b = L[t - 1] - L[t] - h * M[t]
        lo, hi = mp.mpf(V[t].a), mp.mpf(V[t].b)
        cands = [iv.mpf(lo), iv.mpf(hi)]
        if mp.mpf(a.a) > 0:  # strictly convex: add clipped stationary point (any point of V_t is a valid candidate
            # for the minimum only if it is the true minimizer; we use the enclosure of -b/(2a))
            s = -b / (2 * a)
            slo, shi = max(mp.mpf(s.a), lo), min(mp.mpf(s.b), hi)
            if slo <= shi:
                # minimum over the box is >= value at the stationary point = -b^2/(4a)
                cands.append(None)
        vals = []
        for cnd in cands:
            if cnd is None:
                vals.append(-(b * b) / (4 * a))
            else:
                vals.append(a * cnd * cnd + b * cnd)
        m = min(mp.mpf(x.a) for x in vals)
        tot += iv.mpf(m)
    return tot


def main():
    t0 = time.time()
    I = load("optcdeg2")
    pattern_check(I)
    u, y, v = load_minlplib()
    chk = check("optcdeg2", to_osil(u, y, v), I)
    print("primal", chk, flush=True)
    Y, V = state_bounds(passes=int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    print("bounds done", time.time() - t0, flush=True)
    vb = np.array([[float(mp.mpf(x.a)), float(mp.mpf(x.b))] for x in V])
    yb = np.array([[float(mp.mpf(x.a)), float(mp.mpf(x.b))] for x in Y])
    np.save("logs/optcdeg2_vbounds.npy", vb)
    np.save("logs/optcdeg2_ybounds.npy", yb)
    sw = np.where(np.diff(np.sign(u)) != 0)[0]
    m0, l0 = costates(y, v, 0.0)
    m1, l1 = costates(y, v, 1.0)
    c = -l0[sw[1]] / (l1[sw[1]] - l0[sw[1]])
    mu, lam = costates(y, v, c)
    np.save("logs/optcdeg2_mu.npy", mu)    # multipliers used by optcdeg2_head.py, optcdeg2_verify.py
    np.save("logs/optcdeg2_lam.npy", lam)  # and the verifier's v_optcdeg2.py
    D = dual_value(mu, lam, V)
    rec = dict(name="optcdeg2", primal_obj=chk["obj"], primal_cons_viol=chk["cons_viol"], primal_bound_viol=chk["bound_viol"],
               dual_bound=float(mp.mpf(D.a)), dual_upper_end=float(mp.mpf(D.b)), lamN1=float(c), seconds=time.time() - t0)
    print(json.dumps(rec))
    with open("logs/optcdeg2_bound.json", "w") as f:
        json.dump(rec, f, indent=1)


if __name__ == "__main__":
    main()
