import QipmFormal.SDPMixture.Sandwich
import QipmFormal.SDPMixture.NormBounds
import QipmFormal.SDPMixture.Centrality

/-! # Sharpness and centering of equal scalar endpoint mixtures

The endpoint example attains both common-parameter norm bounds. Its
trace-normalized defect is zero, so it does not establish necessity of the
same ratio condition for point-centered neighborhoods.
-/
namespace QipmFormal.SDPMixture
noncomputable section
open scoped MatrixOrder Matrix.Norms.L2Operator

variable {n : Type*} [Fintype n] [DecidableEq n]

lemma frobeniusNorm_one : frobeniusNorm (1 : Matrix n n ℝ) = Real.sqrt (Fintype.card n) := by
  simp [frobeniusNorm, Matrix.one_apply]

lemma frobeniusNorm_scalar (c : ℝ) :
    frobeniusNorm (c • (1 : Matrix n n ℝ)) = Real.sqrt (Fintype.card n) * |c| := by
  rw [frobeniusNorm_smul, frobeniusNorm_one, mul_comm]

lemma opNorm_scalar [Nonempty n] (c : ℝ) : opNorm (c • (1 : Matrix n n ℝ)) = |c| := by
  simp [opNorm, norm_smul, Real.norm_eq_abs]

lemma kantorovich_excess_nonneg {R : ℝ} (hR : 0 < R) : 0 ≤ Mixture.kantorovich R - 1 := by
  rw [Mixture.kantorovich_sub_one _ hR]
  positivity

/-- The common-parameter Frobenius bound is attained in every dimension. -/
theorem endpoint_mixture_frobenius_sharp {m M : ℝ} (hm : 0 < m) (hM : 0 < M) :
    frobeniusNorm (centralMatrix (fun _ : Fin 2 => (1 / 2 : ℝ))
      ![m • (1 : Matrix n n ℝ), M • (1 : Matrix n n ℝ)] - 1) =
      Real.sqrt (Fintype.card n) * (Mixture.kantorovich (M / m) - 1) := by
  rw [endpoint_mixture_sharp hm hM, kantorovich_ratio_eq hm hM]
  have heq : Mixture.kantorovich (M / m) • (1 : Matrix n n ℝ) - 1 =
      (Mixture.kantorovich (M / m) - 1) • (1 : Matrix n n ℝ) := by simp [sub_smul]
  rw [heq, frobeniusNorm_scalar, abs_of_nonneg (kantorovich_excess_nonneg (div_pos hM hm))]

/-- In positive dimension the common-parameter operator bound is attained. -/
theorem endpoint_mixture_operator_sharp [Nonempty n] {m M : ℝ}
    (hm : 0 < m) (hM : 0 < M) :
    opNorm (centralMatrix (fun _ : Fin 2 => (1 / 2 : ℝ))
      ![m • (1 : Matrix n n ℝ), M • (1 : Matrix n n ℝ)] - 1) =
      Mixture.kantorovich (M / m) - 1 := by
  rw [endpoint_mixture_sharp hm hM, kantorovich_ratio_eq hm hM]
  have heq : Mixture.kantorovich (M / m) • (1 : Matrix n n ℝ) - 1 =
      (Mixture.kantorovich (M / m) - 1) • (1 : Matrix n n ℝ) := by simp [sub_smul]
  rw [heq, opNorm_scalar, abs_of_nonneg (kantorovich_excess_nonneg (div_pos hM hm))]

/-- A positive scalar matrix has zero trace-normalized central defect. -/
theorem scalar_normalized_defect_zero [Nonempty n] {c : ℝ} (hc : c ≠ 0) :
    ((c • (1 : Matrix n n ℝ)).trace / Fintype.card n)⁻¹ •
      (c • (1 : Matrix n n ℝ)) - 1 = 0 := by
  have hn : (Fintype.card n : ℝ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp [Matrix.trace_smul, hn, smul_smul, hc]

/-- The same sharp common-parameter example is exactly central at its own parameter. -/
theorem endpoint_mixture_point_defect_zero [Nonempty n] {m M : ℝ}
    (hm : 0 < m) (hM : 0 < M) :
    let Z := centralMatrix (fun _ : Fin 2 => (1 / 2 : ℝ))
      ![m • (1 : Matrix n n ℝ), M • (1 : Matrix n n ℝ)]
    (Z.trace / Fintype.card n)⁻¹ • Z - 1 = 0 := by
  dsimp only
  rw [endpoint_mixture_sharp hm hM]
  apply scalar_normalized_defect_zero
  positivity

/-- With the corresponding exact-center slacks, the actual point-centered defect is zero. -/
theorem endpoint_mixture_sdpDefect_point_zero [Nonempty n] {m M μ : ℝ}
    (hm : 0 < m) (hmM : m ≤ M) (hμ : 0 < μ) :
    let w := fun _ : Fin 2 => (1 / 2 : ℝ)
    let X := ![m • (1 : Matrix n n ℝ), M • (1 : Matrix n n ℝ)]
    let S := fun i => μ • (X i)⁻¹
    sdpDefect (matrixMix w X) (matrixMix w S)
      (pointParameter (matrixMix w X) (matrixMix w S)) = 0 := by
  dsimp only
  have hadm := endpoint_mixture_admissible (n := n) hmM
  have hX := fun i => posDef_of_scalar_lower hm (hadm.2 i).1
  rw [sdpDefect_mixture_point hadm.1 hμ hX (fun _ => rfl)]
  rw [← normalized_defect_eq_recentered (one_le_centralMatrix hadm.1 hX)]
  exact endpoint_mixture_point_defect_zero hm (hm.trans_le hmM)

/-- Scalar multiples of identity each have operator condition number one. -/
theorem scalar_operator_condition_one [Nonempty n] {c : ℝ} (hc : 0 < c) :
    opNorm (c • (1 : Matrix n n ℝ)) * opNorm (c • (1 : Matrix n n ℝ))⁻¹ = 1 := by
  rw [scalar_matrix_inv c hc.ne', opNorm_scalar, opNorm_scalar,
    abs_of_pos hc, abs_of_pos (inv_pos.mpr hc)]
  exact mul_inv_cancel₀ hc.ne'

/-- Individual condition numbers one do not bound the common-parameter mixture defect. -/
theorem scalar_one_nine_operator_defect [Nonempty n] :
    opNorm (centralMatrix (fun _ : Fin 2 => (1 / 2 : ℝ))
      ![(1 : Matrix n n ℝ), (9 : ℝ) • (1 : Matrix n n ℝ)] - 1) = 16 / 9 := by
  have h := endpoint_mixture_operator_sharp (n := n)
    (m := 1) (M := 9) (by norm_num) (by norm_num)
  norm_num [Mixture.kantorovich] at h ⊢
  exact h

end
end QipmFormal.SDPMixture
