# Independent review: switch-preserving grid transfer

Date: 2026-09-07. Target: [uniform-grid transfer note](cia-reopened-grid-transfer.md).
This is an independent agent review, not external peer review. The mathematical
arguments and exact checks below were developed independently of the proposed
network-flow implementation. Source priority is a separate literature-review task.

**Verdict:** The transfer theorem is correct for a positive uniform cell length,
a positive integer number of cells, finitely many modes, and a nonnegative integer
switch budget. Its constant is best possible when mode count and switch budget
are allowed to vary. The instance-wise and minimax comparisons use the correct
quantifiers. The binary case has a sharper half-cell bound, extending to unequal
cell lengths.

## Flow, chronology, and strict error

At each mode node `(i,k)`, flow from the preceding chain edge plus the assignment
from cell `k` equals outgoing chain flow. Thus that outgoing flow is the cumulative
number of selected cells in mode `i`. The proposed lower and upper bounds are
exactly the floor and ceiling of the corresponding cumulative normalized mass.
For the last cell the outgoing arc goes to the common sink. The total supply and
sink demand are both `N`.

Deleting assignment arcs with zero original mass preserves the explicit fractional
feasible solution. All remaining capacities, lower bounds, supplies, and demands
are integers. The usual integral feasible-flow theorem therefore supplies an
assignment in which every cell selects exactly one supported mode. Integral target
prefixes force equality; nonintegral target prefixes permit only their two adjacent
integers, each at distance strictly less than one. There are finitely many prefixes
and modes, so their maximum is still strictly less than one.

Support preservation is essential to the switch-count consequence. For each cell,
the selected mode occurs in an original positive-length constant block intersecting
the cell in positive measure. Choose an interior time in that intersection. The
chosen times strictly increase as cells progress, so original block indices cannot
decrease. Removing unselected original blocks and then merging equal neighboring
modes gives the grid control's block sequence. In particular its switch count is
no greater than the original count. This argument allows arbitrarily many original
switches inside one cell and repeated modes in nonadjacent original blocks.

On a cell with selected mode `i`, the `i` component of cumulative `v-w` has
nonnegative derivative, and every other component has nonpositive derivative,
almost everywhere. Absolute values of these monotone functions attain their
maxima at cell endpoints. The strict endpoint estimate therefore controls all
continuous times. This step is valid even when original switch times lie strictly
inside the cells.

The network has `O(nN)` nodes and arcs. Exact rational overlap masses, prefix sums,
floors, and ceilings can be computed with polynomial bit complexity from explicitly
supplied rational switches and a rational positive cell length. The claim properly
measures complexity in `N`, rather than its binary encoding length. This is a
construction for a supplied continuous schedule; it does not compute the globally
optimal continuous schedule.

## Optimal values and the scope of the minimax comparison

For a fixed measurable relaxed control, each fixed mode word has a compact ordered
switch-time simplex, allowing zero-duration blocks. Moving switches changes the
control in `L1` by a quantity tending to zero, so its cumulative-error objective is
continuous. There are finitely many words of at most `s+1` modes. A continuous
optimum therefore exists. Rounding that optimum and applying the triangle
inequality gives the strict instance-specific upper estimate
`OPT_grid < OPT_cont + Delta`. Restriction of admissible integer schedules gives
`OPT_cont <= OPT_grid` for the same relaxed input.

Taking a supremum loses strictness. Moreover, a supremum over grid-constant relaxed
inputs and one over all measurable relaxed inputs need not preserve the reverse
comparison. The note correctly records only the immediately established minimax
upper bound. No lower minimax comparison follows from the instance-wise inequality
alone when the adversary's class changes.

Skipping original blocks can introduce previously absent direct mode transitions
or violate dwell-time requirements. Neither property is promised. The unit-flow
proof does not directly extend to unequal cell weights.

## Sharpness of the universal transfer coefficient

A particularly small family uses `n>=2`, unit cell length, `N=n+1`, and switch budget
`s=n-1=N-2`. Let the relaxed control be uniform across all `n` modes on `[0,1]` and
then equal to mode `n` on `[1,N]`. Every grid schedule has discrepancy `1-1/n` at
time one in its selected first mode. The constant mode-`n` schedule attains that
bound over the full horizon. Thus its grid optimum is exactly `1-1/n`.

A continuous feasible schedule visits modes `1,...,n`, spending `1/n` time in each
on the first cell, and then remains in mode `n`. It uses `n-1` switches. Direct
integration gives cumulative error exactly `(n-1)/n^2`. Consequently

```
OPT_grid - OPT_cont >= (1-1/n)^2 -> 1.
```

This proves sharpness of the coefficient `Delta` in a transfer statement universal
in mode count, grid size, and switch budget. It already uses grid-constant relaxed
inputs and the range `s<=N-2`. For `n=4`, the gap is at least `9/16>1/2`, so a
universal half-cell transfer claim would be false. This calculation by itself does
not assess the exact assumptions or status of any claim in a particular source.

More generally, repeating the word `1,...,n` exactly `m` times on the first cell,
with block length `1/(nm)`, yields error `(n-1)/(n^2 m)`. An earlier proposed value
`(n-1)/(nm)` was a valid but loose upper bound, not the exact error; this was
reported to the author and corrected. One repetition suffices for sharpness.

## Binary refinement, including nonuniform grids

With two modes and uniform spacing, round the normalized cumulative occupation
of mode one at each prefix to the nearest integer, using a fixed tie rule. Each
increment is zero or one because each original normalized cell mass lies in
`[0,1]`. Zero original mass forces a zero increment; unit mass forces a unit
increment. Thus the rounding preserves support, its prefix error is at most
`Delta/2`, and the existing monotonicity and chronology arguments preserve the
error and switch count. A single cell split equally between two original modes
proves that the coefficient one half cannot be improved when a switch is allowed.

There is also a direct proof for arbitrary positive cell lengths with
`D=max_j Delta_j`. Maintain the scalar mode-one discrepancy `e` in `[-D/2,D/2]`.
For a cell of length `d` and original mode-one mass `a`, choose the only supported
mode when `a=0` or `a=d`; this leaves `e` unchanged. Otherwise both modes are
supported, and the two possible updated discrepancies are `e-a` and `e+d-a`.
The first is at most `D/2`, the second at least `-D/2`, and their separation is
`d<=D`; at least one is inside the desired interval. Choose the nearer to zero.
The resulting supported schedule has error at most `D/2` throughout and no more
switches than the original schedule. This is an elementary extension, not a
claim that the multivariate weighted problem has been solved.

## Independent exact checks

Run:

```
python3 code/cia_reopened/check_grid_transfer_review.py
```

The [checker](../code/cia_reopened/check_grid_transfer_review.py) uses exhaustive
selection and a prefix-count dynamic program, independently of the flow proof.
Integer microcell arithmetic and `Fraction` arithmetic make every comparison exact.
The run checks:

- All 8,819 original controls in six small uniform-grid families, including every
  original mode word, every supported grid selection, and all 22,065 supported
  selections satisfying the prefix floor/ceiling bounds. Every instance has a
  feasible selection. Every supported selection preserves chronological block
  order and does not increase switches. All prefix-feasible selections satisfy
  the strict full-horizon discrepancy bound.
- 500 rational controls with varied mode counts, switch locations, positive cell
  lengths, and horizon lengths. A dynamic program independently finds supported
  prefix witnesses. Exact integration at all original and grid breakpoints checks
  the full-horizon guarantee and the binary nearest-prefix refinement.
- 56 sharpness-family parameter pairs, checking switch counts, exact continuous
  construction error, and the matching grid lower and upper bounds.
- 200 two-mode controls on nonuniform rational grids, checking the greedy half-mesh
  bound, support, and switch count, plus the single-cell binary sharpness example.

These checks support the analytic proof; their finite scope does not independently
establish its generality or publication priority.
