"""Summarize c1_fail.jsonl (forced-in / removal upper bounds at low tau^2, n = 800)."""
import json, collections, numpy as np
from scipy.stats import norm
rows = [json.loads(l) for l in open('c1_fail.jsonl')]
d = collections.defaultdict(list)
for r in rows:
    d[(r['p'], round(r['lam'], 1), r['tau2_target'])].append(r)
for key in sorted(d):
    p, lam, t2 = key; v = d[key]; n = v[0]['n']; bl = n / (n + lam); cost = lam * bl ** 2
    c = 2 * np.log(p * lam / n); th = np.mean([r['tau2_hat'] for r in v])
    print(f"p=1e{int(round(np.log10(p)))} lam={lam:5.1f} tau_lam^2={t2:6.2f} (c-{c - t2:4.1f}) tau_hat^2={th:6.2f} "
          f"E#nulls>m0={p * 2 * norm.sf(np.sqrt(th)):10.0f} | fail_frc {np.mean([r['fail_frc'] for r in v]):.1f} "
          f"fail_rem {np.mean([r['fail_rem'] for r in v]):.1f} | median (ub_frc-fS)/(lam b_lam^2) "
          f"{np.median([(r['ub_frc'] - r['fS']) / cost for r in v]):6.2f} | witness {np.mean([r['wit'] for r in v]):.1f}")
