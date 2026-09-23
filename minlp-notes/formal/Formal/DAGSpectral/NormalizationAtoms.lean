import Formal.DAGSpectral.NormalizationTrials
import Formal.DAGSpectral.LabeledFactors

namespace DAGSpectral
noncomputable section
open Matrix
open scoped BigOperators
namespace NormalizationTrials
variable {p M m : ℕ}

def factorSum (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ) (F : Finset (Fin M)) :
    Matrix (Fin p) (Fin p) ℚ := ∑ j ∈ F, w j • vecMulVec (u j) (u j)

/-- Congruence of the actual rational rank-one sum. -/
theorem transform_factorSum (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (F : Finset (Fin M)) {r : ℕ} (T : Matrix (Fin r) (Fin p) ℚ) :
    T * factorSum u w F * Tᵀ =
      ∑ j ∈ F, w j • vecMulVec (T *ᵥ u j) (T *ᵥ u j) := by
  simp only [factorSum, Matrix.mul_sum, Matrix.sum_mul, Matrix.mul_smul, Matrix.smul_mul,
    Matrix.mul_vecMulVec, Matrix.vecMulVec_mul, Matrix.vecMul_transpose]

theorem factorSum_diagonal (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (F : Finset (Fin M)) {r : ℕ} (T : Matrix (Fin r) (Fin p) ℚ) (i : Fin r) :
    (T * factorSum u w F * Tᵀ) i i = ∑ j ∈ F, w j * ((T *ᵥ u j) i)^2 := by
  rw [transform_factorSum]
  simp only [Matrix.sum_apply, Matrix.smul_apply, Matrix.vecMulVec_apply, smul_eq_mul]
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem factorSum_range (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (F : Finset (Fin M)) (s : Finset (Fin M))
    (hrange : ∀ j ∈ F, rangeProjector (columns u s) *ᵥ u j = u j) :
    rangeProjector (columns u s) * factorSum u w F = factorSum u w F := by
  simp only [factorSum,Matrix.mul_sum,Matrix.mul_smul,Matrix.mul_vecMulVec]
  apply Finset.sum_congr rfl
  intro j hj
  rw [hrange j hj]

/-- The strict factor coordinate bound implies the source atom diagonal filter.
Each PSD input contributes at most p LDL factors. -/
theorem factorSum_accepts (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (F : Finset (Fin M)) (s : Finset (Fin M)) (hcard : F.card ≤ p)
    (hrange : ∀ j ∈ F, rangeProjector (columns u s) *ᵥ u j = u j)
    (hmag : ∀ j ∈ F, ∀ i, w j * ((transform u w s *ᵥ u j) i) ^ 2 < 4) :
    acceptsAtom u w s (factorSum u w F) := by
  refine ⟨factorSum_range u w F s hrange, ?_⟩
  intro i
  rw [factorSum_diagonal]
  calc
    ∑ j ∈ F, w j * ((transform u w s *ᵥ u j) i)^2 ≤ ∑ _j ∈ F, (4:ℚ) :=
      Finset.sum_le_sum (fun j hj => (hmag j hj i).le)
    _ = 4 * F.card := by simp [mul_comm]
    _ ≤ 4 * p := mul_le_mul_of_nonneg_left (by exact_mod_cast hcard) (by norm_num)

/-- The atom test also bounds every entry; no entrywise cancellation estimate
is assumed by the producer. -/
theorem real_factor_coordinate_bound {w τ : ℚ} (hw : 0 ≤ w)
    (h : |Real.sqrt (w : ℝ) * (τ : ℝ)| < 2) : w * τ^2 < 4 := by
  have hs := Real.sq_sqrt (show (0:ℝ) ≤ w by exact_mod_cast hw)
  have ha := abs_lt.mp h
  have hp : (Real.sqrt (w:ℝ) * (τ:ℝ))^2 < 4 := by nlinarith
  have hreal : (w:ℝ) * (τ:ℝ)^2 < 4 := by nlinarith
  exact_mod_cast hreal

/-- Membership in the actual real column span proves the exact rational
projector test; rational coefficients are not an extra premise. -/
theorem projector_eq_of_real_span {r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (hV : Function.Injective V.mulVec) (v : Fin p → ℚ)
    (hv : (fun i => (v i : ℝ)) ∈
      Submodule.span ℝ (Set.range (ratMatrixReal V).col)) :
    rangeProjector V *ᵥ v = v := by
  rw [← Matrix.range_mulVecLin] at hv
  obtain ⟨x,hx⟩ := hv
  have hPV : rangeProjector V * V = V := by
    rw [rangeProjector,Matrix.mul_assoc,gramLeftInverse_mul V hV,Matrix.mul_one]
  have he : ratMatrixReal (rangeProjector V) *ᵥ (fun i => (v i : ℝ)) =
      fun i => (v i : ℝ) := by
    rw [← hx]
    change ratMatrixReal (rangeProjector V) *ᵥ ((ratMatrixReal V) *ᵥ x) =
      (ratMatrixReal V) *ᵥ x
    rw [Matrix.mulVec_mulVec,← ratMatrixReal_mul,hPV]
  rw [ratMatrixReal_mulVec] at he
  funext i
  exact_mod_cast congrFun he i

end NormalizationTrials
end
end DAGSpectral
