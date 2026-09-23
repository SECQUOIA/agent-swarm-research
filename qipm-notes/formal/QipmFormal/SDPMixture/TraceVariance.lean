import QipmFormal.SDPMixture.VarianceBounds
import QipmFormal.SDPMixture.Decoder
import QipmFormal.SDPMixture.Centrality

/-! # Trace refinement of matrix multiplicative variance

The trace estimate has no dimension factor. It bounds the algebraic-gap /
complementarity discrepancy more tightly than applying a general trace versus
Frobenius norm comparison to the previously proved norm estimate.
-/
namespace QipmFormal.SDPMixture
noncomputable section
open scoped BigOperators MatrixOrder

variable {I n : Type*} [Fintype I] [Fintype n] [DecidableEq n]

/-- Pairing a scalar matrix upper bound with a positive matrix preserves the bound. -/
theorem trace_mul_le_scalar {A B : Matrix n n ℝ} {c : ℝ}
    (hA : A ≤ c • (1 : Matrix n n ℝ)) (hB : B.PosSemidef) :
    (A * B).trace ≤ c * B.trace := by
  have h := trace_mul_nonneg_of_posSemidef (Matrix.le_iff.mp hA) hB
  simp only [sub_mul, Matrix.trace_sub, smul_mul_assoc, one_mul,
    Matrix.trace_smul, smul_eq_mul] at h
  linarith

omit [DecidableEq n] in
/-- For real symmetric matrices the trace of the square is the Frobenius norm squared. -/
theorem trace_square_eq_frobeniusNorm_sq {D : Matrix n n ℝ} (hD : D.IsHermitian) :
    (D * D).trace = frobeniusNorm D ^ 2 := by
  rw [frobeniusNorm_sq]
  simp only [Matrix.trace, Matrix.diag, Matrix.mul_apply]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  have hij : D j i = D i j := by simpa using congrArg (fun A => A i j) hD.eq
  rw [hij, pow_two]

/-- The trace defect obeys the same dimension-free additive variance bound. -/
theorem centralMatrix_trace_variance_bound {w : I → ℝ} {X : I → Matrix n n ℝ}
    {m : ℝ} (hw : Mixture.ProbWeights w) (hm : 0 < m)
    (hX : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i) :
    (centralMatrix w X - 1).trace ≤
      m⁻¹ ^ 2 * ∑ i, w i * frobeniusNorm (X i - matrixMix w X) ^ 2 := by
  have hpos : ∀ i, (X i).PosDef := fun i => posDef_of_scalar_lower hm (hX i)
  have hmean := matrixMix_posDef hw hpos
  have hV : (variance w X).trace ≤
      m⁻¹ * ∑ i, w i * frobeniusNorm (X i - matrixMix w X) ^ 2 := by
    simp only [variance, Matrix.trace_sum, Matrix.trace_smul, smul_eq_mul, Finset.mul_sum]
    apply Finset.sum_le_sum
    intro i _
    have hD := (hpos i).isHermitian.sub hmean.isHermitian
    have hD2 : ((X i - matrixMix w X) * (X i - matrixMix w X)).PosSemidef := by
      simpa only [hD.eq] using Matrix.posSemidef_conjTranspose_mul_self (X i - matrixMix w X)
    have hb := trace_mul_le_scalar (inverse_scalar_upper hm (hX i)) hD2
    have he : ((X i - matrixMix w X) * (X i)⁻¹ * (X i - matrixMix w X)).trace =
        ((X i)⁻¹ * ((X i - matrixMix w X) * (X i - matrixMix w X))).trace := by
      rw [Matrix.trace_mul_cycle, Matrix.trace_mul_comm]
    rw [trace_square_eq_frobeniusNorm_sq hD] at hb
    rw [he]
    calc
      _ ≤ w i * (m⁻¹ * frobeniusNorm (X i - matrixMix w X) ^ 2) :=
        mul_le_mul_of_nonneg_left hb (hw.1 i)
      _ = _ := by ring
  rw [normalized_variance_identity hw hpos, Matrix.trace_mul_cycle]
  rw [hmean.posSemidef.inv_sqrt, CFC.sqrt_mul_sqrt_self _ hmean.posSemidef.inv.nonneg]
  calc
    ((matrixMix w X)⁻¹ * variance w X).trace ≤ m⁻¹ * (variance w X).trace :=
      trace_mul_le_scalar (inverse_scalar_upper hm (matrixMix_scalar_lower hw hX))
        (variance_posSemidef hw hpos)
    _ ≤ m⁻¹ * (m⁻¹ * ∑ i, w i * frobeniusNorm (X i - matrixMix w X) ^ 2) :=
      mul_le_mul_of_nonneg_left hV (inv_nonneg.mpr hm.le)
    _ = _ := by ring

/-- Trace variance controls the excess complementarity over the averaged algebraic gap. -/
theorem complementarity_discrepancy_variance_bound
    {w : I → ℝ} {X S : I → Matrix n n ℝ} {m μ : ℝ}
    (hw : Mixture.ProbWeights w) (hm : 0 < m) (hμ : 0 ≤ μ)
    (hX : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i)
    (hc : ∀ i, S i = μ • (X i)⁻¹) :
    (matrixMix w X * matrixMix w S).trace - Fintype.card n * μ ≤
      μ * m⁻¹ ^ 2 * ∑ i, w i * frobeniusNorm (X i - matrixMix w X) ^ 2 := by
  rw [complementarity_discrepancy hw (fun i => posDef_of_scalar_lower hm (hX i)) hc]
  simpa only [mul_assoc] using
    mul_le_mul_of_nonneg_left (centralMatrix_trace_variance_bound hw hm hX) hμ

end
end QipmFormal.SDPMixture
