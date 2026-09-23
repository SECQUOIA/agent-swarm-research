import Formal.NetworkSimplex.ThresholdRows

/-! Adding an actual gadget balance equation changes only its three flow coefficients. -/
namespace NetworkSimplex.Chain.Threshold
variable {m : ℕ} {I : Type*} [DecidableEq I]

@[simp] theorem balance_bypass_coefficient (i : I) :
    (balanceExpression (m := m) i).coefficient .bypassFlow = 1 := by
  simp [balanceExpression, AffineExpression.coefficient]

@[simp] theorem balance_aFlow_coefficient (i j : I) :
    (balanceExpression (m := m) i).coefficient (.aFlow j) = if i = j then 1 else 0 := by
  simp [balanceExpression, AffineExpression.coefficient]

@[simp] theorem balance_bFlow_coefficient (i j : I) :
    (balanceExpression (m := m) i).coefficient (.bFlow j) = if i = j then 1 else 0 := by
  simp [balanceExpression, AffineExpression.coefficient]

/-- All product and state-weight coefficients are unchanged by a balance repair. -/
def NonFlow : Coordinate m I → Prop
  | .bypassFlow | .aFlow _ | .bFlow _ => False
  | _ => True

@[simp] theorem balance_nonFlow_coefficient (i : I) (v : Coordinate m I) (hv : NonFlow v) :
    (balanceExpression i).coefficient v = 0 := by
  cases v <;> simp_all [NonFlow, balanceExpression, AffineExpression.coefficient]

/-- Select the sign of the actual balance equation, without changing its coordinates. -/
def balanceRepair (e : AffineExpression (Coordinate m I)) (i : I) (addBalance : Bool) :=
  AffineExpression.add e (if addBalance then balanceExpression i else .neg (balanceExpression i))

omit [DecidableEq I] in
theorem balanceRepair_eval (e : AffineExpression (Coordinate m I)) (i : I) (s : Bool)
    (x : Coordinate m I → ℝ) (h : (balanceExpression i).eval x = 0) :
    (balanceRepair e i s).eval x = e.eval x := by
  cases s <;> simp [balanceRepair, AffineExpression.eval, h]

theorem balanceRepair_nonFlow (e : AffineExpression (Coordinate m I)) (i : I) (s : Bool)
    (v : Coordinate m I) (hv : NonFlow v) :
    (balanceRepair e i s).coefficient v = e.coefficient v := by
  have h := balance_nonFlow_coefficient i v hv
  cases s <;> simp only [balanceRepair, Bool.false_eq_true, ↓reduceIte,
    AffineExpression.coefficient] <;> change _ + _ = _ <;> simp [h]

/-- A negative exceptional bypass coefficient is repaired by adding one actual balance. -/
theorem balanceRepair_add_unit (e : AffineExpression (Coordinate m I)) (i : I)
    (hh : e.coefficient .bypassFlow = -2) (hi : e.coefficient (.aFlow i) = -1)
    (ha : ∀ j, -1 ≤ e.coefficient (.aFlow j) ∧ e.coefficient (.aFlow j) ≤ 1)
    (hb : ∀ j, e.coefficient (.bFlow j) = 0) :
    (balanceRepair e i true).coefficient .bypassFlow = -1 ∧
    (∀ j, -1 ≤ (balanceRepair e i true).coefficient (.aFlow j) ∧
      (balanceRepair e i true).coefficient (.aFlow j) ≤ 1) ∧
    (∀ j, -1 ≤ (balanceRepair e i true).coefficient (.bFlow j) ∧
      (balanceRepair e i true).coefficient (.bFlow j) ≤ 1) := by
  have hc (v : Coordinate m I) : (balanceRepair e i true).coefficient v =
      e.coefficient v + (balanceExpression i).coefficient v := rfl
  simp only [hc, balance_bypass_coefficient, balance_aFlow_coefficient,
    balance_bFlow_coefficient, hh]
  refine ⟨by norm_num, ?_, ?_⟩
  · intro j
    by_cases h : i = j
    · subst j; simp [hi]
    · simpa [h] using ha j
  · intro j
    simp only [hb, zero_add]
    split_ifs <;> omega

/-- A positive exceptional bypass coefficient is repaired by subtracting one actual balance. -/
theorem balanceRepair_sub_unit (e : AffineExpression (Coordinate m I)) (i : I)
    (hh : e.coefficient .bypassFlow = 2) (hi : e.coefficient (.aFlow i) = 1)
    (ha : ∀ j, -1 ≤ e.coefficient (.aFlow j) ∧ e.coefficient (.aFlow j) ≤ 1)
    (hb : ∀ j, e.coefficient (.bFlow j) = 0) :
    (balanceRepair e i false).coefficient .bypassFlow = 1 ∧
    (∀ j, -1 ≤ (balanceRepair e i false).coefficient (.aFlow j) ∧
      (balanceRepair e i false).coefficient (.aFlow j) ≤ 1) ∧
    (∀ j, -1 ≤ (balanceRepair e i false).coefficient (.bFlow j) ∧
      (balanceRepair e i false).coefficient (.bFlow j) ≤ 1) := by
  have hc (v : Coordinate m I) : (balanceRepair e i false).coefficient v =
      e.coefficient v - (balanceExpression i).coefficient v := rfl
  simp only [hc, balance_bypass_coefficient, balance_aFlow_coefficient,
    balance_bFlow_coefficient, hh]
  refine ⟨by norm_num, ?_, ?_⟩
  · intro j
    by_cases h : i = j
    · subst j; simp [hi]
    · simpa [h] using ha j
  · intro j
    simp only [hb, zero_sub]
    split_ifs <;> omega

end NetworkSimplex.Chain.Threshold
