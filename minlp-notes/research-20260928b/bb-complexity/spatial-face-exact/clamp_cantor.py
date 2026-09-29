"""Revision after review: clamped relaxation-point splitting on the kink family (Propositions 5.4, 5.5).

f_a = 2|x-a| - (x-a)(y-b) on [0,1]^2, b = sqrt2 - 1 (c = -1, L = 2), N_opt = 2 for every a (Thm 4.4).
Node bound: exact closed form (oblivious.lb_kink).  At a straddling node the relaxation minimiser is
unique: xhat = a and yhat = l_y + rho w_y with rho = (a - l_x)/w_x (proof of Prop. 5.7).
Rules: bisect; R(alpha, beta, sel) with sel in {w (widest, ties to x), x (x only), sp (product-score
strong branching)}; Rscip = SCIP 10 default point (midpull .75, x relative width if < .5, clamp .2);
INC = incumbent branching (split at the incumbent's coordinate if strictly inside, else bisect),
incumbent (a, 1/2).

[A] exact rational replay of the x-intervals for a = 1/6, beta = 1/5 (Proposition 5.5 (i));
[B] cross-check of this runner against face_bb (HiGHS LP) on a few runs;
[C] node counts for a = 1/6 against the proved bound 0.0745 eps^(-1/2) (Proposition 5.5 (ii));
[D] clamp counts k0(a) near clamp points and the corrected bound of Proposition 5.4(c).
"""
import math
from fractions import Fraction as Fr
import numpy as np
from oblivious import lb_kink

B0 = math.sqrt(2) - 1


def run_fast(a, eps, rule, cap=2_000_000):
    stack = [(np.zeros(2), np.ones(2))]
    n = 0
    while stack:
        l, u = stack.pop()
        n += 1
        if n > cap:
            return None
        lb = lb_kink(l, u, a, B0, True)
        if lb >= -eps:
            continue
        w = u - l
        rho = (a - l[0]) / w[0]
        xhat = np.array([a, l[1] + rho * w[1]])

        def pt(i, kind, alpha, beta):
            mid = 0.5 * (l[i] + u[i])
            if kind == "INC":
                xs = (a, 0.5)[i]
                return xs if l[i] < xs < u[i] else mid
            al = alpha
            if kind == "Rscip":
                mp = 0.75 * (w[i] if w[i] < 0.5 else 1.0)
                al = 1 - mp
            p = al * xhat[i] + (1 - al) * mid
            return min(max(p, l[i] + beta * w[i]), u[i] - beta * w[i])

        if rule == "bisect":
            i = 0 if w[0] >= w[1] else 1
            p = 0.5 * (l[i] + u[i])
        else:
            kind, alpha, beta, sel = rule
            if sel == "w":
                i = 0 if w[0] >= w[1] else 1
            elif sel == "x":
                i = 0
            elif sel == "sp":
                best, i = -math.inf, 0
                for q in (0, 1):
                    pq = pt(q, kind, alpha, beta)
                    l1, u1 = l.copy(), u.copy(); u1[q] = pq
                    l2, u2 = l.copy(), u.copy(); l2[q] = pq
                    g1 = lb_kink(l1, u1, a, B0, True) - lb; g2 = lb_kink(l2, u2, a, B0, True) - lb
                    s = max(g1, 1e-9) * max(g2, 1e-9)
                    if s > best * (1 + 1e-9) + 1e-15:
                        best, i = s, q
            p = pt(i, kind, alpha, beta)
        l1, u1 = l.copy(), u.copy(); u1[i] = p
        l2, u2 = l.copy(), u.copy(); l2[i] = p
        stack += [(l2, u2), (l1, u1)]
    return n


RULES = {"bisect": "bisect", "LP(1,.2)w": ("R", 1.0, 0.2, "w"), "LP(1,.2)x": ("R", 1.0, 0.2, "x"),
         "LP(1,.2)sp": ("R", 1.0, 0.2, "sp"), "LP(1,0)w": ("R", 1.0, 0.0, "w"), "LP(1,.1)w": ("R", 1.0, 0.1, "w"),
         "R(.25,.2)w": ("R", 0.25, 0.2, "w"), "SCIPdef w": ("Rscip", None, 0.2, "w"),
         "SCIPdef x": ("Rscip", None, 0.2, "x"), "INC w": ("INC", None, None, "w")}


def part_a():
    a, beta = Fr(1, 6), Fr(1, 5)
    l, u = Fr(0), Fr(1)
    for k in range(12):
        w = u - l
        rho = (a - l) / w
        p = min(max(a, l + beta * w), u - beta * w)
        assert p != a and rho in (Fr(1, 6), Fr(5, 6)) and w == beta ** k
        l, u = (l, p) if a < p else (p, u)
    print("[A] a = 1/6, beta = 1/5: 12 straddling x-intervals replayed exactly; widths 5^-k, "
          "rho alternates 1/6, 5/6, every split clamped (never at a)")


def part_b():
    import face_bb as F
    import instances as I
    worst = 0
    for a in (1 / 6, 1 / 3, 0.2 - 1e-3):
        P = I.with_incumbent(I.kink(a=a), [a, 0.5])
        for name, fr in (("LP(1,.2)w", "LP(1,.2)w"), ("SCIPdef w", "SCIPdef w"), ("LP(1,.2)sp", "LP(1,.2)sp"),
                         ("INC w", "INC w"), ("bisect", "bisect")):
            for eps in (1e-2, 1e-3, 1e-4):
                n1 = run_fast(a, eps, RULES[name]); n2 = F.run(P, eps, F.RULES[fr])
                worst = max(worst, abs(n1 - n2))
    print(f"[B] fast closed-form runner versus face_bb (HiGHS LP), 45 runs: max |difference in nodes| = {worst}")


def part_c():
    a = 1 / 6
    print("[C] a = 1/6 node counts, eps = 1e-2 .. 1e-8; proved: LP(1,.2)w >= 0.0745/sqrt(eps)")
    for name in ("bisect", "LP(1,.2)w", "LP(1,.2)x", "LP(1,.2)sp", "LP(1,0)w", "LP(1,.1)w", "R(.25,.2)w",
                 "SCIPdef w", "SCIPdef x", "INC w"):
        ns = [run_fast(a, 10.0 ** -k, RULES[name]) for k in range(2, 9)]
        extra = ""
        if name == "LP(1,.2)w":
            ok = all(n >= 0.0745 / math.sqrt(10.0 ** -k) for n, k in zip(ns, range(2, 9)))
            extra = f"  bound holds: {ok}; bound values {[round(0.0745 * 10 ** (k / 2), 1) for k in range(2, 9)]}"
        print(f"    {name:11s} {ns}  nodes*sqrt(eps) = {[round(n * 10 ** (-k / 2), 2) for n, k in zip(ns, range(2, 9))]}{extra}",
              flush=True)


def k0(a, beta=0.2, kmax=200):
    l, u = 0.0, 1.0
    for k in range(kmax):
        w = u - l
        rho = (a - l) / w
        if beta <= rho <= 1 - beta:
            return k
        p = l + beta * w if rho < beta else u - beta * w
        l, u = (l, p) if a < p else (p, u)
    return None


def part_d():
    print("[D] clamp counts k0(a) (beta = .2) and the bound 1 + 4 beta^-(k0+1)/(1-beta) of Prop. 5.4(c); LP(1,.2)w")
    for a in (0.3, 0.199, 0.1999, 0.19999, 0.199999):
        kk = k0(a)
        bound = 1 + 4 * 0.2 ** (-(kk + 1)) / 0.8
        ns = [run_fast(a, 10.0 ** -k, RULES["LP(1,.2)w"]) for k in (4, 6, 8)]
        print(f"    a={a:<9} k0={kk:2d}  nodes at 1e-4,1e-6,1e-8 = {ns}  bound = {bound:.3g}", flush=True)


if __name__ == "__main__":
    part_a()
    part_b()
    part_c()
    part_d()
