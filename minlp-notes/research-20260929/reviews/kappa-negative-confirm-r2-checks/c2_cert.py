"""Referee check (round-2 confirmation of kappa-negative.md, item R1).

Independent exact check of f* = J(zbar) at the three kappa = -0.5, N = 4000 grids of Section 9.1.
Own code, written from the note's definitions (Section 9 two-switch toy, Section 0 family, Lemma 5.2):

  J(u) = h sum_t [(x_t - a_t)^2/2 + k x_t u_t] + Phi(x_N),  x_{t+1} = x_t + h u_t,  x_0 = 0,
  Phi(x) = -3x + x^2/2  (= (x - 3)^2/2 + const),  k = 1/2  (kappa = -1/2),  |u| <= 1,  box |x| <= 4,
  a = 4 on [0, t1), -4 on [t1, t2), 4 on [t2, 2],  a_t = a(t h) with decimal jump times read exactly.

Family S_t(x) = p^A_t (x - x^A_t) + P (x - x^A_t)^2/2, P = -k, slopes = costates of the anchor z^A.
Derived here (not imported): the stage residual minus its value at z^A_t is
  h sigma^A_t om + h d^2/2 + (h^2/2)(-k) om^2      (K_t = h, beta_t = P + k = 0),
and the terminal term has curvature 1 + k > 0 and zero slope.  States stay in [-2, 2], inside the box,
so the minimizing d is 0 and the loss of stage t is max(0, -min over the two ends of the control range).

Certificate: lifted node on the fractional stage n (interval V from the affine zero-loss conditions of
all other stages), plus the two outer nodes [V_hi, 1] and [-1, V_lo] anchored at z(V_hi), z(V_lo)
(the anchor the referee chose; the author's anchors are node KKT points).
"""
import json
import sys
import time
from fractions import Fraction as Fr

K = Fr(1, 2)


def data(N, t1, t2):
    h = Fr(2, N)
    a = []
    for t in range(N):
        th = t * h
        a.append(Fr(4) if th < t1 else (Fr(-4) if th < t2 else Fr(4)))
    return h, a


def sim(u, h, a):
    N = len(u)
    x = [Fr(0)] * (N + 1)
    for t in range(N):
        x[t + 1] = x[t] + h * u[t]
    J = sum(h * ((x[t] - a[t]) ** 2 / 2 + K * x[t] * u[t]) for t in range(N)) + (-3 * x[N] + x[N] ** 2 / 2)
    p = [Fr(0)] * (N + 1)
    p[N] = -3 + x[N]
    for t in range(N - 1, -1, -1):
        p[t] = p[t + 1] + h * (x[t] - a[t] + K * u[t])
    sig = [K * x[t] + p[t + 1] for t in range(N)]
    return x, J, sig


def Hij(i, j, h, N):
    m = max(i, j)
    return h * h * (h * (N - 1 - m) + 1 + (K if i != j else 0))


def stage_loss(sig_t, u_t, lo, hi, h):
    """loss of a stage with control range [lo, hi], anchor control u_t, switching value sig_t."""
    vals = [Fr(0)]
    for e in (lo, hi):
        om = e - u_t
        vals.append(h * sig_t * om - (h * h / 2) * K * om * om)
    return max(Fr(0), -min(vals))


def run(t1s, t2s, N, s1, s2, n):
    t0 = time.time()
    t1, t2 = Fr(t1s), Fr(t2s)
    h, a = data(N, t1, t2)
    u = [Fr(1)] * N
    for t in range(s1, s2):
        u[t] = Fr(-1)
    # fractional stage n: solve sigma_n(v) = 0 exactly (sigma_n is affine in v with slope H_nn / h)
    u[n] = Fr(0)
    _, _, sig0 = sim(u, h, a)
    Hnn = Hij(n, n, h, N)
    v = -h * sig0[n] / Hnn
    u[n] = v
    x, J, sig = sim(u, h, a)
    assert sig[n] == 0 and -1 < v < 1
    # sanity: J is the stated quadratic (exact finite differences at two stages)
    for (i, j) in ((n, n), (n, s2 if n != s2 else s1)):
        du = Fr(1, 7)
        ui = list(u); ui[i] += du
        if i != j:
            ui[j] += du
        _, Ji, _ = sim(ui, h, a)
        pred = h * du * (sig[i] + (sig[j] if i != j else 0)) + du * du * (
            (Hij(i, i, h, N) / 2) + ((Hij(j, j, h, N) / 2 + Hij(i, j, h, N)) if i != j else 0))
        assert Ji - J == pred, (i, j)
    # KKT signs
    viol = [t for t in range(N) if t != n and ((u[t] == 1 and sig[t] > 0) or (u[t] == -1 and sig[t] < 0))]
    assert not viol, viol[:5]
    assert max(abs(xx) for xx in x) <= 2
    # plain certificate (anchor zbar)
    loss = {t: stage_loss(sig[t], u[t], Fr(-1), Fr(1), h) for t in range(N)}
    fail = {t: float(l / h ** 2) for t, l in loss.items() if l > 0}
    gap = sum(loss.values()) / h ** 2
    # lifted interval V: sigma_t(v') = sig_t + c_t (v' - v), c_t = H_tn / h > 0
    lo, hi = Fr(-1), Fr(1)
    for t in range(N):
        if t == n:
            continue
        c = Hij(t, n, h, N) / h
        assert c > 0
        if u[t] == 1:     # need sigma_t(v') <= -h k  (far move om = -2: -2 h sig - 2 h^2 k >= 0)
            hi = min(hi, v + (-h * K - sig[t]) / c)
        else:             # need sigma_t(v') >= h k
            lo = max(lo, v + (h * K - sig[t]) / c)
    assert lo <= v <= hi
    # check the end points by rebuilding z(v') from scratch: all stages other than n exact
    ends = {}
    for e in (lo, hi):
        ue = list(u); ue[n] = e
        xe, Je, sge = sim(ue, h, a)
        le = [stage_loss(sge[t], ue[t], Fr(-1), Fr(1), h) for t in range(N) if t != n]
        assert max(le) == 0
        assert Je == J + Hnn / 2 * (e - v) ** 2
        ends[e] = (Je, sge[n])
    nodes = [dict(kind="lifted", V=[float(lo), float(hi)], bound_minus_J_over_h2=0.0)]
    ok = True
    for (l_, r_, anc) in ((hi, Fr(1), hi), (Fr(-1), lo, lo)):
        if l_ >= r_:
            continue
        Je, sn = ends[anc]
        ln = stage_loss(sn, anc, l_, r_, h)
        B = Je - ln
        ok = ok and B >= J
        nodes.append(dict(kind="fixed", interval=[float(l_), float(r_)], anchor=float(anc),
                          anchor_J_minus_J_over_h2=float((Je - J) / h ** 2), stage_n_loss_over_h2=float(ln / h ** 2),
                          bound_minus_J_over_h2=float((B - J) / h ** 2), exact_bound_minus_J=str(B - J) if B - J < 1 else "big"))
    rec = dict(t1=t1s, t2=t2s, N=N, switching=[s1, s2], frac=n, u_frac=float(v), J=float(J), plain_gap_over_h2=float(gap),
               failing=fail, V=[float(lo), float(hi)], nodes=nodes, certified=ok, sec=round(time.time() - t0, 1))
    return rec


if __name__ == "__main__":
    cases = [("0.5", "1.5", 4000, 503, 1495, 503), ("0.7", "1.3", 4000, 1196, 1557, 1196),
             ("0.75", "1.25", 4000, 1387, 1581, 1580)]
    out = []
    for c in cases:
        r = run(*c)
        print(json.dumps(r), flush=True)
        out.append(r)
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "logs/cert4000.json", "w"), indent=1)
