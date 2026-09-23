import Mathlib
import Formal.GridSwitching.Model
import Formal.GridSwitching.Endpoint
import Formal.GridSwitching.Compactness
import Formal.GridSwitching.UniformTransfer

/-!
# SC25 and SC26: instance and minimax transfer on a uniform grid

This module proves `cor:opt-transfer` of
`paper-switching-control/sections/11-transfer-and-coarsening.tex`: the two-sided comparisons
`eq:instance-transfer` and `eq:minimax-transfer` between the continuous and the grid values on
a uniform grid of width `h`.

* SC25, `eq:instance-transfer`: `OPT A T s ≤ gridOPT x A T s < OPT A T s + h`
  (`OPT_le_gridOPT_uniform`, `gridOPT_lt_OPT_add`, combined in `instance_transfer`).
* SC26, `eq:minimax-transfer`: `F n s T ≤ gridF x n s T < F n s T + h`
  (`F_le_gridF_uniform`, `gridF_lt_F_add`, combined in `minimax_transfer`).

## How "uniform grid of width `h`" is stated

A grid is a strictly increasing `x : Fin (N + 1) → ℝ` with `x 0 = 0` and `x (Fin.last N) = T`.
Uniformity of width `h` is the hypothesis pair `0 < h` and `∀ j : Fin N, cellLength x j = h`,
exactly as in SC24 (`exists_isGridSchedule_uniform`). This form is used rather than the
concrete `uniformGrid N h` so that the results apply to any grid that happens to be uniform;
`instance_transfer_uniformGrid` and `minimax_transfer_uniformGrid` record that the hypotheses
are met by the concrete uniform grid, hence that the statements are not vacuous. The horizon
`T = N * h` is a consequence, not a further hypothesis. The uniformity hypothesis enters only
through SC24, which is where the sources use it: it makes every row of the cell-occupation
matrix a point of the simplex.

## Where attainment is used, and why the argument fails without it

Attainment (SC07) is used twice, and neither use can be replaced by manipulation of suprema
or infima.

* In `gridOPT_lt_OPT_add` the continuous optimum `OPT A T s` is realized by an actual schedule
  `W` (`exists_OPT_eq`). SC24 transfers that specific `W` to a grid schedule `V` with
  `D W V T < h`, and the triangle inequality `D_le_D_add_schedule` gives
  `gridOPT x A T s ≤ D A V T ≤ D A W T + D W V T = OPT A T s + D W V T < OPT A T s + h`.
  Without attainment one would only have schedules `W` with `D A W T < OPT A T s + ε` for each
  `ε > 0`, and transferring them yields `gridOPT x A T s < OPT A T s + h + ε` for every
  `ε > 0`, hence only the non-strict `gridOPT x A T s ≤ OPT A T s + h`. The strict inequality
  needs one schedule that achieves the infimum exactly.

* In `gridF_lt_F_add` the grid minimax value is realized by an actual grid-constant input `A*`
  (`exists_gridF_eq`), and then
  `gridF x n s T = gridOPT x A* T s < OPT A* T s + h ≤ F n s T + h`.
  This is the step the sources flag: a supremum of pointwise strict inequalities is not
  automatically strict. From `gridOPT x A T s < OPT A T s + h ≤ F n s T + h` for every
  grid-constant `A` one can only conclude `gridF x n s T ≤ F n s T + h` by `csSup_le`, since
  the supremum of a family of values each strictly below a bound need not be strictly below
  it. Attainment converts the family of strict inequalities into a single strict inequality at
  the maximizer, which is then inherited by the supremum because the supremum *equals* that
  value. The last step uses that a grid-constant input is in particular cumulative
  (`gridCumulative_isCumulative`), so it is admissible in the supremum defining `F n s T`.

## Why the left inequality of SC26 is not the left inequality of SC25

`gridOPT` is defined for every input, but `gridF` maximizes only over grid-constant inputs
while `F` maximizes over all cumulative inputs. The two suprema therefore range over different
input classes, and `OPT A T s ≤ gridOPT x A T s` for a fixed `A` does not bound `F n s T` by
`gridF x n s T`: an arbitrary cumulative `A` is not admissible on the right. The left
inequality must instead come from SC06 (`F_le_gridF`), which first replaces `A` by its cell
average `cellAverageInput x A`; averaging preserves every grid node, hence the grid instance
optimum, and produces an input that *is* grid constant. That route is
`eq:minimax-grid-domination`.
-/

namespace GridSwitching

open Set

variable {n N : ℕ}

/-! ## SC25: instance transfer -/

/-- SC25, left inequality of `eq:instance-transfer`: restricting the switch times to grid nodes
can only increase the instance optimum. This is pure restriction of the schedule set
(`OPT_le_gridOPT`); no uniformity and no transfer construction are involved. It is stated here
in the uniform setting only so that the two halves of `eq:instance-transfer` carry the same
hypotheses. -/
theorem OPT_le_gridOPT_uniform (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (_hh : 0 < h) (_hunif : ∀ j : Fin N, cellLength x j = h)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) :
    OPT A T s ≤ gridOPT x A T s :=
  OPT_le_gridOPT hn hx hA s

/-- SC25, right inequality of `eq:instance-transfer`: on a uniform grid of width `h` the grid
instance optimum is strictly below `OPT A T s + h`.

The proof takes a schedule `W` **attaining** `OPT A T s` (`exists_OPT_eq`, SC07), transfers it
by SC24 (`exists_isGridSchedule_uniform`) to a grid schedule `V` with the same block budget and
`D W V T < h`, and concludes by the triangle inequality `D_le_D_add_schedule`. See the module
doc comment for why attainment cannot be dropped here. -/
theorem gridOPT_lt_OPT_add (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin N, cellLength x j = h)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) :
    gridOPT x A T s < OPT A T s + h := by
  obtain ⟨W, hW, hWopt⟩ := exists_OPT_eq hn hA hx.horizon_nonneg s
  obtain ⟨V, hV, hWV⟩ := exists_isGridSchedule_uniform hn hx hh hunif hW
  have hWc : IsCumulative W T := hW.isCumulative
  have hVc : IsCumulative V T := (hV.isSchedule hx).isCumulative
  have hstep : D A V T ≤ D A W T + D W V T :=
    D_le_D_add_schedule hn hA hWc hx.horizon_nonneg fun i t ht => by
      rw [abs_sub_comm]
      exact le_D hWc hVc i ht
  have hgrid : gridOPT x A T s ≤ D A V T := gridOPT_le_D hn hx hA hx.horizon_nonneg hV
  rw [hWopt]
  linarith

/-- SC25 (`eq:instance-transfer`): for every cumulative input, every switch budget and every
uniform grid of width `h`,
`OPT A T s ≤ gridOPT x A T s < OPT A T s + h`. -/
theorem instance_transfer (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin N, cellLength x j = h)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) :
    OPT A T s ≤ gridOPT x A T s ∧ gridOPT x A T s < OPT A T s + h :=
  ⟨OPT_le_gridOPT_uniform hn hx hh hunif hA s, gridOPT_lt_OPT_add hn hx hh hunif hA s⟩

/-! ## SC26: minimax transfer -/

/-- SC26, left inequality of `eq:minimax-transfer`. This is `eq:minimax-grid-domination`
(SC06, `F_le_gridF`), which passes through exact cell averaging. It is **not** a consequence of
the left inequality of SC25: `F` maximizes over all cumulative inputs while `gridF` maximizes
only over grid-constant ones, so the instance comparison `OPT A T s ≤ gridOPT x A T s` cannot
be pushed through the two suprema. -/
theorem F_le_gridF_uniform (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (_hh : 0 < h) (_hunif : ∀ j : Fin N, cellLength x j = h) (s : ℕ) :
    F n s T ≤ gridF x n s T :=
  F_le_gridF hn hx s

/-- SC26, right inequality of `eq:minimax-transfer`: on a uniform grid of width `h` the grid
minimax value is strictly below `F n s T + h`.

The proof takes a grid-constant input `A*` **attaining** `gridF x n s T` (`exists_gridF_eq`,
SC07) and chains
`gridF x n s T = gridOPT x A* T s < OPT A* T s + h ≤ F n s T + h`,
the middle step being SC25 and the last step the admissibility of `A*` in the supremum
defining `F n s T` (a grid-constant input is cumulative). Attainment is essential: the
pointwise strict inequalities `gridOPT x A T s < F n s T + h`, valid for every grid-constant
`A`, only give the non-strict `gridF x n s T ≤ F n s T + h` when passed to the supremum. -/
theorem gridF_lt_F_add (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin N, cellLength x j = h) (s : ℕ) :
    gridF x n s T < F n s T + h := by
  obtain ⟨A, hAconst, hAeq⟩ := exists_gridF_eq hn hx s
  obtain ⟨r, hr, rfl⟩ := hAconst
  have hAc : IsCumulative (gridCumulative x r) T :=
    gridCumulative_isCumulative hx.orderedTimes hr
  have hlt : gridOPT x (gridCumulative x r) T s < OPT (gridCumulative x r) T s + h :=
    gridOPT_lt_OPT_add hn hx hh hunif hAc s
  have hle : OPT (gridCumulative x r) T s ≤ F n s T :=
    OPT_le_F hn hAc hx.horizon_nonneg s
  rw [hAeq]
  linarith

/-- SC26 (`eq:minimax-transfer`): for every switch budget and every uniform grid of width `h`,
`F n s T ≤ gridF x n s T < F n s T + h`. -/
theorem minimax_transfer (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin N, cellLength x j = h) (s : ℕ) :
    F n s T ≤ gridF x n s T ∧ gridF x n s T < F n s T + h :=
  ⟨F_le_gridF_uniform hn hx hh hunif s, gridF_lt_F_add hn hx hh hunif s⟩

/-! ## The hypotheses are met by the concrete uniform grid -/

/-- SC25 on the concrete uniform grid `uniformGrid N h` with horizon `N * h`. -/
theorem instance_transfer_uniformGrid (hn : 0 < n) {h : ℝ} (hh : 0 < h)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A ((N : ℝ) * h)) (s : ℕ) :
    OPT A ((N : ℝ) * h) s ≤ gridOPT (uniformGrid N h) A ((N : ℝ) * h) s ∧
      gridOPT (uniformGrid N h) A ((N : ℝ) * h) s < OPT A ((N : ℝ) * h) s + h :=
  instance_transfer hn (isGrid_uniformGrid hh) hh (fun j => cellLength_uniformGrid j) hA s

/-- SC26 on the concrete uniform grid `uniformGrid N h` with horizon `N * h`. -/
theorem minimax_transfer_uniformGrid (hn : 0 < n) {h : ℝ} (hh : 0 < h) (s : ℕ) :
    F n s ((N : ℝ) * h) ≤ gridF (uniformGrid N h) n s ((N : ℝ) * h) ∧
      gridF (uniformGrid N h) n s ((N : ℝ) * h) < F n s ((N : ℝ) * h) + h :=
  minimax_transfer hn (isGrid_uniformGrid hh) hh (fun j => cellLength_uniformGrid j) s

end GridSwitching
