"""Scope check for the bound-tightening corollary (reviewer script).

Standard solvers propagate the objective cutoff f(y) <= c through the
expression graph with interval arithmetic.  This removes feasible points using
information other than the (G_alpha) relaxation, so Lemma 0 does not apply.
Instance: f = t^2 - 2 t^4, t = y - 1/3, y in [0,1] (the scout's nondeg1),
f* = 0, exact alphaBB with alpha = 13/3.  DAG: u = t^2, v = u^2, f = u - 2 v.

Run: node = root; FBBT to a fixed point on u - 2v <= c; if empty, prune; else
alphaBB bound on the contracted box; prune if bound >= f* - eps; else bisect.
Report relaxations/nodes and compare with the Theorem B lower bound (valid
only without cutoff propagation).
"""
import math
import thm_b_1d as T
from bisection_checks import lb_box
from numpy.polynomial import Polynomial as Poly

A = 1.0 / 3.0
ALPHA = 13.0 / 3.0


def sq_range(lo, hi):
    if lo <= 0 <= hi:
        return 0.0, max(lo * lo, hi * hi)
    return min(lo * lo, hi * hi), max(lo * lo, hi * hi)


def fbbt(tl, th, c, max_rounds=200):
    rounds = 0
    while rounds < max_rounds:
        rounds += 1
        ul, uh = sq_range(tl, th)
        vl, vh = ul * ul, uh * uh
        # backward on u - 2 v <= c
        uh2 = min(uh, c + 2 * vh)
        vl2 = max(vl, (ul - c) / 2)
        if uh2 < ul or vl2 > vh:
            return None, rounds
        # v = u^2 with u >= 0
        ul2 = max(ul, math.sqrt(max(vl2, 0.0)))
        uh2 = min(uh2, math.sqrt(vh))
        if uh2 < ul2:
            return None, rounds
        # u = t^2
        r = math.sqrt(uh2)
        ntl, nth = max(tl, -r), min(th, r)
        if ul2 > 0:
            s = math.sqrt(ul2)
            if ntl > -s and nth < s:
                return None, rounds
            if ntl > -s:
                ntl = max(ntl, s)
            if nth < s:
                nth = min(nth, -s)
        if ntl > nth:
            return None, rounds
        if (nth - ntl) >= 0.999 * (th - tl):
            return (ntl, nth), rounds
        tl, th = ntl, nth
    return (tl, th), rounds


def run(eps, cutoff):
    F, _ = T.poly_instance([0, 0, 1, 0, -2], A)
    stack, nodes, fb_rounds, relax = [(-A, 1 - A)], 0, 0, 0
    while stack:
        tl, th = stack.pop()
        nodes += 1
        box, r = fbbt(tl, th, cutoff)
        fb_rounds += r
        if box is None:
            continue
        tl, th = box
        relax += 1
        if lb_box(F, ALPHA, tl + A, th + A) >= -eps:
            continue
        m = 0.5 * (tl + th)
        stack += [(tl, m), (m, th)]
    return nodes, relax, fb_rounds


if __name__ == "__main__":
    F, _ = T.poly_instance([0, 0, 1, 0, -2], A)
    for eps in (1e-2, 1e-5, 1e-8):
        thmB = T.bound(F, 0.0, ALPHA, eps, [A])
        a = run(eps, cutoff=-eps)
        b = run(eps, cutoff=0.0)
        print(f"eps={eps:.0e}: ThmB lower bound (no cutoff propagation) = {thmB:.2f} leaves; "
              f"cutoff f<=UBD-eps: nodes={a[0]}, relaxations={a[1]}, FBBT rounds={a[2]}; "
              f"cutoff f<=UBD: nodes={b[0]}, relaxations={b[1]}, FBBT rounds={b[2]}")
