"""Exact independent checks for the polynomial tube review.

The closed-form trajectories below are separate enclosure oracles. This script
does not certify arbitrary physical metadata or an arbitrary callable RHS.
"""

from fractions import Fraction as Q
from dataclasses import replace
import hashlib
import itertools
import json
from pathlib import Path
import random

from extended_rpd import PolynomialModel
from polynomial_tubes import Interval, TubeFailure, _round_outward, certify_tubes
from ode_support_experiment import compile_slabs, round_physical_supports
from rational_affine_flow import certify_affine_flow


def main():
    counts = {"interval_corner_checks": 0, "outward_rounding_checks": 0,
              "analytic_state_checks": 0, "strict_inclusion_coordinates": 0,
              "failure_checks": 0, "exact_composition_checks": 0,
              "physical_support_corner_checks": 0}
    rng = random.Random(190926)
    intervals = []
    for _ in range(32):
        a, b = sorted(Q(rng.randrange(-30, 31), rng.randrange(1, 12)) for _ in range(2))
        intervals.append(Interval(a, b))
    for a, b in itertools.product(intervals, repeat=2):
        for x, y in itertools.product((a.lower, a.upper), (b.lower, b.upper)):
            for actual, computed in ((x+y, a+b), (x-y, a-b), (x*y, a*b)):
                assert computed.lower <= actual <= computed.upper
                counts["interval_corner_checks"] += 1
    for denominator in (1, 2, 3, 7, 100, 10**12):
        for numerator in range(-31, 32):
            for divisor in range(1, 12):
                value = Q(numerator, divisor)
                rounded = _round_outward(Interval(value, value), denominator)
                assert rounded.lower <= value <= rounded.upper
                assert value - rounded.lower < Q(1, denominator)
                assert rounded.upper - value < Q(1, denominator)
                assert (rounded.lower*denominator).denominator == 1
                assert (rounded.upper*denominator).denominator == 1
                counts["outward_rounding_checks"] += 1

    def check(model, duration, steps, solution, points, **options):
        certificate = certify_tubes(model, duration, steps, **options)
        assert certificate.steps == len(certificate.slabs) == steps
        for j, slab in enumerate(certificate.slabs):
            assert slab.start == j*duration/steps
            assert slab.duration == duration/steps
            assert slab.initial == (certificate.initial if j == 0 else certificate.slabs[j-1].endpoint)
            for raw, image, refined in zip(slab.raw_box, slab.picard_image, slab.refined_box):
                assert raw[0] < image[0] <= image[1] < raw[1]
                assert raw[0] <= refined[0] <= refined[1] <= raw[1]
                counts["strict_inclusion_coordinates"] += 1
            for p in points:
                for theta in (Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)):
                    t = slab.start + theta*slab.duration
                    for value, bound in zip(solution(p, t), slab.refined_box):
                        assert bound[0] <= value <= bound[1]
                        counts["analytic_state_checks"] += 1
                endpoint = solution(p, slab.start+slab.duration)
                for value, bound in zip(endpoint, slab.endpoint):
                    assert bound[0] <= value <= bound[1]
                    counts["analytic_state_checks"] += 1
        return certificate

    # Rational closed-form nonlinear solutions, including a near-pole horizon.
    for sign, horizon in ((1, Q(1, 4)), (1, Q(3, 4)), (-1, Q(1))):
        model = PolynomialModel((), ((0, 5),), lambda p, x, s=sign: [s*x[0]*x[0]], ((1,),))
        check(model, horizon, 60, lambda p, t, s=sign: (1/(1-s*t),), [()])

    # An autonomous polynomial lift with exact x=t, y=t^2 trajectories.
    lift = PolynomialModel((), ((0, 1), (0, 1)), lambda p, x: [1, 2*x[0]], ((0,), (0,)))
    lift_certificate = check(lift, Q(1), 40, lambda p, t: (t, t*t), [()], grid_denominator=None)
    assert lift_certificate.slabs[0].inflations > 0

    # Parameter-dependent affine invariants, mixed signs, and a negative pivot.
    affine = PolynomialModel(
        ((Q(-1, 2), Q(1, 2)), (1, 2)), ((-5, 5),)*3,
        lambda p, x: [p[0], -p[0], 0],
        ((0, 1, 0), (1, -1, 0), (Q(1, 2), Q(1, 2), 0)),
        ((1, 1, 0), (-1, -1, 2), (-2, -2, 0)), (0, 0, 0),
        ((1, 0), (0, 1), (-2, 0)))
    pgrid = list(itertools.product((Q(-1, 2), Q(0), Q(1, 2)), (Q(1), Q(3, 2), Q(2))))
    for sweeps in (0, 1, 3):
        check(affine, Q(1), 24,
              lambda p, t: (p[1]+p[0]*t, p[0]-p[1]-p[0]*t, (p[0]+p[1])/2),
              pgrid, row_sweeps=sweeps)

    # A positive margin certifies an equilibrium even without endpoint rounding.
    equilibrium = PolynomialModel((), ((-1, 1),), lambda p, x: [0], ((0,),))
    equilibrium_certificate = check(equilibrium, Q(1), 3, lambda p, t: (Q(0),), [()],
                                    grid_denominator=None)
    assert all(slab.endpoint == ((Q(0), Q(0)),) for slab in equilibrium_certificate.slabs)

    # Independently known exact physical solutions test the entire composition.
    riccati = PolynomialModel(((Q(-1, 2), Q(1, 2)),), ((Q(4, 5), Q(13, 10)),),
                              lambda p, x: [p[0]*x[0]*x[0]], ((0, 1),))
    cases = ((lift, Q(1), 40, (), [()], lambda p: (Q(1), Q(1))),
             (affine, Q(1), 24, (Q(0), Q(3, 2)), pgrid,
              lambda p: (p[1]+p[0], -p[1], (p[0]+p[1])/2)),
             (riccati, Q(1, 4), 12, (Q(0),), [(Q(j, 10),) for j in range(-5, 6)],
              lambda p: (1/(1-p[0]/4),)))
    for model, horizon, steps, nominal, points, solution in cases:
        tube = certify_tubes(model, horizon, steps)
        for sweeps, denominator in itertools.product((0, 1), (None, 1, 7, 10**6)):
            slabs = compile_slabs(model, nominal, horizon, steps, tubes=tube, row_sweeps=sweeps,
                                  support_denominator=denominator)
            flow = certify_affine_flow(slabs, model.initial_signed_coefficients(), model.parameter_box)
            for p in points:
                x = solution(p)
                signed = (*x, *(-value for value in x))
                for lower, true in zip(flow.evaluate(p), signed):
                    assert lower <= true
                    counts["exact_composition_checks"] += 1
    # Rounding must preserve the physical-manifold inequality at every box corner.
    rounding_model = PolynomialModel(((1, 2), (-3, -1)), ((2, 4), (-2, -1), (0, Q(1, 3))),
                                    lambda p, x: [0, 0, 0], ((0, 0, 0),)*3)
    for _ in range(20):
        rows = []
        for output in range(6):
            row = [Q(rng.randrange(-200, 201), rng.randrange(1, 50)) for _ in range(9)]
            for j in range(6):
                if j != output:
                    row[2+j] = abs(row[2+j])
            rows.append(tuple(row))
        for denominator in (1, 2, 7, 10**6):
            rounded = round_physical_supports(rows, rounding_model, denominator)
            for output, row in enumerate(rounded):
                assert all(value >= 0 for j, value in enumerate(row[2:-1]) if j != output)
                assert all((value*denominator).denominator == 1 for value in row)
            for p in itertools.product(*rounding_model.parameter_box):
                for x in itertools.product(*rounding_model.state_box):
                    point = (*p, *x, *(-value for value in x), Q(1))
                    for original, changed in zip(rows, rounded):
                        assert sum(a*b for a, b in zip(changed, point)) <= sum(a*b for a, b in zip(original, point))
                        counts["physical_support_corner_checks"] += 1
    # Structural metadata/grid guards prevent accidentally reusing another tube.
    eqtube = equilibrium_certificate
    altered = (replace(eqtube, duration=Q(2)), replace(eqtube, steps=2),
               replace(eqtube, slabs=eqtube.slabs[:-1]),
               replace(eqtube, parameter_box=((Q(0), Q(0)),)),
               replace(eqtube, physical_box=((Q(-2), Q(2)),)),
               replace(eqtube, initial_coefficients=((Q(1),),)),
               replace(eqtube, invariant_A=((Q(1),),)),
               replace(eqtube, invariant_b=(Q(0),)),
               replace(eqtube, invariant_D=((),)),
               replace(eqtube, slabs=(replace(eqtube.slabs[0], start=Q(1)), *eqtube.slabs[1:])),
               replace(eqtube, slabs=(replace(eqtube.slabs[0], duration=Q(1)), *eqtube.slabs[1:])))
    for tube in altered:
        try:
            compile_slabs(equilibrium, (), Q(1), 3, tubes=tube)
        except ValueError as error:
            assert "metadata mismatch" in str(error)
            counts["failure_checks"] += 1
        else:
            raise AssertionError("Mismatched tube metadata was accepted")

    # Exact failure of convergence at fixed denominator, without loss of validity.
    drift = PolynomialModel((), ((0, 1),), lambda p, x: [Q(1, 3)], ((0,),))
    nonconvergence = []
    for steps in (2, 3, 10, 40, 100):
        certificate = check(drift, Q(1), steps, lambda p, t: (t/3,), [()],
                            inflation=0, margin=Q(1, 3), grid_denominator=1)
        assert certificate.slabs[-1].endpoint == ((Q(0), Q(2, 3)),)
        unrounded = certify_tubes(drift, 1, steps, inflation=0, margin=Q(1, 3), grid_denominator=None)
        assert unrounded.slabs[-1].endpoint == ((Q(1, 3), Q(1, 3)),)
        nonconvergence.append({"steps": steps, "rounded_endpoint": certificate.slabs[-1].endpoint,
                               "unrounded_endpoint": unrounded.slabs[-1].endpoint})

    # Failure is not a nonexistence certificate: a coarse stable decay also fails.
    decay = PolynomialModel((), ((0, 1),), lambda p, x: [-x[0]], ((1,),))
    exploding = PolynomialModel((), ((0, 100),), lambda p, x: [x[0]*x[0]], ((1,),))
    for model, duration in ((decay, 2), (exploding, 1)):
        try:
            certify_tubes(model, duration, 1, max_inflations=3)
        except TubeFailure as failure:
            assert failure.slab_index == 0 and failure.max_inflations == 3
            assert failure.raw_box and failure.picard_image
            counts["failure_checks"] += 1
        else:
            raise AssertionError("Expected explicit failure on the coarse fixed grid")
    for options in ({"steps": 0}, {"steps": True}, {"steps": 1, "margin": 0},
                    {"steps": 1, "duration": 0}, {"steps": 1, "inflation": -1},
                    {"steps": 1, "max_inflations": -1}, {"steps": 1, "row_sweeps": True},
                    {"steps": 1, "grid_denominator": 0}, {"steps": 1, "grid_denominator": 1.5},
                    {"steps": 1, "grid_denominator": True}, {"steps": 1, "margin": 0.001}):
        kwargs = {"duration": 1, **options}
        try:
            certify_tubes(equilibrium, **kwargs)
        except (ValueError, TypeError):
            counts["failure_checks"] += 1
        else:
            raise AssertionError(f"Invalid exact-input options were accepted: {kwargs}")
    # False metadata can fail loudly, but consistency alone cannot validate it.
    invalid = PolynomialModel((), ((0, 1),), lambda p, x: [0], ((2,),))
    try:
        certify_tubes(invalid, 1, 2)
    except ValueError as error:
        assert "physical-box intersection" in str(error)
        counts["failure_checks"] += 1
    else:
        raise AssertionError("Contradictory initial physical bound was accepted")

    root = Path(__file__).parent
    return {"status": "passed", "counts": counts, "fixed_denominator_counterexample": nonconvergence,
            "source_sha256": {name: hashlib.sha256((root/name).read_bytes()).hexdigest()
                              for name in ("polynomial_tubes.py", "extended_rpd.py", "ode_support_experiment.py",
                                           "rational_affine_flow.py", Path(__file__).name)}}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, default=str))
