import Formal.DAGSpectral.EigenCompareDifferenceTrace
import Formal.DAGSpectral.EigenCompareThresholdTrace
import Formal.DAGSpectral.EigenCompareFinishTrace
import Formal.DAGSpectral.EigenComparePreprocessingTrace

/-! A complete rational execution transcript for exact least-eigenvalue
comparison, including all preprocessing and both adaptive searches. -/
namespace DAGSpectral
open Matrix

def eigenDepthExpr (R δ : ℚ) : ArithmeticExpr :=
  .op .div (.op .mul (.atom 4) (.atom R)) (.atom δ)

@[simp] theorem eigenDepthExpr_eval (R δ : ℚ) : (eigenDepthExpr R δ).eval = 4*R/δ := rfl
@[simp] theorem eigenDepthExpr_operations (R δ : ℚ) : (eigenDepthExpr R δ).operations = 2 := rfl

def compareMinimumEigenvaluesWithTrace {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    Ordering × List ArithmeticEvent :=
  let difference := eigenDifferenceWithTrace A B
  let coefficients := charpolyCoefficientsWithTrace difference.1
  let gap := separationFromCoefficientsWithTrace coefficients.1
  let radius := eigenSearchRadiusWithTrace A B
  let depth := (eigenDepthExpr radius.1 gap.1).run
  let t := depth.1.num.natAbs.size
  let left := dyadicIndexWithTrace (eigenThresholdTestWithTrace A) radius.1 t
  let right := dyadicIndexWithTrace (eigenThresholdTestWithTrace B) radius.1 t
  let finish := eigenFinishWithTrace radius.1 gap.1 left.1 right.1 t
  (finish.1, difference.2 ++ coefficients.2 ++ gap.2 ++ radius.2 ++ depth.2 ++
    left.2 ++ right.2 ++ finish.2)

def eigenComparisonExecutionTrace {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    List ArithmeticEvent :=
  let R := eigenSearchRadius A B
  let δ := eigenComparisonGap A B
  let t := eigenComparisonDepth A B
  (eigenDifferenceWithTrace A B).2 ++
    (charpolyCoefficientsWithTrace (eigenDifferenceFinite A B)).2 ++
    (separationFromCoefficientsWithTrace (eigenDifferenceCoefficients A B)).2 ++
    (eigenSearchRadiusWithTrace A B).2 ++
    (eigenDepthExpr R δ).trace ++
    dyadicExecutionTrace (eigenThresholdTestWithTrace A) R t ++
    dyadicExecutionTrace (eigenThresholdTestWithTrace B) R t ++
    (eigenFinishWithTrace R δ
      (dyadicIndex (eigenThresholdTest A) R t) (dyadicIndex (eigenThresholdTest B) R t) t).2

theorem compareMinimumEigenvaluesWithTrace_eq {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    compareMinimumEigenvaluesWithTrace A B =
      (compareMinimumEigenvalues A B, eigenComparisonExecutionTrace A B) := by
  have hcoef : (charpolyCoefficientsWithTrace (eigenDifferenceFinite A B)).1 =
      eigenDifferenceCoefficients A B := charpolyCoefficientsWithTrace_values _
  have htestA : (fun q => (eigenThresholdTestWithTrace A q).1) = eigenThresholdTest A :=
    funext (eigenThresholdTestWithTrace_value A)
  have htestB : (fun q => (eigenThresholdTestWithTrace B q).1) = eigenThresholdTest B :=
    funext (eigenThresholdTestWithTrace_value B)
  unfold compareMinimumEigenvaluesWithTrace eigenComparisonExecutionTrace
  simp only [eigenDifferenceWithTrace_value, hcoef, separationFromCoefficientsWithTrace_value,
    eigenSearchRadiusWithTrace_value, ArithmeticExpr.run_eq, eigenDepthExpr_eval,
    dyadicIndexWithTrace_eq, htestA, htestB]
  change ( _ , _ ) = ( _ , _ )
  congr 1
  rw [eigenFinishWithTrace_value]
  rfl

theorem compareMinimumEigenvaluesWithTrace_correct {n : ℕ} [Nonempty (Fin n)]
    (A B : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).PosSemidef) (hB : (ratMatrixReal B).PosSemidef) :
    ((compareMinimumEigenvaluesWithTrace A B).1 = .eq ↔
      minimumEigenvalue (ratMatrixReal A) = minimumEigenvalue (ratMatrixReal B)) ∧
    ((compareMinimumEigenvaluesWithTrace A B).1 = .lt ↔
      minimumEigenvalue (ratMatrixReal A) < minimumEigenvalue (ratMatrixReal B)) ∧
    ((compareMinimumEigenvaluesWithTrace A B).1 = .gt ↔
      minimumEigenvalue (ratMatrixReal B) < minimumEigenvalue (ratMatrixReal A)) := by
  rw [compareMinimumEigenvaluesWithTrace_eq]
  exact compareMinimumEigenvalues_correct A B hA hB

end DAGSpectral
