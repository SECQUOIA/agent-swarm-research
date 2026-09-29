"""Hill-climb separable 2D instances to maximize leaves(rule) / N_guill(grid).

N_guill(grid) (exact guillotine optimum with cuts on knots + uniform grid) is an
upper bound on the true N_guill, so large ratios certify non-competitiveness
(up to floating point).  Usage: python3 search_sep2d.py RULE K RESTARTS STEPS SEED [EPS]
"""
import sys
import numpy as np
from nd_sep import run, guill_grid, default_grid
from poly1d import Inst, from_lines


def build(params, eps):
    Is = []
    for P in params:
        lines = [(s, b) for s, b in P] + [(0.0, 0.3), (2.0, -0.7)]
        xs, ms = from_lines(lines)
        ms = ms - ms.min() + eps / 2
        Is.append(Inst(xs, ms))
    return Is


def rand_params(rng, K):
    out = []
    for _ in range(2):
        P = []
        for _ in range(K):
            p = rng.uniform(0, 1); mu = np.exp(rng.uniform(np.log(1e-4), np.log(0.5)))
            e = rng.normal(0, 1.0) * rng.choice([0.0, 1.0])
            P.append((2 * p + e, -p * p + mu - e * p))
        out.append(P)
    return out


def perturb(rng, params):
    out = []
    for P in params:
        Q = []
        for s, b in P:
            if rng.uniform() < 0.3:
                s += rng.normal(0, 0.1); b += rng.normal(0, 0.02)
            Q.append((s, b))
        out.append(Q)
    return out


def score(params, rule, eps, G=33):
    try:
        Is = build(params, eps)
    except ValueError:
        return -1, None
    nodes, leaves = run(Is, rule, cap=20000)
    if nodes is None:
        return -1, None
    grids = [default_grid(I, G) for I in Is]
    ng = guill_grid(Is, grids)
    if ng <= 0:
        return -1, None
    return leaves / ng, (nodes, leaves, ng, len(grids[0]), len(grids[1]))


if __name__ == "__main__":
    rule, K, restarts, steps, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    eps = float(sys.argv[6]) if len(sys.argv) > 6 else 1e-6
    rng = np.random.default_rng(seed)
    best = (-1, None, None)
    for rep in range(restarts):
        params = rand_params(rng, K)
        cur = score(params, rule, eps)
        for it in range(steps):
            p2 = perturb(rng, params)
            s2 = score(p2, rule, eps)
            if s2[0] >= cur[0]:
                params, cur = p2, s2
        print(rule, rep, "ratio %.3f" % cur[0], "(nodes, leaves, N_guill_grid, G1, G2) =", cur[1], flush=True)
        if cur[0] > best[0]:
            best = (cur[0], cur[1], params)
    print("BEST", rule, "%.3f" % best[0], best[1])

