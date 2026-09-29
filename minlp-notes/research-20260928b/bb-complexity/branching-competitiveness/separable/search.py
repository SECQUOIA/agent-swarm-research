"""Hill-climbing search for separable 2D instances maximizing omega_leaves / N_grid.

Each coordinate: H = max of lines (convex, exact rationals), m = H - t^2 shifted to min 0.
Lines are tangents of t^2 at p shifted up by mu, with an optional slope tilt s:
    l(t) = (2p + s) t - p^2 + mu - s p.
N_grid = exact least guillotine certificate with cuts in (knots + omega cuts + greedy points);
it is >= N_guill, so the printed ratio is a lower bound on the true ratio omega/N_guill.
usage: python3 search.py RULE ITERS SEED [LINES]
"""
import random
import sys
from fractions import Fraction as Fr
from sepexact import Coord, run, guill_grid
import fam


def coord_from_lines(lines):
    # breakpoints of max of lines on [0,1]: evaluate upper envelope exactly
    pts = {Fr(0), Fr(1)}
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            (a1, b1), (a2, b2) = lines[i], lines[j]
            if a1 != a2:
                t = (b2 - b1) / (a1 - a2)
                if 0 < t < 1:
                    pts.add(t)
    xs = sorted(pts)
    H = [max(a * t + b for a, b in lines) for t in xs]
    # keep only true kinks
    keep = [0]
    for k in range(1, len(xs) - 1):
        s1 = (H[k] - H[keep[-1]]) / (xs[k] - xs[keep[-1]])
        s2 = (H[k + 1] - H[k]) / (xs[k + 1] - xs[k])
        if s1 != s2:
            keep.append(k)
    keep.append(len(xs) - 1)
    return Coord([xs[k] for k in keep], [H[k] for k in keep])


def rand_line(rng):
    p = Fr(rng.randint(0, 1000), 1000)
    mu = Fr(rng.choice([0, 0, 1, 2, 5, 10, 20, 50, 100, 300]), 1000) * Fr(rng.randint(1, 10), 10)
    s = Fr(rng.choice([0, 0, 0, -1, 1, -3, 3, -10, 10]), 4) * Fr(rng.randint(1, 8), 8)
    return (2 * p + s, -p * p + mu - s * p)


def evaluate(lines1, lines2, eps, rule, cap=6000, G=44):
    c1, c2 = coord_from_lines(lines1), coord_from_lines(lines2)
    r = run([c1, c2], eps, rule, cap=cap, record=True)
    if r is None:
        return None
    if r["leaves"] < 3:
        return (0, r["leaves"], 1, c1, c2)
    cuts = fam.cut_positions(r)
    grids = []
    for c, cu in zip((c1, c2), cuts):
        base = set(c.x) | {c.L, c.U}
        extra = fam.greedy_multi(c, eps, K=8)
        pts = set(fam.thin(sorted(base), G // 3)) | set(fam.thin(sorted(cu | {c.L, c.U}), G // 3)) \
            | set(fam.thin(sorted(extra), G // 3))
        grids.append(sorted(pts))
    N, _ = guill_grid(c1, c2, grids[0], grids[1], eps, certificate=False)
    if N is None:
        return None
    return (r["leaves"] / N, r["leaves"], N, c1, c2)


if __name__ == "__main__":
    rule = sys.argv[1]
    iters = int(sys.argv[2])
    seed = int(sys.argv[3])
    k = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    rng = random.Random(seed)
    best_overall = 0
    R = int(sys.argv[5]) if len(sys.argv) > 5 else 10 ** 6
    for restart in range(R):
        eps = Fr(1, rng.choice([100, 1000, 10000, 100000, 1000000]))
        L1 = [rand_line(rng) for _ in range(k)]
        L2 = [rand_line(rng) for _ in range(k)]
        cur = evaluate(L1, L2, eps, rule)
        if cur is None:
            continue
        for it in range(iters):
            M1, M2 = list(L1), list(L2)
            tgt = M1 if rng.random() < 0.5 else M2
            j = rng.randrange(len(tgt))
            tgt[j] = rand_line(rng) if rng.random() < 0.3 else (
                tgt[j][0] + Fr(rng.randint(-20, 20), 100), tgt[j][1] + Fr(rng.randint(-20, 20), 1000))
            e2 = eps if rng.random() < 0.8 else Fr(1, rng.choice([100, 1000, 10000, 100000, 1000000]))
            new = evaluate(M1, M2, e2, rule)
            if new is None:
                continue
            if new[0] >= cur[0]:
                L1, L2, eps, cur = M1, M2, e2, new
        if cur[0] > best_overall:
            best_overall = cur[0]
            c1, c2 = cur[3], cur[4]
            print(f"restart {restart} ratio {cur[0]:.3f} leaves {cur[1]} Ngrid {cur[2]} eps {eps} "
                  f"knots {len(c1.x)},{len(c2.x)} L1={[(str(a), str(b)) for a, b in L1]} "
                  f"L2={[(str(a), str(b)) for a, b in L2]}", flush=True)
    print(f"done: {restart + 1} restarts, best ratio {best_overall:.3f}")
