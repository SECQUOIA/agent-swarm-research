import Formal.MultilinearGap.StructuralTreewidthGluing

/-! Independent good colorings can be matched and glued at an articulation.
Only vertices incident to an edge constrain a coloring. -/

namespace MultilinearGap.TreewidthGraph

variable {V : Type*} {G H K : SimpleGraph V}

theorem cycle_vertex_incident {u x : V} (p : G.Walk u u) (hp : p.IsCycle)
    (hx : x ∈ p.support) : ∃ y, G.Adj x y := by
  classical
  let q := p.rotate x hx
  exact ⟨q.snd, q.adj_snd (hp.rotate hx).not_nil⟩

/-- Changing colors at isolated vertices does not affect the cycle condition. -/
theorem good_congr_incident (factor a b : V → Bool)
    (h : ∀ x, (∃ y, G.Adj x y) → a x = b x) (ha : Good factor a G) :
    Good factor b G := by
  intro u p hp c hc
  apply ha u p hp c
  intro x hx hf
  rw [h x (cycle_vertex_incident p hp hx)]
  exact hc x hx hf

/-- Independently chosen good colorings glue at a single shared vertex.
The second coloring may be globally swapped to match the first there. -/
theorem exists_good_union_at_vertex {s : V} (hsep : MeetOnlyAt H K s)
    (factor : V → Bool) (hH : ∃ a, Good factor a H) (hK : ∃ b, Good factor b K) :
    ∃ color, Good factor color (H ⊔ K) := by
  classical
  obtain ⟨a, ha⟩ := hH
  obtain ⟨b, hb⟩ := hK
  obtain ⟨b, hb, hbs⟩ := exists_good_matching_vertex factor b hb s (a s)
  let color := fun x => if ∃ y, H.Adj x y then a x else b x
  refine ⟨color, good_union_at_vertex hsep factor color ?_ ?_⟩
  · apply good_congr_incident factor a color _ ha
    intro x hx
    exact (if_pos hx).symm
  · apply good_congr_incident factor b color _ hb
    intro x hx
    dsimp [color]
    split_ifs with hh
    · obtain ⟨y, hy⟩ := hh
      obtain ⟨z, hz⟩ := hx
      have hxs := hsep y x z hy.symm hz
      simpa [hxs] using hbs
    · rfl

end MultilinearGap.TreewidthGraph
