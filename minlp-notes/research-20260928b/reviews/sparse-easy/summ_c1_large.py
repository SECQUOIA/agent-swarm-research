"""Summarize c1_large.jsonl: per (p, lam) the fraction of root-exact, witness-certified C1, detected failure."""
import json, collections, numpy as np
rows = [json.loads(l) for l in open('c1_large.jsonl')]
d = collections.defaultdict(list)
for r in rows:
    d[(r['p'], round(r['lam'], 1), r['tau2_target'])].append(r)
cur = None
for key in sorted(d):
    p, lam, t2 = key; v = d[key]; n = v[0]['n']
    if (p, lam) != cur:
        cur = (p, lam)
        print(f"\np=1e{int(round(np.log10(p)))}, lam={lam} (n={n}, n/lam={n/lam:.1f}): 2log(p lam/n)={2*np.log(p*lam/n):.2f}, 2log p={2*np.log(p):.2f}")
        print("  tau_lam^2  mean tau_hat^2 | root exact | witness C1 | fail(frc) fail(rem) | undecided")
    root = np.mean([r['root'] for r in v]); wit = np.mean([r['wit'] for r in v])
    ff = np.mean([r['fail_frc'] for r in v]); fr = np.mean([r['fail_rem'] for r in v])
    und = np.mean([(not r['wit']) and (not r['fail']) for r in v])
    print(f"  {t2:8.2f}   {np.mean([r['tau2_hat'] for r in v]):8.2f}      |   {root:4.1f}     |   {wit:4.1f}     |  {ff:4.1f}      {fr:4.1f}    |  {und:4.1f}")
