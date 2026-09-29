"""Reviewer check of Lemma 0 with OBBT in 2D (independent code).

Separable exact alphaBB: f = h1(y1) + h2(y2), f_B = sum_i (h_i - alpha a_i^B).
OBBT on node B with cutoff c = f* - eps: the projection of {y in B : f_B(y) <= c}
onto coordinate i is {t : phi_i(t) <= c - sum_{j != i} min phi_j}, a 1D
sublevel set of a convex function.  OBBT is iterated (relaxation rebuilt on the
reduced box) while it shrinks the box.  Each round's frame B_k minus B_{k+1}
is split into 2n boxes.  Then widest-side bisection.

Checks:
  * every leaf and every removed piece satisfies (V) (exact separable test);
  * the family covers [0,1]^2 with disjoint interiors (area sum = 1);
  * |P| >= Theorem B bound, and |P| <= (2n+1) * (#relaxation solves);
  * merging the frames of several rounds of one node into a single frame
    (decomposing B_0 minus B_final directly) can break (V).
"""
import math
import numpy as np
from numpy.polynomial import Polynomial as Poly
from scipy import integrate

import thm_b_1d as T
from bisection_checks import sep_instance


def phi_poly(F, alpha, l, u):
    (lo, hi, p), = F.pieces
    return p + Poly([alpha * l * u, -alpha * (l + u), alpha])


def min_on(p, l, u):
    c = [l, u] + [r.real for r in p.deriv().roots() if abs(r.imag) < 1e-12 and l < r.real < u]
    vals = [p(t) for t in c]
    k = int(np.argmin(vals))
    return vals[k], c[k]


def sublevel(p, l, u, level):
    """Interval {t in [l,u] : p(t) <= level} for convex p on [l,u], or None."""
    v, t0 = min_on(p, l, u)
    if v > level:
        return None
    def root(lo, hi, inside_hi):
        for _ in range(200):
            m = 0.5 * (lo + hi)
            if (p(m) <= level) == inside_hi:
                hi = m
            else:
                lo = m
        return lo, hi
    left = l if p(l) <= level else root(l, t0, True)[1]
    right = u if p(u) <= level else root(t0, u, False)[0]
    return left, right


def frame_pieces(B, Bp):
    """Split B minus int(Bp) into at most 2n boxes (Bp subset of B)."""
    pieces, n = [], len(B)
    for i in range(n):
        for side in (0, 1):
            box = []
            ok = True
            for j in range(n):
                if j < i:
                    box.append(Bp[j])
                elif j == i:
                    seg = (B[i][0], Bp[i][0]) if side == 0 else (Bp[i][1], B[i][1])
                    if seg[1] - seg[0] <= 0:
                        ok = False
                    box.append(seg)
                else:
                    box.append(B[j])
            if ok:
                pieces.append(tuple(box))
    return pieces


def valid_V(Fs, fstar, alpha, eps, C):
    tot = sum(min_on(phi_poly(F, alpha, l, u), l, u)[0] for F, (l, u) in zip(Fs, C))
    return tot - fstar + eps >= -1e-12


def run(Fs, alpha, eps, obbt=True, rounds=20):
    fstars = [T.fmin(F)[0] for F in Fs]
    fstar = sum(fstars)
    c = fstar - eps
    stack = [((0.0, 1.0), (0.0, 1.0))]
    fam, relax, merged_bad, merged_tested = [], 0, 0, 0
    while stack:
        B0 = stack.pop()
        B = B0
        pruned = False
        nround = 0
        round_pieces = []
        for _ in range(rounds if obbt else 1):
            relax += 1
            ps = [phi_poly(F, alpha, l, u) for F, (l, u) in zip(Fs, B)]
            mins = [min_on(p, l, u)[0] for p, (l, u) in zip(ps, B)]
            if sum(mins) > c:
                pruned = True
                break
            if not obbt:
                break
            newB = []
            for i, (p, (l, u)) in enumerate(zip(ps, B)):
                iv = sublevel(p, l, u, c - (sum(mins) - mins[i]))
                newB.append(iv)
            newB = tuple(newB)
            pcs = frame_pieces(B, newB)
            round_pieces += pcs
            nround += 1
            shrink = np.prod([u - l for l, u in newB]) < 0.99 * np.prod([u - l for l, u in B])
            B = newB
            if not shrink:
                break
        fam += round_pieces
        if nround >= 2:
            for S in frame_pieces(B0, B):
                merged_tested += 1
                if not valid_V(Fs, fstar, alpha, eps, S):
                    merged_bad += 1
        if pruned:
            fam.append(B)
            continue
        w = [u - l for l, u in B]
        i = int(np.argmax(w))
        s = 0.5 * (B[i][0] + B[i][1])
        b1, b2 = list(B), list(B)
        b1[i] = (B[i][0], s)
        b2[i] = (s, B[i][1])
        stack += [tuple(b1), tuple(b2)]
    return fam, relax, merged_bad, merged_tested


if __name__ == "__main__":
    for kind in ("nondeg", "mixed"):
        Fs, alpha, cpt = sep_instance(kind)
        fstar = sum(T.fmin(F)[0] for F in Fs)
        print(f"== 2D separable {kind}, alpha={alpha:.4g}")
        for eps in (1e-2, 1e-4, 1e-6):
            g = lambda y2, y1: 1.0 / (Fs[0](y1) + Fs[1](y2) - fstar + eps)
            I, _ = integrate.nquad(g, [[0, 1], [0, 1]],
                                   opts=[{"points": [cpt[1]], "limit": 200}, {"points": [cpt[0]], "limit": 200}])
            thmB = (2 * alpha / math.pi ** 2) * I
            for obbt in (False, True):
                fam, relax, bad, tested = run(Fs, alpha, eps, obbt)
                area = sum((C[0][1] - C[0][0]) * (C[1][1] - C[1][0]) for C in fam)
                nV = sum(valid_V(Fs, fstar, alpha, eps, C) for C in fam)
                print(f"  eps={eps:.0e} obbt={obbt!s:5s} |P|={len(fam):5d} relaxations={relax:5d} (V) holds on {nV}/{len(fam)} "
                      f"area={area:.12f} ThmB={thmB:.2f} |P|/ThmB={len(fam)/thmB:.2f} |P|/relax={len(fam)/relax:.2f}"
                      + (f"  merged-frame pieces violating (V): {bad}/{tested}" if obbt else ""))
