import Formal.QuadraticPrecision.SpectralUpper
import Formal.QuadraticPrecision.SquareMinimum

/-! Explicit positive-accuracy depths for the original quadratic. A unit
slack in the total weight also covers rank-zero and empty-dimensional inputs. -/
namespace QuadraticPrecision
noncomputable section
variable {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}

def precisionWeight (hH : H.IsHermitian) (l u : Input n) : ℝ :=
  spectralWeight hH l u + 1

theorem precisionWeight_pos (hH : H.IsHermitian) (l u : Input n) :
    0 < precisionWeight hH l u := by
  have := spectralWeight_nonneg hH l u
  unfold precisionWeight
  linarith

theorem spectral_error_le_accuracy (hH : H.IsHermitian) (l u : Input n)
    {ε : ℝ} (hε : 0 < ε) :
    spectralWeight hH l u *
      (squareWidth (precisionDepth (precisionWeight hH l u) ε))^2 / 4 ≤ ε := by
  rw [squareWidth_sq, mul_div_assoc]
  have hh := precisionDepth_sufficient (precisionWeight_pos hH l u) hε
  have hn : 0 ≤ (1 / 4 : ℝ) ^ precisionDepth (precisionWeight hH l u) ε / 4 := by positivity
  calc
    _ ≤ precisionWeight hH l u *
        ((1/4 : ℝ)^precisionDepth (precisionWeight hH l u) ε / 4) := by
      apply mul_le_mul_of_nonneg_right _ hn
      unfold precisionWeight
      linarith
    _ ≤ ε := hh

theorem quadratic_graph_binary_accuracy (hH : H.IsHermitian) (a l u : Input n)
    (b : ℝ) {ε : ℝ} (hε : 0 < ε) :
    HasBinaryGraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε
      (H.rank * precisionDepth (precisionWeight hH l u) ε) := by
  have h := (quadratic_graph_binary_upper hH a l u b
    (precisionDepth (precisionWeight hH l u) ε)).mono_error
    (spectral_error_le_accuracy hH l u hε)
  convert h using 1
  ext x
  simp only [Set.mem_Icc, Pi.le_def, Set.mem_ofPred_eq, forall_and]

theorem quadratic_epigraph_binary_accuracy (hH : H.IsHermitian) (a l u : Input n)
    (b : ℝ) {ε : ℝ} (hε : 0 < ε) :
    HasBinaryEpigraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε
      (negativeInertia hH * precisionDepth (precisionWeight hH l u) ε) := by
  have h := (quadratic_epigraph_binary_upper hH a l u b
    (precisionDepth (precisionWeight hH l u) ε)).mono_error
    (spectral_error_le_accuracy hH l u hε)
  convert h using 1
  ext x
  simp only [Set.mem_Icc, Pi.le_def, Set.mem_ofPred_eq, forall_and]

theorem quadratic_hypograph_binary_accuracy (hH : H.IsHermitian) (a l u : Input n)
    (b : ℝ) {ε : ℝ} (hε : 0 < ε) :
    HasBinaryHypographLift (Set.Icc l u) (quadraticPolynomial H a b) ε
      (positiveInertia hH * precisionDepth (precisionWeight hH l u) ε) := by
  have h := (quadratic_hypograph_binary_upper hH a l u b
    (precisionDepth (precisionWeight hH l u) ε)).mono_error
    (spectral_error_le_accuracy hH l u hε)
  convert h using 1
  ext x
  simp only [Set.mem_Icc, Pi.le_def, Set.mem_ofPred_eq, forall_and]

end
end QuadraticPrecision
