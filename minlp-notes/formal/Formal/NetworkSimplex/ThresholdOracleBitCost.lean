import Formal.NetworkSimplex.ThresholdOracleSize
import Formal.NetworkSimplex.ThresholdThreePacked
import Formal.ReciprocalAnchor.ManyBitCost

/-!
Operand bounds and a schoolbook bit-work model for the actual packed oracle.
The operation count comes from its implemented row generation, grouping, and
circuit scan. All generated-row and tested-circuit operands are bounded below,
including partial sums and tests that do not return a violated circuit.

The primitive model is the established digit-scan, schoolbook multiplication,
long-division, and Euclidean-normalization model. This does not assert a runtime
refinement of Lean's compiled `Rat` arithmetic or its array implementation.
-/
namespace NetworkSimplex.Chain.Threshold
open ReciprocalAnchor
open NetworkSimplex.ThresholdGrouping NetworkSimplex.ThresholdOracle
open ReciprocalAnchor.ManyLeaf.BitCost
namespace RationalData

/-- Every partial input sum used in a cached residual has the same size bound. -/
theorem filtered_partial_bits {m L B : ℕ} {D : RationalData m L} (h : D.InputBits B)
    (f : Fin (m + 1) → ℚ) (hf : ∀ j, RationalBits (f j) B)
    (P : Fin (m + 1) → Prop) [DecidablePred P] {part : List ℚ}
    (hp : part.Sublist (List.ofFn fun j => if P j then f j else 0)) :
    RationalBits part.sum (rowBits m B) := by
  have ht : ∀ q ∈ part, RationalBits q B := by
    intro q hq
    obtain ⟨j, rfl⟩ := List.mem_ofFn.mp (hp.subset hq)
    split_ifs
    · exact hf j
    · exact rationalBits_mono rationalBits_zero h.pos
  have hl : part.length ≤ m + 1 := by simpa only [List.length_ofFn] using hp.length_le
  apply rationalBits_mono (input_sum_bits h ht hl)
  unfold rowBits
  nlinarith

/-- Rational intermediates for global rows, including the cached total. -/
def globalOperandTrace {m L : ℕ} (D : RationalData m L) (j : Fin (m + 1)) : List ℚ :=
  [0, 1, D.xh, D.total, D.weights j, D.zh j, D.weights 0,
    D.weights 0 - D.total, D.zh j - D.weights j, D.weights j - D.zh j]

theorem globalOperandTrace_bits {m L B : ℕ} {D : RationalData m L} (h : D.InputBits B)
    (j : Fin (m + 1)) : ∀ q ∈ D.globalOperandTrace j, RationalBits q (rowBits m B) := by
  have htotal := total_bits h
  simp only [globalOperandTrace, List.forall_mem_cons, List.mem_nil_iff, false_implies,
    forall_const, and_true]
  exact ⟨rationalBits_mono rationalBits_zero (by unfold rowBits; nlinarith),
    rationalBits_mono rationalBits_one (by unfold rowBits; nlinarith),
    rationalBits_mono h.xh (by unfold rowBits; nlinarith),
    rationalBits_mono htotal (by unfold rowBits; nlinarith),
    rationalBits_mono (h.weights j) (by unfold rowBits; nlinarith),
    rationalBits_mono (h.zh j) (by unfold rowBits; nlinarith),
    rationalBits_mono (h.weights 0) (by unfold rowBits; nlinarith),
    rationalBits_mono (rationalBits_sub (h.weights 0) htotal) (by unfold rowBits; nlinarith),
    rationalBits_mono (rationalBits_sub (h.zh j) (h.weights j)) (by unfold rowBits; nlinarith),
    rationalBits_mono (rationalBits_sub (h.weights j) (h.zh j)) (by unfold rowBits; nlinarith)⟩

/-- All arithmetic intermediates for residuals and gadget rows. Conditional rows
select from these values or zero; no additional arithmetic is hidden by a branch. -/
def gadgetOperandTrace {m L : ℕ} (D : RationalData m L) (i : Fin L)
    (j : Fin (m + 1)) : List ℚ :=
  let A := (List.ofFn fun k => if observesA (D.c i k) then D.u i k else 0).sum
  let V := (List.ofFn fun k => if D.c i k = .bOnly then D.v i k else 0).sum
  [D.xa i, D.u i j, D.v i j, A, V, D.xa i - A, D.residual i,
    D.u i j + D.v i j, -D.u i j, -D.v i j, -(D.u i j + D.v i j),
    D.total, D.total - D.residual i]

theorem gadgetOperandTrace_bits {m L B : ℕ} {D : RationalData m L} (h : D.InputBits B)
    (i : Fin L) (j : Fin (m + 1)) :
    ∀ q ∈ D.gadgetOperandTrace i j, RationalBits q (rowBits m B) := by
  have hz := rationalBits_mono rationalBits_zero (show 1 ≤ B from h.pos)
  have hsum (f : Fin (m + 1) → ℚ) (hf : ∀ k, RationalBits (f k) B)
      (P : Fin (m + 1) → Prop) [DecidablePred P] :
      RationalBits (List.ofFn fun k => if P k then f k else 0).sum
        (1 + (m + 1) * (B + 1)) := by
    apply input_sum_bits h
    · intro q hq
      obtain ⟨k, rfl⟩ := List.mem_ofFn.mp hq
      split_ifs <;> first | exact hf k | exact hz
    · simp
  have hA := hsum (D.u i) (h.u i) (fun k => observesA (D.c i k))
  have hV := hsum (D.v i) (h.v i) (fun k => D.c i k = .bOnly)
  have hres := residual_bits h i
  have ht := total_bits h
  have huv := rationalBits_add (h.u i j) (h.v i j)
  simp only [gadgetOperandTrace, List.forall_mem_cons, List.mem_nil_iff, false_implies,
    forall_const, and_true]
  exact ⟨rationalBits_mono (h.xa i) (by unfold rowBits; nlinarith),
    rationalBits_mono (h.u i j) (by unfold rowBits; nlinarith),
    rationalBits_mono (h.v i j) (by unfold rowBits; nlinarith),
    rationalBits_mono hA (by unfold rowBits; nlinarith),
    rationalBits_mono hV (by unfold rowBits; nlinarith),
    rationalBits_mono (rationalBits_sub (h.xa i) hA) (by unfold rowBits; nlinarith),
    rationalBits_mono hres (by unfold rowBits; nlinarith),
    rationalBits_mono huv (by unfold rowBits; nlinarith),
    rationalBits_mono (rationalBits_neg (h.u i j)) (by unfold rowBits; nlinarith),
    rationalBits_mono (rationalBits_neg (h.v i j)) (by unfold rowBits; nlinarith),
    rationalBits_mono (rationalBits_neg huv) (by unfold rowBits; nlinarith),
    rationalBits_mono ht (by unfold rowBits; nlinarith),
    rationalBits_mono (rationalBits_sub ht hres) (by unfold rowBits; nlinarith)⟩

/-- Grouping comparisons, at every prefix, use actual original row values. -/
theorem grouping_prefix_operand_bits {K m L B : ℕ} {D : RationalData m L}
    (h : D.InputBits B) (key : ProfileNormal m → Fin K)
    {seenRows : List (IndexedRow K (ProfileRow m (Fin L)))}
    (hp : seenRows.Sublist (D.indexedRows key)) (k : Fin K)
    {old incoming : IndexedRow K (ProfileRow m (Fin L))}
    (hold : (group seenRows).table.get k = some old)
    (hin : incoming ∈ D.indexedRows key) :
    RationalBits old.value (rowBits m B) ∧ RationalBits incoming.value (rowBits m B) :=
  ⟨indexedRows_bits h key (hp.subset (group_minimum seenRows k hold).1),
    indexedRows_bits h key hin⟩

end RationalData
end NetworkSimplex.Chain.Threshold

namespace NetworkSimplex.ThresholdOracle
open ReciprocalAnchor NetworkSimplex.ThresholdGrouping

/-- All successful selections are bounded, regardless of whether their circuit is violated. -/
theorem tested_selection_bits {K m L B W S : ℕ}
    {D : Chain.Threshold.RationalData m L} (h : D.InputBits B)
    (key : Chain.ProfileNormal m → Fin K) (c : Circuit K) (hlen : c.length ≤ S)
    (hw : ∀ t ∈ c, RationalBits (t.2 : ℚ) W)
    {rows : List (ℕ × IndexedRow K (Chain.ProfileRow m (Fin L)))}
    (hs : selectTerms (group (D.indexedRows key)).table.get c = some rows) :
    (∀ t ∈ rows, RationalBits t.2.value (Chain.Threshold.RationalData.rowBits m B) ∧
      RationalBits (t.1 : ℚ) W ∧
      RationalBits ((t.1 : ℚ) * t.2.value) (Chain.Threshold.RationalData.rowBits m B + W)) ∧
    ∀ part, part.Sublist rows → RationalBits (weightedValue (fun r => r.value) part)
      (1 + S * (Chain.Threshold.RationalData.rowBits m B + W + 1)) := by
  have hterms (t : ℕ × IndexedRow K (Chain.ProfileRow m (Fin L))) (ht : t ∈ rows) :
      RationalBits t.2.value (Chain.Threshold.RationalData.rowBits m B) ∧
        RationalBits (t.1 : ℚ) W := by
    obtain ⟨_, k, hk, hr⟩ := selectTerms_rows _ _ hs ht
    exact ⟨Chain.Threshold.RationalData.indexedRows_bits h key
      (group_minimum (D.indexedRows key) k hr).1, hw _ hk⟩
  constructor
  · intro t ht
    obtain ⟨hr, hw⟩ := hterms t ht
    exact ⟨hr, hw, by simpa only [Nat.add_comm] using rationalBits_mul hw hr⟩
  · intro part hp
    have hsize := (selectTerms_length _ _ hs).trans hlen
    apply rationalBits_mono (weightedValue_partial_bits (fun r => r.value) rows
      (fun t ht => (hterms t ht).1) (fun t ht => (hterms t ht).2) hp)
    exact Nat.add_le_add_left (Nat.mul_le_mul_right _ hsize) 1

end NetworkSimplex.ThresholdOracle

namespace NetworkSimplex.Chain.Threshold
open ReciprocalAnchor NetworkSimplex.ThresholdOracle
open ReciprocalAnchor.ManyLeaf.BitCost

/-- A common width includes source rows, weights, products, and every tested partial sum. -/
def oracleBits (m B W S : ℕ) : ℕ :=
  max (RationalData.rowBits m B + W + 1) (1 + S * (RationalData.rowBits m B + W + 1))

theorem rowBits_le_oracleBits (m B W S : ℕ) : RationalData.rowBits m B ≤ oracleBits m B W S :=
  (by omega : RationalData.rowBits m B ≤ RationalData.rowBits m B + W + 1).trans
    (Nat.le_max_left _ _)

/-- The common width applies to all operands of every successfully selected circuit,
including circuits whose weighted value is nonnegative and which are therefore skipped. -/
theorem packed_tested_operand_bits {m L B W S : ℕ} {D : RationalData m L}
    (h : D.InputBits B) (c : Circuit (normalKeyCount m)) (hlen : c.length ≤ S)
    (hw : ∀ t ∈ c, RationalBits (t.2 : ℚ) W) {rows : EncodedCut m L}
    (hs : selectTerms (packedGroup D).table.get c = some rows) :
    (∀ t ∈ rows, RationalBits t.2.value (oracleBits m B W S) ∧
      RationalBits (t.1 : ℚ) (oracleBits m B W S) ∧
      RationalBits ((t.1 : ℚ) * t.2.value) (oracleBits m B W S)) ∧
    ∀ part, part.Sublist rows → RationalBits (weightedValue (fun r => r.value) part)
      (oracleBits m B W S) := by
  have hh := tested_selection_bits h packNormal c hlen hw hs
  have hmax : RationalData.rowBits m B + W + 1 ≤ oracleBits m B W S := Nat.le_max_left _ _
  constructor
  · intro t ht
    obtain ⟨hr, hw, hp⟩ := hh.1 t ht
    exact ⟨rationalBits_mono hr (by omega), rationalBits_mono hw (by omega),
      rationalBits_mono hp (by omega)⟩
  · intro part hp
    exact rationalBits_mono (hh.2 part hp) (Nat.le_max_right _ _)

/-- The bit budget uses the actual oracle charge, not the library's worst-case prefix length. -/
def packedOracleBitWork {m L : ℕ} (D : RationalData m L)
    (library : List (Circuit (normalKeyCount m))) (B W S : ℕ) : ℕ :=
  bitWorkBudget (packedOracle D library).2 (oracleBits m B W S)

theorem packedOracleBitWork_le {m L : ℕ} (D : RationalData m L) (hm : 1 ≤ m)
    (library : List (Circuit (normalKeyCount m))) (B W S : ℕ) :
    packedOracleBitWork D library B W S ≤
      (26 * m * (L + 1) + (library.map (fun c => 2 * c.length + 1)).sum) *
        (256 * (oracleBits m B W S + 1) ^ 3) :=
  bitWorkBudget_le (packedOracle_arithmeticCharge D hm library) le_rfl

/-- Every primitive on bounded oracle operands has the stated modeled bit cost. -/
theorem oracle_primitive_cost {m B W S : ℕ} {q r : ℚ}
    (hq : RationalBits q (oracleBits m B W S))
    (hr : RationalBits r (oracleBits m B W S)) (op : RationalPrimitive) :
    primitiveBitCost op q r (oracleBits m B W S) ≤
      256 * (oracleBits m B W S + 1) ^ 3 := primitiveBitCost_le hq hr op

theorem threeLibrary_size_weights :
    (∀ c ∈ threeLibrary, c.length ≤ 11) ∧
    (∀ c ∈ threeLibrary, ∀ t ∈ c, RationalBits (t.2 : ℚ) 2) := by
  constructor
  · decide +kernel
  · have h : ∀ c ∈ threeLibrary, ∀ t ∈ c, t.2 < 4 := by decide +kernel
    intro c hc t ht
    exact nat_weight_bits (h c hc t ht) (by decide)

/-- The concrete three-label width accounts for all eleven positions, including skipped zeros. -/
def threeOracleBits (B : ℕ) : ℕ := 1 + 11 * (RationalData.rowBits 3 B + 3)

theorem oracleBits_three (B : ℕ) : oracleBits 3 B 2 11 = threeOracleBits B := by
  unfold oracleBits threeOracleBits
  apply max_eq_right
  omega

/-- Every partial sum in every tested three-label circuit has the concrete width. -/
theorem three_tested_partial_bits {L B : ℕ} {D : RationalData 3 L} (h : D.InputBits B)
    (c : Circuit (normalKeyCount 3)) (hc : c ∈ threeLibrary) {rows : EncodedCut 3 L}
    (hs : selectTerms (packedGroup D).table.get c = some rows)
    (part : EncodedCut 3 L) (hp : part.Sublist rows) :
    RationalBits (weightedValue (fun r => r.value) part) (threeOracleBits B) :=
  (tested_selection_bits h packNormal c (threeLibrary_size_weights.1 c hc)
    (threeLibrary_size_weights.2 c hc) hs).2 part hp

def threeOracleBitWork {L : ℕ} (D : RationalData 3 L) (B : ℕ) : ℕ :=
  bitWorkBudget (threeOracle D).2 (threeOracleBits B)

/-- In the explicit schoolbook model, fixed-three-label separation has linear data-size
factor and a cubic input-bit factor. Array/key bookkeeping is a separate cost model. -/
theorem threeOracleBitWork_polynomial {L : ℕ} (D : RationalData 3 L) (B : ℕ) :
    threeOracleBitWork D B ≤ (78 * (L + 1) + 371) *
      (256 * (132 * B + 299) ^ 3) := by
  apply bitWorkBudget_le (threeOracle_charge D)
  unfold threeOracleBits RationalData.rowBits
  omega

end NetworkSimplex.Chain.Threshold
