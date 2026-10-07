"""Jeroslow-type instance with one dense row and separable nonconvex blocks.

    min  sum_i c y_i (1 - y_i)   s.t.  2 sum_i y_i = n,  y in [0,1]^n,  n odd.

OPT = c/4 (one block at 1/2). The node bound on a box B is the coupling
Lagrangian dual on B, which for separable blocks equals
min { sum_i chord_{B_i}(y_i) : 2 sum y = n, y in B } (chords = convex envelopes
of the concave blocks). This is a continuous knapsack, solved exactly by a
greedy rule.

Runs best-first spatial B&B with two branching rules and counts leaves, to
compare with the lower bound C(n+1, (n+1)/2) of Theorem 5.1 (valid for every
branching rule and split point).

Usage: python3 jeroslow_bb.py
"""
import heapq
from math import comb

C = 1.0


def chord(l, u):
    """Chord of c y(1-y) on [l,u]: value at l and slope."""
    fl = C * l * (1 - l)
    if u - l < 1e-15:
        return fl, 0.0
    return fl, C * (1 - l - u)


def node_bound(box, target):
    """Exact min of sum chord_i(y_i) s.t. sum y = target, y in box."""
    n = len(box)
    lo = sum(l for l, u in box)
    hi = sum(u for l, u in box)
    if target < lo - 1e-12 or target > hi + 1e-12:
        return float("inf"), None
    y = [l for l, u in box]
    val = sum(chord(l, u)[0] for l, u in box)
    need = target - lo
    order = sorted(range(n), key=lambda i: chord(*box[i])[1])
    for i in order:
        if need <= 1e-15:
            break
        l, u = box[i]
        step = min(u - l, need)
        y[i] += step
        val += chord(l, u)[1] * step
        need -= step
    return val, y


def fbbt(box, target):
    """Bound propagation on the row sum y = target (to a fixpoint)."""
    box = list(box)
    for _ in range(50):
        lo = sum(l for l, u in box)
        hi = sum(u for l, u in box)
        changed = False
        for i, (l, u) in enumerate(box):
            nl = max(l, target - (hi - u))
            nu = min(u, target - (lo - l))
            if nl > nu + 1e-12:
                return None
            if nl > l + 1e-12 or nu < u - 1e-12:
                box[i] = (nl, max(nl, nu))
                lo += nl - l
                hi += box[i][1] - u
                changed = True
        if not changed:
            break
    return tuple(box)


def bb(n, eps, rule, use_fbbt=False):
    target = n / 2.0
    ub = C / 4.0
    root = tuple((0.0, 1.0) for _ in range(n))
    val, y = node_bound(root, target)
    heap = [(val, 0, root, y)]
    cnt = 1
    leaves = 0
    nodes = 1
    while heap:
        val, _, box, y = heapq.heappop(heap)
        if val >= ub - eps:
            leaves += 1
            continue
        # choose branching variable
        gaps = []
        for i, (l, u) in enumerate(box):
            f0, s = chord(l, u)
            g = C * y[i] * (1 - y[i]) - (f0 + s * (y[i] - l))
            gaps.append(g)
        i = max(range(n), key=lambda j: gaps[j])
        l, u = box[i]
        if rule == "bisect":
            m = 0.5 * (l + u)
        else:  # split at the relaxation point (clipped away from the ends)
            m = min(max(y[i], l + 0.1 * (u - l)), u - 0.1 * (u - l))
        for (a, b) in ((l, m), (m, u)):
            nb = list(box)
            nb[i] = (a, b)
            nb = tuple(nb)
            if use_fbbt:
                nb = fbbt(nb, target)
                if nb is None:
                    nodes += 1
                    leaves += 1
                    continue
            v2, y2 = node_bound(nb, target)
            nodes += 1
            if y2 is None:
                leaves += 1
                continue
            cnt += 1
            heapq.heappush(heap, (v2, cnt, nb, y2))
        if nodes > 3_000_000:
            return None, nodes
    return leaves, nodes


if __name__ == "__main__":
    print("n  lower_bound C(n+1,(n+1)/2)  leaves(bisect)  leaves(split-at-y)  eps"
          "  | with FBBT on the row (outside the theorem's model): bisect, split-at-y")
    for n in [3, 5, 7, 9, 11, 13]:
        for eps in [0.05, 0.01]:
            lb = comb(n + 1, (n + 1) // 2)
            l1, _ = bb(n, eps, "bisect")
            l2, _ = bb(n, eps, "at_y")
            f1, _ = bb(n, eps, "bisect", True)
            f2, _ = bb(n, eps, "at_y", True)
            print(f"{n:2d}  {lb:8d}  {l1}  {l2}  {eps}  | {f1}  {f2}")
