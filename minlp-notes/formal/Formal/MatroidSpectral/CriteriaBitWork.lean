import Formal.MatroidSpectral.CriteriaControl

/-! Full counted selector bounds. In addition to exact rational arithmetic,
these include candidate identifier materialization and finite scan control. -/
namespace MatroidSpectral
open Matrix DAGSpectral DAGSpectral.NormalizationTrials ReciprocalAnchor
variable {p m M : ℕ}

def selectionWorkBound (p m q n operations width : ℕ) : ℕ :=
  2+n*(2*materializeSetWork m+(2*(p*p*(q+1))+operations)*(256*(width+1)^3)+1+(m+n+2)^2)

theorem selectSetsBitRun_D_work (D : FactorData p m M) {B q : ℕ}
    (hD : ∀ o, MatrixBits (D.atom o) B) (xs : List (Finset (Fin m)))
    (hxs : ∀ S ∈ xs, S.card ≤ q) :
    let K := arithmeticWidth (2*determinantOperations p+1) (1 + (q+1)*(B+1))
    (selectSetsBitRun D determinantLERun K xs).2 ≤
      selectionWorkBound p m q xs.length (2*determinantOperations p+1) K := by
  apply selectSetsBitRun_work D hD determinantLERun
  · exact (arithmeticWidth_zero _).symm.le.trans (arithmeticWidth_mono (Nat.zero_le _))
  · intro A hA T hT
    exact determinantLERun_bounds (by omega) hA hT
  · exact hxs

theorem selectSetsBitRun_E_work (D : FactorData p m M) {B q : ℕ}
    (hD : ∀ o, MatrixBits (D.atom o) B) (xs : List (Finset (Fin m)))
    (hxs : ∀ S ∈ xs, S.card ≤ q) :
    let L := 1 + (q+1)*(B+1)
    let K := eigenExecutionWidth p L
    (selectSetsBitRun D minimumEigenvalueLERun K xs).2 ≤
      selectionWorkBound p m q xs.length (eigenSelectorOperations p L) K := by
  apply selectSetsBitRun_work D hD minimumEigenvalueLERun
  · exact inputBits_le_eigenExecutionWidth _ _
  · intro A hA T hT
    exact minimumEigenvalueLERun_bounds (by omega) hA hT
  · exact hxs

theorem selectSetsBitRun_A_work (D : FactorData p m M) {B q : ℕ}
    (hD : ∀ o, MatrixBits (D.atom o) B) (xs : List (Finset (Fin m)))
    (hxs : ∀ S ∈ xs, S.card ≤ q) :
    let K := arithmeticWidth (inverseTraceCompareOperations p) (1 + (q+1)*(B+1))
    (selectSetsBitRun D (fun A B => inverseTraceCostLERun B A) K xs).2 ≤
      selectionWorkBound p m q xs.length (inverseTraceCompareOperations p) K := by
  apply selectSetsBitRun_work D hD (fun A B => inverseTraceCostLERun B A)
  · exact (arithmeticWidth_zero _).symm.le.trans (arithmeticWidth_mono (Nat.zero_le _))
  · intro A hA T hT
    exact inverseTraceCostLERun_bounds (by omega) hT hA
  · exact hxs

theorem selectSetsBitRun_contrast_work (D : FactorData p m M) {B q : ℕ}
    (hD : ∀ o, MatrixBits (D.atom o) B) (c : Fin p → ℚ)
    (hc : ∀ i, RationalBits (c i) B) (xs : List (Finset (Fin m)))
    (hxs : ∀ S ∈ xs, S.card ≤ q) :
    let K := contrastTraceBits p (1 + (q+1)*(B+1))
    (selectSetsBitRun D (fun A B => contrastCostLERun B A c) K xs).2 ≤
      selectionWorkBound p m q xs.length (contrastComparisonOperations p) K := by
  apply selectSetsBitRun_work D hD (fun A B => contrastCostLERun B A c)
  · exact inputBits_le_contrastTraceBits _ _
  · intro A hA T hT
    exact contrastCostLERun_bounds (by omega) hT hA
      (fun i => rationalBits_mono (hc i) (by nlinarith))
  · exact hxs

theorem selectSetsBitRun_weightedContrast_work (D : FactorData p m M) {k B q : ℕ}
    (hD : ∀ o, MatrixBits (D.atom o) B) (cs : Fin k → Fin p → ℚ)
    (ws : Fin k → ℚ) (hc : ∀ i j, RationalBits (cs i j) B)
    (hw : ∀ i, RationalBits (ws i) B) (xs : List (Finset (Fin m)))
    (hxs : ∀ S ∈ xs, S.card ≤ q) :
    let K := weightedContrastTraceBits p k (1 + (q+1)*(B+1))
    (selectSetsBitRun D (fun A B => weightedContrastCostLERun B A cs ws) K xs).2 ≤
      selectionWorkBound p m q xs.length (weightedCompareOperations p k) K := by
  have hBL : B ≤ 1 + (q+1)*(B+1) := by nlinarith
  apply selectSetsBitRun_work D hD (fun A B => weightedContrastCostLERun B A cs ws)
  · unfold weightedContrastTraceBits weightedContrastInputBits
    omega
  · intro A hA T hT
    exact weightedContrastCostLERun_bounds (by omega) hT hA
      (fun i j => rationalBits_mono (hc i j) hBL)
      (fun i => rationalBits_mono (hw i) hBL)
  · exact hxs

end MatroidSpectral
