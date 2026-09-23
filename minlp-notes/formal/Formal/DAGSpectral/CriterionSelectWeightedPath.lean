import Formal.DAGSpectral.CriterionSelectWeightedScan
import Formal.DAGSpectral.CriterionSelectPath

namespace DAGSpectral
open ReciprocalAnchor

@[simp] theorem selectPathsRun_weightedContrast {p m k : ℕ}
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (cs : Fin k → Fin p → ℚ) (ws : Fin k → ℚ) (xs : List (List (Fin m))) :
    (selectPathsRun Q0 Q (fun a b => weightedContrastCostLERun b a cs ws) xs).1 =
      selectWeightedContrast (rationalPathInformation Q0 Q) cs ws xs := by
  simp only [selectPathsRun_result,weightedContrastCostLERun_value,selectWeightedContrast]

theorem selectPathsRun_weightedContrast_bitWork {p m k B N : ℕ}
    {Q0 : Matrix (Fin p) (Fin p) ℚ} {Q : Fin m → Matrix (Fin p) (Fin p) ℚ}
    (h0 : MatrixBits Q0 B) (hQ : ∀ e, MatrixBits (Q e) B)
    (cs : Fin k → Fin p → ℚ) (ws : Fin k → ℚ)
    (hc : ∀ i j, RationalBits (cs i j) B) (hw : ∀ i, RationalBits (ws i) B)
    (xs : List (List (Fin m))) (hxs : ∀ a ∈ xs, a.length ≤ N) :
    let K := weightedContrastTraceBits p k (1 + (N + 1) * (B + 1))
    traceBitWork K
      (selectPathsRun Q0 Q (fun a b => weightedContrastCostLERun b a cs ws) xs).2 ≤
      (xs.length-1)*(2*(p*p*(N+1))+weightedCompareOperations p k)*(256*(K+1)^3) := by
  have hBL : B ≤ 1 + (N+1)*(B+1) := by nlinarith
  apply selectPathsRun_bitWork h0 hQ (fun a b => weightedContrastCostLERun b a cs ws)
  · unfold weightedContrastTraceBits weightedContrastInputBits
    omega
  · intro A hA D hD
    exact weightedContrastCostLERun_bounds (by omega) hD hA
      (fun i j => rationalBits_mono (hc i j) hBL)
      (fun i => rationalBits_mono (hw i) hBL)
  · exact hxs

def weightedPathSelectionConstant (p : ℕ) : ℕ :=
  (2*p*p+2*contrastOperations p+17)*256*(3*weightedWidthConstant p)^3

/-- The full path-matrix evaluation and weighted candidate scan are polynomial
in path length, candidate count, contrast count, and rational input bit width. -/
theorem selectPathsRun_weightedContrast_polynomial_bitWork {p m k B N : ℕ}
    {Q0 : Matrix (Fin p) (Fin p) ℚ} {Q : Fin m → Matrix (Fin p) (Fin p) ℚ}
    (h0 : MatrixBits Q0 B) (hQ : ∀ e, MatrixBits (Q e) B)
    (cs : Fin k → Fin p → ℚ) (ws : Fin k → ℚ)
    (hc : ∀ i j, RationalBits (cs i j) B) (hw : ∀ i, RationalBits (ws i) B)
    (xs : List (List (Fin m))) (hxs : ∀ a ∈ xs, a.length ≤ N) :
    traceBitWork (weightedContrastTraceBits p k (1+(N+1)*(B+1)))
      (selectPathsRun Q0 Q (fun a b => weightedContrastCostLERun b a cs ws) xs).2 ≤
      weightedPathSelectionConstant p*xs.length*(N+1)^4*(k+1)^4*(B+1)^3 := by
  have hs := selectPathsRun_weightedContrast_bitWork h0 hQ cs ws hc hw xs hxs
  have hL : 1+(N+1)*(B+1)+1 ≤ 3*(N+1)*(B+1) := by nlinarith
  have hK := (weightedContrastTraceBits_linear p k (1+(N+1)*(B+1))).trans
    (Nat.mul_le_mul_left (weightedWidthConstant p*(k+1)) hL)
  have ho : 2*(p*p*(N+1))+weightedCompareOperations p k ≤
      (2*p*p+2*contrastOperations p+17)*(N+1)*(k+1) := by
    unfold weightedCompareOperations
    nlinarith [Nat.zero_le (N*k*(2*contrastOperations p+14)),Nat.zero_le (2*p*p*k*(N+1))]
  have hl : xs.length-1 ≤ xs.length := Nat.sub_le _ _
  apply hs.trans
  calc
    _ ≤ xs.length*((2*p*p+2*contrastOperations p+17)*(N+1)*(k+1))*
        (256*(weightedWidthConstant p*(k+1)*(3*(N+1)*(B+1)))^3) := by gcongr
    _ = _ := by unfold weightedPathSelectionConstant; ring

end DAGSpectral
