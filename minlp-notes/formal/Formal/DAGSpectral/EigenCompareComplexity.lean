import Formal.DAGSpectral.EigenCompare
import Formal.DAGSpectral.EigenComparePreprocessingTrace

/-! Input-matrix bit bounds for the actual eigenvalue-comparison radius,
computed separation gap, and finite bisection depth. -/
namespace DAGSpectral
open ReciprocalAnchor Matrix
open scoped BigOperators

lemma eigenDifferenceMatrix_bits {n C : ℕ} {A B : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A C) (hB : MatrixBits B C) :
    MatrixBits (eigenDifferenceMatrix A B) (2 * C + 1) := by
  intro i j
  have hz := rationalBits_mono rationalBits_zero (rationalBits_pos (hA i.1 j.1))
  have ha : RationalBits (if i.2 = j.2 then A i.1 j.1 else 0) C := by
    split_ifs
    · exact hA _ _
    · exact hz
  have hb : RationalBits (if i.1 = j.1 then B i.2 j.2 else 0) C := by
    split_ifs
    · exact hB _ _
    · exact hz
  simpa only [eigenDifferenceMatrix, two_mul] using rationalBits_sub ha hb

lemma eigenDifferenceFinite_bits {n C : ℕ} {A B : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A C) (hB : MatrixBits B C) :
    MatrixBits (eigenDifferenceFinite A B) (2 * C + 1) := by
  intro i j
  exact eigenDifferenceMatrix_bits hA hB (finProdFinEquiv.symm i) (finProdFinEquiv.symm j)

lemma eigenDifferenceCoefficients_length {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    (eigenDifferenceCoefficients A B).length = n * n + 1 := by
  simp [eigenDifferenceCoefficients]

lemma eigenDifferenceCoefficients_bits {n C : ℕ} {A B : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A C) (hB : MatrixBits B C) :
    ∀ q ∈ eigenDifferenceCoefficients A B,
      RationalBits q (charpolyBits (n * n) (2 * C + 1)) := by
  intro q hq
  obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hq
  exact rationalCharpolyCoeff_bits (eigenDifferenceFinite_bits hA hB) i

/-- Bit budget for the actual rational search radius. -/
def eigenRadiusBits (n C : ℕ) : ℕ := 5 + 2 * n * (C + 1)

def eigenGapBits (n C : ℕ) : ℕ :=
  rootSeparationBitBound (n * n) (charpolyBits (n * n) (2 * C + 1))

def eigenDepthBound (n C : ℕ) : ℕ := 3 + eigenRadiusBits n C + eigenGapBits n C

lemma eigenComparisonGap_bits {n C : ℕ} {A B : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A C) (hB : MatrixBits B C) :
    RationalBits (eigenComparisonGap A B) (eigenGapBits n C) := by
  apply separationFromCoefficients_bits_of_length
    (le_of_eq (eigenDifferenceCoefficients_length A B))
  exact eigenDifferenceCoefficients_bits hA hB

lemma eigenComparisonDepth_le {n C : ℕ} {A B : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A C) (hB : MatrixBits B C) :
    eigenComparisonDepth A B ≤ eigenDepthBound n C :=
  bisection_numerator_size (eigenSearchRadius_bits hA hB) (eigenComparisonGap_bits hA hB)

/-- Dimension-only coefficients for the linear input-size estimates. -/
def eigenRadiusLinear (n : ℕ) : ℕ := 5 + 2 * n

def eigenCoeffLinear (m : ℕ) : ℕ := 1 + 2 ^ m * (2 + m.factorial * (3 * m + 3))

def eigenGapLinear (n : ℕ) : ℕ := 2 + (n * n + 1) * (2 * eigenCoeffLinear (n * n) + 1)

def eigenDepthLinear (n : ℕ) : ℕ := 3 + eigenRadiusLinear n + eigenGapLinear n

lemma eigenRadiusBits_linear (n C : ℕ) :
    eigenRadiusBits n C ≤ eigenRadiusLinear n * (C + 1) := by
  unfold eigenRadiusBits eigenRadiusLinear
  nlinarith

lemma eigenCharpolyBits_linear (m C : ℕ) :
    charpolyBits m (2 * C + 1) ≤ eigenCoeffLinear m * (C + 1) := by
  unfold charpolyBits determinantBits eigenCoeffLinear
  ring_nf
  omega

lemma eigenGapBits_linear (n C : ℕ) :
    eigenGapBits n C ≤ eigenGapLinear n * (C + 1) := by
  have hc := eigenCharpolyBits_linear (n * n) C
  unfold eigenGapBits rootSeparationBitBound eigenGapLinear
  have hh := Nat.mul_le_mul_left (n * n + 1) (Nat.mul_le_mul_left 2 hc)
  nlinarith

lemma eigenDepthBound_linear (n C : ℕ) :
    eigenDepthBound n C ≤ eigenDepthLinear n * (C + 1) := by
  have hr := eigenRadiusBits_linear n C
  have hg := eigenGapBits_linear n C
  unfold eigenDepthBound eigenDepthLinear
  nlinarith

/-- The executed comparison depth is linear in the original matrix entry bit
budget at fixed dimension; no gap or coefficient-height hypothesis is supplied. -/
lemma eigenComparisonDepth_linear {n C : ℕ} {A B : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A C) (hB : MatrixBits B C) :
    eigenComparisonDepth A B ≤ eigenDepthLinear n * (C + 1) :=
  (eigenComparisonDepth_le hA hB).trans (eigenDepthBound_linear n C)

end DAGSpectral
