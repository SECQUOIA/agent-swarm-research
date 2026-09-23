import Mathlib

/-!
# The grid switching model: relaxed controls, schedules, errors, and grids

This is the foundational module of the arbitrary-grid switching package. Everything is
parametric in the number of modes `n` (as `Fin n`) and in the horizon `T : ℝ`; nothing is
hard-wired to a fixed mode count or to unit cells.

The four groups of declarations correspond to the tier-0 obligations of
`topics/17-grid-switching/CLAIMS.md`.

* `SimplexRates`, `cumulative`, `masses` (SC01): a relaxed control is a measurable map into
  the standard simplex, its cumulative allocation is the coordinatewise interval integral, and
  its terminal masses are the cumulative values at the horizon.
* `IsCumulative` (SC02): the cumulative class `Acal_n(T)`, characterized by vanishing at the
  origin, monotonicity, unit Lipschitz increments, and the conservation identity
  `∑ i, A i t = t`. The easy direction is `SimplexRates.isCumulative` below; the converse,
  that every `IsCumulative` vector arises from a relaxed control, is
  `GridSwitching.exists_simplexRates_cumulative` in `Formal.GridSwitching.Cumulative`.
* `occupation`, `OrderedTimes`, `IsSchedule` (SC03): schedules parameterized by a word and
  ordered switch times, following `eq:schedule-parameterization`. Initial activation is free,
  so a class with block budget `k` allows `s = k - 1` switches.
* `errorSet`, `D`, `Dminus`, `OPT`, `F`, `IsGrid`, `IsGridConstant`, `IsGridSchedule`,
  `gridOPT`, `gridF` (SC04): the two error criteria, the instance optima, the minimax values,
  and their grid analogues.

Two conventions of the package are load-bearing here.

* Blocks versus switches: `IsSchedule k T W` bounds the number of activation *blocks* by `k`,
  while `OPT A T s` and `F n s T` are indexed by the number of *switches* `s = k - 1`. The
  one-sided quantities `OPTminus` and `Gminus` are indexed by blocks.
* The grid asymmetry: `gridOPT` is defined for *every* input function, with no hypothesis at
  all, whereas `gridF` maximizes only over grid-constant inputs.
-/

namespace GridSwitching

open MeasureTheory Set

variable {n : ℕ}

/-! ## SC01: relaxed controls and their cumulative allocations -/

/-- A relaxed control on the horizon `[0, T]`: a family of rates that is measurable with
respect to Lebesgue measure restricted to `[0, T]`, nonnegative there, and sums to one there.
Measurability is required only on the horizon, and the two pointwise conditions are only
imposed on the horizon, so the values away from `[0, T]` are unconstrained. -/
structure SimplexRates (α : Fin n → ℝ → ℝ) (T : ℝ) : Prop where
  /-- Each rate is almost everywhere strongly measurable on the horizon. -/
  measurable : ∀ i, AEStronglyMeasurable (α i) (volume.restrict (Icc 0 T))
  /-- Rates are nonnegative on the horizon. -/
  nonneg : ∀ t ∈ Icc 0 T, ∀ i, 0 ≤ α i t
  /-- Rates sum to one on the horizon. -/
  conservation : ∀ t ∈ Icc 0 T, ∑ i, α i t = 1

/-- At every time of the horizon the rate vector lies in the standard simplex. This is the
`Delta_n` of the source, expressed with Mathlib's `stdSimplex`. -/
theorem SimplexRates.mem_stdSimplex {α : Fin n → ℝ → ℝ} {T : ℝ} (hα : SimplexRates α T)
    {t : ℝ} (ht : t ∈ Icc 0 T) : (fun i => α i t) ∈ stdSimplex ℝ (Fin n) :=
  ⟨fun i => hα.nonneg t ht i, hα.conservation t ht⟩

/-- Cumulative allocation `A i t = ∫_0^t α i` of a relaxed control, as in `eq:cumulatives`. -/
noncomputable def cumulative (α : Fin n → ℝ → ℝ) (i : Fin n) (t : ℝ) : ℝ :=
  ∫ s in (0 : ℝ)..t, α i s

/-- Terminal masses `m i = A i T` of a cumulative allocation, as in `eq:cumulatives`. -/
def masses (A : Fin n → ℝ → ℝ) (T : ℝ) (i : Fin n) : ℝ := A i T

/-- A single rate never exceeds one on the horizon, because the rates are nonnegative and
sum to one there. -/
theorem SimplexRates.le_one {α : Fin n → ℝ → ℝ} {T : ℝ} (hα : SimplexRates α T)
    {t : ℝ} (ht : t ∈ Icc 0 T) (i : Fin n) : α i t ≤ 1 := by
  calc α i t ≤ ∑ j, α j t :=
        Finset.single_le_sum (fun j _ => hα.nonneg t ht j) (Finset.mem_univ i)
    _ = 1 := hα.conservation t ht

/-- Bounded measurable simplex rates are integrable on the horizon; no separate integrability
hypothesis is needed. -/
theorem SimplexRates.integrableOn {α : Fin n → ℝ → ℝ} {T : ℝ} (hα : SimplexRates α T)
    (i : Fin n) : IntegrableOn (α i) (Icc 0 T) := by
  have hc : IntegrableOn (fun _ : ℝ => (1 : ℝ)) (Icc 0 T) :=
    integrableOn_const isCompact_Icc.measure_ne_top
  refine hc.mono' (hα.measurable i) ?_
  refine (ae_restrict_iff' measurableSet_Icc).mpr (Filter.Eventually.of_forall fun t ht => ?_)
  simpa [Real.norm_eq_abs, abs_of_nonneg (hα.nonneg t ht i)] using hα.le_one ht i

/-- Integrability of a rate on every subinterval of the horizon. -/
theorem SimplexRates.intervalIntegrable {α : Fin n → ℝ → ℝ} {T s t : ℝ}
    (hα : SimplexRates α T) (hs : 0 ≤ s) (hst : s ≤ t) (ht : t ≤ T) (i : Fin n) :
    IntervalIntegrable (α i) volume s t :=
  (intervalIntegrable_iff_integrableOn_Icc_of_le hst).mpr
    ((hα.integrableOn i).mono_set (Icc_subset_Icc hs ht))

@[simp] theorem cumulative_zero (α : Fin n → ℝ → ℝ) (i : Fin n) : cumulative α i 0 = 0 := by
  simp [cumulative]

/-- Cumulative increments are nonnegative: the cumulative allocation is nondecreasing. -/
theorem cumulative_increment_nonneg {α : Fin n → ℝ → ℝ} {T : ℝ} (hα : SimplexRates α T)
    (i : Fin n) {s t : ℝ} (hs : 0 ≤ s) (hst : s ≤ t) (ht : t ≤ T) :
    0 ≤ cumulative α i t - cumulative α i s := by
  rw [cumulative, cumulative, intervalIntegral.integral_interval_sub_left
    (hα.intervalIntegrable le_rfl (hs.trans hst) ht i)
    (hα.intervalIntegrable le_rfl hs (hst.trans ht) i)]
  exact intervalIntegral.integral_nonneg hst fun x hx =>
    hα.nonneg x ⟨hs.trans hx.1, hx.2.trans ht⟩ i

/-- Cumulative increments are bounded by elapsed time: the cumulative allocation is
`1`-Lipschitz. -/
theorem cumulative_increment_le {α : Fin n → ℝ → ℝ} {T : ℝ} (hα : SimplexRates α T)
    (i : Fin n) {s t : ℝ} (hs : 0 ≤ s) (hst : s ≤ t) (ht : t ≤ T) :
    cumulative α i t - cumulative α i s ≤ t - s := by
  rw [cumulative, cumulative, intervalIntegral.integral_interval_sub_left
    (hα.intervalIntegrable le_rfl (hs.trans hst) ht i)
    (hα.intervalIntegrable le_rfl hs (hst.trans ht) i)]
  have hle := intervalIntegral.integral_mono_on hst (hα.intervalIntegrable hs hst ht i)
    (intervalIntegrable_const (c := (1 : ℝ)))
    (fun x hx => hα.le_one ⟨hs.trans hx.1, hx.2.trans ht⟩ i)
  simpa using hle

/-- The cumulative allocation is monotone on the horizon. -/
theorem cumulative_mono {α : Fin n → ℝ → ℝ} {T : ℝ} (hα : SimplexRates α T)
    (i : Fin n) {s t : ℝ} (hs : 0 ≤ s) (hst : s ≤ t) (ht : t ≤ T) :
    cumulative α i s ≤ cumulative α i t := by
  linarith [cumulative_increment_nonneg hα i hs hst ht]

/-- Cumulative mode allocations sum to elapsed time on the horizon. -/
theorem cumulative_conservation {α : Fin n → ℝ → ℝ} {T t : ℝ} (hα : SimplexRates α T)
    (ht : t ∈ Icc 0 T) : ∑ i, cumulative α i t = t := by
  unfold cumulative
  rw [← intervalIntegral.integral_finsetSum
    (fun i _ => hα.intervalIntegrable le_rfl ht.1 ht.2 i)]
  calc (∫ s in (0 : ℝ)..t, ∑ i, α i s) = ∫ _s in (0 : ℝ)..t, (1 : ℝ) := by
        refine intervalIntegral.integral_congr fun s hs => ?_
        rw [uIcc_of_le ht.1] at hs
        exact hα.conservation s ⟨hs.1, hs.2.trans ht.2⟩
    _ = t := by simp

/-! ## SC02: the cumulative class -/

/-- The cumulative class `Acal_n(T)`: vectors of functions that vanish at the origin, are
nondecreasing, have unit Lipschitz increments, and allocate exactly the elapsed time.

`SimplexRates.isCumulative` shows every relaxed control produces such a vector; the converse
is `GridSwitching.exists_simplexRates_cumulative` in `Formal.GridSwitching.Cumulative`. -/
structure IsCumulative (A : Fin n → ℝ → ℝ) (T : ℝ) : Prop where
  /-- No mass has accumulated at time zero. -/
  initial : ∀ i, A i 0 = 0
  /-- Each coordinate is nondecreasing on the horizon. -/
  mono : ∀ i s t, 0 ≤ s → s ≤ t → t ≤ T → A i s ≤ A i t
  /-- Each coordinate has increments bounded by elapsed time. -/
  lipschitz : ∀ i s t, 0 ≤ s → s ≤ t → t ≤ T → A i t - A i s ≤ t - s
  /-- The coordinates allocate exactly the elapsed time. -/
  conservation : ∀ t ∈ Icc 0 T, ∑ i, A i t = t

/-- SC02, easy direction: the cumulative allocation of a relaxed control lies in the
cumulative class. -/
theorem SimplexRates.isCumulative {α : Fin n → ℝ → ℝ} {T : ℝ} (hα : SimplexRates α T) :
    IsCumulative (cumulative α) T where
  initial i := cumulative_zero α i
  mono i _ _ hs hst ht := cumulative_mono hα i hs hst ht
  lipschitz i _ _ hs hst ht := cumulative_increment_le hα i hs hst ht
  conservation _ ht := cumulative_conservation hα ht

/-- Every coordinate of a cumulative allocation is nonnegative on the horizon. -/
theorem IsCumulative.nonneg {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) (i : Fin n)
    {t : ℝ} (ht : t ∈ Icc 0 T) : 0 ≤ A i t := by
  simpa [hA.initial i] using hA.mono i 0 t le_rfl ht.1 ht.2

/-- Every coordinate of a cumulative allocation is bounded by elapsed time. -/
theorem IsCumulative.le_self {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) (i : Fin n)
    {t : ℝ} (ht : t ∈ Icc 0 T) : A i t ≤ t := by
  simpa [hA.initial i] using hA.lipschitz i 0 t le_rfl ht.1 ht.2

/-! ## SC03: schedules

A schedule is described by `eq:schedule-parameterization`: a word `p : Fin k → Fin n` of at
most `k` activation blocks together with ordered times `0 = τ_0 ≤ ... ≤ τ_k = T`. Initial
activation is free, so `k` blocks correspond to `s = k - 1` switches. -/

/-- Telescoping sum over the block index. -/
private theorem sum_succ_sub_castSucc {k : ℕ} (f : Fin (k + 1) → ℝ) :
    ∑ j : Fin k, (f j.succ - f j.castSucc) = f (Fin.last k) - f 0 := by
  induction k with
  | zero => simp
  | succ k ih =>
    have h := ih fun m : Fin (k + 1) => f m.castSucc
    rw [Fin.sum_univ_castSucc]
    simp only [Fin.succ_castSucc] at h ⊢
    rw [h]
    simp only [Fin.succ_last, Fin.castSucc_zero]
    ring

/-- A comparison of clipped times that is monotone in the clipping level. -/
private theorem min_sub_min_mono {a b s t : ℝ} (hab : a ≤ b) (hst : s ≤ t) :
    min s b - min s a ≤ min t b - min t a := by
  simp only [min_def]; split_ifs <;> linarith

/-- Cumulative occupation contributed by one activation block: mode `q` is active on the time
interval with endpoints `a` and `b`. -/
noncomputable def blockOcc (q : Fin n) (a b : ℝ) (i : Fin n) (t : ℝ) : ℝ :=
  if q = i then min t b - min t a else 0

/-- Two consecutive blocks with the same mode merge into one. -/
theorem blockOcc_merge (q : Fin n) (a b c : ℝ) (i : Fin n) (t : ℝ) :
    blockOcc q a b i t + blockOcc q b c i t = blockOcc q a c i t := by
  simp only [blockOcc]; split_ifs <;> ring

/-- A zero-length block contributes nothing. -/
@[simp] theorem blockOcc_self (q : Fin n) (a : ℝ) (i : Fin n) (t : ℝ) :
    blockOcc q a a i t = 0 := by simp [blockOcc]

/-- Cumulative occupation of mode `i` under the word `p` and the ordered times `τ`, as in
`eq:schedule-parameterization`. -/
noncomputable def occupation {k : ℕ} (p : Fin k → Fin n) (τ : Fin (k + 1) → ℝ) (i : Fin n)
    (t : ℝ) : ℝ :=
  ∑ j : Fin k, if p j = i then min t (τ j.succ) - min t (τ j.castSucc) else 0

/-- The occupation is the sum of the individual block occupations. -/
theorem occupation_eq_sum_blockOcc {k : ℕ} (p : Fin k → Fin n) (τ : Fin (k + 1) → ℝ)
    (i : Fin n) (t : ℝ) :
    occupation p τ i t = ∑ j : Fin k, blockOcc (p j) (τ j.castSucc) (τ j.succ) i t := rfl

/-- Ordered switch times `0 = τ_0 ≤ τ_1 ≤ ... ≤ τ_k = T`. -/
structure OrderedTimes {k : ℕ} (τ : Fin (k + 1) → ℝ) (T : ℝ) : Prop where
  /-- The schedule starts at time zero. -/
  first : τ 0 = 0
  /-- The schedule ends at the horizon. -/
  last : τ (Fin.last k) = T
  /-- The times are nondecreasing. -/
  mono : Monotone τ

/-- The schedule class `Wcal_{n,k}(T)`: cumulative occupations of words with at most `k`
activation blocks, equivalently at most `s = k - 1` switches, since initial activation is
free. Zero-length blocks and repeated modes are permitted. -/
def IsSchedule (k : ℕ) (T : ℝ) (W : Fin n → ℝ → ℝ) : Prop :=
  ∃ (p : Fin k → Fin n) (τ : Fin (k + 1) → ℝ), OrderedTimes τ T ∧ W = occupation p τ

/-- All switch times of an ordered-time family are nonnegative. -/
theorem OrderedTimes.nonneg {k : ℕ} {τ : Fin (k + 1) → ℝ} {T : ℝ} (hτ : OrderedTimes τ T)
    (m : Fin (k + 1)) : 0 ≤ τ m := hτ.first ▸ hτ.mono (Fin.zero_le m)

/-- Every block occupies a nonnegative amount of time. -/
theorem occupation_nonneg {k : ℕ} {p : Fin k → Fin n} {τ : Fin (k + 1) → ℝ}
    (hτ : Monotone τ) (i : Fin n) (t : ℝ) : 0 ≤ occupation p τ i t := by
  refine Finset.sum_nonneg fun j _ => ?_
  have h : τ j.castSucc ≤ τ j.succ := hτ (Fin.castSucc_le_succ j)
  split_ifs with hp
  · simpa using min_le_min (le_refl t) h
  · exact le_rfl

/-- No mass has been occupied at time zero. -/
@[simp] theorem occupation_zero {k : ℕ} {p : Fin k → Fin n} {τ : Fin (k + 1) → ℝ} {T : ℝ}
    (hτ : OrderedTimes τ T) (i : Fin n) : occupation p τ i 0 = 0 := by
  refine Finset.sum_eq_zero fun j _ => ?_
  rw [min_eq_left (hτ.nonneg j.succ), min_eq_left (hτ.nonneg j.castSucc)]
  simp

/-- The occupation of each mode is nondecreasing in time. -/
theorem occupation_mono {k : ℕ} {p : Fin k → Fin n} {τ : Fin (k + 1) → ℝ}
    (hτ : Monotone τ) (i : Fin n) {s t : ℝ} (hst : s ≤ t) :
    occupation p τ i s ≤ occupation p τ i t := by
  refine Finset.sum_le_sum fun j _ => ?_
  have h : τ j.castSucc ≤ τ j.succ := hτ (Fin.castSucc_le_succ j)
  split_ifs with hp
  · exact min_sub_min_mono h hst
  · exact le_rfl

/-- The modes jointly occupy all the elapsed time, clipped to the horizon. -/
theorem occupation_sum {k : ℕ} (p : Fin k → Fin n) {τ : Fin (k + 1) → ℝ} {T : ℝ}
    (hτ : OrderedTimes τ T) (t : ℝ) :
    ∑ i, occupation p τ i t = min t T - min t (0 : ℝ) := by
  simp only [occupation]
  rw [Finset.sum_comm]
  have h : ∀ j : Fin k,
      (∑ _i : Fin n, if p j = _i then min t (τ j.succ) - min t (τ j.castSucc) else 0) =
        min t (τ j.succ) - min t (τ j.castSucc) := by
    intro j
    simp
  simp only [h]
  rw [sum_succ_sub_castSucc fun m => min t (τ m), hτ.first, hτ.last]

/-- The occupation of each mode has increments bounded by elapsed time. -/
theorem occupation_lipschitz {k : ℕ} {p : Fin k → Fin n} {τ : Fin (k + 1) → ℝ} {T : ℝ}
    (hτ : OrderedTimes τ T) (i : Fin n) {s t : ℝ} (hs : 0 ≤ s) (hst : s ≤ t) (ht : t ≤ T) :
    occupation p τ i t - occupation p τ i s ≤ t - s := by
  have hsum : ∑ i', (occupation p τ i' t - occupation p τ i' s) = t - s := by
    rw [Finset.sum_sub_distrib, occupation_sum p hτ t, occupation_sum p hτ s,
      min_eq_left ht, min_eq_left (hst.trans ht), min_eq_right hs,
      min_eq_right (hs.trans hst)]
    ring
  rw [← hsum]
  refine Finset.single_le_sum (f := fun i' => occupation p τ i' t - occupation p τ i' s)
    (fun i' _ => ?_) (Finset.mem_univ i)
  have := occupation_mono (p := p) hτ.mono i' hst
  linarith

/-- The cumulative occupation of a schedule lies in the cumulative class: the two classes are
compared by the same four conditions. -/
theorem occupation_isCumulative {k : ℕ} (p : Fin k → Fin n) {τ : Fin (k + 1) → ℝ} {T : ℝ}
    (hτ : OrderedTimes τ T) : IsCumulative (occupation p τ) T where
  initial i := occupation_zero hτ i
  mono i _ _ _ hst _ := occupation_mono hτ.mono i hst
  lipschitz i _ _ hs hst ht := occupation_lipschitz hτ i hs hst ht
  conservation t ht := by
    rw [occupation_sum p hτ t, min_eq_left ht.2, min_eq_right ht.1]; ring

/-- Every schedule is a cumulative allocation. -/
theorem IsSchedule.isCumulative {k : ℕ} {T : ℝ} {W : Fin n → ℝ → ℝ} (h : IsSchedule k T W) :
    IsCumulative W T := by
  obtain ⟨p, τ, hτ, rfl⟩ := h
  exact occupation_isCumulative p hτ

/-! ### SC03 closure: normalizing a block word

Deleting zero-length blocks and merging equal consecutive modes leave the cumulative
occupation unchanged and each removes one block. Together with the budget monotonicity
`IsSchedule.mono`, this gives the closure claim `isSchedule_of_card_positiveBlocks`: a
parameterization with at most `k` positive-length blocks is a schedule with block budget
`k`. -/

/-- Peeling the first block off a word. -/
theorem occupation_succ {k : ℕ} (p : Fin (k + 1) → Fin n) (τ : Fin (k + 2) → ℝ) (i : Fin n)
    (t : ℝ) :
    occupation p τ i t =
      blockOcc (p 0) (τ 0) (Fin.tail τ 0) i t + occupation (Fin.tail p) (Fin.tail τ) i t := by
  simp only [occupation, blockOcc]
  rw [Fin.sum_univ_succ, Fin.castSucc_zero]
  rfl

/-- Deleting a zero-length leading block does not change the cumulative occupation. -/
theorem occupation_delete {k : ℕ} (p : Fin (k + 1) → Fin n) (τ : Fin (k + 2) → ℝ)
    (h : τ 0 = Fin.tail τ 0) : occupation p τ = occupation (Fin.tail p) (Fin.tail τ) := by
  funext i t
  rw [occupation_succ, ← h, blockOcc_self, zero_add]

/-- Merging two equal consecutive leading modes does not change the cumulative occupation
and uses one block fewer. -/
theorem occupation_merge {k : ℕ} (p : Fin (k + 2) → Fin n) (τ : Fin (k + 3) → ℝ)
    (h : p 0 = Fin.tail p 0) :
    occupation p τ =
      occupation (Fin.tail p) (Fin.cons (τ 0) (Fin.tail (Fin.tail τ))) := by
  funext i t
  rw [occupation_succ p τ, occupation_succ (Fin.tail p) (Fin.tail τ),
    occupation_succ (Fin.tail p) (Fin.cons (τ 0) (Fin.tail (Fin.tail τ))),
    Fin.cons_zero, Fin.tail_cons, ← add_assoc, ← h, blockOcc_merge]

/-- Budget monotonicity, one step: appending a zero-length final block. -/
theorem IsSchedule.succ (hn : 0 < n) {k : ℕ} {T : ℝ} {W : Fin n → ℝ → ℝ}
    (h : IsSchedule k T W) : IsSchedule (k + 1) T W := by
  obtain ⟨p, τ, hτ, rfl⟩ := h
  have hsnocLast : (Fin.snoc τ T : Fin (k + 2) → ℝ) (Fin.last k).castSucc = T := by
    rw [Fin.snoc_castSucc]; exact hτ.last
  have hsnocSucc : (Fin.snoc τ T : Fin (k + 2) → ℝ) (Fin.last k).succ = T := by
    rw [Fin.succ_last, Fin.snoc_last]
  refine ⟨Fin.snoc p ⟨0, hn⟩, Fin.snoc τ T, ⟨?_, ?_, ?_⟩, ?_⟩
  · rw [← Fin.castSucc_zero, Fin.snoc_castSucc]; exact hτ.first
  · simp
  · refine Fin.monotone_iff_le_succ.mpr fun j => ?_
    refine Fin.lastCases ?_ ?_ j
    · rw [hsnocLast, hsnocSucc]
    · intro j0
      rw [Fin.snoc_castSucc, Fin.succ_castSucc, Fin.snoc_castSucc]
      exact hτ.mono (Fin.castSucc_le_succ j0)
  · funext i t
    simp only [occupation]
    rw [Fin.sum_univ_castSucc, hsnocLast, hsnocSucc, sub_self, ite_self, add_zero]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [Fin.snoc_castSucc, Fin.succ_castSucc, Fin.snoc_castSucc, Fin.snoc_castSucc]

/-- Budget monotonicity: enlarging the block budget enlarges the schedule class. -/
theorem IsSchedule.mono (hn : 0 < n) {k k' : ℕ} {T : ℝ} {W : Fin n → ℝ → ℝ} (hkk : k ≤ k')
    (h : IsSchedule k T W) : IsSchedule k' T W := by
  obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hkk
  induction d with
  | zero => simpa using h
  | succ d ih => exact (ih (by omega)).succ hn

/-- The blocks of positive length in an ordered-time parameterization. -/
noncomputable def positiveBlocks {k : ℕ} (τ : Fin (k + 1) → ℝ) : Finset (Fin k) :=
  Finset.univ.filter fun j => τ j.castSucc < τ j.succ

@[simp] theorem mem_positiveBlocks {k : ℕ} {τ : Fin (k + 1) → ℝ} {j : Fin k} :
    j ∈ positiveBlocks τ ↔ τ j.castSucc < τ j.succ := by
  rw [positiveBlocks, Finset.mem_filter]
  exact ⟨fun h => h.2, fun h => ⟨Finset.mem_univ j, h⟩⟩

/-- Positive blocks of the tail inject into the positive blocks of the whole word. -/
private theorem image_positiveBlocks_tail {k : ℕ} (τ : Fin (k + 2) → ℝ) :
    ((positiveBlocks (Fin.tail τ)).image Fin.succ) ⊆ positiveBlocks τ := by
  intro j hj
  simp only [Finset.mem_image, mem_positiveBlocks] at hj
  obtain ⟨j0, hj0, rfl⟩ := hj
  exact mem_positiveBlocks.mpr hj0

/-- Normalization: every parameterization with monotone times equals the occupation of one
whose block count is at most its number of positive-length blocks, with the same first and
last times. -/
private theorem exists_reduced {m : ℕ} (p : Fin m → Fin n) (τ : Fin (m + 1) → ℝ)
    (hτ : Monotone τ) :
    ∃ (c : ℕ) (p' : Fin c → Fin n) (τ' : Fin (c + 1) → ℝ), Monotone τ' ∧
      τ' 0 = τ 0 ∧ τ' (Fin.last c) = τ (Fin.last m) ∧
      occupation p' τ' = occupation p τ ∧ c ≤ (positiveBlocks τ).card := by
  induction m with
  | zero => exact ⟨0, p, τ, hτ, rfl, rfl, rfl, Nat.zero_le _⟩
  | succ m ih =>
    have htail : Monotone (Fin.tail τ) :=
      fun a b hab => hτ (Fin.succ_le_succ_iff.mpr hab)
    obtain ⟨c, p', τ', hm', h0', hl', hocc', hc'⟩ := ih (Fin.tail p) (Fin.tail τ) htail
    have hcard : (positiveBlocks (Fin.tail τ)).card ≤ (positiveBlocks τ).card := by
      calc (positiveBlocks (Fin.tail τ)).card
          = ((positiveBlocks (Fin.tail τ)).image Fin.succ).card :=
            (Finset.card_image_of_injective _ (Fin.succ_injective m)).symm
        _ ≤ (positiveBlocks τ).card := Finset.card_le_card (image_positiveBlocks_tail τ)
    have hlast : Fin.tail τ (Fin.last m) = τ (Fin.last (m + 1)) := by
      exact congrArg τ (Fin.succ_last m)
    rcases eq_or_lt_of_le (show τ 0 ≤ Fin.tail τ 0 from hτ (Fin.zero_le _)) with heq | hlt
    · exact ⟨c, p', τ', hm', h0'.trans heq.symm, hl'.trans hlast,
        hocc'.trans (occupation_delete p τ heq).symm, hc'.trans hcard⟩
    · refine ⟨c + 1, Fin.cons (p 0) p', Fin.cons (τ 0) τ', ?_, ?_, ?_, ?_, ?_⟩
      · refine Fin.monotone_iff_le_succ.mpr fun j => ?_
        refine Fin.cases ?_ ?_ j
        · rw [Fin.castSucc_zero, Fin.cons_zero, Fin.cons_succ, h0']
          exact hlt.le
        · intro j0
          rw [← Fin.succ_castSucc, Fin.cons_succ, Fin.cons_succ]
          exact hm' (Fin.castSucc_le_succ j0)
      · exact Fin.cons_zero _ _
      · have hlc : (Fin.last (c + 1) : Fin (c + 2)) = (Fin.last c).succ :=
          (Fin.succ_last c).symm
        rw [hlc, Fin.cons_succ, hl', hlast]
      · funext i t
        rw [occupation_succ (Fin.cons (p 0) p') (Fin.cons (τ 0) τ'), occupation_succ p τ,
          Fin.cons_zero, Fin.cons_zero, Fin.tail_cons, Fin.tail_cons, hocc', h0']
      · have h0mem : (0 : Fin (m + 1)) ∈ positiveBlocks τ := by
          rw [mem_positiveBlocks, Fin.castSucc_zero]
          exact hlt
        have hnot : (0 : Fin (m + 1)) ∉ (positiveBlocks (Fin.tail τ)).image Fin.succ := by
          simp only [Finset.mem_image, not_exists, not_and]
          exact fun j0 _ => Fin.succ_ne_zero j0
        calc c + 1 ≤ (positiveBlocks (Fin.tail τ)).card + 1 := by omega
          _ = (insert (0 : Fin (m + 1))
                ((positiveBlocks (Fin.tail τ)).image Fin.succ)).card := by
            rw [Finset.card_insert_of_notMem hnot,
              Finset.card_image_of_injective _ (Fin.succ_injective m)]
          _ ≤ (positiveBlocks τ).card :=
            Finset.card_le_card (Finset.insert_subset h0mem (image_positiveBlocks_tail τ))

/-- SC03 closure claim: a parameterization with at most `k` positive-length blocks is a
schedule for the block budget `k`. Zero-length blocks are deleted and equal consecutive modes
are merged without changing the cumulative occupation, so the block count cannot increase. -/
theorem isSchedule_of_card_positiveBlocks (hn : 0 < n) {m k : ℕ} {T : ℝ}
    (p : Fin m → Fin n) (τ : Fin (m + 1) → ℝ) (hτ : OrderedTimes τ T)
    (hcard : (positiveBlocks τ).card ≤ k) : IsSchedule k T (occupation p τ) := by
  obtain ⟨c, p', τ', hm', h0', hl', hocc', hc'⟩ := exists_reduced p τ hτ.mono
  refine IsSchedule.mono hn (hc'.trans hcard) ⟨p', τ', ⟨?_, ?_, hm'⟩, hocc'.symm⟩
  · rw [h0']; exact hτ.first
  · rw [hl']; exact hτ.last

/-! ## SC04: errors, instance optima, minimax values, and grids

The two error criteria of `eq:errors` are suprema over modes and over the horizon. They are
defined here as `sSup` of explicitly described sets; attainment of these suprema (and of the
optima below) is the obligation SC07 of a later module, so only nonnegativity, boundedness of
the error set, and the upper-bound property are proved here. -/

/-- The set of coordinatewise absolute discrepancies over the horizon, as in `eq:errors`. -/
def errorSet (A W : Fin n → ℝ → ℝ) (T : ℝ) : Set ℝ :=
  {e | ∃ i : Fin n, ∃ t ∈ Icc (0 : ℝ) T, e = |A i t - W i t|}

/-- The full error `D(A, W)` of `eq:errors`. -/
noncomputable def D (A W : Fin n → ℝ → ℝ) (T : ℝ) : ℝ := sSup (errorSet A W T)

/-- The set of one-sided discrepancies `W i t - A i t` over the horizon, as in `eq:errors`. -/
def lowerErrorSet (A W : Fin n → ℝ → ℝ) (T : ℝ) : Set ℝ :=
  {e | ∃ i : Fin n, ∃ t ∈ Icc (0 : ℝ) T, e = W i t - A i t}

/-- The one-sided error `D⁻(A, W)` of `eq:errors`. -/
noncomputable def Dminus (A W : Fin n → ℝ → ℝ) (T : ℝ) : ℝ := sSup (lowerErrorSet A W T)

/-- The error set is nonempty as soon as there is a mode and the horizon is not empty. -/
theorem errorSet_nonempty (hn : 0 < n) {A W : Fin n → ℝ → ℝ} {T : ℝ} (hT : 0 ≤ T) :
    (errorSet A W T).Nonempty :=
  ⟨|A ⟨0, hn⟩ 0 - W ⟨0, hn⟩ 0|, ⟨0, hn⟩, 0, ⟨le_rfl, hT⟩, rfl⟩

/-- Every error of two cumulative allocations lies between zero and the horizon. -/
theorem errorSet_mem_Icc {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) {e : ℝ} (he : e ∈ errorSet A W T) : e ∈ Icc (0 : ℝ) T := by
  obtain ⟨i, t, ht, rfl⟩ := he
  refine ⟨abs_nonneg _, abs_le.mpr ⟨?_, ?_⟩⟩ <;>
    [linarith [hA.nonneg i ht, hW.le_self i ht, ht.2];
     linarith [hW.nonneg i ht, hA.le_self i ht, ht.2]]

/-- The error set of two cumulative allocations is bounded above by the horizon. -/
theorem errorSet_bddAbove {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) : BddAbove (errorSet A W T) :=
  ⟨T, fun _ he => (errorSet_mem_Icc hA hW he).2⟩

/-- `D` dominates every individual discrepancy: it is an upper bound for the error set. -/
theorem le_D {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) (hW : IsCumulative W T)
    (i : Fin n) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) : |A i t - W i t| ≤ D A W T :=
  le_csSup (errorSet_bddAbove hA hW) ⟨i, t, ht, rfl⟩

/-- `D` is the least upper bound of the error set: any uniform bound dominates it. -/
theorem D_le {A W : Fin n → ℝ → ℝ} {T c : ℝ} (hc : 0 ≤ c)
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |A i t - W i t| ≤ c) : D A W T ≤ c :=
  Real.sSup_le (fun _ he => by obtain ⟨i, t, ht, rfl⟩ := he; exact h i t ht) hc

/-- The full error is nonnegative. -/
theorem D_nonneg (hn : 0 < n) {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) (hT : 0 ≤ T) : 0 ≤ D A W T := by
  obtain ⟨e, he⟩ := errorSet_nonempty hn (A := A) (W := W) hT
  exact (errorSet_mem_Icc hA hW he).1.trans (le_csSup (errorSet_bddAbove hA hW) he)

/-- The one-sided error set contains zero, because it includes the time `t = 0`. -/
theorem zero_mem_lowerErrorSet (hn : 0 < n) {A W : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hW : IsCumulative W T) (hT : 0 ≤ T) :
    (0 : ℝ) ∈ lowerErrorSet A W T :=
  ⟨⟨0, hn⟩, 0, ⟨le_rfl, hT⟩, by rw [hA.initial, hW.initial, sub_zero]⟩

/-- The one-sided error set is bounded above by the horizon. -/
theorem lowerErrorSet_bddAbove {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) : BddAbove (lowerErrorSet A W T) := by
  refine ⟨T, fun e he => ?_⟩
  obtain ⟨i, t, ht, rfl⟩ := he
  linarith [hW.le_self i ht, hA.nonneg i ht, ht.2]

/-- The one-sided error is nonnegative, as recorded after `eq:errors`. -/
theorem Dminus_nonneg (hn : 0 < n) {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) (hT : 0 ≤ T) : 0 ≤ Dminus A W T :=
  le_csSup (lowerErrorSet_bddAbove hA hW) (zero_mem_lowerErrorSet hn hA hW hT)

/-- The one-sided error never exceeds the full error. -/
theorem Dminus_le_D (hn : 0 < n) {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) (hT : 0 ≤ T) : Dminus A W T ≤ D A W T := by
  refine Real.sSup_le (fun e he => ?_) (D_nonneg hn hA hW hT)
  obtain ⟨i, t, ht, rfl⟩ := he
  calc W i t - A i t ≤ |W i t - A i t| := le_abs_self _
    _ = |A i t - W i t| := abs_sub_comm _ _
    _ ≤ D A W T := le_D hA hW i ht

/-! ### Constant schedules

The schedule that activates a single mode throughout the horizon. It witnesses that the
schedule classes are nonempty for every positive block budget. -/

/-- The schedule that activates mode `q` on all of `[0, T]`. -/
noncomputable def constSchedule (q : Fin n) (T : ℝ) : Fin n → ℝ → ℝ :=
  occupation (fun _ : Fin 1 => q) ![0, T]

/-- The constant schedule uses a single activation block, that is, no switches. -/
theorem isSchedule_constSchedule {T : ℝ} (hT : 0 ≤ T) (q : Fin n) :
    IsSchedule 1 T (constSchedule q T) := by
  refine ⟨fun _ => q, ![0, T], ⟨rfl, rfl, ?_⟩, rfl⟩
  refine Fin.monotone_iff_le_succ.mpr fun j => ?_
  fin_cases j
  simpa using hT

/-- Every positive block budget admits at least one schedule. -/
theorem exists_isSchedule (hn : 0 < n) {T : ℝ} (hT : 0 ≤ T) {k : ℕ} (hk : 0 < k) :
    ∃ W : Fin n → ℝ → ℝ, IsSchedule k T W :=
  ⟨constSchedule ⟨0, hn⟩ T, IsSchedule.mono hn hk (isSchedule_constSchedule hT ⟨0, hn⟩)⟩

/-! ### Instance optima and minimax values

`OPT` is indexed by the number of switches `s`, so it minimizes over schedules with `s + 1`
activation blocks; `OPTminus` is indexed by the number of blocks `k`. This matches the
intentional indexing of `eq:instance-optima` and `eq:minimax-values`. -/

/-- The full errors attainable by schedules with block budget `k`. -/
def scheduleErrorSet (A : Fin n → ℝ → ℝ) (T : ℝ) (k : ℕ) : Set ℝ :=
  {e | ∃ W : Fin n → ℝ → ℝ, IsSchedule k T W ∧ e = D A W T}

/-- The one-sided errors attainable by schedules with block budget `k`. -/
def scheduleLowerErrorSet (A : Fin n → ℝ → ℝ) (T : ℝ) (k : ℕ) : Set ℝ :=
  {e | ∃ W : Fin n → ℝ → ℝ, IsSchedule k T W ∧ e = Dminus A W T}

/-- The continuous instance optimum `OPT_s(A)` of `eq:instance-optima`, indexed by the number
of switches `s`; the corresponding block budget is `s + 1`. It is defined for every input. -/
noncomputable def OPT (A : Fin n → ℝ → ℝ) (T : ℝ) (s : ℕ) : ℝ :=
  sInf (scheduleErrorSet A T (s + 1))

/-- The one-sided instance optimum `OPT⁻_k(A)` of `eq:instance-optima`, indexed by the number
of activation blocks `k`. -/
noncomputable def OPTminus (A : Fin n → ℝ → ℝ) (T : ℝ) (k : ℕ) : ℝ :=
  sInf (scheduleLowerErrorSet A T k)

/-- The minimax value `F_{n,s}(T)` of `eq:minimax-values`, indexed by switches. The adversary
moves first: the supremum over relaxed inputs is outside the minimum over schedules. -/
noncomputable def F (n s : ℕ) (T : ℝ) : ℝ :=
  sSup {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsCumulative A T ∧ v = OPT A T s}

/-- The one-sided minimax value `G⁻_{n,k}(T)` of `eq:minimax-values`, indexed by blocks. -/
noncomputable def Gminus (n k : ℕ) (T : ℝ) : ℝ :=
  sSup {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsCumulative A T ∧ v = OPTminus A T k}

/-- The set minimized by `OPT` is nonempty for every input and every switch budget. -/
theorem scheduleErrorSet_nonempty (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ} (hT : 0 ≤ T)
    {k : ℕ} (hk : 0 < k) : (scheduleErrorSet A T k).Nonempty := by
  obtain ⟨W, hW⟩ := exists_isSchedule hn hT hk
  exact ⟨D A W T, W, hW, rfl⟩

/-! ### Grids

A grid is a strictly increasing `x_0 = 0 < ... < x_N = T`. The grid input class consists of
relaxed controls that are constant on each cell, presented by an explicit per-cell rate
matrix; the grid schedule class restricts switch times to grid points.

The asymmetry of `eq:grid-definitions` is preserved exactly: `gridOPT` carries no hypothesis
on the input `A` at all, whereas `gridF` maximizes only over `IsGridConstant` inputs. -/

variable {N : ℕ}

/-- A grid `x_0 = 0 < x_1 < ... < x_N = T` on the horizon. -/
structure IsGrid (x : Fin (N + 1) → ℝ) (T : ℝ) : Prop where
  /-- The grid starts at the origin. -/
  first : x 0 = 0
  /-- The grid ends at the horizon. -/
  last : x (Fin.last N) = T
  /-- The grid points are strictly increasing. -/
  strictMono : StrictMono x

/-- The cell length `Delta_j = x_j - x_{j-1}`. -/
def cellLength (x : Fin (N + 1) → ℝ) (j : Fin N) : ℝ := x j.succ - x j.castSucc

/-- The mesh width `bar Delta = max_j Delta_j`. -/
noncomputable def meshWidth (x : Fin (N + 1) → ℝ) : ℝ := ⨆ j : Fin N, cellLength x j

/-- A grid is in particular a family of ordered times, so it parameterizes schedules. -/
theorem IsGrid.orderedTimes {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T) :
    OrderedTimes x T :=
  ⟨hx.first, hx.last, hx.strictMono.monotone⟩

/-- Cell lengths of a grid are positive. -/
theorem IsGrid.cellLength_pos {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T) (j : Fin N) :
    0 < cellLength x j :=
  sub_pos.mpr (hx.strictMono (Fin.castSucc_lt_succ (i := j)))

/-- No cell is longer than the mesh width. -/
theorem cellLength_le_meshWidth (x : Fin (N + 1) → ℝ) (j : Fin N) :
    cellLength x j ≤ meshWidth x :=
  le_ciSup (Finite.bddAbove_range _) j

/-- A per-cell rate matrix: each row is a point of the standard simplex. -/
structure IsRateMatrix (r : Fin N → Fin n → ℝ) : Prop where
  /-- Rates are nonnegative. -/
  nonneg : ∀ j i, 0 ≤ r j i
  /-- Each cell's rates sum to one. -/
  conservation : ∀ j, ∑ i, r j i = 1

/-- The cumulative allocation of the relaxed control that uses the constant rate vector
`r j` on the cell `j`. -/
noncomputable def gridCumulative (x : Fin (N + 1) → ℝ) (r : Fin N → Fin n → ℝ) (i : Fin n)
    (t : ℝ) : ℝ :=
  ∑ j : Fin N, r j i * (min t (x j.succ) - min t (x j.castSucc))

/-- The grid input class `Acal_n(T)` of `eq:grid-definitions`: cumulative allocations of
relaxed controls that are constant on every cell. -/
def IsGridConstant (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) : Prop :=
  ∃ r : Fin N → Fin n → ℝ, IsRateMatrix r ∧ A = gridCumulative x r

/-- The modes of a grid-constant input jointly allocate the elapsed time, clipped to the
horizon. -/
theorem gridCumulative_sum {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : OrderedTimes x T)
    {r : Fin N → Fin n → ℝ} (hr : IsRateMatrix r) (t : ℝ) :
    ∑ i, gridCumulative x r i t = min t T - min t (0 : ℝ) := by
  simp only [gridCumulative]
  rw [Finset.sum_comm]
  have h : ∀ j : Fin N, (∑ i, r j i * (min t (x j.succ) - min t (x j.castSucc))) =
      min t (x j.succ) - min t (x j.castSucc) := by
    intro j
    rw [← Finset.sum_mul, hr.conservation j, one_mul]
  simp only [h]
  rw [sum_succ_sub_castSucc fun m => min t (x m), hx.first, hx.last]

/-- Each coordinate of a grid-constant input is nondecreasing in time. -/
theorem gridCumulative_mono {x : Fin (N + 1) → ℝ} (hx : Monotone x)
    {r : Fin N → Fin n → ℝ} (hr : IsRateMatrix r) (i : Fin n) {s t : ℝ} (hst : s ≤ t) :
    gridCumulative x r i s ≤ gridCumulative x r i t := by
  refine Finset.sum_le_sum fun j _ => ?_
  exact mul_le_mul_of_nonneg_left
    (min_sub_min_mono (hx (Fin.castSucc_le_succ j)) hst) (hr.nonneg j i)

/-- SC04: the grid input class consists of cumulative allocations. -/
theorem gridCumulative_isCumulative {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : OrderedTimes x T)
    {r : Fin N → Fin n → ℝ} (hr : IsRateMatrix r) : IsCumulative (gridCumulative x r) T where
  initial i := by
    refine Finset.sum_eq_zero fun j _ => ?_
    rw [min_eq_left (hx.nonneg j.succ), min_eq_left (hx.nonneg j.castSucc)]
    simp
  mono i _ _ _ hst _ := gridCumulative_mono hx.mono hr i hst
  lipschitz i a b ha hab hb := by
    have hsum : ∑ i', (gridCumulative x r i' b - gridCumulative x r i' a) = b - a := by
      rw [Finset.sum_sub_distrib, gridCumulative_sum hx hr b, gridCumulative_sum hx hr a,
        min_eq_left hb, min_eq_left (hab.trans hb), min_eq_right ha,
        min_eq_right (ha.trans hab)]
      ring
    rw [← hsum]
    refine Finset.single_le_sum
      (f := fun i' => gridCumulative x r i' b - gridCumulative x r i' a)
      (fun i' _ => ?_) (Finset.mem_univ i)
    have := gridCumulative_mono hx.mono hr i' hab
    linarith
  conservation t ht := by
    rw [gridCumulative_sum hx hr t, min_eq_left ht.2, min_eq_right ht.1]; ring

/-- The grid schedule class `Wcal_{n,k}(T)` of `eq:grid-definitions`: words with at most `k`
activation blocks whose switch times are grid points. The horizon is not a separate
parameter: it is the last grid point `x (Fin.last N)`. -/
def IsGridSchedule (x : Fin (N + 1) → ℝ) (k : ℕ) (W : Fin n → ℝ → ℝ) : Prop :=
  ∃ (p : Fin k → Fin n) (g : Fin (k + 1) → Fin (N + 1)), Monotone g ∧ g 0 = 0 ∧
    g (Fin.last k) = Fin.last N ∧ W = occupation p (x ∘ g)

/-- A grid schedule is a schedule. -/
theorem IsGridSchedule.isSchedule {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T) {k : ℕ}
    {W : Fin n → ℝ → ℝ} (h : IsGridSchedule x k W) : IsSchedule k T W := by
  obtain ⟨p, g, hg, hg0, hgl, rfl⟩ := h
  exact ⟨p, x ∘ g, ⟨by simp [hg0, hx.first], by simp [hgl, hx.last],
    hx.strictMono.monotone.comp hg⟩, rfl⟩

/-- The full errors attainable by grid schedules with block budget `k`. -/
def gridScheduleErrorSet (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ) (k : ℕ) :
    Set ℝ :=
  {e | ∃ W : Fin n → ℝ → ℝ, IsGridSchedule x k W ∧ e = D A W T}

/-- The one-sided errors attainable by grid schedules with block budget `k`. -/
def gridScheduleLowerErrorSet (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ) (k : ℕ) :
    Set ℝ :=
  {e | ∃ W : Fin n → ℝ → ℝ, IsGridSchedule x k W ∧ e = Dminus A W T}

/-- The grid instance optimum `OPT_s^T(A)` of `eq:grid-definitions`, indexed by switches.

This is defined for *every* input function, with no grid-constancy or even measurability
hypothesis; the asymmetry with `gridF` below is deliberate and load-bearing. -/
noncomputable def gridOPT (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ) (s : ℕ) : ℝ :=
  sInf (gridScheduleErrorSet x A T (s + 1))

/-- The one-sided grid instance optimum `OPT_k^{-,T}(A)`, indexed by blocks. Like `gridOPT`
it is defined for every input. -/
noncomputable def gridOPTminus (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ) (k : ℕ) :
    ℝ :=
  sInf (gridScheduleLowerErrorSet x A T k)

/-- The grid minimax value `F^T_{n,s}` of `eq:grid-definitions`, indexed by switches.

Unlike `gridOPT`, this maximizes only over grid-constant inputs. -/
noncomputable def gridF (x : Fin (N + 1) → ℝ) (n s : ℕ) (T : ℝ) : ℝ :=
  sSup {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧ v = gridOPT x A T s}

/-- The one-sided grid minimax value `G^{-,T}_{n,k}`, indexed by blocks. It too maximizes
only over grid-constant inputs. -/
noncomputable def gridGminus (x : Fin (N + 1) → ℝ) (n k : ℕ) (T : ℝ) : ℝ :=
  sSup {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧ v = gridOPTminus x A T k}

/-! ### SC03 closure, general form: deleting and merging at an arbitrary position

`occupation_delete` and `occupation_merge` act at the head of the word, which is all the
left-to-right normalization below needs. `occupation_merge_at` and `occupation_delete_at`
record the general statements: two consecutive blocks carrying the same mode may be merged at
any position, and a zero-length block may be deleted at any position, in both cases leaving
the cumulative occupation unchanged and using one block fewer. -/

/-- Deleting an interior time point commutes with the block-index deletion, away from the
merged block. -/
private theorem succAbove_castSucc_succ {m : ℕ} (j b : Fin (m + 1)) (hb : b ≠ j) :
    ((j.succ : Fin (m + 2)).castSucc).succAbove b.succ =
      ((j.succ : Fin (m + 2)).succAbove b).succ := by
  rcases lt_or_gt_of_ne hb with h | h
  · have h1 : b.castSucc < (j.succ : Fin (m + 2)) := by
      simp only [Fin.lt_def, Fin.val_castSucc, Fin.val_succ] at h ⊢; omega
    have h2 : (b.succ).castSucc < (j.succ : Fin (m + 2)).castSucc := by
      simp only [Fin.lt_def, Fin.val_castSucc, Fin.val_succ] at h ⊢; omega
    rw [Fin.succAbove_of_castSucc_lt _ _ h1, Fin.succAbove_of_castSucc_lt _ _ h2,
      Fin.succ_castSucc]
  · have h1 : (j.succ : Fin (m + 2)) ≤ b.castSucc := by
      simp only [Fin.le_def, Fin.lt_def, Fin.val_castSucc, Fin.val_succ] at h ⊢; omega
    have h2 : (j.succ : Fin (m + 2)).castSucc ≤ (b.succ).castSucc := by
      simp only [Fin.le_def, Fin.lt_def, Fin.val_castSucc, Fin.val_succ] at h ⊢; omega
    rw [Fin.succAbove_of_le_castSucc _ _ h1, Fin.succAbove_of_le_castSucc _ _ h2]

/-- Merging the two consecutive blocks `j` and `j + 1` when they carry the same mode: the
cumulative occupation is unchanged and the block count drops by one. The merged word deletes
block index `j + 1`, and the merged times delete the interior time `τ_{j+1}`. -/
theorem occupation_merge_at {k : ℕ} (p : Fin (k + 2) → Fin n) (τ : Fin (k + 3) → ℝ)
    (j : Fin (k + 1)) (h : p j.castSucc = p j.succ) :
    occupation p τ =
      occupation (Fin.removeNth j.succ p)
        (Fin.removeNth (j.succ : Fin (k + 2)).castSucc τ) := by
  funext i t
  simp only [occupation_eq_sum_blockOcc, Fin.removeNth]
  rw [Fin.sum_univ_succAbove
    (fun b : Fin (k + 2) => blockOcc (p b) (τ b.castSucc) (τ b.succ) i t) j.succ]
  set H : Fin (k + 1) → ℝ := fun b =>
    blockOcc (p ((j.succ : Fin (k + 2)).succAbove b))
      (τ ((j.succ : Fin (k + 2)).succAbove b).castSucc)
      (τ ((j.succ : Fin (k + 2)).succAbove b).succ) i t with hH
  set G : Fin (k + 1) → ℝ := fun b =>
    blockOcc (p ((j.succ : Fin (k + 2)).succAbove b))
      (τ ((j.succ : Fin (k + 2)).castSucc.succAbove b.castSucc))
      (τ ((j.succ : Fin (k + 2)).castSucc.succAbove b.succ)) i t with hG
  have hpivot : (j.succ : Fin (k + 2)).succAbove j = j.castSucc :=
    Fin.succAbove_of_castSucc_lt _ _ Fin.castSucc_lt_succ
  have hGH : ∀ b ∈ Finset.univ.erase j, G b = H b := by
    intro b hb
    have hbj : b ≠ j := (Finset.mem_erase.mp hb).1
    simp only [hG, hH, Fin.castSucc_succAbove_castSucc, succAbove_castSucc_succ j b hbj]
  have hGj : G j = blockOcc (p j.succ) (τ (j.succ : Fin (k + 2)).castSucc)
      (τ (j.succ : Fin (k + 2)).succ) i t + H j := by
    have hleft : ((j.succ : Fin (k + 2)).castSucc).succAbove j.castSucc =
        j.castSucc.castSucc := by
      rw [Fin.castSucc_succAbove_castSucc, hpivot]
    have hright : ((j.succ : Fin (k + 2)).castSucc).succAbove j.succ =
        (j.succ : Fin (k + 2)).succ :=
      Fin.succAbove_of_le_castSucc _ _ le_rfl
    simp only [hG, hH, hpivot, hleft, hright, h]
    rw [← Fin.succ_castSucc]
    linarith [blockOcc_merge (p j.succ) (τ j.castSucc.castSucc) (τ j.castSucc.succ)
      (τ (j.succ : Fin (k + 2)).succ) i t]
  rw [← Finset.add_sum_erase _ H (Finset.mem_univ j),
    ← Finset.add_sum_erase _ G (Finset.mem_univ j), Finset.sum_congr rfl hGH, hGj]
  ring

/-- Deleting a time point commutes with the block-index deletion, away from the deleted
block. -/
private theorem castSucc_succAbove_succ' {m : ℕ} (j : Fin (m + 1)) (b : Fin m)
    (hb : b.succ ≠ j) :
    ((j.castSucc : Fin (m + 2))).succAbove b.succ = (j.succAbove b).succ := by
  rcases lt_or_gt_of_ne hb with h | h
  · have hbj : b.castSucc < j := lt_trans (Fin.castSucc_lt_succ (i := b)) h
    have h1 : (b.succ).castSucc < (j.castSucc : Fin (m + 2)) := by
      simp only [Fin.lt_def, Fin.val_castSucc, Fin.val_succ] at h ⊢; omega
    rw [Fin.succAbove_of_castSucc_lt _ _ h1, Fin.succAbove_of_castSucc_lt _ _ hbj,
      Fin.succ_castSucc]
  · have hbj : j ≤ b.castSucc := by
      simp only [Fin.le_def, Fin.lt_def, Fin.val_castSucc, Fin.val_succ] at h ⊢; omega
    have h1 : (j.castSucc : Fin (m + 2)) ≤ (b.succ).castSucc := by
      simp only [Fin.le_def, Fin.lt_def, Fin.val_castSucc, Fin.val_succ] at h ⊢; omega
    rw [Fin.succAbove_of_le_castSucc _ _ h1, Fin.succAbove_of_le_castSucc _ _ hbj]

/-- Deleting the zero-length block `j`: the cumulative occupation is unchanged and the block
count drops by one. The shortened word deletes block index `j`, and the shortened times delete
the time `τ_j`, which by hypothesis equals `τ_{j+1}`. At `j = 0` this is
`occupation_delete`. -/
theorem occupation_delete_at {k : ℕ} (p : Fin (k + 1) → Fin n) (τ : Fin (k + 2) → ℝ)
    (j : Fin (k + 1)) (h : τ j.castSucc = τ j.succ) :
    occupation p τ =
      occupation (Fin.removeNth j p) (Fin.removeNth (j.castSucc : Fin (k + 2)) τ) := by
  funext i t
  simp only [occupation_eq_sum_blockOcc, Fin.removeNth]
  rw [Fin.sum_univ_succAbove
    (fun b : Fin (k + 1) => blockOcc (p b) (τ b.castSucc) (τ b.succ) i t) j, h,
    blockOcc_self, zero_add]
  refine Finset.sum_congr rfl fun b _ => ?_
  have hleft : τ ((j.castSucc : Fin (k + 2)).succAbove b.castSucc)
      = τ (j.succAbove b).castSucc := by
    rw [Fin.castSucc_succAbove_castSucc]
  have hright : τ ((j.castSucc : Fin (k + 2)).succAbove b.succ) = τ (j.succAbove b).succ := by
    by_cases hb : b.succ = j
    · have hcast : b.castSucc < j := by rw [← hb]; exact Fin.castSucc_lt_succ (i := b)
      rw [hb, Fin.succAbove_castSucc_self, Fin.succAbove_of_castSucc_lt _ _ hcast,
        Fin.succ_castSucc, hb]
      exact h.symm
    · rw [castSucc_succAbove_succ' j b hb]
  rw [hleft, hright]

/-! ### SC03 closure, general form: reduced parameterizations

A parameterization is *reduced* when every block has positive length and no two consecutive
blocks carry the same mode: its blocks are exactly the maximal runs of positive length.
`exists_isReduced` performs both normalization steps at once — deleting zero-length blocks
and merging equal consecutive modes — without changing the cumulative occupation and without
increasing the block count. -/

/-- A block word with ordered times is *reduced* when every block has positive length and no
two consecutive blocks carry the same mode. The blocks of a reduced parameterization are
exactly the maximal runs of positive length. -/
structure IsReduced {k : ℕ} (p : Fin k → Fin n) (τ : Fin (k + 1) → ℝ) : Prop where
  /-- Every block has positive length. -/
  positive : ∀ j : Fin k, τ j.castSucc < τ j.succ
  /-- Consecutive blocks carry different modes. -/
  ne_consecutive : ∀ j j' : Fin k, (j : ℕ) + 1 = (j' : ℕ) → p j ≠ p j'

private theorem exists_isReduced_aux {m : ℕ} (p : Fin m → Fin n) (τ : Fin (m + 1) → ℝ)
    (hτ : Monotone τ) :
    ∃ (c : ℕ) (p' : Fin c → Fin n) (τ' : Fin (c + 1) → ℝ), Monotone τ' ∧
      τ' 0 = τ 0 ∧ τ' (Fin.last c) = τ (Fin.last m) ∧
      occupation p' τ' = occupation p τ ∧ IsReduced p' τ' ∧
      c ≤ (positiveBlocks τ).card := by
  induction m with
  | zero =>
    exact ⟨0, p, τ, hτ, rfl, rfl, rfl, ⟨fun j => j.elim0, fun j => j.elim0⟩, Nat.zero_le _⟩
  | succ m ih =>
    have htail : Monotone (Fin.tail τ) :=
      fun a b hab => hτ (Fin.succ_le_succ_iff.mpr hab)
    obtain ⟨c, p', τ', hm', h0', hl', hocc', hred', hc'⟩ := ih (Fin.tail p) (Fin.tail τ) htail
    have hcard : (positiveBlocks (Fin.tail τ)).card ≤ (positiveBlocks τ).card := by
      calc (positiveBlocks (Fin.tail τ)).card
          = ((positiveBlocks (Fin.tail τ)).image Fin.succ).card :=
            (Finset.card_image_of_injective _ (Fin.succ_injective m)).symm
        _ ≤ (positiveBlocks τ).card := Finset.card_le_card (image_positiveBlocks_tail τ)
    have hlast : Fin.tail τ (Fin.last m) = τ (Fin.last (m + 1)) :=
      congrArg τ (Fin.succ_last m)
    rcases eq_or_lt_of_le (show τ 0 ≤ Fin.tail τ 0 from hτ (Fin.zero_le _)) with heq | hlt
    · exact ⟨c, p', τ', hm', h0'.trans heq.symm, hl'.trans hlast,
        hocc'.trans (occupation_delete p τ heq).symm, hred', hc'.trans hcard⟩
    · have htail' : Monotone (Fin.tail τ') :=
        fun a b hab => hm' (Fin.succ_le_succ_iff.mpr hab)
      by_cases hmg : ∃ j : Fin c, (j : ℕ) = 0 ∧ p 0 = p' j
      · obtain ⟨j0, hj0, hpeq⟩ := hmg
        obtain ⟨d, rfl⟩ : ∃ d, c = d + 1 := ⟨c - 1, by omega⟩
        have hj0' : j0 = (0 : Fin (d + 1)) := by
          apply Fin.ext
          rw [Fin.val_zero]
          exact hj0
        subst hj0'
        have hpeq0 : p 0 = p' 0 := hpeq
        have hlt0 : τ 0 < τ' 0 := by rw [h0']; exact hlt
        have hpos0 : τ' 0 < Fin.tail τ' 0 := by
          have hp := hred'.positive 0
          rw [Fin.castSucc_zero] at hp
          exact hp
        refine ⟨d + 1, p', Fin.cons (τ 0) (Fin.tail τ'), ?_, ?_, ?_, ?_, ⟨?_, ?_⟩,
          hc'.trans hcard⟩
        · refine Fin.monotone_iff_le_succ.mpr fun j => ?_
          refine Fin.cases ?_ ?_ j
          · rw [Fin.castSucc_zero, Fin.cons_zero, Fin.cons_succ]
            linarith
          · intro j1
            rw [← Fin.succ_castSucc, Fin.cons_succ, Fin.cons_succ]
            exact htail' (Fin.castSucc_le_succ j1)
        · exact Fin.cons_zero _ _
        · have hlc : (Fin.last (d + 1) : Fin (d + 2)) = (Fin.last d).succ :=
            (Fin.succ_last d).symm
          rw [hlc, Fin.cons_succ]
          exact (congrArg τ' (Fin.succ_last d)).trans (hl'.trans hlast)
        · funext i t
          have e1 := occupation_succ p' (Fin.cons (τ 0) (Fin.tail τ')) i t
          rw [Fin.cons_zero, Fin.tail_cons] at e1
          have e2 := occupation_succ p' τ' i t
          have e3 := occupation_succ p τ i t
          have e4 : occupation p' τ' i t = occupation (Fin.tail p) (Fin.tail τ) i t := by
            rw [hocc']
          have e5 := blockOcc_merge (p' 0) (τ 0) (τ' 0) (Fin.tail τ' 0) i t
          rw [← h0', hpeq0] at e3
          rw [e1, e3]
          linarith
        · intro j
          refine Fin.cases ?_ ?_ j
          · rw [Fin.castSucc_zero, Fin.cons_zero, Fin.cons_succ]
            linarith
          · intro j1
            rw [← Fin.succ_castSucc, Fin.cons_succ, Fin.cons_succ]
            exact hred'.positive j1.succ
        · exact hred'.ne_consecutive
      · push Not at hmg
        have h0mem : (0 : Fin (m + 1)) ∈ positiveBlocks τ := by
          rw [mem_positiveBlocks, Fin.castSucc_zero]; exact hlt
        have hnot : (0 : Fin (m + 1)) ∉ (positiveBlocks (Fin.tail τ)).image Fin.succ := by
          simp only [Finset.mem_image, not_exists, not_and]
          exact fun j0 _ => Fin.succ_ne_zero j0
        have hconsCard : c + 1 ≤ (positiveBlocks τ).card := by
          calc c + 1 ≤ (positiveBlocks (Fin.tail τ)).card + 1 := by omega
            _ = (insert (0 : Fin (m + 1))
                  ((positiveBlocks (Fin.tail τ)).image Fin.succ)).card := by
              rw [Finset.card_insert_of_notMem hnot,
                Finset.card_image_of_injective _ (Fin.succ_injective m)]
            _ ≤ (positiveBlocks τ).card :=
              Finset.card_le_card (Finset.insert_subset h0mem (image_positiveBlocks_tail τ))
        refine ⟨c + 1, Fin.cons (p 0) p', Fin.cons (τ 0) τ', ?_, ?_, ?_, ?_, ⟨?_, ?_⟩,
          hconsCard⟩
        · refine Fin.monotone_iff_le_succ.mpr fun j => ?_
          refine Fin.cases ?_ ?_ j
          · rw [Fin.castSucc_zero, Fin.cons_zero, Fin.cons_succ, h0']
            exact hlt.le
          · intro j1
            rw [← Fin.succ_castSucc, Fin.cons_succ, Fin.cons_succ]
            exact hm' (Fin.castSucc_le_succ j1)
        · exact Fin.cons_zero _ _
        · have hlc : (Fin.last (c + 1) : Fin (c + 2)) = (Fin.last c).succ :=
            (Fin.succ_last c).symm
          rw [hlc, Fin.cons_succ, hl', hlast]
        · funext i t
          rw [occupation_succ (Fin.cons (p 0) p') (Fin.cons (τ 0) τ'), occupation_succ p τ,
            Fin.cons_zero, Fin.cons_zero, Fin.tail_cons, Fin.tail_cons, hocc', h0']
        · intro j
          refine Fin.cases ?_ ?_ j
          · rw [Fin.castSucc_zero, Fin.cons_zero, Fin.cons_succ, h0']
            exact hlt
          · intro j1
            rw [← Fin.succ_castSucc, Fin.cons_succ, Fin.cons_succ]
            exact hred'.positive j1
        · intro a b
          refine Fin.cases ?_ ?_ a
          · refine Fin.cases ?_ ?_ b
            · intro hab
              simp only [Fin.val_zero] at hab
              omega
            · intro b1 hab
              have hb1 : (b1 : ℕ) = 0 := by
                simp only [Fin.val_zero, Fin.val_succ] at hab; omega
              rw [Fin.cons_zero, Fin.cons_succ]
              exact hmg b1 hb1
          · intro a1
            refine Fin.cases ?_ ?_ b
            · intro hab
              simp only [Fin.val_zero, Fin.val_succ] at hab
              omega
            · intro b1 hab
              rw [Fin.cons_succ, Fin.cons_succ]
              refine hred'.ne_consecutive a1 b1 ?_
              simp only [Fin.val_succ] at hab
              omega

/-- **SC03 closure claim, full form.** Deleting zero-length blocks and merging equal
consecutive modes turns any parameterization into a reduced one — every block of positive
length, no two consecutive blocks sharing a mode, so the blocks are exactly the maximal runs
— with the same cumulative occupation and no more blocks than the original had
positive-length blocks. -/
theorem exists_isReduced {m : ℕ} {T : ℝ} (p : Fin m → Fin n) (τ : Fin (m + 1) → ℝ)
    (hτ : OrderedTimes τ T) :
    ∃ (c : ℕ) (p' : Fin c → Fin n) (τ' : Fin (c + 1) → ℝ),
      OrderedTimes τ' T ∧ IsReduced p' τ' ∧ occupation p' τ' = occupation p τ ∧
      c ≤ (positiveBlocks τ).card := by
  obtain ⟨c, p', τ', hm', h0', hl', hocc', hred', hc'⟩ := exists_isReduced_aux p τ hτ.mono
  exact ⟨c, p', τ', ⟨h0'.trans hτ.first, hl'.trans hτ.last, hm'⟩, hred', hocc', hc'⟩

/-- A schedule lies in the class whose budget is the number of maximal runs of its
positive-length blocks: if the reduced parameterization `(q, σ)` has the same cumulative
occupation as `(p, τ)` and `r` blocks, then `(p, τ)` is a schedule for every budget `k ≥ r`.
Existence of such a `(q, σ)` is `exists_isReduced`. -/
theorem isSchedule_of_isReduced (hn : 0 < n) {m r k : ℕ} {T : ℝ}
    {p : Fin m → Fin n} {τ : Fin (m + 1) → ℝ}
    {q : Fin r → Fin n} {σ : Fin (r + 1) → ℝ} (hσ : OrderedTimes σ T) (_hq : IsReduced q σ)
    (hocc : occupation q σ = occupation p τ) (hrk : r ≤ k) :
    IsSchedule k T (occupation p τ) :=
  IsSchedule.mono hn hrk ⟨q, σ, hσ, hocc.symm⟩

/-- Packaged run form: a parameterization whose reduction has at most `k` blocks — that is,
whose positive-length blocks form at most `k` maximal runs — is a schedule for the budget
`k`. -/
theorem isSchedule_of_card_runs (hn : 0 < n) {m k : ℕ} {T : ℝ}
    (p : Fin m → Fin n) (τ : Fin (m + 1) → ℝ)
    (h : ∃ (r : ℕ) (q : Fin r → Fin n) (σ : Fin (r + 1) → ℝ), r ≤ k ∧ OrderedTimes σ T ∧
      IsReduced q σ ∧ occupation q σ = occupation p τ) :
    IsSchedule k T (occupation p τ) := by
  obtain ⟨r, q, σ, hrk, hσ, hq, hocc⟩ := h
  exact isSchedule_of_isReduced hn hσ hq hocc hrk

/-! ### Congruence of the errors and optima on the horizon

Every quantity of SC04 reads the inputs only on `[0, T]`, so two inputs that agree there have
the same errors, instance optima and grid instance optima. These lemmas are what lets SC02's
converse transport `F` and `Gminus` between the cumulative class and relaxed controls; see
`GridSwitching.F_eq_sSup_simplexRates` in `Formal.GridSwitching.Cumulative`. -/

/-- Inputs agreeing on the horizon have the same error set. -/
theorem errorSet_congr_of_eqOn {A B W : Fin n → ℝ → ℝ} {T : ℝ}
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, A i t = B i t) :
    errorSet A W T = errorSet B W T := by
  ext e
  constructor
  · rintro ⟨i, t, ht, rfl⟩; exact ⟨i, t, ht, by rw [h i t ht]⟩
  · rintro ⟨i, t, ht, rfl⟩; exact ⟨i, t, ht, by rw [h i t ht]⟩

/-- Inputs agreeing on the horizon have the same full error. -/
theorem D_congr_of_eqOn {A B W : Fin n → ℝ → ℝ} {T : ℝ}
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, A i t = B i t) : D A W T = D B W T := by
  rw [D, D, errorSet_congr_of_eqOn h]

/-- Inputs agreeing on the horizon have the same one-sided error set. -/
theorem lowerErrorSet_congr_of_eqOn {A B W : Fin n → ℝ → ℝ} {T : ℝ}
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, A i t = B i t) :
    lowerErrorSet A W T = lowerErrorSet B W T := by
  ext e
  constructor
  · rintro ⟨i, t, ht, rfl⟩; exact ⟨i, t, ht, by rw [h i t ht]⟩
  · rintro ⟨i, t, ht, rfl⟩; exact ⟨i, t, ht, by rw [h i t ht]⟩

/-- Inputs agreeing on the horizon have the same one-sided error. -/
theorem Dminus_congr_of_eqOn {A B W : Fin n → ℝ → ℝ} {T : ℝ}
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, A i t = B i t) :
    Dminus A W T = Dminus B W T := by
  rw [Dminus, Dminus, lowerErrorSet_congr_of_eqOn h]

/-- Inputs agreeing on the horizon have the same continuous instance optimum. -/
theorem OPT_congr_of_eqOn {A B : Fin n → ℝ → ℝ} {T : ℝ} {s : ℕ}
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, A i t = B i t) : OPT A T s = OPT B T s := by
  rw [OPT, OPT]
  congr 1
  ext e
  constructor
  · rintro ⟨W, hW, rfl⟩; exact ⟨W, hW, D_congr_of_eqOn h⟩
  · rintro ⟨W, hW, rfl⟩; exact ⟨W, hW, (D_congr_of_eqOn h).symm⟩

/-- Inputs agreeing on the horizon have the same one-sided instance optimum. -/
theorem OPTminus_congr_of_eqOn {A B : Fin n → ℝ → ℝ} {T : ℝ} {k : ℕ}
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, A i t = B i t) :
    OPTminus A T k = OPTminus B T k := by
  rw [OPTminus, OPTminus]
  congr 1
  ext e
  constructor
  · rintro ⟨W, hW, rfl⟩; exact ⟨W, hW, Dminus_congr_of_eqOn h⟩
  · rintro ⟨W, hW, rfl⟩; exact ⟨W, hW, (Dminus_congr_of_eqOn h).symm⟩

/-- Inputs agreeing on the horizon have the same grid instance optimum. -/
theorem gridOPT_congr_of_eqOn {x : Fin (N + 1) → ℝ} {A B : Fin n → ℝ → ℝ} {T : ℝ} {s : ℕ}
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, A i t = B i t) :
    gridOPT x A T s = gridOPT x B T s := by
  rw [gridOPT, gridOPT]
  congr 1
  ext e
  constructor
  · rintro ⟨W, hW, rfl⟩; exact ⟨W, hW, D_congr_of_eqOn h⟩
  · rintro ⟨W, hW, rfl⟩; exact ⟨W, hW, (D_congr_of_eqOn h).symm⟩

/-- Inputs agreeing on the horizon have the same one-sided grid instance optimum. -/
theorem gridOPTminus_congr_of_eqOn {x : Fin (N + 1) → ℝ} {A B : Fin n → ℝ → ℝ} {T : ℝ} {k : ℕ}
    (h : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, A i t = B i t) :
    gridOPTminus x A T k = gridOPTminus x B T k := by
  rw [gridOPTminus, gridOPTminus]
  congr 1
  ext e
  constructor
  · rintro ⟨W, hW, rfl⟩; exact ⟨W, hW, Dminus_congr_of_eqOn h⟩
  · rintro ⟨W, hW, rfl⟩; exact ⟨W, hW, (Dminus_congr_of_eqOn h).symm⟩

/-! ### Grid-constant inputs are cumulative allocations of genuine relaxed controls

`gridCumulative` is defined by a formula. This section exhibits the piecewise-constant
relaxed control it represents: the cell indicators `cellPulse` (with the initial time
assigned to the first cell, so that the rates sum to one at *every* time of the closed
horizon), weighted by the rows of the rate matrix. -/

/-- The indicator of the times at most `c`. -/
noncomputable def step (c t : ℝ) : ℝ := if t ≤ c then 1 else 0

theorem step_nonneg (c t : ℝ) : 0 ≤ step c t := by
  rw [step]; split_ifs <;> norm_num

theorem step_mono_right {c d : ℝ} (h : c ≤ d) (t : ℝ) : step c t ≤ step d t := by
  by_cases h1 : t ≤ c
  · rw [step, step, if_pos h1, if_pos (h1.trans h)]
  · rw [step, if_neg h1]; exact step_nonneg d t

theorem measurable_step (c : ℝ) : Measurable (step c) := by
  unfold step
  exact Measurable.ite measurableSet_Iic measurable_const measurable_const

theorem intervalIntegrable_step (c a b : ℝ) : IntervalIntegrable (step c) volume a b := by
  rw [intervalIntegrable_iff]
  have hfin : volume (uIoc a b) ≠ ⊤ := by rw [Set.uIoc]; exact measure_Ioc_lt_top.ne
  refine (integrableOn_const (C := (1 : ℝ)) hfin).mono'
    (measurable_step c).aestronglyMeasurable ?_
  filter_upwards with u
  rw [Real.norm_eq_abs, step]
  split_ifs <;> norm_num

/-- The integral of a half-line indicator over `[0, t]` is the clipped endpoint. -/
theorem integral_step {c t : ℝ} (hc : 0 ≤ c) (ht : 0 ≤ t) :
    ∫ u in (0 : ℝ)..t, step c u = min t c := by
  rw [intervalIntegral.integral_of_le ht]
  have hind : ∀ u : ℝ, step c u = (Set.Iic c).indicator (fun _ => (1 : ℝ)) u := by
    intro u; rw [step, Set.indicator_apply]; rfl
  simp only [hind]
  rw [MeasureTheory.setIntegral_indicator measurableSet_Iic, Set.Ioc_inter_Iic,
    MeasureTheory.setIntegral_const, Real.volume_real_Ioc_of_le (le_min ht hc),
    sub_zero, smul_eq_mul, mul_one]

/-- Indicator of grid cell `j`, with the initial time assigned to the first cell so that the
cell indicators sum to one at every time of the closed horizon. -/
noncomputable def cellPulse (x : Fin (N + 1) → ℝ) (j : Fin N) (t : ℝ) : ℝ :=
  if (j : ℕ) = 0 then step (x j.succ) t else step (x j.succ) t - step (x j.castSucc) t

theorem cellPulse_apply_of_zero {x : Fin (N + 1) → ℝ} {j : Fin N} (h : (j : ℕ) = 0) (t : ℝ) :
    cellPulse x j t = step (x j.succ) t := if_pos h

theorem cellPulse_apply_of_ne {x : Fin (N + 1) → ℝ} {j : Fin N} (h : (j : ℕ) ≠ 0) (t : ℝ) :
    cellPulse x j t = step (x j.succ) t - step (x j.castSucc) t := if_neg h

theorem measurable_cellPulse (x : Fin (N + 1) → ℝ) (j : Fin N) :
    Measurable (cellPulse x j) := by
  by_cases h : (j : ℕ) = 0
  · have he : cellPulse x j = step (x j.succ) := funext (cellPulse_apply_of_zero h)
    rw [he]; exact measurable_step _
  · have he : cellPulse x j = fun t => step (x j.succ) t - step (x j.castSucc) t :=
      funext (cellPulse_apply_of_ne h)
    rw [he]; exact (measurable_step _).sub (measurable_step _)

theorem cellPulse_nonneg {x : Fin (N + 1) → ℝ} (hx : Monotone x) (j : Fin N) (t : ℝ) :
    0 ≤ cellPulse x j t := by
  by_cases h : (j : ℕ) = 0
  · rw [cellPulse_apply_of_zero h]; exact step_nonneg _ _
  · rw [cellPulse_apply_of_ne h]
    exact sub_nonneg.mpr (step_mono_right (hx (Fin.castSucc_le_succ j)) t)

theorem intervalIntegrable_cellPulse (x : Fin (N + 1) → ℝ) (j : Fin N) (a b : ℝ) :
    IntervalIntegrable (cellPulse x j) volume a b := by
  by_cases h : (j : ℕ) = 0
  · have he : cellPulse x j = step (x j.succ) := funext (cellPulse_apply_of_zero h)
    rw [he]; exact intervalIntegrable_step _ _ _
  · have he : cellPulse x j = fun t => step (x j.succ) t - step (x j.castSucc) t :=
      funext (cellPulse_apply_of_ne h)
    rw [he]; exact (intervalIntegrable_step _ _ _).sub (intervalIntegrable_step _ _ _)

/-- The cell indicators sum to one up to the last grid point, at every time. -/
theorem cellPulse_sum (hN : 0 < N) (x : Fin (N + 1) → ℝ) (t : ℝ) :
    ∑ j : Fin N, cellPulse x j t = step (x (Fin.last N)) t := by
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 1 := ⟨N - 1, by omega⟩
  rw [Fin.sum_univ_succ]
  have h0 : cellPulse x 0 t = step (x (0 : Fin (M + 1)).succ) t :=
    cellPulse_apply_of_zero (by simp) t
  have hs : ∀ j : Fin M, cellPulse x j.succ t =
      step (x j.succ.succ) t - step (x j.castSucc.succ) t := by
    intro j
    rw [cellPulse_apply_of_ne (by simp) t, ← Fin.succ_castSucc]
  have ht : ∑ j : Fin M, (step (x j.succ.succ) t - step (x j.castSucc.succ) t) =
      step (x (Fin.last M).succ) t - step (x (0 : Fin (M + 1)).succ) t :=
    sum_succ_sub_castSucc fun u : Fin (M + 1) => step (x u.succ) t
  have hlast : ((Fin.last M).succ : Fin (M + 2)) = Fin.last (M + 1) := Fin.succ_last M
  rw [h0, Finset.sum_congr rfl fun j _ => hs j, ht, hlast]
  ring

/-- The piecewise-constant relaxed control described by a per-cell rate matrix. -/
noncomputable def gridRateFun (x : Fin (N + 1) → ℝ) (r : Fin N → Fin n → ℝ) (i : Fin n)
    (t : ℝ) : ℝ :=
  ∑ j : Fin N, r j i * cellPulse x j t

/-- A rate matrix on a grid really does define a relaxed control. -/
theorem simplexRates_gridRateFun (hN : 0 < N) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : OrderedTimes x T) {r : Fin N → Fin n → ℝ} (hr : IsRateMatrix r) :
    SimplexRates (gridRateFun x r) T where
  measurable i :=
    (Finset.measurable_sum Finset.univ fun j _ =>
      measurable_const.mul (measurable_cellPulse x j)).aestronglyMeasurable
  nonneg t _ i :=
    Finset.sum_nonneg fun j _ => mul_nonneg (hr.nonneg j i) (cellPulse_nonneg hx.mono j t)
  conservation t ht := by
    simp only [gridRateFun]
    rw [Finset.sum_comm]
    have h : ∀ j : Fin N, (∑ i, r j i * cellPulse x j t) = cellPulse x j t := by
      intro j; rw [← Finset.sum_mul, hr.conservation j, one_mul]
    simp only [h]
    rw [cellPulse_sum hN x t, hx.last]
    simp [step, ht.2]

/-- The integral of a cell indicator is the cell's clipped length. -/
theorem integral_cellPulse {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : OrderedTimes x T) (j : Fin N)
    {t : ℝ} (ht : 0 ≤ t) :
    ∫ u in (0 : ℝ)..t, cellPulse x j u = min t (x j.succ) - min t (x j.castSucc) := by
  by_cases h : (j : ℕ) = 0
  · have hzero : x j.castSucc = 0 := by
      have hj : j.castSucc = (0 : Fin (N + 1)) := Fin.ext (by simpa using h)
      rw [hj, hx.first]
    rw [hzero, min_eq_right ht, sub_zero,
      intervalIntegral.integral_congr (g := step (x j.succ))
        fun u _ => cellPulse_apply_of_zero h u,
      integral_step (hx.nonneg j.succ) ht]
  · rw [intervalIntegral.integral_congr
      (g := fun u => step (x j.succ) u - step (x j.castSucc) u)
      fun u _ => cellPulse_apply_of_ne h u,
      intervalIntegral.integral_sub (intervalIntegrable_step _ _ _)
        (intervalIntegrable_step _ _ _),
      integral_step (hx.nonneg j.succ) ht, integral_step (hx.nonneg j.castSucc) ht]

/-- The cumulative allocation of the piecewise-constant control is exactly the formula
`gridCumulative`. -/
theorem cumulative_gridRateFun {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : OrderedTimes x T)
    (r : Fin N → Fin n → ℝ) (i : Fin n) {t : ℝ} (ht : 0 ≤ t) :
    cumulative (gridRateFun x r) i t = gridCumulative x r i t := by
  rw [cumulative]
  simp only [gridRateFun, gridCumulative]
  rw [intervalIntegral.integral_finsetSum
    fun j _ => (intervalIntegrable_cellPulse x j 0 t).const_mul (r j i)]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [intervalIntegral.integral_const_mul, integral_cellPulse hx j ht]

/-- **The grid input class consists of genuine relaxed controls.** Every grid-constant
cumulative allocation is the cumulative allocation of an explicit piecewise-constant
`SimplexRates` control. -/
theorem IsGridConstant.exists_simplexRates (hN : 0 < N) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : OrderedTimes x T) {A : Fin n → ℝ → ℝ} (hA : IsGridConstant x A) :
    ∃ α : Fin n → ℝ → ℝ, SimplexRates α T ∧
      ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, cumulative α i t = A i t := by
  obtain ⟨r, hr, rfl⟩ := hA
  exact ⟨gridRateFun x r, simplexRates_gridRateFun hN hx hr,
    fun i _ ht => cumulative_gridRateFun hx r i ht.1⟩

/-- A grid on a positive horizon has at least one cell. -/
theorem IsGrid.pos_of_horizon_pos {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    (hT : 0 < T) : 0 < N := by
  by_contra hcon
  have hN : N = 0 := by omega
  subst hN
  have hfin : (Fin.last 0 : Fin (0 + 1)) = 0 := Fin.ext (by simp)
  have he : x (Fin.last 0) = x 0 := congrArg x hfin
  rw [hx.last, hx.first] at he
  exact hT.ne' he

end GridSwitching
