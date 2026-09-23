import Formal.NetworkSimplex.ProfileHull
import Formal.NetworkSimplex.SimplexEncoding
import Formal.NetworkSimplex.TwoOracle
import Formal.NetworkSimplex.ThreeOracle
import Formal.NetworkSimplex.Circuits

/-! Exact finite criteria for membership in the original sparse-product chain hull. -/

namespace NetworkSimplex.Chain.ReductionData

noncomputable section

variable {L : ℕ}

/-- Two explicit simplex labels: original-domain checks, the zero rows, and five tests. -/
theorem mem_hull_iff_five_tests (D : ReductionData 2 (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    D.graphPoint ∈ convexHull ℝ D.graph ↔
      D.OriginalDomain ∧ 0 ≤ D.grouped (.subset ∅) ∧ D.twoTests := by
  rw [D.mem_hull_iff, ← D.two_tests_iff_fullProfile hc hh]

/-- Three explicit simplex labels: the same domain checks and sixteen tests. -/
theorem mem_hull_iff_sixteen_tests (D : ReductionData 3 (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    D.graphPoint ∈ convexHull ℝ D.graph ↔
      D.OriginalDomain ∧ 0 ≤ D.grouped (.subset ∅) ∧ D.threeBounds.SixteenTests := by
  rw [D.mem_hull_iff, ← D.three_tests_iff_fullProfile hc hh]

/-- The sixteen nonnegative circuit combinations give the same exact hull test. -/
theorem mem_hull_iff_circuit_tests (D : ReductionData 3 (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    D.graphPoint ∈ convexHull ℝ D.graph ↔
      D.OriginalDomain ∧ 0 ≤ D.grouped (.subset ∅) ∧
        ThreeStateCircuits.CircuitTests D.threeBounds := by
  rw [D.mem_hull_iff_sixteen_tests hc hh,
    ThreeStateCircuits.circuit_tests_iff_sixteen_tests]

end
end NetworkSimplex.Chain.ReductionData
