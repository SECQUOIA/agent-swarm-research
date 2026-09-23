"""Exact small-instance review of the all-ranges PSD path approximation set.

This deliberately exhaustive checker exercises every enumerated basis and
every feasible path in its small fixtures. It is a proof stress test, not
a practical implementation or performance benchmark of the theorem.
"""

from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path
import random
from time import perf_counter

import sympy as sp


HERE = Path(__file__).resolve().parent


def is_psd(matrix):
    assert matrix == matrix.T
    return all(matrix.extract(indices, indices).det() >= 0
               for size in range(1, matrix.rows + 1)
               for indices in combinations(range(matrix.rows), size))


def factors(matrix):
    residual = matrix.copy()
    result = []
    while residual != sp.zeros(matrix.rows):
        pivot = next(i for i in range(matrix.rows) if residual[i, i] > 0)
        weight = residual[pivot, pivot]
        vector = residual[:, pivot] / weight
        result.append((weight, vector))
        residual -= weight * vector * vector.T
        assert is_psd(residual)
    assert len(result) <= matrix.rows
    assert sum((w * v * v.T for w, v in result), sp.zeros(matrix.rows)) == matrix
    return result


def all_paths(vertices, edges):
    prefixes = {0: [()]}
    for vertex in range(vertices):
        for edge, (start, end, _) in enumerate(edges):
            assert 0 <= start < end < vertices
            if start == vertex:
                prefixes.setdefault(end, []).extend(
                    path + (edge,) for path in prefixes.get(vertex, []))
    return prefixes.get(vertices - 1, [])


def review_case(name, vertices, edges, prior, eta, counts):
    p, limit = prior.rows, max(1, vertices - 1)
    zero = sp.zeros(p)
    paths = all_paths(vertices, edges)
    information = {path: prior + sum((edges[e][2] for e in path), zero)
                   for path in paths}
    labels = [(-1, w, v) for w, v in factors(prior)]
    for edge, (_, _, matrix) in enumerate(edges):
        labels.extend((edge, w, v) for w, v in factors(matrix))
    counts["factorizations"] += len(edges) + 1
    counts["feasible_paths"] += len(paths)
    cover = set()
    if vertices == 1:
        cover.add(())
    zero_paths = [path for path in paths if information[path] == zero]
    assert zero_paths == [path for path in paths if prior == zero
                          and all(edges[e][2] == zero for e in path)]
    if prior == zero and zero_paths:
        cover.add(zero_paths[0])
        counts["rank_zero_families"] += 1

    # Store surviving bases to audit the max-volume existence argument too.
    surviving = {}
    for rank in range(1, p + 1):
        for basis in combinations(range(len(labels)), rank):
            V = sp.Matrix.hstack(*(labels[i][2] for i in basis))
            gram = V.T * V
            if gram.det() == 0:
                continue
            counts["independent_basis_trials"] += 1
            left = gram.inv() * V.T
            projector = V * left
            assert projector * projector == projector
            assert projector == projector.T
            if projector * prior != prior:
                counts["prior_range_rejections"] += 1
                continue
            in_range = {e for e, (_, _, matrix) in enumerate(edges)
                        if projector * matrix == matrix}
            counts["edge_range_deletions"] += len(edges) - len(in_range)
            scales = []
            for i in basis:
                weight = labels[i][1]
                scale = sp.Rational(1)
                while scale * scale * weight < 1:
                    scale *= 2
                while scale * scale * weight >= 4:
                    scale /= 2
                assert 1 <= scale * scale * weight < 4
                scales.append(scale)
            T = sp.diag(*scales) * left
            K = V * sp.diag(*(1 / scale for scale in scales))
            assert T * K == sp.eye(rank)
            assert K * T == projector
            A0 = T * prior * T.T
            assert K * A0 * K.T == prior
            if any(A0[i, i] > 4 * p for i in range(rank)):
                counts["prior_magnitude_rejections"] += 1
                continue
            transformed = {e: T * edges[e][2] * T.T for e in in_range}
            retained = {e for e, matrix in transformed.items()
                        if all(matrix[i, i] <= 4 * p for i in range(rank))}
            counts["edge_magnitude_deletions"] += len(in_range) - len(retained)
            for e in retained:
                assert K * transformed[e] * K.T == edges[e][2]
                assert all(abs(value) <= 4 * p for value in transformed[e])
            owners = sorted({labels[i][0] for i in basis if labels[i][0] >= 0})
            if len(owners) < sum(labels[i][0] >= 0 for i in basis):
                counts["repeated_owner_trials"] += 1
            bits = {e: 1 << i for i, e in enumerate(owners)}
            complete = (1 << len(owners)) - 1
            h = eta / (rank * limit)
            coordinates = [(i, j) for i in range(rank) for j in range(i, rank)]
            integer = {e: tuple(int(sp.floor(transformed[e][i, j] / h))
                                for i, j in coordinates) for e in retained}

            def path_label(path):
                return tuple(sum(integer[e][j] for e in path)
                             for j in range(len(coordinates)))

            states = {0: {(0, (0,) * len(coordinates)): ()}}
            for vertex in range(vertices):
                for edge, (start, end, _) in enumerate(edges):
                    if start != vertex or edge not in retained:
                        continue
                    following = states.setdefault(end, {})
                    for (mask, label), prefix in states.get(vertex, {}).items():
                        key = (mask | bits.get(edge, 0),
                               tuple(a + b for a, b in zip(label, integer[edge])))
                        path = prefix + (edge,)
                        if key in following:
                            counts["state_merges"] += 1
                            if len(path) != len(following[key]):
                                counts["different_length_merges"] += 1
                        else:
                            following[key] = path
            terminal = states.get(vertices - 1, {})
            accepted = [path for (mask, _), path in terminal.items() if mask == complete]
            cover.update(accepted)
            if owners and not any(set(owners) <= set(path) for path in paths):
                counts["incompatible_owner_trials"] += 1
                assert not accepted
            for path in accepted:
                A = T * information[path] * T.T
                assert is_psd(A - sp.eye(rank))
                assert information[path].rank() == rank
                counts["accepted_basis_path_pairs"] += 1
            surviving[basis] = (retained, owners)
            for target in paths:
                if not set(target) <= retained or not set(owners) <= set(target):
                    continue
                representative = terminal[(complete, path_label(target))]
                A = T * information[target] * T.T
                Ahat = T * information[representative] * T.T
                assert is_psd(A - sp.eye(rank))
                assert all(abs(entry) < limit * h for entry in Ahat - A)
                for path in (target, representative):
                    residual = [sum(transformed[e][i, j] for e in path) - h * value
                                for (i, j), value in zip(coordinates, path_label(path))]
                    assert all(0 <= value < limit * h for value in residual)
                    counts["signed_floor_residuals"] += len(residual)
                assert is_psd(information[representative] - (1 - eta) * information[target])
                assert is_psd((1 + eta) * information[target] - information[representative])
                counts["same_label_sandwiches"] += 1

    for target, matrix in information.items():
        rank = matrix.rank()
        if rank:
            target_labels = [i for i, (owner, _, _) in enumerate(labels)
                             if owner == -1 or owner in target]
            candidates = []
            for basis in combinations(target_labels, rank):
                V = sp.Matrix.hstack(*(labels[i][2] for i in basis))
                volume = (V.T * V).det() * sp.prod(labels[i][1] for i in basis)
                if volume > 0:
                    candidates.append((volume, basis, V))
            assert candidates
            _, basis, V = max(candidates, key=lambda item: item[0])
            assert basis in surviving
            retained, owners = surviving[basis]
            assert set(target) <= retained and set(owners) <= set(target)
            left = (V.T * V).inv() * V.T
            for label in target_labels:
                _, weight, vector = labels[label]
                coordinate = left * vector
                assert all(coordinate[i] ** 2 * weight <= labels[basis[i]][1]
                           for i in range(rank))
            counts["max_volume_path_witnesses"] += 1
        witnesses = [path for path in cover
                     if is_psd(information[path] - (1 - eta) * matrix)
                     and is_psd((1 + eta) * matrix - information[path])]
        assert witnesses, (name, target)
        representative = information[witnesses[0]]
        assert representative.rank() == rank
        assert all(representative * vector == sp.zeros(p, 1) for vector in matrix.nullspace())
        counts["covered_paths"] += 1
    assert cover <= set(paths)
    counts["output_paths"] += len(cover)
    counts["cases"] += 1
    return {"name": name, "paths": len(paths), "output_paths": len(cover),
            "ranks": sorted({matrix.rank() for matrix in information.values()})}


def main():
    started = perf_counter()
    counts = Counter()
    cases = []
    eta = sp.Rational(1, 2)

    def check(name, vertices, edges, prior):
        cases.append(review_case(name, vertices, edges, prior, eta, counts))

    check("no feasible path", 2, [], sp.zeros(2))
    check("empty path with singular prior", 1, [], sp.diag(1, 0))
    check("zero paths of different lengths", 3,
          [(0, 2, sp.zeros(2)), (0, 1, sp.zeros(2)), (1, 2, sp.zeros(2))], sp.zeros(2))
    for p in (1, 2, 3):
        h = eta / (2 * p)
        check(f"rank {p} variable-length collisions", 3,
              [(0, 2, h * sp.eye(p) / 5), (0, 1, 3 * h * sp.eye(p) / 20),
               (1, 2, 3 * h * sp.eye(p) / 20)], sp.eye(p))
    # A different kernel cannot be replaced by an arbitrarily nearby line.
    a, b, c = sp.Matrix([1, 0]), sp.Matrix([1, sp.Rational(1, 2) ** 80]), sp.Matrix([0, 1])
    check("near-parallel singular ranges and mixed ranks", 3,
          [(0, 2, a * a.T), (0, 2, b * b.T), (0, 2, sp.zeros(2)),
           (0, 1, a * a.T), (1, 2, c * c.T)], sp.zeros(2))
    check("incompatible owners and full-rank edge", 4,
          [(0, 1, a * a.T), (1, 3, sp.zeros(2)),
           (0, 2, c * c.T), (2, 3, sp.zeros(2)), (0, 3, sp.eye(2))], sp.zeros(2))
    # Force a proper oblique range, extreme conditioning, and signed entries.
    V = sp.Matrix([[1, 0], [2, sp.Rational(1, 2) ** 60], [-1, -sp.Rational(1, 2) ** 60]])
    lift = lambda matrix: V * matrix * V.T
    h = eta / 4
    A = sp.Matrix([[h / 2, -h / 5], [-h / 5, h / 2]])
    B = sp.Matrix([[3 * h / 5, -h / 10], [-h / 10, 3 * h / 5]])
    check("oblique rank-two range with signed collisions", 3,
          [(0, 2, lift(A)), (0, 2, lift(B)), (0, 1, sp.zeros(3)),
           (1, 2, lift(A)), (0, 2, sp.eye(3))], lift(sp.eye(2)))
    rng = random.Random(621441)
    for p in (2, 3):
        for instance in range(3):
            def random_matrix():
                vector = sp.Matrix([sp.Rational(rng.randrange(-2, 3), 3) for _ in range(p)])
                return sp.Rational(rng.randrange(1, 5), 4) * vector * vector.T
            prior = sp.zeros(p) if instance == 0 else random_matrix()
            edges = [(0, 1, random_matrix()), (1, 3, random_matrix()),
                     (0, 2, random_matrix()), (2, 3, random_matrix()),
                     (0, 3, random_matrix())]
            check(f"seeded rational p={p} instance={instance}", 4, edges, prior)
    for epsilon in (sp.Rational(1, 10000), sp.Rational(1, 7), sp.Rational(999, 1000)):
        delta, eta_memory = epsilon / 8, epsilon / 4
        lower = (1 - eta_memory) * (1 - delta) / (1 + delta)
        upper = (1 + eta_memory) * (1 + delta) / (1 - delta)
        assert lower >= 1 - epsilon and upper <= 1 + epsilon
        counts["memory_loss_checks"] += 1
    assert counts["different_length_merges"] > 0
    assert counts["incompatible_owner_trials"] > 0
    assert counts["prior_range_rejections"] > 0
    assert counts["edge_range_deletions"] > 0
    assert counts["repeated_owner_trials"] > 0
    note = HERE.parent.parent / "notes/research-20260912-dag-psd-approximation-set.md"
    report = {"status": "passed", "scope": "Exact small-instance full-basis proof stress checks",
              "counts": dict(counts), "cases": cases,
              "candidate_note_sha256": hashlib.sha256(note.read_bytes()).hexdigest(),
              "reviewer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "seconds": perf_counter() - started}
    output = HERE / "results/psd-approximation-set-independent-review.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
