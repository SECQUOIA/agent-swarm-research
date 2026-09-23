# Arbitrary-grid one-switch minimax and sharp grid transfer: obligations

This frozen inventory covers topic 17 of the
[recommended-topic sequence](../../RECOMMENDED-TOPICS-PLAN.md): the exact
one-switch minimax value on an arbitrary grid
([Section 8](../../../paper-switching-control/sections/08-finite-grid-one-switch.tex)),
the sharp grid-transfer results
([Section 11](../../../paper-switching-control/sections/11-transfer-and-coarsening.tex)),
and the supporting algorithm and certificate claims of
[Section 10](../../../paper-switching-control/sections/10-instance-algorithms.tex)
that those two sections rely on. The foundational definitions are
[Section 1](../../../paper-switching-control/sections/01-foundations.tex) and the
one-switch error formula of
[Section 2](../../../paper-switching-control/sections/02-uniform-one-switch.tex).
Full derivations are [`cia-reopened-finite-grid.md`](../../../notes/cia-reopened-finite-grid.md)
and [`cia-reopened-grid-transfer.md`](../../../notes/cia-reopened-grid-transfer.md).

**Relation to topic 1.** The existing package
[`topics/01-switching-control`](../01-switching-control/README.md) verified exact
values on *fixed small unit grids with exactly three modes*. Its model is
hard-wired: the mode count is the literal type `Fin 3` and cells have width one.
This topic needs an arbitrary mode count `n >= 3`, an arbitrary strictly
increasing grid, and an arbitrary horizon, so it builds a new model in
`Formal/GridSwitching`. Three assets of the old package are reused rather than
rewritten: `SwitchingControl.Boundary` (abstract nonintegral-interpolation and
finite-witness-closure arguments), `SwitchingControl.Continuous.endpoint_bound`
(endpoint control implies interior control on an arbitrary-width cell), and the
measurable-rates pattern of `SwitchingControl.Measurable`. Any reuse must be
identified in `COVERAGE.md`; nothing may be inherited silently.

An obligation is discharged by an actual theorem with the stated hypotheses.
This inventory is not a completion claim.

Conventions fixed for the whole package:

- `n >= 2` modes unless an entry says `n >= 3`; horizon `T > 0`; a grid is a
  strictly increasing `x_0 = 0 < ... < x_N = T` with cell lengths `Delta_j` and
  `bar Delta = max_j Delta_j`.
- **Initial activation is free**: only a change between two successive active
  modes is a switch. Blocks `k` and switches `s` are related by `k = s + 1`;
  `F` is indexed by switches, `G^-` by blocks. Repeated modes, constant
  schedules, zero-length blocks and unrestricted initial and final modes are
  always permitted, and there are no dwell or transition restrictions unless an
  entry states them.
- The minimax quantifier order is **sup over relaxed inputs of min over
  schedules**; the adversary moves first. No reverse-order value is defined.
- `OPT_s^T(A)` is defined for every measurable `A`, but `F^T_{n,s}` maximizes
  only over grid-constant inputs. This asymmetry is load-bearing and must be
  preserved exactly.
- Two unrelated objects are both written `H` in the sources: `H_n(T)` is the
  *continuous* one-switch minimax of Section 2, while `H` of `eq:grid-H` is the
  two-large-modes grid quantity. They must get distinct Lean names.
- Division is total in Lean; hypotheses the sources leave implicit must be
  stated. Boundary cases must be included: `N = 1`, `a = b`, `b = N`,
  zero-length phases, `tau = 0`, `tau = T`, `n = 2` where admitted, and the
  empty omitted-mass maximum.

## Tier 0: model and definitions

| ID | Required assertion | Source |
|---|---|---|
| SC01 | Define the simplex, a relaxed control as a measurable map into it, its cumulative allocation `A_i(t) = int_0^t alpha_i` and terminal masses `m_i`. | `eq:cumulatives` |
| SC02 | Prove the characterization of the cumulative class `Acal_n(T)`: `A_i` nondecreasing, 1-Lipschitz, `A_i(0) = 0`, `sum_i A_i(t) = t`; **and the converse**, that every such vector arises from a relaxed control. | Section 1, model paragraph. The converse needs absolute continuity and a.e. differentiation; it is a genuine obligation, not a definition. |
| SC03 | Define schedules by `eq:schedule-parameterization`, the cumulative occupation of a word and ordered times, the switch count with free initial activation, and the class `Wcal_{n,k}(T)`. Prove the closure claim that deleting zero-length blocks and merging equal consecutive modes cannot increase the switch count. | Section 1 |
| SC04 | Define `D`, `D^-` (`eq:errors`), the instance optima (`eq:instance-optima`), the minimax values (`eq:minimax-values`), and the grid analogues (`eq:grid-definitions`), preserving the asymmetry recorded above. | Section 1 |

## Tier 1: foundational quantitative claims

| ID | Required assertion | Source |
|---|---|---|
| SC05 | Endpoint monotonicity: on a block with selected mode `p`, `A_p - W_p` is nonincreasing and every other `A_i - W_i` is nondecreasing; hence both errors are determined by block endpoints, and for a grid schedule by grid endpoints, even when the input varies inside cells. | `lem:endpoint` |
| SC06 | Cell averaging preserves every grid endpoint and hence the grid error and grid instance optimum of every grid schedule; consequently `F_{n,s}(T) <= F^T_{n,s}` and the one-sided analogue. Averaging does **not** preserve the continuous instance optimum, and that must not be claimed. | `eq:minimax-grid-domination` |
| SC07 | Compactness and attainment: `Acal_n(T)` and `Wcal_{n,k}(T)` are compact in the uniform norm; each instance optimum is 1-Lipschitz in `A`; all instance optima and minimax values are attained. | `prop:compactness` |
| SC08 | Scaling `F_{n,s}(T) = T F_{n,s}(1)`, the `T = 0` convention, and monotonicity in the switch budget. | `eq:scaling` |
| SC09 | `F_{n,0}(T) = F^T_{n,0} = T(1 - 1/n)` on every grid. | `prop:no-switch` |
| SC10 | The three-term one-switch error formula `D(A, W^{p,q,tau}) = max{max_{i notin {p,q}} m_i, tau - A_p(tau), T - m_q - tau}`, including `tau = 0`, `tau = T`, and the `n = 2` convention that the omitted maximum is zero. | `lem:one-switch-error` |

## Tier 2: the arbitrary-grid one-switch minimax

| ID | Required assertion | Source |
|---|---|---|
| SC11 | Dominance: for a fixed initial mode and switch time, a largest-mass mode other than the initial one is an optimal final mode; only `p -> 1` with `p != 1` and `1 -> 2` need be considered. | Section 8 proof; `thm:linear-one-switch` |
| SC12 | The two linear-program families `eq:grid-LP` are well formed, and **sufficiency** holds: every feasible point of either family yields, by linear interpolation through `0, t_a, t_b, T`, a grid-constant relaxed control whose grid one-switch optimum is at least `E`. Include constant schedules, `a = b`, and `b = N`. The all-initial-modes family deliberately does **not** impose `m_2 <= E`. | Section 8; note Sections "Linear programs", "Sufficiency" |
| SC13 | `F^T_{n,1} >= T/3`, by three modes of mass `T/3`. | Section 8 |
| SC14 | **Coverage**: for `T/3 < E < F` the cutoff indices `k_1 <= k_2` are positive, the case split on `m_2 <= E` versus `m_2 > E` (the latter using `3E > T`) applies, averaging modes `3..n` preserves the required inequalities, and the resulting point is feasible in the corresponding closed program; then a pigeonhole over the finite set of (family, `a`, `b`) and a bounded-subsequence limit produce a feasible point of objective `F`. The cutoff upper inequalities are strict before the limit. | Section 8; note "Coverage" |
| SC15 | The boundary case `F = T/3`: the explicit two-large-modes point with `a = b = c` is feasible, using `E <= t_c <= 3E` and `t_{c-1} <= E`. | Section 8 |
| SC16 | The two-large-modes family is bounded by `H`: `E <= (T + t_b)/4` and `E <= (T - t_{b-1})/2`, and only `b = c` can exceed `T/3`. | Section 8 |
| SC17 | The two-large-modes family attains `H`, by the explicit witness `eq:grid-H-witness`. | Section 8 |
| SC18 | Symmetrization to one distinguished mode in the all-initial-modes family, with its three preservation claims (averaged initial deficit stays above `E`; the common terminal mass does not exceed the old `m_2`, so the first eligible final time moves weakly later; mode 1's initial deficit is nondecreasing). | Section 8; note "One distinguished mode suffices" |
| SC19 | Elimination: with `x = A_1(A)`, `y = A_1(B)` and bulk values, such states exist **iff** `E <= A`, `nE <= (n-2)A + B` and the `M`-interval `eq:grid-M-interval` is nonempty; the reconstruction `eq:grid-xy-reconstruct` works; and the endpoint comparisons are *exactly* `eq:grid-admissible` together with `L_ab <= E <= U_ab`. Both directions of the equivalence are required, and all eight comparisons must be reproduced. | Section 8; note "Eliminate cumulative states" |
| SC20 | **`thm:finite-one`**: for `n >= 3` and every strictly increasing finite grid, `F^T_{n,1} = max{H, max over admissible (a,b) of U_ab}`, with an empty inner maximum ignored; a maximizing relaxed input exists with at most three phases and two component types; `N = 1`, zero-length phases and constant integer controls are permitted, and arbitrary measurable inputs are covered through SC05. | `thm:finite-one` |
| SC21 | `cor:three-unit-one`: the residue formula for `F^unit_{3,1}(N)`, the `N = 1` value `2/3`, the residue inequalities `eq:residue-inequalities`, and the two explicit witnesses. | `cor:three-unit-one` |
| SC22 | `ex:five-nine`: `F^unit_{5,1}(9) = 17/5`, with the stated rates, terminal masses `(13/5, 8/5, 8/5, 8/5, 8/5)`, the dominance lower bound, and the two-case analytic upper bound; the value exceeds both the uniform-input value `16/5` and the three-mode value `3`. | `ex:five-nine` |
| SC23 | The nonuniform admissibility witness: for `n = 9` and the stated six-point grid, a truncated formula gives `2077/216` whereas the exact first-family maximum is `2593/270`. | Section 8, closing paragraph |

## Tier 3: sharp grid transfer and certified coarsening

| ID | Required assertion | Source |
|---|---|---|
| SC24 | `thm:sharp-transfer`: on a uniform grid of width `h`, every finitely switching schedule `W` has a grid schedule `V` with no more switches and `norm(V - W)_inf < h`, whose word is a chronological subsequence of the original block word after merging adjacent equal labels. The rounding step requires an integral assignment with prefix bounds `floor(S_ji) <= sum_{q<=j} y_qi <= ceil(S_ji)`, supported where the cell occupation is positive. **This is the package's identified risk**: the sources obtain it from integral network-flow feasibility, which the pinned Mathlib does not provide. Any correct route is acceptable; if it cannot be completed it must be recorded as an open obligation and the topic must not be labeled complete. | `thm:sharp-transfer` |
| SC25 | `eq:instance-transfer`: `OPT_s(A) <= OPT_s^T(A) < OPT_s(A) + h` for every `A in Acal_n(T)`, every `s >= 0`, and a uniform grid of width `h`. | `cor:opt-transfer` |
| SC26 | `eq:minimax-transfer`: `F_{n,s}(T) <= F^T_{n,s} < F_{n,s}(T) + h`. The left inequality must come from SC06 (cell averaging), **not** from SC25; the strict right inequality must use attainment of a grid maximizer from SC07. A supremum of strict pointwise inequalities is not automatically strict, and the proof must not pretend otherwise. | `cor:opt-transfer` |
| SC27 | `prop:binary-transfer`: for two modes on an **arbitrary** grid, a finitely switching schedule has a grid replacement with no more switches and discrepancy at most `bar Delta / 2` (non-strict), and that constant is sharp for transfer of a supplied schedule. | `prop:binary-transfer` |
| SC28 | `prop:transfer-sharpness`: the coefficient one in `eq:instance-transfer` is not uniformly reducible, even for grid-constant inputs with `1 <= s <= N - 2`. Include the family `N = n + 1`, `s = n - 1` with gap at least `(1 - 1/n)^2`, the repeated-cycle family `N = nm + 1`, `s = nm - 1` with gap at least `(1 - 1/n)(1 - 1/(nm))`, and the concrete `n = 4`, `m = 1` gap `9/16 > 1/2`. | `prop:transfer-sharpness` and the following paragraph |
| SC29 | The source correction, recorded as scope rather than mathematics: the refuted statement is the instance-wise half-mesh inference preceding the conjecture in the cited article and dissertation, which is a heuristic and not a proved theorem; the example says nothing about the difference of two minimax values; the one-switch half-mesh estimate survives. | Section 11 |
| SC30 | `thm:certified-coarsening`: `U_h - h < OPT_s(A) <= U_h = D(A, V_h)`; the `M = ceil(1/eps)` consequence; the `O(n(N+M))` coarse-data construction for nonaligned grids; the `s = 1` and `n = 2` refinement `U_h - h/2 <= OPT_s(A) <= U_h`; the nested-grid chain; and the clipping remark, including that clipping makes the endpoint non-strict while `U_h - h = 0` retains strictness. | `thm:certified-coarsening` and the following remarks |
| SC31 | `ex:dwell-grid-gap`: with two modes, one switch and dwell `1/2`, the dwell-constrained gap stays `1/2` along every uniform grid with an odd number of cells. | `ex:dwell-grid-gap` |
| SC32 | `cor:coarse-perturbation`: `U_h - h - delta < OPT_s(A) <= D(A, V_h) <= U_h + delta`, suboptimality strictly below `h + 2 delta`, and `delta = rho T` from a pointwise rate bound. | `cor:coarse-perturbation` |

## Tier 4: supporting algorithm and certificate claims

| ID | Required assertion | Source |
|---|---|---|
| SC33 | `thm:linear-one-switch`: at a fixed boundary an optimal ordered pair is among the three stated candidates (two for `n = 2`), so the at-most-one-switch problem is solved by comparing candidates at all permitted boundaries against the best constant schedule; with a prescribed initial mode and any subset of permitted boundaries. | `thm:linear-one-switch` |
| SC34 | The unimodality refinement: `t - A_p(t)` is nondecreasing and the difference of the two deficits is strictly increasing, so the two boundaries adjacent to the unique crossing suffice. | Section 10 |
| SC35 | `lem:final-residual`: the exact error `max{E_0, max_{i != j} r_i, T - u - r_j}` of completing a fixed prefix in mode `j`, that a largest-residual eligible mode is optimal, and that residuals may be negative. Its stated limitation (no greedy rule for choosing the prefix) must be preserved. | `lem:final-residual` |
| SC36 | `prop:subset-DP`: the block-subset cost `eq:block-subset-cost` is exactly the component error of a mode occupying those blocks, including disconnected subsets and `c_i(empty) = m_i`, and the recurrence `eq:subset-DP` computes the optimum. | `prop:subset-DP` |
| SC37 | `thm:fixed-budget`: exact fixed-budget optimization with the stated arithmetic and storage bounds, including the run-subdivision covering claim that any feasible grid schedule has at most `k` maximal runs and can be subdivided to exactly `k` nominal blocks without changing the control. | `thm:fixed-budget` |

## Explicit exclusions

- `lem:candidate-labels`, which Section 10 itself disclaims as unused by the
  subset algorithm, and the continuous exact LP benchmark `eq:continuous-cell-LP`.
- The remaining sections of the manuscript: uniform-grid recurrences, the
  heavy-mode and reach results, four-block certificates, small-budget minimax,
  general budgets, higher reach, and the refutation apparatus for the published
  conjecture beyond SC29's scope statement.
- Machine-level bit-complexity claims. As in topics 3 and 16, the verified
  content of an algorithmic claim is its correctness, termination and exact
  arithmetic-operation or size recursions; no counted bit-cost model is claimed.
  Every complexity assertion above must be mapped in `COVERAGE.md` either to a
  Lean statement or to this exclusion, with its reason.
- Numerical LP and MILP comparisons, the Python checker, benchmark timings, and
  the Lotka-Volterra application.
- Novelty and bibliographic priority. The sources credit support-preserving
  matching rounding, network integrality, and standard subset dynamic
  programming as established.
