import Formal.GridSwitching.Model

/-!
# SC02, converse direction: every cumulative vector comes from a relaxed control

`SimplexRates.isCumulative` in `Formal.GridSwitching.Model` shows that the cumulative
allocation of a relaxed control satisfies `IsCumulative`. This module proves the converse
asserted after `eq:cumulatives`: every `IsCumulative` vector is the cumulative allocation of
some relaxed control.

The argument follows the source. A coordinate `A i` is extended from `[0, T]` to all of `ℝ`
by clamping the time argument (`extended`); the extension is monotone and `1`-Lipschitz, hence
absolutely continuous, hence differentiable almost everywhere with
`∫_0^t (A i)' = A i t - A i 0`. Its derivative is nonnegative because the extension is
monotone, and differentiating the conservation identity `∑ i, A i t = t` on the open horizon
shows that the derivatives sum to one almost everywhere.

The rates must satisfy the simplex conditions at *every* time of the horizon, not merely
almost everywhere, so `derivRates` replaces the derivative vector by the uniform vector
`(1/n, ..., 1/n)` at the null set of times where the derivatives fail to sum to one. This
changes no integral.

The Mathlib inputs are `Monotone.ae_differentiableAt`,
`LipschitzOnWith.absolutelyContinuousOnInterval` and
`AbsolutelyContinuousOnInterval.integral_deriv_eq_sub`.
-/

namespace GridSwitching

open MeasureTheory Set

variable {n : ℕ}

/-! ## Clamping the time argument -/

/-- Time clamped to the horizon `[0, T]`. -/
noncomputable def clampTime (T t : ℝ) : ℝ := max 0 (min t T)

theorem clampTime_mem {T : ℝ} (hT : 0 ≤ T) (t : ℝ) : clampTime T t ∈ Icc (0 : ℝ) T :=
  ⟨le_max_left _ _, max_le hT (min_le_right _ _)⟩

theorem clampTime_mono (T : ℝ) : Monotone (clampTime T) :=
  fun _ _ h => max_le_max le_rfl (min_le_min h le_rfl)

theorem clampTime_eq_self {T t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) : clampTime T t = t := by
  rw [clampTime, min_eq_left ht.2, max_eq_right ht.1]

theorem clampTime_zero {T : ℝ} (hT : 0 ≤ T) : clampTime T 0 = 0 :=
  clampTime_eq_self ⟨le_rfl, hT⟩

theorem clampTime_sub_le {T s t : ℝ} (h : s ≤ t) :
    clampTime T t - clampTime T s ≤ t - s := by
  simp only [clampTime, max_def, min_def]
  split_ifs <;> linarith

/-! ## The clamped extension of a cumulative allocation -/

/-- A cumulative allocation extended to all of `ℝ` by clamping the time to the horizon. -/
noncomputable def extended (A : Fin n → ℝ → ℝ) (T : ℝ) (i : Fin n) (t : ℝ) : ℝ :=
  A i (clampTime T t)

theorem extended_eq {A : Fin n → ℝ → ℝ} {T t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) (i : Fin n) :
    extended A T i t = A i t := by rw [extended, clampTime_eq_self ht]

theorem extended_zero {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T)
    (i : Fin n) : extended A T i 0 = 0 := by
  rw [extended_eq ⟨le_rfl, hT⟩ i, hA.initial]

/-- The increment of a clamped extension is nonnegative and bounded by elapsed time. -/
theorem extended_increment {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T)
    (i : Fin n) {a b : ℝ} (hab : a ≤ b) :
    0 ≤ extended A T i b - extended A T i a ∧
      extended A T i b - extended A T i a ≤ b - a := by
  have hca := clampTime_mem (T := T) hT a
  have hcb := clampTime_mem (T := T) hT b
  have hle : clampTime T a ≤ clampTime T b := clampTime_mono T hab
  refine ⟨?_, ?_⟩
  · have := hA.mono i _ _ hca.1 hle hcb.2
    simpa [extended] using this
  · have h1 := hA.lipschitz i _ _ hca.1 hle hcb.2
    have h2 := clampTime_sub_le (T := T) hab
    simp only [extended]
    linarith

theorem extended_monotone {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T)
    (i : Fin n) : Monotone (extended A T i) :=
  fun _ _ hab => by linarith [(extended_increment hA hT i hab).1]

theorem extended_lipschitz {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T)
    (i : Fin n) : LipschitzWith 1 (extended A T i) := by
  refine LipschitzWith.of_dist_le_mul fun a b => ?_
  rw [Real.dist_eq, Real.dist_eq, NNReal.coe_one, one_mul]
  rcases le_total a b with h | h
  · obtain ⟨h1, h2⟩ := extended_increment hA hT i h
    rw [abs_sub_comm a b, abs_sub_comm (extended A T i a),
      abs_of_nonneg (by linarith : (0 : ℝ) ≤ b - a), abs_of_nonneg h1]
    linarith
  · obtain ⟨h1, h2⟩ := extended_increment hA hT i h
    rw [abs_of_nonneg (by linarith : (0 : ℝ) ≤ a - b), abs_of_nonneg h1]
    linarith

theorem extended_sum {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T)
    (t : ℝ) : ∑ i, extended A T i t = clampTime T t :=
  hA.conservation _ (clampTime_mem hT t)

/-! ## The recovered relaxed control -/

/-- The relaxed control recovered from a cumulative allocation: the derivative of the clamped
extension, replaced by the uniform simplex point on the null set of times where the
derivatives fail to sum to one. -/
noncomputable def derivRates (A : Fin n → ℝ → ℝ) (T : ℝ) (i : Fin n) (t : ℝ) : ℝ :=
  if ∑ j, deriv (extended A T j) t = 1 then deriv (extended A T i) t else (n : ℝ)⁻¹

theorem measurable_derivRates (A : Fin n → ℝ → ℝ) (T : ℝ) (i : Fin n) :
    Measurable (derivRates A T i) := by
  have hm : Measurable fun t => ∑ j, deriv (extended A T j) t :=
    Finset.univ.measurable_sum fun j _ => measurable_deriv _
  exact Measurable.ite (hm (measurableSet_singleton 1)) (measurable_deriv _) measurable_const

/-- The recovered rates are nonnegative everywhere. -/
theorem derivRates_nonneg {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T)
    (i : Fin n) (t : ℝ) : 0 ≤ derivRates A T i t := by
  rw [derivRates]
  split_ifs
  · exact (extended_monotone hA hT i).deriv_nonneg
  · positivity

/-- The recovered rates sum to one everywhere. -/
theorem derivRates_sum (hn : 0 < n) (A : Fin n → ℝ → ℝ) (T : ℝ) (t : ℝ) :
    ∑ i, derivRates A T i t = 1 := by
  by_cases h : ∑ j, deriv (extended A T j) t = 1
  · have hi : ∀ i : Fin n, derivRates A T i t = deriv (extended A T i) t := fun _ => if_pos h
    rw [Finset.sum_congr rfl fun i _ => hi i]
    exact h
  · have hn' : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn.ne'
    have hi : ∀ i : Fin n, derivRates A T i t = (n : ℝ)⁻¹ := fun _ => if_neg h
    rw [Finset.sum_congr rfl fun i _ => hi i, Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, nsmul_eq_mul, mul_inv_cancel₀ hn']

/-- SC02, converse direction: the recovered rates form a relaxed control. -/
theorem simplexRates_derivRates (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) : SimplexRates (derivRates A T) T where
  measurable i := (measurable_derivRates A T i).aestronglyMeasurable
  nonneg t _ i := derivRates_nonneg hA hT i t
  conservation t _ := derivRates_sum hn A T t

/-- Differentiating the conservation identity: almost everywhere on the open horizon the
derivatives of the clamped extensions sum to one. -/
theorem ae_sum_deriv_extended {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) :
    ∀ᵐ t : ℝ, t ∈ Ioo (0 : ℝ) T → ∑ j, deriv (extended A T j) t = 1 := by
  have hdiff : ∀ᵐ t : ℝ, ∀ j : Fin n, DifferentiableAt ℝ (extended A T j) t :=
    MeasureTheory.ae_all_iff.mpr fun j => (extended_monotone hA hT j).ae_differentiableAt
  filter_upwards [hdiff] with t ht htmem
  have hsum : HasDerivAt (∑ j : Fin n, extended A T j)
      (∑ j, deriv (extended A T j) t) t :=
    HasDerivAt.sum fun j _ => (ht j).hasDerivAt
  have heq : (id : ℝ → ℝ) =ᶠ[nhds t] (∑ j : Fin n, extended A T j) := by
    filter_upwards [Ioo_mem_nhds htmem.1 htmem.2] with s hs
    rw [Finset.sum_apply, extended_sum hA hT s, clampTime_eq_self ⟨hs.1.le, hs.2.le⟩]
    rfl
  exact (hsum.congr_of_eventuallyEq heq).unique (hasDerivAt_id t)

/-- The fundamental theorem of calculus for the clamped extension, which is Lipschitz and
hence absolutely continuous. -/
theorem integral_deriv_extended {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hT : 0 ≤ T) (i : Fin n) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) :
    ∫ s in (0 : ℝ)..t, deriv (extended A T i) s = A i t := by
  have hac : AbsolutelyContinuousOnInterval (extended A T i) 0 t :=
    ((extended_lipschitz hA hT i).lipschitzOnWith).absolutelyContinuousOnInterval
  rw [hac.integral_deriv_eq_sub, extended_eq ht i, extended_zero hA hT i, sub_zero]

/-- The recovered rates integrate back to the given cumulative allocation. -/
theorem cumulative_derivRates {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) (i : Fin n) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) :
    cumulative (derivRates A T) i t = A i t := by
  have hcongr : ∀ᵐ s : ℝ, s ∈ uIoc (0 : ℝ) t →
      derivRates A T i s = deriv (extended A T i) s := by
    have hne : ∀ᵐ s : ℝ, s ≠ T := by
      rw [MeasureTheory.ae_iff]
      simp
    filter_upwards [ae_sum_deriv_extended hA hT, hne] with s h1 h2 hs
    rw [uIoc_of_le ht.1] at hs
    have hmem : s ∈ Ioo (0 : ℝ) T :=
      ⟨hs.1, lt_of_le_of_ne (hs.2.trans ht.2) h2⟩
    rw [derivRates, if_pos (h1 hmem)]
  rw [cumulative, intervalIntegral.integral_congr_ae hcongr,
    integral_deriv_extended hA hT i ht]

/-- **SC02, converse direction.** Every vector in the cumulative class `Acal_n(T)` is the
cumulative allocation of a relaxed control. -/
theorem exists_simplexRates_cumulative (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hT : 0 ≤ T) (hA : IsCumulative A T) :
    ∃ α : Fin n → ℝ → ℝ, SimplexRates α T ∧
      ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, cumulative α i t = A i t :=
  ⟨derivRates A T, simplexRates_derivRates hn hA hT,
    fun i _ ht => cumulative_derivRates hA hT i ht⟩

/-- **SC02.** The cumulative class is exactly the class of cumulative allocations of relaxed
controls, up to agreement on the horizon. -/
theorem isCumulative_iff_exists_simplexRates (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hT : 0 ≤ T) :
    IsCumulative A T ↔ ∃ α : Fin n → ℝ → ℝ, SimplexRates α T ∧
      ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, cumulative α i t = A i t := by
  refine ⟨exists_simplexRates_cumulative hn hT, ?_⟩
  rintro ⟨α, hα, hAα⟩
  refine ⟨fun i => ?_, fun i s t hs hst ht => ?_, fun i s t hs hst ht => ?_, fun t ht => ?_⟩
  · rw [← hAα i 0 ⟨le_rfl, hT⟩, cumulative_zero]
  · rw [← hAα i s ⟨hs, hst.trans ht⟩, ← hAα i t ⟨hs.trans hst, ht⟩]
    exact cumulative_mono hα i hs hst ht
  · rw [← hAα i s ⟨hs, hst.trans ht⟩, ← hAα i t ⟨hs.trans hst, ht⟩]
    exact cumulative_increment_le hα i hs hst ht
  · have hs : ∑ i, A i t = ∑ i, cumulative α i t :=
      Finset.sum_congr rfl fun i _ => (hAα i t ht).symm
    rw [hs]
    exact cumulative_conservation hα ht

/-! ## SC04 over relaxed controls

`F` and `Gminus` are defined in `Formal.GridSwitching.Model` as suprema over the cumulative
class `IsCumulative`. The source `eq:minimax-values` takes the supremum over relaxed
controls. The two agree, and that is exactly where the SC02 converse is load-bearing for
SC04: the inclusion of the relaxed-control set into the cumulative set is
`SimplexRates.isCumulative`, and the reverse inclusion is
`exists_simplexRates_cumulative` combined with `OPT_congr_of_eqOn` and
`OPTminus_congr_of_eqOn`, since the instance optima read the input only on `[0, T]`. -/

/-- **`F` is the source's supremum over relaxed controls.** -/
theorem F_eq_sSup_simplexRates (hn : 0 < n) {s : ℕ} {T : ℝ} (hT : 0 ≤ T) :
    F n s T = sSup {v : ℝ | ∃ α : Fin n → ℝ → ℝ, SimplexRates α T ∧
      v = OPT (cumulative α) T s} := by
  rw [F]
  congr 1
  ext v
  constructor
  · rintro ⟨A, hA, rfl⟩
    obtain ⟨α, hα, hAα⟩ := exists_simplexRates_cumulative hn hT hA
    exact ⟨α, hα, OPT_congr_of_eqOn fun i t ht => (hAα i t ht).symm⟩
  · rintro ⟨α, hα, rfl⟩
    exact ⟨cumulative α, hα.isCumulative, rfl⟩

/-- **`Gminus` is the source's supremum over relaxed controls.** -/
theorem Gminus_eq_sSup_simplexRates (hn : 0 < n) {k : ℕ} {T : ℝ} (hT : 0 ≤ T) :
    Gminus n k T = sSup {v : ℝ | ∃ α : Fin n → ℝ → ℝ, SimplexRates α T ∧
      v = OPTminus (cumulative α) T k} := by
  rw [Gminus]
  congr 1
  ext v
  constructor
  · rintro ⟨A, hA, rfl⟩
    obtain ⟨α, hα, hAα⟩ := exists_simplexRates_cumulative hn hT hA
    exact ⟨α, hα, OPTminus_congr_of_eqOn fun i t ht => (hAα i t ht).symm⟩
  · rintro ⟨α, hα, rfl⟩
    exact ⟨cumulative α, hα.isCumulative, rfl⟩

end GridSwitching
