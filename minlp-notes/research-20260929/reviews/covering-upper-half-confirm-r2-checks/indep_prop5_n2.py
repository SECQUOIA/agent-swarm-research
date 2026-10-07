"""Independent n = 2 check of Proposition 5 with the slope clause (round 2).

The note's own check (check_prop5_slopes.py) uses n = 1.  Here: a path with two
edges, s1, s2 in [-1, 1],

  root   f_r(s1)     = a_r s1^2 + b_r s1,
  middle f_m(s1, s2) = kap (s1 - s2)^2 + c_m s2^2,
  leaf   f_l(s2)     = a_l s2^2 + b_l s2,

with parameters chosen so that all partial minimizers are interior.  Then U_e,
V_e, L_e = f* - V_e, w_e, psi'_e = U_e - theta'_e w_e are exact quadratics
(tau' = 1/7, theta'_1 = 5/7 for the middle edge, theta'_2 = 2/7 for the leaf
edge).  Cells: rule R3 adapted to tau' with tolerance eps/(2n) = eps/4 (proof
of Theorem 3 with h = 4r/tau').  Exact leaves aligned with the cells: root
leaves = cells of P_1, middle leaves = products D1 x D2, leaf leaves = cells of
P_2.  (LC)/(CM) only for pairs whose interiors meet, maximal intercepts.  The
certificate value l_r is computed exactly (box minima of quadratics).

Slopes compared:
  (a) 0 (constant minorants);
  (b) the balanced-minimizer slope of the closed-cell bracket, half-width tau' w;
  (c) the two extreme slopes (and a random slope) of the interval of slopes
      whose intercept-minimized closed-cell bracket is <= eps/(2n).
Proposition 5 predicts f* - l_r <= eps/2 for (b) and (c) (exact leaves, so the
bag terms of Lemma 1' are <= 0), and nothing for (a).
"""
import numpy as np
from scipy.optimize import minimize_scalar, brentq


def min1d(A, B, lo, hi):
    """exact min over [lo, hi] of A x^2 + B x (arrays allowed for B, lo, hi)."""
    lo = np.asarray(lo, float); hi = np.asarray(hi, float)
    B = np.asarray(B, float)
    v = np.minimum(A * lo * lo + B * lo, A * hi * hi + B * hi)
    if A > 0:
        x = np.clip(-B / (2 * A), lo, hi)
        v = np.minimum(v, A * x * x + B * x)
    return v


def qv(q, s):
    return q[0] * s * s + q[1] * s + q[2]


def qmax(q, lo, hi):
    return -min1d(-q[0], -q[1], lo, hi) + q[2]


def qmin(q, lo, hi):
    return min1d(q[0], q[1], lo, hi) + q[2]


def setup(a_r, b_r, kap, c_m, a_l, b_l):
    K2 = kap + c_m + a_l
    K1 = a_r + kap
    assert K2 > 0 and K1 > 0 and kap + c_m > 0
    # interior partial minimizers for all |s| <= 1
    assert (2 * kap + abs(b_l)) / (2 * K2) <= 1 + 1e-12
    assert (2 * kap + abs(b_r)) / (2 * K1) <= 1 + 1e-12
    U2 = (a_l, b_l, 0.0)
    U1 = (kap - kap ** 2 / K2, kap * b_l / K2, -b_l ** 2 / (4 * K2))
    V1 = (a_r, b_r, 0.0)
    V2 = (kap + c_m - kap ** 2 / K1, kap * b_r / K1, -b_r ** 2 / (4 * K1))
    s1 = (U1[0] + V1[0], U1[1] + V1[1], U1[2] + V1[2])
    s2 = (U2[0] + V2[0], U2[1] + V2[1], U2[2] + V2[2])
    fs1 = float(qmin(s1, -1.0, 1.0)); fs2 = float(qmin(s2, -1.0, 1.0))
    assert abs(fs1 - fs2) < 1e-12, (fs1, fs2)
    fstar = fs1
    edges = []
    tau = 1.0 / 7
    for U, V, th in [(U1, V1, 5 * tau), (U2, V2, 2 * tau)]:
        L = (-V[0], -V[1], fstar - V[2])
        w = (U[0] - L[0], U[1] - L[1], U[2] - L[2])
        psi = (U[0] - th * w[0], U[1] - th * w[1], U[2] - th * w[2])
        P = tuple(psi[i] + tau * w[i] for i in range(3))   # upper sliver
        Q = tuple(psi[i] - tau * w[i] for i in range(3))   # lower sliver
        M = max(2 * U[0], -2 * L[0], 0.0)
        G = max(abs(2 * U[0] * x + U[1]) for x in (-1, 1))
        G = max(G, max(abs(2 * L[0] * x + L[1]) for x in (-1, 1)))
        wmin_all = float(qmin(w, -1.0, 1.0))
        assert wmin_all >= -1e-12
        edges.append(dict(U=U, L=L, w=w, psi=psi, P=P, Q=Q, M=M, G=G))
    return fstar, edges


def r3_cells(e, eps, n=2):
    tau = 1.0 / (3 * n + 1)
    tol = eps / (2 * n)
    out, stack = [], [(-1.0, 1.0)]
    while stack:
        lo, hi = stack.pop()
        r = (hi - lo) / 2
        wmin = max(float(qmin(e["w"], lo, hi)), 0.0)
        if min(lo + 1, 1 - hi) >= 4 * r / tau:
            B = (16 / tau + 0.5) * e["M"] * r * r - tau * wmin
        else:
            B = 2 * e["G"] * r + 2.5 * e["M"] * r * r - 2 * tau * wmin
        if B > tol:
            mid = (lo + hi) / 2
            stack += [(lo, mid), (mid, hi)]
        else:
            out.append((lo, hi))
    return sorted(out)


def bracket(mu, e, lo, hi):
    # max_{cl D}(mu s - P) + max_{cl D}(Q - mu s); the intercept cancels
    P, Q = e["P"], e["Q"]
    return float(qmax((-P[0], mu - P[1], -P[2]), lo, hi)
                 + qmax((Q[0], Q[1] - mu, Q[2]), lo, hi))


def slopes(e, cells, eps, n=2):
    tol = eps / (2 * n)
    bal, lo_s, hi_s, gmax = [], [], [], -np.inf
    for lo, hi in cells:
        res = minimize_scalar(lambda m: bracket(m, e, lo, hi),
                              bounds=(-100, 100), method="bounded",
                              options={"xatol": 1e-13})
        m0 = res.x
        g0 = bracket(m0, e, lo, hi)
        gmax = max(gmax, g0)
        bal.append(m0)
        f = lambda m: bracket(m, e, lo, hi) - tol
        if g0 < tol:
            hi_s.append(brentq(f, m0, m0 + 1e4, xtol=1e-14))
            lo_s.append(brentq(f, m0 - 1e4, m0, xtol=1e-14))
        else:
            hi_s.append(m0); lo_s.append(m0)
    return np.array(bal), np.array(lo_s), np.array(hi_s), gmax


def cert_value(inst, cells1, cells2, mu1, mu2):
    a_r, b_r, kap, c_m, a_l, b_l = inst
    lo2 = np.array([c[0] for c in cells2]); hi2 = np.array([c[1] for c in cells2])
    # leaf bag: beta_2 = min_{cl D2} (f_l - mu2 s2)
    beta2 = min1d(a_l, b_l - mu2, lo2, hi2)
    beta1 = np.empty(len(cells1))
    for j, (lo1, hi1) in enumerate(cells1):
        m1 = mu1[j]
        # min over D1 x D2 of kap (s1 - s2)^2 + c_m s2^2 + mu2 s2 - m1 s1,
        # plus beta2.  Hessian det = 4 kap c_m: PD iff c_m > 0.
        best = np.full(len(cells2), np.inf)
        # edges s1 = lo1, hi1 (min over s2 in [lo2, hi2])
        for s1 in (lo1, hi1):
            v = min1d(kap + c_m, mu2 - 2 * kap * s1, lo2, hi2) \
                + kap * s1 * s1 - m1 * s1
            best = np.minimum(best, v)
        # edges s2 = lo2, hi2 (min over s1 in [lo1, hi1]), vectorized in s2
        for s2 in (lo2, hi2):
            s1 = np.clip(s2 + m1 / (2 * kap), lo1, hi1)
            cand = [s1, np.full_like(s2, lo1), np.full_like(s2, hi1)]
            for x in cand:
                v = kap * (x - s2) ** 2 + c_m * s2 ** 2 + mu2 * s2 - m1 * x
                best = np.minimum(best, v)
        if c_m > 0:   # interior stationary point
            # grad: 2kap(s1-s2) - m1 = 0; -2kap(s1-s2) + 2c_m s2 + mu2 = 0
            s2 = (m1 - mu2) / (2 * c_m)
            s1 = s2 + m1 / (2 * kap)
            inside = (s1 >= lo1) & (s1 <= hi1) & (s2 >= lo2) & (s2 <= hi2)
            v = kap * (s1 - s2) ** 2 + c_m * s2 ** 2 + mu2 * s2 - m1 * s1
            best = np.where(inside, np.minimum(best, v), best)
        beta1[j] = np.min(best + beta2)
    lo1 = np.array([c[0] for c in cells1]); hi1 = np.array([c[1] for c in cells1])
    return float(np.min(min1d(a_r, b_r + mu1, lo1, hi1) + beta1))


def main():
    rng = np.random.default_rng(5)
    insts = {
        "tilted (a_r, b_r, kap, c_m, a_l, b_l) = (1, -1, 5, 0, 1, 1)": (1.0, -1.0, 5.0, 0.0, 1.0, 1.0),
        "asymmetric (0.5, -0.8, 10, 0.3, 2, 0.6)": (0.5, -0.8, 10.0, 0.3, 2.0, 0.6),
        "Proposition 4, beta = 1, kappa = 10: (2, 0, 10, -1, 2, 0)": (2.0, 0.0, 10.0, -1.0, 2.0, 0.0),
    }
    ok = True
    for name, inst in insts.items():
        fstar, edges = setup(*inst)
        print(f"{name}: f* = {fstar:.6f}, M_e = {[round(e['M'], 3) for e in edges]}, "
              f"G_e = {[round(e['G'], 3) for e in edges]}")
        for eps in [1e-2, 1e-3, 1e-4]:
            c1 = r3_cells(edges[0], eps); c2 = r3_cells(edges[1], eps)
            b1, l1, h1, g1 = slopes(edges[0], c1, eps)
            b2, l2, h2, g2 = slopes(edges[1], c2, eps)
            gz = fstar - cert_value(inst, c1, c2, 0 * b1, 0 * b2)
            gb = fstar - cert_value(inst, c1, c2, b1, b2)
            gext = []
            for (m1, m2) in [(l1, l2), (h1, h2), (l1, h2), (h1, l2)]:
                gext.append(fstar - cert_value(inst, c1, c2, m1, m2))
            u1 = rng.uniform(size=len(b1)); u2 = rng.uniform(size=len(b2))
            gr = fstar - cert_value(inst, c1, c2, l1 + u1 * (h1 - l1),
                                    l2 + u2 * (h2 - l2))
            worst = max([gb, gr] + gext)
            ok = ok and worst <= eps / 2 + 1e-12 and max(g1, g2) <= eps / 4 + 1e-12
            print(f"  eps={eps:g}: cells {len(c1)}, {len(c2)}; max balanced bracket "
                  f"{max(g1, g2):.2e} (<= eps/4 = {eps / 4:.1e}); gap/eps: "
                  f"constant {gz / eps:.3f}, balanced {gb / eps:.3f}, "
                  f"extreme slopes {max(gext) / eps:.5f}, random {gr / eps:.3f}")
    print("slope-clause cases within eps/2 and brackets within eps/(2n):", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
