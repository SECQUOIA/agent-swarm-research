import Formal.MultilinearGap.StructuralFeedbackAssembly

/-! The sharpness flower has one feedback variable. Its graph assertions refer
to the actual scopes, including the inactive factor vertices in the feedback
incidence convention. -/
namespace MultilinearGap.StructuralSharpness
open CubicGap SimpleGraph
noncomputable section

def flowerFeedback (n : ℕ) : Finset (Coord n) := {none}

@[simp] theorem flowerFeedback_card (n : ℕ) : (flowerFeedback n).card = 1 := by
  simp [flowerFeedback]

private theorem pair_residual_neighbor {n : ℕ} (i : Fin n)
    (v : Coord n ⊕ Finset (Coord n))
    (h : (feedbackIncidence (flowerFeedback n) (supports n)).Adj (.inr (pairSupport i)) v) :
    v = .inl (some i) := by
  cases v with
  | inr s => exact False.elim h
  | inl j =>
    change pairSupport i ∈ supports n ∧ j ∈ pairSupport i \ flowerFeedback n at h
    have hh := h.2
    simp only [Finset.mem_sdiff, pairSupport, flowerFeedback, Finset.mem_insert,
      Finset.mem_singleton] at hh
    exact congrArg Sum.inl (hh.1.resolve_left hh.2)

private theorem cycle_factor_eq_leaf {n : ℕ} {s : Finset (Coord n)}
    (p : (feedbackIncidence (flowerFeedback n) (supports n)).Walk (.inr s) (.inr s))
    (hp : p.IsCycle) : s = leafSupport n := by
  have ha := p.adj_snd hp.not_nil
  have hs : s ∈ supports n := by
    cases h : p.snd with
    | inl j => rw [h] at ha; change s ∈ supports n ∧ j ∈ s \ flowerFeedback n at ha; exact ha.1
    | inr t => rw [h] at ha; exact False.elim ha
  rcases Finset.mem_insert.mp hs with hs | hs
  · exact hs
  · obtain ⟨i, _, hi⟩ := Finset.mem_image.mp hs
    subst s
    exact False.elim (hp.snd_ne_penultimate
      ((pair_residual_neighbor i _ ha).trans
        (pair_residual_neighbor i _ (p.adj_penultimate hp.not_nil).symm).symm))

private theorem no_variable_cycle {n : ℕ} (i : Coord n)
    (p : (feedbackIncidence (flowerFeedback n) (supports n)).Walk (.inl i) (.inl i)) :
    ¬ p.IsCycle := by
  intro hp
  have hs : p.snd = .inr (leafSupport n) := by
    have ha := p.adj_snd hp.not_nil
    have hc : ∃ q : (feedbackIncidence (flowerFeedback n) (supports n)).Walk p.snd p.snd,
        q.IsCycle := ⟨_, hp.rotate (p.getVert_mem_support 1)⟩
    cases he : p.snd with
    | inl j => rw [he] at ha; exact False.elim ha
    | inr s =>
      rw [he] at hc
      obtain ⟨q, hq⟩ := hc
      exact congrArg Sum.inr (cycle_factor_eq_leaf q hq)
  have ht : p.penultimate = .inr (leafSupport n) := by
    have ha := p.adj_penultimate hp.not_nil
    have hc : ∃ q : (feedbackIncidence (flowerFeedback n) (supports n)).Walk
        p.penultimate p.penultimate, q.IsCycle :=
      ⟨_, hp.rotate (p.getVert_mem_support (p.length - 1))⟩
    cases he : p.penultimate with
    | inl j => rw [he] at ha; exact False.elim ha
    | inr s =>
      rw [he] at hc
      obtain ⟨q, hq⟩ := hc
      exact congrArg Sum.inr (cycle_factor_eq_leaf q hq)
  exact hp.snd_ne_penultimate (hs.trans ht.symm)

/-- Deleting the one anchor variable leaves an actual incidence forest. -/
theorem flower_feedback_acyclic (n : ℕ) :
    (feedbackIncidence (flowerFeedback n) (supports n)).IsAcyclic := by
  intro v p hp
  cases v with
  | inl i => exact no_variable_cycle i p hp
  | inr s =>
    have ha := p.adj_snd hp.not_nil
    have hc : ∃ q : (feedbackIncidence (flowerFeedback n) (supports n)).Walk p.snd p.snd,
        q.IsCycle := ⟨_, hp.rotate (p.getVert_mem_support 1)⟩
    cases he : p.snd with
    | inr t => rw [he] at ha; exact False.elim ha
    | inl i =>
      rw [he] at hc
      obtain ⟨q, hq⟩ := hc
      exact no_variable_cycle i q hq

open StructuralTreewidth

/-- The three-edge branch from the anchor to the large factor. -/
def flowerBranch {n : ℕ} (i : Fin n) :
    (flowerGraph n).Walk (.inl none) (.inr none) :=
  .cons (v := .inr (some i)) (by trivial)
    (.cons (v := .inl (some i)) (by rfl) (.cons (by trivial) .nil))

theorem flowerBranch_isPath {n : ℕ} (i : Fin n) : (flowerBranch i).IsPath := by
  simp [flowerBranch, SimpleGraph.Walk.isPath_def, SimpleGraph.Walk.support]

/-- Two distinct branches rule out acyclicity for every `n≥2`. -/
theorem flower_not_acyclic (n : ℕ) (hn : 2 ≤ n) : ¬ (flowerGraph n).IsAcyclic := by
  intro h
  let i : Fin n := ⟨0, by omega⟩
  let j : Fin n := ⟨1, by omega⟩
  have he := (h.subsingleton_path (.inl none) (.inr none)).elim
    ⟨flowerBranch i, flowerBranch_isPath i⟩ ⟨flowerBranch j, flowerBranch_isPath j⟩
  have hs := congrArg (fun p : (flowerGraph n).Path (.inl none) (.inr none) => p.val.snd) he
  change (Sum.inr (some i) : FlowerVertex n) = Sum.inr (some j) at hs
  have hij : i = j := Option.some.inj (Sum.inr.inj hs)
  have := congrArg Fin.val hij
  simp [i, j] at this

/-- The named incidence graph has treewidth exactly two. -/
theorem flower_treewidth_exactly_two (n : ℕ) (hn : 2 ≤ n) :
    HasTreewidthAtMost (flowerGraph n) 2 ∧ ¬ HasTreewidthAtMost (flowerGraph n) 1 := by
  exact ⟨flower_hasTreewidthAtMost_two n, fun h => flower_not_acyclic n hn h.isAcyclic⟩

/-- Map the named factors back to the actual distinct monomial scopes. -/
def flowerActualHom (n : ℕ) : flowerGraph n →g flowerSupportGraph n where
  toFun := Sum.map id (flowerFactorMap n)
  map_rel' := by
    intro v w h
    cases v with
    | inl i =>
      cases w with
      | inl j => exact False.elim h
      | inr s => exact (flowerIncidence_iff_mem i s).mp h
    | inr s =>
      cases w with
      | inl i => exact (flowerIncidence_iff_mem i s).mp h
      | inr t => exact False.elim h

/-- The actual scope incidence graph, not just an auxiliary indexing, has
exactly treewidth two. -/
theorem flower_supports_treewidth_exactly_two (n : ℕ) (hn : 2 ≤ n) :
    HasTreewidthAtMost (flowerSupportGraph n) 2 ∧
      ¬ HasTreewidthAtMost (flowerSupportGraph n) 1 := by
  refine ⟨flower_supports_treewidth_le_two n, fun h => ?_⟩
  apply (flower_treewidth_exactly_two n hn).2
  exact h.of_injective_hom (flowerActualHom n)
    (Sum.map_injective.mpr ⟨Function.injective_id, (flowerFactorMap_bijective n).1⟩)

/-- The same named flower embeds in the convention used by the feedback
headline theorem, where unused factor vertices are retained as isolated. -/
def flowerFullHom (n : ℕ) :
    flowerGraph n →g feedbackIncidence (∅ : Finset (Coord n)) (supports n) where
  toFun := Sum.map id (flowerFactorScope n)
  map_rel' := by
    intro v w h
    have hm (s : Option (Fin n)) : flowerFactorScope n s ∈ supports n :=
      (flowerFactorMap n s).property
    cases v with
    | inl i =>
      cases w with
      | inl j => exact False.elim h
      | inr s =>
        exact ⟨hm s, by simpa using (flowerIncidence_iff_mem i s).mp h⟩
    | inr s =>
      cases w with
      | inl i =>
        exact ⟨hm s, by simpa using (flowerIncidence_iff_mem i s).mp h⟩
      | inr t => exact False.elim h

/-- No deletion leaves a cycle, so the exhibited feedback set of size one
is minimum, rather than just a size-one upper bound. -/
theorem flower_empty_feedback_not_acyclic (n : ℕ) (hn : 2 ≤ n) :
    ¬ (feedbackIncidence (∅ : Finset (Coord n)) (supports n)).IsAcyclic := by
  intro h
  exact flower_not_acyclic n hn (h.comap (flowerFullHom n)
    (Sum.map_injective.mpr ⟨Function.injective_id, flowerFactorScope_injective n⟩))

/-- No gap constant below two works for all actual feedback-one flowers. -/
theorem feedback_one_sharp (C : ℝ)
    (hC : ∀ n : ℕ, 2 ≤ n → ∀ F : Finset (Coord n), F.card = 1 →
      (feedbackIncidence F (supports n)).IsAcyclic →
      termwiseGap (supports n) (means n) ≤ C * hullGap (polynomial n) (means n)) :
    2 ≤ C := by
  apply universal_constant_ge_two C
  intro n hn
  exact hC n hn (flowerFeedback n) (flowerFeedback_card n) (flower_feedback_acyclic n)

end
end MultilinearGap.StructuralSharpness
