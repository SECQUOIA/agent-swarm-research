import Formal.NetworkSimplex.ThresholdResults

/-! The delivered convex combination omits all zero-weight states. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
variable {m L : ℕ}

/-- Stable filtering of state indices; normalized flow arrays are shared by reference. -/
def positiveStates (D : RationalData m L) : List (Fin (m + 1)) :=
  (List.finRange (m + 1)).filter fun j => 0 < D.weights j

@[simp] theorem mem_positiveStates (D : RationalData m L) (j : Fin (m + 1)) :
    j ∈ positiveStates D ↔ 0 < D.weights j := by simp [positiveStates]

theorem positiveStates_length (D : RationalData m L) : (positiveStates D).length ≤ m + 1 := by
  exact (List.length_filter_le _ _).trans (by simp)

theorem positiveStates_sum {V : Type*} [AddCommMonoid V] [Module ℝ V]
    (D : RationalData m L) (hw : ∀ j, 0 ≤ D.weights j) (p : Fin (m + 1) → V) :
    ((positiveStates D).map fun j => (D.weights j : ℝ) • p j).sum =
      ∑ j, (D.weights j : ℝ) • p j := by
  have hlist (js : List (Fin (m + 1))) :
      ((js.filter fun j => 0 < D.weights j).map fun j => (D.weights j : ℝ) • p j).sum =
        (js.map fun j => (D.weights j : ℝ) • p j).sum := by
    induction js with
    | nil => rfl
    | cons j js ih =>
      by_cases hj : 0 < D.weights j
      · simp [hj, ih]
      · have hz : D.weights j = 0 := le_antisymm (le_of_not_gt hj) (hw j)
        simp [hz, ih]
  rw [positiveStates, hlist]
  rw [← List.ofFn_eq_map, List.sum_ofFn]

/-- Positive states alone give the exact original moments with total weight one. -/
theorem checkedWitness_positive_decomposition (D : RationalData m L)
    (cache : List (CachedBasis (normalKeyCount m) m)) {out : ProfileRecovery m L}
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (ho : (checkedWitness D cache).1 = some out) :
    (∀ j ∈ positiveStates D, 0 < D.weights j ∧ out.graphPoint D j ∈ D.toReal.graph) ∧
    ((positiveStates D).map fun j => (D.weights j : ℝ)).sum = 1 ∧
    ((positiveStates D).map fun j => (D.weights j : ℝ) • out.graphPoint D j).sum =
      D.toReal.graphPoint ∧ (positiveStates D).length ≤ m + 1 := by
  obtain ⟨hp, hw, hs, _⟩ := checkedWitness_sound D cache hc hh ho
  have hn (j) : 0 ≤ D.weights j := by
    have h : 0 ≤ (D.weights j : ℝ) := hw.1 j
    exact_mod_cast h
  refine ⟨fun j hj => ⟨(mem_positiveStates D j).mp hj, hp j⟩, ?_, ?_, positiveStates_length D⟩
  · have h := positiveStates_sum D hn (fun _ => (1 : ℝ))
    simpa only [smul_eq_mul, mul_one, hw.2] using h
  · exact (positiveStates_sum D hn (out.graphPoint D)).trans hs

/-- The output filter visits each state exactly once and emits at most one index.
This is separate from the stored-atom recovery ledger. -/
def positiveStatesWork (D : RationalData m L) : ℕ :=
  (List.finRange (m + 1)).length + (positiveStates D).length

theorem positiveStatesWork_le (D : RationalData m L) :
    positiveStatesWork D ≤ 2 * (m + 1) := by
  have h := positiveStates_length D
  simp only [positiveStatesWork, List.length_finRange]
  omega

end NetworkSimplex.Chain.Threshold
