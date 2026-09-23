import QipmFormal.SDPMixture.Variance
import QipmFormal.SDPMixture.Sandwich
import QipmFormal.SDPMixture.NormBounds
import QipmFormal.SDPMixture.Frobenius
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Isometric

/-! # Dimension-free additive variance bounds for positive matrix mixtures

A common lower bound `m I ≤ Xᵢ` suffices: the inverse square root of the
mean and the inverse of each summand each contribute one factor `m⁻¹`.
Operator norms are Euclidean operator norms; Frobenius bounds use mixed
operator/Frobenius product estimates, avoiding any factor from dimension.
No distinct matrices in the family are required to commute.
-/
namespace QipmFormal.SDPMixture
noncomputable section
open scoped BigOperators MatrixOrder Matrix.Norms.L2Operator

variable {I n : Type*} [Fintype I] [Fintype n] [DecidableEq n]

/-- A positive scalar lower bound reverses under matrix inversion. -/
theorem inverse_scalar_upper {X : Matrix n n ℝ} {m : ℝ}
    (hm : 0 < m) (hX : m • (1 : Matrix n n ℝ) ≤ X) :
    X⁻¹ ≤ m⁻¹ • (1 : Matrix n n ℝ) := by
  have hp := posDef_of_scalar_lower hm hX
  have hinv : X * X⁻¹ = 1 := Matrix.mul_nonsing_inv _ (isUnit_iff_ne_zero.mpr hp.det_pos.ne')
  have hinv' : X⁻¹ * X = 1 := Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr hp.det_pos.ne')
  have hc : Commute (X - m • (1 : Matrix n n ℝ)) X⁻¹ := by
    unfold Commute SemiconjBy
    simp only [mul_sub, sub_mul, smul_mul_assoc, mul_smul_comm, one_mul, mul_one,
      hinv, hinv']
  have hs := Commute.mul_nonneg (sub_nonneg.mpr hX) hp.posSemidef.inv.nonneg hc
  simp only [sub_mul, hinv, smul_mul_assoc, one_mul] at hs
  apply (smul_le_smul_iff_of_pos_left hm).mp
  simpa only [smul_smul, mul_inv_cancel₀ hm.ne', one_smul] using sub_nonneg.mp hs

/-- Inverting a positive scalar lower bound gives the dimension-free operator bound. -/
theorem inverse_norm_le {X : Matrix n n ℝ} {m : ℝ}
    (hm : 0 < m) (hX : m • (1 : Matrix n n ℝ) ≤ X) : ‖X⁻¹‖ ≤ m⁻¹ := by
  exact opNorm_le_of_nonneg_le (posDef_of_scalar_lower hm hX).posSemidef.inv.nonneg
    (inv_nonneg.mpr hm.le) (inverse_scalar_upper hm hX)

/-- The outer inverse square root contributes one inverse factor, not two. -/
theorem inverse_sqrt_norm_sq_le {X : Matrix n n ℝ} {m : ℝ}
    (hm : 0 < m) (hX : m • (1 : Matrix n n ℝ) ≤ X) :
    ‖(CFC.sqrt X)⁻¹‖ ^ 2 ≤ m⁻¹ := by
  have hp := posDef_of_scalar_lower hm hX
  rw [hp.posSemidef.inv_sqrt, CFC.norm_sqrt X⁻¹ hp.posSemidef.inv.nonneg,
    Real.sq_sqrt (norm_nonneg _)]
  exact inverse_norm_le hm hX

/-- The additive operator variance estimate only needs a common positive lower bound. -/
theorem centralMatrix_operator_variance_bound {w : I → ℝ} {X : I → Matrix n n ℝ}
    {m : ℝ} (hw : Mixture.ProbWeights w) (hm : 0 < m)
    (hX : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i) :
    opNorm (centralMatrix w X - 1) ≤
      m⁻¹ ^ 2 * ∑ i, w i * opNorm (X i - matrixMix w X) ^ 2 := by
  change ‖centralMatrix w X - 1‖ ≤ m⁻¹ ^ 2 * ∑ i, w i * ‖X i - matrixMix w X‖ ^ 2
  have hpos : ∀ i, (X i).PosDef := fun i => posDef_of_scalar_lower hm (hX i)
  have hV : ‖variance w X‖ ≤ m⁻¹ * ∑ i, w i * ‖X i - matrixMix w X‖ ^ 2 := by
    calc
      ‖variance w X‖ ≤ ∑ i, ‖w i • ((X i - matrixMix w X) * (X i)⁻¹ *
          (X i - matrixMix w X))‖ := norm_sum_le _ _
      _ ≤ ∑ i, m⁻¹ * (w i * ‖X i - matrixMix w X‖ ^ 2) := by
        apply Finset.sum_le_sum
        intro i _
        rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg (hw.1 i)]
        calc
          w i * ‖(X i - matrixMix w X) * (X i)⁻¹ * (X i - matrixMix w X)‖
              ≤ w i * ((‖X i - matrixMix w X‖ * ‖(X i)⁻¹‖) *
                  ‖X i - matrixMix w X‖) := by
            apply mul_le_mul_of_nonneg_left _ (hw.1 i)
            exact (norm_mul_le _ _).trans
              (mul_le_mul_of_nonneg_right (norm_mul_le _ _) (norm_nonneg _))
          _ ≤ w i * ((‖X i - matrixMix w X‖ * m⁻¹) *
                  ‖X i - matrixMix w X‖) := by
            apply mul_le_mul_of_nonneg_left _ (hw.1 i)
            apply mul_le_mul_of_nonneg_right _ (norm_nonneg _)
            exact mul_le_mul_of_nonneg_left (inverse_norm_le hm (hX i)) (norm_nonneg _)
          _ = m⁻¹ * (w i * ‖X i - matrixMix w X‖ ^ 2) := by ring
      _ = m⁻¹ * ∑ i, w i * ‖X i - matrixMix w X‖ ^ 2 := (Finset.mul_sum ..).symm
  rw [normalized_variance_identity hw hpos]
  calc
    ‖(CFC.sqrt (matrixMix w X))⁻¹ * variance w X * (CFC.sqrt (matrixMix w X))⁻¹‖
        ≤ ‖(CFC.sqrt (matrixMix w X))⁻¹‖ ^ 2 * ‖variance w X‖ := by
      calc
        _ ≤ (‖(CFC.sqrt (matrixMix w X))⁻¹‖ * ‖variance w X‖) *
            ‖(CFC.sqrt (matrixMix w X))⁻¹‖ := by
          exact (norm_mul_le _ _).trans
            (mul_le_mul_of_nonneg_right (norm_mul_le _ _) (norm_nonneg _))
        _ = _ := by ring
    _ ≤ m⁻¹ * (m⁻¹ * ∑ i, w i * ‖X i - matrixMix w X‖ ^ 2) := by
      exact mul_le_mul (inverse_sqrt_norm_sq_le hm (matrixMix_scalar_lower hw hX))
        hV (norm_nonneg _) (inv_nonneg.mpr hm.le)
    _ = _ := by ring

/-- The additive Frobenius variance estimate is dimension-free as well. -/
theorem centralMatrix_frobenius_variance_bound {w : I → ℝ} {X : I → Matrix n n ℝ}
    {m : ℝ} (hw : Mixture.ProbWeights w) (hm : 0 < m)
    (hX : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i) :
    frobeniusNorm (centralMatrix w X - 1) ≤
      m⁻¹ ^ 2 * ∑ i, w i * frobeniusNorm (X i - matrixMix w X) ^ 2 := by
  have hpos : ∀ i, (X i).PosDef := fun i => posDef_of_scalar_lower hm (hX i)
  have hV : frobeniusNorm (variance w X) ≤
      m⁻¹ * ∑ i, w i * frobeniusNorm (X i - matrixMix w X) ^ 2 := by
    calc
      frobeniusNorm (variance w X) ≤ ∑ i, frobeniusNorm
          (w i • ((X i - matrixMix w X) * (X i)⁻¹ * (X i - matrixMix w X))) :=
        frobeniusNorm_sum_le _ _
      _ ≤ ∑ i, m⁻¹ * (w i * frobeniusNorm (X i - matrixMix w X) ^ 2) := by
        apply Finset.sum_le_sum
        intro i _
        rw [frobeniusNorm_smul, abs_of_nonneg (hw.1 i)]
        calc
          w i * frobeniusNorm ((X i - matrixMix w X) * (X i)⁻¹ *
              (X i - matrixMix w X))
              ≤ w i * ((frobeniusNorm (X i - matrixMix w X) * ‖(X i)⁻¹‖) *
                  frobeniusNorm (X i - matrixMix w X)) := by
            apply mul_le_mul_of_nonneg_left _ (hw.1 i)
            exact (frobeniusNorm_mul_le _ _).trans (mul_le_mul_of_nonneg_right
              (frobeniusNorm_mul_le_mul_opNorm _ _) (frobeniusNorm_nonneg _))
          _ ≤ w i * ((frobeniusNorm (X i - matrixMix w X) * m⁻¹) *
                  frobeniusNorm (X i - matrixMix w X)) := by
            apply mul_le_mul_of_nonneg_left _ (hw.1 i)
            apply mul_le_mul_of_nonneg_right _ (frobeniusNorm_nonneg _)
            exact mul_le_mul_of_nonneg_left (inverse_norm_le hm (hX i))
              (frobeniusNorm_nonneg _)
          _ = m⁻¹ * (w i * frobeniusNorm (X i - matrixMix w X) ^ 2) := by ring
      _ = m⁻¹ * ∑ i, w i * frobeniusNorm (X i - matrixMix w X) ^ 2 :=
        (Finset.mul_sum ..).symm
  rw [normalized_variance_identity hw hpos]
  calc
    frobeniusNorm ((CFC.sqrt (matrixMix w X))⁻¹ * variance w X *
        (CFC.sqrt (matrixMix w X))⁻¹)
        ≤ ‖(CFC.sqrt (matrixMix w X))⁻¹‖ ^ 2 * frobeniusNorm (variance w X) := by
      calc
        _ ≤ (‖(CFC.sqrt (matrixMix w X))⁻¹‖ * frobeniusNorm (variance w X)) *
            ‖(CFC.sqrt (matrixMix w X))⁻¹‖ := by
          exact (frobeniusNorm_mul_le_mul_opNorm _ _).trans
            (mul_le_mul_of_nonneg_right (frobeniusNorm_mul_le_opNorm_mul _ _) (norm_nonneg _))
        _ = _ := by ring
    _ ≤ m⁻¹ * (m⁻¹ * ∑ i, w i * frobeniusNorm (X i - matrixMix w X) ^ 2) := by
      exact mul_le_mul (inverse_sqrt_norm_sq_le hm (matrixMix_scalar_lower hw hX))
        hV (frobeniusNorm_nonneg _) (inv_nonneg.mpr hm.le)
    _ = _ := by ring

/-- The operator variance bound survives the standard trace recentering. -/
theorem recentered_operator_variance_bound [Nonempty n]
    {w : I → ℝ} {X : I → Matrix n n ℝ} {m : ℝ}
    (hw : Mixture.ProbWeights w) (hm : 0 < m)
    (hX : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i) :
    let D := centralMatrix w X - 1
    opNorm ((1 + D.trace / Fintype.card n)⁻¹ •
      (D - (D.trace / Fintype.card n) • (1 : Matrix n n ℝ))) ≤
        m⁻¹ ^ 2 * ∑ i, w i * opNorm (X i - matrixMix w X) ^ 2 := by
  have hD : (0 : Matrix n n ℝ) ≤ centralMatrix w X - 1 :=
    sub_nonneg.mpr (one_le_centralMatrix hw fun i => posDef_of_scalar_lower hm (hX i))
  exact (opNorm_recentered_le hD).trans (centralMatrix_operator_variance_bound hw hm hX)

/-- The Frobenius variance bound survives the standard trace recentering. -/
theorem recentered_frobenius_variance_bound
    {w : I → ℝ} {X : I → Matrix n n ℝ} {m : ℝ}
    (hw : Mixture.ProbWeights w) (hm : 0 < m)
    (hX : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i) :
    let D := centralMatrix w X - 1
    frobeniusNorm ((1 + D.trace / Fintype.card n)⁻¹ •
      (D - (D.trace / Fintype.card n) • (1 : Matrix n n ℝ))) ≤
        m⁻¹ ^ 2 * ∑ i, w i * frobeniusNorm (X i - matrixMix w X) ^ 2 := by
  have hD : (0 : Matrix n n ℝ) ≤ centralMatrix w X - 1 :=
    sub_nonneg.mpr (one_le_centralMatrix hw fun i => posDef_of_scalar_lower hm (hX i))
  exact (frobeniusNorm_recentered_le _ (Matrix.nonneg_iff_posSemidef.mp hD)).trans
    (centralMatrix_frobenius_variance_bound hw hm hX)

end
end QipmFormal.SDPMixture
