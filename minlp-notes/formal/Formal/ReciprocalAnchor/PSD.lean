import Mathlib

namespace ReciprocalAnchor

open Matrix

/-- The reciprocal-anchor arrow matrix, with independent branch moments. -/
def arrowMatrix (w v q r t : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  !![w, 0, q; 0, v, r; q, r, t]

def ArrowPSD (w v q r t : ℝ) : Prop :=
  (arrowMatrix w v q r t).PosSemidef

theorem arrowPSD_iff_quadratic (w v q r t : ℝ) :
    ArrowPSD w v q r t ↔
      ∀ x y z : ℝ, 0 ≤ w * x ^ 2 + v * y ^ 2 + 2 * q * x * z + 2 * r * y * z + t * z ^ 2 := by
  rw [ArrowPSD, Matrix.posSemidef_iff_dotProduct_mulVec]
  have hherm : (arrowMatrix w v q r t).IsHermitian := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [arrowMatrix, Matrix.conjTranspose]
  simp only [hherm, true_and]
  constructor
  · intro h x y z
    have hh := h ![x,y,z]
    simp [arrowMatrix, dotProduct, Matrix.mulVec, Fin.sum_univ_succ] at hh
    nlinarith
  · intro h x
    have hh := h (x 0) (x 1) (x 2)
    simp [arrowMatrix, dotProduct, Matrix.mulVec, Fin.sum_univ_succ]
    nlinarith

private theorem cross_zero {q t : ℝ} (h : ∀ x : ℝ, 0 ≤ 2 * q * x + t) : q = 0 := by
  by_contra hq
  have hh := h (-(t + 1) / (2 * q))
  have hid : 2 * q * (-(t + 1) / (2 * q)) + t = -1 := by
    field_simp
    ring
  rw [hid] at hh
  norm_num at hh

private theorem quadratic_nonneg {w q τ : ℝ} (hw : 0 ≤ w) (hτ : 0 ≤ τ)
    (hq : q ^ 2 ≤ w * τ) (x z : ℝ) : 0 ≤ w * x ^ 2 + 2 * q * x * z + τ * z ^ 2 := by
  rcases eq_or_lt_of_le hw with hw | hw
  · have hq0 : q = 0 := by nlinarith [sq_nonneg q]
    subst w
    subst q
    simpa using mul_nonneg hτ (sq_nonneg z)
  · have h := mul_nonneg (sub_nonneg.mpr hq) (sq_nonneg z)
    nlinarith [sq_nonneg (w * x + q * z)]

private theorem minimum_identity {w q : ℝ} (hz : w = 0 → q = 0) :
    w * (-q / w) ^ 2 + 2 * q * (-q / w) = -(q ^ 2 / w) := by
  by_cases hw : w = 0
  · simp [hw, hz hw]
  · field_simp
    ring

/-- PSD is exactly two closed rotated-cone inequalities, including zero branches. -/
theorem arrowPSD_iff_soc {w v q r t : ℝ} (hw : 0 ≤ w) (hv : 0 ≤ v) :
    ArrowPSD w v q r t ↔
      ∃ τ₁ τ₀ : ℝ, 0 ≤ τ₁ ∧ 0 ≤ τ₀ ∧ q ^ 2 ≤ w * τ₁ ∧
        r ^ 2 ≤ v * τ₀ ∧ τ₁ + τ₀ ≤ t := by
  rw [arrowPSD_iff_quadratic]
  constructor
  · intro h
    have hq : w = 0 → q = 0 := by
      intro hw0
      apply cross_zero (t := t)
      intro x
      simpa [hw0] using h x 0 1
    have hr : v = 0 → r = 0 := by
      intro hv0
      apply cross_zero (t := t)
      intro y
      simpa [hv0] using h 0 y 1
    refine ⟨q ^ 2 / w, r ^ 2 / v, div_nonneg (sq_nonneg _) hw,
      div_nonneg (sq_nonneg _) hv, ?_, ?_, ?_⟩
    · by_cases hw0 : w = 0
      · simp [hw0, hq hw0]
      · rw [mul_div_cancel₀ _ hw0]
    · by_cases hv0 : v = 0
      · simp [hv0, hr hv0]
      · rw [mul_div_cancel₀ _ hv0]
    · have hh := h (-q / w) (-r / v) 1
      have h₁ := minimum_identity hq
      have h₀ := minimum_identity hr
      nlinarith
  · rintro ⟨τ₁,τ₀,h₁,h₀,hq,hr,ht⟩ x y z
    have hx := quadratic_nonneg hw h₁ hq x z
    have hy := quadratic_nonneg hv h₀ hr y z
    have hz := mul_nonneg (sub_nonneg.mpr ht) (sq_nonneg z)
    nlinarith

/-- Nonnegative weighted sums preserve this matrix inequality. -/
theorem arrowPSD_add_smul {w v q r t w' v' q' r' t' α β : ℝ}
    (h : ArrowPSD w v q r t) (h' : ArrowPSD w' v' q' r' t')
    (hα : 0 ≤ α) (hβ : 0 ≤ β) :
    ArrowPSD (α * w + β * w') (α * v + β * v') (α * q + β * q')
      (α * r + β * r') (α * t + β * t') := by
  rw [arrowPSD_iff_quadratic] at h h' ⊢
  intro x y z
  have h₁ := mul_nonneg hα (h x y z)
  have h₂ := mul_nonneg hβ (h' x y z)
  nlinarith

/-- The precise matrix and two-cone formulation in the one-leaf hull theorem. -/
theorem reciprocal_anchor_psd_iff_soc {m t q w : ℝ}
    (hw : 0 ≤ w) (hv : 0 ≤ m - w) :
    (arrowMatrix w (m - w) q (1 - q) t).PosSemidef ↔
      ∃ τ₁ τ₀ : ℝ, 0 ≤ τ₁ ∧ 0 ≤ τ₀ ∧ q ^ 2 ≤ w * τ₁ ∧
        (1 - q) ^ 2 ≤ (m - w) * τ₀ ∧ τ₁ + τ₀ ≤ t :=
  arrowPSD_iff_soc hw hv

/-- Every original reciprocal graph point satisfies the matrix inequality. -/
theorem graph_arrowPSD {X Y : ℝ} (hX : 0 < X) (hY : 0 ≤ Y) (hY1 : Y ≤ 1) :
    ArrowPSD (X * Y) (X - X * Y) Y (1 - Y) (1 / X) := by
  rw [arrowPSD_iff_quadratic]
  intro x y z
  have h₁ := mul_nonneg (div_nonneg hY hX.le) (sq_nonneg (X * x + z))
  have h₀ := mul_nonneg (div_nonneg (sub_nonneg.mpr hY1) hX.le)
    (sq_nonneg (X * y + z))
  have hid : X * Y * x ^ 2 + (X - X * Y) * y ^ 2 + 2 * Y * x * z +
      2 * (1 - Y) * y * z + (1 / X) * z ^ 2 =
      (Y / X) * (X * x + z) ^ 2 + ((1 - Y) / X) * (X * y + z) ^ 2 := by
    field_simp
    ring
  rw [hid]
  exact add_nonneg h₁ h₀

end ReciprocalAnchor
