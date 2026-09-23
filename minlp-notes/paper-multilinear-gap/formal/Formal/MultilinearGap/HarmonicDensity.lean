import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

namespace MultilinearGap

open MeasureTheory Set
noncomputable section

/-- Upper endpoint of the harmonic tail. -/
def harmonicHeight (M p : ℝ) : ℝ := min (M * p) 1

/-- Normalizing constant for the flat part and harmonic tail. -/
def harmonicNorm (M p : ℝ) : ℝ := 1 + Real.log (harmonicHeight M p / p)

/-- A bounded harmonic kernel with mean `p` on the unit interval. -/
def harmonicDensity (M p t : ℝ) : ℝ :=
  if p = 0 then 0 else if t ≤ p then 1 / harmonicNorm M p
  else if t ≤ harmonicHeight M p then p / harmonicNorm M p * t⁻¹ else 0

theorem le_harmonicHeight {M p : ℝ} (hM : 1 ≤ M) (hp : 0 ≤ p) (hp1 : p ≤ 1) :
    p ≤ harmonicHeight M p := by
  exact le_min (by nlinarith) hp1

theorem harmonicHeight_le_one (M p : ℝ) : harmonicHeight M p ≤ 1 := min_le_right _ _

theorem harmonicNorm_one_le {M p : ℝ} (hM : 1 ≤ M) (hp : 0 < p) (hp1 : p ≤ 1) :
    1 ≤ harmonicNorm M p := by
  have h := le_harmonicHeight hM hp.le hp1
  have : 0 ≤ Real.log (harmonicHeight M p / p) :=
    Real.log_nonneg ((le_div_iff₀ hp).mpr (by simpa using h))
  dsimp [harmonicNorm]
  linarith

theorem harmonicNorm_le {M p : ℝ} (hM : 1 ≤ M) (hp : 0 < p) (hp1 : p ≤ 1) :
    harmonicNorm M p ≤ 1 + Real.log M := by
  have h := le_harmonicHeight hM hp.le hp1
  unfold harmonicNorm
  apply add_le_add_right
  apply Real.log_le_log (div_pos (lt_of_lt_of_le hp h) hp)
  exact (div_le_iff₀ hp).mpr (min_le_left _ _)

theorem harmonicDensity_measurable (M p : ℝ) : Measurable (harmonicDensity M p) := by
  unfold harmonicDensity
  split
  · exact measurable_const
  · exact Measurable.ite measurableSet_Iic measurable_const
      (Measurable.ite measurableSet_Iic (measurable_const.mul measurable_id.inv) measurable_const)

theorem harmonicDensity_mem_Icc {M p : ℝ} (hM : 1 ≤ M) (hp : 0 ≤ p)
    (hp1 : p ≤ 1) (t : ℝ) : harmonicDensity M p t ∈ Icc 0 1 := by
  by_cases hp0 : p = 0
  · simp [harmonicDensity, hp0]
  have hpp : 0 < p := lt_of_le_of_ne hp (Ne.symm hp0)
  have hn := harmonicNorm_one_le hM hpp hp1
  have hnpos : 0 < harmonicNorm M p := by linarith
  unfold harmonicDensity
  simp only [hp0, ↓reduceIte]
  split_ifs with htp hth
  · exact ⟨by positivity, (div_le_one hnpos).mpr hn⟩
  · have ht : 0 < t := lt_trans hpp (lt_of_not_ge htp)
    constructor
    · positivity
    · have hpt : p ≤ t := le_of_lt (lt_of_not_ge htp)
      have : p / harmonicNorm M p ≤ t :=
        (div_le_iff₀ hnpos).mpr (by nlinarith)
      simpa only [div_eq_mul_inv] using (div_le_one ht).mpr this
  · exact ⟨le_rfl, zero_le_one⟩

theorem harmonicDensity_tail {M p t : ℝ} (hp : p ≠ 0) (hpt : p < t)
    (hth : t ≤ harmonicHeight M p) :
    harmonicDensity M p t = p / harmonicNorm M p * t⁻¹ := by
  simp [harmonicDensity, hp, not_le.mpr hpt, hth]

theorem harmonicDensity_tail_lower {M p t : ℝ} (hM : 1 ≤ M) (hp : 0 < p)
    (hp1 : p ≤ 1) (hpt : p ≤ t) (hth : t ≤ harmonicHeight M p) :
    p / ((1 + Real.log M) * t) ≤ harmonicDensity M p t := by
  have hn := harmonicNorm_one_le hM hp hp1
  have hnpos : 0 < harmonicNorm M p := by linarith
  have hnle := harmonicNorm_le hM hp hp1
  have hL : 0 < 1 + Real.log M := lt_of_lt_of_le hnpos hnle
  have ht : 0 < t := lt_of_lt_of_le hp hpt
  have hden : harmonicNorm M p * t ≤ (1 + Real.log M) * t :=
    mul_le_mul_of_nonneg_right hnle ht.le
  have hh := div_le_div_of_nonneg_left hp.le (mul_pos hnpos ht) hden
  by_cases he : p = t
  · subst t
    have heq : p / (harmonicNorm M p * p) = 1 / harmonicNorm M p := by field_simp
    rw [heq] at hh
    simpa [harmonicDensity, hp.ne'] using hh
  · rw [harmonicDensity_tail hp.ne' (lt_of_le_of_ne hpt he) hth]
    simpa only [div_mul_eq_div_div, div_eq_mul_inv, mul_inv_rev, mul_comm,
      mul_left_comm, mul_assoc] using hh

private theorem harmonicDensity_integrable_left {M p : ℝ} (hp : 0 < p) :
    IntervalIntegrable (harmonicDensity M p) volume 0 p := by
  apply (intervalIntegrable_const (c := 1 / harmonicNorm M p)).congr_uIoo
  rw [uIoo_of_le hp.le]
  intro t ht
  simp [harmonicDensity, hp.ne', ht.2.le]

private theorem harmonicDensity_integrable_middle {M p : ℝ} (hM : 1 ≤ M)
    (hp : 0 < p) (hp1 : p ≤ 1) :
    IntervalIntegrable (harmonicDensity M p) volume p (harmonicHeight M p) := by
  have hph := le_harmonicHeight hM hp.le hp1
  have hi : IntervalIntegrable (fun t : ℝ => t⁻¹) volume p (harmonicHeight M p) :=
    (continuousOn_id.inv₀ (by intro t ht; exact ne_of_gt (lt_of_lt_of_le hp
      ((uIcc_of_le hph ▸ ht).1)))).intervalIntegrable
  apply (hi.const_mul (p / harmonicNorm M p)).congr_uIoo
  rw [uIoo_of_le hph]
  intro t ht
  exact (harmonicDensity_tail hp.ne' ht.1 ht.2.le).symm

private theorem harmonicDensity_integrable_right {M p : ℝ} (hM : 1 ≤ M)
    (hp : 0 < p) (hp1 : p ≤ 1) :
    IntervalIntegrable (harmonicDensity M p) volume (harmonicHeight M p) 1 := by
  apply (intervalIntegrable_const (c := (0 : ℝ))).congr_uIoo
  rw [uIoo_of_le (harmonicHeight_le_one M p)]
  intro t ht
  have hpt : p < t := lt_of_le_of_lt (le_harmonicHeight hM hp.le hp1) ht.1
  simp [harmonicDensity, hp.ne', not_le.mpr hpt, not_le.mpr ht.1]

theorem harmonicDensity_intervalIntegrable {M p : ℝ} (hM : 1 ≤ M)
    (hp : 0 ≤ p) (hp1 : p ≤ 1) :
    IntervalIntegrable (harmonicDensity M p) volume 0 1 := by
  by_cases hp0 : p = 0
  · subst p
    rw [show harmonicDensity M 0 = (fun _ : ℝ => 0) by
      funext t
      simp [harmonicDensity]]
    exact intervalIntegrable_const
  have hpp : 0 < p := lt_of_le_of_ne hp (Ne.symm hp0)
  exact ((harmonicDensity_integrable_left hpp).trans
    (harmonicDensity_integrable_middle hM hpp hp1)).trans
    (harmonicDensity_integrable_right hM hpp hp1)

theorem intervalIntegral_harmonicDensity {M p : ℝ} (hM : 1 ≤ M)
    (hp : 0 ≤ p) (hp1 : p ≤ 1) :
    ∫ t in (0 : ℝ)..1, harmonicDensity M p t = p := by
  by_cases hp0 : p = 0
  · simp [harmonicDensity, hp0]
  have hpp : 0 < p := lt_of_le_of_ne hp (Ne.symm hp0)
  have hph := le_harmonicHeight hM hp hp1
  have hhpos := lt_of_lt_of_le hpp hph
  have hleft : ∫ t in (0 : ℝ)..p, harmonicDensity M p t = p / harmonicNorm M p := by
    calc
      _ = ∫ _t in (0 : ℝ)..p, 1 / harmonicNorm M p := by
        apply intervalIntegral.integral_congr_Ioo_of_le hp
        intro t ht
        simp [harmonicDensity, hp0, ht.2.le]
      _ = _ := by simp [div_eq_mul_inv]
  have hmid : ∫ t in p..harmonicHeight M p, harmonicDensity M p t =
      p / harmonicNorm M p * Real.log (harmonicHeight M p / p) := by
    calc
      _ = ∫ t in p..harmonicHeight M p, p / harmonicNorm M p * t⁻¹ := by
        apply intervalIntegral.integral_congr_Ioo_of_le hph
        intro t ht
        exact harmonicDensity_tail hp0 ht.1 ht.2.le
      _ = _ := by rw [intervalIntegral.integral_const_mul, integral_inv_of_pos hpp hhpos]
  have hright : ∫ t in harmonicHeight M p..1, harmonicDensity M p t = 0 := by
    calc
      _ = ∫ _t in harmonicHeight M p..1, (0 : ℝ) := by
        apply intervalIntegral.integral_congr_Ioo_of_le (harmonicHeight_le_one M p)
        intro t ht
        have hpt : p < t := lt_of_le_of_lt hph ht.1
        simp [harmonicDensity, hp0, not_le.mpr hpt, not_le.mpr ht.1]
      _ = _ := by simp
  rw [← intervalIntegral.integral_add_adjacent_intervals
    ((harmonicDensity_integrable_left hpp).trans
      (harmonicDensity_integrable_middle hM hpp hp1))
    (harmonicDensity_integrable_right hM hpp hp1)]
  rw [← intervalIntegral.integral_add_adjacent_intervals
    (harmonicDensity_integrable_left hpp) (harmonicDensity_integrable_middle hM hpp hp1)]
  rw [hleft, hmid, hright]
  have hn : harmonicNorm M p ≠ 0 := ne_of_gt (lt_of_lt_of_le zero_lt_one
    (harmonicNorm_one_le hM hpp hp1))
  dsimp [harmonicNorm] at *
  field_simp
  simp

/-- Coordinates outside the active set carry at most one threshold of mass. -/
theorem harmonic_inactive_sum_le {ι : Type*} (s : Finset ι)
    (p : ι → ℝ) {M t : ℝ} (hM : 0 < M) (ht : 0 ≤ t)
    (hcard : (s.card : ℝ) ≤ M) :
    ∑ i ∈ s.filter (fun i => ¬t ≤ M * p i), p i ≤ t := by
  classical
  calc
    _ ≤ ∑ _i ∈ s.filter (fun i => ¬t ≤ M * p i), t / M := by
      apply Finset.sum_le_sum
      intro i hi
      exact (le_div_iff₀ hM).mpr (by
        have := (Finset.mem_filter.mp hi).2
        nlinarith)
    _ = ((s.filter (fun i => ¬t ≤ M * p i)).card : ℝ) * (t / M) := by simp
    _ ≤ (s.card : ℝ) * (t / M) := by
      apply mul_le_mul_of_nonneg_right _ (div_nonneg ht hM.le)
      exact_mod_cast Finset.card_filter_le s (fun i => ¬t ≤ M * p i)
    _ ≤ M * (t / M) := mul_le_mul_of_nonneg_right hcard (div_nonneg ht hM.le)
    _ = t := mul_div_cancel₀ t hM.ne'

/-- Removing coordinates below the activity threshold loses at most `t` mass. -/
theorem harmonic_active_sum_lower {ι : Type*} (s : Finset ι)
    (p : ι → ℝ) {M t : ℝ} (hM : 0 < M) (ht : 0 ≤ t)
    (hcard : (s.card : ℝ) ≤ M) :
    (∑ i ∈ s, p i) - t ≤ ∑ i ∈ s.filter (fun i => t ≤ M * p i), p i := by
  classical
  have hsum := Finset.sum_filter_add_sum_filter_not s (fun i => t ≤ M * p i) p
  have hbound := harmonic_inactive_sum_le s p hM ht hcard
  linarith

end
end MultilinearGap
