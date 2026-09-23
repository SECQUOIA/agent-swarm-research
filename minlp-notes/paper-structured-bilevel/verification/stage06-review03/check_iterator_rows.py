"""Reproduce the frozen compressed solver's consumed-constraint-iterator bug."""
from pathlib import Path
import sys

paper = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(paper / 'process/snapshots/stage06-round01/code'))
import compressed_solver as solver

instance = solver.Instance((1,), (-1,), (1,), (0,), (1,), 3, 1, 1, 3)
atlas = solver.build_atlas(instance)
rows = [solver.Constraint(0, (1,), '1/2'),
        solver.Constraint(0, (-1,), '-1/2')]
for semantics in ('optimistic', 'pessimistic'):
    sequence_result = solver.optimize_tariff(atlas, rows, semantics)
    iterator_result = solver.optimize_tariff(atlas, iter(rows), semantics)
    assert sequence_result is None  # Actual follower never equals one half.
    assert iterator_result is not None  # The frozen bug, not expected behavior.
    print(semantics, 'list:', sequence_result, 'iterator:', iterator_result)
