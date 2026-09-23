import Formal.NetworkSimplex.ThresholdObservedHull

/-! Observed-state compression for arbitrary real query points. -/
namespace NetworkSimplex
open scoped BigOperators
namespace Chain.ReductionData
open Chain.Threshold
noncomputable section
variable {m L : ℕ}

/-- Restrict observed states and merge all remaining mass with the residual.
The selected states are retained even when their weight is zero. -/
def compressObserved {m L : ℕ} (D : ReductionData m (Fin L)) (J : Finset (Fin m)) :
    ReductionData J.card (Fin L) where
  c i := Fin.cases .neither (fun j => D.c i (observedIndex J j).val.succ)
  u i := Fin.cases 0 (fun j => D.u i (observedIndex J j).val.succ)
  v i := Fin.cases 0 (fun j => D.v i (observedIndex J j).val.succ)
  weights := Fin.cases (1 - ∑ j : Fin J.card, D.weights (observedIndex J j).val.succ)
    (fun j => D.weights (observedIndex J j).val.succ)
  xa := D.xa
  xh := D.xh
  observedH := Fin.cases false (fun j => D.observedH (observedIndex J j).val.succ)
  zh := Fin.cases 0 (fun j => D.zh (observedIndex J j).val.succ)



/-- Every structural observation is retained, independently of its weight. -/
def CoversObservations (D : ReductionData m (Fin L)) (J : Finset (Fin m)) : Prop :=
  (∀ i, D.c i 0 = .neither) ∧ D.observedH 0 = false ∧
  ∀ j, j ∉ J → (∀ i, D.c i j.succ = .neither) ∧ D.observedH j.succ = false

def observedEmbed (J : Finset (Fin m)) : Fin (J.card + 1) → Fin (m + 1) :=
  Fin.cases 0 (fun j => (observedIndex J j).val.succ)

theorem compressed_selected (D : ReductionData m (Fin L)) (J : Finset (Fin m))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (e : ChainArc L) (k : Fin (J.card + 1)) :
    Selected (D.compressObserved J).c (fun j => (D.compressObserved J).observedH j = true) (e,k) ↔
      Selected D.c (fun j => D.observedH j = true) (e, observedEmbed J k) := by
  refine Fin.cases ?_ (fun j => ?_) k
  · rcases e with ⟨i,flag⟩ | h
    · cases flag <;> simp [Selected, compressObserved, observedEmbed, hc, observesA, observesB]
    · simp [Selected, compressObserved, observedEmbed, hh]
  · rcases e with ⟨i,flag⟩ | h
    · cases flag <;> rfl
    · rfl

def compressedObservation (D : ReductionData m (Fin L)) (J : Finset (Fin m))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    Observation (D.compressObserved J).c (fun j => (D.compressObserved J).observedH j = true) →
      Observation D.c (fun j => D.observedH j = true) :=
  fun o => ⟨(o.val.1, observedEmbed J o.val.2),
    (compressed_selected D J hc hh o.val.1 o.val.2).mp o.property⟩

theorem compressedObservation_surjective (D : ReductionData m (Fin L)) (J : Finset (Fin m))
    (hJ : D.CoversObservations J) :
    Function.Surjective (D.compressedObservation J hJ.1 hJ.2.1) := by
  rintro ⟨⟨e,k⟩,hs⟩
  have hk : ∃ j : Fin m, k = j.succ ∧ j ∈ J := by
    revert hs
    refine Fin.cases ?_ (fun j => ?_) k
    · intro hs
      rcases e with ⟨i,flag⟩ | h
      · cases flag <;> simp [Selected, hJ.1, observesA, observesB] at hs
      · simp [Selected, hJ.2.1] at hs
    · intro hs
      refine ⟨j, rfl, ?_⟩
      by_contra hn
      rcases e with ⟨i,flag⟩ | h
      · cases flag <;> simp [Selected, (hJ.2.2 j hn).1, observesA, observesB] at hs
      · simp [Selected, (hJ.2.2 j hn).2] at hs
  obtain ⟨j, rfl, hj⟩ := hk
  let k := ((observedIndex J).symm ⟨j,hj⟩).succ
  have he : observedEmbed J k = j.succ := by simp [k, observedEmbed]
  refine ⟨⟨(e,k), (compressed_selected D J hJ.1 hJ.2.1 e k).mpr ?_⟩, ?_⟩
  · simpa [he] using hs
  · apply Subtype.ext
    simp [compressedObservation, he]

theorem observedEmbed_group (J : Finset (Fin m)) (k : Fin (J.card + 1)) :
    observedStateIndex J (observedGroup J (observedEmbed J k)) = k := by
  refine Fin.cases ?_ (fun j => ?_) k
  · exact observedStateIndex_none J
  · simp [observedEmbed, observedGroup_succ]

theorem compressed_weights (D : ReductionData m (Fin L)) (J : Finset (Fin m))
    (hw : Simplex D.weights) (k : Fin (J.card + 1)) :
    (D.compressObserved J).weights k =
      groupSum (observedGroup J) D.weights ((observedStateIndex J).symm k) := by
  refine Fin.cases ?_ (fun j => ?_) k
  · have he : (observedStateIndex J).symm 0 = none :=
      (observedStateIndex J).symm_apply_eq.mpr (observedStateIndex_none J).symm
    rw [he, merged_residual_weight J _ hw]
    change (1 - ∑ j : Fin J.card, D.weights (observedIndex J j).val.succ) = _
    congr 1
    exact (observedIndex J).sum_comp (fun j => D.weights j.val.succ)
  · have he : (observedStateIndex J).symm j.succ = some (observedIndex J j) :=
      (observedStateIndex J).symm_apply_eq.mpr (by simp)
    rw [he, observed_weight]
    rfl

/-- Compression changes precisely the state weights and their labels. Every
flow coordinate and every structurally observed product is retained. -/
theorem compressed_point (D : ReductionData m (Fin L)) (J : Finset (Fin m))
    (hJ : D.CoversObservations J) (hw : Simplex D.weights) :
    let p := relabelPoint (observedStateIndex J)
      (mergedPoint (observedGroup J) D.graphPoint)
    (p.1, p.2.1, p.2.2 ∘ D.compressedObservation J hJ.1 hJ.2.1) =
      (D.compressObserved J).graphPoint := by
  dsimp only
  apply Prod.ext
  · rfl
  · apply Prod.ext
    · funext k
      exact (compressed_weights D J hw k).symm
    · funext o
      rcases o with ⟨⟨e,k⟩,hs⟩
      revert hs
      refine Fin.cases ?_ (fun j => ?_) k
      · intro hs
        rcases e with ⟨i,flag⟩ | h
        · cases flag <;> simp [Selected, compressObserved, observesA, observesB] at hs
        · simp [Selected, compressObserved] at hs
      · intro hs
        rcases e with ⟨i,flag⟩ | h
        · cases flag <;> rfl
        · rfl

/-- The executable rational compression is the exact original chain hull
reduction. The entire original simplex remains a separate prerequisite. -/
theorem compressObserved_hull_iff (D : ReductionData m (Fin L)) (J : Finset (Fin m))
    (hJ : D.CoversObservations J) :
    D.graphPoint ∈ convexHull ℝ D.graph ↔
      Simplex D.weights ∧
        (D.compressObserved J).graphPoint ∈ convexHull ℝ
          (D.compressObserved J).graph := by
  let g := observedGroup J
  let e := observedStateIndex J
  let f := D.compressedObservation J hJ.1 hJ.2.1
  have hf := D.compressedObservation_surjective J hJ
  have ho : ∀ (o : Observation D.c (fun j => D.observedH j = true)) k,
      g k = g o.val.2 → k = o.val.2 := by
    intro o k hk
    obtain ⟨⟨⟨arc,j⟩,hs⟩,rfl⟩ := hf o
    change g k = g (observedEmbed J j) at hk
    change k = observedEmbed J j
    revert hs hk
    refine Fin.cases ?_ (fun j => ?_) j
    · intro hs hk
      rcases arc with ⟨i,flag⟩ | h
      · cases flag <;> simp [Selected, compressObserved, observesA, observesB] at hs
      · simp [Selected, compressObserved] at hs
    · intro hs hk
      apply (observedGroup_fiber J (observedIndex J j) k).mp
      simpa [g, observedEmbed, observedGroup_succ] using hk
  change D.graphPoint ∈ convexHull ℝ
    (Graph (incidence L) (demand L) (fun _ => 1) (fun o => o.val.1) (fun o => o.val.2)) ↔ _
  refine (hull_merge_iff g (A := incidence L) (b := demand L) (u := fun _ => 1)
    (arc := fun o : Observation D.c (fun j => D.observedH j = true) => o.val.1)
    (p := D.graphPoint) ho).trans ?_
  apply and_congr_right
  intro hw
  refine (relabel_mem_hull_iff (incidence L) (demand L) (fun _ => 1)
    (fun o => o.val.1) (g ∘ fun o => o.val.2) e
    (mergedPoint g D.graphPoint)).symm.trans ?_
  refine (hull_observation_surjective (incidence L) (demand L) (fun _ => 1)
    (fun o => o.val.1) (e ∘ g ∘ fun o => o.val.2)
    (relabelPoint e (mergedPoint g D.graphPoint)) f hf).symm.trans ?_
  have hp := compressed_point D J hJ hw
  change (_, _, _) ∈ _ ↔ _
  with_unfolding_all rw [hp]
  have he : (e ∘ g ∘ (fun o => o.val.2)) ∘ f =
      (fun o : Observation (D.compressObserved J).c
        (fun j => (D.compressObserved J).observedH j = true) => o.val.2) := by
    funext o
    exact observedEmbed_group J o.val.2
  exact Iff.of_eq (congrArg (fun state => (D.compressObserved J).graphPoint ∈
    convexHull ℝ (Graph (incidence L) (demand L) (fun _ => 1)
      (fun o : Observation (D.compressObserved J).c
        (fun j => (D.compressObserved J).observedH j = true) => o.val.1) state)) he)

/-- Structural coverage transfers to every real point of the same instance. -/
theorem CoversObservations.of_pattern_eq {D E : ReductionData m (Fin L)}
    {J : Finset (Fin m)} (h : D.CoversObservations J)
    (hc : D.c = E.c) (hh : D.observedH = E.observedH) : E.CoversObservations J := by
  simpa only [CoversObservations, ← hc, ← hh] using h

theorem compressObserved_pattern_eq (D E : ReductionData m (Fin L)) (J : Finset (Fin m))
    (hc : D.c = E.c) (hh : D.observedH = E.observedH) :
    (D.compressObserved J).c = (E.compressObserved J).c ∧
      (D.compressObserved J).observedH = (E.compressObserved J).observedH := by
  simp only [compressObserved, hc, hh, and_self]

end
end Chain.ReductionData

namespace Chain.Threshold.RationalData
variable {m L : ℕ}

/-- The executable rational compression is the restriction of the real map. -/
theorem compressObserved_toReal (D : RationalData m L) (J : Finset (Fin m)) :
    (D.compressObserved J).toReal = D.toReal.compressObserved J := by
  unfold toReal compressObserved ReductionData.compressObserved
  congr 1
  · funext i j
    refine Fin.cases ?_ (fun k => ?_) j <;> simp
  · funext i j
    refine Fin.cases ?_ (fun k => ?_) j <;> simp
  · funext j
    refine Fin.cases ?_ (fun k => ?_) j <;> simp
  · funext j
    refine Fin.cases ?_ (fun k => ?_) j <;> simp

theorem CoversObservations.toReal {D : RationalData m L} {J : Finset (Fin m)}
    (h : D.CoversObservations J) : D.toReal.CoversObservations J := h

end Chain.Threshold.RationalData
end NetworkSimplex
