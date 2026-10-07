"""Is the tiny entry that triggers SCIP's dynamism abort rounding noise?
For sample records that failed with 'numerics' (dynamism) on piece 1-3/4a, take the failing ray r and
SCIP's own eigendecomposition (dumped).  A = sum_{I-} |theta_i| (v_i.r)^2 (+ wray^2/(4 sqrt(1+kappa^2)) in
Case 4) and B are built from the components v_i.r (i in I-) and wray.  A component is 'noise' if
|v_i.r| <= 1e-12 * sum_k |V_ik r_k| (i.e. at the level of rounding in the dot product).  If every
such component is noise, A and B are zero up to rounding and the abort is caused by rounding.
Reports the counts, and the dynamism ratio min/max(|A|,|B|,|C|) for both groups.
Usage: python3 dyn_noise.py"""
import os, json, gzip, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
res = collections.Counter(); ratios = collections.defaultdict(list)
for l in gzip.open(os.path.join(HERE, '../r1-logs/sample_records.jsonl.gz'), 'rt'):
    rec = json.loads(l)
    if rec.get('fail') != 'numerics' or rec['set'] != 'minlplib':
        continue
    fe = [e for e in rec['perray'] if e.get('fail')]
    if not fe:
        continue
    e = fe[0]; co = np.array(e['c1234a'][:3], float)
    nz = np.abs(co[co != 0])
    if nz.size == 0 or nz.max() / nz.min() < 1e15:
        res['fails on 4b piece'] += 1
        continue
    nq = rec['nquad']; sf = rec['sidefactor']
    th = sf * np.array(rec['eigval'], float); V = np.array(rec['eigvec'], float).reshape(nq, nq)   # row i = eigvector i
    r = np.zeros(rec['nv'])
    for k, v in rec['rays'][e['i']]:
        r[k] = v
    rq = r[:nq]
    comp = V @ rq; scale = np.abs(V) @ np.abs(rq)
    neg = th < -1e-9; zero = np.abs(th) <= 1e-9
    noisy_y = bool(np.all(np.abs(comp[neg]) <= 1e-12 * np.maximum(scale[neg], 1e-300)))
    ok = noisy_y
    if rec['case4']:
        vb = np.array(rec['vb'], float)
        terms = list(vb[zero] * comp[zero]) + list(sf * np.array(rec['lincoefs'], float) * r[nq:nq + rec['nlin']])
        tscale = list(np.abs(vb[zero]) * scale[zero]) + [abs(t) for t in terms[len(vb[zero]):]]
        if rec['auxvar'] is not None:
            terms.append(-sf * r[-1]); tscale.append(abs(r[-1]))
        wray = sum(terms); ws = sum(tscale)
        ok = ok and (abs(wray) <= 1e-12 * max(ws, 1e-300))
    key = 'A,B consistent with 0 (noise)' if ok else 'A or B genuinely nonzero'
    res[key] += 1; ratios[key].append(nz.min() / nz.max())
print(dict(res))
for k, v in ratios.items():
    v = np.array(v); print(k, 'dynamism ratio quantiles 10/50/90%:', np.quantile(v, [.1, .5, .9]))
