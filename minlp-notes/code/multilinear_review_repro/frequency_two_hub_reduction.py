"""Exhaustive check of the prize-collecting edge-cover / hub reduction.

Independent 2026-09-25 reproduction of the unarchived 150-instance check
reported in notes/review-multilinear-frequency-two-optimization.md for
results/positive-multilinear-frequency-two-optimization.md. It was written
from the review's description; the reviewer's original script is not
available, so the instances are new ones.

Part A (the review's check): on 150 seeded small graphs with signed integer
edge costs, zero or positive penalties, parallel edges, and isolated vertices,
compare by brute force the signed-cost prize-collecting optimum
    min_S  c(S) + sum_{v uncovered by S} p_v
with the note's reduction: fix negative-cost edges, zero their endpoints'
penalties, add hub h and mate k with edge hk of cost 0 and an edge vh of cost
p_v for every original vertex, and take a minimum-cost edge cover of the
augmented graph. Also checks that the original edges of an optimal augmented
cover, plus the fixed edges, are optimal for the original problem.

Part B (additional): on 150 seeded frequency-two positive polynomials with
rational lambda, compare brute-force min_X f(X)-lambda^T X with the value
obtained through identity (1), dummy leaves, separate unused variables, and
the same reduction. All arithmetic is exact (integers and Fractions).
"""
import itertools
import random
from fractions import Fraction as F


def pc_value(n_vertices, edges, penalty, chosen):
    covered = set()
    for e in chosen:
        covered.update(edges[e][:2])
    return (sum(edges[e][2] for e in chosen)
            + sum(penalty[v] for v in range(n_vertices) if v not in covered))


def pc_brute(n_vertices, edges, penalty):
    return min(pc_value(n_vertices, edges, penalty, s)
               for r in range(len(edges) + 1)
               for s in itertools.combinations(range(len(edges)), r))


def hub_reduction(n_vertices, edges, penalty):
    """Return (value, recovered original edge set) via the hub edge cover."""
    fixed = [e for e, (_, _, c) in enumerate(edges) if c < 0]
    const = sum(edges[e][2] for e in fixed)
    pen = list(penalty)
    for e in fixed:
        u, v, _ = edges[e]
        pen[u] = pen[v] = 0
    keep = [e for e, (_, _, c) in enumerate(edges) if c >= 0]
    h, k = n_vertices, n_vertices + 1
    aug = [(edges[e][0], edges[e][1], edges[e][2], e) for e in keep]
    aug += [(v, h, pen[v], None) for v in range(n_vertices)]
    aug += [(h, k, 0, None)]
    best = None
    for r in range(len(aug) + 1):
        for s in itertools.combinations(range(len(aug)), r):
            cov = set()
            for i in s:
                cov.update(aug[i][:2])
            if len(cov) < n_vertices + 2:
                continue
            cost = sum(aug[i][2] for i in s)
            if best is None or cost < best[0]:
                best = (cost, [aug[i][3] for i in s if aug[i][3] is not None])
    return const + best[0], fixed + best[1]


def check_graph(n_vertices, edges, penalty):
    opt = pc_brute(n_vertices, edges, penalty)
    val, rec = hub_reduction(n_vertices, edges, penalty)
    assert val == opt, (n_vertices, edges, penalty, opt, val)
    assert pc_value(n_vertices, edges, penalty, rec) == opt
    return opt


def part_a(count=150, seed=20260925):
    rng = random.Random(seed)
    feats = dict(negative=0, zero_cost=0, zero_penalty=0, parallel=0,
                 isolated=0, no_edges=0)
    for _ in range(count):
        nv = 1 if rng.random() < 0.05 else rng.randint(2, 6)
        ne = rng.randint(0, 7) if nv >= 2 else 0
        edges = []
        for _ in range(ne):
            if edges and rng.random() < 0.25:
                u, v, _ = rng.choice(edges)      # force a parallel edge
            else:
                u, v = rng.sample(range(nv), 2)
            edges.append((u, v, rng.randint(-3, 4)))
        penalty = [rng.choice([0, 0, 1, 2, 3, 5]) for _ in range(nv)]
        check_graph(nv, edges, penalty)
        pairs = [frozenset(e[:2]) for e in edges]
        used = {x for e in edges for x in e[:2]}
        feats['negative'] += any(c < 0 for *_, c in edges)
        feats['zero_cost'] += any(c == 0 for *_, c in edges)
        feats['zero_penalty'] += 0 in penalty
        feats['parallel'] += len(set(pairs)) < len(pairs)
        feats['isolated'] += len(used) < nv
        feats['no_edges'] += ne == 0
    assert all(feats.values()), feats
    return feats


def part_b(count=150, seed=20260926):
    rng = random.Random(seed)
    done = 0
    while done < count:
        n, m = rng.randint(2, 7), rng.randint(1, 4)
        incid = [sorted(rng.sample(range(m), rng.choice([0, 1, 1, 2, 2, 2])))
                 if m >= 2 else rng.choice([[], [0], [0]])
                 for _ in range(n)]
        supports = [frozenset(i for i in range(n) if t in incid[i])
                    for t in range(m)]
        if any(len(s) < 2 for s in supports) or len(set(supports)) < m:
            continue                            # nonlinear, distinct supports
        coef = [rng.randint(1, 4) for _ in range(m)]
        lam = [F(rng.randint(-6, 6), rng.choice([1, 2, 3])) for _ in range(n)]
        brute = min(sum(c for c, s in zip(coef, supports)
                        if all(X[i] for i in s))
                    - sum(l * xi for l, xi in zip(lam, X))
                    for X in itertools.product((0, 1), repeat=n))
        # Dual graph: monomials are vertices, variables are edges.
        penalty, edges, const = list(coef), [], F(0)
        for i in range(n):
            if not incid[i]:
                const += min(F(0), -lam[i])     # optimized separately
                continue
            const -= lam[i]                     # constant in identity (1)
            if len(incid[i]) == 1:
                penalty.append(0)               # zero-penalty dummy leaf
                edges.append((incid[i][0], len(penalty) - 1, lam[i]))
            else:
                edges.append((incid[i][0], incid[i][1], lam[i]))
        val, _ = hub_reduction(len(penalty), edges, penalty)
        assert const + val == brute, (supports, coef, lam, brute, const + val)
        done += 1
    return done


if __name__ == '__main__':
    feats = part_a()
    print('Part A: 150 prize-collecting instances, hub reduction value equals '
          'brute-force optimum exactly; recovered edge sets optimal')
    print('  instances containing each feature:', feats)
    print(f'Part B: {part_b()} frequency-two polynomial instances, '
          'min f(X)-lambda^T X equals reduction value exactly')
    print('ALL CHECKS PASSED')
