import Formal.QuadraticAggregation.DefinitionsSequence
import Formal.QuadraticAggregation.Hyperplanes

/- Independent review: the source definition and the model definition are equivalent,
and the geometric reductions retain their intended assumptions. -/
open QuadraticAggregation

example {n m : ℕ} (D : System n m) :
    D.AsymptoticHC ↔ D.AsymptoticHCSequence := D.asymptoticHC_iff_sequence

example {n m : ℕ} {D : System n m} (h : D.HHC) : D.AsymptoticHC :=
  h.asymptoticHC

example {n m : ℕ} (D : System n m) {v : Vec n}
    (h : ∀ i, q (D.A i) v < 0) : convexHull ℝ D.feasible = Set.univ :=
  D.convexHull_eq_univ_of_negative_recession h

#print axioms System.asymptoticHC_iff_sequence
#print axioms System.HHC.asymptoticHC
#print axioms System.convexHull_eq_univ_of_negative_recession
#print axioms System.exists_strict_support
#print axioms exists_simplex_separator
#print axioms System.hyperplane_certificate
#print axioms System.sweep_disjoint
#print axioms System.exists_unbounded_certificates
