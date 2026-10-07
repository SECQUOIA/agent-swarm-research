"""Three-variable study (other methods are solved only when X - B > 1e-7 max(1,|X|)): random objectives min x'Hx + g'x over [0,1]^3.
For n = 3 the exact lift X is exact, so each relaxation's gap is measured
against the true minimum.  All constraint families are added in full
(4 triangles, K, A, all 24 family orientations).
Usage: python n3_study.py dist nsamples seed out.jsonl"""
import sys, json, itertools, time
import numpy as np
sys.path.insert(0, '.')
from relax import Relax, ORIENTS

def build(H, g, parts):
    R = Relax(H, g)
    T = (0, 1, 2)
    for t in range(4):
        R.add_triangle(0, 1, 2, t)
    if 'K' in parts: R.add_K(T)
    if 'A' in parts: R.add_A(T)
    if 'F' in parts:
        for o in ORIENTS: R.add_F(T, o)
    if 'X' in parts: R.add_X(T)
    return R

METHODS = {'B': '', 'K': 'K', 'A': 'A', 'KA': 'KA', 'F': 'F', 'KAF': 'KAF', 'X': 'X'}

def sample(dist, rng):
    if dist == 'gauss_plus':
        H = rng.normal(size=(3, 3)); H = (H + H.T) / 2
        np.fill_diagonal(H, np.abs(np.diag(H)))
        g = rng.normal(size=3)
    elif dist == 'gauss_mixed':
        H = rng.normal(size=(3, 3)); H = (H + H.T) / 2
        g = rng.normal(size=3)
    elif dist == 'gauss_plus_centered':
        H = rng.normal(size=(3, 3)); H = (H + H.T) / 2
        np.fill_diagonal(H, np.abs(np.diag(H)))
        c = rng.random(3)
        g = -2 * H @ c + 0.1 * rng.normal(size=3)
    elif dist == 'int_plus':
        H = np.zeros((3, 3))
        for i in range(3):
            H[i, i] = rng.integers(1, 51)
            for j in range(i + 1, 3):
                H[i, j] = H[j, i] = rng.integers(-50, 51)
        g = rng.integers(-50, 51, size=3).astype(float)
    return H, g

def main():
    dist, ns, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = np.random.default_rng(seed)
    with open(out, 'w') as f:
        for s in range(ns):
            H, g = sample(dist, rng)
            rec = {'dist': dist, 'seed': seed, 's': s, 'H': H.tolist(), 'g': g.tolist()}
            for m in ['B', 'X'] + [m for m in METHODS if m not in ('B', 'X')]:
                if m not in ('B', 'X') and rec['X'] - rec['B'] <= 1e-7 * max(1.0, abs(rec['X'])):
                    break
                parts = METHODS[m]
                R = build(H, g, parts)
                res = R.solve('clarabel', tol=1e-10)
                rec[m] = res['pobj']; rec[m + '_safe'] = res['safe']; rec[m + '_st'] = res['status']
            f.write(json.dumps(rec) + '\n'); f.flush()

if __name__ == '__main__':
    main()
