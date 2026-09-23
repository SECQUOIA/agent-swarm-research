"""Canonical sparse rows for the single chronological chamber.

Sort inequality and equality rows separately by
(tuple(sorted((column, coefficient) for nonzero coefficients)), rhs).
Keep duplicate rows. Variable coordinates and the objective are unchanged.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'reference'))
from general_reach_research import weighted_triple_relaxation


def row_key(item):
    row, rhs = item
    return tuple(sorted((column, value) for column, value in row.items() if value)), rhs


def canonical_rows(rows):
    return [(dict(entries), rhs) for entries, rhs in sorted(map(row_key, rows))]


def chronological_program(order, base_program=None):
    """Build the fixed chamber; an explicit base program permits order audits."""
    size, ub, eq, obj = (weighted_triple_relaxation()
                         if base_program is None else base_program)
    ub = list(ub)
    for a, b in zip(order, order[1:]):
        for i in range(6):
            ub.append(({7+7*a+i: 1, 7+7*b+i: -1}, 0))
    return size, canonical_rows(ub), canonical_rows(eq), obj
