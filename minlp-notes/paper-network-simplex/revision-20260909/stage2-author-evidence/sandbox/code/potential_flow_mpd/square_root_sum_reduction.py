"""Exact cactus reduction for SRS <= versus maximum potential drop >=.

No symbolic roots enter the encoded graph. The standalone check combines
symbolic identities, exact topology/input checks, and independent numerical
solution of the nonlinear flow equations. These checks are evidence, not a
replacement for the proof in notes/potential-flow-mpd-cactus-investigation.md.
"""
from dataclasses import dataclass
from fractions import Fraction
from math import prod


@dataclass
class Instance:
    n: int
    arcs: list
    source: int
    sink: int
    threshold: Fraction
    scale: int
    constant: int
    radicands: list


def reduce_srs(radicands, threshold, integer_resistances=True):
    """Reduce nonnegative integer radicands and integer threshold exactly."""
    assert all(isinstance(a, int) and a >= 0 for a in radicands)
    assert isinstance(threshold, int)
    threshold -= sum(a == 1 for a in radicands)
    radicands = [a for a in radicands if a > 1]
    if not radicands:
        return Instance(2, [(0, 1, Fraction(1))], 0, 1,
                        Fraction(1 if threshold >= 0 else 2), 1, 1, [])
    m = len(radicands)
    arcs = []
    for i, a in enumerate(radicands):
        u, mid, v = 3*i, 3*i+1, 3*i+2
        A, half_B = Fraction((a-1)**2), Fraction((a-1)**2, 2*a)
        arcs.extend([(u, v, A), (u, mid, half_B), (mid, v, half_B)])
        if i:
            arcs.append((u-1, u, Fraction(1)))
    scale = 2*prod(radicands) if integer_resistances else 1
    constant = sum(a+1 for a in radicands)+m-1
    arcs = [(u, v, beta*scale) for u, v, beta in arcs]
    return Instance(3*m, arcs, 0, 3*m-1,
                    Fraction(scale*(constant-2*threshold)),
                    scale, constant, radicands)


def upper_bound_srs(branch_totals, bridge_total, threshold):
    """Encode Q-sum sqrt(r) >= H as sum sqrt(N) <= K.

    branch_totals lists positive rational (A,B) for cycles on the block path.
    Return a Boolean for a rational/trivial instance, or integer (N,K).
    This routine avoids algebraic arithmetic and integer factorization.
    """
    Q = Fraction(bridge_total)
    radicals = []
    for A, B in branch_totals:
        A, B = Fraction(A), Fraction(B)
        assert A > 0 and B > 0
        if A == B:
            Q += A/4
        else:
            Q += A*B*(A+B)/(A-B)**2
            radicals.append(4*A**3*B**3/(A-B)**4)
    T = Q-Fraction(threshold)
    if not radicals:
        return T >= 0
    if T <= 0:
        return False
    D = T.denominator*prod(r.denominator for r in radicals)
    N = [D*D*r.numerator//r.denominator for r in radicals]
    K = D*T
    assert K.denominator == 1
    return N, K.numerator


def check():
    import numpy as np
    import sympy as sp
    import networkx as nx
    from pbflow import Graph, solve_flow, check_flow

    a, q = sp.symbols('a q', positive=True)
    # a>=2 is imposed by the encoder; positive suffices for the identity.
    xA, xB = q/(sp.sqrt(a)+1), q*sp.sqrt(a)/(sp.sqrt(a)+1)
    A, B = (a-1)**2, (a-1)**2/a
    assert sp.simplify(xA+xB-q) == 0
    assert sp.simplify(A*xA**2-B*xB**2) == 0
    assert sp.simplify(A*xA**2-q**2*(a+1-2*sp.sqrt(a))) == 0
    A, B = sp.symbols('A B', positive=True)
    assert sp.simplify(A*B/(sp.sqrt(A)+sp.sqrt(B))**2 -
                      A*B*(A+B)/(A-B)**2 +
                      2*A*B*sp.sqrt(A*B)/(A-B)**2) == 0

    rng = np.random.default_rng(230905)
    worst = 0.0
    for trial in range(120):
        radicands = [int(x) for x in rng.integers(0, 18, int(rng.integers(1, 7)))]
        k = int(rng.integers(0, 30))
        inst = reduce_srs(radicands, k)
        topo = nx.Graph()
        topo.add_nodes_from(range(inst.n))
        topo.add_edges_from((u, v) for u, v, _ in inst.arcs)
        assert nx.is_connected(topo)
        assert topo.number_of_edges() == len(inst.arcs)
        assert max(dict(topo.degree()).values()) <= 3
        assert all(len(cycle) == 3 for cycle in nx.cycle_basis(topo))
        assert all(beta > 0 and beta.denominator == 1 for _, _, beta in inst.arcs)
        # Normalize the global scaling before floating evaluation to avoid
        # artificial absolute residual growth; this leaves all flows unchanged.
        G = Graph(inst.n, [(u, v, beta/inst.scale) for u, v, beta in inst.arcs])
        b = np.zeros(inst.n)
        b[inst.source], b[inst.sink] = 1., -1.
        x, pi = solve_flow(G, b)
        residual = max(check_flow(G, b, x, pi))
        worst = max(worst, residual)
        assert residual < 1e-7, (radicands, residual)
        assert min(x) > 0
        if inst.radicands:
            exact_drop = inst.constant-2*sum(sp.sqrt(a) for a in inst.radicands)
            assert abs((pi[inst.source]-pi[inst.sink])-float(exact_drop)) < 1e-7
            cycles = [(Fraction((a-1)**2), Fraction((a-1)**2, a))
                      for a in inst.radicands]
            encoded = upper_bound_srs(cycles, len(cycles)-1,
                                      inst.threshold/inst.scale)
            truth = bool(sum(sp.sqrt(a) for a in radicands) <= k)
            if isinstance(encoded, bool):
                assert encoded == truth
            else:
                N, K = encoded
                assert bool(sum(sp.sqrt(n) for n in N) <= K) == truth
        else:
            assert (Fraction(1) >= inst.threshold) == (
                sum(sp.sqrt(a) for a in radicands) <= k)
    # Edge cases: equal branches and exact equality are rationally handled.
    assert upper_bound_srs([(4, 4)], 0, 1) is True
    assert upper_bound_srs([(4, 4)], 0, Fraction(3, 2)) is False
    assert upper_bound_srs([(1, 2)], 0, 6) is False
    print('Symbolic gadget and rationalization identities passed.')
    print(f'120 reduction/topology/integrality/decision checks passed; max residual {worst:.3g}.')


if __name__ == '__main__':
    check()
