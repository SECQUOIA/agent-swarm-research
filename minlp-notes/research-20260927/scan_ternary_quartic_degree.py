"""Finite exact first-jet scan and numerical strict Hessian-Gram search.

The point is (alpha**e1, alpha**e2, alpha**e3), alpha**d=2.
Numerical solver output is discovery evidence, not an infeasibility proof.
"""

from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import sys

import cvxpy as cp
import numpy as np
import scipy.sparse as sparse
import sympy as sp


MONOMIALS = [a for a in product(range(5), repeat=3) if sum(a) <= 4]
XM = [a for a in product(range(3), repeat=3) if sum(a) <= 2]
VP = list(combinations(range(3), 2)) + [(i, i) for i in range(3)]
ROWS = [(a, i, j) for a in XM for i, j in VP]
ROW_INDEX = {row: k for k, row in enumerate(ROWS)}


def first_jet(degree, exponents):
    matrix = sp.zeros(4 * degree, len(MONOMIALS))
    for column, monomial in enumerate(MONOMIALS):
        power = sum(a * e for a, e in zip(monomial, exponents))
        quotient, remainder = divmod(power, degree)
        matrix[remainder, column] = sp.Rational(2) ** quotient
        for i in range(3):
            if monomial[i]:
                quotient, remainder = divmod(power - exponents[i], degree)
                matrix[(i + 1) * degree + remainder, column] = (
                    monomial[i] * sp.Rational(2) ** quotient)
    kernel = matrix.nullspace()
    return sp.Matrix.hstack(*kernel) if kernel else sp.zeros(35, 0)


def coefficient_maps():
    hessian = sp.zeros(len(ROWS), len(MONOMIALS))
    for column, monomial in enumerate(MONOMIALS):
        for i, j in VP:
            coefficient = monomial[i] * (monomial[j] - (i == j))
            if not coefficient:
                continue
            powers = list(monomial)
            powers[i] -= 1
            powers[j] -= 1
            hessian[ROW_INDEX[(tuple(powers), i, j)], column] = (
                coefficient * (1 if i == j else 2))
    basis = [((0, 0, 0), i) for i in range(3)]
    for k in range(3):
        powers = tuple(int(i == k) for i in range(3))
        basis.extend((powers, i) for i in range(3))
    row_indices, column_indices = [], []
    for k, (a, i) in enumerate(basis):
        for ell, (b, j) in enumerate(basis):
            powers = tuple(ai + bi for ai, bi in zip(a, b))
            row_indices.append(ROW_INDEX[(powers, min(i, j), max(i, j))])
            column_indices.append(12 * k + ell)
    gram = sparse.coo_matrix(
        (np.ones(144), (row_indices, column_indices)), shape=(60, 144)).tocsr()
    return hessian, gram


def search(kernel, hessian, gram):
    exact_coefficients = hessian * kernel
    coefficient_matrix = np.array(exact_coefficients, dtype=float)
    coefficient_matrix /= np.maximum(1, np.abs(coefficient_matrix).max(axis=0))
    matrix = cp.Variable((12, 12), symmetric=True)
    weights = cp.Variable(kernel.cols)
    margin = cp.Variable()
    constraints = [
        gram @ cp.vec(matrix, order="C") == coefficient_matrix @ weights,
        cp.trace(matrix) == 1,
        matrix - margin * np.eye(12) >> 0,
    ]
    problem = cp.Problem(cp.Maximize(margin), constraints)
    problem.solve(solver="CLARABEL", max_iter=250,
                  tol_gap_abs=1e-9, tol_gap_rel=1e-9, tol_feas=1e-9)
    answer = {"solver": "CLARABEL", "status": problem.status,
              "margin": None if margin.value is None else float(margin.value)}
    if matrix.value is not None:
        answer["gram_min_eigenvalue"] = float(np.linalg.eigvalsh(matrix.value).min())
        answer["coefficient_residual"] = float(np.max(np.abs(
            gram @ matrix.value.reshape(-1) - coefficient_matrix @ weights.value)))
    # A numerical dual is only a candidate. Project rationally onto the
    # exact annihilator of the Hessian coefficient space, then prove PD.
    if constraints[0].dual_value is not None:
        multiplier = sp.Matrix([sp.Rational(round(float(value) * 2**40), 2**40)
                                for value in constraints[0].dual_value])
        multiplier -= exact_coefficients * (
            (exact_coefficients.T * exact_coefficients).inv()
            * exact_coefficients.T * multiplier)
        assert exact_coefficients.T * multiplier == sp.zeros(kernel.cols, 1)
        adjoint = sp.Matrix(12, 12, lambda i, j:
                            multiplier[gram[:, 12*i+j].nonzero()[0][0]])
        assert adjoint == adjoint.T
        try:
            left, diagonal = adjoint.LDLdecomposition(hermitian=False)
            if all(diagonal[i, i] > 0 for i in range(12)):
                assert left * diagonal * left.T == adjoint
                answer["exact_exclusion"] = "positive definite rational dual annihilator"
                answer["dual_multiplier"] = [str(value) for value in multiplier]
                answer["dual_minimum_ldl_pivot"] = str(min(diagonal[i, i] for i in range(12)))
        except ZeroDivisionError:
            pass
    return answer


def main():
    hessian, gram = coefficient_maps()
    results = []
    counts = Counter()
    for degree in (7, 9, 11):
        for exponents in combinations(range(1, degree), 3):
            kernel = first_jet(degree, exponents)
            result = {"degree": degree, "exponents": exponents,
                      "first_jet_kernel_dimension": kernel.cols}
            if not kernel.cols:
                result["exact_exclusion"] = "zero polynomial space"
            else:
                pure = [MONOMIALS.index(tuple(4 if i == k else 0 for i in range(3)))
                        for k in range(3)]
                missing = [k for k, row in enumerate(pure)
                           if not any(kernel[row, j] for j in range(kernel.cols))]
                if missing:
                    result["exact_exclusion"] = "forced zero pure quartic coefficient"
                    result["missing_pure_quartic_variables"] = missing
                elif not any(kernel[0, j] for j in range(kernel.cols)):
                    result["exact_exclusion"] = "forced zero at rational origin"
                else:
                    result.update(search(kernel, hessian, gram))
                    print(json.dumps({key: value for key, value in result.items()
                                      if key not in ("dual_multiplier", "dual_minimum_ldl_pivot")}), flush=True)
            counts[(degree, result.get("exact_exclusion", "numerical SDP"))] += 1
            results.append(result)
    destination = Path(__file__).with_name("ternary-quartic-degree-scan-results.json")
    destination.write_text(json.dumps(results, indent=2) + "\n")
    for key, count in sorted(counts.items()):
        print(key, count)
    print("Numerical statuses alone are not exact infeasibility certificates.")


def verify_saved():
    """Verify the recorded exclusions with rational arithmetic only."""
    hessian, gram = coefficient_maps()
    destination = Path(__file__).with_name("ternary-quartic-degree-scan-results.json")
    records = json.loads(destination.read_text())
    expected = {(d, e) for d in (7, 9, 11) for e in combinations(range(1, d), 3)}
    actual = {(r["degree"], tuple(r["exponents"])) for r in records}
    assert len(records) == len(expected) == 196 and actual == expected
    counts = Counter()
    for record in records:
        kernel = first_jet(record["degree"], record["exponents"])
        assert kernel.cols == record["first_jet_kernel_dimension"]
        reason = record["exact_exclusion"]
        if reason == "zero polynomial space":
            assert kernel.cols == 0
        elif reason == "forced zero pure quartic coefficient":
            missing = record["missing_pure_quartic_variables"]
            assert missing
            for k in missing:
                row = MONOMIALS.index(tuple(4 if i == k else 0 for i in range(3)))
                assert all(kernel[row, j] == 0 for j in range(kernel.cols))
        elif reason == "forced zero at rational origin":
            assert all(kernel[0, j] == 0 for j in range(kernel.cols))
        elif reason == "positive definite rational dual annihilator":
            multiplier = sp.Matrix([sp.Rational(value) for value in record["dual_multiplier"]])
            assert len(multiplier) == 60
            assert (hessian * kernel).T * multiplier == sp.zeros(kernel.cols, 1)
            adjoint = sp.Matrix(12, 12, lambda i, j:
                                multiplier[gram[:, 12*i+j].nonzero()[0][0]])
            assert adjoint == adjoint.T
            left, diagonal = adjoint.LDLdecomposition(hermitian=False)
            assert all(diagonal[i, i] > 0 for i in range(12))
            assert left * diagonal * left.T == adjoint
        else:
            raise AssertionError(reason)
        counts[reason] += 1
    print("PASS: all 196 recorded exclusions verified with exact rational arithmetic")
    print(dict(counts))


if __name__ == "__main__":
    if sys.argv[1:] == ["--verify"]:
        verify_saved()
    elif not sys.argv[1:]:
        main()
    else:
        raise SystemExit("Usage: scan_ternary_quartic_degree.py [--verify]")
