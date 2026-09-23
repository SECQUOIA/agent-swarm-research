import Formal.NetworkSimplex.ThresholdPartial
import Formal.NetworkSimplex.Circuits

/-! The existing sixteen-test theorem applied to partial tables of original rows. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators
open ThreeStateCircuits

/-- Every possible real right-hand side is represented by the existing profile bounds. -/
def boundsOfRhs (b : Fin 11 → ℝ) : ThreeStateBounds :=
  ⟨-b 7, -b 8, -b 9, -b 10, b 0, b 1, b 2, b 3, b 4, b 5, b 6⟩

theorem rhs_boundsOfRhs (b : Fin 11 → ℝ) : rhs (boundsOfRhs b) = b := by
  funext i
  fin_cases i <;> simp [rhs, boundsOfRhs]

theorem three_full_complete (b : Fin 11 → ℝ)
    (h : ∀ c, 0 ≤ ∑ i, (weight c i : ℝ) * b i) :
    ∃ x : Fin 3 → ℝ, ∀ i, ∑ j, (normal i j : ℝ) * x j ≤ b i := by
  have hc : CircuitTests (boundsOfRhs b) := by
    simpa only [CircuitTests, rhs_boundsOfRhs] using h
  obtain ⟨x, y, z, hp⟩ := (circuit_tests_iff_feasible (boundsOfRhs b)).mp hc
  rcases hp with ⟨h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11⟩
  simp only [boundsOfRhs] at h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11
  refine ⟨![x, y, z], ?_⟩
  intro i
  fin_cases i <;> simp [normal, Fin.sum_univ_succ] <;> linarith

theorem three_weight_zero_or_one_le (c : Fin 16) (i : Fin 11) :
    (weight c i : ℝ) = 0 ∨ 1 ≤ (weight c i : ℝ) := by
  have hw := weight_nonnegative c i
  have he : weight c i = 0 ∨ 1 ≤ weight c i := by omega
  exact_mod_cast he

/-- Absent normal groups are omitted; no redundant box branch is added to a cut. -/
theorem three_partial_feasible_iff (b : Fin 11 → Option ℝ) :
    (∃ x : Fin 3 → ℝ, ∀ i r, b i = some r → ∑ j, (normal i j : ℝ) * x j ≤ r) ↔
      PartialCircuitTests (fun c i => (weight c i : ℝ)) b := by
  constructor
  · rintro ⟨x, hx⟩
    exact partial_library_necessary (fun i j => (normal i j : ℝ))
      (fun c i => (weight c i : ℝ)) (fun c i => by exact_mod_cast weight_nonnegative c i)
      (fun c j => by exact_mod_cast normal_cancellation c j) b hx
  · exact complete_partial_library (fun i j => (normal i j : ℝ))
      (fun c i => (weight c i : ℝ)) three_weight_zero_or_one_le three_full_complete b

end NetworkSimplex.Threshold
