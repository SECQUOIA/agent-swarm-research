import QipmFormal.Preconditioner.Spectral
import QipmFormal.Preconditioner.Congruence

/-! The manuscript's generic simultaneous-preconditioning inequality, with actual
positive inverse square roots and spectral condition numbers. -/

namespace QipmFormal.Preconditioner
noncomputable section
open Matrix
variable {n : Type*} [Fintype n] [DecidableEq n] [Nonempty n]

omit [Nonempty n] in
private theorem energy_whitened (A M : Matrix n n ℝ) (x : n → ℝ) :
    energy (inverseSqrt M * A * inverseSqrt M) x = energy A (inverseSqrt M *ᵥ x) := by
  simpa only [inverseSqrt_symmetric] using energy_congruence A (inverseSqrt M) x

/-- The relative condition number is bounded by the product of the two
condition numbers after simultaneous preconditioning. -/
theorem simultaneous_preconditioning {A₀ A₁ M : Matrix n n ℝ}
    (h₀ : A₀.PosDef) (h₁ : A₁.PosDef) (hM : M.PosDef) :
    spectralCondition (inverseSqrt A₀ * A₁ * inverseSqrt A₀)
      (inverseSqrt_congruence_posDef h₁ h₀).1 ≤
    spectralCondition (inverseSqrt M * A₀ * inverseSqrt M)
      (inverseSqrt_congruence_posDef h₀ hM).1 *
    spectralCondition (inverseSqrt M * A₁ * inverseSqrt M)
      (inverseSqrt_congruence_posDef h₁ hM).1 := by
  let B₀ := inverseSqrt M * A₀ * inverseSqrt M
  let B₁ := inverseSqrt M * A₁ * inverseSqrt M
  have hB₀ : B₀.PosDef := inverseSqrt_congruence_posDef h₀ hM
  have hB₁ : B₁.PosDef := inverseSqrt_congruence_posDef h₁ hM
  let a₀ := minEigen B₀ hB₀.1
  let b₀ := maxEigen B₀ hB₀.1
  let a₁ := minEigen B₁ hB₁.1
  let b₁ := maxEigen B₁ hB₁.1
  have ha₀ : 0 < a₀ := minEigen_pos hB₀
  have ha₁ : 0 < a₁ := minEigen_pos hB₁
  have hb₀ : 0 < b₀ := ha₀.trans_le (minEigen_le_maxEigen hB₀.1)
  have hb₁ : 0 < b₁ := ha₁.trans_le (minEigen_le_maxEigen hB₁.1)
  have hbound : spectralCondition (inverseSqrt A₀ * A₁ * inverseSqrt A₀)
      (inverseSqrt_congruence_posDef h₁ h₀).1 ≤ (b₁ / a₀) / (a₁ / b₀) := by
    apply spectralCondition_le_of_bounds (inverseSqrt_congruence_posDef h₁ h₀)
      (div_pos ha₁ hb₀)
    intro x
    let y := inverseSqrt A₀ *ᵥ x
    let z := (inverseSqrt M)⁻¹ *ᵥ y
    have hz : inverseSqrt M *ᵥ z = y := by
      dsimp [z]
      rw [mulVec_mulVec, mul_nonsing_inv _
        ((isUnit_iff_isUnit_det _).mp (inverseSqrt_isUnit hM)), one_mulVec]
    have he₀ : energy B₀ z = euclideanSq x := by
      rw [energy_whitened, hz]
      dsimp [y]
      rw [← energy_whitened, inverseSqrt_whitens h₀]
      simp [energy, euclideanSq]
    have he₁ : energy B₁ z = energy (inverseSqrt A₀ * A₁ * inverseSqrt A₀) x := by
      rw [energy_whitened, hz, energy_whitened]
    have hl₀ : a₀ * euclideanSq z ≤ euclideanSq x := by
      simpa only [he₀] using (energy_bounds hB₀.1 z).1
    have hu₀ : euclideanSq x ≤ b₀ * euclideanSq z := by
      simpa only [he₀] using (energy_bounds hB₀.1 z).2
    have hl₁ : a₁ * euclideanSq z ≤ energy (inverseSqrt A₀ * A₁ * inverseSqrt A₀) x := by
      simpa only [he₁] using (energy_bounds hB₁.1 z).1
    have hu₁ : energy (inverseSqrt A₀ * A₁ * inverseSqrt A₀) x ≤ b₁ * euclideanSq z := by
      simpa only [he₁] using (energy_bounds hB₁.1 z).2
    constructor
    · rw [div_mul_eq_mul_div]
      apply (div_le_iff₀ hb₀).mpr
      nlinarith [mul_le_mul_of_nonneg_left hu₀ ha₁.le,
        mul_le_mul_of_nonneg_right hl₁ hb₀.le]
    · rw [div_mul_eq_mul_div]
      apply (le_div_iff₀ ha₀).mpr
      nlinarith [mul_le_mul_of_nonneg_left hl₀ hb₁.le,
        mul_le_mul_of_nonneg_right hu₁ ha₀.le]
  convert hbound using 1
  simp only [spectralCondition, a₀, b₀, a₁, b₁, B₀, B₁,
    div_eq_mul_inv, _root_.mul_inv_rev, inv_inv]
  ring

end
end QipmFormal.Preconditioner
