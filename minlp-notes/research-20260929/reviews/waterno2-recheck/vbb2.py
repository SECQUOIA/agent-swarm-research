"""Faster variant of the first verifier's exact-rational B&B (../waterno2-verification/vbb.py).

Only bound propagation (FBBT) changes.  vbb.py propagates in exact Fraction
arithmetic, which takes about 90% of its run time.  Here propagation uses
float interval arithmetic with explicit outward rounding:

  * every decimal row coefficient a is enclosed as [fdn(a), fup(a)], every
    row side L, U as fdn(L), fup(U);
  * every float product or quotient p is widened to nextafter(p, -inf) /
    nextafter(p, +inf) (IEEE round-to-nearest leaves the exact value strictly
    inside);
  * sums use math.fsum, widened by two ulps (fsum is correctly rounded; two
    ulps also cover a one-ulp double-rounding error);
  * square roots use IEEE sqrt (correctly rounded) widened by one ulp;
  * cube / cube-root propagation stays exact (Fraction), as in vbb.py.

The relaxation rows, the node bound (exact Fraction evaluation of
min over the box of (c + A^T y) z - y.b), OBBT, branching and pruning are
vbb.py's code, unchanged.  A node is discarded only if (a) propagation proves
it empty, or (b) its exact bound is >= target.
Result: phi >= min(target, bounds of open nodes).
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import math
import sys
from fractions import Fraction as F

sys.path.insert(0, _RESEARCH + "/reviews/waterno2-verification")
import vbb  # noqa: E402

INF = math.inf
nextafter = math.nextafter
fsum = math.fsum


def DN(x):
    return nextafter(x, -INF)


def UP(x):
    return nextafter(x, INF)


def fdn(q):
    f = float(q)
    while F(f) > q:
        f = nextafter(f, -INF)
    return f


def fup(q):
    f = float(q)
    while F(f) < q:
        f = nextafter(f, INF)
    return f


def fin(x):
    return -INF < x < INF


class PeriodF(vbb.Period):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        fr = []
        for (cols, cf, L, U, nm) in self.rows:
            al = [fdn(a) for a in cf]
            ah = [fup(a) for a in cf]
            pos = [a > 0 for a in cf]
            for a, l_, h_, p in zip(cf, al, ah, pos):
                assert a != 0
                assert (0 < l_ <= a <= h_) if p else (l_ <= a <= h_ < 0)
            Llo = None if L is None else fdn(L)
            Uhi = None if U is None else fup(U)
            fr.append((cols, al, ah, pos, Llo, Uhi))
        self.frows = fr

    # ------------------------------------------------------------ rows
    def _rows(self, lo, hi):
        for (cols, al, ah, pos, Llo, Uhi) in self.frows:
            tl, th = [], []
            nli = nhi = 0
            for col, a1, a2, p in zip(cols, al, ah, pos):
                l, h = lo[col], hi[col]
                zl, zh = (l, h) if p else (h, l)   # z giving min / max of a*z
                if fin(zl):
                    u, v = a1 * zl, a2 * zl
                    tl.append(DN(u if u < v else v))
                else:
                    tl.append(None)
                    nli += 1
                if fin(zh):
                    u, v = a1 * zh, a2 * zh
                    th.append(UP(u if u > v else v))
                else:
                    th.append(None)
                    nhi += 1
            sl = DN(DN(fsum(x for x in tl if x is not None)))
            sh = UP(UP(fsum(x for x in th if x is not None)))
            if Uhi is not None and nli == 0 and sl > Uhi:
                return False
            if Llo is not None and nhi == 0 and sh < Llo:
                return False
            if (Uhi is None or nli > 1) and (Llo is None or nhi > 1):
                continue
            for k in range(len(cols)):
                col, a1, a2, p = cols[k], al[k], ah[k], pos[k]
                # rigorous lower / upper bounds on the sum of the other terms
                if tl[k] is None:
                    ol = sl if nli == 1 else None
                else:
                    ol = DN(sl - tl[k]) if nli == 0 else None
                if th[k] is None:
                    oh = sh if nhi == 1 else None
                else:
                    oh = UP(sh - th[k]) if nhi == 0 else None
                # a*z in [qlo, qhi]
                qlo = DN(Llo - oh) if (Llo is not None and oh is not None) else None
                qhi = UP(Uhi - ol) if (Uhi is not None and ol is not None) else None
                # a > 0: z >= qlo/a, z <= qhi/a;  a < 0: z >= qhi/a, z <= qlo/a.
                # a is only known to lie in [a1, a2] (same sign), so take the
                # extreme quotient over both ends, rounded outward.
                zlo, zhi = (qlo, qhi) if p else (qhi, qlo)
                if zlo is not None:
                    u, v = zlo / a1, zlo / a2
                    f = DN(u if u < v else v)
                    if f > lo[col]:
                        lo[col] = f
                if zhi is not None:
                    u, v = zhi / a1, zhi / a2
                    f = UP(u if u > v else v)
                    if f < hi[col]:
                        hi[col] = f
                if lo[col] > hi[col]:
                    return False
        return True

    # ------------------------------------------------------------ monomials
    def _mons(self, lo, hi):
        for (kind, x, y, w) in self.aux:
            if kind == "sq":
                l, h = lo[x], hi[x]
                if fin(l) and fin(h):
                    if l >= 0:
                        a, b = DN(l * l), UP(h * h)
                    elif h <= 0:
                        a, b = DN(h * h), UP(l * l)
                    else:
                        a, b = 0.0, UP(max(l * l, h * h))
                    if a > lo[w]:
                        lo[w] = a
                    if b < hi[w]:
                        hi[w] = b
                elif lo[w] < 0.0:
                    lo[w] = 0.0
                if lo[w] < 0.0:
                    lo[w] = 0.0
                if lo[w] > hi[w]:
                    return False
                if fin(hi[w]):
                    r = UP(math.sqrt(hi[w]))
                    if -r > lo[x]:
                        lo[x] = -r
                    if r < hi[x]:
                        hi[x] = r
                if lo[w] > 0:
                    s = DN(math.sqrt(lo[w]))
                    if lo[x] > -s:
                        if s > lo[x]:
                            lo[x] = s
                    elif hi[x] < s:
                        if -s < hi[x]:
                            hi[x] = -s
                if lo[x] > hi[x]:
                    return False
            elif kind == "cube":
                # exact, as in vbb.py
                l, h = lo[x], hi[x]
                if fin(l):
                    lo[w] = max(lo[w], fdn(F(l) ** 3))
                if fin(h):
                    hi[w] = min(hi[w], fup(F(h) ** 3))
                if lo[w] > hi[w]:
                    return False
                if fin(lo[w]):
                    lo[x] = max(lo[x], vbb.cbrt_dn(F(lo[w])))
                if fin(hi[w]):
                    hi[x] = min(hi[x], vbb.cbrt_up(F(hi[w])))
                if lo[x] > hi[x]:
                    return False
            else:
                lx, hx, ly, hy = lo[x], hi[x], lo[y], hi[y]
                if fin(lx) and fin(hx) and fin(ly) and fin(hy):
                    ps = (lx * ly, lx * hy, hx * ly, hx * hy)
                    a, b = DN(min(ps)), UP(max(ps))
                    if a > lo[w]:
                        lo[w] = a
                    if b < hi[w]:
                        hi[w] = b
                if lo[w] > hi[w]:
                    return False
                if fin(lo[w]) and fin(hi[w]):
                    Wl, Wh = lo[w], hi[w]
                    for (p_, q_) in ((x, y), (y, x)):
                        ql, qh = lo[q_], hi[q_]
                        if fin(ql) and fin(qh) and (ql > 0 or qh < 0):
                            cand = (Wl / ql, Wl / qh, Wh / ql, Wh / qh)
                            a, b = DN(min(cand)), UP(max(cand))
                            if a > lo[p_]:
                                lo[p_] = a
                            if b < hi[p_]:
                                hi[p_] = b
                            if lo[p_] > hi[p_]:
                                return False
        return True


solve = vbb.solve
