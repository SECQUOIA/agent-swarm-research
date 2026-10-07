"""Reviewer's independent re-verification of the box certificates of Theorems B2(1) and B3.

Written from the note's statement of the reduction, not from verify_zB.py.  Differences from the
author's verifier:
  * test points are built here from the note's formulas;
  * every certificate is checked at all 8 vertices of the box (no sign-pattern shortcut);
  * the 'psi' certificate is checked against the exact maximum of Psi over the box (Psi is bilinear in
    (x11, x22) for fixed x21 and concave in x21), not against an interval bound;
  * coverage is checked geometrically: the box volumes of each facet sum exactly to 8 and the boxes
    are pairwise interior-disjoint (pairwise test in numpy on exact dyadic float64 endpoints).
The only shared convention is the bisection rule used to decode a path into a box (split the free
coordinate with the longest edge, ties to the lowest index in the order x11, x12, x21, x22).

usage: python3 indep_verify_boxes.py FILE.jsonl.gz RHO FAMILY     (FAMILY = B or tan:ETA:K)
"""
import sys, json, gzip
from fractions import Fraction as Fr
import numpy as np

ORDER = [(0, 0), (0, 1), (1, 0), (1, 1)]


def points(rho, fam):
    one = Fr(1)
    sb = (Fr(0), Fr(0), one)
    if fam == 'B':
        P1 = (rho, -rho, one)
        P2 = (rho, -2 * rho, one)
    else:
        _, eta, k = fam.split(':')
        eta, k = Fr(eta), Fr(k)
        # exact rational square root of k
        from math import isqrt
        a, b = k.numerator, k.denominator
        ra, rb = isqrt(a), isqrt(b)
        assert ra * ra == a and rb * rb == b
        sk = Fr(ra, rb)
        P1 = (rho, -rho, 1 - 2 * rho * (1 - eta))
        P2 = (rho, -k * rho, 1 - 2 * sk * rho * (1 - eta))
    mid = lambda p, q: tuple((p[i] + q[i]) / 2 for i in range(3))
    return [sb, P1, P2, mid(sb, P1), mid(sb, P2), mid(P1, P2)]


def decode(facet, path):
    fi, fj, fs = facet
    lo = {ij: Fr(-1) for ij in ORDER}
    hi = {ij: Fr(1) for ij in ORDER}
    lo[(fi, fj)] = hi[(fi, fj)] = Fr(fs)
    free = [ij for ij in ORDER if ij != (fi, fj)]
    for ch in path:
        best = None
        for ij in free:  # longest edge, first in ORDER on ties
            L = hi[ij] - lo[ij]
            if best is None or L > best[0]:
                best = (L, ij)
        ij = best[1]
        m = (lo[ij] + hi[ij]) / 2
        if ch == '0':
            hi[ij] = m
        elif ch == '1':
            lo[ij] = m
        else:
            raise ValueError(ch)
    return lo, hi


def vertices(lo, hi):
    for a in (lo[(0, 0)], hi[(0, 0)]):
        for b in (lo[(0, 1)], hi[(0, 1)]):
            for c in (lo[(1, 0)], hi[(1, 0)]):
                for d in (lo[(1, 1)], hi[(1, 1)]):
                    yield a, b, c, d


def quad(X, s, v):
    """v^T X M(s) v with M(x, y, w) = [[w, x], [y, 1]]."""
    x11, x12, x21, x22 = X
    x, y, w = s
    # X M = [[x11 w + x12 y, x11 x + x12], [x21 w + x22 y, x21 x + x22]]
    A = x11 * w + x12 * y
    B = x11 * x + x12
    C = x21 * w + x22 * y
    D = x21 * x + x22
    return v[0] * v[0] * A + v[0] * v[1] * (B + C) + v[1] * v[1] * D


def psi_max(lo, hi, rho):
    best = None
    for x11 in (lo[(0, 0)], hi[(0, 0)]):
        for x22 in (lo[(1, 1)], hi[(1, 1)]):
            a = rho * (x11 - x22)
            b = x11 * x22
            l, h = lo[(1, 0)], hi[(1, 0)]
            t = a / (2 * rho * rho)
            t = min(max(t, l), h)
            val = a * t + b - rho * rho * t * t
            best = val if best is None or val > best else best
    return best


def main(fname, rho, fam):
    rho = Fr(rho)
    pts = points(rho, fam)
    qs = [s[2] - s[0] * s[1] for s in pts]
    assert all(q > 0 for q in qs), qs
    blocks, cur = {}, {}
    for line in gzip.open(fname, 'rt'):
        d = json.loads(line)
        if 'facet_start' in d:
            assert Fr(str(d['rho'])) == rho or Fr(d['rho']) == rho
            cur[tuple(d['facet_start'])] = []
        elif 'facet_done' in d:
            blocks[tuple(d['facet'])] = cur.pop(tuple(d['facet']))
        elif 'cert' in d:
            cur[tuple(d['facet'])].append(d)
    facets = [(i, j, s) for i in range(2) for j in range(2) for s in (1, -1)]
    ok = True
    counts = {}
    for f in facets:
        if f not in blocks:
            print('MISSING facet', f); ok = False; continue
        leaves = blocks[f]
        boxes = []
        vol = Fr(0)
        for d in leaves:
            lo, hi = decode(f, d['path'])
            free = [ij for ij in ORDER if ij != (f[0], f[1])]
            v = Fr(1)
            for ij in free:
                v *= hi[ij] - lo[ij]
            vol += v
            boxes.append([lo[ij] for ij in free] + [hi[ij] for ij in free])
            c = d['cert']
            counts[c] = counts.get(c, 0) + 1
            if c == 'det':
                good = all(a * dd - b * cc < 0 for a, b, cc, dd in vertices(lo, hi))
            elif c == 'a22':
                good = all(rho * cc + dd < 0 for a, b, cc, dd in vertices(lo, hi))
            elif c == 'psi':
                good = psi_max(lo, hi, rho) < 0
            elif c == 'pt':
                k, (v0, v1) = d['data']
                vv = (Fr(v0), Fr(v1))
                s = pts[k]
                foot = (s[0], s[1], s[2] - qs[k])
                good = all(quad(X, s, vv) < 0 and quad(X, foot, vv) < 0 for X in vertices(lo, hi))
            else:
                good = False
            if not good:
                print('LEAF FAIL', f, d); ok = False
        if vol != 8:
            print('facet', f, 'volume', vol, '!= 8'); ok = False
        # pairwise interior-disjointness
        arr = np.array([[float(t) for t in b] for b in boxes])
        for b, row in zip(boxes, arr):
            assert all(Fr(float(t)) == t for t in b)
        n = len(arr)
        lo_, hi_ = arr[:, :3], arr[:, 3:]
        bad = 0
        CH = 128
        for i0 in range(0, n, CH):
            L = lo_[i0:i0 + CH, None, :]
            H = hi_[i0:i0 + CH, None, :]
            ov = np.all((np.minimum(H, hi_[None, :, :]) - np.maximum(L, lo_[None, :, :])) > 0, axis=2)
            idx = np.arange(i0, min(i0 + CH, n))
            ov[np.arange(len(idx)), idx] = False
            bad += int(ov.sum())
        if bad:
            print('facet', f, 'overlapping pairs', bad // 2); ok = False
        print('facet', f, 'leaves', n, 'volume', vol, 'overlaps', bad // 2, flush=True)
    print(fname, 'family', fam, 'rho', rho, counts, 'total', sum(counts.values()))
    print('INDEPENDENT CHECK PASS' if ok else 'INDEPENDENT CHECK FAIL', flush=True)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
