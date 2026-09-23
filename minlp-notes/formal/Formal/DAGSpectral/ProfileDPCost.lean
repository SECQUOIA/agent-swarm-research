import Formal.DAGSpectral.ProfileDPBounds

namespace DAGSpectral

/-- Charge every comparison in the representative-list membership test, even
when the actual Boolean evaluation could stop early. -/
def representativeComparisonBudget {α κ : Type*} [DecidableEq κ] (key : α → κ) :
    List α → ℕ
  | [] => 0
  | _ :: xs => representativeComparisonBudget key xs + (representatives key xs).length

theorem representativeComparisonBudget_le {α κ : Type*} [DecidableEq κ]
    (key : α → κ) (xs : List α) : representativeComparisonBudget key xs ≤ xs.length ^ 2 := by
  induction xs with
  | nil => simp [representativeComparisonBudget]
  | cons a xs ih =>
    have hh := (List.pwFilter_sublist (R := fun a b => key a ≠ key b) xs).length_le
    change (representatives key xs).length ≤ xs.length at hh
    simp only [representativeComparisonBudget, List.length_cons]
    nlinarith

namespace ExplicitDAG
open scoped BigOperators
variable {v m : ℕ} {κ : Type*} [Fintype κ]
variable (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
  (required : Finset (Fin m)) (label : Fin m → κ → ℤ)

/-- Charged key comparisons in the actual representative merges at all vertices. -/
def comparisonBudget : ℕ :=
  ∑ t : Fin v, representativeComparisonBudget (stateKey required label)
    (candidates G allowed s t (run G allowed s required label t.val))

variable (window : Finset ℤ)
  (hw : ∀ t es, G.AllowedPath allowed s t es → ∀ i, profile label es i ∈ window)
include hw

theorem candidate_length_bound (t : Fin v) :
    (candidates G allowed s t (run G allowed s required label t.val)).length ≤
      1 + m * (2 ^ required.card * window.card ^ Fintype.card κ) := by
  rw [candidates_decomposition, List.length_append, transitionCandidates_length]
  have hseed : (if t = s then ([[]] : List (List (Fin m))) else []).length ≤ 1 := by
    split_ifs <;> simp
  apply Nat.add_le_add hseed
  calc
    _ ≤ ∑ _e : Fin m, (2 ^ required.card * window.card ^ Fintype.card κ) := by
      apply Finset.sum_le_sum
      intro e _
      split_ifs
      · exact run_state_bound G allowed s required label window hw _ _
      · exact Nat.zero_le _
    _ = _ := by simp

theorem comparisonBudget_bound : comparisonBudget G allowed s required label ≤
    v * (1 + m * (2 ^ required.card * window.card ^ Fintype.card κ)) ^ 2 := by
  unfold comparisonBudget
  calc
    _ ≤ ∑ _t : Fin v, (1 + m * (2 ^ required.card * window.card ^ Fintype.card κ)) ^ 2 := by
      apply Finset.sum_le_sum
      intro t _
      exact (representativeComparisonBudget_le _ _).trans
        (Nat.pow_le_pow_left (candidate_length_bound G allowed s required label window hw t) 2)
    _ = _ := by simp

end ExplicitDAG
end DAGSpectral
