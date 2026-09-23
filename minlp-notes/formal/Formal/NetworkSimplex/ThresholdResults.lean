import Formal.NetworkSimplex.ThresholdDomainRun
import Formal.NetworkSimplex.ThresholdGeneralPacked
import Formal.NetworkSimplex.ThresholdWitness

/-! Original-domain admission composed with the executable profile oracles and recovery. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
variable {m L : ℕ}

/-- The circuit cache is produced once for the dimension, outside the query. -/
def membershipRun (D : RationalData m L)
    (library : List (NetworkSimplex.ThresholdOracle.Circuit (normalKeyCount m))) : Bool × ℕ :=
  let domain := D.domainRun
  let profile := generalOracle D library
  (domain.1 && profile.1.isNone, domain.2 + profile.2)

theorem membershipRun_correct (D : RationalData m L)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    (membershipRun D (generalLibrary m)).1 = true ↔
      D.toReal.graphPoint ∈ convexHull ℝ D.toReal.graph := by
  simp only [membershipRun, Bool.and_eq_true, Option.isNone_iff_eq_none,
    D.domainRun_correct, generalOracle_none_iff, D.toReal.mem_hull_iff,
    D.toReal.exists_fullProfile_iff_rows hc hh]
  exact and_congr_right fun _ => (exists_congr fun x => D.toReal.rows_iff_reducedProfile x).symm

theorem membershipRun_charge (D : RationalData m L) (hm : 1 ≤ m) :
    (membershipRun D (generalLibrary m)).2 ≤
      (2 * (m + 1) * L + 8 * L + 3 * (m + 1) + 4) +
      26 * m * (L + 1) + 2 ^ (4 * (m + 1) ^ 2) * (2 * m + 3) := by
  have h := generalOracle_charge D hm
  simp only [membershipRun, D.domainRun_charge]
  omega

/-- Recovery is returned only after the actual original-domain admission checks pass. -/
def checkedWitness (D : RationalData m L)
    (cache : List (CachedBasis (normalKeyCount m) m)) : Option (ProfileRecovery m L) × ℕ :=
  let domain := D.domainRun
  if domain.1 then
    let out := recoverWitness D cache
    (out.1, domain.2 + out.2)
  else (none, domain.2)

theorem checkedWitness_source (D : RationalData m L)
    (cache : List (CachedBasis (normalKeyCount m) m)) {out : ProfileRecovery m L}
    (h : (checkedWitness D cache).1 = some out) :
    D.toReal.OriginalDomain ∧ (recoverWitness D cache).1 = some out := by
  dsimp only [checkedWitness] at h
  split at h
  · rename_i hd
    exact ⟨D.domainRun_correct.mp hd, h⟩
  · contradiction

theorem checkedWitness_success_iff (D : RationalData m L)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    (∃ out, (checkedWitness D (packedBasisLibrary m)).1 = some out) ↔
      D.toReal.graphPoint ∈ convexHull ℝ D.toReal.graph := by
  constructor
  · rintro ⟨out, ho⟩
    obtain ⟨hd, hr⟩ := checkedWitness_source D _ ho
    exact (recoverWitness_success_iff D hc hh hd).mp ⟨out, hr⟩
  · intro h
    have hd := D.domainRun_correct.mpr (D.toReal.mem_hull_iff.mp h).1
    obtain ⟨out, ho⟩ := recoverWitness_complete D hc hh h
    exact ⟨out, by simp [checkedWitness, hd, ho]⟩

theorem checkedWitness_sound (D : RationalData m L)
    (cache : List (CachedBasis (normalKeyCount m) m)) {out : ProfileRecovery m L}
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (ho : (checkedWitness D cache).1 = some out) :
    (∀ j, out.graphPoint D j ∈ D.toReal.graph) ∧
    Simplex (fun j => (D.weights j : ℝ)) ∧
    (∑ j, (D.weights j : ℝ) • out.graphPoint D j = D.toReal.graphPoint) ∧
    Fintype.card (Fin (m + 1)) = m + 1 := by
  obtain ⟨hd, hr⟩ := checkedWitness_source D cache ho
  exact recoverWitness_sound D cache hc hh hd hr

theorem checkedWitness_charge (D : RationalData m L) (hm : 1 ≤ m) :
    (checkedWitness D (packedBasisLibrary m)).2 ≤
      (2 * (m + 1) * L + 8 * L + 3 * (m + 1) + 4) +
      (26 * m * (L + 1) + normalKeyCount m +
        normalKeyCount m ^ m * basisTrialCharge (normalKeyCount m) m +
        (m + 3 + L * (9 * (m + 1) + 1) + (m + 1) + (m + 1) * (2 * L + 2))) := by
  have h := recoverWitness_work D hm
  dsimp only [checkedWitness]
  split <;> simp only
  · rw [D.domainRun_charge]
    omega
  · rw [D.domainRun_charge]
    omega

end NetworkSimplex.Chain.Threshold
