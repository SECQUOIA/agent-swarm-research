"""Exact finite checks independent of all repository oracle implementations."""
from itertools import product
from pathlib import Path
import json
import random

counts = dict(theta_boxes=0, nonempty_theta_boxes=0, transportation_instances=0,
              transportation_targets=0, feasible_transportation_targets=0)
intervals = [(a, b) for a in range(-2, 3) for b in range(a, 3)]
for si, ti, hi in product(intervals, repeat=3):
    ls, us = si
    lt, ut = ti
    lh, uh = hi
    points = [(s, t) for s in range(ls, us + 1) for t in range(lt, ut + 1)
              if lh <= s + t <= uh]
    counts['theta_boxes'] += 1
    assert bool(points) == (ls + lt <= uh and lh <= us + ut)
    if not points:
        continue
    counts['nonempty_theta_boxes'] += 1
    amin = [max(ls, lh - ut), max(lt, lh - us), max(lh, ls + lt)]
    bmax = [min(us, uh - lt), min(ut, uh - ls), min(uh, us + ut)]
    forms = [[s for s, t in points], [t for s, t in points], [s + t for s, t in points]]
    assert amin == [min(v) for v in forms]
    assert bmax == [max(v) for v in forms]
    s = max(ls, lh - ut)
    t = max(lt, lh - s)
    assert (s, t) in points

rng = random.Random(8675309)
for trial in range(120):
    k = rng.randrange(2, 5)
    d = rng.randrange(1, 4)
    lower, upper, column_options = [], [], []
    for j in range(d):
        feasible_column = [rng.randrange(-1, 2) for _ in range(k - 1)]
        feasible_column.append(-sum(feasible_column))
        lo = [v - rng.randrange(2) for v in feasible_column]
        up = [v + rng.randrange(2) for v in feasible_column]
        lower.append(lo)
        upper.append(up)
        column_options.append([v for v in product(*(range(a, b + 1) for a, b in zip(lo, up)))
                               if sum(v) == 0])
    possible = {(0,) * k}
    for options in column_options:
        possible = {tuple(a + b for a, b in zip(u, v)) for u in possible for v in options}
    targets = set(possible)
    for _ in range(60):
        delta = [rng.randrange(-5, 6) for _ in range(k - 1)]
        delta.append(-sum(delta))
        targets.add(tuple(delta))
    subsets = [set(i for i, flag in enumerate(mask) if flag) for mask in product([0, 1], repeat=k)]
    for delta in targets:
        passes = all(sum(delta[i] for i in S) <= sum(
            min(sum(upper[j][i] for i in S), -sum(lower[j][i] for i in range(k) if i not in S))
            for j in range(d)) for S in subsets)
        assert passes == (delta in possible), (lower, upper, delta)
        counts['transportation_targets'] += 1
        counts['feasible_transportation_targets'] += passes
    counts['transportation_instances'] += 1
Path(__file__).with_suffix('.json').write_text(json.dumps(counts, indent=2) + '\n')
print(counts)
