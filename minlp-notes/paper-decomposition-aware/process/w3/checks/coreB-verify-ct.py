#!/usr/bin/env python3
"""Second coreB verification: the full CT schedule and Theorem thm:approx.

Exact arithmetic (fractions). Checks, on planted mixed-integer box QPs with
an exactly certified weighted growth constant gamma:
  * CT (Algorithm alg:ct) with per-coordinate meshes h_ij = 2^{E-j-e_i}:
    returned beta <= OPT <= F(xhat) <= beta + eps         (thm:approx(a));
  * the returned record is a valid path certificate (Def. def:cert,
    (C1) and (C2) recomputed from the grids alone);
  * the successful trial mu satisfies 2^mu <= 6 sqrt(kappa-bar) and
    mu <= mu* = max{2, ceil(log4(8 kappa-bar))}           (thm:approx(b));
  * trial mu* run alone is never aborted and succeeds by stage J;
  * stress mode: caps 5 for mu <= 3, then 2^{mu+1}+2 (> 1+2/theta), and
    wide boxes, so that early trials abort; checks thm:approx(a) and (C1)/(C2) across trials;
  * the termination trial mu_T of the proof of thm:approx(a) (least mu>=2
    with 2^-mu <= min h_iJ/s_i) is not aborted, has at most
    max(1+2/theta, s_i+1) nodes per coordinate, and succeeds;
  * every node of every trial has a denominator dividing Gamma_X 2^alpha,
    alpha = J + max|e_i| + |E| + mu K_mu (Appendix A, bit lengths).
Scalar facts of thm:approx(b) and the node formula are checked separately.
Usage: python3 coreB-verify-ct.py SEED NINST
"""
import math
import random
import sys
from fractions import Fraction as Fr
from itertools import product


def ceil_log2(x):
    k = 0
    while (1 << k) < x:
        k += 1
    return k


def graded(lo, hi, c, h, th, integer):
    """Graded grid of [lo,hi] (Def. def:graded) with center c."""
    assert lo <= c <= hi
    nodes = {c}
    for sgn, end in ((1, hi), (-1, lo)):
        t = Fr(0)
        R = abs(end - c)
        while t < R:
            if integer:
                step = max(Fr(1), Fr(math.floor(h + th * t)))
            else:
                step = h + th * t
            t = min(t + step, R)
            nodes.add(c + sgn * t)
    return sorted(nodes)


def eff(a, b, integer):
    return Fr(0) if (integer and b - a == 1) else b - a


def wvec(g, integer):
    w = {}
    for k, v in enumerate(g):
        best = Fr(0)
        if k > 0:
            best = max(best, eff(g[k - 1], v, integer))
        if k + 1 < len(g):
            best = max(best, eff(v, g[k + 1], integer))
        w[v] = best
    return w


def ldl_psd(A):
    n = len(A)
    A = [row[:] for row in A]
    for k in range(n):
        if A[k][k] < 0:
            return False
        if A[k][k] == 0:
            if any(A[k][j] != 0 for j in range(k + 1, n)):
                return False
            continue
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            for j in range(k + 1, n):
                A[i][j] -= f * A[k][j]
    return True


class Inst:
    pass


def make_instance(rng, n, wide=False):
    wmax = 40 if wide else 6
    for _ in range(500):
        I = Inst()
        I.n = n
        I.integer = [rng.random() < 0.4 for _ in range(n)]
        I.lo, I.hi, I.xs, I.b = [], [], [], []
        for i in range(n):
            if I.integer[i]:
                lo = Fr(rng.randint(-3, 0))
                hi = lo + rng.randint(1, wmax)
            else:
                lo = Fr(rng.randint(-6, 0), rng.randint(1, 3))
                hi = lo + Fr(rng.randint(1, wmax + 2), rng.randint(1, 3))
            I.lo.append(lo)
            I.hi.append(hi)
            r = rng.random()
            if r < 0.3:
                xs, b = lo, Fr(rng.randint(1, 6), 2)
            elif r < 0.6:
                xs, b = hi, -Fr(rng.randint(1, 6), 2)
            else:
                if I.integer[i]:
                    xs = Fr(rng.randint(int(lo), int(hi)))
                else:
                    xs = lo + (hi - lo) * Fr(rng.randint(1, 5), 6)
                b = Fr(0)
            I.xs.append(xs)
            I.b.append(b)
        A = [[Fr(0)] * n for _ in range(n)]
        for i in range(n):
            A[i][i] = Fr(rng.randint(-2, 8), 2)
            for j in range(i + 1, n):
                A[i][j] = A[j][i] = Fr(rng.randint(-4, 4), 2)
        I.A = A
        I.L = [max(Fr(0), 2 * A[i][i]) for i in range(n)]
        I.P = [i for i in range(n) if I.L[i] > 0]
        if not I.P:
            continue
        s = [I.hi[i] - I.lo[i] for i in range(n)]
        M = [[A[i][j] + (abs(I.b[i]) / s[i] if i == j else 0)
              for j in range(n)] for i in range(n)]
        # largest dyadic gamma = k/256 with M - gamma diag(L) PSD
        best = None
        for k in range(1, 4 * 256 + 1):
            g = Fr(k, 256)
            Mg = [[M[i][j] - (g * I.L[i] if i == j else 0) for j in range(n)]
                  for i in range(n)]
            if ldl_psd(Mg):
                best = g
            else:
                break
        if best is None:
            continue
        I.gamma = best
        I.kbar = max(Fr(1), 1 / best)
        return I
    raise RuntimeError("no instance")


def F(I, x):
    d = [x[i] - I.xs[i] for i in range(I.n)]
    v = sum(I.b[i] * d[i] for i in range(I.n))
    for i in range(I.n):
        for j in range(I.n):
            v += I.A[i][j] * d[i] * d[j]
    return v


def solve_grid(I, grids):
    """beta, a minimizer, min-marginals of Q on the product grid."""
    ws = [wvec(grids[i], I.integer[i]) for i in range(I.n)]
    beta, ybest = None, None
    mm = [dict() for _ in range(I.n)]
    for y in product(*grids):
        q = F(I, y) - sum(I.L[i] * ws[i][y[i]] ** 2 / 8 for i in range(I.n))
        if beta is None or q < beta:
            beta, ybest = q, y
        for i in range(I.n):
            if y[i] not in mm[i] or q < mm[i][y[i]]:
                mm[i][y[i]] = q
    return beta, ybest, mm


def mesh(I):
    e, r = {}, {}
    for i in I.P:
        k = 0
        while Fr(4) ** k < I.L[i]:
            k += 1
        while Fr(4) ** (k - 1) >= I.L[i]:
            k -= 1
        assert Fr(4) ** (k - 1) < I.L[i] <= Fr(4) ** k
        e[i], r[i] = k, Fr(2) ** (-k)
        assert Fr(1, 4) < I.L[i] * r[i] ** 2 <= 1
    E = -200
    while not all(Fr(2) ** E * r[i] >= I.hi[i] - I.lo[i] for i in I.P):
        E += 1
    return e, r, E


def trial(I, theta, K, eps, J, U, xhat, e, r, E):
    """TRIAL (Algorithm alg:trial). Returns status, U, xhat, record."""
    n = I.n
    box = [(I.lo[i], I.hi[i]) for i in range(n)]
    c = list(I.lo)
    grids_hist = []
    for j in range(J + 1):
        grids = []
        for i in range(n):
            if i in I.P:
                h = Fr(2) ** (E - j) * r[i]
                g = graded(box[i][0], box[i][1], c[i], h, theta, I.integer[i])
            else:
                g = [I.lo[i], I.hi[i]]
            grids.append(g)
        if max(len(g) for g in grids) > K:
            return "abort", U, xhat, grids_hist
        grids_hist.append(grids)
        beta, y, mm = solve_grid(I, grids)
        if F(I, y) < U:
            U, xhat = F(I, y), y
        if U - beta <= eps:
            return "success", U, xhat, (grids_hist, beta)
        newbox = []
        for i in range(n):
            if i not in I.P:
                newbox.append(box[i])
                continue
            g = grids[i]
            kept = [(g[k], g[k + 1]) for k in range(len(g) - 1)
                    if min(mm[i][g[k]], mm[i][g[k + 1]]) <= U]
            assert kept, "Prop filter: minimizer interval retained"
            newbox.append((min(a for a, _ in kept), max(b for _, b in kept)))
        box = newbox
        c = list(y)
    return "fail", U, xhat, grids_hist


def check_certificate(I, grids_hist, beta, xhat):
    """Def. def:cert, (C1) and (C2), recomputed from the grids."""
    n = I.n
    assert all(I.lo[i] <= xhat[i] <= I.hi[i] for i in range(n))
    assert all(xhat[i].denominator == 1 for i in range(n) if I.integer[i])
    G0 = grids_hist[0]
    assert all(min(G0[i]) == I.lo[i] and max(G0[i]) == I.hi[i] for i in range(n))
    k = len(grids_hist) - 1
    for j in range(k + 1):
        Gj = grids_hist[j]
        for i in range(n):
            if I.integer[i]:
                assert all(v.denominator == 1 for v in Gj[i])
        _, _, mm = solve_grid(I, Gj)
        if j == k:
            assert min(min(m.values()) for m in mm) >= beta, "(C2)"
            continue
        Gn = grids_hist[j + 1]
        for i in range(n):
            lo1, hi1 = min(Gn[i]), max(Gn[i])
            assert min(Gj[i]) <= lo1 and hi1 <= max(Gj[i]), "nested"
            g = Gj[i]
            for t in range(len(g) - 1):
                a, a2 = g[t], g[t + 1]
                if lo1 <= a and a2 <= hi1:
                    continue
                ok = min(mm[i][a], mm[i][a2]) >= beta
                if not ok and eff(a, a2, I.integer[i]) == 0:
                    ok = all(mm[i][v] >= beta for v in (a, a2)
                             if not lo1 <= v <= hi1)
                assert ok, "(C1)"


def run_instance(I, q, stats, small_cap=False):
    n = I.n
    eps = Fr(1, 2 ** q)
    e, r, E = mesh(I)
    nP = len(I.P)
    eta0 = Fr(2) ** E
    J = 0
    while Fr(9, 16) * nP * eta0 ** 2 / 4 ** J > eps:
        J += 1
    Kmu = lambda mu: 10 * 2 ** mu * ceil_log2(nP + 2)
    # stress caps: 5 for mu <= 3 (forces aborts), then 2^{mu+1}+2 > 1+2/theta,
    # which keeps the termination argument of thm:approx(a) valid
    Kct = (lambda mu: 5 if mu <= 3 else 2 ** (mu + 1) + 2) if small_cap else Kmu
    OPT = F(I, I.xs)
    assert OPT == 0
    # Gamma_X and denominators
    GX = 1
    for i in range(n):
        GX *= I.lo[i].denominator * I.hi[i].denominator
    # CT
    U, xhat = F(I, I.lo), tuple(I.lo)
    mu = 2
    while True:
        theta = Fr(1, 2 ** mu)
        status, U, xhat, rec = trial(I, theta, Kct(mu), eps, J, U, xhat, e, r, E)
        if status != "success":
            stats["unsuccessful_trials"] += 1
        hist = rec[0] if status == "success" else rec
        alpha = J + max(abs(e[i]) for i in I.P) + abs(E) + mu * Kmu(mu)
        for grids in hist:
            for g in grids:
                for v in g:
                    assert (GX * 2 ** alpha) % v.denominator == 0, "denominator"
        if status == "success":
            break
        mu += 1
        assert mu <= 14, "CT runaway"
    grids_hist, beta = rec
    # thm:approx(a)
    assert beta <= OPT <= F(I, xhat) <= beta + eps
    assert F(I, xhat) == U
    check_certificate(I, grids_hist, beta, xhat)
    if small_cap:
        # stress mode: only part (a) and certificate validity are claimed
        stats["inst_small"] += 1
        return
    # thm:approx(b)
    kb = I.kbar
    mustar = 2
    while Fr(4) ** mustar < 8 * kb:
        mustar += 1
    assert 8 * kb * Fr(1, 4 ** mustar) <= 1
    assert mu <= mustar, (mu, mustar, kb)
    assert Fr(4) ** mu <= 36 * kb
    stats["mu_hist"][mu] = stats["mu_hist"].get(mu, 0) + 1
    # trial mu* alone: never aborted, succeeds by stage J
    st, _, _, _ = trial(I, Fr(1, 2 ** mustar), Kmu(mustar), eps, J, F(I, I.lo),
                        tuple(I.lo), e, r, E)
    assert st == "success", ("mu* trial", st)
    # termination trial mu_T of thm:approx(a)
    hJ = {i: Fr(2) ** (E - J) * r[i] for i in I.P}
    muT = 2
    while Fr(1, 2 ** muT) > min(hJ[i] / (I.hi[i] - I.lo[i]) for i in I.P):
        muT += 1
    assert mu <= muT
    if muT <= 7 and n == 2:
        thT = Fr(1, 2 ** muT)
        st, _, _, recT = trial(I, thT, Kmu(muT), eps, J, F(I, I.lo),
                               tuple(I.lo), e, r, E)
        assert st == "success", ("mu_T trial", st)
        for grids in recT[0]:
            for i in I.P:
                bound = max(1 + 2 / thT, I.hi[i] - I.lo[i] + 1)
                assert len(grids[i]) <= bound < Kmu(muT)
        stats["muT_runs"] += 1
    stats["inst"] += 1
    stats["maxkbar"] = max(stats["maxkbar"], kb)


def scalar_checks():
    # 2^{mu*} <= 6 sqrt(kbar), mu* <= 3(1+log2 kbar), on a fine grid
    # including the jump points kbar = 4^m/8 (+tiny).
    pts = [1 + k / 1000 for k in range(0, 200000)]
    pts += [4 ** m / 8 * (1 + d) for m in range(2, 30) for d in (0, 1e-12, 1e-6)]
    for kb in pts:
        if kb < 1:
            continue
        mus = max(2, math.ceil(math.log(8 * kb, 4) - 1e-15))
        assert 4 ** mus >= 8 * kb * (1 - 1e-12)
        assert 2 ** mus <= 6 * math.sqrt(kb) + 1e-9, kb
        assert mus <= 3 * (1 + math.log2(kb)) + 1e-12
    # eq:logabsorb: ceil(log2(nP+2))^p <= 2 p^p (n+2), nP <= n
    for p in range(1, 41):
        for n in list(range(1, 3000)) + [10 ** k for k in range(4, 19)]:
            lhs = math.ceil(math.log2(n + 2)) ** p
            assert lhs <= 2 * p ** p * (n + 2), (p, n)
    # sum_{mu=2}^{mu*} K_mu^p <= 2 K_{mu*}^p  (K_mu = C 2^mu)
    for p in range(1, 12):
        for mus in range(2, 30):
            assert sum(Fr(2) ** (mu * p) for mu in range(2, mus + 1)) <= \
                2 * Fr(2) ** (mus * p)
    # node formula of Appendix A: h((1+th)^k-1)/th with th=2^-mu
    for mu in range(2, 8):
        th = Fr(1, 2 ** mu)
        for k in range(0, 60):
            lhs = ((1 + th) ** k - 1) / th
            rhs = Fr((2 ** mu + 1) ** k - 2 ** (mu * k), 2 ** (mu * (k - 1))) \
                if k >= 1 else Fr(0)
            assert lhs == rhs
            # k unclipped continuous steps of h+theta t reach exactly this
            t = Fr(0)
            for _ in range(k):
                t = t + 1 + th * t
            assert t == lhs
    # (G5)/(Lemma states) constants at m=1: ceilings, not plain logs
    phi = lambda m: 0.75 + 8 * math.log(1.25 + 4 * math.sqrt(2 * m))
    psi = lambda m: 0.75 + 8 * math.log(1.25 + 3 * math.sqrt(m))
    assert phi(1) > 10 * math.log2(3) and phi(1) <= 10 * 2
    assert psi(1) <= 8 * math.log2(3)
    for m in range(1, 200000):
        assert phi(m) <= 10 * math.ceil(math.log2(m + 2))
        assert psi(m) <= 8 * math.ceil(math.log2(m + 2))
    print("scalar checks: ok")


def graded_integer_exhaustive():
    """Lemma graded (a),(b),(c) exhaustively for integer coordinates."""
    cnt = 0
    for th in (Fr(1, 4), Fr(1, 8), Fr(1, 16)):
        for h in (Fr(1, 3), Fr(1, 2), Fr(1), Fr(3, 2), Fr(2), Fr(5), Fr(8)):
            hh = max(h, Fr(1))
            for R in range(0, 160):
                g = graded(Fr(0), Fr(R), Fr(0), h, th, True)
                side = len(g) - 1
                if R > 0:
                    bound = math.ceil(4 / th * math.log(1 + th * R / hh))
                    assert side <= bound, (th, h, R, side, bound)
                w = wvec(g, True)
                for v in g:
                    assert w[v] <= h + th * abs(v), (th, h, R, v)
                if h >= R:
                    assert len(g) <= 2
                cnt += 1
    print("graded integer exhaustive: %d grids ok" % cnt)


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    ninst = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    rng = random.Random(seed)
    scalar_checks()
    graded_integer_exhaustive()
    stats = {"inst": 0, "mu_hist": {}, "muT_runs": 0, "maxkbar": Fr(0),
             "unsuccessful_trials": 0, "inst_small": 0}
    for t in range(ninst):
        n = 2 if t % 3 else 3
        I = make_instance(rng, n)
        q = rng.choice([4, 7, 10]) if n == 2 else 4
        run_instance(I, q, stats)
    nb = stats["unsuccessful_trials"]
    for t in range(ninst):
        I = make_instance(rng, 2, wide=True)
        run_instance(I, rng.choice([4, 7, 10]), stats, small_cap=True)
    print("reduced-cap stress (caps 5, then 2^(mu+1)+2; wide boxes): %d instances ok, %d aborted or "
          "failed trials before success" % (stats["inst_small"],
                                            stats["unsuccessful_trials"] - nb))
    print("CT runs: %d instances ok; successful trial histogram %s; "
          "termination-trial runs %d; max kappa-bar %s"
          % (stats["inst"], dict(sorted(stats["mu_hist"].items())),
             stats["muT_runs"], float(stats["maxkbar"])))


if __name__ == "__main__":
    main()
