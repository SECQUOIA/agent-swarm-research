import Formal.MultilinearGap.SharpUpper
import Formal.MultilinearGap.Suprema
import Formal.MultilinearGap.BoxSuprema

/-! The worst degree and dimension ratios have sharp leading constant one. -/
namespace MultilinearGap

open CubicGap Filter Real
open scoped Topology
noncomputable section

theorem degree_sharp_upper (d : ℕ) (hd : 1 ≤ d) :
    CubeDegreeBound d (sharpZ (sharpLambda d)) := by
  intro I hI hEq S a x ha hdeg hx
  have hdpos : 0 < (d : ℝ) := by exact_mod_cast (show 0 < d by omega)
  have hscale : (d : ℝ) ≤ exp (sharpLambda d - 1) := by
    rw [← exp_log hdpos]
    apply exp_le_exp.mpr
    have h := le_max_right (exp 6) (1 + log (d : ℝ))
    dsimp [sharpLambda]
    linarith
  apply sharp_cube_gap_bound S a ha x hx (sharpLambda d) (le_max_left _ _)
  intro s hs
  have hcard : (s.card : ℝ) ≤ (d : ℝ) := by exact_mod_cast hdeg s hs
  exact hcard.trans hscale

theorem growthScale_pos (n : ℕ) (hn : 8 ≤ n) :
    0 < log (n : ℝ) / log (log (n : ℝ)) := by
  have hnpos : 0 < (n : ℝ) := by exact_mod_cast (show 0 < n by omega)
  have hn8 : (8 : ℝ) ≤ n := by exact_mod_cast hn
  have hlog : 1 < log (n : ℝ) := by
    apply (lt_log_iff_exp_lt hnpos).mpr
    exact exp_one_lt_d9.trans_le (by linarith)
  exact div_pos (by linarith) (log_pos hlog)

theorem normalized_squeeze (f : ℕ → ℝ)
    (hbounds : ∀ n : ℕ, 8 ≤ n →
      lowerComparison n ≤ f n ∧ f n ≤ sharpZ (sharpLambda n)) :
    Tendsto (fun n : ℕ => f n / (log n / log (log n)))
      atTop (𝓝 1) := by
  apply tendsto_of_tendsto_of_tendsto_of_le_of_le'
    tendsto_lowerComparison_normalized tendsto_sharpZ_degree_normalized
  · filter_upwards [eventually_ge_atTop 8] with n hn
    exact div_le_div_of_nonneg_right (hbounds n hn).1 (growthScale_pos n hn).le
  · filter_upwards [eventually_ge_atTop 8] with n hn
    exact div_le_div_of_nonneg_right (hbounds n hn).2 (growthScale_pos n hn).le

/-- The cube degree supremum at every integer allowance has leading constant one. -/
theorem degreeSupremum_asymptotic :
    Tendsto (fun d : ℕ => degreeSupremum d / (log d / log (log d)))
      atTop (𝓝 1) := by
  apply normalized_squeeze
  intro n hn
  have hb := suprema_bounds n hn _ (degree_sharp_upper n (by omega))
  exact ⟨hb.1.trans hb.2.1, hb.2.2⟩

/-- The corresponding dimension supremum has the same asymptotic growth. -/
theorem dimensionSupremum_asymptotic :
    Tendsto (fun n : ℕ => dimensionSupremum n / (log n / log (log n)))
      atTop (𝓝 1) := by
  apply normalized_squeeze
  intro n hn
  have hb := suprema_bounds n hn _ (degree_sharp_upper n (by omega))
  exact ⟨hb.1, hb.2.1.trans hb.2.2⟩

/-- The degree supremum includes every finite nonnegative box, with fixed
coordinates allowed, and the original unexpanded termwise relaxation. -/
theorem boxDegreeSupremum_asymptotic :
    Tendsto (fun d : ℕ => boxDegreeSupremum d / (log d / log (log d)))
      atTop (𝓝 1) := by
  apply normalized_squeeze
  intro n hn
  have hb := box_suprema_bounds n hn _ (degree_sharp_upper n (by omega))
  exact ⟨hb.1.trans hb.2.1, hb.2.2⟩

/-- The all-box dimension supremum requires exactly `n` coordinates. -/
theorem boxDimensionSupremum_asymptotic :
    Tendsto (fun n : ℕ => boxDimensionSupremum n / (log n / log (log n)))
      atTop (𝓝 1) := by
  apply normalized_squeeze
  intro n hn
  have hb := box_suprema_bounds n hn _ (degree_sharp_upper n (by omega))
  exact ⟨hb.1, hb.2.1.trans hb.2.2⟩

/-- Both worst-case relaxation ratios grow as log(n)/log(log(n)), with
leading constant one, over the full finite nonnegative-box domain. -/
theorem sharp_positive_growth :
    Tendsto (fun d : ℕ => boxDegreeSupremum d / (log d / log (log d))) atTop (𝓝 1) ∧
    Tendsto (fun n : ℕ => boxDimensionSupremum n / (log n / log (log n))) atTop (𝓝 1) :=
  ⟨boxDegreeSupremum_asymptotic, boxDimensionSupremum_asymptotic⟩

end
end MultilinearGap
