"""Find and print one exact instance where iterated bound tightening makes more than 2n
bound changes at one node (n = 2, box [0,2]x[0,3]), with the certified chain, and
confirm kappa <= L + S for the minimum trees of that instance (same model as
thm18c_counting.py)."""
import itertools
import random
from fractions import Fraction as Fr

from exact import phi
from thm18c_counting import Run, rand_A, exact_kappa

rng = random.Random(20260929)
lo0, hi0 = (0, 0), (2, 3)
n = 2
P = [tuple(Fr(v) for v in p) for p in itertools.product(range(3), range(4))]
found = 0
for t in range(2000):
    A = rand_A(rng, n)
    c = [Fr(rng.randint(1, 2 * (h - l) * 4 - 1), 8) + l for l, h in zip(lo0, hi0)]
    y = [sum(A[i][j] * c[j] for j in range(n)) + Fr(rng.randint(-4, 4), 10) for i in range(n)]
    OPT = min(phi(A, y, p) for p in P)
    eps = rng.choice([Fr(0), OPT / 100, OPT / 10, OPT / 3])
    tau = OPT - eps
    run = Run(A, y, lo0, hi0, tau, 'iter', [0, 1])
    # every sub-box reachable as a node box: check the reduction at each box
    for l1, h1 in [(a, b) for a in range(3) for b in range(a, 3)]:
        for l2, h2 in [(a, b) for a in range(4) for b in range(a, 4)]:
            steps, rl, rh = run.reduce((l1, l2), (h1, h2))
            if len(steps) > 2 * n:
                changes = []
                for (clo, chi, pl, ph, nl, nh) in steps:
                    changes.append(f"{clo}-{chi} -> {nl}-{nh}")
                kappa = exact_kappa(A, y, P, tau)
                N, L, S, _ = run.best(lo0, hi0, 'N')
                N2, L2, S2, _ = run.best(lo0, hi0, 'LS')
                one = Run(A, y, lo0, hi0, tau, 'one', [0, 1])
                s1, _, _ = one.reduce((l1, l2), (h1, h2))
                print(f"A = {[[str(v) for v in r] for r in A]}, y = {[str(v) for v in y]}, OPT = {OPT}, eps = {eps}")
                print(f"   node box lo={(l1, l2)} hi={(h1, h2)}: {len(steps)} certified bound changes with iterated passes (one pass: {len(s1)})")
                for ch in changes:
                    print("      ", ch)
                print(f"   kappa = {kappa}; min-N tree: N={N}, L={L}, S={S}; min-(L+S) tree: L+S={L2 + S2}")
                found += 1
                break
        if found:
            break
    if found:
        break
print("found" if found else "none found")
