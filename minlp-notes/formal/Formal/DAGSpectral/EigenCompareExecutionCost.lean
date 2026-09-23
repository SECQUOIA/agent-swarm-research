import Formal.DAGSpectral.EigenCompareExecution
import Formal.DAGSpectral.EigenCompareComplexity

/-! Polynomial bit work of the complete executable exact comparator. All
budgets are derived from the original rational entries, not supplied gaps or
an algebraic comparison oracle. -/
namespace DAGSpectral
open ReciprocalAnchor Matrix

lemma arithmeticWidth_bits_mono (d : ℕ) {B C : ℕ} (h : B ≤ C) :
    arithmeticWidth d B ≤ arithmeticWidth d C := by
  unfold arithmeticWidth
  exact Nat.sub_le_sub_right (Nat.mul_le_mul_left _ (Nat.add_le_add_right h 2)) 2

def eigenExecutionDepth (n : ℕ) : ℕ :=
  coefficientOperations (n*n) + coefficientOperations n + 10

def eigenExecutionBase (n C : ℕ) : ℕ :=
  10 + 2*C + eigenRadiusBits n C + eigenGapBits n C +
    separationPreprocessingWidth (n*n+1) (charpolyBits (n*n) (2*C+1)) +
    radiusPreprocessingWidth n C + 4*eigenDepthBound n C

def eigenExecutionWidth (n C : ℕ) : ℕ :=
  arithmeticWidth (eigenExecutionDepth n) (eigenExecutionBase n C)

theorem eigenComparisonExecutionTrace_bits {n C : ℕ} (hC : 0 < C)
    {A B : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A C) (hB : MatrixBits B C) :
    ∀ e ∈ eigenComparisonExecutionTrace A B, eventBits (eigenExecutionWidth n C) e := by
  let W := eigenExecutionBase n C
  let D := eigenExecutionDepth n
  let T := eigenComparisonDepth A B
  have hT : T ≤ eigenDepthBound n C := eigenComparisonDepth_le hA hB
  have hW : 0 < W := by dsimp [W,eigenExecutionBase]; omega
  have hBW : W ≤ eigenExecutionWidth n C := by
    change W ≤ arithmeticWidth D W
    simpa only [arithmeticWidth_zero] using
      arithmeticWidth_mono (B := W) (Nat.zero_le D)
  have hRW : eigenRadiusBits n C ≤ W := by dsimp [W,eigenExecutionBase]; omega
  have hGW : eigenGapBits n C ≤ W := by dsimp [W,eigenExecutionBase]; omega
  have hCW : 2*C+1 ≤ W := by dsimp [W,eigenExecutionBase]; omega
  have h8 : 8 ≤ D := by dsimp [D,eigenExecutionDepth]; omega
  have hR : RationalBits (eigenSearchRadius A B) (eigenRadiusBits n C) :=
    eigenSearchRadius_bits hA hB
  have hG := eigenComparisonGap_bits hA hB
  have hloop (M : Matrix (Fin n) (Fin n) ℚ) (hM : MatrixBits M C) :
      ∀ e ∈ dyadicExecutionTrace (eigenThresholdTestWithTrace M)
        (eigenSearchRadius A B) T, eventBits (eigenExecutionWidth n C) e := by
    apply dyadicExecutionTrace_bits _ hR _ _ le_rfl
    · apply le_trans _ hBW
      dsimp [W,eigenExecutionBase]
      omega
    · intro q hq e he
      apply eventBits_mono (eigenThresholdTestWithTrace_bits hM hq e he)
      apply le_trans (arithmeticWidth_bits_mono _ ?_) (arithmeticWidth_mono ?_)
      · dsimp [W,eigenExecutionBase]
        omega
      · dsimp [D,eigenExecutionDepth]
        omega
  intro e he
  simp only [eigenComparisonExecutionTrace, List.mem_append] at he
  rcases he with ((((((he | he) | he) | he) | he) | he) | he) | he
  · apply eventBits_mono (eigenDifferenceWithTrace_bits hC hA hB e he)
    exact (arithmeticWidth_bits_mono _ (by omega : C ≤ W)).trans
      (arithmeticWidth_mono (by omega : 1 ≤ D))
  · apply eventBits_mono
      (charpolyCoefficientsWithTrace_bits (by omega : 0 < 2*C+1)
        (eigenDifferenceFinite_bits hA hB) e he)
    exact (arithmeticWidth_bits_mono _ hCW).trans
      (arithmeticWidth_mono (by dsimp [D,eigenExecutionDepth]; omega))
  · have hh := separationFromCoefficientsWithTrace_bits
      (eigenDifferenceCoefficients_bits hA hB) e he
    rw [eigenDifferenceCoefficients_length] at hh
    apply eventBits_mono hh
    apply le_trans _ hBW
    dsimp [W,eigenExecutionBase]
    omega
  · apply eventBits_mono (eigenSearchRadiusWithTrace_bits hA hB e he)
    apply le_trans _ hBW
    dsimp [W,eigenExecutionBase]
    omega
  · have hfour : RationalBits (4:ℚ) W := by
      have hh : RationalBits (4:ℚ) 3 := by unfold RationalBits; decide
      exact rationalBits_mono hh (by dsimp [W,eigenExecutionBase]; omega)
    have hx := (eigenDepthExpr (eigenSearchRadius A B) (eigenComparisonGap A B)).eval_trace_bits
      (show (eigenDepthExpr _ _).leavesBounded W from
        ⟨⟨hfour,rationalBits_mono hR hRW⟩,rationalBits_mono hG hGW⟩)
    apply eventBits_mono (hx.2 e he)
    simp only [eigenDepthExpr_operations]
    exact arithmeticWidth_mono (by omega)
  · exact hloop A hA e he
  · exact hloop B hB e he
  · have htW : 2*T+2 ≤ W := by dsimp [W,eigenExecutionBase]; omega
    apply eventBits_mono (eigenFinishWithTrace_bits hW
      (rationalBits_mono hR hRW) (rationalBits_mono hG hGW)
      (dyadicIndex_lt _ _ _) (dyadicIndex_lt _ _ _) htW e he)
    exact arithmeticWidth_mono h8

def eigenPreprocessingOperations (n : ℕ) : ℕ :=
  (n*n)*(n*n) + (n*n+1)*coefficientOperations (n*n) + 4*(n*n+1)+3 + 6*n+2 + 2 + 18

def eigenExecutionOperationBound (n T : ℕ) : ℕ :=
  eigenPreprocessingOperations n + 2*T*(T+thresholdTestOperations n+5)+T

theorem eigenComparisonExecutionTrace_length {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    (eigenComparisonExecutionTrace A B).length ≤
      eigenExecutionOperationBound n (eigenComparisonDepth A B) := by
  have hc := charpolyCoefficientsWithTrace_length (eigenDifferenceFinite A B)
  have hg := separationFromCoefficientsWithTrace_length (eigenDifferenceCoefficients A B)
  rw [eigenDifferenceCoefficients_length] at hg
  have hr := eigenSearchRadiusWithTrace_length A B
  have hleft := dyadicExecutionTrace_length (eigenThresholdTestWithTrace A)
    (eigenThresholdTestWithTrace_length A) (eigenSearchRadius A B) (eigenComparisonDepth A B)
  have hright := dyadicExecutionTrace_length (eigenThresholdTestWithTrace B)
    (eigenThresholdTestWithTrace_length B) (eigenSearchRadius A B) (eigenComparisonDepth A B)
  simp only [eigenComparisonExecutionTrace, List.length_append,
    eigenDifferenceWithTrace_length, ArithmeticExpr.trace_length,
    eigenDepthExpr_operations, eigenFinishWithTrace_length]
  unfold eigenExecutionOperationBound eigenPreprocessingOperations
  nlinarith

theorem eigenComparisonExecution_bitWork {n C : ℕ} (hC : 0 < C)
    {A B : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A C) (hB : MatrixBits B C) :
    traceBitWork (eigenExecutionWidth n C) (compareMinimumEigenvaluesWithTrace A B).2 ≤
      eigenExecutionOperationBound n (eigenComparisonDepth A B) *
        (256*(eigenExecutionWidth n C+1)^3) := by
  rw [compareMinimumEigenvaluesWithTrace_eq]
  exact (traceBitWork_le (eigenComparisonExecutionTrace_bits hC hA hB)).trans
    (Nat.mul_le_mul_right _ (eigenComparisonExecutionTrace_length A B))

def eigenExecutionBaseLinear (n : ℕ) : ℕ :=
  12 + eigenRadiusLinear n + eigenGapLinear n +
    (2*(n*n+1)+3)*(eigenCoeffLinear (n*n)+1) + (2*n+3) + 4*eigenDepthLinear n

theorem eigenExecutionBase_linear (n C : ℕ) :
    eigenExecutionBase n C ≤ eigenExecutionBaseLinear n * (C+1) := by
  have hr := eigenRadiusBits_linear n C
  have hg := eigenGapBits_linear n C
  have ht := eigenDepthBound_linear n C
  have hp := radiusPreprocessingWidth_linear n C
  have hs := separationPreprocessingWidth_linear (n*n+1) (charpolyBits (n*n) (2*C+1))
  have hc := eigenCharpolyBits_linear (n*n) C
  have hcs : charpolyBits (n*n) (2*C+1)+1 ≤ (eigenCoeffLinear (n*n)+1)*(C+1) := by
    nlinarith
  have hs' := hs.trans (Nat.mul_le_mul_left _ hcs)
  unfold eigenExecutionBase eigenExecutionBaseLinear
  nlinarith

def eigenExecutionWidthLinear (n : ℕ) : ℕ :=
  2^(eigenExecutionDepth n)*(eigenExecutionBaseLinear n+2)+1

theorem eigenExecutionWidth_linear (n C : ℕ) :
    eigenExecutionWidth n C+1 ≤ eigenExecutionWidthLinear n*(C+1) := by
  have hb := eigenExecutionBase_linear n C
  have hb' : eigenExecutionBase n C+2 ≤ (eigenExecutionBaseLinear n+2)*(C+1) := by
    nlinarith
  have hm := Nat.mul_le_mul_left (2^(eigenExecutionDepth n)) hb'
  have hw : eigenExecutionWidth n C ≤
      2^(eigenExecutionDepth n)*(eigenExecutionBase n C+2) := by
    exact Nat.sub_le _ _
  unfold eigenExecutionWidthLinear
  nlinarith

def eigenExecutionOperationConstant (n : ℕ) : ℕ :=
  eigenPreprocessingOperations n+2*thresholdTestOperations n+13

theorem eigenExecutionOperationBound_quadratic (n T : ℕ) :
    eigenExecutionOperationBound n T ≤ eigenExecutionOperationConstant n*(T+1)^2 := by
  have h1 : 1 ≤ (T+1)^2 := by
    have : 0 < (T+1)^2 := by positivity
    omega
  have ht : T ≤ (T+1)^2 := by nlinarith
  have ht2 : T*T ≤ (T+1)^2 := by nlinarith
  have hpre := Nat.mul_le_mul_left (eigenPreprocessingOperations n) h1
  have hlinear := Nat.mul_le_mul_left (2*thresholdTestOperations n+11) ht
  have hquad := Nat.mul_le_mul_left 2 ht2
  unfold eigenExecutionOperationBound eigenExecutionOperationConstant
  nlinarith

def eigenComparisonBitConstant (n : ℕ) : ℕ :=
  256*eigenExecutionOperationConstant n*(eigenDepthLinear n+1)^2*
    (eigenExecutionWidthLinear n)^3

/-- The returned comparison is exact, and its complete recorded rational
arithmetic costs at most a dimension-dependent constant times `(inputBits+1)^5`.
The exponent is uniform; fixed dimension is the only parameter absorbed into
its constant. Inputs may have repeated or exactly equal eigenvalues. -/
theorem compareMinimumEigenvalues_polynomial_bitWork {n C : ℕ} (hC : 0 < C)
    {A B : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A C) (hB : MatrixBits B C) :
    traceBitWork (eigenExecutionWidth n C) (compareMinimumEigenvaluesWithTrace A B).2 ≤
      eigenComparisonBitConstant n*(C+1)^5 := by
  have ht := eigenComparisonDepth_linear hA hB
  have ht' : eigenComparisonDepth A B+1 ≤ (eigenDepthLinear n+1)*(C+1) := by nlinarith
  have ho := (eigenExecutionOperationBound_quadratic n (eigenComparisonDepth A B)).trans
    (Nat.mul_le_mul_left _ (Nat.pow_le_pow_left ht' 2))
  have hw := Nat.pow_le_pow_left (eigenExecutionWidth_linear n C) 3
  have hcost := eigenComparisonExecution_bitWork hC hA hB
  apply hcost.trans
  calc
    _ ≤ (eigenExecutionOperationConstant n*((eigenDepthLinear n+1)*(C+1))^2)*
        (256*(eigenExecutionWidthLinear n*(C+1))^3) := by gcongr
    _ = eigenComparisonBitConstant n*(C+1)^5 := by unfold eigenComparisonBitConstant; ring

end DAGSpectral
