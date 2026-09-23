"""Hypergraph / coefficient families for the term-by-term ratio experiments."""
from __future__ import annotations

import itertools
import random

from envelopes import Multilinear


def complete(n, k, coef=1.0):
    """Complete k-uniform hypergraph K_n^(k) (k=2: complete graph, k=3: all triangles)."""
    return Multilinear(n, [(coef, t) for t in itertools.combinations(range(n), k)])


def complete_mixed(n, degrees, coefs=None):
    """All subsets of the given sizes, e.g. degrees=(2,3): K_n edges + all triangles."""
    coefs = coefs or {k: 1.0 for k in degrees}
    terms = [(coefs[k], t) for k in degrees for t in itertools.combinations(range(n), k)]
    return Multilinear(n, terms)


def cone(n, k=3, apex=1):
    """Star/cone: every term contains the `apex` fixed vertices; the rest is complete (k-apex)-uniform
    on the remaining n-apex vertices. k=3, apex=1: terms {0,i,j} for all pairs i<j."""
    core = tuple(range(apex))
    rest = range(apex, n)
    return Multilinear(n, [(1.0, core + t) for t in itertools.combinations(rest, k - apex)])


def sunflower(n_petals, core_size=1, petal_size=2):
    """Sunflower: common core plus pairwise disjoint petals."""
    core = tuple(range(core_size))
    terms, nxt = [], core_size
    for _ in range(n_petals):
        petal = tuple(range(nxt, nxt + petal_size))
        terms.append((1.0, core + petal))
        nxt += petal_size
    return Multilinear(nxt, terms)


def tight_path(n, k=3):
    """Consecutive k-windows {i, ..., i+k-1}."""
    return Multilinear(n, [(1.0, tuple(range(i, i + k))) for i in range(n - k + 1)])


def tight_cycle(n, k=3):
    return Multilinear(n, [(1.0, tuple((i + s) % n for s in range(k))) for i in range(n)])


def loose_path(n_edges, k=3):
    """Consecutive triples sharing one vertex: {0,1,2},{2,3,4},..."""
    terms, nxt = [], 0
    for _ in range(n_edges):
        terms.append((1.0, tuple(range(nxt, nxt + k))))
        nxt += k - 1
    return Multilinear(nxt + 1, terms)


def loose_cycle(n_edges, k=3):
    f = loose_path(n_edges, k)
    n = f.n - 1  # identify last vertex with vertex 0
    terms = [(a, tuple(j % n for j in t)) for a, t in f.terms]
    return Multilinear(n, terms)


def random_uniform(n, k, m, seed, coef_dist="one"):
    rng = random.Random(seed)
    allt = list(itertools.combinations(range(n), k))
    ts = rng.sample(allt, min(m, len(allt)))
    return Multilinear(n, [(_coef(rng, coef_dist), t) for t in ts])


def random_mixed(n, m2, m3, seed, coef_dist="one"):
    rng = random.Random(seed)
    e = rng.sample(list(itertools.combinations(range(n), 2)), m2)
    t = rng.sample(list(itertools.combinations(range(n), 3)), m3)
    return Multilinear(n, [(_coef(rng, coef_dist), s) for s in e + t])


def random_degrees(n, m, seed, degrees=(2, 3, 4), coef_dist="one"):
    """m random terms with random sizes drawn from `degrees`."""
    rng = random.Random(seed)
    terms, seen = [], set()
    while len(terms) < m:
        k = rng.choice(degrees)
        t = tuple(sorted(rng.sample(range(n), k)))
        if t not in seen:
            seen.add(t)
            terms.append((_coef(rng, coef_dist), t))
    return Multilinear(n, terms)


def _coef(rng, dist):
    if dist == "one":
        return 1.0
    if dist == "uniform":
        return rng.uniform(0.1, 1.0)
    if dist == "loguniform":
        return 10 ** rng.uniform(-2, 0)
    raise ValueError(dist)


def fano():
    lines = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
    return Multilinear(7, [(1.0, t) for t in lines])


def paper_example():
    """phi = x1x2x3x4x5 + x1x2x3x4 + x1x3x4x5 + x2x3x5 + x1x3x5 + x4x5 + x1x2 (paper, Sec. 4)."""
    terms = [(0, 1, 2, 3, 4), (0, 1, 2, 3), (0, 2, 3, 4), (1, 2, 4), (0, 2, 4), (3, 4), (0, 1)]
    return Multilinear(5, [(1.0, t) for t in terms])


def with_coefs(f, coefs):
    return Multilinear(f.n, [(c, t) for c, (_, t) in zip(coefs, f.terms)])


def star_monomial(m, b=1.0, a=1.0):
    """Bilinear star x_0 * (x_1+...+x_m) with coefficient a, plus the leaf monomial b * x_1...x_m.
    Extremal point of the Fano plane (m=3) reduces to this; predicted max ratio 2 - 1/m at
    x = (1/m, (m-1)/m, ..., (m-1)/m)."""
    terms = [(a, (0, i)) for i in range(1, m + 1)] + [(b, tuple(range(1, m + 1)))]
    return Multilinear(m + 1, terms)


def star_leaf_uniform(m, r, b=1.0):
    """Bilinear star plus all r-subsets of the leaves with coefficient b."""
    terms = [(1.0, (0, i)) for i in range(1, m + 1)] + [(b, t) for t in itertools.combinations(range(1, m + 1), r)]
    return Multilinear(m + 1, terms)
