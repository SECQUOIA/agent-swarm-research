import Formal.NetworkSimplex.ThresholdUnitOracleShape
import Formal.NetworkSimplex.ThresholdFlowRepresentative

/-! Executable symbolic expressions for encoded original-row certificates. -/
namespace NetworkSimplex.Chain.Threshold
open NetworkSimplex.ThresholdOracle
open scoped BigOperators

/-- Only the observation pattern is read when constructing symbolic rows. -/
def RationalData.patternData {m L : ℕ} (D : RationalData m L) : ReductionData m (Fin L) where
  c := D.c
  u := fun _ _ => 0
  v := fun _ _ => 0
  weights := fun _ => 0
  xa := fun _ => 0
  xh := 0
  observedH := D.observedH
  zh := fun _ => 0

def encodedExpression {m L : ℕ} (D : RationalData m L) (rows : EncodedCut m L) :
    AffineExpression (Coordinate m (Fin L)) :=
  .sumList (rows.flatMap fun t => List.replicate t.1 (rowExpression D.patternData t.2.payload))

theorem patternData_rowExpression {m L : ℕ} (D : RationalData m L)
    (r : ProfileRow m (Fin L)) :
    rowExpression D.patternData r = rowExpression D.toReal r :=
  rowExpression_eq_of_pattern_eq _ _ rfl rfl r

private theorem sum_replicated {α : Type*} (xs : List (ℕ × α)) (f : α → ℝ) :
    (xs.flatMap fun t => List.replicate t.1 (f t.2)).sum =
      (xs.map fun t => (t.1 : ℝ) * f t.2).sum := by
  induction xs with
  | nil => simp
  | cons t xs ih => simp [ih, List.sum_replicate, nsmul_eq_mul]

theorem encodedExpression_eval {m L : ℕ} (D : RationalData m L)
    (rows : EncodedCut m L) (x : Coordinate m (Fin L) → ℝ) :
    (encodedExpression D rows).eval x = rows.eval (fun r => (rowExpression D.toReal r).eval x) := by
  simp only [encodedExpression, AffineExpression.eval_sumList, List.map_flatMap,
    List.map_replicate, patternData_rowExpression, EncodedCut.eval, realCut]
  exact sum_replicated rows (fun r => (rowExpression D.toReal r.payload).eval x)

theorem encodedExpression_coefficient {m L : ℕ} (D : RationalData m L)
    (rows : EncodedCut m L) (z : Coordinate m (Fin L)) :
    ((encodedExpression D rows).coefficient z : ℝ) =
      rows.eval (fun r => ((rowExpression D.toReal r).coefficient z : ℝ)) := by
  simp only [encodedExpression, AffineExpression.coefficient_sumList, List.map_flatMap,
    List.map_replicate, patternData_rowExpression, EncodedCut.eval, realCut, Int.cast_list_sum]
  exact sum_replicated rows (fun r => ((rowExpression D.toReal r.payload).coefficient z : ℝ))

/-- Coefficients of the actual executable output are those of one source row or
one actual source circuit. No numerical candidate values appear in this identity. -/
theorem encodedExpression_shape {L : ℕ} (D : RationalData 3 L)
    {rows : EncodedCut 3 L} (ho : (threeOracle D).1 = some rows) :
    (∃ r : ProfileRow 3 (Fin L), normalVector (D.toReal.rowNormal r) = 0 ∧
      ∀ z, (encodedExpression D rows).coefficient z = (rowExpression D.toReal r).coefficient z) ∨
    (∃ c : Fin 16, ThreeBranch D.toReal c (selectedThreeBranch D) ∧
      ∀ z, (encodedExpression D rows).coefficient z =
        (circuitExpression D.toReal c (selectedThreeBranch D)).coefficient z) := by
  rcases threeOracle_output_shape D ho with ⟨r, hr, he⟩ | ⟨c, hc, he⟩
  · left
    refine ⟨r, hr, fun z => ?_⟩
    have hh := (encodedExpression_coefficient D rows z).trans (he _)
    exact_mod_cast hh
  · right
    refine ⟨c, hc, fun z => ?_⟩
    rw [circuitExpression_coefficient]
    have hh := (encodedExpression_coefficient D rows z).trans (he _)
    unfold circuitCoefficient rowCoefficient
    exact_mod_cast hh

/-- Syntax-tree node count, also bounding one recursive coefficient query. -/
def expressionNodes {C : Type*} : AffineExpression C → ℕ
  | .constant _ | .variable _ => 1
  | .add e f => expressionNodes e + expressionNodes f + 1
  | .neg e => expressionNodes e + 1

theorem rowExpression_nodes {L : ℕ} (D : RationalData 3 L)
    (r : ProfileRow 3 (Fin L)) : expressionNodes (rowExpression D.patternData r) ≤ 40 := by
  cases r <;>
    simp [rowExpression, residualExpression, totalExpression, AffineExpression.sum,
      AffineExpression.sumList, expressionNodes, apply_ite] <;> split_ifs <;> norm_num

private theorem threeLibrary_bounds :
    ∀ c ∈ threeLibrary, c.length ≤ 11 ∧ ∀ t ∈ c, t.2 ≤ 2 := by decide +kernel

theorem threeOracle_rows_bounds {L : ℕ} (D : RationalData 3 L)
    {rows : EncodedCut 3 L} (ho : (threeOracle D).1 = some rows) :
    rows.length ≤ 11 ∧ ∀ t ∈ rows, t.1 ≤ 2 := by
  obtain ⟨_, c, hc, hs⟩ := circuitOracle_some (packedGroup D).table.get
    (fun r => r.value) threeLibrary ho
  refine ⟨(selectTerms_length _ _ hs).trans (threeLibrary_bounds c hc).1, ?_⟩
  intro t ht
  obtain ⟨_, k, hk, _⟩ := selectTerms_rows _ _ hs ht
  exact (threeLibrary_bounds c hc).2 (k, t.1) hk

private theorem sumList_nodes_bound {C : Type*} (es : List (AffineExpression C))
    (B : ℕ) (hb : ∀ e ∈ es, expressionNodes e ≤ B) :
    expressionNodes (.sumList es) ≤ es.length * (B + 1) + 1 := by
  induction es with
  | nil => simp [AffineExpression.sumList, expressionNodes]
  | cons e es ih =>
    have he := hb e (by simp)
    have ht := ih (fun f hf => hb f (List.mem_cons_of_mem e hf))
    simp only [AffineExpression.sumList, expressionNodes, List.length_cons]
    nlinarith

private theorem replicated_length_bound {α β : Type*} (rows : List (ℕ × α))
    (f : α → β) (hw : ∀ t ∈ rows, t.1 ≤ 2) :
    (rows.flatMap fun t => List.replicate t.1 (f t.2)).length ≤ 2 * rows.length := by
  induction rows with
  | nil => simp
  | cons t rows ih =>
    have h := hw t (by simp)
    have ht := ih (fun u hu => hw u (List.mem_cons_of_mem t hu))
    simp only [List.flatMap_cons, List.length_append, List.length_replicate, List.length_cons]
    omega

/-- The symbolic output has bounded size independent of the number of gadgets.
Together with the recursive coefficient function this bounds each repair query. -/
theorem encodedExpression_nodes {L : ℕ} (D : RationalData 3 L)
    {rows : EncodedCut 3 L} (ho : (threeOracle D).1 = some rows) :
    expressionNodes (encodedExpression D rows) ≤ 903 := by
  have hr := threeOracle_rows_bounds D ho
  let es := rows.flatMap fun t => List.replicate t.1 (rowExpression D.patternData t.2.payload)
  have hl : es.length ≤ 22 := (replicated_length_bound rows
    (fun r => rowExpression D.patternData r.payload) hr.2).trans (by omega)
  have hb : ∀ e ∈ es, expressionNodes e ≤ 40 := by
    intro e he
    obtain ⟨t, _, ht⟩ := List.mem_flatMap.mp he
    have heq := (List.mem_replicate.mp ht).2
    subst e
    exact rowExpression_nodes D t.2.payload
  have hn := sumList_nodes_bound es 40 hb
  change expressionNodes (.sumList es) ≤ 903
  omega

end NetworkSimplex.Chain.Threshold
