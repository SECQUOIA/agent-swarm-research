import Formal.NetworkSimplex.ThresholdObservedRunSize
import Formal.NetworkSimplex.ThresholdObservedHull
import Formal.NetworkSimplex.ThresholdResults
import Formal.NetworkSimplex.ThresholdObservedParameterCost

/-! Actual cached observed-label membership and compact recovery, with query work. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open NetworkSimplex.ThresholdGrouping NetworkSimplex.ThresholdOracle
variable {m L : ℕ}

/-- Check all original weights, including the separately stored residual. -/
def originalWeightsRun (D : RationalData m L) : Bool × ℕ :=
  let scan := weightScan (List.ofFn D.weights)
  (scan.2.1 && decide (scan.1 = 1), scan.2.2 + 2)

theorem originalWeightsRun_correct (D : RationalData m L) :
    (originalWeightsRun D).1 = true ↔ Simplex D.toReal.weights := by
  simp only [originalWeightsRun, Bool.and_eq_true, decide_eq_true_eq,
    weightScan_nonneg, weightScan_sum, List.sum_ofFn, List.mem_ofFn,
    forall_exists_index, forall_apply_eq_imp_iff]
  change ((∀ j, 0 ≤ D.weights j) ∧ ∑ j, D.weights j = 1) ↔
    ((∀ j, 0 ≤ (D.weights j : ℝ)) ∧ ∑ j, (D.weights j : ℝ) = 1)
  constructor
  · rintro ⟨hn, hs⟩
    exact ⟨fun j => by exact_mod_cast hn j, by exact_mod_cast hs⟩
  · rintro ⟨hn, hs⟩
    exact ⟨fun j => by exact_mod_cast hn j, by exact_mod_cast hs⟩

theorem originalWeightsRun_work (D : RationalData m L) :
    (originalWeightsRun D).2 = 3 * (m + 1) + 2 := by
  simp [originalWeightsRun, weightScan_work]

/-- The cache and original-simplex scan are shared; the fixed-parameter circuit
library is supplied from preprocessing. Compressed residual sums are never
recomputed by the downstream oracle. -/
def observedMembership (D : RationalData m L) (labels : List (Fin m))
    (library : List (Circuit (normalKeyCount labels.toFinset.card))) : Bool × ℕ :=
  let cache := D.observedCache labels
  let admission := originalWeightsRun D
  let core := runCachedSize cache (fun _ D lib => membershipRun D lib) library
  (admission.1 && core.1, cache.work + admission.2 + core.2)

theorem observedMembership_correct (D : RationalData m L) (labels : List (Fin m))
    (hJ : D.CoversObservations labels.toFinset) :
    (observedMembership D labels (generalLibrary labels.toFinset.card)).1 = true ↔
      D.toReal.graphPoint ∈ convexHull ℝ D.toReal.graph := by
  simp only [observedMembership, runCachedSize_eq, Bool.and_eq_true, originalWeightsRun_correct,
    RationalData.observedCache_data,
    membershipRun_correct _ (D.compressObserved_residual_class _)
      (D.compressObserved_residual_bypass _)]
  exact (D.compressObserved_hull_iff _ hJ).symm

/-- Original weights are stored once; all unused states reference compressed
atom zero. The compact representation does not materialize the dense expansion. -/
structure ObservedRecovery (m a L : ℕ) where
  weights : Vector ℚ (m + 1)
  cache : RationalData.ObservedCache m a L
  reduced : ProfileRecovery a L

def observedWitness (D : RationalData m L) (labels : List (Fin m))
    (bases : List (CachedBasis (normalKeyCount labels.toFinset.card) labels.toFinset.card)) :
    Option (ObservedRecovery m labels.toFinset.card L) × ℕ :=
  let cache := D.observedCache labels
  let admission := originalWeightsRun D
  if admission.1 then
    let core := runCachedSize cache (fun _ D bs => checkedWitness D bs) bases
    (core.1.map (fun r => ⟨Vector.ofFn D.weights, cache, r⟩),
      cache.work + admission.2 + core.2 + (m + 1))
  else (none, cache.work + admission.2)

theorem observedWitness_success_iff (D : RationalData m L) (labels : List (Fin m))
    (hJ : D.CoversObservations labels.toFinset) :
    (∃ out, (observedWitness D labels (packedBasisLibrary labels.toFinset.card)).1 = some out) ↔
      D.toReal.graphPoint ∈ convexHull ℝ D.toReal.graph := by
  rw [D.compressObserved_hull_iff _ hJ]
  simp only [observedWitness, runCachedSize_eq]
  split
  · rename_i hw
    have hs := (originalWeightsRun_correct D).mp hw
    rw [and_iff_right hs]
    constructor
    · rintro ⟨out, ho⟩
      obtain ⟨r, hr, _⟩ := Option.map_eq_some_iff.mp ho
      rw [RationalData.observedCache_data] at hr
      exact (checkedWitness_success_iff _ (D.compressObserved_residual_class _)
        (D.compressObserved_residual_bypass _)).mp ⟨r,hr⟩
    · intro h
      obtain ⟨r,hr⟩ := (checkedWitness_success_iff _ (D.compressObserved_residual_class _)
        (D.compressObserved_residual_bypass _)).mpr h
      refine ⟨⟨Vector.ofFn D.weights, D.observedCache labels, r⟩, ?_⟩
      rw [RationalData.observedCache_data, hr]
      rfl
  · rename_i hw
    have hs : ¬ Simplex D.toReal.weights := fun h => hw ((originalWeightsRun_correct D).mpr h)
    simp [hs]

theorem observedWitness_source (D : RationalData m L) (labels : List (Fin m))
    (bases : List (CachedBasis (normalKeyCount labels.toFinset.card) labels.toFinset.card))
    {out : ObservedRecovery m labels.toFinset.card L}
    (ho : (observedWitness D labels bases).1 = some out) :
    Simplex D.toReal.weights ∧ out.weights = Vector.ofFn D.weights ∧
      out.cache = D.observedCache labels ∧
      (checkedWitness (D.compressObserved labels.toFinset) bases).1 = some out.reduced := by
  simp only [observedWitness, runCachedSize_eq] at ho
  split at ho
  · rename_i hw
    obtain ⟨r,hr,he⟩ := Option.map_eq_some_iff.mp ho
    subst out
    exact ⟨(originalWeightsRun_correct D).mp hw, rfl, rfl,
      by simpa only [RationalData.observedCache_data] using hr⟩
  · contradiction

/-- Uniform bound also covers zero observed labels. -/
theorem membershipRun_uniform_charge (D : RationalData m L) :
    (membershipRun D (generalLibrary m)).2 ≤
      40 * (m + 1) * (L + 1) + 2 ^ (4 * (m + 1) ^ 2) * (2 * m + 3) := by
  have hd := D.arithmeticCharge_le
  have hg := (group_cost (D.indexedRows packNormal)).1
  rw [D.indexedRows_length packNormal] at hg
  have hc := circuitOracle_cost (packedGroup D).table.get (fun r => r.value) (generalLibrary m)
  have hl := generalLibrary_charge m
  have hdom := D.domainRun_charge
  change D.domainRun.2 + (D.arithmeticCharge +
    (group (D.indexedRows packNormal)).comparisons +
    (circuitOracle (packedGroup D).table.get (fun r => r.value) (generalLibrary m)).2) ≤ _
  rw [hdom]
  nlinarith

theorem observedMembership_work (D : RationalData m L) (labels : List (Fin m)) :
    (observedMembership D labels (generalLibrary labels.toFinset.card)).2 ≤
      15 * m + 5 * labels.length + 70 * (labels.toFinset.card + 1) * (L + 1) + 15 +
        2 ^ (4 * (labels.toFinset.card + 1) ^ 2) * (2 * labels.toFinset.card + 3) := by
  have hp := D.observedCache_work labels
  have hc := membershipRun_uniform_charge (D.observedCache labels).data
  simp only [observedMembership, runCachedSize_eq]
  change (D.observedCache labels).work + (originalWeightsRun D).2 + _ ≤ _
  rw [originalWeightsRun_work]
  nlinarith

/-- The basis scan has the same uniform treatment of dimension zero. -/
theorem recoverPackedProfile_uniform_charge (D : RationalData m L) :
    (recoverPackedProfile D (packedBasisLibrary m)).2 ≤ 26 * (m + 1) * (L + 1) +
      normalKeyCount m + normalKeyCount m ^ m * basisTrialCharge (normalKeyCount m) m := by
  have hd := D.arithmeticCharge_le
  have hg := (group_cost (D.indexedRows packNormal)).1
  rw [D.indexedRows_length packNormal] at hg
  have hc := recoverFromCache_charge (keyNormalRat m) (packedRationalTable D).get
  change D.arithmeticCharge + (group (D.indexedRows packNormal)).comparisons +
    normalKeyCount m + (scanBases (keyNormalRat m) (packedRationalTable D).get
      (basisLibrary (keyNormalRat m))).2 ≤ _
  nlinarith

theorem recoverWitness_uniform_charge (D : RationalData m L) :
    (recoverWitness D (packedBasisLibrary m)).2 ≤ 42 * (m + 1) * (L + 1) +
      normalKeyCount m + normalKeyCount m ^ m * basisTrialCharge (normalKeyCount m) m := by
  have hp := recoverPackedProfile_uniform_charge D
  dsimp only [recoverWitness]
  split
  · dsimp only
    nlinarith
  · rename_i x _
    have hx := recoverProfile_work D x
    dsimp only
    nlinarith

theorem checkedWitness_uniform_charge (D : RationalData m L) :
    (checkedWitness D (packedBasisLibrary m)).2 ≤ 60 * (m + 1) * (L + 1) +
      normalKeyCount m + normalKeyCount m ^ m * basisTrialCharge (normalKeyCount m) m := by
  have h := recoverWitness_uniform_charge D
  dsimp only [checkedWitness]
  split <;> simp only <;> rw [D.domainRun_charge] <;> nlinarith

/-- Bookkeeping, the complete compressed recovery and copying all original
weights are included. Dense state/arc expansion is not executed. -/
theorem observedWitness_work (D : RationalData m L) (labels : List (Fin m)) :
    (observedWitness D labels (packedBasisLibrary labels.toFinset.card)).2 ≤
      16 * m + 5 * labels.length + 90 * (labels.toFinset.card + 1) * (L + 1) + 16 +
        normalKeyCount labels.toFinset.card +
        normalKeyCount labels.toFinset.card ^ labels.toFinset.card *
          basisTrialCharge (normalKeyCount labels.toFinset.card) labels.toFinset.card := by
  have hp := D.observedCache_work labels
  have hc := checkedWitness_uniform_charge (D.observedCache labels).data
  simp only [observedWitness, runCachedSize_eq]
  split <;> simp only <;> rw [originalWeightsRun_work] <;> nlinarith

/-- Explicit fixed-observed-parameter separation/membership scale. -/
theorem observedMembership_work_exp (D : RationalData m L) (labels : List (Fin m)) :
    (observedMembership D labels (generalLibrary labels.toFinset.card)).2 ≤
      15 * m + 5 * labels.length + 70 * (labels.toFinset.card + 1) * (L + 1) + 15 +
        2 ^ (8 * (labels.toFinset.card + 2) ^ 2) :=
  (observedMembership_work D labels).trans
    (Nat.add_le_add_left (observed_circuit_parameter_bound labels.toFinset.card) _)

theorem observedWitness_work_exp (D : RationalData m L) (labels : List (Fin m)) :
    (observedWitness D labels (packedBasisLibrary labels.toFinset.card)).2 ≤
      16 * m + 5 * labels.length + 90 * (labels.toFinset.card + 1) * (L + 1) + 16 +
        2 ^ (8 * (labels.toFinset.card + 2) ^ 2) := by
  have h := observedWitness_work D labels
  have hp := observed_basis_parameter_bound labels.toFinset.card
  omega

end NetworkSimplex.Chain.Threshold
