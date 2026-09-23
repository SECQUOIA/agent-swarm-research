"""Exact stress checks of the proposed fixed-dimension graph theorem.

This is a proof review, not an implementation or performance benchmark of
the full FPTAS. It finds the proof's best factor basis from an exhaustively
known optimum and checks that this basis's rounded-label DP has the claimed
guarantee. The theorem's algorithm enumerates a superset of those bases.
"""

from fractions import Fraction as Q
from itertools import combinations
import hashlib
import json
from pathlib import Path
import random
from time import perf_counter

import sympy as sp


HERE = Path(__file__).resolve().parent


def factor_psd(matrix):
    """Independent pivoted Schur elimination, retaining vectors in original coordinates."""
    residual = matrix.copy()
    output = []
    while any(residual[i, i] != 0 for i in range(matrix.rows)):
        pivot = next(i for i in range(matrix.rows) if residual[i, i] != 0)
        weight = residual[pivot, pivot]
        assert weight > 0
        vector = residual[:, pivot]/weight
        output.append((weight, vector))
        residual -= weight*vector*vector.T
        assert residual == residual.T
        assert all(residual[i, i] >= 0 for i in range(matrix.rows))
    assert residual == sp.zeros(matrix.rows)
    assert sum((weight*vector*vector.T for weight, vector in output), sp.zeros(matrix.rows)) == matrix
    assert len(output) <= matrix.rows
    return output


def psd(matrix):
    return all(matrix.extract(indices, indices).det() >= 0
               for size in range(1, matrix.rows+1)
               for indices in combinations(range(matrix.rows), size))


def enumerate_paths(vertices, edges):
    paths = {0: [()]}
    for vertex in range(vertices):
        for edge, (u, v, _) in enumerate(edges):
            if u == vertex:
                paths.setdefault(v, []).extend(path+(edge,) for path in paths.get(u, []))
    return paths.get(vertices-1, [])


def review_case(vertices, edges, prior, eta, counts):
    p, N = prior.rows, max(1, vertices-1)
    edge_factors = [factor_psd(e[2]) for e in edges]
    prior_factors = factor_psd(prior)
    counts["factorizations"] += len(edges)+1
    paths = enumerate_paths(vertices, edges)
    assert paths
    def information(path):
        return prior+sum((edges[e][2] for e in path), sp.zeros(p))
    optimum = max(paths, key=lambda path: information(path).det())
    optimum_value = information(optimum).det()
    labels = [(None, w, v) for w, v in prior_factors]
    labels += [(e, w, v) for e in optimum for w, v in edge_factors[e]]
    candidates = []
    for basis in combinations(range(len(labels)), p):
        V = sp.Matrix.hstack(*(labels[i][2] for i in basis))
        squared_volume = V.det()**2*sp.prod(labels[i][1] for i in basis)
        if squared_volume > 0:
            candidates.append((squared_volume, basis, V))
    if optimum_value == 0:
        assert not candidates
        assert all(information(path).det() == 0 for path in paths)
        counts["singular_fallbacks"] += 1
        return
    _, basis, V = max(candidates, key=lambda item: item[0])
    weights = [labels[i][1] for i in basis]
    # Check the real maximum-volume coordinate statement without square roots.
    for _, weight, vector in labels:
        coordinate = V.inv()*vector
        assert all(coordinate[i]**2*weight <= weights[i] for i in range(p))
    tau = []
    for weight in weights:
        value = sp.Rational(1)
        while value**2*weight < 1:
            value *= 2
        while value**2*weight >= 4:
            value /= 2
        assert 1 <= value**2*weight < 4
        tau.append(value)
    T = sp.diag(*tau)*V.inv()
    transformed_prior = T*prior*T.T
    transformed = [T*edge[2]*T.T for edge in edges]
    assert all(transformed_prior[i, i] <= 4*p for i in range(p))
    retained = {e for e, matrix in enumerate(transformed)
                if all(matrix[i, i] <= 4*p for i in range(p))}
    assert set(optimum) <= retained
    for e in retained:
        assert all(abs(x) <= 4*p for x in transformed[e])
    owner_list = sorted({labels[i][0] for i in basis if labels[i][0] is not None})
    owner_bits = {e: 1 << i for i, e in enumerate(owner_list)}
    complete = (1 << len(owner_list))-1
    if len(owner_list) < sum(labels[i][0] is not None for i in basis):
        counts["repeated_basis_owners"] += 1
    Astar = T*information(optimum)*T.T
    assert psd(Astar-sp.eye(p))
    h = sp.Rational(eta)/(p*p*N)
    coordinates = [(i, j) for i in range(p) for j in range(i, p)]
    integer = {e: tuple(int(sp.floor(transformed[e][i, j]/h)) for i, j in coordinates)
               for e in retained}
    labels_of = lambda path: tuple(sum(integer[e][j] for e in path) for j in range(len(coordinates)))
    states = {0: {(0, (0,)*len(coordinates)): ()}}
    merges = 0
    for vertex in range(vertices):
        for e, (u, v, _) in enumerate(edges):
            if u != vertex or e not in retained:
                continue
            following = states.setdefault(v, {})
            for (mask, label), path in states.get(u, {}).items():
                key = (mask | owner_bits.get(e, 0), tuple(a+b for a, b in zip(label, integer[e])))
                if key in following:
                    merges += 1
                else:
                    following[key] = path+(e,)
    key = (complete, labels_of(optimum))
    representative = states[vertices-1][key]
    Ahat = T*information(representative)*T.T
    difference = Ahat-Astar
    assert all(abs(x) < N*h for x in difference)
    assert psd(Ahat-(1-sp.Rational(eta)/p)*Astar)
    assert information(representative).det() >= (1-sp.Rational(eta))*optimum_value
    for path in paths:
        if set(path) <= retained:
            residual = [sum(transformed[e][i, j] for e in path)-h*label
                        for (i, j), label in zip(coordinates, labels_of(path))]
            assert all(0 <= x < N*h for x in residual)
            counts["floor_residuals"] += len(residual)
    counts["positive_cases"] += 1
    counts["state_merges"] += merges
    counts["exhaustive_paths"] += len(paths)


def main():
    started = perf_counter()
    rng = random.Random(442917)
    counts = {"factorizations": 0, "positive_cases": 0, "singular_fallbacks": 0,
              "repeated_basis_owners": 0, "floor_residuals": 0,
              "state_merges": 0, "exhaustive_paths": 0,
              "corollary_loss_checks": 0}
    for p in (1, 2, 3):
        for instance in range(8):
            def random_psd(rank):
                matrix = sp.zeros(p)
                for _ in range(rank):
                    vector = sp.Matrix([sp.Rational(rng.randrange(-3, 4), 3) for _ in range(p)])
                    matrix += sp.Rational(rng.randrange(1, 5), 4)*vector*vector.T
                # Preserve exact PSD while creating extreme coordinate conditioning.
                scale = sp.diag(*[sp.Rational(2)**(60*(i-p//2)) for i in range(p)])
                return scale*matrix*scale
            prior = random_psd(instance % (p+1))
            edges = [(u, v, random_psd(rng.randrange(p+1)))
                     for u in range(5) for v in range(u+1, min(6, u+3))]
            review_case(6, edges, prior, sp.Rational(1, 3), counts)
        # Entire feasible family singular, despite nonzero matrices for p > 1.
        matrix = sp.diag(*([1]*(p-1)+[0]))
        review_case(3, [(0, 1, matrix), (1, 2, matrix), (0, 2, matrix)],
                    sp.zeros(p), sp.Rational(1, 2), counts)
        # Distinct lengths and information values merge at the optimum's rounded state.
        h = sp.Rational(1, 2)/(p*p*2)
        review_case(3, [(0, 2, h*sp.eye(p)/5), (0, 1, 3*h*sp.eye(p)/20),
                        (1, 2, 3*h*sp.eye(p)/20)], sp.eye(p), sp.Rational(1, 2), counts)
        if p > 1:
            # Negative off-diagonal values share floor labels; truncation toward zero is not used.
            h = sp.Rational(1, 2)/(p*p)
            A, B = h*sp.eye(p)/2, 3*h*sp.eye(p)/5
            A[0, 1] = A[1, 0] = -h/5
            B[0, 1] = B[1, 0] = -h/10
            review_case(2, [(0, 1, A), (0, 1, B)], sp.eye(p), sp.Rational(1, 2), counts)
    for p in range(1, 8):
        for epsilon in (sp.Rational(1, 1000), sp.Rational(1, 7), sp.Rational(9, 10)):
            delta = epsilon/(4*p)
            factor = (1-epsilon/2)*((1-delta)/(1+delta))**p
            assert factor >= 1-epsilon
            counts["corollary_loss_checks"] += 1
    note = HERE.parent.parent / "notes/research-20260912-fixed-parameter-doptimal-fptas.md"
    report = {"status": "passed", "scope": "Independent theorem stress checks, not the full FPTAS",
              "counts": counts, "candidate_note_sha256": hashlib.sha256(note.read_bytes()).hexdigest(),
              "reviewer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "seconds": perf_counter()-started}
    (HERE / "results/doptimal-fptas-theorem-independent-review.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
