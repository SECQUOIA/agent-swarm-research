"""Augmented-Lagrangian lower bounds in spatial branch-and-bound: prototype and node counts.

Supports results/augmented-lagrangian-exact-local-bounds.md.

Two node lower-bounding schemes for  min f(z) s.t. g_j(z) <= 0, h_k(z) = 0, z in box:

  standard : alphaBB relaxations of f, g_j, h_k (Gershgorin alpha from interval Hessians),
             relaxed convex program solved numerically (SLSQP, multistart).  Second-order
             pointwise convergent, but never exact at a constrained minimizer whose
             Lagrangian Hessian is indefinite.
  AL       : alphaBB applied to the augmented Lagrangian
                 AL(z) = f + lam^T h + (rho/2)|h|^2 + (1/(2 rho)) sum_j [max(0, mu_j + rho g_j)^2 - mu_j^2]
             with multipliers (mu, lam) supplied from the incumbent.  AL <= f on the feasible set,
             so min_Z AL is a valid lower bound for every mu >= 0, rho > 0.  Convexity of AL on Z is
             certified with a structured interval-Hessian bound (Lemma 3 of the note), the convex
             program is solved by L-BFGS-B and the value is certified by the gradient inequality
             (one gradient evaluation).  Near a nondegenerate KKT point the certificate succeeds,
             alpha = 0, and the bound is exact.

Interval arithmetic is a minimal implementation for polynomial data.  Floating point throughout:
this is an illustration of node counts, not a rigorous certificate.

Run:  conda run -n minlp-notes python code/augmented_lagrangian_bb/albb.py [quick]
"""
import heapq
import math
import sys
import time

import numpy as np
import sympy as sp
from scipy.optimize import minimize


# ----------------------------------------------------------------------------- intervals
class I:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        if hi is None:
            hi = lo
        self.lo = float(lo)
        self.hi = float(hi)

    @staticmethod
    def of(v):
        return v if isinstance(v, I) else I(v)

    def __add__(self, o):
        o = I.of(o)
        return I(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, o):
        return self + (-I.of(o))

    def __rsub__(self, o):
        return I.of(o) + (-self)

    def __mul__(self, o):
        o = I.of(o)
        p = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return I(min(p), max(p))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = I.of(o)
        if o.lo <= 0.0 <= o.hi:
            raise ZeroDivisionError("interval contains zero")
        return self * I(1.0 / o.hi, 1.0 / o.lo)

    def __rtruediv__(self, o):
        return I.of(o) / self

    def __pow__(self, n):
        n = int(n)
        if n == 0:
            return I(1.0)
        if n == 1:
            return I(self.lo, self.hi)
        if n % 2 == 1:
            return I(self.lo ** n, self.hi ** n)
        a, b = abs(self.lo), abs(self.hi)
        if self.lo <= 0.0 <= self.hi:
            return I(0.0, max(a, b) ** n)
        return I(min(a, b) ** n, max(a, b) ** n)

    @property
    def mid(self):
        return 0.5 * (self.lo + self.hi)

    @property
    def rad(self):
        return 0.5 * (self.hi - self.lo)

    def __repr__(self):
        return f"[{self.lo:.6g}, {self.hi:.6g}]"


def imat(m):
    """Interval matrix (list of lists of I/float) -> (midpoint array, radius array)."""
    m = [[I.of(e) for e in row] for row in m]
    mid = np.array([[e.mid for e in row] for row in m])
    rad = np.array([[e.rad for e in row] for row in m])
    return mid, rad


def gershgorin_min(mid, rad):
    """Lower bound on the smallest eigenvalue of every symmetric matrix in the interval matrix."""
    n = mid.shape[0]
    best = math.inf
    for i in range(n):
        s = sum(abs(mid[i, j]) + rad[i, j] for j in range(n) if j != i)
        best = min(best, mid[i, i] - rad[i, i] - s)
    return best


def gershgorin_max(mid, rad):
    return -gershgorin_min(-mid, rad)


# ----------------------------------------------------------------------------- problems
class Fun:
    """A scalar function with gradient and Hessian, callable on floats or intervals."""

    def __init__(self, expr, xs):
        self.n = len(xs)
        self.val = sp.lambdify(xs, expr, modules=[{}])
        self.grad = [sp.lambdify(xs, sp.diff(expr, v), modules=[{}]) for v in xs]
        self.hess = [[sp.lambdify(xs, sp.diff(expr, v, w), modules=[{}]) for w in xs] for v in xs]

    def v(self, x):
        return self.val(*x)

    def g(self, x):
        return [gi(*x) for gi in self.grad]

    def H(self, x):
        return [[hij(*x) for hij in row] for row in self.hess]


class Problem:
    def __init__(self, name, n, f, gs, hs, root, zstar, fstar, mu, lam):
        xs = sp.symbols(f"x0:{n}")
        self.name, self.n = name, n
        self.f = Fun(f(xs), xs)
        self.gs = [Fun(e, xs) for e in gs(xs)]
        self.hs = [Fun(e, xs) for e in hs(xs)]
        self.root = tuple(root)
        self.zstar = np.array(zstar, float)
        self.fstar = float(fstar)
        self.mu = np.array(mu, float)
        self.lam = np.array(lam, float)


def box_iv(box):
    return [I(l, u) for (l, u) in box]


# ----------------------------------------------------------------------------- standard alphaBB bound
def alpha_under(fun, box):
    mid, rad = imat(fun.H(box_iv(box)))
    return max(0.0, -0.5 * gershgorin_min(mid, rad))


def alpha_over(fun, box):
    mid, rad = imat(fun.H(box_iv(box)))
    return max(0.0, 0.5 * gershgorin_max(mid, rad))


def standard_bound(P, box, nstarts=6, rng=None):
    """alphaBB relaxation of objective and constraints on the box; numerical convex solve."""
    lo = np.array([l for l, _ in box])
    hi = np.array([u for _, u in box])
    af = alpha_under(P.f, box)
    ag = [alpha_under(g, box) for g in P.gs]
    ahc = [alpha_under(h, box) for h in P.hs]
    ahv = [alpha_over(h, box) for h in P.hs]

    def sep(x, a):
        return a * float(np.dot(x - lo, x - hi))

    def sep_grad(x, a):
        return a * (2.0 * x - lo - hi)

    def fcv(x):
        return P.f.v(x) + sep(x, af)

    def fcv_g(x):
        return np.array(P.f.g(x), float) + sep_grad(x, af)

    cons = []
    for g, a in zip(P.gs, ag):
        cons.append({"type": "ineq", "fun": (lambda x, g=g, a=a: -(g.v(x) + sep(x, a))),
                     "jac": (lambda x, g=g, a=a: -(np.array(g.g(x), float) + sep_grad(x, a)))})
    for h, ac, av in zip(P.hs, ahc, ahv):
        cons.append({"type": "ineq", "fun": (lambda x, h=h, a=ac: -(h.v(x) + sep(x, a))),
                     "jac": (lambda x, h=h, a=ac: -(np.array(h.g(x), float) + sep_grad(x, a)))})
        cons.append({"type": "ineq", "fun": (lambda x, h=h, a=av: (h.v(x) - sep(x, a))),
                     "jac": (lambda x, h=h, a=av: (np.array(h.g(x), float) - sep_grad(x, a)))})
    bounds = list(zip(lo, hi))
    rng = rng or np.random.default_rng(0)
    starts = [0.5 * (lo + hi)] + [lo + rng.random(P.n) * (hi - lo) for _ in range(nstarts - 1)]
    best = math.inf
    feas_found = False
    for x0 in starts:
        try:
            r = minimize(fcv, x0, jac=fcv_g, bounds=bounds, constraints=cons, method="SLSQP",
                         options={"ftol": 1e-12, "maxiter": 500})
        except Exception:
            continue
        viol = max([0.0] + [-c["fun"](r.x) for c in cons])
        if viol <= 1e-8:
            feas_found = True
            best = min(best, float(r.fun))
    if not feas_found:
        # feasibility phase
        def viol2(x):
            return sum(max(0.0, -c["fun"](x)) ** 2 for c in cons)
        vbest = math.inf
        for x0 in starts:
            r = minimize(viol2, x0, bounds=bounds, method="L-BFGS-B")
            vbest = min(vbest, r.fun)
            if r.fun <= 1e-16:
                r2 = minimize(fcv, r.x, jac=fcv_g, bounds=bounds, constraints=cons, method="SLSQP",
                              options={"ftol": 1e-12, "maxiter": 500})
                viol = max([0.0] + [-c["fun"](r2.x) for c in cons])
                if viol <= 1e-8:
                    best = min(best, float(r2.fun))
                    feas_found = True
        if not feas_found:
            return math.inf  # relaxed problem infeasible (numerically)
    return best


# ----------------------------------------------------------------------------- augmented Lagrangian bound
def al_value(P, x, mu, lam, rho):
    v = P.f.v(x)
    for g, m in zip(P.gs, mu):
        t = m + rho * g.v(x)
        v += (max(0.0, t) ** 2 - m * m) / (2.0 * rho)
    for h, l in zip(P.hs, lam):
        hv = h.v(x)
        v += l * hv + 0.5 * rho * hv * hv
    return v


def al_grad(P, x, mu, lam, rho):
    gr = np.array(P.f.g(x), float)
    for g, m in zip(P.gs, mu):
        t = m + rho * g.v(x)
        if t > 0.0:
            gr += t * np.array(g.g(x), float)
    for h, l in zip(P.hs, lam):
        gr += (l + rho * h.v(x)) * np.array(h.g(x), float)
    return gr


def al_lambda_min_bound(P, box, mu, lam, rho, thetas=(0.05, 0.1, 0.2, 0.35, 0.5, 0.7, 0.9)):
    """Certified lower bound on the smallest eigenvalue of the (generalized) Hessian of AL on the box.

    Hessian = H0(z) + rho B(z)^T B(z) on the region where the sign pattern of mu_j + rho g_j is fixed.
    Lemma: for interval enclosures [H0] (mid Hc, radius RH) and [B] (mid Bc, radius RB),
        lambda_min >= lambda_min(Hc + rho (1-theta) Bc^T Bc) - ||RH||_2 - rho ||RB||_2^2 (1-theta)/theta.
    Constraints whose sign is undetermined on the box contribute the interval coefficient
    [0, (mu_j + rho g_hi)_+] on their Hessian and are dropped from B (their rank-one term is PSD).
    """
    xb = box_iv(box)
    n = P.n
    H0 = [[I.of(e) for e in row] for row in P.f.H(xb)]
    rows = []
    for g, m in zip(P.gs, mu):
        gv = I.of(g.v(xb))
        lo_t, hi_t = m + rho * gv.lo, m + rho * gv.hi
        if hi_t <= 0.0:
            continue  # inactive on the whole box: no contribution
        coef = I(lo_t, hi_t) if lo_t > 0.0 else I(0.0, hi_t)
        Hg = g.H(xb)
        for i in range(n):
            for j in range(n):
                H0[i][j] = H0[i][j] + coef * I.of(Hg[i][j])
        if lo_t > 0.0:
            rows.append([I.of(e) for e in g.g(xb)])
    for h, l in zip(P.hs, lam):
        hv = I.of(h.v(xb))
        coef = I(l, l) + rho * hv
        Hh = h.H(xb)
        for i in range(n):
            for j in range(n):
                H0[i][j] = H0[i][j] + coef * I.of(Hh[i][j])
        rows.append([I.of(e) for e in h.g(xb)])
    Hc, RH = imat(H0)
    Hc = 0.5 * (Hc + Hc.T)
    normRH = np.linalg.norm(RH, 2)
    # (a) drop the PSD term rho B^T B entirely: lambda_min >= lambda_min([H0]) >= Gershgorin bound
    best = max(gershgorin_min(Hc, RH), float(np.linalg.eigvalsh(Hc).min()) - normRH)
    if not rows:
        return best
    # (b) structured bound keeping the rank-|A| term
    Bc, RB = imat(rows)
    normRB2 = np.linalg.norm(RB, 2) ** 2
    for th in thetas:
        M = Hc + rho * (1.0 - th) * (Bc.T @ Bc)
        val = float(np.linalg.eigvalsh(M).min()) - normRH - rho * normRB2 * (1.0 - th) / th
        best = max(best, val)
    return best


def al_bound(P, box, mu, lam, rho, x_hint=None):
    """Valid lower bound on min{f : feasible, z in box} from alphaBB applied to AL on the box."""
    lo = np.array([l for l, _ in box])
    hi = np.array([u for _, u in box])
    lam_min = al_lambda_min_bound(P, box, mu, lam, rho)
    alpha = max(0.0, -0.5 * lam_min)

    def phi(x):
        return al_value(P, x, mu, lam, rho) + alpha * float(np.dot(x - lo, x - hi))

    def phi_g(x):
        return al_grad(P, x, mu, lam, rho) + alpha * (2.0 * x - lo - hi)

    starts = [0.5 * (lo + hi)]
    if x_hint is not None:
        starts.insert(0, np.clip(x_hint, lo, hi))
    best = math.inf
    for x0 in starts:
        r = minimize(phi, x0, jac=phi_g, bounds=list(zip(lo, hi)), method="L-BFGS-B",
                     options={"ftol": 1e-15, "gtol": 1e-12, "maxiter": 1000})
        xh = r.x
        gr = phi_g(xh)
        # gradient certificate: phi convex on box => min_Z phi >= phi(xh) + min_z grad^T (z - xh)
        cert = phi(xh) + float(np.sum(np.minimum(gr * (lo - xh), gr * (hi - xh))))
        best = min(best, cert) if best == math.inf else max(best, cert)  # any valid certificate; keep the best (largest)
    return best, alpha, lam_min


# ----------------------------------------------------------------------------- branch and bound
def branch_and_bound(P, eps, use_std=True, use_al=True, mu=None, lam=None, rho=10.0, eta=0.0,
                     max_nodes=100000, root=None):
    """Bisection of the widest side, best-bound selection, incumbent fixed at f* + eta."""
    mu = P.mu if mu is None else np.asarray(mu, float)
    lam = P.lam if lam is None else np.asarray(lam, float)
    UB = P.fstar + eta
    root = P.root if root is None else tuple(root)
    stats = {"nodes": 0, "max_open": 0, "max_depth": 0, "fathom_std": 0, "fathom_al": 0,
             "fathom_both": 0, "al_exact_boxes": 0, "min_width": math.inf}

    def bound(box):
        Ls = standard_bound(P, box) if use_std else -math.inf
        La, alpha, lm = al_bound(P, box, mu, lam, rho, x_hint=P.zstar) if use_al else (-math.inf, None, None)
        return Ls, La, alpha

    heap = []
    Ls, La, alpha = bound(root)
    L = max(Ls, La)
    counter = 0
    heap.append((L, counter, 0, root, Ls, La, alpha))
    stats["max_open"] = int(L < UB - eps)
    while heap:
        L, _, depth, box, Ls, La, alpha = heapq.heappop(heap)
        stats["nodes"] += 1
        stats["max_depth"] = max(stats["max_depth"], depth)
        w = max(u - l for l, u in box)
        stats["min_width"] = min(stats["min_width"], w)
        if L >= UB - eps:
            fs, fa = Ls >= UB - eps, La >= UB - eps
            if fs and fa:
                stats["fathom_both"] += 1
            elif fa:
                stats["fathom_al"] += 1
            else:
                stats["fathom_std"] += 1
            if fa and alpha == 0.0:
                stats["al_exact_boxes"] += 1
            continue
        if stats["nodes"] > max_nodes:
            stats["nodes"] = None
            return stats
        widths = [u - l for (l, u) in box]
        i = int(np.argmax(widths))
        l, u = box[i]
        mid = 0.5 * (l + u)
        for child in ((l, mid), (mid, u)):
            nb = list(box)
            nb[i] = child
            nb = tuple(nb)
            Ls, La, alpha = bound(nb)
            Lc = max(Ls, La)
            counter += 1
            if Lc < UB - eps:
                heapq.heappush(heap, (Lc, counter, depth + 1, nb, Ls, La, alpha))
            else:
                # count fathomed children as processed nodes (they are created and bounded)
                stats["nodes"] += 1
                fs, fa = Ls >= UB - eps, La >= UB - eps
                if fs and fa:
                    stats["fathom_both"] += 1
                elif fa:
                    stats["fathom_al"] += 1
                else:
                    stats["fathom_std"] += 1
                if fa and alpha == 0.0:
                    stats["al_exact_boxes"] += 1
                stats["min_width"] = min(stats["min_width"], max(uu - ll for ll, uu in nb))
        stats["max_open"] = max(stats["max_open"], len(heap))
    return stats


# ----------------------------------------------------------------------------- examples
def examples():
    ex = []
    # A (repo example): min x1^2 + x2^2 s.t. x1 x2 >= 1, box [0.5,2]^2.  z*=(1,1), mu*=2.  L convex (PSD).
    ex.append(Problem("A", 2, lambda x: x[0] ** 2 + x[1] ** 2, lambda x: [1 - x[0] * x[1]], lambda x: [],
                      [(0.5, 2.0), (0.5, 2.0)], [1, 1], 2.0, [2.0], []))
    # B (repo degenerate): min x2 - x1 s.t. x2 >= x1 + (x1-1)^4, box [0,2]x[0,3]. z*=(1,1), mu*=1, L=(x1-1)^4 convex.
    ex.append(Problem("B", 2, lambda x: x[1] - x[0], lambda x: [x[0] + (x[0] - 1) ** 4 - x[1]], lambda x: [],
                      [(0.0, 2.0), (0.0, 3.0)], [1, 1], 0.0, [1.0], []))
    # C (indefinite Lagrangian): min x1^2 + x2^2 - (1/2)(x1+x2-2)^2 s.t. x1 x2 >= 1, box [0.5,2]^2.
    #   z*=(1,1), mu*=2, Hessian of L: eigen -2 along (1,1) (normal), +4 along (1,-1) (critical).
    ex.append(Problem("C", 2, lambda x: x[0] ** 2 + x[1] ** 2 - sp.Rational(1, 2) * (x[0] + x[1] - 2) ** 2,
                      lambda x: [1 - x[0] * x[1]], lambda x: [],
                      [(0.5, 2.0), (0.5, 2.0)], [1, 1], 2.0, [2.0], []))
    # D (3 variables, bilinear equality, active quadratic inequality, one inactive linear inequality):
    #   min -4x0 - x1 - 2x2 + x0 x2 - x1^2 + (x0-x1)^2  s.t.  x0^2+x1^2+x2^2 <= 3,  0.5 - x0 <= 0,  x0 x1 - x2 = 0,
    #   box [0.5,2]^3.  z* = (1,1,1), mu* = (1, 0), lam* = 1 (by construction; global minimality checked numerically).
    ex.append(Problem("D", 3, lambda x: -4 * x[0] - x[1] - 2 * x[2] + x[0] * x[2] - x[1] ** 2 + (x[0] - x[1]) ** 2,
                      lambda x: [x[0] ** 2 + x[1] ** 2 + x[2] ** 2 - 3, sp.Rational(1, 2) - x[0]],
                      lambda x: [x[0] * x[1] - x[2]],
                      [(0.5, 2.0), (0.5, 2.0), (0.5, 2.0)], [1, 1, 1], -4.0 - 1.0 - 2.0 + 1.0 - 1.0, [1.0, 0.0], [1.0]))
    # E (degenerate, nonconvex near the minimizer, unconstrained): min x^4 + (x^2 - y)^2 on [-1,1]^2, z*=0.
    ex.append(Problem("E", 2, lambda x: x[0] ** 4 + (x[0] ** 2 - x[1]) ** 2, lambda x: [], lambda x: [],
                      [(-1.0, 1.0), (-1.0, 1.0)], [0, 0], 0.0, [], []))
    return {p.name: p for p in ex}


def choose_rho(P, x=None, mu=None, lam=None, factor=2.0, offset=1.0):
    """rho = factor * rho_min + offset, where rho_min is the smallest penalty making the Hessian of the
    augmented Lagrangian at x positive semidefinite (Finsler threshold), found by bisection."""
    x = P.zstar if x is None else np.asarray(x, float)
    mu = P.mu if mu is None else mu
    lam = P.lam if lam is None else lam
    HL = np.array(P.f.H(x), float)
    rows = []
    for g, m in zip(P.gs, mu):
        HL += m * np.array(g.H(x), float)
        if m > 1e-12:
            rows.append(np.array(g.g(x), float))
    for h, l in zip(P.hs, lam):
        HL += l * np.array(h.H(x), float)
        rows.append(np.array(h.g(x), float))
    if not rows:
        return offset
    B = np.array(rows)
    BtB = B.T @ B
    if np.linalg.eigvalsh(HL).min() >= 0.0:
        return offset
    lo, hi = 0.0, 1.0
    while np.linalg.eigvalsh(HL + hi * BtB).min() < 0.0 and hi < 1e8:
        hi *= 2.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if np.linalg.eigvalsh(HL + mid * BtB).min() < 0.0:
            lo = mid
        else:
            hi = mid
    return factor * hi + offset


def convexity_radius(P, rho, mu=None, lam=None, wmax=2.0):
    """Largest centered box half-width (dyadic search) at which the AL convexity certificate passes."""
    mu = P.mu if mu is None else mu
    lam = P.lam if lam is None else lam
    lo_w, hi_w = 0.0, wmax
    for _ in range(40):
        w = 0.5 * (lo_w + hi_w)
        box = tuple((z - w, z + w) for z in P.zstar)
        if al_lambda_min_bound(P, box, mu, lam, rho) >= 0.0:
            lo_w = w
        else:
            hi_w = w
    return lo_w


def run_table(P, eps_list, rho, use_std, use_al, mu=None, lam=None, eta=0.0, label=""):
    print(f"Example {P.name} {label}: std={use_std} AL={use_al} rho={rho} eta={eta}")
    print("   eps        nodes  max_open  depth  fath_std  fath_al  fath_both  AL_exact  min_width")
    rows = []
    for eps in eps_list:
        t0 = time.time()
        s = branch_and_bound(P, eps, use_std=use_std, use_al=use_al, mu=mu, lam=lam, rho=rho, eta=eta)
        if s["nodes"] is None:
            print(f"  {eps:9.2e}  (node limit)")
            break
        print(f"  {eps:9.2e}  {s['nodes']:6d}  {s['max_open']:6d}  {s['max_depth']:5d}  "
              f"{s['fathom_std']:7d}  {s['fathom_al']:7d}  {s['fathom_both']:8d}  {s['al_exact_boxes']:7d}  "
              f"{s['min_width']:9.2e}   ({time.time()-t0:.1f}s)")
        rows.append((eps, s))
    print()
    return rows


if __name__ == "__main__":
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    EX = examples()
    eps_list = [4.0 ** (-k) for k in range(2, 7 if quick else 11)]
    for name in (sys.argv[2:] or ("C", "A", "B", "D", "E")):
        P = EX[name]
        rho = choose_rho(P)
        print(f"Example {P.name}: rho_auto = {rho:.4g}; convexity radius (half-width of centered box): "
              + ", ".join(f"rho={r:g}: {convexity_radius(P, r):.4g}" for r in (1.0, 2.0, rho, 4.0, 16.0, 64.0)))
        run_table(P, eps_list, rho=rho, use_std=True, use_al=False)
        run_table(P, eps_list, rho=rho, use_std=True, use_al=True)
        run_table(P, eps_list, rho=rho, use_std=False, use_al=True)
        run_table(P, eps_list, rho=rho, use_std=True, use_al=True, eta=1e-9, label="(incumbent error 1e-9)")
        run_table(P, eps_list, rho=rho, use_std=True, use_al=True, mu=P.mu + 1e-4, label="(multiplier error 1e-4)")
    print("done")
