# Exact one-switch worst-case error on every rational grid

Date: 2026-09-07. Status: full proof, independent mathematical review, and independent implementation review passed. The targeted primary-literature search found no matching theorem; publication priority remains qualified.

**Theorem.** For every `n>=3` and rational grid `0=t_0<...<t_N=T`, the full worst-case cumulative CIA error under at most one grid-endpoint switch has an explicit formula evaluable in `O(N^2)` exact rational arithmetic operations. A worst relaxed control has at most three time phases and just two types of component. Its value and a compressed extremizer have polynomial bit complexity in the grid input length and `log n`; expanding all `n` component functions costs at least linear time in `n`.

Both controls are constant on the supplied grid cells, initial activation is free, and constant integer schedules are allowed. Cell averaging gives the same value if the relaxed input may vary measurably inside cells. The error is the maximum absolute cumulative component discrepancy over the whole horizon. This theorem optimizes over all relaxed inputs; rounding one given input is cheaper.

## Explicit formula

Let `c` be the first index with `t_c>=T/3`, and put

```
H=min{(T+t_c)/4, (T-t_(c-1))/2}.
```

For every `1<=a<=b<=N`, set `A=t_a`, `B=t_b`, `P=t_(a-1)`, `Q=t_(b-1)`. Define

```
L_ab=max{T/3, (n-1)T/n-B, ((n-1)T-A-(n-1)B)/n},
U_ab=min{A, ((n-2)A+B)/n, (n-1)T/n-P,
         ((n-1)T-P-(n-1)Q)/n, (T-P+(n-2)A)/n}.
```

Retain only pairs satisfying `(n-2)(T-A)<=(n-1)B` and `L_ab<=U_ab`. Then the exact minimax is

```
F_n(t)=max{H, max_retained_pairs U_ab}.
```

An empty inner maximum is ignored. A maximizing `H` has two identical distinguished modes and `n-2` identical remaining modes, in at most two time phases. A maximizing pair has one distinguished mode and `n-1` identical remaining modes, in at most three phases. The [full proof](../notes/cia-reopened-finite-grid.md) gives explicit rational reconstruction, proves the reductions through constant-dimensional LPs, and handles ties and empty phases.

For a fixed initial mode, a largest-total remaining mode is always an optimal final mode. Sorting terminal totals therefore reduces all schedules to two families. Averaging interchangeable modes preserves each family's obstruction. Cutoff times for the two relevant final totals leave only two grid indices. Eliminating their cumulative states and terminal totals yields the formula. This is the structural reason the mode count enters only through rational coefficients.

## A resolved example

For five modes on nine unit cells,

```
F_5(9)=17/5.
```

The previously retained lower witness is now matched by a universal upper bound. A short analytic proof, independently derived during review, is included with the full theorem; this particular value does not depend on numerical LP certificates. It exceeds both the uniform-input value `16/5` and the three-mode worst-case value `3`.

## Implementation and verification

[Lean topic 17](../formal/topics/17-grid-switching/COVERAGE.md) verifies the
arbitrary-grid formula, both LP families, reconstruction of a compressed
maximizer, and the exact examples. Its verification record documents the
completed proof checks. This guarantee concerns the mathematical definitions;
it does not verify the Python implementations or their bit complexity.

[minimax.py](../code/cia_reopened/minimax.py) implements the formula and compressed extremizer using only the Python standard library. [finite_grid_research.py](../code/cia_reopened/finite_grid_research.py) retains the earlier LP formulation as an optional independent audit; its numerical discovery stage is not needed by the exact solver.

The [mathematical review](../notes/review-cia-reopened-finite-grid.md) and [implementation review](../notes/review-cia-reopened-finite-grid-code.md) independently checked all reductions. Their checks include full-control LPs, direct enumeration using the original absolute cumulative error, 99 additional certified-LP comparisons, and 24 extreme arithmetic cases with mode counts exceeding `10^100` and narrow rational grid intervals. Numerical MILPs supply additional corroboration, not the proof.

The [literature assessment](../notes/cia-reopened-literature.md) distinguishes established CIA optimization methods from this outer minimax characterization. The result supplies exact benchmarks for chosen grids; it does not optimize the grid itself or solve arbitrary-budget minimax problems. A failed simplified formula on a nonuniform grid is retained in the proof note to explain why all admissibility conditions matter.
