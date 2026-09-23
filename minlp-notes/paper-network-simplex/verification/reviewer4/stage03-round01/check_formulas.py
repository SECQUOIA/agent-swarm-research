"""Independent exact finite checks, without repository implementation imports."""
import itertools as it
import json
from pathlib import Path
import random

rng = random.Random(31415)
normals = [(1, 0), (0, 1), (1, 1)]


def vertices(lo, hi):
    rows = [(a, b, c) for (a, b), l, u in zip(normals, lo, hi) for c in (l, u)]
    ans = set()
    for (a, b, c), (d, e, f) in it.combinations(rows, 2):
        det = a * e - b * d
        if det:
            assert abs(det) == 1
            p = ((c * e - b * f) // det, (a * f - c * d) // det)
            if all(l <= x * p[0] + y * p[1] <= u
                   for (x, y), l, u in zip(normals, lo, hi)):
                ans.add(p)
    return ans


def supports(lo, hi):
    a, b, c = lo
    x, y, z = hi
    return (max(a, c-y), max(b, c-x), max(c, a+b)), (min(x, z-b), min(y, z-a), min(z, x+y))


def choose(lo, hi):
    s = max(lo[0], lo[2]-hi[1])
    t = max(lo[1], lo[2]-s)
    assert all(l <= q <= u for l, q, u in zip(lo, (s, t, s+t), hi))
    return s, t


intervals = list(it.combinations_with_replacement(range(-2, 3), 2))
feasible = []
counts = {"theta_interval_systems": 0, "theta_nonempty": 0,
          "theta_sum_decompositions": 0, "transport_candidates": 0,
          "transport_negative_targets": 0}
for pairs in it.product(intervals, repeat=3):
    lo, hi = tuple(p[0] for p in pairs), tuple(p[1] for p in pairs)
    vs = vertices(lo, hi)
    predicted = all(l <= u for l, u in zip(lo, hi)) and lo[0]+lo[1] <= hi[2] and lo[2] <= hi[0]+hi[1]
    assert bool(vs) == predicted
    counts["theta_interval_systems"] += 1
    if vs:
        low, high = supports(lo, hi)
        for k, (a, b) in enumerate(normals):
            assert low[k] == min(a*s+b*t for s, t in vs)
            assert high[k] == max(a*s+b*t for s, t in vs)
        choose(lo, hi)
        feasible.append((lo, hi, vs))
        counts["theta_nonempty"] += 1

for _ in range(400):
    states = rng.choices(feasible, k=rng.randrange(1, 5))
    ss = [supports(lo, hi) for lo, hi, _ in states]
    total_lo = tuple(sum(s[0][k] for s in ss) for k in range(3))
    total_hi = tuple(sum(s[1][k] for s in ss) for k in range(3))
    for target in vertices(total_lo, total_hi):
        rem = target
        for i, (lo, hi, _) in enumerate(states):
            r = (*rem, sum(rem))
            il = tuple(max(lo[k], r[k]-sum(s[1][k] for s in ss[i+1:])) for k in range(3))
            iu = tuple(min(hi[k], r[k]-sum(s[0][k] for s in ss[i+1:])) for k in range(3))
            p = choose(il, iu)
            assert all(l <= q <= u for l, q, u in zip(lo, (*p, sum(p)), hi))
            rem = tuple(a-b for a, b in zip(rem, p))
        assert rem == (0, 0)
        counts["theta_sum_decompositions"] += 1

for _ in range(200):
    k, d = rng.randrange(2, 5), rng.randrange(1, 4)
    lower = [[rng.randrange(-2, 2) for _ in range(d)] for _ in range(k)]
    upper = [[lower[i][j]+rng.randrange(3) for j in range(d)] for i in range(k)]
    local = all(sum(lower[i][j] for i in range(k)) <= 0 <= sum(upper[i][j] for i in range(k)) for j in range(d))
    totals = {(0,)*k}
    for j in range(d):
        col = [p for p in it.product(*(range(lower[i][j], upper[i][j]+1) for i in range(k))) if sum(p) == 0]
        totals = {tuple(a+b for a, b in zip(t, p)) for t in totals for p in col}
    for _ in range(20):
        first = [rng.randrange(-4, 5) for _ in range(k-1)]
        delta = tuple(first + [-sum(first)])
        ok = local
        for mask in range(1 << k):
            s = [i for i in range(k) if mask >> i & 1]
            comp = [i for i in range(k) if i not in s]
            rhs = sum(min(sum(upper[i][j] for i in s), -sum(lower[i][j] for i in comp)) for j in range(d))
            ok = ok and sum(delta[i] for i in s) <= rhs
        assert ok == (delta in totals)
        counts["transport_candidates"] += 1
        if local and any(delta[i] < sum(lower[i]) for i in range(k)):
            assert not ok
            counts["transport_negative_targets"] += 1

counts["status"] = "PASS"
Path(__file__).with_suffix('.json').write_text(json.dumps(counts, indent=2)+'\n')
print(json.dumps(counts))
