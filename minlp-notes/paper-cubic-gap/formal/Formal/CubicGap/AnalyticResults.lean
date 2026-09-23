import Formal.CubicGap.AnalyticLimit
import Formal.CubicGap.ThreeSupports
import Formal.CubicGap.RoundingUpper

/-! Two-sided bounds for the actual degree-three supremum on cubes and on all
finite nonnegative boxes. -/

namespace CubicGap

open MultilinearGap
noncomputable section

/-- Each analytic family ratio belongs to the original degree-three class. -/
theorem analyticRatio_mem_degreeRatios (m : ℕ) (hm : 9 ≤ m) :
    analyticRatio m ∈ degreeRatios 3 :=
  three_ratio_mem_degreeRatios m (analyticCoefficients m)
    (analyticCoefficients_nonneg m) (analytic_hullGap_pos m hm)

/-- The same cube is an admissible finite nonnegative box. -/
theorem analyticRatio_mem_boxDegreeRatios (m : ℕ) (hm : 9 ≤ m) :
    analyticRatio m ∈ boxDegreeRatios 3 :=
  degreeRatios_subset_boxDegreeRatios 3 (analyticRatio_mem_degreeRatios m hm)

/-- The Bernstein slack gives a lower bound for the actual cube supremum,
without assuming convergence of the analytic family ratios. -/
theorem analyticRefinedLimit_le_degreeSupremum :
    analyticRefinedLimit ≤ degreeSupremum 3 := by
  apply analyticRatio_uniform_upper_ge_refined
  intro k
  exact le_csSup (degreeRatios_bddAbove cubic_degree_bound)
    (analyticRatio_mem_degreeRatios _ (analyticSize_ge_nine k))

/-- The refined lower bound also applies to the supremum over all finite boxes. -/
theorem analyticRefinedLimit_le_boxDegreeSupremum :
    analyticRefinedLimit ≤ boxDegreeSupremum 3 := by
  apply analyticRatio_uniform_upper_ge_refined
  intro k
  exact le_csSup (boxDegreeRatios_bddAbove cubic_degree_bound)
    (analyticRatio_mem_boxDegreeRatios _ (analyticSize_ge_nine k))

/-- The headline lower bound for the original degree-three cube supremum. -/
theorem cubic_degreeSupremum_lower : (483 / 223 : ℝ) ≤ degreeSupremum 3 :=
  analytic_headline_lt_refined.le.trans analyticRefinedLimit_le_degreeSupremum

/-- The headline lower bound for the original all-box degree-three supremum. -/
theorem cubic_boxDegreeSupremum_lower : (483 / 223 : ℝ) ≤ boxDegreeSupremum 3 :=
  analytic_headline_lt_refined.le.trans analyticRefinedLimit_le_boxDegreeSupremum

/-- Certified two-sided bounds for the worst degree-three cube ratio. -/
theorem cubic_degreeSupremum_sandwich :
    (1610000 / 743033 : ℝ) ≤ degreeSupremum 3 ∧
      degreeSupremum 3 ≤ (31 / 12 : ℝ) := by
  exact ⟨analyticRefinedLimit_reduced ▸ analyticRefinedLimit_le_degreeSupremum,
    cubic_degreeSupremum_le⟩

/-- Certified two-sided bounds for the worst degree-three ratio over all
finite nonnegative boxes, including boxes with fixed coordinates. -/
theorem cubic_boxDegreeSupremum_sandwich :
    (1610000 / 743033 : ℝ) ≤ boxDegreeSupremum 3 ∧
      boxDegreeSupremum 3 ≤ (31 / 12 : ℝ) := by
  exact ⟨analyticRefinedLimit_reduced ▸ analyticRefinedLimit_le_boxDegreeSupremum,
    cubic_boxDegreeSupremum_le⟩

/-- The explicit 108-variable member is an admissible degree-three witness above two. -/
theorem analytic_thirty_six_witness :
    analyticRatio 36 ∈ degreeRatios 3 ∧ 2 < analyticRatio 36 :=
  ⟨analyticRatio_mem_degreeRatios 36 (by norm_num), analyticRatio_thirty_six_gt_two⟩

/-- Every nonzero coefficient of the expanded analytic polynomial is a positive
natural integer, and its distinct squarefree support has degree two or three. -/
theorem analytic_nonzero_support (m : ℕ) (hm : 9 ∣ m)
    (s : Finset (Fin 3 × Fin m))
    (hs : threeSupportCoefficients m (analyticCoefficients m) s ≠ 0) :
    (∃ n : ℕ, 0 < n ∧ threeSupportCoefficients m (analyticCoefficients m) s = (n : ℝ)) ∧
      (s.card = 2 ∨ s.card = 3) := by
  obtain ⟨n, hn⟩ := threeSupportCoefficients_nat m (analyticCoefficients m)
    (analyticCoefficients_integer m hm) s
  refine ⟨⟨n, ?_, hn⟩, threeSupportCoefficients_card m (analyticCoefficients m) s hs⟩
  by_contra h
  have hn0 : n = 0 := by omega
  exact hs (by simpa [hn0] using hn)

/-- The finite witnesses use genuine positive integer monomial coefficients,
with no constant, linear, repeated-variable, or higher-degree terms. -/
theorem analytic_integer_support_witness (c : ℝ) (hc : c < analyticRefinedLimit) :
    ∃ m, 9 ≤ m ∧ 9 ∣ m ∧
      (∀ s, threeSupportCoefficients m (analyticCoefficients m) s ≠ 0 →
        (∃ n : ℕ, 0 < n ∧
          threeSupportCoefficients m (analyticCoefficients m) s = (n : ℝ)) ∧
        (s.card = 2 ∨ s.card = 3)) ∧
      0 < hullGap (analyticFamily m) (analyticMeans m) ∧ c < analyticRatio m := by
  obtain ⟨m, hm, hdiv, _, hgap, hratio⟩ := analytic_integer_family_witness c hc
  exact ⟨m, hm, hdiv, fun s hs => analytic_nonzero_support m hdiv s hs, hgap, hratio⟩

end
end CubicGap
