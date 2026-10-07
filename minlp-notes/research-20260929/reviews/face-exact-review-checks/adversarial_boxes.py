"""Referee test of Lemma 2.1 / Theorem 1 (face-exact-exponential.md): try to find valid boxes C whose
intersection with R = x* + [-r, r]^n has volume fraction above the Lemma 2.1 supremum nu.

Independent implementation: termwise relaxation (x_i^2 exact, secant of -kappa x_i^4, McCormick of each
b_i x_i x_{i+1}, signs of b_i arbitrary) solved as a QP by Clarabel directly (not bb_path.py).
Validity: LB(C) >= f* - eps.  By monotonicity of this relaxation, C valid implies C ∩ R valid, so the
search is over boxes inside R (boxes partially outside R cannot do better).
Search: greedy maximal face extension by bisection + face-exchange moves, many random starts, plus
starts at orthant boxes with vertex x* (aligned to x*) and at cubes centred at x*.
Usage: python3 adversarial_boxes.py [quick]
"""
import math
import sys
import itertools
import numpy as np
import scipy.sparse as sp
import clarabel
from scipy import optimize
from multiprocessing import Pool

D = 2.0


class Inst:
    def __init__(self, n, bvec, kappa, c, eps, r, name):
        self.n, self.b, self.kappa, self.c, self.eps, self.r, self.name = n, np.array(bvec, float), kappa, np.array(c, float), eps, r, name
        self.xs, self.fs = self.solve()
        self.lo, self.hi = self.xs - r, self.xs + r
        assert np.all(self.lo >= -1 - 1e-12) and np.all(self.hi <= 1 + 1e-12), "R must lie in X0"

    def f(self, x):
        return float(np.sum(x * x - self.kappa * x ** 4 + self.c * x) + np.sum(self.b * x[:-1] * x[1:]))

    def solve(self):
        best = None
        rng = np.random.default_rng(0)
        for x0 in [np.zeros(self.n)] + [rng.uniform(-1, 1, self.n) for _ in range(40)]:
            res = optimize.minimize(self.f, x0, method="L-BFGS-B", bounds=[(-1, 1)] * self.n,
                                    options={"ftol": 1e-15, "gtol": 1e-13, "maxiter": 20000})
            if best is None or res.fun < best.fun:
                best = res
        # polish with Newton on the gradient (interior minimizer)
        x = best.x.copy()
        for _ in range(20):
            g = 2 * x - 4 * self.kappa * x ** 3 + self.c
            g[:-1] += self.b * x[1:]; g[1:] += self.b * x[:-1]
            H = np.diag(2 - 12 * self.kappa * x ** 2) + np.diag(self.b, 1) + np.diag(self.b, -1)
            x = x - np.linalg.solve(H, g)
        return x, self.f(x)

    def LB(self, l, u):
        n, m = self.n, self.n - 1
        k = self.kappa
        slope = -k * (l + u) * (l * l + u * u)          # secant of -k x^4 on [l,u]
        const = float(np.sum(-k * l ** 4 - slope * l))
        N = n + m
        P = sp.csc_matrix((np.full(n, 2.0), (np.arange(n), np.arange(n))), shape=(N, N))
        q = np.concatenate([self.c + slope, self.b])
        rows, cols, vals, rhs = [], [], [], []
        ri = 0
        for e in range(m):
            i, j, w = e, e + 1, n + e
            if self.b[e] > 0:     # w >= l_j x_i + l_i x_j - l_i l_j ; w >= u_j x_i + u_i x_j - u_i u_j
                cons = [((l[j], l[i], -1.0), l[i] * l[j]), ((u[j], u[i], -1.0), u[i] * u[j])]
            else:                 # w <= u_j x_i + l_i x_j - l_i u_j ; w <= l_j x_i + u_i x_j - u_i l_j
                cons = [((-u[j], -l[i], 1.0), -l[i] * u[j]), ((-l[j], -u[i], 1.0), -u[i] * l[j])]
            for (ai, aj, aw), rh in cons:
                rows += [ri, ri, ri]; cols += [i, j, w]; vals += [ai, aj, aw]; rhs.append(rh); ri += 1
        for i in range(n):
            rows.append(ri); cols.append(i); vals.append(1.0); rhs.append(u[i]); ri += 1
            rows.append(ri); cols.append(i); vals.append(-1.0); rhs.append(-l[i]); ri += 1
        A = sp.csc_matrix((vals, (rows, cols)), shape=(ri, N))
        st = clarabel.DefaultSettings(); st.verbose = False
        st.tol_gap_abs = st.tol_gap_rel = 1e-11; st.tol_feas = 1e-11
        sol = clarabel.DefaultSolver(P, q, A, np.array(rhs), [clarabel.NonnegativeConeT(ri)], st).solve()
        return sol.obj_val + const

    def valid(self, l, u):
        return self.LB(l, u) >= self.fs - self.eps


def logfrac(I, l, u):
    return float(np.sum(np.log((u - l) / (2 * I.r))))


def extend(I, l, u, order, tol):
    l, u = l.copy(), u.copy()
    for (i, side) in order:
        if side == 0:
            a, bnd = l[i], I.lo[i]            # try to move l[i] down to bnd
            l2 = l.copy(); l2[i] = bnd
            if I.valid(l2, u):
                l = l2; continue
            good, bad = a, bnd
            while abs(good - bad) > tol:
                mid = 0.5 * (good + bad); l2[i] = mid
                if I.valid(l2, u): good = mid
                else: bad = mid
            l[i] = good
        else:
            a, bnd = u[i], I.hi[i]
            u2 = u.copy(); u2[i] = bnd
            if I.valid(l, u2):
                u = u2; continue
            good, bad = a, bnd
            while abs(good - bad) > tol:
                mid = 0.5 * (good + bad); u2[i] = mid
                if I.valid(l, u2): good = mid
                else: bad = mid
            u[i] = good
    return l, u


def search(args):
    I, start, seed, nexch = args
    rng = np.random.default_rng(seed)
    n, tol = I.n, 2e-4 * I.r
    l, u = start
    faces = [(i, s) for i in range(n) for s in (0, 1)]
    for _ in range(3):
        l, u = extend(I, l, u, [faces[k] for k in rng.permutation(len(faces))], tol)
    best = logfrac(I, l, u)
    for t in range(nexch):
        delta = I.r * rng.choice([0.2, 0.1, 0.05, 0.02, 0.01])
        i, s = faces[rng.integers(len(faces))]
        l2, u2 = l.copy(), u.copy()
        if s == 0: l2[i] = min(l2[i] + delta, u2[i] - 1e-6)
        else: u2[i] = max(u2[i] - delta, l2[i] + 1e-6)
        order = [faces[k] for k in rng.permutation(len(faces)) if faces[k] != (i, s)]
        l2, u2 = extend(I, l2, u2, order, tol)
        v = logfrac(I, l2, u2)
        if v > best + 1e-9:
            l, u, best = l2, u2, v
    # center-inequality check of Lemma 2.1 at the found box (must hold)
    h = (u - l) / 2; z = (u + l) / 2
    s = 1 - h / I.r
    Lc = np.sum(np.abs(I.b) * (h[:-1] * h[1:]))
    Uc = (D / 2) * np.sum((I.r * s) ** 2) + np.sum(np.abs(I.b) * (I.r * s[:-1]) * (I.r * s[1:]))
    return best, l, u, Lc - Uc - I.eps, I.LB(l, u) - I.fs


def nu_exact(I):
    """sup prod(1-s_i) over s admissible in Lemma 2.1 with L = b sum d_i d_{i+1}, U = (D/2)|t|^2 + b sum t_i t_{i+1}."""
    n, bb, r, eps = I.n, float(np.min(np.abs(I.b))), I.r, I.eps
    assert np.allclose(np.abs(I.b), bb)
    def cons(s):
        return (D / 2) * np.sum(s * s) + np.sum(s[:-1] * s[1:]) * bb + eps / r ** 2 - bb * np.sum((1 - s[:-1]) * (1 - s[1:]))
    best = -math.inf
    rng = np.random.default_rng(1)
    for _ in range(60):
        s0 = rng.uniform(0, 1, n)
        res = optimize.minimize(lambda s: -np.sum(np.log1p(-np.minimum(s, 1 - 1e-12))), s0, method="SLSQP",
                                bounds=[(0, 1 - 1e-9)] * n, constraints=[{"type": "ineq", "fun": cons}],
                                options={"ftol": 1e-14, "maxiter": 1000})
        if res.success and cons(res.x) >= -1e-9:
            best = max(best, -res.fun)
    return best


def instances(quick):
    out = []
    ns = (2, 3, 4) if quick else (2, 3, 4, 5)
    for n in ns:
        out.append(Inst(n, [0.8] * (n - 1), 0.0, np.zeros(n), 1e-4, 1.0, "A kappa=0 c=0 b=+0.8 r=1 eps=1e-4"))
        out.append(Inst(n, [0.8 * (-1) ** e for e in range(n - 1)], 0.0, np.zeros(n), 1e-4, 1.0,
                        "B kappa=0 c=0 mixed signs r=1 eps=1e-4"))
        out.append(Inst(n, [0.8] * (n - 1), 0.0, np.zeros(n), 1e-4, 0.1, "C kappa=0 c=0 small R r=0.1 eps=1e-4"))
        c0 = np.random.default_rng(0).uniform(-0.3, 0.3, n)
        I = Inst(n, [0.8] * (n - 1), 0.1, c0, 1e-4, 0.5, "D kappa=0.1 seed0 (x*!=0) secant r=0.5 eps=1e-4")
        out.append(I)
        out.append(Inst(n, [0.8] * (n - 1), 0.0, np.zeros(n), 0.05, 1.0, "E kappa=0 c=0 r=1 eps=0.05"))
    return out


def starts(I, k, rng):
    n = I.n
    S = []
    S.append((I.xs - 1e-6, I.xs + 1e-6))                      # tiny cube at x*
    for sig in itertools.product((-1, 1), repeat=n):           # orthant boxes with vertex x* (aligned)
        sig = np.array(sig)
        l = np.where(sig > 0, I.xs, I.xs - 1e-3 * I.r); u = np.where(sig > 0, I.xs + 1e-3 * I.r, I.xs)
        S.append((l, u))
    while len(S) < k:
        z = I.xs + rng.uniform(-I.r, I.r, n) * rng.choice([0.1, 0.5, 1.0])
        z = np.clip(z, I.lo + 1e-5, I.hi - 1e-5)
        S.append((z - 1e-6, z + 1e-6))
    return S


def main():
    quick = sys.argv[1:] == ["quick"]
    rng = np.random.default_rng(5)
    insts = instances(quick)
    jobs, meta = [], []
    for I in insts:
        for s_i, st in enumerate(starts(I, 24 if quick else 40, rng)):
            if not I.valid(*st):
                continue
            jobs.append((I, st, int(rng.integers(1 << 30)), 30 if quick else 60))
            meta.append(I)
    with Pool(34) as pool:
        res = pool.map(search, jobs, chunksize=1)
    by = {}
    for I, rr in zip(meta, res):
        by.setdefault((I.name, I.n), (I, []))[1].append(rr)
    print("name | n | best valid-box log-fraction (fraction^(1/n)) | exact Lemma 2.1 nu (^(1/n)) | closed form theta^n e^(lam(1+eps'')) (^(1/n)) | "
          "max center-ineq slack (must be <= 0) | min LB-f* at found boxes (>= -eps)")
    rho = D / (2 * 0.8); S = math.sqrt(1 + rho); th = S / (1 + S); lam = (1 + S) / (2 * S * S)
    for (name, n), (I, rr) in by.items():
        bestv = max(x[0] for x in rr)
        arg = max(rr, key=lambda x: x[0])
        nu = nu_exact(I)
        epsp = I.eps / (0.8 * I.r ** 2)
        cf = n * math.log(th) + lam * (1 + epsp)
        slack = max(x[3] for x in rr)
        minlb = min(x[4] for x in rr)
        flag = "VIOLATION" if bestv > nu + 1e-6 or slack > 1e-9 else "ok"
        print(f"{name} | n={n} | {bestv:.4f} ({math.exp(bestv/n):.4f}) | {nu:.4f} ({math.exp(nu/n):.4f}) | {cf:.4f} ({math.exp(cf/n):.4f}) | "
              f"{slack:.3e} | {minlb:.2e} | 1/best={math.exp(-bestv):.2f} vs Thm1 {math.exp(-cf):.2f} | {flag}")
        l, u = arg[1], arg[2]
        print(f"     best box (relative to x*): l-x*={np.round(l - I.xs, 3)}, u-x*={np.round(u - I.xs, 3)}")


if __name__ == "__main__":
    main()
