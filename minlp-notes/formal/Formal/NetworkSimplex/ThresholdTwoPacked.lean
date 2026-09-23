import Formal.NetworkSimplex.ThresholdPackedOracle
import Formal.NetworkSimplex.ThresholdSmallCompleteness
import Formal.NetworkSimplex.ThresholdDenseOracle
import Formal.NetworkSimplex.ProfileHull

/-! The five two-label tests on groups of actual source rows. -/
namespace NetworkSimplex.Chain.Threshold
open NetworkSimplex.ThresholdOracle
open scoped BigOperators

local instance twoPackedKeyCountNeZero : NeZero (normalKeyCount 2) := ⟨by decide⟩

theorem twoWeight_cast (c : Fin 5) (i : Fin 6) :
    ((TwoStateCircuits.weight c i).toNat : ℝ) = (TwoStateCircuits.weight c i : ℝ) := by
  exact_mod_cast Int.toNat_of_nonneg (TwoStateCircuits.weight_nonnegative c i)

theorem two_zero : keyNormal (0 : Fin (normalKeyCount 2)) = 0 := by decide +kernel

theorem two_zero_value (x : Fin 2 → ℝ) : keyValue 0 x = 0 := by
  simp [keyValue, two_zero]

def twoKey : Fin 6 → Fin (normalKeyCount 2) := ![1, 2, 3, 4, 5, 6]

theorem twoKey_normal : ∀ i, keyNormal (twoKey i) = TwoStateCircuits.normal i := by
  decide +kernel

theorem twoKey_cover (k : Fin (normalKeyCount 2)) : k = 0 ∨ ∃ i, twoKey i = k := by
  revert k
  decide +kernel

theorem twoKey_value (i : Fin 6) (x : Fin 2 → ℝ) :
    keyValue (twoKey i) x = ∑ j, (TwoStateCircuits.normal i j : ℝ) * x j := by
  simp only [keyValue, twoKey_normal]

def twoCircuit (c : Fin 5) : Circuit (normalKeyCount 2) :=
  List.ofFn fun i : Fin 6 => (twoKey i, (TwoStateCircuits.weight c i).toNat)

def twoLibrary : List (Circuit (normalKeyCount 2)) :=
  [(0, 1)] :: List.ofFn twoCircuit

theorem twoLibrary_charge :
    (twoLibrary.map fun c => 2 * c.length + 1).sum = 68 := by decide +kernel

theorem twoLibrary_cancel (c : Circuit (normalKeyCount 2)) (hc : c ∈ twoLibrary)
    (x : Fin 2 → ℝ) : (c.map fun t => (t.2 : ℝ) * keyValue t.1 x).sum = 0 := by
  rcases List.mem_cons.mp hc with rfl | hc
  · simp [two_zero_value]
  · obtain ⟨c, rfl⟩ := List.mem_ofFn.mp hc
    change (List.ofFn fun i : Fin 6 =>
      ((TwoStateCircuits.weight c i).toNat : ℝ) * keyValue (twoKey i) x).sum = 0
    rw [List.sum_ofFn]
    simp_rw [twoKey_value]
    simp_rw [twoWeight_cast, Finset.mul_sum]
    rw [Finset.sum_comm]
    apply Finset.sum_eq_zero
    intro j _
    simp_rw [← mul_assoc, ← Finset.sum_mul]
    have hc : (∑ i, (TwoStateCircuits.weight c i : ℝ) *
        (TwoStateCircuits.normal i j : ℝ)) = 0 := by
      exact_mod_cast TwoStateCircuits.normal_cancellation c j
    rw [hc, zero_mul]

def twoOracle {L : ℕ} (D : RationalData 2 L) : Option (EncodedCut 2 L) × ℕ :=
  packedOracle D twoLibrary

theorem twoOracle_charge {L : ℕ} (D : RationalData 2 L) :
    (twoOracle D).2 ≤ 52 * (L + 1) + 68 := by
  simpa only [twoOracle, twoLibrary_charge] using
    packedOracle_arithmeticCharge D (by decide) twoLibrary


theorem two_scan_none_iff {α : Type*} (table : Fin (normalKeyCount 2) → Option α)
    (rhs : α → ℚ) :
    (circuitOracle table rhs twoLibrary).1 = none ↔
      (∀ r, table 0 = some r → 0 ≤ rhs r) ∧
      NetworkSimplex.Threshold.PartialCircuitTests
        (fun c i => (TwoStateCircuits.weight c i : ℝ))
        (fun i => (table (twoKey i)).map (fun r => (rhs r : ℝ))) := by
  have hd := dense_circuitOracle_none_iff table rhs twoKey
    (fun c i => (TwoStateCircuits.weight c i).toNat)
  simp only [twoWeight_cast] at hd
  change (circuitOracle table rhs ([(0, 1)] ::
    denseLibrary twoKey (fun c i => (TwoStateCircuits.weight c i).toNat))).1 = none ↔ _
  cases ht : table 0 with
  | none => simp [circuitOracle, selectTerms, ht, hd]
  | some r =>
    by_cases hn : rhs r < 0
    · simp [circuitOracle, selectTerms, ht, weightedValue, hn, not_le.mpr hn]
    · simp [circuitOracle, selectTerms, ht, weightedValue, hn, hd, le_of_not_gt hn]

/-- The complete rational oracle accepts exactly when the original reduced
profile system is feasible. No artificial positive-subset row is inserted. -/
theorem twoOracle_none_iff {L : ℕ} (D : RationalData 2 L) :
    (twoOracle D).1 = none ↔ ∃ x : Fin 2 → ℝ, D.toReal.ReducedProfile x := by
  change (circuitOracle (packedGroup D).table.get (fun r => r.value) twoLibrary).1 = none ↔ _
  rw [two_scan_none_iff, ← NetworkSimplex.Threshold.two_partial_feasible_iff]
  constructor
  · rintro ⟨hz, x, hx⟩
    refine ⟨x, (packed_constraints D x).mp ?_⟩
    intro k r hr
    rcases twoKey_cover k with rfl | ⟨i, rfl⟩
    · simpa [two_zero_value] using (show (0 : ℝ) ≤ (r.value : ℝ) by
        exact_mod_cast hz r hr)
    · rw [twoKey_value]
      exact hx i (r.value : ℝ) (by simp [hr])
  · rintro ⟨x, hx⟩
    have hh := (packed_constraints D x).mpr hx
    constructor
    · intro r hr
      have h := hh 0 r hr
      rw [two_zero_value] at h
      exact_mod_cast h
    · refine ⟨x, ?_⟩
      intro i v hv
      cases ht : (packedGroup D).table.get (twoKey i) with
      | none => simp [ht] at hv
      | some r =>
        simp only [ht, Option.map_some, Option.some.injEq] at hv
        rw [← hv, ← twoKey_value]
        exact hh _ r ht

/-- The library has 5 nonzero-normal tests and one zero-normal test. -/
theorem twoLibrary_length : twoLibrary.length = 5 + 1 := by decide +kernel

/-- Acceptance together with the original-domain checks is exactly membership
in the original bilinear convex hull. State zero is the unobserved residual. -/
theorem twoOracle_hull_iff {L : ℕ} (D : RationalData 2 L)
    (hc : ∀ i, D.toReal.c i 0 = .neither) (hh : D.toReal.observedH 0 = false) :
    D.toReal.graphPoint ∈ convexHull ℝ D.toReal.graph ↔
      D.toReal.OriginalDomain ∧ (twoOracle D).1 = none := by
  rw [ReductionData.mem_hull_iff, D.toReal.exists_fullProfile_iff_rows hc hh,
    twoOracle_none_iff]
  exact and_congr_right fun _ => exists_congr fun x => D.toReal.rows_iff_reducedProfile x

/-- Returned certificates retain the identifiers of actual input rows. -/
theorem twoOracle_row_source {L : ℕ} (D : RationalData 2 L)
    {rows : EncodedCut 2 L} (ho : (twoOracle D).1 = some rows)
    {t : ℕ × PackedRow 2 L} (ht : t ∈ rows) : t.2 ∈ D.indexedRows packNormal :=
  packed_row_source D twoLibrary ho ht

/-- A returned cut is violated at the rational query and valid at every real
feasible profile with the same observation pattern. -/
theorem twoOracle_separates {L : ℕ} (D : RationalData 2 L)
    {rows : EncodedCut 2 L} (ho : (twoOracle D).1 = some rows)
    (E : ReductionData 2 (Fin L)) (x : Fin 2 → ℝ)
    (hn : ∀ r, D.toReal.rowNormal r = E.rowNormal r)
    (hf : E.ReducedProfile x) :
    rows.eval D.toReal.rowRhs < 0 ∧ 0 ≤ rows.eval E.rowRhs :=
  packedOracle_separates_real D twoLibrary twoLibrary_cancel ho E x hn hf

end NetworkSimplex.Chain.Threshold
