"""Reviewer's independent stress test of Lemma 4.1 (key lemma) and Proposition 4.4.

Lemma 4.1: for a d-dim C^1 submanifold S of R^n and any box B,
    I(S, B) = int_{S cap B} q_B^{-d/2} dsigma <= C_{n,d} * sum_I M^I(S; B),
    C_{n,d} = (pi^2/d)^{d/2} binom(n,d)^{1/2}.
The sharpest case is a single graph piece of S^I (multiplicity 1): then the bound is C_{n,d}.

Method (independent of the author's code):
  * d = 1 curves in R^n: split S cap B into runs on which the dominant tangent coordinate i
    (argmax |t_i|, first on ties) is constant; on a run y_i is strictly monotone.  Integrate in
    theta with y_i = l_i + w_i sin^2(theta); the integrand 2 sqrt(a_i) q^{-1/2} |c'|/|c'_i| is
    bounded by 2 sqrt(n), so Gauss-Legendre is accurate.  Run end points are refined by bisection.
    Local multiplicity M^{i}(S; B) = max overlap of the y_i-ranges of runs with dominant index i.
  * d = 2 surfaces in R^3: for each coordinate plane (i,j) with normal-dominant k, and each sheet,
    integrate 4 sqrt(a_i a_j)/(q |n_k|) (bounded by 2/|n_k|) on a midpoint grid in (theta_i, theta_j).
Random boxes (log-uniform size and aspect) near S, then Nelder-Mead on the worst ratios.
Usage: python3 key_lemma_stress.py [seed]
"""
import math
import sys
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
GLX, GLW = np.polynomial.legendre.leggauss(40)


def Cnd(n, d):
    return (math.pi ** 2 / d) ** (d / 2) * math.comb(n, d) ** 0.5


# ---------------------------------------------------------------- d = 1 curves
class Curve:
    def __init__(self, name, n, fun, dfun, s0, s1, closed):
        self.name, self.n, self.fun, self.dfun = name, n, fun, dfun
        self.s0, self.s1, self.closed = s0, s1, closed


def circle(R=1.0):
    return Curve("circle", 2, lambda s: np.stack([R * np.cos(s), R * np.sin(s)], -1),
                 lambda s: np.stack([-R * np.sin(s), R * np.cos(s)], -1), 0, 2 * math.pi, True)


def ellipse(a=1.0, b=0.1):
    return Curve(f"ellipse({a},{b})", 2, lambda s: np.stack([a * np.cos(s), b * np.sin(s)], -1),
                 lambda s: np.stack([-a * np.sin(s), b * np.cos(s)], -1), 0, 2 * math.pi, True)


def helix(c=0.15, turns=2):
    return Curve(f"helix(c={c})", 3,
                 lambda s: np.stack([np.cos(s), np.sin(s), c * s], -1),
                 lambda s: np.stack([-np.sin(s), np.cos(s), c * np.ones_like(s)], -1),
                 0, 2 * math.pi * turns, False)


def line(theta, n=2):
    d = np.array([math.cos(theta), math.sin(theta)])
    return Curve(f"line({theta:.3f})", 2, lambda s: s[..., None] * d, lambda s: np.ones_like(s)[..., None] * d,
                 -3, 3, False)


def key_of(C, s, l, u):
    P, T = C.fun(s), C.dfun(s)
    inside = np.all((P >= l) & (P <= u), axis=-1)
    dom = np.argmax(np.abs(T), axis=-1)
    return np.where(inside, dom, -1)


def refine(C, sa, sb, keyval, l, u, it=60):
    """sa has key != keyval, sb has key == keyval; bisect for the transition."""
    for _ in range(it):
        m = 0.5 * (sa + sb)
        if key_of(C, np.array([m]), l, u)[0] == keyval:
            sb = m
        else:
            sa = m
    return sb


def curve_integral(C, l, u, N=6001):
    l, u = np.asarray(l, float), np.asarray(u, float)
    n = C.n
    s = np.linspace(C.s0, C.s1, N)
    k = key_of(C, s, l, u)
    if C.closed:  # rotate so the start is at a key change (avoid splitting a run artificially)
        ch = np.nonzero(k != np.roll(k, 1))[0]
        if len(ch) == 0:
            ch = [0]
        shift = ch[0]
        period = C.s1 - C.s0
        s = np.concatenate([s[shift:-1], s[:shift + 1] + period]) if shift > 0 else s
        k = key_of(C, s, l, u)
    runs = []
    i0 = None
    for idx in range(len(s) + 1):
        kv = k[idx] if idx < len(s) else -2
        if i0 is not None and kv != k[i0]:
            runs.append((i0, idx - 1))
            i0 = None
        if i0 is None and idx < len(s) and kv >= 0:
            i0 = idx
    total, pieces = 0.0, []
    w = u - l
    for (a, b) in runs:
        i = k[a]
        sa = refine(C, s[a - 1], s[a], i, l, u) if a > 0 else s[a]
        sb = refine(C, s[b + 1], s[b], i, l, u) if b < len(s) - 1 else s[b]
        ya, yb = C.fun(np.array([sa]))[0, i], C.fun(np.array([sb]))[0, i]
        th = lambda y: math.asin(math.sqrt(min(1.0, max(0.0, (y - l[i]) / w[i]))))
        ta, tb = th(ya), th(yb)
        val = 0.0
        edges = np.linspace(ta, tb, 5)
        for e0, e1 in zip(edges[:-1], edges[1:]):
            tn = 0.5 * (e1 - e0) * GLX + 0.5 * (e0 + e1)
            wn = 0.5 * abs(e1 - e0) * GLW
            ytar = l[i] + w[i] * np.sin(tn) ** 2
            lo, hi = np.full_like(tn, sa), np.full_like(tn, sb)
            incr = yb > ya
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                ym = C.fun(mid)[:, i]
                go = (ym < ytar) if incr else (ym > ytar)
                lo = np.where(go, mid, lo)
                hi = np.where(go, hi, mid)
            sm = 0.5 * (lo + hi)
            P, T = C.fun(sm), C.dfun(sm)
            aa = np.clip((P - l) * (u - P), 0, None)
            q = aa.sum(-1)
            g = 2 * np.sqrt(aa[:, i]) / np.sqrt(np.maximum(q, 1e-300)) * np.linalg.norm(T, axis=-1) / np.abs(T[:, i])
            val += float(np.sum(wn * g))
        total += val
        pieces.append((i, min(ya, yb), max(ya, yb), val))
    msum = 0
    for i in range(n):
        iv = [(p[1], p[2]) for p in pieces if p[0] == i and p[2] - p[1] > 1e-12]
        pts = sorted([(x0, 1) for x0, _ in iv] + [(x1, -1) for _, x1 in iv], key=lambda t: (t[0], t[1]))
        cur = best = 0
        for _, dlt in pts:
            cur += dlt
            best = max(best, cur)
        msum += best
    return total, msum, pieces


# -------------------------------------------------------------- d = 2 surfaces
def surface_integral(kind, l, u, G=260, par=None):
    """kind 'ellipsoid' (par = semi-axes) or 'plane' (par = (normal, c)). Returns (total, per-patch list)."""
    l, u = np.asarray(l, float), np.asarray(u, float)
    w = u - l
    t = (np.arange(G) + 0.5) * (math.pi / 2) / G
    T1, T2 = np.meshgrid(t, t, indexing="ij")
    dA = (math.pi / 2 / G) ** 2
    out = []
    for (i, j, k) in [(1, 2, 0), (0, 2, 1), (0, 1, 2)]:
        yi = l[i] + w[i] * np.sin(T1) ** 2
        yj = l[j] + w[j] * np.sin(T2) ** 2
        ai, aj = w[i] ** 2 * (np.sin(T1) * np.cos(T1)) ** 2, w[j] ** 2 * (np.sin(T2) * np.cos(T2)) ** 2
        sheets = []
        if kind == "ellipsoid":
            c = np.asarray(par, float)
            r = 1 - (yi / c[i]) ** 2 - (yj / c[j]) ** 2
            ok = r >= 0
            for sg in (1, -1):
                yk = sg * c[k] * np.sqrt(np.where(ok, r, 0))
                sheets.append((ok, yk))
        else:
            nv, cc = par
            yk = (cc - nv[i] * yi - nv[j] * yj) / nv[k]
            sheets.append((np.ones_like(yi, bool), yk))
        for ok, yk in sheets:
            Y = np.zeros(yi.shape + (3,))
            Y[..., i], Y[..., j], Y[..., k] = yi, yj, yk
            if kind == "ellipsoid":
                N = Y / np.asarray(par, float) ** 2
            else:
                N = np.broadcast_to(np.asarray(par[0], float), Y.shape)
            N = N / np.linalg.norm(N, axis=-1, keepdims=True)
            dom = np.argmax(np.abs(N), axis=-1)
            ak = np.clip((yk - l[k]) * (u[k] - yk), 0, None)
            mask = ok & (dom == k) & (yk >= l[k]) & (yk <= u[k])
            q = ai + aj + ak
            g = np.where(mask, 4 * np.sqrt(ai * aj) / np.maximum(q, 1e-300) / np.maximum(np.abs(N[..., k]), 1e-300), 0)
            out.append(float(g.sum() * dA))
    return sum(out), out


def box_from(p, n):
    c = np.array(p[:n])
    lw = np.array(p[n:2 * n])
    w = np.exp(lw)
    return c - w / 2, c + w / 2


def stress_curve(C, ntrial=1500):
    n = C.n
    bound1 = Cnd(n, 1)
    worst_total, worst_piece, worst_box = 0.0, 0.0, None
    cand = []
    for _ in range(ntrial):
        s = rng.uniform(C.s0, C.s1)
        c0 = C.fun(np.array([s]))[0] + rng.normal(0, 0.2, n) * rng.choice([0, 1, 0.1])
        lw = rng.uniform(math.log(1e-3), math.log(4.0)) + rng.normal(0, 1.2, n)
        p = np.concatenate([c0, lw])
        l, u = box_from(p, n)
        tot, ms, pcs = curve_integral(C, l, u)
        if ms == 0:
            continue
        r1 = tot / (bound1 * ms)
        rp = max(pp[3] for pp in pcs) / bound1
        cand.append((max(r1, rp), p))
        worst_total, worst_piece = max(worst_total, r1), max(worst_piece, rp)
    cand.sort(key=lambda t: -t[0])

    def negratio(p):
        l, u = box_from(p, n)
        tot, ms, pcs = curve_integral(C, l, u, N=3001)
        if ms == 0:
            return 0.0
        return -max(tot / (bound1 * ms), max(pp[3] for pp in pcs) / bound1)
    for _, p in cand[:4]:
        r = minimize(negratio, p, method="Nelder-Mead", options={"maxiter": 250, "xatol": 1e-7, "fatol": 1e-9})
        l, u = box_from(r.x, n)
        tot, ms, pcs = curve_integral(C, l, u, N=20001)
        if ms:
            worst_total = max(worst_total, tot / (bound1 * ms))
            worst_piece = max(worst_piece, max(pp[3] for pp in pcs) / bound1)
    return worst_total, worst_piece


def main():
    # sanity: circle in [-1,1]^2 has q = 1 on S, so I = 2 pi exactly
    tot, ms, _ = curve_integral(circle(), [-1, -1], [1, 1], N=20001)
    print(f"sanity circle/[-1,1]^2: I = {tot:.6f} (2pi = {2 * math.pi:.6f}), local sum_I M^I = {ms}")
    # sanity: comb tooth at height h in [0,1]^2: closed form 2 arcsin((1+4h(1-h))^-1/2)
    for h in (0.5, 0.1, 1e-3):
        C = Curve("seg", 2, lambda s, h=h: np.stack([s, h * np.ones_like(s)], -1),
                  lambda s: np.stack([np.ones_like(s), np.zeros_like(s)], -1), 0.0, 1.0, False)
        tot, ms, _ = curve_integral(C, [0, 0], [1, 1], N=4001)
        cf = 2 * math.asin((1 + 4 * h * (1 - h)) ** -0.5)
        print(f"sanity comb tooth h={h}: numeric {tot:.6f}, closed form {cf:.6f}")
    # Prop 4.4(a) limit I/k -> int_0^1 2 arcsin((1+4h(1-h))^-1/2) dh
    hs = (np.arange(200000) + 0.5) / 200000
    print(f"Prop 4.4 limit I/k = {np.mean(2 * np.arcsin((1 + 4 * hs * (1 - hs)) ** -0.5)):.5f} "
          f"(note: 1.8403); bound per tooth pi*sqrt2 = {math.pi * math.sqrt(2):.4f}")
    print("-- d = 1 curves: max over boxes of I/(C_{n,1} * local sum_I M^I) and of (single run)/C_{n,1}")
    for C in (circle(), ellipse(1.0, 0.1), line(0.3), line(math.pi / 4), line(1.2), helix(0.15), helix(1.0)):
        wt, wp = stress_curve(C)
        print(f"{C.name:16s} n={C.n}: worst total ratio {wt:.4f}, worst single-run ratio {wp:.4f}")
    print("-- d = 2 surfaces in R^3: max over boxes of (one graph patch)/C_{3,2}, C_{3,2} = "
          f"{Cnd(3, 2):.4f}; and total/(C_{{3,2}} * #nonzero patches)")
    tot, pp = surface_integral("ellipsoid", [-1, -1, -1], [1, 1, 1], G=600, par=(1, 1, 1))
    print(f"sanity sphere/[-1,1]^3: I = {tot:.5f} (q = 2 on S, so 4pi/2 = {2 * math.pi:.5f})")
    B = Cnd(3, 2)
    for kind, par in [("ellipsoid", (1, 1, 1)), ("ellipsoid", (1, .6, .3))] + \
                     [("plane", (v / np.linalg.norm(v), 0.0)) for v in
                      (np.array([1, 1, 1.]), np.array([1, .5, .2]), np.array([1, 1e-3, 1e-3]))]:
        worst_patch, worst_tot, cand = 0.0, 0.0, []
        for _ in range(500):
            if kind == "ellipsoid":
                z = rng.normal(size=3)
                z = z / np.linalg.norm(z) * np.asarray(par)
            else:
                z = rng.normal(size=3)
                z = z - (z @ par[0]) * par[0]
            c0 = z + rng.normal(0, 0.1, 3) * rng.choice([0, 1])
            lw = rng.uniform(math.log(0.02), math.log(3.0)) + rng.normal(0, 1.0, 3)
            p = np.concatenate([c0, lw])
            l, u = box_from(p, 3)
            tot, pp = surface_integral(kind, l, u, G=120, par=par)
            nz = sum(1 for x in pp if x > 1e-12)
            if nz == 0:
                continue
            rpatch, rtot = max(pp) / B, tot / (B * nz)
            worst_patch, worst_tot = max(worst_patch, rpatch), max(worst_tot, rtot)
            cand.append((rpatch, p))
        cand.sort(key=lambda t: -t[0])
        for _, p in cand[:3]:
            f = lambda x: -max(surface_integral(kind, *box_from(x, 3), G=90, par=par)[1]) / B
            r = minimize(f, p, method="Nelder-Mead", options={"maxiter": 200, "xatol": 1e-6, "fatol": 1e-7})
            tot, pp = surface_integral(kind, *box_from(r.x, 3), G=500, par=par)
            worst_patch = max(worst_patch, max(pp) / B)
        print(f"{kind} {np.round(np.asarray(par[0] if kind == 'plane' else par, float), 3)}: "
              f"worst patch ratio {worst_patch:.4f}, worst total/(C*#patches) {worst_tot:.4f}")


if __name__ == "__main__":
    main()
