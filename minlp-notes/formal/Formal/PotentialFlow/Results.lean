import Formal.PotentialFlow.Certificate
import Formal.PotentialFlow.RationalBridge

namespace PotentialFlow.RationalNetwork

variable {n m : ℕ} (G : RationalNetwork n m)

/-- Every accepted exact certificate encloses the unique physical minimizing flow.
No optimizer result or pre-existing physical solution is a hypothesis. -/
theorem accepted_sound {hm : 0 < m} {b : Fin n → ℚ}
    {C : RationalCertificate n m} (h : G.Accepted hm b C) :
    ∃ x : Fin m → ℝ,
      G.toReal.Feasible (fun v => (b v : ℝ)) x ∧
      (∀ z, G.toReal.Feasible (fun v => (b v : ℝ)) z →
        G.toReal.energy x ≤ G.toReal.energy z) ∧
      (∀ z, G.toReal.Feasible (fun v => (b v : ℝ)) z →
        (∀ w, G.toReal.Feasible (fun v => (b v : ℝ)) w →
          G.toReal.energy z ≤ G.toReal.energy w) → z = x) ∧
      (∃ p, G.toReal.drops p = fun e =>
        edgeLaw (G.toReal.positive e) (G.toReal.negative e) (x e)) ∧
      (0 ≤ G.toReal.energy (fun e => (C.flow e : ℝ)) - G.toReal.energy x ∧
        G.toReal.energy (fun e => (C.flow e : ℝ)) - G.toReal.energy x ≤ (C.gap : ℝ)) ∧
      (∀ e, |(C.flow e : ℝ) - x e| ≤ (C.radius : ℝ)) ∧
      (∀ e, edgeLaw (G.toReal.positive e) (G.toReal.negative e)
          ((C.flow e : ℝ) - (C.radius : ℝ)) ≤
          edgeLaw (G.toReal.positive e) (G.toReal.negative e) (x e) ∧
        edgeLaw (G.toReal.positive e) (G.toReal.negative e) (x e) ≤
          edgeLaw (G.toReal.positive e) (G.toReal.negative e)
            ((C.flow e : ℝ) + (C.radius : ℝ))) := by
  have hc := G.accepted_positive h
  have hy := G.accepted_feasible h
  obtain ⟨x, ⟨hx, hmin⟩, huniq⟩ := G.toReal.exists_unique_energy_minimizer _ hc _ hy
  have ha := G.accepted_coefficientMinimum h
  have hr := G.accepted_radius h
  have hu := fun e => (G.accepted_roots h e).1
  have hroot := fun e => (G.accepted_roots h e).2
  have hgap := G.accepted_gap h
  have herror := G.toReal.certificate_radius ha.1 ha.2.1 ha.2.2 hy hx hmin
    hu hroot hgap hr.1 hr.2
  refine ⟨x, hx, hmin, (fun z hz hmz => huniq z ⟨hz, hmz⟩),
    G.toReal.energy_minimizer_potential hx hmin, ⟨sub_nonneg.mpr (hmin _ hy), ?_⟩,
    herror, G.toReal.certificate_pressure hc herror⟩
  rw [hgap]
  exact G.toReal.energy_error_le_gap hc hx hu hroot

end PotentialFlow.RationalNetwork
