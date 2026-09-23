# Exact CIA algorithms for many modes and a fixed switch budget

Date: 2026-09-07. Status: independent mathematical and implementation reviews passed, including mode-specific minimum dwell times. No matching specialized CIA result was found in the bounded primary-source search; standard dynamic programming is explicitly credited.

Let a rational grid have `N` positive-length intervals and let `n` relaxed mode allocations be nonnegative and sum to elapsed time. The objective is the maximum absolute cumulative allocation error over all components and times. Initial activation is free. Repeated modes and constant schedules are allowed.

**One-switch theorem.** Exact optimization under at most one switch takes `O(nN)` arithmetic operations on an arbitrary grid. It permits a subset of admissible switch boundaries and a fixed initial mode. With cumulative input already available for random access, `O(n log N)` further queries suffice.

**Fixed-budget theorem.** With switch budget `s>=0` and `k=min(s+1,N)`, exact optimization takes

```
O(nN + binomial(N-1,k-1) n (k 2^k + 3^k))
```

arithmetic operations and `O(nN+n2^k)` storage. In particular, two switches admit `O(nN^2)` exact optimization. The dependence on the number of modes is linear for every fixed budget. Rational input gives polynomial bit complexity for fixed `s`; the algorithm is not fixed-parameter tractable in `s` alone because the exponent of grid size grows with the budget.

The fixed-budget theorem also permits a nonnegative minimum dwell duration for each mode. Every maximal constant run, including initial and final runs, must meet that mode's duration; unused modes impose no dwell obligation. Feasibility is decided exactly. More generally the fixed-block recurrence permits restrictions determined solely by each mode's assigned blocks, with their checking cost included. Extending those restrictions to the full-budget enumeration also requires invariance under subdivision of a run into adjacent equally labeled blocks, as minimum dwell times satisfy. Arbitrary transition graphs couple different modes and are outside this theorem.

## Why the mode enumeration disappears

For one switch at time `t`, with distinct initial and final modes `p,q`, the exact error is

```
max{max_(i outside {p,q}) m_i, t-A_p(t), T-t-m_q},
```

where `m_i=A_i(T)`. For a fixed initial mode, a largest-total remaining mode is always an optimal final choice. For `n>=3`, if `h1,h2` are the two largest-total modes, only three pairs need checking per boundary: `(h1,h2)`, `(h2,h1)`, and `(p,h1)`, where `p` maximizes the cumulative allocation among all other modes. With two modes only the first two pairs are needed; with one mode the constant schedule is optimal. Constants are checked separately. Monotonicity handles all intermediate times even if the relaxed input varies within cells.

For the general result, fix `k` positive consecutive blocks and let `l_j` be their lengths. A mode `i` assigned the subset `U` of blocks has exact cost

```
c_i(U)=max_j |A_i(t_(b_j))-sum_(h in U,h<=j) l_h|.
```

The empty subset has cost `m_i`, so unused modes are included. Set the cost to infinity for a subset violating its mode's dwell rule, merging consecutive assigned blocks when measuring runs. Assigning all blocks is a partition into these mode-specific subsets. The standard recurrence

```
D_i(S)=min_(U subset S) max{D_(i-1)(S minus U),c_i(U)}
```

therefore gives its exact optimum. There are `3^k` transitions per mode. Enumerate the grid boundary sets and retain the best assignment. Every schedule using fewer switches is represented by subdividing its runs and assigning adjacent blocks the same mode; this preserves actual run lengths and dwell feasibility.

The [full proofs](../notes/cia-reopened-practical-algorithm.md) also give an optimal last-block completion rule for any fixed prefix and a supporting `d^2+d` candidate-label bound for `d` fixed roles. Neither justifies greedily choosing earlier blocks.

## Implementation and observed performance

[Lean topic 17](../formal/topics/17-grid-switching/COVERAGE.md) verifies the
one-switch candidate reduction, fixed-prefix completion, subset recurrence,
and unrestricted fixed-budget covering argument, including the state,
transition, and partition counts. This does not verify the Python code,
measured runtimes, bit-cost analysis, or the mode-specific dwell extension.
The linked verification record retains the completed proof checks.

[rounding.py](../code/cia_reopened/rounding.py) uses exact rational arithmetic and no optimization package. Its public routines implement one-switch optimization, prescribed-block assignment, fixed-budget optimization, and last-block completion. Infeasible dwell-constrained cases return `None`.

On a public three-mode Lotka–Volterra control profile, the exact one-switch optimum for the documented normalized and quantized 12,000-interval input is `1.889`; the recorded solve took about `0.27` seconds. Exact aggregation to a permitted half-unit switching grid gives optimum `1.5` with two switches. On a permitted unit switching grid, three switches give `0.8540056` and use a repeated mode. These are exact results for the specified input and permissible boundaries. They do not assert full fine-grid optimality for the coarse tests or demonstrate improved physical-state or economic performance. The [benchmark record and source](../notes/cia-reopened-practical-algorithm.md) include the normalization error, data hash, independent enumeration, and reproduction commands.

The [first independent review](../notes/review-cia-reopened-practical-algorithm.md) and [fixed-budget review](../notes/review-cia-reopened-fixed-budget.md) cover direct original-objective enumeration, thousands of exact cases, controls varying within grid cells, repeated modes, ties, and feasible/infeasible dwell restrictions. The [source audit](../notes/cia-reopened-literature.md) distinguishes the parameter dependence here from established general CIA graph algorithms and dwell-time heuristics.

The method is intended for many modes or a small set of candidate switching boundaries. It retains combinatorial growth in grid size and switch budget; the one-switch specialization should be used when applicable.
