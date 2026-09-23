import Formal.MultilinearGap.StructuralTreewidthReduction
import Formal.MultilinearGap.StructuralTreewidthGluing

/-!
# Edge-network accumulation along width-two elimination

An expansion replaces each active graph edge by a graph with its two endpoints.
Distinct edge pieces have disjoint interiors. Eliminating a degree-two vertex
combines two pieces in series and, when the fill edge already exists, in
parallel. Pendant pieces are set aside and attached at their sole surviving
endpoint after the remaining graph has been colored.
-/
namespace MultilinearGap.StructuralTreewidth

open TreewidthGraph

variable {V W : Type*}

/-- A graph obtained by replacing active edges by internally disjoint pieces. -/
structure EdgeExpansion (G : SimpleGraph W)
    (Piece : V → V → SimpleGraph V → Prop) where
  vertex : W ↪ V
  piece : W → W → SimpleGraph V
  symmetric : ∀ a b, piece a b = piece b a
  absent : ∀ a b, ¬ G.Adj a b → piece a b = ⊥
  valid : ∀ a b, G.Adj a b → Piece (vertex a) (vertex b) (piece a b)
  active : ∀ a b x y, (piece a b).Adj x y →
    ∀ c, x = vertex c → c = a ∨ c = b
  shared : ∀ a b c d x y z, (piece a b).Adj x y → (piece c d).Adj y z →
    ((a = c ∧ b = d) ∨ (a = d ∧ b = c)) ∨ ∃ w, y = vertex w

namespace EdgeExpansion

variable {G : SimpleGraph W} {Piece : V → V → SimpleGraph V → Prop}

def graph (E : EdgeExpansion G Piece) : SimpleGraph V := ⨆ a, ⨆ b, E.piece a b

@[simp] theorem graph_adj (E : EdgeExpansion G Piece) (x y : V) :
    E.graph.Adj x y ↔ ∃ a b, (E.piece a b).Adj x y := by
  simp [graph, SimpleGraph.iSup_adj]

theorem adjacent_of_piece (E : EdgeExpansion G Piece) {a b : W} {x y : V}
    (h : (E.piece a b).Adj x y) : G.Adj a b := by
  by_contra hab
  simp [E.absent a b hab] at h

/-- The two edge networks around a degree-two vertex meet only at that vertex. -/
theorem series_separation (E : EdgeExpansion G Piece) {v a b : W}
    (hav : a ≠ v) (hbv : b ≠ v) (hab : a ≠ b) :
    MeetOnlyAt (E.piece a v) (E.piece v b) (E.vertex v) := by
  intro x y z h₁ h₂
  rcases E.shared a v v b x y z h₁ h₂ with h | ⟨w, hw⟩
  · rcases h with ⟨h, _⟩ | ⟨h, _⟩
    · exact (hav h).elim
    · exact (hab h).elim
  · have h₁ := E.active a v y x h₁.symm w hw
    have h₂ := E.active v b y z h₂ w hw
    rcases h₁ with rfl | rfl
    · rcases h₂ with h | h
      · exact (hav h).elim
      · exact (hab h).elim
    · exact hw

/-- No other active terminal is incident to the first series piece. -/
theorem no_incident_of_ne (E : EdgeExpansion G Piece) {a b c : W}
    (hca : c ≠ a) (hcb : c ≠ b) : ∀ z, ¬ (E.piece a b).Adj (E.vertex c) z := by
  intro z hz
  rcases E.active a b (E.vertex c) z hz c rfl with h | h
  · exact hca h
  · exact hcb h

/-- Distinct active edges can share only their common active endpoints. -/
theorem pieces_meet_only_terminals (E : EdgeExpansion G Piece) (a b c d : W)
    (hneq : ¬ ((a = c ∧ b = d) ∨ (a = d ∧ b = c))) :
    MeetOnlyAtPair (E.piece a b) (E.piece c d) (E.vertex a) (E.vertex b) := by
  intro x y z h₁ h₂
  rcases E.shared a b c d x y z h₁ h₂ with h | ⟨w, hw⟩
  · exact (hneq h).elim
  · rcases E.active a b y x h₁.symm w hw with rfl | rfl
    · exact Or.inl hw
    · exact Or.inr hw

/-- Deleting an isolated or pendant active vertex leaves the other pieces
unchanged. The graph parameter may be any graph with the same remaining edges. -/
def restrict (E : EdgeExpansion G Piece) (v : W)
    (H : SimpleGraph {w : W // w ≠ v})
    (hH : ∀ a b, H.Adj a b ↔ G.Adj a.val b.val) : EdgeExpansion H Piece where
  vertex := ⟨fun w => E.vertex w.val, E.vertex.injective.comp Subtype.val_injective⟩
  piece := fun a b => E.piece a.val b.val
  symmetric := fun a b => E.symmetric a.val b.val
  absent := fun a b hab => E.absent _ _ (fun h => hab ((hH a b).mpr h))
  valid := fun a b hab => E.valid _ _ ((hH a b).mp hab)
  active := by
    intro a b x y h c hc
    rcases E.active _ _ _ _ h c.val hc with h | h
    · exact Or.inl (Subtype.ext h)
    · exact Or.inr (Subtype.ext h)
  shared := by
    intro a b c d x y z h₁ h₂
    rcases E.shared _ _ _ _ _ _ _ h₁ h₂ with h | ⟨w, hw⟩
    · left
      rcases h with ⟨h₁, h₂⟩ | ⟨h₁, h₂⟩
      · exact Or.inl ⟨Subtype.ext h₁, Subtype.ext h₂⟩
      · exact Or.inr ⟨Subtype.ext h₁, Subtype.ext h₂⟩
    · right
      have hwv : w ≠ v := by
        rcases E.active _ _ _ _ h₁.symm w hw with h | h
        · simpa only [h] using a.property
        · simpa only [h] using b.property
      exact ⟨⟨w, hwv⟩, hw⟩

@[simp] theorem restrict_graph_adj (E : EdgeExpansion G Piece) (v : W)
    (H : SimpleGraph {w : W // w ≠ v})
    (hH : ∀ a b, H.Adj a b ↔ G.Adj a.val b.val) (x y : V) :
    (E.restrict v H hH).graph.Adj x y ↔
      ∃ a b, a ≠ v ∧ b ≠ v ∧ (E.piece a b).Adj x y := by
  simp only [graph_adj, restrict]
  constructor
  · rintro ⟨a, b, hab⟩
    exact ⟨a.val, b.val, a.property, b.property, hab⟩
  · rintro ⟨a, b, hav, hbv, hab⟩
    exact ⟨⟨a, hav⟩, ⟨b, hbv⟩, hab⟩

theorem graph_eq_restrict_of_isolated (E : EdgeExpansion G Piece) (v : W)
    (H : SimpleGraph {w : W // w ≠ v})
    (hH : ∀ a b, H.Adj a b ↔ G.Adj a.val b.val)
    (hzero : ∀ w, ¬ G.Adj v w) : E.graph = (E.restrict v H hH).graph := by
  ext x y
  rw [graph_adj, restrict_graph_adj]
  constructor
  · rintro ⟨a, b, hab⟩
    have hg := E.adjacent_of_piece hab
    have hav : a ≠ v := fun h => hzero b (h ▸ hg)
    have hbv : b ≠ v := fun h => hzero a (h ▸ hg.symm)
    exact ⟨a, b, hav, hbv, hab⟩
  · rintro ⟨a, b, _, _, hab⟩
    exact ⟨a, b, hab⟩

/-- The removed pendant network is attached to the remaining expansion at
exactly its surviving endpoint. -/
theorem pendant_separation (E : EdgeExpansion G Piece) (v a : W)
    (H : SimpleGraph {w : W // w ≠ v})
    (hH : ∀ a b, H.Adj a b ↔ G.Adj a.val b.val) :
    MeetOnlyAt (E.piece v a) (E.restrict v H hH).graph (E.vertex a) := by
  intro x y z h₁ h₂
  obtain ⟨c, d, hcv, hdv, h₂⟩ := (restrict_graph_adj E v H hH y z).mp h₂
  rcases E.shared v a c d x y z h₁ h₂ with h | ⟨w, hw⟩
  · rcases h with ⟨h, _⟩ | ⟨h, _⟩
    · exact (hcv h.symm).elim
    · exact (hdv h.symm).elim
  · have he₁ := E.active v a y x h₁.symm w hw
    have he₂ := E.active c d y z h₂ w hw
    rcases he₁ with rfl | rfl
    · rcases he₂ with h | h
      · exact (hcv h.symm).elim
      · exact (hdv h.symm).elim
    · exact hw

/-- A pendant reduction partitions all actual edges into the removed network
and the remaining expansion. -/
theorem graph_eq_pendant_union (E : EdgeExpansion G Piece) (v a : W)
    (H : SimpleGraph {w : W // w ≠ v})
    (hH : ∀ a b, H.Adj a b ↔ G.Adj a.val b.val)
    (hone : ∀ w, G.Adj v w ↔ w = a) :
    E.graph = E.piece v a ⊔ (E.restrict v H hH).graph := by
  ext x y
  rw [SimpleGraph.sup_adj, graph_adj, restrict_graph_adj]
  constructor
  · rintro ⟨c, d, hcd⟩
    by_cases hcv : c = v
    · subst c
      have hd := (hone d).mp (E.adjacent_of_piece hcd)
      subst d
      exact Or.inl hcd
    by_cases hdv : d = v
    · subst d
      have hc := (hone c).mp (E.adjacent_of_piece hcd).symm
      subst c
      exact Or.inl (by simpa only [E.symmetric a v] using hcd)
    exact Or.inr ⟨c, d, hcv, hdv, hcd⟩
  · rintro (h | ⟨c, d, _, _, h⟩)
    · exact ⟨v, a, h⟩
    · exact ⟨c, d, h⟩

end EdgeExpansion
end MultilinearGap.StructuralTreewidth
