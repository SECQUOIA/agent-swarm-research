import Formal.QuadraticAggregation.ShorModel
import Formal.QuadraticAggregation.ClosedSystem

/-!
# Convex aggregation bounds the Shor projection

Every PSD aggregation yields a valid closed quadratic inequality for the actual
Shor projection. Nonconstant aggregations therefore make that projection proper.
-/

open scoped BigOperators Matrix
open Matrix Set

namespace QuadraticAggregation.System

variable {n m : ℕ}

/-- A convex aggregate remains valid after the semidefinite lifting. -/
theorem shorProjection_aggregate_nonpos (D : System n m) {w : Vec m}
    (hw : ∀ i, 0 ≤ w i) (hA : (D.aggA w).PosSemidef)
    {x : Vec n} (hx : x ∈ D.shorProjection) :
    q (D.aggA w) x + 2 * (D.aggB w ⬝ᵥ x) + D.aggC w ≤ 0 := by
  obtain ⟨Y, hY, hi⟩ := hx
  have hsum : ∑ i, w i * (D.eval x i + tracePair (D.A i) Y) ≤ 0 :=
    Finset.sum_nonpos fun i _ => mul_nonpos_of_nonneg_of_nonpos (hw i) (hi i)
  simp only [mul_add, Finset.sum_add_distrib, D.agg_eval, ← D.tracePair_aggA] at hsum
  have hnonneg := tracePair_nonneg hA hY
  linarith

/-- A nonconstant PSD aggregation excludes a full Shor projection, without
any hidden-convexity or feasibility assumption. -/
theorem Certificate.shorProjection_ne_univ {D : System n m} {w : Vec m}
    (hw : D.Certificate w) : D.shorProjection ≠ Set.univ := by
  intro hall
  apply quadratic_nonpos_ne_univ _ _ _ hw.2.2.1 hw.2.2.2
  exact Set.eq_univ_of_forall fun x =>
    D.shorProjection_aggregate_nonpos hw.1 hw.2.2.1 (hall.symm ▸ Set.mem_univ x)

/-- A full strict hull always forces a full Shor projection. -/
theorem shorProjection_eq_univ_of_convexHull_eq_univ (D : System n m)
    (hhull : convexHull ℝ D.feasible = Set.univ) : D.shorProjection = Set.univ := by
  have hsub := convexHull_min D.feasible_subset_shorProjection D.convex_shorProjection
  exact Set.eq_univ_of_forall fun x => hsub (hhull.symm ▸ Set.mem_univ x)

/-- Corollary 4 for the strict hull. -/
theorem shorProjection_eq_univ_iff (D : System n m)
    (hS : D.feasible.Nonempty) (hHC : D.AsymptoticHC) :
    D.shorProjection = Set.univ ↔ convexHull ℝ D.feasible = Set.univ := by
  refine ⟨fun hfull => ?_, D.shorProjection_eq_univ_of_convexHull_eq_univ⟩
  by_contra hproper
  obtain ⟨w, hw⟩ := D.exists_certificate_of_proper hS hHC hproper
  exact hw.shorProjection_ne_univ hfull

/-- The same equivalence for the closed feasible hull. -/
theorem shorProjection_eq_univ_iff_closed (D : System n m)
    (hS : D.feasible.Nonempty) (hHC : D.AsymptoticHC) :
    D.shorProjection = Set.univ ↔ convexHull ℝ D.closedFeasible = Set.univ := by
  have h := D.strict_proper_hull_iff_closed hS hHC
  have heq : convexHull ℝ D.feasible = Set.univ ↔
      convexHull ℝ D.closedFeasible = Set.univ := by
    simpa only [not_not] using not_congr h
  exact (D.shorProjection_eq_univ_iff hS hHC).trans heq

end QuadraticAggregation.System
