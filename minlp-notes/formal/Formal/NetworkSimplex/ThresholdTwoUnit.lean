import Formal.NetworkSimplex.ThresholdTwoProducts

/-! Every actual affine branch of the five two-label circuits has unit coefficients. -/
namespace NetworkSimplex.Chain.Threshold.TwoLabels
open scoped BigOperators
open TwoStateCircuits
variable {I : Type*} [DecidableEq I]

omit [DecidableEq I] in
private theorem branch_rows_injective (D : ReductionData 2 I) (c : Fin 5)
    (r : Fin 6 → ProfileRow 2 I) (hr : TwoBranch D c r) {k l : Fin 6}
    (hk : weight c k ≠ 0) (hl : weight c l ≠ 0) (he : r k = r l) : k = l := by
  apply normal_injective
  rw [← hr k hk, ← hr l hl, he]

theorem twoBranch_aFlow_unit (D : ReductionData 2 I) (c : Fin 5)
    (r : Fin 6 → ProfileRow 2 I) (hr : TwoBranch D c r) (i : I) :
    -1 ≤ ∑ k, weight c k * rowCoefficient D (r k) (.aFlow i) ∧
      (∑ k, weight c k * rowCoefficient D (r k) (.aFlow i)) ≤ 1 := by
  apply sum_unit_of_unique_signs
  · intro k
    have hf := row_flow_product_unit D (r k) (.aFlow i) trivial
    have hw := weight_nonnegative c k
    have hw' := weight_le_one c k
    interval_cases h : weight c k <;> simp_all
  · intro k l hk hl
    have hwk : weight c k ≠ 0 := by intro h; simp [h] at hk
    have hwl : weight c l ≠ 0 := by intro h; simp [h] at hl
    have hpk : 0 < rowCoefficient D (r k) (.aFlow i) := by
      nlinarith [weight_nonnegative c k]
    have hpl : 0 < rowCoefficient D (r l) (.aFlow i) := by
      nlinarith [weight_nonnegative c l]
    have hek : r k = .endpointB i := by
      rw [row_aFlow_coefficient] at hpk
      split_ifs at hpk <;> simp_all
    have hel : r l = .endpointB i := by
      rw [row_aFlow_coefficient] at hpl
      split_ifs at hpl <;> simp_all
    exact branch_rows_injective D c r hr hwk hwl (hek.trans hel.symm)
  · intro k l hk hl
    have hwk : weight c k ≠ 0 := by intro h; simp [h] at hk
    have hwl : weight c l ≠ 0 := by intro h; simp [h] at hl
    have hpk : rowCoefficient D (r k) (.aFlow i) < 0 := by
      nlinarith [weight_nonnegative c k]
    have hpl : rowCoefficient D (r l) (.aFlow i) < 0 := by
      nlinarith [weight_nonnegative c l]
    have hek : r k = .endpointA i := by
      rw [row_aFlow_coefficient] at hpk
      split_ifs at hpk <;> simp_all
    have hel : r l = .endpointA i := by
      rw [row_aFlow_coefficient] at hpl
      split_ifs at hpl <;> simp_all
    exact branch_rows_injective D c r hr hwk hwl (hek.trans hel.symm)

private theorem actual_row_bypass_pattern (D : ReductionData 2 I) (r : ProfileRow 2 I)
    (k : Fin 6) (hn : normalVector (D.rowNormal r) = normal k) :
    (k.val < 3 → -1 ≤ rowCoefficient D r .bypassFlow ∧ rowCoefficient D r .bypassFlow ≤ 0) ∧
    (k = 3 ∨ k = 4 → rowCoefficient D r .bypassFlow = 0) ∧
    (k = 5 → rowCoefficient D r .bypassFlow = 1) := by
  rw [row_bypassFlow_coefficient]
  fin_cases k <;> cases r <;> simp only [ReductionData.rowNormal] at hn <;>
    (try split_ifs at hn) <;>
    simp_all [negativeBypassRow, normalVector, TwoStateCircuits.normal, funext_iff,
      Fin.forall_fin_succ] <;> (try split_ifs at hn) <;> aesop

theorem twoBranch_bypassFlow_unit (D : ReductionData 2 I) (c : Fin 5)
    (r : Fin 6 → ProfileRow 2 I) (hr : TwoBranch D c r) :
    -1 ≤ ∑ k, weight c k * rowCoefficient D (r k) .bypassFlow ∧
      (∑ k, weight c k * rowCoefficient D (r k) .bypassFlow) ≤ 1 := by
  have h (k : Fin 6) (hk : weight c k ≠ 0) := actual_row_bypass_pattern D (r k) k (hr k hk)
  have h0 := h 0
  have h1 := h 1
  have h2 := h 2
  have h3 := h 3
  have h4 := h 4
  have h5 := h 5
  fin_cases c <;> simp [weight, Fin.sum_univ_succ] at h0 h1 h2 h3 h4 h5 ⊢ <;> omega

/-- All five exact branches are unit in the original flow/product coordinates. -/
theorem twoBranch_flow_product_unit (D : ReductionData 2 I) (c : Fin 5)
    (r : Fin 6 → ProfileRow 2 I) (hr : TwoBranch D c r)
    (z : Coordinate 2 I) (hz : FlowOrProduct z) :
    -1 ≤ ∑ k, weight c k * rowCoefficient D (r k) z ∧
      (∑ k, weight c k * rowCoefficient D (r k) z) ≤ 1 := by
  cases z with
  | bypassFlow => exact twoBranch_bypassFlow_unit D c r hr
  | aFlow i => exact twoBranch_aFlow_unit D c r hr i
  | bFlow i => simp
  | aProduct i j => exact twoBranch_aProduct_unit D c r hr i j
  | bProduct i j => exact twoBranch_bProduct_unit D c r hr i j
  | bypassProduct j => exact twoBranch_bypassProduct_unit D c r hr j
  | weight j => exact False.elim hz

/-- The literal original-coordinate affine expression for a five-circuit branch. -/
def circuitExpression (D : ReductionData 2 I) (c : Fin 5) (r : Fin 6 → ProfileRow 2 I) :
    AffineExpression (Coordinate 2 I) :=
  AffineExpression.sum fun k => if weight c k = 1 then rowExpression D (r k) else .constant 0

theorem circuitExpression_coefficient (D : ReductionData 2 I) (c : Fin 5)
    (r : Fin 6 → ProfileRow 2 I) (z : Coordinate 2 I) :
    (circuitExpression D c r).coefficient z = ∑ k, weight c k * rowCoefficient D (r k) z := by
  rw [circuitExpression, AffineExpression.coefficient_sum]
  apply Finset.sum_congr rfl
  intro k _
  have hw := weight_nonnegative c k
  have hw' := weight_le_one c k
  interval_cases hk : weight c k <;> simp [AffineExpression.coefficient, rowCoefficient]

omit [DecidableEq I] in
theorem circuitExpression_eval (D : ReductionData 2 I) (c : Fin 5)
    (r : Fin 6 → ProfileRow 2 I) (xb : I → ℝ) (hc : ∀ i, D.c i 0 = .neither) :
    (circuitExpression D c r).eval (coordinates D xb) = ∑ k, (weight c k : ℝ) * D.rowRhs (r k) := by
  rw [circuitExpression, AffineExpression.eval_sum]
  apply Finset.sum_congr rfl
  intro k _
  have hw := weight_nonnegative c k
  have hw' := weight_le_one c k
  interval_cases hk : weight c k <;> simp [AffineExpression.eval, rowExpression_eval D xb hc]

theorem circuitExpression_unit (D : ReductionData 2 I) (c : Fin 5)
    (r : Fin 6 → ProfileRow 2 I) (hr : TwoBranch D c r)
    (z : Coordinate 2 I) (hz : FlowOrProduct z) :
    -1 ≤ (circuitExpression D c r).coefficient z ∧ (circuitExpression D c r).coefficient z ≤ 1 := by
  rw [circuitExpression_coefficient]
  exact twoBranch_flow_product_unit D c r hr z hz

end NetworkSimplex.Chain.Threshold.TwoLabels
