import Formal.NetworkSimplex.ThresholdPackedOracle
import Formal.NetworkSimplex.ThresholdThreeCompleteness
import Formal.NetworkSimplex.ThresholdDenseOracle

/-! The sixteen three-label tests on groups of actual source rows. -/
namespace NetworkSimplex.Chain.Threshold
open NetworkSimplex.ThresholdOracle
open scoped BigOperators

local instance threePackedKeyCountNeZero : NeZero (normalKeyCount 3) := ⟨by decide⟩

theorem threeWeight_cast (c : Fin 16) (i : Fin 11) :
    ((ThreeStateCircuits.weight c i).toNat : ℝ) = (ThreeStateCircuits.weight c i : ℝ) := by
  exact_mod_cast Int.toNat_of_nonneg (ThreeStateCircuits.weight_nonnegative c i)

theorem three_zero : keyNormal (0 : Fin (normalKeyCount 3)) = 0 := by decide +kernel

theorem three_zero_value (x : Fin 3 → ℝ) : keyValue 0 x = 0 := by
  simp [keyValue, three_zero]

def threeKey : Fin 11 → Fin (normalKeyCount 3) := ![1, 2, 4, 3, 5, 6, 7, 8, 9, 10, 11]

theorem threeKey_normal : ∀ i, keyNormal (threeKey i) = ThreeStateCircuits.normal i := by
  decide +kernel

theorem threeKey_cover (k : Fin (normalKeyCount 3)) : k = 0 ∨ ∃ i, threeKey i = k := by
  revert k
  decide +kernel

theorem threeKey_value (i : Fin 11) (x : Fin 3 → ℝ) :
    keyValue (threeKey i) x = ∑ j, (ThreeStateCircuits.normal i j : ℝ) * x j := by
  simp only [keyValue, threeKey_normal]

def threeCircuit (c : Fin 16) : Circuit (normalKeyCount 3) :=
  List.ofFn fun i : Fin 11 => (threeKey i, (ThreeStateCircuits.weight c i).toNat)

def threeLibrary : List (Circuit (normalKeyCount 3)) :=
  [(0, 1)] :: List.ofFn threeCircuit

theorem threeLibrary_charge :
    (threeLibrary.map fun c => 2 * c.length + 1).sum = 371 := by decide +kernel

theorem threeLibrary_cancel (c : Circuit (normalKeyCount 3)) (hc : c ∈ threeLibrary)
    (x : Fin 3 → ℝ) : (c.map fun t => (t.2 : ℝ) * keyValue t.1 x).sum = 0 := by
  rcases List.mem_cons.mp hc with rfl | hc
  · simp [three_zero_value]
  · obtain ⟨c, rfl⟩ := List.mem_ofFn.mp hc
    change (List.ofFn fun i : Fin 11 =>
      ((ThreeStateCircuits.weight c i).toNat : ℝ) * keyValue (threeKey i) x).sum = 0
    rw [List.sum_ofFn]
    simp_rw [threeKey_value]
    simp_rw [threeWeight_cast, Finset.mul_sum]
    rw [Finset.sum_comm]
    apply Finset.sum_eq_zero
    intro j _
    simp_rw [← mul_assoc, ← Finset.sum_mul]
    have hc : (∑ i, (ThreeStateCircuits.weight c i : ℝ) *
        (ThreeStateCircuits.normal i j : ℝ)) = 0 := by
      exact_mod_cast ThreeStateCircuits.normal_cancellation c j
    rw [hc, zero_mul]

def threeOracle {L : ℕ} (D : RationalData 3 L) : Option (EncodedCut 3 L) × ℕ :=
  packedOracle D threeLibrary

theorem threeOracle_charge {L : ℕ} (D : RationalData 3 L) :
    (threeOracle D).2 ≤ 78 * (L + 1) + 371 := by
  simpa only [threeOracle, threeLibrary_charge] using
    packedOracle_arithmeticCharge D (by decide) threeLibrary


theorem three_scan_none_iff {α : Type*} (table : Fin (normalKeyCount 3) → Option α)
    (rhs : α → ℚ) :
    (circuitOracle table rhs threeLibrary).1 = none ↔
      (∀ r, table 0 = some r → 0 ≤ rhs r) ∧
      NetworkSimplex.Threshold.PartialCircuitTests
        (fun c i => (ThreeStateCircuits.weight c i : ℝ))
        (fun i => (table (threeKey i)).map (fun r => (rhs r : ℝ))) := by
  have hd := dense_circuitOracle_none_iff table rhs threeKey
    (fun c i => (ThreeStateCircuits.weight c i).toNat)
  simp only [threeWeight_cast] at hd
  change (circuitOracle table rhs ([(0, 1)] ::
    denseLibrary threeKey (fun c i => (ThreeStateCircuits.weight c i).toNat))).1 = none ↔ _
  cases ht : table 0 with
  | none => simp [circuitOracle, selectTerms, ht, hd]
  | some r =>
    by_cases hn : rhs r < 0
    · simp [circuitOracle, selectTerms, ht, weightedValue, hn, not_le.mpr hn]
    · simp [circuitOracle, selectTerms, ht, weightedValue, hn, hd, le_of_not_gt hn]

/-- The complete rational oracle accepts exactly when the original reduced
profile system is feasible. No artificial positive-subset row is inserted. -/
theorem threeOracle_none_iff {L : ℕ} (D : RationalData 3 L) :
    (threeOracle D).1 = none ↔ ∃ x : Fin 3 → ℝ, D.toReal.ReducedProfile x := by
  change (circuitOracle (packedGroup D).table.get (fun r => r.value) threeLibrary).1 = none ↔ _
  rw [three_scan_none_iff, ← NetworkSimplex.Threshold.three_partial_feasible_iff]
  constructor
  · rintro ⟨hz, x, hx⟩
    refine ⟨x, (packed_constraints D x).mp ?_⟩
    intro k r hr
    rcases threeKey_cover k with rfl | ⟨i, rfl⟩
    · simpa [three_zero_value] using (show (0 : ℝ) ≤ (r.value : ℝ) by
        exact_mod_cast hz r hr)
    · rw [threeKey_value]
      exact hx i (r.value : ℝ) (by simp [hr])
  · rintro ⟨x, hx⟩
    have hh := (packed_constraints D x).mpr hx
    constructor
    · intro r hr
      have h := hh 0 r hr
      rw [three_zero_value] at h
      exact_mod_cast h
    · refine ⟨x, ?_⟩
      intro i v hv
      cases ht : (packedGroup D).table.get (threeKey i) with
      | none => simp [ht] at hv
      | some r =>
        simp only [ht, Option.map_some, Option.some.injEq] at hv
        rw [← hv, ← threeKey_value]
        exact hh _ r ht

end NetworkSimplex.Chain.Threshold
