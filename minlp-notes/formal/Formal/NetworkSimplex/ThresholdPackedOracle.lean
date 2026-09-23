import Formal.NetworkSimplex.ThresholdKeys
import Formal.NetworkSimplex.ThresholdRationalRows
import Formal.NetworkSimplex.ThresholdCircuitOracle

/-! Packed grouping and exact separation of original reduced profile rows. -/
namespace NetworkSimplex.Chain.Threshold
open NetworkSimplex.ThresholdGrouping NetworkSimplex.ThresholdOracle
open scoped BigOperators

abbrev PackedRow (m L : ℕ) := IndexedRow (normalKeyCount m) (ProfileRow m (Fin L))
abbrev EncodedCut (m L : ℕ) := List (ℕ × PackedRow m L)

def packedGroup {m L : ℕ} (D : RationalData m L) := group (D.indexedRows packNormal)

def packedOracle {m L : ℕ} (D : RationalData m L)
    (library : List (Circuit (normalKeyCount m))) : Option (EncodedCut m L) × ℕ :=
  let grouped := packedGroup D
  let result := circuitOracle grouped.table.get (fun r => r.value) library
  (result.1, D.arithmeticCharge + grouped.comparisons + result.2)

/-- The table is equivalent to all actual source inequalities, including zero normals. -/
theorem packed_constraints {m L : ℕ} (D : RationalData m L) (x : Fin m → ℝ) :
    (∀ k r, (packedGroup D).table.get k = some r → keyValue k x ≤ (r.value : ℝ)) ↔
      D.toReal.ReducedProfile x := by
  exact (group_real_constraints_iff (D.indexedRows packNormal) (fun k => keyValue k x)).trans
    (D.indexedRows_constraints packNormal keyValue keyValue_packNormal x)

theorem packed_row_source {m L : ℕ} (D : RationalData m L)
    (library : List (Circuit (normalKeyCount m))) {rows : EncodedCut m L}
    (ho : (packedOracle D library).1 = some rows) {t : ℕ × PackedRow m L} (ht : t ∈ rows) :
    t.2 ∈ D.indexedRows packNormal :=
  groupedCircuitOracle_original_rows (D.indexedRows packNormal) library ho ht

/-- The output is an affine cut encoded by its integer weights and original row
identifiers. The chosen rows remain fixed when the candidate point changes. -/
def EncodedCut.eval {m L : ℕ} (rows : EncodedCut m L)
    (valueAt : ProfileRow m (Fin L) → ℝ) : ℝ :=
  realCut (fun r => valueAt r.payload) rows

theorem packedOracle_separates {m L : ℕ} (D : RationalData m L)
    (library : List (Circuit (normalKeyCount m)))
    (hc : ∀ c ∈ library, ∀ x : Fin m → ℝ,
      (c.map fun t => (t.2 : ℝ) * keyValue t.1 x).sum = 0)
    {rows : EncodedCut m L} (ho : (packedOracle D library).1 = some rows)
    (E : RationalData m L) (hx : Fin m → ℝ)
    (hn : ∀ r, D.toReal.rowNormal r = E.toReal.rowNormal r)
    (hf : E.toReal.ReducedProfile hx) :
    rows.eval D.toReal.rowRhs < 0 ∧ 0 ≤ rows.eval E.toReal.rowRhs := by
  have hf' : ∀ r ∈ D.indexedRows packNormal,
      keyValue r.key hx ≤ E.toReal.rowRhs r.payload := by
    intro r hr
    have hspec := D.indexedRows_spec packNormal hr
    rw [hspec.1, keyValue_packNormal, hn]
    exact (ReductionData.rows_iff_reducedProfile E.toReal hx).mpr hf r.payload
  have hh := groupedCircuitOracle_separates (D.indexedRows packNormal) library
    (fun r => E.toReal.rowRhs r) (fun k => keyValue k hx) hf'
    (fun c hc' => hc c hc' hx) ho
  have hq : realCut (fun r : PackedRow m L => (r.value : ℝ)) rows =
      rows.eval D.toReal.rowRhs := by
    unfold realCut EncodedCut.eval
    apply congrArg List.sum
    apply List.map_congr_left
    intro t ht
    dsimp only
    rw [(D.indexedRows_spec packNormal (packed_row_source D library ho ht)).2]
  rw [hq] at hh
  exact hh

/-- Global validity also holds at arbitrary real feasible points. -/
theorem packedOracle_separates_real {m L : ℕ} (D : RationalData m L)
    (library : List (Circuit (normalKeyCount m)))
    (hc : ∀ c ∈ library, ∀ x : Fin m → ℝ,
      (c.map fun t => (t.2 : ℝ) * keyValue t.1 x).sum = 0)
    {rows : EncodedCut m L} (ho : (packedOracle D library).1 = some rows)
    (E : ReductionData m (Fin L)) (hx : Fin m → ℝ)
    (hn : ∀ r, D.toReal.rowNormal r = E.rowNormal r)
    (hf : E.ReducedProfile hx) :
    rows.eval D.toReal.rowRhs < 0 ∧ 0 ≤ rows.eval E.rowRhs := by
  have hf' : ∀ r ∈ D.indexedRows packNormal,
      keyValue r.key hx ≤ E.rowRhs r.payload := by
    intro r hr
    have hspec := D.indexedRows_spec packNormal hr
    rw [hspec.1, keyValue_packNormal, hn]
    exact (ReductionData.rows_iff_reducedProfile E hx).mpr hf r.payload
  have hh := groupedCircuitOracle_separates (D.indexedRows packNormal) library
    (fun r => E.rowRhs r) (fun k => keyValue k hx) hf'
    (fun c hc' => hc c hc' hx) ho
  have hq : realCut (fun r : PackedRow m L => (r.value : ℝ)) rows =
      rows.eval D.toReal.rowRhs := by
    unfold realCut EncodedCut.eval
    apply congrArg List.sum
    apply List.map_congr_left
    intro t ht
    dsimp only
    rw [(D.indexedRows_spec packNormal (packed_row_source D library ho ht)).2]
  rw [hq] at hh
  exact hh

/-- Arithmetic work includes actual cached row generation, grouping comparisons,
and the actual tested library prefix. Key operations are counted separately. -/
theorem packedOracle_arithmeticCharge {m L : ℕ} (D : RationalData m L)
    (hm : 1 ≤ m) (library : List (Circuit (normalKeyCount m))) :
    (packedOracle D library).2 ≤ 26 * m * (L + 1) +
      (library.map (fun c => 2 * c.length + 1)).sum := by
  have hd := D.arithmeticCharge_linear hm
  have hg := (group_cost (D.indexedRows packNormal)).1
  rw [D.indexedRows_length packNormal] at hg
  have hc := circuitOracle_cost (packedGroup D).table.get (fun r => r.value) library
  change D.arithmeticCharge + (group (D.indexedRows packNormal)).comparisons +
    (circuitOracle (packedGroup D).table.get (fun r => r.value) library).2 ≤ _
  nlinarith

end NetworkSimplex.Chain.Threshold
