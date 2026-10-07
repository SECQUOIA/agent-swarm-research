"""Independent checks for the COPS chain certificate (reviewer code).

1. OSIL structure of chainN (own assertions).
2. z-parametrization of the linear rows and the polyline form of objective/length.
3. Summation-by-parts identity (exact rationals) .
4. Discrete catenary calibration lemma: symbolic check of the reduction and of the
   AM-GM remainder, plus direct high-precision random / adversarial tests.
5. Theorem f >= B on random feasible chains (random multipliers).
6. Primal vectors of the authors: exact linear rows, 50-digit nonlinear row/objective.
"""
import os
import random
import sys
from fractions import Fraction as Fr

import mpmath as mp

import osilx

# research-20260929/ of this checkout (this file is in research-20260929/reviews/<dir>/)
R29 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

OSIL = os.path.join(os.path.expanduser("~/.cache/minlplib/minlplib/osil"), "chain%d.osil")


def sq(k):
    return ("sqrt", ("sum", ("square", ("var", k, "1")), ("num", "1")))


def load(N):
    m = osilx.read(OSIL % N)
    n = 2 * N + 2
    assert len(m["names"]) == n and len(m["cons"]) == N + 1 and set(m["vt"]) == {"C"}
    fixed = {0: "1", N: "3"}
    for j in range(n):
        if j in fixed:
            assert m["lb"][j] == m["ub"][j] == fixed[j]
        else:
            assert (m["lb"][j], m["ub"][j]) == ("-INF", "INF")
    eta = m["cons"][0]["lin"][N + 1][1:]
    assert Fr(eta) == Fr(1, 2 * N)
    for i in range(N):
        c = m["cons"][i]
        assert (c["lb"], c["ub"], c["constant"], c["quad"], c["nl"]) == ("0", "0", "0", [], None)
        assert c["lin"] == {i: "-1", i + 1: "1", N + 1 + i: "-" + eta, N + 2 + i: "-" + eta}
    c = m["cons"][N]
    assert (c["lb"], c["ub"], c["constant"], c["lin"], c["quad"]) == ("4", "4", "0", {}, [])
    t = []
    for i in range(N):
        t += [sq(N + 1 + i), sq(N + 2 + i)]
    assert c["nl"] == ("product", ("sum",) + tuple(t), ("num", eta))
    o = m["obj"]
    assert (o["sense"], o["constant"], o["lin"], o["quad"]) == ("min", "0", {}, [])
    t = []
    for i in range(N):
        t += [("product", sq(N + 1 + i), ("var", i, "1")), ("product", sq(N + 2 + i), ("var", i + 1, "1"))]
    assert o["nl"] == ("product", ("sum",) + tuple(t), ("num", eta))
    return m, eta


def check_param(N, m, eta, trials=3):
    """random z -> (x,u): linear rows exactly zero (Fractions); nonlinear parts = polyline form."""
    rnd = random.Random(1)
    E = Fr(eta)
    h = 2 * E
    mp.mp.dps = 60
    for _ in range(trials):
        zin = [Fr(rnd.randint(-300000, 400000), 100000) for _ in range(N)]
        z = [2 - zin[0]] + zin + [6 - zin[-1]]
        x = [(z[i] + z[i + 1]) / 2 for i in range(N + 1)]
        u = [(z[i + 1] - z[i]) / (2 * E) for i in range(N + 1)]
        X = x + u
        assert x[0] == 1 and x[N] == 3
        for i in range(N):
            assert osilx.ev_row(m["cons"][i], X, Fr, {}) == 0
        # inverse map: z_i = x_i - eta u_i, z_{N+1} = x_N + eta u_N
        assert all(z[i] == x[i] - E * u[i] for i in range(N + 1)) and z[N + 1] == x[N] + E * u[N]
        Xm = [mp.mpf(v.numerator) / v.denominator for v in X]
        fns = {"sqrt": mp.sqrt}
        obj = osilx.ev_tree(m["obj"]["nl"], Xm, lambda s: mp.mpf(s), fns)
        ln = osilx.ev_tree(m["cons"][N]["nl"], Xm, lambda s: mp.mpf(s), fns)
        zm = [mp.mpf(v.numerator) / v.denominator for v in z]
        em, hm = mp.mpf(1) / (2 * N), mp.mpf(1) / N
        lam0 = mp.sqrt(em ** 2 + (zm[1] - 1) ** 2)
        lamN = mp.sqrt(em ** 2 + (3 - zm[N]) ** 2)
        lam = {k: mp.sqrt(hm ** 2 + (zm[k + 1] - zm[k]) ** 2) for k in range(1, N)}
        f2 = lam0 + 3 * lamN + sum(lam[k] * (zm[k] + zm[k + 1]) / 2 for k in lam)
        L2 = lam0 + lamN + sum(lam.values())
        assert abs(obj - f2) < mp.mpf(10) ** -50 and abs(ln - L2) < mp.mpf(10) ** -50, (obj - f2, ln - L2)
    return True


def check_identity(N, trials=5):
    rnd = random.Random(2)
    for _ in range(trials):
        z = [None] + [Fr(rnd.randint(-10 ** 7, 10 ** 7), rnd.randint(1, 10 ** 4)) for _ in range(N)]
        lam = [None] + [Fr(rnd.randint(-10 ** 6, 10 ** 6), rnd.randint(1, 999)) for _ in range(N - 1)]
        V = Fr(rnd.randint(-10 ** 6, 10 ** 6), 7)
        L = sum(lam[1:])
        v = [None, V]
        for k in range(1, N):
            v.append(v[k] + lam[k])
        lhs = sum(lam[k] * (z[k] + z[k + 1]) / 2 for k in range(1, N))
        rhs = (V + L) * z[N] - V * z[1] - sum((v[k] + lam[k] / 2) * (z[k + 1] - z[k]) for k in range(1, N))
        assert lhs == rhs and v[N] == V + L
    return True


def lemma_symbolic():
    """sympy: (i) G(b)-G(a)-c-|m|*sqrt(...) equals the step-2 expression (H'=1, a,b via sinh),
    (ii) step-2 expression - f(D) = (sqrt(tanh D) u cosh D - sqrt(Y coth D))^2, Y = (1+u^2)sh^2 D - sh^2 tau."""
    import sympy as sp
    pa, pb, t = sp.symbols("phi_a phi_b tau", real=True)
    S, D = (pa + pb) / 2, (pb - pa) / 2
    G = lambda ph: (sp.sinh(ph) * sp.cosh(ph) + ph) / 2      # G(sinh phi) with H' = 1
    c = 2 * G(t)
    a, b = sp.sinh(pa), sp.sinh(pb)
    lhs_diff = G(pb) - G(pa) - c
    u = sp.sinh(S)  # sign handled separately: |(a+b)/2| = |u| cosh D
    X = sp.sinh(D) * sp.cosh(D)
    step2_noroot = D - t + (1 + 2 * u ** 2) * X - sp.sinh(t) * sp.cosh(t)
    r1 = sp.simplify(sp.expand_trig(sp.expand((lhs_diff - step2_noroot).rewrite(sp.exp))))
    m = sp.simplify(((a + b) / 2 - u * sp.cosh(D)).rewrite(sp.exp))
    Y2 = sp.simplify((((b - a) ** 2 - (2 * sp.sinh(t)) ** 2) / 4 - ((1 + u ** 2) * sp.sinh(D) ** 2 - sp.sinh(t) ** 2)).rewrite(sp.exp))
    # AM-GM remainder, with u >= 0, Y >= 0 as symbols
    uu, DD, tt, YY = sp.symbols("u D tau Y", positive=True)
    Xs = sp.sinh(DD) * sp.cosh(DD)
    e2 = DD - tt + (1 + 2 * uu ** 2) * Xs - sp.sinh(tt) * sp.cosh(tt) - 2 * uu * sp.cosh(DD) * sp.sqrt(YY)
    fD = DD - tt - sp.sinh(tt) * sp.cosh(tt) + sp.sinh(tt) ** 2 * sp.coth(DD)
    sq_ = (sp.sqrt(sp.tanh(DD)) * uu * sp.cosh(DD) - sp.sqrt(YY * sp.coth(DD))) ** 2
    rem = sp.simplify((e2 - fD - sq_).subs(YY, (1 + uu ** 2) * sp.sinh(DD) ** 2 - sp.sinh(tt) ** 2).rewrite(sp.exp))
    fp = sp.simplify(sp.diff(fD, DD) - (1 - sp.sinh(tt) ** 2 / sp.sinh(DD) ** 2))
    f_at_tau = sp.simplify(fD.subs(DD, tt))
    return dict(G_diff_minus_step2=r1, midpoint_identity=m, root_arg_identity=Y2,
                amgm_remainder=rem, fprime_identity=fp, f_at_tau=f_at_tau)


def Gf(v, H):
    return (v * mp.sqrt(H * H + v * v) + H * H * mp.asinh(v / H)) / 2


def lemma_gap(a, b, h, H):
    """G(b) - G(a) - c - |(a+b)/2| sqrt((b-a)^2 - h^2) (should be >= 0 for b - a >= h)."""
    c = 2 * Gf(h / 2, H)
    r = (b - a) ** 2 - h * h
    assert r > -mp.mpf(10) ** (-mp.mp.dps + 10) * (h * h + 1)
    return Gf(b, H) - Gf(a, H) - c - abs((a + b) / 2) * mp.sqrt(max(r, 0))


def lemma_random(n=200000, seed=5):
    """direct 50-digit test of the lemma in its original variables, over wide scales,
    including the equality manifold and its neighbourhood."""
    mp.mp.dps = 50
    rnd = random.Random(seed)
    worst = mp.inf
    worst_rel = mp.inf
    eq_max = mp.mpf(0)
    for it in range(n):
        H = mp.mpf(10) ** rnd.uniform(-4, 3)
        h = mp.mpf(10) ** rnd.uniform(-5, 1)
        mode = it % 4
        tau = mp.asinh(h / (2 * H))
        if mode == 0:     # generic
            a = mp.mpf(rnd.uniform(-1, 1)) * mp.mpf(10) ** rnd.uniform(-4, 3)
            b = a + h + mp.mpf(10) ** rnd.uniform(-8, 3)
        elif mode == 1:   # exact equality manifold: asinh(b/H) - asinh(a/H) = 2 tau
            pa = mp.mpf(rnd.uniform(-8, 8))
            a, b = H * mp.sinh(pa), H * mp.sinh(pa + 2 * tau)
            g = lemma_gap(a, b, h, H)
            eq_max = max(eq_max, abs(g) / (abs(Gf(b, H)) + abs(Gf(a, H)) + 1e-300))
            continue
        elif mode == 2:   # perturbed equality
            pa = mp.mpf(rnd.uniform(-8, 8))
            d = 2 * tau * (1 + mp.mpf(rnd.uniform(-1, 1)) * mp.mpf(10) ** rnd.uniform(-9, -1))
            a, b = H * mp.sinh(pa), H * mp.sinh(pa + d)
            if b - a < h:
                continue
        else:             # b - a = h exactly (sqrt term vanishes) or huge separation
            a = mp.mpf(rnd.uniform(-1, 1)) * mp.mpf(10) ** rnd.uniform(-4, 2)
            b = a + h * (1 if rnd.random() < 0.5 else mp.mpf(10) ** rnd.uniform(0, 4))
        g = lemma_gap(a, b, h, H)
        scale = abs(Gf(b, H)) + abs(Gf(a, H)) + H * H
        worst = min(worst, g)
        worst_rel = min(worst_rel, g / scale)
    return dict(n=n, min_gap=mp.nstr(worst, 5), min_rel_gap=mp.nstr(worst_rel, 5),
                max_rel_equality_residual=mp.nstr(eq_max, 5))


def lemma_adversarial(seed=9):
    """for several (h, H'), minimise the lemma gap over (a, b) numerically (b = a + h + s^2)."""
    from scipy.optimize import minimize
    rnd = random.Random(seed)
    mp.mp.dps = 30
    out = []
    for _ in range(40):
        H = 10 ** rnd.uniform(-3, 1)
        h = 10 ** rnd.uniform(-3, 0)

        def obj(p):
            a, s = mp.mpf(p[0]), mp.mpf(p[1])
            hm = mp.mpf(h)
            return float(lemma_gap(a, a + hm + s * s, hm, mp.mpf(H)))
        best = min((minimize(obj, [rnd.uniform(-2, 2), rnd.uniform(0, 1)], method="Nelder-Mead",
                             options=dict(xatol=1e-12, fatol=1e-18, maxiter=4000)) for _ in range(3)),
                   key=lambda r: r.fun)
        out.append(best.fun)
    return min(out)


def theorem_random(N, trials=300, seed=4):
    """random feasible chains (length row enforced by scaling the z-deviations) vs B(V,H')."""
    mp.mp.dps = 30
    rnd = random.Random(seed)
    eta, h = mp.mpf(1) / (2 * N), mp.mpf(1) / N
    worst = mp.inf
    done = 0
    while done < trials:
        # random z profile, then scale vertical deviations from a line so the length is exactly 4
        z1 = mp.mpf(rnd.uniform(-1.5, 3.5))
        zN = mp.mpf(rnd.uniform(0.5, 5.5))
        base = [z1 + (zN - z1) * k / (N - 1) for k in range(N)]  # indices 0..N-1 = z_1..z_N
        dev = [mp.mpf(0)] + [mp.mpf(rnd.gauss(0, 1)) for _ in range(N - 2)] + [mp.mpf(0)]
        smooth = rnd.random() < 0.5
        if smooth:
            A, B_ = rnd.uniform(-3, 3), rnd.uniform(-2, 2)
            dev = [mp.mpf(A * mp.sin(mp.pi * k / (N - 1)) + B_ * mp.sin(2 * mp.pi * k / (N - 1))) for k in range(N)]

        def total_len(s):
            z = [base[k] + s * dev[k] for k in range(N)]
            l0 = mp.sqrt(eta ** 2 + (z[0] - 1) ** 2)
            lN = mp.sqrt(eta ** 2 + (3 - z[-1]) ** 2)
            return l0 + lN + sum(mp.sqrt(h ** 2 + (z[k + 1] - z[k]) ** 2) for k in range(N - 1)) - 4
        if total_len(0) >= 0:
            continue
        hi = mp.mpf(1)
        while total_len(hi) < 0:
            hi *= 2
        s = mp.findroot(total_len, (mp.mpf(0), hi), solver="anderson")
        z = [base[k] + s * dev[k] for k in range(N)]
        l0 = mp.sqrt(eta ** 2 + (z[0] - 1) ** 2)
        lN = mp.sqrt(eta ** 2 + (3 - z[-1]) ** 2)
        lam = [mp.sqrt(h ** 2 + (z[k + 1] - z[k]) ** 2) for k in range(N - 1)]
        assert abs(l0 + lN + sum(lam) - 4) < mp.mpf(10) ** -25
        f = l0 + 3 * lN + sum(lam[k] * (z[k] + z[k + 1]) / 2 for k in range(N - 1))
        L = 4 - l0 - lN
        for _ in range(5):
            V = mp.mpf(rnd.uniform(-4, 4))
            H = mp.mpf(10) ** rnd.uniform(-3, 1)
            B = l0 + 3 * lN + (V + L) * z[-1] - V * z[0] - Gf(V + L, H) + Gf(V, H) + (N - 1) * 2 * Gf(eta, H)
            worst = min(worst, f - B)
        done += 1
    return mp.nstr(worst, 6)


def theorem_near_opt(N, trials=200, seed=8):
    """perturb the (authors') optimal chain, restore the length row exactly, and compare f with
    B at the perturbed end values, using the optimal multipliers of v_chain_bnb.Window.mult
    and randomly perturbed multipliers."""
    import v_chain_bnb as vb
    mp.mp.dps = 40
    W = vb.Window(N)
    path = os.path.join(R29, "open-instances-wave2/cops/logs/chain%d_primal.txt") % N
    X = [mp.mpf(float(s)) for s in open(path).read().split()]
    eta, h = mp.mpf(1) / (2 * N), mp.mpf(1) / N
    z0 = [X[0] + eta * X[N + 1]] + [X[i] + eta * X[N + 1 + i] for i in range(1, N)]  # z_1..z_N
    rnd = random.Random(seed)
    worst, worst_opt = mp.inf, mp.inf
    for t in range(trials):
        amp = mp.mpf(10) ** rnd.uniform(-9, -1)
        dev = [mp.mpf(rnd.gauss(0, 1)) for _ in range(N)]
        if t % 2:
            dev = [mp.sin((k + 1) * mp.pi * rnd.uniform(0.2, 3) / N) for k in range(N)]

        def parts(s):
            z = [z0[k] + amp * dev[k] + s for k in range(N)]
            return z

        def total_len(z):
            l0 = mp.sqrt(eta ** 2 + (z[0] - 1) ** 2)
            lN = mp.sqrt(eta ** 2 + (3 - z[-1]) ** 2)
            lam = [mp.sqrt(h ** 2 + (z[k + 1] - z[k]) ** 2) for k in range(N - 1)]
            return l0, lN, lam

        # restore the length by scaling the deviation from the straight chord
        def F(sc):
            z = [z0[k] + amp * dev[k] for k in range(N)]
            zl = [z[0] + (z[-1] - z[0]) * k / (N - 1) for k in range(N)]
            zz = [zl[k] + sc * (z[k] - zl[k]) for k in range(N)]
            l0, lN, lam = total_len(zz)
            return l0 + lN + sum(lam) - 4, zz
        sc = mp.findroot(lambda s: F(s)[0], mp.mpf(1))
        _, z = F(sc)
        l0, lN, lam = total_len(z)
        assert abs(l0 + lN + sum(lam) - 4) < mp.mpf(10) ** -30
        f = l0 + 3 * lN + sum(lam[k] * (z[k] + z[k + 1]) / 2 for k in range(N - 1))
        L = 4 - l0 - lN
        mu = W.mult(float(z[0]), float(z[-1]))
        for j in range(4):
            V, H = mp.mpf(mu[0]), mp.mpf(mu[1])
            if j:
                V += mp.mpf(rnd.gauss(0, 1)) * mp.mpf(10) ** rnd.uniform(-8, -1)
                H *= 1 + mp.mpf(rnd.gauss(0, 1)) * mp.mpf(10) ** rnd.uniform(-8, -1)
            B = l0 + 3 * lN + (V + L) * z[-1] - V * z[0] - Gf(V + L, H) + Gf(V, H) + (N - 1) * 2 * Gf(eta, H)
            worst = min(worst, f - B)
            if j == 0:
                worst_opt = min(worst_opt, f - B)
    return mp.nstr(worst, 6), mp.nstr(worst_opt, 6)


def primal_check(N, m, eta, path):
    X = [float(s) for s in open(path).read().split()]
    assert len(X) == 2 * N + 2
    Xf = [Fr(v) for v in X]
    assert Xf[0] == 1 and Xf[N] == 3
    lin_viol = max(abs(osilx.ev_row(m["cons"][i], Xf, Fr, {})) for i in range(N))
    mp.mp.dps = 50
    Xm = [mp.mpf(v) for v in X]
    fns = {"sqrt": mp.sqrt}
    obj = osilx.ev_tree(m["obj"]["nl"], Xm, lambda s: mp.mpf(s), fns)
    ln = osilx.ev_tree(m["cons"][N]["nl"], Xm, lambda s: mp.mpf(s), fns)
    return dict(obj=mp.nstr(obj, 20), lin_row_viol=float(lin_viol), len_row_viol=mp.nstr(abs(ln - 4), 3))


if __name__ == "__main__":
    what = sys.argv[1]
    if what == "struct":
        for N in (50, 100, 200, 400):
            m, eta = load(N)
            check_param(N, m, eta, trials=2 if N <= 100 else 1)
            check_identity(N, trials=3)
            path = os.path.join(R29, "open-instances-wave2/cops/logs/chain%d_primal.txt") % N
            print(N, "eta", eta, "structure/param/identity ok; author primal:", primal_check(N, m, eta, path), flush=True)
    elif what == "lemma":
        if len(sys.argv) <= 3:
            print("symbolic:", lemma_symbolic(), flush=True)
            print("random:", lemma_random(int(sys.argv[2]) if len(sys.argv) > 2 else 200000), flush=True)
        print("adversarial min gap:", lemma_adversarial(), flush=True)
    elif what == "theorem":
        for N in (5, 20, 50):
            print(N, "min f - B over random feasible chains and multipliers:", theorem_random(N, trials=100), flush=True)
        for N in (50, 100):
            print(N, "near-optimal perturbations: min f - B (any mult, optimal mult):", theorem_near_opt(N), flush=True)
