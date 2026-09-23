# Independent review: exact CIA with a fixed switch budget

Date: 2026-09-07. Target: Extension 2 and the additional candidate-set lemma in
[the practical algorithm note](cia-reopened-practical-algorithm.md), implemented in
[`rounding.py`](../code/cia_reopened/rounding.py) as `optimal_block_assignment` and
`optimal_few_switches`. This is an independent agent review, not external peer
review. The final-block residual lemma has separate independent coverage in the
existing practical-algorithm review.

**Verdict:** The fixed-block subset dynamic program, its reduction from a total
switch budget, its mode-specific minimum-dwell extension, its complexity bounds,
and the mode-label candidate-set lemma are correct. The method includes repeated modes and schedules using fewer switches
than allowed. Exact checks using a separate microinterval integration oracle
passed. Literature priority remains a separate question.

## Exact mode-wise costs and subset recurrence

Fix `k` positive-length consecutive blocks. Assigning a subset `U` of blocks to
mode `i` completely determines that mode's binary service, whether or not `U` is
contiguous. On every block its signed allocation-minus-service discrepancy is
nondecreasing if inactive and nonincreasing if active. Consequently the maximum
absolute discrepancy occurs among the block endpoints. The initial endpoint has
zero error and can be omitted from the displayed maximum. Thus the proposed
`c_i(U)` is the exact full-horizon error, even when relaxed controls vary within
grid cells. In particular `c_i(empty)=A_i(T)`: unused modes cannot be discarded.

Every complete mode labeling corresponds to exactly one ordered family of disjoint
subsets `U_1,...,U_n` covering the blocks, with empty subsets allowed. Conversely,
every such family gives a valid labeling. The objective is the maximum of the
mode-specific costs. Conditioning on the blocks assigned to the last processed
mode therefore yields precisely the proposed recurrence. A partial state need
not describe a complete feasible control: it records the costs of its processed
modes only, which depend solely on their own assigned blocks. This is enough for
the recurrence, and all blocks are assigned at the terminal state.

The implementation faithfully uses this recurrence. Its inner subset loop includes
the empty subset, its unreachable states are distinct from finite values, and its
traceback reconstructs disjoint assignments covering every block. Disconnected
subsets permit a mode to reappear after intervening modes. Neighboring blocks can
also have the same mode.

## Reduction from the switch budget

Let `k=min(s+1,N)`. Every labeling of `k` positive blocks has at most `k-1<=s`
actual mode changes. In the other direction, any schedule with at most `s` switches
has at most `k` nonempty constant stretches because it is already grid restricted.
If it has fewer, subdivide stretches at unused grid boundaries until exactly `k`
blocks are present. This is possible because the grid has `N>=k` cells. The
subdivision preserves the schedule by assigning equal labels to adjacent new
blocks. Enumerating all `k-1` internal boundary sets therefore includes every
feasible schedule, without needing a separate enumeration of smaller block counts.

This argument covers `s=0`, `s>=N-1`, `N=1`, and `n=1`. No assumption that the
number of distinct used modes equals the number of blocks is made. It would be
incorrect to restrict the assignment to distinct mode labels: the integral
profile with chronological modes `(0,1,0)` has zero-error two-switch optimum,
which such a restriction would miss.

## Complexity and practical interpretation

For each mode there are `2^k` costs, each obtained by a `k`-endpoint scan. The
number of recurrence transitions is

```
sum_{S subset {1,...,k}} 2^|S| = 3^k.
```

The fixed-partition arithmetic bound is therefore
`O(n(k 2^k + 3^k))`, and its traceback requires `O(n2^k)` storage. Including
cumulative input preprocessing and boundary enumeration gives exactly

```
O(nN + binomial(N-1,k-1) n (k 2^k + 3^k))
```

operations and `O(nN+n2^k)` storage as stated. Since `k2^k=O(3^k)`, the
fixed-partition expression may also be written `O(n3^k)`. The explicitly stated
form matches the implementation. Two switches give `O(nN^2)` arithmetic time;
for each fixed budget the dependence on mode count is linear.

These are arithmetic-operation bounds with exact rational data, not unit-cost
claims for arbitrary bit lengths. The algorithm still enumerates a number of
partitions with exponent depending on the budget. It is a polynomial algorithm
for every fixed budget, not an FPT algorithm in the budget alone. This statement
concerns the presented algorithm and does not rule out a different FPT algorithm.
The existing linear one-switch method is preferable when only one switch is
allowed. No practical superiority over general solvers on typical low-mode
instances is inferred from the asymptotic mode-count improvement alone.

## Mode-specific minimum dwell times

The implemented minimum-dwell extension is also correct. A mode's maximal active
runs depend only on its own block subset, so an inadmissible subset can be assigned
infinite cost without changing the recurrence. The implementation sums adjacent
assigned block lengths, checks a run when an inactive block begins, and checks
any remaining run at the horizon. Thus artificial subdivision does not split a
physical dwell run. Empty subsets remain admissible, so a mode with a minimum
dwell exceeding the entire horizon may still be unused.

The declared convention imposes the dwell requirement on both initial and terminal
runs, including the whole-horizon run of a constant schedule. This is explicit and
consistent. Some applications exempt boundary runs or inherit an initial residence
time, but those different conventions are not silently assumed here. An infeasible
fixed partition or full instance returns `None` without traceback. The added scan
is still linear in the number of blocks per subset, leaving the stated complexity
order unchanged.

Other restrictions determined by one mode's entire subset can be handled the same
way, with their admissibility-check cost included. General transition restrictions
couple different modes and are outside this separation argument. The mathematical
extension should not be confused with unimplemented optional API features.

## Candidate-label lemma

For a fixed equality pattern with `d` distinct roles, the proposed candidate set
contains the `d` largest-total modes and the `d` cheapest modes for each role.
Suppose an optimal injective assignment uses a label outside this set. Since that
label is outside the largest-total set, at least one of those `d` high-total labels
is omitted: otherwise all `d` assignments would already belong to that set. The
removed label's total is therefore no greater than the old omitted-mode penalty.
At least one of its role's `d` cheapest labels is unused by the other `d-1` roles.
Replacing it with that label cannot increase the role cost or the omitted-mode
penalty. The replacement enters the candidate set and preserves injectivity.
Repeating eliminates all outside labels. Ties do not obstruct the argument.

This is a correct elementary exchange argument. If `n=d`, there are no outside
labels because the largest-total set already contains every label. If `n<d`,
there is no injective assignment, as the note specifies. The proof does not require
special relationships between role costs and mode totals; a checker below tests
it on general tables as an additional independent sanity check.

## Independent exact verification

Run:

```
python3 code/cia_reopened/check_fixed_budget_review.py
```

The [independent checker](../code/cia_reopened/check_fixed_budget_review.py) imports
only the two optimizers under review. Its reference calculation explicitly
enumerates grid schedules, then integrates all mode discrepancies at every fine
microinterval endpoint. It never calls the implementation's role-cost formula or
its discrepancy evaluator. Only aggregate coarse-cell masses are supplied to the
optimizers, so changing relaxed controls inside a cell tests the endpoint reduction
as well as the combinatorial optimization.

The recorded run passed:

- All 729 three-mode pure microcontrols on six half-length intervals, grouped into
  three coarse cells, plus 40 nonuniform rational controls with one to three
  varying relaxed segments per coarse cell.
- 3,836 comparisons over total switch budgets, including budgets exceeding the
  number of available boundaries, and 3,139 comparisons for prescribed partitions.
- Three explicit regressions for a repeated mode, subdivision with adjacent equal
  modes, and a positive contribution from an unused mode.
- 100 general role-cost tables comparing all injective assignments with assignments
  restricted to the proposed candidate-label set.

The dwell extension additionally passed 608 comparisons, including 52 infeasible
cases, across 50 random instances. It compares both APIs with a reference that groups
complete grid schedules into maximal runs and sums their physical durations. It
checks rational nonuniform grids, feasible and infeasible cases, both horizon ends,
and modes that may remain unused. Explicit regressions require adjacent assigned
blocks to merge into a feasible run, prevent separated activations from pooling
their durations, and detect an infeasible single-mode horizon. Invalid negative,
missing, floating, and Boolean dwell data are rejected.

Every returned objective equals independently computed discrepancy and the global
brute-force optimum in its tested feasible class. These finite checks complement
the proofs above and do not establish publication priority.
