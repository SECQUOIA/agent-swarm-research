import QipmFormal.ScalarCert.Tail

/-!
# Monotonicity and range of `Y` and `P`

The key algebraic identity is `P v ^ 2 = ((1 - v^2)⁻¹)^2 - 1` on `[0,1)`,
which makes both the strict monotonicity and the surjectivity of `P`
onto `(0, ∞)` immediate.  `Y` is strictly monotone by termwise comparison
of its power series.
-/

namespace QipmFormal.ScalarCert

open Real Set

lemma one_sub_sq_pos {v : ℝ} (hv : |v| < 1) : (0:ℝ) < 1 - v ^ 2 := by
  have := abs_lt.mp hv
  nlinarith [this.1, this.2]

/-- `P v ^ 2 = ((1-v²)⁻¹)² - 1`. -/
theorem P_sq {v : ℝ} (hv : |v| < 1) : P v ^ 2 = (1 - v ^ 2)⁻¹ ^ 2 - 1 := by
  have h1 : (0:ℝ) < 1 - v ^ 2 := one_sub_sq_pos hv
  have h2 : (0:ℝ) ≤ 2 - v ^ 2 := by nlinarith
  rw [P, A, mul_div_assoc']
  rw [div_pow, mul_pow, Real.sq_sqrt h2]
  field_simp
  ring

lemma P_nonneg {v : ℝ} (hv0 : 0 ≤ v) (hv : |v| < 1) : 0 ≤ P v := by
  have h1 : (0:ℝ) < 1 - v ^ 2 := one_sub_sq_pos hv
  have h2 : (0:ℝ) ≤ 2 - v ^ 2 := by nlinarith
  exact mul_nonneg hv0 (div_nonneg (Real.sqrt_nonneg _) h1.le)

/-- `P` is strictly monotone on `[0,1)`. -/
theorem P_strictMonoOn : StrictMonoOn P (Ico 0 1) := by
  intro a ha b hb hab
  have hA : |a| < 1 := by rw [abs_of_nonneg ha.1]; exact ha.2
  have hB : |b| < 1 := by rw [abs_of_nonneg hb.1]; exact hb.2
  have h1a : (0:ℝ) < 1 - a ^ 2 := one_sub_sq_pos hA
  have h1b : (0:ℝ) < 1 - b ^ 2 := one_sub_sq_pos hB
  have hsq : P a ^ 2 < P b ^ 2 := by
    rw [P_sq hA, P_sq hB]
    have hlt : 1 - b ^ 2 < 1 - a ^ 2 := by nlinarith [ha.1, hb.1]
    have : (1 - a ^ 2)⁻¹ < (1 - b ^ 2)⁻¹ := by
      rw [inv_lt_inv₀ h1a h1b]; exact hlt
    have hpos : (0:ℝ) < (1 - a ^ 2)⁻¹ := by positivity
    nlinarith [this, hpos]
  have hPa := P_nonneg ha.1 hA
  have hPb := P_nonneg hb.1 hB
  nlinarith [hsq, hPa, hPb]

/-- `Y` is strictly monotone on `[0,1)`, by termwise comparison of the series. -/
theorem Y_strictMonoOn : StrictMonoOn Y (Ico 0 1) := by
  intro a ha b hb hab
  have hA : |a| < 1 := by rw [abs_of_nonneg ha.1]; exact ha.2
  have hB : |b| < 1 := by rw [abs_of_nonneg hb.1]; exact hb.2
  have hsa := hasSum_term hA
  have hsb := hasSum_term hB
  refine hasSum_lt (i := 0) ?_ ?_ hsa hsb
  · intro k
    have hcoef : (0:ℝ) ≤ (2 - (1/2 : ℝ) ^ k) / (2 * (k : ℝ) + 1) := by
      have : (0:ℝ) < 2 * (k : ℝ) + 1 := by positivity
      exact div_nonneg (coef_nonneg k) this.le
    have hpow : a ^ (2 * k + 1) ≤ b ^ (2 * k + 1) :=
      pow_le_pow_left₀ ha.1 hab.le _
    exact mul_le_mul_of_nonneg_left hpow hcoef
  · simp only [term, pow_zero, Nat.cast_zero]
    norm_num
    exact hab

end QipmFormal.ScalarCert
