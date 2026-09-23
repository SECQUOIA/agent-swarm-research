import Formal.MultilinearGap.FloorGain
import Formal.MultilinearGap.FloorExpBound

/-! Two explicit estimates for the shifted harmonic failure integral.
Both estimates split the integration interval at `1 / L`; the lower estimate
retains the quadratic error in the exponential expansion. -/

namespace MultilinearGap
open Set MeasureTheory
noncomputable section

private lemma failure_cont {L e a b : ℝ} (hL : 0 < L) (he : 0 < e)
    (ha : 0 ≤ a) (hab : a ≤ b) :
    ContinuousOn (fun z : ℝ => 1 - Real.exp (-1 / (L * (z + e)))) (uIcc a b) := by
  rw [uIcc_of_le hab]
  apply continuousOn_const.sub
  apply Real.continuous_exp.comp_continuousOn
  apply continuousOn_const.div (continuousOn_const.mul (continuousOn_id.add continuousOn_const))
  intro z hz
  exact ne_of_gt (mul_pos hL (show 0 < z + e by linarith [hz.1]))

private lemma inv_integrable {a b : ℝ} (ha : 0 < a) (hab : a ≤ b) :
    IntervalIntegrable (fun z : ℝ => 1 / z) volume a b := by
  apply ContinuousOn.intervalIntegrable
  rw [uIcc_of_le hab]
  exact continuousOn_const.div continuousOn_id (fun z hz => ne_of_gt (lt_of_lt_of_le ha hz.1))

private lemma literal_floorIntegral_upper {L e : ℝ} (hL : 1 < L) (he : 0 < e) :
    (∫ z in (0 : ℝ)..1, 1 - Real.exp (-1 / (L * (z + e)))) ≤
      (1 + Real.log L) / L := by
  have hL0 : 0 < L := by linarith
  have ha : 0 < 1 / L := one_div_pos.mpr hL0
  have ha1 : 1 / L ≤ 1 := (div_le_one hL0).mpr hL.le
  have hfa := (failure_cont hL0 he (a := 0) (by norm_num) ha.le).intervalIntegrable (μ := volume)
  have hfb := (failure_cont hL0 he ha.le ha1).intervalIntegrable (μ := volume)
  have hga := intervalIntegral.integral_mono_on ha.le hfa intervalIntegrable_const
    (g := fun _ => (1 : ℝ)) (fun z hz => by linarith [Real.exp_pos (-1 / (L * (z + e)))])
  have hgb := intervalIntegral.integral_mono_on ha1 hfb ((inv_integrable ha ha1).const_mul (1 / L))
    (g := fun z => (1 / L) * (1 / z)) (fun z hz => by
      have hz0 : 0 < z := lt_of_lt_of_le ha hz.1
      have hx := Real.add_one_le_exp (-1 / (L * (z + e)))
      have hdiv : 1 / (L * (z + e)) ≤ 1 / (L * z) :=
        one_div_le_one_div_of_le (mul_pos hL0 hz0) (by nlinarith)
      have hid : 1 / (L * z) = (1 / L) * (1 / z) := by ring
      rw [← hid]
      simp only [neg_div] at hx ⊢
      linarith)
  rw [intervalIntegral.integral_const_mul, integral_one_div_of_pos ha zero_lt_one] at hgb
  simp only [one_div_one_div] at hgb
  rw [← intervalIntegral.integral_add_adjacent_intervals hfa hfb]
  simp only [intervalIntegral.integral_const, sub_zero, smul_eq_mul, mul_one] at hga
  calc
    _ ≤ 1 / L + (1 / L) * Real.log L := add_le_add hga hgb
    _ = _ := by ring

private lemma inv_sq_integrable {a b : ℝ} (ha : 0 < a) (hab : a ≤ b) :
    IntervalIntegrable (fun z : ℝ => 1 / z ^ 2) volume a b := by
  apply ContinuousOn.intervalIntegrable
  rw [uIcc_of_le hab]
  exact continuousOn_const.div (continuousOn_id.pow 2)
    (fun z hz => pow_ne_zero 2 (ne_of_gt (lt_of_lt_of_le ha hz.1)))

private lemma integral_inv_sq_floor {L : ℝ} (hL : 1 < L) :
    (∫ z in (1 / L)..1, 1 / z ^ 2) = L - 1 := by
  have ha : 0 < 1 / L := one_div_pos.mpr (by linarith)
  have ha1 : 1 / L ≤ 1 := (div_le_one (by linarith)).mpr hL.le
  have hh := integral_zpow (a := 1 / L) (b := 1) (n := -2)
    (Or.inr ⟨by norm_num, notMem_uIcc_of_lt ha zero_lt_one⟩)
  norm_num at hh
  simpa [zpow_neg, zpow_ofNat, one_div, div_neg, neg_sub] using hh

/-- The harmonic integral is at most `(1 + log L) / L`, uniformly in the shift. -/
theorem floorIntegral_upper {L e : ℝ} (hL : 1 < L) (he : 0 < e) :
    floorIntegral L e ≤ (1 + Real.log L) / L :=
  literal_floorIntegral_upper hL he

private lemma lower_pointwise {L e z : ℝ} (hL : 0 < L) (he : 0 < e)
    (hz : 1 / L ≤ z) :
    (1 / (L * (1 + L * e))) * (1 / z) - (1 / (2 * L^2)) * (1 / z^2) ≤
      1 - Real.exp (-1 / (L * (z + e))) := by
  have hz0 : 0 < z := lt_of_lt_of_le (one_div_pos.mpr hL) hz
  have hze : 0 < z + e := by positivity
  have hLe : 0 < 1 + L * e := by positivity
  have hLz : 1 ≤ L * z := (div_le_iff₀ hL).mp hz |>.trans_eq (mul_comm z L)
  have hden : L * (z + e) ≤ L * (1 + L * e) * z := by
    nlinarith [mul_le_mul_of_nonneg_left hLz (mul_pos hL he).le]
  have hlo := one_div_le_one_div_of_le (mul_pos hL hze) hden
  have hhi := one_div_le_one_div_of_le (mul_pos hL hz0)
    (show L * z ≤ L * (z + e) by nlinarith)
  have hq := sub_sq_div_two_le_one_sub_exp_neg (le_of_lt (one_div_pos.mpr (mul_pos hL hze)))
  have hsq : (1 / (L * (z + e)))^2 ≤ (1 / (L * z))^2 :=
    pow_le_pow_left₀ (by positivity) hhi 2
  have hid1 : 1 / (L * (1 + L * e) * z) = (1 / (L * (1 + L * e))) * (1 / z) := by
    simp only [one_div, mul_inv_rev]
    ring
  have hid2 : (1 / (L * z))^2 / 2 = (1 / (2 * L^2)) * (1 / z^2) := by ring
  rw [hid1] at hlo
  rw [show -(1 / (L * (z + e))) = -1 / (L * (z + e)) by ring] at hq
  nlinarith

/-- A lower bound retaining the shift loss and the exact integrated quadratic error. -/
theorem floorIntegral_lower {L e : ℝ} (hL : 1 < L) (he : 0 < e) :
    Real.log L / (L * (1 + L * e)) - (L - 1) / (2 * L^2) ≤ floorIntegral L e := by
  have hL0 : 0 < L := by linarith
  have ha : 0 < 1 / L := one_div_pos.mpr hL0
  have ha1 : 1 / L ≤ 1 := (div_le_one hL0).mpr hL.le
  have hfa := (failure_cont hL0 he (a := 0) (by norm_num) ha.le).intervalIntegrable (μ := volume)
  have hfb := (failure_cont hL0 he ha.le ha1).intervalIntegrable (μ := volume)
  have hfirst : 0 ≤ ∫ z in (0 : ℝ)..(1/L), 1 - Real.exp (-1 / (L * (z + e))) := by
    apply intervalIntegral.integral_nonneg ha.le
    intro z hz
    have hz0 : 0 ≤ z := hz.1
    have hd : 0 < L * (z + e) := mul_pos hL0 (by linarith)
    exact sub_nonneg.mpr (Real.exp_le_one_iff.mpr
      (div_nonpos_of_nonpos_of_nonneg (by norm_num) hd.le))
  have hg := ((inv_integrable ha ha1).const_mul (1 / (L * (1 + L * e)))).sub
    ((inv_sq_integrable ha ha1).const_mul (1 / (2 * L^2)))
  have hm := intervalIntegral.integral_mono_on ha1 hg hfb
    (fun z hz => lower_pointwise hL0 he hz.1)
  rw [intervalIntegral.integral_sub
      ((inv_integrable ha ha1).const_mul (1 / (L * (1 + L * e))))
      ((inv_sq_integrable ha ha1).const_mul (1 / (2 * L^2))),
    intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
    integral_one_div_of_pos ha zero_lt_one, integral_inv_sq_floor hL] at hm
  simp only [one_div_one_div] at hm
  have hs := intervalIntegral.integral_add_adjacent_intervals hfa hfb
  unfold floorIntegral
  calc
    _ = (1 / (L * (1 + L * e))) * Real.log L - (1 / (2 * L^2)) * (L - 1) := by ring
    _ ≤ ∫ z in (1/L)..1, 1 - Real.exp (-1 / (L * (z + e))) := hm
    _ ≤ _ := by linarith

end
end MultilinearGap
