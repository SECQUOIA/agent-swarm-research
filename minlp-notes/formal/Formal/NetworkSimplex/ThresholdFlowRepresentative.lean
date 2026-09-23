import Formal.NetworkSimplex.ThresholdFlowWitness
import Formal.NetworkSimplex.ThresholdBalanceRepair

/-! Every three-label circuit has a representative with unit flow coefficients. -/
namespace NetworkSimplex.Chain.Threshold
open ThreeStateCircuits
variable {I : Type*} [DecidableEq I]

/-- Unit bounds for the three kinds of flow coordinate. -/
def UnitFlow (e : AffineExpression (Coordinate 3 I)) : Prop :=
  (-1 ≤ e.coefficient .bypassFlow ∧ e.coefficient .bypassFlow ≤ 1) ∧
  (∀ i, -1 ≤ e.coefficient (.aFlow i) ∧ e.coefficient (.aFlow i) ≤ 1) ∧
  (∀ i, -1 ≤ e.coefficient (.bFlow i) ∧ e.coefficient (.bFlow i) ≤ 1)

/-- At most one actual gadget balance suffices. The repair leaves every product and state-weight
coefficient unchanged, and preserves the expression on the entire balance domain. -/
theorem exists_unit_flow_representative (D : ReductionData 3 I) {c : Fin 16}
    {r : Fin 11 → ProfileRow 3 I} (hr : ThreeBranch D c r) :
    ∃ e : AffineExpression (Coordinate 3 I),
      (e = circuitExpression D c r ∨
        ∃ i s, e = balanceRepair (circuitExpression D c r) i s) ∧
      (∀ x, (∀ i, (balanceExpression i).eval x = 0) →
        e.eval x = (circuitExpression D c r).eval x) ∧
      UnitFlow e ∧
      (∀ v, NonFlow v → e.coefficient v = circuitCoefficient D c r v) := by
  let e := circuitExpression D c r
  have ha (i : I) : -1 ≤ e.coefficient (.aFlow i) ∧ e.coefficient (.aFlow i) ≤ 1 := by
    simpa only [e, circuitExpression_coefficient] using circuit_aFlow_unit D hr i
  have hb (i : I) : e.coefficient (.bFlow i) = 0 := by
    simp only [e, circuitExpression_coefficient, circuit_bFlow]
  have hcoef (v : Coordinate 3 I) : e.coefficient v = circuitCoefficient D c r v :=
    circuitExpression_coefficient D c r v
  rcases bypass_cases r c with hu | ⟨_, hn, _⟩ | ⟨_, hp, _⟩
  · have hh : -1 ≤ e.coefficient .bypassFlow ∧ e.coefficient .bypassFlow ≤ 1 := by
      rw [hcoef, circuit_bypass_eq D hr]
      exact hu
    exact ⟨e, Or.inl rfl, fun _ _ => rfl, ⟨hh, ha, fun i => by simp [hb i]⟩,
      fun v _ => hcoef v⟩
  · have hn' : circuitCoefficient D c r .bypassFlow = -2 := by
      rw [circuit_bypass_eq D hr]; exact hn
    obtain ⟨i, _, hi⟩ := negative_bypass_witness D hr hn'
    have hh : e.coefficient .bypassFlow = -2 := (hcoef _).trans hn'
    have hi' : e.coefficient (.aFlow i) = -1 := (hcoef _).trans hi
    obtain ⟨hh', ha', hb'⟩ := balanceRepair_add_unit e i hh hi' ha hb
    refine ⟨balanceRepair e i true, Or.inr ⟨i, true, rfl⟩,
      fun x hx => balanceRepair_eval e i true x (hx i), ?_, ?_⟩
    · exact ⟨by simp [hh'], ha', hb'⟩
    · intro v hv
      exact (balanceRepair_nonFlow e i true v hv).trans (hcoef v)
  · have hp' : circuitCoefficient D c r .bypassFlow = 2 := by
      rw [circuit_bypass_eq D hr]; exact hp
    obtain ⟨i, _, hi⟩ := positive_bypass_witness D hr hp'
    have hh : e.coefficient .bypassFlow = 2 := (hcoef _).trans hp'
    have hi' : e.coefficient (.aFlow i) = 1 := (hcoef _).trans hi
    obtain ⟨hh', ha', hb'⟩ := balanceRepair_sub_unit e i hh hi' ha hb
    refine ⟨balanceRepair e i false, Or.inr ⟨i, false, rfl⟩,
      fun x hx => balanceRepair_eval e i false x (hx i), ?_, ?_⟩
    · exact ⟨by simp [hh'], ha', hb'⟩
    · intro v hv
      exact (balanceRepair_nonFlow e i false v hv).trans (hcoef v)

end NetworkSimplex.Chain.Threshold
