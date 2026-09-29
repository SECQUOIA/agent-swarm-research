"""Reviewer check: R(1, beta) never splits at a when a lies in a Cantor-type set (Prop 5.4(b), Conj 5.7).

For beta = 1/5 and a = 1/6, the relaxation point xhat = a (Prop 5.4(a)) lies in the outer beta-fraction of
every straddling x-interval, so every x split is clamped and never lands on a.  Part A replays the
x-intervals in exact rational arithmetic.  Part B counts nodes with the reviewer's exact PL bound
(kink_rules.relax) for the scout's L=2, c=-1, b=sqrt2-1 but a = 1/6, and compares with bisection.
N_opt = 2 for every a (Theorem 4.4), so growth of R(1,.2)w contradicts Prop 5.4(b) and Conjecture 5.7.
"""
from fractions import Fraction as Fr
import math
from kink_rules import run, mk_R, rule_bisect, rule_scip

beta = Fr(1, 5)
a = Fr(1, 6)
l, u = Fr(0), Fr(1)
print("[A] exact x-intervals for a = 1/6, R(1,1/5) (x̂ = a at straddling nodes):")
for k in range(12):
    w = u - l
    lo, hi = l + beta * w, u - beta * w
    clamped = not (lo <= a <= hi)
    p = min(max(a, lo), hi)
    side = "left" if a < p else ("right" if a > p else "at a")
    print(f"    step {k:2d}: [{float(l):.10f}, {float(u):.10f}] w={float(w):.3e}  split {float(p):.10f}  "
          f"clamped={clamped}  a in {side} child")
    if p == a:
        break
    l, u = (l, p) if a < p else (p, u)
print("    fixed point of the two-step map t -> beta(1-beta) + beta^2 t:", beta / (1 + beta))

print("[B] nodes for a = 1/6 (L=2, c=-1, b=sqrt2-1); eps = 1e-2 .. 1e-8")
eps_list = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8]
kw = dict(a=1.0 / 6.0)
for name, r in [("bisect", rule_bisect), ("R(1,.2)w", mk_R(1, .2)), ("R(1,.2)x", mk_R(1, .2, "x")),
                ("R(1,.2)sp", mk_R(1, .2, "p")), ("R(1,.1)w", mk_R(1, .1)), ("SCIPactual w", rule_scip("w"))]:
    row = [run(r, e, cap=400000, **kw) for e in eps_list]
    scaled = [f"{n * math.sqrt(e):.2f}" if n else "-" for n, e in zip(row, eps_list)]
    print(f"    {name:12s} {row}   nodes*sqrt(eps) = {scaled}")
