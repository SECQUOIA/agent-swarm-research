import Formal.InfiniteAggregation.Model

/-!
# Two scalar endpoints with a prescribed quadratic increment

The endpoints lie on opposite sides of zero, so zero is their convex combination.
-/

noncomputable section

namespace InfiniteAggregation

theorem two_roots_weights (d k : ℝ) (hk : 0 < k) :
    ∃ tm tp a b : ℝ,
      tm < 0 ∧ 0 < tp ∧
      2 * d * tm + tm ^ 2 = k ∧ 2 * d * tp + tp ^ 2 = k ∧
      0 ≤ a ∧ 0 ≤ b ∧ a + b = 1 ∧ a * tm + b * tp = 0 := by
  let s := Real.sqrt (d ^ 2 + k)
  have hs : 0 ≤ s := Real.sqrt_nonneg _
  have hs2 : s ^ 2 = d ^ 2 + k := Real.sq_sqrt (by positivity)
  have hsd : d < s := by nlinarith [sq_nonneg (s + d)]
  have hsnd : -d < s := by nlinarith [sq_nonneg (s - d)]
  have hsp : 0 < s := by nlinarith
  refine ⟨-d - s, -d + s, (-d + s) / (2 * s), (d + s) / (2 * s),
    by linarith, by linarith, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · nlinarith
  · nlinarith
  · exact div_nonneg (by linarith) (by positivity)
  · exact div_nonneg (by linarith) (by positivity)
  · field_simp
    ring
  · field_simp
    ring

end InfiniteAggregation
