# Exact switching-control research code

These routines minimize cumulative allocation discrepancy, with initial activation free and switches allowed at grid boundaries. See the [paper-readiness record](../../notes/cia-reopened-paper-readiness.md) for theorem scopes and independent reviews. Run commands below from the repository root with Python 3.10 or later.

## Public routines

`minimax.py` and `rounding.py` require only the Python standard library. Inputs to `rounding.py` are exact interval **masses**, not rates: each row contains nonnegative allocations summing to that interval's duration. Use integers or `fractions.Fraction`; floating-point values and booleans are rejected. Modes are indexed from zero. The following example uses an explicit import path to avoid a collision with Python's standard-library module named `code`.

```python
import sys
from fractions import Fraction as Q
sys.path.insert(0, "code/cia_reopened")
from minimax import minimax
from rounding import optimal_one_switch, optimal_few_switches, schedule_error

value, compressed_witness = minimax(5, range(10))
assert value == Q(17, 5)

rows = [(1, 0), (0, 1), (1, 0)]
durations = [1, 1, 1]
one = optimal_one_switch(rows, durations)
two = optimal_few_switches(rows, durations, 2, minimum_dwell=[1, 1])
assert two is not None and two.error == 0
assert two.schedule() == (0, 1, 0)
assert schedule_error(rows, durations, one.schedule()) == one.error
```

| Routine | Contract |
| --- | --- |
| `minimax(n, grid)` | Worst-case one-switch value and compressed extremizer for `n>=3`; grid endpoints start at zero and strictly increase. Also accepts rational strings. `O(N^2)` rational operations, no LP. See its docstring and proof for witness reconstruction. |
| `optimal_one_switch(allocations, durations, *, switch_indices=None, initial_mode=None)` | Exact supplied-input optimum in `O(nN)` arithmetic operations. Optional internal boundary indices and fixed initial mode. Returns a solution with `.error` and `.schedule()`. |
| `optimal_few_switches(allocations, durations, switch_budget, *, minimum_dwell=None)` | Exact fixed-budget optimization, allowing repeated modes and fewer switches. Optional one minimum duration per mode; every maximal run, including initial and final runs, must satisfy it. Returns `None` if infeasible. |
| `optimal_block_assignment(allocations, durations, boundaries, *, minimum_dwell=None)` | Exact mode assignment for prescribed blocks. Boundary indices include `0` and `N`. Neighboring blocks may use the same mode and form one dwell run. Returns `None` if infeasible. |
| `complete_with_one_block(allocations, durations, prefix, *, require_switch=False)` | Optimal constant suffix after a fixed grid schedule prefix. Returns `(error, final_mode)`. The prefix must leave a nonempty suffix. |
| `schedule_error(allocations, durations, schedule)` | Direct exact discrepancy evaluation for a supplied grid word. |

For `k=min(s+1,N)`, the general optimizer uses `O(nN + binomial(N-1,k-1) n (k 2^k + 3^k))` arithmetic operations. Use the specialized routine for one switch without mode-specific dwell constraints. Dense grids and large budgets can make partition enumeration impractical. Arbitrary mode-transition restrictions are not implemented.

## Verification commands

Standard-library checks:

```sh
python code/cia_reopened/check_rounding.py
python code/cia_reopened/check_rounding_review.py
python code/cia_reopened/check_fixed_budget_review.py
python code/cia_reopened/check_grid_transfer_review.py
python code/cia_reopened/check_seeded_review.py
python code/cia_reopened/small_grid_boundary.py
python code/cia_reopened/check_small_grid_review.py
```

Independent optional comparisons using NumPy and SciPy:

```sh
python code/cia_reopened/check_finite_math_review.py
python code/cia_reopened/check_finite_grid_review.py
python -O code/cia_reopened/check_finite_grid_review.py --validation-only
```

`finite_grid_research.py` retains the earlier LP derivation and exact primal/dual certificate checks. Numerical rational reconstruction can fail closed on difficult inputs; the public `minimax.py` formula avoids that dependency. `general_reach_relaxation_witness.json` is a counterexample to a relaxation, not a physical control; `check_seeded_review.py` independently audits this distinction. The two small-grid scripts implement independent exhaustive integer proofs.

To reproduce the public profile experiment, download the pinned CSV linked in the [benchmark record](../../notes/cia-reopened-practical-algorithm.md), verify its recorded SHA-256, and run:

```sh
python code/cia_reopened/check_rounding.py --public-benchmark /path/to/mmlotka_nt_12000_400.csv
```

The script applies the normalization/quantization convention and restricted switching grids documented in the benchmark record. The input CSV is external and is not required by any mathematical proof. [final-validation.json](final-validation.json) records final file hashes and integration checks; detailed research runs and independent review evidence are recorded in the linked Markdown notes.
