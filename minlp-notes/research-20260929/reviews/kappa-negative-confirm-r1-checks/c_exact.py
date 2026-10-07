"""Exact (rational) re-checks, confirmation referee round 1, written from the note's definitions.

part two:  two-switch toy of Section 9.1, kappa = -0.5 (k = 1/2), (t1, t2) = (7/10, 13/10), N = 500, 1000, 2000:
           float pattern search (c_two.py), exact KKT point, exact plain-certificate stage losses with the
           family P = -k (beta = 0, K = h): vertex stage loss = max(0, h^2|kappa|Delta^2/2 - h|sigma|Delta),
           fractional stage loss = (h^2/2)|kappa| max over the two ends of omega^2.  Also the best and
           second-best monotone pattern values near the switches (float scan, for information).
part qneg: single-switch toys (a = 2 on [0,1), -1 after; T = 2): q<0 toy k = 3, Phi = x - x^2; kappa = -1
           toy k = 1, Phi = x.  Exact best single-switch bang-bang KKT point at N = 200, 400, 2000; vertex
           margins |sigma|/h below Delta|kappa|/2; at N = 2000 the lifted interval V for the smallest-margin
           stage n and the bound of the outer node anchored at z(r), r the inner end of V.
"""
import json
import sys
from fractions import Fraction as Fr

T = Fr(2)


def piece(pts, N):
    out = []
    for t in range(N):
        v = pts[0][1]
        for ti, vi in pts:
            if Fr(ti) * N <= Fr(t) * T:
                v = vi
        out.append(v)
    return out


def traj(N, a, k, phi1, phi2, u):
    h = T / N
    x = [Fr(0)]
    for t in range(N):
        x.append(x[-1] + h * u[t])
    J = sum(h * ((x[t] - a[t]) ** 2 / 2 + k[t] * x[t] * u[t]) for t in range(N)) + phi1 * x[N] + phi2 * x[N] ** 2 / 2
    p = [None] * (N + 1)
    p[N] = phi1 + phi2 * x[N]
    for t in range(N - 1, -1, -1):
        p[t] = p[t + 1] + h * (x[t] - a[t] + k[t] * u[t])
    sig = [k[t] * x[t] + p[t + 1] for t in range(N)]
    return x, J, sig


def Hij(N, k, phi2, i, j):
    h = T / N
    m = max(i, j)
    return h * h * (h * (N - 1 - m) + phi2 + (k[m] if i != j else 0))


def part_two():
    sys.path.insert(0, ".")
    from c_two import Toy, kkt_search
    recs = []
    for N in (500, 1000, 2000):
        ft = Toy("0.7", "1.3", 0.5, 0.5, "1", N)
        r = kkt_search(ft, int(0.299 * N), int(0.389 * N), max(6, N // 50), 12)
        a = [Fr(v) for v in piece((("0", 4), ("0.7", -4), ("1.3", 4)), N)]
        k = [Fr(1, 2)] * N
        phi1, phi2 = Fr(-3), Fr(1)
        u = [Fr(1) if v >= 1 - 1e-12 else Fr(-1) if v <= -1 + 1e-12 else None for v in r["u"]]
        F = [t for t in range(N) if u[t] is None]
        for t in F:
            u[t] = Fr(0)
        if F:
            _, _, sig0 = traj(N, a, k, phi1, phi2, u)
            h = T / N
            # solve H_FF v = -h sig0_F   (exact, |F| <= 2)
            A = [[Hij(N, k, phi2, i, j) for j in F] for i in F]
            b = [-h * sig0[i] for i in F]
            if len(F) == 1:
                sol = [b[0] / A[0][0]]
            else:
                det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
                sol = [(b[0] * A[1][1] - A[0][1] * b[1]) / det, (A[0][0] * b[1] - A[1][0] * b[0]) / det]
            for t, v in zip(F, sol):
                u[t] = v
        x, J, sig = traj(N, a, k, phi1, phi2, u)
        h = T / N
        ok = all((sig[t] == 0) if t in F else (sig[t] <= 0 if u[t] == 1 else sig[t] >= 0) for t in range(N))
        ok = ok and all(-1 <= u[t] <= 1 for t in F)
        kap = Fr(1, 2)
        losses = {}
        for t in range(N):
            if t in F:
                L = h * h / 2 * kap * max((1 - u[t]) ** 2, (1 + u[t]) ** 2)
            else:
                L = max(Fr(0), h * h * kap * 4 / 2 - h * abs(sig[t]) * 2)
            if L > 0:
                losses[t] = L
        sw = [t for t in range(1, N) if u[t] != u[t - 1]]
        rec = dict(N=N, kkt_exact=ok, frac=[(t, float(u[t])) for t in F], change_stages=sw,
                   gap_over_h2=float(sum(losses.values()) / h ** 2),
                   losses_over_h2={t: float(L / h ** 2) for t, L in losses.items()},
                   margins_small={t: float(abs(sig[t]) / h) for t in range(N) if t not in F and abs(sig[t]) / h < 1})
        print(json.dumps(rec), flush=True)
        recs.append(rec)
    return recs


def single_switch(N, kk, phi1, phi2):
    a = [Fr(v) for v in piece((("0", 2), ("1", -1)), N)]
    k = [Fr(kk)] * N
    h = T / N
    best = None
    # search near the continuous switch (scan all s with a cheap float pre-screen would be faster; N <= 2000 ok)
    for s in range(int(0.2 * N), int(0.4 * N)):
        u = [Fr(1)] * s + [Fr(-1)] * (N - s)
        x, J, sig = traj(N, a, k, Fr(phi1), Fr(phi2), u)
        if all((sig[t] <= 0 if u[t] == 1 else sig[t] >= 0) for t in range(N)):
            if best is None or J < best[0]:
                best = (J, s, u, x, sig)
    return a, k, best


def part_qneg():
    recs = []
    for name, kk, phi1, phi2, kap in (("q<0 (k=3)", 3, 1, -2, 3), ("kappa=-1 (k=1)", 1, 1, 0, 1)):
        for N in ((200, 400) if kk == 3 else ()):
            a, k, (J, s, u, x, sig) = single_switch(N, kk, phi1, phi2)
            h = T / N
            small = sorted((float(abs(sig[t]) / h), t) for t in range(N) if abs(sig[t]) / h < kap)
            rec = dict(toy=name, N=N, switch_stage=s, small_margins=small)
            print(json.dumps(rec), flush=True)
            recs.append(rec)
        N = 2000
        a, k, (J, s, u, x, sig) = single_switch(N, kk, phi1, phi2)
        h = T / N
        n = min(range(N), key=lambda t: abs(sig[t]))
        # lifted interval for u_n: sigma_t(v) = sigma_t + H_tn (v - u_n)/h; zero loss at t != n iff
        # sigma_t(v) * (-u_t) >= 0 and |sigma_t(v)| >= h |kappa| Delta / 2 = h kap   (beta = 0, P = -k)
        lo, hi = Fr(-1), Fr(1)
        for t in range(N):
            if t == n:
                continue
            c = Hij(N, k, Fr(phi2), t, n) / h
            # need -u_t * (sig_t + c (v - u_n)) >= h kap
            A = -u[t] * c
            B = -u[t] * sig[t] - h * kap
            # A (v - u_n) + B >= 0
            if A > 0:
                lo = max(lo, u[n] - B / A)
            elif A < 0:
                hi = min(hi, u[n] - B / A)
            elif B < 0:
                lo, hi = Fr(1), Fr(-1)
        r = hi if hi < 1 else lo
        node = (r, Fr(1)) if hi < 1 else (Fr(-1), r)
        # anchor z(r)
        ur = list(u)
        ur[n] = r
        xr, Jr, sigr = traj(N, a, k, Fr(phi1), Fr(phi2), ur)
        # stage n loss over the node, family P = -k (beta = 0): -min over omega in [node - r] of h sig om + h^2 kappa om^2/2
        oms = [node[0] - r, node[1] - r]
        vals = [h * sigr[n] * om - h * h * kap * om * om / 2 for om in oms]   # concave: min at an end
        Ln = max(Fr(0), -min(vals))
        # other stages at z(r): check zero loss directly
        Lother = Fr(0)
        for t in range(N):
            if t == n:
                continue
            om = -2 * ur[t]
            Lother += max(Fr(0), -(h * sigr[t] * om - h * h * kap * om * om / 2))
        rec = dict(toy=name, N=N, switch_stage=s, n=n, margin_n=float(abs(sig[n]) / h), V_inner_end=float(r),
                   node=[float(node[0]), float(node[1])], sigma_n_at_r_over_h=float(sigr[n] / h),
                   J_anchor_minus_J_over_h2=float((Jr - J) / h ** 2), loss_n_over_h2=float(Ln / h ** 2),
                   loss_other_over_h2=float(Lother / h ** 2),
                   bound_minus_J_over_h2=float((Jr - Ln - Lother - J) / h ** 2))
        print(json.dumps(rec), flush=True)
        recs.append(rec)
    return recs


if __name__ == "__main__":
    for part in sys.argv[1:]:
        recs = dict(two=part_two, qneg=part_qneg)[part]()
        with open(f"logs/exact_{part}.json", "w") as f:
            json.dump(recs, f, indent=1, default=str)
