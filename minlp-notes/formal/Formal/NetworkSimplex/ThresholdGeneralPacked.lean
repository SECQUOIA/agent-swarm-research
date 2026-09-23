import Formal.NetworkSimplex.ThresholdPackedOracle
import Formal.NetworkSimplex.ThresholdDenseOracle
import Formal.NetworkSimplex.ThresholdCircuitPreprocess
import Formal.NetworkSimplex.ThresholdPreprocessCriterion

/-! The executable general fixed-state circuit oracle, after parameter-only preprocessing. -/
namespace NetworkSimplex.Chain.Threshold
open NetworkSimplex.ThresholdOracle
open scoped BigOperators

theorem keyNormal_rowSignedZeroOne (m : ℕ) :
    NetworkSimplex.Threshold.RowSignedZeroOne (@keyNormal m) := by
  intro k
  by_cases hk : k.val < 2 ^ m
  · left
    intro j
    simp only [keyNormal, hk, ↓reduceIte]
    split_ifs <;> simp
  · right
    intro j
    simp only [keyNormal, hk, ↓reduceIte]
    split_ifs <;> simp

/-- This finite library depends only on the number of explicit labels. Its
coefficients and supports are computed once, before any candidate query. -/
def generalLibrary (m : ℕ) : List (Circuit (normalKeyCount m)) :=
  (NetworkSimplex.Threshold.preprocessCircuits (@keyNormal m)).map fun c =>
    denseCircuit c.candidate.support c.weight

/-- The query consumes the cached library; preprocessing is not repeated per row. -/
def generalOracle {m L : ℕ} (D : RationalData m L)
    (library : List (Circuit (normalKeyCount m))) : Option (EncodedCut m L) × ℕ :=
  packedOracle D library

theorem generalLibrary_cancel (m : ℕ) (c : Circuit (normalKeyCount m))
    (hc : c ∈ generalLibrary m) (x : Fin m → ℝ) :
    (c.map fun t => (t.2 : ℝ) * keyValue t.1 x).sum = 0 := by
  unfold generalLibrary at hc
  obtain ⟨c, hmem, rfl⟩ := List.mem_map.mp hc
  have hh := (NetworkSimplex.Threshold.preprocessCircuits_sound (@keyNormal m)
    (keyNormal_rowSignedZeroOne m) hmem).2.2
  simp only [denseCircuit, List.map_ofFn, List.sum_ofFn]
  change (∑ i, (c.weight i : ℝ) * keyValue (c.candidate.support i) x) = 0
  simp only [keyValue]
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_eq_zero
  intro j _
  simp_rw [← mul_assoc, ← Finset.sum_mul]
  have he : (∑ i, (c.weight i : ℝ) * (keyNormal (c.candidate.support i) j : ℝ)) = 0 := by
    exact_mod_cast hh j
  rw [he, zero_mul]

theorem generalLibrary_charge (m : ℕ) :
    ((generalLibrary m).map fun c => 2 * c.length + 1).sum ≤
      2 ^ (4 * (m + 1) ^ 2) * (2 * m + 3) := by
  have hlen := NetworkSimplex.Threshold.preprocessCircuits_length_exp (@keyNormal m)
  have hsum : ∀ cs : List (NetworkSimplex.Threshold.CompiledCircuit m (normalKeyCount m)),
      (cs.map fun c => 2 * (denseCircuit c.candidate.support c.weight).length + 1).sum ≤
        cs.length * (2 * m + 3) := by
    intro cs
    induction cs with
    | nil => simp
    | cons c cs ih =>
      simp only [List.map_cons, List.sum_cons, List.length_cons, denseCircuit, List.length_ofFn]
      have hc := c.candidate.size.isLt
      simp only [denseCircuit, List.length_ofFn] at ih
      nlinarith
  have hs := hsum (NetworkSimplex.Threshold.preprocessCircuits (@keyNormal m))
  simp only [generalLibrary, List.map_map, Function.comp_def]
  exact hs.trans (Nat.mul_le_mul_right _ hlen)

theorem generalOracle_charge {m L : ℕ} (D : RationalData m L) (hm : 1 ≤ m) :
    (generalOracle D (generalLibrary m)).2 ≤
      26 * m * (L + 1) + 2 ^ (4 * (m + 1) ^ 2) * (2 * m + 3) :=
  (packedOracle_arithmeticCharge D hm _).trans
    (Nat.add_le_add_left (generalLibrary_charge m) _)


theorem general_scan_none_iff {m : ℕ} {α : Type*}
    (table : Fin (normalKeyCount m) → Option α) (rhs : α → ℚ) :
    (circuitOracle table rhs (generalLibrary m)).1 = none ↔
      NetworkSimplex.Threshold.CompiledPartialTests (@keyNormal m)
        (fun k => (table k).map (fun r => (rhs r : ℝ))) := by
  rw [circuitOracle_none_iff]
  constructor
  · intro h c hc hp
    apply (dense_test_iff table rhs c.candidate.support c.weight).mp
      (h _ (List.mem_map.mpr ⟨c, hc, rfl⟩))
    intro i hi
    exact (hp i hi).elim
  · intro h d hd rows hs
    unfold generalLibrary at hd
    obtain ⟨c, hc, rfl⟩ := List.mem_map.mp hd
    apply (dense_test_iff table rhs c.candidate.support c.weight).mpr ?_ rows hs
    intro hp
    apply h c hc
    intro i hi
    have hw := (NetworkSimplex.Threshold.preprocessCircuits_sound (@keyNormal m)
      (keyNormal_rowSignedZeroOne m) hc).1 i
    have hz := hp i hi
    have hpos : (0 : ℝ) < c.weight i := by exact_mod_cast hw.1
    linarith

/-- Actual finite preprocessing followed by exact grouped circuit scanning is
complete for the original profile system in every dimension. -/
theorem generalOracle_none_iff {m L : ℕ} (D : RationalData m L) :
    (generalOracle D (generalLibrary m)).1 = none ↔
      ∃ x : Fin m → ℝ, D.toReal.ReducedProfile x := by
  change (circuitOracle (packedGroup D).table.get (fun r => r.value)
    (generalLibrary m)).1 = none ↔ _
  rw [general_scan_none_iff, ← NetworkSimplex.Threshold.feasible_iff_compiledPartialTests
    (@keyNormal m) (keyNormal_rowSignedZeroOne m)]
  constructor
  · rintro ⟨x, hx⟩
    refine ⟨x, (packed_constraints D x).mp ?_⟩
    intro k r hr
    have hh := hx k (by simp [hr])
    simpa only [hr, Option.map_some, Option.getD_some, keyValue] using hh
  · rintro ⟨x, hx⟩
    refine ⟨x, ?_⟩
    intro k hk
    cases ht : (packedGroup D).table.get k with
    | none => simp [ht] at hk
    | some r =>
      have hh := (packed_constraints D x).mpr hx k r ht
      simpa only [ht, Option.map_some, Option.getD_some, keyValue] using hh


/-- Returned cuts have bounded support and primitive-library integer weights,
and every payload is an actual original row. -/
theorem generalOracle_returned_bounds {m L : ℕ} (D : RationalData m L)
    {rows : EncodedCut m L}
    (ho : (generalOracle D (generalLibrary m)).1 = some rows) :
    rows.length ≤ m + 1 ∧ ∀ t ∈ rows,
      t.1 ≤ NetworkSimplex.Threshold.delta01 m ∧ t.2 ∈ D.indexedRows packNormal := by
  obtain ⟨_, d, hd, hs⟩ := circuitOracle_some (packedGroup D).table.get
    (fun r => r.value) (generalLibrary m) ho
  unfold generalLibrary at hd
  obtain ⟨c, hc, rfl⟩ := List.mem_map.mp hd
  have hb := NetworkSimplex.Threshold.preprocessCircuits_sound (@keyNormal m)
    (keyNormal_rowSignedZeroOne m) hc
  constructor
  · have hh := selectTerms_length _ _ hs
    simp only [denseCircuit, List.length_ofFn] at hh
    have hsize := c.candidate.size.isLt
    omega
  · intro t ht
    constructor
    · obtain ⟨_, k, hk, _⟩ := selectTerms_rows _ _ hs ht
      obtain ⟨i, hi⟩ := List.mem_ofFn.mp hk
      have he := congrArg Prod.snd hi
      change c.weight i = t.1 at he
      rw [← he]
      exact (hb.1 i).2
    · exact packed_row_source D (generalLibrary m) ho ht

end NetworkSimplex.Chain.Threshold
