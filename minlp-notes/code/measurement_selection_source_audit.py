"""Exact checks for the 2026-09-12 correlated measurement selection audit.

Run with Python and SymPy. An optional path to measure_optimize.py checks the
authors' two coefficient-building methods without importing their solver stack.
"""

import ast
import itertools
import sys
from pathlib import Path
from types import SimpleNamespace

import sympy as s


def information(covariance, sensitivity, selected):
    if not selected:
        return s.zeros(sensitivity.cols), s.zeros(sensitivity.cols)
    rows = list(selected)
    q = sensitivity[rows, :]
    marginal = q.T * covariance.extract(rows, rows).inv() * q
    gated = q.T * covariance.inv().extract(rows, rows) * q
    return marginal, gated


def subsets(n):
    for size in range(n + 1):
        yield from itertools.combinations(range(n), size)


def main():
    rho = s.Rational(3, 4)
    r = s.Matrix([[1, rho], [rho, 1]])
    q = s.ones(2, 1)
    marginal, gated = information(r, q, [0])
    assert marginal[0] == 1 and gated[0] == s.Rational(16, 7)
    full, full_gated = information(r, q, [0, 1])
    assert full == full_gated == s.Matrix([s.Rational(8, 7)])
    conditional_response = (1 - rho) ** 2 / (1 - rho**2)
    assert conditional_response == s.Rational(1, 7)
    print(f"two sensors: singleton marginal={marginal[0]}, gated={gated[0]}; "
          f"full={full[0]}; conditional response={conditional_response}")

    r3 = s.Matrix([[1, 0, rho], [0, 1, 0], [rho, 0, 1]])
    q3 = s.Matrix([1, s.Rational(6, 5), 0])
    singleton_values = [tuple(m[0] for m in information(r3, q3, [i])) for i in range(3)]
    assert singleton_values == [(1, s.Rational(16, 7)), (s.Rational(36, 25), s.Rational(36, 25)), (0, 0)]
    print(f"three-sensor ranking reversal (marginal,gated): {singleton_values}")

    b = s.Matrix([[1, s.Rational(1, 10), s.Rational(1, 10)],
                  [s.Rational(1, 10), 4, s.Rational(1, 2)],
                  [s.Rational(1, 10), s.Rational(1, 2), 8]])
    r6 = s.kronecker_product(s.Matrix([[1, s.Rational(1, 2)], [s.Rational(1, 2), 1]]), b)
    assert all(r6[:i, :i].det() > 0 for i in range(1, 7))
    assert r6.inv()[:3, :3] == s.Rational(4, 3) * b.inv()
    singleton_inflations = [s.factor(r6[i, i] * r6.inv()[i, i]) for i in range(3)]
    print(f"kinetics covariance determinant={r6.det()}; singleton inflation={singleton_inflations}")
    print(f"kinetics singleton decimal inflation={[float(x) for x in singleton_inflations]}")

    # Liu's exact identity, checked at every subset of the six-channel block.
    a = s.Rational(1, 4)
    remainder = r6 - a * s.eye(6)
    assert all(remainder[:i, :i].det() > 0 for i in range(1, 7))
    inv_remainder = remainder.inv()
    q6 = s.Matrix([[1, 2], [2, -1], [3, 1], [1, 2], [2, -1], [3, 1]])
    for selected in subsets(6):
        d = s.diag(*[int(i in selected) for i in range(6)])
        identity = (q6.T * inv_remainder * q6
                    - q6.T * inv_remainder * (inv_remainder + d / a).inv() * inv_remainder * q6)
        marginal, gated = information(r6, q6, selected)
        assert identity == marginal
        difference = gated - marginal
        assert difference[0, 0] >= 0 and difference[1, 1] >= 0 and difference.det() >= 0
    print("Liu identity and positive semidefinite inflation: all 64 subsets passed")

    for selected in subsets(3):
        marginal, gated = information(s.diag(1, 4, 8), q3, selected)
        assert marginal == gated
    print("independent-noise control: all 8 subsets passed")

    if len(sys.argv) == 2:
        check_author_methods(Path(sys.argv[1]))


def check_author_methods(path):
    import numpy as np

    source = ast.parse(path.read_text())
    original = next(node for node in source.body
                    if isinstance(node, ast.ClassDef) and node.name == "MeasurementOptimizer")
    names = {"_split_sigma", "assemble_unit_fims"}
    methods = [node for node in original.body
               if isinstance(node, ast.FunctionDef) and node.name in names]
    assert {node.name for node in methods} == names
    # Run the unchanged, inspected methods with only their NumPy dependency.
    extracted = ast.ClassDef(name="AuditedMethods", bases=[], keywords=[],
                             body=methods, decorator_list=[])
    module = ast.fix_missing_locations(ast.Module(body=[extracted], type_ignores=[]))
    namespace = {"np": np}
    exec(compile(module, str(path), "exec"), namespace)
    obj = namespace["AuditedMethods"]()
    obj.static_idx_dynamic_flatten = []
    obj.dynamic_idx_dynamic_flatten = [0, 1]
    obj.dynamic_to_flatten = [0, 1]
    obj.num_measure_dynamic_flatten = 2
    obj.jac_dynamic_flatten = [[1.0], [1.0]]
    obj.sens_info = SimpleNamespace(n_parameters=1, Nt=1)
    obj.precompute_print_level = 0
    obj._split_sigma(np.array([[1.0, 0.75], [0.75, 1.0]]))
    obj.assemble_unit_fims()
    singleton = np.array(obj.unit_fims[0])[0, 0]
    full = sum(np.array(unit) for unit in obj.unit_fims)[0, 0]
    assert np.isclose(singleton, 16 / 7) and np.isclose(full, 8 / 7)
    print(f"unchanged author methods: singleton={singleton:.12g}, full={full:.12g}")


if __name__ == "__main__":
    main()
