import Formal.MultilinearGap.StructuralTreewidthAssembly

/-! Degree-two suppression preserves the graph represented by an edge expansion. -/

namespace MultilinearGap.StructuralTreewidth.EdgeExpansion

variable {V W : Type*} {G : SimpleGraph W} {Piece : V → V → SimpleGraph V → Prop}

/-- The two possible orientations of one unordered pair. -/
def SamePair (a b x y : W) : Prop := (x = a ∧ y = b) ∨ (x = b ∧ y = a)

lemma SamePair.symm {a b x y : W} (h : SamePair a b x y) : SamePair a b y x := by
  unfold SamePair at *
  tauto

open scoped Classical in
noncomputable def suppressPiece (E : EdgeExpansion G Piece) (v a b : W)
    (x y : {w : W // w ≠ v}) : SimpleGraph V :=
  if SamePair a b x.val y.val then E.piece x.val y.val ⊔ (E.piece a v ⊔ E.piece v b)
  else E.piece x.val y.val

lemma suppressPiece_source (E : EdgeExpansion G Piece) {v a b : W}
    {x y : {w : W // w ≠ v}} {r s : V}
    (h : (E.suppressPiece v a b x y).Adj r s) :
    ∃ i j, (E.piece i j).Adj r s ∧
      ((i = x.val ∧ j = y.val) ∨
       (SamePair a b x.val y.val ∧ ((i = a ∧ j = v) ∨ (i = v ∧ j = b)))) := by
  classical
  unfold suppressPiece at h
  split_ifs at h with hxy
  · rcases h with h | h | h
    · exact ⟨x, y, h, Or.inl ⟨rfl, rfl⟩⟩
    · exact ⟨a, v, h, Or.inr ⟨hxy, Or.inl ⟨rfl, rfl⟩⟩⟩
    · exact ⟨v, b, h, Or.inr ⟨hxy, Or.inr ⟨rfl, rfl⟩⟩⟩
  · exact ⟨x, y, h, Or.inl ⟨rfl, rfl⟩⟩

lemma eliminateVertex_adj_iff_pair {v a b : W} (hab : a ≠ b)
    (hd : ∀ w, G.Adj v w ↔ w = a ∨ w = b) (x y : {w : W // w ≠ v}) :
    (eliminateVertex G v).Adj x y ↔ G.Adj x.val y.val ∨ SamePair a b x.val y.val := by
  change (G.Adj x.val y.val ∨ (x.val ≠ y.val ∧ G.Adj v x.val ∧ G.Adj v y.val)) ↔ _
  rw [hd, hd]
  unfold SamePair
  grind

/-- Suppress an active degree-two vertex, retaining its two networks inside the
new edge piece. The special-piece validity premise isolates the graph bookkeeping
from the series/parallel semantics. -/
noncomputable def suppress (E : EdgeExpansion G Piece) (v a b : W) (hab : a ≠ b)
    (hd : ∀ w, G.Adj v w ↔ w = a ∨ w = b)
    (hvalid : ∀ x y : {w : W // w ≠ v}, SamePair a b x.val y.val →
      Piece (E.vertex x.val) (E.vertex y.val)
        (E.piece x.val y.val ⊔ (E.piece a v ⊔ E.piece v b))) :
    EdgeExpansion (eliminateVertex G v) Piece where
  vertex := ⟨fun w => E.vertex w.val, E.vertex.injective.comp Subtype.val_injective⟩
  piece := E.suppressPiece v a b
  symmetric := by
    intro x y
    classical
    unfold suppressPiece
    by_cases hxy : SamePair a b x.val y.val
    · rw [if_pos hxy, if_pos hxy.symm, E.symmetric x.val y.val]
    · have hyx : ¬ SamePair a b y.val x.val := fun h => hxy h.symm
      rw [if_neg hxy, if_neg hyx, E.symmetric x.val y.val]
  absent := by
    intro x y hn
    classical
    have hn' := not_or.mp (mt (eliminateVertex_adj_iff_pair hab hd x y).mpr hn)
    simp only [suppressPiece, if_neg hn'.2, E.absent _ _ hn'.1]
  valid := by
    intro x y hxy
    classical
    unfold suppressPiece
    split_ifs with h
    · exact hvalid x y h
    · exact E.valid x.val y.val (((eliminateVertex_adj_iff_pair hab hd x y).mp hxy).resolve_right h)
  active := by
    intro x y r s hrs c hrc
    obtain ⟨i, j, hij, hsource⟩ := E.suppressPiece_source hrs
    have hactive := E.active i j r s hij c.val hrc
    have hc := c.property
    simp only [Subtype.ext_iff]
    unfold SamePair at hsource
    grind
  shared := by
    intro x y z t r s q h₁ h₂
    obtain ⟨i, j, hij, hi⟩ := E.suppressPiece_source h₁
    obtain ⟨k, l, hkl, hk⟩ := E.suppressPiece_source h₂
    rcases E.shared i j k l r s q hij hkl with hsame | ⟨w, hw⟩
    · left
      have hx := x.property
      have hy := y.property
      have hz := z.property
      have ht := t.property
      simp only [Subtype.ext_iff]
      unfold SamePair at hi hk
      grind
    · by_cases hwv : w = v
      · left
        have ha₁ := E.active i j s r hij.symm w hw
        have ha₂ := E.active k l s q hkl w hw
        have hx := x.property
        have hy := y.property
        have hz := z.property
        have ht := t.property
        simp only [Subtype.ext_iff]
        unfold SamePair at hi hk
        grind
      · exact Or.inr ⟨⟨w, hwv⟩, hw⟩

/-- Suppression changes the active graph but retains every original expanded edge. -/
theorem suppress_graph (E : EdgeExpansion G Piece) (v a b : W) (hab : a ≠ b)
    (hd : ∀ w, G.Adj v w ↔ w = a ∨ w = b)
    (hvalid : ∀ x y : {w : W // w ≠ v}, SamePair a b x.val y.val →
      Piece (E.vertex x.val) (E.vertex y.val)
        (E.piece x.val y.val ⊔ (E.piece a v ⊔ E.piece v b))) :
    (E.suppress v a b hab hd hvalid).graph = E.graph := by
  classical
  have hav : a ≠ v := ((hd a).mpr (Or.inl rfl)).ne.symm
  have hbv : b ≠ v := ((hd b).mpr (Or.inr rfl)).ne.symm
  let a' : {w : W // w ≠ v} := ⟨a, hav⟩
  let b' : {w : W // w ≠ v} := ⟨b, hbv⟩
  have hspecial : SamePair a b a'.val b'.val := Or.inl ⟨rfl, rfl⟩
  have hseries : E.piece a v ⊔ E.piece v b ≤ E.suppressPiece v a b a' b' := by
    rw [suppressPiece, if_pos hspecial]
    exact le_sup_right
  have hkeep : ∀ x y : {w : W // w ≠ v},
      E.piece x.val y.val ≤ E.suppressPiece v a b x y := by
    intro x y
    unfold suppressPiece
    split_ifs
    · exact le_sup_left
    · exact le_rfl
  ext r s
  constructor
  · intro hrs
    obtain ⟨x, y, hxy⟩ := (graph_adj _ r s).mp hrs
    obtain ⟨i, j, hij, _⟩ := E.suppressPiece_source hxy
    exact (E.graph_adj r s).mpr ⟨i, j, hij⟩
  · intro hrs
    obtain ⟨i, j, hij⟩ := (E.graph_adj r s).mp hrs
    apply (graph_adj _ r s).mpr
    change ∃ x y : {w : W // w ≠ v}, (E.suppressPiece v a b x y).Adj r s
    by_cases hiv : i = v
    · rw [hiv] at hij
      have hj := (hd j).mp (E.adjacent_of_piece hij)
      refine ⟨a', b', hseries ?_⟩
      rcases hj with hja | hjb
      · rw [hja, E.symmetric v a] at hij
        exact Or.inl hij
      · rw [hjb] at hij
        exact Or.inr hij
    · by_cases hjv : j = v
      · rw [hjv] at hij
        have hi := (hd i).mp (E.adjacent_of_piece hij).symm
        refine ⟨a', b', hseries ?_⟩
        rcases hi with hia | hib
        · rw [hia] at hij
          exact Or.inl hij
        · rw [hib, E.symmetric b v] at hij
          exact Or.inr hij
      · exact ⟨⟨i, hiv⟩, ⟨j, hjv⟩, hkeep ⟨i, hiv⟩ ⟨j, hjv⟩ hij⟩

end MultilinearGap.StructuralTreewidth.EdgeExpansion
