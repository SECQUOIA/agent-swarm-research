import QipmFormal.SDPMixture.Centrality
import QipmFormal.SDPMixture.Sandwich
import QipmFormal.SDPMixture.NormBounds

/-! # Actual complementarity gaps and unnormalized residuals -/
namespace QipmFormal.SDPMixture
noncomputable section
open scoped MatrixOrder Matrix.Norms.L2Operator
open Matrix

variable {I n : Type*} [Fintype I] [Fintype n] [DecidableEq n]
  {w : I → ℝ} {X S : I → Matrix n n ℝ} {μ m M : ℝ}

/-- The actual complementarity excess lies between zero and the ratio certificate. -/
theorem complementarity_discrepancy_bounds (hw : Mixture.ProbWeights w) (hμ : 0 < μ)
    (hm : 0 < m) (hmM : m ≤ M)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i)
    (hhi : ∀ i, X i ≤ M • (1 : Matrix n n ℝ))
    (hc : ∀ i, S i = μ • (X i)⁻¹) :
    0 ≤ (matrixMix w X * matrixMix w S).trace - Fintype.card n * μ ∧
      (matrixMix w X * matrixMix w S).trace - Fintype.card n * μ ≤
        Fintype.card n * (Mixture.kantorovich (M / m) - 1) * μ := by
  have hX i := posDef_of_scalar_lower hm (hlo i)
  rw [complementarity_discrepancy hw hX hc]
  refine ⟨mul_nonneg hμ.le (central_defect_trace_nonneg hw hX), ?_⟩
  have hs := (centralMatrix_sandwich hw hm hmM hlo hhi).2
  have ht := (Matrix.le_iff.mp hs).trace_nonneg
  simp only [Matrix.trace_sub, Matrix.trace_smul, Matrix.trace_one, smul_eq_mul] at ht ⊢
  nlinarith

/-- The own-point parameter remains between the original parameter and its ratio bound. -/
theorem pointParameter_mixture_bounds [Nonempty n]
    (hw : Mixture.ProbWeights w) (hμ : 0 < μ) (hm : 0 < m) (hmM : m ≤ M)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i)
    (hhi : ∀ i, X i ≤ M • (1 : Matrix n n ℝ))
    (hc : ∀ i, S i = μ • (X i)⁻¹) :
    μ ≤ pointParameter (matrixMix w X) (matrixMix w S) ∧
      pointParameter (matrixMix w X) (matrixMix w S) ≤ Mixture.kantorovich (M / m) * μ := by
  have hb := complementarity_discrepancy_bounds hw hμ hm hmM hlo hhi hc
  have hn : (0 : ℝ) < Fintype.card n := Nat.cast_pos.mpr Fintype.card_pos
  unfold pointParameter
  constructor
  · apply (le_div_iff₀ hn).mpr
    nlinarith [hb.1]
  · apply (div_le_iff₀ hn).mpr
    nlinarith [hb.2]

/-- Multiplying the normalized defect by its parameter recovers the raw residual. -/
theorem rawResidual_eq_smul_sdpDefect (A B : Matrix n n ℝ) (hμ : μ ≠ 0) :
    CFC.sqrt A * B * CFC.sqrt A - μ • (1 : Matrix n n ℝ) =
      μ • sdpDefect A B μ := by
  rw [sdpDefect, smul_sub, smul_smul, mul_inv_cancel₀ hμ, one_smul]

/-- The Euclidean operator residual scales exactly by the positive parameter. -/
theorem opNorm_rawResidual (A B : Matrix n n ℝ) (hμ : 0 < μ) :
    opNorm (CFC.sqrt A * B * CFC.sqrt A - μ • (1 : Matrix n n ℝ)) =
      μ * opNorm (sdpDefect A B μ) := by
  rw [rawResidual_eq_smul_sdpDefect A B hμ.ne']
  simp only [opNorm, norm_smul, Real.norm_eq_abs, abs_of_pos hμ]

/-- The Frobenius residual scales exactly by the positive parameter. -/
theorem frobeniusNorm_rawResidual (A B : Matrix n n ℝ) (hμ : 0 < μ) :
    frobeniusNorm (CFC.sqrt A * B * CFC.sqrt A - μ • (1 : Matrix n n ℝ)) =
      μ * frobeniusNorm (sdpDefect A B μ) := by
  rw [rawResidual_eq_smul_sdpDefect A B hμ.ne', frobeniusNorm_smul, abs_of_pos hμ]

end
end QipmFormal.SDPMixture
