import Formal.MatroidSpectral.CriteriaExecution
import Formal.DAGSpectral.CriterionSelectContrastPath
import Formal.DAGSpectral.CriterionSelectWeightedPath

namespace MatroidSpectral
open Matrix DAGSpectral DAGSpectral.NormalizationTrials ReciprocalAnchor
variable {p m M : ℕ}

@[simp] theorem selectSetsRun_contrast (D : FactorData p m M)
    (c : Fin p → ℚ) (xs : List (Finset (Fin m))) :
    (selectSetsRun D (fun A B => contrastCostLERun B A c) xs).1 =
      selectContrast (information D) c xs := by
  simp only [selectSetsRun_result,contrastCostLERun_value,selectContrast]

theorem selectSetsRun_contrast_bitWork (D : FactorData p m M) {B q : ℕ}
    (hD : ∀ o, MatrixBits (D.atom o) B) (c : Fin p → ℚ)
    (hc : ∀ i, RationalBits (c i) B) (xs : List (Finset (Fin m)))
    (hxs : ∀ S ∈ xs, S.card ≤ q) :
    let K := contrastTraceBits p (1 + (q+1)*(B+1))
    traceBitWork K (selectSetsRun D (fun A B => contrastCostLERun B A c) xs).2 ≤
      (xs.length-1)*(2*(p*p*(q+1))+contrastComparisonOperations p)*(256*(K+1)^3) := by
  apply selectSetsRun_bitWork D hD (fun A B => contrastCostLERun B A c)
  · exact inputBits_le_contrastTraceBits _ _
  · intro A hA T hT
    exact contrastCostLERun_bounds (by omega) hT hA
      (fun i => rationalBits_mono (hc i) (by nlinarith))
  · exact hxs

@[simp] theorem selectSetsRun_weightedContrast (D : FactorData p m M) {k : ℕ}
    (cs : Fin k → Fin p → ℚ) (ws : Fin k → ℚ) (xs : List (Finset (Fin m))) :
    (selectSetsRun D (fun A B => weightedContrastCostLERun B A cs ws) xs).1 =
      selectWeightedContrast (information D) cs ws xs := by
  simp only [selectSetsRun_result,weightedContrastCostLERun_value,selectWeightedContrast]

theorem selectSetsRun_weightedContrast_bitWork (D : FactorData p m M) {k B q : ℕ}
    (hD : ∀ o, MatrixBits (D.atom o) B) (cs : Fin k → Fin p → ℚ)
    (ws : Fin k → ℚ) (hc : ∀ i j, RationalBits (cs i j) B)
    (hw : ∀ i, RationalBits (ws i) B) (xs : List (Finset (Fin m)))
    (hxs : ∀ S ∈ xs, S.card ≤ q) :
    let K := weightedContrastTraceBits p k (1 + (q+1)*(B+1))
    traceBitWork K
      (selectSetsRun D (fun A B => weightedContrastCostLERun B A cs ws) xs).2 ≤
      (xs.length-1)*(2*(p*p*(q+1))+weightedCompareOperations p k)*(256*(K+1)^3) := by
  have hBL : B ≤ 1 + (q+1)*(B+1) := by nlinarith
  apply selectSetsRun_bitWork D hD (fun A B => weightedContrastCostLERun B A cs ws)
  · unfold weightedContrastTraceBits weightedContrastInputBits
    omega
  · intro A hA T hT
    exact weightedContrastCostLERun_bounds (by omega) hT hA
      (fun i j => rationalBits_mono (hc i j) hBL)
      (fun i => rationalBits_mono (hw i) hBL)
  · exact hxs

theorem selectSetsRun_weightedContrast_polynomial_bitWork (D : FactorData p m M)
    {k B q : ℕ} (hD : ∀ o, MatrixBits (D.atom o) B)
    (cs : Fin k → Fin p → ℚ) (ws : Fin k → ℚ)
    (hc : ∀ i j, RationalBits (cs i j) B) (hw : ∀ i, RationalBits (ws i) B)
    (xs : List (Finset (Fin m))) (hxs : ∀ S ∈ xs, S.card ≤ q) :
    traceBitWork (weightedContrastTraceBits p k (1+(q+1)*(B+1)))
      (selectSetsRun D (fun A B => weightedContrastCostLERun B A cs ws) xs).2 ≤
      weightedPathSelectionConstant p*xs.length*(q+1)^4*(k+1)^4*(B+1)^3 := by
  have hs := selectSetsRun_weightedContrast_bitWork D hD cs ws hc hw xs hxs
  have hL : 1+(q+1)*(B+1)+1 ≤ 3*(q+1)*(B+1) := by nlinarith
  have hK := (weightedContrastTraceBits_linear p k (1+(q+1)*(B+1))).trans
    (Nat.mul_le_mul_left (weightedWidthConstant p*(k+1)) hL)
  have ho : 2*(p*p*(q+1))+weightedCompareOperations p k ≤
      (2*p*p+2*contrastOperations p+17)*(q+1)*(k+1) := by
    unfold weightedCompareOperations
    nlinarith [Nat.zero_le (q*k*(2*contrastOperations p+14)),Nat.zero_le (2*p*p*k*(q+1))]
  have hl : xs.length-1 ≤ xs.length := Nat.sub_le _ _
  apply hs.trans
  calc
    _ ≤ xs.length*((2*p*p+2*contrastOperations p+17)*(q+1)*(k+1))*
        (256*(weightedWidthConstant p*(k+1)*(3*(q+1)*(B+1)))^3) := by gcongr
    _ = _ := by unfold weightedPathSelectionConstant; ring

end MatroidSpectral
