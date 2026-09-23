"""Finite exact checks for full-support scalar quadratic message elimination.

Uses Fraction Schur complements and exact SymPy quadratic inequality sets.
This is a deliberately small correctness checker, not the proposed efficient
envelope implementation, a smoothed experiment, or a complexity proof.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import product

import sympy as s


M = F(2, 3)  # C=1, d=1, rho=1/4: C/[2*d*(1-rho)].
I = s.Interval(-s.Rational(2, 3), s.Rational(2, 3))
COUNTS = dict(instances=0, messages=0, support_qps=0, endpoint_bounds=0,
              derivative_bounds=0, atoms=0, candidates=0, outside_active_region=0)


def solve(a, b):
    aug = [list(row) + [rhs] for row, rhs in zip(a, b)]
    for j in range(len(b)):
        pivot = next(i for i in range(j, len(b)) if aug[i][j])
        # All systems here must be SPD principal matrices or their Schur
        # complements. Positive unpivoted elimination pivots check that fact.
        assert pivot == j and aug[j][j] > 0
        aug[j], aug[pivot] = aug[pivot], aug[j]
        scale = aug[j][j]
        aug[j] = [v / scale for v in aug[j]]
        for i in range(len(b)):
            if i != j:
                scale = aug[i][j]
                aug[i] = [v - scale * w for v, w in zip(aug[i], aug[j])]
    return [row[-1] for row in aug]


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


@dataclass(frozen=True)
class Quad:
    a: F
    b: F
    c: F
    mask: int

    @property
    def coefficients(self):
        return self.a, self.b, self.c

    def value(self, t):
        return self.a * t * t + self.b * t + self.c


@lru_cache(None)
def nonpositive(coefficients):
    """Exact real solution set of a quadratic <= 0; no floating point."""
    a, b, c = map(s.Rational, coefficients)
    if not a:
        if not b:
            return s.S.Reals if c <= 0 else s.S.EmptySet
        root = -c / b
        return s.Interval(-s.oo, root) if b > 0 else s.Interval(root, s.oo)
    disc = b * b - 4 * a * c
    if disc < 0:
        return s.S.Reals if a < 0 else s.S.EmptySet
    if disc == 0:
        return s.FiniteSet(-b / (2 * a)) if a > 0 else s.S.Reals
    center, radius = -b / (2 * a), s.sqrt(disc) / (2 * abs(a))
    left, right = center - radius, center + radius
    if a > 0:
        return s.Interval(left, right)
    return s.Union(s.Interval(-s.oo, left), s.Interval(right, s.oo))


def active_region(q, competitors):
    region = I
    for other in competitors:
        diff = tuple(x - y for x, y in zip(q.coefficients, other.coefficients))
        region = region.intersect(nonpositive(diff))
        if region is s.S.EmptySet:
            break
    return region


def has_interval(region):
    if isinstance(region, s.Interval):
        return True
    if isinstance(region, s.Union):
        return any(has_interval(part) for part in region.args)
    assert region is s.S.EmptySet or isinstance(region, s.FiniteSet), region
    return False


def prune(quads):
    unique = list({q.coefficients: q for q in quads}.values())
    kept, regions = [], []
    for q in unique:
        region = active_region(q, unique)
        # Tangency-only alternatives can be removed by continuity. Keep full
        # polynomials attaining the envelope on a nonempty open interval.
        if has_interval(region):
            kept.append(q)
            regions.append(region)
    assert s.Union(*regions) == I
    return kept, regions


def subsets(vertices):
    for bits in product((0, 1), repeat=len(vertices)):
        yield sum(bit << v for bit, v in zip(bits, vertices))


class Instance:
    def __init__(self, name, n, blocks, edges, variant):
        self.name, self.n, self.blocks = name, n, blocks
        self.q = [[F(i == j) for j in range(n)] for i in range(n)]
        for i, j in edges:
            self.q[i][j] = self.q[j][i] = F((-1) ** (i + j), 32)
        self.c = [F((-1) ** i * (i % 3 + 1), 4) for i in range(n)]
        self.lam = [ci * ci / 4 for ci in self.c]
        if variant == "near_tie":
            self.lam = [v + F((-1) ** i, 10**8) for i, v in enumerate(self.lam)]
        elif variant == "negative":
            self.lam[1] = F(-1, 100)
            self.lam[-1] += F(1, 10000)
        for i in range(n):
            assert abs(self.c[i]) <= 1
            assert sum(abs(self.q[i][j]) for j in range(n) if j != i) <= F(1, 4)
        assert M == F(1) / (2 * F(1) * (1 - F(1, 4)))

    def conditional(self, mask, boundary, include_boundary):
        indices = [i for i in range(self.n) if i != boundary and mask >> i & 1]
        h = [[self.q[i][j] for j in indices] for i in indices]
        c = [self.c[i] for i in indices]
        r = [self.q[i][boundary] for i in indices]
        inv_c, inv_r = solve(h, c), solve(h, r)
        for t in (-M, M):
            values = [-ci / 2 - ri * t for ci, ri in zip(inv_c, inv_r)]
            assert all(abs(x) <= M for x in values)
            COUNTS["endpoint_bounds"] += len(values)
        COUNTS["support_qps"] += 1
        return Quad((self.q[boundary][boundary] if include_boundary else F(0))
                    - dot(r, inv_r),
                    (self.c[boundary] if include_boundary else F(0)) - dot(r, inv_c),
                    sum((self.lam[i] for i in range(self.n) if mask >> i & 1), F(0))
                    - dot(c, inv_c) / 4, mask)

    def certify(self, candidates, vertices, boundary, include_boundary):
        free = sorted(vertices - {boundary})
        brute = [self.conditional(mask | ((1 << boundary) if include_boundary else 0),
                                  boundary, include_boundary) for mask in subsets(free)]
        for q in brute:
            for t in (-M, M):
                assert abs(2 * q.a * t + q.b) <= F(8, 3)
                COUNTS["derivative_bounds"] += 1
        lookup = {q.mask: q.coefficients for q in brute}
        for q in candidates:
            assert q.coefficients == lookup[q.mask]
        # A candidate is a feasible complete support, so it cannot beat brute
        # force. Covering I by its exact brute-optimal region proves equality
        # everywhere, including irrational crossings and isolated ties.
        regions = [active_region(q, brute) for q in candidates]
        assert s.Union(*regions) == I, (self.name, boundary, regions)
        COUNTS["messages"] += 1

    def vertex(self, v):
        children = [self.block(v, block) for block in self.blocks.get(v, [])]
        own = Quad(self.q[v][v], self.c[v], self.lam[v], 1 << v)
        candidates = []
        # The production proposal merges ordered interval lists. Here exact
        # interval intersections identify the same feasible simultaneous
        # active combinations; this tiny checker does not claim its runtime.
        choices = [list(zip(quads, regions)) for quads, regions, _ in children]
        for combo in product(*choices):
            region = I
            coefficients = list(own.coefficients)
            mask = own.mask
            for q, active in combo:
                region = region.intersect(active)
                coefficients = [a + b for a, b in zip(coefficients, q.coefficients)]
                mask |= q.mask
            if has_interval(region):
                candidates.append(Quad(*coefficients, mask))
        kept, regions = prune(candidates)
        vertices = {v}.union(*(vertices for _, _, vertices in children))
        self.certify(kept, vertices, v, True)
        best = min(kept, key=lambda q: q.c)
        atom = (best.c - self.lam[v], best.mask & ~(1 << v))
        direct = min(self.conditional(mask, v, False).c
                     for mask in subsets(sorted(vertices - {v})))
        assert atom[0] == direct
        assert self.conditional(atom[1], v, False).c == atom[0]
        COUNTS["atoms"] += 1
        return kept, regions, atom, vertices

    def block(self, parent, children):
        messages = [self.vertex(v) for v in children]
        choices = []
        for v, (quads, regions, atom, _) in zip(children, messages):
            choices.append([(v, q, region) for q, region in zip(quads, regions)]
                           + [(v, atom, None)])
        candidates = []
        for combo in product(*choices):
            active = [(v, q, region) for v, q, region in combo if isinstance(q, Quad)]
            h = [[q.a if v == w else self.q[v][w] for w, _, _ in active]
                 for v, q, _ in active]
            c = [q.b for _, q, _ in active]
            r = [self.q[v][parent] for v, _, _ in active]
            inv_c, inv_r = solve(h, c), solve(h, r)
            constant, mask = F(0), 0
            for _, q, _ in combo:
                if isinstance(q, Quad):
                    constant += q.c
                    mask |= q.mask
                else:
                    constant += q[0]
                    mask |= q[1]
            candidate = Quad(-dot(r, inv_r), -dot(r, inv_c),
                             constant - dot(c, inv_c) / 4, mask)
            # Every generated full polynomial must be an actual support value,
            # including combinations evaluated outside a child's active region.
            assert candidate.coefficients == self.conditional(mask, parent, False).coefficients
            for t in (-M, M):
                values = [-ci / 2 - ri * t for ci, ri in zip(inv_c, inv_r)]
                assert all(abs(x) <= M for x in values)
                for value, (_, _, region) in zip(values, active):
                    if not bool(region.contains(s.Rational(value))):
                        COUNTS["outside_active_region"] += 1
            candidates.append(candidate)
            COUNTS["candidates"] += 1
        kept, regions = prune(candidates)
        vertices = {parent}.union(*(vertices for _, _, _, vertices in messages))
        self.certify(kept, vertices, parent, False)
        return kept, regions, vertices

    def check(self):
        quads, _, atom, _ = self.vertex(0)
        assert all(q.a > 0 and abs(q.b / (2 * q.a)) <= M for q in quads)
        dp_opt = min([atom[0]] + [q.c - q.b * q.b / (4 * q.a) for q in quads])
        brute_opt = None
        for mask in subsets(list(range(self.n))):
            ids = [i for i in range(self.n) if mask >> i & 1]
            h = [[self.q[i][j] for j in ids] for i in ids]
            c = [self.c[i] for i in ids]
            x = solve(h, c)
            value = sum((self.lam[i] for i in ids), F(0)) - dot(c, x) / 4
            brute_opt = value if brute_opt is None else min(brute_opt, value)
        assert dp_opt == brute_opt
        COUNTS["instances"] += 1
        print(self.name, "exact envelope and optimum verified")


def clique_edges(blocks):
    return [(a, b) for block in blocks for a, b in product(block, repeat=2) if a < b]


def main():
    # Cover constant, linear, tangent, no-root, and two-root branches of the
    # exact inequality primitive used for every envelope certificate.
    assert nonpositive((0, 0, 0)) == s.S.Reals
    assert nonpositive((0, 0, 1)) == s.S.EmptySet
    assert nonpositive((0, 2, -1)) == s.Interval(-s.oo, s.Rational(1, 2))
    assert nonpositive((0, -2, 1)) == s.Interval(s.Rational(1, 2), s.oo)
    assert nonpositive((1, 0, 1)) == s.S.EmptySet
    assert nonpositive((-1, 0, -1)) == s.S.Reals
    assert nonpositive((1, -2, 1)) == s.FiniteSet(1)
    assert nonpositive((-1, 2, -1)) == s.S.Reals
    assert nonpositive((1, 0, -2)) == s.Interval(-s.sqrt(2), s.sqrt(2))
    assert nonpositive((-1, 0, 2)) == s.Union(s.Interval(-s.oo, -s.sqrt(2)),
                                                        s.Interval(s.sqrt(2), s.oo))
    # The cycle checks the algebra for a nonclique biconnected block as well;
    # it is outside the note's narrower stated block-graph class.
    cases = [
        ("triangle_chain", 5, {0: [(1, 2)], 2: [(3, 4)]},
         clique_edges([(0, 1, 2), (2, 3, 4)])),
        ("triangle_star", 7, {0: [(1, 2), (3, 4), (5, 6)]},
         clique_edges([(0, 1, 2), (0, 3, 4), (0, 5, 6)])),
        ("four_cycle", 4, {0: [(1, 2, 3)]}, [(0, 1), (1, 2), (2, 3), (3, 0)]),
    ]
    for name, n, blocks, edges in cases:
        for variant in ("exact_tie", "near_tie", "negative"):
            Instance(name + "/" + variant, n, blocks, edges, variant).check()
    assert COUNTS["outside_active_region"] > 0
    print("PASS", COUNTS)


if __name__ == "__main__":
    main()
