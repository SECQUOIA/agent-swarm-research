"""Stronger tests of Theorem 5.1 (vertex localization under CND) and Theorem 5.4
(face localization under ND1), designed so that removals occur.

(5') linediag expanded, y = (t+1+u, t) with t in [0.3, 1.1], |u| <= 0.012
     (m(y) + eps < theta = 4.3e-3).  Box distances from y to its faces drawn in
     [0, 4 r] with r = 2(m(y)+eps)/D(y), D(y) = min_i D_i(y); some coordinates
     get large distances.  Check: y removed => d_i^C(y) < r for every i.
(6') iso2 / rot0.1 expanded, point x* or a nearby point; one coordinate thin
     (both sides log-uniform in [1e-3 eps, eps]), the other wide.  Check: removed =>
     min_i d_i^C(y) < 2(m(y)+eps)/L0 with L0 = 7.9 (L = 8 at x*).
Run: python3 loc_check.py > logs/loc_check.log
"""
import numpy as np
import inst as I
from loss_check import DL, removed

rng = np.random.default_rng(17)
d = I.make('linediag'); dag = d['reps']['exp']
for eps in (1e-4, 1e-5):
    stats = dict(boxes=0, removed=0, violations=0, removed_all_small=0, removed_with_both_sides_small=0)
    ratio = []
    for trial in range(400):
        t = rng.uniform(0.3, 1.1); u = rng.uniform(-0.012, 0.012)
        yv = [t + 1.0 + u, t]
        m = dag.f(yv)
        D, _ = DL(d['f'], d['syms'], yv)
        r = 2 * (m + eps) / D.min()
        draw = lambda: r * 10 ** rng.uniform(-3, 0.6) if rng.random() < 0.85 else rng.uniform(0, 0.2)
        dist = [(draw(), draw()) for _ in range(2)]
        box = [(yv[i] - dist[i][0], yv[i] + dist[i][1]) for i in range(2)]
        dC = [min(dd) for dd in dist]
        rem, st = removed(dag, box, yv, -eps, R=60000)
        stats['boxes'] += 1
        if rem:
            stats['removed'] += 1
            ratio.append(max(dC) / r)
            if not all(di < r for di in dC):
                stats['violations'] += 1
                print('  VIOLATION', yv, box, dC, r, st)
            if all(max(dd) < r for dd in dist):
                stats['removed_with_both_sides_small'] += 1
    print(f'(5\') eps={eps:.0e}: {stats}; max over removed of max_i d_i / r = {max(ratio) if ratio else float("nan"):.3f}')

for name in ('iso2', 'rot0.1'):
    d = I.make(name); dag = d['reps']['exp']; xs = d['xstar']
    for eps in (1e-3, 1e-4):
        stats = dict(boxes=0, removed=0, violations=0)
        worst = 0.0
        for trial in range(200):
            off = rng.uniform(-0.3, 0.3, size=2) * np.sqrt(eps)
            yv = [xs[0] + off[0], xs[1] + off[1]]
            m = dag.f(yv)
            if m + eps > 3 * eps:
                continue
            thin = rng.integers(0, 2)
            dist = []
            for i in range(2):
                if i == thin:
                    dist.append((eps * 10 ** rng.uniform(-3, 0), eps * 10 ** rng.uniform(-3, 0)))
                else:
                    dist.append((rng.uniform(0.001, 0.4), rng.uniform(0.001, 0.4)))
            box = [(yv[i] - dist[i][0], yv[i] + dist[i][1]) for i in range(2)]
            dC = [min(dd) for dd in dist]
            rem, st = removed(dag, box, yv, -eps, R=60000)
            stats['boxes'] += 1
            if rem:
                stats['removed'] += 1
                bound = 2 * (m + eps) / 7.9
                worst = max(worst, min(dC) / bound)
                if not min(dC) < bound:
                    stats['violations'] += 1
                    print('  VIOLATION', name, yv, box, dC, bound)
        print(f'(6\') {name} eps={eps:.0e}: {stats}; max over removed of min_i d_i / bound = {worst:.3f}')
