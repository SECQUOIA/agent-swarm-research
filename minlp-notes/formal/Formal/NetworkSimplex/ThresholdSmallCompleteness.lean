import Formal.NetworkSimplex.ThresholdPartial
import Formal.NetworkSimplex.ThresholdTwoOccurrence
import Formal.NetworkSimplex.FiveTests

/-! Completeness of the one- and two-label circuit libraries, including absent rows. -/
namespace NetworkSimplex.OneStateCircuits
open scoped BigOperators

def normal : Fin 2 → Fin 1 → ℤ := ![![1], ![-1]]
def weight (_ : Fin 1) (_ : Fin 2) : ℤ := 1
theorem weight_nonnegative (c : Fin 1) (i : Fin 2) : 0 ≤ weight c i := by simp [weight]
theorem normal_cancellation : ∀ (c : Fin 1) (j : Fin 1),
    ∑ i, weight c i * normal i j = 0 := by decide +kernel
end NetworkSimplex.OneStateCircuits

namespace NetworkSimplex.Threshold
open scoped BigOperators

theorem one_full_complete (b : Fin 2 → ℝ)
    (h : ∀ c, 0 ≤ ∑ i, (OneStateCircuits.weight c i : ℝ) * b i) :
    ∃ x : Fin 1 → ℝ, ∀ i, ∑ j, (OneStateCircuits.normal i j : ℝ) * x j ≤ b i := by
  have hh := h 0
  simp [OneStateCircuits.weight, Fin.sum_univ_succ] at hh
  refine ⟨![-b 1], ?_⟩
  intro i
  fin_cases i
  · simpa [OneStateCircuits.normal] using (show -b 1 ≤ b 0 by linarith)
  · simp [OneStateCircuits.normal]

theorem two_full_complete (b : Fin 6 → ℝ)
    (h : ∀ c, 0 ≤ ∑ i, (TwoStateCircuits.weight c i : ℝ) * b i) :
    ∃ x : Fin 2 → ℝ, ∀ i, ∑ j, (TwoStateCircuits.normal i j : ℝ) * x j ≤ b i := by
  have h0 := h 0
  have h1 := h 1
  have h2 := h 2
  have h3 := h 3
  have h4 := h 4
  simp [TwoStateCircuits.weight, Fin.sum_univ_succ] at h0 h1 h2 h3 h4
  have ht : FiveTests (-b 3) (b 0) (-b 4) (b 1) (-b 5) (b 2) := by
    unfold FiveTests
    constructor <;> try linarith
    constructor <;> try linarith
    constructor <;> try linarith
    constructor <;> linarith
  obtain ⟨x, y, hxy⟩ := (five_tests_iff_feasible _ _ _ _ _ _).mp ht
  rcases hxy with ⟨r1,r2,r3,r4,r5,r6⟩
  refine ⟨![x,y], ?_⟩
  intro i
  fin_cases i <;> simp [TwoStateCircuits.normal, Fin.sum_univ_succ] <;> linarith

theorem one_weight_zero_or_one_le (c : Fin 1) (i : Fin 2) :
    (OneStateCircuits.weight c i : ℝ) = 0 ∨ 1 ≤ (OneStateCircuits.weight c i : ℝ) := by
  have hw := OneStateCircuits.weight_nonnegative c i
  have he : OneStateCircuits.weight c i = 0 ∨ 1 ≤ OneStateCircuits.weight c i := by omega
  exact_mod_cast he

theorem one_partial_feasible_iff (b : Fin 2 → Option ℝ) :
    (∃ x : Fin 1 → ℝ, ∀ i r, b i = some r →
      ∑ j, (OneStateCircuits.normal i j : ℝ) * x j ≤ r) ↔
      PartialCircuitTests (fun c i => (OneStateCircuits.weight c i : ℝ)) b := by
  constructor
  · rintro ⟨x, hx⟩
    exact partial_library_necessary (fun i j => (OneStateCircuits.normal i j : ℝ))
      (fun c i => (OneStateCircuits.weight c i : ℝ))
      (fun c i => by exact_mod_cast OneStateCircuits.weight_nonnegative c i)
      (fun c j => by exact_mod_cast OneStateCircuits.normal_cancellation c j) b hx
  · exact complete_partial_library (fun i j => (OneStateCircuits.normal i j : ℝ))
      (fun c i => (OneStateCircuits.weight c i : ℝ))
      one_weight_zero_or_one_le one_full_complete b

theorem two_weight_zero_or_one_le (c : Fin 5) (i : Fin 6) :
    (TwoStateCircuits.weight c i : ℝ) = 0 ∨ 1 ≤ (TwoStateCircuits.weight c i : ℝ) := by
  have hw := TwoStateCircuits.weight_nonnegative c i
  have he : TwoStateCircuits.weight c i = 0 ∨ 1 ≤ TwoStateCircuits.weight c i := by omega
  exact_mod_cast he

theorem two_partial_feasible_iff (b : Fin 6 → Option ℝ) :
    (∃ x : Fin 2 → ℝ, ∀ i r, b i = some r →
      ∑ j, (TwoStateCircuits.normal i j : ℝ) * x j ≤ r) ↔
      PartialCircuitTests (fun c i => (TwoStateCircuits.weight c i : ℝ)) b := by
  constructor
  · rintro ⟨x, hx⟩
    exact partial_library_necessary (fun i j => (TwoStateCircuits.normal i j : ℝ))
      (fun c i => (TwoStateCircuits.weight c i : ℝ))
      (fun c i => by exact_mod_cast TwoStateCircuits.weight_nonnegative c i)
      (fun c j => by exact_mod_cast TwoStateCircuits.normal_cancellation c j) b hx
  · exact complete_partial_library (fun i j => (TwoStateCircuits.normal i j : ℝ))
      (fun c i => (TwoStateCircuits.weight c i : ℝ))
      two_weight_zero_or_one_le two_full_complete b

end NetworkSimplex.Threshold
