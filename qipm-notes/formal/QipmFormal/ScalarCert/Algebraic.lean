import QipmFormal.ScalarCert.Inverse

/-!
# Rational two-sided bounds for `A` and `P`

`A v = √(2-v²)/(1-v²)` is algebraic: rational bounds follow from rational
squaring, which is exactly how `appendix-scalar-certificate.tex` certifies
`A(v₀)` and `A(w₀)`.
-/

namespace QipmFormal.ScalarCert

open Real

/-- Rational lower bound for `A` by squaring. -/
theorem le_A {v q : ℝ} (hv : |v| < 1) (hq : 0 ≤ q) (h : q ^ 2 ≤ 2 - v ^ 2) :
    q / (1 - v ^ 2) ≤ A v := by
  have h1 : (0:ℝ) < 1 - v ^ 2 := one_sub_sq_pos hv
  have h2 : (0:ℝ) ≤ 2 - v ^ 2 := by nlinarith
  have hle : q ≤ √(2 - v ^ 2) := (Real.le_sqrt hq h2).mpr h
  rw [A]
  gcongr

/-- Rational upper bound for `A` by squaring. -/
theorem A_le {v r : ℝ} (hv : |v| < 1) (hr : 0 ≤ r) (h : 2 - v ^ 2 ≤ r ^ 2) :
    A v ≤ r / (1 - v ^ 2) := by
  have h1 : (0:ℝ) < 1 - v ^ 2 := one_sub_sq_pos hv
  have hle : √(2 - v ^ 2) ≤ r := (Real.sqrt_le_left hr).mpr h
  rw [A]
  gcongr

/-- Rational upper bound for `P v = v * A v`. -/
theorem P_le {v r : ℝ} (hv : |v| < 1) (hv0 : 0 ≤ v) (hr : 0 ≤ r)
    (h : 2 - v ^ 2 ≤ r ^ 2) : P v ≤ v * (r / (1 - v ^ 2)) :=
  mul_le_mul_of_nonneg_left (A_le hv hr h) hv0

end QipmFormal.ScalarCert
