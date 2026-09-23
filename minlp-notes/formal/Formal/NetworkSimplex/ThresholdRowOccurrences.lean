import Formal.NetworkSimplex.ThresholdRows

/-! The signs of actual original-coordinate occurrences, before selecting circuit rows. -/
namespace NetworkSimplex.Chain.Threshold
variable {m : ℕ} {I : Type*} [DecidableEq I]

@[simp] theorem row_bFlow_coefficient (D : ReductionData m I) (r : ProfileRow m I) (i : I) :
    rowCoefficient D r (.bFlow i) = 0 := by
  cases r <;> simp [rowCoefficient, rowExpression, AffineExpression.coefficient,
    totalExpression]

theorem row_aFlow_coefficient (D : ReductionData m I) (r : ProfileRow m I) (i : I) :
    rowCoefficient D r (.aFlow i) =
      (if r = .endpointB i then 1 else 0) - (if r = .endpointA i then 1 else 0) := by
  cases r <;> simp [rowCoefficient, rowExpression, AffineExpression.coefficient,
    totalExpression]

def negativeBypassRow : ProfileRow m I → Bool
  | .totalUpper | .endpointA _ => true
  | _ => false

theorem row_bypassFlow_coefficient (D : ReductionData m I) (r : ProfileRow m I) :
    rowCoefficient D r .bypassFlow =
      (if r = .totalLower then 1 else 0) -
      (if negativeBypassRow r then 1 else 0) := by
  cases r <;> simp [rowCoefficient, rowExpression, AffineExpression.coefficient,
    totalExpression, negativeBypassRow]

theorem row_aProduct_bounds (D : ReductionData m I) (r : ProfileRow m I) (i : I) (j : Fin m) :
    -1 ≤ rowCoefficient D r (.aProduct i j) ∧ rowCoefficient D r (.aProduct i j) ≤ 1 := by
  cases r <;> simp [rowCoefficient, rowExpression, AffineExpression.coefficient,
    totalExpression] <;> split_ifs <;> norm_num

theorem row_bProduct_bounds (D : ReductionData m I) (r : ProfileRow m I) (i : I) (j : Fin m) :
    -1 ≤ rowCoefficient D r (.bProduct i j) ∧ rowCoefficient D r (.bProduct i j) ≤ 1 := by
  cases r <;> simp [rowCoefficient, rowExpression, AffineExpression.coefficient,
    totalExpression] <;> split_ifs <;> norm_num

theorem row_bypassProduct_bounds (D : ReductionData m I) (r : ProfileRow m I) (j : Fin m) :
    -1 ≤ rowCoefficient D r (.bypassProduct j) ∧ rowCoefficient D r (.bypassProduct j) ≤ 1 := by
  cases r <;> simp [rowCoefficient, rowExpression, AffineExpression.coefficient,
    totalExpression] <;> split_ifs <;> norm_num

theorem row_aProduct_positive (D : ReductionData m I) (r : ProfileRow m I) (i : I) (j : Fin m)
    (h : 0 < rowCoefficient D r (.aProduct i j)) :
    (r = .bothUpper i j ∧ D.c i j.succ = .both) ∨
      (r = .endpointA i ∧ observesA (D.c i j.succ)) := by
  cases r <;> simp_all [rowCoefficient, rowExpression, AffineExpression.coefficient,
    totalExpression] <;> (try split_ifs at h) <;> simp_all
  all_goals aesop

theorem row_aProduct_negative (D : ReductionData m I) (r : ProfileRow m I) (i : I) (j : Fin m)
    (h : rowCoefficient D r (.aProduct i j) < 0) :
    (r = .aLower i j ∧ D.c i j.succ = .aOnly) ∨
      (r = .bothLower i j ∧ D.c i j.succ = .both) ∨
      (r = .endpointB i ∧ observesA (D.c i j.succ)) := by
  cases r <;> simp_all [rowCoefficient, rowExpression, AffineExpression.coefficient,
    totalExpression] <;> (try split_ifs at h) <;> simp_all
  all_goals aesop

theorem row_bProduct_positive (D : ReductionData m I) (r : ProfileRow m I) (i : I) (j : Fin m)
    (h : 0 < rowCoefficient D r (.bProduct i j)) :
    (r = .bothUpper i j ∧ D.c i j.succ = .both) ∨
      (r = .endpointB i ∧ D.c i j.succ = .bOnly) := by
  cases r <;> simp_all [rowCoefficient, rowExpression, AffineExpression.coefficient,
    totalExpression] <;> (try split_ifs at h) <;> simp_all
  all_goals aesop

theorem row_bProduct_negative (D : ReductionData m I) (r : ProfileRow m I) (i : I) (j : Fin m)
    (h : rowCoefficient D r (.bProduct i j) < 0) :
    (r = .bLower i j ∧ D.c i j.succ = .bOnly) ∨
      (r = .bothLower i j ∧ D.c i j.succ = .both) ∨
      (r = .endpointA i ∧ D.c i j.succ = .bOnly) := by
  cases r <;> simp_all [rowCoefficient, rowExpression, AffineExpression.coefficient,
    totalExpression] <;> (try split_ifs at h) <;> simp_all
  all_goals aesop

theorem row_bypassProduct_positive (D : ReductionData m I) (r : ProfileRow m I) (j : Fin m)
    (h : 0 < rowCoefficient D r (.bypassProduct j)) : r = .bypassLower j := by
  cases r <;> simp_all [rowCoefficient, rowExpression, AffineExpression.coefficient,
    totalExpression] <;> (try split_ifs at h) <;> simp_all

theorem row_bypassProduct_negative (D : ReductionData m I) (r : ProfileRow m I) (j : Fin m)
    (h : rowCoefficient D r (.bypassProduct j) < 0) : r = .bypassUpper j := by
  cases r <;> simp_all [rowCoefficient, rowExpression, AffineExpression.coefficient,
    totalExpression] <;> (try split_ifs at h) <;> simp_all

/-- Weights are allowed general coefficients; the threshold concerns flows and products. -/
def FlowOrProduct : Coordinate m I → Prop
  | .weight _ => False
  | _ => True

theorem row_flow_product_unit (D : ReductionData m I) (r : ProfileRow m I)
    (z : Coordinate m I) (hz : FlowOrProduct z) :
    -1 ≤ rowCoefficient D r z ∧ rowCoefficient D r z ≤ 1 := by
  cases z with
  | bypassFlow =>
    rw [row_bypassFlow_coefficient]
    cases r <;> simp [negativeBypassRow]
  | aFlow i =>
    rw [row_aFlow_coefficient]
    cases r <;> simp <;> split_ifs <;> norm_num
  | bFlow i => simp
  | aProduct i j => exact row_aProduct_bounds D r i j
  | bProduct i j => exact row_bProduct_bounds D r i j
  | bypassProduct j => exact row_bypassProduct_bounds D r j
  | weight j => exact False.elim hz

end NetworkSimplex.Chain.Threshold
