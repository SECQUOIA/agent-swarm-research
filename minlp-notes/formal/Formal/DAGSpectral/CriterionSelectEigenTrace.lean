import Formal.DAGSpectral.CriterionSelectPath
import Formal.DAGSpectral.EigenCompareExecutionCost

namespace DAGSpectral
open Matrix

def minimumEigenvalueLERun {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    Bool × List ArithmeticEvent :=
  let r := compareMinimumEigenvaluesWithTrace A B
  (r.1 != Ordering.gt,r.2)

@[simp] theorem minimumEigenvalueLERun_result {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    (minimumEigenvalueLERun A B).1 = minimumEigenvalueLE A B := by
  simp [minimumEigenvalueLERun,compareMinimumEigenvaluesWithTrace_eq,minimumEigenvalueLE]

def eigenSelectorOperations (n B : ℕ) : ℕ :=
  eigenExecutionOperationConstant n*(eigenDepthLinear n*(B+1)+1)^2

theorem minimumEigenvalueLERun_bounds {n B : ℕ} (hB : 0 < B)
    {A C : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) (hC : MatrixBits C B) :
    (minimumEigenvalueLERun A C).2.length ≤ eigenSelectorOperations n B ∧
    ∀ e ∈ (minimumEigenvalueLERun A C).2, eventBits (eigenExecutionWidth n B) e := by
  simp only [minimumEigenvalueLERun,compareMinimumEigenvaluesWithTrace_eq]
  refine ⟨?_,eigenComparisonExecutionTrace_bits hB hA hC⟩
  exact (eigenComparisonExecutionTrace_length A C).trans
    ((eigenExecutionOperationBound_quadratic n _).trans
      (Nat.mul_le_mul_left _ (Nat.pow_le_pow_left
        (Nat.add_le_add_right (eigenComparisonDepth_linear hA hC) 1) 2)))

theorem inputBits_le_eigenExecutionWidth (n B : ℕ) : B ≤ eigenExecutionWidth n B := by
  have h : B ≤ eigenExecutionBase n B := by unfold eigenExecutionBase; omega
  exact h.trans ((arithmeticWidth_zero _).symm.le.trans
    (arithmeticWidth_mono (Nat.zero_le _)))

@[simp] theorem selectPathsRun_eigenvalue {p m : ℕ}
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (xs : List (List (Fin m))) :
    (selectPathsRun Q0 Q minimumEigenvalueLERun xs).1 =
      selectMinimumEigenvalue (rationalPathInformation Q0 Q) xs := by
  simp only [selectPathsRun_result,minimumEigenvalueLERun_result,selectMinimumEigenvalue]

/-- Exact E-selection includes path construction and every rational operation
of the certified algebraic eigenvalue comparison. -/
theorem selectPathsRun_eigenvalue_bitWork {p m B N : ℕ}
    {Q0 : Matrix (Fin p) (Fin p) ℚ} {Q : Fin m → Matrix (Fin p) (Fin p) ℚ}
    (h0 : MatrixBits Q0 B) (hQ : ∀ e, MatrixBits (Q e) B)
    (xs : List (List (Fin m))) (hxs : ∀ a ∈ xs, a.length ≤ N) :
    let L := 1 + (N + 1) * (B + 1)
    let K := eigenExecutionWidth p L
    traceBitWork K (selectPathsRun Q0 Q minimumEigenvalueLERun xs).2 ≤
      (xs.length-1)*(2*(p*p*(N+1))+eigenSelectorOperations p L)*(256*(K+1)^3) := by
  apply selectPathsRun_bitWork h0 hQ minimumEigenvalueLERun
  · exact inputBits_le_eigenExecutionWidth _ _
  · intro A hA D hD
    exact minimumEigenvalueLERun_bounds (by omega) hA hD
  · exact hxs

end DAGSpectral
