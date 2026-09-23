import CertifiedMinlp.ExactCorrections
import Mathlib.Analysis.Convex.Mul

/-! Exact arithmetic and quantified conclusions of the manuscript examples. -/
namespace CertifiedMinlp
namespace Examples

/-- These rational numbers are the exact IEEE binary64 values of the three
printed decimal inputs. Identification with a software parser is outside Lean. -/
theorem exact_binary_leaf_difference (x : ℝ) :
    (3602879701896397 / 36028797018963968 : ℝ) * x ^ 2 +
      (3602879701896397 / 18014398509481984 : ℝ) * x ^ 2 -
      (1351079888211149 / 4503599627370496 : ℝ) * x ^ 2 =
      -(1 / 2 ^ 55 : ℝ) * x ^ 2 := by ring

theorem exact_binary_leaf_concave :
    ConcaveOn ℝ Set.univ (fun x : ℝ => -(1 / 2 ^ 55 : ℝ) * x ^ 2) := by
  have h := (even_two.convexOn_pow (𝕜 := ℝ)).neg.smul
    (c := (1 / 2 ^ 55 : ℝ)) (by positivity)
  simpa only [Pi.smul_apply, Pi.neg_apply, smul_eq_mul, mul_neg, neg_mul] using h

theorem negative_quadratic_not_convex (c L U : ℝ) (hc : 0 < c) (hLU : L < U) :
    ¬ ConvexOn ℝ (Set.Icc L U) (fun x : ℝ => -c * x ^ 2) := by
  intro h
  have hconv := h.2
  have hm := hconv (x := L) ⟨le_rfl, hLU.le⟩ (y := U) ⟨hLU.le, le_rfl⟩
    (a := 1 / 2) (b := 1 / 2) (by norm_num) (by norm_num) (by norm_num)
  simp only [smul_eq_mul] at hm
  have hs : 0 < c * (U - L) ^ 2 := mul_pos hc (sq_pos_of_pos (sub_pos.mpr hLU))
  nlinarith

theorem exact_binary_leaf_not_convex (L U : ℝ) (hLU : L < U) :
    ¬ ConvexOn ℝ (Set.Icc L U) (fun x : ℝ => -(1 / 2 ^ 55 : ℝ) * x ^ 2) :=
  negative_quadratic_not_convex _ L U (by positivity) hLU

theorem quadratic_tangent (x : ℝ) :
    (2 / 3 : ℝ) * x - 2 / 9 ≤ x ^ 2 - 1 / 9 := by
  nlinarith [sq_nonneg (x - 1 / 3)]

theorem rounded_slope_excludes_feasible_point :
    (1 / 3 : ℝ) ^ 2 - 1 / 9 = 0 ∧
      (67 / 100 : ℝ) * (1 / 3) - 2 / 9 = 1 / 900 ∧
      0 < (67 / 100 : ℝ) * (1 / 3) - 2 / 9 := by norm_num

theorem rounded_slope_data :
    (2 / 3 : ℝ) - 67 / 100 = -1 / 300 ∧
      ((1 / 3 : ℝ) ^ 2 - 1 / 9) - (67 / 100) * (1 / 3) = -67 / 300 ∧
      max ((-1 / 300 : ℝ) * (1 / 3 - 0)) ((-1 / 300) * (1 / 3 - 1)) =
        1 / 450 ∧
      (-67 / 300 : ℝ) - 1 / 450 = -203 / 900 := by norm_num

theorem corrected_cut_identity (x : ℝ) :
    x ^ 2 - 1 / 9 - ((67 / 100) * x - 203 / 900) =
      (x - 67 / 200) ^ 2 + 799 / 360000 := by ring

theorem corrected_cut_strict_underestimate (x : ℝ) :
    (67 / 100 : ℝ) * x - 203 / 900 < x ^ 2 - 1 / 9 := by
  have h := corrected_cut_identity x
  nlinarith [sq_nonneg (x - 67 / 200)]

/-- The optimal intercept for the given slope, on the stated box. The proof of
necessity uses the interior contact point, rather than assuming optimality. -/
theorem fixed_slope_optimal_intercept (b : ℝ) :
    (∀ x ∈ Set.Icc (0 : ℝ) 1, (67 / 100 : ℝ) * x + b ≤ x ^ 2 - 1 / 9) ↔
      b ≤ -1 / 9 - (67 / 100 : ℝ) ^ 2 / 4 := by
  constructor
  · intro h
    have ht := h (67 / 200) (by constructor <;> norm_num)
    nlinarith
  · intro hb x _
    nlinarith [sq_nonneg (x - 67 / 200)]

theorem corrected_intercept_strictly_suboptimal :
    (-203 / 900 : ℝ) < -1 / 9 - (67 / 100 : ℝ) ^ 2 / 4 := by norm_num

theorem rounded_slope_halfline_failure :
    ¬ BddAbove (shiftValues (.lowerBounded 0) (1 / 3) (2 / 3 - 67 / 100)) := by
  rw [shiftValues_bddAbove_iff _ _ _ (by norm_num [Coordinate.contains])]
  norm_num [Coordinate.finiteShift]

theorem halfline_rounding_data :
    (2 / 3 : ℝ) - 3 / 5 = 1 / 15 ∧
      (Coordinate.lowerBounded 0).exactShift (1 / 3) (1 / 15) = 1 / 45 ∧
      (((1 / 3 : ℝ) ^ 2 - 1 / 9) - (3 / 5) * (1 / 3)) - 1 / 45 = -2 / 9 := by
  norm_num [Coordinate.exactShift]

theorem halfline_corrected_cut (x : ℝ) (_hx : 0 ≤ x) :
    (3 / 5 : ℝ) * x - 2 / 9 ≤ x ^ 2 - 1 / 9 := by
  nlinarith [sq_nonneg (x - 1 / 3)]

/-- Even the slope that fails the chosen support correction has a finite affine
underestimator on the half-line (indeed, on the entire real line). -/
theorem failed_support_has_underestimator (x : ℝ) :
    (67 / 100 : ℝ) * x + (-1 / 9 - (67 / 100 : ℝ) ^ 2 / 4) ≤
      x ^ 2 - 1 / 9 := by nlinarith [sq_nonneg (x - 67 / 200)]

theorem feasible_row_cut_without_underestimation :
    (∀ x ∈ Set.Icc (-1 : ℝ) 1, x ≤ 0 → 2 * x ≤ 0) ∧
      ¬ (∀ x ∈ Set.Icc (-1 : ℝ) 1, 2 * x ≤ x) := by
  constructor
  · intro x _ hx
    linarith
  · intro h
    have ht := h 1 (by constructor <;> norm_num)
    norm_num at ht

theorem false_million_lower_bound :
    (1 : ℝ) ≤ 1 ∧ ¬ ((10 ^ 6 : ℝ) ≤ 1) ∧
      ¬ (∀ x : ℝ, 1 ≤ x → 10 ^ 6 ≤ x) := by
  constructor
  · norm_num
  constructor
  · norm_num
  · intro h
    have ht := h 1 le_rfl
    norm_num at ht

theorem continuous_rounding_invalid :
    (1 / 2 : ℝ) ≤ 3 / 4 ∧ ¬ ((1 : ℝ) ≤ 3 / 4) ∧
      ¬ (∀ x : ℝ, 1 / 2 ≤ x → 1 ≤ x) := by
  constructor
  · norm_num
  constructor
  · norm_num
  · intro h
    have ht := h (3 / 4) (by norm_num)
    norm_num at ht

theorem continuous_adjacent_branches_not_exhaustive :
    ¬ (∀ x : ℝ, x ≤ 0 ∨ 1 ≤ x) := by
  intro h
  have ht := h (1 / 2)
  norm_num at ht

theorem epigraph_free_residual :
    Coordinate.free.finiteShift ((0 : ℝ) + (-1) - (-1)) ∧
      Coordinate.free.exactShift 0 ((0 : ℝ) + (-1) - (-1)) = 0 := by
  norm_num [Coordinate.finiteShift, Coordinate.exactShift]

end Examples
end CertifiedMinlp
