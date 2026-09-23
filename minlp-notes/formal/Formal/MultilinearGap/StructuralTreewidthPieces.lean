import Formal.MultilinearGap.StructuralTreewidthGluing
import Mathlib.Combinatorics.SimpleGraph.Operations

/-! Series-parallel pieces in their original ambient graph, without relabeling
vertices or assuming a coloring. Separation hypotheses concern actual edges. -/

namespace MultilinearGap.TreewidthGraph

variable {V : Type*}

/-- A two-terminal piece assembled from original bipartite edges. -/
inductive SPPiece (factor : V → Bool) : V → V → SimpleGraph V → Prop
  | edge (u v : V) (htype : factor u ≠ factor v) :
      SPPiece factor u v (SimpleGraph.edge u v)
  | series {u m v : V} {H K : SimpleGraph V} (hne : u ≠ v)
      (hsep : MeetOnlyAt H K m) (left : SPPiece factor u m H)
      (right : SPPiece factor m v K) : SPPiece factor u v (H ⊔ K)
  | parallel {u v : V} {H K : SimpleGraph V} (hsep : MeetOnlyAtPair H K u v)
      (hsimple : ¬ (H.Adj u v ∧ K.Adj u v))
      (left : SPPiece factor u v H) (right : SPPiece factor u v K) :
      SPPiece factor u v (H ⊔ K)
  | reverse {u v : V} {H : SimpleGraph V} (piece : SPPiece factor u v H) :
      SPPiece factor v u H

namespace SPPiece

variable {factor : V → Bool} {u v : V} {H : SimpleGraph V}

theorem ne (h : SPPiece factor u v H) : u ≠ v := by
  induction h with
  | edge u v ht => exact fun huv => ht (congrArg _ huv)
  | series hne _ _ _ _ _ => exact hne
  | parallel _ _ _ _ ih _ => exact ih
  | reverse _ ih => exact ih.symm

/-- Every terminal belongs to an actual edge of the piece. -/
theorem terminals_incident (h : SPPiece factor u v H) :
    (∃ x, H.Adj u x) ∧ (∃ x, H.Adj v x) := by
  induction h with
  | edge u v ht =>
    have huv : u ≠ v := fun h => ht (congrArg _ h)
    constructor
    · exact ⟨v, by simp [SimpleGraph.edge, huv]⟩
    · exact ⟨u, by simp [SimpleGraph.edge, huv, huv.symm]⟩
  | series _ _ _ _ ih₁ ih₂ =>
    exact ⟨ih₁.1.imp (fun _ h => Or.inl h), ih₂.2.imp (fun _ h => Or.inr h)⟩
  | parallel _ _ _ _ ih _ =>
    exact ⟨ih.1.imp (fun _ h => Or.inl h), ih.2.imp (fun _ h => Or.inl h)⟩
  | reverse _ ih => exact ih.symm

theorem bipartite (h : SPPiece factor u v H) :
    ∀ x y, H.Adj x y → factor x ≠ factor y := by
  induction h with
  | edge u v ht =>
    intro x y hxy
    simp only [SimpleGraph.edge_adj] at hxy
    rcases hxy with ⟨⟨rfl, rfl⟩ | ⟨rfl, rfl⟩, _⟩
    · exact ht
    · exact ht.symm
  | series _ _ _ _ ih₁ ih₂ =>
    intro x y hxy
    exact hxy.elim (ih₁ x y) (ih₂ x y)
  | parallel _ _ _ _ ih₁ ih₂ =>
    intro x y hxy
    exact hxy.elim (ih₁ x y) (ih₂ x y)
  | reverse _ ih => exact ih

theorem series_left_terminal_isolated {m : V} {K : SimpleGraph V}
    (a : SPPiece factor u m H) (hsep : MeetOnlyAt H K m) :
    ∀ x, ¬ K.Adj u x := by
  obtain ⟨y, hy⟩ := a.terminals_incident.1
  intro x hx
  exact a.ne (hsep y u x hy.symm hx)

theorem series_right_terminal_isolated {m : V} {K : SimpleGraph V}
    (b : SPPiece factor m v K) (hsep : MeetOnlyAt H K m) :
    ∀ x, ¬ H.Adj v x := by
  obtain ⟨y, hy⟩ := b.terminals_incident.2
  intro x hx
  exact b.ne (hsep x v y hx.symm hy).symm

theorem series_no_direct {m : V} {K : SimpleGraph V}
    (a : SPPiece factor u m H) (b : SPPiece factor m v K)
    (hsep : MeetOnlyAt H K m) : ¬ (H ⊔ K).Adj u v := by
  intro huv
  exact huv.elim (fun h => b.series_right_terminal_isolated hsep u h.symm)
    (fun h => a.series_left_terminal_isolated hsep v h)

end SPPiece
end MultilinearGap.TreewidthGraph
