import Formal.MultilinearGap.StructuralTreewidthNetworks

/-! Assembly of independently chosen colors across actual graph separators. -/
namespace MultilinearGap.TreewidthGraph

open StructuralTreewidth

variable {V : Type*} {H K : SimpleGraph V} {s t m : V}

/-- Exactly the vertices whose colors can affect a two-terminal signature. -/
def ColorRelevant (H : SimpleGraph V) (s t x : V) : Prop :=
  x = s ∨ x = t ∨ ∃ y, H.Adj x y

lemma realizesSignature_congr_color (factor c d : V → Bool) {a : Signature}
    (h : RealizesSignature factor c H s t a)
    (hcolor : ∀ x, ColorRelevant H s t x → c x = d x) :
    RealizesSignature factor d H s t a := by
  have hw : ∀ {u v} (p : H.Walk u v), (¬ p.Nil ∨ u = s) →
      ∀ x ∈ p.support, c x = d x := by
    intro u v p hp x hx
    apply hcolor x
    rcases hp with hp | rfl
    · exact Or.inr (Or.inr (exists_adj_of_mem_support p hp hx))
    · by_cases hn : p.Nil
      · cases p with
        | nil => exact Or.inl (by simpa using hx)
        | cons hadj q => simp at hn
      · exact Or.inr (Or.inr (exists_adj_of_mem_support p hn hx))
  have hm : ∀ {u v} (p : H.Walk u v), (¬ p.Nil ∨ u = s) → ∀ b,
      Monochromatic factor c b p ↔ Monochromatic factor d b p := by
    intro u v p hp b
    unfold Monochromatic
    constructor <;> intro hc x hx hf
    · rw [← hw p hp x hx]
      exact hc x hx hf
    · rw [hw p hp x hx]
      exact hc x hx hf
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro u p hp b hc
    exact h.1 u p hp b ((hm p (Or.inl hp.not_nil) b).mpr hc)
  · rw [← hcolor s (Or.inl rfl)]
    exact h.2.1
  · rw [← hcolor t (Or.inr (Or.inl rfl))]
    exact h.2.2.1
  · intro b bit
    rw [h.2.2.2 b bit]
    simp_rw [hm _ (Or.inr rfl) b]

/-- Compatible colors on the relevant vertices combine into one ambient coloring. -/
lemma exists_common_coloring (factor c d : V → Bool)
    {u v w z : V} {a b : Signature}
    (ha : RealizesSignature factor c H u v a)
    (hb : RealizesSignature factor d K w z b)
    (hcompat : ∀ x, ColorRelevant H u v x → ColorRelevant K w z x → c x = d x) :
    ∃ color, RealizesSignature factor color H u v a ∧
      RealizesSignature factor color K w z b := by
  classical
  let color := fun x => if ColorRelevant H u v x then c x else d x
  refine ⟨color, realizesSignature_congr_color factor c color ha ?_,
    realizesSignature_congr_color factor d color hb ?_⟩
  · intro x hx
    simp [color, hx]
  · intro x hx
    dsimp [color]
    split_ifs with hh
    · exact (hcompat x hh hx).symm
    · rfl

/-- Independent parallel child colorings with compatible signatures can be
assembled into a realization of their parallel signature. -/
theorem exists_realizesSignature_parallel (factor : V → Bool) (hst : s ≠ t)
    (hsep : MeetOnlyAtPair H K s t) {a b : Signature}
    (ha : ∃ color, RealizesSignature factor color H s t a)
    (hb : ∃ color, RealizesSignature factor color K s t b)
    (hc : parallelCompatible (factor s) (factor t) a b) :
    ∃ color, RealizesSignature factor color (H ⊔ K) s t (parallelSignature a b) := by
  obtain ⟨c, ha⟩ := ha
  obtain ⟨d, hb⟩ := hb
  have hcn := realizesSignature_normalize factor c ha
  have hdn := realizesSignature_normalize factor d hb
  have h₀ : (factor s && c s) = (factor s && d s) := ha.2.1.symm.trans (hc.1.trans hb.2.1)
  have h₁ : (factor t && c t) = (factor t && d t) := ha.2.2.1.symm.trans (hc.2.1.trans hb.2.2.1)
  have heq : ∀ x, ColorRelevant H s t x → ColorRelevant K s t x →
      (factor x && c x) = (factor x && d x) := by
    intro x hx hrelK
    rcases hx with rfl | rfl | ⟨y, hy⟩
    · exact h₀
    · exact h₁
    · rcases hrelK with rfl | rfl | ⟨z, hz⟩
      · exact h₀
      · exact h₁
      · rcases hsep y x z hy.symm hz with rfl | rfl
        · exact h₀
        · exact h₁
  obtain ⟨color, hH, hK⟩ := exists_common_coloring factor _ _ hcn hdn heq
  exact ⟨color, realizesSignature_parallel factor color hst hsep hH hK hc⟩

/-- Independent series child colorings can be matched using their common
signature color at the articulation. -/
theorem exists_realizesSignature_series (factor : V → Bool)
    (hsep : MeetOnlyAt H K m) (hst : s ≠ t) (hsm : s ≠ m) (hmt : m ≠ t)
    (hs : ∀ x, ¬ K.Adj s x) (ht : ∀ x, ¬ H.Adj t x) {a b : Signature}
    (ha : ∃ color, RealizesSignature factor color H s m a)
    (hb : ∃ color, RealizesSignature factor color K m t b)
    (hc : a.rightColor = b.leftColor) :
    ∃ color, RealizesSignature factor color (H ⊔ K) s t (seriesSignature (factor m) a b) := by
  obtain ⟨c, ha⟩ := ha
  obtain ⟨d, hb⟩ := hb
  have hcn := realizesSignature_normalize factor c ha
  have hdn := realizesSignature_normalize factor d hb
  have hmid : (factor m && c m) = (factor m && d m) := ha.2.2.1.symm.trans (hc.trans hb.2.1)
  have heq : ∀ x, ColorRelevant H s m x → ColorRelevant K m t x →
      (factor x && c x) = (factor x && d x) := by
    intro x hx hrelK
    rcases hx with rfl | rfl | ⟨y, hy⟩
    · rcases hrelK with hm | ht' | ⟨y, hy⟩
      · exact (hsm hm).elim
      · exact (hst ht').elim
      · exact (hs y hy).elim
    · exact hmid
    · rcases hrelK with rfl | rfl | ⟨z, hz⟩
      · exact hmid
      · exact (ht y hy).elim
      · have hxm := hsep y x z hy.symm hz
        simpa [hxm] using hmid
  obtain ⟨color, hH, hK⟩ := exists_common_coloring factor _ _ hcn hdn heq
  exact ⟨color, realizesSignature_series factor color hsep hst hsm hmt hs ht hH hK⟩

end MultilinearGap.TreewidthGraph
