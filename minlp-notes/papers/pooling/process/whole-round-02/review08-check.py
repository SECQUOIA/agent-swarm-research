"""Finite exact checks for round-2 reviewer 08; not a proof of the theorems."""
from itertools import product
from pathlib import Path
from random import Random
import hashlib
import re

rng = Random(208)
feasible_count = 0
for case in range(1200):
    n = rng.randrange(1, 7)
    undirected = [(i, i + 1) for i in range(n - 1)]
    if n >= 3 and case % 3 == 0:
        undirected.append((n - 1, 0))
    edges = [(a, b) if rng.randrange(2) else (b, a) for a, b in undirected]
    lo = [rng.randrange(-2, 2) for _ in edges]
    hi = [l + rng.randrange(3) for l in lo]
    alpha = [rng.randrange(-4, 3) for _ in range(n)]
    beta = [a + rng.randrange(5) for a in alpha]
    divergences = []
    for w in product(*(range(l, u + 1) for l, u in zip(lo, hi))):
        d = [0] * n
        for (a, b), t in zip(edges, w):
            d[a] += t
            d[b] -= t
        if all(a <= x <= b for a, x, b in zip(alpha, d, beta)):
            divergences.append(d)
    def upper_cut(mask):
        return sum(u if (mask >> a & 1) else -l
                   for (a, b), l, u in zip(edges, lo, hi)
                   if (mask >> a & 1) != (mask >> b & 1))
    def lower_cut(mask):
        return sum(l if (mask >> a & 1) else -u
                   for (a, b), l, u in zip(edges, lo, hi)
                   if (mask >> a & 1) != (mask >> b & 1))
    def subset_sum(values, mask):
        return sum(x for i, x in enumerate(values) if mask >> i & 1)
    cuts = all(subset_sum(alpha, s) <= upper_cut(s)
               and subset_sum(beta, s) >= lower_cut(s) for s in range(1 << n))
    assert cuts == bool(divergences), (case, edges, lo, hi, alpha, beta)
    if not divergences:
        continue
    feasible_count += 1
    all_mask = (1 << n) - 1
    def g(s):
        return min(upper_cut(t) + subset_sum(beta, s & ~t)
                   - subset_sum(alpha, t & ~s) for t in range(1 << n))
    assert g(0) == g(all_mask) == 0
    costs = [rng.randrange(-4, 5) for _ in range(n)]
    order = sorted(range(n), key=lambda i: -costs[i])
    mask = 0
    greedy = [0] * n
    for i in order:
        old = g(mask)
        mask |= 1 << i
        greedy[i] = g(mask) - old
    assert greedy in divergences
    assert sum(c * d for c, d in zip(costs, greedy)) == max(
        sum(c * x for c, x in zip(costs, d)) for d in divergences)
print(f"1200 exact integer-flow/cut comparisons passed; {feasible_count} feasible cases also passed box-rank greedy support checks.")
print("Integer enumeration is independent finite evidence; incidence integrality connects these integer-data examples to real feasibility.")

root = Path('papers/pooling/process/snapshots/whole-round-02')
index = (root / 'source-index.md').read_text()
sources = re.findall(r'Source: \[`([^`]+)`\].*?SHA256: `([^`]+)`', index, re.S)
for path, digest in sources:
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, path
tex = '\n'.join(p.read_text() for p in (root / 'sections').glob('*.tex'))
cited = set()
for m in re.finditer(r'\\cite\w*\s*(?:\[[^\]]*\]\s*)*\{([^}]+)\}', tex):
    cited.update(x.strip() for x in m[1].split(','))
keys = re.findall(r'@\w+\{([^,]+),', (root / 'bibliography.bib').read_text())
assert len(keys) == len(set(keys))
assert cited == set(keys)
print(f"All {len(sources)} adjacent-source hashes match; all {len(keys)} bibliography keys are cited, unique, and resolved.")
