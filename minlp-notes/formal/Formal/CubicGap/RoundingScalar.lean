import Mathlib

/-! Scalar inequalities for the 18:6:7 cubic rounding mixture.
All statements include equality and zero-gap boundaries. -/
namespace CubicGap

/-- The one-low-coordinate inequality holds without upper bounds on the failure masses. -/
theorem rounding_one_low (u a b : ℝ) (hu : 0 ≤ u) (hb : 0 ≤ b) (hba : b ≤ a) :
    12 * min u (a + b) ≤
      18 * (min u a / 2 + min u b / 4) +
        7 * (min u (2 * a) / 2 + min u (2 * b) / 4) := by
  simp only [min_def]
  split_ifs <;> linarith

/-- The common orientation/high-biased deficiency controls three eighths of the term gap. -/
theorem rounding_high_orientation (u a b : ℝ) (hba : b ≤ a) :
    3 / 8 * min u (a + b) ≤ a / 2 + b / 4 := by
  have h := min_le_right u (a + b)
  linarith

/-- Independence controls seven sixteenths of the gap when all three marginals are high. -/
theorem rounding_high_independent (u a b : ℝ)
    (hu : 1 / 2 ≤ u) (hu1 : u ≤ 1) (ha : 0 ≤ a) (ha1 : a ≤ 1 / 2)
    (hb : 0 ≤ b) (hb1 : b ≤ 1 / 2) :
    7 / 16 * min u (a + b) ≤ u * (a + b - a * b) := by
  let s := a + b
  have hs : 0 ≤ s := by dsimp [s]; linarith
  have hs1 : s ≤ 1 := by dsimp [s]; linarith
  have hab : a * b ≤ s ^ 2 / 4 := by dsimp [s]; nlinarith [sq_nonneg (a - b)]
  have hu0 : 0 ≤ u := by linarith
  have hprod := mul_le_mul_of_nonneg_left hab hu0
  have hquad : 7 / 16 ≤ u * (1 - u / 4) := by
    nlinarith [mul_nonneg (show 0 ≤ u - 1 / 2 by linarith)
      (show 0 ≤ 7 / 2 - u by linarith)]
  by_cases hsu : s ≤ u
  · rw [min_eq_right hsu]
    have hmon : u * (1 - u / 4) ≤ u * (1 - s / 4) := by
      nlinarith [mul_nonneg hu0 (sub_nonneg.mpr hsu)]
    have hscaled := mul_le_mul_of_nonneg_right (hquad.trans hmon) hs
    dsimp [s] at *
    nlinarith
  · rw [min_eq_left (le_of_not_ge hsu)]
    have hmon : u - u ^ 2 / 4 ≤ s - s ^ 2 / 4 := by
      nlinarith [mul_nonneg (show 0 ≤ s - u by linarith)
        (show 0 ≤ 4 - s - u by linarith)]
    have hlower : 7 / 16 ≤ s - s ^ 2 / 4 := by nlinarith
    have hscaled := mul_le_mul_of_nonneg_left hlower hu0
    dsimp [s] at *
    nlinarith

/-- Independence supplies half the smallest marginal if a second marginal is low. -/
theorem rounding_two_low_independent (u v w : ℝ)
    (hu : 0 ≤ u) (hv : 0 ≤ v) (hvhalf : v ≤ 1 / 2) (hw : w ≤ 1) :
    u / 2 ≤ u * (1 - v * w) := by
  have hvw : v * w ≤ 1 / 2 := by nlinarith [mul_le_mul_of_nonneg_left hw hv]
  nlinarith [mul_le_mul_of_nonneg_left hvw hu]

/-- Weighted deficiency bound for cubics with at least two low coordinates. -/
theorem rounding_two_low_mixture (u dO dI dB : ℝ)
    (hO : u / 2 ≤ dO) (hI : u / 2 ≤ dI) (hB : 0 ≤ dB) :
    12 * u ≤ 18 * dO + 6 * dI + 7 * dB := by linarith

/-- Weighted deficiency bound for cubics with exactly one low coordinate. -/
theorem rounding_one_low_mixture (u a b dO dI dB : ℝ)
    (hu : 0 ≤ u) (hb : 0 ≤ b) (hba : b ≤ a)
    (hO : min u a / 2 + min u b / 4 ≤ dO)
    (hI : 0 ≤ dI) (hB : min u (2 * a) / 2 + min u (2 * b) / 4 ≤ dB) :
    12 * min u (a + b) ≤ 18 * dO + 6 * dI + 7 * dB := by
  linarith [rounding_one_low u a b hu hb hba]

/-- Weighted deficiency bound for cubics with no low coordinate. -/
theorem rounding_high_mixture (t dO dI dB : ℝ)
    (hO : 3 / 8 * t ≤ dO) (hI : 7 / 16 * t ≤ dI) (hB : 3 / 8 * t ≤ dB) :
    12 * t ≤ 18 * dO + 6 * dI + 7 * dB := by linarith

/-- A doubled failure interval improves, or preserves, the bilinear half-gap bound. -/
theorem rounding_bilinear_one_low (u a : ℝ) (ha : 0 ≤ a) :
    min u a / 2 ≤ min u (2 * a) / 2 := by
  exact div_le_div_of_nonneg_right (min_le_min_left u (by linarith)) (by norm_num)

/-- Bilinear terms with two low marginals. -/
theorem rounding_bilinear_low_mixture (t dO dI dB : ℝ)
    (hO : t / 2 ≤ dO) (hI : t / 2 ≤ dI) (hB : 0 ≤ dB) :
    12 * t ≤ 18 * dO + 6 * dI + 7 * dB := by linarith

/-- Bilinear terms with one low marginal, retaining the stronger 25/62 estimate. -/
theorem rounding_bilinear_mixed_mixture (t dO dI dB : ℝ)
    (hO : t / 2 ≤ dO) (hI : 0 ≤ dI) (hB : t / 2 ≤ dB) :
    25 / 2 * t ≤ 18 * dO + 6 * dI + 7 * dB := by linarith

/-- The common 12/31 guarantee for the mixed bilinear case. -/
theorem rounding_bilinear_mixed_uniform (t dO dI dB : ℝ) (ht : 0 ≤ t)
    (hO : t / 2 ≤ dO) (hI : 0 ≤ dI) (hB : t / 2 ≤ dB) :
    12 * t ≤ 18 * dO + 6 * dI + 7 * dB := by linarith

/-- Bilinear terms with two high marginals, retaining the stronger half-gap estimate. -/
theorem rounding_bilinear_high_mixture (t dO dI dB : ℝ)
    (hO : t / 2 ≤ dO) (hI : t / 2 ≤ dI) (hB : t / 2 ≤ dB) :
    31 / 2 * t ≤ 18 * dO + 6 * dI + 7 * dB := by linarith

/-- The common 12/31 guarantee for the high bilinear case. -/
theorem rounding_bilinear_high_uniform (t dO dI dB : ℝ) (ht : 0 ≤ t)
    (hO : t / 2 ≤ dO) (hI : t / 2 ≤ dI) (hB : t / 2 ≤ dB) :
    12 * t ≤ 18 * dO + 6 * dI + 7 * dB := by linarith

end CubicGap
