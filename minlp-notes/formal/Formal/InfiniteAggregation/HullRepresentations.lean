import Formal.InfiniteAggregation.Hull
import Formal.InfiniteAggregation.HullClosedConsequences
import Formal.InfiniteAggregation.Lift
import Formal.InfiniteAggregation.Consequences

/-! Exact finite lifts and complete good-aggregation descriptions of both hulls. -/

open Set

namespace InfiniteAggregation

theorem mem_convexHull_iff_strict_lift {r : ℕ} (hr : 2 ≤ r) (x : Var r) :
    x ∈ convexHull ℝ (feasible r) ↔
      ∃ σ : ℝ, 1 / 2 < σ ∧ (hullLift x σ).PosDef := by
  rw [convexHull_feasible_eq_hullRegion hr]
  exact mem_hullRegion_iff_lift x

theorem mem_closedHull_iff_lift {r : ℕ} (hr : 2 ≤ r) (x : Var r) :
    x ∈ closure (convexHull ℝ (feasible r)) ↔
      ∃ σ : ℝ, 1 / 2 ≤ σ ∧ (hullLift x σ).PosSemidef := by
  rw [closure_convexHull_feasible_eq_closedRegion hr]
  exact mem_closedRegion_iff_lift x

theorem mem_weakHull_iff_lift {r : ℕ} (hr : 2 ≤ r) (x : Var r) :
    x ∈ convexHull ℝ (weakFeasible r) ↔
      ∃ σ : ℝ, 1 / 2 ≤ σ ∧ (hullLift x σ).PosSemidef := by
  rw [convexHull_weakFeasible_eq_closedRegion hr]
  exact mem_closedRegion_iff_lift x

theorem closedHull_eq_all_good_weak {r : ℕ} (hr : 2 ≤ r) :
    closure (convexHull ℝ (feasible r)) =
      {x | ∀ w : Weight, Good r w → aggregate w x ≤ 0} := by
  apply Subset.antisymm
  · intro x hx w hw
    exact good_closedHull_valid hw hx
  · intro x hx
    rw [closure_convexHull_feasible_eq_closedRegion hr]
    apply goodCone_weak_intersection_subset_closedRegion
    intro w hw hne
    exact hx w ((good_iff_goodCone hr w).2 ⟨hw, hne⟩)

end InfiniteAggregation
