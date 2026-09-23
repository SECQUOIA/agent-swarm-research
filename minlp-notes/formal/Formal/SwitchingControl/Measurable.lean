import Formal.SwitchingControl.Continuous

/-!
# Measurable relaxed controls and their cumulative allocations

Measurability is required only with respect to Lebesgue measure restricted to
`[0,T]`. Nonnegative rates summing to one are automatically integrable. Their
interval integrals satisfy precisely the cumulative assumptions used by the
continuous switching argument.
-/
namespace SwitchingControl.Measurable

open MeasureTheory Set

/-- A measurable simplex-valued control on the specified horizon. -/
structure SimplexRates (α : Fin 3 → ℝ → ℝ) (T : ℝ) : Prop where
  measurable : ∀ i, AEStronglyMeasurable (α i) (volume.restrict (Icc 0 T))
  nonnegative : ∀ t ∈ Icc 0 T, ∀ i, 0 ≤ α i t
  conservation : ∀ t ∈ Icc 0 T, ∑ i, α i t = 1

/-- Integrated occupation of a relaxed control. -/
noncomputable def cumulative (α : Fin 3 → ℝ → ℝ) (i : Fin 3) (t : ℝ) : ℝ :=
  ∫ s in 0..t, α i s

/-- The simplex conditions give a coordinatewise bound of one. -/
theorem rate_le_one {α : Fin 3 → ℝ → ℝ} {T : ℝ} (hα : SimplexRates α T)
    {t : ℝ} (ht : t ∈ Icc 0 T) (i : Fin 3) : α i t ≤ 1 := by
  calc
    α i t ≤ ∑ j, α j t := Finset.single_le_sum (fun j _ => hα.nonnegative t ht j)
      (Finset.mem_univ i)
    _ = 1 := hα.conservation t ht

/-- Bounded measurable simplex rates need no separate integrability assumption. -/
theorem rates_integrable {α : Fin 3 → ℝ → ℝ} {T : ℝ} (hα : SimplexRates α T)
    (i : Fin 3) : IntegrableOn (α i) (Icc 0 T) := by
  have hc : IntegrableOn (fun _ : ℝ => (1 : ℝ)) (Icc 0 T) :=
    integrableOn_const isCompact_Icc.measure_ne_top
  apply hc.mono' (hα.measurable i)
  apply (ae_restrict_iff' measurableSet_Icc).mpr
  exact Filter.Eventually.of_forall fun t ht => by
    simpa [Real.norm_eq_abs, abs_of_nonneg (hα.nonnegative t ht i)] using
      rate_le_one hα ht i

/-- Integrability on every subinterval of the control horizon. -/
theorem rates_intervalIntegrable {α : Fin 3 → ℝ → ℝ} {T s t : ℝ}
    (hα : SimplexRates α T) (hs : 0 ≤ s) (hst : s ≤ t) (ht : t ≤ T)
    (i : Fin 3) : IntervalIntegrable (α i) volume s t := by
  apply (intervalIntegrable_iff_integrableOn_Icc_of_le hst).mpr
  exact (rates_integrable hα i).mono_set (Icc_subset_Icc hs ht)

@[simp] theorem cumulative_initial (α : Fin 3 → ℝ → ℝ) (i : Fin 3) :
    cumulative α i 0 = 0 := by simp [cumulative]

/-- The integrated coordinate increases by between zero and elapsed time. -/
theorem cumulative_increments {α : Fin 3 → ℝ → ℝ} {T : ℝ} (hα : SimplexRates α T)
    (i : Fin 3) : Continuous.UnitIncrements (cumulative α i) T := by
  intro s t hs hst ht
  have hit := rates_intervalIntegrable hα (le_refl 0) (hs.trans hst) ht i
  have his := rates_intervalIntegrable hα (le_refl 0) hs (hst.trans ht) i
  have hist := rates_intervalIntegrable hα hs hst ht i
  rw [cumulative, cumulative, intervalIntegral.integral_interval_sub_left hit his]
  constructor
  · exact intervalIntegral.integral_nonneg hst fun x hx =>
      hα.nonnegative x ⟨hs.trans hx.1, hx.2.trans ht⟩ i
  · have hle := intervalIntegral.integral_mono_on hst hist
      (intervalIntegrable_const (c := (1 : ℝ)))
      (fun x hx => rate_le_one hα ⟨hs.trans hx.1, hx.2.trans ht⟩ i)
    simpa using hle

/-- Cumulative mode allocations sum to elapsed time. -/
theorem cumulative_conservation {α : Fin 3 → ℝ → ℝ} {T t : ℝ}
    (hα : SimplexRates α T) (ht : t ∈ Icc 0 T) :
    ∑ i, cumulative α i t = t := by
  unfold cumulative
  rw [← intervalIntegral.integral_finsetSum
    (fun i _ => rates_intervalIntegrable hα (le_refl 0) ht.1 ht.2 i)]
  calc
    (∫ s in 0..t, ∑ i, α i s) = ∫ _s in 0..t, (1 : ℝ) := by
      apply intervalIntegral.integral_congr
      intro s hs
      rw [uIcc_of_le ht.1] at hs
      exact hα.conservation s ⟨hs.1, hs.2.trans ht.2⟩
    _ = t := by simp

/-- Ordinary measurable rates are a special case of the restricted-measure
hypothesis; all rate bounds are required only on the control horizon. -/
theorem simplexRates_of_measurable {α : Fin 3 → ℝ → ℝ} {T : ℝ}
    (hm : ∀ i, _root_.Measurable (α i))
    (hn : ∀ t ∈ Icc 0 T, ∀ i, 0 ≤ α i t)
    (hs : ∀ t ∈ Icc 0 T, ∑ i, α i t = 1) : SimplexRates α T :=
  ⟨fun i => (hm i).aestronglyMeasurable, hn, hs⟩

end SwitchingControl.Measurable
