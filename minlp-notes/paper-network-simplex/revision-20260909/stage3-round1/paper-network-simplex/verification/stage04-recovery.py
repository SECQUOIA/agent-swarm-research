"""Exact checks of the new finite-basis bounded-rank recovery construction.

Reuses the existing exact support-library builder, but implements the new
intersection basis library and sequential recovery here. No LP is called.
All returned state vectors are checked against the original unmerged state
inequalities and aggregate identities with Fraction arithmetic.
"""

from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import importlib.util
import json
import random

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "rank_support", ROOT / "code/network-simplex-bounded-rank-verify.py")
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def determinant(a):
    if not a:
        return 1
    return sum((-1) ** j * a[0][j]
               * determinant([row[:j] + row[j + 1:] for row in a[1:]])
               for j in range(len(a)))


def inverse(a, det):
    n = len(a)
    return [[F((-1) ** (i + j) * determinant([
        [a[ii][jj] for jj in range(n) if jj != i]
        for ii in range(n) if ii != j]), det)
        for j in range(n)] for i in range(n)]


def recovery_library(lib):
    m, rays = lib[:2]
    normals = sorted(set(m) | {tuple(-v for v in h) for h in rays})
    rank = len(m[0])
    bases = []
    maxdet = 0
    for ids in combinations(range(len(normals)), rank):
        b = [list(normals[i]) for i in ids]
        d = determinant(b)
        if d:
            inv = inverse(b, d)
            assert all(dot(b[i], [inv[k][j] for k in range(rank)]) == (i == j)
                       for i in range(rank) for j in range(rank))
            bases.append((ids, inv))
            maxdet = max(maxdet, abs(d))
    return normals, bases, maxdet


def recover(lib, rec, endpoints, aggregate):
    m, rays, duals = lib[:3]
    normals, bases, _ = rec
    supports = [[min(sum(q * d[i] for i, q in dual) for dual in choices)
                 for choices in duals] for d in endpoints]
    suffix = [[F(0)] * len(rays) for _ in range(len(endpoints) + 1)]
    for i in range(len(endpoints) - 1, -1, -1):
        suffix[i] = [a + b for a, b in zip(supports[i], suffix[i + 1])]
    remaining = list(aggregate)
    states = []
    attempts = 0
    for i, d in enumerate(endpoints):
        upper = dict(zip(m, d))
        for h, value in zip(rays, suffix[i + 1]):
            normal = tuple(-v for v in h)
            rhs = value - dot(h, remaining)
            upper[normal] = min(upper.get(normal, rhs), rhs)
        rhs = [upper[n] for n in normals]
        found = None
        for ids, inv in bases:
            attempts += 1
            candidate = [dot(row, [rhs[k] for k in ids]) for row in inv]
            if all(dot(n, candidate) <= v for n, v in zip(normals, rhs)):
                found = candidate
                break
        assert found is not None
        assert all(dot(n, found) <= v for n, v in zip(m, d))
        remaining = [a - b for a, b in zip(remaining, found)]
        assert all(dot(h, remaining) <= v for h, v in zip(rays, suffix[i + 1]))
        states.append(found)
    assert not any(remaining)
    assert [sum(t[k] for t in states) for k in range(len(aggregate))] == aggregate
    return states, attempts


def run(name, c, count, seed):
    rng = random.Random(seed)
    lib = BASE.library(c)
    rec = recovery_library(lib)
    m = lib[0]
    rank = len(c[0])
    where = {row: i for i, row in enumerate(m)}
    state_count = maxdenbits = attempts = 0
    for case in range(count):
        n = 25 if case == count - 1 else rng.randint(1, 7)
        raw = [rng.randrange(5) for _ in range(n)]
        if not sum(raw):
            raw[0] = 1
        weights = [F(v, sum(raw)) for v in raw]
        witnesses = [[w * F(rng.randint(-2, 2), 4 * rank) for _ in range(rank)]
                     for w in weights]
        endpoints = []
        for j, (w, point) in enumerate(zip(weights, witnesses)):
            assert all(abs(dot(row, point)) <= w for row in c)
            d = [w] * len(m)
            # Include dimensions 0 through r, random equality slices, and
            # zero-weight states. Fixed normals remain unchanged.
            chosen = list(range(case % (rank + 1)))
            chosen += [e for e in range(rank, len(c)) if rng.random() < .3]
            for e in chosen:
                normal = tuple(c[e])
                value = dot(normal, point)
                d[where[normal]] = value
                d[where[tuple(-v for v in normal)]] = -value
            endpoints.append(d)
        aggregate = [sum(t[k] for t in witnesses) for k in range(rank)]
        states, n_attempts = recover(lib, rec, endpoints, aggregate)
        attempts += n_attempts
        state_count += n
        for w, state in zip(weights, states):
            if not w:
                assert not any(state)
            maxdenbits = max(maxdenbits, *(v.denominator.bit_length() for v in state))
    return {"name": name, "rank": rank, "cases": count, "states": state_count,
            "support_rays": len(lib[1]), "recovery_normals": len(rec[0]),
            "recovery_bases": len(rec[1]), "largest_basis_determinant": rec[2],
            "basis_candidates_tested": attempts, "largest_output_denominator_bits": maxdenbits}


def sharp_k4_checks():
    c = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [-1, 0, 1], [0, -1, -1]]
    arcs = [(1, 2), (1, 3), (2, 3), (0, 1), (0, 2), (0, 3)]
    a = [[int(head == i) - int(tail == i) for tail, head in arcs] for i in range(4)]
    assert all(sum(a[i][e] * c[e][j] for e in range(6)) == 0
               for i in range(4) for j in range(3))
    checked = accepted = 0
    for pnum, qnum in product(range(-7, 8), repeat=2):
        p, q = F(pnum, 768), F(qnum, 768)
        assert abs(p) < F(1, 96) and abs(q) < F(1, 96)
        w = 2 * p + q
        checked += 1
        if w < 0:
            # Exact residual support certificate: h theta0 <= 1/3,
            # h theta2 = 0, h aggregate = 1/3, h theta1 = w.
            assert F(1, 3) - w > F(1, 3)
            continue
        v = [F(1, 2)] * 6
        v[3] = F(1, 4)
        b = [dot(row, v) for row in a]
        assert b == [F(-5, 4), F(-3, 4), F(1, 2), F(3, 2)]
        theta = [[p, q, p], [q / 2, -q / 2, F(0)],
                 [F(1, 6) - p - q / 2, F(1, 24) - q / 2, F(1, 8) - p]]
        flows = [[v[e] / 3 + dot(c[e], t) for e in range(6)] for t in theta]
        assert all(0 <= value <= F(1, 3) for f in flows for value in f)
        assert all([dot(row, f) for row in a] == [value / 3 for value in b] for f in flows)
        aggregate = [sum(f[e] for f in flows) for e in range(6)]
        assert aggregate == [F(2, 3), F(13, 24), F(5, 8), F(11, 24), F(11, 24), F(1, 3)]
        assert flows[0][0] == F(1, 6) + p and flows[0][1] == F(1, 6) + q
        assert flows[0][4] == flows[1][2] == F(1, 6)
        assert flows[1][3] == F(1, 12)
        accepted += 1
    return {"five_product_grid": checked, "exact_witnesses": accepted,
            "exact_negative_support_certificates": checked - accepted}


if __name__ == "__main__":
    graphs = [("cycle", [[1]]), ("theta", [[1, 0], [0, 1], [1, 1]]),
              ("K4", [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [-1, 0, 1], [0, -1, -1]]),
              ("rank4_box", [[int(i == j) for i in range(4)] for j in range(4)])]
    result = {"status": "PASS", "recovery": [run(n, c, 16, 7700 + i)
              for i, (n, c) in enumerate(graphs)], "sharp_k4": sharp_k4_checks()}
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
