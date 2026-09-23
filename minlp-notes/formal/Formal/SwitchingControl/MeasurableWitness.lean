import Formal.SwitchingControl.Measurable

/-! The pure `01201` lower witness as an actual measurable relaxed control. -/
namespace SwitchingControl.MeasurableWitness

open MeasureTheory Set

/-- Indicator of the initial segment ending at `c`. -/
noncomputable def step (c t : ℝ) : ℝ := if t ≤ c then 1 else 0

/-- Rates for the five consecutive pure unit phases `01201`. -/
noncomputable def rates (i : Fin 3) (t : ℝ) : ℝ :=
  if i = 0 then step 1 t + step 4 t - step 3 t
  else if i = 1 then step 2 t - step 1 t + 1 - step 4 t
  else step 3 t - step 2 t

theorem step_measurable (c : ℝ) : _root_.Measurable (step c) := by
  exact measurable_const.ite measurableSet_Iic measurable_const

theorem rates_measurable (i : Fin 3) : _root_.Measurable (rates i) := by
  unfold rates
  split_ifs
  · exact ((step_measurable 1).add (step_measurable 4)).sub (step_measurable 3)
  · exact (((step_measurable 2).sub (step_measurable 1)).add measurable_const).sub
      (step_measurable 4)
  · exact (step_measurable 3).sub (step_measurable 2)

theorem rates_nonnegative (t : ℝ) (i : Fin 3) : 0 ≤ rates i t := by
  fin_cases i <;> simp only [rates] <;>
    unfold step <;> split_ifs <;> norm_num at * <;> linarith

theorem rates_sum (t : ℝ) : ∑ i, rates i t = 1 := by
  simp [rates, Fin.sum_univ_succ]
  ring

theorem rates_valid (T : ℝ) : Measurable.SimplexRates rates T :=
  Measurable.simplexRates_of_measurable rates_measurable
    (fun t _ i => rates_nonnegative t i) (fun t _ => rates_sum t)

theorem step_integrable (c t : ℝ) (ht : 0 ≤ t) :
    IntervalIntegrable (step c) volume 0 t := by
  apply (intervalIntegrable_iff_integrableOn_Icc_of_le ht).mpr
  have hc : IntegrableOn (fun _ : ℝ => (1 : ℝ)) (Icc 0 t) :=
    integrableOn_const isCompact_Icc.measure_ne_top
  apply hc.mono' (step_measurable c).aestronglyMeasurable
  exact Filter.Eventually.of_forall fun x => by
    unfold step
    split_ifs <;> norm_num

theorem step_integral (c t : ℝ) (hc : 0 ≤ c) (ht : 0 ≤ t) :
    (∫ s in 0..t, step c s) = min t c := by
  by_cases hct : c ≤ t
  · have he : step c = ({x : ℝ | x ≤ c}.indicator (fun _ => (1 : ℝ))) := by
      funext x
      simp [step, Set.indicator_apply]
    rw [he, intervalIntegral.integral_indicator ⟨hc, hct⟩]
    simp [min_eq_right hct]
  · have htc : t ≤ c := (not_le.mp hct).le
    calc
      (∫ s in 0..t, step c s) = ∫ _s in 0..t, (1 : ℝ) := by
        apply intervalIntegral.integral_congr
        intro s hs
        rw [uIcc_of_le ht] at hs
        simp [step, hs.2.trans htc]
      _ = min t c := by simp [min_eq_left htc]

/-- The lower witness's cumulative formula is the integral of its pure rates. -/
theorem cumulative_rates (i : Fin 3) (t : ℝ) (ht : 0 ≤ t) :
    Measurable.cumulative rates i t = Continuous.witness i t := by
  have h1 := step_integrable 1 t ht
  have h2 := step_integrable 2 t ht
  have h3 := step_integrable 3 t ht
  have h4 := step_integrable 4 t ht
  have hc : IntervalIntegrable (fun _ : ℝ => (1 : ℝ)) volume 0 t :=
    intervalIntegrable_const
  fin_cases i
  · change (∫ s in 0..t, step 1 s + step 4 s - step 3 s) =
      min t 1 + min t 4 - min t 3
    rw [intervalIntegral.integral_sub (h1.add h4) h3,
      intervalIntegral.integral_add h1 h4,
      step_integral 1 t (by norm_num) ht, step_integral 4 t (by norm_num) ht,
      step_integral 3 t (by norm_num) ht]
  · change (∫ s in 0..t, step 2 s - step 1 s + 1 - step 4 s) =
      min t 2 - min t 1 + t - min t 4
    rw [intervalIntegral.integral_sub ((h2.sub h1).add hc) h4,
      intervalIntegral.integral_add (h2.sub h1) hc,
      intervalIntegral.integral_sub h2 h1,
      step_integral 2 t (by norm_num) ht, step_integral 1 t (by norm_num) ht,
      step_integral 4 t (by norm_num) ht]
    simp
  · change (∫ s in 0..t, step 3 s - step 2 s) = min t 3 - min t 2
    rw [intervalIntegral.integral_sub h3 h2,
      step_integral 3 t (by norm_num) ht, step_integral 2 t (by norm_num) ht]

/-- Time dilation of the pure witness. -/
noncomputable def dilatedRates (d : ℝ) (i : Fin 3) (t : ℝ) : ℝ := rates i (t / d)

theorem dilatedRates_valid (d T : ℝ) : Measurable.SimplexRates (dilatedRates d) T := by
  apply Measurable.simplexRates_of_measurable
  · intro i
    exact (rates_measurable i).comp (measurable_id.div_const d)
  · intro t _ i
    exact rates_nonnegative (t / d) i
  · intro t _
    exact rates_sum (t / d)

/-- The dilated cumulative witness agrees with the integral on its horizon. -/
theorem cumulative_dilatedRates (d : ℝ) (hd : 0 < d) (i : Fin 3) (t : ℝ)
    (ht : 0 ≤ t) :
    Measurable.cumulative (dilatedRates d) i t = d * Continuous.witness i (t / d) := by
  unfold Measurable.cumulative dilatedRates
  rw [intervalIntegral.integral_comp_div (rates i) hd.ne']
  simp only [zero_div, smul_eq_mul]
  exact congrArg (fun x => d * x) (cumulative_rates i (t / d) (div_nonneg ht hd.le))

end SwitchingControl.MeasurableWitness
