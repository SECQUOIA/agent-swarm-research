"""Exact finite checks of Stage 5's risky algebra and counting boundaries.

Run with the repository's minlp-notes Python (SymPy required). These checks
support, and do not replace, the manuscript's universal proofs or the
classical random-width theorem. No random CSP experiment is used as a proof.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import sympy as sp

HERE = Path(__file__).resolve().parent


def rank_and_basis(rows):
    pivots = {}
    originals = []
    for original in rows:
        row = original
        while row:
            bit = row.bit_length() - 1
            if bit in pivots:
                row ^= pivots[bit]
            else:
                pivots[bit] = row
                originals.append(original)
                break
    return len(pivots), originals


def support_check():
    n, D = 4, 3
    supports = [s for s in range(1, 1 << n) if s.bit_count() <= D]
    count = 0
    for select in range(1 << len(supports)):
        rows = [s for j, s in enumerate(supports) if select >> j & 1]
        rank, basis = rank_and_basis(rows)
        union = 0
        basis_union = 0
        for s in rows:
            union |= s
        for s in basis:
            basis_union |= s
        assert union == basis_union
        assert union.bit_count() <= D * rank
        # Enumerate every fiber, so this tests every consistent signed RHS.
        fibers = {}
        for witness in range(1 << n):
            rhs = tuple((s & witness).bit_count() % 2 for s in rows)
            fibers[rhs] = fibers.get(rhs, 0) + 1
        assert len(fibers) == 1 << rank
        assert set(fibers.values()) == {1 << (n - rank)}
        # Repetition preserves rank and the union, including the empty case.
        assert rank_and_basis(rows + rows)[0] == rank
        count += 1
    return {"families": count, "original_dimension": n, "max_support": D,
            "fiber_count": "all Boolean assignments and all consistent RHS"}


def signed_law_check():
    count = 0
    # Constant class plus two free classes; all orientations and allocations.
    choices = list(product(range(3), (-1, 1)))
    for coords in product(choices, repeat=4):
        vectors = [(0, 1)] + list(coords)
        points = []
        for signs in product((-1, 1), repeat=2):
            class_values = (1,) + signs
            points.append([1] + [s * class_values[c] for c, s in coords])
        for i in range(5):
            for j in range(5):
                ci, si = vectors[i]
                cj, sj = vectors[j]
                intended = si * sj if ci == cj else 0
                actual = Q(sum(p[i] * p[j] for p in points), len(points))
                assert actual == intended
        count += 1
    return {"signed_class_systems": count, "coordinates": 4,
            "constant_class_included": True}


def width_closure_check():
    edges = [(0b000111, 1), (0b011001, 1),
             (0b101010, 1), (0b110100, -1)]
    def close(width):
        signs = dict([(0, 1)] + edges)
        changed = True
        while changed:
            changed = False
            items = list(signs.items())
            for a, sa in items:
                for b, sb in items:
                    c, sc = a ^ b, sa * sb
                    if c.bit_count() > width:
                        continue
                    if c in signs:
                        if signs[c] != sc:
                            return None
                    else:
                        signs[c] = sc
                        changed = True
        return signs
    signs = close(3)
    assert signs is not None
    indices = [0] + [1 << i for i in range(6)]
    gram = sp.Matrix([[signs.get(i ^ j, 0) for j in indices] for i in indices])
    assert gram == sp.eye(7)
    assert all(signs[e] == b for e, b in edges)
    assert close(4) is None
    assert not any(all((-1)**((w & e).bit_count()) == b for e, b in edges)
                   for w in range(64))
    return {"width_3_odd_top_moments_defined_directly": True,
            "width_3_square_degree_1_gram": "identity(7)",
            "width_4_derives_contradiction": True,
            "scope": "one finite inconsistent formula, not linear-width existence"}


def symbolic_check():
    x = sp.symbols('x0:3')
    a = sp.symbols('a0:3')
    h, beta, b, u, v = sp.symbols('h beta b u v')
    clause = (1 - b * sp.prod(x)) / 2
    bernstein = 0
    for s in product((0, 1), repeat=3):
        corner_value = (1 - b * sp.prod(a[i] + h * s[i] for i in range(3))) / 2
        basis = sp.prod(x[i] - a[i] if s[i] else a[i] + h - x[i]
                        for i in range(3))
        bernstein += (corner_value - beta) * basis
    assert sp.expand(bernstein - h**3 * (clause - beta)) == 0
    assert sp.expand(v-sp.prod(x) - (v-u*x[2]) - x[2]*(u-x[0]*x[1])) == 0
    corner = (1-b*sp.prod(a))/2
    cut = 3*h/2-b*(u*(x[2]-a[2])+a[2]*(x[0]*x[1]-a[0]*a[1]))/2
    assert sp.expand((1-b*v)/2-corner+3*h/2-cut
                     + b*((v-u*x[2])+a[2]*(u-x[0]*x[1]))/2) == 0
    # Overlapping, repeated parity factors with a globally coupled multiplier.
    z0, z1, z2 = x[0]*x[1], -x[1]*x[2], x[0]*x[2]
    indicator = (1+z0)*(1-z1)*(1+z0)/8
    P = 2+z0-z1+3*z2
    def boolean_reduce(expr):
        poly = sp.Poly(sp.expand(expr), *x)
        return sp.expand(sum(c*sp.prod(xi**(k % 2) for xi,k in zip(x, powers))
                             for powers,c in poly.terms()))
    assert boolean_reduce(indicator**2-indicator) == 0
    assert boolean_reduce(indicator*P**2-(indicator*P)**2) == 0
    return {"bernstein": "formal identity after multiplying by h^3",
            "cubic_graph_transfer": True, "order_one_quadratic_identity": True,
            "repeated_overlapping_parity_indicator_square": True}


def affine_check():
    count = 0
    for n in range(1, 10):
        vertices = list(product((-1, 1), repeat=n))
        assert sum(sum(w) >= 0 for w in vertices) >= len(vertices)//2
        assert Q(sum(sum(w) for w in vertices), len(vertices)) == 0
        assert Q(sum(sum(w)**2 for w in vertices), len(vertices)) == n
        for r in range(1, n+3):
            for t in range(min(r-1, (n+1)//2)):
                s = n-t
                for fixed in product((-1, 1), repeat=t):
                    a = sum(fixed)
                    if a < 0:
                        assert a < 0  # P=1 rejects the node.
                        continue
                    k = a+1
                    assert k <= s and 1+2*k <= 2*r
                    vals = [(a+sum(w)) if all(w[i] == -1 for i in range(k)) else 0
                            for w in product((-1, 1), repeat=s)]
                    assert Q(sum(vals), 1 << s) == -Q(1, 1 << k)
                    count += 1
    return {"exact_negative_localizers": count, "dimension_range": [1, 9],
            "order_range": "1 through n+2"}


def main():
    report = {"arithmetic": "exact integer, rational, and symbolic",
              "rank_and_fibers": support_check(),
              "signed_moment_realization": signed_law_check(),
              "source_width_convention": width_closure_check(),
              "symbolic_identities": symbolic_check(),
              "affine_obstructions": affine_check()}
    assert 384 * 3**24 < 2**64
    assert Q(7, 16*64) == Q(7, 1024)
    assert Q(7, 16*64*3) == Q(7, 3072)
    assert Q(7, 3072*17) == Q(7, 52224)
    assert sp.ceiling(3 / Q(1, 16)) == 48
    report["constants"] = {"deletion_integer_bound": True,
                           "original_exponent": "7n/1024",
                           "quadratic_lift_exponent": "7n/3072",
                           "lifted_dimension_exponent": "7N/52224",
                           "upper_base": 48}
    report["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE/'check_stage05_author.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
