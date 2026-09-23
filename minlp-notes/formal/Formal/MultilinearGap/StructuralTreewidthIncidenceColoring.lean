import Formal.MultilinearGap.StructuralTreewidthColoring

/-! One-sided coloring for the actual variable-factor incidence graph. -/

namespace MultilinearGap.StructuralTreewidth

open TreewidthGraph

/-- Every finite width-two incidence graph admits a two-coloring of its
factors such that every monochromatic-factor cycle has even factor count.
The hypothesis is an actual tree decomposition, with no coloring or
series-parallel certificate supplied as a premise. -/
theorem incidence_exists_good_two_coloring {I J : Type*} [Finite I] [Finite J]
    (incident : I → J → Prop)
    (hwidth : HasTreewidthAtMost (incidenceGraph incident) 2) :
    ∃ color : J → Bool,
      Good (Sum.elim (fun _ : I => false) (fun _ : J => true))
        (Sum.elim (fun _ : I => false) color) (incidenceGraph incident) := by
  let factor : I ⊕ J → Bool := Sum.elim (fun _ => false) (fun _ => true)
  have hbip : ∀ a b, (incidenceGraph incident).Adj a b → factor a ≠ factor b := by
    intro a b hab
    cases a <;> cases b <;> simp_all [incidenceGraph, factor]
  obtain ⟨c, hc⟩ := exists_good_of_treewidth_two factor hbip hwidth
  refine ⟨fun j => c (.inr j), ?_⟩
  intro u p hp b hm
  apply hc u p hp b
  intro x hx hf
  cases x with
  | inl i => simp [factor] at hf
  | inr j => exact hm (.inr j) hx rfl

end MultilinearGap.StructuralTreewidth
