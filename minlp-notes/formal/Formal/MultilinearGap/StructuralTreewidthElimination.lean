import Formal.MultilinearGap.StructuralTreewidthDecomposition
import Mathlib.Combinatorics.SimpleGraph.Finite

/-!
# Elimination from actual width-two tree decompositions

Choose a graph vertex whose highest containing bag is deepest. Every neighbor
belongs to that same bag: the two highest bags are comparable prefixes of an
edge-covering bag, and maximal depth orders them. Thus a bag-size-three
decomposition supplies a vertex with at most two neighbors. Completing those
neighbors to a clique and deleting the vertex preserves the decomposition.
-/

namespace MultilinearGap.StructuralTreewidth

variable {V : Type*}

theorem RootedTreeDecomposition.exists_closedNeighborhood_bag [Finite V] [Nonempty V]
    {G : SimpleGraph V} {Label : Type*} [DecidableEq Label]
    (D : RootedTreeDecomposition G Label) :
    ∃ (v : V) (t : List Label), t ∈ D.nodes ∧ v ∈ D.bag t ∧
      ∀ w, G.Adj v w → w ∈ D.bag t := by
  classical
  let _ := Fintype.ofFinite V
  choose root hroot hmem hinterval using D.connected_bags
  obtain ⟨v, _, hv⟩ := Finset.exists_max_image Finset.univ
    (fun v => (root v).length) Finset.univ_nonempty
  refine ⟨v, root v, hroot v, hmem v, ?_⟩
  intro w hvw
  obtain ⟨s, hs, hvs, hws⟩ := D.edge_covered hvw
  obtain ⟨hvp, _⟩ := hinterval v s hs hvs
  obtain ⟨hwp, hwinterval⟩ := hinterval w s hs hws
  exact hwinterval (root v)
    (List.prefix_of_prefix_length_le hwp hvp (hv w (Finset.mem_univ w))) hvp

/-- Complete the neighborhood of `v` before deleting `v`. -/
def fillNeighbors (G : SimpleGraph V) (v : V) : SimpleGraph V where
  Adj a b := G.Adj a b ∨ (a ≠ b ∧ G.Adj v a ∧ G.Adj v b)
  symm := ⟨by intro a b h; rcases h with h | ⟨hne, ha, hb⟩
              · exact Or.inl h.symm
              · exact Or.inr ⟨hne.symm, hb, ha⟩⟩
  loopless := ⟨by intro a; simp⟩

/-- Delete a vertex, retaining all old edges and adding an edge between its
remaining neighbors. At degree two this is the usual series elimination. -/
def eliminateVertex (G : SimpleGraph V) (v : V) : SimpleGraph {w : V // w ≠ v} :=
  (fillNeighbors G v).comap Subtype.val

/-- Completing neighbors covered by one bag preserves the decomposition. -/
def RootedTreeDecomposition.fillNeighbors {G : SimpleGraph V} {Label : Type*}
    [DecidableEq Label] (D : RootedTreeDecomposition G Label) (v : V)
    (t : List Label) (ht : t ∈ D.nodes)
    (hn : ∀ w, G.Adj v w → w ∈ D.bag t) :
    RootedTreeDecomposition (StructuralTreewidth.fillNeighbors G v) Label :=
  { D with
    edge_covered := fun _ _ h => by
      rcases h with h | ⟨_, ha, hb⟩
      · exact D.edge_covered h
      · exact ⟨t, ht, hn _ ha, hn _ hb⟩ }

theorem HasTreewidthAtMost.exists_elimination_step [Finite V] [Nonempty V]
    {G : SimpleGraph V} {width : ℕ} (hG : HasTreewidthAtMost G width) :
    ∃ v : V, (∃ S : Finset V, S.card ≤ width ∧ ∀ w, G.Adj v w → w ∈ S) ∧
      HasTreewidthAtMost (eliminateVertex G v) width := by
  classical
  let _ := Fintype.ofFinite V
  obtain ⟨L, hL, D, hcard⟩ := hG
  obtain ⟨v, t, ht, hv, hn⟩ := D.exists_closedNeighborhood_bag
  refine ⟨v, ⟨(D.bag t).erase v, ?_, ?_⟩, ?_⟩
  · have h := Finset.card_erase_add_one hv
    have := hcard t ht
    omega
  · intro w hw
    exact Finset.mem_erase.mpr ⟨hw.ne.symm, hn w hw⟩
  · have hf : HasTreewidthAtMost (fillNeighbors G v) width :=
      ⟨L, hL, D.fillNeighbors v t ht hn, hcard⟩
    let f : eliminateVertex G v →g fillNeighbors G v :=
      ⟨Subtype.val, fun h => h⟩
    exact hf.of_injective_hom f Subtype.val_injective

/-- A complete degree-at-most-two elimination certificate. The recursive graph
adds the possible edge between the two neighbors; mere degeneracy would omit
this necessary fill edge and would be a weaker condition. -/
inductive HasWidthTwoElimination : {V : Type u} → SimpleGraph V → Prop
  | empty {V : Type u} [IsEmpty V] (G : SimpleGraph V) : HasWidthTwoElimination G
  | step {V : Type u} (G : SimpleGraph V) (v : V)
      (neighbors : ∃ S : Finset V, S.card ≤ 2 ∧ ∀ w, G.Adj v w → w ∈ S)
      (rest : HasWidthTwoElimination (eliminateVertex G v)) : HasWidthTwoElimination G

theorem hasWidthTwoElimination_of_treewidth [Finite V] {G : SimpleGraph V}
    (hG : HasTreewidthAtMost G 2) : HasWidthTwoElimination G := by
  classical
  let _ := Fintype.ofFinite V
  suffices h : ∀ n, ∀ (W : Type _) [Fintype W] (H : SimpleGraph W),
      Fintype.card W = n → HasTreewidthAtMost H 2 → HasWidthTwoElimination H by
    exact h (Fintype.card V) V G rfl hG
  intro n
  induction n using Nat.strong_induction_on with
  | h n ih =>
    intro W _ H hcard hH
    cases isEmpty_or_nonempty W with
    | inl hW => exact HasWidthTwoElimination.empty H
    | inr hW =>
      obtain ⟨v, hn, hnext⟩ := hH.exists_elimination_step
      apply HasWidthTwoElimination.step H v hn
      apply ih (Fintype.card {w : W // w ≠ v}) ?_ _ _ rfl hnext
      rw [← hcard]
      exact Fintype.card_subtype_lt (x := v) (by simp)

end MultilinearGap.StructuralTreewidth
