import Formal.NetworkSimplex.ThresholdObservedAlgorithm
import Formal.NetworkSimplex.ThresholdObservedReal
import Formal.NetworkSimplex.ThresholdWeightSeparator
import Formal.NetworkSimplex.ThresholdSeparation

/-! Exact separation in the original ambient coordinates after observed-label compression. -/
namespace NetworkSimplex.Chain.Threshold
open NetworkSimplex.ThresholdOracle
variable {m L : ℕ}

abbrev ObservedCut (m a L : ℕ) := WeightCut m ⊕ FullCut a L

/-- The fixed observation-index map supplies the compressed cut interpretation;
evaluation uses the same affine substitution at every candidate point. -/
noncomputable def ObservedCut.valueAt (J : Finset (Fin m))
    (cut : ObservedCut m J.card L) (E : ReductionData m (Fin L)) : ℝ :=
  match cut with
  | .inl weight => weight.value E.weights
  | .inr compressed => compressed.valueAt (E.compressObserved J)

def observedSeparate (D : RationalData m L) (labels : List (Fin m))
    (library : List (Circuit (normalKeyCount labels.toFinset.card))) :
    Option (ObservedCut m labels.toFinset.card L) × ℕ :=
  let cache := D.observedCache labels
  let weights := weightSeparator D.weights
  match weights.1 with
  | some cut => (some (.inl cut), cache.work + weights.2)
  | none =>
    let core := runCachedSize cache (fun _ D lib => separateGeneral D lib) library
    (core.1.map Sum.inr, cache.work + weights.2 + core.2)

theorem observedSeparate_none_iff (D : RationalData m L) (labels : List (Fin m))
    (hJ : D.CoversObservations labels.toFinset) :
    (observedSeparate D labels (generalLibrary labels.toFinset.card)).1 = none ↔
      D.toReal.graphPoint ∈ convexHull ℝ D.toReal.graph := by
  rw [D.compressObserved_hull_iff _ hJ]
  cases hw : (weightSeparator D.weights).1 with
  | none =>
    have hs : Simplex D.toReal.weights := (weightSeparator_none D.weights).mp hw
    simp only [observedSeparate, runCachedSize_eq, hw, Option.map_eq_none_iff, hs, true_and,
      RationalData.observedCache_data]
    exact separateGeneral_none_iff _ (D.compressObserved_residual_class _)
      (D.compressObserved_residual_bypass _)
  | some w =>
    have hs : ¬ Simplex D.toReal.weights := by
      intro h
      have hn := (weightSeparator_none D.weights).mpr h
      rw [hw] at hn
      contradiction
    simp [observedSeparate, hw, hs]

/-- Every returned fixed cut is violated at the query and valid at every real
hull point of the original observation pattern, with all unused labels present. -/
theorem observedSeparate_sound (D : RationalData m L) (labels : List (Fin m))
    (hJ : D.CoversObservations labels.toFinset)
    {cut : ObservedCut m labels.toFinset.card L}
    (ho : (observedSeparate D labels (generalLibrary labels.toFinset.card)).1 = some cut) :
    cut.valueAt labels.toFinset D.toReal < 0 ∧
      ∀ E : ReductionData m (Fin L), D.c = E.c → D.observedH = E.observedH →
        E.graphPoint ∈ convexHull ℝ E.graph → 0 ≤ cut.valueAt labels.toFinset E := by
  cases hw : (weightSeparator D.weights).1 with
  | some w =>
    have he : Sum.inl w = cut := by simpa [observedSeparate, runCachedSize_eq, hw] using ho
    subst cut
    obtain ⟨hn,hv⟩ := weightSeparator_some D.weights hw
    exact ⟨hn, fun E _ _ h => hv E.weights (E.mem_hull_iff.mp h).1.1⟩
  | none =>
    have hr : ((separateGeneral (D.compressObserved labels.toFinset)
        (generalLibrary labels.toFinset.card)).1.map Sum.inr) = some cut := by
      simpa only [observedSeparate, runCachedSize_eq, hw, RationalData.observedCache_data] using ho
    obtain ⟨c,hc,rfl⟩ := Option.map_eq_some_iff.mp hr
    obtain ⟨hn,hv⟩ := separateGeneral_sound (D.compressObserved labels.toFinset)
      (D.compressObserved_residual_class _) (D.compressObserved_residual_bypass _) hc
    constructor
    · simpa only [ObservedCut.valueAt, RationalData.compressObserved_toReal] using hn
    · intro E hclass hbypass hmem
      have hE := hJ.toReal.of_pattern_eq hclass hbypass
      have hcompressed := (E.compressObserved_hull_iff labels.toFinset hE).mp hmem |>.2
      have hp := D.toReal.compressObserved_pattern_eq E labels.toFinset hclass hbypass
      apply hv (E.compressObserved labels.toFinset) ?_ ?_ hcompressed
      · simpa only [ReductionData.compressObserved, RationalData.compressObserved,
          RationalData.toReal] using hp.1
      · simpa only [ReductionData.compressObserved, RationalData.compressObserved,
          RationalData.toReal] using hp.2

theorem separateGeneral_uniform_work (D : RationalData m L) :
    (separateGeneral D (generalLibrary m)).2 ≤ 80 * (m + 1) * (L + 1) +
      2 ^ (8 * (m + 2) ^ 2) := by
  have hp := membershipRun_uniform_charge D
  have hb := observed_circuit_parameter_bound m
  have hd := D.domainSeparator_charge_le
  have hg : (generalOracle D (generalLibrary m)).2 ≤
      (membershipRun D (generalLibrary m)).2 := by
    change _ ≤ D.domainRun.2 + _
    omega
  cases h : D.domainSeparator.1 <;> simp only [separateGeneral, h] <;> nlinarith

theorem observedSeparate_work (D : RationalData m L) (labels : List (Fin m)) :
    (observedSeparate D labels (generalLibrary labels.toFinset.card)).2 ≤
      14 * m + 5 * labels.length + 110 * (labels.toFinset.card + 1) * (L + 1) + 16 +
        2 ^ (8 * (labels.toFinset.card + 2) ^ 2) := by
  have hc := D.observedCache_work labels
  have hp := separateGeneral_uniform_work (D.observedCache labels).data
  cases h : (weightSeparator D.weights).1 <;>
    simp only [observedSeparate, runCachedSize_eq, h] <;> rw [weightSeparator_work] <;> nlinarith

end NetworkSimplex.Chain.Threshold
