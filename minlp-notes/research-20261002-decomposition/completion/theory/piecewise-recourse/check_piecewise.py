"""Targeted exact checks for scalar recourse and piecewise curvature."""
from dataclasses import replace
from fractions import Fraction as Q
from itertools import product
import json
import random

from scalar_piecewise import (Block, Piece, construct, evaluate, is_psd,
                              pack_pieces, unpack_pieces, verify)


def separating_block(magnitude):
    m = Q(magnitude)
    return Block(((2*m+2, 2*m), (2*m, 2*m)), (-2*m-4, -2*m), (1, 0),
                 (0, 0), (1, 1), Q(0), Q(3, 4), 2*m+8, -2, Q(1, 4))


def analytic_response(magnitude, z):
    m = Q(magnitude)
    if z <= Q(1, 4):
        return (Q(1, 2)-2*z)**2, (Q(0), z)
    if z <= Q(1, 2):
        return Q(0), (2*z-Q(1, 2), Q(1, 2)-z)
    return m/(m+1)*(z-Q(1, 2))**2, (((m+2)*z-Q(1, 2))/(m+1), Q(0))


def must_reject(call):
    try:
        call()
    except ValueError:
        return 1
    raise AssertionError("invalid input/certificate was accepted")


def main():
    counts = {"family_blocks": 0, "analytic_response_checks": 0,
              "interpolation_checks": 0, "growth_checks": 0,
              "random_blocks": 0, "feasible_value_checks": 0,
              "rejected_invalid_inputs": 0, "singular_kink_checks": 0,
              "empty_private_checks": 0, "budget_interruptions": 0,
              "serialization_roundtrips": 0, "invalid_serializations": 0}
    curvature_rows = []
    for magnitude in (1, 2, 10, 10**6, 2**40):
        block = separating_block(magnitude)
        pieces = construct(block)
        assert len(pieces) == 3
        assert [(p.lower, p.upper) for p in pieces] == [
            (Q(0), Q(1, 4)), (Q(1, 4), Q(1, 2)), (Q(1, 2), Q(3, 4))]
        ell = verify(block, pieces)
        reloaded = unpack_pieces(json.loads(json.dumps(pack_pieces(pieces))))
        assert reloaded == pieces
        assert verify(block, reloaded) == ell
        counts["serialization_roundtrips"] += 1
        assert ell == 8
        assert len({p.slope for p in pieces}) == 3
        counts["family_blocks"] += 1
        curvature_rows.append({"M": str(magnitude), "direct_curvature": str(block.retained_hessian),
                               "certified_reduced_curvature": str(ell), "regions": len(pieces)})
        for j in range(97):
            z = Q(j, 128)
            value, response = evaluate(pieces, z)
            assert (value, response) == analytic_response(magnitude, z)
            assert block.objective(response, z) == value
            counts["analytic_response_checks"] += 1
        for a, b in product((Q(0), Q(1, 8), Q(1, 4), Q(3, 8), Q(1, 2), Q(3, 4)), repeat=2):
            if a >= b:
                continue
            va = evaluate(pieces, a)[0]
            vb = evaluate(pieces, b)[0]
            for lam in (Q(1, 7), Q(1, 3), Q(1, 2), Q(5, 7)):
                z = (1-lam)*a + lam*b
                vz = evaluate(pieces, z)[0]
                # Exact unbiased corner interpolation with the reduced curvature.
                assert (1-lam)*va + lam*vb <= vz + ell*lam*(1-lam)*(b-a)**2/2
                counts["interpolation_checks"] += 1
        for z, v, y1, y2 in product((Q(0), Q(1, 5), Q(1, 2), Q(3, 4)),
                                     (Q(0), Q(1, 3), Q(1)),
                                     (Q(0), Q(1, 3), Q(1)),
                                     (Q(0), Q(1, 5), Q(1))):
            t, u, w = z-Q(1, 5), y1, y2-Q(1, 5)
            r, s = u+w-t, u-2*t
            base = z*z+block.objective((y1, y2), z)-Q(1, 20)
            assert base == t*t+magnitude*r*r+s*s+u/5
            fullgap = base-v*v+3*v-t*v
            assert fullgap >= (t*t+u*u+w*w+v*v)/36
            counts["growth_checks"] += 1

    rng = random.Random(41231)
    for n in (1, 2, 3, 4):
        for repetition in range(5):
            matrix = [[rng.randrange(-2, 3) for _ in range(n)] for _ in range(n)]
            hessian = tuple(tuple(sum(matrix[k][i]*matrix[k][j] for k in range(n))
                                  + int(i == j) for j in range(n)) for i in range(n))
            block = Block(hessian, tuple(rng.randrange(-5, 6) for _ in range(n)),
                          tuple(rng.randrange(-2, 3) for _ in range(n)),
                          (Q(-1, 2),)*n, (Q(1),)*n, Q(-1), Q(1),
                          rng.randrange(-3, 4), rng.randrange(-2, 3), Q(1, 7))
            pieces = construct(block)
            ell = verify(block, pieces)
            counts["random_blocks"] += 1
            for j in range(33):
                z = Q(j, 16)-1
                value, response = evaluate(pieces, z)
                assert block.objective(response, z) == value
                for _ in range(3):
                    y = tuple(Q(rng.randrange(7), 4)-Q(1, 2) for _ in range(n))
                    assert block.objective(y, z) >= value
                    counts["feasible_value_checks"] += 1
            for _ in range(30):
                a, b = sorted((Q(rng.randrange(33), 16)-1, Q(rng.randrange(33), 16)-1))
                lam = Q(rng.randrange(1, 10), 10)
                z = (1-lam)*a+lam*b
                assert ((1-lam)*evaluate(pieces, a)[0]+lam*evaluate(pieces, b)[0]
                        <= evaluate(pieces, z)[0]+ell*lam*(1-lam)*(b-a)**2/2)
                counts["interpolation_checks"] += 1

    # A singular residual with a discontinuous response and a downward kink.
    kink = Block(((0,),), (1,), (0,), (-1,), (1,), Q(-1), Q(1))
    pieces = (
        Piece(Q(-1), Q(0), (Q(1),), (Q(0),), (Q(0),), (Q(0),),
              (Q(0),), (Q(-1),), (Q(0), Q(1), Q(0))),
        Piece(Q(0), Q(1), (Q(-1),), (Q(0),), (Q(0),), (Q(1),),
              (Q(0),), (Q(0),), (Q(0), Q(-1), Q(0))))
    assert verify(kink, pieces) == 0
    for j in range(65):
        z = Q(j, 32)-1
        assert evaluate(pieces, z)[0] == -abs(z)
        counts["singular_kink_checks"] += 1

    block = separating_block(10)
    pieces = construct(block)
    invalid_calls = [
        lambda: verify(block, pieces[:-1]),
        lambda: verify(block, pieces + (pieces[-1],)),
        lambda: verify(block, (replace(pieces[0], upper=Q(1, 5)),)+pieces[1:]),
        lambda: verify(block, (replace(pieces[0], value=(0, 0, 0)),)+pieces[1:]),
        lambda: verify(block, (replace(pieces[0], intercept=(Q(1, 100), 0)),)+pieces[1:]),
        lambda: verify(block, (replace(pieces[0], lower_multiplier_intercept=(-1, 0)),)+pieces[1:]),
        lambda: verify(block, (replace(pieces[0], value=(0.25, -2, 4)),)+pieces[1:]),
        lambda: construct(block, max_patterns=8),
        lambda: construct(kink),
        lambda: verify(replace(kink, C=((-1,),)), pieces),
    ]
    for call in invalid_calls:
        counts["rejected_invalid_inputs"] += must_reject(call)
    assert is_psd(((1, 1), (1, 1)))
    assert not is_psd(((0, 1), (1, 0)))
    empty = Block((), (), (), (), (), Q(-1), Q(1), 2, 1, Q(1, 3))
    empty_pieces = construct(empty)
    assert verify(empty, empty_pieces) == 2
    for z in (Q(-1), Q(0), Q(1, 7), Q(1)):
        expected = z*z+z+Q(1, 3)
        assert empty.objective((), z) == expected
        assert isinstance(empty.objective((), z), Q)
        assert evaluate(empty_pieces, z) == (expected, ())
        counts["empty_private_checks"] += 1
    for call in (lambda: empty.objective((Q(0),), Q(0)),
                 lambda: empty.objective((), 0.0),
                 lambda: block.objective((0.0, Q(0)), Q(0)),
                 lambda: block.objective((Q(0),), Q(0))):
        counts["rejected_invalid_inputs"] += must_reject(call)
    def interrupt():
        raise RuntimeError("cooperative budget exhausted")
    for call in (lambda: construct(block, budget_check=interrupt),
                 lambda: verify(block, pieces, budget_check=interrupt)):
        try:
            call()
        except RuntimeError as exc:
            assert str(exc) == "cooperative budget exhausted"
            counts["budget_interruptions"] += 1
        else:
            raise AssertionError("ignored budget callback")
    packed = pack_pieces(pieces)
    for bad in (True, False, 0.0, float("nan"), "0.25", "1/0", " 1/2", "1/2 ", "1e4", None):
        records = json.loads(json.dumps(packed))
        records[0]["lower"] = bad
        counts["invalid_serializations"] += must_reject(lambda: unpack_pieces(records))
    for mutate in (lambda d: d.pop("value"),
                   lambda d: d.update(extra="0"),
                   lambda d: d.update(slope="0"),
                   lambda d: d.update(value=["0", "0"])):
        records = json.loads(json.dumps(packed))
        mutate(records[0])
        counts["invalid_serializations"] += must_reject(lambda: unpack_pieces(records))
    records = json.loads(json.dumps(packed))
    records[0]["lower"] = int(pieces[0].lower)
    records[0]["upper"] = pieces[0].upper
    assert unpack_pieces(records) == pieces
    counts["serialization_roundtrips"] += 1
    print(json.dumps({"status": "passed", "counts": counts,
                      "curvature_separation": curvature_rows,
                      "scope": "exact scalar-attachment construction and certificate diagnostics; no global performance claim"}, indent=2))


if __name__ == "__main__":
    main()
