import QipmFormal.SDPMixture.Variance

/-! # Slack mixtures, complementarity, and the point's own parameter -/
namespace QipmFormal.SDPMixture
noncomputable section
open scoped BigOperators MatrixOrder
open Matrix

variable {I n : Type*} [Fintype I] [Fintype n] [DecidableEq n]
  {w : I → ℝ} {X S : I → Matrix n n ℝ} {μ : ℝ}

/-- Complementarity defect measured at a specified positive parameter. -/
def sdpDefect (X S : Matrix n n ℝ) (μ : ℝ) : Matrix n n ℝ :=
  μ⁻¹ • (CFC.sqrt X * S * CFC.sqrt X) - 1

/-- The complementarity parameter associated with the point itself. -/
def pointParameter (X S : Matrix n n ℝ) : ℝ :=
  (X * S).trace / Fintype.card n

theorem mixed_slack (hc : ∀ i, S i = μ • (X i)⁻¹) :
    matrixMix w S = μ • inverseMix w X := by
  simp only [matrixMix, inverseMix, hc, Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [smul_comm]

theorem mixed_slack_posDef (hw : Mixture.ProbWeights w) (hμ : 0 < μ)
    (hX : ∀ i, (X i).PosDef) (hc : ∀ i, S i = μ • (X i)⁻¹) :
    (matrixMix w S).PosDef := by
  rw [mixed_slack hc]
  exact (inverseMix_posDef hw hX).smul hμ

theorem sdpDefect_mixture (_hw : Mixture.ProbWeights w) (hμ : 0 < μ)
    (_hX : ∀ i, (X i).PosDef) (hc : ∀ i, S i = μ • (X i)⁻¹) :
    sdpDefect (matrixMix w X) (matrixMix w S) μ = centralMatrix w X - 1 := by
  rw [sdpDefect, mixed_slack hc]
  simp only [Matrix.mul_smul, Matrix.smul_mul, smul_smul, inv_mul_cancel₀ (ne_of_gt hμ),
    one_smul, centralMatrix]

/-- Cyclicity of trace removes both square roots. -/
theorem trace_centralMatrix (hw : Mixture.ProbWeights w)
    (hX : ∀ i, (X i).PosDef) :
    (centralMatrix w X).trace = (matrixMix w X * inverseMix w X).trace := by
  unfold centralMatrix
  rw [Matrix.trace_mul_cycle, CFC.sqrt_mul_sqrt_self _ (matrixMix_posDef hw hX).posSemidef.nonneg,
    Matrix.trace_mul_comm]

theorem complementarity_mixture (hw : Mixture.ProbWeights w)
    (hX : ∀ i, (X i).PosDef) (hc : ∀ i, S i = μ • (X i)⁻¹) :
    (matrixMix w X * matrixMix w S).trace = μ * (centralMatrix w X).trace := by
  rw [mixed_slack hc, Matrix.mul_smul, Matrix.trace_smul, smul_eq_mul,
    trace_centralMatrix hw hX]

/-- The excess complementarity over the common exact-center algebraic gap. -/
theorem complementarity_discrepancy (hw : Mixture.ProbWeights w)
    (hX : ∀ i, (X i).PosDef) (hc : ∀ i, S i = μ • (X i)⁻¹) :
    (matrixMix w X * matrixMix w S).trace - Fintype.card n * μ =
      μ * (centralMatrix w X - 1).trace := by
  rw [complementarity_mixture hw hX hc, Matrix.trace_sub, Matrix.trace_one]
  ring

theorem central_defect_trace_nonneg (hw : Mixture.ProbWeights w)
    (hX : ∀ i, (X i).PosDef) : 0 ≤ (centralMatrix w X - 1).trace :=
  (Matrix.le_iff.mp (one_le_centralMatrix hw hX)).trace_nonneg

variable [Nonempty n]

theorem pointParameter_mixture (hw : Mixture.ProbWeights w)
    (hX : ∀ i, (X i).PosDef) (hc : ∀ i, S i = μ • (X i)⁻¹) :
    pointParameter (matrixMix w X) (matrixMix w S) =
      μ * (1 + (centralMatrix w X - 1).trace / Fintype.card n) := by
  rw [pointParameter, complementarity_mixture hw hX hc, Matrix.trace_sub, Matrix.trace_one]
  have hn : (Fintype.card n : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr Fintype.card_pos)
  field_simp
  ring

theorem pointParameter_mixture_pos (hw : Mixture.ProbWeights w) (hμ : 0 < μ)
    (hX : ∀ i, (X i).PosDef) (hc : ∀ i, S i = μ • (X i)⁻¹) :
    0 < pointParameter (matrixMix w X) (matrixMix w S) := by
  rw [pointParameter_mixture hw hX hc]
  apply mul_pos hμ
  have := div_nonneg (central_defect_trace_nonneg hw hX)
    (Nat.cast_nonneg (α := ℝ) (Fintype.card n))
  linarith

theorem sdpDefect_mixture_point (hw : Mixture.ProbWeights w) (hμ : 0 < μ)
    (hX : ∀ i, (X i).PosDef) (hc : ∀ i, S i = μ • (X i)⁻¹) :
    sdpDefect (matrixMix w X) (matrixMix w S)
        (pointParameter (matrixMix w X) (matrixMix w S)) =
      (1 + (centralMatrix w X - 1).trace / Fintype.card n)⁻¹ •
        ((centralMatrix w X - 1) -
          ((centralMatrix w X - 1).trace / Fintype.card n) • (1 : Matrix n n ℝ)) := by
  let t := (centralMatrix w X - 1).trace / Fintype.card n
  have ht : 0 ≤ t := div_nonneg (central_defect_trace_nonneg hw hX) (Nat.cast_nonneg _)
  have ht1 : 1 + t ≠ 0 := ne_of_gt (by linarith)
  rw [sdpDefect, pointParameter_mixture hw hX hc, mixed_slack hc,
    Matrix.mul_smul, Matrix.smul_mul, smul_smul]
  change ((μ * (1 + t))⁻¹ * μ) • centralMatrix w X - 1 =
    (1 + t)⁻¹ • (centralMatrix w X - 1 - t • (1 : Matrix n n ℝ))
  have hscale : (μ * (1 + t))⁻¹ * μ = (1 + t)⁻¹ := by
    field_simp
  rw [hscale, smul_sub, smul_sub, smul_smul]
  have hs : (1 + t)⁻¹ • (1 : Matrix n n ℝ) +
      ((1 + t)⁻¹ * t) • (1 : Matrix n n ℝ) = 1 := by
    rw [← add_smul]
    have hh : (1 + t)⁻¹ + (1 + t)⁻¹ * t = 1 := by field_simp
    rw [hh, one_smul]
  rw [sub_sub, hs]

end
end QipmFormal.SDPMixture
