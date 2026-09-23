import Formal.NetworkSimplex.ThresholdCircuitOracle
import Formal.NetworkSimplex.ThresholdPartial

/-! Exact connection between finite dense circuit tables and the executed sparse scan. -/
namespace NetworkSimplex.ThresholdOracle
open scoped BigOperators

/-- A finite dense weight vector is encoded as the actual sparse-oracle input.
Zero entries may remain in the list; selection ignores them. -/
def denseCircuit {N K : ℕ} (key : Fin N → Fin K) (weight : Fin N → ℕ) : Circuit K :=
  List.ofFn fun i ↦ (key i, weight i)

def denseLibrary {C N K : ℕ} (key : Fin N → Fin K)
    (weight : Fin C → Fin N → ℕ) : List (Circuit K) :=
  List.ofFn fun c ↦ denseCircuit key (weight c)

/-- Selection succeeds precisely when every nonzero list entry has a present row. -/
theorem selectTerms_exists_iff {K : ℕ} {α : Type*} (table : Fin K → Option α)
    (c : Circuit K) :
    (∃ rows, selectTerms table c = some rows) ↔
      ∀ term ∈ c, table term.1 = none → term.2 = 0 := by
  induction c with
  | nil => simp [selectTerms]
  | cons term cs ih =>
    rcases term with ⟨key, w⟩
    by_cases hw : w = 0
    · simpa [selectTerms, hw] using ih
    · cases ht : table key with
      | none => simp [selectTerms, hw, ht]
      | some row =>
        cases hs : selectTerms table cs with
        | none => simpa [selectTerms, hw, ht, hs] using ih
        | some rows => simpa [selectTerms, hw, ht, hs] using ih

/-- For dense circuits, absent directions must have zero weight.
The key map need not be injective. -/
theorem dense_selectTerms_exists_iff {N K : ℕ} {α : Type*}
    (table : Fin K → Option α) (key : Fin N → Fin K) (weight : Fin N → ℕ) :
    (∃ rows, selectTerms table (denseCircuit key weight) = some rows) ↔
      ∀ i, table (key i) = none → weight i = 0 := by
  rw [selectTerms_exists_iff]
  simp [denseCircuit, List.mem_ofFn]

/-- The selected original rows have exactly the dense weighted right-hand side. -/
theorem dense_selected_value {N K : ℕ} {α : Type*} (table : Fin K → Option α)
    (rhs : α → ℚ) (key : Fin N → Fin K) (weight : Fin N → ℕ)
    {rows : List (ℕ × α)} (hs : selectTerms table (denseCircuit key weight) = some rows) :
    (weightedValue rhs rows : ℝ) =
      ∑ i, (weight i : ℝ) * ((table (key i)).map (fun row ↦ (rhs row : ℝ))).getD 0 := by
  rw [cast_weightedValue]
  have hh := selectTerms_sum table (fun row ↦ (rhs row : ℝ))
    (fun k ↦ ((table k).map (fun row ↦ (rhs row : ℝ))).getD 0)
    (fun k row hk ↦ by simp [hk]) (denseCircuit key weight) hs
  simpa [realCut, denseCircuit, List.map_ofFn, List.sum_ofFn, Function.comp_def] using hh

private theorem dense_support_cast_iff {N K : ℕ} {α : Type*}
    (table : Fin K → Option α) (rhs : α → ℚ) (key : Fin N → Fin K) (weight : Fin N → ℕ) :
    (∀ i, table (key i) = none → weight i = 0) ↔
      ∀ i, (table (key i)).map (fun row ↦ (rhs row : ℝ)) = none → (weight i : ℝ) = 0 := by
  simp

/-- A single selected circuit test agrees exactly with the partial-table test. -/
theorem dense_test_iff {N K : ℕ} {α : Type*} (table : Fin K → Option α)
    (rhs : α → ℚ) (key : Fin N → Fin K) (weight : Fin N → ℕ) :
    (∀ rows, selectTerms table (denseCircuit key weight) = some rows →
      0 ≤ weightedValue rhs rows) ↔
    ((∀ i, (table (key i)).map (fun row ↦ (rhs row : ℝ)) = none → (weight i : ℝ) = 0) →
      0 ≤ ∑ i, (weight i : ℝ) *
        ((table (key i)).map (fun row ↦ (rhs row : ℝ))).getD 0) := by
  constructor
  · intro h hp
    obtain ⟨rows, hs⟩ := (dense_selectTerms_exists_iff table key weight).mpr
      ((dense_support_cast_iff table rhs key weight).mpr hp)
    rw [← dense_selected_value table rhs key weight hs]
    exact_mod_cast h rows hs
  · intro h rows hs
    have hp := (dense_selectTerms_exists_iff table key weight).mp ⟨rows, hs⟩
    have hh := h ((dense_support_cast_iff table rhs key weight).mp hp)
    rw [← dense_selected_value table rhs key weight hs] at hh
    exact_mod_cast hh

/-- Acceptance of the actual executable scan is equivalent to all dense partial
circuit inequalities. Absent zero-weight keys impose no extra requirement. -/
theorem dense_circuitOracle_none_iff {C N K : ℕ} {α : Type*} (table : Fin K → Option α)
    (rhs : α → ℚ) (key : Fin N → Fin K) (weight : Fin C → Fin N → ℕ) :
    (circuitOracle table rhs (denseLibrary key weight)).1 = none ↔
      NetworkSimplex.Threshold.PartialCircuitTests
        (fun c i ↦ (weight c i : ℝ))
        (fun i ↦ (table (key i)).map (fun row ↦ (rhs row : ℝ))) := by
  rw [circuitOracle_none_iff]
  simp only [denseLibrary, List.mem_ofFn]
  constructor
  · intro h c
    exact (dense_test_iff table rhs key (weight c)).mp
      (h (denseCircuit key (weight c)) ⟨c, rfl⟩)
  · intro h circuit hc
    obtain ⟨c, rfl⟩ := hc
    exact (dense_test_iff table rhs key (weight c)).mpr (h c)

/-- The dense representation has `N` entries per circuit, so the executed
arithmetic/comparison ledger is at most `C * (2*N + 1)`. -/
theorem dense_circuitOracle_cost {C N K : ℕ} {α : Type*} (table : Fin K → Option α)
    (rhs : α → ℚ) (key : Fin N → Fin K) (weight : Fin C → Fin N → ℕ) :
    (circuitOracle table rhs (denseLibrary key weight)).2 ≤ C * (2 * N + 1) := by
  have h := circuitOracle_cost table rhs (denseLibrary key weight)
  simpa [denseLibrary, denseCircuit, List.map_ofFn, List.sum_ofFn, Function.comp_def] using h

end NetworkSimplex.ThresholdOracle
