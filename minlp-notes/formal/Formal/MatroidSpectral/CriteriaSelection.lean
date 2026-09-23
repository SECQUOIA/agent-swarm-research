import Formal.MatroidSpectral.Criteria
import Formal.DAGSpectral.CriterionSelectMatrix
import Formal.DAGSpectral.CriterionSelectContrast
import Formal.DAGSpectral.CriterionSelectWeighted
import Formal.DAGSpectral.EigenCompareExecutionCost
import Formal.DAGSpectral.PathInformationBits

/-! Actual finite-list selection on rational information matrices. All selected
objects are members of the returned candidate list. Eigenvalue comparisons use
the existing exact rational characteristic-polynomial and bisection algorithm,
including equal and repeated eigenvalues. -/
namespace MatroidSpectral
open Matrix DAGSpectral DAGSpectral.NormalizationTrials

variable {p m M : ℕ} (D : FactorData p m M)
  {F : Finset (Finset (Fin m))} {xs : List (Finset (Fin m))} {η ε : ℝ}

theorem select_D_guarantee
    (h : IsRelativeCover (ε / p) (fun S => ratMatrixReal (information D S)) F xs.toFinset)
    (hp : 0 < p) (hε : 0 ≤ ε) (hε1 : ε ≤ 1) {B : Finset (Fin m)}
    (hB : selectDeterminant (information D) xs = some B) :
    B ∈ F ∧ ∀ S ∈ F, (1-ε) * (ratMatrixReal (information D S)).det ≤
      (ratMatrixReal (information D B)).det :=
  h.selectDeterminant_guarantee (fun S _ => information_real_psd D S) hp hε hε1 hB

theorem select_E_guarantee [NeZero p]
    (h : IsRelativeCover ε (fun S => ratMatrixReal (information D S)) F xs.toFinset)
    (hε1 : ε ≤ 1) {B : Finset (Fin m)}
    (hB : selectMinimumEigenvalue (information D) xs = some B) :
    B ∈ F ∧ ∀ S ∈ F, (1-ε) * minimumEigenvalue (ratMatrixReal (information D S)) ≤
      minimumEigenvalue (ratMatrixReal (information D B)) :=
  h.selectMinimumEigenvalue_guarantee (fun S _ => information_real_psd D S) hε1 hB

theorem select_A_guarantee
    (h : IsRelativeCover (ε / (1 + ε))
      (fun S => ratMatrixReal (information D S)) F xs.toFinset)
    (hε : 0 ≤ ε) {B : Finset (Fin m)}
    (hB : selectInverseTrace (information D) xs = some B) :
    B ∈ F ∧ ∀ S ∈ F, inverseTraceCost (ratMatrixReal (information D B)) ≤
      ENNReal.ofReal (1 + ε) * inverseTraceCost (ratMatrixReal (information D S)) := by
  have hd : 0 < 1 + ε := by linarith
  have he : (1 - ε / (1 + ε))⁻¹ = 1 + ε := by field_simp; ring
  simpa only [he] using h.selectInverseTrace_guarantee
    (fun S _ => information_real_psd D S) (div_nonneg hε hd.le)
    ((div_lt_one hd).mpr (by linarith)) hB

theorem select_contrast_guarantee
    (h : IsRelativeCover η (fun S => ratMatrixReal (information D S)) F xs.toFinset)
    (hη0 : 0 ≤ η) (hη1 : η < 1) (c : Fin p → ℚ) {B : Finset (Fin m)}
    (hB : selectContrast (information D) c xs = some B) :
    B ∈ F ∧ ∀ S ∈ F, contrastCost (ratMatrixReal (information D B)) (fun i => (c i : ℝ)) ≤
      ENNReal.ofReal ((1-η)⁻¹) *
        contrastCost (ratMatrixReal (information D S)) (fun i => (c i : ℝ)) :=
  h.selectContrast_guarantee (fun S _ => information_real_psd D S) hη0 hη1 c hB

theorem select_weightedContrast_guarantee {k : ℕ}
    (h : IsRelativeCover η (fun S => ratMatrixReal (information D S)) F xs.toFinset)
    (hη0 : 0 ≤ η) (hη1 : η < 1) (cs : Fin k → Fin p → ℚ)
    (ws : Fin k → ℚ) (hw : ∀ i, 0 ≤ ws i) {B : Finset (Fin m)}
    (hB : selectWeightedContrast (information D) cs ws xs = some B) :
    B ∈ F ∧ ∀ S ∈ F,
      weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ))
        (ratMatrixReal (information D B)) ≤ ENNReal.ofReal ((1-η)⁻¹) *
      weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ))
        (ratMatrixReal (information D S)) :=
  h.selectWeightedContrast_guarantee (fun S _ => information_real_psd D S)
    hη0 hη1 cs ws hw hB

theorem information_eq_rationalPathInformation (S : Finset (Fin m)) :
    information D S = rationalPathInformation (D.atom none) (fun e => D.atom (some e))
      S.toList := by
  simp [information,rationalPathInformation]

/-- The selected matrix entry encoding is polynomial in base size and the
original atom encoding, with no dependence on inverse eigenvalues. -/
theorem information_bits {K q : ℕ} (hD : ∀ o, MatrixBits (D.atom o) K)
    (S : Finset (Fin m)) (hS : S.card ≤ q) :
    MatrixBits (information D S) (1 + (q+1)*(K+1)) := by
  rw [information_eq_rationalPathInformation]
  exact rationalPathInformation_bits (hD none) (fun e => hD (some e)) S.toList
    (by simpa using hS)

/-- Exact E-comparison costs a fixed-dimension constant times the fifth power
of the information-entry bit bound. The traced run is the actual comparator. -/
theorem information_eigenComparison_bitWork {K q : ℕ}
    (hD : ∀ o, MatrixBits (D.atom o) K) (S T : Finset (Fin m))
    (hS : S.card ≤ q) (hT : T.card ≤ q) :
    traceBitWork (eigenExecutionWidth p (1 + (q+1)*(K+1)))
      (compareMinimumEigenvaluesWithTrace (information D S) (information D T)).2 ≤
      eigenComparisonBitConstant p * (2 + (q+1)*(K+1))^5 := by
  simpa only [show 1 + (q+1)*(K+1) + 1 = 2 + (q+1)*(K+1) by omega] using
    compareMinimumEigenvalues_polynomial_bitWork (by omega : 0 < 1 + (q+1)*(K+1))
      (information_bits D hD S hS) (information_bits D hD T hT)

/-- The finite selection performs one comparison per candidate after the first.
This records the actual pairs and remains true for ties. -/
theorem information_selector_comparisons (better : Finset (Fin m) → Finset (Fin m) → Bool)
    (xs : List (Finset (Fin m))) :
    (bestByWithTrace better xs).2.length = xs.length - 1 :=
  bestByWithTrace_length better xs

end MatroidSpectral
