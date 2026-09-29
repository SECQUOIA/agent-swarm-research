"""Exact finite checks of the strict-cut candidate-list mechanism.

The finite integer-query feasibility simulator enumerates a small box;
it is intentionally not an implementation of the cited FPT algorithm.
The checks challenge the transcript argument and exact ties, not runtime.
"""

from fractions import Fraction as Q
from itertools import product


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def instance(a, b, c, e):
    def value(z):
        x, y = z
        return (Q(x*x+y*y, 2) + a*x + b*y
                + Q((x+y-c)**4, 8) + e*Q((2*x-y)**4, 16))

    def approximate_gradient(z):
        x, y = z
        t, u = x+y-c, 2*x-y
        gradient = (x+a+Q(t**3, 2)+e*Q(u**3, 2),
                    y+b+Q(t**3, 2)-e*Q(u**3, 4))
        # Canonical query-dependent error, exactly norm 1/4.
        error = (Q(3 if (x+y) % 2 else -3, 20),
                 Q(1 if x % 2 else -1, 5))
        assert dot(error, error) == Q(1, 16)
        return tuple(v+h for v, h in zip(gradient, error))

    return value, approximate_gradient


def candidate_list(universe, facets, approximate_gradient, initial, order):
    """No objective values or comparisons are available to this function."""
    remaining = set(universe)
    archive = [initial]
    transcript = []
    while remaining:
        z = min(remaining, key=order)
        outside = next(((a, b) for a, b in facets if dot(a, z) > b), None)
        if outside is not None:
            a, b = outside
            kind = "domain"
        else:
            archive.append(z)
            a = approximate_gradient(z)
            if all(v == 0 for v in a):
                return archive, transcript, z
            b = dot(a, z) - Q(1, 4)
            kind = "objective"
        assert dot(a, z) > b
        transcript.append((z, a, b, kind))
        remaining = {w for w in remaining if dot(a, w) <= b}
    return archive, transcript, None


def run_cases():
    box = list(product(range(-3, 4), repeat=2))
    facets = [((Q(1), Q(2)), Q(2)), ((Q(-1), Q(1)), Q(3))]
    feasible = [z for z in box if all(dot(a, z) <= b for a, b in facets)]
    assert (0, 0) in feasible
    cases = 0
    cuts = 0
    for a, b, c, e in product((Q(-3, 2), Q(1, 2)),
                              (Q(-1), Q(3, 2)), (-1, 0, 1), (0, 1)):
        value, gradient = instance(a, b, c, e)
        optimum = min(map(value, feasible))
        minimizers = {z for z in feasible if value(z) == optimum}
        for order in (lambda z: z, lambda z: (-z[1], -z[0]),
                      lambda z: (z[0]**2+2*z[1]**2, z)):
            archive, transcript, early = candidate_list(box, facets, gradient, (0, 0), order)
            assert all(z in feasible for z in archive)
            assert min(map(value, archive)) == optimum
            assert minimizers.issubset(set(archive))
            visited_optimum = (0, 0) in minimizers
            for z, normal, rhs, kind in transcript:
                if kind == "objective" and z in minimizers:
                    visited_optimum = True
                if not visited_optimum:
                    assert all(dot(normal, w) <= rhs for w in minimizers)
                if kind == "objective":
                    assert all(dot(normal, w) <= rhs for w in feasible
                               if w != z and value(w) <= value(z))
            # Nonadaptive all-pairs selection and threshold batches.
            comparisons = [[value(z) <= value(w) for w in archive] for z in archive]
            selected = next(i for i, row in enumerate(comparisons) if all(row))
            assert value(archive[selected]) == optimum
            selected_set = {archive[i] for i, row in enumerate(comparisons) if all(row)}
            assert selected_set == minimizers
            for threshold in (optimum-1, optimum, optimum+1):
                weak = any(value(z) <= threshold for z in archive)
                strict = any(value(z) < threshold for z in archive)
                assert weak == (optimum <= threshold)
                assert strict == (optimum < threshold)
                assert (weak and not strict) == (optimum == threshold)
            cuts += len(transcript)
            cases += 1
    return cases, cuts


def boundary_cases():
    # Two adjacent integer optima: the query itself is cut off, but recorded.
    z, w = (Q(0),), (Q(1),)
    q = (Q(-1, 4),)  # true gradient -1/2, maximal permitted error +1/4.
    rhs = dot(q, z) - Q(1, 4)
    assert dot(q, z) > rhs and dot(q, w) == rhs

    # A zero approximate normal is an early certificate, without value tests.
    archive, transcript, early = candidate_list(
        list(product(range(-1, 2), repeat=2)), [],
        lambda z: tuple(Q(x) for x in z), (0, 0),
        lambda z: (z[0]**2+z[1]**2, z))
    assert early == (0, 0) and not transcript and (0, 0) in archive

    # The empty-target completion is always a strict separator of its query.
    for z in product(range(-2, 3), repeat=2):
        normal, rhs = (Q(1), Q(0)), Q(z[0]-1)
        assert dot(normal, z) > rhs


if __name__ == "__main__":
    cases, cuts = run_cases()
    boundary_cases()
    print(f"PASS: {cases} value-free candidate-list runs, {cuts} exact strict cuts.")
    print("PASS: optimal archives, fixed-target prefixes, pairwise/threshold batches.")
    print("PASS: adjacent optimum tie, zero-normal stop, empty-target completion.")
