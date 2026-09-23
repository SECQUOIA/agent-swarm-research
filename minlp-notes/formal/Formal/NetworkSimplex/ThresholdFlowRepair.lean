import Formal.NetworkSimplex.ThresholdFlowRows

/-! Actual affine expressions for circuit sums and their flow-balance repairs. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open ThreeStateCircuits
variable {I : Type*} [DecidableEq I]

/-- Weighted source expressions, using the only three weights in the circuit table. -/
def circuitExpression (D : ReductionData 3 I) (c : Fin 16)
    (r : Fin 11 → ProfileRow 3 I) : AffineExpression (Coordinate 3 I) :=
  AffineExpression.sum fun k =>
    if weight c k = 0 then .constant 0
    else if weight c k = 1 then rowExpression D (r k)
    else .add (rowExpression D (r k)) (rowExpression D (r k))

def circuitCoefficient (D : ReductionData 3 I) (c : Fin 16)
    (r : Fin 11 → ProfileRow 3 I) (v : Coordinate 3 I) : ℤ :=
  ∑ k, weight c k * rowCoefficient D (r k) v

omit [DecidableEq I] in
theorem weight_zero_one_two : ∀ (c : Fin 16) (k : Fin 11),
    weight c k = 0 ∨ weight c k = 1 ∨ weight c k = 2 := by decide +kernel

theorem circuitExpression_coefficient (D : ReductionData 3 I) (c : Fin 16)
    (r : Fin 11 → ProfileRow 3 I) (v : Coordinate 3 I) :
    (circuitExpression D c r).coefficient v = circuitCoefficient D c r v := by
  rw [circuitExpression, AffineExpression.coefficient_sum]
  apply Finset.sum_congr rfl
  intro k _
  rcases weight_zero_one_two c k with h | h | h <;>
    simp [h, AffineExpression.coefficient, rowCoefficient]
  ring

omit [DecidableEq I] in
theorem circuitExpression_eval (D : ReductionData 3 I) (c : Fin 16)
    (r : Fin 11 → ProfileRow 3 I) (x : Coordinate 3 I → ℝ) :
    (circuitExpression D c r).eval x = ∑ k, (weight c k : ℝ) * (rowExpression D (r k)).eval x := by
  rw [circuitExpression, AffineExpression.eval_sum]
  apply Finset.sum_congr rfl
  intro k _
  rcases weight_zero_one_two c k with h | h | h <;> simp [h, AffineExpression.eval]
  ring

omit [DecidableEq I] in
/-- The symbolic circuit sum evaluates to the actual reduced certificate. -/
theorem circuitExpression_eval_rhs (D : ReductionData 3 I) (c : Fin 16)
    (r : Fin 11 → ProfileRow 3 I) (xb : I → ℝ) (hc : ∀ i, D.c i 0 = .neither) :
    (circuitExpression D c r).eval (coordinates D xb) = ∑ k, (weight c k : ℝ) * D.rowRhs (r k) := by
  simp only [circuitExpression_eval, rowExpression_eval D xb hc]

@[simp] theorem circuit_bFlow (D : ReductionData 3 I) (c : Fin 16)
    (r : Fin 11 → ProfileRow 3 I) (i : I) : circuitCoefficient D c r (.bFlow i) = 0 := by
  simp [circuitCoefficient]

/-- A source row other than the negative full row occurs with total weight at most one. -/
theorem ThreeBranch.row_weight_bound (D : ReductionData 3 I) {c : Fin 16}
    {r : Fin 11 → ProfileRow 3 I} (h : ThreeBranch D c r) (s : ProfileRow 3 I)
    (hs : s ≠ .totalLower) :
    0 ≤ (∑ k, weight c k * (if r k = s then 1 else 0)) ∧
      (∑ k, weight c k * (if r k = s then 1 else 0)) ≤ 1 := by
  have hnon : ∀ k, 0 ≤ weight c k * (if r k = s then 1 else 0) := by
    intro k; split_ifs <;> simp [weight_nonnegative]
  refine ⟨Finset.sum_nonneg (fun k _ => hnon k), ?_⟩
  by_cases hex : ∃ k, weight c k ≠ 0 ∧ r k = s
  · obtain ⟨k, hk, hrk⟩ := hex
    have hsum : (∑ j, weight c j * (if r j = s then 1 else 0)) = weight c k := by
      rw [Finset.sum_eq_single k]
      · simp [hrk]
      · intro j _ hj
        by_cases h0 : weight c j = 0
        · simp [h0]
        · have hrj : r j ≠ s := by
            intro he
            exact hj (h.row_injective D h0 hk (he.trans hrk.symm))
          simp [hrj]
      · simp
    rw [hsum]
    apply weight_le_one_except_full c k
    intro hk10
    subst k
    have hh := row_negative_full D (r 10) (h 10 hk)
    exact hs (hrk.symm.trans hh)
  · have hz : ∀ k, weight c k * (if r k = s then 1 else 0) = 0 := by
      intro k
      by_cases hk : weight c k = 0
      · simp [hk]
      · have hr : r k ≠ s := fun h => hex ⟨k, hk, h⟩
        simp [hr]
    simp [hz]

/-- Opposite endpoint occurrences give unit coefficients on every direct gadget flow. -/
theorem circuit_aFlow_unit (D : ReductionData 3 I) {c : Fin 16}
    {r : Fin 11 → ProfileRow 3 I} (h : ThreeBranch D c r) (i : I) :
    -1 ≤ circuitCoefficient D c r (.aFlow i) ∧ circuitCoefficient D c r (.aFlow i) ≤ 1 := by
  have ha := h.row_weight_bound D (.endpointA i) (by simp)
  have hb := h.row_weight_bound D (.endpointB i) (by simp)
  simp only [circuitCoefficient, row_aFlow_coefficient, mul_sub, Finset.sum_sub_distrib]
  omega

/-- A canonical bypass vector ignores arbitrary choices for absent normals. -/
def bypassVector (r : Fin 11 → ProfileRow 3 I) (k : Fin 11) : ℤ :=
  if k.val < 7 then (if negativeBypassRow (r k) then -1 else 0)
  else if k = 10 then 1 else 0

theorem circuit_bypass_eq (D : ReductionData 3 I) {c : Fin 16}
    {r : Fin 11 → ProfileRow 3 I} (h : ThreeBranch D c r) :
    circuitCoefficient D c r .bypassFlow = ∑ k, weight c k * bypassVector r k := by
  apply Finset.sum_congr rfl
  intro k _
  by_cases hk : weight c k = 0
  · simp [hk]
  · congr 1
    by_cases hpos : k.val < 7
    · have he : positiveIndex ⟨k.val, hpos⟩ = k := rfl
      have hn := positive_row_not_totalLower D (r k) ⟨k.val, hpos⟩ (by simpa only [he] using h k hk)
      simp [bypassVector, hpos, row_bypassFlow_coefficient, hn, apply_ite]
    · by_cases hf : k = 10
      · subst k
        have hr := row_negative_full D (r 10) (h 10 hk)
        simp [hr, bypassVector, row_bypassFlow_coefficient, negativeBypassRow]
      · have hlt : k.val - 7 < 3 := by omega
        have he : negativeSingletonIndex ⟨k.val - 7, hlt⟩ = k := by
          ext; dsimp [negativeSingletonIndex]; omega
        have hz := negative_singleton_bypass_zero D (r k) ⟨k.val - 7, hlt⟩
          (by simpa only [he] using h k hk)
        simp [bypassVector, hpos, hf, hz]

omit [DecidableEq I] in
/-- The only possible nonunit bypass coefficients have the two claimed circuit forms. -/
theorem bypass_cases (r : Fin 11 → ProfileRow 3 I) (c : Fin 16) :
    (-1 ≤ ∑ k, weight c k * bypassVector r k ∧ ∑ k, weight c k * bypassVector r k ≤ 1) ∨
    (c = 11 ∧ (∑ k, weight c k * bypassVector r k) = -2 ∧
      bypassVector r 0 = -1 ∧ bypassVector r 1 = -1 ∧ bypassVector r 2 = -1) ∨
    (c = 15 ∧ (∑ k, weight c k * bypassVector r k) = 2 ∧
      bypassVector r 3 = 0 ∧ bypassVector r 4 = 0 ∧ bypassVector r 5 = 0) := by
  have hb (k : Fin 7) : -1 ≤ bypassVector r (positiveIndex k) ∧
      bypassVector r (positiveIndex k) ≤ 0 := by
    simp only [bypassVector, positiveIndex, k.isLt, ↓reduceIte]
    split_ifs <;> omega
  have h7 : bypassVector r 7 = 0 := by simp [bypassVector]
  have h8 : bypassVector r 8 = 0 := by simp [bypassVector]
  have h9 : bypassVector r 9 = 0 := by simp [bypassVector]
  have h10 : bypassVector r 10 = 1 := by simp [bypassVector]
  have h0 : -1 ≤ bypassVector r 0 ∧ bypassVector r 0 ≤ 0 := hb 0
  have h1 : -1 ≤ bypassVector r 1 ∧ bypassVector r 1 ≤ 0 := hb 1
  have h2 : -1 ≤ bypassVector r 2 ∧ bypassVector r 2 ≤ 0 := hb 2
  have h3 : -1 ≤ bypassVector r 3 ∧ bypassVector r 3 ≤ 0 := hb 3
  have h4 : -1 ≤ bypassVector r 4 ∧ bypassVector r 4 ≤ 0 := hb 4
  have h5 : -1 ≤ bypassVector r 5 ∧ bypassVector r 5 ≤ 0 := hb 5
  have h6 : -1 ≤ bypassVector r 6 ∧ bypassVector r 6 ≤ 0 := hb 6
  fin_cases c <;> simp [weight, Fin.sum_univ_succ] at h7 h8 h9 h10 ⊢ <;> omega

end NetworkSimplex.Chain.Threshold
