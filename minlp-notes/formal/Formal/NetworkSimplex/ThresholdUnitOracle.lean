import Formal.NetworkSimplex.ThresholdUnitOracleRepair
import Formal.NetworkSimplex.ThresholdUnitOracleExpression

/-! Executable unit separation for the three-label original-coordinate hull. -/
namespace NetworkSimplex.Chain.Threshold

/-- Counted implementation of the recursive coefficient query. -/
def coefficientWithWork {C : Type*} [DecidableEq C] (z : C) : AffineExpression C → ℤ × ℕ
  | .constant _ => (0, 1)
  | .variable w => (if w = z then 1 else 0, 1)
  | .add e f =>
      let a := coefficientWithWork z e
      let b := coefficientWithWork z f
      (a.1 + b.1, a.2 + b.2 + 1)
  | .neg e =>
      let a := coefficientWithWork z e
      (-a.1, a.2 + 1)

theorem coefficientWithWork_spec {C : Type*} [DecidableEq C] (z : C)
    (e : AffineExpression C) :
    coefficientWithWork z e = (e.coefficient z, expressionNodes e) := by
  induction e with
  | constant a => rfl
  | «variable» w => rfl
  | add e f he hf =>
    simp [coefficientWithWork, he, hf, AffineExpression.coefficient, expressionNodes]
  | neg e he => simp [coefficientWithWork, he, AffineExpression.coefficient, expressionNodes]

/-- Scan the actual grouped rows, then repair the selected symbolic cut. The
ledger charges its expression construction and every recursive coefficient visit
and comparison, the gadget-index list, and the constant-size balance append, in
addition to the original arithmetic scan ledger. -/
def threeUnitOracle {L : ℕ} (D : RationalData 3 L) :
    Option (AffineExpression (Coordinate 3 (Fin L))) × ℕ :=
  let scan := threeOracle D
  match scan.1 with
  | none => (none, scan.2)
  | some rows =>
      let repaired := unitRepair (encodedExpression D rows)
      (repaired.1, scan.2 + expressionNodes (encodedExpression D rows) +
        repaired.2 * (expressionNodes (encodedExpression D rows) + 1) + L + 10)

theorem encodedExpression_repairable {L : ℕ} (D : RationalData 3 L)
    {rows : EncodedCut 3 L} (ho : (threeOracle D).1 = some rows) :
    Repairable (encodedExpression D rows) := by
  rcases encodedExpression_shape D ho with ⟨r, _, hr⟩ | ⟨c, hc, hr⟩
  · exact Repairable.congr hr (rowExpression_repairable D.toReal r)
  · exact Repairable.congr hr (circuitExpression_repairable D.toReal hc)

/-- Repair never loses an infeasibility certificate. -/
theorem threeUnitOracle_none_iff {L : ℕ} (D : RationalData 3 L) :
    (threeUnitOracle D).1 = none ↔ ∃ x : Fin 3 → ℝ, D.toReal.ReducedProfile x := by
  rw [← threeOracle_none_iff]
  cases hs : (threeOracle D).1 with
  | none => simp [threeUnitOracle, hs]
  | some rows =>
    obtain ⟨out, ho, _, _⟩ := unitRepair_correct _ (encodedExpression_repairable D hs)
    simp [threeUnitOracle, hs, ho]

theorem threeUnitOracle_cost {L : ℕ} (D : RationalData 3 L) :
    (threeUnitOracle D).2 ≤ 983 * L + 3170 := by
  have hs := threeOracle_charge D
  cases ho : (threeOracle D).1 with
  | none => simp only [threeUnitOracle, ho]; omega
  | some rows =>
    have hr := unitRepair_cost (encodedExpression D rows)
    have hn := encodedExpression_nodes D ho
    have hm : (unitRepair (encodedExpression D rows)).2 *
        (expressionNodes (encodedExpression D rows) + 1) ≤ (L + 2) * 904 :=
      Nat.mul_le_mul hr (by omega)
    simp only [threeUnitOracle, ho]
    omega

/-- Every returned cut is unit and has exactly the selected source cut's value
on the complete real gadget-balance domain. -/
theorem threeUnitOracle_output {L : ℕ} (D : RationalData 3 L)
    {out : AffineExpression (Coordinate 3 (Fin L))}
    (ho : (threeUnitOracle D).1 = some out) :
    UnitFlowProducts out ∧ ∃ rows : EncodedCut 3 L, (threeOracle D).1 = some rows ∧
      ∀ x, (∀ i, (balanceExpression i).eval x = 0) →
        out.eval x = rows.eval (fun r => (rowExpression D.toReal r).eval x) := by
  cases hs : (threeOracle D).1 with
  | none => simp [threeUnitOracle, hs] at ho
  | some rows =>
    obtain ⟨out', hr, hu, hv⟩ := unitRepair_correct _ (encodedExpression_repairable D hs)
    have he : out' = out := by simpa [threeUnitOracle, hs, hr] using ho
    subst out'
    refine ⟨hu, rows, rfl, fun x hx => ?_⟩
    exact (hv x hx).trans (encodedExpression_eval D rows x)

private theorem rowNormal_pattern_eq {L : ℕ} (D : RationalData 3 L)
    (E : ReductionData 3 (Fin L)) (hc : D.c = E.c) (hh : D.observedH = E.observedH)
    (r : ProfileRow 3 (Fin L)) : D.toReal.rowNormal r = E.rowNormal r := by
  cases r <;> simp [ReductionData.rowNormal, RationalData.toReal, hc, hh]

/-- The actual executable separator returns a unit cut strictly violated by the
query and valid at every real point of the same original hull. -/
theorem threeUnitOracle_separates {L : ℕ} (D : RationalData 3 L)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    {out : AffineExpression (Coordinate 3 (Fin L))}
    (ho : (threeUnitOracle D).1 = some out) :
    UnitFlowProducts out ∧ out.eval (coordinates D.toReal D.toReal.xb) < 0 ∧
      ∀ E : ReductionData 3 (Fin L), D.c = E.c → D.observedH = E.observedH →
        E.graphPoint ∈ convexHull ℝ E.graph → 0 ≤ out.eval (coordinates E E.xb) := by
  obtain ⟨hu, rows, hs, heval⟩ := threeUnitOracle_output D ho
  have hbal (E : ReductionData 3 (Fin L)) (i : Fin L) :
      (balanceExpression i).eval (coordinates E E.xb) = 0 := by
    apply balanceExpression_eval
    simp [ReductionData.xb]
  have hquery : out.eval (coordinates D.toReal D.toReal.xb) = rows.eval D.toReal.rowRhs := by
    rw [heval _ (hbal D.toReal)]
    congr 1
    funext r
    exact rowExpression_eval D.toReal D.toReal.xb hc r
  have hnegative : rows.eval D.toReal.rowRhs < 0 := by
    obtain ⟨hv, _, _, _⟩ := NetworkSimplex.ThresholdOracle.circuitOracle_some
      (packedGroup D).table.get (fun r => r.value) threeLibrary hs
    have hv' : (NetworkSimplex.ThresholdOracle.weightedValue
        (fun r : PackedRow 3 L => r.value) rows : ℝ) < 0 := by exact_mod_cast hv
    rw [NetworkSimplex.ThresholdOracle.cast_weightedValue] at hv'
    have hr : NetworkSimplex.ThresholdOracle.realCut
        (fun r : PackedRow 3 L => (r.value : ℝ)) rows = rows.eval D.toReal.rowRhs := by
      unfold NetworkSimplex.ThresholdOracle.realCut EncodedCut.eval
      apply congrArg List.sum
      apply List.map_congr_left
      intro t ht
      dsimp only
      rw [(D.indexedRows_spec packNormal (packed_row_source D threeLibrary hs ht)).2]
    exact hr ▸ hv'
  refine ⟨hu, hquery ▸ hnegative, ?_⟩
  intro E hclasses hbypass hmem
  have hec : ∀ i, E.c i 0 = .neither := by rw [← hclasses]; exact hc
  have heh : E.observedH 0 = false := by rw [← hbypass]; exact hh
  obtain ⟨x, hx⟩ := (E.exists_fullProfile_iff_rows hec heh).mp (E.mem_hull_iff.mp hmem).2
  have hvalid := (packedOracle_separates_real D threeLibrary threeLibrary_cancel hs E x
    (rowNormal_pattern_eq D E hclasses hbypass)
    ((ReductionData.rows_iff_reducedProfile E x).mp hx)).2
  rw [heval _ (hbal E)]
  have hr : (fun r => (rowExpression D.toReal r).eval (coordinates E E.xb)) = E.rowRhs := by
    funext r
    exact rowExpression_eval_other D.toReal E E.xb hclasses hbypass hec r
  rw [hr]
  exact hvalid

end NetworkSimplex.Chain.Threshold
