import Formal.NetworkSimplex.ThresholdObservedAlgorithm
import Formal.NetworkSimplex.ThresholdCompactDecomposition

/-! The returned compact atoms reconstruct every original state and coordinate. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
variable {m L : ℕ}

/-- Mathematical semantics of the cached rank lookup: observed labels retain their
own normalized atom; all unused labels and the residual use atom zero. -/
def observedAtomIndex (J : Finset (Fin m)) (k : Fin (m + 1)) : Fin (J.card + 1) :=
  observedStateIndex J (observedGroup J k)

noncomputable def expandedObservedAtom (D : RationalData m L) (J : Finset (Fin m))
    (R : ProfileRecovery J.card L) (k : Fin (m + 1)) :
    Point (ChainArc L) (Fin (m + 1)) (Observation D.c (fun j => D.observedH j = true)) :=
  vertexAtom (fun o => o.val.1) (fun o => o.val.2)
    (R.atoms.get (observedAtomIndex J k)).flow k

theorem observedGroup_unique_observation (D : RationalData m L) (J : Finset (Fin m))
    (hJ : D.CoversObservations J) (o : Observation D.c (fun j => D.observedH j = true))
    (k : Fin (m + 1)) (hk : observedGroup J k = observedGroup J o.val.2) : k = o.val.2 := by
  obtain ⟨⟨⟨arc,j⟩,hs⟩,rfl⟩ := D.compressedObservation_surjective J hJ o
  change observedGroup J k = observedGroup J (RationalData.observedEmbed J j) at hk
  change k = RationalData.observedEmbed J j
  revert hs hk
  refine Fin.cases ?_ (fun j => ?_) j
  · intro hs hk
    rcases arc with ⟨i,flag⟩ | h
    · cases flag <;> simp [Selected, RationalData.compressObserved, observesA, observesB] at hs
    · simp [Selected, RationalData.compressObserved] at hs
  · intro hs hk
    apply (observedGroup_fiber J (observedIndex J j) k).mp
    simpa [RationalData.observedEmbed, observedGroup_succ] using hk

/-- Exact original-coordinate decomposition from the stored compressed atoms.
At zero merged weight the returned normalized atom remains a valid graph flow;
every constituent has zero weight, so it contributes zero to all moments. -/
theorem observed_recovery_decomposition (D : RationalData m L) (J : Finset (Fin m))
    (hJ : D.CoversObservations J) (hw : Simplex D.toReal.weights)
    (bases : List (CachedBasis (normalKeyCount J.card) J.card))
    {R : ProfileRecovery J.card L}
    (hr : (checkedWitness (D.compressObserved J) bases).1 = some R) :
    (∀ k, expandedObservedAtom D J R k ∈ D.toReal.graph) ∧
      ∑ k, (D.weights k : ℝ) • expandedObservedAtom D J R k = D.toReal.graphPoint := by
  let C := D.compressObserved J
  let flow := fun l : Option {j // j ∈ J} => (R.atoms.get (observedStateIndex J l)).flow
  have hs := checkedWitness_sound C bases (D.compressObserved_residual_class J)
    (D.compressObserved_residual_bypass J) hr
  have hf : ∀ l, Flow (incidence L) (demand L) (fun _ => 1) 1 (flow l) :=
    fun l => (hs.1 (observedStateIndex J l)).2.1
  have hsum : ∑ l, groupSum (observedGroup J) D.toReal.weights l •
      vertexAtom (fun o : Observation D.c (fun j => D.observedH j = true) => o.val.1)
        (observedGroup J ∘ fun o => o.val.2) (flow l) l =
      mergedPoint (observedGroup J) D.toReal.graphPoint := by
    apply Prod.ext
    · rw [weighted_vertexAtom_flow]
      have hflow := congrArg Prod.fst hs.2.2.1
      simp only [Prod.fst_sum, Prod.smul_fst, ProfileRecovery.graphPoint] at hflow
      have hwg (l) : groupSum (observedGroup J) D.toReal.weights l =
          C.toReal.weights (observedStateIndex J l) := by
        simpa only [Equiv.symm_apply_apply] using
          (D.compressed_weights J hw (observedStateIndex J l)).symm
      simp_rw [hwg]
      change (∑ l, (C.weights (observedStateIndex J l) : ℝ) •
        (R.atoms.get (observedStateIndex J l)).flow) = _
      rw [(observedStateIndex J).sum_comp (fun k => (C.weights k : ℝ) • (R.atoms.get k).flow)]
      exact hflow
    · apply Prod.ext
      · funext l
        simp only [Prod.snd_sum, Prod.fst_sum, Prod.smul_snd, Prod.smul_fst,
          Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
        simp [vertexAtom, mergedPoint, mul_ite]
        rfl
      · funext o
        rw [weighted_vertexAtom_product]
        obtain ⟨q,rfl⟩ := D.compressedObservation_surjective J hJ o
        have hi := RationalData.observedEmbed_group J q.val.2
        have hprod := congrArg (fun p => p.2.2 q) hs.2.2.1
        change (∑ k, (C.weights k : ℝ) •
          vertexAtom (fun o => o.val.1) (fun o => o.val.2)
            (R.atoms.get k).flow k).2.2 q = _ at hprod
        rw [weighted_vertexAtom_product] at hprod
        have hwg := D.compressed_weights J hw q.val.2
        have hindex : (observedStateIndex J).symm q.val.2 =
            observedGroup J (RationalData.observedEmbed J q.val.2) := by
          exact (observedStateIndex J).symm_apply_eq.mpr hi.symm
        rw [hindex] at hwg
        have hp := congrArg (fun p => p.2.2 q) (D.compressed_point J hJ hw)
        change D.toReal.graphPoint.2.2 (D.compressedObservation J hJ.1 hJ.2.1 q) =
          C.toReal.graphPoint.2.2 q at hp
        change groupSum (observedGroup J) D.toReal.weights
            (observedGroup J (RationalData.observedEmbed J q.val.2)) *
          (R.atoms.get (observedStateIndex J (observedGroup J
            (RationalData.observedEmbed J q.val.2)))).flow q.val.1 = _
        rw [hi, ← hwg]
        exact hprod.trans hp.symm
  exact compact_vertex_refinement (incidence L) (demand L) (fun _ => 1)
    (fun o : Observation D.c (fun j => D.observedH j = true) => o.val.1)
    (fun o : Observation D.c (fun j => D.observedH j = true) => o.val.2)
    (observedGroup J) D.toReal.graphPoint flow hf
    (observedGroup_unique_observation D J hJ) hsum

theorem observedWitness_decomposition (D : RationalData m L) (labels : List (Fin m))
    (hJ : D.CoversObservations labels.toFinset)
    (bases : List (CachedBasis (normalKeyCount labels.toFinset.card) labels.toFinset.card))
    {out : ObservedRecovery m labels.toFinset.card L}
    (ho : (observedWitness D labels bases).1 = some out) :
    (∀ k, expandedObservedAtom D labels.toFinset out.reduced k ∈ D.toReal.graph) ∧
      ∑ k, (out.weights.get k : ℝ) • expandedObservedAtom D labels.toFinset out.reduced k =
        D.toReal.graphPoint := by
  obtain ⟨hw,hweights,_,hr⟩ := observedWitness_source D labels bases ho
  rw [hweights]
  simpa only [Vector.get_ofFn] using
    observed_recovery_decomposition D labels.toFinset hJ hw bases hr

/-- Constant-time indexed flow lookup in the compact output. No original-state
by arc matrix is produced by the recovery program. -/
def ObservedRecovery.rationalFlow {a : ℕ} (out : ObservedRecovery m a L)
    (k : Fin (m + 1)) (arc : ChainArc L) : ℚ :=
  (out.reduced.atoms.get (out.cache.atomIndex k)).rationalFlow arc

noncomputable def ObservedRecovery.graphAtom {a : ℕ} (out : ObservedRecovery m a L)
    (D : RationalData m L) (k : Fin (m + 1)) :
    Point (ChainArc L) (Fin (m + 1)) (Observation D.c (fun j => D.observedH j = true)) :=
  vertexAtom (fun o => o.val.1) (fun o => o.val.2)
    (fun arc => (out.rationalFlow k arc : ℝ)) k

theorem observedWitness_graphAtom (D : RationalData m L) (labels : List (Fin m))
    (bases : List (CachedBasis (normalKeyCount labels.toFinset.card) labels.toFinset.card))
    {out : ObservedRecovery m labels.toFinset.card L}
    (ho : (observedWitness D labels bases).1 = some out) (k : Fin (m + 1)) :
    out.graphAtom D k = expandedObservedAtom D labels.toFinset out.reduced k := by
  obtain ⟨_,_,hc,_⟩ := observedWitness_source D labels bases ho
  simp only [ObservedRecovery.graphAtom, ObservedRecovery.rationalFlow,
    hc, RationalData.observedCache_atomIndex, rationalFlow_cast]
  rfl

/-- The actual cached-rank lookup, original weight vector and stored normalized
atoms give a full graph decomposition with exact original moments. -/
theorem observedWitness_cached_decomposition (D : RationalData m L)
    (labels : List (Fin m)) (hJ : D.CoversObservations labels.toFinset)
    (bases : List (CachedBasis (normalKeyCount labels.toFinset.card) labels.toFinset.card))
    {out : ObservedRecovery m labels.toFinset.card L}
    (ho : (observedWitness D labels bases).1 = some out) :
    (∀ k, out.graphAtom D k ∈ D.toReal.graph) ∧
      ∑ k, (out.weights.get k : ℝ) • out.graphAtom D k = D.toReal.graphPoint := by
  simp_rw [observedWitness_graphAtom D labels bases ho]
  exact observedWitness_decomposition D labels hJ bases ho

/-- Bound for the normalized decomposition payload: one flow per compressed state
and all original weights. This formula does not measure the full `ObservedRecovery`,
which also retains cached input, restored profiles, and unnormalized flows. -/
theorem observedWitness_compact_flow_size (m a L : ℕ) :
    (m + 1) + (a + 1) * (2 * L + 1) ≤
      3 * (a + 1) * (L + 1) + (m + 1) := by nlinarith

/-- Dense expansion would emit precisely one entry per original state and arc. -/
theorem observedWitness_dense_flow_size (m L : ℕ) :
    Fintype.card (Fin (m + 1) × ChainArc L) = (m + 1) * (2 * L + 1) := by
  simp [ChainArc]
  ring

end NetworkSimplex.Chain.Threshold
