import Formal.MultilinearGap.StructuralTreewidthAssembly
import Formal.MultilinearGap.StructuralTreewidthPieces

/-! Bipartite edges initialize the network accumulator. A degree-two
suppression preserves genuine series-parallel pieces, including the case where
a preexisting active edge must be combined in parallel with the series piece. -/
namespace MultilinearGap.StructuralTreewidth

open TreewidthGraph

variable {V W : Type*} {factor : V → Bool} {G : SimpleGraph W}

namespace EdgeExpansion

theorem series_piece (E : EdgeExpansion G (SPPiece factor)) (v a b : W)
    (hab : a ≠ b) (hdegree : ∀ w, G.Adj v w ↔ w = a ∨ w = b) :
    SPPiece factor (E.vertex a) (E.vertex b) (E.piece a v ⊔ E.piece v b) := by
  obtain ⟨hav, hbv⟩ := degree_two_neighbors_survive v a b hdegree
  exact .series (fun h => hab (E.vertex.injective h))
    (E.series_separation hav hbv hab)
    (E.valid a v ((hdegree a).mpr (Or.inl rfl)).symm)
    (E.valid v b ((hdegree b).mpr (Or.inr rfl)))

/-- The old terminal edge and the new series piece meet only at the two
terminals, so their union is a genuine parallel composition. -/
theorem combined_piece (E : EdgeExpansion G (SPPiece factor)) (v a b : W)
    (hab : a ≠ b) (hdegree : ∀ w, G.Adj v w ↔ w = a ∨ w = b) :
    SPPiece factor (E.vertex a) (E.vertex b)
      (E.piece a b ⊔ (E.piece a v ⊔ E.piece v b)) := by
  classical
  obtain ⟨hav, hbv⟩ := degree_two_neighbors_survive v a b hdegree
  have hs := E.series_piece v a b hab hdegree
  by_cases hedge : G.Adj a b
  · apply SPPiece.parallel ?_ ?_ (E.valid a b hedge) hs
    · intro x y z h₁ h₂
      rcases h₂ with h₂ | h₂
      · exact E.pieces_meet_only_terminals a b a v (by grind) x y z h₁ h₂
      · exact E.pieces_meet_only_terminals a b v b (by grind) x y z h₁ h₂
    · intro h
      have hav' := E.no_incident_of_ne (a := v) (b := b) hav hab
      have hbv' := E.no_incident_of_ne (a := a) (b := v) hab.symm hbv
      rcases h.2 with ha | hb
      · exact hbv' (E.vertex a) ha.symm
      · exact hav' (E.vertex b) hb
  · simpa only [E.absent a b hedge, bot_sup_eq] using hs

/-- Either orientation of the new fill edge carries the same combined graph. -/
theorem combined_piece_of_pair (E : EdgeExpansion G (SPPiece factor)) (v a b : W)
    (hab : a ≠ b) (hdegree : ∀ w, G.Adj v w ↔ w = a ∨ w = b)
    (x y : W) (hpair : (x = a ∧ y = b) ∨ (x = b ∧ y = a)) :
    SPPiece factor (E.vertex x) (E.vertex y)
      (E.piece x y ⊔ (E.piece a v ⊔ E.piece v b)) := by
  rcases hpair with ⟨hx, hy⟩ | ⟨hx, hy⟩
  · rw [hx, hy]
    exact E.combined_piece v a b hab hdegree
  · rw [hx, hy, E.symmetric b a]
    exact (E.combined_piece v a b hab hdegree).reverse

end EdgeExpansion

/-- The original bipartite graph is expanded into its actual singleton edges. -/
noncomputable def edgeExpansion (G : SimpleGraph V) (factor : V → Bool)
    (hbip : ∀ a b, G.Adj a b → factor a ≠ factor b) :
    EdgeExpansion G (SPPiece factor) := by
  classical
  refine {
    vertex := Function.Embedding.refl V
    piece := fun a b => if G.Adj a b then SimpleGraph.edge a b else ⊥
    symmetric := ?_
    absent := ?_
    valid := ?_
    active := ?_
    shared := ?_
  }
  · intro a b
    by_cases hab : G.Adj a b
    · simp only [hab, hab.symm, if_true]
      exact SimpleGraph.edge_comm a b
    · have hba : ¬ G.Adj b a := fun h => hab h.symm
      simp only [hab, hba, if_false]
  · intro a b hab
    simp only [hab, if_false]
  · intro a b hab
    change SPPiece factor a b _
    simpa only [hab, if_true] using SPPiece.edge a b (hbip a b hab)
  · intro a b x y h c hc
    by_cases hab : G.Adj a b
    · simp only [hab, if_true, SimpleGraph.edge_adj] at h
      change x = c at hc
      rcases h.1 with ⟨hx, _⟩ | ⟨hx, _⟩
      · exact Or.inl (hc.symm.trans hx)
      · exact Or.inr (hc.symm.trans hx)
    · simp only [hab, if_false, SimpleGraph.bot_adj] at h
  · intro a b c d x y z h₁ h₂
    exact Or.inr ⟨y, rfl⟩

theorem edgeExpansion_graph (G : SimpleGraph V) (factor : V → Bool)
    (hbip : ∀ a b, G.Adj a b → factor a ≠ factor b) :
    (edgeExpansion G factor hbip).graph = G := by
  classical
  ext x y
  rw [EdgeExpansion.graph_adj]
  constructor
  · rintro ⟨a, b, h⟩
    change (if G.Adj a b then SimpleGraph.edge a b else ⊥).Adj x y at h
    split_ifs at h with hab
    · simp only [SimpleGraph.edge_adj] at h
      rcases h.1 with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
      · exact hab
      · exact hab.symm
    · exact h.elim
  · intro h
    refine ⟨x, y, ?_⟩
    change (if G.Adj x y then SimpleGraph.edge x y else ⊥).Adj x y
    rw [if_pos h]
    exact (SimpleGraph.edge_adj x y x y).mpr ⟨Or.inl ⟨rfl, rfl⟩, h.ne⟩

end MultilinearGap.StructuralTreewidth
