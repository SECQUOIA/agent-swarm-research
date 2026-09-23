import Formal.InfiniteAggregation.Model

/-! Explicit candidate hull regions and the original weak system. -/

noncomputable section

namespace InfiniteAggregation

/-- The explicit ordinary-hull region; its equality with the hull is proved separately. -/
def hullRegion (r : ℕ) : Set (Var r) :=
  {x | qnorm x.1 < 1 ∧ qnorm x.2 < 1 ∧
    1 / 2 < dot x.1 x.2 + Real.sqrt ((1 - qnorm x.1) * (1 - qnorm x.2))}

/-- The explicit candidate closed hull, including zero-slack boundary points. -/
def closedRegion (r : ℕ) : Set (Var r) :=
  {x | qnorm x.1 ≤ 1 ∧ qnorm x.2 ≤ 1 ∧
    1 / 2 ≤ dot x.1 x.2 + Real.sqrt ((1 - qnorm x.1) * (1 - qnorm x.2))}

/-- The original system with all three strict inequalities replaced by weak ones. -/
def weakFeasible (r : ℕ) : Set (Var r) := {x | ∀ i, eval x i ≤ 0}

theorem mem_weakFeasible_iff {r : ℕ} (x : Var r) :
    x ∈ weakFeasible r ↔ qnorm x.1 ≤ 1 ∧ qnorm x.2 ≤ 1 ∧ 1 / 2 ≤ dot x.1 x.2 := by
  simp [weakFeasible, eval, Fin.forall_fin_succ]

theorem feasible_subset_weakFeasible {r : ℕ} : feasible r ⊆ weakFeasible r :=
  fun _ hx i => (hx i).le

theorem feasible_subset_hullRegion {r : ℕ} : feasible r ⊆ hullRegion r := by
  intro x hx
  obtain ⟨hu, hv, huv⟩ := (mem_feasible_iff x).1 hx
  exact ⟨hu, hv, lt_of_lt_of_le huv (le_add_of_nonneg_right (Real.sqrt_nonneg _))⟩

theorem weakFeasible_subset_closedRegion {r : ℕ} : weakFeasible r ⊆ closedRegion r := by
  intro x hx
  obtain ⟨hu, hv, huv⟩ := (mem_weakFeasible_iff x).1 hx
  exact ⟨hu, hv, le_trans huv (le_add_of_nonneg_right (Real.sqrt_nonneg _))⟩

theorem hullRegion_subset_closedRegion {r : ℕ} : hullRegion r ⊆ closedRegion r :=
  fun _ hx => ⟨hx.1.le, hx.2.1.le, hx.2.2.le⟩

end InfiniteAggregation
