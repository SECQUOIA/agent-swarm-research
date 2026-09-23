import Formal.QuadraticAggregation.Model

open scoped BigOperators Matrix

namespace QuadraticAggregation
namespace System

variable {n m : ℕ}

/-- Strict feasibility bounds the constant term of every nonzero nonnegative
aggregation. Removing that term from a sweeping inequality leaves a bound
that is homogeneous in the nonconstant coefficients. -/
theorem sweep_constant_elimination (D : System n m)
    {x₀ : Vec n} (hx₀ : x₀ ∈ D.feasible)
    {w : Vec m} (hw : ∀ i, 0 ≤ w i) (hwne : w ≠ 0)
    (α : Vec n) (r : ℝ)
    (hsweep : ∀ x, 0 ≤ q (D.aggA w) x +
      2 * (r * (α ⬝ᵥ x)) * (D.aggB w ⬝ᵥ x) + D.aggC w * (r * (α ⬝ᵥ x)) ^ 2) :
    ∀ x, 0 ≤ q (D.aggA w) x + 2 * (r * (α ⬝ᵥ x)) * (D.aggB w ⬝ᵥ x) -
      (r * (α ⬝ᵥ x)) ^ 2 * (q (D.aggA w) x₀ + 2 * (D.aggB w ⬝ᵥ x₀)) := by
  have hfeas := D.agg_eval_neg hw hwne hx₀
  rw [D.agg_eval] at hfeas
  intro x
  have hbound : D.aggC w ≤ -(q (D.aggA w) x₀ + 2 * (D.aggB w ⬝ᵥ x₀)) := by
    linarith
  have hmul := mul_le_mul_of_nonneg_right hbound (sq_nonneg (r * (α ⬝ᵥ x)))
  have hs := hsweep x
  nlinarith

/-- A sweeping certificate has nonzero nonconstant coefficients: otherwise its
strictly negative constant term violates the inequality in the normal direction. -/
theorem sweep_pair_ne_zero (D : System n m)
    {x₀ : Vec n} (hx₀ : x₀ ∈ D.feasible)
    {w : Vec m} (hw : ∀ i, 0 ≤ w i) (hwne : w ≠ 0)
    {α : Vec n} (hα : α ≠ 0) {r : ℝ} (hr : r ≠ 0)
    (hsweep : ∀ x, 0 ≤ q (D.aggA w) x +
      2 * (r * (α ⬝ᵥ x)) * (D.aggB w ⬝ᵥ x) + D.aggC w * (r * (α ⬝ᵥ x)) ^ 2) :
    (D.aggA w, D.aggB w) ≠ (0 : Mat n × Vec n) := by
  intro hp
  have hA : D.aggA w = 0 := congrArg Prod.fst hp
  have hB : D.aggB w = 0 := congrArg Prod.snd hp
  have hc : D.aggC w < 0 := D.trivial_aggC_neg hw hwne hA hB ⟨x₀, hx₀⟩
  have hs := hsweep α
  rw [hA, hB] at hs
  simp only [q, Matrix.zero_mulVec, dotProduct_zero, zero_dotProduct, mul_zero, zero_add] at hs
  have hdot : α ⬝ᵥ α ≠ 0 := by
    intro h
    exact hα ((dotProduct_self_eq_zero).mp h)
  have hsq : 0 < (r * (α ⬝ᵥ α)) ^ 2 := sq_pos_of_ne_zero (mul_ne_zero hr hdot)
  exact (not_lt_of_ge hs) (mul_neg_of_neg_of_pos hc hsq)

end System
end QuadraticAggregation
