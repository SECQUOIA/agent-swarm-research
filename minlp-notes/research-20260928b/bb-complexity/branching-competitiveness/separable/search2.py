"""Hill-climb on separable 2D instances maximizing RULE_leaves / OPT_min_leaves (both exact).
OPT_min = best offline tree that splits at relaxation minimizers (any coordinate choice).
usage: python3 search2.py RULE ITERS SEED LINES"""
import random
import sys
from fractions import Fraction as Fr
from sepexact import run, opt_min
from search import coord_from_lines, rand_line

EPS = [100, 1000, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 8]


def evaluate(L1, L2, eps, rule):
    c1, c2 = coord_from_lines(L1), coord_from_lines(L2)
    r = run([c1, c2], eps, rule, cap=20000)
    if r is None:
        return None
    o = opt_min(c1, c2, eps, cap=200000)
    if o is None:
        return None
    return (r["leaves"] / o, r["leaves"], o)


if __name__ == "__main__":
    rule, iters, seed, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    rng = random.Random(seed)
    best = 0
    R = int(sys.argv[5]) if len(sys.argv) > 5 else 10 ** 6
    for restart in range(R):
        eps = Fr(1, rng.choice(EPS))
        L1 = [rand_line(rng) for _ in range(k)]
        L2 = [rand_line(rng) for _ in range(k)]
        cur = evaluate(L1, L2, eps, rule)
        if cur is None:
            continue
        for it in range(iters):
            M1, M2 = list(L1), list(L2)
            tgt = M1 if rng.random() < 0.5 else M2
            if rng.random() < 0.1 and len(tgt) < 3 * k:
                tgt.append(rand_line(rng))
            else:
                j = rng.randrange(len(tgt))
                tgt[j] = rand_line(rng) if rng.random() < 0.3 else (
                    tgt[j][0] + Fr(rng.randint(-20, 20), 100), tgt[j][1] + Fr(rng.randint(-20, 20), 1000))
            e2 = eps if rng.random() < 0.85 else Fr(1, rng.choice(EPS))
            new = evaluate(M1, M2, e2, rule)
            if new is None:
                continue
            if new[0] >= cur[0]:
                L1, L2, eps, cur = M1, M2, e2, new
        if cur[0] > best:
            best = cur[0]
            print(f"restart {restart} ratio {cur[0]:.3f} rule {cur[1]} optmin {cur[2]} eps {eps} "
                  f"L1={[(str(a), str(b)) for a, b in L1]} L2={[(str(a), str(b)) for a, b in L2]}", flush=True)
    print(f"done: {restart + 1} restarts, best ratio {best:.3f}")
