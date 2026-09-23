import QipmFormal.ScalarCert.Monotone

/-!
# The explicit inverse of `P`, and the map `W`

From `P v ^ 2 = (1-v²)⁻¹² - 1` one reads off an explicit inverse

  `Pinv y = √(1 - (√(1+y²))⁻¹)`,   `P (Pinv y) = y`  for `y > 0`.

Specialised at `y = Y v * A v` this is the map `W` appearing in the proof of
`thm:scalar-dilation`:  `W v = √(1 - (1 + Y v ^2 A v ^2)^{-1/2})`.
-/

namespace QipmFormal.ScalarCert

open Real Set

/-- Explicit inverse of `P` on `(0,∞)`. -/
noncomputable def Pinv (y : ℝ) : ℝ := √(1 - (√(1 + y ^ 2))⁻¹)

lemma one_le_sqrt_one_add_sq (y : ℝ) : (1:ℝ) ≤ √(1 + y ^ 2) :=
  Real.one_le_sqrt.mpr (by nlinarith [sq_nonneg y])

lemma sqrt_one_add_sq_pos (y : ℝ) : (0:ℝ) < √(1 + y ^ 2) :=
  lt_of_lt_of_le one_pos (one_le_sqrt_one_add_sq y)

lemma inner_nonneg (y : ℝ) : (0:ℝ) ≤ 1 - (√(1 + y ^ 2))⁻¹ := by
  have h := one_le_sqrt_one_add_sq y
  have : (√(1 + y ^ 2))⁻¹ ≤ 1 := inv_le_one_of_one_le₀ h
  linarith

lemma inner_lt_one (y : ℝ) : 1 - (√(1 + y ^ 2))⁻¹ < 1 := by
  have := sqrt_one_add_sq_pos y
  have : (0:ℝ) < (√(1 + y ^ 2))⁻¹ := by positivity
  linarith

lemma Pinv_lt_one (y : ℝ) : Pinv y < 1 := by
  rw [Pinv]
  exact (Real.sqrt_lt' one_pos).mpr (by simpa using inner_lt_one y)

lemma Pinv_nonneg (y : ℝ) : 0 ≤ Pinv y := Real.sqrt_nonneg _

lemma Pinv_pos {y : ℝ} (hy : 0 < y) : 0 < Pinv y := by
  rw [Pinv]
  apply Real.sqrt_pos.mpr
  have h1 : (1:ℝ) < √(1 + y ^ 2) :=
    (Real.lt_sqrt zero_le_one).mpr (by nlinarith)
  have : (√(1 + y ^ 2))⁻¹ < 1 := inv_lt_one_of_one_lt₀ h1
  linarith

lemma Pinv_mem {y : ℝ} (_hy : 0 < y) : Pinv y ∈ Ico 0 1 :=
  ⟨Pinv_nonneg y, Pinv_lt_one y⟩

lemma Pinv_sq (y : ℝ) : (Pinv y) ^ 2 = 1 - (√(1 + y ^ 2))⁻¹ :=
  Real.sq_sqrt (inner_nonneg y)

/-- `Pinv` really is a right inverse of `P` on `(0,∞)`. -/
theorem P_Pinv {y : ℝ} (hy : 0 < y) : P (Pinv y) = y := by
  have habs : |Pinv y| < 1 := by
    rw [abs_of_nonneg (Pinv_nonneg y)]; exact Pinv_lt_one y
  have hs : (0:ℝ) < √(1 + y ^ 2) := sqrt_one_add_sq_pos y
  have hone : 1 - (Pinv y) ^ 2 = (√(1 + y ^ 2))⁻¹ := by
    rw [Pinv_sq]; ring
  have hsq : P (Pinv y) ^ 2 = y ^ 2 := by
    rw [P_sq habs, hone, inv_inv, Real.sq_sqrt (by nlinarith [sq_nonneg y])]
    ring
  have hP0 : 0 ≤ P (Pinv y) := P_nonneg (Pinv_nonneg y) habs
  nlinarith [hsq, hP0, hy]

/-- `Y 0 = 0`. -/
@[simp] lemma Y_zero : Y 0 = 0 := by simp [Y]

lemma Y_pos {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : 0 < Y v := by
  have := Y_strictMonoOn (a := 0) ⟨le_refl 0, by norm_num⟩ ⟨hv0.le, hv1⟩ hv0
  simpa using this

lemma A_pos {v : ℝ} (hv : |v| < 1) : 0 < A v := by
  have h1 : (0:ℝ) < 1 - v ^ 2 := one_sub_sq_pos hv
  have h2 : (0:ℝ) < 2 - v ^ 2 := by nlinarith
  exact div_pos (Real.sqrt_pos.mpr h2) h1

/-- The map `W` of the proof of `thm:scalar-dilation`. -/
noncomputable def W (v : ℝ) : ℝ := Pinv (Y v * A v)

lemma YA_pos {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : 0 < Y v * A v := by
  have habs : |v| < 1 := by rw [abs_of_pos hv0]; exact hv1
  exact mul_pos (Y_pos hv0 hv1) (A_pos habs)

theorem P_W {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : P (W v) = Y v * A v :=
  P_Pinv (YA_pos hv0 hv1)

lemma W_mem {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : W v ∈ Ico 0 1 :=
  Pinv_mem (YA_pos hv0 hv1)

end QipmFormal.ScalarCert
