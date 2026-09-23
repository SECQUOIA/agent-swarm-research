import Formal.DAGSpectral.CriterionSelectWeightedTrace
import Formal.DAGSpectral.CriterionSelectCostTrace

namespace DAGSpectral
open ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost

def weightedContrastCostLERun {n m : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ)
    (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ) : Bool × List ArithmeticEvent :=
  let a := rationalWeightedContrastCostWithTrace A cs ws
  let b := rationalWeightedContrastCostWithTrace B cs ws
  let c := rationalCostLERun a.1 b.1
  (c.1,a.2 ++ b.2 ++ c.2)

@[simp] theorem weightedContrastCostLERun_value {n m : ℕ}
    (A B : Matrix (Fin n) (Fin n) ℚ) (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ) :
    (weightedContrastCostLERun A B cs ws).1 = weightedContrastCostLE A B cs ws := by
  simp [weightedContrastCostLERun,weightedContrastCostLE]

def weightedCompareOperations (n m : ℕ) : ℕ := 2*m*(contrastOperations n+7)+3

theorem weightedContrastCostLERun_bounds {n m B : ℕ} (hB : 0 < B)
    {A D : Matrix (Fin n) (Fin n) ℚ} {cs : Fin m → Fin n → ℚ} {ws : Fin m → ℚ}
    (hA : MatrixBits A B) (hD : MatrixBits D B)
    (hc : ∀ i j, RationalBits (cs i j) B) (hw : ∀ i, RationalBits (ws i) B) :
    (weightedContrastCostLERun A D cs ws).2.length ≤ weightedCompareOperations n m ∧
      ∀ e ∈ (weightedContrastCostLERun A D cs ws).2,
        eventBits (weightedContrastTraceBits n m B) e := by
  have ha := rationalWeightedContrastCostWithTrace_bits hB hA hc hw
  have hd := rationalWeightedContrastCostWithTrace_bits hB hD hc hw
  have hp : 0 < weightedContrastTraceBits n m B := by
    unfold weightedContrastTraceBits weightedFoldWidth
    omega
  have hs := rationalCostLERun_bounds hp
    (show optionalRationalBits (rationalWeightedContrastCostWithTrace A cs ws).1
      (weightedContrastTraceBits n m B) from fun q hq => ha.1 q hq)
    (show optionalRationalBits (rationalWeightedContrastCostWithTrace D cs ws).1
      (weightedContrastTraceBits n m B) from fun q hq => hd.1 q hq)
  refine ⟨?_,?_⟩
  · have hl := rationalWeightedContrastCostWithTrace_length A cs ws
    have hr := rationalWeightedContrastCostWithTrace_length D cs ws
    simp only [weightedContrastCostLERun,List.length_append]
    unfold weightedCompareOperations
    nlinarith
  · intro e he
    simp only [weightedContrastCostLERun,List.mem_append] at he
    rcases he with (he|he)|he
    · exact ha.2 e he
    · exact hd.2 e he
    · exact hs.2 e he

def selectWeightedContrastRun {α : Type*} {n m : ℕ}
    (J : α → Matrix (Fin n) (Fin n) ℚ) (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ)
    (xs : List α) : Option α × List ArithmeticEvent :=
  bestByRun (fun a b => weightedContrastCostLERun (J b) (J a) cs ws) xs

@[simp] theorem selectWeightedContrastRun_result {α : Type*} {n m : ℕ}
    (J : α → Matrix (Fin n) (Fin n) ℚ) (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ)
    (xs : List α) : (selectWeightedContrastRun J cs ws xs).1 =
      selectWeightedContrast J cs ws xs := by
  simp only [selectWeightedContrastRun,bestByRun_result,weightedContrastCostLERun_value,
    selectWeightedContrast]

theorem selectWeightedContrastRun_bitWork {α : Type*} {n m B : ℕ} (hB : 0 < B)
    (J : α → Matrix (Fin n) (Fin n) ℚ) (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ)
    (xs : List α) (hJ : ∀ a ∈ xs, MatrixBits (J a) B)
    (hc : ∀ i j, RationalBits (cs i j) B) (hw : ∀ i, RationalBits (ws i) B) :
    traceBitWork (weightedContrastTraceBits n m B) (selectWeightedContrastRun J cs ws xs).2 ≤
      (xs.length-1)*weightedCompareOperations n m*
        (256*(weightedContrastTraceBits n m B+1)^3) :=
  bestByRun_bitWork _ (fun a => MatrixBits (J a) B)
    (fun _ ha _ hb => weightedContrastCostLERun_bounds hB hb ha hc hw) xs hJ

theorem weighted_arithmeticWidth_linear {K L B : ℕ} (d : ℕ)
    (hK : K ≤ L * (B + 1)) : arithmeticWidth d K ≤ (2^d*(L+2))*(B+1) := by
  have h0 : arithmeticWidth d K ≤ 2^d*(K+2) := Nat.sub_le _ _
  have h1 : K+2 ≤ (L+2)*(B+1) := by nlinarith
  exact h0.trans (by simpa only [mul_assoc] using Nat.mul_le_mul_left (2^d) h1)

def contrastWidthConstant (n : ℕ) : ℕ :=
  2^(2*n)*(2^(2*n)*(2^(pseudoInverseTraceDepth n)*3+3)+2)

theorem contrastTraceBits_linear (n B : ℕ) :
    contrastTraceBits n B ≤ contrastWidthConstant n*(B+1) := by
  have h0 := weighted_arithmeticWidth_linear (L := 1) (B := B)
    (pseudoInverseTraceDepth n) (show B ≤ 1*(B+1) by omega)
  have h1 : arithmeticWidth (pseudoInverseTraceDepth n) B+B+1 ≤
      (2^(pseudoInverseTraceDepth n)*3+1)*(B+1) := by nlinarith
  have h2 := weighted_arithmeticWidth_linear (2*n) h1
  exact weighted_arithmeticWidth_linear (2*n) h2

def weightedWidthConstant (n : ℕ) : ℕ := 3*(contrastWidthConstant n+2)

theorem weightedContrastTraceBits_linear (n m B : ℕ) :
    weightedContrastTraceBits n m B+1 ≤ weightedWidthConstant n*(m+1)*(B+1) := by
  have hc := contrastTraceBits_linear n B
  have hk : weightedContrastInputBits n B+1 ≤ (contrastWidthConstant n+2)*(B+1) := by
    unfold weightedContrastInputBits
    nlinarith
  have h0 : weightedContrastTraceBits n m B+1 ≤
      3*(m+1)*(weightedContrastInputBits n B+1) := by
    unfold weightedContrastTraceBits weightedFoldWidth
    nlinarith
  have h1 := Nat.mul_le_mul_left (3*(m+1)) hk
  unfold weightedWidthConstant
  nlinarith

def weightedSelectionBitConstant (n : ℕ) : ℕ :=
  (2*contrastOperations n+17)*256*(weightedWidthConstant n)^3

/-- Complete scan cost, polynomial in candidate count, contrast count, and input
bit width. Only the matrix dimension enters the constant. -/
theorem selectWeightedContrastRun_polynomial_bitWork {α : Type*} {n m B : ℕ}
    (hB : 0 < B) (J : α → Matrix (Fin n) (Fin n) ℚ)
    (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ) (xs : List α)
    (hJ : ∀ a ∈ xs, MatrixBits (J a) B)
    (hc : ∀ i j, RationalBits (cs i j) B) (hw : ∀ i, RationalBits (ws i) B) :
    traceBitWork (weightedContrastTraceBits n m B) (selectWeightedContrastRun J cs ws xs).2 ≤
      weightedSelectionBitConstant n*xs.length*(m+1)^4*(B+1)^3 := by
  have ho : weightedCompareOperations n m ≤ (2*contrastOperations n+17)*(m+1) := by
    unfold weightedCompareOperations
    nlinarith
  have hk := Nat.pow_le_pow_left (weightedContrastTraceBits_linear n m B) 3
  have hl : xs.length-1 ≤ xs.length := Nat.sub_le _ _
  apply (selectWeightedContrastRun_bitWork hB J cs ws xs hJ hc hw).trans
  calc
    _ ≤ xs.length*((2*contrastOperations n+17)*(m+1))*
        (256*(weightedWidthConstant n*(m+1)*(B+1))^3) := by gcongr
    _ = _ := by unfold weightedSelectionBitConstant; ring

end DAGSpectral
