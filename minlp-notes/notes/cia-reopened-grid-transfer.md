# Uniform-grid transfer without increasing the switch count

Date: 2026-09-07. Status: [independent mathematical and exact computational review](review-cia-reopened-grid-transfer.md) and [primary-source comparison](cia-reopened-literature.md) complete. Controlled prefix rounding and support-preserving matching rounding are established. The retained contribution is the switch-preserving consequence, its sharp universal constant, and its application to the continuous CIA bounds. The [result statement](../results/cia-sharp-grid-transfer.md) collects the final conclusions.

## Statement

[Lean topic 17](../formal/topics/17-grid-switching/COVERAGE.md) verifies
supported prefix rounding, the switch-preserving transfer and sharpness
claims, and the binary refinement. It also proves an arbitrary-grid
one-switch certificate: for maximum cell length `barDelta` and the same
measurable input,
`OPT_grid(alpha,1)-barDelta/2 <= OPT_cont(alpha,1) <= OPT_grid(alpha,1)`.
Moving the switch of an attained continuous optimum to the nearer endpoint
of its cell proves this non-strict bound; no sharpness claim for the gap
between optima follows. The linked verification record documents completed
proof checks, not verification of the network-flow implementation or its
bit-cost bound.

Let `w:[0,T]->{e_1,...,e_n}` be an integer control with at most `s` switches, and let `T=N Delta`, with a uniform grid of `N` intervals. There is an integer control `v`, constant on every grid interval, such that:

1. `v` has at most `s` switches;
2. its sequence of nonempty constant blocks is a subsequence of the original chronological block sequence, after merging equal consecutive modes;
3. `max_i sup_t |integral_0^t (v_i-w_i)| < Delta`.

For rational original switch times and rational `Delta`, a network-flow construction computes `v` in polynomial time in `n`, the explicitly supplied grid length `N`, and the input bit length. The claim does not give a polynomial algorithm in `log N` for an explicitly output length-`N` schedule.

Consequently, for any fixed measurable relaxed control `alpha`, write `OPT_cont(alpha,s)` and `OPT_grid(alpha,s)` for its best cumulative error with continuous and grid-restricted switches. Then

```
OPT_cont(alpha,s) <= OPT_grid(alpha,s) < OPT_cont(alpha,s)+Delta.
```

If one defines the continuous minimax over all measurable relaxed controls and the grid minimax over grid-constant relaxed controls, the immediately justified conclusion is

```
F_grid(n,s,N,Delta) <= F_cont(n,s,N Delta)+Delta.
```

No reverse minimax inequality is inferred from the instance-specific comparison, because the two suprema range over different relaxed-control classes. The constant `Delta` is independent of the switch budget. For one switch, the existing nearest-endpoint transfer gives the stronger `Delta/2` correction; the present statement is mainly useful for larger budgets.

## Proof

For grid cell `j`, let `a_ij=Delta^(-1) integral_cell_j w_i`, and let `S_ik=sum_(j<=k) a_ij`. Every column of `a` sums to one.

Create a supply-one node for each cell. It may send flow to mode `i` at that cell only if `a_ij>0`. Each mode has a chronological chain. The chain edge after cell `k` has integer lower and upper capacities `floor(S_ik)` and `ceil(S_ik)`. The mode chains discharge to a common sink of demand `N`. The assignment `a_ij` and its prefix sums provide a feasible fractional flow. Integral flow feasibility gives a zero-one assignment `y_ij` supported where `a_ij>0`, with one selected mode per cell and

```
floor(S_ik) <= sum_(j<=k)y_ij <= ceil(S_ik).
```

Thus every endpoint discrepancy between `v` and `w` has absolute value strictly smaller than `Delta`. Within a cell, the selected component of `integral(v-w)` is nondecreasing and every other component is nonincreasing. Hence its maximum absolute value occurs at an endpoint. The strict bound therefore holds throughout the horizon.

For each cell choose a time at which the original `w` equals its selected mode. Such a time exists on a set of positive measure by support preservation. Choose it away from original switches and grid boundaries. These selected times are strictly increasing with cell index. The original block containing the selected time therefore has a nondecreasing block index. Every change of selected mode requires an increase in the original block index. There are at most `s` such increases that change modes; equivalently deleting unused blocks and merging repeats cannot increase the original number of switches. This proves the block-subsequence and switch-count claims.

For fixed `alpha`, a continuously placed optimum exists: there are finitely many mode words of length at most `s+1`, each ordered switch-time simplex is compact, and cumulative error is continuous in its switch times. Apply the construction to such an optimum and use the triangle inequality. Restriction of feasible schedules gives the other inequality. The grid minimax upper bound follows by taking the supremum, with the strict instance-wise bound weakened to a non-strict universal bound.

## Meaning and limits

The construction repairs a chosen continuous schedule; it does not independently solve the CIA optimization problem. It preserves the switch count, not minimum dwell times or arbitrary restrictions on allowed consecutive modes: skipping an intermediate mode can create a forbidden direct transition. The uniform grid is essential to this particular unit-flow integrality proof. Unequal cell lengths do not give unit assignment weights.

The chronological argument applies to any support-preserving grid rounding procedure. It is separate from the classical prefix-rounding construction. The linear dependence on the mesh width is useful even when the continuous schedule repeatedly returns to a mode; simply rounding every switch separately would accumulate a budget-dependent error estimate.

## Binary controls on arbitrary grids

For two modes, an elementary supported greedy construction improves the schedule-transfer bound to `D/2`, where `D` is the largest grid-cell length, even on a nonuniform grid. This refinement and its sharpness passed independent review.

Maintain the mode-one endpoint discrepancy `e=integral(v_1-w_1)` in `[-D/2,D/2]`. On a cell of length `d<=D`, let `a` be the occupation of mode one by `w`. If `a=0`, select mode two; if `a=d`, select mode one. These forced choices leave `e` unchanged and preserve support. Otherwise both modes occur on the cell. The new discrepancy is either `e-a` or `e+d-a`. The first is at most `D/2`, the second is at least `-D/2`, and their distance is `d<=D`. Therefore at least one lies in `[-D/2,D/2]`; choose it. The second component's discrepancy is the negative of the first. Cellwise monotonicity supplies the all-time error bound, and the chronological support argument preserves the number of switches.

Rational occupation masses permit exact rational arithmetic, with one decision per cell after those masses have been computed. The constant `1/2` is sharp for schedule transfer: on a single cell of length `D`, take `w` equal to each mode for half the cell. Either constant grid schedule has error `D/2` at the final endpoint. This does not assert a matching minimax difference over grid-constant relaxed inputs.

## Sharp universal transfer constant and a half-grid obstruction

The coefficient one cannot be reduced uniformly over mode counts and switch budgets, even when the relaxed control is constant on the same grid and `1<=s<=N-2`.

Fix integers `n>=2,m>=1`, use unit grid length `N=nm+1`, and allow `s=nm-1=N-2` switches. Set `alpha_i=1/n` for every mode in the first cell `[0,1]`, and `alpha=e_n` for the rest of the horizon.

Every grid schedule selects one mode throughout the first cell. Its negative discrepancy at time one is `1-1/n`, proving `OPT_grid>=1-1/n`. The constant schedule `e_n` has error exactly `1-1/n`: every other discrepancy is `1/n` after time one, and all discrepancies then remain constant. Thus

```
OPT_grid=1-1/n.
```

For a continuous competitor, repeat the word `1,...,n` exactly `m` times within the first cell, using blocks of length `1/(nm)`, and continue mode `n` after time one. The final block merges with the pure tail. There are exactly `nm-1` switches. All discrepancies reset to zero after each cycle of length `1/m`; within each cycle, a component's maximal absolute discrepancy is at most `(n-1)/(n^2 m)`. The first mode at the end of its activation attains that value. After time one all discrepancies are zero. Therefore

```
OPT_cont <= (n-1)/(n^2 m),
OPT_grid-OPT_cont >= (1-1/n)(1-1/(nm)).
```

Already taking `m=1` and letting `n` grow proves sharpness of the universal unit-grid transfer constant. Multiplying all times by `Delta` gives the general scale. The argument is an instance-wise gap, not an equality for the difference between two minimax functions.

For the concrete choice `n=4,m=1`, `N=5` and `s=3`, the grid optimum is `3/4`, while the continuous competitor has error `3/16`. Hence the gap is at least `9/16>1/2`. This disproves a universal half-grid instance-wise correction.

### Relation to the source's half-grid discussion

Zeile's 2021 dissertation, *Combinatorial Integral Decompositions for Mixed-Integer Optimal Control*, printed p.139 (PDF page index 146), argues immediately before Conjecture 7.1 that discretization adds at most half the maximum grid width because individual switch times can be moved by that amount. The same argument appears in the final Sager–Zeile article on printed p.615. The construction above shows why that inference is invalid for multiple switches. These passages are heuristics leading into conjectures, not proved rounding theorems; the result should not be described as refuting an established theorem. Independent source and mathematical reviews checked the instance-wise comparison and admissible-control conventions.

Primary source: [open author dissertation](https://mathopt.de/publications/Zeile2021a.pdf). The complete text was newly retrieved during this continuation, resolving the earlier access limitation for this source.

## Source comparison

The prior integral-prefix construction is recorded in [the earlier investigation](cia-many-mode-switching-investigation.md), with attribution to classical controlled rounding and Knuth's two-way rounding. Bestehorn and Kirches, *The integrated control deviation of mixed-integer optimal control problems with vanishing constraints*, PAMM (2021), DOI `10.1002/pamm.202000022`, already establish support-preserving rounding with error at most `Delta`. Their fuller *Matching Algorithms and Complexity Results for Constrained Mixed-Integer Optimal Control with Switching Costs* develops matching algorithms and complexity results. The [source audit](cia-reopened-literature.md) records precise statements and page locators. No matching sharp switch-budget-preserving transfer theorem was found in the bounded search; no independent novelty is claimed for matching rounding itself.
