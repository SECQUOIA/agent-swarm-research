import Mathlib.Analysis.Convex.Function
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic

/-! Domain-sensitive examples. Definedness is separate from Lean's totalized operations. -/

namespace CertifiedMinlp

def quotientDefined (_numerator denominator : ℝ) : Prop := denominator ≠ 0

theorem cancel_self_on_quotient_domain (x : ℝ) (hx : quotientDefined x x) :
    x / x = 1 := div_self hx

theorem cancellation_does_not_extend_domain :
    ¬ quotientDefined 0 0 ∧ (0 : ℝ) / 0 ≠ 1 := by
  norm_num [quotientDefined]

theorem quotient_not_defined_on_zero_box {B : Set ℝ} (hzero : 0 ∈ B) :
    ¬ ∀ x ∈ B, quotientDefined x x := by
  intro h
  exact (h 0 hzero) rfl

theorem sqrt_square_exact (x : ℝ) : Real.sqrt (x ^ 2) = |x| :=
  Real.sqrt_sq_eq_abs x

theorem sqrt_square_eq_self_iff (x : ℝ) : Real.sqrt (x ^ 2) = x ↔ 0 ≤ x := by
  rw [sqrt_square_exact, abs_eq_self]

theorem sqrt_square_negative_counterexample : Real.sqrt ((-1 : ℝ) ^ 2) ≠ -1 := by
  norm_num

def nonnegativeQuadrant : Set (ℝ × ℝ) := {p | 0 ≤ p.1 ∧ 0 ≤ p.2}

theorem product_nonnegative_on_quadrant {p : ℝ × ℝ} (hp : p ∈ nonnegativeQuadrant) :
    0 ≤ p.1 * p.2 := mul_nonneg hp.1 hp.2

theorem bilinear_not_concave_on_nonnegativeQuadrant :
    ¬ ConcaveOn ℝ nonnegativeQuadrant (fun p : ℝ × ℝ => p.1 * p.2) := by
  intro h
  have hh := h.2 (show (0, 0) ∈ nonnegativeQuadrant by norm_num [nonnegativeQuadrant])
    (show (1, 1) ∈ nonnegativeQuadrant by norm_num [nonnegativeQuadrant])
    (show (0 : ℝ) ≤ 1 / 2 by norm_num) (show (0 : ℝ) ≤ 1 / 2 by norm_num)
    (show (1 / 2 : ℝ) + 1 / 2 = 1 by norm_num)
  norm_num at hh

end CertifiedMinlp
