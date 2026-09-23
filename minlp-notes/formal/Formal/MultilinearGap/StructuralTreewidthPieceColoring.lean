import Formal.MultilinearGap.StructuralTreewidthPieces
import Formal.MultilinearGap.StructuralTreewidthEmbedding
import Formal.MultilinearGap.StructuralTreewidthColorAssembly

/-! The finite parity invariant is realized by actual series-parallel pieces
on their original vertices, including all terminal orientations. -/

namespace MultilinearGap.TreewidthGraph

open StructuralTreewidth

variable {V : Type*} {factor : V → Bool} {u v : V} {H : SimpleGraph V}

/-- All required signatures have genuine graph colorings. The direct-edge
indicator is characterized by actual adjacency, rather than assumed syntax. -/
theorem SPPiece.invariant (piece : SPPiece factor u v H) :
    ∃ direct p : Bool, (direct = true ↔ H.Adj u v) ∧
      Valid (factor u) (factor v) direct p ∧
      ∀ sig ∈ required (factor u) (factor v) direct p,
        ∃ color, RealizesSignature factor color H u v sig := by
  classical
  induction piece with
  | edge u v htype =>
    refine ⟨true, true, ?_, fun _ => ⟨htype, rfl⟩, ?_⟩
    · simp [SimpleGraph.edge_adj, show u ≠ v from fun h => htype (congrArg _ h)]
    · intro sig hs
      have hsig : sig = active (factor u) (factor v) false true ∨
          sig = active (factor u) (factor v) true true := by
        cases hu : factor u <;> cases hv : factor v <;>
          simp_all [required, needsBlocking]
      rcases hsig with rfl | rfl
      · exact ⟨fun _ => false, edge_realizesSignature factor u v htype false⟩
      · exact ⟨fun _ => true, edge_realizesSignature factor u v htype true⟩
  | @series u m v H K hne hsep left right ih₁ ih₂ =>
    obtain ⟨d₁, p₁, hd₁, hv₁, h₁⟩ := ih₁
    obtain ⟨d₂, p₂, hd₂, hv₂, h₂⟩ := ih₂
    refine ⟨false, Bool.xor (Bool.xor p₁ p₂) (factor m), ?_, by simp [Valid], ?_⟩
    · simp [left.series_no_direct right hsep]
    · intro sig hs
      have hsig := required_series (factor u) (factor m) (factor v)
        d₁ d₂ p₁ p₂ hv₁ hv₂ hs
      obtain ⟨⟨a, b⟩, hab, rfl⟩ := Finset.mem_image.mp hsig
      obtain ⟨hab, hmatch⟩ := Finset.mem_filter.mp hab
      obtain ⟨ha, hb⟩ := Finset.mem_product.mp hab
      exact exists_realizesSignature_series factor hsep hne left.ne right.ne
        (left.series_left_terminal_isolated hsep)
        (right.series_right_terminal_isolated hsep) (h₁ a ha) (h₂ b hb) hmatch
  | @parallel u v H K hsep hsimple left right ih₁ ih₂ =>
    obtain ⟨d₁, p₁, hd₁, hv₁, h₁⟩ := ih₁
    obtain ⟨d₂, p₂, hd₂, hv₂, h₂⟩ := ih₂
    have hd : (d₁ && d₂) = false := by
      cases hd₁' : d₁ <;> cases hd₂' : d₂ <;> simp_all
    refine ⟨d₁ || d₂, parallelParity (factor u) (factor v) d₁ d₂ p₁ p₂,
      ?_, parallel_valid _ _ _ _ _ _ hv₁ hv₂, ?_⟩
    · simp only [Bool.or_eq_true, hd₁, hd₂, SimpleGraph.sup_adj]
    · intro sig hs
      have hsig := required_parallel (factor u) (factor v) d₁ d₂ p₁ p₂ hv₁ hv₂ hd hs
      obtain ⟨⟨a, b⟩, hab, rfl⟩ := Finset.mem_image.mp hsig
      obtain ⟨hab, hmatch⟩ := Finset.mem_filter.mp hab
      obtain ⟨ha, hb⟩ := Finset.mem_product.mp hab
      exact exists_realizesSignature_parallel factor left.ne hsep
        (h₁ a ha) (h₂ b hb) hmatch
  | @reverse u v H piece ih =>
    obtain ⟨d, p, hd, hv, hi⟩ := ih
    refine ⟨d, p, ?_, ?_, ?_⟩
    · exact hd.trans (H.adj_comm u v)
    · exact fun h => ⟨(hv h).1.symm, (hv h).2⟩
    · intro sig hs
      rw [← required_reverse] at hs
      obtain ⟨a, ha, rfl⟩ := Finset.mem_image.mp hs
      obtain ⟨color, hc⟩ := hi a ha
      exact ⟨color, hc.reverse⟩

/-- Every actual piece has a coloring with even factor count on every
monochromatic-factor cycle. -/
theorem SPPiece.exists_good (piece : SPPiece factor u v H) :
    ∃ color, Good factor color H := by
  obtain ⟨d, p, _, _, hi⟩ := piece.invariant
  obtain ⟨color, hc⟩ := hi (active (factor u) (factor v) false p) (by simp [required])
  exact ⟨color, hc.1⟩

end MultilinearGap.TreewidthGraph
