"""Discovery: faces of P3plus obtained from the five contacts of a family
member by dropping one or two contacts; their extreme rays are tested for
membership in the cone dual to R.  Numerical only."""
import sys, json, time, warnings
from itertools import combinations
import numpy as np, cvxpy as cp
warnings.filterwarnings("ignore")
from cube3 import *
from sdp3 import *
from zero_pattern import pattern
from face_explore import lin_value, lin_deriv
from face_explore_generic import FaceSepVar

def family_contacts(h, d1, d2, d3, k):
    D = d1 + d2 - h
    return [((h / d1, 0, 0), 0), ((0, h / d2, 0), 1), ((1, 0, (d1 - h) / d3), 2),
            ((0, 1, (d2 - h) / d3), 2), ((1, 1, (D + k) / d3), 2)]

def transform_contacts(contacts, g):
    """Contacts of p o g^{-1}: if p vanishes at z then p o g^{-1} vanishes at g(z)."""
    perm, flips = g
    out = []
    for pt, i in contacts:
        # g(z)_j = z_{perm[j]} or 1 - z_{perm[j]}
        new = [ (1 - pt[perm[j]]) if flips[j] else pt[perm[j]] for j in range(3)]
        jdir = [j for j in range(3) if perm[j] == i][0]
        out.append((tuple(new), jdir))
    return out

if __name__ == '__main__':
    seed = int(sys.argv[1]); n = int(sys.argv[2]); per = int(sys.argv[3]); drop = int(sys.argv[4])
    rng = np.random.default_rng(seed)
    FS = FaceSepVar(10); R1 = Relaxation(use_family=True); R0 = Relaxation(use_family=False)
    found = []; allvals = []; stats = dict(faces=0, rays=0, notd3=0, missing=0)
    t0 = time.time()
    for it in range(n):
        d1, d2 = rng.uniform(0.3, 2, 2); h = rng.uniform(0.05, 0.95) * min(d1, d2)
        k = rng.uniform(0.05, 2); D = d1 + d2 - h; d3 = (D + k) * rng.uniform(1.05, 3)
        contacts = family_contacts(h, d1, d2, d3, k)
        g = GROUP[rng.integers(48)]
        contacts = transform_contacts(contacts, g)
        keep_sets = list(combinations(range(5), 5 - drop))
        keep = keep_sets[rng.integers(len(keep_sets))]
        rows = []
        for idx in keep:
            pt, i = contacts[idx]; rows += [lin_value(pt), lin_deriv(pt, i)]
        A = np.zeros((10, 10)); A[:len(rows)] = np.array(rows)
        FS.A.value = A; stats['faces'] += 1
        for j in range(per):
            w = rng.normal(size=10)
            try:
                val, st, p = FS.solve(w)
            except Exception:
                break
            if p is None or st not in ('optimal', 'optimal_inaccurate'): break
            p = p / np.abs(p).max(); stats['rays'] += 1
            try:
                r1 = R1.solve(p)[0]; r0 = R0.solve(p)[0]
            except Exception:
                continue
            allvals.append((float(r1), float(r0)))
            if r0 < -1e-6: stats['notd3'] += 1
            if r1 < -1e-6:
                stats['missing'] += 1
                pat, z = pattern(p, 1e-5)
                found.append(dict(p=p.tolist(), r1=r1, r0=r0, keep=keep, zeros=[(list(s), list(x)) for s, x in z]))
                print('MISSING', it, j, 'r1', r1, 'r0', r0, 'pattern', pat, np.round(p, 4).tolist(), flush=True)
    print(stats, 'time', time.time() - t0, flush=True)
    json.dump(dict(found=found, vals=allvals, stats=stats), open(f'../logs/family_neighborhood_{drop}_{seed}.json', 'w'))
