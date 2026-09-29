"""Theorem 2 check: adversarial sharp minimum against oblivious rules (exact rationals).

Instance f(y) = 2 alpha |y - a|_1 on [0,1]^n (alpha = 1), incumbent 0.  Node values are
exact (separable closed form in node_value).  An earlier version pruned every node without
a in its interior, which is wrong for n >= 2 (other coordinates can make such a node
invalid) and undercounted T; the review of 2026-09-29 found this.  The adversary builds a against the
rule as in the proof (middle thirds), then the tree is simulated on f_a.
"""
from fractions import Fraction as Fr
import math


def adversary(rule, n, K):
    box = [(Fr(0), Fr(1))] * n
    A = [(Fr(1, 3), Fr(2, 3))] * n
    for _ in range(K):
        i, s = rule(box)
        (l, u), (al, au) = box[i], A[i]
        left = (al, min(au, s)) if al < s else None
        right = (max(al, s), au) if s < au else None
        cand = [c for c in (left, right) if c is not None and c[1] > c[0]]
        Ap = max(cand, key=lambda c: c[1] - c[0])
        L3 = (Ap[1] - Ap[0]) / 3
        A = A[:i] + [(Ap[0] + L3, Ap[1] - L3)] + A[i + 1:]
        box = box[:i] + [(l, s) if Ap[1] <= s else (s, u)] + box[i + 1:]
    return tuple((al + au) / 2 for al, au in A)


def node_value(box, a):
    """Exact min over the box of m - q_B for m = eps + 2|y - a|_1 (without eps), alpha = 1.

    Separable: in coordinate i the minimum is -(a_i - l_i)(u_i - a_i) at a_i if a_i lies in
    [l_i, u_i] (slope 2 >= width), and 2 dist(a_i, [l_i, u_i]) at the nearer endpoint otherwise."""
    v = 0
    for (l, u), ai in zip(box, a):
        if l <= ai <= u:
            v -= (ai - l) * (u - ai)
        else:
            v += 2 * (l - ai if ai < l else ai - u)
    return v


def tree(rule, a, eps, cap=10 ** 6):
    n = len(a)
    stack, nodes = [tuple([(Fr(0), Fr(1))] * n)], 0
    while stack:
        box = stack.pop()
        nodes += 1
        if nodes > cap:
            return None
        if eps + node_value(box, a) >= 0:
            continue
        i, s = rule(box)
        l, u = box[i]
        stack.append(box[:i] + ((l, s),) + box[i + 1:])
        stack.append(box[:i] + ((s, u),) + box[i + 1:])
    return nodes


def widest(box):
    return max(range(len(box)), key=lambda j: box[j][1] - box[j][0])


RULES = {
    "bisection": lambda box: (widest(box), (box[widest(box)][0] + box[widest(box)][1]) / 2),
    "golden": lambda box: (widest(box), box[widest(box)][0] + Fr(382, 1000) * (box[widest(box)][1] - box[widest(box)][0])),
    "ten-percent": lambda box: (widest(box), box[widest(box)][0] + Fr(1, 10) * (box[widest(box)][1] - box[widest(box)][0])),
}

if __name__ == "__main__":
    for n in (1, 2):
        for name, rule in RULES.items():
            for k in (4, 8, 12):
                eps = Fr(1, 10 ** k)
                bound = n * math.log(1 / (9 * float(eps))) / math.log(36)
                K = math.ceil(bound) + 2
                a = adversary(rule, n, K)
                T = tree(rule, a, eps)
                print(f"n={n} {name:12s} eps=1e-{k:<2d} T={T:5d}  Theorem 2 bound 2*ceil(n log_36(1/(9eps)))+1 = {2*math.ceil(bound)+1}; "
                      f"N_opt <= 2^n = {2**n}")
                assert T >= 2 * math.ceil(bound) + 1
    print("all assertions passed")
