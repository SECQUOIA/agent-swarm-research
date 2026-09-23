import Formal.NetworkSimplex.ThresholdRows

/-! Represent an unreduced profile by adding a dummy unobserved state of weight zero. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
noncomputable section
variable {m : ℕ} {I : Type*}

/-- Every original state is retained as an explicit state. The new state zero
has no observations and zero weight, so eliminating it loses no profile coordinate. -/
def unreducedData (D : ReductionData m I) : ReductionData (m + 1) I where
  c i := Fin.cons .neither (D.c i)
  u i := Fin.cons 0 (D.u i)
  v i := Fin.cons 0 (D.v i)
  weights := Fin.cons 0 D.weights
  xa := D.xa
  xh := D.xh
  observedH := Fin.cons false D.observedH
  zh := Fin.cons 0 D.zh

@[simp] theorem unreducedData_total (D : ReductionData m I) :
    (unreducedData D).total = D.total := rfl

theorem unreducedData_full_cons_iff (D : ReductionData m I) (w : Fin (m + 1) → ℝ) :
    (unreducedData D).FullProfile (Fin.cons 0 w) ↔ D.FullProfile w := by
  simp [ReductionData.FullProfile, Profile, unreducedData, Fin.forall_fin_succ,
    GadgetProfile, residual, bSum, freeA, Fin.sum_univ_succ, observesA]

/-- The lifted reduced rows describe the original full profile, including
observations on its state zero. No assumption that any original state is unobserved is used. -/
theorem unreducedData_reduced_iff (D : ReductionData m I) (w : Fin (m + 1) → ℝ) :
    (unreducedData D).ReducedProfile w ↔ D.FullProfile w := by
  have he := (unreducedData D).fullProfile_restore_iff w (fun _ => rfl) rfl
  constructor
  · intro h
    have hsum : ∑ j, w j = D.total := by
      have hu := h.2.1
      have hl := h.2.2.1
      change (∑ j, w j) ≤ D.total at hu
      change -(∑ j, w j) ≤ 0 - D.total at hl
      linarith
    apply (unreducedData_full_cons_iff D w).mp
    simpa only [unreducedData_total, restoreProfile, hsum, sub_self] using he.mpr h
  · intro h
    have hsum : ∑ j, w j = D.total := h.2.1
    apply he.mp
    simpa only [unreducedData_total, restoreProfile, hsum, sub_self] using
      (unreducedData_full_cons_iff D w).mpr h

/-- Existing symbolic row evaluation applies to the dummy-state construction. -/
theorem unreducedData_rowExpression_eval (D : ReductionData m I) (xb : I → ℝ)
    (r : ProfileRow (m + 1) I) :
    (rowExpression (unreducedData D) r).eval (coordinates (unreducedData D) xb) =
      (unreducedData D).rowRhs r :=
  rowExpression_eval (unreducedData D) xb (fun _ => rfl) r

end
end NetworkSimplex.Chain.Threshold
