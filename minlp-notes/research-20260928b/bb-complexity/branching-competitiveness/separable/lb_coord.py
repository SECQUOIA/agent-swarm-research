"""Exact check of the coordinate-ambiguity lower bound (every I1 rule, n >= 2).

Two 1D functions on [0,1] (alpha = 1; H = m + t^2 is a maximum of four lines, so convex):
  R ('rigid'):      H_R = max(lL, lR, t/2 + phi,  3t/2 - 1/2 + phi)
  N ('non-rigid'):  H_N = max(lL, lR, t/2 - phi', 3t/2 - 1/2 - phi'),   phi' = phi/(n-1)
with the common lines lL = r0 + 1/4 + sL (t - 1/2), lR = r0 + 1/4 + sR (t - 1/2).
So R = N near 1/2, and R - N = phi + phi' (a constant) near 0 and near 1.
Instance A_i (i = 1..n): coordinate i uses R, the others use N.  Then all A_i coincide on a
neighbourhood of the centre (1/2,...,1/2) and on a neighbourhood of every corner of [0,1]^n.
Checks, exactly: convexity; the agreement neighbourhoods; min m = 0 (so f* = min f); unique
root minimizer (1/2,...,1/2) and equal root value in all A_i; root invalid; cutting coordinate i
at 1/2 gives two valid children (T_opt = 3); cutting any other coordinate at any point gives two
invalid children (T >= 7).
usage: python3 lb_coord.py n"""
import sys
from fractions import Fraction as Fr
from sepexact import Coord

HALF, QUART = Fr(1, 2), Fr(1, 4)


def lines(n, eps, r0, sL, sR, sign):
    phi = (n - 1) * (QUART - r0) - eps / 2
    c = phi if sign > 0 else -phi / (n - 1)
    return [(sL, r0 + QUART - HALF * sL), (sR, r0 + QUART - HALF * sR),
            (HALF, c), (Fr(3, 2), c - HALF)], phi


def coord(ls):
    pts = {Fr(0), Fr(1)}
    for i in range(len(ls)):
        for j in range(i + 1, len(ls)):
            (a1, b1), (a2, b2) = ls[i], ls[j]
            if a1 != a2:
                t = (b2 - b1) / (a1 - a2)
                if 0 < t < 1:
                    pts.add(t)
    xs = sorted(pts)
    H = [max(a * t + b for a, b in ls) for t in xs]
    return Coord(xs, H, shift=False)


def check(n, eps, r0, sL, sR):
    LR, phi = lines(n, eps, r0, sL, sR, +1)
    LN, _ = lines(n, eps, r0, sL, sR, -1)
    R, N = coord(LR), coord(LN)
    out = {"phi": phi, "convex": R.is_convex() and N.is_convex()}
    # agreement, computed exactly from the knots (H_R, H_N are piecewise linear with knots R.x, N.x):
    # centre: both equal max(lL, lR) between the last knots below 1/2 and the first above;
    # ends: both are on their floor lines (slope 1/2 at 0, 3/2 at 1) up to their first/last knot.
    lo = max(max(x for x in R.x if x < HALF), max(x for x in N.x if x < HALF))
    hi = min(min(x for x in R.x if x > HALF), min(x for x in N.x if x > HALF))
    centre_ok = all(R.Hat(t) == N.Hat(t) for t in (lo, HALF, hi))
    out["R = N on"] = (lo, hi, centre_ok)
    a, b = min(R.x[1], N.x[1]), max(R.x[-2], N.x[-2])
    c0 = R.m(Fr(0)) - N.m(Fr(0))
    ends_ok = all(R.m(t) - N.m(t) == c0 for t in (Fr(0), a, b, Fr(1))) and a > 0 and b < 1
    out["R - N = const on [0,a] and [b,1]"] = (c0, a, b, ends_ok)
    minR = min(R.m(t) for t in R.x)
    minN = min(N.m(t) for t in N.x)
    out["min m"] = minR + (n - 1) * minN
    FR, yR, _ = R.node(Fr(0), Fr(1))
    FN, yN, _ = N.node(Fr(0), Fr(1))
    uniq = all(R.H[q] - R.x[q] > FR for q in range(len(R.x)) if R.x[q] != yR) and \
        all(N.H[q] - N.x[q] > FN for q in range(len(N.x)) if N.x[q] != yN)
    out["root minimizers, unique"] = (yR, yN, uniq)
    root = FR + (n - 1) * FN
    out["root value, invalid"] = (root, root + eps < 0)
    ch = [R.F(Fr(0), HALF), R.F(HALF, Fr(1))]
    out["R-cut child margins (>= 0: valid)"] = [h + (n - 1) * FN + eps for h in ch]
    worst = max(N.F(*iv) for k in range(1, 1000) for iv in ((Fr(0), Fr(k, 1000)), (Fr(k, 1000), Fr(1))))
    out["N-cut: max child value + eps over 999 cut points (< 0: invalid)"] = worst + FR + (n - 2) * FN + eps
    out["N-cut: analytic bound max(N(0),N(1)) + FR + (n-2)FN + eps"] = max(N.m(Fr(0)), N.m(Fr(1))) + FR + (n - 2) * FN + eps
    return out


def tiefree_R(n, eps, r0, sL, sR, p):
    """Variant of R with root minimizer p (not 1/2) and the same root value -c; its outer lines
    pass through p, so that cutting at p still leaves two valid children."""
    phi = (n - 1) * (QUART - r0) - eps / 2
    c = QUART - r0
    ls = [(sL, p - c - sL * p), (sR, p - c - sR * p), (p, phi), (1 + p, phi - p)]
    return coord(ls)


def rules_on(cs, eps, sels=("knot", "proj")):
    from sepexact import Coord, run
    out = {}
    for sel in sels:
        Coord.sel = sel
        for C in cs:
            C.cache.clear()
        out[sel] = {rule: run(cs, eps, rule)["nodes"] for rule in ("omega", "deficit")}
    Coord.sel = "knot"
    return out


if __name__ == "__main__":
    # usage: python3 lb_coord.py [n ...]   (default: 2..40 checks, rules for 2..5)
    ns = [int(a) for a in sys.argv[1:]] or list(range(2, 41))
    eps = Fr(1, 100)
    for n in ns:
        r0 = QUART - Fr(1, 5 * n)          # c = 1/(5n); r0 = 3/20 at n = 2
        sL, sR = 1 - eps / (4 * (n - 1)), 1 + eps / (4 * (n - 1))
        out = check(n, eps, r0, sL, sR)
        ok = (out["convex"] and out["min m"] == 0 and out["root minimizers, unique"][2]
              and out["root value, invalid"][1] and min(out["R-cut child margins (>= 0: valid)"]) >= 0
              and out["N-cut: max child value + eps over 999 cut points (< 0: invalid)"] < 0
              and out["N-cut: analytic bound max(N(0),N(1)) + FR + (n-2)FN + eps"] < 0
              and out["R - N = const on [0,a] and [b,1]"][3] and out["R = N on"][2])
        print(f"n={n}: all items hold: {ok}; " + "; ".join(f"{k}: {v}" for k, v in out.items()), flush=True)
        assert ok
        if n <= 5:
            from sepexact import opt_min
            R = coord(lines(n, eps, r0, sL, sR, +1)[0])
            N = coord(lines(n, eps, r0, sL, sR, -1)[0])
            for i in range(n):
                cs = [N] * n
                cs[i] = R
                extra = f", OPT_min leaves {opt_min(cs[0], cs[1], eps)}" if n == 2 else ""
                print(f"n={n}: A_{i + 1}: nodes {rules_on(cs, eps)}{extra}", flush=True)
            p = HALF + Fr(1, 50)
            Rp = tiefree_R(n, eps, r0, sL, sR, p)
            FRp, yRp, wRp = Rp.node(Fr(0), Fr(1))
            FN = N.F(Fr(0), Fr(1))
            margins = [Rp.F(Fr(0), p) + (n - 1) * FN + eps, Rp.F(p, Fr(1)) + (n - 1) * FN + eps]
            minRp = min(Rp.m(t) for t in Rp.x)
            print(f"n={n}: tie-free R': convex {Rp.is_convex()}, root minimizer {yRp}, value {FRp} (= -c: "
                  f"{FRp == -(QUART - r0)}), w {wRp} < 1/4, cut-at-p child margins {margins}, "
                  f"min R' + (n-1) min N = {minRp + (n - 1) * min(N.m(t) for t in N.x)}", flush=True)
            for i in range(n):
                cs = [N] * n
                cs[i] = Rp
                print(f"n={n}: tie-free A'_{i + 1}: nodes {rules_on(cs, eps)} (2^(n+1)-1 = {2 ** (n + 1) - 1})", flush=True)
