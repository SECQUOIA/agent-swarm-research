"""Reviewer support-<=2 value (a verified feasible upper bound on z_K for any rho) for given records.
Usage: python3 pairs_upper.py INST:K [...]"""
import sys, os, json, gzip
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep_check import build, zk_pairs
import gurobi_fullspace as GF
keys = [(a.split(':')[0], int(a.split(':')[1])) for a in sys.argv[1:]]
S, G = GF.stream_results()
for l in gzip.open(os.path.join(GF.HERE, '../r1-logs/sample_records.jsonl.gz'), 'rt'):
    rec = json.loads(l); key = (rec['inst'], rec['k'])
    if key not in keys:
        continue
    Q, b, c, sbar, P, w, width, nq = build(rec)
    keep = width > 1e-9; P, w = P[:, keep], w[keep]; wf = np.maximum(w, 1e-9 * w.max())
    z, arg, g0 = zk_pairs(Q, b, c, sbar, P, wf)
    print(key, 'reviewer support<=2 value', z, arg, '| stream zK2', S[key]['zK2'], 'stream zK', S[key]['zK'], 'kind', S[key]['zK_kind'],
          'stream gurobi', G.get(key, {}).get('obj'), G.get(key, {}).get('bound'), G.get(key, {}).get('status'))
