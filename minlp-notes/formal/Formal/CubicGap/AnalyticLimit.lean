import Formal.CubicGap.AnalyticFamily

/-! Limits of the explicit lower approximants for the analytic cubic family.
Only the lower approximants are asserted to converge; the true hull-gap ratios
need not converge for these consequences. -/
namespace CubicGap

open Filter
open scoped Topology
noncomputable section

/-- Positive multiples of nine, the admissible sizes for the analytic family. -/
def analyticSize (k : ℕ) : ℕ := 9 * (k + 1)

/-- The finite lower bound obtained from the refined Bernstein minorant. -/
def analyticRatioLower (m : ℕ) : ℝ :=
  (161 / 4 - 135 / (4 * (m : ℝ)) + 6 / (m : ℝ)^2) /
    (223 / 12 - 901 / 120000 + 135 / (4 * (m : ℝ)) + 9 / (m : ℝ)^2)

/-- The refined asymptotic lower bound. -/
def analyticRefinedLimit : ℝ := 4830000 / 2229099

lemma analyticSize_ge_nine (k : ℕ) : 9 ≤ analyticSize k := by
  unfold analyticSize
  omega

lemma analyticSize_dvd_nine (k : ℕ) : 9 ∣ analyticSize k := by
  exact dvd_mul_right 9 (k + 1)

lemma tendsto_analyticSize :
    Tendsto (fun k => (analyticSize k : ℝ)) atTop atTop := by
  have h : Tendsto (fun k : ℕ => (k : ℝ) + 1) atTop atTop :=
    tendsto_natCast_atTop_atTop.atTop_add tendsto_const_nhds
  simpa [analyticSize, Nat.cast_mul, Nat.cast_add, Nat.cast_one] using
    h.const_mul_atTop (by norm_num : (0 : ℝ) < 9)

/-- The explicitly certified lower bounds converge to the refined constant. -/
theorem tendsto_analyticRatioLower :
    Tendsto (fun k => analyticRatioLower (analyticSize k)) atTop
      (𝓝 analyticRefinedLimit) := by
  have hlinear : Tendsto (fun k => 135 / (4 * (analyticSize k : ℝ)))
      atTop (𝓝 0) := by
    exact tendsto_const_nhds.div_atTop
      (tendsto_analyticSize.const_mul_atTop (by norm_num : (0 : ℝ) < 4))
  have hsquare : Tendsto (fun k => (analyticSize k : ℝ)^2) atTop atTop :=
    (tendsto_pow_atTop (by norm_num : 2 ≠ 0)).comp tendsto_analyticSize
  have h6 : Tendsto (fun k => 6 / (analyticSize k : ℝ)^2) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop hsquare
  have h9 : Tendsto (fun k => 9 / (analyticSize k : ℝ)^2) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop hsquare
  have hnum := ((tendsto_const_nhds (x := (161 / 4 : ℝ))).sub hlinear).add h6
  have hden := ((tendsto_const_nhds (x := (223 / 12 - 901 / 120000 : ℝ))).add
    hlinear).add h9
  have hlim := hnum.div hden (by norm_num)
  norm_num [analyticRatioLower, analyticRefinedLimit] at hlim ⊢
  exact hlim

/-- The simpler finite estimate displayed with the headline bound. -/
def analyticHeadlineLower (m : ℕ) : ℝ :=
  (161 / 4 - 135 / (4 * (m : ℝ)) + 6 / (m : ℝ)^2) /
    (223 / 12 + 135 / (4 * (m : ℝ)) + 9 / (m : ℝ)^2)

/-- The unrefined displayed finite estimates converge to the headline constant. -/
theorem tendsto_analyticHeadlineLower :
    Tendsto (fun k => analyticHeadlineLower (analyticSize k)) atTop
      (𝓝 (483 / 223 : ℝ)) := by
  have hlinear : Tendsto (fun k => 135 / (4 * (analyticSize k : ℝ)))
      atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop
      (tendsto_analyticSize.const_mul_atTop (by norm_num : (0 : ℝ) < 4))
  have hsquare : Tendsto (fun k => (analyticSize k : ℝ)^2) atTop atTop :=
    (tendsto_pow_atTop (by norm_num : 2 ≠ 0)).comp tendsto_analyticSize
  have h6 : Tendsto (fun k => 6 / (analyticSize k : ℝ)^2) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop hsquare
  have h9 : Tendsto (fun k => 9 / (analyticSize k : ℝ)^2) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop hsquare
  have hnum := ((tendsto_const_nhds (x := (161 / 4 : ℝ))).sub hlinear).add h6
  have hden := ((tendsto_const_nhds (x := (223 / 12 : ℝ))).add hlinear).add h9
  have hlim := hnum.div hden (by norm_num)
  norm_num [analyticHeadlineLower] at hlim ⊢
  exact hlim

/-- The positive Bernstein slack strengthens every admissible finite estimate. -/
theorem analyticHeadlineLower_le_refined (m : ℕ) (hm : 9 ≤ m) :
    analyticHeadlineLower m ≤ analyticRatioLower m := by
  have hm9 : (9 : ℝ) ≤ m := by exact_mod_cast hm
  have hmpos : (0 : ℝ) < m := by linarith
  have hlinear : 135 / (4 * (m : ℝ)) ≤ 15 / 4 := by
    apply (div_le_iff₀ (by positivity : (0 : ℝ) < 4 * m)).mpr
    nlinarith
  have hnum : 0 ≤ 161 / 4 - 135 / (4 * (m : ℝ)) + 6 / (m : ℝ)^2 := by
    have h6 : (0 : ℝ) ≤ 6 / (m : ℝ)^2 := by positivity
    linarith
  unfold analyticHeadlineLower analyticRatioLower
  apply div_le_div_of_nonneg_left hnum
  · have h135 : (0 : ℝ) ≤ 135 / (4 * (m : ℝ)) := by positivity
    have h9 : (0 : ℝ) ≤ 9 / (m : ℝ)^2 := by positivity
    linarith
  · linarith

/-- Every smaller constant is eventually exceeded by the lower approximants. -/
theorem analyticRatioLower_eventually_gt (c : ℝ) (hc : c < analyticRefinedLimit) :
    ∀ᶠ k in atTop, c < analyticRatioLower (analyticSize k) := by
  exact tendsto_analyticRatioLower.eventually (lt_mem_nhds hc)

/-- Transfer the lower-approximant limit without assuming convergence of the
actual ratio sequence. -/
theorem analytic_actual_eventually_gt (ratio : ℕ → ℝ)
    (hlower : ∀ m, 9 ≤ m → analyticRatioLower m ≤ ratio m)
    (c : ℝ) (hc : c < analyticRefinedLimit) :
    ∀ᶠ k in atTop, c < ratio (analyticSize k) := by
  filter_upwards [analyticRatioLower_eventually_gt c hc] with k hk
  exact hk.trans_le (hlower _ (analyticSize_ge_nine k))

/-- A uniform upper bound for the ratios at admissible sizes must dominate the
refined limit. -/
theorem analytic_uniform_upper_ge_refined (ratio : ℕ → ℝ)
    (hlower : ∀ m, 9 ≤ m → analyticRatioLower m ≤ ratio m)
    (C : ℝ) (hupper : ∀ k, ratio (analyticSize k) ≤ C) :
    analyticRefinedLimit ≤ C := by
  apply le_of_tendsto' tendsto_analyticRatioLower
  intro k
  exact (hlower _ (analyticSize_ge_nine k)).trans (hupper k)

/-- Every smaller constant is exceeded at an actual positive multiple of nine. -/
theorem analytic_actual_exists_gt (ratio : ℕ → ℝ)
    (hlower : ∀ m, 9 ≤ m → analyticRatioLower m ≤ ratio m)
    (c : ℝ) (hc : c < analyticRefinedLimit) :
    ∃ m, 9 ≤ m ∧ 9 ∣ m ∧ c < ratio m := by
  obtain ⟨k, hk⟩ := (analytic_actual_eventually_gt ratio hlower c hc).exists
  exact ⟨analyticSize k, analyticSize_ge_nine k, analyticSize_dvd_nine k, hk⟩

/-- The finite member with 36 variables per block already exceeds two. -/
theorem analyticRatioLower_thirty_six_gt_two : 2 < analyticRatioLower 36 := by
  norm_num [analyticRatioLower]

/-- A reduced expression for the refined limit. -/
theorem analyticRefinedLimit_reduced : analyticRefinedLimit = 1610000 / 743033 := by
  norm_num [analyticRefinedLimit]

/-- The refined certificate strictly improves the simpler headline bound. -/
theorem analytic_headline_lt_refined : (483 / 223 : ℝ) < analyticRefinedLimit := by
  norm_num [analyticRefinedLimit]

/-- The actual continuous graph-hull ratio for an analytic-family member. -/
def analyticRatio (m : ℕ) : ℝ :=
  analyticTermwiseGap m / hullGap (analyticFamily m) (analyticMeans m)

theorem analyticRatioLower_le_ratio (m : ℕ) (hm : 9 ≤ m) :
    analyticRatioLower m ≤ analyticRatio m :=
  analytic_finite_ratio_lower m hm

/-- For every constant below the refined limit, all sufficiently large
admissible family members exceed that constant. No limit of actual ratios is claimed. -/
theorem analyticRatio_eventually_gt (c : ℝ) (hc : c < analyticRefinedLimit) :
    ∀ᶠ k in atTop, c < analyticRatio (analyticSize k) :=
  analytic_actual_eventually_gt analyticRatio analyticRatioLower_le_ratio c hc

/-- Every smaller constant has a finite witness with positive integer orbit
coefficients, represented by a positive multiple of nine. -/
theorem analyticRatio_exists_gt (c : ℝ) (hc : c < analyticRefinedLimit) :
    ∃ m, 9 ≤ m ∧ 9 ∣ m ∧ c < analyticRatio m :=
  analytic_actual_exists_gt analyticRatio analyticRatioLower_le_ratio c hc

/-- Any upper bound for the actual analytic-family ratios dominates the refined limit. -/
theorem analyticRatio_uniform_upper_ge_refined (C : ℝ)
    (hupper : ∀ k, analyticRatio (analyticSize k) ≤ C) :
    analyticRefinedLimit ≤ C :=
  analytic_uniform_upper_ge_refined analyticRatio analyticRatioLower_le_ratio C hupper

/-- The 108-variable member (36 variables in each of three groups) exceeds two. -/
theorem analyticRatio_thirty_six_gt_two : 2 < analyticRatio 36 :=
  analyticRatioLower_thirty_six_gt_two.trans_le (analyticRatioLower_le_ratio 36 (by norm_num))

/-- The refined bound gives actual finite witnesses above the simpler headline bound. -/
theorem analyticRatio_exists_gt_headline :
    ∃ m, 9 ≤ m ∧ 9 ∣ m ∧ (483 / 223 : ℝ) < analyticRatio m :=
  analyticRatio_exists_gt _ analytic_headline_lt_refined

/-- A witness can simultaneously be chosen with positive integer orbit
coefficients and a strictly positive continuous hull gap. -/
theorem analytic_integer_family_witness (c : ℝ) (hc : c < analyticRefinedLimit) :
    ∃ m, 9 ≤ m ∧ 9 ∣ m ∧
      (∀ i, 0 < analyticCoefficients m i ∧ ∃ n : ℕ, analyticCoefficients m i = n) ∧
      0 < hullGap (analyticFamily m) (analyticMeans m) ∧ c < analyticRatio m := by
  obtain ⟨m, hm, hdiv, hratio⟩ := analyticRatio_exists_gt c hc
  exact ⟨m, hm, hdiv,
    fun i => ⟨analyticCoefficients_pos m (by omega) i,
      analyticCoefficients_integer m hdiv i⟩,
    analytic_hullGap_pos m hm, hratio⟩

/-- Exact value of the simpler certificate at 36 variables per group. -/
theorem analyticHeadlineLower_thirty_six :
    analyticHeadlineLower 36 = 16985 / 8436 := by
  norm_num [analyticHeadlineLower]

/-- The headline certificate itself already exceeds two at this size. -/
theorem analyticHeadlineLower_thirty_six_gt_two : 2 < analyticHeadlineLower 36 := by
  rw [analyticHeadlineLower_thirty_six]
  norm_num

end
end CubicGap
