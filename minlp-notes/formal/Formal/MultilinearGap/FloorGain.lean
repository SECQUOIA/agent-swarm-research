import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Analysis.Convex.SpecificFunctions.Basic

/-! The scalar gain from a shifted harmonic density, uniformly in an anchor mean. -/

namespace MultilinearGap

open MeasureTheory Set

noncomputable section

/-- The simultaneous gain factor for a marginal floor. -/
def floorIntegral (L e : ℝ) : ℝ :=
  ∫ z in (0 : ℝ)..1, 1 - Real.exp (-1 / (L * (z + e)))

theorem shifted_failure_continuousOn {L τ S u : ℝ} (hL : 0 < L) (hτ : 0 < τ) :
    ContinuousOn (fun t : ℝ => 1 - Real.exp (-S / (L * (t + τ)))) (Icc 0 u) := by
  apply continuousOn_const.sub
  apply Real.continuous_exp.comp_continuousOn
  apply continuousOn_const.div (continuousOn_const.mul (continuousOn_id.add continuousOn_const))
  intro t ht
  exact ne_of_gt (mul_pos hL (by dsimp; linarith [ht.1]))

theorem shifted_failure_intervalIntegrable {L τ S u : ℝ}
    (hL : 0 < L) (hτ : 0 < τ) (hu : 0 ≤ u) :
    IntervalIntegrable (fun t : ℝ => 1 - Real.exp (-S / (L * (t + τ)))) volume 0 u :=
  (shifted_failure_continuousOn hL hτ).intervalIntegrable_of_Icc hu

theorem floorIntegral_intervalIntegrable {L e : ℝ} (hL : 0 < L) (he : 0 < e) :
    IntervalIntegrable (fun z : ℝ => 1 - Real.exp (-1 / (L * (z + e)))) volume 0 1 :=
  shifted_failure_intervalIntegrable hL he zero_le_one

theorem floorIntegral_pos {L e : ℝ} (hL : 0 < L) (he : 0 < e) :
    0 < floorIntegral L e := by
  apply intervalIntegral.integral_pos zero_lt_one (shifted_failure_continuousOn hL he)
  · intro z hz
    apply sub_nonneg.mpr
    apply Real.exp_le_one_iff.mpr
    exact div_nonpos_of_nonpos_of_nonneg (by norm_num)
      (mul_nonneg hL.le (by linarith [hz.1]))
  · refine ⟨0, by simp, ?_⟩
    apply sub_pos.mpr
    apply Real.exp_lt_one_iff.mpr
    exact div_neg_of_neg_of_pos (by norm_num) (by positivity)

theorem floorIntegral_le_one {L e : ℝ} (hL : 0 < L) (he : 0 < e) :
    floorIntegral L e ≤ 1 := by
  have h := intervalIntegral.integral_mono_on zero_le_one
    (floorIntegral_intervalIntegrable hL he) (intervalIntegrable_const (c := (1 : ℝ)))
    (fun z _ => sub_le_self (1 : ℝ) (Real.exp_pos _).le)
  simpa [floorIntegral] using h

/-- Concavity below one and monotonicity above one give a uniform exponential chord. -/
theorem min_one_mul_one_sub_exp_neg_le {a y : ℝ} (ha : 0 ≤ a) (hy : 0 ≤ y) :
    min 1 y * (1 - Real.exp (-a)) ≤ 1 - Real.exp (-(a * y)) := by
  by_cases hy1 : y ≤ 1
  · have h := convexOn_exp.2 (Set.mem_univ (-a)) (Set.mem_univ (0 : ℝ))
      hy (show 0 ≤ 1 - y by linarith) (show y + (1 - y) = 1 by ring)
    simp only [smul_eq_mul, mul_zero, add_zero, Real.exp_zero] at h
    rw [min_eq_right hy1]
    have heq : y * -a = -(a * y) := by ring
    rw [heq] at h
    nlinarith
  · rw [min_eq_left (le_of_not_ge hy1), one_mul]
    apply sub_le_sub_left
    apply Real.exp_le_exp.mpr
    nlinarith

/-- The pointwise comparison after scaling the anchor interval to `[0,1]`. -/
theorem floor_gain_pointwise {L τ u e S z : ℝ}
    (hL : 0 < L) (hτ : 0 < τ) (hu : 0 < u) (he : 0 < e)
    (hτu : τ / u ≤ e) (hS : 0 ≤ S) (hz : 0 ≤ z) :
    min u S * (1 - Real.exp (-1 / (L * (z + e)))) ≤
      u * (1 - Real.exp (-S / (L * (u * z + τ)))) := by
  have hd : 0 < L * (z + e) := mul_pos hL (by positivity)
  have hd' : 0 < L * (u * z + τ) := mul_pos hL (by positivity)
  have hchord := min_one_mul_one_sub_exp_neg_le
    (show 0 ≤ 1 / (L * (z + e)) by positivity) (div_nonneg hS hu.le)
  have hmin : u * min 1 (S / u) = min u S := by
    rw [mul_min_of_nonneg _ _ hu.le, mul_one, mul_div_cancel₀ S hu.ne']
  have hchord' := mul_le_mul_of_nonneg_left hchord hu.le
  rw [← mul_assoc, hmin] at hchord'
  rw [← neg_div] at hchord'
  refine hchord'.trans (mul_le_mul_of_nonneg_left ?_ hu.le)
  apply sub_le_sub_left
  apply Real.exp_le_exp.mpr
  have hτ' : τ ≤ e * u := (div_le_iff₀ hu).mp hτu
  have hdle : L * (u * z + τ) ≤ u * (L * (z + e)) := by
    nlinarith [mul_le_mul_of_nonneg_left hτ' hL.le]
  have hdiv := div_le_div_of_nonneg_left hS hd' hdle
  have heq : 1 / (L * (z + e)) * (S / u) = S / (u * (L * (z + e))) := by
    simp only [div_eq_mul_inv, mul_inv_rev]; ring
  rw [heq]
  simpa only [neg_div] using neg_le_neg hdiv

/-- The same gain factor works for every positive anchor mean with `τ / u ≤ e`.
The total failure mass may be zero. -/
theorem floor_integral_gain {L τ u e S : ℝ}
    (hL : 0 < L) (hτ : 0 < τ) (hu : 0 < u) (he : 0 < e)
    (hτu : τ / u ≤ e) (hS : 0 ≤ S) :
    min u S * floorIntegral L e ≤
      ∫ t in (0 : ℝ)..u, 1 - Real.exp (-S / (L * (t + τ))) := by
  have hc : ContinuousOn (fun z : ℝ => 1 - Real.exp (-S / (L * (u * z + τ))))
      (Icc 0 1) := by
    apply continuousOn_const.sub
    apply Real.continuous_exp.comp_continuousOn
    apply continuousOn_const.div
      (continuousOn_const.mul ((continuousOn_const.mul continuousOn_id).add continuousOn_const))
    intro z hz
    exact ne_of_gt (mul_pos hL (by dsimp; nlinarith [hz.1]))
  have h := intervalIntegral.integral_mono_on zero_le_one
    ((floorIntegral_intervalIntegrable hL he).const_mul (min u S))
    ((hc.intervalIntegrable_of_Icc zero_le_one).const_mul u)
    (fun z hz => floor_gain_pointwise hL hτ hu he hτu hS hz.1)
  rw [intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul] at h
  have hscale := intervalIntegral.smul_integral_comp_mul_left
    (a := (0 : ℝ)) (b := 1) (fun t : ℝ => 1 - Real.exp (-S / (L * (t + τ)))) u
  simp only [smul_eq_mul, mul_zero, mul_one] at hscale
  exact h.trans_eq hscale

end
end MultilinearGap
