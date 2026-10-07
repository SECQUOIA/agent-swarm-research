"""Review r2: independent recomputation of the Lemma A norm-bound certificates.

For each selected record: Y00-scaling, the Lemma A bound
||w||^2 <= floor(1/(4(rho' - eps))) with rho' = rho/Y00 and eps = max(0, -lambda_min(S)) + 1e-9,
then exhaustive enumeration of ALL nonzero w with ||w||^2 <= bound (both signs,
no symmetry reduction), with the best integer v0 found by evaluating q_Y at
the two integers nearest the real minimizer, at the stored (unscaled) matrix.
Records: all 20 capped records with a finite bound <= 3, plus 12 random finished ones.
Usage from split-practice/: python3 reviews/r2-code/r2_certify.py
"""
import itertools
import json
import math
import random
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
recs = [json.loads(l) for k in range(3) for l in open(ROOT / f'logs/sep_run2_s{k}.jsonl')]
logged = {json.loads(l)['file']: json.loads(l) for l in open(ROOT / 'logs/ratio_certificates_r1.jsonl')}


def best_ratio(Y, bound):
    n = Y.shape[0] - 1
    s = Y[0, 0]; x = Y[0, 1:]; X = Y[1:, 1:]
    best, arg = -np.inf, None
    # value patterns: multisets of nonzero integers (with sign) whose squares sum <= bound
    vals = [a for a in range(-math.isqrt(bound), math.isqrt(bound) + 1) if a]
    for k in range(1, bound + 1):
        # enumerate coefficient tuples for support size k, then all supports at once
        tuples = [c for c in itertools.product(vals, repeat=k) if sum(a * a for a in c) <= bound]
        if not tuples:
            break
        S = np.array(list(itertools.combinations(range(n), k)), dtype=int)
        for c in tuples:
            c = np.array(c, float)
            t = x[S] @ c
            quad = np.einsum('i,mij,j->m', c, X[S[:, :, None], S[:, None, :]], c)
            v0 = np.floor(-t / s - 0.5)
            q = np.minimum.reduce([s * u * u + 2 * u * t + u * s + quad + t for u in (v0 - 1, v0, v0 + 1, v0 + 2)])
            ratio = -q / float(c @ c)
            i = int(np.argmax(ratio))
            if ratio[i] > best:
                best, arg = float(ratio[i]), (S[i].tolist(), c.tolist())
    return best, arg


rng = random.Random(7)
capped = [d for d in recs if not d['ratio']['complete']]
finished = [d for d in recs if d['ratio']['complete'] and d['ratio']['ratio'] > 0]
sample = capped + rng.sample(finished, 12)
n_ok = 0
for d in sample:
    t0 = time.time()
    f = d['file']; n = f.split('_n')[1].split('_')[0]
    Y = np.load(ROOT / f'data/points_{"BT" if f.startswith("bt") else "DM"}{n}/{f}')['Y']
    Y = (Y + Y.T) / 2
    s = Y[0, 0]
    Ys = Y / s
    S = Ys[1:, 1:] - np.outer(Ys[0, 1:], Ys[0, 1:])
    eps = max(0.0, -float(np.linalg.eigvalsh(S)[0])) + 1e-9
    rho = d['ratio']['ratio']
    if rho / s <= eps:
        print(f, 'no finite bound'); continue
    bound = math.floor(1 / (4 * (rho / s - eps)))
    if bound > 3:
        print(f'{f}: capped={not d["ratio"]["complete"]} bound {bound} > 3, not enumerated here '
              f'(logged bound {logged[f].get("bound")}, status {logged[f]["status"]})')
        continue
    best, arg = best_ratio(Y, bound)
    excess = best - rho
    ok = excess <= 1e-6
    n_ok += ok
    lg = logged[f]
    print(f'{f}: capped={not d["ratio"]["complete"]} rho={rho:.12g} bound={bound} (logged {lg.get("bound")}) '
          f'max={best:.12g} excess={excess:.3g} (logged {lg.get("excess")}) certified={ok} argmax={arg} {time.time() - t0:.1f}s',
          flush=True)
print('certified in this sample:', n_ok)
