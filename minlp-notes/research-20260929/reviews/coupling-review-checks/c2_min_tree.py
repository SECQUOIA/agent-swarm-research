"""Exact minimum number of leaves of a spatial B&B tree for the Jeroslow-type
instance of Theorem 5.1, over all trees whose split points lie on a grid.

    min sum_i y_i (1 - y_i)  s.t.  sum_i y_i = n/2,  y in [0,1]^n,  n odd.

A box is a leaf if its node bound (chord knapsack = box Lagrangian dual) is
>= UBD - eps with UBD = OPT = 1/4, or if it is infeasible. minLeaves(B) =
1 if B is a leaf, else min over (i, s) of minLeaves(B_left) + minLeaves(B_right).
Memoized up to coordinate permutations.

Theorem 5.1 predicts >= C(n+1, (n+1)/2) without bound tightening, for any
split points. The FBBT variant (row propagation before bounding) is outside
the theorem; it tests whether the bound is fragile to bound tightening.

Usage: python3 c2_min_tree.py
"""
import sys
from functools import lru_cache
from fractions import Fraction as Fr
from math import comb

sys.setrecursionlimit(100000)


def make(n, grid, eps, use_fbbt):
    T = Fr(n, 2)
    ub = Fr(1, 4)

    def f(y):
        return y * (1 - y)

    def bound(box):
        lo = sum(l for l, u in box)
        hi = sum(u for l, u in box)
        if T < lo or T > hi:
            return None
        val = sum(f(l) for l, u in box)
        need = T - lo
        sl = sorted(((f(u) - f(l)) / (u - l) if u > l else Fr(0), i) for i, (l, u) in enumerate(box))
        for s, i in sl:
            if need <= 0:
                break
            l, u = box[i]
            st = min(u - l, need)
            val += s * st
            need -= st
        return val

    def fbbt(box):
        lo = sum(l for l, u in box)
        hi = sum(u for l, u in box)
        out = []
        for l, u in box:
            nl = max(l, T - (hi - u))
            nu = min(u, T - (lo - l))
            if nl > nu:
                return None
            out.append((nl, nu))
        return tuple(out)

    def is_leaf(box):
        b = box
        if use_fbbt:
            b = fbbt(box)
            if b is None:
                return True
        v = bound(b)
        return v is None or v >= ub - eps

    @lru_cache(maxsize=None)
    def best(box):
        if is_leaf(box):
            return 1
        res = None
        for i, (l, u) in enumerate(box):
            if i > 0 and box[i] == box[i - 1]:
                continue  # symmetric duplicate
            for s in grid:
                if l < s < u:
                    left = tuple(sorted(box[:i] + ((l, s),) + box[i + 1:]))
                    right = tuple(sorted(box[:i] + ((s, u),) + box[i + 1:]))
                    a = best(left)
                    if res is not None and a >= res:
                        continue
                    t = a + best(right)
                    if res is None or t < res:
                        res = t
        return res if res is not None else 10 ** 9  # cannot split further

    root = tuple(((Fr(0), Fr(1)),) * n)
    return best(root)


if __name__ == "__main__":
    eps = Fr(1, 100)
    cases = [(3, [Fr(j, 10) for j in range(1, 10)]),
             (3, [Fr(j, 12) for j in range(1, 12)]),
             (5, [Fr(1, 4), Fr(1, 2), Fr(3, 4)]),
             (5, [Fr(1, 3), Fr(1, 2), Fr(2, 3)]),
             (7, [Fr(1, 2)])]
    print("n  grid  C(n+1,(n+1)/2)  min leaves (no FBBT)  min leaves (FBBT)")
    for n, grid in cases:
        a = make(n, grid, eps, False)
        b = make(n, grid, eps, True)
        print(f"{n}  {[str(g) for g in grid]}  {comb(n + 1, (n + 1) // 2)}  {a}  {b}", flush=True)
