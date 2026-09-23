"""Independent exact audit of surrogate-cell screening and dense recovery.

Run: python code/bilevel_reopened/screening_second_review.py
Uses SymPy rational arithmetic; no approximate optimization or shared solver.
The cases have one leader, diagonal surrogate, and dense true Hessian.
"""

from itertools import product
import json
import random

import sympy as s


def clip_interval(interval, intercept, slope):
    """Intersect a rational closed interval with intercept+slope*x >= 0."""
    if interval is None:
        return None
    lo, hi = interval
    if slope > 0:
        lo = max(lo, -intercept / slope)
    elif slope < 0:
        hi = min(hi, -intercept / slope)
    elif intercept < 0:
        return None
    return (lo, hi) if lo <= hi else None


def active_piece(Q, c, C, status, interval):
    n = len(c)
    free = [i for i in range(n) if status[i] == "F"]
    a, b = s.zeros(n, 1), s.zeros(n, 1)
    for i in range(n):
        a[i] = int(status[i] == "U")
    if free:
        inverse = Q.extract(free, free).inv()
        af = -inverse * (c + Q * a).extract(free, [0])
        bf = -inverse * C.extract(free, [0])
        for j, i in enumerate(free):
            a[i], b[i] = af[j], bf[j]
    ga, gb = Q * a + c, Q * b + C
    for i in range(n):
        if status[i] == "F":
            interval = clip_interval(interval, a[i], b[i])
            interval = clip_interval(interval, 1 - a[i], -b[i])
        else:
            sign = 1 if status[i] == "L" else -1
            interval = clip_interval(interval, sign * ga[i], sign * gb[i])
    return interval, a, b


def ge_root(value, square, strict=False):
    return bool(value >= 0 and (value**2 > square if strict else value**2 >= square))


def screen(Q, Qhat, c, C, ya, yb, interval):
    inverse, residual = Q.inv(), Q - Qhat
    pa, pb = residual * ya, residual * yb
    eta = max(((pa + pb*x).T * inverse * (pa + pb*x))[0] for x in interval)
    sa, sb = ya - inverse*pa/2, yb - inverse*pb/2
    ta, tb = Qhat*ya + c + pa/2, Qhat*yb + C + pb/2
    choices = []
    for i in range(len(c)):
        sl, sh = sorted(sa[i] + sb[i]*x for x in interval)
        tl, th = sorted(ta[i] + tb[i]*x for x in interval)
        rr, ss = inverse[i, i]*eta/4, Q[i, i]*eta/4
        lower = ge_root(tl, ss, True) or ge_root(-sh, rr)
        upper = ge_root(-th, ss, True) or ge_root(sl-1, rr)
        free = ge_root(sl, rr, True) and ge_root(1-sh, rr, True)
        # The original theorem uses the three tests above. Do not silently
        # strengthen them when checking its literal implementation.
        assert sum((lower, upper, free)) <= 1
        choices.append("L" if lower else "U" if upper else "F" if free else "LFU")
    return choices


def optimize_piece(piece, objective, upper_rows):
    interval, a, b = piece
    for xa, row, rhs in upper_rows:
        interval = clip_interval(interval, rhs-(row.T*a)[0], -xa-(row.T*b)[0])
    if interval is None:
        return None
    xa, row = objective
    return min((row.T*a)[0] + (xa+(row.T*b)[0])*x for x in interval)


def run_case(seed, zero_residual=False, singleton=False):
    rng = random.Random(seed)
    n = 4
    Qhat = s.diag(*[s.Rational(rng.randint(2, 5)) for _ in range(n)])
    A = s.Matrix(n, n, [rng.randint(-2, 2) for _ in range(n*n)])
    # The symmetric residual can be indefinite. Its row norm is < min d_i,
    # so positive definiteness of the true Hessian still follows directly.
    residual = A.T*A/s.Integer(25) if seed % 2 == 0 else (A+A.T)/s.Integer(25)
    Q = Qhat if zero_residual else Qhat + residual
    c = s.Matrix([s.Rational(rng.randint(-5, 3), 2) for _ in range(n)])
    C = s.Matrix([s.Rational(rng.choice([-4, -2, 1, 3, 5]), 2) for _ in range(n)])
    X = (s.Rational(1, 2), s.Rational(1, 2)) if singleton else (s.Rational(0), s.Rational(1))
    breaks = {X[0], X[1]}
    for i in range(n):
        for bound in [0, 1]:
            point = (-Qhat[i, i]*bound-c[i])/C[i]
            if X[0] < point < X[1]:
                breaks.add(point)
    breaks = sorted(breaks)
    cells = list(zip(breaks, breaks[1:])) if not singleton else [X]
    objective = (s.Rational(-1), s.Matrix([2, -3, 1, -2]))
    upper_rows = [(s.Rational(1, 3), s.Matrix([1, -1, 2, 0]), s.Rational(3, 2))]
    # Add an exact response-dependent equality on a subset of cases.
    if seed % 4 == 0:
        row = s.Matrix([0, 0, 0, 1])
        for status in product("LFU", repeat=n):
            point_piece, pa, pb = active_piece(Q, c, C, status, (s.Rational(1, 2),)*2)
            if point_piece is not None:
                rhs = (row.T*(pa+pb/2))[0]
                break
        upper_rows = [(s.Rational(0), row, rhs), (s.Rational(0), -row, -rhs)]
    full = []
    for status in product("LFU", repeat=n):
        value = optimize_piece(active_piece(Q, c, C, status, X), objective, upper_rows)
        if value is not None:
            full.append(value)
    restricted, count, ambiguous = [], 0, 0
    for cell in cells:
        midpoint = sum(cell)/2
        status = ["L" if -c[i]-C[i]*midpoint <= 0 else "U"
                  if -c[i]-C[i]*midpoint >= Qhat[i, i] else "F" for i in range(n)]
        _, ya, yb = active_piece(Qhat, c, C, status, cell)
        choices = screen(Q, Qhat, c, C, ya, yb, cell)
        ambiguous = max(ambiguous, sum(len(v)>1 for v in choices))
        # Independently check EVERY certified implication over every true
        # active piece in this cell, including its degenerate endpoints.
        for status in product("LFU", repeat=n):
            region, za, zb = active_piece(Q, c, C, status, cell)
            if region is None:
                continue
            for x in (*region, sum(region)/2):
                y, z = ya+yb*x, za+zb*x
                error, p = z-y, (Q-Qhat)*y
                assert (error.T*Q*error + p.T*error)[0] <= 0
                gradient = Q*z+c+C*x
                for i, choice in enumerate(choices):
                    if choice == "L":
                        assert z[i] == 0
                    elif choice == "U":
                        assert z[i] == 1
                    elif choice == "F":
                        assert gradient[i] == 0
        for assignment in product(*choices):
            count += 1
            value = optimize_piece(active_piece(Q, c, C, assignment, cell), objective, upper_rows)
            if value is not None:
                restricted.append(value)
    assert (min(full) if full else None) == (min(restricted) if restricted else None)
    return {"seed": seed, "zero_residual": zero_residual, "singleton": singleton,
            "cells": len(cells), "max_ambiguous": ambiguous,
            "recovery_assignments": count, "optimum": str(min(full)) if full else None}


if __name__ == "__main__":
    records = [run_case(seed, seed % 3 == 0, seed % 5 == 0) for seed in range(20)]
    print(json.dumps({"passed": len(records), "arithmetic": "exact rational", "cases": records}, indent=2))
