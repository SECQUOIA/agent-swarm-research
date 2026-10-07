"""For records where the reviewer's full-space Gurobi optimum exceeds the stream's z_K, re-solve with the
quadratic constraint relaxed to q <= TOL * q(sbar) (the stream's candidate acceptance tolerance is
q <= 1e-3 q(sbar) + 1e-10 scale) to test whether that tolerance explains the difference.
Usage: python3 gurobi_relaxed.py TOL INST:K [...]"""
import sys, os, json, gzip
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep_check import build
import gurobi_fullspace as GF
tol = float(sys.argv[1]); keys = [(a.split(':')[0], int(a.split(':')[1])) for a in sys.argv[2:]]
S, G = GF.stream_results()
for l in gzip.open(os.path.join(GF.HERE, '../r1-logs/sample_records.jsonl.gz'), 'rt'):
    rec = json.loads(l); key = (rec['inst'], rec['k'])
    if key not in keys:
        continue
    Q, b, c, sbar, P, w, width, nq = build(rec)
    keep = width > 1e-9; P, w = P[:, keep], w[keep]; wf = np.maximum(w, 1e-9 * w.max())
    q0 = float(sbar @ Q @ sbar + b @ sbar + c)
    cap = 4 * S[key]['zK']
    _, res = GF.solve((key, Q, b, c - tol * q0, sbar, P, wf, cap, 60))
    g = G.get(key, {})
    print(key, 'tol', tol, 'relaxed optimum', res['obj'], 'bound', res['bound'], res['status'], '| stream zK', S[key]['zK'], 'stream gurobi obj', g.get('obj'))
