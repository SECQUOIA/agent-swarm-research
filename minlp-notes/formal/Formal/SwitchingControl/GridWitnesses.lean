import Formal.SwitchingControl.GridRates
import Formal.SwitchingControl.Sharpness

/-! Actual measurable controls realizing the three sharp endpoint profiles. -/
namespace SwitchingControl.GridWitnesses

open MeasureTheory Set

noncomputable def fiveWeights : Fin 5 → Fin 3 → ℝ :=
  ![![1,0,0], ![0,1,0], ![1,0,0], ![0,1,0], ![1,0,0]]

noncomputable def sixWeights : Fin 6 → Fin 3 → ℝ :=
  ![![1,0,0], ![0,1,0], ![1,0,0], ![0,1,0], ![1,0,0], ![0,1,0]]

noncomputable def sevenWeights : Fin 7 → Fin 3 → ℝ :=
  ![![1/3,1/3,1/3], ![1,0,0], ![0,1,0], ![0,0,1], ![1,0,0],
    ![1/3,1/3,1/3], ![0,0,1]]

theorem fiveWeights_nonnegative : ∀ j i, 0 ≤ fiveWeights j i := by
  intro j i
  fin_cases j <;> fin_cases i <;> norm_num [fiveWeights]

theorem sixWeights_nonnegative : ∀ j i, 0 ≤ sixWeights j i := by
  intro j i
  fin_cases j <;> fin_cases i <;> norm_num [sixWeights]

theorem sevenWeights_nonnegative : ∀ j i, 0 ≤ sevenWeights j i := by
  intro j i
  fin_cases j <;> fin_cases i <;> norm_num [sevenWeights]

theorem fiveWeights_sum : ∀ j, ∑ i, fiveWeights j i = 1 := by
  intro j
  fin_cases j <;> norm_num [fiveWeights, Fin.sum_univ_succ]

theorem sixWeights_sum : ∀ j, ∑ i, sixWeights j i = 1 := by
  intro j
  fin_cases j <;> norm_num [sixWeights, Fin.sum_univ_succ]

theorem sevenWeights_sum : ∀ j, ∑ i, sevenWeights j i = 1 := by
  intro j
  fin_cases j <;> norm_num [sevenWeights, Fin.sum_univ_succ]

theorem five_endpoints (j : Fin 5) (i : Fin 3) :
    Measurable.cumulative (GridRates.rates fiveWeights) i (j.val + 1) =
      fiveSharpProfile j i := by
  rw [GridRates.cumulative_rates _ _ _ (by positivity)]
  fin_cases j <;> fin_cases i <;>
    norm_num [fiveWeights, fiveSharpProfile, GridRates.cellLength, Fin.sum_univ_succ]

theorem six_endpoints (j : Fin 6) (i : Fin 3) :
    Measurable.cumulative (GridRates.rates sixWeights) i (j.val + 1) =
      sixSharpProfile j i := by
  rw [GridRates.cumulative_rates _ _ _ (by positivity)]
  fin_cases j <;> fin_cases i <;>
    norm_num [sixWeights, sixSharpProfile, GridRates.cellLength, Fin.sum_univ_succ]

theorem seven_endpoints (j : Fin 7) (i : Fin 3) :
    Measurable.cumulative (GridRates.rates sevenWeights) i (j.val + 1) =
      sevenSharpProfile j i := by
  rw [GridRates.cumulative_rates _ _ _ (by positivity)]
  fin_cases j <;> fin_cases i <;>
    norm_num [sevenWeights, sevenSharpProfile, SevenWitness.target,
      GridRates.cellLength, Fin.sum_univ_succ]

/-- Rescaling cells from width one to width `d`. -/
noncomputable def dilated {n : ℕ} (r : Fin n → Fin 3 → ℝ)
    (d : ℝ) (i : Fin 3) (t : ℝ) : ℝ := GridRates.rates r i (t / d)

theorem dilated_valid {n : ℕ} (hn : 0 < n) (r : Fin n → Fin 3 → ℝ)
    (hr : ∀ j i, 0 ≤ r j i) (hs : ∀ j, ∑ i, r j i = 1)
    {d : ℝ} (hd : 0 < d) : Measurable.SimplexRates (dilated r d) (n * d) := by
  have hb := GridRates.rates_valid hn r hr hs
  apply Measurable.simplexRates_of_measurable
  · intro i
    have hm : _root_.Measurable (GridRates.rates r i) :=
      Finset.measurable_sum _ fun j _ =>
        measurable_const.mul (GridRates.pulse_measurable j.val)
    exact hm.comp (measurable_id.div_const d)
  · intro t ht i
    apply hb.nonnegative (t / d) _ i
    exact ⟨div_nonneg ht.1 hd.le, (div_le_iff₀ hd).mpr ht.2⟩
  · intro t ht
    apply hb.conservation (t / d)
    exact ⟨div_nonneg ht.1 hd.le, (div_le_iff₀ hd).mpr ht.2⟩

theorem cumulative_dilated {n : ℕ} (r : Fin n → Fin 3 → ℝ)
    {d : ℝ} (hd : 0 < d) (i : Fin 3) (t : ℝ) :
    Measurable.cumulative (dilated r d) i (d * t) =
      d * Measurable.cumulative (GridRates.rates r) i t := by
  unfold Measurable.cumulative dilated
  rw [intervalIntegral.integral_comp_div _ hd.ne']
  simp [hd.ne']

/-- The alternating five-cell witness is measurable at every positive cell width. -/
theorem five_realization {d : ℝ} (hd : 0 < d) :
    ∃ α : Fin 3 → ℝ → ℝ, Measurable.SimplexRates α (5 * d) ∧
      ∀ j : Fin 5, ∀ i : Fin 3,
        Measurable.cumulative α i (d * (j.val + 1)) = d * fiveSharpProfile j i := by
  refine ⟨dilated fiveWeights d,
    dilated_valid (by decide) fiveWeights fiveWeights_nonnegative fiveWeights_sum hd, ?_⟩
  intro j i
  rw [cumulative_dilated _ hd, five_endpoints]

/-- The alternating six-cell witness is measurable at every positive cell width. -/
theorem six_realization {d : ℝ} (hd : 0 < d) :
    ∃ α : Fin 3 → ℝ → ℝ, Measurable.SimplexRates α (6 * d) ∧
      ∀ j : Fin 6, ∀ i : Fin 3,
        Measurable.cumulative α i (d * (j.val + 1)) = d * sixSharpProfile j i := by
  refine ⟨dilated sixWeights d,
    dilated_valid (by decide) sixWeights sixWeights_nonnegative sixWeights_sum hd, ?_⟩
  intro j i
  rw [cumulative_dilated _ hd, six_endpoints]

/-- The rational seven-cell witness is measurable at every positive cell width. -/
theorem seven_realization {d : ℝ} (hd : 0 < d) :
    ∃ α : Fin 3 → ℝ → ℝ, Measurable.SimplexRates α (7 * d) ∧
      ∀ j : Fin 7, ∀ i : Fin 3,
        Measurable.cumulative α i (d * (j.val + 1)) = d * sevenSharpProfile j i := by
  refine ⟨dilated sevenWeights d,
    dilated_valid (by decide) sevenWeights sevenWeights_nonnegative sevenWeights_sum hd, ?_⟩
  intro j i
  rw [cumulative_dilated _ hd, seven_endpoints]

end SwitchingControl.GridWitnesses
