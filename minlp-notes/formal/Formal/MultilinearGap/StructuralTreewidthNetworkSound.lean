import Formal.MultilinearGap.StructuralTreewidthColorAssembly
import Formal.MultilinearGap.StructuralTreewidthEmbedding

/-! Soundness of the finite-state invariant on concrete series-parallel graphs. -/
namespace MultilinearGap.StructuralTreewidth

open TreewidthGraph

private theorem exists_realizes_map (f : ℕ ↪ ℕ) (factor F : ℕ → Bool)
    {G : SimpleGraph ℕ} {u v : ℕ} {a : Signature}
    (hf : ∀ x, F (f x) = factor x)
    (h : ∃ c, RealizesSignature factor c G u v a) :
    ∃ C, RealizesSignature F C (G.map f) (f u) (f v) a := by
  obtain ⟨c, hc⟩ := h
  exact ⟨glueLabels f f c c,
    realizesSignature_map_embedding f factor c F _ hf (glueLabels_left f f c c) hc⟩

private theorem edge_state_sound (left : Bool) {a : Signature}
    (ha : a ∈ required left (!left) true true) :
    ∃ color, RealizesSignature (fun n : ℕ => if left then n == 0 else n == 1)
      color (edgeGraph.map edgeEmbedding) 0 1 a := by
  have ha' : a = active left (!left) false true ∨ a = active left (!left) true true := by
    cases left <;> simpa [required, needsBlocking] using ha
  rcases ha' with rfl | rfl
  all_goals
    first
    | exact ⟨fun _ => false, realizesSignature_map_embedding edgeEmbedding
        (edgeFactor left) (fun _ => false) _ (fun _ => false)
        (by intro x; cases x <;> cases left <;> rfl) (by intro x; rfl)
        (edge_realizes_active left false)⟩
    | exact ⟨fun _ => true, realizesSignature_map_embedding edgeEmbedding
        (edgeFactor left) (fun _ => true) _ (fun _ => true)
        (by intro x; cases x <;> cases left <;> rfl) (by intro x; rfl)
        (edge_realizes_active left true)⟩

/-- Every finite signature computed for a network is realized by an actual
coloring, with exactly the claimed simple-path parities and even cycles. -/
theorem Network.states_sound {l r direct : Bool} (N : Network l r direct)
    {a : Signature} (ha : a ∈ N.states) :
    ∃ color, RealizesSignature N.factor color N.graph 0 1 a := by
  induction N generalizing a with
  | edgeVF => exact edge_state_sound false ha
  | edgeFV => exact edge_state_sound true ha
  | @series l m r d₁ d₂ A B ihA ihB =>
    obtain ⟨⟨a, b⟩, hab, rfl⟩ := Finset.mem_image.mp ha
    obtain ⟨hab, hcolor⟩ := Finset.mem_filter.mp hab
    obtain ⟨ha, hb⟩ := Finset.mem_product.mp hab
    let F := glueLabels seriesLeft seriesRight A.factor B.factor
    have hf : A.factor 1 = B.factor 0 := by simp
    have hA := exists_realizes_map seriesLeft A.factor F
      (glueLabels_left _ _ _ _) (ihA ha)
    have hB := exists_realizes_map seriesRight B.factor F
      (glueLabels_right _ _ _ _ (series_labels_compatible hf)) (ihB hb)
    have hsep : MeetOnlyAt (A.graph.map seriesLeft) (B.graph.map seriesRight) 2 :=
      fun _ _ _ => series_meet_only_at _ _
    have hs : ∀ x, ¬ (B.graph.map seriesRight).Adj 0 x := by
      intro x hx
      obtain ⟨i, j, _, hi, _⟩ := (SimpleGraph.map_adj _ _ _ _).mp hx
      have hh : seriesLeft 0 = seriesRight i := hi.symm
      exact (by have := (series_intersection 0 i).mp hh; omega)
    have ht : ∀ x, ¬ (A.graph.map seriesLeft).Adj 1 x := by
      intro x hx
      obtain ⟨i, j, _, hi, _⟩ := (SimpleGraph.map_adj _ _ _ _).mp hx
      have hh : seriesLeft i = seriesRight 1 := hi
      exact (by have := (series_intersection i 1).mp hh; omega)
    have hm : F 2 = m := by
      change glueLabels seriesLeft seriesRight A.factor B.factor (seriesLeft 1) = m
      rw [glueLabels_left, A.factor_one]
    simpa only [Network.graph, seriesGraph, Network.factor, hm] using
      exists_realizesSignature_series F hsep (by decide) (by decide) (by decide)
        hs ht hA hB hcolor
  | @parallel l r d₁ d₂ hsimple A B ihA ihB =>
    obtain ⟨⟨a, b⟩, hab, rfl⟩ := Finset.mem_image.mp ha
    obtain ⟨hab, hcolor⟩ := Finset.mem_filter.mp hab
    obtain ⟨ha, hb⟩ := Finset.mem_product.mp hab
    let F := glueLabels parallelLeft parallelRight A.factor B.factor
    have hf₀ : A.factor 0 = B.factor 0 := by simp
    have hf₁ : A.factor 1 = B.factor 1 := by simp
    have hA := exists_realizes_map parallelLeft A.factor F
      (glueLabels_left _ _ _ _) (ihA ha)
    have hB := exists_realizes_map parallelRight B.factor F
      (glueLabels_right _ _ _ _ (parallel_labels_compatible hf₀ hf₁)) (ihB hb)
    have hsep : MeetOnlyAtPair (A.graph.map parallelLeft) (B.graph.map parallelRight) 0 1 :=
      fun _ _ _ => parallel_meet_only_at _ _
    have hl : F 0 = l := by
      change glueLabels parallelLeft parallelRight A.factor B.factor (parallelLeft 0) = l
      rw [glueLabels_left, A.factor_zero]
    have hr : F 1 = r := by
      change glueLabels parallelLeft parallelRight A.factor B.factor (parallelLeft 1) = r
      rw [glueLabels_left, A.factor_one]
    have hc : parallelCompatible (F 0) (F 1) a b := by simpa [hl, hr] using hcolor
    exact exists_realizesSignature_parallel F (by decide) hsep hA hB hc

/-- Every concrete bipartite series-parallel network admits a factor coloring
whose monochromatic simple cycles contain an even number of factor vertices. -/
theorem Network.exists_good {l r direct : Bool} (N : Network l r direct) :
    ∃ color, Good N.factor color N.graph := by
  obtain ⟨a, ha⟩ := N.states_nonempty
  obtain ⟨color, hc⟩ := N.states_sound ha
  exact ⟨color, hc.1⟩

end MultilinearGap.StructuralTreewidth
