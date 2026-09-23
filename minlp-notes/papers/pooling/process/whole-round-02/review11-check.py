"""Independent finite exact checks for whole-paper reviewer 11.

These rational certificates supplement the general proofs; they do not prove
the asymptotic claims or verify a numerical optimizer.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import re


def vertices(n, eps):
    result = []
    for bits in product((0, 1), repeat=n):
        x = []
        prev = Q(0)
        for bit in bits:
            prev = bit + (1 - 2 * bit) * eps * prev
            x.append(prev)
        result.append((bits, x))
    return result


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


count = 0
for n in range(2, 8):
    eps = Q(1, 4)
    vs = vertices(n, eps)
    d = [(1 - eps) * eps ** (2 * (n - j) - 1)
         for j in range(1, n)] + [Q(0)]
    assert len({x[-1] for _, x in vs}) == 2 ** n
    for bits, x in vs:
        t = x[-1]
        z = t - t * t
        assert dot(d, x) == z
        # Independently check all physical interface balances and quality.
        an, ap, bp, bw, pw, pv = 1 - t, t, 1 - t, t, 1 - t, t
        q = ap + 2 * bp
        assert an + ap == bp + bw == ap + bp == pw + pv == 1
        assert t + an == bw + pw == 1
        assert q * pv == pv + z
        assert all(0 <= f <= 1 for f in (an, ap, bp, bw, pw, pv, z))
        expose = d[:-1] + [2 * t - 1]
        for other_bits, y in vs:
            if bits != other_bits:
                assert dot(expose, x) > dot(expose, y)
            # All edge derivatives of perturbed profit are negative.
            if sum(a != b for a, b in zip(bits, other_bits)) == 1:
                dt = y[-1] - t
                assert -dt * dt + Q(1, 4 ** n) * dt < 0
        count += 1
    # Convex combinations give explicit physical hull decompositions.
    for (_, x), (_, y) in zip(vs, vs[1:]):
        mid = [(a + b) / 2 for a, b in zip(x, y)]
        lower = dot(d, mid)
        assert lower == (dot(d, x) + dot(d, y)) / 2
        assert lower <= mid[-1] - mid[-1] ** 2

slabs = 0
for n in range(1, 5):
    for weights in product(range(1, 4), repeat=n):
        total = sum(weights)
        vs = vertices(n, Q(1, 8 * total))
        for target in range(total + 1):
            subset_yes = any(dot(weights, bits) == target for bits, _ in vs)
            slab_yes = any(abs(dot(weights, x) - target) <= Q(1, 4)
                           for _, x in vs)
            assert subset_yes == slab_yes
            slabs += 1

snapshot = Path('papers/pooling/process/snapshots/whole-round-02')
manifest = json.loads((snapshot / 'manifest.json').read_text())
for file, digest in manifest.items():
    assert hashlib.sha256((snapshot / file).read_bytes()).hexdigest() == digest
index = (snapshot / 'source-index.md').read_text()
pairs = re.findall(r'Source: \[`([^`]+)`\].*?SHA256: `([0-9a-f]+)`', index, re.S)
for file, digest in pairs:
    assert hashlib.sha256(Path(file).read_bytes()).hexdigest() == digest

print(f'PASS: {count} physical vertex/exposure certificates, n=2,...,7.')
print('PASS: every incident-edge strict local derivative and adjacent-pair hull lift.')
print(f'PASS: {slabs} exhaustive small SUBSET SUM/slab equivalences.')
print(f'PASS: {len(manifest)} snapshot files and {len(pairs)} indexed-source hashes.')
print('All arithmetic exact; finite checks supplement, not replace, the proofs.')
