import QipmFormal.SDPMixture.Defs
import QipmFormal.Mixture.Decoder

/-!
# Matrix observables and mixture-stable wrong outputs

The decoder acts on the trace-normalized positive matrix, not on the
amplitude vector of its symmetric coordinates.
-/
namespace QipmFormal.SDPMixture
noncomputable section
open scoped BigOperators MatrixOrder
open Matrix

variable {I n : Type*} [Fintype I] [Fintype n] [DecidableEq n]

omit [DecidableEq n] in
theorem trace_matrixMix (w : I → ℝ) (X : I → Matrix n n ℝ) :
    (matrixMix w X).trace = ∑ i, w i * (X i).trace := by
  simp [matrixMix]

omit [DecidableEq n] in
theorem trace_mul_matrixMix (w : I → ℝ) (X : I → Matrix n n ℝ)
    (O : Matrix n n ℝ) :
    (O * matrixMix w X).trace = ∑ i, w i * (O * X i).trace := by
  simp [matrixMix, Matrix.mul_sum]

omit [DecidableEq n] in
theorem trace_mul_nonneg_of_posSemidef {A B : Matrix n n ℝ}
    (hA : A.PosSemidef) (hB : B.PosSemidef) : 0 ≤ (A * B).trace := by
  classical
  have hs : (CFC.sqrt B).IsHermitian := (CFC.sqrt_nonneg B).posSemidef.isHermitian
  have hp := (hA.mul_mul_conjTranspose_same (CFC.sqrt B)).trace_nonneg
  rw [hs.eq, Matrix.trace_mul_cycle, ← pow_two, CFC.sq_sqrt B hB.nonneg] at hp
  simpa only [Matrix.trace_mul_comm B A] using hp

theorem observable_trace_bounds {O X : Matrix n n ℝ}
    (hX : X.PosSemidef) (hlo : -(1 : Matrix n n ℝ) ≤ O)
    (hhi : O ≤ 1) : -(X.trace) ≤ (O * X).trace ∧ (O * X).trace ≤ X.trace := by
  have hl := trace_mul_nonneg_of_posSemidef (Matrix.le_iff.mp hlo) hX
  have hu := trace_mul_nonneg_of_posSemidef (Matrix.le_iff.mp hhi) hX
  simp only [sub_mul, Matrix.trace_sub, neg_mul, one_mul, Matrix.trace_neg] at hl hu
  constructor <;> linarith

/-- The expectation of the two-outcome observable in the trace-normalized state. -/
def observableExpectation (O X : Matrix n n ℝ) : ℝ := (O * X).trace / X.trace

def plusProbability (O X : Matrix n n ℝ) : ℝ :=
  (1 + observableExpectation O X) / 2

/-- Trace normalization produces the density matrix used by the decoder. -/
def density (X : Matrix n n ℝ) : Matrix n n ℝ := X.trace⁻¹ • X

omit [DecidableEq n] in
theorem density_posSemidef {X : Matrix n n ℝ} (hX : X.PosSemidef) :
    (density X).PosSemidef := hX.smul (inv_nonneg.mpr hX.trace_nonneg)

omit [DecidableEq n] in
theorem trace_density {X : Matrix n n ℝ} (ht : 0 < X.trace) :
    (density X).trace = 1 := by
  simp [density, ne_of_gt ht]

omit [DecidableEq n] in
theorem observableExpectation_eq_trace (O X : Matrix n n ℝ) :
    observableExpectation O X = (O * density X).trace := by
  simp [observableExpectation, density, div_eq_mul_inv, mul_comm]

/-- The positive outcome effect of the binary measurement. -/
def plusEffect (O : Matrix n n ℝ) : Matrix n n ℝ := (1 / 2 : ℝ) • (1 + O)

omit [Fintype n] in
theorem plusEffect_posSemidef {O : Matrix n n ℝ}
    (hlo : -(1 : Matrix n n ℝ) ≤ O) : (plusEffect O).PosSemidef := by
  apply Matrix.PosSemidef.smul _ (by norm_num)
  simpa only [sub_neg_eq_add, add_comm] using Matrix.le_iff.mp hlo

omit [Fintype n] in
theorem minusEffect_posSemidef {O : Matrix n n ℝ}
    (hhi : O ≤ 1) : (plusEffect (-O)).PosSemidef := by
  apply plusEffect_posSemidef
  exact neg_le_neg hhi

omit [Fintype n] in
theorem binary_effects_sum (O : Matrix n n ℝ) :
    plusEffect O + plusEffect (-O) = 1 := by
  unfold plusEffect
  rw [← smul_add]
  have h : (1 + O) + (1 + -O) = (2 : ℝ) • (1 : Matrix n n ℝ) := by
    rw [two_smul]
    abel
  rw [h, smul_smul]
  norm_num

theorem plusProbability_eq_measurement (O : Matrix n n ℝ) (X : Matrix n n ℝ)
    (ht : 0 < X.trace) :
    plusProbability O X = (plusEffect O * density X).trace := by
  rw [plusEffect, Matrix.smul_mul, add_mul, one_mul, Matrix.trace_smul,
    Matrix.trace_add, trace_density ht, ← observableExpectation_eq_trace]
  simp only [smul_eq_mul, plusProbability]
  ring

theorem observableExpectation_bounds {O X : Matrix n n ℝ}
    (hX : X.PosSemidef) (ht : 0 < X.trace)
    (hlo : -(1 : Matrix n n ℝ) ≤ O) (hhi : O ≤ 1) :
    -1 ≤ observableExpectation O X ∧ observableExpectation O X ≤ 1 := by
  have h := observable_trace_bounds hX hlo hhi
  unfold observableExpectation
  constructor
  · apply (le_div_iff₀ ht).mpr
    simpa using h.1
  · apply (div_le_iff₀ ht).mpr
    simpa using h.2

theorem plusProbability_valid {O X : Matrix n n ℝ}
    (hX : X.PosSemidef) (ht : 0 < X.trace)
    (hlo : -(1 : Matrix n n ℝ) ≤ O) (hhi : O ≤ 1) :
    0 ≤ plusProbability O X ∧ plusProbability O X ≤ 1 := by
  have h := observableExpectation_bounds hX ht hlo hhi
  unfold plusProbability
  constructor <;> linarith

omit [DecidableEq n] in
theorem plusProbability_bias (O X : Matrix n n ℝ) :
    plusProbability O X - 1 / 2 = observableExpectation O X / 2 := by
  unfold plusProbability
  ring

omit [DecidableEq n] in
/-- Trace weighting preserves every common signed neighbor margin. -/
theorem observable_margin_mix (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (X : I → Matrix n n ℝ) (O : Matrix n n ℝ) (p γ : ℝ)
    (hmargin : ∀ i, γ * (X i).trace ≤ p * (O * X i).trace) :
    γ * (matrixMix w X).trace ≤ p * (O * matrixMix w X).trace := by
  rw [trace_matrixMix, trace_mul_matrixMix]
  simp only [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro i _
  have h := mul_le_mul_of_nonneg_left (hmargin i) (hw.1 i)
  nlinarith

omit [DecidableEq n] in
theorem observable_normalized_margin_mix (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (X : I → Matrix n n ℝ) (O : Matrix n n ℝ) (p γ : ℝ)
    (ht : 0 < (matrixMix w X).trace)
    (hmargin : ∀ i, γ * (X i).trace ≤ p * (O * X i).trace) :
    γ ≤ p * observableExpectation O (matrixMix w X) := by
  rw [observableExpectation, ← mul_div_assoc]
  exact (le_div_iff₀ ht).mpr (observable_margin_mix w hw X O p γ hmargin)

/-- A general affine score may use primal, slack, and multiplier coordinates. -/
def matrixTripleScore {R : Type*} [Fintype R] (AX AS : Matrix n n ℝ)
    (ay : R → ℝ) (a₀ : ℝ) (X : Matrix n n ℝ) (y : R → ℝ)
    (S : Matrix n n ℝ) : ℝ :=
  (AX * X).trace + (AS * S).trace + Mixture.dot ay y + a₀

omit [DecidableEq n] in
theorem matrixTripleScore_mix {R : Type*} [Fintype R]
    (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (AX AS : Matrix n n ℝ) (ay : R → ℝ) (a₀ : ℝ)
    (X S : I → Matrix n n ℝ) (y : I → R → ℝ) :
    matrixTripleScore AX AS ay a₀ (matrixMix w X) (Mixture.mix w y) (matrixMix w S) =
      ∑ i, w i * matrixTripleScore AX AS ay a₀ (X i) (y i) (S i) := by
  simp only [matrixTripleScore, trace_mul_matrixMix, Mixture.dot_mix,
    mul_add, Finset.sum_add_distrib, ← Finset.sum_mul, hw.2, one_mul]

omit [DecidableEq n] in
theorem matrixTripleScore_wrong_mix {R : Type*} [Fintype R]
    (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (AX AS : Matrix n n ℝ) (ay : R → ℝ) (a₀ p γ : ℝ)
    (X S : I → Matrix n n ℝ) (y : I → R → ℝ)
    (hwrong : ∀ i, p * matrixTripleScore AX AS ay a₀ (X i) (y i) (S i) ≤ -γ) :
    p * matrixTripleScore AX AS ay a₀ (matrixMix w X) (Mixture.mix w y) (matrixMix w S)
      ≤ -γ := by
  rw [matrixTripleScore_mix w hw, Finset.mul_sum]
  calc
    _ ≤ ∑ i, w i * (-γ) := Finset.sum_le_sum fun i _ => by
      simpa only [mul_left_comm p] using mul_le_mul_of_nonneg_left (hwrong i) (hw.1 i)
    _ = -γ := by rw [← Finset.sum_mul, hw.2, one_mul]

end
end QipmFormal.SDPMixture
