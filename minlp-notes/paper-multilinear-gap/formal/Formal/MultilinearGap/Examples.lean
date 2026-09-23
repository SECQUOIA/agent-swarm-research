import Formal.MultilinearGap.ExactResults
import Formal.MultilinearGap.Termwise

/-! Exact instances printed in the standalone paper. The equalities concern
the continuous graph hull and actual individual-term gaps, not scalar surrogates. -/
namespace MultilinearGap
noncomputable section
open CubicGap

/-- The first row of the paper's table. -/
theorem example_two :
    hullGap (polynomial 2) (means 2) = 3 / 2 ∧
    termwiseGap (supports 2) (means 2) / hullGap (polynomial 2) (means 2) = 4 / 3 := by
  have h := hullGap_exact 2 1 (by norm_num) (by norm_num) (by norm_num)
    (by norm_num [cutoffBudget]) (by norm_num [cutoffBudget])
  norm_num at h
  constructor
  · exact h
  · rw [termwiseGap_eq 2 (by norm_num), h]
    norm_num

/-- The second row of the paper's table. -/
theorem example_eight :
    hullGap (polynomial 8) (means 8) = 7 / 2 ∧
    termwiseGap (supports 8) (means 8) / hullGap (polynomial 8) (means 8) = 16 / 7 := by
  have h := hullGap_exact 8 2 (by norm_num) (by norm_num) (by norm_num)
    (by norm_num [cutoffBudget]) (by norm_num [cutoffBudget])
  norm_num at h
  constructor
  · exact h
  · rw [termwiseGap_eq 8 (by norm_num), h]
    norm_num

/-- The third row of the paper's table. -/
theorem example_sixteen :
    hullGap (polynomial 16) (means 16) = 37 / 8 ∧
    termwiseGap (supports 16) (means 16) / hullGap (polynomial 16) (means 16) = 128 / 37 := by
  have h := hullGap_exact 16 3 (by norm_num) (by norm_num) (by norm_num)
    (by norm_num [cutoffBudget]) (by norm_num [cutoffBudget])
  norm_num at h
  constructor
  · exact h
  · rw [termwiseGap_eq 16 (by norm_num), h]
    norm_num

/-- The fourth row of the paper's table, whose ambient cube has 2^64 + 64 coordinates. -/
theorem example_sixty_four :
    hullGap (polynomial 64) (means 64) = 219 / 32 ∧
    termwiseGap (supports 64) (means 64) / hullGap (polynomial 64) (means 64) = 2048 / 219 := by
  have h := hullGap_exact 64 5 (by norm_num) (by norm_num) (by norm_num)
    (by norm_num [cutoffBudget]) (by norm_num [cutoffBudget])
  norm_num at h
  constructor
  · exact h
  · rw [termwiseGap_eq 64 (by norm_num), h]
    norm_num

/-- Adjacent cutoff formulas agree precisely at their common budget boundary. -/
theorem adjacent_cutoff_values (L s : ℕ) :
    ((s : ℝ) + ((L : ℝ) - s) / 2 ^ s) -
      ((s + 1 : ℝ) + ((L : ℝ) - (s + 1)) / 2 ^ (s + 1)) =
        cutoffBudget L (s + 1) - 1 := by
  simp only [cutoffBudget, Nat.cast_add, Nat.cast_one, pow_succ]
  field_simp
  ring

end
end MultilinearGap
