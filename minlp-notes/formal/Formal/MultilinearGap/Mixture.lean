import Formal.CubicGap.Expectation

/-! A common mixture of three rounding laws transfers their termwise guarantees. -/

namespace MultilinearGap

open CubicGap

noncomputable section

variable {Ω : Type*} [Fintype Ω]

/-- Mix three finite laws with positive, unnormalized masses. -/
def threeMix (μ₁ μ₂ μ₃ : Law Ω) (r₁ r₂ r₃ : ℝ)
    (h₁ : 0 < r₁) (h₂ : 0 < r₂) (h₃ : 0 < r₃) : Law Ω where
  weight w := (r₁ * μ₁.weight w + r₂ * μ₂.weight w + r₃ * μ₃.weight w) /
    (r₁ + r₂ + r₃)
  nonneg w := div_nonneg (by positivity [μ₁.nonneg w, μ₂.nonneg w, μ₃.nonneg w])
    (by positivity)
  mass_one := by
    simp only [← Finset.sum_div, Finset.sum_add_distrib, ← Finset.mul_sum,
      Law.mass_one, mul_one]
    exact div_self (by positivity)

theorem threeMix_expect (μ₁ μ₂ μ₃ : Law Ω) (r₁ r₂ r₃ : ℝ)
    (h₁ : 0 < r₁) (h₂ : 0 < r₂) (h₃ : 0 < r₃) (f : Ω → ℝ) :
    (threeMix μ₁ μ₂ μ₃ r₁ r₂ r₃ h₁ h₂ h₃).expect f =
      (r₁ * μ₁.expect f + r₂ * μ₂.expect f + r₃ * μ₃.expect f) /
        (r₁ + r₂ + r₃) := by
  simp only [Law.expect, threeMix, div_mul_eq_mul_div, add_mul,
    ← Finset.sum_div, Finset.sum_add_distrib, mul_assoc, Finset.mul_sum]

/-- Mixing preserves any common expected observable, including all coordinate
means of the three rounding laws. -/
theorem threeMix_expect_common (μ₁ μ₂ μ₃ : Law Ω) (r₁ r₂ r₃ : ℝ)
    (h₁ : 0 < r₁) (h₂ : 0 < r₂) (h₃ : 0 < r₃) (f : Ω → ℝ) (x : ℝ)
    (hx₁ : μ₁.expect f = x) (hx₂ : μ₂.expect f = x) (hx₃ : μ₃.expect f = x) :
    (threeMix μ₁ μ₂ μ₃ r₁ r₂ r₃ h₁ h₂ h₃).expect f = x := by
  rw [threeMix_expect, hx₁, hx₂, hx₃]
  apply (div_eq_iff (by positivity : r₁ + r₂ + r₃ ≠ 0)).mpr
  ring

theorem threeMix_deficiency (μ₁ μ₂ μ₃ : Law Ω) (r₁ r₂ r₃ : ℝ)
    (h₁ : 0 < r₁) (h₂ : 0 < r₂) (h₃ : 0 < r₃) (f : Ω → ℝ) (u : ℝ) :
    u - (threeMix μ₁ μ₂ μ₃ r₁ r₂ r₃ h₁ h₂ h₃).expect f =
      (r₁ * (u - μ₁.expect f) + r₂ * (u - μ₂.expect f) +
        r₃ * (u - μ₃.expect f)) / (r₁ + r₂ + r₃) := by
  rw [threeMix_expect]
  field_simp
  ring

/-- A term can use any one of the three component estimates. Nonnegative
deficiencies from the other components preserve its guarantee. -/
theorem threeMix_deficiency_ge (μ₁ μ₂ μ₃ : Law Ω) (r₁ r₂ r₃ : ℝ)
    (h₁ : 0 < r₁) (h₂ : 0 < r₂) (h₃ : 0 < r₃) (f : Ω → ℝ) (u T : ℝ)
    (hn₁ : 0 ≤ u - μ₁.expect f) (hn₂ : 0 ≤ u - μ₂.expect f)
    (hn₃ : 0 ≤ u - μ₃.expect f)
    (hgood : T ≤ r₁ * (u - μ₁.expect f) ∨
      T ≤ r₂ * (u - μ₂.expect f) ∨ T ≤ r₃ * (u - μ₃.expect f)) :
    T / (r₁ + r₂ + r₃) ≤
      u - (threeMix μ₁ μ₂ μ₃ r₁ r₂ r₃ h₁ h₂ h₃).expect f := by
  rw [threeMix_deficiency]
  apply div_le_div_of_nonneg_right _ (by positivity)
  have hp₁ := mul_nonneg h₁.le hn₁
  have hp₂ := mul_nonneg h₂.le hn₂
  have hp₃ := mul_nonneg h₃.le hn₃
  rcases hgood with h | h | h <;> linarith

end
end MultilinearGap
