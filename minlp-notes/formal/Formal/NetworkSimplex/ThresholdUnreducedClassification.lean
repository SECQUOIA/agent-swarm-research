import Formal.NetworkSimplex.ThresholdUnreducedCircuits

namespace NetworkSimplex.Threshold.UnreducedCircuits
open scoped BigOperators

def pivot : Fin 41 → Fin 14 :=
  ![0, 1, 2, 3, 4, 5, 6,
    0, 0, 0, 1, 1, 2, 2, 4, 5, 6, 6, 6, 0, 0, 0, 5, 0, 1, 1, 4, 1, 2, 2, 2, 2, 2,
    2, 2, 2, 3, 4, 4, 6, 9]

theorem pivot_weight : ∀ c, weight c (pivot c) = 1 := by decide +kernel

set_option maxHeartbeats 0 in
-- Expanding the 41 supports requires 574 scalar coordinate checks.
/-- Every real dependence on a displayed support is a scalar multiple of its primitive row. -/
theorem dependence_on_support (c : Fin 41) (a : Fin 14 → ℝ)
    (hs : ∀ i, weight c i = 0 → a i = 0)
    (hc : ∀ j, ∑ i, a i * (normal i j : ℝ) = 0) :
    a = fun i => a (pivot c) * (weight c i : ℝ) := by
  fin_cases c <;>
    (simp only [Fin.forall_fin_succ] at hs hc
     simp [weight, normal, Fin.sum_univ_succ] at hs hc
     ext i
     fin_cases i <;> simp [weight, pivot] <;> simp_all <;> linarith)

end NetworkSimplex.Threshold.UnreducedCircuits
