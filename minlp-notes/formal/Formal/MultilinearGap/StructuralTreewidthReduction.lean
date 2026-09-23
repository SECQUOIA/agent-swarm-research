import Formal.MultilinearGap.StructuralTreewidthElimination

/-!
# Exact local reductions supplied by width-two elimination

The neighbor classification uses actual adjacency rather than an oversized
covering set. In the two-neighbor case, elimination adds exactly the edge
between the two distinct neighbors.
-/
namespace MultilinearGap.StructuralTreewidth

variable {V : Type*} {G : SimpleGraph V}

/-- The three exact local cases in a degree-at-most-two reduction. -/
inductive NeighborCase (G : SimpleGraph V) (v : V) : Prop
  | zero (adj : ∀ w, ¬ G.Adj v w)
  | one (a : V) (adj : ∀ w, G.Adj v w ↔ w = a)
  | two (a b : V) (distinct : a ≠ b) (adj : ∀ w, G.Adj v w ↔ w = a ∨ w = b)

theorem neighborCase (G : SimpleGraph V) (v : V)
    (h : ∃ S : Finset V, S.card ≤ 2 ∧ ∀ w, G.Adj v w → w ∈ S) :
    NeighborCase G v := by
  classical
  let S := h.choose.filter (G.Adj v)
  have hcard : S.card ≤ 2 := (Finset.card_filter_le _ _).trans h.choose_spec.1
  have hmem (w : V) : w ∈ S ↔ G.Adj v w := by
    simp only [S, Finset.mem_filter]
    exact and_iff_right_of_imp (h.choose_spec.2 w)
  by_cases hzero : S.card = 0
  · exact .zero fun w hw => by
      have := (hmem w).mpr hw
      simp [Finset.card_eq_zero.mp hzero] at this
  by_cases hone : S.card = 1
  · obtain ⟨a, ha⟩ := Finset.card_eq_one.mp hone
    exact .one a fun w => by rw [← hmem, ha]; simp
  have htwo : S.card = 2 := by omega
  obtain ⟨a, b, hab, hs⟩ := Finset.card_eq_two.mp htwo
  exact .two a b hab fun w => by rw [← hmem, hs]; simp

@[simp] theorem eliminateVertex_adj (G : SimpleGraph V) (v : V)
    (a b : {w : V // w ≠ v}) :
    (eliminateVertex G v).Adj a b ↔
      G.Adj a.val b.val ∨ (a.val ≠ b.val ∧ G.Adj v a.val ∧ G.Adj v b.val) := Iff.rfl

/-- An isolated-vertex reduction adds no edges. -/
theorem eliminateVertex_zero (v : V) (h : ∀ w, ¬ G.Adj v w) :
    eliminateVertex G v = G.comap (fun w : {w : V // w ≠ v} => w.val) := by
  ext a b
  simp [eliminateVertex_adj, h]

/-- Removing a pendant vertex adds no edges either. -/
theorem eliminateVertex_one (v a : V) (h : ∀ w, G.Adj v w ↔ w = a) :
    eliminateVertex G v = G.comap (fun w : {w : V // w ≠ v} => w.val) := by
  ext x y
  simp only [eliminateVertex_adj, h, SimpleGraph.comap_adj]
  grind

/-- Suppression of a degree-two vertex adds precisely its terminal edge. -/
theorem eliminateVertex_two (v a b : V) (hab : a ≠ b)
    (h : ∀ w, G.Adj v w ↔ w = a ∨ w = b)
    (x y : {w : V // w ≠ v}) :
    (eliminateVertex G v).Adj x y ↔ G.Adj x.val y.val ∨
      (x.val = a ∧ y.val = b) ∨ (x.val = b ∧ y.val = a) := by
  simp only [eliminateVertex_adj, h]
  grind

/-- In the degree-two case, the two terminals survive deletion. -/
theorem degree_two_neighbors_survive (v a b : V)
    (h : ∀ w, G.Adj v w ↔ w = a ∨ w = b) : a ≠ v ∧ b ≠ v := by
  exact ⟨((h a).mpr (Or.inl rfl)).ne.symm,
    ((h b).mpr (Or.inr rfl)).ne.symm⟩

/-- A preexisting terminal edge is exactly the parallel-merge case. -/
theorem eliminateVertex_two_existing (v a b : V)
    (h : ∀ w, G.Adj v w ↔ w = a ∨ w = b) (hab : G.Adj a b) :
    eliminateVertex G v = G.comap (fun w : {w : V // w ≠ v} => w.val) := by
  ext x y
  rw [eliminateVertex_two v a b hab.ne h]
  change (G.Adj x.val y.val ∨ _ ∨ _) ↔ G.Adj x.val y.val
  constructor
  · rintro (hxy | ⟨hx, hy⟩ | ⟨hx, hy⟩)
    · exact hxy
    · simpa [hx, hy] using hab
    · simpa [hx, hy] using hab.symm
  · exact Or.inl

/-- Elimination induction exposing the exact isolated, pendant, and series
cases. The remaining graph in the series case includes the fill edge, so this
principle is stronger than induction on two-degenerate graphs. -/
theorem HasWidthTwoElimination.induction_reductions
    {P : ∀ (W : Type u), SimpleGraph W → Prop}
    (empty : ∀ (W : Type u) [IsEmpty W] (H : SimpleGraph W), P W H)
    (isolated : ∀ (W : Type u) (H : SimpleGraph W) (v : W),
      (∀ w, ¬ H.Adj v w) → P _ (eliminateVertex H v) → P W H)
    (pendant : ∀ (W : Type u) (H : SimpleGraph W) (v a : W),
      (∀ w, H.Adj v w ↔ w = a) → P _ (eliminateVertex H v) → P W H)
    (series : ∀ (W : Type u) (H : SimpleGraph W) (v a b : W),
      a ≠ b → (∀ w, H.Adj v w ↔ w = a ∨ w = b) →
      P _ (eliminateVertex H v) → P W H)
    {W : Type u} {H : SimpleGraph W} (h : HasWidthTwoElimination H) : P W H := by
  induction h with
  | empty H => exact empty _ H
  | @step W H v neighbors rest ih =>
    cases neighborCase H v neighbors with
    | zero h => exact isolated W H v h ih
    | one a h => exact pendant W H v a h ih
    | two a b hab h => exact series W H v a b hab h ih

/-- Treewidth two gives the exact reduction induction, with no separate
series-parallel certificate assumption. -/
theorem HasTreewidthAtMost.induction_reductions
    {P : ∀ (W : Type u), SimpleGraph W → Prop}
    (empty : ∀ (W : Type u) [IsEmpty W] (H : SimpleGraph W), P W H)
    (isolated : ∀ (W : Type u) (H : SimpleGraph W) (v : W),
      (∀ w, ¬ H.Adj v w) → P _ (eliminateVertex H v) → P W H)
    (pendant : ∀ (W : Type u) (H : SimpleGraph W) (v a : W),
      (∀ w, H.Adj v w ↔ w = a) → P _ (eliminateVertex H v) → P W H)
    (series : ∀ (W : Type u) (H : SimpleGraph W) (v a b : W),
      a ≠ b → (∀ w, H.Adj v w ↔ w = a ∨ w = b) →
      P _ (eliminateVertex H v) → P W H)
    {W : Type u} [Finite W] {H : SimpleGraph W} (h : HasTreewidthAtMost H 2) :
    P W H :=
  (hasWidthTwoElimination_of_treewidth h).induction_reductions
    empty isolated pendant series

end MultilinearGap.StructuralTreewidth
