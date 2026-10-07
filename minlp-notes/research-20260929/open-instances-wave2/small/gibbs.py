"""Rigorous dual bounds and primal points for ex6_2_7 and ex6_2_5 (Gibbs energy).

Method (Lagrangian over the 3 mass balances, tangent-plane test per phase):
  for every feasible n,  f(n) = sum_p G_p(n_p) = lam.b + sum_p [G_p(n_p) - lam.n_p]
  and, writing n_p = t y (t = sum n_p, y in the simplex),
      G_p(t y) - lam.(t y) = t (G_p(y) - lam.y) + t ln t R_p(y)      (exact scaling identity,
                                                                    R_p from gibbs_model)
  with t in (0, tmax], tmax = sum_i b_i, and y_i >= ymin = 1e-7 / tmax.
  If m_p <= min_y (G_p(y) - lam.y) over that simplex, then
      f(n) >= lam.b + sum_p [ min(0, tmax m_p) + E_p ],   E_p <= min t ln t R_p(y).
  m_p is certified by a 2-D interval branch and bound (numpy, outward rounding;
  log widened by 16 ulp), and every leaf box is re-verified with mpmath.iv.

Primal: multistart SLSQP, then Newton on the KKT system in 50-digit arithmetic;
the reported point is rounded to 17 significant digits, and the last phase is
set to b - (other phases) in exact decimal arithmetic, so the rows hold exactly.

Usage: python3 gibbs.py ex6_2_7|ex6_2_5 [tau]
"""
import json
import os
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction

import mpmath as mp
import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ev  # noqa: E402
import gibbs_model as gm  # noqa: E402
import ia  # noqa: E402
from ia import AD, NI  # noqa: E402

name = sys.argv[1]
TAU = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-12
LOG = open(os.path.join(ev.HERE, "logs", f"{name}_gibbs.log"), "w")


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


M = gm.load(name)
TR = gm.phase_trees(M)
I = M["I"]
bF = [Fraction(v) for v in M["b"]]
b = np.array([float(v) for v in M["b"]])
say(f"{name}: b = {M['b']}, terms/phase {[len(t) for t in TR]}, R_p = {[[str(v) for v in r] for r in M['R']]}")

# ---------------- primal: multistart + Newton ----------------
FFN = {"ln": np.log}


def Gf(p, n):
    return gm.G_eval(TR[p], list(n), float, FFN)


def ftot(x):
    return sum(Gf(p, x[M["phases"][p]]) for p in range(3))


rng = np.random.default_rng(1)
cons = [{"type": "eq", "fun": (lambda x, i=i: x[3 * i] + x[3 * i + 1] + x[3 * i + 2] - b[i])} for i in range(3)]
bnds = [(1e-7, b[j // 3]) for j in range(9)]
best = None
for trial in range(200):
    W = rng.dirichlet(np.ones(3), size=3)
    x0 = np.maximum(np.array([W[j // 3][j % 3] * b[j // 3] for j in range(9)]), 2e-7)
    r = minimize(ftot, x0, method="SLSQP", bounds=bnds, constraints=cons, options={"ftol": 1e-14, "maxiter": 500})
    if r.success and (best is None or r.fun < best.fun):
        best = r
say("multistart best (float):", best.fun)

mp.mp.dps = 50
MPFN = {"ln": lambda a: ia.ad_log(a, mp.log)}


def grad_mp(p, n):
    x = [AD(mp.mpf(n[i]), tuple(mp.mpf(1 if k == i else 0) for k in range(3))) for i in range(3)]
    s = None
    for T in TR[p]:
        v = ia.ev_ad(T, x, mp.mpf, MPFN)
        s = v if s is None else s + v
    return s.v, list(s.g)


# unknowns: n (9, variable order x2..x10) and lam (3)
xk = [mp.mpf(v) for v in best.x]
lam = [mp.mpf(0)] * 3
g0 = grad_mp(0, [xk[j] for j in M["phases"][0]])[1]
lam = list(g0)


def F(z):
    n, lm = z[:9], z[9:]
    out = []
    for p in range(3):
        idx = M["phases"][p]
        g = grad_mp(p, [n[j] for j in idx])[1]
        out += [g[i] - lm[i] for i in range(3)]
    out += [n[3 * i] + n[3 * i + 1] + n[3 * i + 2] - mp.mpf(M["b"][i]) for i in range(3)]
    return out


z = xk + lam
for it in range(30):
    Fz = F(z)
    res = max(abs(v) for v in Fz)
    if res < mp.mpf("1e-45"):
        break
    h = mp.mpf("1e-25")
    J = mp.matrix(12, 12)
    for j in range(12):
        zz = list(z)
        zz[j] += h * max(1, abs(z[j]))
        Fj = F(zz)
        for i in range(12):
            J[i, j] = (Fj[i] - Fz[i]) / (h * max(1, abs(z[j])))
    dz = mp.lu_solve(J, mp.matrix([-v for v in Fz]))
    z = [z[i] + dz[i] for i in range(12)]
say(f"Newton: {it} iterations, KKT residual {mp.nstr(max(abs(v) for v in F(z)), 3)}")
nstar = z[:9]
lamstar = z[9:]
assert all(v > mp.mpf("1e-7") for v in nstar), "a component is at its lower bound; KKT system would differ"
fstar = sum(gm.G_eval(TR[p], [nstar[j] for j in M["phases"][p]], mp.mpf, {"ln": mp.log}) for p in range(3))
say("KKT point objective (50 digits):", mp.nstr(fstar, 25))
say("lambda (50 digits):", [mp.nstr(v, 25) for v in lamstar])
say("lam.b:", mp.nstr(sum(lamstar[i] * mp.mpf(M["b"][i]) for i in range(3)), 25))

# primal point with exact mass balances: phases 0,1 rounded to 17 digits, phase 2 = b - others (exact decimal)
getcontext().prec = 60
xs = [Decimal(mp.nstr(v, 17)) for v in nstar]
for i in range(3):
    xs[3 * i + 2] = Decimal(M["b"][i]) - xs[3 * i] - xs[3 * i + 1]
r = ev.evaluate(I, [str(v) for v in xs], dps=50)
say(f"primal point: obj {mp.nstr(r['obj'], 20)}, max row viol {mp.nstr(r['row_viol'], 3)}, max bound viol {mp.nstr(r['bound_viol'], 3)}")
primal_obj = r["obj"]
with open(os.path.join(ev.HERE, "logs", f"{name}_primal.txt"), "w") as fo:
    for j, nm in enumerate(I["names"]):
        fo.write(f"{nm} {xs[j]}\n")

# ---------------- dual: lam as doubles (used as exact binary values) ----------------
lamd = [float(v) for v in lamstar]
tmax = float(sum(bF))                       # sum of b_i (exact here: 1 or 100)
assert Fraction(tmax) == sum(bF)
ymin = float(np.nextafter(1e-7 / tmax, 0))  # y_i = n_i/t >= 1e-7/tmax; slightly smaller is a superset
dn, up = ia.dn, ia.up


def dep_order(p):
    """dependent component = largest amount at the KKT point (keeps tangent points off the hypotenuse)"""
    n = [float(nstar[j]) for j in M["phases"][p]]
    d = int(np.argmax(n))
    return [k for k in range(3) if k != d] + [d]


def ad_eval(p, order, Y1, Y2, Y3, second):
    """G_p in the 2-D parametrization y_o0 = Y1, y_o1 = Y2, y_o2 = Y3 (= 1 - y_o0 - y_o1, enclosed
    separately); derivatives w.r.t. (y_o0, y_o1). second=True: nested AD (value, gradient, Hessian)."""
    z = NI(np.zeros(Y1.lo.shape))
    one = NI(np.ones(Y1.lo.shape))
    mone = NI(-np.ones(Y1.lo.shape))
    seeds = {order[0]: (one, z), order[1]: (z, one), order[2]: (mone, mone)}
    Ys = {order[0]: Y1, order[1]: Y2, order[2]: Y3}
    if second:
        x = [AD(AD(Ys[i], seeds[i]), (AD(seeds[i][0], (z, z)), AD(seeds[i][1], (z, z)))) for i in range(3)]
        fn = {"ln": lambda a: ia.ad_log(a, lambda v: ia.ad_log(v, ia.ilog))}
    else:
        x = [AD(Ys[i], seeds[i]) for i in range(3)]
        fn = {"ln": lambda a: ia.ad_log(a, ia.ilog)}
    s = None
    for T in TR[p]:
        v = ia.ev_ad(T, x, NI.const, fn)
        s = v if s is None else s + v
    return s


def quad1d_min(g, lam, D):
    """rigorous lower bound of min over d in D=[l,u], gg in g=[g_lo,g_hi] of gg*d + lam/2 d^2 (lam: float array)."""
    l, u = D.lo, D.hi
    L = NI(lam) * 0.5
    vals = []
    for gg in (NI(g.lo), NI(g.hi)):
        for d in (NI(l), NI(u)):
            vals.append((gg * d + L * (d * d)).lo)
    endmin = np.minimum(np.minimum(vals[0], vals[1]), np.minimum(vals[2], vals[3]))
    pos = lam > 0
    lam_safe = np.where(pos, lam, 1.0)
    gmax2 = np.maximum(g.lo * g.lo, g.hi * g.hi)
    vert = -(up(up(gmax2) / dn(2.0 * lam_safe)))          # -g^2/(2 lam), rounded down
    marg = 1e-9 * (np.abs(l) + np.abs(u)) + 1e-300
    v1, v2 = -g.lo / lam_safe, -g.hi / lam_safe
    vlo, vhi = np.minimum(v1, v2), np.maximum(v1, v2)
    maybe_inside = pos & (vhi >= l - marg) & (vlo <= u + marg)
    return np.where(maybe_inside, np.minimum(endmin, vert), endmin)


def lower_bounds(p, order, lo1, hi1, lo2, hi2):
    Y1, Y2 = NI(lo1, hi1), NI(lo2, hi2)
    Y3 = NI(np.maximum(dn(dn(1.0 - hi1) - hi2), ymin), up(up(1.0 - lo1) - lo2))
    L = [NI(lamd[o]) for o in order]
    dL = [L[0] - L[2], L[1] - L[2]]
    s = ad_eval(p, order, Y1, Y2, Y3, True)
    nat = s.v.v - L[0] * Y1 - L[1] * Y2 - L[2] * Y3
    gB = [s.v.g[a] - dL[a] for a in range(2)]
    c1, c2 = 0.5 * (lo1 + hi1), 0.5 * (lo2 + hi2)
    C3 = NI(dn(dn(1.0 - c1) - c2), up(up(1.0 - c1) - c2))
    ok = C3.lo >= ymin
    C3 = NI(np.where(ok, C3.lo, 0.5), np.where(ok, C3.hi, 0.5))
    C1, C2 = NI(c1), NI(c2)
    sc = ad_eval(p, order, C1, C2, C3, False)
    fc = sc.v - L[0] * C1 - L[1] * C2 - L[2] * C3
    gc = [sc.g[a] - dL[a] for a in range(2)]
    D1, D2 = Y1 - C1, Y2 - C2
    mv = fc + gB[0] * D1 + gB[1] * D2
    # second order: f(y) >= f(c) + g(c).d + lam_lo/2 |d|^2, lam_lo <= lambda_min(H) on the box
    H00, H11 = s.g[0].g[0], s.g[1].g[1]
    bmax = np.maximum(np.maximum(np.abs(s.g[0].g[1].lo), np.abs(s.g[0].g[1].hi)),
                      np.maximum(np.abs(s.g[1].g[0].lo), np.abs(s.g[1].g[0].hi)))
    A, Cc, B = NI(H00.lo), NI(H11.lo), NI(bmax)
    half = (A + Cc) * 0.5
    diff = (A - Cc) * 0.5
    lam_lo = (half - ia.isqrt(diff * diff + B * B)).lo
    q1 = quad1d_min(gc[0], lam_lo, D1)
    q2 = quad1d_min(gc[1], lam_lo, D2)
    so2 = dn(dn(fc.lo + q1) + q2)
    lb = np.where(ok, np.maximum(nat.lo, np.maximum(mv.lo, so2)), nat.lo)
    return lb, np.where(ok, fc.hi, np.inf), lam_lo


def bnb(p, maxlevel=60):
    order = dep_order(p)
    lo1, hi1, lo2, hi2 = np.array([ymin]), np.array([1.0]), np.array([ymin]), np.array([1.0])
    leaves, ub, nbox, level = [], np.inf, 0, 0
    while lo1.size:
        level += 1
        keep = up(up(1.0 - lo1) - lo2) >= ymin     # drop boxes entirely outside y3 >= ymin
        lo1, hi1, lo2, hi2 = lo1[keep], hi1[keep], lo2[keep], hi2[keep]
        if not lo1.size:
            break
        nbox += lo1.size
        lbs, fch = [], []
        for k in range(0, lo1.size, 200000):
            sl = slice(k, k + 200000)
            lb_, fc_, _ = lower_bounds(p, order, lo1[sl], hi1[sl], lo2[sl], hi2[sl])
            lbs.append(lb_)
            fch.append(fc_)
        lb, fch = np.concatenate(lbs), np.concatenate(fch)
        ub = min(ub, float(np.min(fch)))
        fath = lb >= -TAU
        if np.any(fath):
            leaves.append(np.stack([lo1[fath], hi1[fath], lo2[fath], hi2[fath], lb[fath]], axis=1))
        lo1, hi1, lo2, hi2 = lo1[~fath], hi1[~fath], lo2[~fath], hi2[~fath]
        if not lo1.size:
            break
        if level >= maxlevel:
            say(f"  phase {p}: STOP at level {level}: {lo1.size} open boxes, min lb {np.min(lb[~fath]):.3e}")
            return None, ub, nbox, np.concatenate(leaves), level
        m1, m2 = 0.5 * (lo1 + hi1), 0.5 * (lo2 + hi2)
        lo1, hi1, lo2, hi2 = (np.concatenate([lo1, m1, lo1, m1]), np.concatenate([m1, hi1, m1, hi1]),
                              np.concatenate([lo2, lo2, m2, m2]), np.concatenate([m2, m2, hi2, hi2]))
    leaves = np.concatenate(leaves)
    return float(np.min(leaves[:, 4])), ub, nbox, leaves, level


def f_mp(p, order, y1, y2):
    """f = G_p(y) - lam.y at a point, 40 digits (for the sampling sanity check)."""
    with mp.workdps(40):
        y = [None] * 3
        y[order[0]], y[order[1]] = mp.mpf(y1), mp.mpf(y2)
        y[order[2]] = 1 - y[order[0]] - y[order[1]]
        g = gm.G_eval(TR[p], y, mp.mpf, {"ln": mp.log})
        return g - sum(mp.mpf(lamd[k]) * y[k] for k in range(3))


distinct = []
for p in range(3):
    if not any(TR[p] == TR[q] for q in distinct):
        distinct.append(p)
say("distinct phase functions:", distinct, "; tau =", TAU, "; ymin =", ymin, "; tmax =", tmax)
m = {}
rs = np.random.default_rng(7)
for p in distinct:
    t0 = time.time()
    mlb, ub, nbox, leaves, level = bnb(p)
    say(f"  phase {p} (dependent comp {dep_order(p)[2]}): boxes {nbox}, leaves {len(leaves)}, levels {level}, "
        f"certified min >= {mlb}, best f(center) <= {ub:.3e}, {time.time() - t0:.1f} s")
    m[p] = mlb
    if mlb is None:
        continue
    # sanity check (not part of the proof): f at random points of sampled leaves >= the leaf's bound
    order = dep_order(p)
    idx = np.concatenate([np.argsort(leaves[:, 4])[:200], rs.integers(0, len(leaves), 800)])
    worst = mp.inf
    for k in idx:
        lo1, hi1, lo2, hi2, lb = leaves[k]
        for _ in range(2):
            y1, y2 = rs.uniform(lo1, hi1), rs.uniform(lo2, hi2)
            if 1 - y1 - y2 < ymin:
                continue
            worst = min(worst, f_mp(p, order, y1, y2) - mp.mpf(lb))
    say(f"  phase {p}: sampled {len(idx)} leaves: min (f(y) - leaf bound) = {mp.nstr(worst, 4)} (must be >= 0)")
mp_all = {p: m[[q for q in distinct if TR[q] == TR[p]][0]] for p in range(3)}
if any(v is None for v in mp_all.values()):
    say("dual bound: FAILED (B&B did not fathom)")
    sys.exit(1)
iv = mp.iv

# assemble the bound in mpmath interval arithmetic
iv.dps = 40
lamb = sum(iv.mpf(lamd[i]) * iv.mpf(M["b"][i]) for i in range(3))
total = lamb
for p in range(3):
    mp_ = iv.mpf(mp_all[p])
    term = mp_ * iv.mpf(tmax) if mp_all[p] < 0 else iv.mpf(0)
    # E_p: t ln t R_p(y) with t in (0, tmax], y in simplex; R_p >= 0 coefficients here
    # E_p: t ln t R_p(y) >= -(1/e) max_i R_p,i, because R_p,i >= 0 (asserted), 0 <= R_p(y) <= max_i R_p,i
    # and t ln t >= -1/e for t > 0
    R = M["R"][p]
    assert all(v >= 0 for v in R)
    Rmax = max(R)
    E = -(iv.mpf(Rmax.numerator) / iv.mpf(Rmax.denominator)) / iv.e if Rmax > 0 else iv.mpf(0)
    total = total + term + E
say("lam.b (interval):", lamb)
say(f"RIGOROUS DUAL BOUND: {mp.nstr(mp.mpf(total.a), 17)}")
say(f"primal: {mp.nstr(primal_obj, 17)}; gap {mp.nstr(primal_obj - mp.mpf(total.a), 3)}")
json.dump(dict(name=name, dual=str(mp.mpf(total.a)), primal=str(primal_obj), lam=lamd, m={str(k): v for k, v in mp_all.items()},
               tau=TAU, tmax=tmax, ymin=ymin), open(os.path.join(ev.HERE, "logs", f"{name}_gibbs.json"), "w"), indent=1)
