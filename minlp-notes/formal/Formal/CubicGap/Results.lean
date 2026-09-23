import Formal.CubicGap.Maxima
import Formal.CubicGap.TwoResults
import Formal.CubicGap.ThreeResults

namespace CubicGap

noncomputable section

theorem twoMeans_eq_threshold (m : ℕ) : twoMeans m = thresholdTwoMeans m := by
  funext i
  rcases i with ⟨g,j⟩
  fin_cases g <;> norm_num [twoMeans, thresholdTwoMeans]

theorem threeMarginals_eq_threshold (m : ℕ) : threeMarginals m = thresholdThreeMeans m := by
  funext i
  rcases i with ⟨g,j⟩
  fin_cases g <;> norm_num [threeMarginals, thresholdThreeMeans]

theorem two_hull_gap4 : hullGap (twoFamily 4) (twoMeans 4) = 16 := by
  have hu := two_maximum 4
  rw [← twoMeans_eq_threshold] at hu
  rw [hullGap, hu.csSup_eq, two_minimum4.csInf_eq]
  norm_num [twoUpper, Nat.choose]

theorem two_hull_gap8 : hullGap (twoFamily 8) (twoMeans 8) = 132 := by
  have hu := two_maximum 8
  rw [← twoMeans_eq_threshold] at hu
  rw [hullGap, hu.csSup_eq, two_minimum8.csInf_eq]
  norm_num [twoUpper, Nat.choose]

theorem two_hull_gap12 : hullGap (twoFamily 12) (twoMeans 12) = 450 := by
  have hu := two_maximum 12
  rw [← twoMeans_eq_threshold] at hu
  rw [hullGap, hu.csSup_eq, two_minimum12.csInf_eq]
  norm_num [twoUpper, Nat.choose]

theorem two_hull_gap16 : hullGap (twoFamily 16) (twoMeans 16) = 1072 := by
  have hu := two_maximum 16
  rw [← twoMeans_eq_threshold] at hu
  rw [hullGap, hu.csSup_eq, two_minimum16.csInf_eq]
  norm_num [twoUpper, Nat.choose]

theorem three_hull_gap6 :
    hullGap (threeFamily 6 coefficients6) (threeMarginals 6) = 10411/52 := by
  have hu := three_maximum 6 (by decide) coefficients6 (by decide +kernel)
  rw [← threeMarginals_eq_threshold] at hu
  rw [hullGap, hu.csSup_eq, three_minimum6.csInf_eq, arithmetic6.1]
  norm_num

theorem three_hull_gap8 :
    hullGap (threeFamily 8 coefficients8) (threeMarginals 8) = 3225/7 := by
  have hu := three_maximum 8 (by decide) coefficients8 (by decide +kernel)
  rw [← threeMarginals_eq_threshold] at hu
  rw [hullGap, hu.csSup_eq, three_minimum8.csInf_eq, arithmetic8.1]
  norm_num

theorem three_hull_gap64 :
    hullGap (threeFamily 64 coefficients64) (threeMarginals 64) = 27562048/105 := by
  have hu := three_maximum 64 (by decide) coefficients64 (by decide +kernel)
  rw [← threeMarginals_eq_threshold] at hu
  rw [hullGap, hu.csSup_eq, three_minimum64.csInf_eq, arithmetic64.1]
  norm_num

end
end CubicGap
