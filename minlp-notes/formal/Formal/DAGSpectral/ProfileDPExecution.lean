import Formal.DAGSpectral.ProfileDPCost

namespace DAGSpectral

/-- Evaluate every key comparison, including the tail when an earlier result is
false. The second component counts the comparisons actually evaluated. -/
def compareAllCounted {α κ : Type*} [DecidableEq κ] (key : α → κ) (a : α) :
    List α → Bool × ℕ
  | [] => (true, 0)
  | b :: xs =>
    let rest := compareAllCounted key a xs
    (decide (key a ≠ key b) && rest.1, rest.2 + 1)

theorem compareAllCounted_spec {α κ : Type*} [DecidableEq κ]
    (key : α → κ) (a : α) (xs : List α) :
    compareAllCounted key a xs = (decide (∀ b ∈ xs, key a ≠ key b), xs.length) := by
  induction xs with
  | nil => simp [compareAllCounted]
  | cons b xs ih => simp [compareAllCounted, ih]

/-- A concrete full-scan implementation of the representative filter, returning
its comparison count together with its actual selected objects. -/
def representativesCounted {α κ : Type*} [DecidableEq κ] (key : α → κ) :
    List α → List α × ℕ
  | [] => ([], 0)
  | a :: xs =>
    let tail := representativesCounted key xs
    let checked := compareAllCounted key a tail.1
    (if checked.1 then a :: tail.1 else tail.1, tail.2 + checked.2)

theorem representativesCounted_spec {α κ : Type*} [DecidableEq κ]
    (key : α → κ) (xs : List α) :
    representativesCounted key xs =
      (representatives key xs, representativeComparisonBudget key xs) := by
  induction xs with
  | nil => rfl
  | cons a xs ih =>
    simp [representativesCounted, ih, compareAllCounted_spec,
      representatives, List.pwFilter, representativeComparisonBudget]

namespace ExplicitDAG
open scoped BigOperators
variable {v m : ℕ} {κ : Type*} [Fintype κ]

/-- The counted producer performs the same vertex updates as `run`, using the
full-scan dictionary above. No enumeration of feasible paths is introduced. -/
def runCounted (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
    (required : Finset (Fin m)) (label : Fin m → κ → ℤ) : ℕ → PathTable v m × ℕ
  | 0 => (fun _ => [], 0)
  | n + 1 =>
    let old := runCounted G allowed s required label n
    if hn : n < v then
      let t : Fin v := ⟨n, hn⟩
      let merged := representativesCounted (stateKey required label)
        (candidates G allowed s t old.1)
      (Function.update old.1 t merged.1, old.2 + merged.2)
    else old

variable (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
  (required : Finset (Fin m)) (label : Fin m → κ → ℤ)

theorem runCounted_table (n : ℕ) : (runCounted G allowed s required label n).1 =
    run G allowed s required label n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    by_cases hn : n < v <;>
      simp [runCounted, run, hn, ih, representativesCounted_spec]

def vertexComparisonCost (k : ℕ) : ℕ :=
  if hk : k < v then representativeComparisonBudget (stateKey required label)
    (candidates G allowed s ⟨k,hk⟩ (run G allowed s required label k)) else 0

theorem runCounted_cost (n : ℕ) : (runCounted G allowed s required label n).2 =
    ∑ k ∈ Finset.range n, vertexComparisonCost G allowed s required label k := by
  induction n with
  | zero => simp [runCounted]
  | succ n ih =>
    rw [Finset.sum_range_succ]
    by_cases hn : n < v <;>
      simp [runCounted, hn, ih, runCounted_table, representativesCounted_spec,
        vertexComparisonCost]

/-- At completion the producer's actual full-scan comparison count is the
previously bounded per-vertex comparison budget. -/
theorem runCounted_final_cost : (runCounted G allowed s required label v).2 =
    comparisonBudget G allowed s required label := by
  rw [runCounted_cost, ← Fin.sum_univ_eq_sum_range]
  unfold comparisonBudget
  apply Finset.sum_congr rfl
  intro t _
  simp [vertexComparisonCost, t.isLt]

theorem runCounted_comparisons_bound (window : Finset ℤ)
    (hw : ∀ t es, G.AllowedPath allowed s t es → ∀ i, profile label es i ∈ window) :
    (runCounted G allowed s required label v).2 ≤
      v * (1 + m * (2 ^ required.card * window.card ^ Fintype.card κ)) ^ 2 := by
  rw [runCounted_final_cost]
  exact comparisonBudget_bound G allowed s required label window hw

/-- Return the actual terminal paths together with the full-scan merge count.
Terminal owner-mask tests are separate from this dictionary-comparison count. -/
def outputCounted (t : Fin v) : List (List (Fin m)) × ℕ :=
  let result := runCounted G allowed s required label v
  ((result.1 t).filter (fun es => decide (ownerMask required es = required)), result.2)

theorem outputCounted_spec (t : Fin v) : outputCounted G allowed s required label t =
    (output G allowed s t required label, comparisonBudget G allowed s required label) := by
  apply Prod.ext
  · simp only [outputCounted, output, runCounted_table]
  · exact runCounted_final_cost G allowed s required label

end ExplicitDAG
end DAGSpectral
