"""Search for bad instances of R_min (exact rationals).

Phase 1: scan the 'ties' family of thm1_check.py for the largest worst-over-ties
         ratio T/(2N-1) and print the instance and the adversarial tree.
Phase 2: hill-climb (random rational perturbations of m, knots kept) to find
         instances with UNIQUE relaxation minimizers at every processed node
         and a large T/(2N-1); report the best per N.

Usage: python3 worst_rmin.py SEED NSCAN NCLIMB
"""
import random
import sys
from fractions import Fraction as Fr
from functools import lru_cache

from exact1d import Inst
from thm1_check import make, worst_tree


def adversarial_tree(I):
    @lru_cache(maxsize=None)
    def W(l, u):
        v, arg = I.node(l, u)
        if v >= 0:
            return 0, ()
        best = None
        for s in arg:
            a, ta = W(l, s)
            b, tb = W(s, u)
            if best is None or a + b > best[0]:
                best = (a + b, ((l, u, s),) + ta + tb)
        return 1 + best[0], best[1]
    return W(Fr(0), Fr(1))


def unique_run(I):
    """R_min run; returns (#internal, all_unique)."""
    out, uniq, stack = 0, True, [(Fr(0), Fr(1))]
    while stack:
        l, u = stack.pop()
        v, arg = I.node(l, u)
        if v >= 0:
            continue
        if len(arg) != 1:
            uniq = False
        s = arg[0]
        out += 1
        stack += [(l, s), (s, u)]
    return out, uniq


def score(I):
    N = len(I.greedy()) - 1
    if N < 2:
        return None
    k, uniq = unique_run(I)
    return (2 * k + 1) / (2 * N - 1), N, 2 * k + 1, uniq


def main():
    seed, nscan, nclimb = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    best = None
    for t in range(nscan):
        I = make(rng, "ties")
        if I is None:
            continue
        N = len(I.greedy()) - 1
        if N < 2:
            continue
        W, tree = adversarial_tree(I)
        r = (2 * W + 1) / (2 * N - 1)
        if best is None or r > best[0]:
            best = (r, N, 2 * W + 1, I, tree)
    r, N, T, I, tree = best
    print(f"phase 1: worst over ties: T={T} N={N} ratio={float(r):.4f}")
    print("  knots:", [str(x) for x in I.x])
    print("  m    :", [str(m) for m in I.m])
    print("  convex H:", I.convex(), " eps =", I.eps)
    print("  greedy certificate:", [str(s) for s in I.greedy()])
    for (l, u, s) in tree:
        v, arg = I.node(l, u)
        print(f"  node [{l}, {u}] value {v} minimizers {[str(a) for a in arg]} -> split {s}")

    # phase 2: hill climbing for unique-minimizer instances
    bestN = {}
    for trial in range(nclimb):
        kind = rng.choice(["convex", "nonconvex", "rigid", "flat", "manymin"])
        I = make(rng, kind)
        if I is None:
            continue
        sc = score(I)
        if sc is None:
            continue
        cur = I
        for it in range(150):
            ms = list(cur.m)
            k = rng.randrange(len(ms))
            ms[k] = ms[k] * Fr(rng.randint(50, 200), 100)
            try:
                J = Inst(cur.x, [m - min(ms) + cur.eps for m in ms])
            except AssertionError:
                continue
            if kind == "convex" and not J.convex():
                continue
            s2 = score(J)
            if s2 is None or not s2[3]:
                continue
            if sc[3] is False or s2[0] >= sc[0]:
                cur, sc = J, s2
        if sc[3]:
            N = sc[1]
            if N not in bestN or sc[0] > bestN[N][0]:
                bestN[N] = (sc[0], sc[2], kind, cur.convex())
    for N in sorted(bestN):
        r, T, kind, cvx = bestN[N]
        print(f"phase 2 (unique minimizers): N={N} best T={T} ratio={float(r):.4f} (family {kind}, convex H {cvx})")


if __name__ == "__main__":
    main()
