"""Independent full-state LP comparisons on arbitrary directed multigraphs.

Run from the repository root: PYTHONPATH=code python -m network_simplex_compressed.verify
"""

from fractions import Fraction as F
from types import SimpleNamespace

import numpy as np

from network_simplex_compressed import CompressedNetworkSimplex, separate
from network_simplex_benchmarks.baselines import Instance, full_ef, full_ef_membership, incidence


def main():
    optimization_checks = membership_checks = certificate_checks = 0
    for seed in range(100):
        rng = np.random.default_rng(seed)
        vertices = int(rng.integers(2, 11))
        E = int(rng.integers(1, 25))
        arcs = [(int(rng.integers(vertices)), int(rng.integers(vertices)), int(rng.integers(1, 9))) for _ in range(E)]
        reference = np.array([rng.integers(u+1) for _, _, u in arcs])
        m = int(rng.integers(0, 9))
        observations = [(e, j) for e in range(E) for j in range(m) if rng.random() < .2]
        instance = Instance(arcs, np.zeros(vertices), m, observations, reference)
        instance.balances = incidence(instance) @ reference
        model = CompressedNetworkSimplex(arcs, -instance.balances, m, observations)
        reduced = CompressedNetworkSimplex(arcs, -instance.balances, m, observations, eliminate_observed=True)
        assert model.n-model.original_n == sum(b.rank*len(b.labels) for b in model.blocks)
        for b in model.blocks:
            assert len(b.rows) <= (1 if b.rank == 1 else 3*b.rank-3)
        for rows in (model.eq, model.ub):
            assert all(abs(a) == 1 for terms, _ in rows for k, a in terms.items() if k >= model.original_n)
        expected_auxiliary = 0
        for b in model.blocks:
            vertices_in_block = {v for e in b.edges for v in arcs[e][:2]}
            for j in b.labels:
                parent = {v: v for v in vertices_in_block}
                def find(v):
                    while parent[v] != v:
                        v = parent[v]
                    return v
                unobserved = [e for e in b.edges if (e, j) not in observations]
                for e in unobserved:
                    a, h, _ = arcs[e]
                    parent[find(a)] = find(h)
                expected_auxiliary += len(unobserved)-len(parent)+len({find(v) for v in parent})
        assert reduced.n-reduced.original_n == expected_auxiliary
        for rows in (reduced.eq, reduced.ub):
            assert all(abs(a) == 1 for terms, _ in rows for k, a in terms.items() if k >= reduced.original_n)
        for trial in range(3):
            c = rng.normal(size=model.original_n)
            fixed = None if trial == 0 else (np.zeros(m) if trial == 1 else np.full(m, 1/(m+1)))
            got = model.optimize(c, y_fixed=fixed)
            expected = full_ef(instance, c, y_fixed=fixed)
            assert got.success and expected.success, (seed, trial, got, expected)
            assert abs(got.fun-expected.fun) < 1e-7, (seed, trial, got.fun, expected.fun)
            got_reduced = reduced.optimize(c, y_fixed=fixed)
            assert got_reduced.success and abs(got_reduced.fun-expected.fun) < 1e-7, (seed, trial, got_reduced)
            optimization_checks += 2
        # Exact rank-one point, then perturb a product while holding x,y fixed.
        y = tuple(F(1, m+1) for _ in range(m))
        z = {(e, j): F(int(reference[e]), m+1) for e, j in observations}
        point = SimpleNamespace(x=tuple(map(int, reference)), y=y, z=z)
        assert model.membership(point).success
        assert reduced.membership(point).success
        membership_checks += 2
        if observations:
            for delta in (F(-1, 3), F(1, 3), F(3)):
                perturbed = dict(z); perturbed[observations[0]] += delta
                point = SimpleNamespace(x=tuple(map(int, reference)), y=y, z=perturbed)
                got = model.membership(point)
                expected = full_ef_membership(instance, np.array(reference, dtype=float), np.array(y, dtype=float),
                                              np.array([perturbed[o] for o in observations], dtype=float))
                assert got.success == expected.success, (seed, delta, got, expected)
                assert reduced.membership(point).success == expected.success
                membership_checks += 2
                for candidate in (model, reduced):
                    certificate = separate(candidate, point)
                    if expected.success:
                        assert certificate.status == "numerically_feasible", (seed, certificate)
                    else:
                        assert certificate.status == "certified_outside", (seed, certificate)
                        assert certificate.cut.evaluate(point) > 0
                        c = np.zeros(model.original_n)
                        for key, value in certificate.cut.coefficients.items():
                            k = key[1] if key[0] == "x" else (E+key[1] if key[0] == "y" else E+m+observations.index(key[1:]))
                            c[k] = -float(value)
                        check = full_ef(instance, c)
                        assert check.success and -check.fun+float(certificate.cut.constant) < 1e-7, (seed, check)
                        certificate_checks += 1
    # Structural and capacity infeasibility, self-loop degeneracy, empty graph.
    for arcs, balances in [([], [1]), ([(0, 1, 0)], [-1, 1]), ([(0, 0, -1)], [0]),
                           ([(0, 1, 0), (1, 0, 0)], [-1, 1])]:
        model = CompressedNetworkSimplex(arcs, balances, 1, [])
        assert model.optimize(np.zeros(model.original_n)).status == 2
    empty = CompressedNetworkSimplex([], [], 0, [])
    assert empty.optimize([]).success
    loop = CompressedNetworkSimplex([(0, 0, 0)], [0], 2, [(0, 0)])
    assert loop.optimize([0, 0, 0, -1]).fun == 0
    print(f"PASS: {optimization_checks} objective comparisons; {membership_checks} membership checks; "
          f"{certificate_checks} exact Farkas cuts also checked by full-EF optimization; six degenerate models")


if __name__ == "__main__":
    main()
