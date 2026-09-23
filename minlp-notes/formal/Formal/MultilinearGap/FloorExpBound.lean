import Mathlib

namespace MultilinearGap

/-- A global quadratic lower bound for the probability of at least one event
in the Poisson comparison used by the marginal-floor estimate. -/
theorem sub_sq_div_two_le_one_sub_exp_neg {u : ℝ} (hu : 0 ≤ u) :
    u - u ^ 2 / 2 ≤ 1 - Real.exp (-u) := by
  let f : ℝ → ℝ := fun x => 1 - x + x ^ 2 / 2 - Real.exp (-x)
  have hd (x : ℝ) : HasDerivAt f (x - 1 + Real.exp (-x)) x := by
    dsimp [f]
    convert! (((hasDerivAt_const x (1 : ℝ)).sub (hasDerivAt_id x)).add
      (((hasDerivAt_id x).pow 2).div_const 2)).sub
      ((hasDerivAt_id x).neg.exp) using 1
    simp
    ring
  have hm : Monotone f := monotone_of_deriv_nonneg
    (fun x => (hd x).differentiableAt) (fun x => by
      rw [(hd x).deriv]
      have := Real.add_one_le_exp (-x)
      linarith)
  have h := hm hu
  dsimp [f] at h
  simp only [neg_zero, Real.exp_zero, zero_pow (by norm_num : 2 ≠ 0),
    zero_div, sub_zero, add_zero, sub_self] at h
  linarith

end MultilinearGap
