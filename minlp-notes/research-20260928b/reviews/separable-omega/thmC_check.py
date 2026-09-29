"""Review check of Theorem C (coordinate-ambiguity lower bound, every I1 rule, n >= 2).

Instances (note, Section 6), alpha = 1, eps = 1/100, c := 1/4 - r0:
  sL, sR = 1 -+ eps/(4(n-1));  phi = (n-1)(1/4 - r0) - eps/2
  lL(t) = r0 + 1/4 + sL (t - 1/2),  lR(t) = r0 + 1/4 + sR (t - 1/2)
  H_R = max(lL, lR, t/2 + phi, 3t/2 - 1/2 + phi),  H_N = max(lL, lR, t/2 - phi', 3t/2 - 1/2 - phi'),
  phi' = phi/(n-1);  m = H - t^2;  A_i uses R in coordinate i and N elsewhere.

Part 1 (sympy): the conditions the proof needs, as functions of (n, c, eps), and the interval of
  admissible c.  Part 2 (exact, Fractions): every item for n = 2..40 with r0 = 1/4 - 1/(5n)
  (= 3/20 at n = 2, the note's value) and for the author's script choice
  r0 = (n-1)/(4n) + 1/50 (n >= 3), which fails for n >= 12.  Part 3: information model:
  equality of f near the centre and near every corner, inequality near facet centres.
  Part 4: omega / deficit / OPT_min on A_1, A_2 (n = 2, 3), both tie orders and selections.
"""
import itertools
import sympy as sp
from fractions import Fraction as Fr
from sepcore import PL, run, opt_min2

EPS = Fr(1, 100)
H2, Q4 = Fr(1, 2), Fr(1, 4)


def lines(n, eps, r0):
    sL, sR = 1 - eps / (4 * (n - 1)), 1 + eps / (4 * (n - 1))
    phi = (n - 1) * (Q4 - r0) - eps / 2
    ph2 = phi / (n - 1)
    common = [(sL, r0 + Q4 - H2 * sL), (sR, r0 + Q4 - H2 * sR)]
    R = common + [(H2, phi), (Fr(3, 2), phi - H2)]
    N = common + [(H2, -ph2), (Fr(3, 2), -ph2 - H2)]
    return R, N, phi


def active(lines_, t):
    v = [a * t + b for a, b in lines_]
    mx = max(v)
    return {k for k in range(4) if v[k] == mx}


def region(lines_, want, around):
    """maximal interval around `around` on which the max is attained only by lines in `want`
    (exact, from envelope kinks)."""
    c = PL.from_lines(lines_)
    xs = c.x
    # H is linear between knots; on each open cell the active set is constant
    cells = []
    for k in range(len(xs) - 1):
        mid = (xs[k] + xs[k + 1]) / 2
        cells.append((xs[k], xs[k + 1], active(lines_, mid) <= want))
    k0 = max(k for k in range(len(cells)) if cells[k][0] <= around)
    if around == cells[k0][0] and k0 > 0 and around != xs[0]:
        pass
    lo = k0
    while lo > 0 and cells[lo - 1][2] and cells[lo][2]:
        lo -= 1
    hi = k0
    while hi < len(cells) - 1 and cells[hi + 1][2] and cells[hi][2]:
        hi += 1
    if not cells[k0][2]:
        return None
    return cells[lo][0], cells[hi][1]


def exact_checks(n, r0, verbose=True):
    eps = EPS
    LR, LN, phi = lines(n, eps, r0)
    R, N = PL.from_lines(LR), PL.from_lines(LN)
    out = {}
    out["convex"] = R.convex() and N.convex()
    FR, yR, wR = R.node(Fr(0), Fr(1))
    FN, yN, wN = N.node(Fr(0), Fr(1))
    # uniqueness of the root minimizer: every other candidate strictly larger
    def unique(c, F, y):
        i = [k for k in range(len(c.x)) if c.Hk[k] - c.x[k] == F]
        return len(i) == 1 and c.x[i[0]] == y
    out["root minimizers"] = (yR, yN, unique(R, FR, yR) and unique(N, FN, yN))
    out["F_R(root) == F_N(root)"] = FR == FN
    minR, minN = min(R.m(t) for t in R.x), min(N.m(t) for t in N.x)
    out["min m_R + (n-1) min m_N"] = minR + (n - 1) * minN
    root = FR + (n - 1) * FN
    out["root value + eps (<0 invalid)"] = root + eps
    right = [R.node(Fr(0), H2)[0] + (n - 1) * FN + eps, R.node(H2, Fr(1))[0] + (n - 1) * FN + eps]
    out["right-cut child margins (>=0 valid)"] = right
    # wrong cut of an N coordinate at any point: child value <= max(m_N(0), m_N(1)) (endpoint);
    # sup over cut points of F_N([0,y]) and F_N([y,1]) is that bound (y -> 0 or 1).
    bound = max(N.m(Fr(0)), N.m(Fr(1))) + FR + (n - 2) * FN + eps
    out["wrong-cut analytic bound (<0 invalid)"] = bound
    # exact sweep over cut points: all knots of N and a fine rational grid
    ys = sorted(set(N.x[1:-1]) | {Fr(k, 997) for k in range(1, 997)})
    worst = max(max(N.node(Fr(0), y)[0], N.node(y, Fr(1))[0]) for y in ys)
    out["wrong-cut sweep max (<0 invalid)"] = worst + FR + (n - 2) * FN + eps
    # agreement neighbourhoods
    cen = (region(LR, {0, 1}, H2), region(LN, {0, 1}, H2))
    out["R=N near 1/2 on"] = (max(cen[0][0], cen[1][0]), min(cen[0][1], cen[1][1])) if None not in cen else None
    left = (region(LR, {2}, Fr(0)), region(LN, {2}, Fr(0)))
    rightr = (region(LR, {3}, Fr(1) - Fr(1, 10 ** 9)), region(LN, {3}, Fr(1) - Fr(1, 10 ** 9)))
    out["R-N const near 0 on [0,a], a="] = min(left[0][1], left[1][1]) if None not in left else None
    out["R-N const near 1 on [b,1], b="] = max(rightr[0][0], rightr[1][0]) if None not in rightr else None
    ok = (out["convex"] and out["root minimizers"][2] and out["root minimizers"][:2] == (H2, H2)
          and out["F_R(root) == F_N(root)"] and out["min m_R + (n-1) min m_N"] == 0
          and out["root value + eps (<0 invalid)"] < 0 and min(right) >= 0 and bound < 0
          and out["wrong-cut sweep max (<0 invalid)"] < 0 and out["R=N near 1/2 on"] is not None
          and out["R=N near 1/2 on"][0] < H2 < out["R=N near 1/2 on"][1]
          and out["R-N const near 0 on [0,a], a="] and out["R-N const near 1 on [b,1], b="])
    return ok, out, (R, N)


def symbolic():
    n, c, e, t = sp.symbols("n c eps t", positive=True)
    r0 = sp.Rational(1, 4) - c
    phi = (n - 1) * c - e / 2
    sL, sR = 1 - e / (4 * (n - 1)), 1 + e / (4 * (n - 1))
    lL = lambda s: r0 + sp.Rational(1, 4) + sL * (s - sp.Rational(1, 2))
    lR = lambda s: r0 + sp.Rational(1, 4) + sR * (s - sp.Rational(1, 2))
    ph2 = phi / (n - 1)
    conds = {
        "(1) lL,lR beat R's lines at 1/2: r0 - phi > 0": sp.simplify(r0 - phi),
        "(2) lL,lR beat N's lines at 1/2: r0 + phi' > 0": sp.simplify(r0 + ph2),
        "(3) root invalid: n c - eps > 0": n * c - e,
        "(4) N's own line dominates at 0: -phi' - lL(0) > 0": sp.simplify(-ph2 - lL(0)),
        "(4') and -phi' - lR(0) > 0": sp.simplify(-ph2 - lR(0)),
        "(5) wrong cut invalid: -(m_N(0) - (n-1)c + eps) > 0": sp.simplify(-(-ph2 - (n - 1) * c + e)),
        "(6) right cut valid: phi - (n-1)c + eps >= 0": sp.simplify(phi - (n - 1) * c + e),
        "(7) R's line dominates at 0: phi - lL(0) > 0": sp.simplify(phi - lL(0)),
    }
    for k, v in conds.items():
        print(f"  {k}:  {sp.factor(v)}")
    lo = sp.solve(sp.Eq(conds["(5) wrong cut invalid: -(m_N(0) - (n-1)c + eps) > 0"], 0), c)[0]
    hi = sp.solve(sp.Eq(conds["(1) lL,lR beat R's lines at 1/2: r0 - phi > 0"], 0), c)[0]
    print(f"  admissible c: {sp.factor(lo)} < c < {sp.factor(hi)}  (also c > eps/n from (3))")
    gap = sp.factor(sp.simplify(hi - lo))
    print(f"  hi - lo = {gap}   (> 0 iff eps < (n-1)/(2n))")
    # choice c = 1/(5n): check (1)-(7) symbolically for n >= 2 and eps = 1/100
    cs = 1 / (5 * n)
    print("  choice c = 1/(5n), eps = 1/100 (so r0 = 1/4 - 1/(5n), = 3/20 at n = 2):")
    for k, v in conds.items():
        expr = sp.factor(sp.simplify(v.subs({c: cs, e: sp.Rational(1, 100)})))
        # numerator/denominator sign for n >= 2
        num, den = sp.fraction(sp.together(expr))
        m = sp.symbols("m", nonnegative=True)
        numm = sp.expand(num.subs(n, m + 2))
        denm = sp.expand(den.subs(n, m + 2))
        pos = all(co >= 0 for co in sp.Poly(numm, m).coeffs()) and sp.Poly(numm, m).coeffs()[-1] > 0 \
            if numm != 0 else False
        posd = all(co >= 0 for co in sp.Poly(denm, m).coeffs()) and sp.Poly(denm, m).coeffs()[-1] > 0
        tag = "positive for all n >= 2" if pos and posd else ("== 0? " + str(numm == 0))
        if k.startswith("(6)"):
            tag = f"= {sp.simplify(expr)} (>= 0)"
        print(f"    {k}: {expr}  -> {tag}")


def info_model(n, r0):
    LR, LN, _ = lines(n, EPS, r0)
    R, N = PL.from_lines(LR), PL.from_lines(LN)

    def f(i, y):   # f - f* = sum m (instance A_i, 0-based)
        return sum((R if k == i else N).m(y[k]) for k in range(n))
    d = Fr(1, 10 ** 4)
    near_c = all(f(0, y) == f(1, y) for y in itertools.product([H2 - d, H2, H2 + d], repeat=n))
    corners = all(f(0, tuple(v + s * d for v, s in zip(cn, sg))) == f(1, tuple(v + s * d for v, s in zip(cn, sg)))
                  for cn in itertools.product([Fr(0), Fr(1)], repeat=n)
                  for sg in [tuple(1 if v == 0 else -1 for v in cn)] for d in (Fr(0), Fr(1, 10 ** 4)))
    facet = (Fr(0),) + (H2,) * (n - 1)
    return near_c, corners, f(0, facet) - f(1, facet)


if __name__ == "__main__":
    print("Part 1: symbolic conditions")
    symbolic()
    print("\nPart 2: exact checks")
    bad = []
    for n in range(2, 41):
        r0 = Fr(1, 4) - Fr(1, 5 * n)
        ok, out, _ = exact_checks(n, r0)
        if n in (2, 3, 4, 6, 12, 40):
            print(f" n={n} r0=1/4-1/(5n)={r0}:")
            for k, v in out.items():
                print(f"    {k}: {v}")
        if not ok:
            bad.append(n)
    print(f" r0 = 1/4 - 1/(5n): all items hold for n = 2..40 except {bad}")
    fails = []
    for n in range(3, 15):
        r0 = Fr(n - 1, 4 * n) + Fr(1, 50)
        ok, out, _ = exact_checks(n, r0)
        if not ok:
            fails.append((n, out["root value + eps (<0 invalid)"], out["wrong-cut analytic bound (<0 invalid)"]))
    print(" author's script choice r0 = (n-1)/(4n) + 1/50 fails at (n, root+eps, wrong-cut bound):")
    for fl in fails:
        print("    ", fl)
    ok4 = exact_checks(4, Fr(3, 16) + Fr(1, 50))[1]
    print(" author's r0 at n=4 (cross-check with lb_coord.log):", ok4["root value + eps (<0 invalid)"] - EPS,
          ok4["wrong-cut sweep max (<0 invalid)"])
    print("\nPart 3: information model (A_1 vs A_2)")
    for n in (2, 3, 4):
        r0 = Fr(1, 4) - Fr(1, 5 * n)
        nc, co, fd = info_model(n, r0)
        print(f" n={n}: equal near centre {nc}; equal at/near every corner {co}; "
              f"f(A_1) - f(A_2) at facet centre (0,1/2,..) = {fd}")
    print("\nPart 4: rules on the instances")
    for n in (2, 3):
        r0 = Fr(1, 4) - Fr(1, 5 * n)
        LR, LN, _ = lines(n, EPS, r0)
        for sel in ("wmax", "left", "right"):
            R, N = PL.from_lines(LR, sel=sel), PL.from_lines(LN, sel=sel)
            row = []
            for i in (0, 1):
                cs = [N] * n
                cs[i] = R
                for rule in ("omega", "deficit"):
                    for tie in ("low", "high"):
                        row.append(f"A_{i+1} {rule}/{tie}={run(cs, EPS, rule, tie)['nodes']}")
                if n == 2:
                    row.append(f"A_{i+1} OPT_min leaves={opt_min2(cs[0], cs[1], EPS)}")
            print(f" n={n} sel={sel}: " + ", ".join(row))
