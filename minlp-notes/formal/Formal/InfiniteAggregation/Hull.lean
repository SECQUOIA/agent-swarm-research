import Formal.InfiniteAggregation.HullCore
import Formal.InfiniteAggregation.HullCone

/-! The exact ordinary convex hull, proved by a two-point decomposition. -/

namespace InfiniteAggregation

theorem convexHull_feasible_eq_hullRegion {r : ℕ} (hr : 2 ≤ r) :
    convexHull ℝ (feasible r) = hullRegion r :=
  Set.Subset.antisymm convexHull_subset_hullRegion (hullRegion_subset_convexHull hr)

theorem hullRegion_convex {r : ℕ} (hr : 2 ≤ r) : Convex ℝ (hullRegion r) := by
  rw [← convexHull_feasible_eq_hullRegion hr]
  exact convex_convexHull ℝ _

theorem convexHull_eq_all_good_strict {r : ℕ} (hr : 2 ≤ r) :
    convexHull ℝ (feasible r) = {x | ∀ w : Weight, Good r w → aggregate w x < 0} := by
  apply Set.Subset.antisymm
  · intro x hx w hw
    exact hw.2.2 x hx
  · intro x hx
    apply hullRegion_subset_convexHull hr
    apply goodCone_strict_intersection_subset_hullRegion
    intro w hw hne
    exact hx w ((good_iff_goodCone hr w).2 ⟨hw, hne⟩)

end InfiniteAggregation
