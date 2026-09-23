import Mathlib

/-! Exact Bernstein certificate for the scalar minorant in the cubic analytic family. -/

namespace CubicGap.Bernstein

noncomputable section

def cubic (a b c : ℝ) : ℝ :=
  6 * c ^ 3 + 27 * b * c ^ 2 + 18 * b ^ 2 + 30 * a * c + 20 * a * b + 9 * a ^ 2

def affine (a b c : ℝ) : ℝ := 37 * a + (79 / 2) * b + 38 * c - 103 / 3

def slack : ℝ := 901 / 120000

def lowerP (c : ℝ) : ℝ :=
  (-972 * c ^ 4 + 576 * c ^ 3 + 1404 * c ^ 2 - 768 * c + 101) / 96

def lowerR (c : ℝ) : ℝ :=
  (-78732 * c ^ 4 + 212256 * c ^ 3 - 203796 * c ^ 2 + 82032 * c - 11275) / 2976

/-- The five degree-four Bernstein basis terms, with the binomial factors explicit. -/
def bernstein4 (v₀ v₁ v₂ v₃ v₄ t : ℝ) : ℝ :=
  v₀ * (1 - t) ^ 4 + v₁ * 4 * t * (1 - t) ^ 3 +
    v₂ * 6 * t ^ 2 * (1 - t) ^ 2 + v₃ * 4 * t ^ 3 * (1 - t) + v₄ * t ^ 4

theorem bernstein4_lower {v₀ v₁ v₂ v₃ v₄ d t : ℝ}
    (ht : 0 ≤ t) (ht' : t ≤ 1)
    (h₀ : d ≤ v₀) (h₁ : d ≤ v₁) (h₂ : d ≤ v₂) (h₃ : d ≤ v₃) (h₄ : d ≤ v₄) :
    d ≤ bernstein4 v₀ v₁ v₂ v₃ v₄ t := by
  have hOne : 0 ≤ 1 - t := sub_nonneg.mpr ht'
  calc
    d = bernstein4 d d d d d t := by unfold bernstein4; ring
    _ ≤ bernstein4 v₀ v₁ v₂ v₃ v₄ t := by
      unfold bernstein4
      gcongr

theorem lowerP_first {c : ℝ} (hc : 0 ≤ c) (hc' : c ≤ 1 / 5) :
    slack ≤ lowerP c := by
  have ht : 0 ≤ 5 * c := by linarith
  have ht' : 5 * c ≤ 1 := by linarith
  have h := bernstein4_lower (d := slack) ht ht'
    (v₀ := 63125 / 60000) (v₁ := 39125 / 60000) (v₂ := 20975 / 60000)
    (v₃ := 9395 / 60000) (v₄ := 4133 / 60000)
    (by norm_num [slack]) (by norm_num [slack]) (by norm_num [slack])
    (by norm_num [slack]) (by norm_num [slack])
  convert h using 1
  unfold lowerP bernstein4
  ring

theorem lowerP_second {c : ℝ} (hc : 1 / 5 ≤ c) (hc' : c ≤ 3 / 10) :
    slack ≤ lowerP c := by
  have ht : 0 ≤ 10 * c - 2 := by linarith
  have ht' : 10 * c - 2 ≤ 1 := by linarith
  have h := bernstein4_lower (d := slack) ht ht'
    (v₀ := 16532 / 240000) (v₁ := 6008 / 240000) (v₂ := 1802 / 240000)
    (v₃ := 3788 / 240000) (v₄ := 11597 / 240000)
    (by norm_num [slack]) (by norm_num [slack]) (by norm_num [slack])
    (by norm_num [slack]) (by norm_num [slack])
  convert h using 1
  unfold lowerP bernstein4
  ring

theorem lowerR_first {c : ℝ} (hc : 3 / 10 ≤ c) (hc' : c ≤ 1 / 2) :
    slack ≤ lowerR c := by
  have ht : 0 ≤ 5 * c - 3 / 2 := by linarith
  have ht' : 5 * c - 3 / 2 ≤ 1 := by linarith
  have h := bernstein4_lower (d := slack) ht ht'
    (v₀ := 215357 / 7440000) (v₁ := 1285415 / 7440000) (v₂ := 1434125 / 7440000)
    (v₃ := 1250375 / 7440000) (v₄ := 1008125 / 7440000)
    (by norm_num [slack]) (by norm_num [slack]) (by norm_num [slack])
    (by norm_num [slack]) (by norm_num [slack])
  convert h using 1
  unfold lowerR bernstein4
  ring

theorem lowerR_second {c : ℝ} (hc : 1 / 2 ≤ c) (hc' : c ≤ 3 / 4) :
    slack ≤ lowerR c := by
  have ht : 0 ≤ 4 * c - 2 := by linarith
  have ht' : 4 * c - 2 ≤ 1 := by linarith
  have h := bernstein4_lower (d := slack) ht ht'
    (v₀ := 25808 / 190464) (v₁ := 18056 / 190464) (v₂ := 7964 / 190464)
    (v₃ := 9230 / 190464) (v₄ := 15869 / 190464)
    (by norm_num [slack]) (by norm_num [slack]) (by norm_num [slack])
    (by norm_num [slack]) (by norm_num [slack])
  convert h using 1
  unfold lowerR bernstein4
  ring

theorem lowerR_third {c : ℝ} (hc : 3 / 4 ≤ c) (hc' : c ≤ 1) :
    slack ≤ lowerR c := by
  have ht : 0 ≤ 4 * c - 3 := by linarith
  have ht' : 4 * c - 3 ≤ 1 := by linarith
  have h := bernstein4_lower (d := slack) ht ht'
    (v₀ := 15869 / 190464) (v₁ := 22508 / 190464) (v₂ := 34520 / 190464)
    (v₃ := 45920 / 190464) (v₄ := 31040 / 190464)
    (by norm_num [slack]) (by norm_num [slack]) (by norm_num [slack])
    (by norm_num [slack]) (by norm_num [slack])
  convert h using 1
  unfold lowerR bernstein4
  ring

/-- The constrained low-c branch uses only the upper bound on a; b is arbitrary. -/
theorem constrained_lower_bound {a b c : ℝ} (ha : a ≤ 1)
    (_hc : 0 ≤ c) (hc' : c ≤ 3 / 10) :
    lowerP c ≤ cubic a b c - affine a b c := by
  have hg : -49 / 6 + 30 * c - 15 * c ^ 2 ≤ 0 := by
    have h : 0 ≤ (3 / 10 - c) * (51 / 2 - 15 * c) := by
      apply mul_nonneg <;> linarith
    nlinarith
  have hlinear := mul_nonneg_of_nonpos_of_nonpos hg (sub_nonpos.mpr ha)
  have h₁ := sq_nonneg ((a - 1) + (10 / 9) * (b - (13 / 24 - 3 * c ^ 2 / 4)))
  have h₂ := sq_nonneg (b - (13 / 24 - 3 * c ^ 2 / 4))
  have hid : cubic a b c - affine a b c - lowerP c =
      9 * ((a - 1) + (10 / 9) * (b - (13 / 24 - 3 * c ^ 2 / 4))) ^ 2 +
      (62 / 9) * (b - (13 / 24 - 3 * c ^ 2 / 4)) ^ 2 +
      (-49 / 6 + 30 * c - 15 * c ^ 2) * (a - 1) := by
    unfold cubic affine lowerP
    ring
  linarith

/-- Completing the square gives an unrestricted lower bound in the other two coordinates. -/
theorem unrestricted_lower_bound (a b c : ℝ) :
    lowerR c ≤ cubic a b c - affine a b c := by
  have h₁ := sq_nonneg (a + (10 / 9) * b + (30 * c - 37) / 18)
  have h₂ := sq_nonneg (b + (9 * (27 * c ^ 2 - 79 / 2) - 10 * (30 * c - 37)) / 124)
  have hid : cubic a b c - affine a b c - lowerR c =
      9 * (a + (10 / 9) * b + (30 * c - 37) / 18) ^ 2 +
      (62 / 9) * (b + (9 * (27 * c ^ 2 - 79 / 2) - 10 * (30 * c - 37)) / 124) ^ 2 := by
    unfold cubic affine lowerR
    ring
  linarith

/-- Universal scalar minorant, with the exact positive rational slack from the paper.
The proof also covers all real b and all a ≤ 1. -/
theorem scalar_minorant {a b c : ℝ} (ha : a ≤ 1) (hc : 0 ≤ c) (hc' : c ≤ 1) :
    affine a b c + 901 / 120000 ≤ cubic a b c := by
  have h : slack ≤ cubic a b c - affine a b c := by
    by_cases hlow : c ≤ 3 / 10
    · apply le_trans _ (constrained_lower_bound ha hc hlow)
      by_cases hfirst : c ≤ 1 / 5
      · exact lowerP_first hc hfirst
      · exact lowerP_second (le_of_not_ge hfirst) hlow
    · apply le_trans _ (unrestricted_lower_bound a b c)
      by_cases hfirst : c ≤ 1 / 2
      · exact lowerR_first (le_of_not_ge hlow) hfirst
      · by_cases hsecond : c ≤ 3 / 4
        · exact lowerR_second (le_of_not_ge hfirst) hsecond
        · exact lowerR_third (le_of_not_ge hsecond) hc'
  unfold slack at h
  linarith

end

end CubicGap.Bernstein
