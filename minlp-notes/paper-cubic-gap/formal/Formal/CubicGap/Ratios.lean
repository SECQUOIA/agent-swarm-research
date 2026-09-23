import Formal.CubicGap.Results
import Formal.CubicGap.TermwiseFamilyUpper
import Formal.CubicGap.OrbitExpansion

namespace CubicGap

noncomputable section

/-- The weighted sum of the individual monomials' exact envelope widths. -/
def twoTermwiseGap (m : ℕ) : ℝ := termwiseUpperTwo m - termwiseLowerTwo m

def threeTermwiseGap (m : ℕ) (coef : Fin 6 → ℚ) : ℝ :=
  termwiseUpperThree m coef - termwiseLowerThree m coef

theorem two_termwise_gap (m : ℕ) : twoTermwiseGap m = (twoUpper m : ℝ) := by
  simp [twoTermwiseGap, termwiseUpperTwo_eq, termwiseLowerTwo_eq]

theorem three_termwise_gap (m : ℕ) (coef : Fin 6 → ℚ) :
    threeTermwiseGap m coef = ((orbitUpper m coef - orbitLower m coef : ℚ) : ℝ) := by
  simp [threeTermwiseGap, termwiseUpperThree_eq, termwiseLowerThree_eq]

theorem two_ratio4 :
    twoTermwiseGap 4 / hullGap (twoFamily 4) (twoMeans 4) = 27/16 := by
  rw [two_termwise_gap, two_hull_gap4, two_arithmetic4.2.2.1]
  norm_num

theorem two_ratio8 :
    twoTermwiseGap 8 / hullGap (twoFamily 8) (twoMeans 8) = 21/11 := by
  rw [two_termwise_gap, two_hull_gap8, two_arithmetic8.2.2.1]
  norm_num

theorem two_ratio12 :
    twoTermwiseGap 12 / hullGap (twoFamily 12) (twoMeans 12) = 99/50 := by
  rw [two_termwise_gap, two_hull_gap12, two_arithmetic12.2.2.1]
  norm_num

theorem two_ratio16 :
    twoTermwiseGap 16 / hullGap (twoFamily 16) (twoMeans 16) = 135/67 := by
  rw [two_termwise_gap, two_hull_gap16, two_arithmetic16.2.2.1]
  norm_num

theorem three_ratio6 :
    threeTermwiseGap 6 coefficients6 /
      hullGap (threeFamily 6 coefficients6) (threeMarginals 6) = 20891/10411 := by
  rw [three_termwise_gap, three_hull_gap6, arithmetic6.1, arithmetic6.2.1]
  norm_num

theorem three_ratio8 :
    threeTermwiseGap 8 coefficients8 /
      hullGap (threeFamily 8 coefficients8) (threeMarginals 8) = 6601/3225 := by
  rw [three_termwise_gap, three_hull_gap8, arithmetic8.1, arithmetic8.2.1]
  norm_num

theorem three_ratio64 :
    threeTermwiseGap 64 coefficients64 /
      hullGap (threeFamily 64 coefficients64) (threeMarginals 64) = 7443345/3445256 := by
  rw [three_termwise_gap, three_hull_gap64, arithmetic64.1, arithmetic64.2.1]
  norm_num

/-- Four explicit finite positive cubic examples exceed the bilinear factor two. -/
theorem four_strict_counterexamples :
    2 < twoTermwiseGap 16 / hullGap (twoFamily 16) (twoMeans 16) ∧
    2 < threeTermwiseGap 6 coefficients6 /
      hullGap (threeFamily 6 coefficients6) (threeMarginals 6) ∧
    2 < threeTermwiseGap 8 coefficients8 /
      hullGap (threeFamily 8 coefficients8) (threeMarginals 8) ∧
    2 < threeTermwiseGap 64 coefficients64 /
      hullGap (threeFamily 64 coefficients64) (threeMarginals 64) := by
  rw [two_ratio16, three_ratio6, three_ratio8, three_ratio64]
  norm_num

end
end CubicGap
