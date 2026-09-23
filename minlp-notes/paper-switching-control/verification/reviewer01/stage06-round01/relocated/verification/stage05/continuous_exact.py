"""Small-instance exact continuous CIA solver by word/cell/vertex enumeration.

All enumeration is finite and all arithmetic rational. This is a verification
benchmark, not a scalable LP implementation. The input masses specify constant
rates within each input cell. See the manuscript subsection on exact continuous
optimization; one_sided=True minimizes max(W-A), not max|A-W|.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reference"))
from rounding import _validated


@dataclass(frozen=True)
class ContinuousSolution:
    error: Q
    modes: tuple[int, ...]
    times: tuple[Q, ...]  # includes 0 and T; zero-length blocks are permitted
    one_sided: bool
    word_cell_programs: int


def solve_square(rows, rhs):
    """Return the unique rational solution, or None if the matrix is singular."""
    n = len(rhs)
    matrix = [list(map(Q, row)) + [Q(b)] for row, b in zip(rows, rhs)]
    for col in range(n):
        pivot = next((j for j in range(col, n) if matrix[j][col]), None)
        if pivot is None:
            return None
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        scale = matrix[col][col]
        matrix[col] = [x / scale for x in matrix[col]]
        for j in range(n):
            if j != col and matrix[j][col]:
                scale = matrix[j][col]
                matrix[j] = [x - scale*y for x, y in zip(matrix[j], matrix[col])]
    return tuple(row[-1] for row in matrix)


def minimum_vertex(inequalities, dimension):
    """Minimize the last coordinate over a bounded rational polytope Ax <= b."""
    inequalities = tuple(sorted(set(inequalities)))
    best = None
    for active in combinations(inequalities, dimension):
        point = solve_square([row for row, _ in active], [b for _, b in active])
        if point is None or (best is not None and point[-1] >= best[-1]):
            continue
        if all(sum(a*x for a, x in zip(row, point)) <= b for row, b in inequalities):
            best = point
    return best


def optimal_continuous(allocations, durations, switch_budget, *, one_sided=False):
    """Complete rational enumeration; intended only for very small instances."""
    rows, dt, n = _validated(allocations, durations)
    if type(switch_budget) is not int or switch_budget < 0:
        raise ValueError("switch_budget must be a nonnegative integer")
    if type(one_sided) is not bool:
        raise TypeError("one_sided must be a bool")
    k, N = switch_budget + 1, len(dt)
    knots = [Q(0)]
    cumulative = [[Q(0)] * n]
    for row, length in zip(rows, dt):
        knots.append(knots[-1] + length)
        cumulative.append([a+b for a, b in zip(cumulative[-1], row)])
    T = knots[-1]
    best = None
    programs = 0
    for cells in combinations_with_replacement(range(N), k-1):
        base = []
        for j, cell in enumerate(cells):
            row = [Q(0)] * k
            row[j] = 1
            base.append((tuple(row), knots[cell+1]))
            base.append((tuple(-x for x in row), -knots[cell]))
        for j in range(k-2):
            row = [Q(0)] * k
            row[j], row[j+1] = 1, -1
            base.append((tuple(row), Q(0)))
        row = (Q(0),) * (k-1) + (Q(1),)
        base.extend([(row, T), (tuple(-x for x in row), Q(0))])
        for word in product(range(n), repeat=k):
            programs += 1
            inequalities = list(base)
            for j in range(1, k+1):
                for i in range(n):
                    # discrepancy A_i(t_j)-W_i(t_j) = coeff*x + constant
                    coeff = [Q(0)] * k
                    if j < k:
                        cell = cells[j-1]
                        rate = rows[cell][i] / dt[cell]
                        coeff[j-1] = rate
                        constant = cumulative[cell][i] - rate*knots[cell]
                    else:
                        constant = cumulative[-1][i]
                    for h in range(1, j+1):
                        if word[h-1] != i:
                            continue
                        if h < k:
                            coeff[h-1] -= 1
                        else:
                            constant -= T
                        if h > 1:
                            coeff[h-2] += 1
                    # Always require W-A <= E.
                    negative = [-x for x in coeff]
                    negative[-1] = -1
                    inequalities.append((tuple(negative), constant))
                    if not one_sided:
                        positive = list(coeff)
                        positive[-1] = -1
                        inequalities.append((tuple(positive), -constant))
            point = minimum_vertex(inequalities, k)
            if point is not None and (best is None or point[-1] < best[0]):
                best = (point[-1], word, (Q(0),) + point[:-1] + (T,))
    if best is None:
        raise RuntimeError("The bounded schedule enumeration unexpectedly had no feasible vertex")
    return ContinuousSolution(*best, one_sided, programs)
