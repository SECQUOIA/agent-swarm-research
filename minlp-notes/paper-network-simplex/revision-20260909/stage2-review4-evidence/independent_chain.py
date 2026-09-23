"""Independent exact profile checks against the full path/simplex hull.

No author or production verification code is imported. Circuit enumeration
and recovered lifts use exact arithmetic; scipy comparisons are numerical.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json
import math
import random
import numpy as np
import sympy as sp
from scipy.optimize import linprog


def primitive(v):
    den = math.lcm(*(int(x.q) for x in v))
    nums = [int(x * den) for x in v]
    g = math.gcd(*nums)
    return tuple(x // g for x in nums)


normals = sorted(set(product((0, 1), repeat=3)) - {(0, 0, 0)} |
                 {(-1, 0, 0), (0, -1, 0), (0, 0, -1), (-1, -1, -1)})
circuits = []
for size in range(2, 5):
    for rows in combinations(normals, size):
        ker = sp.Matrix(rows).T.nullspace()
        if len(ker) != 1:
            continue
        vec = ker[0]
        if all(x < 0 for x in vec):
            vec = -vec
        if all(x > 0 for x in vec):
            circuits.append((rows, primitive(vec)))
assert len(circuits) == 16
assert sorted(sum(w) for _, w in circuits) == [2]*4 + [3]*6 + [4]*5 + [5]

bases = []
for rows in combinations(normals, 3):
    a = sp.Matrix(rows)
    if a.det():
        bases.append((rows, tuple(tuple(F(v) for v in a.inv().row(i)) for i in range(3))))


def profile(L, x, y, obs, z):
    lam = [1-sum(y), *y]
    total = 1-x[-1]
    grouped = {}
    scalar_ok = True

    def put(row, rhs):
        nonlocal scalar_ok
        # Substitute w0 = total - w1 - w2 - w3 into raw rows.
        n = tuple(row[j]-row[0] for j in range(1, 4))
        r = rhs-row[0]*total
        if not any(n):
            scalar_ok &= r >= 0
        else:
            assert n in normals
            grouped[n] = min(grouped.get(n, r), r)

    def singleton(j, sign, rhs):
        row = [0]*4
        row[j] = sign
        put(row, rhs)

    for j in range(4):
        singleton(j, 1, lam[j])
        singleton(j, -1, 0)
    for (e, j), val in z.items():
        if e == 2*L:
            singleton(j, 1, lam[j]-val)
            singleton(j, -1, val-lam[j])
    classes = []
    for i in range(L):
        low = F(0)
        B, U = [], []
        for j in range(4):
            a, b = z.get((2*i, j)), z.get((2*i+1, j))
            if a is None and b is None:
                U.append(j)
            elif a is None:
                B.append(j)
                low -= b
                singleton(j, -1, -b)
            elif b is None:
                low += a
                singleton(j, -1, -a)
            else:
                low += a
                singleton(j, 1, a+b)
                singleton(j, -1, -a-b)
        # The achievable a-aggregate is [low + sum_B w, low + sum_(B+U) w].
        put([int(j in B) for j in range(4)], x[2*i]-low)
        put([-int(j in B+U) for j in range(4)], low-x[2*i])
        classes.append((B, U, low))
    ok = scalar_ok and all(val >= 0 for val in z.values())
    for rows, weights in circuits:
        if all(n in grouped for n in rows):
            ok &= sum(w*grouped[n] for n, w in zip(rows, weights)) >= 0
    if not ok:
        return False, None
    for rows, inv in bases:
        if not all(n in grouped for n in rows):
            continue
        rhs = [grouped[n] for n in rows]
        p = [sum(v*r for v, r in zip(row, rhs)) for row in inv]
        if all(sum(a*b for a, b in zip(n, p)) <= r for n, r in grouped.items()):
            w = [total-sum(p), *p]
            break
    else:
        raise AssertionError('Circuit acceptance had no exact profile vertex')
    flows = [[F(0)]*(2*L+1) for _ in range(4)]
    for i, (B, U, low) in enumerate(classes):
        need = x[2*i]-low-sum(w[j] for j in B)
        for j in range(4):
            a, b = z.get((2*i, j)), z.get((2*i+1, j))
            if a is not None:
                value = a
            elif b is not None:
                value = w[j]-b
            else:
                value = min(need, w[j])
                need -= value
            flows[j][2*i] = value
            flows[j][2*i+1] = w[j]-value
        assert need == 0
    for j in range(4):
        flows[j][-1] = lam[j]-w[j]
        assert all(0 <= v <= lam[j] for v in flows[j])
        assert all(flows[j][2*i]+flows[j][2*i+1]+flows[j][-1] == lam[j] for i in range(L))
    assert all(sum(f[e] for f in flows) == x[e] for e in range(2*L+1))
    assert all(flows[j][e] == value for (e, j), value in z.items())
    return True, flows


rng = random.Random(9442026)
counts = dict(queries=0, accepted_exact_lifts=0, rejected_exact_tests=0,
              zero_weights=0, zero_chain_flow=0, zero_bypass=0, numerical_disagreements=0)
for L in (1, 2, 3, 4):
    paths = []
    for bits in product((0, 1), repeat=L):
        paths.append([int(k % 2 == bits[k//2]) for k in range(2*L)] + [0])
    paths.append([0]*(2*L)+[1])
    for case in range(100):
        density = (case % 5)/4
        obs = [(e, j) for e in range(2*L+1) for j in range(1, 4)
               if rng.random() < density]
        vertices = []
        for state in range(4):
            for p in paths:
                vertices.append(tuple(p + [int(state == j) for j in range(1, 4)] +
                                      [p[e]*int(state == j) for e, j in obs]))
        mass = [rng.randrange(4) for _ in vertices]
        if case % 7 == 0:
            mass[:len(paths)] = [0]*len(paths)
            mass[len(paths):2*len(paths)] = [0]*len(paths)
        if case % 11 == 0:
            mass = [int(i % len(paths) == len(paths)-1) for i in range(len(vertices))]
        if case % 13 == 0:
            mass = [int(i % len(paths) != len(paths)-1) for i in range(len(vertices))]
        den = sum(mass)
        query = [sum(F(m)*v[k] for m, v in zip(mass, vertices))/den
                 for k in range(len(vertices[0]))]
        x, y = query[:2*L+1], query[2*L+1:2*L+4]
        if case % 2 and obs:
            k = rng.randrange(len(obs))
            query[2*L+4+k] += F(rng.choice((-3, -1, 1, 3)), 50)
        z = dict(zip(obs, query[2*L+4:]))
        ok, _ = profile(L, x, y, obs, z)
        Aeq = np.array([[float(v[k]) for v in vertices] for k in range(len(query))] + [[1.]*len(vertices)])
        rhs = np.array([float(v) for v in query] + [1.])
        raw = linprog(np.zeros(len(vertices)), A_eq=Aeq, b_eq=rhs, bounds=(0, None), method='highs')
        assert raw.status in (0, 2), raw.message
        counts['numerical_disagreements'] += (ok != raw.success)
        assert ok == raw.success, (L, case, ok, raw.message)
        counts['queries'] += 1
        counts['accepted_exact_lifts' if ok else 'rejected_exact_tests'] += 1
        counts['zero_weights'] += any(v == 0 for v in [1-sum(y), *y])
        counts['zero_chain_flow'] += x[-1] == 1
        counts['zero_bypass'] += x[-1] == 0
out = dict(circuits=[{'rows': rows, 'weights': weights} for rows, weights in circuits],
           basis_count=len(bases), results=counts)
Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(counts, indent=2))
