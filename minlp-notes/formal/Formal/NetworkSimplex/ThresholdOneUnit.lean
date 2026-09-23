import Formal.NetworkSimplex.ThresholdSmallSource

/-! Unit coefficients of the literal two-row branch for one explicit label. -/
namespace NetworkSimplex.Chain.Threshold.OneLabels
open scoped BigOperators
open OneStateCircuits
variable {I : Type*} [DecidableEq I]

private theorem aProduct_sign (D : ReductionData 1 I) (r : ProfileRow 1 I)
    (k : Fin 2) (hn : normalVector (D.rowNormal r) = normal k) (i : I) :
    (k = 0 → 0 ≤ rowCoefficient D r (.aProduct i 0)) ∧
    (k = 1 → rowCoefficient D r (.aProduct i 0) ≤ 0) := by
  have hite (p : Prop) [Decidable p] : (0 : ℤ) ≤ if p then 1 else 0 :=
    ite_nonneg (by norm_num) (by norm_num)
  have hn' := congrFun hn 0
  fin_cases k <;> cases r <;>
    simp_all [ReductionData.rowNormal, normalVector, normal, rowCoefficient, rowExpression,
      residualExpression, totalExpression, AffineExpression.coefficient, observesA]
  all_goals split_ifs at * <;> simp_all [AffineExpression.coefficient]

private theorem bProduct_sign (D : ReductionData 1 I) (r : ProfileRow 1 I)
    (k : Fin 2) (hn : normalVector (D.rowNormal r) = normal k) (i : I) :
    (k = 0 → 0 ≤ rowCoefficient D r (.bProduct i 0)) ∧
    (k = 1 → rowCoefficient D r (.bProduct i 0) ≤ 0) := by
  have hn' := congrFun hn 0
  fin_cases k <;> cases r <;>
    simp_all [ReductionData.rowNormal, normalVector, normal, rowCoefficient, rowExpression,
      residualExpression, totalExpression, AffineExpression.coefficient, observesA]
  all_goals split_ifs at * <;> simp_all [AffineExpression.coefficient]

private theorem bypass_sign (D : ReductionData 1 I) (r : ProfileRow 1 I)
    (k : Fin 2) (hn : normalVector (D.rowNormal r) = normal k) :
    (k = 0 → -1 ≤ rowCoefficient D r .bypassFlow ∧ rowCoefficient D r .bypassFlow ≤ 0) ∧
    (k = 1 → 0 ≤ rowCoefficient D r .bypassFlow ∧ rowCoefficient D r .bypassFlow ≤ 1) := by
  have hn' := congrFun hn 0
  fin_cases k <;> cases r <;>
    simp_all [ReductionData.rowNormal, normalVector, normal, row_bypassFlow_coefficient,
      negativeBypassRow]
  all_goals split_ifs at *

private theorem negative_aFlow_zero (D : ReductionData 1 I) (r : ProfileRow 1 I)
    (hn : normalVector (D.rowNormal r) = normal 1) (i : I) :
    rowCoefficient D r (.aFlow i) = 0 := by
  have hn' := congrFun hn 0
  cases r <;> simp_all [ReductionData.rowNormal, normalVector, normal, row_aFlow_coefficient]
  all_goals split_ifs at hn'

private theorem bypassProduct_sign (D : ReductionData 1 I) (r : ProfileRow 1 I)
    (k : Fin 2) (hn : normalVector (D.rowNormal r) = normal k) :
    (k = 0 → rowCoefficient D r (.bypassProduct 0) ≤ 0) ∧
    (k = 1 → 0 ≤ rowCoefficient D r (.bypassProduct 0)) := by
  have hn' := congrFun hn 0
  fin_cases k <;> cases r <;>
    simp_all [ReductionData.rowNormal, normalVector, normal, rowCoefficient, rowExpression,
      residualExpression, totalExpression, AffineExpression.coefficient]
  all_goals split_ifs at * <;> simp_all

/-- The sole one-label circuit is unit in every original flow and product coordinate. -/
theorem oneBranch_flow_product_unit (D : ReductionData 1 I) (c : Fin 1)
    (r : Fin 2 → ProfileRow 1 I) (hr : OneBranch D c r)
    (z : Coordinate 1 I) (hz : FlowOrProduct z) :
    -1 ≤ ∑ k, weight c k * rowCoefficient D (r k) z ∧
      (∑ k, weight c k * rowCoefficient D (r k) z) ≤ 1 := by
  have h0 := row_flow_product_unit D (r 0) z hz
  have h1 := row_flow_product_unit D (r 1) z hz
  simp only [weight, one_mul, Fin.sum_univ_two]
  cases z with
  | bypassFlow =>
    have h := (bypass_sign D (r 0) 0 (hr 0)).1 rfl
    have h' := (bypass_sign D (r 1) 1 (hr 1)).2 rfl
    omega
  | aFlow i => simp only [negative_aFlow_zero D (r 1) (hr 1) i, add_zero]; exact h0
  | bFlow i => simp
  | aProduct i j =>
    have hj : j = 0 := Subsingleton.elim _ _
    subst j
    have h := (aProduct_sign D (r 0) 0 (hr 0) i).1 rfl
    have h' := (aProduct_sign D (r 1) 1 (hr 1) i).2 rfl
    omega
  | bProduct i j =>
    have hj : j = 0 := Subsingleton.elim _ _
    subst j
    have h := (bProduct_sign D (r 0) 0 (hr 0) i).1 rfl
    have h' := (bProduct_sign D (r 1) 1 (hr 1) i).2 rfl
    omega
  | bypassProduct j =>
    have hj : j = 0 := Subsingleton.elim _ _
    subst j
    have h := (bypassProduct_sign D (r 0) 0 (hr 0)).1 rfl
    have h' := (bypassProduct_sign D (r 1) 1 (hr 1)).2 rfl
    omega
  | weight j => exact False.elim hz

/-- Literal affine sum of the positive and negative source rows. -/
def circuitExpression (D : ReductionData 1 I) (_c : Fin 1) (r : Fin 2 → ProfileRow 1 I) :
    AffineExpression (Coordinate 1 I) := AffineExpression.sum fun k => rowExpression D (r k)

theorem circuitExpression_coefficient (D : ReductionData 1 I) (c : Fin 1)
    (r : Fin 2 → ProfileRow 1 I) (z : Coordinate 1 I) :
    (circuitExpression D c r).coefficient z = ∑ k, weight c k * rowCoefficient D (r k) z := by
  simp [circuitExpression, weight, rowCoefficient]

omit [DecidableEq I] in
theorem circuitExpression_eval (D : ReductionData 1 I) (c : Fin 1)
    (r : Fin 2 → ProfileRow 1 I) (xb : I → ℝ) (hc : ∀ i, D.c i 0 = .neither) :
    (circuitExpression D c r).eval (coordinates D xb) = ∑ k, (weight c k : ℝ) * D.rowRhs (r k) := by
  simp [circuitExpression, weight, rowExpression_eval D xb hc]

theorem circuitExpression_unit (D : ReductionData 1 I) (c : Fin 1)
    (r : Fin 2 → ProfileRow 1 I) (hr : OneBranch D c r)
    (z : Coordinate 1 I) (hz : FlowOrProduct z) :
    -1 ≤ (circuitExpression D c r).coefficient z ∧ (circuitExpression D c r).coefficient z ≤ 1 := by
  rw [circuitExpression_coefficient]
  exact oneBranch_flow_product_unit D c r hr z hz

end NetworkSimplex.Chain.Threshold.OneLabels
