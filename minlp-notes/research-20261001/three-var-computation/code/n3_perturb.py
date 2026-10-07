"""Search for objectives where B + all 24 family blocks (BF24) is weaker than the
exact lift X in three variables.  Objectives: pool objectives plus Gaussian
perturbations of relative size sigma (entrywise N(0, (sigma*max|C|)^2) on H, g).
Usage: python n3_perturb.py pool.jsonl out.jsonl seed"""
import sys, json
import numpy as np
sys.path.insert(0, '.')
from n3_study import build

def main():
    pool, out, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
    rng = np.random.default_rng(seed)
    P = [json.loads(l) for l in open(pool)]
    with open(out, 'w') as f:
        for i, r in enumerate(P):
            H0, g0 = np.array(r['H']), np.array(r['g'])
            s = max(np.abs(H0).max(), np.abs(g0).max())
            for sigma in (0.0, 0.03, 0.1, 0.3, 1.0):
                for rep in range(1 if sigma == 0 else 5):
                    E = rng.normal(size=(3, 3)) * sigma * s
                    H = H0 + (E + E.T) / 2
                    g = g0 + rng.normal(size=3) * sigma * s
                    rec = {'i': i, 'sigma': sigma, 'rep': rep, 'H': H.tolist(), 'g': g.tolist(),
                           'npos': int((np.diag(H) > 0).sum())}
                    for parts in ('', 'K', 'KA', 'F', 'X'):
                        res = build(H, g, parts).solve('clarabel', tol=1e-10)
                        rec[parts or 'B'] = res['pobj']; rec[(parts or 'B') + '_safe'] = res['safe']
                    f.write(json.dumps(rec) + '\n'); f.flush()

if __name__ == '__main__':
    main()
