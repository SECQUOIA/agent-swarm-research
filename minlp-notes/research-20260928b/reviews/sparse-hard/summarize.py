"""Summaries of e2.jsonl (pure noise vs planted, exact cliques, C1 halves) and e3.jsonl (SNR scan)."""
import json, sys
import numpy as np
from collections import defaultdict
from cliquelib import instance_author

D = '/home/sgusev/repo/minlp-notes/research-20260928b/reviews/sparse-hard/'


def e2():
    rows = [json.loads(l) for l in open(D + 'e2.jsonl')]
    g = defaultdict(list)
    for r in rows:
        g[(r['p'], r['k'], r['alpha'], r['b'])].append(r)
    print("E2: exact clique number over ALL k-subsets (10 seeds per cell)")
    print("p k alpha b n | omega median [min,max] | S* optimal | removal half holds/fails/undet | forced half holds | C1 holds | max member rank of f | max member feature rank by |x'y|")
    viol = 0; checked = 0
    for key in sorted(g):
        rs = g[key]
        om = [r['omega'] for r in rs]
        rem = [r.get('removal') for r in rs]
        frc = [r.get('forced') for r in rs]
        c1 = sum(1 for a, b in zip(rem, frc) if a == 'holds' and b == 'holds')
        # feature ranks of clique members
        fr = []
        for r in rs:
            X, y, S = instance_author(r['n'], r['p'], r['k'], b=r['b'], sigma=0.5, seed=r['seed'])
            c = np.abs(X.T @ y); rank = np.empty(r['p'], int); rank[np.argsort(-c)] = np.arange(r['p'])
            fr.append(max(rank[j] for cl in r['clique'] for j in cl) + 1 if r['omega'] > 1 else 0)
        for r in rs:
            if r.get('removal') == 'holds':
                checked += 1
                if r['omega'] > r['k'] + 1:
                    viol += 1
        print(key, rs[0]['n'], "| %.1f [%d,%d] | %d/10 | %d/%d/%d | %d | %d | %d | median %s max %d" % (
            np.median(om), min(om), max(om), sum(r['rec'] for r in rs),
            rem.count('holds'), rem.count('fails'), rem.count('undetermined'), frc.count('holds'), c1,
            max(r['clique_max_rank'] for r in rs), np.median(fr), max(fr)))
    print("Lemma 1.3 consistency: instances with removal half certified: %d; of these with omega > k+1: %d" % (checked, viol))


def e3():
    rows = [json.loads(l) for l in open(D + 'e3.jsonl')]
    g = defaultdict(list)
    for r in rows:
        g[r['kappa_s']].append(r)
    x = rows[0]['x']
    print("\nE3: total-SNR scan, p=30, k=3, n=%d, x=2 log C(p,k)/n=%.3f, e^{-x}(1+2x)-1=%.3f, lam=sqrt(n)" % (
        rows[0]['n'], x, np.exp(-x) * (1 + 2 * x) - 1))
    print("kappa_s | omega median [min,max] | S* optimal | cliques disjoint from S*")
    for kap in sorted(g):
        rs = g[kap]; om = [r['omega'] for r in rs]
        print("%5.2f | %.1f [%d,%d] | %d/%d | %d/%d" % (kap, np.median(om), min(om), max(om),
              sum(r['rec'] for r in rs), len(rs), sum(r['disjoint_from_Sstar'] for r in rs), len(rs)))


if __name__ == '__main__':
    which = sys.argv[1:] or ['e2', 'e3']
    if 'e2' in which:
        e2()
    if 'e3' in which:
        e3()
