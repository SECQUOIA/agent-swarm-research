import Formal.PotentialFlow.Example
import Formal.PotentialFlow.Results

namespace PotentialFlow.Example

/-- The saved certificate encloses the unique physical flow on all six edges. -/
theorem saved_example_verified :
    ∃ x : Fin 6 → ℝ,
      network.toReal.Feasible (fun v => (nominations v : ℝ)) x ∧
      (∀ z, network.toReal.Feasible (fun v => (nominations v : ℝ)) z →
        network.toReal.energy x ≤ network.toReal.energy z) ∧
      (∃ p, network.toReal.drops p = fun e =>
        edgeLaw (network.toReal.positive e) (network.toReal.negative e) (x e)) ∧
      (∀ e, |(certificate.flow e : ℝ) - x e| ≤ (certificate.radius : ℝ)) ∧
      (∀ e, |(certificate.flow e : ℝ) - x e| < (1 / 5000 : ℝ)) := by
  obtain ⟨x, hx, hmin, _, hp, _, hr, _⟩ := network.accepted_sound accepted
  refine ⟨x, hx, hmin, hp, hr, fun e => (hr e).trans_lt ?_⟩
  have h : (certificate.radius : ℝ) < ((1 / 5000 : ℚ) : ℝ) :=
    Rat.cast_lt.mpr radius_lt_one_five_thousandth
  norm_num at h ⊢
  exact h

end PotentialFlow.Example
