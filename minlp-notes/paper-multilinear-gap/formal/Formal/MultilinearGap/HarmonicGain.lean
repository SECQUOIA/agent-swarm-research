import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Formal.MultilinearGap.HarmonicDensity
import Formal.MultilinearGap.AsymptoticScalars

namespace MultilinearGap

open scoped BigOperators
open MeasureTheory Set

noncomputable section

/-- A lower bound for an independent union probability, without an exponential remainder. -/
theorem one_add_sum_mul_prod_one_sub_le_one {I : Type*} (s : Finset I) (q : I → ℝ)
    (hq : ∀ i ∈ s, 0 ≤ q i ∧ q i ≤ 1) :
    (1 + ∑ i ∈ s, q i) * ∏ i ∈ s, (1 - q i) ≤ 1 := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert i s hi ih =>
    have hqi := hq i (Finset.mem_insert_self i s)
    have hqs : ∀ j ∈ s, 0 ≤ q j ∧ q j ≤ 1 := fun j hj =>
      hq j (Finset.mem_insert_of_mem hj)
    have hS : 0 ≤ ∑ j ∈ s, q j := Finset.sum_nonneg fun j hj => (hqs j hj).1
    have hP : 0 ≤ ∏ j ∈ s, (1 - q j) :=
      Finset.prod_nonneg fun j hj => sub_nonneg.mpr (hqs j hj).2
    have hstep : (1 + (q i + ∑ j ∈ s, q j)) * (1 - q i) ≤
        1 + ∑ j ∈ s, q j := by nlinarith [sq_nonneg (q i), mul_nonneg hqi.1 hS]
    simp only [Finset.sum_insert hi, Finset.prod_insert hi]
    calc
      (1 + (q i + ∑ j ∈ s, q j)) * ((1 - q i) * ∏ j ∈ s, (1 - q j))
          = ((1 + (q i + ∑ j ∈ s, q j)) * (1 - q i)) * ∏ j ∈ s, (1 - q j) := by ring
      _ ≤ (1 + ∑ j ∈ s, q j) * ∏ j ∈ s, (1 - q j) :=
        mul_le_mul_of_nonneg_right hstep hP
      _ ≤ 1 := ih hqs

/-- The independent union probability dominates `z / (1 + z)` when the sum
of its Bernoulli probabilities is at least `z`. -/
theorem union_ge_div_one_add {I : Type*} (s : Finset I) (q : I → ℝ)
    (hq : ∀ i ∈ s, 0 ≤ q i ∧ q i ≤ 1) {z : ℝ}
    (hz : 0 ≤ z) (hsum : z ≤ ∑ i ∈ s, q i) :
    z / (1 + z) ≤ 1 - ∏ i ∈ s, (1 - q i) := by
  have hS : 0 ≤ ∑ i ∈ s, q i := hz.trans hsum
  have hmain := one_add_sum_mul_prod_one_sub_le_one s q hq
  have hbound : (∑ i ∈ s, q i) / (1 + ∑ i ∈ s, q i) ≤
      1 - ∏ i ∈ s, (1 - q i) := by
    apply (div_le_iff₀ (by positivity : 0 < 1 + ∑ i ∈ s, q i)).mpr
    nlinarith
  refine le_trans ?_ hbound
  apply (div_le_div_iff₀ (by positivity) (by positivity)).mpr
  nlinarith

/-- A uniform small upper bound on `z` gives a linear union estimate. -/
theorem union_ge_div_one_add_of_le {I : Type*} (s : Finset I) (q : I → ℝ)
    (hq : ∀ i ∈ s, 0 ≤ q i ∧ q i ≤ 1) {z δ : ℝ}
    (hz : 0 ≤ z) (hδ : z ≤ δ) (hsum : z ≤ ∑ i ∈ s, q i) :
    z / (1 + δ) ≤ 1 - ∏ i ∈ s, (1 - q i) := by
  exact (div_le_div_of_nonneg_left hz (by positivity) (by linarith)).trans
    (union_ge_div_one_add s q hq hz hsum)

/-- Integrate the reciprocal lower bound on the one-low window. -/
theorem harmonic_window_integral {T a β Λ δ : ℝ}
    (hT : 0 < T) (ha : 0 < a) (hβ : 0 < β) (_hΛ : 0 < Λ)
    (_hδ : 0 ≤ δ) :
    (∫ t in (T / a)..(β * T), ((1 - β) * T / (Λ * t)) / (1 + δ)) =
      ((1 - β) / (1 + δ) * Real.log (β * a) / Λ) * T := by
  have hleft : 0 < T / a := div_pos hT ha
  have hright : 0 < β * T := mul_pos hβ hT
  have heq : (fun t : ℝ => ((1 - β) * T / (Λ * t)) / (1 + δ)) =
      (fun t : ℝ => ((1 - β) * T / Λ / (1 + δ)) * t⁻¹) := by
    funext t
    simp only [div_eq_mul_inv, mul_inv_rev]
    ring
  rw [heq, intervalIntegral.integral_const_mul, integral_inv_of_pos hleft hright]
  have hratio : β * T / (T / a) = β * a := by field_simp
  rw [hratio]
  ring

/-- The harmonic gain on a positive window; the hypotheses are the two
pointwise estimates supplied by the active-marginal calculation. -/
theorem harmonic_window_gain {I : Type*} (s : Finset I) (q : ℝ → I → ℝ)
    {T a β Λ δ : ℝ} (hT : 0 < T) (ha : 0 < a) (hβ : 0 < β)
    (hβ1 : β ≤ 1) (hΛ : 0 < Λ) (hδ : 0 ≤ δ) (hwindow : T / a ≤ β * T)
    (hq : ∀ t ∈ Icc (T / a) (β * T), ∀ i ∈ s, 0 ≤ q t i ∧ q t i ≤ 1)
    (hz : ∀ t ∈ Icc (T / a) (β * T), (1 - β) * T / (Λ * t) ≤ δ)
    (hsum : ∀ t ∈ Icc (T / a) (β * T), (1 - β) * T / (Λ * t) ≤ ∑ i ∈ s, q t i)
    (hfi : IntervalIntegrable (fun t => 1 - ∏ i ∈ s, (1 - q t i)) volume (T / a) (β * T)) :
    ((1 - β) / (1 + δ) * Real.log (β * a) / Λ) * T ≤
      ∫ t in (T / a)..(β * T), 1 - ∏ i ∈ s, (1 - q t i) := by
  have htpos : ∀ t ∈ Icc (T / a) (β * T), 0 < t := fun t ht =>
    lt_of_lt_of_le (div_pos hT ha) ht.1
  have hc : ContinuousOn (fun t : ℝ => ((1 - β) * T / (Λ * t)) / (1 + δ))
      (Icc (T / a) (β * T)) := by
    exact (continuousOn_const.div (continuousOn_const.mul continuousOn_id)
      (fun t ht => ne_of_gt (mul_pos hΛ (htpos t ht)))).div_const _
  rw [← harmonic_window_integral hT ha hβ hΛ hδ]
  apply intervalIntegral.integral_mono_on hwindow
    (hc.intervalIntegrable_of_Icc hwindow) hfi
  intro t ht
  apply union_ge_div_one_add_of_le s (q t) (hq t ht)
  · exact div_nonneg (mul_nonneg (sub_nonneg.mpr hβ1) hT.le)
      (mul_nonneg hΛ.le (htpos t ht).le)
  · exact hz t ht
  · exact hsum t ht

/-- Small marginals supply a harmonic lower bound on their total conditional
failure probability; coordinates removed by the cutoff lose at most `t` mass. -/
theorem harmonic_density_sum_lower {I : Type*} (s : Finset I) (p : I → ℝ)
    {M t T β : ℝ} (hM : 1 ≤ M) (ht : 0 < t) (ht1 : t ≤ 1)
    (hcard : (s.card : ℝ) ≤ M)
    (hp : ∀ i ∈ s, 0 ≤ p i ∧ p i ≤ 1)
    (hpt : ∀ i ∈ s, p i ≤ t) (hT : T ≤ ∑ i ∈ s, p i)
    (htβ : t ≤ β * T) :
    (1 - β) * T / ((1 + Real.log M) * t) ≤ ∑ i ∈ s, harmonicDensity M (p i) t := by
  classical
  have hMp : 0 < M := lt_of_lt_of_le zero_lt_one hM
  have hΛ : 0 < 1 + Real.log M := by linarith [Real.log_nonneg hM]
  have hden : 0 < (1 + Real.log M) * t := mul_pos hΛ ht
  have hm := harmonic_active_sum_lower s p hMp ht.le hcard
  have hmass : (1 - β) * T ≤ ∑ i ∈ s.filter (fun i => t ≤ M * p i), p i := by
    nlinarith
  calc
    (1 - β) * T / ((1 + Real.log M) * t) ≤
        (∑ i ∈ s.filter (fun i => t ≤ M * p i), p i) / ((1 + Real.log M) * t) :=
      div_le_div_of_nonneg_right hmass hden.le
    _ = ∑ i ∈ s.filter (fun i => t ≤ M * p i), p i / ((1 + Real.log M) * t) :=
      Finset.sum_div _ _ _
    _ ≤ ∑ i ∈ s.filter (fun i => t ≤ M * p i), harmonicDensity M (p i) t := by
      apply Finset.sum_le_sum
      intro i hi
      obtain ⟨his, hactive⟩ := Finset.mem_filter.mp hi
      have hpi : 0 < p i := by
        have : 0 < M * p i := ht.trans_le hactive
        exact pos_of_mul_pos_right this hMp.le
      exact harmonicDensity_tail_lower hM hpi (hp i his).2 (hpt i his)
        (le_min hactive ht1)
    _ ≤ ∑ i ∈ s, harmonicDensity M (p i) t := by
      apply Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
      intro i hi _
      exact (harmonicDensity_mem_Icc hM (hp i hi).1 (hp i hi).2 t).1

/-- The reciprocal lower bound remains small throughout the chosen window. -/
theorem harmonic_window_z_le {T a β Λ t : ℝ} (hT : 0 < T) (ha : 0 < a)
    (hβ : 0 ≤ β) (hΛ : 0 < Λ) (ht : T / a ≤ t) :
    (1 - β) * T / (Λ * t) ≤ a / Λ := by
  have htpos : 0 < t := (div_pos hT ha).trans_le ht
  apply (div_le_div_iff₀ (mul_pos hΛ htpos) hΛ).mpr
  have hTa : T ≤ a * t := by
    have := (div_le_iff₀ ha).mp ht
    nlinarith
  have : (1 - β) * T ≤ a * t := by nlinarith [mul_nonneg hβ hT.le]
  nlinarith [mul_le_mul_of_nonneg_left this hΛ.le]

/-- The harmonic conditional union probability is always in the unit interval. -/
theorem harmonic_union_mem_Icc {I : Type*} (s : Finset I) (p : I → ℝ)
    {M : ℝ} (hM : 1 ≤ M) (hp : ∀ i ∈ s, 0 ≤ p i ∧ p i ≤ 1) (t : ℝ) :
    0 ≤ 1 - ∏ i ∈ s, (1 - harmonicDensity M (p i) t) ∧
      1 - ∏ i ∈ s, (1 - harmonicDensity M (p i) t) ≤ 1 := by
  have h0 : ∀ i ∈ s, 0 ≤ 1 - harmonicDensity M (p i) t := fun i hi =>
    sub_nonneg.mpr (harmonicDensity_mem_Icc hM (hp i hi).1 (hp i hi).2 t).2
  have h1 : ∀ i ∈ s, 1 - harmonicDensity M (p i) t ≤ 1 := fun i hi => by
    linarith [(harmonicDensity_mem_Icc hM (hp i hi).1 (hp i hi).2 t).1]
  exact ⟨sub_nonneg.mpr (Finset.prod_le_one h0 h1), by
    linarith [Finset.prod_nonneg h0]⟩

/-- Every harmonic conditional union is integrable over a finite interval. -/
theorem harmonic_union_intervalIntegrable {I : Type*} (s : Finset I) (p : I → ℝ)
    {M : ℝ} (hM : 1 ≤ M) (hp : ∀ i ∈ s, 0 ≤ p i ∧ p i ≤ 1) (v w : ℝ) :
    IntervalIntegrable (fun t => 1 - ∏ i ∈ s, (1 - harmonicDensity M (p i) t)) volume v w := by
  have hm : Measurable (fun t => 1 - ∏ i ∈ s, (1 - harmonicDensity M (p i) t)) :=
    measurable_const.sub (s.measurable_prod fun i _ =>
      measurable_const.sub (harmonicDensity_measurable M (p i)))
  apply (intervalIntegrable_const (c := (1 : ℝ))).mono_fun hm.aestronglyMeasurable
  exact Filter.Eventually.of_forall fun t => by
    dsimp only
    rw [Real.norm_eq_abs, abs_of_nonneg (harmonic_union_mem_Icc s p hM hp t).1]
    simpa using (harmonic_union_mem_Icc s p hM hp t).2

/-- A complete scalar one-low harmonic gain estimate. The finite collection of
failure marginals has size at most the cutoff, and every marginal is below the
left endpoint of the integration window. -/
theorem harmonic_gain {I : Type*} (s : Finset I) (p : I → ℝ)
    {M T a β u : ℝ} (hM : 1 ≤ M) (hT : 0 < T) (ha : 0 < a)
    (hβ : 0 < β) (hβ1 : β ≤ 1) (hwindow : T / a ≤ β * T)
    (hTu : T ≤ u) (hu : u ≤ 1) (hcard : (s.card : ℝ) ≤ M)
    (hp : ∀ i ∈ s, 0 ≤ p i ∧ p i ≤ 1)
    (hsmall : ∀ i ∈ s, p i ≤ T / a) (hmass : T ≤ ∑ i ∈ s, p i) :
    ((1 - β) / (1 + a / (1 + Real.log M)) * Real.log (β * a) / (1 + Real.log M)) * T ≤
      ∫ t in 0..u, 1 - ∏ i ∈ s, (1 - harmonicDensity M (p i) t) := by
  have hΛ : 0 < 1 + Real.log M := by linarith [Real.log_nonneg hM]
  have hend : β * T ≤ u := (mul_le_of_le_one_left hT.le hβ1).trans hTu
  have hlocal := harmonic_window_gain s (fun t i => harmonicDensity M (p i) t)
    hT ha hβ hβ1 hΛ (div_nonneg ha.le hΛ.le) hwindow
    (fun t _ i hi => harmonicDensity_mem_Icc hM (hp i hi).1 (hp i hi).2 t)
    (fun t ht => harmonic_window_z_le hT ha hβ.le hΛ ht.1)
    (fun t ht => harmonic_density_sum_lower s p hM
      ((div_pos hT ha).trans_le ht.1) (ht.2.trans (hend.trans hu)) hcard hp
      (fun i hi => (hsmall i hi).trans ht.1) hmass ht.2)
    (harmonic_union_intervalIntegrable s p hM hp _ _)
  refine hlocal.trans (intervalIntegral.integral_mono_interval (div_pos hT ha).le
    hwindow hend ?_ (harmonic_union_intervalIntegrable s p hM hp 0 u))
  exact Filter.Eventually.of_forall fun t => (harmonic_union_mem_Icc s p hM hp t).1

/-- The cutoff associated with the sharp asymptotic parameter is admissible. -/
theorem sharp_cutoff_ge_one {Λ : ℝ} (hΛ : Real.exp 6 ≤ Λ) :
    1 ≤ Real.exp (Λ - 1) := by
  apply Real.one_le_exp_iff.mpr
  have : 1 ≤ Real.exp (6:ℝ) := Real.one_le_exp_iff.mpr (by norm_num)
  linarith

/-- The harmonic parameter normalizes to exactly `Λ`. -/
theorem sharp_cutoff_log (Λ : ℝ) : 1 + Real.log (Real.exp (Λ - 1)) = Λ := by
  rw [Real.log_exp]
  ring

/-- The one-low harmonic estimate in the parameters used by the sharp upper
bound. It applies to all positive deficits in the small-marginal branch. -/
theorem sharp_harmonic_gain {I : Type*} (s : Finset I) (p : I → ℝ)
    {Λ T u : ℝ} (hΛ : Real.exp 6 ≤ Λ) (hT : 0 < T) (hTu : T ≤ u)
    (hu : u ≤ 1) (hcard : (s.card : ℝ) ≤ Real.exp (Λ - 1))
    (hp : ∀ i ∈ s, 0 ≤ p i ∧ p i ≤ 1)
    (hsmall : ∀ i ∈ s, p i ≤ T / sharpA Λ) (hmass : T ≤ ∑ i ∈ s, p i) :
    sharpH Λ * T ≤ ∫ t in 0..u,
      1 - ∏ i ∈ s, (1 - harmonicDensity (Real.exp (Λ - 1)) (p i) t) := by
  have hb := log_ge_six hΛ
  have hb0 : 0 < Real.log Λ := by linarith
  have hβ : 0 < 1 / Real.log Λ := div_pos zero_lt_one hb0
  have hβ1 : 1 / Real.log Λ ≤ 1 := (div_le_one hb0).mpr (by linarith)
  have hwindow : T / sharpA Λ ≤ (1 / Real.log Λ) * T := by
    apply (div_le_iff₀ (sharpA_pos hΛ)).mpr
    have := mul_le_mul_of_nonneg_right (sharp_interval_nonempty hΛ).le hT.le
    nlinarith
  have h := harmonic_gain s p (sharp_cutoff_ge_one hΛ) hT (sharpA_pos hΛ)
    hβ hβ1 hwindow hTu hu hcard hp hsmall hmass
  rw [sharp_cutoff_log, ← sharpH_eq_gain hΛ] at h
  exact h

end
end MultilinearGap
