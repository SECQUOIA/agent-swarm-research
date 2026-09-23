"""Independent exact quadratic enumeration and numerical envelope falsification."""
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

OUT = Path(__file__).parent
SNAP = OUT.parents[2] / 'process/snapshots/stage01-round02'

def characters(n, edges):
    signs = np.array(list(product((-1, 1), repeat=n)), dtype=np.int64)
    return np.array([signs[:, i] * signs[:, j] for i, j in edges]).T

records = []
for n in range(2, 8):
    edges = list(combinations(range(n), 2))
    free = [k for k, (i, j) in enumerate(edges) if i > 0]
    coeffs = np.ones((2 ** len(free), len(edges)), dtype=np.int64)
    coeffs[:, free] = np.array(list(product((-1, 1), repeat=len(free))), dtype=np.int64)
    values = coeffs @ characters(n, edges).T
    # Every summand is +/-1 and there are at most 21, so int64 cannot overflow.
    ranges = (values.max(axis=1) - values.min(axis=1)) // 2
    keys, counts = np.unique(ranges, return_counts=True)
    records.append(dict(n=n, representatives=len(coeffs), minimum=int(ranges.min()),
                        center=str(Fraction(len(edges), int(ranges.min()))),
                        histogram={str(k): int(v) for k, v in zip(keys, counts)}))
assert [r['minimum'] for r in records] == [1, 2, 4, 4, 5, 8]

witness_edges = {3: [], 4: [], 5: [(1, 2), (1, 4), (2, 3)],
                 6: [(1, 4), (1, 5), (2, 3), (2, 5), (3, 4)],
                 7: [(1, 2), (1, 3), (1, 6), (2, 3), (2, 5), (3, 4)]}
witnesses = []
for n, negative in list(witness_edges.items()) + [(7, witness_edges[6])]:
    edges = list(combinations(range(n), 2))
    a = np.array([-1 if e in negative else 1 for e in edges], dtype=np.int64)
    q = characters(n, edges) @ a
    best = Fraction(0)
    for k in range(2, n + 1):
        for face in combinations(range(n), k):
            subedges = [e for e in edges if all(v in face for v in e)]
            suba = np.array([-1 if e in negative else 1 for e in subedges], dtype=np.int64)
            subq = characters(n, subedges) @ suba
            best = max(best, Fraction(2 * len(subedges), int(subq.max() - subq.min())))
    witnesses.append(dict(n=n, negative=negative, qmin=int(q.min()), qmax=int(q.max()),
                          all_faces=str(best)))
assert [(r['qmin'], r['qmax']) for r in witnesses] == [(-1,3),(-2,6),(-4,4),(-5,5),(-7,9),(-9,11)]
assert witnesses[-1]['all_faces'] == '3'

# Numerical LP searches include zero weights, tiny weights, endpoints and unequal means.
rng = np.random.default_rng(1002)
checks = 0
for n in range(2, 7):
    edges = list(combinations(range(n), 2))
    vertices = np.array(list(product((0, 1), repeat=n)), dtype=float)
    chars = characters(n, edges)
    eq = np.vstack((np.ones(len(vertices)), vertices.T))
    for trial in range(20):
        a = rng.integers(-3, 4, len(edges)).astype(float)
        if trial == 0:
            a[:] = 0
        elif trial == 1:
            a[:] = 1e-6
        face_ratios = [0.0]
        for mask in range(1 << n):
            keep = np.array([bool(mask & (1 << i) and mask & (1 << j)) for i,j in edges])
            q = chars @ (a * keep)
            if np.ptp(q) > 0:
                face_ratios.append(2 * np.abs(a * keep).sum() / np.ptp(q))
        c = max(face_ratios)
        objective = sum(a[k] * vertices[:,i] * vertices[:,j] for k,(i,j) in enumerate(edges))
        for point in [rng.random(n), rng.choice([0.0,0.5,1.0],n), np.full(n, 0.5)]:
            low = linprog(objective, A_eq=eq, b_eq=np.r_[1,point], bounds=(0,None), method='highs')
            high = linprog(-objective, A_eq=eq, b_eq=np.r_[1,point], bounds=(0,None), method='highs')
            assert low.success and high.success
            h = -high.fun-low.fun
            t = sum(abs(a[k])*min(point[i],point[j],1-point[i],1-point[j]) for k,(i,j) in enumerate(edges))
            assert t <= c*h + 1e-8, (n,a,point,t,c,h)
            if np.all(point == 0.5):
                assert abs(h - np.ptp(chars@a)/4) < 1e-8
            checks += 1

# Replay the literal frozen appendix rather than importing its checker.
appendix = (SNAP/'sections/appendix-finite-signings.tex').read_text()
printed = appendix.split('\\begin{verbatim}')[1].split('\\end{verbatim}')[0]
namespace = {}
exec(printed, namespace)
report = dict(exact_enumeration=records, exact_witnesses=witnesses,
              numerical_lp_points=checks, printed_result=namespace['result'],
              limits='Enumeration is exact through K7 only. LP tests use floating point and do not prove universal claims.')
(OUT/'results.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
