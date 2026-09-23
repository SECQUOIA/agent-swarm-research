import Formal.DAGSpectral.CoverLabelCost

namespace DAGSpectral
open Matrix ReciprocalAnchor
open scoped BigOperators
namespace CoverBitCost
open CoverNormalizationExecution NormalizationBits

/-- Sum the operations that actually constructed the prior, atom, and label
caches. Every atom includes its range and magnitude tests; the labels charge
the full stored square rather than only the upper-triangular DP coordinates. -/
theorem cacheWork_bound {p r m B C : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    {w : Fin r → ℚ} {A : Option (Fin m) → Matrix (Fin p) (Fin p) ℚ} {h : ℚ}
    (hV : MatrixBits V B) (hw : ∀ i, RationalBits (w i) B)
    (hA : ∀ o, MatrixBits (A o) B) (hh : RationalBits h C) :
    cacheWork (trialRun V (actualScales w) A h)
      (atomBudget p r B (6*B+1) B) (transformBudget p r B (6*B+1) B) C ≤
      (m+1)*atomCostCoefficient p r*(B+1)^3 +
        m*r*r*(268*(transformBudget p r B (6*B+1) B+C+1)^3) := by
  let F := transformBudget p r B (6*B+1) B
  let K := atomBudget p r B (6*B+1) B
  have hp := atomRun_bitWork_polynomial hV hw (hA none)
  have ha (e : Fin m) := atomRun_bitWork_polynomial hV hw (hA (some e))
  have hl (e : Fin m) := labelRunWork_bound
    (transformProducer V (actualScales w) (A (some e))) h
    (transform_bits hV (actualScales_bits hw) (hA (some e))) hh
  simp only [cacheWork, trialRun, Vector.get_ofFn, atomRun_normalized, normalizeRun_atom]
  calc
    _ = traceBitWork K (atomRun V (actualScales w) (A none)).events +
        ∑ e : Fin m, (traceBitWork K (atomRun V (actualScales w) (A (some e))).events +
          labelRunWork (transformProducer V (actualScales w) (A (some e))) h F C) := by
      simp only [labelRunWork, Nat.add_assoc, F, K]
    _ ≤ atomCostCoefficient p r*(B+1)^3 + ∑ _e : Fin m,
        (atomCostCoefficient p r*(B+1)^3 + r*r*(268*(F+C+1)^3)) := by
      exact Nat.add_le_add hp (Finset.sum_le_sum fun e _ => Nat.add_le_add (ha e) (hl e))
    _ = _ := by simp; dsimp [F]; ring

end CoverBitCost
end DAGSpectral
