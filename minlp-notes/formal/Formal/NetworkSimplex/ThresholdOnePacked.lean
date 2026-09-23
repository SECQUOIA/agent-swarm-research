import Formal.NetworkSimplex.ThresholdPackedOracle
import Formal.NetworkSimplex.ThresholdSmallCompleteness
import Formal.NetworkSimplex.ThresholdDenseOracle
import Formal.NetworkSimplex.ProfileHull

/-! The one-label tests on groups of actual source rows. -/
namespace NetworkSimplex.Chain.Threshold
open NetworkSimplex.ThresholdOracle
open scoped BigOperators

local instance onePackedKeyCountNeZero : NeZero (normalKeyCount 1) := ⟨by decide⟩

theorem oneWeight_cast (c : Fin 1) (i : Fin 2) :
    ((OneStateCircuits.weight c i).toNat : ℝ) = (OneStateCircuits.weight c i : ℝ) := by
  exact_mod_cast Int.toNat_of_nonneg (OneStateCircuits.weight_nonnegative c i)

theorem one_zero : keyNormal (0 : Fin (normalKeyCount 1)) = 0 := by decide +kernel

theorem one_zero_value (x : Fin 1 → ℝ) : keyValue 0 x = 0 := by
  simp [keyValue, one_zero]

def oneKey : Fin 2 → Fin (normalKeyCount 1) := ![1, 2]

theorem oneKey_normal : ∀ i, keyNormal (oneKey i) = OneStateCircuits.normal i := by
  decide +kernel

theorem oneKey_cover (k : Fin (normalKeyCount 1)) : k = 0 ∨ (∃ i, oneKey i = k) ∨ k = 3 := by
  revert k
  decide +kernel

theorem one_pack_unused (p : ProfileNormal 1) : packNormal p ≠ 3 := by
  revert p
  decide +kernel

theorem one_group_unused {L : ℕ} (D : RationalData 1 L) :
    (packedGroup D).table.get 3 = none := by
  apply (NetworkSimplex.ThresholdGrouping.group_none_iff _ _).mpr
  intro r hr
  rw [(D.indexedRows_spec packNormal hr).1]
  exact one_pack_unused _

theorem oneKey_value (i : Fin 2) (x : Fin 1 → ℝ) :
    keyValue (oneKey i) x = ∑ j, (OneStateCircuits.normal i j : ℝ) * x j := by
  simp only [keyValue, oneKey_normal]

def oneCircuit (c : Fin 1) : Circuit (normalKeyCount 1) :=
  List.ofFn fun i : Fin 2 => (oneKey i, (OneStateCircuits.weight c i).toNat)

def oneLibrary : List (Circuit (normalKeyCount 1)) :=
  [(0, 1)] :: List.ofFn oneCircuit

theorem oneLibrary_charge :
    (oneLibrary.map fun c => 2 * c.length + 1).sum = 8 := by decide +kernel

theorem oneLibrary_cancel (c : Circuit (normalKeyCount 1)) (hc : c ∈ oneLibrary)
    (x : Fin 1 → ℝ) : (c.map fun t => (t.2 : ℝ) * keyValue t.1 x).sum = 0 := by
  rcases List.mem_cons.mp hc with rfl | hc
  · simp [one_zero_value]
  · obtain ⟨c, rfl⟩ := List.mem_ofFn.mp hc
    change (List.ofFn fun i : Fin 2 =>
      ((OneStateCircuits.weight c i).toNat : ℝ) * keyValue (oneKey i) x).sum = 0
    rw [List.sum_ofFn]
    simp_rw [oneKey_value]
    simp_rw [oneWeight_cast, Finset.mul_sum]
    rw [Finset.sum_comm]
    apply Finset.sum_eq_zero
    intro j _
    simp_rw [← mul_assoc, ← Finset.sum_mul]
    have hc : (∑ i, (OneStateCircuits.weight c i : ℝ) *
        (OneStateCircuits.normal i j : ℝ)) = 0 := by
      exact_mod_cast OneStateCircuits.normal_cancellation c j
    rw [hc, zero_mul]

def oneOracle {L : ℕ} (D : RationalData 1 L) : Option (EncodedCut 1 L) × ℕ :=
  packedOracle D oneLibrary

theorem oneOracle_charge {L : ℕ} (D : RationalData 1 L) :
    (oneOracle D).2 ≤ 26 * (L + 1) + 8 := by
  simpa only [oneOracle, oneLibrary_charge] using
    packedOracle_arithmeticCharge D (by decide) oneLibrary


theorem one_scan_none_iff {α : Type*} (table : Fin (normalKeyCount 1) → Option α)
    (rhs : α → ℚ) :
    (circuitOracle table rhs oneLibrary).1 = none ↔
      (∀ r, table 0 = some r → 0 ≤ rhs r) ∧
      NetworkSimplex.Threshold.PartialCircuitTests
        (fun c i => (OneStateCircuits.weight c i : ℝ))
        (fun i => (table (oneKey i)).map (fun r => (rhs r : ℝ))) := by
  have hd := dense_circuitOracle_none_iff table rhs oneKey
    (fun c i => (OneStateCircuits.weight c i).toNat)
  simp only [oneWeight_cast] at hd
  change (circuitOracle table rhs ([(0, 1)] ::
    denseLibrary oneKey (fun c i => (OneStateCircuits.weight c i).toNat))).1 = none ↔ _
  cases ht : table 0 with
  | none => simp [circuitOracle, selectTerms, ht, hd]
  | some r =>
    by_cases hn : rhs r < 0
    · simp [circuitOracle, selectTerms, ht, weightedValue, hn, not_le.mpr hn]
    · simp [circuitOracle, selectTerms, ht, weightedValue, hn, hd, le_of_not_gt hn]

/-- The complete rational oracle accepts exactly when the original reduced
profile system is feasible. No artificial positive-subset row is inserted. -/
theorem oneOracle_none_iff {L : ℕ} (D : RationalData 1 L) :
    (oneOracle D).1 = none ↔ ∃ x : Fin 1 → ℝ, D.toReal.ReducedProfile x := by
  change (circuitOracle (packedGroup D).table.get (fun r => r.value) oneLibrary).1 = none ↔ _
  rw [one_scan_none_iff, ← NetworkSimplex.Threshold.one_partial_feasible_iff]
  constructor
  · rintro ⟨hz, x, hx⟩
    refine ⟨x, (packed_constraints D x).mp ?_⟩
    intro k r hr
    rcases oneKey_cover k with rfl | ⟨i, rfl⟩ | rfl
    · simpa [one_zero_value] using (show (0 : ℝ) ≤ (r.value : ℝ) by
        exact_mod_cast hz r hr)
    · rw [oneKey_value]
      exact hx i (r.value : ℝ) (by simp [hr])
    · rw [one_group_unused] at hr
      contradiction
  · rintro ⟨x, hx⟩
    have hh := (packed_constraints D x).mpr hx
    constructor
    · intro r hr
      have h := hh 0 r hr
      rw [one_zero_value] at h
      exact_mod_cast h
    · refine ⟨x, ?_⟩
      intro i v hv
      cases ht : (packedGroup D).table.get (oneKey i) with
      | none => simp [ht] at hv
      | some r =>
        simp only [ht, Option.map_some, Option.some.injEq] at hv
        rw [← hv, ← oneKey_value]
        exact hh _ r ht

/-- The library has 1 nonzero-normal tests and one zero-normal test. -/
theorem oneLibrary_length : oneLibrary.length = 1 + 1 := by decide +kernel

/-- Acceptance together with the original-domain checks is exactly membership
in the original bilinear convex hull. State zero is the unobserved residual. -/
theorem oneOracle_hull_iff {L : ℕ} (D : RationalData 1 L)
    (hc : ∀ i, D.toReal.c i 0 = .neither) (hh : D.toReal.observedH 0 = false) :
    D.toReal.graphPoint ∈ convexHull ℝ D.toReal.graph ↔
      D.toReal.OriginalDomain ∧ (oneOracle D).1 = none := by
  rw [ReductionData.mem_hull_iff, D.toReal.exists_fullProfile_iff_rows hc hh,
    oneOracle_none_iff]
  exact and_congr_right fun _ => exists_congr fun x => D.toReal.rows_iff_reducedProfile x

/-- Returned certificates retain the identifiers of actual input rows. -/
theorem oneOracle_row_source {L : ℕ} (D : RationalData 1 L)
    {rows : EncodedCut 1 L} (ho : (oneOracle D).1 = some rows)
    {t : ℕ × PackedRow 1 L} (ht : t ∈ rows) : t.2 ∈ D.indexedRows packNormal :=
  packed_row_source D oneLibrary ho ht

/-- A returned cut is violated at the rational query and valid at every real
feasible profile with the same observation pattern. -/
theorem oneOracle_separates {L : ℕ} (D : RationalData 1 L)
    {rows : EncodedCut 1 L} (ho : (oneOracle D).1 = some rows)
    (E : ReductionData 1 (Fin L)) (x : Fin 1 → ℝ)
    (hn : ∀ r, D.toReal.rowNormal r = E.rowNormal r)
    (hf : E.ReducedProfile x) :
    rows.eval D.toReal.rowRhs < 0 ∧ 0 ≤ rows.eval E.rowRhs :=
  packedOracle_separates_real D oneLibrary oneLibrary_cancel ho E x hn hf

end NetworkSimplex.Chain.Threshold
