import Formal.DAGSpectral.CoverNormalizationExecution

namespace DAGSpectral
open ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost
open scoped BigOperators
namespace CoverNormalizationExecution

/-- Charge the cached full square of labels, including entries below the diagonal
that are evaluated but not used as DP coordinates. -/
def labelRunWork {r : ℕ} (A : Matrix (Fin r) (Fin r) ℚ) (h : ℚ) (B C : ℕ) : ℕ :=
  traceBitWork (max B C) (labelRun A h).quotients.events + (labelRun A h).floorWork

theorem labelRunWork_eq {r : ℕ} (A : Matrix (Fin r) (Fin r) ℚ)
    (h : ℚ) (B C : ℕ) :
    labelRunWork A h B C = ∑ i, ∑ j, floorLabelBitWork (A i j) h B C := by
  simp [labelRunWork,traceBitWork,labelRun_events,labelRun_floorWork,
    floorLabelBitWork,Finset.sum_add_distrib,List.map_ofFn,Function.comp_def,
    List.sum_ofFn]

theorem labelRunWork_bound {r B C : ℕ} (A : Matrix (Fin r) (Fin r) ℚ)
    (h : ℚ) (hA : ∀ i j, RationalBits (A i j) B) (hh : RationalBits h C) :
    labelRunWork A h B C ≤ r*r*(268*(B+C+1)^3) := by
  rw [labelRunWork_eq]
  calc
    _ ≤ ∑ _i : Fin r, ∑ _j : Fin r, 268*(B+C+1)^3 := by
      exact Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j _ =>
        floorLabelBitWork_le (hA i j) hh
    _ = _ := by simp; ring

end CoverNormalizationExecution
namespace CoverBitCost
open CoverNormalizationExecution

/-- The cache stores the results of all rational arithmetic and floor operations.
The budgets parameterize the schoolbook arithmetic model, not the returned paths. -/
def cacheWork {p r m : ℕ} (R : TrialRun p r m) (K F C : ℕ) : ℕ :=
  traceBitWork K R.prior.events +
    ∑ e : Fin m, (traceBitWork K (R.atoms.get e).events +
      traceBitWork (max F C) (R.labels.get e).quotients.events +
      (R.labels.get e).floorWork)

end CoverBitCost
end DAGSpectral
