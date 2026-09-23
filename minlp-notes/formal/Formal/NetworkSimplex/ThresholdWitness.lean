import Formal.NetworkSimplex.ThresholdPackedRecovery
import Formal.NetworkSimplex.ThresholdRecoveryPipeline

/-! End-to-end executable rational graph recovery from the original grouped rows. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
variable {m L : ℕ}

/-- The cache is supplied from parameter-only preprocessing. Success stores the
actual greedy disaggregation and normalized atoms, rather than merely a profile. -/
def recoverWitness (D : RationalData m L)
    (cache : List (CachedBasis (normalKeyCount m) m)) : Option (ProfileRecovery m L) × ℕ :=
  let p := recoverPackedProfile D cache
  match p.1 with
  | none => (none, p.2)
  | some x =>
    let out := recoverProfile D x
    (some out, p.2 + out.work)

theorem recoverWitness_source (D : RationalData m L)
    (cache : List (CachedBasis (normalKeyCount m) m)) {out : ProfileRecovery m L}
    (ho : (recoverWitness D cache).1 = some out) :
    ∃ x, (recoverPackedProfile D cache).1 = some x ∧ out = recoverProfile D x := by
  dsimp only [recoverWitness] at ho
  split at ho
  · contradiction
  · rename_i x hx
    exact ⟨x, hx, (Option.some.inj ho).symm⟩

/-- Every accepted original-domain query produces graph atoms with exact original moments. -/
theorem recoverWitness_sound (D : RationalData m L)
    (cache : List (CachedBasis (normalKeyCount m) m)) {out : ProfileRecovery m L}
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (hd : D.toReal.OriginalDomain) (ho : (recoverWitness D cache).1 = some out) :
    (∀ j, out.graphPoint D j ∈ D.toReal.graph) ∧
    Simplex (fun j => (D.weights j : ℝ)) ∧
    (∑ j, (D.weights j : ℝ) • out.graphPoint D j = D.toReal.graphPoint) ∧
    Fintype.card (Fin (m + 1)) = m + 1 := by
  obtain ⟨x, hx, rfl⟩ := recoverWitness_source D cache ho
  exact recoverProfile_decomposition D x hc hh hd (recoverPackedProfile_sound D cache hx)

/-- The actual program succeeds on every hull point, including lower-dimensional profiles. -/
theorem recoverWitness_complete (D : RationalData m L)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (h : D.toReal.graphPoint ∈ convexHull ℝ D.toReal.graph) :
    ∃ out, (recoverWitness D (packedBasisLibrary m)).1 = some out := by
  have hp := (D.toReal.exists_fullProfile_iff_rows hc hh).mp ((D.toReal.mem_hull_iff.mp h).2)
  have hr : ∃ x, D.toReal.ReducedProfile x := by
    obtain ⟨x, hx⟩ := hp
    exact ⟨x, (D.toReal.rows_iff_reducedProfile x).mp hx⟩
  obtain ⟨x, hx, _⟩ := recoverPackedProfile_complete D hr
  exact ⟨recoverProfile D x, by simp [recoverWitness, hx]⟩

/-- Admission plus actual successful recovery is equivalent to original hull membership. -/
theorem recoverWitness_success_iff (D : RationalData m L)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (hd : D.toReal.OriginalDomain) :
    (∃ out, (recoverWitness D (packedBasisLibrary m)).1 = some out) ↔
      D.toReal.graphPoint ∈ convexHull ℝ D.toReal.graph := by
  constructor
  · rintro ⟨out, ho⟩
    obtain ⟨x, hx, _⟩ := recoverWitness_source D (packedBasisLibrary m) ho
    exact D.toReal.mem_hull_iff.mpr ⟨hd, _,
      recoverProfile_fullProfile D x hc hh (recoverPackedProfile_sound D _ hx)⟩
  · exact recoverWitness_complete D hc hh

/-- Fixed-dimension preprocessing is excluded; every query-stage arithmetic ledger is included. -/
theorem recoverWitness_work (D : RationalData m L) (hm : 1 ≤ m) :
    (recoverWitness D (packedBasisLibrary m)).2 ≤
      26 * m * (L + 1) + normalKeyCount m +
      (normalKeyCount m) ^ m * basisTrialCharge (normalKeyCount m) m +
      (m + 3 + L * (9 * (m + 1) + 1) + (m + 1) + (m + 1) * (2 * L + 2)) := by
  have hp := recoverPackedProfile_charge D hm
  dsimp only [recoverWitness]
  split
  · dsimp only
    omega
  · rename_i x _
    have hx := recoverProfile_work D x
    dsimp only
    omega

end NetworkSimplex.Chain.Threshold
