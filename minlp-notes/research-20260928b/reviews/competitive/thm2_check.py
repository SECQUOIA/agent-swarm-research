"""Reviewer check of Theorem 2 (oblivious rules), exact rationals.

Independent implementation of the middle-third adversary against rules that
see only the box and depth, including depth-dependent, coordinate-cycling
and hash-based (pseudo-random but deterministic) rules, n = 1, 2, 3.
Instance f_a(y) = 2 |y - a|_1 on [0,1]^n, alpha = 1, f* = 0.
Node values (derived by the reviewer): phi_B is separable; each coordinate
term 2|t - a_i| - (t-l)(u-t) is convex, minimized at a_i if a_i is in
[l,u] (slopes of opposite sign there since u - l <= 1) and otherwise at the
endpoint nearest a_i with value >= 0.  NOTE: for n >= 2 a node with a on
its boundary (or outside it in one coordinate) is NOT automatically pruned:
the other coordinates can still make phi_B negative.  The exact separable
minimum is used.
Checks T >= 2 ceil(n log_36(1/(9 eps))) + 1 and that the 2^n orthant boxes
at a are valid (exact evaluation of the separable minimum).
"""
import hashlib
import math
from fractions import Fraction as Fr


def widest(box):
    return max(range(len(box)), key=lambda j: (box[j][1] - box[j][0], -j))


def rule_bis(box, depth):
    i = widest(box); l, u = box[i]
    return i, (l + u) / 2


def rule_cycle(box, depth):
    i = depth % len(box); l, u = box[i]
    return i, l + Fr((depth % 3) + 1, 4) * (u - l)


def rule_hash(box, depth):
    h = hashlib.sha256(repr([(float(l), float(u)) for l, u in box]).encode()).digest()
    i = h[0] % len(box); l, u = box[i]
    return i, l + Fr(1 + h[1] % 254, 256) * (u - l)


def rule_edge(box, depth):
    i = widest(box); l, u = box[i]
    return i, l + Fr(1, 50) * (u - l)


RULES = {"bisect-widest": rule_bis, "cycle-depth": rule_cycle, "hash": rule_hash, "2%-edge": rule_edge}


def adversary(rule, n, K):
    box = tuple([(Fr(0), Fr(1))] * n)
    A = [(Fr(1, 3), Fr(2, 3))] * n
    for depth in range(K):
        i, s = rule(box, depth)
        l, u = box[i]
        al, au = A[i]
        left = (al, min(au, s))
        right = (max(al, s), au)
        if left[1] - left[0] >= right[1] - right[0]:
            Ap, child = left, (l, s)
        else:
            Ap, child = right, (s, u)
        third = (Ap[1] - Ap[0]) / 3
        A[i] = (Ap[0] + third, Ap[1] - third)
        box = box[:i] + (child,) + box[i + 1:]
        for j in range(n):              # (P1) invariant, exact
            assert A[j][0] - box[j][0] >= A[j][1] - A[j][0] and box[j][1] - A[j][1] >= A[j][1] - A[j][0]
    return tuple((al + au) / 2 for al, au in A)


def coord_min(t_l, t_u, a):
    """min over t in [t_l,t_u] of 2|t-a| - (t-t_l)(t_u-t) (convex): candidates a (if inside), ends."""
    cands = [t_l, t_u] + ([a] if t_l <= a <= t_u else [])
    return min(2 * abs(t - a) - (t - t_l) * (t_u - t) for t in cands)


def tree(rule, a, eps, cap=2 * 10 ** 5):
    n = len(a)
    stack, nodes = [(tuple([(Fr(0), Fr(1))] * n), 0)], 0
    while stack:
        box, depth = stack.pop()
        nodes += 1
        if nodes > cap:
            return None
        if eps + sum(coord_min(l, u, ai) for (l, u), ai in zip(box, a)) >= 0:
            continue
        i, s = rule(box, depth)
        l, u = box[i]
        stack.append((box[:i] + ((l, s),) + box[i + 1:], depth + 1))
        stack.append((box[:i] + ((s, u),) + box[i + 1:], depth + 1))
    return nodes


if __name__ == "__main__":
    for n in (1, 2, 3):
        for name, rule in RULES.items():
            for k in (4, 8, 12):
                eps = Fr(1, 10 ** k)
                X = n * math.log(1 / (9 * float(eps))) / math.log(36)
                a = adversary(rule, n, math.ceil(X) + 1)
                # orthant certificate valid: eps + sum of coordinate minima over [0,a_i] and [a_i,1] >= eps > 0
                for i in range(n):
                    assert coord_min(Fr(0), a[i], a[i]) >= 0 and coord_min(a[i], Fr(1), a[i]) >= 0
                if n == 3 and k > 8:
                    continue
                T = tree(rule, a, eps)
                bound = 2 * math.ceil(X) + 1
                Ts = ">2e5" if T is None else str(T)
                assert T is None or T >= bound, (n, name, k, T, bound)
                print(f"n={n} {name:14s} eps=1e-{k:<2d} T={Ts:>6s} >= bound {bound:3d}; N_opt <= {2**n}", flush=True)
    print("all assertions passed")
