import Formal.NetworkSimplex.ThresholdRationalRows
import Formal.NetworkSimplex.ThresholdCircuitOracle
import Formal.ReciprocalAnchor.ManyRationalSize

/-! Bounds for the actual rational rows and partial circuit sums. -/
namespace NetworkSimplex.Chain.Threshold
open ReciprocalAnchor
namespace RationalData
variable {m L B : ℕ}

structure InputBits (D : RationalData m L) (B : ℕ) : Prop where
  u : ∀ i j, RationalBits (D.u i j) B
  v : ∀ i j, RationalBits (D.v i j) B
  weights : ∀ j, RationalBits (D.weights j) B
  xa : ∀ i, RationalBits (D.xa i) B
  xh : RationalBits D.xh B
  zh : ∀ j, RationalBits (D.zh j) B

def rowBits (m B : ℕ) : ℕ := (2 * m + 6) * (B + 2)

theorem InputBits.pos {D : RationalData m L} (h : D.InputBits B) : 0 < B :=
  rationalBits_pos h.xh

theorem input_sum_bits {D : RationalData m L} (_h : D.InputBits B)
    {xs : List ℚ} (hx : ∀ x ∈ xs, RationalBits x B) (hl : xs.length ≤ m + 1) :
    RationalBits xs.sum (1 + (m + 1) * (B + 1)) :=
  rationalBits_mono (rationalBits_list_sum hx) (by gcongr)

theorem residual_bits {D : RationalData m L} (h : D.InputBits B) (i : Fin L) :
    RationalBits (D.residual i) (B + 2 * (1 + (m + 1) * (B + 1)) + 2) := by
  have hz := rationalBits_mono rationalBits_zero (show 1 ≤ B from h.pos)
  have ha : RationalBits
      ((List.ofFn fun j => if observesA (D.c i j) then D.u i j else 0).sum)
      (1 + (m + 1) * (B + 1)) := by
    apply input_sum_bits h
    · intro q hq
      obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hq
      split_ifs <;> first | exact h.u i j | exact hz
    · simp
  have hb : RationalBits
      ((List.ofFn fun j => if D.c i j = .bOnly then D.v i j else 0).sum)
      (1 + (m + 1) * (B + 1)) := by
    apply input_sum_bits h
    · intro q hq
      obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hq
      split_ifs <;> first | exact h.v i j | exact hz
    · simp
  simpa only [residual, show B + (1 + (m + 1) * (B + 1)) + 1 +
    (1 + (m + 1) * (B + 1)) + 1 = B + 2 * (1 + (m + 1) * (B + 1)) + 2 by omega]
    using rationalBits_add (rationalBits_sub (h.xa i) ha) hb

theorem total_bits {D : RationalData m L} (h : D.InputBits B) :
    RationalBits D.total (B + 2) := by
  simpa [total, Nat.add_comm, Nat.add_left_comm] using rationalBits_sub rationalBits_one h.xh

theorem cachedRhs_bits {D : RationalData m L} (h : D.InputBits B)
    (r : ProfileRow m (Fin L)) : RationalBits (D.cachedRhs D.cache r) (rowBits m B) := by
  have hz : RationalBits (0 : ℚ) (rowBits m B) :=
    rationalBits_mono rationalBits_zero (by unfold rowBits; nlinarith)
  have hinput : B ≤ rowBits m B := by unfold rowBits; nlinarith
  have hsum : 2 * B + 1 ≤ rowBits m B := by unfold rowBits; nlinarith
  have htot : B + 2 ≤ rowBits m B := by unfold rowBits; nlinarith
  have hend : (B + 2) + (B + 2 * (1 + (m + 1) * (B + 1)) + 2) + 1 ≤
      rowBits m B := by unfold rowBits; nlinarith
  have hr : B + 2 * (1 + (m + 1) * (B + 1)) + 2 ≤ rowBits m B := by omega
  have hw : B + (B + 2) + 1 ≤ rowBits m B := by unfold rowBits; nlinarith
  cases r with
  | lower j => exact hz
  | upper j => exact rationalBits_mono (h.weights j.succ) hinput
  | totalLower => exact rationalBits_mono (rationalBits_sub (h.weights 0) (total_bits h)) hw
  | totalUpper => exact rationalBits_mono (total_bits h) htot
  | bypassLower j =>
    simp only [cachedRhs]; split_ifs
    · exact rationalBits_mono (rationalBits_sub (h.zh j.succ) (h.weights j.succ)) (by omega)
    · exact hz
  | bypassUpper j =>
    simp only [cachedRhs]; split_ifs
    · exact rationalBits_mono (rationalBits_sub (h.weights j.succ) (h.zh j.succ)) (by omega)
    · exact hz
  | aLower i j =>
    simp only [cachedRhs]; split_ifs
    · exact rationalBits_mono (rationalBits_neg (h.u i j.succ)) hinput
    · exact hz
  | bLower i j =>
    simp only [cachedRhs]; split_ifs
    · exact rationalBits_mono (rationalBits_neg (h.v i j.succ)) hinput
    · exact hz
  | bothLower i j =>
    simp only [cachedRhs]; split_ifs
    · exact rationalBits_mono
        (rationalBits_neg (rationalBits_add (h.u i j.succ) (h.v i j.succ))) (by omega)
    · exact hz
  | bothUpper i j =>
    simp only [cachedRhs]; split_ifs
    · exact rationalBits_mono (rationalBits_add (h.u i j.succ) (h.v i j.succ)) (by omega)
    · exact hz
  | endpointB i =>
    simpa only [cachedRhs, cache_gadget, gadgetCache] using rationalBits_mono (residual_bits h i) hr
  | endpointA i =>
    change RationalBits (D.total - (D.cache.gadget i).endpoint) _
    simpa only [cache_gadget, gadgetCache] using
      rationalBits_mono (rationalBits_sub (total_bits h) (residual_bits h i)) hend

theorem indexedRows_bits {K : ℕ} {D : RationalData m L} (h : D.InputBits B)
    (key : ProfileNormal m → Fin K)
    {r : NetworkSimplex.ThresholdGrouping.IndexedRow K (ProfileRow m (Fin L))}
    (hr : r ∈ D.indexedRows key) : RationalBits r.value (rowBits m B) := by
  obtain ⟨tag, _, rfl⟩ := List.mem_map.mp hr
  exact cachedRhs_bits h tag

end RationalData
end NetworkSimplex.Chain.Threshold

namespace NetworkSimplex.ThresholdOracle
open ReciprocalAnchor

theorem nat_weight_bits {w W : ℕ} (hw : w < 2 ^ W) (hW : 0 < W) :
    RationalBits (w : ℚ) W := by
  simpa [RationalBits] using And.intro hw (show 1 < 2 ^ W by exact Nat.one_lt_two_pow hW.ne')

/-- Every intermediate sum, including arbitrary sublists of the selected terms,
has the same polynomial bound. This also covers prefixes and suffixes of a fold. -/
theorem weightedValue_partial_bits {α : Type*} (rhs : α → ℚ)
    (rows : List (ℕ × α)) {B W : ℕ}
    (hr : ∀ t ∈ rows, RationalBits (rhs t.2) B)
    (hw : ∀ t ∈ rows, RationalBits (t.1 : ℚ) W)
    {part : List (ℕ × α)} (hp : part.Sublist rows) :
    RationalBits (weightedValue rhs part) (1 + rows.length * (B + W + 1)) := by
  have hh : ∀ q ∈ part.map (fun t => (t.1 : ℚ) * rhs t.2), RationalBits q (B + W) := by
    intro q hq
    obtain ⟨t, ht, rfl⟩ := List.mem_map.mp hq
    simpa [Nat.add_comm] using rationalBits_mul (hw t (hp.subset ht)) (hr t (hp.subset ht))
  have hs := rationalBits_list_sum hh
  apply rationalBits_mono hs
  simp only [List.length_map]
  exact Nat.add_le_add_left (Nat.mul_le_mul_right _ hp.length_le) 1

theorem selected_row_bits {K m L B : ℕ}
    {D : Chain.Threshold.RationalData m L}
    (h : D.InputBits B) (key : Chain.ProfileNormal m → Fin K)
    (library : List (Circuit K))
    {rows : List (ℕ × ThresholdGrouping.IndexedRow K (Chain.ProfileRow m (Fin L)))}
    (ho : (groupedCircuitOracle (D.indexedRows key) library).1 = some rows)
    {weight : ℕ} {row : ThresholdGrouping.IndexedRow K (Chain.ProfileRow m (Fin L))}
    (hr : (weight, row) ∈ rows) :
    RationalBits row.value (Chain.Threshold.RationalData.rowBits m B) :=
  Chain.Threshold.RationalData.indexedRows_bits h key
    (groupedCircuitOracle_original_rows _ _ ho hr)

/-- A returned cut uses the source library's weights and support bound. -/
theorem emitted_partial_bits {K m L B W S : ℕ}
    {D : Chain.Threshold.RationalData m L}
    (h : D.InputBits B) (key : Chain.ProfileNormal m → Fin K)
    (library : List (Circuit K))
    (hs : ∀ c ∈ library, c.length ≤ S)
    (hw : ∀ c ∈ library, ∀ t ∈ c, RationalBits (t.2 : ℚ) W)
    {rows : List (ℕ × ThresholdGrouping.IndexedRow K (Chain.ProfileRow m (Fin L)))}
    (ho : (groupedCircuitOracle (D.indexedRows key) library).1 = some rows)
    {part : List (ℕ × ThresholdGrouping.IndexedRow K (Chain.ProfileRow m (Fin L)))}
    (hp : part.Sublist rows) :
    RationalBits (weightedValue (fun r => r.value) part)
      (1 + S * (Chain.Threshold.RationalData.rowBits m B + W + 1)) := by
  obtain ⟨_, c, hc, hselect⟩ := circuitOracle_some
    (ThresholdGrouping.group (D.indexedRows key)).table.get (fun r => r.value) library ho
  have hlen := (selectTerms_length _ _ hselect).trans (hs c hc)
  apply rationalBits_mono (weightedValue_partial_bits (fun r => r.value) rows
    (fun t ht => selected_row_bits h key library ho ht) ?_ hp)
  · exact Nat.add_le_add_left (Nat.mul_le_mul_right _ hlen) 1
  · intro t ht
    obtain ⟨_, k, hk, _⟩ := selectTerms_rows _ _ hselect ht
    exact hw c hc (k, t.1) hk

end NetworkSimplex.ThresholdOracle
