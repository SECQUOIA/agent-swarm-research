import Formal.QuadraticAggregation.Consequences

open QuadraticAggregation
open scoped Matrix

-- The pure linear boundary case requires no nonzero quadratic part.
example {n : ℕ} (b : Vec n) (c : ℝ) (hb : b ≠ 0) :
    ∀ r : ℝ, ∃ x, r < 2 * (b ⬝ᵥ x) + c := by
  simpa using quadratic_unbounded_above (0 : Mat n) b c Matrix.PosSemidef.zero (Or.inr hb)

-- The converse about the actual Shor projection has no hidden-convexity premise.
example {n m : ℕ} (D : System n m) (hS : D.feasible.Nonempty) :
    D.shorProjection = Set.univ ↔ ¬ ∃ w, D.Certificate w :=
  D.shorProjection_eq_univ_iff_no_certificate hS

#print axioms quadratic_nonpos_convex
#print axioms quadratic_nonpos_isClosed
#print axioms quadratic_unbounded_above
#print axioms System.closed_convexHull_subset_aggregate
#print axioms System.Certificate.closed_convexHull_ne_univ
#print axioms System.closed_proper_hull_iff_certificate
#print axioms System.closed_hull_eq_univ_iff_strict
#print axioms System.closed_hull_eq_univ_iff_strict_of_hhc
#print axioms System.shorProjection_eq_univ_iff_no_certificate
#print axioms System.shor_and_hulls_eq_univ
#print axioms System.shor_and_hulls_eq_univ_of_hhc
