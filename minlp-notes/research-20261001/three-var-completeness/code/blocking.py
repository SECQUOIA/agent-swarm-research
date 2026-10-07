"""Combinatorial blocking criterion (proved in note.md, Lemma B).

A zero configuration is a list of face statuses s in {0,1,-1}^3 (-1 = free
coordinate, generic in (0,1)).  The origin is *blocked* if for every subset
Fr of free summand coordinates, pi_Fr(0) lies in the affine hull of
pi_Fr(V(Fr)), where V(Fr) are the zeros with s_j != 1 for all j not in Fr.
Generic positions are modelled by random reals (two independent draws)."""
from itertools import combinations, product
import numpy as np

FACES = [s for s in product((0, 1, -1), repeat=3) if s != (-1, -1, -1)]

def in_affine_hull(points, target, tol=1e-9):
    if len(points) == 0:
        return False
    P = np.array(points, float); t = np.array(target, float)
    if P.shape[1] == 0:
        return True
    base = P[0]
    D = (P[1:] - base).T if len(P) > 1 else np.zeros((P.shape[1], 0))
    r = t - base
    if D.shape[1] == 0:
        return np.linalg.norm(r) < tol
    sol, *_ = np.linalg.lstsq(D, r, rcond=None)
    return np.linalg.norm(D @ sol - r) < tol

def blocked(config, rng, draws=2):
    for _ in range(draws):
        pts = []
        for s in config:
            pts.append([rng.uniform(0.1, 0.9) if c == -1 else float(c) for c in s])
        for k in range(4):
            for Fr in combinations(range(3), k):
                vis = [p for p, s in zip(pts, config)
                       if all(s[j] != 1 for j in range(3) if j not in Fr)]
                proj = [[p[i] for i in Fr] for p in vis]
                if not in_affine_hull(proj, [0.0] * len(Fr)):
                    return False
    return True

def realizable_combinatorics(config):
    """Necessary conditions for a nonnegative quadratic with positive
    diagonal and p(0) > 0."""
    if (0, 0, 0) in config:
        return False
    verts = [s for s in config if -1 not in s]
    for v in verts:
        for s in config:
            if s.count(-1) == 1:
                # edge incident to v?
                if all(s[j] == v[j] for j in range(3) if s[j] != -1):
                    return False
    return True

def conditions(config):
    return sum(1 + s.count(-1) for s in config)

GROUP_ACT = []
from itertools import permutations
for perm in permutations(range(3)):
    for flips in product((0, 1), repeat=3):
        GROUP_ACT.append((perm, flips))

def act(s, g):
    perm, flips = g
    out = []
    for i in range(3):
        c = s[perm[i]]
        if c != -1 and flips[i]:
            c = 1 - c
        out.append(c)
    return tuple(out)

def canon_fixing_origin(config):
    """Canonical form under the 6 coordinate permutations (fix the origin)."""
    best = None
    for perm in permutations(range(3)):
        img = tuple(sorted(act(s, (perm, (0, 0, 0))) for s in config))
        if best is None or img < best:
            best = img
    return best

if __name__ == '__main__':
    import sys
    rng = np.random.default_rng(0)
    maxk = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    minimal = []
    seen = set()
    for k in range(1, maxk + 1):
        for config in combinations(FACES, k):
            if not realizable_combinatorics(config):
                continue
            key = canon_fixing_origin(config)
            if key in seen:
                continue
            seen.add(key)
            if not blocked(config, rng):
                continue
            # subset-minimal?
            if any(set(m) <= set(key) for m in minimal):
                continue
            minimal.append(key)
            print(k, conditions(key), key, flush=True)
    print('minimal blocking configurations (up to permutations fixing origin):', len(minimal))
