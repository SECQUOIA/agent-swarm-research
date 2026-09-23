import Formal.InfiniteAggregation.HullClosure
import Formal.InfiniteAggregation.HullCore
import Formal.InfiniteAggregation.HullCone

/-! Exact closure and the convex hull of the original weak system. -/

open Set

noncomputable section

namespace InfiniteAggregation

variable {r : ℕ}

theorem closure_convexHull_feasible_eq_closedRegion (hr : 2 ≤ r) :
    closure (convexHull ℝ (feasible r)) = closedRegion r := by
  rw [Subset.antisymm convexHull_subset_hullRegion (hullRegion_subset_convexHull hr)]
  exact closure_hullRegion_eq_closedRegion

theorem closedRegion_convex_from_hull (hr : 2 ≤ r) : Convex ℝ (closedRegion r) := by
  rw [← closure_convexHull_feasible_eq_closedRegion hr]
  exact (convex_convexHull ℝ (feasible r)).closure

theorem hullRegion_subset_weakSegments (hr : 2 ≤ r) : hullRegion r ⊆ weakSegments r := by
  intro x hx
  obtain ⟨y, hy, z, hz, a, b, ha, hb, hab, hcomb⟩ :=
    two_point_decomposition_of_strict_hull_inequalities hr x hx.1 hx.2.1 hx.2.2
  refine ⟨(a, y, z), ⟨⟨ha, by linarith⟩,
    feasible_subset_weakFeasible hy, feasible_subset_weakFeasible hz⟩, ?_⟩
  change a • y + (1 - a) • z = x
  have hba : 1 - a = b := by linarith
  rw [hba]
  exact hcomb

theorem closedRegion_subset_weakSegments (hr : 2 ≤ r) :
    closedRegion r ⊆ weakSegments r := by
  rw [← closure_hullRegion_eq_closedRegion]
  exact closure_minimal (hullRegion_subset_weakSegments hr) isCompact_weakSegments.isClosed

/-- The original weak system has the closed region as its ordinary convex hull. -/
theorem convexHull_weakFeasible_eq_closedRegion (hr : 2 ≤ r) :
    convexHull ℝ (weakFeasible r) = closedRegion r := by
  apply Subset.antisymm
  · exact convexHull_min weakFeasible_subset_closedRegion (closedRegion_convex_from_hull hr)
  · exact (closedRegion_subset_weakSegments hr).trans weakSegments_subset_convexHull

theorem convexHull_weakFeasible_eq_closure_convexHull_feasible (hr : 2 ≤ r) :
    convexHull ℝ (weakFeasible r) = closure (convexHull ℝ (feasible r)) := by
  rw [convexHull_weakFeasible_eq_closedRegion hr,
    closure_convexHull_feasible_eq_closedRegion hr]

theorem isCompact_convexHull_weakFeasible (hr : 2 ≤ r) :
    IsCompact (convexHull ℝ (weakFeasible r)) := by
  rw [convexHull_weakFeasible_eq_closedRegion hr]
  exact isCompact_closedRegion

end InfiniteAggregation
