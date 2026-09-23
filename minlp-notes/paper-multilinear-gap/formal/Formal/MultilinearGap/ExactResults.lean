import Formal.MultilinearGap.ExactLaw
import Formal.MultilinearGap.ExactUpper

/-! Exact finite graph-hull gap of the dyadic counterexample family. -/
namespace MultilinearGap
noncomputable section
open CubicGap

/-- The cutoff construction attains the exact lower envelope. -/
theorem polynomial_exact_minimum (L s : ℕ) (hs1 : 1 ≤ s) (hsL : s < L)
    (hlo : cutoffBudget L (s + 1) ≤ 1) (hhi : 1 ≤ cutoffBudget L s) :
    IsLeast (envelopeValues (polynomial L) (means L))
      ((L : ℝ) - ((s : ℝ) + ((L : ℝ) - s) / 2 ^ s)) := by
  apply minimum_from_laws (polynomial L) (polynomial_separatelyAffine L) (means L)
  · intro μ hmean
    simpa only [Nat.cast_sub (Nat.le_of_lt hsL)] using
      law_polynomial_exact_lower_bound L s (Nat.le_of_lt hsL) μ hmean
  · exact exists_exact_attaining_law L s hs1 hsL hlo hhi

/-- Exact width of the original continuous graph hull, including attainment
of both envelope endpoints. -/
theorem hullGap_exact (L s : ℕ) (hL : 2 ≤ L) (hs1 : 1 ≤ s) (hsL : s < L)
    (hlo : cutoffBudget L (s + 1) ≤ 1) (hhi : 1 ≤ cutoffBudget L s) :
    hullGap (polynomial L) (means L) = (s : ℝ) + ((L : ℝ) - s) / 2 ^ s := by
  rw [hullGap, (polynomial_maximum L hL).csSup_eq,
    (polynomial_exact_minimum L s hs1 hsL hlo hhi).csInf_eq]
  ring

/-- Every family size at least two has a cutoff yielding the exact formula. -/
theorem exists_hullGap_exact (L : ℕ) (hL : 2 ≤ L) :
    ∃ s : ℕ, 1 ≤ s ∧ s < L ∧ cutoffBudget L (s + 1) ≤ 1 ∧
      1 ≤ cutoffBudget L s ∧
      hullGap (polynomial L) (means L) = (s : ℝ) + ((L : ℝ) - s) / 2 ^ s := by
  obtain ⟨s, hs1, hsL, hlo, hhi⟩ := exists_exact_cutoff L hL
  exact ⟨s, hs1, hsL, hlo, hhi, hullGap_exact L s hL hs1 hsL hlo hhi⟩

end
end MultilinearGap
