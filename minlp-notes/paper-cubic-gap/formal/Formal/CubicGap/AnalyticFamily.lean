import Formal.CubicGap.AnalyticValues
import Formal.CubicGap.Bernstein

/-! The continuous Bernstein minorant certifies every member of the analytic
cubic family, through actual vertex laws and the original graph hull. -/

namespace CubicGap

noncomputable section

/-- Normalized success count in one of the three groups. -/
def analyticCount (m : ℕ) (v : Vertex (Fin 3 × Fin m)) (g : Fin 3) : ℝ :=
  count (fun i => v (g, i)) / (m : ℝ)

theorem analyticCount_mem (m : ℕ) (hm : 0 < m)
    (v : Vertex (Fin 3 × Fin m)) (g : Fin 3) :
    0 ≤ analyticCount m v g ∧ analyticCount m v g ≤ 1 := by
  have hmp : (0 : ℝ) < m := by exact_mod_cast hm
  have hc : (count (fun i => v (g, i)) : ℝ) ≤ m := by
    exact_mod_cast (show count (fun i => v (g, i)) ≤ m from
      by simpa using count_le (fun i => v (g, i)))
  exact ⟨by unfold analyticCount; positivity, (div_le_one hmp).mpr hc⟩

/-- Exact finite-size correction to the continuous cubic polynomial. -/
theorem analytic_binary_expansion (m : ℕ) (hm : 0 < m)
    (v : Vertex (Fin 3 × Fin m)) :
    18 / (m : ℝ) ^ 3 * analyticFamily m (vertexPoint v) =
      Bernstein.cubic (analyticCount m v 0) (analyticCount m v 1) (analyticCount m v 2) -
        (18 * (analyticCount m v 2) ^ 2 +
          27 * analyticCount m v 1 * analyticCount m v 2 +
          18 * analyticCount m v 1 + 9 * analyticCount m v 0) / m +
        12 * analyticCount m v 2 / (m : ℝ) ^ 2 := by
  have hm0 : (m : ℝ) ≠ 0 := by exact_mod_cast Nat.ne_of_gt hm
  rw [analyticFamily, show threeFamily m (analyticCoefficients m) (vertexPoint v) = _ from
    threeFamily_binary m (analyticCoefficients m) v]
  simp only [countPhi, analyticCoefficients, Fin.isValue, Matrix.cons_val_zero,
    Matrix.cons_val_one, Nat.cast_choose_two, Matrix.cons_val, Rat.cast_add, Rat.cast_mul,
    Rat.cast_ofNat, Rat.cast_natCast, choose_three_real, Rat.cast_div, Rat.cast_sub, Rat.cast_one]
  unfold Bernstein.cubic analyticCount
  field_simp
  ring

/-- The finite-size loss is at most 72/m at every binary vertex. -/
theorem analytic_binary_lower (m : ℕ) (hm : 0 < m)
    (v : Vertex (Fin 3 × Fin m)) :
    Bernstein.affine (analyticCount m v 0) (analyticCount m v 1) (analyticCount m v 2) +
      901 / 120000 - 72 / (m : ℝ) ≤
      18 / (m : ℝ) ^ 3 * analyticFamily m (vertexPoint v) := by
  have ha := analyticCount_mem m hm v 0
  have hb := analyticCount_mem m hm v 1
  have hc := analyticCount_mem m hm v 2
  have hminor := Bernstein.scalar_minorant (b := analyticCount m v 1) ha.2 hc.1 hc.2
  have hsq : (analyticCount m v 2) ^ 2 ≤ 1 := by
    nlinarith [mul_nonneg hc.1 (sub_nonneg.mpr hc.2)]
  have hbc : analyticCount m v 1 * analyticCount m v 2 ≤ 1 :=
    (mul_le_mul hb.2 hc.2 hc.1 (by norm_num)).trans (by norm_num)
  have hcorr : 18 * (analyticCount m v 2) ^ 2 +
      27 * analyticCount m v 1 * analyticCount m v 2 +
      18 * analyticCount m v 1 + 9 * analyticCount m v 0 ≤ 72 := by nlinarith
  have hcorr' := div_le_div_of_nonneg_right hcorr (Nat.cast_nonneg m : (0 : ℝ) ≤ m)
  have hlast : 0 ≤ 12 * analyticCount m v 2 / (m : ℝ) ^ 2 :=
    div_nonneg (mul_nonneg (by norm_num) hc.1) (sq_nonneg _)
  rw [analytic_binary_expansion m hm]
  linarith

/-- Every law with the individual requested marginals has the same count means. -/
theorem analyticCount_expect (m : ℕ) (hm : 0 < m)
    (μ : Law (Vertex (Fin 3 × Fin m))) (hμ : HasMeans μ (analyticMeans m))
    (g : Fin 3) :
    μ.expect (fun v => analyticCount m v g) =
      if g = 0 then 1 / 4 else if g = 1 then 1 / 2 else 3 / 4 := by
  let p : Fin 3 → ℝ := fun g => if g = 0 then 1 / 4 else if g = 1 then 1 / 2 else 3 / 4
  have hmean := expect_group_count_of_mean m μ p (fun g j => hμ (g,j)) g
  unfold analyticCount
  rw [Law.expect_div_const, hmean]
  have hm0 : (m : ℝ) ≠ 0 := by exact_mod_cast Nat.ne_of_gt hm
  exact mul_div_cancel_left₀ (p g) hm0

/-- No independence assumption is needed: the affine certificate holds for every coupling. -/
theorem analytic_law_lower (m : ℕ) (hm : 0 < m)
    (μ : Law (Vertex (Fin 3 × Fin m))) (hμ : HasMeans μ (analyticMeans m)) :
    139 / 6 + 901 / 120000 - 72 / (m : ℝ) ≤
      18 / (m : ℝ) ^ 3 * μ.expect (fun v => analyticFamily m (vertexPoint v)) := by
  have h := μ.expect_mono (analytic_binary_lower m hm)
  simp only [Bernstein.affine, Law.expect_add, Law.expect_sub, Law.expect_const_mul,
    Law.expect_const, analyticCount_expect m hm μ hμ] at h
  norm_num [Fin.ext_iff] at h ⊢
  linarith

/-- Lower bound for the actual convex-envelope endpoint. -/
theorem analytic_scaled_minimum_lower (m : ℕ) (hm : 0 < m) :
    139 / 6 + 901 / 120000 - 72 / (m : ℝ) ≤
      18 / (m : ℝ) ^ 3 * sInf (envelopeValues (analyticFamily m) (analyticMeans m)) := by
  have h := (envelopeValues_endpoints (analyticFamily m)
    (threeFamily_coordinate_affine m (analyticCoefficients m)) (analyticMeans m)
    (thresholdThreeMeans_mem_cube m)).1.1
  obtain ⟨μ, hμ, he⟩ := (mem_cubeGraph_hull_iff (analyticFamily m)
    (threeFamily_coordinate_affine m (analyticCoefficients m)) (analyticMeans m) _).mp h
  rw [← he]
  exact analytic_law_lower m hm μ hμ

/-- The refined finite bound concerns the width of the original continuous graph hull. -/
theorem analytic_scaled_hullGap_upper (m : ℕ) (hm : 0 < m) :
    18 / (m : ℝ) ^ 3 * hullGap (analyticFamily m) (analyticMeans m) ≤
      223 / 12 - 901 / 120000 + 135 / (4 * (m : ℝ)) + 9 / (m : ℝ) ^ 2 := by
  have hlo := analytic_scaled_minimum_lower m hm
  have hhi := analytic_scaled_maximum m hm
  unfold hullGap
  rw [mul_sub, hhi]
  have hm0 : (m : ℝ) ≠ 0 := by exact_mod_cast Nat.ne_of_gt hm
  have he : 72 / (m : ℝ) - 153 / (4 * (m : ℝ)) = 135 / (4 * (m : ℝ)) := by
    field_simp
    ring
  linarith

/-- The explicit lower approximant bounds the actual termwise-to-hull ratio. -/
theorem analytic_finite_ratio_lower (m : ℕ) (hm : 9 ≤ m) :
    (161 / 4 - 135 / (4 * (m : ℝ)) + 6 / (m : ℝ) ^ 2) /
      (223 / 12 - 901 / 120000 + 135 / (4 * (m : ℝ)) + 9 / (m : ℝ) ^ 2) ≤
      analyticTermwiseGap m / hullGap (analyticFamily m) (analyticMeans m) := by
  have hmn : 0 < m := by omega
  have hmr : (9 : ℝ) ≤ m := by exact_mod_cast hm
  have hmp : (0 : ℝ) < m := by exact_mod_cast hmn
  have hs : 0 < 18 / (m : ℝ) ^ 3 := by positivity
  have hh := analytic_hullGap_pos m hm
  have hn : 0 ≤ 161 / 4 - 135 / (4 * (m : ℝ)) + 6 / (m : ℝ) ^ 2 := by
    have he : 135 / (4 * (m : ℝ)) ≤ 135 / 36 := by
      apply div_le_div_of_nonneg_left (by norm_num) (by norm_num)
      linarith
    have : 0 ≤ 6 / (m : ℝ) ^ 2 := by positivity
    linarith
  have hdiv := div_le_div_of_nonneg_left hn (mul_pos hs hh)
    (analytic_scaled_hullGap_upper m hmn)
  refine hdiv.trans_eq ?_
  rw [← analytic_scaled_termwiseGap m hmn]
  exact mul_div_mul_left _ _ hs.ne'

/-- The simpler finite bound follows by discarding the positive Bernstein slack. -/
theorem analytic_finite_ratio_lower_simple (m : ℕ) (hm : 9 ≤ m) :
    (161 / 4 - 135 / (4 * (m : ℝ)) + 6 / (m : ℝ) ^ 2) /
      (223 / 12 + 135 / (4 * (m : ℝ)) + 9 / (m : ℝ) ^ 2) ≤
      analyticTermwiseGap m / hullGap (analyticFamily m) (analyticMeans m) := by
  have hmr : (9 : ℝ) ≤ m := by exact_mod_cast hm
  have hmp : (0 : ℝ) < m := by linarith
  have hn : 0 ≤ 161 / 4 - 135 / (4 * (m : ℝ)) + 6 / (m : ℝ) ^ 2 := by
    have he : 135 / (4 * (m : ℝ)) ≤ 135 / 36 := by
      apply div_le_div_of_nonneg_left (by norm_num) (by norm_num)
      linarith
    have : 0 ≤ 6 / (m : ℝ) ^ 2 := by positivity
    linarith
  have hd : 0 < 223 / 12 - 901 / 120000 +
      135 / (4 * (m : ℝ)) + 9 / (m : ℝ) ^ 2 := by positivity
  exact (div_le_div_of_nonneg_left hn hd (by linarith)).trans
    (analytic_finite_ratio_lower m hm)

end
end CubicGap
