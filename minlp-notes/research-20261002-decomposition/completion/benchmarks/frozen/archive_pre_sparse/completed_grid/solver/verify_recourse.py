"""Replay original-model recourse certificates without solving QPs or LPs."""

from fractions import Fraction as F
import json
from pathlib import Path
import argparse

from certified_grid import BoxQP, rational


class RecourseCertificateError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise RecourseCertificateError(message)


def _positive_semidefinite(matrix):
    """Symmetric Schur complements with a positive diagonal pivot."""
    a = [list(row) for row in matrix]
    while a:
        if any(a[i][i] < 0 for i in range(len(a))):
            return False
        pivot = next((i for i in range(len(a)) if a[i][i] > 0), None)
        if pivot is None:
            return all(not v for row in a for v in row)
        rest = [i for i in range(len(a)) if i != pivot]
        a = [[a[i][j] - a[i][pivot] * a[pivot][j] / a[pivot][pivot]
              for j in rest] for i in rest]
    return True


def _affine_range(a, b, bounds):
    lo = hi = a
    for coefficient, (left, right) in zip(b, bounds):
        lo += min(coefficient * left, coefficient * right)
        hi += max(coefficient * left, coefficient * right)
    return lo, hi


def verify_selector(problem, proof):
    """Check PSD and a whole-parameter-box affine KKT identity exactly."""
    try:
        private, attachments = tuple(proof["private"]), tuple(proof["attachments"])
        n = len(problem.b)
        for indices in (private, attachments):
            _require(len(set(indices)) == len(indices) and
                     all(type(i) is int and 0 <= i < n for i in indices), "invalid indices")
        _require(private and not set(private) & set(attachments), "invalid partition")
        a = tuple(map(rational, proof["a"]))
        B = tuple(tuple(map(rational, row)) for row in proof["B"])
        _require(len(a) == len(private) == len(B) and
                 all(len(row) == len(attachments) for row in B), "affine dimensions mismatch")
        if proof["kind"] == "fixed":
            _require(not attachments, "fixed elimination has attachments")
            _require(all(problem.bounds[i][0] == problem.bounds[i][1] == value
                         for i, value in zip(private, a)), "coordinate is not fixed")
            return True
        _require(proof["kind"] == "affine", "unknown elimination kind")
        _require(not set(private) & problem.integers, "integer convex recourse is unsupported")
        _require(all(lo < hi for lo, hi in problem.bounds), "fixed coordinates must be substituted")
        _require(all(not problem.A[i][j] for i in private for j in range(n)
                     if j not in private and j not in attachments), "an attachment is missing")
        C = [[problem.A[i][j] for j in private] for i in private]
        _require(_positive_semidefinite(C), "private Hessian is not PSD")
        zbox = [problem.bounds[j] for j in attachments]
        for row, i in enumerate(private):
            lo, hi = problem.bounds[i]
            lower, upper = _affine_range(a[row], B[row], zbox)
            _require(lo <= lower <= upper <= hi, "response violates private bounds")
            gamma = problem.b[i] + sum((C[row][t] * a[t] for t in range(len(private))), F(0))
            T = [problem.A[i][j] + sum((C[row][t] * B[t][col]
                 for t in range(len(private))), F(0)) for col, j in enumerate(attachments)]
            grad_lo, grad_hi = _affine_range(gamma, T, zbox)
            if a[row] == lo and all(not v for v in B[row]):
                _require(grad_lo >= 0, "lower-bound KKT sign fails")
            elif a[row] == hi and all(not v for v in B[row]):
                _require(grad_hi <= 0, "upper-bound KKT sign fails")
            else:
                _require(not gamma and all(not v for v in T), "free gradient is not identically zero")
        return True
    except RecourseCertificateError:
        raise
    except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError) as exc:
        raise RecourseCertificateError("malformed affine selector") from exc


def verify_pipeline(certificate, problem=None, max_table_states=1000000):
    """Check every elimination, reduced proof, original lift and value.

    Supply problem when checking a certificate for an externally expected
    instance. Otherwise the certificate's explicitly embedded model is used.
    """
    from recourse import transform, lift
    try:
        _require(certificate["schema"] == "recourse-qp-v1", "unknown recourse schema")
        _require(type(certificate["exact_requested"]) is bool, "invalid exact-output request flag")
        original = BoxQP.from_dict(certificate["problem"])
        _require(problem is None or original.to_dict() == problem.to_dict(), "original model mismatch")
        current, history = original, []
        for proof in certificate["steps"]:
            _require(current is not None, "extra transformation after constant model")
            verify_selector(current, proof)
            history.append((current, proof))
            current, constant = transform(current, proof)
        inner = certificate["inner"]
        if current is None:
            _require(inner is None and certificate["method"] == "constant", "invalid constant proof")
            point, lower, upper, status = (), constant, constant, "exact"
        else:
            _require(inner is not None, "missing reduced proof")
            # A decomposition is an algorithmic witness; the mathematical
            # reduced model must match even if another valid tree was used.
            inner_problem = BoxQP.from_dict(inner["problem"])
            for key in ("A", "b", "bounds", "integers", "constant"):
                _require(inner_problem.to_dict()[key] == current.to_dict()[key], "reduced model mismatch")
            if certificate["method"] == "mincut":
                from mincut_adapter import verify_mincut
                _require(inner["exact_requested"] == certificate["exact_requested"], "exact-output request mismatch")
                _require(verify_mincut(inner), "invalid minimum-cut proof")
            else:
                _require(certificate["method"] == "grid", "unknown reduced method")
                _require((inner["schema"] == "certified-grid-qp-exact-v1")
                         == certificate["exact_requested"], "exact-output request mismatch")
                from verify_certificate import verify_certificate
                verify_certificate(inner, max_table_states=max_table_states)
            point = tuple(map(rational, inner["point"]))
            lower, upper, status = rational(inner["lower"]), rational(inner["upper"]), inner["status"]
        for before, proof in reversed(history):
            point = lift(before, proof, point)
        _require(original.feasible(point) and original.value(point) == upper, "invalid original lift")
        _require(tuple(map(rational, certificate["point"])) == point, "lifted point mismatch")
        _require(rational(certificate["lower"]) == lower and rational(certificate["upper"]) == upper
                 and rational(certificate["gap"]) == upper - lower, "final bounds mismatch")
        _require(certificate["status"] == status, "termination status mismatch")
        epsilon = rational(certificate["epsilon"])
        _require(epsilon >= 0, "negative tolerance")
        if status in ("certified", "epsilon_optimal"):
            _require(upper - lower <= epsilon, "requested tolerance is not met")
        return {"valid": True, "lower": str(lower), "upper": str(upper),
                "gap": str(upper - lower), "removed_coordinates": len(original.b) - (len(current.b) if current else 0)}
    except RecourseCertificateError:
        raise
    except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError) as exc:
        raise RecourseCertificateError("malformed recourse certificate: " + str(exc)) from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify_pipeline(json.loads(args.certificate.read_text()))))


if __name__ == "__main__":
    main()
