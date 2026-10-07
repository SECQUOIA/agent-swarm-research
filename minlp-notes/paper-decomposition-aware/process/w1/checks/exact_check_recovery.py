"""Check snapping recovery (tau = 1/(4 n R)) and the candidate-denominator rule.

For instances with flat or multiple optimal sets: take optimizers s (face
optimizers, midpoints of flat pieces, and points of flat pieces very close to
a bound so that extra snaps occur), perturb within tau/2, snap, solve the
selected-face stationarity system by exact vertex enumeration, and verify
that every returned point is optimal and accepted by
F(x) - beta < 1/(V W) when beta = F* - 1/(2 V^2).
"""
import random
from fractions import Fraction as Fr
from itertools import combinations

from exact_common import (value, heights, face_candidates, lp_feasible_point)
from exact_check_height import hand_instances, random_instance

random.seed(7)
stats = dict(instances=0, recoveries=0, extra_snaps=0, singular_systems=0)


def recover(H, b, bounds, integers, y, tau):
    n = len(y)
    x = list(y)
    free = []
    for i in range(n):
        l, u = bounds[i]
        if i in integers or l == u:
            continue
        if y[i] - l <= tau:
            x[i] = l
        elif u - y[i] <= tau:
            x[i] = u
        else:
            free.append(i)
    fixed = [i for i in range(n) if i not in free]
    A = [[H[i][j] for j in free] for i in free]
    rhs = [-b[i] - sum(H[i][j] * x[j] for j in fixed) for i in free]
    if not free:
        return x, free
    sol = lp_feasible_point(A, rhs, [bounds[i] for i in free])
    if sol is None:
        return None, free
    for i, v in zip(free, sol):
        x[i] = v
    return x, free


def perturb(s, bounds, integers, radius):
    n = len(s)
    y = list(s)
    cont = [i for i in range(n) if i not in integers and bounds[i][0] < bounds[i][1]]
    if not cont:
        return y
    per = radius / len(cont) / Fr(2)  # sup-norm per coordinate keeps l2 <= radius
    for i in cont:
        y[i] = min(max(s[i] + per * Fr(random.randint(-1000, 1000), 1000), bounds[i][0]),
                   bounds[i][1])
    return y


def run(H, b, c, bounds, integers):
    n = len(b)
    hs = heights(H, b, c, bounds, integers)
    R, V = hs["R_had"], hs["V_had"]
    tau = Fr(1, 4 * n * R)
    cands = face_candidates(H, b, c, bounds, integers)
    Fstar = min(value(H, b, c, list(x)) for x, _ in cands)
    opt = [list(x) for x, _ in cands if value(H, b, c, list(x)) == Fstar]
    pts = list(opt)
    for x1, x2 in combinations(opt, 2):
        if any(x1[i] != x2[i] for i in integers):
            continue
        for t in (Fr(1, 2), Fr(1, 3), tau / 3, tau * Fr(5, 4)):
            s = [x1[i] + t * (x2[i] - x1[i]) for i in range(n)]
            if value(H, b, c, s) == Fstar:
                pts.append(s)
    stats["instances"] += 1
    beta = Fstar - Fr(1, 2 * V * V)
    for s in pts:
        for _ in range(3):
            y = perturb(s, bounds, integers, tau / 2)
            x, free = recover(H, b, bounds, integers, y, tau)
            assert x is not None, (s, y)
            Fx = value(H, b, c, x)
            assert Fx == Fstar, (s, y, x, Fx, Fstar)
            assert Fx - beta < Fr(1, V * Fx.denominator)
            stats["recoveries"] += 1
            interior = [i for i in range(n) if i not in integers
                        and bounds[i][0] < s[i] < bounds[i][1]]
            if len(free) < len(interior):
                stats["extra_snaps"] += 1
            if free:
                from exact_common import det
                if det([[H[i][j] for j in free] for i in free]) == 0:
                    stats["singular_systems"] += 1


for inst in hand_instances():
    run(*inst)
for _ in range(80):
    run(*random_instance(random.choice([2, 3])))
print(stats)
