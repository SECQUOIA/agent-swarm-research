import Mathlib

/-! The original reciprocal graph and the proposed one-leaf conic hull. -/

namespace ReciprocalAnchor

abbrev Point := Fin 4 → ℝ

def point (m t q w : ℝ) : Point := ![m, t, q, w]

def graph (a b : ℝ) : Set Point :=
  {z | ∃ x y : ℝ, a ≤ x ∧ x ≤ b ∧ 0 ≤ y ∧ y ≤ 1 ∧
    z = point x (1 / x) y (x * y)}

def hull (a b : ℝ) : Set Point := convexHull ℝ (graph a b)

def LinearBounds (a b m t q w : ℝ) : Prop :=
  0 ≤ q ∧ q ≤ 1 ∧ a * q ≤ w ∧ w ≤ b * q ∧
    a * (1 - q) ≤ m - w ∧ m - w ≤ b * (1 - q) ∧
    t ≤ (a + b - m) / (a * b)

def SOCBounds (m t q w : ℝ) : Prop :=
  ∃ tau₁ tau₀ : ℝ, 0 ≤ tau₁ ∧ 0 ≤ tau₀ ∧ q ^ 2 ≤ w * tau₁ ∧
    (1 - q) ^ 2 ≤ (m - w) * tau₀ ∧ tau₁ + tau₀ ≤ t

def ConicBounds (a b m t q w : ℝ) : Prop :=
  LinearBounds a b m t q w ∧ SOCBounds m t q w

end ReciprocalAnchor
