"""Three-variable study on hard objectives (hardobj.py).  For n = 3 the exact
lift X is exact.  Usage: python n3_hard.py plus|any nsamples seed out.jsonl"""
import sys, json
import numpy as np
sys.path.insert(0, '.')
from hardobj import sample_hard
from n3_study import build, METHODS

def main():
    kind, ns, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = np.random.default_rng(seed)
    with open(out, 'w') as f:
        for s in range(ns):
            H, g, c0, info = sample_hard(rng, plus_only=(kind == 'plus'))
            rec = {'kind': kind, 'seed': seed, 's': s, 'H': H.tolist(), 'g': g.tolist(), 'c0': c0, 'info': info}
            for m, parts in METHODS.items():
                R = build(H, g, parts)
                res = R.solve('clarabel', tol=1e-10)
                rec[m] = res['pobj'] + c0; rec[m + '_safe'] = res['safe'] + c0; rec[m + '_st'] = res['status']
                rec[m + '_size'] = R.size()
            f.write(json.dumps(rec) + '\n'); f.flush()

if __name__ == '__main__':
    main()
