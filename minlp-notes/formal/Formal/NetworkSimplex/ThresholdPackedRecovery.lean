import Formal.NetworkSimplex.ThresholdBasisOracle
import Formal.NetworkSimplex.ThresholdPackedOracle

/-! Complete executable recovery from the actual grouped original profile rows. -/

namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open NetworkSimplex.ThresholdGrouping
open Matrix

def keyNormalRat (m : ℕ) : Matrix (Fin (normalKeyCount m)) (Fin m) ℚ :=
  fun k j => (keyNormal k j : ℚ)

def packedRationalTable {m L : ℕ} (D : RationalData m L) :
    Vector (Option ℚ) (normalKeyCount m) :=
  Vector.ofFn (fun k => ((packedGroup D).table.get k).map (fun r => r.value))

@[simp] theorem packedRationalTable_get {m L : ℕ} (D : RationalData m L)
    (k : Fin (normalKeyCount m)) :
    (packedRationalTable D).get k = ((packedGroup D).table.get k).map (fun r => r.value) := by
  simp [packedRationalTable]

@[simp] theorem keyNormalRat_dot_cast {m : ℕ} (k : Fin (normalKeyCount m))
    (x : Fin m → ℝ) :
    (fun j => (keyNormalRat m k j : ℝ)) ⬝ᵥ x = keyValue k x := by
  simp [keyNormalRat, keyValue, dotProduct]

/-- Casting the actual grouped rational table recovers exactly the original reduced system. -/
theorem packed_realPartialSet_eq {m L : ℕ} (D : RationalData m L) :
    realPartialSet (keyNormalRat m) (packedRationalTable D).get =
      {x | D.toReal.ReducedProfile x} := by
  ext x
  change x ∈ realPartialSet (keyNormalRat m) (packedRationalTable D).get ↔
    D.toReal.ReducedProfile x
  rw [← packed_constraints D x]
  constructor
  · intro hx k r hr
    have ht : (packedRationalTable D).get k = some r.value := by simp [hr]
    simpa using hx k r.value ht
  · intro hx k b hb
    rw [packedRationalTable_get] at hb
    obtain ⟨r, hr, hv⟩ := Option.map_eq_some_iff.mp hb
    subst b
    simpa using hx k r hr

/-- The original coordinate box bounds every reduced-profile feasible set, even if empty. -/
theorem packed_realPartialSet_bounded {m L : ℕ} (D : RationalData m L) :
    Bornology.IsBounded (realPartialSet (keyNormalRat m) (packedRationalTable D).get) := by
  rw [packed_realPartialSet_eq]
  apply (Metric.isBounded_Icc (0 : Fin m → ℝ) (fun j => D.toReal.weights j.succ)).subset
  intro x hx
  exact ⟨fun j => (hx.1 j).1, fun j => (hx.1 j).2⟩

/-- The cache is fixed by dimension and is computed before processing query data. -/
def packedBasisLibrary (m : ℕ) : List (CachedBasis (normalKeyCount m) m) :=
  basisLibrary (keyNormalRat m)

/-- Group original rows, extract their cached values once, and scan the fixed basis cache.
The work ledger excludes preprocessing the dimension-dependent basis library. -/
def recoverPackedProfile {m L : ℕ} (D : RationalData m L)
    (cache : List (CachedBasis (normalKeyCount m) m)) : Option (Fin m → ℚ) × ℕ :=
  let grouped := packedGroup D
  let table := Vector.ofFn (fun k => (grouped.table.get k).map (fun r => r.value))
  let result := scanBases (keyNormalRat m) table.get cache
  (result.1, D.arithmeticCharge + grouped.comparisons + normalKeyCount m + result.2)

theorem recoverPackedProfile_value {m L : ℕ} (D : RationalData m L)
    (cache : List (CachedBasis (normalKeyCount m) m)) :
    (recoverPackedProfile D cache).1 = recoverFromCache (keyNormalRat m)
      (packedRationalTable D).get cache := rfl

/-- Soundness holds for any supplied cache, because every returned point is validated. -/
theorem recoverPackedProfile_sound {m L : ℕ} (D : RationalData m L)
    (cache : List (CachedBasis (normalKeyCount m) m)) {x : Fin m → ℚ}
    (hx : (recoverPackedProfile D cache).1 = some x) :
    D.toReal.ReducedProfile (fun j => (x j : ℝ)) := by
  have hf := scanBases_sound (keyNormalRat m) (packedRationalTable D).get cache hx
  have hc := (rational_feasible_iff_cast _ _ x).mp hf
  rwa [packed_realPartialSet_eq] at hc

/-- A real feasible profile guarantees an actual returned rational profile. -/
theorem recoverPackedProfile_complete {m L : ℕ} (D : RationalData m L)
    (h : ∃ x : Fin m → ℝ, D.toReal.ReducedProfile x) :
    ∃ x : Fin m → ℚ, (recoverPackedProfile D (packedBasisLibrary m)).1 = some x ∧
      D.toReal.ReducedProfile (fun j => (x j : ℝ)) := by
  have hne : (realPartialSet (keyNormalRat m) (packedRationalTable D).get).Nonempty := by
    rwa [packed_realPartialSet_eq]
  obtain ⟨x, hx, _⟩ := recoverFromCache_complete (keyNormalRat m)
    (packedRationalTable D).get hne (packed_realPartialSet_bounded D)
  have hx' : (recoverPackedProfile D (packedBasisLibrary m)).1 = some x := hx
  exact ⟨x, hx', recoverPackedProfile_sound D (packedBasisLibrary m) hx'⟩

theorem recoverPackedProfile_success_iff {m L : ℕ} (D : RationalData m L) :
    (∃ x : Fin m → ℚ, (recoverPackedProfile D (packedBasisLibrary m)).1 = some x) ↔
      ∃ x : Fin m → ℝ, D.toReal.ReducedProfile x := by
  constructor
  · rintro ⟨x, hx⟩
    exact ⟨fun j => (x j : ℝ), recoverPackedProfile_sound D (packedBasisLibrary m) hx⟩
  · intro h
    obtain ⟨x, hx, _⟩ := recoverPackedProfile_complete D h
    exact ⟨x, hx⟩

theorem recoverPackedProfile_none_iff {m L : ℕ} (D : RationalData m L) :
    (recoverPackedProfile D (packedBasisLibrary m)).1 = none ↔
      ¬∃ x : Fin m → ℝ, D.toReal.ReducedProfile x := by
  rw [← recoverPackedProfile_success_iff]
  cases (recoverPackedProfile D (packedBasisLibrary m)).1 <;> simp

/-- Linear query work for fixed dimension; inverse construction belongs to preprocessing. -/
theorem recoverPackedProfile_charge {m L : ℕ} (D : RationalData m L) (hm : 1 ≤ m) :
    (recoverPackedProfile D (packedBasisLibrary m)).2 ≤ 26 * m * (L + 1) + normalKeyCount m +
      (normalKeyCount m) ^ m * basisTrialCharge (normalKeyCount m) m := by
  have hd := D.arithmeticCharge_linear hm
  have hg := (group_cost (D.indexedRows packNormal)).1
  rw [D.indexedRows_length packNormal] at hg
  have hc := recoverFromCache_charge (keyNormalRat m) (packedRationalTable D).get
  change D.arithmeticCharge + (group (D.indexedRows packNormal)).comparisons +
    normalKeyCount m + (scanBases (keyNormalRat m) (packedRationalTable D).get
      (basisLibrary (keyNormalRat m))).2 ≤ _
  nlinarith

end NetworkSimplex.Chain.Threshold
