import Formal.DAGSpectral.CriterionSelectContrastTrace
import Formal.DAGSpectral.CriterionSelectPath

namespace DAGSpectral
open Matrix ReciprocalAnchor

lemma inputBits_le_contrastTraceBits (n B : ℕ) : B ≤ contrastTraceBits n B := by
  have h1 := arithmeticWidth_ge (2*n) (arithmeticWidth (pseudoInverseTraceDepth n) B+B+1)
  have h2 := arithmeticWidth_ge (2*n)
    (arithmeticWidth (2*n) (arithmeticWidth (pseudoInverseTraceDepth n) B+B+1))
  unfold contrastTraceBits
  omega

@[simp] theorem selectPathsRun_contrast {p m : ℕ}
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (c : Fin p → ℚ) (xs : List (List (Fin m))) :
    (selectPathsRun Q0 Q (fun a b => contrastCostLERun b a c) xs).1 =
      selectContrast (rationalPathInformation Q0 Q) c xs := by
  simp only [selectPathsRun_result,contrastCostLERun_value,selectContrast]

/-- Original path sums and rational contrast evaluation are both included.
The contrast coordinates use the same original input-width bound. -/
theorem selectPathsRun_contrast_bitWork {p m B N : ℕ}
    {Q0 : Matrix (Fin p) (Fin p) ℚ} {Q : Fin m → Matrix (Fin p) (Fin p) ℚ}
    (h0 : MatrixBits Q0 B) (hQ : ∀ e, MatrixBits (Q e) B)
    (c : Fin p → ℚ) (hc : ∀ i, RationalBits (c i) B)
    (xs : List (List (Fin m))) (hxs : ∀ a ∈ xs, a.length ≤ N) :
    let L := 1 + (N + 1) * (B + 1)
    let K := contrastTraceBits p L
    traceBitWork K (selectPathsRun Q0 Q (fun a b => contrastCostLERun b a c) xs).2 ≤
      (xs.length-1)*(2*(p*p*(N+1))+contrastComparisonOperations p)*(256*(K+1)^3) := by
  apply selectPathsRun_bitWork h0 hQ (fun a b => contrastCostLERun b a c)
  · exact inputBits_le_contrastTraceBits _ _
  · intro A hA D hD
    exact contrastCostLERun_bounds (by omega) hD hA
      (fun i => rationalBits_mono (hc i) (by nlinarith))
  · exact hxs

end DAGSpectral
