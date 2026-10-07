"""Exactly feasible primal points for lnts50/100/200/400 with a rigorous
objective enclosure (interval existence proof by the Krawczyk test).

Usage: python3 lnts_primal.py 50 100 200 400

Construction (see report.md for the argument):
  * th_1..th_{N-1} are fixed at 40-digit decimal rationals close to the
    linear-tangent law (the known optimum structure);
  * the unknowns are z = (th_0, th_N, h);
  * every free state is defined by the forward recursion obtained by solving
    each OSIL row for its "next" state (each such row is linear in that state
    with coefficient 1), so all 4N rows hold exactly except that the
    recursion values of the fixed variables vx_N, vy_N, py_N must equal
    45, 0, 5;
  * F(z) = (vx_N(z) - 45, vy_N(z), py_N(z) - 5) = 0 is a square 3x3 system.
    The Krawczyk test, evaluated by forward-mode differentiation of the
    recursion in mpmath interval arithmetic, proves that F has exactly one
    zero z* in a box X of radius about 1e-50.
The point x* (rational th_1..th_{N-1}, z*, recursion states, fixed values)
is then exactly feasible. Bounds are checked over the box, the objective
N*h is enclosed over the box, and as a consistency check every OSIL row is
evaluated generically (from the parsed XML) over the full-variable box.

Not part of the proof: the closed-form sums (w, c) and the Newton solves,
which only produce the numbers that the interval test then checks.
"""
import os
import hashlib
import json
import sys
import time
from fractions import Fraction

import mpmath
from mpmath import iv, mp

import osil_iv

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil/lnts{}.osil")
DPS = 110           # working precision (decimal digits) for iv and Newton
TH_DIGITS = 40      # significant digits of the fixed rational controls
CENTER_DIGITS = 75  # significant digits of the box centre
RAD = [Fraction(1, 10**50), Fraction(1, 10**50), Fraction(1, 10**52)]  # radii for th_0, th_N, h
A = 100             # the OSIL constant in 100*cos / 100*sin (asserted below)

# our rigorous dual bounds: summary display (truncated) and the verifier's value (margin 1e-12)
DUAL_SUMMARY = {50: "0.5546687649381", 100: "0.5545954011663", 200: "0.5545770161025", 400: "0.5545724137001"}
DUAL_VERIFIER = {50: "0.5546687649381242", 100: "0.5545954011663566", 200: "0.5545770161025291",
                 400: "0.5545724137001325"}


# ---------------------------------------------------------------- structure
def layout(N):
    th = list(range(0, N + 1))
    px = list(range(N + 1, 2 * N + 2))
    py = list(range(2 * N + 2, 3 * N + 3))
    vx = list(range(3 * N + 3, 4 * N + 4))
    vy = list(range(4 * N + 4, 5 * N + 5))
    return th, px, py, vx, vy, 5 * N + 5


def check_structure(I, N):
    """Assert, by exact string comparison, that the OSIL model is the chain
    used below. Returns the layout and the dict of fixed values."""
    th, px, py, vx, vy, h = layout(N)
    n = len(I["names"])
    assert n == 5 * N + 6 and len(I["cons"]) == 4 * N, (n, len(I["cons"]))
    assert all(t == "C" for t in I["vt"]), "integer variables present"
    o = I["obj"]
    assert o["sense"] == "min" and o["lin"] == {h: str(N)} and o["quad"] == [] and o["nl"] is None, o
    fixed = {px[0]: "0", py[0]: "0", py[N]: "5", vx[0]: "0", vx[N]: "45", vy[0]: "0", vy[N]: "0"}
    for j in range(n):
        b = (I["lb"][j], I["ub"][j])
        if j in th:
            assert b == ("-1.5707963267949", "1.5707963267949"), (j, b)
        elif j == h:
            assert b == ("0", "INF"), (j, b)
        elif j in fixed:
            assert b == (fixed[j], fixed[j]), (j, b)
        else:
            assert b == ("-INF", "INF"), (j, b)
    for r, c in enumerate(I["cons"]):
        assert c["lb"] == "0" and c["ub"] == "0", (r, c["lb"], c["ub"])
        blk, i = divmod(r, N)
        if blk in (0, 1):  # p_{i+1} - p_i - .5 v_i h - .5 v_{i+1} h = 0
            p, v = (px, vx) if blk == 0 else (py, vy)
            assert c["lin"] == {p[i]: "-1", p[i + 1]: "1"}, (r, c["lin"])
            assert sorted(c["quad"]) == sorted([(v[i], h, "-.5"), (v[i + 1], h, "-.5")]), (r, c["quad"])
            assert c["nl"] is None
        else:  # v_{i+1} - v_i + (100 f(th_i) + 100 f(th_{i+1})) * (-.5) * h = 0
            v, f = (vx, "cos") if blk == 2 else (vy, "sin")
            assert c["lin"] == {v[i]: "-1", v[i + 1]: "1"} and c["quad"] == [], (r, c)
            want = ("product",
                    ("sum", ("product", (f, ("var", th[i], "1")), ("num", str(A))),
                     ("product", (f, ("var", th[i + 1], "1")), ("num", str(A)))),
                    ("num", "-.5"), ("var", h, "1"))
            assert c["nl"] == want, (r, c["nl"])
    return (th, px, py, vx, vy, h), {j: Fraction(s) for j, s in fixed.items()}


# ---------------------------------------------- forward-mode differentiation
class D:
    """value + gradient w.r.t. z = (th_0, th_N, h); works for mp and iv numbers."""
    __slots__ = ("v", "g")

    def __init__(self, v, g):
        self.v, self.g = v, g

    def __add__(self, o):
        return D(self.v + o.v, [a + b for a, b in zip(self.g, o.g)])

    def __sub__(self, o):
        return D(self.v - o.v, [a - b for a, b in zip(self.g, o.g)])

    def __mul__(self, o):
        return D(self.v * o.v, [self.v * b + o.v * a for a, b in zip(self.g, o.g)])

    def scale(self, c):
        return D(self.v * c, [a * c for a in self.g])


def recursion(th, h, ctx, keep=False):
    """Forward recursion obtained from the OSIL rows (solved for the next state):
      v_{i+1} = v_i - (100 f(th_i) + 100 f(th_{i+1})) * (-.5) * h
      p_{i+1} = p_i + .5 v_i h + .5 v_{i+1} h
    th: list of D, h: D, ctx: mpmath context (mp or iv). Returns the end
    states (and all states if keep)."""
    zero = D(ctx.mpf(0), [ctx.mpf(0)] * 3)
    a, half, mhalf = ctx.mpf(A), ctx.mpf(1) / 2, -ctx.mpf(1) / 2
    cs = [D(ctx.cos(t.v), [-ctx.sin(t.v) * gk for gk in t.g]) for t in th]
    sn = [D(ctx.sin(t.v), [ctx.cos(t.v) * gk for gk in t.g]) for t in th]
    px, py, vx, vy = [zero], [zero], [zero], [zero]  # px_0 = py_0 = vx_0 = vy_0 = 0 (fixed)
    N = len(th) - 1
    for i in range(N):
        vx.append(vx[i] - ((cs[i].scale(a) + cs[i + 1].scale(a)).scale(mhalf) * h))
        vy.append(vy[i] - ((sn[i].scale(a) + sn[i + 1].scale(a)).scale(mhalf) * h))
        px.append(px[i] + (vx[i] * h).scale(half) + (vx[i + 1] * h).scale(half))
        py.append(py[i] + (vy[i] * h).scale(half) + (vy[i + 1] * h).scale(half))
    if keep:
        return px, py, vx, vy
    return vx[N], vy[N], py[N]


def residual(thfix, z, ctx, with_grad):
    """F(z) and (optionally) its Jacobian, with th_1..th_{N-1} fixed."""
    N = len(thfix) + 1
    e = [[ctx.mpf(1) if k == m else ctx.mpf(0) for k in range(3)] for m in range(3)]
    nog = [ctx.mpf(0)] * 3
    th = [D(z[0], e[0] if with_grad else nog)] + [D(t, nog) for t in thfix] + [D(z[1], e[1] if with_grad else nog)]
    h = D(z[2], e[2] if with_grad else nog)
    vxN, vyN, pyN = recursion(th, h, ctx)
    F = [vxN.v - 45, vyN.v - 0, pyN.v - 5]
    J = [vxN.g, vyN.g, pyN.g]
    assert len(th) == N + 1
    return F, J


# ------------------------------------------------------------ numerics only
def tangent_law(N):
    """High-precision linear-tangent-law optimum via the closed-form sums
    (numerics only; the proof does not use these identities)."""
    w = [Fraction(1, 2)] + [Fraction(1)] * (N - 1) + [Fraction(1, 2)]
    c = [Fraction(0)] * (N + 1)
    for k in range(1, N + 1):
        for j in range(N + 1):
            c[j] += w[k] * Fraction((1 if j <= k - 1 else 0) + (1 if 1 <= j <= k else 0), 2)
    r = [mp.mpf(cj.numerator * wj.denominator) / (cj.denominator * wj.numerator) for wj, cj in zip(w, c)]
    wm = [mp.mpf(wj.numerator) / wj.denominator for wj in w]
    cm = [mp.mpf(cj.numerator) / cj.denominator for cj in c]

    def F(mu, nu, h):
        t = [mpmath.atan(mu + nu * rj) for rj in r]
        return [mp.fsum(wj * mpmath.sin(x) for wj, x in zip(wm, t)),
                A * h * mp.fsum(wj * mpmath.cos(x) for wj, x in zip(wm, t)) - 45,
                A * h * h * mp.fsum(cj * mpmath.sin(x) for cj, x in zip(cm, t)) - 5]

    mu, nu, h = mpmath.findroot(F, (mp.mpf("-1.41"), mp.mpf("2.82") / N, mp.mpf("0.5546") / N),
                                tol=mp.mpf(10) ** (-2 * DPS + 20))
    return [mpmath.atan(mu + nu * rj) for rj in r], h, (mu, nu)


def newton_z(thfix, z):
    for _ in range(30):
        F, J = residual(thfix, z, mp, True)
        dz = mp.lu_solve(mp.matrix(J), mp.matrix(F))
        z = [z[k] - dz[k] for k in range(3)]
        if max(abs(x) for x in dz) < mp.mpf(10) ** (-DPS + 5):
            break
    return z


# ------------------------------------------------------------- helpers
def dec(x, digits):
    """Decimal string with `digits` significant digits (round to nearest)."""
    return mpmath.nstr(x, digits, min_fixed=-10**9, max_fixed=10**9)


def to_iv(q):
    q = Fraction(q)
    return iv.mpf(q.numerator) / q.denominator


def _tfrac(t):
    """Exact Fraction of a raw mpf tuple (sign, man, exp, bc); rejects inf/nan."""
    sgn, man, e, _ = t
    assert man != 0 or e == 0, "special value"
    q = Fraction(int(man)) * (Fraction(2) ** e)
    return -q if sgn else q


def ends(X):
    """Exact rational end points of an iv interval."""
    a, b = X._mpi_
    return _tfrac(a), _tfrac(b)


def hull(a_iv, b_iv):
    """Interval [lower end of a_iv, upper end of b_iv] (exact, same precision)."""
    return iv.mpf([mp.make_mpf(a_iv._mpi_[0]), mp.make_mpf(b_iv._mpi_[1])])


def meet(K, X):
    """K intersect X (exact); assumes they overlap."""
    ka, kb = ends(K)
    xa, xb = ends(X)
    lo = K if ka >= xa else X
    hi = K if kb <= xb else X
    return hull(lo, hi)


def dec_down(q, k):
    """Largest decimal with k digits after the point that is <= q."""
    n = (q * 10**k).__floor__()
    return Fraction(n, 10**k)


def dec_up(q, k):
    n = -((-q * 10**k).__floor__())
    return Fraction(n, 10**k)


def fstr(q, k):
    s = "-" if q < 0 else ""
    q = abs(q)
    n = q * 10**k
    assert n.denominator == 1
    n = n.numerator
    ip, fp = divmod(n, 10**k)
    return f"{s}{ip}.{fp:0{k}d}"


def krawczyk(thfix_iv, y, X):
    """One Krawczyk step; returns K(X) (list of intervals)."""
    Fy, _ = residual(thfix_iv, y, iv, False)
    _, JX = residual(thfix_iv, X, iv, True)
    Jm = mp.matrix([[mp.make_mpf(JX[i][j].mid._mpi_[0]) for j in range(3)] for i in range(3)])
    C = Jm ** -1  # any real matrix works; its entries are used exactly below
    Ci = [[iv.mpf(C[i, j]) for j in range(3)] for i in range(3)]
    K = []
    for i in range(3):
        s = y[i]
        for k in range(3):
            s = s - Ci[i][k] * Fy[k]
        for j in range(3):
            m = (iv.mpf(1) if i == j else iv.mpf(0))
            for k in range(3):
                m = m - Ci[i][k] * JX[k][j]
            s = s + m * (X[j] - y[j])
        K.append(s)
    return K


# -------------------------------------------------------------------- main
def run(N):
    t0 = time.time()
    mp.dps = DPS
    iv.dps = DPS
    path = OSIL.format(N)
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    I = osil_iv.read(path)
    (th, px, py, vx, vy, hix), fixed = check_structure(I, N)

    # 1. numbers (not part of the proof)
    thstar, hstar, (mu, nu) = tangent_law(N)
    thfix_str = [dec(thstar[j], TH_DIGITS) for j in range(1, N)]
    thfix_q = [Fraction(s) for s in thfix_str]
    thfix_mp = [mp.mpf(q.numerator) / q.denominator for q in thfix_q]
    z = newton_z(thfix_mp, [thstar[0], thstar[N], hstar])
    zc_str = [dec(x, CENTER_DIGITS) for x in z]
    zc = [Fraction(s) for s in zc_str]

    # 2. Krawczyk test on X = zc +- RAD (all arithmetic outward rounded)
    thfix_iv = [to_iv(q) for q in thfix_q]
    # X = outward enclosure of the exact box [zc - RAD, zc + RAD]
    X = [hull(to_iv(zc[k] - RAD[k]), to_iv(zc[k] + RAD[k])) for k in range(3)]
    Y = [to_iv(q) for q in zc]  # thin enclosures of the centre (a point of X)
    K = krawczyk(thfix_iv, Y, X)
    inside = all(ends(K[k])[0] > ends(X[k])[0] and ends(K[k])[1] < ends(X[k])[1] for k in range(3))
    assert inside, "Krawczyk test failed"
    Z = [meet(K[k], X[k]) for k in range(3)]  # contains the unique zero z* of F in X
    Y2 = [iv.mpf(v.mid) for v in Z]  # a point inside the step-1 box
    K2 = krawczyk(thfix_iv, Y2, Z)  # z* is in K(Z) too (Krawczyk operator keeps all zeros)
    Z = [meet(K2[k], Z[k]) for k in range(3)]
    # z* lies inside the exact decimal box centre +- radius stored in the point file
    for k in range(3):
        a_, b_ = ends(Z[k])
        assert zc[k] - RAD[k] < a_ and b_ < zc[k] + RAD[k]

    # 3. bounds: th in [-1.5707963267949, 1.5707963267949] (exact decimal; also its double)
    lbq, ubq = Fraction("-1.5707963267949"), Fraction("1.5707963267949")
    lbd, ubd = Fraction(float("-1.5707963267949")), Fraction(float("1.5707963267949"))
    lo_th, hi_th = max(lbq, lbd), min(ubq, ubd)
    assert all(lo_th <= q <= hi_th for q in thfix_q)
    for k in (0, 1):
        a_, b_ = ends(Z[k])
        assert lo_th <= a_ and b_ <= hi_th
    h_lo, h_hi = ends(Z[2])
    assert h_lo > 0  # h >= 0

    # 4. full-variable box: states by interval recursion over Z
    thD = [D(Z[0], [iv.mpf(0)] * 3)] + [D(t, [iv.mpf(0)] * 3) for t in thfix_iv] + [D(Z[1], [iv.mpf(0)] * 3)]
    hD = D(Z[2], [iv.mpf(0)] * 3)
    PX, PY, VX, VY = recursion(thD, hD, iv, keep=True)
    # the end values of the recursion must contain the fixed values (consistency)
    for E, val in ((VX[N].v, 45), (VY[N].v, 0), (PY[N].v, 5)):
        a_, b_ = ends(E)
        assert a_ <= val <= b_
    Xfull = [None] * (5 * N + 6)
    for j in range(N + 1):
        Xfull[th[j]] = thD[j].v
        Xfull[px[j]], Xfull[py[j]], Xfull[vx[j]], Xfull[vy[j]] = PX[j].v, PY[j].v, VX[j].v, VY[j].v
    Xfull[hix] = Z[2]
    for j, q in fixed.items():  # fixed variables take their exact values
        Xfull[j] = to_iv(q)
    # generic bound check over the full box (all bounds from the parsed XML)
    for j in range(len(Xfull)):
        a_, b_ = ends(Xfull[j])
        if not osil_iv.isinf(I["lb"][j]):
            assert a_ >= Fraction(I["lb"][j]), (j, "lb")
        if not osil_iv.isinf(I["ub"][j]):
            assert b_ <= Fraction(I["ub"][j]), (j, "ub")
    # generic row check over the full box (consistency: necessary, not sufficient)
    maxw = 0
    for r, c in enumerate(I["cons"]):
        R = osil_iv.ev_row(c, Xfull)
        a_, b_ = ends(R)
        assert a_ <= Fraction(c["lb"]) and Fraction(c["ub"]) <= b_, (r, R)
        maxw = max(maxw, float(b_ - a_))

    # 5. objective enclosure over the box, generically from the XML and directly
    OBJ = osil_iv.ev_row(I["obj"], Xfull)
    obj_lo, obj_hi = ends(OBJ)
    assert obj_lo <= N * h_lo and N * h_hi <= obj_hi
    obj_lo, obj_hi = N * h_lo, N * h_hi  # exact products of the box ends
    res = dict(instance=f"lnts{N}", N=N, osil=path, osil_sha256=sha, dps=DPS,
               krawczyk_inside=inside,
               box_X_center=zc_str, box_X_radius=[str(r) for r in RAD],
               zero_enclosure_widths=[float(ends(Z[k])[1] - ends(Z[k])[0]) for k in range(3)],
               max_row_enclosure_width=maxw,
               obj_lo_25=fstr(dec_down(obj_lo, 25), 25), obj_hi_25=fstr(dec_up(obj_hi, 25), 25),
               obj_width=float(obj_hi - obj_lo))
    for tag, D_ in (("summary", DUAL_SUMMARY), ("verifier", DUAL_VERIFIER)):
        g = obj_hi - Fraction(D_[N])
        res[f"dual_{tag}"] = D_[N]
        res[f"gap_vs_{tag}_upper"] = fstr(dec_up(g, 20), 20)
        res[f"rel_gap_vs_{tag}_upper"] = mpmath.nstr(mp.mpf(g.numerator) / g.denominator / mp.mpf(D_[N]) * (1 + mp.mpf(10) ** -30), 5)
    res["seconds"] = round(time.time() - t0, 1)

    # 6. point file
    names = I["names"]
    enc = []
    for j in range(len(Xfull)):
        a_, b_ = ends(Xfull[j])
        enc.append([names[j], fstr(dec_down(a_, 60), 60), fstr(dec_up(b_, 60), 60)])
    point = dict(
        instance=f"lnts{N}", osil=path, osil_sha256=sha,
        description=("Exactly feasible point x*. th_1..th_{N-1} are the exact decimal rationals in "
                     "'fixed_controls'. (th_0, th_N, h) is the unique zero of F in the box "
                     "'unknowns_box' (centre +- radius, exact decimals), proved by the Krawczyk test; "
                     "F(z) = (vx_N - 45, vy_N, py_N - 5) with states from the forward recursion "
                     "v_{i+1} = v_i + 50 h (f(th_i) + f(th_{i+1})), p_{i+1} = p_i + h (v_i + v_{i+1}) / 2, "
                     "f = cos for vx, sin for vy, and px_0 = py_0 = vx_0 = vy_0 = 0. All other "
                     "variables equal the recursion values; fixed variables equal their fixed values. "
                     "'enclosures' gives a rigorous outward-rounded [lo, hi] for every variable of x* "
                     "in OSIL order."),
        fixed_controls={names[th[j]]: thfix_str[j - 1] for j in range(1, N)},
        unknowns_box={names[th[0]]: dict(centre=zc_str[0], radius=str(RAD[0])),
                      names[th[N]]: dict(centre=zc_str[1], radius=str(RAD[1])),
                      names[hix]: dict(centre=zc_str[2], radius=str(RAD[2]))},
        fixed_variables={names[j]: str(q) for j, q in fixed.items()},
        objective_enclosure=[res["obj_lo_25"], res["obj_hi_25"]],
        enclosures=enc)
    with open(f"points/lnts{N}_point.json", "w") as f:
        json.dump(point, f, indent=1)
    print(json.dumps(res), flush=True)
    return res


if __name__ == "__main__":
    out = [run(int(a)) for a in sys.argv[1:]]
    with open("logs/lnts_primal_" + "_".join(sys.argv[1:]) + ".json", "w") as f:
        json.dump(out, f, indent=1)
