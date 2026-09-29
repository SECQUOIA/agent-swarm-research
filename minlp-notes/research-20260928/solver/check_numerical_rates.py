#!/usr/bin/env python3
"""Targeted, floating-point moment-SDP and grid-LP checks.

No returned solver number is an exact certificate. Run with --help for the
small reproducible experiment; --check-only performs exact assembly checks.
"""

import argparse
from fractions import Fraction
from itertools import combinations, product
import json
import math
from pathlib import Path
import platform
import time

import cvxpy as cp
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, csr_matrix
import sympy as sp


def monomials(dim, degree):
    return [a for total in range(degree + 1)
            for a in product(range(total + 1), repeat=dim) if sum(a) == total]


def multiply(p, q):
    out = {}
    for a, c in p.items():
        for b, d in q.items():
            ab = tuple(x + y for x, y in zip(a, b))
            out[ab] = out.get(ab, Fraction(0)) + c * d
    return {a: c for a, c in out.items() if c}


def box_generators(dim):
    ans = []
    for j in range(dim):
        power = tuple(2 if i == j else 0 for i in range(dim))
        ans.append({(0,) * dim: Fraction(1), power: Fraction(-1)})
    return ans


def generator_products(generators, dim, degree, preordering):
    sizes = range(len(generators) + 1) if preordering else range(2)
    for size in sizes:
        for subset in combinations(range(len(generators)), size):
            p = {(0,) * dim: Fraction(1)}
            for j in subset:
                p = multiply(p, generators[j])
            if max(map(sum, p)) <= degree:
                yield subset, p


def localizer_map(mons, basis, polynomial, offset, total_variables):
    index = {a: i + offset for i, a in enumerate(mons)}
    rows, cols, values = [], [], []
    k = len(basis)
    for j, beta in enumerate(basis):
        for i, alpha in enumerate(basis):
            for gamma, coeff in polynomial.items():
                exponent = tuple(a + b + c for a, b, c in zip(alpha, beta, gamma))
                rows.append(i + j * k)
                cols.append(index[exponent])
                values.append(float(coeff))
    return coo_matrix((values, (rows, cols)), shape=(k * k, total_variables)).tocsr()


def quadratic_bags():
    # u,y and y,v, after x=(u+1)/2 and z=(v+1)/2.
    left = {(2, 0): Fraction(1, 4), (1, 0): Fraction(1, 2),
            (0, 0): Fraction(1, 4), (1, 1): Fraction(-1), (0, 1): Fraction(-1)}
    right = {(2, 0): Fraction(1), (0, 2): Fraction(1, 4),
             (0, 1): Fraction(1, 2), (0, 0): Fraction(1, 4),
             (1, 1): Fraction(1), (1, 0): Fraction(1)}
    return [(('u', 'y'), left, box_generators(2)),
            (('y', 'v'), right, box_generators(2))]


def affine_bags():
    # x,y and y,v, where z=(v+1)/2 and z >= |y|.
    # Match the affine note's G2=(1-y^2,z,1-z,z-y,z+y) exactly;
    # replacing z,1-z by 1-v^2 changes each truncated cone.
    recourse = [box_generators(2)[0],
        {(0, 0): Fraction(1, 2), (0, 1): Fraction(1, 2)},
        {(0, 0): Fraction(1, 2), (0, 1): Fraction(-1, 2)},
        {(0, 0): Fraction(1, 2), (0, 1): Fraction(1, 2), (1, 0): Fraction(-1)},
        {(0, 0): Fraction(1, 2), (0, 1): Fraction(1, 2), (1, 0): Fraction(1)}]
    return [(('x', 'y'), {(1, 1): Fraction(-1)}, box_generators(2)),
            (('y', 'v'), {(0, 0): Fraction(1, 2), (0, 1): Fraction(1, 2)}, recourse)]


def embed(polynomial, old_names, new_names):
    return {tuple(a[old_names.index(name)] if name in old_names else 0
                  for name in new_names): coeff for a, coeff in polynomial.items()}


def dense_bag(bags):
    names = tuple(dict.fromkeys(name for bag, _, _ in bags for name in bag))
    objective, generators = {}, []
    for old_names, poly, gs in bags:
        for a, c in embed(poly, old_names, names).items():
            objective[a] = objective.get(a, Fraction(0)) + c
        for g in gs:
            lifted = embed(g, old_names, names)
            if lifted not in generators:
                generators.append(lifted)
    return [(names, {a: c for a, c in objective.items() if c}, generators)]


def assemble(bags, order, preordering):
    bag_mons = [monomials(len(names), 2 * order) for names, _, _ in bags]
    offsets = np.cumsum([0] + [len(mons) for mons in bag_mons]).tolist()
    total = offsets[-1]
    objective = np.zeros(total)
    equality, rhs, localizers = [], [], []
    for bag_id, ((names, poly, gs), mons) in enumerate(zip(bags, bag_mons)):
        index = {a: i + offsets[bag_id] for i, a in enumerate(mons)}
        for a, c in poly.items():
            objective[index[a]] = float(c)
        row = np.zeros(total)
        row[index[(0,) * len(names)]] = 1
        equality.append(row)
        rhs.append(1.)
        for subset, g in generator_products(gs, len(names), 2 * order, preordering):
            basis = monomials(len(names), (2 * order - max(map(sum, g))) // 2)
            matrix = localizer_map(mons, basis, g, offsets[bag_id], total)
            localizers.append((matrix, len(basis), bag_id, subset, g, basis))
    if len(bags) == 2:
        assert bags[0][0][1] == bags[1][0][0] == 'y'
        first = {a: i + offsets[0] for i, a in enumerate(bag_mons[0])}
        second = {a: i + offsets[1] for i, a in enumerate(bag_mons[1])}
        # Degree zero already agrees because both laws have mass one.
        for k in range(1, 2 * order + 1):
            row = np.zeros(total)
            row[first[(0, k)]] = 1
            row[second[(k, 0)]] = -1
            equality.append(row)
            rhs.append(0.)
    return objective, csr_matrix(np.asarray(equality)), np.asarray(rhs), localizers, bag_mons, offsets


def polynomial_expression(poly, variables):
    return sum(sp.Rational(c.numerator, c.denominator)
               * sp.prod(v ** power for v, power in zip(variables, a))
               for a, c in poly.items())


def exact_assembly_checks():
    u, y, v, x = sp.symbols('u y v x')
    orig_x, orig_z = (u + 1) / 2, (v + 1) / 2
    original = orig_x**2 - 2*orig_x*y + y**2 + orig_z**2 + 2*y*orig_z
    qb = quadratic_bags()
    assert sp.expand(polynomial_expression(qb[0][1], (u, y))
                     - (orig_x**2 - 2*orig_x*y)) == 0
    assert sp.expand(polynomial_expression(qb[1][1], (y, v))
                     - (y**2 + orig_z**2 + 2*y*orig_z)) == 0
    dense = dense_bag(qb)
    assert sp.expand(polynomial_expression(dense[0][1], (u, y, v)) - original) == 0
    gx, gz = orig_x * (1-orig_x), orig_z * (1-orig_z)
    dense_certificate = ((y-orig_x+orig_z)**2
                         + 2*((orig_x*orig_z)**2 + orig_z**2*gx
                              + orig_x**2*gz + gx*gz))
    assert sp.expand(original - dense_certificate) == 0
    ab = affine_bags()
    affine_original = orig_z - x*y
    assert sp.expand(polynomial_expression(ab[0][1], (x, y))
                     + polynomial_expression(ab[1][1], (y, v)) - affine_original) == 0
    # 1 +/- x = ((1 +/- x)^2 + (1-x^2))/2 gives a dense
    # degree-three preordering certificate (order two).
    affine_certificate = (((1-x)**2 + (1-x*x))*(orig_z+y)
                          + ((1+x)**2 + (1-x*x))*(orig_z-y))/4
    assert sp.expand(affine_original - affine_certificate) == 0
    checked_entries = 0
    point = {'u': Fraction(1, 3), 'x': Fraction(1, 3),
             'y': Fraction(-2, 5), 'v': Fraction(3, 7)}
    for bags in [qb, ab, dense_bag(qb), dense_bag(ab)]:
        for order in [2, 3]:
            for preordering in [False, True]:
                obj, eq, rhs, locs, mons, offsets = assemble(bags, order, preordering)
                moments = []
                for (names, _, _), exponents in zip(bags, mons):
                    moments.extend(math.prod(point[name] ** power for name, power in zip(names, a))
                                   for a in exponents)
                for matrix, size, bag_id, _, g, basis in locs:
                    names = bags[bag_id][0]
                    mon_values = [math.prod(point[name] ** power for name, power in zip(names, a))
                                  for a in basis]
                    g_value = sum(c * math.prod(point[name] ** power for name, power in zip(names, a))
                                  for a, c in g.items())
                    for flat in range(size * size):
                        start, stop = matrix.indptr[flat:flat + 2]
                        actual = sum(Fraction(float(matrix.data[j])) * moments[matrix.indices[j]]
                                     for j in range(start, stop))
                        i, j = flat % size, flat // size
                        assert actual == g_value * mon_values[i] * mon_values[j]
                        checked_entries += 1
                for row_id in range(eq.shape[0]):
                    row = eq.getrow(row_id)
                    actual = sum(Fraction(float(c)) * moments[j] for j, c in zip(row.indices, row.data))
                    assert actual == Fraction(float(rhs[row_id]))
                expected = sum(c * math.prod(point[name] ** power for name, power in zip(names, a))
                               for names, poly, _ in bags for a, c in poly.items())
                assert sum(Fraction(float(c)) * m for c, m in zip(obj, moments)) == expected
    return {'exact_polynomial_and_certificate_checks': 'passed',
            'exact_dirac_localizer_entries_checked': checked_entries,
            'exact_equality_and_objective_assembly_checks': 'passed'}


def solve_moment_sdp(example, order, preordering, dense, solver):
    bags = quadratic_bags() if example == 'quadratic' else affine_bags()
    if dense:
        bags = dense_bag(bags)
    c, e, b, locs, _, _ = assemble(bags, order, preordering)
    moments = cp.Variable(len(c))
    equality = e @ moments == b
    psd = [cp.reshape(a @ moments, (k, k), order='F') >> 0 for a, k, *_ in locs]
    problem = cp.Problem(cp.Minimize(c @ moments), [equality] + psd)
    started = time.perf_counter()
    result = {'example': example, 'order': order, 'dense': dense,
              'cone': 'preordering' if preordering else 'quadratic_module',
              'solver': solver, 'moment_variables': len(c),
              'psd_block_sizes': [k for _, k, *_ in locs]}
    options = ({'tol_gap_abs': 1e-9, 'tol_feas': 1e-9,
                'tol_gap_rel': 1e-9, 'max_iter': 300} if solver == 'CLARABEL'
               else {'eps': 1e-7, 'max_iters': 100000})
    try:
        value = problem.solve(solver=solver, **options)
    except Exception as exc:
        result.update(status='exception', error=repr(exc), elapsed_seconds=time.perf_counter()-started)
        return result
    result.update(status=problem.status, primal_objective=None if value is None else float(value),
                  elapsed_seconds=time.perf_counter()-started, iterations=problem.solver_stats.num_iters)
    if moments.value is not None:
        z = moments.value
        result['equality_residual_max'] = float(np.max(np.abs(e @ z - b)))
        result['primal_min_eigenvalue'] = min(float(np.linalg.eigvalsh((a @ z).reshape((k, k), order='F'))[0])
                                             for a, k, *_ in locs)
    if equality.dual_value is not None and all(con.dual_value is not None for con in psd):
        stationarity = c + e.T @ equality.dual_value
        for (a, _, *_), constraint in zip(locs, psd):
            stationarity -= a.T @ constraint.dual_value.ravel(order='F')
        dual = float(-b @ equality.dual_value)
        result.update(dual_objective=dual,
                      primal_minus_dual=None if value is None else float(value-dual),
                      dual_stationarity_residual_max=float(np.max(np.abs(stationarity))),
                      dual_min_eigenvalue=min(float(np.linalg.eigvalsh(con.dual_value)[0]) for con in psd))
    return result


def grid_approximation(example, degree, grid_points):
    # A finite grid LP gives a lower estimate of the uniform error. The
    # validation grid supplies an additional diagnostic, not a certificate.
    grid = np.cos(np.linspace(0, np.pi, grid_points))
    target = np.maximum(grid, 0)**2 if example == 'quadratic' else np.abs(grid)
    vand = np.polynomial.chebyshev.chebvander(grid, degree)
    a = np.vstack([np.column_stack([vand, -np.ones(grid_points)]),
                   np.column_stack([-vand, -np.ones(grid_points)])])
    result = linprog(np.r_[np.zeros(degree + 1), 1.], A_ub=a,
                     b_ub=np.r_[target, -target], bounds=[(None, None)]*(degree+1)+[(0., None)],
                     method='highs', options={'dual_feasibility_tolerance': 1e-9,
                                              'primal_feasibility_tolerance': 1e-9})
    out = {'example': example, 'degree': degree, 'fit_grid_points': grid_points,
           'success': bool(result.success), 'message': result.message}
    if result.success:
        dense_grid = np.cos(np.linspace(0, np.pi, 10*(grid_points-1)+1))
        dense_target = np.maximum(dense_grid, 0)**2 if example == 'quadratic' else np.abs(dense_grid)
        error = float(np.max(np.abs(np.polynomial.chebyshev.chebval(dense_grid, result.x[:-1])-dense_target)))
        out.update(grid_error_lp=float(result.fun), validation_grid_error=error,
                   validation_grid_points=len(dense_grid), chebyshev_coefficients=result.x[:-1].tolist(),
                   ideal_gap_estimate=float(2*result.fun))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--orders', type=int, nargs='+', default=list(range(2, 7)))
    parser.add_argument('--examples', nargs='+', choices=['quadratic', 'affine'], default=['quadratic', 'affine'])
    parser.add_argument('--solver', choices=['CLARABEL', 'SCS'], default='CLARABEL')
    parser.add_argument('--grid-points', type=int, default=4001)
    parser.add_argument('--lp-degrees', type=int, nargs='+', default=[4, 6, 8, 10, 12, 16, 24, 32])
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('numerical-rate-results.json'))
    args = parser.parse_args()
    checks = exact_assembly_checks()
    print(json.dumps(checks), flush=True)
    if args.check_only:
        return
    output = {'warning': 'Floating-point SDP and finite-grid LP values are not certified bounds.',
              'versions': {'python': platform.python_version(), 'numpy': np.__version__,
                           'scipy': scipy.__version__, 'cvxpy': cp.__version__, 'sympy': sp.__version__},
              'arguments': {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
              'exact_checks': checks, 'sdp': [], 'approximation': []}
    def save():
        args.output.write_text(json.dumps(output, indent=2, allow_nan=False)+'\n')
    for example in args.examples:
        result = solve_moment_sdp(example, 2, True, True, args.solver)
        output['sdp'].append(result)
        print(json.dumps(result), flush=True)
        save()
        for order in args.orders:
            for preordering in [True, False]:
                result = solve_moment_sdp(example, order, preordering, False, args.solver)
                output['sdp'].append(result)
                print(json.dumps(result), flush=True)
                save()
        for degree in args.lp_degrees:
            result = grid_approximation(example, degree, args.grid_points)
            output['approximation'].append(result)
            print(json.dumps({k: v for k, v in result.items() if k != 'chebyshev_coefficients'}), flush=True)
            save()


if __name__ == '__main__':
    main()
