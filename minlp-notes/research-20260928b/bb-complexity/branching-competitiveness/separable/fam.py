"""Coordinate families (exact knot instances, alpha = 1) and grid helpers."""
from fractions import Fraction as Fr
from sepexact import Coord


def sharp(a, s=2, L=0, U=1):
    """m = s|t-a| - (t-a)^2 (exact; H = s|t-a| + 2at - a^2); needs s >= max distance to a."""
    a, s, L, U = Fr(a), Fr(s), Fr(L), Fr(U)
    xs = [L, a, U] if L < a < U else [L, U]
    return Coord.from_m(xs, [s * abs(x - a) - (x - a) ** 2 for x in xs])


def quad(a, g=1, L=0, U=1, rmin=Fr(1, 10 ** 7), ratio=Fr(5, 4), extra=()):
    """knot interpolant of H for m = g (t-a)^2: geometric knots around a (ratio), down to rmin."""
    a, g, L, U = Fr(a), Fr(g), Fr(L), Fr(U)
    pts = {L, U, a} | {Fr(e) for e in extra}
    r = max(a - L, U - a)
    while r > rmin:
        for p in (a - r, a + r):
            if L < p < U:
                pts.add(p)
        r = r / ratio
        r = Fr(r.numerator, r.denominator).limit_denominator(10 ** 12)
    xs = sorted(pts)
    return Coord.from_m(xs, [g * (x - a) ** 2 for x in xs])


def caps(breaks, L=0, U=1, lift=None):
    """sawtooth of caps: m = (t-s_k)(s_{k+1}-t) on each cell (H linear on cells), m = 0 at breaks.
    lift: optional dict break -> extra height (keeps H piecewise linear; convexity not checked)."""
    xs = sorted({Fr(L), Fr(U)} | {Fr(b) for b in breaks})
    ms = [Fr(0)] * len(xs)
    if lift:
        ms = [Fr(lift.get(x, 0)) for x in xs]
    return Coord.from_m(xs, ms, shift=False)


def from_fun(fun, xs):
    xs = sorted({Fr(x) for x in xs})
    return Coord.from_m(xs, [Fr(fun(x)) for x in xs])


def thin(pts, G):
    """keep at most G points (always keep ends), evenly by index."""
    pts = sorted(set(pts))
    if len(pts) <= G:
        return pts
    idx = sorted({round(i * (len(pts) - 1) / (G - 1)) for i in range(G)})
    return [pts[i] for i in idx]


def cut_positions(res, n=2):
    cuts = [set() for _ in range(n)]
    for box, y, i, ph in res["internal"]:
        cuts[i].add(y[i])
    return cuts


def greedy_multi(c, eps, K=12, both=True):
    """breakpoints of left-greedy 1D certificates at budgets eps*2^k, k=0..K (and right-greedy)."""
    pts = set()
    b = Fr(eps)
    for k in range(K + 1):
        pts |= set(c.greedy(b))
        if both:
            # right greedy via reflection
            rc = Coord([-x for x in reversed(c.x)], [h for h in reversed(c.H)], shift=False)
            pts |= {-p for p in rc.greedy(b)}
        b *= 2
    return pts
