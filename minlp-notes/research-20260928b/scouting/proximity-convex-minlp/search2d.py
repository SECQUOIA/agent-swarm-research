"""Adversarial (hill-climbing) search in dimension 2 against conjecture C1:
    prox_inf <= C * Delta(A) * max(1/2, rho_inf(Q)).
Hessians Q = M w w^T + eps I (w small primitive) are not lattice-separable,
have bounded rho_inf, and unbounded condition number as eps -> 0.
"""
from fractions import Fraction as F
import random, sys, json
from qip import qp_opt, int_opt, prox_inf, max_subdet, voronoi_linf_radius

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
starts = int(sys.argv[2]) if len(sys.argv) > 2 else 20
steps = int(sys.argv[3]) if len(sys.argv) > 3 else 60
random.seed(seed)


def evaluate(Q, A, b, c, rho, delta):
    xs = qp_opt(Q, c, A, b)
    if xs is None:
        return None
    opts = int_opt(Q, c, A, b, xs, max_points=150000)
    if not opts or opts == "big":
        return None
    p = float(prox_inf(xs, opts))
    return p / (delta * max(0.5, rho)), p, xs, opts


best_all = []
for s in range(starts):
    p_, q_ = random.choice([(1, 1), (1, 2), (2, 3), (1, 3), (3, 5), (2, 5)])
    w = (p_, -q_)
    M = F(random.choice([10, 100, 1000]))
    eps = F(1, random.choice([1, 10, 100, 1000]))
    Q = [[M * w[i] * w[j] + (eps if i == j else 0) for j in range(2)] for i in range(2)]
    rho = voronoi_linf_radius(Q)
    m = random.randint(2, 4)
    A = [[random.randint(-2, 2) for _ in range(2)] for _ in range(m)]
    if any(not any(r) for r in A):
        continue
    delta = max_subdet(A)
    b = [F(random.randint(-9, 15), random.randint(1, 7)) for _ in range(m)]
    c = [F(random.randint(-50, 50), random.randint(1, 5)) * M for _ in range(2)]
    cur = evaluate(Q, A, b, c, rho, delta)
    if cur is None:
        continue
    for _ in range(steps):
        b2 = [v + F(random.randint(-3, 3), random.randint(1, 7)) if random.random() < 0.5 else v for v in b]
        c2 = [v + F(random.randint(-20, 20), random.randint(1, 5)) * M if random.random() < 0.5 else v for v in c]
        new = evaluate(Q, A, b2, c2, rho, delta)
        if new is not None and new[0] >= cur[0]:
            cur, b, c = new, b2, c2
    best_all.append((cur[0], cur[1], delta, rho, [str(v) for v in Q[0] + Q[1]], A,
                     [str(v) for v in b], [str(v) for v in c], [str(v) for v in cur[2]], cur[3][:2]))

best_all.sort(key=lambda r: -r[0])
print(f"seed={seed} runs={len(best_all)}")
for r in best_all[:6]:
    print(json.dumps({"ratio": round(r[0], 3), "prox": round(r[1], 3), "Delta": r[2], "rho": round(r[3], 3),
                      "Q": r[4], "A": r[5], "b": r[6], "c": r[7], "xstar": r[8], "zopt": r[9]}))
