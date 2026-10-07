"""Minimal blocking configurations with sharper realizability filters, and
SDP feasibility of the face F(B) of P3plus at random generic positions."""
import sys, json, time, warnings
from itertools import combinations, permutations, product
import numpy as np, cvxpy as cp
warnings.filterwarnings("ignore")
from blocking import FACES, blocked, canon_fixing_origin, conditions, act
from face_explore import lin_value, lin_deriv

def realizable(config):
    if (0, 0, 0) in config:
        return False
    for a, b in combinations(config, 2):
        fixed_equal = [j for j in range(3) if a[j] != -1 and a[j] == b[j]]
        if len(fixed_equal) >= 2:
            return False          # common axis-parallel line
    for s in config:
        if s.count(-1) == 2:      # facet zero
            j = [i for i in range(3) if s[i] != -1][0]
            others = [t for t in config if t is not s and t[j] == s[j]]
            if len(others) >= 2:
                return False
    return True

FAMILY = [(-1, 0, 0), (0, -1, 0), (1, 0, -1), (0, 1, -1), (1, 1, -1)]
FAMILY_IMAGES = set()
for perm in permutations(range(3)):
    FAMILY_IMAGES.add(frozenset(act(s, (perm, (0, 0, 0))) for s in FAMILY))

def in_family_pattern(config):
    return any(set(config) <= img for img in FAMILY_IMAGES)

def rows_for(config, rng):
    rows = []
    for s in config:
        pt = [rng.uniform(0.08, 0.92) if c == -1 else float(c) for c in s]
        rows.append(lin_value(pt))
        for i in range(3):
            if s[i] == -1:
                rows.append(lin_deriv(pt, i))
    return np.array(rows)

def build_feas():
    from sdp3 import Separation
    S = Separation()
    A = cp.Parameter((12, 10))
    # maximize p(0) subject to p in base of P3plus and contact rows
    pv = S.pv
    prob = cp.Problem(cp.Maximize(pv[0]), S.prob.constraints + [A @ pv == 0])
    return prob, A, pv

if __name__ == '__main__':
    maxk = int(sys.argv[1]); trials = int(sys.argv[2])
    rng = np.random.default_rng(1)
    minimal = []; seen = set()
    for k in range(1, maxk + 1):
        for config in combinations(FACES, k):
            if not realizable(config):
                continue
            key = canon_fixing_origin(config)
            if key in seen:
                continue
            seen.add(key)
            if not blocked(key, rng):
                continue
            if any(set(m) <= set(key) for m in minimal):
                continue
            minimal.append(key)
    print('minimal blocking (filtered):', len(minimal), flush=True)
    prob, A, pv = build_feas()
    results = []
    for key in minimal:
        c = conditions(key)
        if c > 12:
            results.append((key, c, 'skip')); continue
        best = -np.inf
        for t in range(trials):
            R = rows_for(key, rng)
            Ap = np.zeros((12, 10)); Ap[:R.shape[0]] = R
            A.value = Ap
            try:
                prob.solve(solver='CLARABEL')
                val = prob.value if prob.status in ('optimal', 'optimal_inaccurate') else -np.inf
            except Exception:
                val = -np.inf
            best = max(best, val if val is not None else -np.inf)
        fam = in_family_pattern(key)
        results.append((key, c, best, fam))
        print(c, 'family-sub' if fam else 'NEW', 'max p(0)=%.3g' % best, key, flush=True)
    json.dump([list(map(str, r)) for r in results], open(f'../logs/blocking2_k{maxk}.json', 'w'))
