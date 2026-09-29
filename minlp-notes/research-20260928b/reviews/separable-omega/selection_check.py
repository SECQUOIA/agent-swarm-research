"""Minimizer selection on flat minimizer sets (review check).

The note (Section 1.1) says the computations take 'among the minimizers, the one with the
largest w, then the leftmost'.  The author's code (sepexact.Coord.node) compares only knots and
endpoints.  They differ when phi_J is constant on a whole segment, e.g. on every cell of the
dyadic caps g (phi_{C_k} = 0 on C_k) and of the 'caps' family.  An interior-point solver would
return the centre of such a segment.  This script compares
  knots  (author's code), wmax (the stated rule), center (IPM-like), left, right
on g + g (Proposition D) and on caps(k/7) x quad(29/70) (Section 7.1), with OPT_min computed
under the same selection, and a product upper bound on N_guill for g + g.
usage: python3 selection_check.py
"""
from fractions import Fraction as Fr
from sepcore import PL, dyadic_caps, run, opt_min2


def quad_knots(a, g=1, L=0, U=1, rmin=Fr(1, 10 ** 8), ratio=Fr(5, 4), sel="wmax"):
    """knot interpolant of H for m = g (t - a)^2 (same knot rule as the author's fam.quad)."""
    a, g, L, U = Fr(a), Fr(g), Fr(L), Fr(U)
    pts = {L, U, a}
    r = max(a - L, U - a)
    while r > rmin:
        for p in (a - r, a + r):
            if L < p < U:
                pts.add(p)
        r = r / ratio
        r = Fr(r.numerator, r.denominator).limit_denominator(10 ** 12)
    xs = sorted(pts)
    return PL.from_m(xs, [g * (x - a) ** 2 for x in xs], sel)


def caps7(sel):
    xs = [Fr(k, 7) for k in range(8)]
    return PL.from_m(xs, [0] * 8, sel)


def prod_bound(c, eps, splits=16):
    best = None
    for k in range(1, splits):
        e1 = eps * Fr(k, splits)
        v = c.ncert(e1) * c.ncert(eps - e1)
        best = v if best is None else min(best, v)
    return best


if __name__ == "__main__":
    sels = ("knots", "wmax", "center", "left", "right")
    print("g + g: omega leaves by selection; product upper bound on N_guill (16 budget splits)")
    for k in range(3, 11):
        eps = Fr(1, 10 ** k)
        row = {s: run([dyadic_caps(60, s), dyadic_caps(60, s)], eps, "omega")["leaves"] for s in sels}
        pb = prod_bound(dyadic_caps(60), eps)
        om = {}
        if k <= 6:
            for s in ("knots", "center"):
                om[s] = opt_min2(dyadic_caps(60, s), dyadic_caps(60, s), eps)
        print(f"  eps=1e-{k}: {row}; center/knots = {row['center'] / row['knots']:.2f}; product bound {pb}; "
              f"OPT_min {om}", flush=True)
    print("caps(k/7) x quad(29/70): omega leaves and OPT_min by selection")
    for k in range(3, 7):
        eps = Fr(1, 10 ** k)
        out = []
        for s in ("knots", "wmax", "center"):
            c1, c2 = caps7(s), quad_knots(Fr(29, 70), sel=s)
            out.append(f"{s}: omega {run([c1, c2], eps, 'omega')['leaves']} OPT_min {opt_min2(c1, c2, eps)}")
        print(f"  eps=1e-{k}: " + "; ".join(out), flush=True)
