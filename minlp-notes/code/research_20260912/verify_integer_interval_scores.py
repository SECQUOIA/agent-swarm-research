"""Exact reference checks and a saved-certificate arc benchmark."""

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import random
from time import perf_counter

from certify_noisy_markov import fraction, local_coefficients, matrix, rational, require_spd
from integer_interval_scores import IntegerIntervalScores, IntegerPattern, _outward, _product, _square


def exact_score(F, H, t, ages, coefficients, variance):
    p = len(H)
    adjusted = tuple(F[t][j] - sum((b*F[t-age][j] for age, b in zip(ages, coefficients)), Q(0))
                     for j in range(p))
    return sum((H[i][j]*adjusted[i]*adjusted[j] for i in range(p) for j in range(p)), Q(0))/variance


def ceiling(value):
    return -((-value.numerator)//value.denominator)


def tests():
    rng = random.Random(60219)
    counts = {"primitive_checks": 0, "exact_arc_comparisons": 0,
              "stationary_history_comparisons": 0, "expected_rejections": 0}
    for _ in range(500):
        a, b = sorted((rng.randrange(-100, 101), rng.randrange(-100, 101)))
        c, d = sorted((rng.randrange(-100, 101), rng.randrange(-100, 101)))
        assert _product((a, b), (c, d)) == (min(a*c, a*d, b*c, b*d), max(a*c, a*d, b*c, b*d))
        values = [x*x for x in range(a, b+1)]
        assert _square((a, b)) == (min(values), max(values))
        value, grid = Q(rng.randrange(-1000, 1001), rng.randrange(1, 100)), rng.randrange(1, 30)
        lower, upper = _outward(value, grid)
        assert Q(lower, grid) <= value <= Q(upper, grid)
        assert 0 <= upper-lower <= 1
        counts["primitive_checks"] += 3
    for _ in range(300):
        n, p = rng.randrange(1, 8), rng.randrange(1, 5)
        F = tuple(tuple(Q(rng.randrange(-100, 101), rng.randrange(1, 50)) for _ in range(p)) for _ in range(n))
        raw = [[Q(rng.randrange(-50, 51), rng.randrange(1, 50)) for _ in range(p)] for _ in range(p)]
        H = tuple(tuple(raw[max(i,j)][min(i,j)] for j in range(p)) for i in range(p))
        t = rng.randrange(n)
        ages = tuple(sorted(rng.sample(range(1, t+1), rng.randrange(t+1)), reverse=True))
        coefficients = tuple(Q(rng.randrange(-50, 51), rng.randrange(1, 50)) for _ in ages)
        variance = Q(rng.randrange(1, 100), rng.randrange(1, 100))
        for grid in (100, 10**12):
            scorer = IntegerIntervalScores(F, H, feature_grid=grid+1, coefficient_grid=grid,
                                           score_grid=10**8)
            pattern = scorer.prepare(ages, coefficients, variance)
            score = exact_score(F, H, t, ages, coefficients, variance)
            assert scorer.upper(t, pattern) >= ceiling(score*scorer.score_grid)
            counts["exact_arc_comparisons"] += 1
    # Positive and negative correlations, no latent process, empty histories.
    F = ((Q(-2), Q(3)), (Q(1, 3), Q(-4)), (Q(2, 7), Q(5, 11)))
    H = ((Q(3), Q(-1)), (Q(-1), Q(2)))
    scorer = IntegerIntervalScores(F, H)
    for rho in (Q(-4, 5), Q(0), Q(4, 5)):
        for latent in (Q(0), Q(2, 3)):
            for ages in ((), (1,), (2,), (2, 1)):
                b, d = local_coefficients(tuple(-age for age in ages), 0, rho, latent, Q(1, 7))
                pattern = scorer.prepare_history(ages, rho, latent, Q(1, 7))
                assert scorer.upper(2, pattern) >= ceiling(exact_score(F, H, 2, ages, b, d)*scorer.score_grid)
                counts["stationary_history_comparisons"] += 1
    # An indefinite exact H and a wholly negative quadratic remain valid.
    negative = IntegerIntervalScores(((Q(2),),), ((Q(-1),),), coefficient_grid=1)
    assert negative.upper(0, negative.prepare((), (), Q(1))) == 0
    # Exact cancellation, including intervals straddling zero.
    cancellation = IntegerIntervalScores(((Q(1, 3),), (Q(1, 3),)), ((Q(1),),), feature_grid=2)
    assert cancellation.upper(1, cancellation.prepare((1,), (Q(1),), Q(1))) >= 0
    good = scorer.prepare((), (), Q(1))
    bad = [lambda: IntegerIntervalScores(F, H, feature_grid=True),
           lambda: IntegerIntervalScores(F, H, coefficient_grid=0),
           lambda: IntegerIntervalScores(F, H, score_grid=1.0),
           lambda: IntegerIntervalScores(F, ((1, 2), (3, 4))),
           lambda: IntegerIntervalScores(F, ((1,),)),
           lambda: IntegerIntervalScores(((0.1,),), ((1,),)),
           lambda: scorer.prepare((), (), Q(1, 10**13)),
           lambda: scorer.prepare((), (), Q(-1)),
           lambda: scorer.prepare((1, 1), (1, 2), 1),
           lambda: scorer.prepare((True,), (1,), 1),
           lambda: scorer.prepare((1,), (), 1),
           lambda: scorer.prepare_history((1, 2), Q(1, 2), 1, 1),
           lambda: scorer.prepare_history((), 1, 1, 1),
           lambda: scorer.prepare_history((), 0, -1, 1),
           lambda: scorer.prepare_history((), 0, 1, 0),
           lambda: scorer.upper(True, good),
           lambda: scorer.upper(3, good),
           lambda: scorer.upper(0, scorer.prepare((1,), (1,), 1)),
           lambda: scorer.upper(0, IntegerIntervalScores(F, H, feature_grid=2).prepare((), (), 1)),
           lambda: IntegerPattern((), (), -1, 1, -1),
           lambda: IntegerPattern((), (), 0, 1, 1),
           lambda: IntegerPattern((), (), 1, False, 1),
           lambda: IntegerPattern((), (), 1, 1, 0),
           lambda: IntegerPattern((True,), ((0, 1),), 1, 1, 1),
           lambda: IntegerPattern((0,), ((0, 1),), 1, 1, 1),
           lambda: IntegerPattern((1, 1), ((0, 1), (0, 1)), 1, 1, 1),
           lambda: IntegerPattern((1,), (), 1, 1, 1),
           lambda: IntegerPattern([1], ((0, 1),), 1, 1, 1),
           lambda: IntegerPattern((1,), [(0, 1)], 1, 1, 1),
           lambda: IntegerPattern((1,), ([0, 1],), 1, 1, 1),
           lambda: IntegerPattern((1,), ((2, 1),), 1, 1, 1),
           lambda: IntegerPattern((1,), ((0, 1.0),), 1, 1, 1),
           lambda: IntegerPattern((1,), ((False, 1),), 1, 1, 1),
           lambda: IntegerPattern((1,), ((1,),), 1, 1, 1)]
    for fail in bad:
        try:
            fail()
        except (ValueError, TypeError):
            counts["expected_rejections"] += 1
        else:
            raise AssertionError("Malformed input was accepted")
    return counts


def reachable_arcs(n, k, L, g):
    width = max(L, min(g-1, n-1))
    state_mask, information_mask = (1 << width)-1, (1 << L)-1
    forbidden = (1 << min(g-1, width))-1
    states, arcs = {(0, 0)}, set()
    for t in range(n):
        following = set()
        for chosen, mask in states:
            shifted = (mask << 1) & state_mask
            if chosen+n-t-1 >= k:
                following.add((chosen, shifted))
            if chosen < k and not(mask & forbidden):
                arcs.add((t, mask & information_mask))
                following.add((chosen+1, shifted | (1 if width else 0)))
        states = following
    return tuple(sorted(arcs))


def price(n, k, L, g, scores):
    width = max(L, min(g-1, n-1))
    state_mask, information_mask = (1 << width)-1, (1 << L)-1
    forbidden = (1 << min(g-1, width))-1
    states = {(0, 0): 0}
    for t in range(n):
        following = {}
        for (chosen, mask), score in states.items():
            shifted = (mask << 1) & state_mask
            if chosen+n-t-1 >= k:
                state = (chosen, shifted)
                following[state] = max(following.get(state, score), score)
            if chosen < k and not(mask & forbidden):
                state = (chosen+1, shifted | (1 if width else 0))
                candidate = score + scores[(t, mask & information_mask)]
                following[state] = max(following.get(state, candidate), candidate)
        states = following
    return max(score for (chosen, _), score in states.items() if chosen == k)


def benchmark(path):
    started = perf_counter()
    certificate = json.loads(path.read_text())
    data = certificate["problem_data"]
    F, N = matrix(data["F"]), matrix(certificate["tangent_reference"])
    p, n, k, L, g = certificate["p"], certificate["n"], certificate["k"], certificate["L"], certificate["minimum_gap"]
    inverse = require_spd(N).inv()
    delta = rational(certificate["delta"])
    H = tuple(tuple(fraction(inverse[i, j])/(1-delta) for j in range(p)) for i in range(p))
    rho, latent, nugget = map(rational, (data["rho"], data["latent_variance"], data["nugget_variance"]))
    preparation_seconds = perf_counter()-started
    started = perf_counter()
    arcs = reachable_arcs(n, k, L, g)
    enumeration_seconds = perf_counter()-started
    patterns = {}
    started = perf_counter()
    for mask in sorted({mask for _, mask in arcs}):
        ages = tuple(age for age in range(L, 0, -1) if mask & (1 << (age-1)))
        b, d = local_coefficients(tuple(-age for age in ages), 0, rho, latent, nugget)
        patterns[mask] = ages, b, d
    rational_pattern_seconds = perf_counter()-started
    started = perf_counter()
    scorer = IntegerIntervalScores(F, H, score_grid=certificate["score_grid"])
    rounded = {mask: scorer.prepare(*pattern) for mask, pattern in patterns.items()}
    integer_preparation_seconds = perf_counter()-started
    started = perf_counter()
    interval_scores = {(t, mask): scorer.upper(t, rounded[mask]) for t, mask in arcs}
    integer_arc_seconds = perf_counter()-started
    print(json.dumps({"stage": "integer_arcs_complete", "arcs": len(arcs),
                      "integer_arc_seconds": integer_arc_seconds}), flush=True)
    started = perf_counter()
    exact_scores = {(t, mask): ceiling(exact_score(F, H, t, *patterns[mask])*scorer.score_grid)
                    for t, mask in arcs}
    exact_arc_seconds = perf_counter()-started
    losses = {key: interval_scores[key]-exact_scores[key] for key in arcs}
    assert min(losses.values()) >= 0
    assert len(arcs) == certificate["priced_arcs"]
    assert len(patterns) == certificate["conditional_patterns"]
    started = perf_counter()
    old_price, new_price = price(n, k, L, g, exact_scores), price(n, k, L, g, interval_scores)
    pricing_seconds = perf_counter()-started
    assert old_price == certificate["integer_price"]
    assert 0 <= new_price-old_price <= k*max(losses.values())
    return {"certificate": str(path), "certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "n": n, "p": p, "k": k, "L": L, "minimum_gap": g,
            "feature_grid": scorer.feature_grid, "coefficient_grid": scorer.coefficient_grid,
            "score_grid": scorer.score_grid, "all_reachable_arcs_verified": len(arcs),
            "patterns": len(patterns), "max_H_fraction_bits": max(max(x.numerator.bit_length(), x.denominator.bit_length()) for row in H for x in row),
            "max_variance_fraction_bits": max(max(d.numerator.bit_length(), d.denominator.bit_length()) for _, _, d in patterns.values()),
            "max_arc_loss_units": max(losses.values()), "changed_arc_scores": sum(loss != 0 for loss in losses.values()),
            "old_integer_price": old_price, "new_integer_price": new_price,
            "actual_bound_increase": str(Q(new_price-old_price, scorer.score_grid)),
            "worst_path_increase_bound": str(Q(k*max(losses.values()), scorer.score_grid)),
            "new_display_gap": float(rational(certificate["gap"])+Q(new_price-old_price, scorer.score_grid)),
            "timings_seconds": {"exact_tangent_reconstruction": preparation_seconds,
                                "reachable_arc_enumeration": enumeration_seconds,
                                "rational_conditional_patterns": rational_pattern_seconds,
                                "integer_preparation": integer_preparation_seconds,
                                "integer_arcs": integer_arc_seconds,
                                "exact_rational_arcs": exact_arc_seconds,
                                "two_integer_dynamic_programs": pricing_seconds},
            "arc_evaluation_speedup": exact_arc_seconds/integer_arc_seconds}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    result = {"status": "passed", "tests": tests(),
              "component_sha256": hashlib.sha256(Path(__file__).with_name("integer_interval_scores.py").read_bytes()).hexdigest(),
              "verification_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    if args.certificate:
        result["benchmark"] = benchmark(args.certificate)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
