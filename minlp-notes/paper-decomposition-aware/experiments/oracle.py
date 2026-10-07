"""Independent exact reference for small mixed-integer box QPs.

Uses only the raw coefficients (no solver code). For every integer assignment
and every face of the continuous box (each continuous coordinate at its lower
bound, at its upper bound, or free), solve the free stationarity system
H_FF x_F = -(b_F + H_F,fixed x_fixed) when H_FF is nonsingular, keep the
solution if it lies in the box, and evaluate it.

Correctness: every candidate is feasible, so the minimum over candidates is
at least F*. Conversely, fix the integer part of a global minimizer and,
among minimizers in that slice, take one whose smallest containing face has
minimum dimension. Its free Hessian is positive definite (a null direction
of a singular PSD free Hessian is a direction of zero first- and second-order
change, along which one can move to a smaller face while staying optimal), so
it is the unique stationary point of that face and appears as a candidate.
"""
from fractions import Fraction as F
from itertools import product


def value(A, b, c, x):
    n = len(b)
    return c + sum(b[i] * x[i] for i in range(n)) + sum(
        A[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) / 2


def solve_linear(M, r):
    """Exact Gauss-Jordan; returns None if M is singular."""
    n = len(M)
    rows = [list(M[i]) + [r[i]] for i in range(n)]
    for col in range(n):
        piv = next((k for k in range(col, n) if rows[k][col] != 0), None)
        if piv is None:
            return None
        rows[col], rows[piv] = rows[piv], rows[col]
        p = rows[col][col]
        rows[col] = [v / p for v in rows[col]]
        for k in range(n):
            if k != col and rows[k][col] != 0:
                f = rows[k][col]
                rows[k] = [a - f * bb for a, bb in zip(rows[k], rows[col])]
    return [rows[i][n] for i in range(n)]


def exact_minimum(A, b, c, bounds, integers):
    A = [[F(v) for v in row] for row in A]
    b = [F(v) for v in b]
    c = F(c)
    n = len(b)
    ints = sorted(integers)
    cont = [i for i in range(n) if i not in integers]
    int_ranges = [range(int(bounds[i][0]), int(bounds[i][1]) + 1) for i in ints]
    best, best_points = None, []
    for labels in product(*int_ranges):
        base = [None] * n
        for i, v in zip(ints, labels):
            base[i] = F(v)
        choices = [('lo', 'hi') if bounds[i][0] == bounds[i][1] else ('lo', 'hi', 'free')
                   for i in cont]
        for face in product(*choices):
            x = list(base)
            free = []
            for i, ch in zip(cont, face):
                if ch == 'lo':
                    x[i] = F(bounds[i][0])
                elif ch == 'hi':
                    x[i] = F(bounds[i][1])
                else:
                    free.append(i)
            if free:
                fixed = [i for i in range(n) if i not in free]
                M = [[A[i][j] for j in free] for i in free]
                r = [-b[i] - sum(A[i][j] * x[j] for j in fixed) for i in free]
                sol = solve_linear(M, r)
                if sol is None:
                    continue
                if any(not (bounds[i][0] <= v <= bounds[i][1]) for i, v in zip(free, sol)):
                    continue
                for i, v in zip(free, sol):
                    x[i] = v
            val = value(A, b, c, x)
            if best is None or val < best:
                best, best_points = val, [tuple(x)]
            elif val == best and tuple(x) not in best_points:
                best_points.append(tuple(x))
    return best, best_points
