import Formal.GridSwitching.Compactness

/-!
# SC31: a minimum dwell time can prevent convergence under grid refinement

This module adds the one notion the model of `Formal.GridSwitching.Model` deliberately
lacks — a *minimum dwell time* — and formalizes `ex:dwell-grid-gap` of
`paper-switching-control/sections/11-transfer-and-coarsening.tex`.

## The dwell condition

`IsDwellRuns d p τ` says that the block parameterization `(p, τ)` of
`eq:schedule-parameterization` already presents the **maximal constant runs** of the schedule
(no block of zero length, no two consecutive blocks with the same mode) and that every one of
those runs lasts at least `d`. Quantifying over *all* blocks `j : Fin m` includes the initial
run `[τ_0, τ_1]` and the final run `[τ_{m-1}, τ_m]`, so the dwell requirement is imposed on
the first and last runs exactly as on the interior ones.

`IsDwellSchedule d k T W` is then "`W` has a reduced parameterization with at most `k` runs,
all of length at least `d`", and `IsGridDwellSchedule d x k W` is the same with the run
boundaries constrained to grid nodes. Passing through the reduced parameterization is what
makes the definition faithful: deleting zero-length blocks and merging equal consecutive
labels is exactly the normalization of `occupation_delete` and `occupation_merge`, and it
does not change the cumulative occupation, so "run" means maximal constant run of the
control, not "block of the chosen parameterization".

## The example

With `T = 1`, two modes, switch budget `1` (block budget `2`) and dwell `1/2`:

* `dwellInput` is pure mode one on `[0, 1/2]` and pure mode two on `[1/2, 1]`;
* `isDwellSchedule_dwellInput` and `dwellOPT_dwellInput`: the identical continuous schedule is
  dwell-feasible, so the dwell-constrained continuous optimum is `0`;
* `switchTime_eq_half`: a dwell-feasible two-run schedule on `[0, 1]` must have both runs of
  length exactly `1/2`, hence switch time `1/2`;
* `not_isGridDwellSchedule_two_runs_of_odd`: on the uniform grid `dwellGrid M` with `M` odd,
  `1/2` is not a node, so there is no dwell-feasible two-run grid schedule;
* `exists_eq_constSchedule_of_isGridDwellSchedule`: hence every dwell-feasible grid schedule is
  constant, and `D_dwellInput_constSchedule` computes the error of each constant schedule
  as `1/2`;
* `gridDwellOPT_dwellInput_odd` and `dwell_grid_gap`: the dwell-constrained grid optimum is
  `1/2` and the gap is `1/2`, for **every** odd `M`, while `cellLength_dwellGrid` shows the
  mesh is `1 / M`.

## Hypotheses

The oddness of `M` is used, and is essential: for even `M` the node `1/2` exists and the gap
is `0`. The source states it. The budget hypothesis is the block budget `2` of the source's
"one switch"; `not_isGridDwellSchedule_two_runs_of_odd` is what rules out the two-run case,
and `interval_cases` on the block count covers the remaining cases `0` and `1`.
-/

namespace GridSwitching

open Set

variable {n N : ℕ}

/-! ## Minimum dwell

The model has no dwell notion, so one is added here. It is stated on the block
parameterization, in reduced form, so that "run" means *maximal* constant run. -/

/-- The block parameterization `(p, τ)` presents the maximal constant runs of a schedule and
every run lasts at least `d`.

* `pos`: no block is degenerate, so the parameterization has no zero-length block to delete.
* `maximal`: consecutive blocks carry different modes, so no two blocks can be merged; with
  `pos` this says the blocks *are* the maximal constant runs of the control.
* `dwell`: every run lasts at least `d`. The quantifier ranges over all of `Fin m`, hence over
  the initial run `j = 0` and the final run `j = m - 1` as well as the interior ones. -/
structure IsDwellRuns (d : ℝ) {m : ℕ} (p : Fin m → Fin n) (τ : Fin (m + 1) → ℝ) : Prop where
  /-- No run is degenerate. -/
  pos : ∀ j : Fin m, τ j.castSucc < τ j.succ
  /-- Runs are maximal: consecutive blocks carry different modes. -/
  maximal : ∀ j j' : Fin m, (j' : ℕ) = (j : ℕ) + 1 → p j ≠ p j'
  /-- Every run, the initial and the final one included, lasts at least `d`. -/
  dwell : ∀ j : Fin m, d ≤ τ j.succ - τ j.castSucc

/-- A schedule satisfying minimum dwell `d` with at most `k` activation runs: its reduced
block parameterization has at most `k` blocks and every block lasts at least `d`. -/
def IsDwellSchedule (d : ℝ) (k : ℕ) (T : ℝ) (W : Fin n → ℝ → ℝ) : Prop :=
  ∃ (m : ℕ) (p : Fin m → Fin n) (τ : Fin (m + 1) → ℝ),
    m ≤ k ∧ OrderedTimes τ T ∧ IsDwellRuns d p τ ∧ W = occupation p τ

/-- A grid schedule satisfying minimum dwell `d` with at most `k` activation runs: the
run boundaries are grid nodes, as in `IsGridSchedule`, and the runs are maximal and last at
least `d`. -/
def IsGridDwellSchedule (d : ℝ) (x : Fin (N + 1) → ℝ) (k : ℕ) (W : Fin n → ℝ → ℝ) : Prop :=
  ∃ (m : ℕ) (p : Fin m → Fin n) (g : Fin (m + 1) → Fin (N + 1)),
    m ≤ k ∧ Monotone g ∧ g 0 = 0 ∧ g (Fin.last m) = Fin.last N ∧
      IsDwellRuns d p (x ∘ g) ∧ W = occupation p (x ∘ g)

/-- A dwell-feasible schedule is a cumulative allocation. -/
theorem IsDwellSchedule.isCumulative {d : ℝ} {k : ℕ} {T : ℝ} {W : Fin n → ℝ → ℝ}
    (h : IsDwellSchedule d k T W) : IsCumulative W T := by
  obtain ⟨m, p, τ, _, hτ, _, rfl⟩ := h
  exact occupation_isCumulative p hτ

/-- A dwell-feasible schedule is a schedule with the same block budget: dropping the dwell
constraint only enlarges the class. -/
theorem IsDwellSchedule.isSchedule (hn : 0 < n) {d : ℝ} {k : ℕ} {T : ℝ} {W : Fin n → ℝ → ℝ}
    (h : IsDwellSchedule d k T W) : IsSchedule k T W := by
  obtain ⟨m, p, τ, hm, hτ, _, rfl⟩ := h
  exact IsSchedule.mono hn hm ⟨p, τ, hτ, rfl⟩

/-- A dwell-feasible grid schedule is a dwell-feasible schedule. -/
theorem IsGridDwellSchedule.isDwellSchedule {d : ℝ} {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {k : ℕ} {W : Fin n → ℝ → ℝ} (h : IsGridDwellSchedule d x k W) :
    IsDwellSchedule d k T W := by
  obtain ⟨m, p, g, hm, hg, hg0, hgl, hruns, rfl⟩ := h
  refine ⟨m, p, x ∘ g, hm, ⟨?_, ?_, hx.strictMono.monotone.comp hg⟩, hruns, rfl⟩
  · simp [hg0, hx.first]
  · simp [hgl, hx.last]

/-- A dwell-feasible grid schedule is a grid schedule with the same block budget. -/
theorem IsGridDwellSchedule.isGridSchedule (hn : 0 < n) {d : ℝ} {x : Fin (N + 1) → ℝ}
    {k : ℕ} {W : Fin n → ℝ → ℝ} (h : IsGridDwellSchedule d x k W) : IsGridSchedule x k W := by
  obtain ⟨m, p, g, hm, hg, hg0, hgl, _, rfl⟩ := h
  exact IsGridSchedule.mono hn hm ⟨p, g, hg, hg0, hgl, rfl⟩

/-! ## Dwell-constrained optima -/

/-- The full errors attainable by dwell-feasible schedules with at most `k` runs. -/
def dwellScheduleErrorSet (d : ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ) (k : ℕ) : Set ℝ :=
  {e | ∃ W : Fin n → ℝ → ℝ, IsDwellSchedule d k T W ∧ e = D A W T}

/-- The full errors attainable by dwell-feasible grid schedules with at most `k` runs. -/
def gridDwellScheduleErrorSet (d : ℝ) (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ)
    (k : ℕ) : Set ℝ :=
  {e | ∃ W : Fin n → ℝ → ℝ, IsGridDwellSchedule d x k W ∧ e = D A W T}

/-- The dwell-constrained continuous instance optimum, indexed by the number of switches `s`;
the corresponding run budget is `s + 1`. -/
noncomputable def dwellOPT (d : ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ) (s : ℕ) : ℝ :=
  sInf (dwellScheduleErrorSet d A T (s + 1))

/-- The dwell-constrained grid instance optimum, indexed by the number of switches `s`. -/
noncomputable def gridDwellOPT (d : ℝ) (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ)
    (s : ℕ) : ℝ :=
  sInf (gridDwellScheduleErrorSet d x A T (s + 1))

/-- The set minimized by `dwellOPT` is bounded below by zero. -/
theorem dwellScheduleErrorSet_bddBelow (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) (d : ℝ) (k : ℕ) :
    BddBelow (dwellScheduleErrorSet d A T k) := by
  refine ⟨0, ?_⟩
  rintro e ⟨W, hW, rfl⟩
  exact D_nonneg hn hA hW.isCumulative hT

/-! ## The instance of `ex:dwell-grid-gap`

Horizon `T = 1`, two modes, switch budget `1` and dwell `1/2` for both modes. -/

/-- The word of the two-run control of `ex:dwell-grid-gap`: mode one, then mode two. -/
def dwellWord : Fin 2 → Fin 2 := ![0, 1]

/-- The run boundaries of the two-run control: the single switch happens at `1/2`. Written
as `j / 2`, these are the three points `0`, `1/2`, `1`. -/
noncomputable def dwellTimes : Fin 3 → ℝ := fun j => ((j : ℕ) : ℝ) / 2

/-- The relaxed input of `ex:dwell-grid-gap`: pure mode one before `1/2`, pure mode two
afterwards. It is bang-bang, so it coincides with the continuous schedule that switches at
`1/2`. -/
noncomputable def dwellInput : Fin 2 → ℝ → ℝ := occupation dwellWord dwellTimes

theorem orderedTimes_dwellTimes : OrderedTimes dwellTimes 1 := by
  refine ⟨by norm_num [dwellTimes], by norm_num [dwellTimes],
    Fin.monotone_iff_le_succ.mpr fun j => ?_⟩
  fin_cases j <;> norm_num [dwellTimes]

/-- The input of `ex:dwell-grid-gap` is a cumulative allocation on `[0, 1]`. -/
theorem isCumulative_dwellInput : IsCumulative dwellInput 1 :=
  occupation_isCumulative dwellWord orderedTimes_dwellTimes

theorem dwellInput_zero_apply (t : ℝ) : dwellInput 0 t = min t (1 / 2) - min t 0 := by
  norm_num [dwellInput, occupation, dwellWord, dwellTimes, Fin.sum_univ_two]

theorem dwellInput_one_apply (t : ℝ) : dwellInput 1 t = min t 1 - min t (1 / 2) := by
  norm_num [dwellInput, occupation, dwellWord, dwellTimes, Fin.sum_univ_two]

/-- Both modes of the input carry terminal mass `1/2`. -/
theorem dwellInput_horizon (i : Fin 2) : dwellInput i 1 = 1 / 2 := by
  revert i
  rw [Fin.forall_fin_two, dwellInput_zero_apply, dwellInput_one_apply]
  norm_num

/-- The three bounds on the input used to evaluate the error of a constant schedule. -/
theorem dwellInput_bounds (i : Fin 2) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) 1) :
    0 ≤ dwellInput i t ∧ dwellInput i t ≤ 1 / 2 ∧ t - 1 / 2 ≤ dwellInput i t := by
  obtain ⟨h0, h1⟩ := ht
  have hz : dwellInput 0 t = min t (1 / 2) := by
    rw [dwellInput_zero_apply, min_eq_right h0, sub_zero]
  have ho : dwellInput 1 t = t - min t (1 / 2) := by
    rw [dwellInput_one_apply, min_eq_left h1]
  revert i
  rw [Fin.forall_fin_two, hz, ho]
  rcases le_total t (1 / 2) with h | h
  · rw [min_eq_left h]
    exact ⟨⟨by linarith, by linarith, by linarith⟩, ⟨by linarith, by linarith, by linarith⟩⟩
  · rw [min_eq_right h]
    exact ⟨⟨by linarith, by linarith, by linarith⟩, ⟨by linarith, by linarith, by linarith⟩⟩

/-! ## The continuous side: dwell-feasible with error zero -/

/-- The continuous schedule that switches at `1/2` satisfies the dwell constraint `1/2` with
two runs: both runs, the initial and the final one, have length exactly `1/2`. -/
theorem isDwellRuns_dwellWord : IsDwellRuns (1 / 2) dwellWord dwellTimes := by
  refine ⟨fun j => ?_, fun j j' hj => ?_, fun j => ?_⟩
  · fin_cases j <;> norm_num [dwellTimes]
  · fin_cases j <;> fin_cases j' <;> simp_all [dwellWord]
  · fin_cases j <;> norm_num [dwellTimes]

/-- SC31, first clause: the identical continuous schedule is dwell-feasible. -/
theorem isDwellSchedule_dwellInput : IsDwellSchedule (1 / 2) 2 1 dwellInput :=
  ⟨2, dwellWord, dwellTimes, le_rfl, orderedTimes_dwellTimes, isDwellRuns_dwellWord, rfl⟩

/-- SC31, first clause: and it has error zero, being equal to the input. -/
theorem D_dwellInput_self : D dwellInput dwellInput 1 = 0 :=
  le_antisymm (D_le le_rfl fun _ _ _ => by simp)
    (D_nonneg (by norm_num) isCumulative_dwellInput isCumulative_dwellInput zero_le_one)

/-- SC31: the dwell-constrained continuous optimum with one switch is zero. -/
theorem dwellOPT_dwellInput : dwellOPT (1 / 2) dwellInput 1 1 = 0 := by
  refine le_antisymm ?_ ?_
  · refine csInf_le (dwellScheduleErrorSet_bddBelow (by norm_num) isCumulative_dwellInput
      zero_le_one _ _) ⟨dwellInput, isDwellSchedule_dwellInput, D_dwellInput_self.symm⟩
  · refine le_csInf ⟨0, dwellInput, isDwellSchedule_dwellInput, D_dwellInput_self.symm⟩ ?_
    rintro e ⟨W, hW, rfl⟩
    exact D_nonneg (by norm_num) isCumulative_dwellInput hW.isCumulative zero_le_one

/-! ## The uniform grid with `M` cells on `[0, 1]` -/

/-- The uniform grid `x_j = j / M` on the horizon `[0, 1]`. -/
noncomputable def dwellGrid (M : ℕ) : Fin (M + 1) → ℝ := fun j => ((j : ℕ) : ℝ) / M

@[simp] theorem dwellGrid_apply {M : ℕ} (j : Fin (M + 1)) :
    dwellGrid M j = ((j : ℕ) : ℝ) / M := rfl

theorem isGrid_dwellGrid {M : ℕ} (hM : 0 < M) : IsGrid (dwellGrid M) 1 := by
  have hM' : (0 : ℝ) < (M : ℝ) := by exact_mod_cast hM
  refine ⟨by simp [dwellGrid], ?_, fun a b hab => ?_⟩
  · simp [dwellGrid, div_self (ne_of_gt hM')]
  · have hlt : ((a : ℕ) : ℝ) < ((b : ℕ) : ℝ) := by exact_mod_cast Fin.lt_def.mp hab
    have := mul_lt_mul_of_pos_right hlt (inv_pos.mpr hM')
    simpa [dwellGrid, div_eq_mul_inv] using this

/-- Refinement: the grid with `M` cells has mesh `1 / M`. -/
theorem cellLength_dwellGrid {M : ℕ} (j : Fin M) : cellLength (dwellGrid M) j = 1 / M := by
  simp only [cellLength, dwellGrid, Fin.val_succ, Fin.val_castSucc]
  push_cast
  ring

/-! ## The grid side: the odd-`M` obstruction

A dwell-feasible two-run schedule would need both runs of length exactly `1/2`, so `1/2`
would have to be a grid node; on a uniform grid with an odd number of cells it is not. -/

/-- SC31, third clause, first half: on the horizon `[0, 1]` a two-run schedule with minimum
dwell `1/2` must have **both** runs of length exactly `1/2`, so its switch time is `1/2`.
Only the two dwell inequalities and the two endpoints are used. -/
theorem switchTime_eq_half {p : Fin 2 → Fin n} {τ : Fin 3 → ℝ} (h0 : τ 0 = 0) (h2 : τ 2 = 1)
    (hruns : IsDwellRuns (1 / 2) p τ) :
    τ 1 - τ 0 = 1 / 2 ∧ τ 2 - τ 1 = 1 / 2 ∧ τ 1 = 1 / 2 := by
  have d0 := hruns.dwell 0
  have d1 := hruns.dwell 1
  rw [show ((0 : Fin 2).castSucc : Fin 3) = 0 from rfl,
    show ((0 : Fin 2).succ : Fin 3) = 1 from rfl, h0] at d0
  rw [show ((1 : Fin 2).castSucc : Fin 3) = 1 from rfl,
    show ((1 : Fin 2).succ : Fin 3) = 2 from rfl, h2] at d1
  rw [h0, h2]
  exact ⟨by linarith, by linarith, by linarith⟩

/-- SC31, third clause: with an odd number of cells there is no dwell-feasible two-run grid
schedule. The dwell constraint forces the single interior node to be `1/2`, which would make
the number of cells even. -/
theorem not_isGridDwellSchedule_two_runs_of_odd {M : ℕ} (hM : Odd M) (p : Fin 2 → Fin n)
    (g : Fin 3 → Fin (M + 1)) (hg0 : g 0 = 0) (hgl : g (Fin.last 2) = Fin.last M) :
    ¬ IsDwellRuns (1 / 2) p (dwellGrid M ∘ g) := by
  intro hruns
  have hMpos : 0 < M := hM.pos
  have hM' : (0 : ℝ) < (M : ℝ) := by exact_mod_cast hMpos
  have h0 : (dwellGrid M ∘ g) 0 = 0 := by simp [hg0]
  have h2 : (dwellGrid M ∘ g) 2 = 1 := by
    have hlast : (Fin.last 2 : Fin 3) = 2 := rfl
    rw [hlast] at hgl
    simp [hgl, dwellGrid, div_self (ne_of_gt hM')]
  obtain ⟨-, -, hhalf⟩ := switchTime_eq_half h0 h2 hruns
  have hval : ((g 1 : ℕ) : ℝ) / M = 1 / 2 := hhalf
  have hnat : 2 * (g 1 : ℕ) = M := by
    have : 2 * ((g 1 : ℕ) : ℝ) = (M : ℝ) := by
      field_simp at hval
      linarith
    exact_mod_cast this
  exact (Nat.not_odd_iff_even.mpr ⟨(g 1 : ℕ), by omega⟩) hM

/-- SC31, fourth clause: with an odd number of cells the only dwell-feasible grid schedules
with at most two runs are the constant ones. -/
theorem exists_eq_constSchedule_of_isGridDwellSchedule {M : ℕ} (hM : Odd M)
    {W : Fin n → ℝ → ℝ} (hW : IsGridDwellSchedule (1 / 2) (dwellGrid M) 2 W) :
    ∃ q : Fin n, W = constSchedule q 1 := by
  have hMpos : 0 < M := hM.pos
  have hM' : (0 : ℝ) < (M : ℝ) := by exact_mod_cast hMpos
  obtain ⟨m, p, g, hm, hg, hg0, hgl, hruns, rfl⟩ := hW
  interval_cases m
  · exfalso
    have h : (Fin.last M : Fin (M + 1)) = 0 := by
      rw [← hgl, show (Fin.last 0 : Fin (0 + 1)) = 0 by decide, hg0]
    have := congrArg Fin.val h
    simp at this
    omega
  · refine ⟨p 0, ?_⟩
    have hp : p = fun _ : Fin 1 => p 0 := by funext j; fin_cases j; rfl
    have hτ : (dwellGrid M ∘ g) = ![0, 1] := by
      have hgl' : g 1 = Fin.last M := by
        rw [← hgl]; rfl
      funext j
      fin_cases j
      · simp [Function.comp_apply, hg0]
      · simp [Function.comp_apply, hgl', dwellGrid, div_self (ne_of_gt hM')]
    rw [hτ, constSchedule]
    exact congrArg (fun r => occupation r ![(0 : ℝ), 1]) hp
  · exact absurd hruns (not_isGridDwellSchedule_two_runs_of_odd hM p g hg0 hgl)

/-- Every constant schedule is dwell-feasible on every uniform grid: it has a single run,
of length `1 ≥ 1/2`. -/
theorem isGridDwellSchedule_constSchedule {M : ℕ} (hM : 0 < M) (q : Fin n) :
    IsGridDwellSchedule (1 / 2) (dwellGrid M) 2 (constSchedule q 1) := by
  have hM' : (0 : ℝ) < (M : ℝ) := by exact_mod_cast hM
  refine ⟨1, fun _ => q, ![0, Fin.last M], by norm_num, ?_, rfl, rfl, ⟨?_, ?_, ?_⟩, ?_⟩
  · refine Fin.monotone_iff_le_succ.mpr fun j => ?_
    fin_cases j
    simp
  · intro j
    fin_cases j
    norm_num [dwellGrid, div_self (ne_of_gt hM')]
  · intro j j' hj
    have h1 : (j : ℕ) < 1 := j.isLt
    have h2 : (j' : ℕ) < 1 := j'.isLt
    exfalso
    omega
  · intro j
    fin_cases j
    norm_num [dwellGrid, div_self (ne_of_gt hM')]
  · have hτ : (dwellGrid M ∘ ![(0 : Fin (M + 1)), Fin.last M]) = ![0, 1] := by
      funext j
      fin_cases j
      · simp [dwellGrid]
      · simp [dwellGrid, div_self (ne_of_gt hM')]
    rw [hτ, constSchedule]

/-- SC31, fourth clause: the error of a constant schedule against the input is `1/2`, for
either mode. -/
theorem D_dwellInput_constSchedule (q : Fin 2) : D dwellInput (constSchedule q 1) 1 = 1 / 2 := by
  have hW : IsCumulative (constSchedule q 1) 1 :=
    (isSchedule_constSchedule zero_le_one q).isCumulative
  refine le_antisymm (D_le (by norm_num) fun i t ht => ?_) ?_
  · obtain ⟨hb0, hb1, hb2⟩ := dwellInput_bounds i ht
    rcases eq_or_ne q i with rfl | hqi
    · rw [constSchedule_apply_self q ht]
      have h1 : dwellInput q t ≤ t := isCumulative_dwellInput.le_self q ht
      rw [abs_of_nonpos (by linarith)]
      linarith
    · rw [constSchedule_apply_ne hqi, sub_zero, abs_of_nonneg hb0]
      exact hb1
  · have hex : ∃ i : Fin 2, q ≠ i := by
      fin_cases q
      · exact ⟨1, by decide⟩
      · exact ⟨0, by decide⟩
    obtain ⟨i, hqi⟩ := hex
    have h := le_D isCumulative_dwellInput hW i (show (1 : ℝ) ∈ Icc (0 : ℝ) 1 from
      ⟨zero_le_one, le_rfl⟩)
    rwa [constSchedule_apply_ne hqi, sub_zero, dwellInput_horizon i,
      abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 1 / 2)] at h

/-- SC31, fourth clause: on an odd uniform grid the dwell-feasible errors form the single
point `1/2`. -/
theorem gridDwellScheduleErrorSet_odd {M : ℕ} (hM : Odd M) :
    gridDwellScheduleErrorSet (1 / 2) (dwellGrid M) dwellInput 1 2 = {1 / 2} := by
  ext e
  constructor
  · rintro ⟨W, hW, rfl⟩
    obtain ⟨q, rfl⟩ := exists_eq_constSchedule_of_isGridDwellSchedule hM hW
    exact D_dwellInput_constSchedule q
  · rintro rfl
    exact ⟨constSchedule 0 1, isGridDwellSchedule_constSchedule hM.pos 0,
      (D_dwellInput_constSchedule 0).symm⟩

/-- SC31: on every uniform grid with an odd number of cells the dwell-constrained grid
optimum with one switch is `1/2`. -/
theorem gridDwellOPT_dwellInput_odd {M : ℕ} (hM : Odd M) :
    gridDwellOPT (1 / 2) (dwellGrid M) dwellInput 1 1 = 1 / 2 := by
  rw [gridDwellOPT, gridDwellScheduleErrorSet_odd hM, csInf_singleton]

/-- SC31, the conclusion of `ex:dwell-grid-gap`: for **every** odd number of cells `M` the
dwell-constrained gap between the grid optimum and the continuous optimum equals `1/2`,
while the mesh `1 / M` of the grid tends to zero. The gap therefore does not vanish under
refinement.

**Scope, as the source states it.** This is a failure of an unrestricted transfer conclusion
*for dwell-constrained optima*, not merely a limitation of one construction: the obstruction
is the arithmetic of the grid, and it recurs on every uniform grid with an odd number of
cells, however fine. It is consistent with the package's transfer theorems, which are
switch-preserving and say nothing about dwell: `Formal.GridSwitching.UniformTransfer`
(SC24, `thm:sharp-transfer`) and the two-mode arbitrary-grid statement (SC27,
`prop:binary-transfer`) both transfer a schedule by *moving block boundaries to grid nodes*,
an operation that shortens runs and can delete them altogether, so neither preserves a
minimum dwell constraint. -/
theorem dwell_grid_gap {M : ℕ} (hM : Odd M) :
    gridDwellOPT (1 / 2) (dwellGrid M) dwellInput 1 1 - dwellOPT (1 / 2) dwellInput 1 1
      = 1 / 2 := by
  rw [gridDwellOPT_dwellInput_odd hM, dwellOPT_dwellInput, sub_zero]

end GridSwitching
