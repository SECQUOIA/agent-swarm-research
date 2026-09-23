import Formal.QuadraticAggregation.ShorAlgebra
import Formal.QuadraticAggregation.ShorDuality
import Formal.QuadraticAggregation.SDPCharacterization

/-! Whole-space characterizations for the actual Shor projection and the two hulls. -/

namespace QuadraticAggregation.System
open Set
variable {n m : ℕ}

/-- Lemma 4: strict feasibility alone makes triviality of the Shor projection
equivalent to absence of a nontrivial convex aggregation certificate. -/
theorem shorProjection_eq_univ_iff_no_certificate (D : System n m)
    (hS : D.feasible.Nonempty) :
    D.shorProjection = Set.univ ↔ ¬ ∃ w, D.Certificate w := by
  constructor
  · rintro hfull ⟨w, hw⟩
    exact hw.shorProjection_ne_univ hfull
  · exact D.shorProjection_eq_univ_of_no_certificate hS

/-- The source's coefficient-cone version of Lemma 4, including zero weights. -/
theorem shorProjection_eq_univ_iff_trivial (D : System n m)
    (hS : D.feasible.Nonempty) :
    D.shorProjection = Set.univ ↔
      ∀ w, (∀ i, 0 ≤ w i) → (D.aggA w).PosSemidef →
        D.aggA w = 0 ∧ D.aggB w = 0 :=
  (D.shorProjection_eq_univ_iff_no_certificate hS).trans D.no_certificate_iff_trivial

/-- Exact finite SDP tests also characterize the Shor projection without HHC. -/
theorem shorProjection_eq_univ_iff_sdpTestsZero (D : System n m)
    (hS : D.feasible.Nonempty) :
    D.shorProjection = Set.univ ↔ D.SDPTestsZero :=
  (D.shorProjection_eq_univ_iff_no_certificate hS).trans D.sdpTestsZero_iff_no_certificate.symm

/-- Both hulls and the actual Shor projection fill the whole space together
under asymptotic hyperplane convexity and strict feasibility. -/
theorem shor_and_hulls_eq_univ (D : System n m)
    (hS : D.feasible.Nonempty) (hHC : D.AsymptoticHC) :
    (D.shorProjection = Set.univ ↔ convexHull ℝ D.feasible = Set.univ) ∧
    (D.shorProjection = Set.univ ↔ convexHull ℝ D.closedFeasible = Set.univ) :=
  ⟨D.shorProjection_eq_univ_iff hS hHC, D.shorProjection_eq_univ_iff_closed hS hHC⟩

/-- The original HHC specialization of the strict and closed hull consequences. -/
theorem shor_and_hulls_eq_univ_of_hhc (D : System n m)
    (hS : D.feasible.Nonempty) (hHC : D.HHC) :
    (D.shorProjection = Set.univ ↔ convexHull ℝ D.feasible = Set.univ) ∧
    (D.shorProjection = Set.univ ↔ convexHull ℝ D.closedFeasible = Set.univ) :=
  D.shor_and_hulls_eq_univ hS hHC.asymptoticHC

end QuadraticAggregation.System
