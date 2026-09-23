import Formal.MultilinearGap.StructuralTreewidthExpansion
import Formal.MultilinearGap.StructuralTreewidthSuppression
import Formal.MultilinearGap.StructuralTreewidthPieceColoring
import Formal.MultilinearGap.StructuralTreewidthArticulation

/-!
# One-sided cycle coloring for actual graphs of treewidth at most two

The proof starts from an actual tree decomposition, derives a complete
width-two elimination sequence, and accumulates internally disjoint edge
networks. Degree-two elimination uses series and parallel composition;
pendant elimination uses articulation gluing. No series-parallel network
certificate or coloring is assumed by the public theorem.
-/
namespace MultilinearGap.StructuralTreewidth

open TreewidthGraph

variable {V : Type*}

/-- Every expansion of a width-two elimination graph into genuine
series-parallel pieces admits a good coloring. This strengthened induction
hypothesis retains all edges removed from the active graph. -/
theorem HasWidthTwoElimination.exists_good_expansion
    {W : Type u} {G : SimpleGraph W} (h : HasWidthTwoElimination G)
    (factor : V → Bool) (E : EdgeExpansion G (SPPiece factor)) :
    ∃ color, Good factor color E.graph := by
  revert E
  apply h.induction_reductions
    (P := fun W G => ∀ E : EdgeExpansion G (SPPiece factor), ∃ color, Good factor color E.graph)
  · intro W _ G E
    refine ⟨fun _ => false, ?_⟩
    intro u p hp c hc
    cases p with
    | nil => exact (hp.ne_nil rfl).elim
    | cons hedge tail =>
      obtain ⟨a, b, hab⟩ := (E.graph_adj _ _).mp hedge
      exact isEmptyElim a
  · intro W G v hzero ih E
    have hrest : ∀ a b : {w : W // w ≠ v},
        (eliminateVertex G v).Adj a b ↔ G.Adj a.val b.val := by
      intro a b
      rw [eliminateVertex_zero v hzero]
      rfl
    rw [E.graph_eq_restrict_of_isolated v (eliminateVertex G v) hrest hzero]
    exact ih (E.restrict v (eliminateVertex G v) hrest)
  · intro W G v a hone ih E
    have hrest : ∀ x y : {w : W // w ≠ v},
        (eliminateVertex G v).Adj x y ↔ G.Adj x.val y.val := by
      intro x y
      rw [eliminateVertex_one v a hone]
      rfl
    rw [E.graph_eq_pendant_union v a (eliminateVertex G v) hrest hone]
    exact exists_good_union_at_vertex
      (E.pendant_separation v a (eliminateVertex G v) hrest) factor
      (E.valid v a ((hone a).mpr rfl)).exists_good
      (ih (E.restrict v (eliminateVertex G v) hrest))
  · intro W G v a b hab hd ih E
    have hv : ∀ x y : {w : W // w ≠ v}, EdgeExpansion.SamePair a b x.val y.val →
        SPPiece factor (E.vertex x.val) (E.vertex y.val)
          (E.piece x.val y.val ⊔ (E.piece a v ⊔ E.piece v b)) := by
      intro x y hxy
      exact E.combined_piece_of_pair v a b hab hd x.val y.val hxy
    have hh := ih (E.suppress v a b hab hd hv)
    rwa [E.suppress_graph v a b hab hd hv] at hh

/-- Every finite bipartite graph of treewidth at most two can color its factor
vertices with two colors so every monochromatic-factor cycle has even factor
count. The premise is the actual bag-size tree-decomposition definition. -/
theorem exists_good_of_treewidth_two [Finite V] {G : SimpleGraph V}
    (factor : V → Bool) (hbip : ∀ a b, G.Adj a b → factor a ≠ factor b)
    (hwidth : HasTreewidthAtMost G 2) : ∃ color, Good factor color G := by
  have h := (hasWidthTwoElimination_of_treewidth hwidth).exists_good_expansion factor
    (edgeExpansion G factor hbip)
  rwa [edgeExpansion_graph] at h

end MultilinearGap.StructuralTreewidth
