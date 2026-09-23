import Formal.MatroidSpectral.CriteriaSelection
import Formal.DAGSpectral.CriterionSelectEigenTrace

/-! Executed finite-family selection costs, including construction of both
information matrices at each comparison. Dimension-only constants may be large;
matroid rank and candidate count remain variable. -/
namespace MatroidSpectral
open Matrix DAGSpectral DAGSpectral.NormalizationTrials

variable {p m M : ℕ}

theorem information_eq_sortedInformation (D : FactorData p m M) (S : Finset (Fin m)) :
    information D S = rationalPathInformation (D.atom none) (fun e => D.atom (some e))
      (S.sort (· ≤ ·)) := by
  unfold information rationalPathInformation
  congr 1
  simpa using List.sum_toFinset (fun e => D.atom (some e)) (S.sort_nodup (· ≤ ·))

def selectSetsRun (D : FactorData p m M)
    (compare : Matrix (Fin p) (Fin p) ℚ → Matrix (Fin p) (Fin p) ℚ →
      Bool × List ArithmeticEvent) (xs : List (Finset (Fin m))) :
    Option (Finset (Fin m)) × List ArithmeticEvent :=
  bestByRun (fun S T => pathComparisonRun (D.atom none) (fun e => D.atom (some e))
    compare (S.sort (· ≤ ·)) (T.sort (· ≤ ·))) xs

theorem selectSetsRun_result (D : FactorData p m M) (compare)
    (xs : List (Finset (Fin m))) :
    (selectSetsRun D compare xs).1 =
      bestBy (fun S T => (compare (information D S) (information D T)).1) xs := by
  simp only [selectSetsRun,bestByRun_result,pathComparisonRun_value,
    ← information_eq_sortedInformation]

theorem selectSetsRun_bitWork (D : FactorData p m M) {B q C K : ℕ}
    (hD : ∀ o, MatrixBits (D.atom o) B) (compare)
    (hK : 1 + (q + 1) * (B + 1) ≤ K)
    (hcompare : ∀ A, MatrixBits A (1 + (q + 1) * (B + 1)) →
      ∀ T, MatrixBits T (1 + (q + 1) * (B + 1)) →
      (compare A T).2.length ≤ C ∧ ∀ e ∈ (compare A T).2, eventBits K e)
    (xs : List (Finset (Fin m))) (hxs : ∀ S ∈ xs, S.card ≤ q) :
    traceBitWork K (selectSetsRun D compare xs).2 ≤
      (xs.length-1)*(2*(p*p*(q+1))+C)*(256*(K+1)^3) := by
  apply bestByRun_bitWork _ (fun S => S.card ≤ q) _ xs hxs
  intro S hS T hT
  exact pathComparisonRun_bounds (hD none) (fun e => hD (some e)) compare hK hcompare
    (S.sort (· ≤ ·)) (T.sort (· ≤ ·)) (by simpa using hS) (by simpa using hT)

@[simp] theorem selectSetsRun_D (D : FactorData p m M)
    (xs : List (Finset (Fin m))) :
    (selectSetsRun D determinantLERun xs).1 = selectDeterminant (information D) xs := by
  simp only [selectSetsRun_result,determinantLERun_result,selectDeterminant]

@[simp] theorem selectSetsRun_E (D : FactorData p m M)
    (xs : List (Finset (Fin m))) :
    (selectSetsRun D minimumEigenvalueLERun xs).1 =
      selectMinimumEigenvalue (information D) xs := by
  simp only [selectSetsRun_result,minimumEigenvalueLERun_result,selectMinimumEigenvalue]

@[simp] theorem selectSetsRun_A (D : FactorData p m M)
    (xs : List (Finset (Fin m))) :
    (selectSetsRun D (fun A B => inverseTraceCostLERun B A) xs).1 =
      selectInverseTrace (information D) xs := by
  simp only [selectSetsRun_result,inverseTraceCostLERun_result,selectInverseTrace]

theorem selectSetsRun_D_bitWork (D : FactorData p m M) {B q : ℕ}
    (hD : ∀ o, MatrixBits (D.atom o) B) (xs : List (Finset (Fin m)))
    (hxs : ∀ S ∈ xs, S.card ≤ q) :
    let K := arithmeticWidth (2*determinantOperations p+1) (1 + (q + 1) * (B + 1))
    traceBitWork K (selectSetsRun D determinantLERun xs).2 ≤
      (xs.length-1)*(2*(p*p*(q+1))+(2*determinantOperations p+1))*(256*(K+1)^3) := by
  apply selectSetsRun_bitWork D hD determinantLERun
  · exact (arithmeticWidth_zero _).symm.le.trans (arithmeticWidth_mono (Nat.zero_le _))
  · intro A hA T hT
    exact determinantLERun_bounds (by omega) hA hT
  · exact hxs

theorem selectSetsRun_E_bitWork (D : FactorData p m M) {B q : ℕ}
    (hD : ∀ o, MatrixBits (D.atom o) B) (xs : List (Finset (Fin m)))
    (hxs : ∀ S ∈ xs, S.card ≤ q) :
    let L := 1 + (q + 1) * (B + 1)
    let K := eigenExecutionWidth p L
    traceBitWork K (selectSetsRun D minimumEigenvalueLERun xs).2 ≤
      (xs.length-1)*(2*(p*p*(q+1))+eigenSelectorOperations p L)*(256*(K+1)^3) := by
  apply selectSetsRun_bitWork D hD minimumEigenvalueLERun
  · exact inputBits_le_eigenExecutionWidth _ _
  · intro A hA T hT
    exact minimumEigenvalueLERun_bounds (by omega) hA hT
  · exact hxs

theorem selectSetsRun_A_bitWork (D : FactorData p m M) {B q : ℕ}
    (hD : ∀ o, MatrixBits (D.atom o) B) (xs : List (Finset (Fin m)))
    (hxs : ∀ S ∈ xs, S.card ≤ q) :
    let K := arithmeticWidth (inverseTraceCompareOperations p) (1 + (q + 1) * (B + 1))
    traceBitWork K (selectSetsRun D (fun A B => inverseTraceCostLERun B A) xs).2 ≤
      (xs.length-1)*(2*(p*p*(q+1))+inverseTraceCompareOperations p)*(256*(K+1)^3) := by
  apply selectSetsRun_bitWork D hD (fun A B => inverseTraceCostLERun B A)
  · exact (arithmeticWidth_zero _).symm.le.trans (arithmeticWidth_mono (Nat.zero_le _))
  · intro A hA T hT
    exact inverseTraceCostLERun_bounds (by omega) hT hA
  · exact hxs

end MatroidSpectral
