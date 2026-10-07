#!/usr/bin/env python3
"""Exact local checks for dyadic regridding with affine quadratic minorants.

The tests build shell partitions and minimize affine functions on local box
intersections. They do not implement the full certificate dynamic program.
Python 3.10+, standard library only; results are printed as JSON.
"""

from fractions import Fraction as Q
from itertools import product
from math import lcm, prod
import json


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def divides_denominator(value, denominator):
    require(denominator % value.denominator == 0, "denominator divisibility")


def corners(box):
    return tuple(product(*(tuple(dict.fromkeys(pair)) for pair in box)))


def width(box):
    return max((hi-lo for lo, hi in box), default=Q(0))


def volume(box):
    return prod(hi-lo for lo, hi in box)


def shell_partition(domain, center, h, mu, stage):
    """Lemma 3.1's central cubes and shell cubes, clipped to the domain."""
    boxes = []
    clipped = 0
    for level in range(stage+1):
        step = h if level == 0 else h*Q(2**(level-1), 2**mu)
        indices = range(-1, 1) if level == 0 else range(-2**(mu+1), 2**(mu+1))
        inner_radius = h*2**(level-1) if level else Q(0)
        axes = []
        for (lo, hi), c in zip(domain, center):
            intervals = []
            for index in indices:
                left, right = c+index*step, c+(index+1)*step
                clipped_left, clipped_right = max(lo, left), min(hi, right)
                if clipped_left < clipped_right:
                    inside = c-inner_radius <= left and right <= c+inner_radius
                    intervals.append(((clipped_left, clipped_right), inside,
                                      (clipped_left, clipped_right) != (left, right)))
            axes.append(intervals)
        for selection in product(*axes):
            if level and all(inside for _, inside, _ in selection):
                continue
            boxes.append(tuple(interval for interval, _, _ in selection))
            clipped += any(was_clipped for _, _, was_clipped in selection)
    require(sum(volume(box) for box in boxes) == volume(domain), "shell volume covers domain")
    require(len(boxes) <= (stage+1)*(4*2**mu)**len(domain), "shell box count")
    theta = Q(1, 2**mu)
    for box in boxes:
        distance = max((max(lo-c, c-hi, Q(0)) for (lo, hi), c in zip(box, center)), default=Q(0))
        require(width(box) <= max(h, theta*distance), "shell grading after clipping")
    return tuple(boxes), clipped


def intersect_separator(box, bag, separator, cell):
    result = list(box)
    for variable, (lo, hi) in zip(separator, cell):
        position = bag.index(variable)
        a, b = result[position]
        if max(a, lo) > min(b, hi):
            return None
        result[position] = (max(a, lo), min(b, hi))
    return tuple(result)


def affine_minimum(coefficients, intercept, box):
    # Zero coefficients explicitly choose the lower endpoint.
    point = tuple(hi if a < 0 else lo for a, (lo, hi) in zip(coefficients, box))
    value = intercept+sum(a*x for a, x in zip(coefficients, point))
    require(value == min(intercept+sum(a*x for a, x in zip(coefficients, v))
                         for v in corners(box)), "affine minimum equals corner enumeration")
    return value, point


def quadratic_value(matrix, linear, constant, point):
    return constant+sum(a*x for a, x in zip(linear, point))+sum(
        matrix[i][j]*point[i]*point[j]/2
        for i in range(len(point)) for j in range(len(point))
    )


def minorant(matrix, linear, constant, box, M, p):
    midpoint = tuple((lo+hi)/2 for lo, hi in box)
    gradient = tuple(a+sum(row[j]*midpoint[j] for j in range(len(box)))
                     for a, row in zip(linear, matrix))
    intercept = (quadratic_value(matrix, linear, constant, midpoint)
                 - sum(a*m for a, m in zip(gradient, midpoint))-M*p*width(box)**2/8)
    return gradient, intercept, midpoint


def regridding_checks():
    domain = ((Q(-7, 3), Q(11, 5)), (Q(-5, 7), Q(13, 6)),
              (Q(2, 11), Q(17, 8)), (Q(-9, 10), Q(7, 9)), (Q(-1, 13), Q(19, 12)))
    center = (Q(1, 3), Q(2, 7), Q(5, 11), Q(-1, 9), Q(3, 13))
    bags = ((0, 1), (1, 2, 3), (2, 3, 4), (4,))
    separators = ((), (1,), (2, 3), (4,))
    tops = (0, 0, 1, 1, 2)
    M, constant, p = Q(7, 5), Q(-17, 19), 3
    linears = tuple(tuple(Q(i+1, 17) for i in range(len(bag))) for bag in bags)
    matrices = []
    for bag in bags:
        q = len(bag)
        H = [[Q(0)]*q for _ in range(q)]
        if q >= 2:
            H[0][1] = H[1][0] = M
        for i in range(2 if q >= 2 else 0, q):
            H[i][i] = -M
        matrices.append(tuple(tuple(row) for row in H))
    s0 = width(domain)
    data = [x for pair in domain for x in pair]+list(center)+[s0, M, constant]
    data += [a for row in linears for a in row]
    data += [a/2 for H in matrices for row in H for a in row]
    D = lcm(*(x.denominator for x in data))
    rows = []
    counts = dict(boxes=0, clipped_boxes=0, intersections=0, strict_intersections=0,
                  affine_minima=0, tie_minima=0, center_changes=0)
    mu = 1
    for stage in range(10):
        h, exponent = s0/2**stage, stage+mu
        bound = D*2**exponent
        arithmetic_bound = D**3*2**(2*exponent+3)
        coordinates = list(center)
        chosen = []
        stage_boxes = 0
        for t, (bag, separator, H, linear) in enumerate(zip(bags, separators, matrices, linears)):
            leaves, clips = shell_partition(tuple(domain[i] for i in bag),
                                            tuple(center[i] for i in bag), h, mu, stage)
            cells, cell_clips = shell_partition(tuple(domain[i] for i in separator),
                                                tuple(center[i] for i in separator), h, mu, stage)
            counts["clipped_boxes"] += clips+cell_clips
            counts["boxes"] += len(leaves)+len(cells)
            stage_boxes += len(leaves)+len(cells)
            for box in leaves+cells:
                for pair in box:
                    for endpoint in pair:
                        divides_denominator(endpoint, bound)
                        coordinates.append(endpoint)
            index = (len(leaves)//2+131*stage+17*t) % len(leaves)
            selected_point = None
            for leaf_index in dict.fromkeys((index, 0, len(leaves)-1, len(leaves)//2)):
                leaf = leaves[leaf_index]
                gradient, intercept, midpoint = minorant(H, linear, constant, leaf, M, p)
                for m in midpoint:
                    divides_denominator(m, 2*bound)
                divides_denominator(intercept, arithmetic_bound)
                for a in gradient:
                    divides_denominator(a, D**2*2**(exponent+1))
                for cell in cells:
                    intersection = intersect_separator(leaf, bag, separator, cell)
                    if intersection is None:
                        continue
                    counts["intersections"] += 1
                    counts["strict_intersections"] += intersection != leaf
                    value, point = affine_minimum(gradient, intercept, intersection)
                    counts["affine_minima"] += 1
                    divides_denominator(value, arithmetic_bound)
                    for coordinate in point:
                        divides_denominator(coordinate, bound)
                    if selected_point is None and leaf_index == index:
                        selected_point = point
                        # Every corner can be the unique affine minimizer; ties use endpoints too.
                        for signs in product((-1, 1), repeat=len(bag)):
                            _, corner = affine_minimum(signs, Q(0), intersection)
                            counts["affine_minima"] += 1
                            for coordinate in corner:
                                divides_denominator(coordinate, bound)
                        _, tied = affine_minimum((Q(0),)*len(bag), Q(0), intersection)
                        require(tied == tuple(lo for lo, _ in intersection), "tie chooses endpoints")
                        counts["tie_minima"] += 1
            require(selected_point is not None, "leaf has own-separator intersection")
            chosen.append(selected_point)
        next_center = tuple(chosen[t][bags[t].index(i)] for i, t in enumerate(tops))
        require(all(lo <= x <= hi for x, (lo, hi) in zip(next_center, domain)), "top-selected feasibility")
        for coordinate in next_center:
            divides_denominator(coordinate, bound)
        counts["center_changes"] += next_center != center
        coordinates.extend(next_center)
        max_bits = max(x.denominator.bit_length() for x in coordinates)
        require(max_bits <= D.bit_length()+exponent, "linear coordinate denominator bit bound")
        rows.append(dict(stage=stage, boxes=stage_boxes, coordinate_denominator_bits=max_bits,
                         bound_bits=D.bit_length()+exponent, center=[str(x) for x in next_center]))
        center = next_center
    require(counts["strict_intersections"] > 0 and counts["clipped_boxes"] > 0,
            "strict intersections and clipping exercised")
    require(counts["center_changes"] >= 5, "successive corner-selected centers exercised")
    require(rows[-1]["coordinate_denominator_bits"] >= rows[0]["coordinate_denominator_bits"]+5,
            "nontrivial dyadic denominator growth exercised")
    return dict(input_denominator=str(D), mu=mu, counts=counts, stages=rows)


def boundary_sweep():
    # Larger dyadic grading exponents without constructing high-dimensional partitions.
    D, s0, center = 105, Q(7, 3), Q(2, 7)
    endpoints = (Q(-1, 5), Q(13, 7))
    cases = coordinates = 0
    for mu in (1, 2, 4):
        c = center
        for stage in range(10):
            h = s0/2**stage
            bound = D*2**(stage+mu)
            boundary = [c-h, c, c+h]
            for level in range(1, stage+1):
                step = h*Q(2**(level-1), 2**mu)
                boundary.extend(c+k*step for k in range(-2**(mu+1), 2**(mu+1)+1))
            clipped = tuple(max(endpoints[0], min(endpoints[1], x)) for x in boundary)
            for x in clipped:
                divides_denominator(x, bound)
            # A tied affine function can choose this endpoint of an adjacent cell.
            c = min((x for x in clipped if x > c), default=endpoints[0])
            cases += 1
            coordinates += len(clipped)
    return dict(stages=cases, clipped_boundary_coordinates=coordinates)


def taylor_checks():
    cases = probes = sharp_lower = sharp_upper = 0
    for dimension in (1, 2, 3):
        for sign in (-1, 1):
            M, W = Q(7, 5), Q(10, 3)
            H = [[Q(0)]*dimension for _ in range(dimension)]
            if dimension >= 2:
                H[0][1] = H[1][0] = M
            for i in range(2 if dimension >= 2 else 0, dimension):
                H[i][i] = sign*M
            # H^2=M^2 I proves its spectral norm without numerical eigenvalues.
            require(all(sum(H[i][k]*H[k][j] for k in range(dimension))
                        == (M*M if i == j else 0)
                        for i in range(dimension) for j in range(dimension)), "exact Hessian norm certificate")
            midpoint = tuple(Q(i+1, 7) for i in range(dimension))
            box = tuple((m-W/2, m+W/2) for m in midpoint)
            linear, constant = (Q(2, 11),)*dimension, Q(-3, 13)
            gradient, intercept, _ = minorant(H, linear, constant, box, M, dimension)
            upper = M*dimension*W**2/4
            for offsets in product((Q(-1, 2), Q(-1, 6), Q(0), Q(1, 3), Q(1, 2)), repeat=dimension):
                point = tuple(m+W*d for m, d in zip(midpoint, offsets))
                gap = quadratic_value(H, linear, constant, point)-intercept-sum(a*x for a, x in zip(gradient, point))
                require(0 <= gap <= upper, "affine Taylor error interval")
                sharp_lower += gap == 0
                sharp_upper += gap == upper
                probes += 1
            cases += 1
    require(sharp_lower > 0 and sharp_upper > 0, "both Taylor constants attained")
    # Upper curvature alone cannot certify this symmetric Taylor lower model.
    gradient, intercept, _ = minorant(((Q(-3),),), (Q(0),), Q(0), ((Q(-1), Q(1)),), Q(1), 1)
    gap = quadratic_value(((Q(-3),),), (Q(0),), Q(0), (Q(1),))-intercept-gradient[0]
    require(gap == -1, "counterexample to upper-curvature-only assumption")
    return dict(quadratics=cases, probes=probes, sharp_lower_points=sharp_lower,
                sharp_upper_points=sharp_upper, upper_curvature_only_counterexample=str(gap))


if __name__ == "__main__":
    result = dict(status="passed", arithmetic="fractions.Fraction",
                  scope="Local shell, box-intersection, corner-minimizer, and Taylor invariants; no full DP.",
                  regridding=regridding_checks(), boundaries=boundary_sweep(), taylor=taylor_checks())
    print(json.dumps(result, indent=2))
