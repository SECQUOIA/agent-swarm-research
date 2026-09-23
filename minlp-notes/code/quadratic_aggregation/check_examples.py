"""Numerical sanity checks for results/quadratic-aggregation-trivial-hull-certificate.md.

Run with:  conda run -n minlp-notes python code/quadratic_aggregation/check_examples.py

Checks
1. The Section 5 example (n = 3, m = 4):
   a. S is bounded in (x1, x2): sampled points of S satisfy x1^2 + x2^2 < sqrt(5).
   b. Every convex certificate is trivial: the SDP  max ||pi(lambda)||_inf-coordinate
      over {lambda >= 0, sum lambda = 1, A_lambda PSD}  has value 0 for every coordinate.
   c. The image of the hyperplane {x1 = s t} under f^h is not convex: the midpoint of two
      image points is not attained (nonlinear least squares from many starts stays far).
   d. The image of E = {t = 0} is convex (it is a 2-plane): random convex combinations of
      image points are attained exactly.
2. Random two-quadratic systems (HHC automatic): whenever the SDP says every convex
   certificate is trivial, a randomized midpoint search finds, for each of several random
   targets y, two points of S with midpoint y (consistent with conv(S) = R^n); whenever a
   nontrivial certificate exists, the certificate's convex set excludes some sampled point
   (consistent with conv(S) != R^n).
"""
import numpy as np
import cvxpy as cp
from scipy.optimize import least_squares

rng = np.random.default_rng(20260921)


def sym(M):
    return 0.5 * (M + M.T)


def convex_certificate_size(As, bs, n):
    """Return max over coordinates of |pi(lambda)| on {lambda>=0, sum=1, A_lambda PSD}.

    Value 0 (numerically) means every convex certificate is trivial; +inf-feasibility failure
    (status infeasible) means K is empty.  Also returns one maximizing lambda if nontrivial.
    """
    m = len(As)
    best = 0.0
    best_lam = None
    coords = []
    for i in range(n):
        for j in range(i, n):
            coords.append(("A", i, j))
    for i in range(n):
        coords.append(("b", i))
    for sign in (+1, -1):
        for c in coords:
            lam = cp.Variable(m, nonneg=True)
            A_lam = sum(lam[k] * As[k] for k in range(m))
            b_lam = sum(lam[k] * bs[k] for k in range(m))
            if c[0] == "A":
                obj = sign * A_lam[c[1], c[2]]
            else:
                obj = sign * b_lam[c[1]]
            prob = cp.Problem(cp.Maximize(obj), [cp.sum(lam) == 1, A_lam >> 0])
            try:
                prob.solve(solver=cp.SCS, eps=1e-9, max_iters=20000)
            except Exception:
                prob.solve()
            if prob.status in ("infeasible", "infeasible_inaccurate"):
                return None, None  # K empty
            if prob.value is not None and prob.value > best:
                best = prob.value
                best_lam = lam.value.copy()
    return best, best_lam


def fh(As, bs, cs, x, t):
    return np.array([x @ A @ x + 2 * t * (b @ x) + c * t * t for A, b, c in zip(As, bs, cs)])


def example_section5():
    print("== Section 5 example ==")
    n = 3
    A1 = np.diag([1.0, -1.0, 0.0])
    A2 = -A1
    A3 = np.zeros((3, 3)); A3[0, 1] = A3[1, 0] = 0.5
    A4 = -A3
    As = [A1, A2, A3, A4]
    bs = [np.zeros(3)] * 4
    cs = [-1.0] * 4

    # a. boundedness of S in (x1, x2)
    pts = rng.uniform(-3, 3, size=(200000, 3))
    f = np.stack([p @ A @ p + c for A, c in zip(As, cs)], axis=1) if False else None
    vals = np.stack([np.einsum("ij,jk,ik->i", pts, A, pts) + c for A, c in zip(As, cs)], axis=1)
    inS = np.all(vals < 0, axis=1)
    r2 = pts[inS, 0] ** 2 + pts[inS, 1] ** 2
    print(f"  sampled points in S: {inS.sum()}, max x1^2+x2^2 = {r2.max():.4f} < sqrt(5) = {np.sqrt(5):.4f}: {r2.max() < np.sqrt(5)}")
    assert inS.sum() > 0 and r2.max() < np.sqrt(5)

    # b. every convex certificate trivial
    best, _ = convex_certificate_size(As, bs, n)
    print(f"  max |pi(lambda)| coordinate over normalized convex certificates: {best:.2e} (expected ~0)")
    assert best is not None and best < 1e-5

    # c. hyperplane {x1 = s t} image non-convex
    for s in (1.0, 5.0, 50.0):
        p1 = fh(As, bs, cs, np.array([1.0, 0.0, 0.0]), 1.0 / s)
        p2 = fh(As, bs, cs, np.array([0.0, 1.0, 0.0]), 0.0)
        mid = 0.5 * (p1 + p2)

        def resid(z):
            x = np.array([z[0], z[1], z[2]])
            return fh(As, bs, cs, x, x[0] / s) - mid

        dist = np.inf
        for _ in range(200):
            z0 = rng.normal(size=3) * rng.choice([0.1, 1.0, 10.0])
            sol = least_squares(resid, z0, xtol=1e-14, ftol=1e-14, gtol=1e-14)
            dist = min(dist, np.linalg.norm(sol.fun))
        # exact obstruction: mid forces u = v = 0 and w = 1/(2 s^2), but u = 0, w = x1^2 = 1/(2s^2)
        # gives x2^2 = 1/(2s^2) and v = x1 x2 = +-1/(2 s^2) != 0, so residual >= ~1/(2 s^2) in some coordinate
        print(f"  s={s}: min residual of midpoint over 200 starts = {dist:.3e} (should stay > 0; exact gap ~ {1/(2*s*s):.3e} in v)")
        assert dist > 0.1 / (2 * s * s)

    # d. image of E is convex (a plane): random convex combinations attained
    ok = True
    for _ in range(50):
        x, y = rng.normal(size=3), rng.normal(size=3)
        th = rng.uniform()
        target = th * fh(As, bs, cs, x, 0.0) + (1 - th) * fh(As, bs, cs, y, 0.0)

        def resid2(z):
            return fh(As, bs, cs, np.array([z[0], z[1], 0.0]), 0.0) - target

        best_r = np.inf
        for _ in range(20):
            sol = least_squares(resid2, rng.normal(size=2), xtol=1e-14, ftol=1e-14, gtol=1e-14)
            best_r = min(best_r, np.linalg.norm(sol.fun))
        ok &= best_r < 1e-7
    print(f"  image of E convex (random convex combinations attained): {ok}")
    assert ok


def _negative_set_1d(a, b, c, tol=1e-12):
    """Open set {M : a M^2 + 2 b M + c < 0} as a list of disjoint open intervals."""
    if abs(a) < tol:
        if abs(b) < tol:
            return [(-np.inf, np.inf)] if c < 0 else []
        r = -c / (2 * b)
        return [(-np.inf, r)] if b > 0 else [(r, np.inf)]
    disc = b * b - a * c
    if disc <= 0:
        return [(-np.inf, np.inf)] if a < 0 else []
    r1 = (-b - np.sqrt(disc)) / a
    r2 = (-b + np.sqrt(disc)) / a
    lo, hi = min(r1, r2), max(r1, r2)
    if a > 0:
        return [(lo, hi)]
    return [(-np.inf, lo), (hi, np.inf)]


def _intersect(intervals_a, intervals_b):
    out = []
    for (a1, a2) in intervals_a:
        for (b1, b2) in intervals_b:
            lo, hi = max(a1, b1), min(a2, b2)
            if lo < hi:
                out.append((lo, hi))
    return out


def midpoint_search(As, bs, cs, y, tries=3000):
    """Exact test along random lines: is there v and M+ > 0 > M- with y + M v in S for M in {M+, M-}?

    Then y is a convex combination of two points of S.  Each line is handled exactly by
    intersecting the 1-D solution sets of the quadratic inequalities."""
    n = len(y)
    for _ in range(tries):
        v = rng.normal(size=n)
        v /= np.linalg.norm(v)
        feas = [(-np.inf, np.inf)]
        for A, b, c in zip(As, bs, cs):
            a_ = v @ A @ v
            b_ = v @ A @ y + b @ v
            c_ = y @ A @ y + 2 * b @ y + c
            feas = _intersect(feas, _negative_set_1d(a_, b_, c_))
            if not feas:
                break
        if not feas:
            continue
        has_pos = any(hi > 1e-9 for (lo, hi) in feas)
        has_neg = any(lo < -1e-9 for (lo, hi) in feas)
        if has_pos and has_neg:
            # verify numerically at concrete points
            Mp = next((min(hi, lo + 1.0) if np.isfinite(hi) else lo + 1.0) if lo > 0 else min(hi, 1.0) / 2 if np.isfinite(hi) else 1.0 for (lo, hi) in feas if hi > 1e-9)
            Mm = next((max(lo, hi - 1.0) if np.isfinite(lo) else hi - 1.0) if hi < 0 else max(lo, -1.0) / 2 if np.isfinite(lo) else -1.0 for (lo, hi) in feas if lo < -1e-9)
            if np.all(fh(As, bs, cs, y + Mp * v, 1.0) < 0) and np.all(fh(As, bs, cs, y + Mm * v, 1.0) < 0):
                return True
    return False


def random_two_quadratics(trials=40):
    print("== Random two-quadratic systems (m = 2, n = 3) ==")
    n = 3
    stats = {"trivial_and_hull_full": 0, "trivial_but_midpoint_failed": 0,
             "nontrivial": 0, "K_empty": 0, "S_empty": 0}
    t = 0
    while t < trials:
        As = [sym(rng.normal(size=(n, n))) for _ in range(2)]
        bs = [rng.normal(size=n) for _ in range(2)]
        cs = [rng.normal() for _ in range(2)]
        # ensure S nonempty: shift constants so that a random point is strictly feasible
        x0 = rng.normal(size=n)
        cs = [c - fh([A], [b], [c], x0, 1.0)[0] - abs(rng.normal()) - 0.1 for A, b, c in zip(As, bs, cs)]
        assert np.all(fh(As, bs, cs, x0, 1.0) < 0)
        best, lam = convex_certificate_size(As, bs, n)
        t += 1
        if best is None:
            stats["K_empty"] += 1
            # Proposition 2.13: conv(S) = R^n. check midpoint property for a few targets
            for _ in range(3):
                y = rng.normal(size=n) * 5
                assert midpoint_search(As, bs, cs, y), "K empty but midpoint search failed"
            continue
        if best < 1e-6:
            # every convex certificate trivial: Theorem 1 predicts conv(S) = R^n
            good = all(midpoint_search(As, bs, cs, rng.normal(size=n) * 5) for _ in range(3))
            if good:
                stats["trivial_and_hull_full"] += 1
            else:
                stats["trivial_but_midpoint_failed"] += 1
        else:
            stats["nontrivial"] += 1
            # nontrivial certificate: f_lam convex; check that some sampled point violates f_lam < 0
            Al = sum(l * A for l, A in zip(lam, As)); bl = sum(l * b for l, b in zip(lam, bs)); cl = sum(l * c for l, c in zip(lam, cs))
            pts = rng.normal(size=(20000, n)) * 50
            vals = np.einsum("ij,jk,ik->i", pts, Al, pts) + 2 * pts @ bl + cl
            assert np.any(vals >= 0), "nontrivial certificate but f_lambda < 0 everywhere sampled"
    print("  ", stats)
    assert stats["trivial_but_midpoint_failed"] == 0


def paired_two_quadratics(trials=30):
    """f_2 = -f_1 + const with A_1 indefinite: lambda=(1,1) is a trivial certificate and no
    other nonnegative combination is PSD.  Theorem 1 (m = 2, HHC automatic) predicts conv(S) = R^n."""
    print("== Paired two-quadratic systems: A_2 = -A_1 indefinite, b_2 = -b_1 ==")
    n = 3
    done = 0
    while done < trials:
        A1 = sym(rng.normal(size=(n, n)))
        w = np.linalg.eigvalsh(A1)
        if w.min() > -1e-3 or w.max() < 1e-3:
            continue
        b1 = rng.normal(size=n)
        c1 = rng.normal()
        As = [A1, -A1]; bs = [b1, -b1]; cs = [c1, -c1 - abs(rng.normal()) - 0.5]
        x0 = rng.normal(size=n)
        # S nonempty: need f_1(x0) < 0 and -f_1(x0) + (c1 + c2) < 0, i.e. c1 + c2 < f_1(x0) < 0
        f10 = fh([A1], [b1], [c1], x0, 1.0)[0]
        shift = f10 - 0.5 * (cs[0] + cs[1])
        cs = [cs[0] - shift, cs[1] + shift]
        assert np.all(fh(As, bs, cs, x0, 1.0) < 0)
        best, lam = convex_certificate_size(As, bs, n)
        assert best is not None and best < 1e-6, ("expected only trivial certificates", best)
        for _ in range(3):
            y = rng.normal(size=n) * rng.choice([1.0, 10.0, 100.0])
            assert midpoint_search(As, bs, cs, y), "trivial certificates only, but midpoint search failed"
        done += 1
    print(f"  {done} instances: only trivial certificates, and every random target was a midpoint of two points of S")


def pdlc_margin(mats):
    """max t s.t. sum theta_i M_i >= t I, ||theta||_inf <= 1 (t > 0 iff PDLC)."""
    k = len(mats)
    th = cp.Variable(k)
    t = cp.Variable()
    M = sum(th[i] * mats[i] for i in range(k))
    prob = cp.Problem(cp.Maximize(t), [M >> t * np.eye(mats[0].shape[0]), cp.norm(th, "inf") <= 1])
    prob.solve(solver=cp.SCS, eps=1e-9, max_iters=20000)
    return t.value


def three_quadratics_partial_pdlc(trials=20):
    """Corollary 5(2): m = 3, n = 3, PDLC of the quadratic parts with a negative coefficient,
    only trivial convex certificates.  Construction: A_1 = D indefinite, A_2 = -D, b_2 = -b_1,
    A_3 = mu D - P with P positive definite (so -A_3 + mu D = P is PD, and every nonnegative
    combination with lambda_3 > 0 is indefinite).  Theorem 1 predicts conv(S) = R^3.
    Also records whether the homogenized Q_i satisfy PDLC.  Expected: always (the count of
    instances without it is 0), because f_1 + f_2 is a negative constant, so E_0 lies in the
    span of the Q_i and PDLC of the A_i lifts to the Q_i; see the scope remark after
    Corollary 5 in the result note."""
    print("== Three quadratics, PDLC of quadratic parts only (Corollary 5(2)) ==")
    n = 3
    done = 0
    outside_bds = 0
    while done < trials:
        D = sym(rng.normal(size=(n, n)))
        w = np.linalg.eigvalsh(D)
        if w.min() > -1e-2 or w.max() < 1e-2:
            continue
        G = rng.normal(size=(n, n)); P = G @ G.T + 0.5 * np.eye(n)
        mu = rng.normal()
        A3 = mu * D - P
        b1 = rng.normal(size=n); b3 = rng.normal(size=n)
        As = [D, -D, A3]; bs = [b1, -b1, b3]
        x0 = rng.normal(size=n)
        q0 = x0 @ D @ x0 + 2 * b1 @ x0
        cs = [-q0 - 1.0, q0 - 1.0, -(x0 @ A3 @ x0 + 2 * b3 @ x0) - 1.0]
        assert np.all(fh(As, bs, cs, x0, 1.0) < 0)
        # PDLC of quadratic parts (should hold with theta_3 < 0)
        assert pdlc_margin(As) > 1e-6
        best, lam = convex_certificate_size(As, bs, n)
        assert best is not None and best < 1e-6, ("expected only trivial certificates", best)
        Qs = [np.block([[A, b[:, None]], [b[None, :], np.array([[c]])]]) for A, b, c in zip(As, bs, cs)]
        if pdlc_margin(Qs) < 1e-7:
            outside_bds += 1
        for _ in range(3):
            y = rng.normal(size=n) * rng.choice([1.0, 10.0, 100.0])
            assert midpoint_search(As, bs, cs, y), "trivial certificates only, but midpoint search failed"
        done += 1
    print(f"  {done} instances: quadratic-part PDLC holds, only trivial certificates, every target a midpoint of two points of S;"
          f" {outside_bds} of them have NO positive definite combination of the homogenized Q_i")


if __name__ == "__main__":
    example_section5()
    random_two_quadratics()
    paired_two_quadratics()
    three_quadratics_partial_pdlc()
    print("all checks passed")
