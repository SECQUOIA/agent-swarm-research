import Mathlib
import Formal.GridSwitching.Model
import Formal.GridSwitching.Endpoint

/-!
# Compactness, Lipschitz stability, scaling, and the no-switch value

This module discharges the obligations SC07, SC08 and SC09 of
`topics/17-grid-switching/CLAIMS.md` for the model of `Formal.GridSwitching.Model`.

* SC07 (`prop:compactness`). The error functionals are maxima, not merely suprema
  (`exists_D_eq`, `isGreatest_errorSet`, `exists_Dminus_eq`, `isGreatest_lowerErrorSet`); each
  of the four instance optima is `1`-Lipschitz in the input (`abs_OPT_sub_OPT_le` and its
  three companions); every instance optimum is attained (`exists_OPT_eq`, `exists_OPTminus_eq`,
  `exists_gridOPT_eq`, `exists_gridOPTminus_eq`); and every minimax value is attained
  (`exists_gridF_eq`, `exists_gridGminus_eq`, `exists_F_eq`, `exists_Gminus_eq`).

  Three different compactness arguments appear. The grid schedule class is finite
  (`gridScheduleErrorSet_finite`). The continuous schedule class is a finite union over words
  of continuous images of the compact ordered-time simplex (`isCompact_orderedTimesSet`), using
  the explicit `min` representation of `eq:schedule-parameterization` through
  `abs_occupation_sub_occupation_le`. The grid input class is parameterized by the compact set
  of rate matrices (`isCompact_rateMatrixSet`), and the continuous input class is compact in
  the uniform norm by Arzelà–Ascoli (`isCompact_bcfCumulativeSet`).

  The two uniform-norm compactness statements of `prop:compactness` itself are
  `isCompact_bcfCumulativeSet` for `Acal_n(T)` and `isCompact_bcfScheduleSet` for
  `Wcal_{n,k}(T)`, both inside the bounded continuous maps on the compact horizon.

* SC08 (`eq:scaling`). `F n s 0 = 0` (`F_horizon_zero`), `F n s T = T * F n s 1` for `T > 0`
  (`F_scaling`, from the change of variables `rescale`), the one-sided analogues
  (`Gminus_horizon_zero`, `Gminus_scaling`), and budget monotonicity for all eight optima and
  minimax values (`OPT_mono_budget` and companions).

* SC09 (`prop:no-switch`). `F n 0 T = T (1 - 1/n)` (`F_no_switch`) and the same value on every
  grid (`gridF_no_switch`).
-/

namespace GridSwitching

open Set

open scoped NNReal

open scoped BoundedContinuousFunction

variable {n N : ℕ}

/-! ## SC07, step 1: the error functionals are maxima -/

/-- A cumulative allocation is `1`-Lipschitz on the horizon. -/
theorem abs_sub_le_of_isCumulative {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (i : Fin n) {s t : ℝ} (hs : s ∈ Icc (0 : ℝ) T) (ht : t ∈ Icc (0 : ℝ) T) :
    |A i s - A i t| ≤ |s - t| := by
  rcases le_total s t with h | h
  · have h1 := hA.mono i s t hs.1 h ht.2
    have h2 := hA.lipschitz i s t hs.1 h ht.2
    rw [abs_sub_comm s t, abs_of_nonneg (sub_nonneg.mpr h), abs_le]
    constructor <;> linarith
  · have h1 := hA.mono i t s ht.1 h hs.2
    have h2 := hA.lipschitz i t s ht.1 h hs.2
    rw [abs_of_nonneg (sub_nonneg.mpr h), abs_le]
    constructor <;> linarith

/-- Each coordinate of a cumulative allocation is continuous on the horizon. -/
theorem continuousOn_of_isCumulative {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (i : Fin n) : ContinuousOn (A i) (Icc 0 T) := by
  refine LipschitzOnWith.continuousOn (K := 1) (LipschitzOnWith.of_dist_le_mul ?_)
  intro s hs t ht
  simpa [Real.dist_eq] using abs_sub_le_of_isCumulative hA i hs ht

/-- The error set of two cumulative allocations is compact: it is a finite union of continuous
images of the compact horizon. -/
theorem isCompact_errorSet {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) : IsCompact (errorSet A W T) := by
  have h : errorSet A W T = ⋃ i : Fin n, (fun t => |A i t - W i t|) '' Icc (0 : ℝ) T := by
    ext e
    simp only [errorSet, mem_ofPred_eq, mem_iUnion, mem_image]
    exact ⟨fun ⟨i, t, ht, he⟩ => ⟨i, t, ht, he.symm⟩, fun ⟨i, t, ht, he⟩ => ⟨i, t, ht, he.symm⟩⟩
  rw [h]
  exact isCompact_iUnion fun i => isCompact_Icc.image_of_continuousOn
    (((continuousOn_of_isCumulative hA i).sub (continuousOn_of_isCumulative hW i)).abs)

/-- The one-sided error set of two cumulative allocations is compact. -/
theorem isCompact_lowerErrorSet {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) : IsCompact (lowerErrorSet A W T) := by
  have h : lowerErrorSet A W T = ⋃ i : Fin n, (fun t => W i t - A i t) '' Icc (0 : ℝ) T := by
    ext e
    simp only [lowerErrorSet, mem_ofPred_eq, mem_iUnion, mem_image]
    exact ⟨fun ⟨i, t, ht, he⟩ => ⟨i, t, ht, he.symm⟩, fun ⟨i, t, ht, he⟩ => ⟨i, t, ht, he.symm⟩⟩
  rw [h]
  exact isCompact_iUnion fun i => isCompact_Icc.image_of_continuousOn
    ((continuousOn_of_isCumulative hW i).sub (continuousOn_of_isCumulative hA i))

/-- SC07, attainment of the full error: `D` is a maximum, reached at some mode and time. -/
theorem exists_D_eq (hn : 0 < n) {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) (hT : 0 ≤ T) :
    ∃ i : Fin n, ∃ t ∈ Icc (0 : ℝ) T, D A W T = |A i t - W i t| :=
  (isCompact_errorSet hA hW).sSup_mem (errorSet_nonempty hn hT)

/-- SC07: `D A W T` is the greatest element of the error set, not merely its supremum. -/
theorem isGreatest_errorSet (hn : 0 < n) {A W : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hW : IsCumulative W T) (hT : 0 ≤ T) :
    IsGreatest (errorSet A W T) (D A W T) :=
  ⟨exists_D_eq hn hA hW hT, fun _ he => le_csSup (errorSet_bddAbove hA hW) he⟩

/-- SC07, attainment of the one-sided error: `Dminus` is a maximum. -/
theorem exists_Dminus_eq (hn : 0 < n) {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) (hT : 0 ≤ T) :
    ∃ i : Fin n, ∃ t ∈ Icc (0 : ℝ) T, Dminus A W T = W i t - A i t :=
  (isCompact_lowerErrorSet hA hW).sSup_mem
    ⟨0, zero_mem_lowerErrorSet hn hA hW hT⟩

/-- SC07: `Dminus A W T` is the greatest element of the one-sided error set. -/
theorem isGreatest_lowerErrorSet (hn : 0 < n) {A W : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hW : IsCumulative W T) (hT : 0 ≤ T) :
    IsGreatest (lowerErrorSet A W T) (Dminus A W T) :=
  ⟨exists_Dminus_eq hn hA hW hT, fun _ he => le_csSup (lowerErrorSet_bddAbove hA hW) he⟩

/-! ## SC07, step 2: Lipschitz dependence on the input and on the schedule

The four instance optima are `1`-Lipschitz in the input, in the sense that a uniform
perturbation of the input by `δ` moves each optimum by at most `δ`. The proofs all factor
through the corresponding statement for a single error functional. -/

/-- Perturbing the input uniformly by `δ` raises the full error by at most `δ`. -/
theorem D_le_D_add_input (hn : 0 < n) {A B W : Fin n → ℝ → ℝ} {T δ : ℝ}
    (hB : IsCumulative B T) (hW : IsCumulative W T) (hT : 0 ≤ T)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |A i t - B i t| ≤ δ) :
    D A W T ≤ D B W T + δ := by
  have hδ : 0 ≤ δ := le_trans (abs_nonneg _) (h ⟨0, hn⟩ 0 ⟨le_rfl, hT⟩)
  refine D_le (by linarith [D_nonneg hn hB hW hT]) fun i t ht => ?_
  calc |A i t - W i t| ≤ |A i t - B i t| + |B i t - W i t| := abs_sub_le _ _ _
    _ ≤ δ + D B W T := add_le_add (h i t ht) (le_D hB hW i ht)
    _ = D B W T + δ := by ring

/-- Perturbing the schedule uniformly by `δ` raises the full error by at most `δ`. -/
theorem D_le_D_add_schedule (hn : 0 < n) {A W V : Fin n → ℝ → ℝ} {T δ : ℝ}
    (hA : IsCumulative A T) (hV : IsCumulative V T) (hT : 0 ≤ T)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |W i t - V i t| ≤ δ) :
    D A W T ≤ D A V T + δ := by
  have hδ : 0 ≤ δ := le_trans (abs_nonneg _) (h ⟨0, hn⟩ 0 ⟨le_rfl, hT⟩)
  refine D_le (by linarith [D_nonneg hn hA hV hT]) fun i t ht => ?_
  have hcomm : |V i t - W i t| = |W i t - V i t| := abs_sub_comm _ _
  calc |A i t - W i t| ≤ |A i t - V i t| + |V i t - W i t| := abs_sub_le _ _ _
    _ ≤ D A V T + δ := add_le_add (le_D hA hV i ht) (hcomm ▸ h i t ht)

/-- Perturbing the input uniformly by `δ` raises the one-sided error by at most `δ`. -/
theorem Dminus_le_Dminus_add_input (hn : 0 < n) {A B W : Fin n → ℝ → ℝ} {T δ : ℝ}
    (hB : IsCumulative B T) (hW : IsCumulative W T) (hT : 0 ≤ T)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |A i t - B i t| ≤ δ) :
    Dminus A W T ≤ Dminus B W T + δ := by
  have hδ : 0 ≤ δ := le_trans (abs_nonneg _) (h ⟨0, hn⟩ 0 ⟨le_rfl, hT⟩)
  refine Real.sSup_le (fun e he => ?_) (by linarith [Dminus_nonneg hn hB hW hT])
  obtain ⟨i, t, ht, rfl⟩ := he
  have h1 : W i t - B i t ≤ Dminus B W T := le_csSup (lowerErrorSet_bddAbove hB hW) ⟨i, t, ht, rfl⟩
  have h2 := abs_le.mp (h i t ht)
  linarith [h2.1]

/-- Perturbing the schedule uniformly by `δ` raises the one-sided error by at most `δ`. -/
theorem Dminus_le_Dminus_add_schedule (hn : 0 < n) {A W V : Fin n → ℝ → ℝ} {T δ : ℝ}
    (hA : IsCumulative A T) (hV : IsCumulative V T) (hT : 0 ≤ T)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |W i t - V i t| ≤ δ) :
    Dminus A W T ≤ Dminus A V T + δ := by
  have hδ : 0 ≤ δ := le_trans (abs_nonneg _) (h ⟨0, hn⟩ 0 ⟨le_rfl, hT⟩)
  refine Real.sSup_le (fun e he => ?_) (by linarith [Dminus_nonneg hn hA hV hT])
  obtain ⟨i, t, ht, rfl⟩ := he
  have h1 : V i t - A i t ≤ Dminus A V T := le_csSup (lowerErrorSet_bddAbove hA hV) ⟨i, t, ht, rfl⟩
  have h2 : W i t - V i t ≤ δ := (abs_le.mp (h i t ht)).2
  linarith

/-! ### The optimum sets are bounded below and nonempty -/

/-- The set minimized by `OPT` is bounded below by zero. -/
theorem scheduleErrorSet_bddBelow (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) (k : ℕ) : BddBelow (scheduleErrorSet A T k) := by
  refine ⟨0, ?_⟩
  rintro e ⟨W, hW, rfl⟩
  exact D_nonneg hn hA hW.isCumulative hT

/-- The set minimized by `OPTminus` is bounded below by zero. -/
theorem scheduleLowerErrorSet_bddBelow (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) (k : ℕ) :
    BddBelow (scheduleLowerErrorSet A T k) := by
  refine ⟨0, ?_⟩
  rintro e ⟨W, hW, rfl⟩
  exact Dminus_nonneg hn hA hW.isCumulative hT

/-- The set minimized by `OPTminus` is nonempty for every positive block budget. -/
theorem scheduleLowerErrorSet_nonempty (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ} (hT : 0 ≤ T)
    {k : ℕ} (hk : 0 < k) : (scheduleLowerErrorSet A T k).Nonempty := by
  obtain ⟨W, hW⟩ := exists_isSchedule hn hT hk
  exact ⟨Dminus A W T, W, hW, rfl⟩

/-- The set minimized by `gridOPT` is nonempty for every positive block budget. -/
theorem gridScheduleErrorSet_nonempty (hn : 0 < n) {x : Fin (N + 1) → ℝ}
    (A : Fin n → ℝ → ℝ) (T : ℝ) {k : ℕ} (hk : 0 < k) :
    (gridScheduleErrorSet x A T k).Nonempty := by
  obtain ⟨W, hW⟩ := exists_isGridSchedule hn x hk
  exact ⟨D A W T, W, hW, rfl⟩

/-- The set minimized by `gridOPTminus` is nonempty for every positive block budget. -/
theorem gridScheduleLowerErrorSet_nonempty (hn : 0 < n) {x : Fin (N + 1) → ℝ}
    (A : Fin n → ℝ → ℝ) (T : ℝ) {k : ℕ} (hk : 0 < k) :
    (gridScheduleLowerErrorSet x A T k).Nonempty := by
  obtain ⟨W, hW⟩ := exists_isGridSchedule hn x hk
  exact ⟨Dminus A W T, W, hW, rfl⟩

/-- The set minimized by `gridOPT` is bounded below by zero. -/
theorem gridScheduleErrorSet_bddBelow (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T) (k : ℕ) :
    BddBelow (gridScheduleErrorSet x A T k) := by
  refine ⟨0, ?_⟩
  rintro e ⟨W, hW, rfl⟩
  exact D_nonneg hn hA (hW.isSchedule hx).isCumulative hT

/-- The set minimized by `gridOPTminus` is bounded below by zero. -/
theorem gridScheduleLowerErrorSet_bddBelow (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T) (k : ℕ) :
    BddBelow (gridScheduleLowerErrorSet x A T k) := by
  refine ⟨0, ?_⟩
  rintro e ⟨W, hW, rfl⟩
  exact Dminus_nonneg hn hA (hW.isSchedule hx).isCumulative hT

/-! ### The four instance optima are `1`-Lipschitz in the input -/

/-- SC07: the continuous instance optimum is `1`-Lipschitz in the input, one-sided form. -/
theorem OPT_le_OPT_add (hn : 0 < n) {A B : Fin n → ℝ → ℝ} {T δ : ℝ}
    (hA : IsCumulative A T) (hB : IsCumulative B T) (hT : 0 ≤ T) (s : ℕ)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |A i t - B i t| ≤ δ) :
    OPT A T s ≤ OPT B T s + δ := by
  have key : OPT A T s - δ ≤ OPT B T s := by
    refine le_csInf (scheduleErrorSet_nonempty hn hT (Nat.succ_pos s)) ?_
    rintro e ⟨W, hW, rfl⟩
    have h1 : OPT A T s ≤ D A W T :=
      csInf_le (scheduleErrorSet_bddBelow hn hA hT _) ⟨W, hW, rfl⟩
    have h2 : D A W T ≤ D B W T + δ := D_le_D_add_input hn hB hW.isCumulative hT h
    linarith
  linarith

/-- SC07: the continuous instance optimum is `1`-Lipschitz in the input. -/
theorem abs_OPT_sub_OPT_le (hn : 0 < n) {A B : Fin n → ℝ → ℝ} {T δ : ℝ}
    (hA : IsCumulative A T) (hB : IsCumulative B T) (hT : 0 ≤ T) (s : ℕ)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |A i t - B i t| ≤ δ) :
    |OPT A T s - OPT B T s| ≤ δ := by
  have h' : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |B i t - A i t| ≤ δ := fun i t ht => by
    rw [abs_sub_comm]; exact h i t ht
  rw [abs_sub_le_iff]
  exact ⟨by linarith [OPT_le_OPT_add hn hA hB hT s h],
    by linarith [OPT_le_OPT_add hn hB hA hT s h']⟩

/-- SC07: the one-sided continuous instance optimum is `1`-Lipschitz in the input. -/
theorem OPTminus_le_OPTminus_add (hn : 0 < n) {A B : Fin n → ℝ → ℝ} {T δ : ℝ}
    (hA : IsCumulative A T) (hB : IsCumulative B T) (hT : 0 ≤ T) {k : ℕ} (hk : 0 < k)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |A i t - B i t| ≤ δ) :
    OPTminus A T k ≤ OPTminus B T k + δ := by
  have key : OPTminus A T k - δ ≤ OPTminus B T k := by
    refine le_csInf (scheduleLowerErrorSet_nonempty hn hT hk) ?_
    rintro e ⟨W, hW, rfl⟩
    have h1 : OPTminus A T k ≤ Dminus A W T :=
      csInf_le (scheduleLowerErrorSet_bddBelow hn hA hT _) ⟨W, hW, rfl⟩
    have h2 : Dminus A W T ≤ Dminus B W T + δ :=
      Dminus_le_Dminus_add_input hn hB hW.isCumulative hT h
    linarith
  linarith

/-- SC07: the one-sided continuous instance optimum is `1`-Lipschitz in the input. -/
theorem abs_OPTminus_sub_OPTminus_le (hn : 0 < n) {A B : Fin n → ℝ → ℝ} {T δ : ℝ}
    (hA : IsCumulative A T) (hB : IsCumulative B T) (hT : 0 ≤ T) {k : ℕ} (hk : 0 < k)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |A i t - B i t| ≤ δ) :
    |OPTminus A T k - OPTminus B T k| ≤ δ := by
  have h' : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |B i t - A i t| ≤ δ := fun i t ht => by
    rw [abs_sub_comm]; exact h i t ht
  rw [abs_sub_le_iff]
  exact ⟨by linarith [OPTminus_le_OPTminus_add hn hA hB hT hk h],
    by linarith [OPTminus_le_OPTminus_add hn hB hA hT hk h']⟩

/-- SC07: the grid instance optimum is `1`-Lipschitz in the input, one-sided form. -/
theorem gridOPT_le_gridOPT_add (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {A B : Fin n → ℝ → ℝ} {δ : ℝ} (hA : IsCumulative A T) (hB : IsCumulative B T)
    (hT : 0 ≤ T) (s : ℕ)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |A i t - B i t| ≤ δ) :
    gridOPT x A T s ≤ gridOPT x B T s + δ := by
  have key : gridOPT x A T s - δ ≤ gridOPT x B T s := by
    refine le_csInf (gridScheduleErrorSet_nonempty hn B T (Nat.succ_pos s)) ?_
    rintro e ⟨W, hW, rfl⟩
    have h1 : gridOPT x A T s ≤ D A W T :=
      csInf_le (gridScheduleErrorSet_bddBelow hn hx hA hT _) ⟨W, hW, rfl⟩
    have h2 : D A W T ≤ D B W T + δ :=
      D_le_D_add_input hn hB (hW.isSchedule hx).isCumulative hT h
    linarith
  linarith

/-- SC07: the grid instance optimum is `1`-Lipschitz in the input. -/
theorem abs_gridOPT_sub_gridOPT_le (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A B : Fin n → ℝ → ℝ} {δ : ℝ} (hA : IsCumulative A T)
    (hB : IsCumulative B T) (hT : 0 ≤ T) (s : ℕ)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |A i t - B i t| ≤ δ) :
    |gridOPT x A T s - gridOPT x B T s| ≤ δ := by
  have h' : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |B i t - A i t| ≤ δ := fun i t ht => by
    rw [abs_sub_comm]; exact h i t ht
  rw [abs_sub_le_iff]
  exact ⟨by linarith [gridOPT_le_gridOPT_add hn hx hA hB hT s h],
    by linarith [gridOPT_le_gridOPT_add hn hx hB hA hT s h']⟩

/-- SC07: the one-sided grid instance optimum is `1`-Lipschitz in the input, one-sided form. -/
theorem gridOPTminus_le_gridOPTminus_add (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A B : Fin n → ℝ → ℝ} {δ : ℝ} (hA : IsCumulative A T)
    (hB : IsCumulative B T) (hT : 0 ≤ T) {k : ℕ} (hk : 0 < k)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |A i t - B i t| ≤ δ) :
    gridOPTminus x A T k ≤ gridOPTminus x B T k + δ := by
  have key : gridOPTminus x A T k - δ ≤ gridOPTminus x B T k := by
    refine le_csInf (gridScheduleLowerErrorSet_nonempty hn B T hk) ?_
    rintro e ⟨W, hW, rfl⟩
    have h1 : gridOPTminus x A T k ≤ Dminus A W T :=
      csInf_le (gridScheduleLowerErrorSet_bddBelow hn hx hA hT _) ⟨W, hW, rfl⟩
    have h2 : Dminus A W T ≤ Dminus B W T + δ :=
      Dminus_le_Dminus_add_input hn hB (hW.isSchedule hx).isCumulative hT h
    linarith
  linarith

/-- SC07: the one-sided grid instance optimum is `1`-Lipschitz in the input. -/
theorem abs_gridOPTminus_sub_gridOPTminus_le (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A B : Fin n → ℝ → ℝ} {δ : ℝ} (hA : IsCumulative A T)
    (hB : IsCumulative B T) (hT : 0 ≤ T) {k : ℕ} (hk : 0 < k)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |A i t - B i t| ≤ δ) :
    |gridOPTminus x A T k - gridOPTminus x B T k| ≤ δ := by
  have h' : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |B i t - A i t| ≤ δ := fun i t ht => by
    rw [abs_sub_comm]; exact h i t ht
  rw [abs_sub_le_iff]
  exact ⟨by linarith [gridOPTminus_le_gridOPTminus_add hn hx hA hB hT hk h],
    by linarith [gridOPTminus_le_gridOPTminus_add hn hx hB hA hT hk h']⟩

/-! ## SC07, step 3: attainment of the instance optima

The grid case is finite: there are only finitely many grid schedules, so the infimum is over
a finite nonempty set of reals. The continuous case goes through the compact ordered-time
simplex of `eq:schedule-parameterization`. -/

/-- There are only finitely many grid schedules, so the set minimized by `gridOPT` is finite. -/
theorem gridScheduleErrorSet_finite (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ)
    (k : ℕ) : (gridScheduleErrorSet x A T k).Finite := by
  refine Set.Finite.subset (Set.finite_range
    (fun pg : (Fin k → Fin n) × (Fin (k + 1) → Fin (N + 1)) =>
      D A (occupation pg.1 (x ∘ pg.2)) T)) ?_
  rintro e ⟨W, ⟨p, g, -, -, -, rfl⟩, rfl⟩
  exact ⟨(p, g), rfl⟩

/-- There are only finitely many grid schedules, so the set minimized by `gridOPTminus` is
finite. -/
theorem gridScheduleLowerErrorSet_finite (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ)
    (k : ℕ) : (gridScheduleLowerErrorSet x A T k).Finite := by
  refine Set.Finite.subset (Set.finite_range
    (fun pg : (Fin k → Fin n) × (Fin (k + 1) → Fin (N + 1)) =>
      Dminus A (occupation pg.1 (x ∘ pg.2)) T)) ?_
  rintro e ⟨W, ⟨p, g, -, -, -, rfl⟩, rfl⟩
  exact ⟨(p, g), rfl⟩

/-- SC07: the grid instance optimum is attained by a grid schedule. No hypothesis on the input
is needed, matching the grid asymmetry of `eq:grid-definitions`. -/
theorem exists_gridOPT_eq (hn : 0 < n) (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ)
    (s : ℕ) : ∃ W : Fin n → ℝ → ℝ, IsGridSchedule x (s + 1) W ∧ gridOPT x A T s = D A W T :=
  (gridScheduleErrorSet_nonempty hn A T (Nat.succ_pos s)).csInf_mem
    (gridScheduleErrorSet_finite x A T (s + 1))

/-- SC07: the one-sided grid instance optimum is attained by a grid schedule. -/
theorem exists_gridOPTminus_eq (hn : 0 < n) (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ)
    {k : ℕ} (hk : 0 < k) :
    ∃ W : Fin n → ℝ → ℝ, IsGridSchedule x k W ∧ gridOPTminus x A T k = Dminus A W T :=
  (gridScheduleLowerErrorSet_nonempty hn A T hk).csInf_mem
    (gridScheduleLowerErrorSet_finite x A T k)

/-! ### The ordered-time simplex is compact -/

/-- The ordered switch times of `eq:schedule-parameterization` for a block budget `k`, viewed
as a subset of `Fin (k + 1) → ℝ`. -/
def orderedTimesSet (k : ℕ) (T : ℝ) : Set (Fin (k + 1) → ℝ) := {τ | OrderedTimes τ T}

@[simp] theorem mem_orderedTimesSet {k : ℕ} {T : ℝ} {τ : Fin (k + 1) → ℝ} :
    τ ∈ orderedTimesSet k T ↔ OrderedTimes τ T := Iff.rfl

/-- The ordered-time simplex is compact: it is a closed subset of a product of intervals. -/
theorem isCompact_orderedTimesSet (k : ℕ) (T : ℝ) : IsCompact (orderedTimesSet k T) := by
  have hsub : orderedTimesSet k T ⊆ Set.univ.pi fun _ : Fin (k + 1) => Icc (0 : ℝ) T := by
    intro τ hτ m _
    exact ⟨hτ.nonneg m, hτ.last ▸ hτ.mono (Fin.le_last m)⟩
  refine IsCompact.of_isClosed_subset (isCompact_univ_pi fun _ => isCompact_Icc) ?_ hsub
  have hset : orderedTimesSet k T =
      ({τ : Fin (k + 1) → ℝ | τ 0 = 0} ∩ {τ : Fin (k + 1) → ℝ | τ (Fin.last k) = T}) ∩
        ⋂ j : Fin k, {τ : Fin (k + 1) → ℝ | τ j.castSucc ≤ τ j.succ} := by
    ext τ
    simp only [mem_orderedTimesSet, mem_inter_iff, mem_ofPred_eq, mem_iInter]
    refine ⟨fun hτ => ⟨⟨hτ.first, hτ.last⟩, fun j => hτ.mono (Fin.castSucc_le_succ j)⟩, ?_⟩
    rintro ⟨⟨h0, hl⟩, hm⟩
    exact ⟨h0, hl, Fin.monotone_iff_le_succ.mpr hm⟩
  rw [hset]
  refine IsClosed.inter (IsClosed.inter ?_ ?_) (isClosed_iInter fun j => ?_)
  · exact isClosed_eq (continuous_apply 0) continuous_const
  · exact isClosed_eq (continuous_apply _) continuous_const
  · exact isClosed_le (continuous_apply _) (continuous_apply _)

/-! ### The cumulative occupation is Lipschitz in the switch times -/

/-- Abel summation bound. A telescoped family weighted by coefficients in `[0, 1]` is
controlled by the sum of the absolute values of the telescoped family: the two shifted
coefficient families `Fin.cons 0 c` and `Fin.snoc c 0` differ by at most one at every
index. -/
private theorem abs_sum_coeff_telescope_le {k : ℕ} (c : Fin k → ℝ)
    (hc0 : ∀ j, 0 ≤ c j) (hc1 : ∀ j, c j ≤ 1) (d : Fin (k + 1) → ℝ) :
    |∑ j : Fin k, c j * (d j.succ - d j.castSucc)| ≤ ∑ m : Fin (k + 1), |d m| := by
  have hasum : ∑ m : Fin (k + 1), (Fin.cons 0 c : Fin (k + 1) → ℝ) m * d m
      = ∑ j : Fin k, c j * d j.succ := by
    rw [Fin.sum_univ_succ]; simp
  have hbsum : ∑ m : Fin (k + 1), (Fin.snoc c 0 : Fin (k + 1) → ℝ) m * d m
      = ∑ j : Fin k, c j * d j.castSucc := by
    rw [Fin.sum_univ_castSucc]; simp
  have ha01 : ∀ m, 0 ≤ (Fin.cons 0 c : Fin (k + 1) → ℝ) m ∧
      (Fin.cons 0 c : Fin (k + 1) → ℝ) m ≤ 1 := by
    intro m
    refine Fin.cases ?_ ?_ m
    · simp
    · intro j; simpa using ⟨hc0 j, hc1 j⟩
  have hb01 : ∀ m, 0 ≤ (Fin.snoc c 0 : Fin (k + 1) → ℝ) m ∧
      (Fin.snoc c 0 : Fin (k + 1) → ℝ) m ≤ 1 := by
    intro m
    refine Fin.lastCases ?_ ?_ m
    · simp
    · intro j; simpa using ⟨hc0 j, hc1 j⟩
  have hrw : ∑ j : Fin k, c j * (d j.succ - d j.castSucc)
      = ∑ m : Fin (k + 1), ((Fin.cons 0 c : Fin (k + 1) → ℝ) m * d m
          - (Fin.snoc c 0 : Fin (k + 1) → ℝ) m * d m) := by
    rw [Finset.sum_sub_distrib, hasum, hbsum, ← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun j _ => by ring
  rw [hrw]
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun m _ => ?_)
  obtain ⟨ha0', ha1'⟩ := ha01 m
  obtain ⟨hb0', hb1'⟩ := hb01 m
  rw [← sub_mul, abs_mul]
  refine mul_le_of_le_one_left (abs_nonneg _) ?_
  rw [abs_le]
  constructor <;> linarith

/-- SC07: the explicit `min` representation of `eq:schedule-parameterization` makes the
cumulative occupation Lipschitz in the switch times, uniformly in the mode and the time:
`‖W(·; τ) - W(·; τ')‖_∞ ≤ ∑_m |τ_m - τ'_m|`. -/
theorem abs_occupation_sub_occupation_le {k : ℕ} (p : Fin k → Fin n) (τ τ' : Fin (k + 1) → ℝ)
    (i : Fin n) (t : ℝ) :
    |occupation p τ i t - occupation p τ' i t| ≤ ∑ m : Fin (k + 1), |τ m - τ' m| := by
  classical
  have hmin : ∀ m : Fin (k + 1), |min t (τ m) - min t (τ' m)| ≤ |τ m - τ' m| := by
    intro m
    refine (abs_min_sub_min_le_max t (τ m) t (τ' m)).trans ?_
    rw [sub_self, abs_zero, max_eq_right (abs_nonneg _)]
  have hexp : occupation p τ i t - occupation p τ' i t
      = ∑ j : Fin k, (if p j = i then (1 : ℝ) else 0) *
          ((min t (τ j.succ) - min t (τ' j.succ))
            - (min t (τ j.castSucc) - min t (τ' j.castSucc))) := by
    simp only [occupation, ← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl fun j _ => ?_
    rcases eq_or_ne (p j) i with hp | hp
    · simp only [if_pos hp, one_mul]; ring
    · simp only [if_neg hp, zero_mul, sub_self]
  rw [hexp]
  refine le_trans (abs_sum_coeff_telescope_le _ (fun j => ?_) (fun j => ?_)
    (fun m => min t (τ m) - min t (τ' m))) (Finset.sum_le_sum fun m _ => hmin m)
  · split_ifs <;> norm_num
  · split_ifs <;> norm_num

/-! ### Compactness of the schedule error sets and attainment of the continuous optima -/

/-- The full error of a schedule, as a function of its switch times, is Lipschitz and hence
continuous on the ordered-time simplex. -/
theorem continuousOn_D_occupation (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) {k : ℕ} (p : Fin k → Fin n) :
    ContinuousOn (fun τ : Fin (k + 1) → ℝ => D A (occupation p τ) T)
      (orderedTimesSet k T) := by
  refine LipschitzOnWith.continuousOn (K := (k : ℝ≥0) + 1) (LipschitzOnWith.of_dist_le_mul ?_)
  intro τ hτ τ' hτ'
  have hbound : ∑ m : Fin (k + 1), |τ m - τ' m| ≤ ((k : ℝ) + 1) * dist τ τ' := by
    calc ∑ m : Fin (k + 1), |τ m - τ' m| ≤ ∑ _m : Fin (k + 1), dist τ τ' := by
          refine Finset.sum_le_sum fun m _ => ?_
          rw [← Real.dist_eq]
          exact dist_le_pi_dist τ τ' m
      _ = ((k : ℝ) + 1) * dist τ τ' := by
          rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
          push_cast
          ring
  have h1 : D A (occupation p τ) T
      ≤ D A (occupation p τ') T + ∑ m : Fin (k + 1), |τ m - τ' m| :=
    D_le_D_add_schedule hn hA (occupation_isCumulative p hτ') hT
      fun i t _ => abs_occupation_sub_occupation_le p τ τ' i t
  have h2 : D A (occupation p τ') T
      ≤ D A (occupation p τ) T + ∑ m : Fin (k + 1), |τ' m - τ m| :=
    D_le_D_add_schedule hn hA (occupation_isCumulative p hτ) hT
      fun i t _ => abs_occupation_sub_occupation_le p τ' τ i t
  rw [Finset.sum_congr rfl fun m (_ : m ∈ Finset.univ) => abs_sub_comm (τ' m) (τ m)] at h2
  have hcoe : ((((k : ℝ≥0) + 1 : ℝ≥0)) : ℝ) = (k : ℝ) + 1 := by push_cast; ring
  rw [Real.dist_eq, abs_sub_le_iff, hcoe]
  constructor <;> linarith

/-- The one-sided error of a schedule, as a function of its switch times, is Lipschitz and
hence continuous on the ordered-time simplex. -/
theorem continuousOn_Dminus_occupation (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) {k : ℕ} (p : Fin k → Fin n) :
    ContinuousOn (fun τ : Fin (k + 1) → ℝ => Dminus A (occupation p τ) T)
      (orderedTimesSet k T) := by
  refine LipschitzOnWith.continuousOn (K := (k : ℝ≥0) + 1) (LipschitzOnWith.of_dist_le_mul ?_)
  intro τ hτ τ' hτ'
  have hbound : ∑ m : Fin (k + 1), |τ m - τ' m| ≤ ((k : ℝ) + 1) * dist τ τ' := by
    calc ∑ m : Fin (k + 1), |τ m - τ' m| ≤ ∑ _m : Fin (k + 1), dist τ τ' := by
          refine Finset.sum_le_sum fun m _ => ?_
          rw [← Real.dist_eq]
          exact dist_le_pi_dist τ τ' m
      _ = ((k : ℝ) + 1) * dist τ τ' := by
          rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
          push_cast
          ring
  have h1 : Dminus A (occupation p τ) T
      ≤ Dminus A (occupation p τ') T + ∑ m : Fin (k + 1), |τ m - τ' m| :=
    Dminus_le_Dminus_add_schedule hn hA (occupation_isCumulative p hτ') hT
      fun i t _ => abs_occupation_sub_occupation_le p τ τ' i t
  have h2 : Dminus A (occupation p τ') T
      ≤ Dminus A (occupation p τ) T + ∑ m : Fin (k + 1), |τ' m - τ m| :=
    Dminus_le_Dminus_add_schedule hn hA (occupation_isCumulative p hτ) hT
      fun i t _ => abs_occupation_sub_occupation_le p τ' τ i t
  rw [Finset.sum_congr rfl fun m (_ : m ∈ Finset.univ) => abs_sub_comm (τ' m) (τ m)] at h2
  have hcoe : ((((k : ℝ≥0) + 1 : ℝ≥0)) : ℝ) = (k : ℝ) + 1 := by push_cast; ring
  rw [Real.dist_eq, abs_sub_le_iff, hcoe]
  constructor <;> linarith

/-- SC07: the set minimized by `OPT` is compact, being a finite union over words of continuous
images of the compact ordered-time simplex. -/
theorem isCompact_scheduleErrorSet (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) (k : ℕ) : IsCompact (scheduleErrorSet A T k) := by
  have h : scheduleErrorSet A T k = ⋃ p : Fin k → Fin n,
      (fun τ : Fin (k + 1) → ℝ => D A (occupation p τ) T) '' orderedTimesSet k T := by
    ext e
    simp only [scheduleErrorSet, mem_ofPred_eq, mem_iUnion, mem_image, mem_orderedTimesSet]
    constructor
    · rintro ⟨W, ⟨p, τ, hτ, rfl⟩, rfl⟩
      exact ⟨p, τ, hτ, rfl⟩
    · rintro ⟨p, τ, hτ, rfl⟩
      exact ⟨occupation p τ, ⟨p, τ, hτ, rfl⟩, rfl⟩
  rw [h]
  exact isCompact_iUnion fun p => (isCompact_orderedTimesSet k T).image_of_continuousOn
    (continuousOn_D_occupation hn hA hT p)

/-- SC07: the set minimized by `OPTminus` is compact. -/
theorem isCompact_scheduleLowerErrorSet (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) (k : ℕ) :
    IsCompact (scheduleLowerErrorSet A T k) := by
  have h : scheduleLowerErrorSet A T k = ⋃ p : Fin k → Fin n,
      (fun τ : Fin (k + 1) → ℝ => Dminus A (occupation p τ) T) '' orderedTimesSet k T := by
    ext e
    simp only [scheduleLowerErrorSet, mem_ofPred_eq, mem_iUnion, mem_image,
      mem_orderedTimesSet]
    constructor
    · rintro ⟨W, ⟨p, τ, hτ, rfl⟩, rfl⟩
      exact ⟨p, τ, hτ, rfl⟩
    · rintro ⟨p, τ, hτ, rfl⟩
      exact ⟨occupation p τ, ⟨p, τ, hτ, rfl⟩, rfl⟩
  rw [h]
  exact isCompact_iUnion fun p => (isCompact_orderedTimesSet k T).image_of_continuousOn
    (continuousOn_Dminus_occupation hn hA hT p)

/-- SC07: the continuous instance optimum is attained by a schedule; the infimum defining
`OPT` is a minimum. -/
theorem exists_OPT_eq (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) (s : ℕ) :
    ∃ W : Fin n → ℝ → ℝ, IsSchedule (s + 1) T W ∧ OPT A T s = D A W T :=
  (isCompact_scheduleErrorSet hn hA hT (s + 1)).sInf_mem
    (scheduleErrorSet_nonempty hn hT (Nat.succ_pos s))

/-- SC07: the one-sided continuous instance optimum is attained by a schedule. -/
theorem exists_OPTminus_eq (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) {k : ℕ} (hk : 0 < k) :
    ∃ W : Fin n → ℝ → ℝ, IsSchedule k T W ∧ OPTminus A T k = Dminus A W T :=
  (isCompact_scheduleLowerErrorSet hn hA hT k).sInf_mem
    (scheduleLowerErrorSet_nonempty hn hT hk)

/-! ## SC07, step 4: attainment of the grid minimax values

The grid-constant input class is parameterized by the compact set of rate matrices, a product
of standard simplices, and the grid instance optima depend continuously on the rate matrix. -/

/-- The horizon of a grid is nonnegative. -/
theorem nonneg_of_isGrid {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T) : 0 ≤ T :=
  hx.last ▸ hx.orderedTimes.nonneg (Fin.last N)

/-- The rate matrices of `eq:grid-definitions`, viewed as a subset of `Fin N → Fin n → ℝ`. -/
def rateMatrixSet (N n : ℕ) : Set (Fin N → Fin n → ℝ) := {r | IsRateMatrix r}

@[simp] theorem mem_rateMatrixSet {r : Fin N → Fin n → ℝ} :
    r ∈ rateMatrixSet N n ↔ IsRateMatrix r := Iff.rfl

/-- The uniform rate matrix, all of whose entries are `1 / n`. -/
theorem isRateMatrix_uniform (hn : 0 < n) (N : ℕ) :
    IsRateMatrix (fun (_ : Fin N) (_ : Fin n) => (1 : ℝ) / n) where
  nonneg _ _ := by positivity
  conservation _ := by
    have hne : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn.ne'
    rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    field_simp

/-- The set of rate matrices is compact: a closed subset of a product of unit intervals. -/
theorem isCompact_rateMatrixSet (N n : ℕ) : IsCompact (rateMatrixSet N n) := by
  have hsub : rateMatrixSet N n ⊆
      Set.univ.pi fun _ : Fin N => Set.univ.pi fun _ : Fin n => Icc (0 : ℝ) 1 := by
    intro r hr j _ i _
    refine ⟨hr.nonneg j i, ?_⟩
    calc r j i ≤ ∑ i', r j i' :=
          Finset.single_le_sum (fun i' _ => hr.nonneg j i') (Finset.mem_univ i)
      _ = 1 := hr.conservation j
  refine IsCompact.of_isClosed_subset
    (isCompact_univ_pi fun _ => isCompact_univ_pi fun _ => isCompact_Icc) ?_ hsub
  have hset : rateMatrixSet N n =
      (⋂ j : Fin N, ⋂ i : Fin n, {r : Fin N → Fin n → ℝ | 0 ≤ r j i}) ∩
        ⋂ j : Fin N, {r : Fin N → Fin n → ℝ | ∑ i, r j i = 1} := by
    ext r
    simp only [mem_rateMatrixSet, mem_inter_iff, mem_ofPred_eq, mem_iInter]
    exact ⟨fun hr => ⟨fun j i => hr.nonneg j i, fun j => hr.conservation j⟩,
      fun h => ⟨fun j i => h.1 j i, fun j => h.2 j⟩⟩
  rw [hset]
  refine IsClosed.inter (isClosed_iInter fun j => isClosed_iInter fun i => ?_)
    (isClosed_iInter fun j => ?_)
  · exact isClosed_le continuous_const ((continuous_apply i).comp (continuous_apply j))
  · exact isClosed_eq
      (continuous_finsetSum _ fun i _ => (continuous_apply i).comp (continuous_apply j))
      continuous_const

/-- A grid-constant input depends Lipschitz-continuously on its rate matrix, uniformly on the
horizon. -/
theorem abs_gridCumulative_sub_le {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    (r r' : Fin N → Fin n → ℝ) (i : Fin n) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) :
    |gridCumulative x r i t - gridCumulative x r' i t| ≤ ∑ j : Fin N, |r j i - r' j i| * T := by
  simp only [gridCumulative, ← Finset.sum_sub_distrib]
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun j _ => ?_)
  have hcast : 0 ≤ x j.castSucc := hx.orderedTimes.nonneg j.castSucc
  have hc0 : 0 ≤ min t (x j.succ) - min t (x j.castSucc) :=
    sub_nonneg.mpr (min_le_min le_rfl (hx.strictMono (Fin.castSucc_lt_succ (i := j))).le)
  have hcT : min t (x j.succ) - min t (x j.castSucc) ≤ T := by
    have h1 : min t (x j.succ) ≤ T := (min_le_left _ _).trans ht.2
    have h2 : 0 ≤ min t (x j.castSucc) := le_min ht.1 hcast
    linarith
  rw [← sub_mul, abs_mul, abs_of_nonneg hc0]
  exact mul_le_mul_of_nonneg_left hcT (abs_nonneg _)

/-- The uniform bound of `abs_gridCumulative_sub_le` in terms of the supremum distance between
rate matrices. -/
theorem abs_gridCumulative_sub_le_dist {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    (r r' : Fin N → Fin n → ℝ) (i : Fin n) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) :
    |gridCumulative x r i t - gridCumulative x r' i t| ≤ (N : ℝ) * T * dist r r' := by
  refine (abs_gridCumulative_sub_le hx r r' i ht).trans ?_
  have hT : (0 : ℝ) ≤ T := nonneg_of_isGrid hx
  calc ∑ j : Fin N, |r j i - r' j i| * T ≤ ∑ _j : Fin N, dist r r' * T := by
        refine Finset.sum_le_sum fun j _ => mul_le_mul_of_nonneg_right ?_ hT
        rw [← Real.dist_eq]
        exact (dist_le_pi_dist (r j) (r' j) i).trans (dist_le_pi_dist r r' j)
    _ = (N : ℝ) * T * dist r r' := by
        rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
        ring

/-- The grid instance optimum of a grid-constant input is continuous in its rate matrix. -/
theorem continuousOn_gridOPT_gridCumulative (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) (s : ℕ) :
    ContinuousOn (fun r : Fin N → Fin n → ℝ => gridOPT x (gridCumulative x r) T s)
      (rateMatrixSet N n) := by
  have hT : (0 : ℝ) ≤ T := nonneg_of_isGrid hx
  refine LipschitzOnWith.continuousOn
    (K := ⟨(N : ℝ) * T, by positivity⟩) (LipschitzOnWith.of_dist_le_mul ?_)
  intro r hr r' hr'
  have hcum : IsCumulative (gridCumulative x r) T :=
    gridCumulative_isCumulative hx.orderedTimes hr
  have hcum' : IsCumulative (gridCumulative x r') T :=
    gridCumulative_isCumulative hx.orderedTimes hr'
  have hbound := abs_gridOPT_sub_gridOPT_le hn hx hcum hcum' hT s
    fun i t ht => abs_gridCumulative_sub_le_dist hx r r' i ht
  rw [Real.dist_eq]
  exact hbound

/-- The one-sided grid instance optimum of a grid-constant input is continuous in its rate
matrix. -/
theorem continuousOn_gridOPTminus_gridCumulative (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {k : ℕ} (hk : 0 < k) :
    ContinuousOn (fun r : Fin N → Fin n → ℝ => gridOPTminus x (gridCumulative x r) T k)
      (rateMatrixSet N n) := by
  have hT : (0 : ℝ) ≤ T := nonneg_of_isGrid hx
  refine LipschitzOnWith.continuousOn
    (K := ⟨(N : ℝ) * T, by positivity⟩) (LipschitzOnWith.of_dist_le_mul ?_)
  intro r hr r' hr'
  have hcum : IsCumulative (gridCumulative x r) T :=
    gridCumulative_isCumulative hx.orderedTimes hr
  have hcum' : IsCumulative (gridCumulative x r') T :=
    gridCumulative_isCumulative hx.orderedTimes hr'
  have hbound := abs_gridOPTminus_sub_gridOPTminus_le hn hx hcum hcum' hT hk
    fun i t ht => abs_gridCumulative_sub_le_dist hx r r' i ht
  rw [Real.dist_eq]
  exact hbound

/-- SC07, the case the package needs: the grid minimax value is attained by a grid-constant
input. -/
theorem exists_gridF_eq (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T) (s : ℕ) :
    ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧ gridF x n s T = gridOPT x A T s := by
  have hset : {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧ v = gridOPT x A T s}
      = (fun r : Fin N → Fin n → ℝ => gridOPT x (gridCumulative x r) T s) ''
          rateMatrixSet N n := by
    ext v
    simp only [mem_ofPred_eq, mem_image, mem_rateMatrixSet]
    constructor
    · rintro ⟨A, ⟨r, hr, rfl⟩, rfl⟩
      exact ⟨r, hr, rfl⟩
    · rintro ⟨r, hr, rfl⟩
      exact ⟨gridCumulative x r, ⟨r, hr, rfl⟩, rfl⟩
  have hcomp := (isCompact_rateMatrixSet N n).image_of_continuousOn
    (continuousOn_gridOPT_gridCumulative hn hx s)
  obtain ⟨r, hr, hv⟩ := hcomp.sSup_mem
    (Set.Nonempty.image _ ⟨_, isRateMatrix_uniform hn N⟩)
  refine ⟨gridCumulative x r, ⟨r, hr, rfl⟩, ?_⟩
  change sSup {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧ v = gridOPT x A T s} = _
  rw [hset]
  exact hv.symm

/-- SC07: the one-sided grid minimax value is attained by a grid-constant input. -/
theorem exists_gridGminus_eq (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {k : ℕ} (hk : 0 < k) :
    ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧ gridGminus x n k T = gridOPTminus x A T k := by
  have hset : {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧ v = gridOPTminus x A T k}
      = (fun r : Fin N → Fin n → ℝ => gridOPTminus x (gridCumulative x r) T k) ''
          rateMatrixSet N n := by
    ext v
    simp only [mem_ofPred_eq, mem_image, mem_rateMatrixSet]
    constructor
    · rintro ⟨A, ⟨r, hr, rfl⟩, rfl⟩
      exact ⟨r, hr, rfl⟩
    · rintro ⟨r, hr, rfl⟩
      exact ⟨gridCumulative x r, ⟨r, hr, rfl⟩, rfl⟩
  have hcomp := (isCompact_rateMatrixSet N n).image_of_continuousOn
    (continuousOn_gridOPTminus_gridCumulative hn hx hk)
  obtain ⟨r, hr, hv⟩ := hcomp.sSup_mem
    (Set.Nonempty.image _ ⟨_, isRateMatrix_uniform hn N⟩)
  refine ⟨gridCumulative x r, ⟨r, hr, rfl⟩, ?_⟩
  change sSup {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧ v = gridOPTminus x A T k} = _
  rw [hset]
  exact hv.symm

/-! ## A toolbox for the optima and the minimax values

Convenient one-sided characterizations, used repeatedly in SC08 and SC09. -/

/-- Every schedule bounds the continuous instance optimum from above. -/
theorem OPT_le_D (hn : 0 < n) {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) {s : ℕ} (hW : IsSchedule (s + 1) T W) : OPT A T s ≤ D A W T :=
  csInf_le (scheduleErrorSet_bddBelow hn hA hT _) ⟨W, hW, rfl⟩

/-- A bound valid for every schedule bounds the continuous instance optimum from below. -/
theorem le_OPT (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T c : ℝ} (hT : 0 ≤ T) {s : ℕ}
    (h : ∀ W : Fin n → ℝ → ℝ, IsSchedule (s + 1) T W → c ≤ D A W T) : c ≤ OPT A T s := by
  refine le_csInf (scheduleErrorSet_nonempty hn hT (Nat.succ_pos s)) ?_
  rintro e ⟨W, hW, rfl⟩
  exact h W hW

/-- Every grid schedule bounds the grid instance optimum from above. -/
theorem gridOPT_le_D (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {A W : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T) {s : ℕ}
    (hW : IsGridSchedule x (s + 1) W) : gridOPT x A T s ≤ D A W T :=
  csInf_le (gridScheduleErrorSet_bddBelow hn hx hA hT _) ⟨W, hW, rfl⟩

/-- A bound valid for every grid schedule bounds the grid instance optimum from below. -/
theorem le_gridOPT (hn : 0 < n) {x : Fin (N + 1) → ℝ} {A : Fin n → ℝ → ℝ} {T c : ℝ} {s : ℕ}
    (h : ∀ W : Fin n → ℝ → ℝ, IsGridSchedule x (s + 1) W → c ≤ D A W T) :
    c ≤ gridOPT x A T s := by
  refine le_csInf (gridScheduleErrorSet_nonempty hn A T (Nat.succ_pos s)) ?_
  rintro e ⟨W, hW, rfl⟩
  exact h W hW

/-- The continuous instance optimum never exceeds the horizon. -/
theorem OPT_le_horizon (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) (s : ℕ) : OPT A T s ≤ T := by
  obtain ⟨W, hW⟩ := exists_isSchedule hn hT (Nat.succ_pos s)
  refine (OPT_le_D hn hA hT hW).trans (D_le hT fun i t ht => ?_)
  exact (errorSet_mem_Icc hA hW.isCumulative ⟨i, t, ht, rfl⟩).2

/-- The continuous instance optimum is nonnegative. -/
theorem OPT_nonneg (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) (s : ℕ) : 0 ≤ OPT A T s :=
  le_OPT hn hT fun _W hW => D_nonneg hn hA hW.isCumulative hT

/-- The set maximized by `F`. -/
def minimaxSet (n s : ℕ) (T : ℝ) : Set ℝ :=
  {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsCumulative A T ∧ v = OPT A T s}

@[simp] theorem mem_minimaxSet {n s : ℕ} {T v : ℝ} :
    v ∈ minimaxSet n s T ↔ ∃ A : Fin n → ℝ → ℝ, IsCumulative A T ∧ v = OPT A T s := Iff.rfl

theorem F_eq_sSup (n s : ℕ) (T : ℝ) : F n s T = sSup (minimaxSet n s T) := rfl

/-- The uniform input `A i t = t / n`, which allocates every mode at the same constant rate. -/
noncomputable def uniformCumulative (n : ℕ) : Fin n → ℝ → ℝ := fun _ t => t / n

/-- The uniform input is a cumulative allocation on every horizon. -/
theorem isCumulative_uniformCumulative (hn : 0 < n) (T : ℝ) :
    IsCumulative (uniformCumulative n) T := by
  have hn' : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have hne : (n : ℝ) ≠ 0 := by positivity
  refine ⟨fun _ => by simp [uniformCumulative], fun _ a b _ hab _ => ?_,
    fun _ a b _ hab _ => ?_, fun _ _ => ?_⟩
  · simp only [uniformCumulative]
    gcongr
  · simp only [uniformCumulative, ← sub_div]
    exact div_le_self (by linarith) hn'
  · simp only [uniformCumulative, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
      nsmul_eq_mul]
    field_simp

/-- The set maximized by `F` is nonempty. -/
theorem minimaxSet_nonempty (hn : 0 < n) {T : ℝ} (s : ℕ) :
    (minimaxSet n s T).Nonempty :=
  ⟨_, uniformCumulative n, isCumulative_uniformCumulative hn T, rfl⟩

/-- The set maximized by `F` is bounded above by the horizon. -/
theorem minimaxSet_bddAbove (hn : 0 < n) {T : ℝ} (s : ℕ) (hT : 0 ≤ T) :
    BddAbove (minimaxSet n s T) := by
  refine ⟨T, ?_⟩
  rintro v ⟨A, hA, rfl⟩
  exact OPT_le_horizon hn hA hT s

/-- Every cumulative input bounds the minimax value from below. -/
theorem OPT_le_F (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) (s : ℕ) : OPT A T s ≤ F n s T :=
  le_csSup (minimaxSet_bddAbove hn s hT) ⟨A, hA, rfl⟩

/-- A bound valid for every cumulative input bounds the minimax value from above. -/
theorem F_le {T c : ℝ} {s : ℕ} (hc : 0 ≤ c)
    (h : ∀ A : Fin n → ℝ → ℝ, IsCumulative A T → OPT A T s ≤ c) : F n s T ≤ c := by
  refine Real.sSup_le (fun v hv => ?_) hc
  obtain ⟨A, hA, rfl⟩ := hv
  exact h A hA

/-- The minimax value is nonnegative. -/
theorem F_nonneg (hn : 0 < n) {T : ℝ} (s : ℕ) (hT : 0 ≤ T) : 0 ≤ F n s T :=
  le_trans (OPT_nonneg hn (isCumulative_uniformCumulative hn T) hT s)
    (OPT_le_F hn (isCumulative_uniformCumulative hn T) hT s)

/-! ## SC09: the no-switch value `prop:no-switch` -/

/-- Values of the constant schedule at its own mode, on the horizon. -/
theorem constSchedule_apply_self {T : ℝ} (q : Fin n) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) :
    constSchedule q T q t = t := by
  simp [constSchedule, occupation, min_eq_left ht.2, min_eq_right ht.1]

/-- The constant schedule never activates any other mode. -/
theorem constSchedule_apply_ne {T : ℝ} {q i : Fin n} (hqi : q ≠ i) (t : ℝ) :
    constSchedule q T i t = 0 := by
  simp [constSchedule, occupation, hqi]

/-- A single-block schedule has occupied the whole horizon by its end. -/
private theorem occupation_one_apply {T : ℝ} (hT : 0 ≤ T) (p : Fin 1 → Fin n)
    {τ : Fin 2 → ℝ} (hτ : OrderedTimes τ T) : occupation p τ (p 0) T = T := by
  rw [occupation, Fin.sum_univ_one, if_pos rfl]
  have h0 : τ ((0 : Fin 1).castSucc) = 0 := hτ.first
  have h1 : τ ((0 : Fin 1).succ) = T := hτ.last
  rw [h0, h1, min_self, min_eq_right hT, sub_zero]

/-- Some mode carries at least the average terminal mass `T / n`. -/
theorem exists_mass_ge (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) : ∃ q : Fin n, T / n ≤ A q T := by
  have hne : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn.ne'
  have hsum : ∑ _i : Fin n, T / (n : ℝ) ≤ ∑ i, A i T := by
    rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul,
      hA.conservation T ⟨hT, le_rfl⟩]
    field_simp
    exact le_rfl
  obtain ⟨q, -, hq⟩ := Finset.exists_le_of_sum_le ⟨⟨0, hn⟩, Finset.mem_univ _⟩ hsum
  exact ⟨q, hq⟩

/-- `prop:no-switch`, upper bound: activating a mode throughout gives error at most the mass
missing from that mode. -/
theorem D_constSchedule_le {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) (q : Fin n) : D A (constSchedule q T) T ≤ T - A q T := by
  have hsum : ∀ t ∈ Icc (0 : ℝ) T, ∑ i' ∈ Finset.univ.erase q, A i' t = t - A q t := by
    intro t ht
    have h := Finset.sum_erase_add Finset.univ (fun i' => A i' t) (Finset.mem_univ q)
    rw [hA.conservation t ht] at h
    linarith
  refine D_le (by linarith [hA.le_self q ⟨hT, le_rfl⟩]) fun i t ht => ?_
  rcases eq_or_ne q i with rfl | hqi
  · rw [constSchedule_apply_self q ht]
    have h1 : A q t ≤ t := hA.le_self q ht
    have h2 : t - A q t ≤ T - A q T := by
      rw [← hsum t ht, ← hsum T ⟨hT, le_rfl⟩]
      exact Finset.sum_le_sum fun i' _ => hA.mono i' t T ht.1 ht.2 le_rfl
    rw [abs_of_nonpos (by linarith)]
    linarith
  · rw [constSchedule_apply_ne hqi, sub_zero, abs_of_nonneg (hA.nonneg i ht)]
    calc A i t ≤ A i T := hA.mono i t T ht.1 ht.2 le_rfl
      _ ≤ ∑ i' ∈ Finset.univ.erase q, A i' T :=
          Finset.single_le_sum (f := fun i' => A i' T)
            (fun i' _ => hA.nonneg i' ⟨hT, le_rfl⟩)
            (Finset.mem_erase.mpr ⟨Ne.symm hqi, Finset.mem_univ i⟩)
      _ = T - A q T := hsum T ⟨hT, le_rfl⟩

/-- The no-switch bound is nonnegative. -/
theorem no_switch_value_nonneg (hn : 0 < n) {T : ℝ} (hT : 0 ≤ T) :
    0 ≤ T * (1 - 1 / (n : ℝ)) := by
  have hn' : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have : (1 : ℝ) / n ≤ 1 := by rw [div_le_one (by linarith)]; exact hn'
  nlinarith

/-- `prop:no-switch`, upper bound at the level of the instance optimum: some constant schedule
has error at most `T (1 - 1/n)`. -/
theorem OPT_no_switch_le (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) : OPT A T 0 ≤ T * (1 - 1 / (n : ℝ)) := by
  have hne : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn.ne'
  obtain ⟨q, hq⟩ := exists_mass_ge hn hA hT
  have h1 : OPT A T 0 ≤ D A (constSchedule q T) T :=
    OPT_le_D hn hA hT (isSchedule_constSchedule hT q)
  have h2 : T - A q T ≤ T * (1 - 1 / (n : ℝ)) := by
    have : T * (1 - 1 / (n : ℝ)) = T - T / n := by field_simp
    rw [this]
    linarith
  exact h1.trans ((D_constSchedule_le hA hT q).trans h2)

/-- `prop:no-switch`, lower bound: against an input whose terminal masses are all `T / n`,
every single-block schedule has error at least `T (1 - 1/n)`. -/
theorem le_D_of_isSchedule_one (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) (hmass : ∀ i, A i T = T / n) {W : Fin n → ℝ → ℝ}
    (hW : IsSchedule 1 T W) : T * (1 - 1 / (n : ℝ)) ≤ D A W T := by
  have hn' : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  obtain ⟨p, τ, hτ, rfl⟩ := hW
  have hWq : occupation p τ (p 0) T = T := occupation_one_apply hT p hτ
  have hle : T / n ≤ T := div_le_self hT hn'
  have hkey := le_D hA (occupation_isCumulative p hτ) (p 0) ⟨hT, le_rfl⟩
  rw [hmass (p 0), hWq, abs_of_nonpos (by linarith)] at hkey
  have hfield : T * (1 - 1 / (n : ℝ)) = -(T / n - T) := by
    have hne : (n : ℝ) ≠ 0 := by linarith
    field_simp
    ring
  rw [hfield]
  exact hkey

/-- SC09, continuous case: `F_{n,0}(T) = T (1 - 1/n)`. -/
theorem F_no_switch (hn : 0 < n) {T : ℝ} (hT : 0 ≤ T) :
    F n 0 T = T * (1 - 1 / (n : ℝ)) := by
  refine le_antisymm (F_le (no_switch_value_nonneg hn hT) fun A hA => OPT_no_switch_le hn hA hT)
    ?_
  have hunif : ∀ i : Fin n, uniformCumulative n i T = T / n := fun _ => rfl
  have hA := isCumulative_uniformCumulative (n := n) hn T
  refine le_trans (le_OPT hn hT fun W hW => le_D_of_isSchedule_one hn hA hT hunif hW) ?_
  exact OPT_le_F hn hA hT 0

/-! ### The grid no-switch value -/

/-- The set maximized by `gridF`. -/
def gridMinimaxSet (x : Fin (N + 1) → ℝ) (n s : ℕ) (T : ℝ) : Set ℝ :=
  {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧ v = gridOPT x A T s}

@[simp] theorem mem_gridMinimaxSet {x : Fin (N + 1) → ℝ} {n s : ℕ} {T v : ℝ} :
    v ∈ gridMinimaxSet x n s T ↔
      ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧ v = gridOPT x A T s := Iff.rfl

theorem gridF_eq_sSup (x : Fin (N + 1) → ℝ) (n s : ℕ) (T : ℝ) :
    gridF x n s T = sSup (gridMinimaxSet x n s T) := rfl

/-- The constant schedule is a grid schedule: it switches only at the two extreme grid
points. -/
theorem isGridSchedule_constSchedule {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    (q : Fin n) : IsGridSchedule x 1 (constSchedule q T) := by
  refine ⟨fun _ => q, ![0, Fin.last N], ?_, ?_, ?_, ?_⟩
  · refine Fin.monotone_iff_le_succ.mpr fun j => ?_
    fin_cases j
    simp
  · rfl
  · rfl
  · have hcomp : (x ∘ ![(0 : Fin (N + 1)), Fin.last N]) = ![(0 : ℝ), T] := by
      funext j
      fin_cases j
      · simpa using hx.first
      · simpa using hx.last
    rw [hcomp]
    rfl

/-- The set maximized by `gridF` is bounded above by the horizon. -/
theorem gridMinimaxSet_bddAbove (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    (s : ℕ) : BddAbove (gridMinimaxSet x n s T) := by
  refine ⟨T, ?_⟩
  rintro v ⟨A, ⟨r, hr, rfl⟩, rfl⟩
  exact gridOPT_le_horizon hn hx (gridCumulative_isCumulative hx.orderedTimes hr) s

/-- The uniform grid-constant input allocates every mode at rate `1 / n`, so its cumulative
allocation is `t / n` on the horizon. -/
theorem gridCumulative_uniform (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    (i : Fin n) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) :
    gridCumulative x (fun (_ : Fin N) (_ : Fin n) => (1 : ℝ) / n) i t = t / n := by
  have hne : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn.ne'
  have hcons := (gridCumulative_isCumulative hx.orderedTimes
    (isRateMatrix_uniform hn N)).conservation t ht
  have hconst : ∀ i' : Fin n,
      gridCumulative x (fun (_ : Fin N) (_ : Fin n) => (1 : ℝ) / n) i' t
        = gridCumulative x (fun (_ : Fin N) (_ : Fin n) => (1 : ℝ) / n) i t := fun _ => rfl
  rw [Finset.sum_congr rfl fun i' _ => hconst i', Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul] at hcons
  field_simp at hcons ⊢
  linarith

/-- SC09, grid case: `F^T_{n,0} = T (1 - 1/n)` on every grid. -/
theorem gridF_no_switch (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T) :
    gridF x n 0 T = T * (1 - 1 / (n : ℝ)) := by
  have hT : (0 : ℝ) ≤ T := nonneg_of_isGrid hx
  refine le_antisymm ?_ ?_
  · refine Real.sSup_le (fun v hv => ?_) (no_switch_value_nonneg hn hT)
    obtain ⟨A, ⟨r, hr, rfl⟩, rfl⟩ := hv
    have hA := gridCumulative_isCumulative hx.orderedTimes hr
    obtain ⟨q, hq⟩ := exists_mass_ge hn hA hT
    have hne : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn.ne'
    have h1 : gridOPT x (gridCumulative x r) T 0 ≤ D (gridCumulative x r) (constSchedule q T) T :=
      gridOPT_le_D hn hx hA hT (isGridSchedule_constSchedule hx q)
    have h2 : T - gridCumulative x r q T ≤ T * (1 - 1 / (n : ℝ)) := by
      have hid : T * (1 - 1 / (n : ℝ)) = T - T / n := by field_simp
      rw [hid]
      linarith
    exact h1.trans ((D_constSchedule_le hA hT q).trans h2)
  · set A : Fin n → ℝ → ℝ :=
      gridCumulative x (fun (_ : Fin N) (_ : Fin n) => (1 : ℝ) / n) with hAdef
    have hA : IsCumulative A T :=
      gridCumulative_isCumulative hx.orderedTimes (isRateMatrix_uniform hn N)
    have hmass : ∀ i, A i T = T / n := fun i =>
      gridCumulative_uniform hn hx i ⟨hT, le_rfl⟩
    have hlow : T * (1 - 1 / (n : ℝ)) ≤ gridOPT x A T 0 :=
      le_gridOPT hn fun W hW => le_D_of_isSchedule_one hn hA hT hmass (hW.isSchedule hx)
    refine hlow.trans (le_csSup (gridMinimaxSet_bddAbove hn hx 0) ?_)
    exact ⟨A, ⟨_, isRateMatrix_uniform hn N, hAdef⟩, rfl⟩

/-! ## SC08: the zero horizon, scaling, and budget monotonicity -/

/-! ### The convention at `T = 0` -/

/-- On the degenerate horizon every error vanishes. -/
theorem D_horizon_zero (hn : 0 < n) {A W : Fin n → ℝ → ℝ} (hA : IsCumulative A 0)
    (hW : IsCumulative W 0) : D A W 0 = 0 := by
  refine le_antisymm (D_le le_rfl fun i t ht => ?_) (D_nonneg hn hA hW le_rfl)
  obtain ⟨h1, h2⟩ := ht
  have ht0 : t = 0 := le_antisymm h2 h1
  subst ht0
  simp [hA.initial, hW.initial]

/-- On the degenerate horizon every instance optimum vanishes. -/
theorem OPT_horizon_zero (hn : 0 < n) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A 0) (s : ℕ) :
    OPT A 0 s = 0 := by
  refine le_antisymm ?_ (OPT_nonneg hn hA le_rfl s)
  obtain ⟨W, hW⟩ := exists_isSchedule hn (le_refl (0 : ℝ)) (Nat.succ_pos s)
  calc OPT A 0 s ≤ D A W 0 := OPT_le_D hn hA le_rfl hW
    _ = 0 := D_horizon_zero hn hA hW.isCumulative

/-- SC08: `F_{n,s}(0) = 0`. -/
theorem F_horizon_zero (hn : 0 < n) (s : ℕ) : F n s 0 = 0 :=
  le_antisymm (F_le le_rfl fun _A hA => le_of_eq (OPT_horizon_zero hn hA s))
    (F_nonneg hn s le_rfl)

/-! ### Budget monotonicity -/

/-- SC08: enlarging the switch budget cannot increase the continuous instance optimum. -/
theorem OPT_mono_budget (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) {s s' : ℕ} (hs : s ≤ s') : OPT A T s' ≤ OPT A T s := by
  refine csInf_le_csInf (scheduleErrorSet_bddBelow hn hA hT _)
    (scheduleErrorSet_nonempty hn hT (Nat.succ_pos s)) ?_
  rintro e ⟨W, hW, rfl⟩
  exact ⟨W, IsSchedule.mono hn (by omega) hW, rfl⟩

/-- SC08: enlarging the block budget cannot increase the one-sided instance optimum. -/
theorem OPTminus_mono_budget (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) {k k' : ℕ} (hk : 0 < k) (hkk : k ≤ k') :
    OPTminus A T k' ≤ OPTminus A T k := by
  refine csInf_le_csInf (scheduleLowerErrorSet_bddBelow hn hA hT _)
    (scheduleLowerErrorSet_nonempty hn hT hk) ?_
  rintro e ⟨W, hW, rfl⟩
  exact ⟨W, IsSchedule.mono hn hkk hW, rfl⟩

/-- SC08: enlarging the switch budget cannot increase the minimax value. -/
theorem F_mono_budget (hn : 0 < n) {T : ℝ} (hT : 0 ≤ T) {s s' : ℕ} (hs : s ≤ s') :
    F n s' T ≤ F n s T :=
  F_le (F_nonneg hn s hT) fun _A hA =>
    (OPT_mono_budget hn hA hT hs).trans (OPT_le_F hn hA hT s)

/-! ### Scaling `eq:scaling`

The change of variables `t = c u` is a bijection of both the input class and the schedule
class, and multiplies all errors by `c`. -/

/-- The change of variables `t = c u`, applied to an input or to a schedule. -/
noncomputable def rescale (c : ℝ) (A : Fin n → ℝ → ℝ) : Fin n → ℝ → ℝ :=
  fun i u => A i (c * u) / c

/-- The change of variables is involutive up to inverting the scale. -/
theorem rescale_inv {c : ℝ} (hc : 0 < c) (A : Fin n → ℝ → ℝ) :
    rescale c (rescale (1 / c) A) = A := by
  have hc0 : c ≠ 0 := ne_of_gt hc
  funext i u
  have key : (1 : ℝ) / c * (c * u) = u := by field_simp
  simp only [rescale]
  rw [key]
  field_simp

/-- The change of variables maps the cumulative class on `[0, T]` to the cumulative class on
`[0, T / c]`. -/
theorem rescale_isCumulative {c T : ℝ} (hc : 0 < c) {A : Fin n → ℝ → ℝ}
    (hA : IsCumulative A T) : IsCumulative (rescale c A) (T / c) := by
  have hc0 : c ≠ 0 := ne_of_gt hc
  have hTc : c * (T / c) = T := by field_simp
  have hmem : ∀ u ∈ Icc (0 : ℝ) (T / c), c * u ∈ Icc (0 : ℝ) T := fun u hu =>
    ⟨mul_nonneg hc.le hu.1, hTc ▸ mul_le_mul_of_nonneg_left hu.2 hc.le⟩
  refine ⟨fun i => by simp [rescale, hA.initial], ?_, ?_, ?_⟩
  · intro i a b ha hab hb
    have h1 : (0 : ℝ) ≤ c * a := mul_nonneg hc.le ha
    have h2 : c * a ≤ c * b := mul_le_mul_of_nonneg_left hab hc.le
    have h3 : c * b ≤ T := hTc ▸ mul_le_mul_of_nonneg_left hb hc.le
    exact (div_le_div_iff_of_pos_right hc).mpr (hA.mono i _ _ h1 h2 h3)
  · intro i a b ha hab hb
    have h1 : (0 : ℝ) ≤ c * a := mul_nonneg hc.le ha
    have h2 : c * a ≤ c * b := mul_le_mul_of_nonneg_left hab hc.le
    have h3 : c * b ≤ T := hTc ▸ mul_le_mul_of_nonneg_left hb hc.le
    have h4 := hA.lipschitz i _ _ h1 h2 h3
    have h5 : (A i (c * b) - A i (c * a)) / c ≤ (c * b - c * a) / c :=
      (div_le_div_iff_of_pos_right hc).mpr h4
    simp only [rescale, ← sub_div]
    rwa [show (c * b - c * a) / c = b - a by field_simp] at h5
  · intro u hu
    simp only [rescale]
    rw [← Finset.sum_div, hA.conservation _ (hmem u hu)]
    field_simp

/-- The change of variables acts on a schedule by rescaling its switch times. -/
theorem rescale_occupation {c : ℝ} (hc : 0 < c) {k : ℕ} (p : Fin k → Fin n)
    (τ : Fin (k + 1) → ℝ) : rescale c (occupation p τ) = occupation p fun m => τ m / c := by
  have hc0 : c ≠ 0 := ne_of_gt hc
  funext i u
  simp only [rescale, occupation]
  rw [Finset.sum_div]
  refine Finset.sum_congr rfl fun j _ => ?_
  have hcancel : ∀ a : ℝ, c * (a / c) = a := fun a => by field_simp
  have hmin : ∀ a : ℝ, min (c * u) a = c * min u (a / c) := fun a => by
    rw [mul_min_of_nonneg _ _ hc.le, hcancel]
  rw [hmin (τ j.succ), hmin (τ j.castSucc)]
  split_ifs with hp
  · rw [← mul_sub, mul_comm, mul_div_assoc, div_self hc0, mul_one]
  · simp

/-- The change of variables maps the schedule class on `[0, T]` to the schedule class on
`[0, T / c]`, with the same block budget. -/
theorem rescale_isSchedule {c T : ℝ} (hc : 0 < c) {k : ℕ} {W : Fin n → ℝ → ℝ}
    (h : IsSchedule k T W) : IsSchedule k (T / c) (rescale c W) := by
  obtain ⟨p, τ, hτ, rfl⟩ := h
  refine ⟨p, fun m => τ m / c, ⟨?_, ?_, ?_⟩, rescale_occupation hc p τ⟩
  · rw [hτ.first]; simp
  · rw [hτ.last]
  · exact fun a b hab => (div_le_div_iff_of_pos_right hc).mpr (hτ.mono hab)

/-- SC08: the change of variables divides the full error by `c`. -/
theorem D_rescale (hn : 0 < n) {c T : ℝ} (hc : 0 < c) {A W : Fin n → ℝ → ℝ}
    (hA : IsCumulative A T) (hW : IsCumulative W T) (hT : 0 ≤ T) :
    D (rescale c A) (rescale c W) (T / c) = D A W T / c := by
  have hc0 : c ≠ 0 := ne_of_gt hc
  have hTc : c * (T / c) = T := by field_simp
  have hTc' : (0 : ℝ) ≤ T / c := div_nonneg hT hc.le
  have hcancel : ∀ a : ℝ, c * (a / c) = a := fun a => by field_simp
  have hmem : ∀ u ∈ Icc (0 : ℝ) (T / c), c * u ∈ Icc (0 : ℝ) T := fun u hu =>
    ⟨mul_nonneg hc.le hu.1, hTc ▸ mul_le_mul_of_nonneg_left hu.2 hc.le⟩
  have hmem' : ∀ t ∈ Icc (0 : ℝ) T, t / c ∈ Icc (0 : ℝ) (T / c) := fun t ht =>
    ⟨div_nonneg ht.1 hc.le, (div_le_div_iff_of_pos_right hc).mpr ht.2⟩
  have hA' := rescale_isCumulative hc hA
  have hW' := rescale_isCumulative hc hW
  refine le_antisymm ?_ ?_
  · refine D_le (div_nonneg (D_nonneg hn hA hW hT) hc.le) fun i u hu => ?_
    simp only [rescale, ← sub_div, abs_div, abs_of_pos hc]
    exact (div_le_div_iff_of_pos_right hc).mpr (le_D hA hW i (hmem u hu))
  · have hstep : D A W T ≤ c * D (rescale c A) (rescale c W) (T / c) := by
      refine D_le (mul_nonneg hc.le (D_nonneg hn hA' hW' hTc')) fun i t ht => ?_
      have e1 : rescale c A i (t / c) = A i t / c := by
        simp only [rescale]; rw [hcancel t]
      have e2 : rescale c W i (t / c) = W i t / c := by
        simp only [rescale]; rw [hcancel t]
      have key : |A i t - W i t| = c * |rescale c A i (t / c) - rescale c W i (t / c)| := by
        rw [e1, e2, ← sub_div, abs_div, abs_of_pos hc]
        field_simp
      rw [key]
      exact mul_le_mul_of_nonneg_left (le_D hA' hW' i (hmem' t ht)) hc.le
    calc D A W T / c ≤ (c * D (rescale c A) (rescale c W) (T / c)) / c :=
          (div_le_div_iff_of_pos_right hc).mpr hstep
      _ = D (rescale c A) (rescale c W) (T / c) := by field_simp

/-- SC08: the change of variables divides the continuous instance optimum by `c`. -/
theorem OPT_rescale (hn : 0 < n) {c T : ℝ} (hc : 0 < c) {A : Fin n → ℝ → ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) (s : ℕ) :
    OPT (rescale c A) (T / c) s = OPT A T s / c := by
  have hc0 : c ≠ 0 := ne_of_gt hc
  have hTc' : (0 : ℝ) ≤ T / c := div_nonneg hT hc.le
  have hcancel : ∀ a : ℝ, c * (a / c) = a := fun a => by field_simp
  have hA' := rescale_isCumulative hc hA
  have hcinv : (0 : ℝ) < 1 / c := by positivity
  refine le_antisymm ?_ ?_
  · have h : c * OPT (rescale c A) (T / c) s ≤ OPT A T s := by
      refine le_csInf (scheduleErrorSet_nonempty hn hT (Nat.succ_pos s)) ?_
      rintro e ⟨W, hW, rfl⟩
      have h1 : OPT (rescale c A) (T / c) s ≤ D (rescale c A) (rescale c W) (T / c) :=
        OPT_le_D hn hA' hTc' (rescale_isSchedule hc hW)
      rw [D_rescale hn hc hA hW.isCumulative hT] at h1
      have h2 := mul_le_mul_of_nonneg_left h1 hc.le
      rwa [hcancel (D A W T)] at h2
    calc OPT (rescale c A) (T / c) s = (c * OPT (rescale c A) (T / c) s) / c := by field_simp
      _ ≤ OPT A T s / c := (div_le_div_iff_of_pos_right hc).mpr h
  · refine le_csInf (scheduleErrorSet_nonempty hn hTc' (Nat.succ_pos s)) ?_
    rintro e ⟨V, hV, rfl⟩
    have hWs : IsSchedule (s + 1) T (rescale (1 / c) V) := by
      have h := rescale_isSchedule hcinv hV
      rwa [show T / c / (1 / c) = T by field_simp] at h
    have hVeq : rescale c (rescale (1 / c) V) = V := rescale_inv hc V
    have hD : D (rescale c A) V (T / c) = D A (rescale (1 / c) V) T / c := by
      conv_lhs => rw [← hVeq]
      exact D_rescale hn hc hA hWs.isCumulative hT
    rw [hD]
    exact (div_le_div_iff_of_pos_right hc).mpr (OPT_le_D hn hA hT hWs)

/-- SC08: the change of variables divides the minimax value by `c`. -/
theorem F_rescale (hn : 0 < n) {c T : ℝ} (hc : 0 < c) (hT : 0 ≤ T) (s : ℕ) :
    F n s (T / c) = F n s T / c := by
  have hc0 : c ≠ 0 := ne_of_gt hc
  have hTc' : (0 : ℝ) ≤ T / c := div_nonneg hT hc.le
  have hcinv : (0 : ℝ) < 1 / c := by positivity
  refine le_antisymm ?_ ?_
  · refine F_le (div_nonneg (F_nonneg hn s hT) hc.le) fun B hB => ?_
    have hA : IsCumulative (rescale (1 / c) B) T := by
      have h := rescale_isCumulative hcinv hB
      rwa [show T / c / (1 / c) = T by field_simp] at h
    have hBeq : rescale c (rescale (1 / c) B) = B := rescale_inv hc B
    have hOPT : OPT B (T / c) s = OPT (rescale (1 / c) B) T s / c := by
      conv_lhs => rw [← hBeq]
      exact OPT_rescale hn hc hA hT s
    rw [hOPT]
    exact (div_le_div_iff_of_pos_right hc).mpr (OPT_le_F hn hA hT s)
  · have h : F n s T ≤ c * F n s (T / c) := by
      refine F_le (mul_nonneg hc.le (F_nonneg hn s hTc')) fun A hA => ?_
      have hstep : OPT A T s = c * OPT (rescale c A) (T / c) s := by
        rw [OPT_rescale hn hc hA hT s]; field_simp
      rw [hstep]
      exact mul_le_mul_of_nonneg_left
        (OPT_le_F hn (rescale_isCumulative hc hA) hTc' s) hc.le
    calc F n s T / c ≤ (c * F n s (T / c)) / c := (div_le_div_iff_of_pos_right hc).mpr h
      _ = F n s (T / c) := by field_simp

/-- SC08, `eq:scaling`: `F_{n,s}(T) = T F_{n,s}(1)` for a positive horizon. -/
theorem F_scaling (hn : 0 < n) {T : ℝ} (hT : 0 < T) (s : ℕ) : F n s T = T * F n s 1 := by
  have h := F_rescale hn hT hT.le s
  rw [div_self (ne_of_gt hT)] at h
  rw [h]
  field_simp

/-! ## SC07, step 4 (continuous case): attainment of the minimax value `F`

The cumulative class `Acal_n(T)` is realized as a set of bounded continuous maps on the
compact horizon `Icc 0 T`. It is closed, equicontinuous (every member is `1`-Lipschitz) and
pointwise contained in a compact box, so the Arzelà–Ascoli theorem
`BoundedContinuousFunction.arzela_ascoli₂` makes it compact in the uniform norm. -/

/-- The input read off a bounded continuous map on the horizon, extended by zero outside. Only
the values on `Icc 0 T` matter for any of the errors. -/
noncomputable def ofBCF {T : ℝ} (f : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ)) : Fin n → ℝ → ℝ :=
  fun i t => if h : t ∈ Icc (0 : ℝ) T then f ⟨t, h⟩ i else 0

theorem ofBCF_apply {T : ℝ} (f : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ)) (i : Fin n) {t : ℝ}
    (ht : t ∈ Icc (0 : ℝ) T) : ofBCF f i t = f ⟨t, ht⟩ i := dif_pos ht

theorem ofBCF_coe {T : ℝ} (f : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ)) (i : Fin n)
    (y : ↥(Icc (0 : ℝ) T)) : ofBCF f i (y : ℝ) = f y i := dif_pos y.2

/-- Reading off a value at a fixed time is continuous in the uniform norm. -/
theorem continuous_ofBCF_apply {T : ℝ} (i : Fin n) (t : ℝ) :
    Continuous fun f : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ) => ofBCF f i t := by
  by_cases h : t ∈ Icc (0 : ℝ) T
  · simp only [ofBCF, dif_pos h]
    exact (continuous_apply i).comp (continuous_eval_const _)
  · simp only [ofBCF, dif_neg h]
    exact continuous_const

/-- Two inputs that agree on the horizon are both cumulative or neither is. -/
theorem isCumulative_congr {A B : Fin n → ℝ → ℝ} {T : ℝ} (hT : 0 ≤ T)
    (hA : IsCumulative A T) (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, A i t = B i t) :
    IsCumulative B T where
  initial i := by rw [← h i 0 ⟨le_rfl, hT⟩]; exact hA.initial i
  mono i a b ha hab hb := by
    rw [← h i a ⟨ha, hab.trans hb⟩, ← h i b ⟨ha.trans hab, hb⟩]
    exact hA.mono i a b ha hab hb
  lipschitz i a b ha hab hb := by
    rw [← h i a ⟨ha, hab.trans hb⟩, ← h i b ⟨ha.trans hab, hb⟩]
    exact hA.lipschitz i a b ha hab hb
  conservation t ht := by
    rw [← Finset.sum_congr rfl fun i _ => h i t ht]
    exact hA.conservation t ht

/-- The continuous instance optimum depends only on the values of the input on the horizon. -/
theorem OPT_congr (hn : 0 < n) {A B : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hB : IsCumulative B T) (hT : 0 ≤ T) (s : ℕ)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, A i t = B i t) : OPT A T s = OPT B T s := by
  have h0 : |OPT A T s - OPT B T s| ≤ 0 :=
    abs_OPT_sub_OPT_le hn hA hB hT s fun i t ht => by rw [h i t ht, sub_self, abs_zero]
  exact sub_eq_zero.mp (abs_eq_zero.mp (le_antisymm h0 (abs_nonneg _)))

/-- The cumulative class realized inside the bounded continuous maps on the horizon. -/
def bcfCumulativeSet (n : ℕ) (T : ℝ) : Set (↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ)) :=
  {f | IsCumulative (ofBCF f) T}

@[simp] theorem mem_bcfCumulativeSet {T : ℝ} {f : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ)} :
    f ∈ bcfCumulativeSet n T ↔ IsCumulative (ofBCF f) T := Iff.rfl

/-- The realized cumulative class is closed: all four defining conditions are pointwise
closed conditions. -/
theorem isClosed_bcfCumulativeSet (n : ℕ) (T : ℝ) : IsClosed (bcfCumulativeSet n T) := by
  have hset : bcfCumulativeSet n T =
      ((⋂ i : Fin n, {f : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ) | ofBCF f i 0 = 0}) ∩
        ⋂ (i : Fin n) (a : ℝ) (b : ℝ) (_ : 0 ≤ a) (_ : a ≤ b) (_ : b ≤ T),
          {f : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ) | ofBCF f i a ≤ ofBCF f i b}) ∩
      ((⋂ (i : Fin n) (a : ℝ) (b : ℝ) (_ : 0 ≤ a) (_ : a ≤ b) (_ : b ≤ T),
          {f : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ) | ofBCF f i b - ofBCF f i a ≤ b - a}) ∩
        ⋂ (t : ℝ) (_ : t ∈ Icc (0 : ℝ) T),
          {f : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ) | ∑ i, ofBCF f i t = t}) := by
    ext f
    simp only [mem_bcfCumulativeSet, mem_inter_iff, mem_iInter, mem_ofPred_eq]
    constructor
    · intro hf
      exact ⟨⟨fun i => hf.initial i, fun i a b h1 h2 h3 => hf.mono i a b h1 h2 h3⟩,
        fun i a b h1 h2 h3 => hf.lipschitz i a b h1 h2 h3, fun t ht => hf.conservation t ht⟩
    · rintro ⟨⟨h1, h2⟩, h3, h4⟩
      exact ⟨h1, h2, h3, h4⟩
  rw [hset]
  refine IsClosed.inter (IsClosed.inter ?_ ?_) (IsClosed.inter ?_ ?_)
  · exact isClosed_iInter fun i =>
      isClosed_eq (continuous_ofBCF_apply i 0) continuous_const
  · exact isClosed_iInter fun i => isClosed_iInter fun a => isClosed_iInter fun b =>
      isClosed_iInter fun _ => isClosed_iInter fun _ => isClosed_iInter fun _ =>
        isClosed_le (continuous_ofBCF_apply i a) (continuous_ofBCF_apply i b)
  · exact isClosed_iInter fun i => isClosed_iInter fun a => isClosed_iInter fun b =>
      isClosed_iInter fun _ => isClosed_iInter fun _ => isClosed_iInter fun _ =>
        isClosed_le ((continuous_ofBCF_apply i b).sub (continuous_ofBCF_apply i a))
          continuous_const
  · exact isClosed_iInter fun t => isClosed_iInter fun _ =>
      isClosed_eq (continuous_finsetSum _ fun i _ => continuous_ofBCF_apply i t)
        continuous_const

/-- Members of the realized cumulative class are `1`-Lipschitz, uniformly. -/
theorem bcfCumulativeSet_dist_le {T : ℝ} {f : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ)}
    (hf : f ∈ bcfCumulativeSet n T) (u v : ↥(Icc (0 : ℝ) T)) :
    dist (f u) (f v) ≤ dist u v := by
  rw [dist_pi_le_iff dist_nonneg]
  intro i
  rw [Real.dist_eq, Subtype.dist_eq, Real.dist_eq, ← ofBCF_coe f i u, ← ofBCF_coe f i v]
  exact abs_sub_le_of_isCumulative hf i u.2 v.2

/-- The realized cumulative class is equicontinuous. -/
theorem equicontinuous_bcfCumulativeSet (n : ℕ) (T : ℝ) :
    Equicontinuous fun g : ↥(bcfCumulativeSet n T) =>
      ⇑(g : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ)) := by
  intro y₀
  rw [Metric.equicontinuousAt_iff]
  intro ε hε
  refine ⟨ε, hε, fun y hy g => ?_⟩
  exact lt_of_le_of_lt ((bcfCumulativeSet_dist_le g.2 y₀ y).trans_eq (dist_comm _ _)) hy

/-- SC07: the cumulative class is compact in the uniform norm. -/
theorem isCompact_bcfCumulativeSet (n : ℕ) (T : ℝ) :
    IsCompact (bcfCumulativeSet n T) := by
  refine BoundedContinuousFunction.arzela_ascoli₂
    (Set.univ.pi fun _ : Fin n => Icc (0 : ℝ) T) (isCompact_univ_pi fun _ => isCompact_Icc)
    _ (isClosed_bcfCumulativeSet n T) (fun f y hf i _ => ?_)
    (equicontinuous_bcfCumulativeSet n T)
  have hc : IsCumulative (ofBCF f) T := hf
  rw [← ofBCF_coe f i y]
  exact ⟨hc.nonneg i y.2, (hc.le_self i y.2).trans y.2.2⟩

/-- SC07: the minimax value `F_{n,s}(T)` is attained by a cumulative input. -/
theorem exists_F_eq (hn : 0 < n) {T : ℝ} (hT : 0 ≤ T) (s : ℕ) :
    ∃ A : Fin n → ℝ → ℝ, IsCumulative A T ∧ F n s T = OPT A T s := by
  have himg : minimaxSet n s T =
      (fun f : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ) => OPT (ofBCF f) T s) ''
        bcfCumulativeSet n T := by
    ext v
    simp only [mem_minimaxSet, mem_image, mem_bcfCumulativeSet]
    constructor
    · rintro ⟨A, hA, rfl⟩
      have hcont : Continuous fun y : ↥(Icc (0 : ℝ) T) => fun i : Fin n => A i (y : ℝ) :=
        continuous_pi fun i => (continuousOn_of_isCumulative hA i).domRestrict
      refine ⟨BoundedContinuousFunction.mkOfCompact
        (ContinuousMap.mk (fun y : ↥(Icc (0 : ℝ) T) => fun i : Fin n => A i (y : ℝ)) hcont),
        ?_, ?_⟩
      · refine isCumulative_congr hT hA fun i t ht => ?_
        rw [ofBCF_apply _ i ht]
        rfl
      · refine (OPT_congr hn hA ?_ hT s fun i t ht => ?_).symm
        · refine isCumulative_congr hT hA fun i t ht => ?_
          rw [ofBCF_apply _ i ht]
          rfl
        · rw [ofBCF_apply _ i ht]
          rfl
    · rintro ⟨f, hf, rfl⟩
      exact ⟨ofBCF f, hf, rfl⟩
  have hcont : ContinuousOn
      (fun f : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ) => OPT (ofBCF f) T s)
      (bcfCumulativeSet n T) := by
    refine LipschitzOnWith.continuousOn (K := 1) (LipschitzOnWith.of_dist_le_mul ?_)
    intro f hf g hg
    have hb : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |ofBCF f i t - ofBCF g i t| ≤ dist f g := by
      intro i t ht
      rw [ofBCF_apply f i ht, ofBCF_apply g i ht, ← Real.dist_eq]
      exact (dist_le_pi_dist (f ⟨t, ht⟩) (g ⟨t, ht⟩) i).trans
        (BoundedContinuousFunction.dist_coe_le_dist (f := f) (g := g)
          (⟨t, ht⟩ : ↥(Icc (0 : ℝ) T)))
    simpa [Real.dist_eq] using abs_OPT_sub_OPT_le hn hf hg hT s hb
  have hcomp := (isCompact_bcfCumulativeSet n T).image_of_continuousOn hcont
  obtain ⟨f, hf, hv⟩ := hcomp.sSup_mem (himg ▸ minimaxSet_nonempty hn s)
  refine ⟨ofBCF f, hf, ?_⟩
  rw [F_eq_sSup, himg]
  exact hv.symm

/-! ## The one-sided minimax value `G⁻`

The one-sided criterion is treated by the same arguments; `G⁻` is indexed by activation
blocks. -/

/-- Every schedule bounds the one-sided instance optimum from above. -/
theorem OPTminus_le_Dminus (hn : 0 < n) {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) {k : ℕ} (hW : IsSchedule k T W) : OPTminus A T k ≤ Dminus A W T :=
  csInf_le (scheduleLowerErrorSet_bddBelow hn hA hT _) ⟨W, hW, rfl⟩

/-- A bound valid for every schedule bounds the one-sided instance optimum from below. -/
theorem le_OPTminus (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T c : ℝ} (hT : 0 ≤ T) {k : ℕ}
    (hk : 0 < k) (h : ∀ W : Fin n → ℝ → ℝ, IsSchedule k T W → c ≤ Dminus A W T) :
    c ≤ OPTminus A T k := by
  refine le_csInf (scheduleLowerErrorSet_nonempty hn hT hk) ?_
  rintro e ⟨W, hW, rfl⟩
  exact h W hW

/-- The one-sided instance optimum never exceeds the horizon. -/
theorem OPTminus_le_horizon (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) {k : ℕ} (hk : 0 < k) : OPTminus A T k ≤ T := by
  obtain ⟨W, hW⟩ := exists_isSchedule hn hT hk
  exact (OPTminus_le_Dminus hn hA hT hW).trans
    (Dminus_le_horizon hA hW.isCumulative hT)

/-- The one-sided instance optimum is nonnegative. -/
theorem OPTminus_nonneg (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) {k : ℕ} (hk : 0 < k) : 0 ≤ OPTminus A T k :=
  le_OPTminus hn hT hk fun _W hW => Dminus_nonneg hn hA hW.isCumulative hT

/-- The set maximized by `Gminus`. -/
def minimaxLowerSet (n k : ℕ) (T : ℝ) : Set ℝ :=
  {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsCumulative A T ∧ v = OPTminus A T k}

@[simp] theorem mem_minimaxLowerSet {n k : ℕ} {T v : ℝ} :
    v ∈ minimaxLowerSet n k T ↔
      ∃ A : Fin n → ℝ → ℝ, IsCumulative A T ∧ v = OPTminus A T k := Iff.rfl

theorem Gminus_eq_sSup (n k : ℕ) (T : ℝ) : Gminus n k T = sSup (minimaxLowerSet n k T) := rfl

/-- The set maximized by `Gminus` is nonempty. -/
theorem minimaxLowerSet_nonempty (hn : 0 < n) {T : ℝ} (k : ℕ) :
    (minimaxLowerSet n k T).Nonempty :=
  ⟨_, uniformCumulative n, isCumulative_uniformCumulative hn T, rfl⟩

/-- The set maximized by `Gminus` is bounded above by the horizon. -/
theorem minimaxLowerSet_bddAbove (hn : 0 < n) {T : ℝ} {k : ℕ} (hk : 0 < k) (hT : 0 ≤ T) :
    BddAbove (minimaxLowerSet n k T) := by
  refine ⟨T, ?_⟩
  rintro v ⟨A, hA, rfl⟩
  exact OPTminus_le_horizon hn hA hT hk

/-- Every cumulative input bounds the one-sided minimax value from below. -/
theorem OPTminus_le_Gminus (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) {k : ℕ} (hk : 0 < k) : OPTminus A T k ≤ Gminus n k T :=
  le_csSup (minimaxLowerSet_bddAbove hn hk hT) ⟨A, hA, rfl⟩

/-- A bound valid for every cumulative input bounds the one-sided minimax value from above. -/
theorem Gminus_le {T c : ℝ} {k : ℕ} (hc : 0 ≤ c)
    (h : ∀ A : Fin n → ℝ → ℝ, IsCumulative A T → OPTminus A T k ≤ c) : Gminus n k T ≤ c := by
  refine Real.sSup_le (fun v hv => ?_) hc
  obtain ⟨A, hA, rfl⟩ := hv
  exact h A hA

/-- The one-sided minimax value is nonnegative. -/
theorem Gminus_nonneg (hn : 0 < n) {T : ℝ} {k : ℕ} (hk : 0 < k) (hT : 0 ≤ T) :
    0 ≤ Gminus n k T :=
  le_trans (OPTminus_nonneg hn (isCumulative_uniformCumulative hn T) hT hk)
    (OPTminus_le_Gminus hn (isCumulative_uniformCumulative hn T) hT hk)

/-- SC08: enlarging the block budget cannot increase the one-sided minimax value. -/
theorem Gminus_mono_budget (hn : 0 < n) {T : ℝ} (hT : 0 ≤ T) {k k' : ℕ} (hk : 0 < k)
    (hkk : k ≤ k') : Gminus n k' T ≤ Gminus n k T :=
  Gminus_le (Gminus_nonneg hn hk hT) fun _A hA =>
    (OPTminus_mono_budget hn hA hT hk hkk).trans (OPTminus_le_Gminus hn hA hT hk)

/-- The one-sided instance optimum depends only on the values of the input on the horizon. -/
theorem OPTminus_congr (hn : 0 < n) {A B : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hB : IsCumulative B T) (hT : 0 ≤ T) {k : ℕ} (hk : 0 < k)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, A i t = B i t) : OPTminus A T k = OPTminus B T k := by
  have h0 : |OPTminus A T k - OPTminus B T k| ≤ 0 :=
    abs_OPTminus_sub_OPTminus_le hn hA hB hT hk fun i t ht => by
      rw [h i t ht, sub_self, abs_zero]
  exact sub_eq_zero.mp (abs_eq_zero.mp (le_antisymm h0 (abs_nonneg _)))

/-- SC07: the one-sided minimax value `G⁻_{n,k}(T)` is attained by a cumulative input. -/
theorem exists_Gminus_eq (hn : 0 < n) {T : ℝ} (hT : 0 ≤ T) {k : ℕ} (hk : 0 < k) :
    ∃ A : Fin n → ℝ → ℝ, IsCumulative A T ∧ Gminus n k T = OPTminus A T k := by
  have himg : minimaxLowerSet n k T =
      (fun f : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ) => OPTminus (ofBCF f) T k) ''
        bcfCumulativeSet n T := by
    ext v
    simp only [mem_minimaxLowerSet, mem_image, mem_bcfCumulativeSet]
    constructor
    · rintro ⟨A, hA, rfl⟩
      have hcont : Continuous fun y : ↥(Icc (0 : ℝ) T) => fun i : Fin n => A i (y : ℝ) :=
        continuous_pi fun i => (continuousOn_of_isCumulative hA i).domRestrict
      have hagree : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T,
          A i t = ofBCF (BoundedContinuousFunction.mkOfCompact
            (ContinuousMap.mk (fun y : ↥(Icc (0 : ℝ) T) => fun i : Fin n => A i (y : ℝ))
              hcont)) i t := by
        intro i t ht
        rw [ofBCF_apply _ i ht]
        rfl
      refine ⟨BoundedContinuousFunction.mkOfCompact
        (ContinuousMap.mk (fun y : ↥(Icc (0 : ℝ) T) => fun i : Fin n => A i (y : ℝ)) hcont),
        isCumulative_congr hT hA hagree,
        (OPTminus_congr hn hA (isCumulative_congr hT hA hagree) hT hk hagree).symm⟩
    · rintro ⟨f, hf, rfl⟩
      exact ⟨ofBCF f, hf, rfl⟩
  have hcont : ContinuousOn
      (fun f : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ) => OPTminus (ofBCF f) T k)
      (bcfCumulativeSet n T) := by
    refine LipschitzOnWith.continuousOn (K := 1) (LipschitzOnWith.of_dist_le_mul ?_)
    intro f hf g hg
    have hb : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |ofBCF f i t - ofBCF g i t| ≤ dist f g := by
      intro i t ht
      rw [ofBCF_apply f i ht, ofBCF_apply g i ht, ← Real.dist_eq]
      exact (dist_le_pi_dist (f ⟨t, ht⟩) (g ⟨t, ht⟩) i).trans
        (BoundedContinuousFunction.dist_coe_le_dist (f := f) (g := g)
          (⟨t, ht⟩ : ↥(Icc (0 : ℝ) T)))
    simpa [Real.dist_eq] using abs_OPTminus_sub_OPTminus_le hn hf hg hT hk hb
  have hcomp := (isCompact_bcfCumulativeSet n T).image_of_continuousOn hcont
  obtain ⟨f, hf, hv⟩ := hcomp.sSup_mem (himg ▸ minimaxLowerSet_nonempty hn k)
  refine ⟨ofBCF f, hf, ?_⟩
  rw [Gminus_eq_sSup, himg]
  exact hv.symm

/-! ## SC08 on grids: budget monotonicity for the grid optima -/

/-- Budget monotonicity for grid schedules, one step: append a zero-length final block at the
last grid point. -/
theorem IsGridSchedule.succ (hn : 0 < n) {x : Fin (N + 1) → ℝ} {k : ℕ} {W : Fin n → ℝ → ℝ}
    (h : IsGridSchedule x k W) : IsGridSchedule x (k + 1) W := by
  obtain ⟨p, g, hg, hg0, hgl, rfl⟩ := h
  have hcast : (Fin.snoc g (Fin.last N) : Fin (k + 2) → Fin (N + 1)) (Fin.last k).castSucc
      = Fin.last N := by rw [Fin.snoc_castSucc]; exact hgl
  have hsucc : (Fin.snoc g (Fin.last N) : Fin (k + 2) → Fin (N + 1)) (Fin.last k).succ
      = Fin.last N := by rw [Fin.succ_last, Fin.snoc_last]
  refine ⟨Fin.snoc p ⟨0, hn⟩, Fin.snoc g (Fin.last N), ?_, ?_, ?_, ?_⟩
  · refine Fin.monotone_iff_le_succ.mpr fun j => ?_
    refine Fin.lastCases ?_ ?_ j
    · rw [hcast, hsucc]
    · intro j0
      rw [Fin.snoc_castSucc, Fin.succ_castSucc, Fin.snoc_castSucc]
      exact hg (Fin.castSucc_le_succ j0)
  · rw [← Fin.castSucc_zero, Fin.snoc_castSucc]; exact hg0
  · exact Fin.snoc_last _ _
  · funext i t
    simp only [occupation, Function.comp_apply]
    rw [Fin.sum_univ_castSucc, hcast, hsucc, sub_self, ite_self, add_zero]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [Fin.snoc_castSucc, Fin.succ_castSucc, Fin.snoc_castSucc, Fin.snoc_castSucc]

/-- Budget monotonicity: enlarging the block budget enlarges the grid schedule class. -/
theorem IsGridSchedule.mono (hn : 0 < n) {x : Fin (N + 1) → ℝ} {k k' : ℕ} {W : Fin n → ℝ → ℝ}
    (hkk : k ≤ k') (h : IsGridSchedule x k W) : IsGridSchedule x k' W := by
  obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hkk
  induction d with
  | zero => simpa using h
  | succ d ih => exact (ih (by omega)).succ hn

/-- SC08: enlarging the switch budget cannot increase the grid instance optimum. -/
theorem gridOPT_mono_budget (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T) {s s' : ℕ} (hs : s ≤ s') :
    gridOPT x A T s' ≤ gridOPT x A T s := by
  refine csInf_le_csInf (gridScheduleErrorSet_bddBelow hn hx hA hT _)
    (gridScheduleErrorSet_nonempty hn A T (Nat.succ_pos s)) ?_
  rintro e ⟨W, hW, rfl⟩
  exact ⟨W, IsGridSchedule.mono hn (by omega) hW, rfl⟩

/-- SC08: enlarging the block budget cannot increase the one-sided grid instance optimum. -/
theorem gridOPTminus_mono_budget (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T) {k k' : ℕ} (hk : 0 < k)
    (hkk : k ≤ k') : gridOPTminus x A T k' ≤ gridOPTminus x A T k := by
  refine csInf_le_csInf (gridScheduleLowerErrorSet_bddBelow hn hx hA hT _)
    (gridScheduleLowerErrorSet_nonempty hn A T hk) ?_
  rintro e ⟨W, hW, rfl⟩
  exact ⟨W, IsGridSchedule.mono hn hkk hW, rfl⟩

/-- The grid instance optimum is nonnegative. -/
theorem gridOPT_nonneg (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T) (s : ℕ) :
    0 ≤ gridOPT x A T s :=
  le_gridOPT hn fun _W hW => D_nonneg hn hA (hW.isSchedule hx).isCumulative hT

/-- The grid minimax value is nonnegative. -/
theorem gridF_nonneg (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T) (s : ℕ) :
    0 ≤ gridF x n s T := by
  have hT : (0 : ℝ) ≤ T := nonneg_of_isGrid hx
  have hr := isRateMatrix_uniform (n := n) hn N
  have hA := gridCumulative_isCumulative hx.orderedTimes hr
  exact (gridOPT_nonneg hn hx hA hT s).trans
    (le_csSup (gridMinimaxSet_bddAbove hn hx s) ⟨_, ⟨_, hr, rfl⟩, rfl⟩)

/-- SC08: enlarging the switch budget cannot increase the grid minimax value. -/
theorem gridF_mono_budget (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {s s' : ℕ} (hs : s ≤ s') : gridF x n s' T ≤ gridF x n s T := by
  refine Real.sSup_le (fun v hv => ?_) (gridF_nonneg hn hx s)
  obtain ⟨A, ⟨r, hr, rfl⟩, rfl⟩ := hv
  have hA := gridCumulative_isCumulative hx.orderedTimes hr
  exact (gridOPT_mono_budget hn hx hA (nonneg_of_isGrid hx) hs).trans
    (le_csSup (gridMinimaxSet_bddAbove hn hx s) ⟨_, ⟨r, hr, rfl⟩, rfl⟩)

/-- The one-sided grid instance optimum is nonnegative. -/
theorem gridOPTminus_nonneg (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T) {k : ℕ} (hk : 0 < k) :
    0 ≤ gridOPTminus x A T k := by
  refine le_csInf (gridScheduleLowerErrorSet_nonempty hn A T hk) ?_
  rintro e ⟨W, hW, rfl⟩
  exact Dminus_nonneg hn hA (hW.isSchedule hx).isCumulative hT

/-- The set maximized by `gridGminus`. -/
def gridMinimaxLowerSet (x : Fin (N + 1) → ℝ) (n k : ℕ) (T : ℝ) : Set ℝ :=
  {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧ v = gridOPTminus x A T k}

theorem gridGminus_eq_sSup (x : Fin (N + 1) → ℝ) (n k : ℕ) (T : ℝ) :
    gridGminus x n k T = sSup (gridMinimaxLowerSet x n k T) := rfl

/-- The set maximized by `gridGminus` is bounded above by the horizon. -/
theorem gridMinimaxLowerSet_bddAbove (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {k : ℕ} (hk : 0 < k) : BddAbove (gridMinimaxLowerSet x n k T) := by
  refine ⟨T, ?_⟩
  rintro v ⟨A, ⟨r, hr, rfl⟩, rfl⟩
  exact gridOPTminus_le_horizon hn hx (gridCumulative_isCumulative hx.orderedTimes hr) hk

/-- The one-sided grid minimax value is nonnegative. -/
theorem gridGminus_nonneg (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {k : ℕ} (hk : 0 < k) : 0 ≤ gridGminus x n k T := by
  have hr := isRateMatrix_uniform (n := n) hn N
  have hA := gridCumulative_isCumulative hx.orderedTimes hr
  exact (gridOPTminus_nonneg hn hx hA (nonneg_of_isGrid hx) hk).trans
    (le_csSup (gridMinimaxLowerSet_bddAbove hn hx hk) ⟨_, ⟨_, hr, rfl⟩, rfl⟩)

/-- SC08: enlarging the block budget cannot increase the one-sided grid minimax value. -/
theorem gridGminus_mono_budget (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {k k' : ℕ} (hk : 0 < k) (hkk : k ≤ k') :
    gridGminus x n k' T ≤ gridGminus x n k T := by
  refine Real.sSup_le (fun v hv => ?_) (gridGminus_nonneg hn hx hk)
  obtain ⟨A, ⟨r, hr, rfl⟩, rfl⟩ := hv
  have hA := gridCumulative_isCumulative hx.orderedTimes hr
  exact (gridOPTminus_mono_budget hn hx hA (nonneg_of_isGrid hx) hk hkk).trans
    (le_csSup (gridMinimaxLowerSet_bddAbove hn hx hk) ⟨_, ⟨r, hr, rfl⟩, rfl⟩)

/-! ## SC07: compactness of the schedule class in the uniform norm

`prop:compactness` asserts that `Acal_n(T)` *and* `Wcal_{n,k}(T)` are compact in the uniform
norm `‖A‖_∞ = max_i max_{t ∈ [0,T]} |A_i(t)|`. The first half is
`isCompact_bcfCumulativeSet`; this section supplies the second half in the same bounded
continuous function space.

A remark on the formulation. For the cumulative class the naive predicate
`IsCumulative (ofBCF f) T` is the right one, because all four conditions of `IsCumulative` are
confined to the horizon and are unaffected by the extension of `ofBCF` by zero outside it. For
the schedule class this is not so: `IsSchedule k T V` asserts the *global* identity
`V = occupation p τ` on all of `ℝ`, and `occupation p τ i t` is generally nonzero for `t > T`,
so `IsSchedule k T (ofBCF W)` would be satisfied by almost no `W`. The class is therefore
realized as the set of bounded continuous maps on the horizon that agree there with a
schedule, which is exactly `Wcal_{n,k}(T)` seen through the uniform norm. -/

/-- Each coordinate of a cumulative occupation is continuous. -/
theorem continuous_occupation {k : ℕ} (p : Fin k → Fin n) (τ : Fin (k + 1) → ℝ) (i : Fin n) :
    Continuous (occupation p τ i) := by
  have hfun : occupation p τ i = fun t : ℝ => ∑ j : Fin k,
      if p j = i then min t (τ j.succ) - min t (τ j.castSucc) else 0 := rfl
  rw [hfun]
  refine continuous_finsetSum _ fun j _ => ?_
  by_cases hp : p j = i
  · simp only [if_pos hp]
    exact (continuous_id.min continuous_const).sub (continuous_id.min continuous_const)
  · simp only [if_neg hp]
    exact continuous_const

/-- The cumulative occupation of a word and its switch times, as a bounded continuous map on
the horizon. -/
noncomputable def bcfOccupation {k : ℕ} (T : ℝ) (p : Fin k → Fin n) (τ : Fin (k + 1) → ℝ) :
    ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ) :=
  BoundedContinuousFunction.mkOfCompact
    (ContinuousMap.mk (fun y : ↥(Icc (0 : ℝ) T) => fun i : Fin n => occupation p τ i (y : ℝ))
      (continuous_pi fun i => (continuous_occupation p τ i).comp continuous_subtype_val))

@[simp] theorem bcfOccupation_apply {k : ℕ} (T : ℝ) (p : Fin k → Fin n)
    (τ : Fin (k + 1) → ℝ) (y : ↥(Icc (0 : ℝ) T)) (i : Fin n) :
    bcfOccupation T p τ y i = occupation p τ i (y : ℝ) := rfl

/-- SC07: the uniform-norm form of the switch-time Lipschitz estimate
`abs_occupation_sub_occupation_le`. No hypothesis on the switch times is needed. -/
theorem dist_bcfOccupation_le {k : ℕ} (T : ℝ) (p : Fin k → Fin n) (τ τ' : Fin (k + 1) → ℝ) :
    dist (bcfOccupation T p τ) (bcfOccupation T p τ') ≤ ∑ m : Fin (k + 1), |τ m - τ' m| := by
  have hnn : (0 : ℝ) ≤ ∑ m : Fin (k + 1), |τ m - τ' m| :=
    Finset.sum_nonneg fun m _ => abs_nonneg _
  refine (BoundedContinuousFunction.dist_le hnn).mpr fun y => ?_
  rw [dist_pi_le_iff hnn]
  intro i
  rw [Real.dist_eq, bcfOccupation_apply, bcfOccupation_apply]
  exact abs_occupation_sub_occupation_le p τ τ' i (y : ℝ)

/-- The cumulative occupation depends continuously on the switch times, in the uniform norm. -/
theorem continuous_bcfOccupation {k : ℕ} (T : ℝ) (p : Fin k → Fin n) :
    Continuous fun τ : Fin (k + 1) → ℝ => bcfOccupation T p τ := by
  refine LipschitzWith.continuous (K := (k : ℝ≥0) + 1)
    (LipschitzWith.of_dist_le_mul fun τ τ' => ?_)
  have hbound : ∑ m : Fin (k + 1), |τ m - τ' m| ≤ ((k : ℝ) + 1) * dist τ τ' := by
    calc ∑ m : Fin (k + 1), |τ m - τ' m| ≤ ∑ _m : Fin (k + 1), dist τ τ' := by
          refine Finset.sum_le_sum fun m _ => ?_
          rw [← Real.dist_eq]
          exact dist_le_pi_dist τ τ' m
      _ = ((k : ℝ) + 1) * dist τ τ' := by
          rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
          push_cast
          ring
  have hcoe : ((((k : ℝ≥0) + 1 : ℝ≥0)) : ℝ) = (k : ℝ) + 1 := by push_cast; ring
  rw [hcoe]
  exact (dist_bcfOccupation_le T p τ τ').trans hbound

/-- The schedule class `Wcal_{n,k}(T)` realized inside the bounded continuous maps on the
horizon: those that agree on `[0, T]` with a schedule of block budget `k`. -/
def bcfScheduleSet (n k : ℕ) (T : ℝ) : Set (↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ)) :=
  {W | ∃ V : Fin n → ℝ → ℝ, IsSchedule k T V ∧
    ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, ofBCF W i t = V i t}

/-- Membership in the realized schedule class, in parameterized form. -/
theorem mem_bcfScheduleSet {n k : ℕ} {T : ℝ} {W : ↥(Icc (0 : ℝ) T) →ᵇ (Fin n → ℝ)} :
    W ∈ bcfScheduleSet n k T ↔
      ∃ (p : Fin k → Fin n) (τ : Fin (k + 1) → ℝ), OrderedTimes τ T ∧
        W = bcfOccupation T p τ := by
  constructor
  · rintro ⟨V, ⟨p, τ, hτ, rfl⟩, hagree⟩
    refine ⟨p, τ, hτ, BoundedContinuousFunction.ext fun y => funext fun i => ?_⟩
    rw [← ofBCF_coe W i y, bcfOccupation_apply]
    exact hagree i (y : ℝ) y.2
  · rintro ⟨p, τ, hτ, rfl⟩
    refine ⟨occupation p τ, ⟨p, τ, hτ, rfl⟩, fun i t ht => ?_⟩
    rw [ofBCF_apply _ i ht]
    rfl

/-- Every schedule is realized, on the horizon, by a member of the realized schedule class. -/
theorem exists_mem_bcfScheduleSet {n k : ℕ} {T : ℝ} {V : Fin n → ℝ → ℝ}
    (hV : IsSchedule k T V) : ∃ W ∈ bcfScheduleSet n k T,
      ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, ofBCF W i t = V i t := by
  obtain ⟨p, τ, hτ, rfl⟩ := hV
  exact ⟨bcfOccupation T p τ, mem_bcfScheduleSet.mpr ⟨p, τ, hτ, rfl⟩, fun i t ht => by
    rw [ofBCF_apply _ i ht]; rfl⟩

/-- SC07: the schedule class is compact in the uniform norm. It is the finite union over words
of the image of the compact ordered-time simplex under `τ ↦ occupation p τ`. -/
theorem isCompact_bcfScheduleSet (n k : ℕ) (T : ℝ) : IsCompact (bcfScheduleSet n k T) := by
  have hset : bcfScheduleSet n k T =
      ⋃ p : Fin k → Fin n,
        (fun τ : Fin (k + 1) → ℝ => bcfOccupation T p τ) '' orderedTimesSet k T := by
    ext W
    rw [mem_bcfScheduleSet]
    simp only [mem_iUnion, mem_image, mem_orderedTimesSet]
    constructor
    · rintro ⟨p, τ, hτ, rfl⟩
      exact ⟨p, τ, hτ, rfl⟩
    · rintro ⟨p, τ, hτ, rfl⟩
      exact ⟨p, τ, hτ, rfl⟩
  rw [hset]
  exact isCompact_iUnion fun p =>
    (isCompact_orderedTimesSet k T).image (continuous_bcfOccupation T p)

/-- The realized schedule class sits inside the realized cumulative class, matching
`IsSchedule.isCumulative`. -/
theorem bcfScheduleSet_subset_bcfCumulativeSet (n k : ℕ) {T : ℝ} (hT : 0 ≤ T) :
    bcfScheduleSet n k T ⊆ bcfCumulativeSet n T := by
  rintro W ⟨V, hV, hagree⟩
  exact isCumulative_congr hT hV.isCumulative fun i t ht => (hagree i t ht).symm

/-! ## SC08: the one-sided analogues of `eq:scaling`

`eq:scaling` covers `G⁻_{n,k}(T) = T G⁻_{n,k}(1)` as well. The one-sided criterion is indexed
by activation blocks, so a positive block budget replaces the switch budget throughout. -/

/-- SC08: the change of variables divides the one-sided error by `c`. -/
theorem Dminus_rescale (hn : 0 < n) {c T : ℝ} (hc : 0 < c) {A W : Fin n → ℝ → ℝ}
    (hA : IsCumulative A T) (hW : IsCumulative W T) (hT : 0 ≤ T) :
    Dminus (rescale c A) (rescale c W) (T / c) = Dminus A W T / c := by
  have hc0 : c ≠ 0 := ne_of_gt hc
  have hTc : c * (T / c) = T := by field_simp
  have hTc' : (0 : ℝ) ≤ T / c := div_nonneg hT hc.le
  have hcancel : ∀ a : ℝ, c * (a / c) = a := fun a => by field_simp
  have hmem : ∀ u ∈ Icc (0 : ℝ) (T / c), c * u ∈ Icc (0 : ℝ) T := fun u hu =>
    ⟨mul_nonneg hc.le hu.1, hTc ▸ mul_le_mul_of_nonneg_left hu.2 hc.le⟩
  have hmem' : ∀ t ∈ Icc (0 : ℝ) T, t / c ∈ Icc (0 : ℝ) (T / c) := fun t ht =>
    ⟨div_nonneg ht.1 hc.le, (div_le_div_iff_of_pos_right hc).mpr ht.2⟩
  have hA' := rescale_isCumulative hc hA
  have hW' := rescale_isCumulative hc hW
  refine le_antisymm ?_ ?_
  · refine Real.sSup_le (fun e he => ?_) (div_nonneg (Dminus_nonneg hn hA hW hT) hc.le)
    obtain ⟨i, u, hu, rfl⟩ := he
    have h1 : W i (c * u) - A i (c * u) ≤ Dminus A W T :=
      le_csSup (lowerErrorSet_bddAbove hA hW) ⟨i, c * u, hmem u hu, rfl⟩
    simp only [rescale, ← sub_div]
    exact (div_le_div_iff_of_pos_right hc).mpr h1
  · have hstep : Dminus A W T ≤ c * Dminus (rescale c A) (rescale c W) (T / c) := by
      refine Real.sSup_le (fun e he => ?_)
        (mul_nonneg hc.le (Dminus_nonneg hn hA' hW' hTc'))
      obtain ⟨i, t, ht, rfl⟩ := he
      have e1 : rescale c A i (t / c) = A i t / c := by
        simp only [rescale]; rw [hcancel t]
      have e2 : rescale c W i (t / c) = W i t / c := by
        simp only [rescale]; rw [hcancel t]
      have h1 : rescale c W i (t / c) - rescale c A i (t / c)
          ≤ Dminus (rescale c A) (rescale c W) (T / c) :=
        le_csSup (lowerErrorSet_bddAbove hA' hW') ⟨i, t / c, hmem' t ht, rfl⟩
      rw [e1, e2] at h1
      have h2 := mul_le_mul_of_nonneg_left h1 hc.le
      rwa [← sub_div, hcancel (W i t - A i t)] at h2
    calc Dminus A W T / c ≤ (c * Dminus (rescale c A) (rescale c W) (T / c)) / c :=
          (div_le_div_iff_of_pos_right hc).mpr hstep
      _ = Dminus (rescale c A) (rescale c W) (T / c) := by field_simp

/-- SC08: the change of variables divides the one-sided instance optimum by `c`. -/
theorem OPTminus_rescale (hn : 0 < n) {c T : ℝ} (hc : 0 < c) {A : Fin n → ℝ → ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) {k : ℕ} (hk : 0 < k) :
    OPTminus (rescale c A) (T / c) k = OPTminus A T k / c := by
  have hc0 : c ≠ 0 := ne_of_gt hc
  have hTc' : (0 : ℝ) ≤ T / c := div_nonneg hT hc.le
  have hcancel : ∀ a : ℝ, c * (a / c) = a := fun a => by field_simp
  have hA' := rescale_isCumulative hc hA
  have hcinv : (0 : ℝ) < 1 / c := by positivity
  refine le_antisymm ?_ ?_
  · have h : c * OPTminus (rescale c A) (T / c) k ≤ OPTminus A T k := by
      refine le_csInf (scheduleLowerErrorSet_nonempty hn hT hk) ?_
      rintro e ⟨W, hW, rfl⟩
      have h1 : OPTminus (rescale c A) (T / c) k
          ≤ Dminus (rescale c A) (rescale c W) (T / c) :=
        OPTminus_le_Dminus hn hA' hTc' (rescale_isSchedule hc hW)
      rw [Dminus_rescale hn hc hA hW.isCumulative hT] at h1
      have h2 := mul_le_mul_of_nonneg_left h1 hc.le
      rwa [hcancel (Dminus A W T)] at h2
    calc OPTminus (rescale c A) (T / c) k
        = (c * OPTminus (rescale c A) (T / c) k) / c := by field_simp
      _ ≤ OPTminus A T k / c := (div_le_div_iff_of_pos_right hc).mpr h
  · refine le_csInf (scheduleLowerErrorSet_nonempty hn hTc' hk) ?_
    rintro e ⟨V, hV, rfl⟩
    have hWs : IsSchedule k T (rescale (1 / c) V) := by
      have h := rescale_isSchedule hcinv hV
      rwa [show T / c / (1 / c) = T by field_simp] at h
    have hVeq : rescale c (rescale (1 / c) V) = V := rescale_inv hc V
    have hD : Dminus (rescale c A) V (T / c) = Dminus A (rescale (1 / c) V) T / c := by
      conv_lhs => rw [← hVeq]
      exact Dminus_rescale hn hc hA hWs.isCumulative hT
    rw [hD]
    exact (div_le_div_iff_of_pos_right hc).mpr (OPTminus_le_Dminus hn hA hT hWs)

/-- SC08: the change of variables divides the one-sided minimax value by `c`. -/
theorem Gminus_rescale (hn : 0 < n) {c T : ℝ} (hc : 0 < c) (hT : 0 ≤ T) {k : ℕ} (hk : 0 < k) :
    Gminus n k (T / c) = Gminus n k T / c := by
  have hc0 : c ≠ 0 := ne_of_gt hc
  have hTc' : (0 : ℝ) ≤ T / c := div_nonneg hT hc.le
  have hcinv : (0 : ℝ) < 1 / c := by positivity
  refine le_antisymm ?_ ?_
  · refine Gminus_le (div_nonneg (Gminus_nonneg hn hk hT) hc.le) fun B hB => ?_
    have hA : IsCumulative (rescale (1 / c) B) T := by
      have h := rescale_isCumulative hcinv hB
      rwa [show T / c / (1 / c) = T by field_simp] at h
    have hBeq : rescale c (rescale (1 / c) B) = B := rescale_inv hc B
    have hOPT : OPTminus B (T / c) k = OPTminus (rescale (1 / c) B) T k / c := by
      conv_lhs => rw [← hBeq]
      exact OPTminus_rescale hn hc hA hT hk
    rw [hOPT]
    exact (div_le_div_iff_of_pos_right hc).mpr (OPTminus_le_Gminus hn hA hT hk)
  · have h : Gminus n k T ≤ c * Gminus n k (T / c) := by
      refine Gminus_le (mul_nonneg hc.le (Gminus_nonneg hn hk hTc')) fun A hA => ?_
      have hstep : OPTminus A T k = c * OPTminus (rescale c A) (T / c) k := by
        rw [OPTminus_rescale hn hc hA hT hk]; field_simp
      rw [hstep]
      exact mul_le_mul_of_nonneg_left
        (OPTminus_le_Gminus hn (rescale_isCumulative hc hA) hTc' hk) hc.le
    calc Gminus n k T / c ≤ (c * Gminus n k (T / c)) / c :=
          (div_le_div_iff_of_pos_right hc).mpr h
      _ = Gminus n k (T / c) := by field_simp

/-- SC08, `eq:scaling` for the one-sided value: `G⁻_{n,k}(T) = T G⁻_{n,k}(1)`. -/
theorem Gminus_scaling (hn : 0 < n) {T : ℝ} (hT : 0 < T) {k : ℕ} (hk : 0 < k) :
    Gminus n k T = T * Gminus n k 1 := by
  have h := Gminus_rescale hn hT hT.le hk
  rw [div_self (ne_of_gt hT)] at h
  rw [h]
  field_simp

/-- On the degenerate horizon the one-sided error vanishes. -/
theorem Dminus_horizon_zero (hn : 0 < n) {A W : Fin n → ℝ → ℝ} (hA : IsCumulative A 0)
    (hW : IsCumulative W 0) : Dminus A W 0 = 0 := by
  refine le_antisymm (Real.sSup_le (fun e he => ?_) le_rfl) (Dminus_nonneg hn hA hW le_rfl)
  obtain ⟨i, t, ht, rfl⟩ := he
  obtain ⟨h1, h2⟩ := ht
  have ht0 : t = 0 := le_antisymm h2 h1
  subst ht0
  simp [hA.initial, hW.initial]

/-- On the degenerate horizon the one-sided instance optimum vanishes. -/
theorem OPTminus_horizon_zero (hn : 0 < n) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A 0)
    {k : ℕ} (hk : 0 < k) : OPTminus A 0 k = 0 := by
  refine le_antisymm ?_ (OPTminus_nonneg hn hA le_rfl hk)
  obtain ⟨W, hW⟩ := exists_isSchedule hn (le_refl (0 : ℝ)) hk
  calc OPTminus A 0 k ≤ Dminus A W 0 := OPTminus_le_Dminus hn hA le_rfl hW
    _ = 0 := Dminus_horizon_zero hn hA hW.isCumulative

/-- SC08: `G⁻_{n,k}(0) = 0`. -/
theorem Gminus_horizon_zero (hn : 0 < n) {k : ℕ} (hk : 0 < k) : Gminus n k 0 = 0 :=
  le_antisymm (Gminus_le le_rfl fun _A hA => le_of_eq (OPTminus_horizon_zero hn hA hk))
    (Gminus_nonneg hn hk le_rfl)

end GridSwitching
