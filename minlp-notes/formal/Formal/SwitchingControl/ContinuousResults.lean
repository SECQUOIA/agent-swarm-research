import Formal.SwitchingControl.Results
import Formal.SwitchingControl.ContinuousGrid
import Formal.SwitchingControl.MeasurableWitness

/-! The sharp continuous three-mode, two-switch theorem. -/
namespace SwitchingControl.ContinuousResults

open SwitchingControl.Continuous SwitchingControl.ContinuousGrid

/-- Every valid cumulative input has a two-switch schedule of error at most
one fifth of its horizon. -/
theorem two_switch_upper {T : ℝ} (hT : 0 < T) {A : Fin 3 → ℝ → ℝ}
    (hA : ValidCumulative A T) :
    ∃ p q r : Fin 3, ∃ u v : ℝ, 0 ≤ u ∧ u ≤ v ∧ v ≤ T ∧
      ∀ i : Fin 3, ∀ t ∈ Set.Icc (0 : ℝ) T,
        |A i t - occupation p q r i u v t| ≤ T / 5 := by
  have hd : 0 < T / 5 := by positivity
  have hh : 5 * (T / 5) = T := by ring
  have hgrid : FiveGridUpper 1 := five_cells
  have he := scaled_continuous_upper_of_five_grid (by norm_num : (0 : ℝ) ≤ 1)
    hd hgrid (by simpa only [hh] using hA)
  simpa only [hh, mul_one] using he

/-- The upper bound applies directly to measurable simplex-valued controls;
no separate integrability or cumulative assumptions are imposed. -/
theorem measurable_two_switch_upper {T : ℝ} (hT : 0 < T)
    {α : Fin 3 → ℝ → ℝ} (hα : Measurable.SimplexRates α T) :
    ∃ p q r : Fin 3, ∃ u v : ℝ, 0 ≤ u ∧ u ≤ v ∧ v ≤ T ∧
      ∀ i : Fin 3, ∀ t ∈ Set.Icc (0 : ℝ) T,
        |Measurable.cumulative α i t - occupation p q r i u v t| ≤ T / 5 :=
  two_switch_upper hT (measurable_valid hα)

/-- The bound is attained in the worst case: the time-dilated `01201` witness
forces error at least one fifth of the horizon for every two-switch schedule. -/
theorem two_switch_lower {T : ℝ} (hT : 0 < T) :
    ∃ A : Fin 3 → ℝ → ℝ, ValidCumulative A T ∧
      ∀ p q r : Fin 3, ∀ u v : ℝ, 0 ≤ u → u ≤ v → v ≤ T →
        ∃ i : Fin 3, ∃ t ∈ Set.Icc (0 : ℝ) T,
          T / 5 ≤ |A i t - occupation p q r i u v t| := by
  have hd : 0 < T / 5 := by positivity
  have hh : 5 * (T / 5) = T := by ring
  refine ⟨fun i t => (T / 5) * witness i (t / (T / 5)),
    by simpa only [hh] using dilate_valid hd witness_valid, ?_⟩
  intro p q r u v hu huv hv
  simpa only [hh] using scaled_three_block_lower_bound (T / 5) hd p q r u v hu huv
    (by simpa only [hh] using hv)

/-- Exact minimax characterization `F₃,₂(T)=T/5`: a uniform achievable bound
and a valid input forcing that same bound against every competing schedule. -/
theorem continuous_three_mode_two_switch_minimax {T : ℝ} (hT : 0 < T) :
    (∀ A : Fin 3 → ℝ → ℝ, ValidCumulative A T →
      ∃ p q r : Fin 3, ∃ u v : ℝ, 0 ≤ u ∧ u ≤ v ∧ v ≤ T ∧
        ∀ i : Fin 3, ∀ t ∈ Set.Icc (0 : ℝ) T,
          |A i t - occupation p q r i u v t| ≤ T / 5) ∧
    (∃ A : Fin 3 → ℝ → ℝ, ValidCumulative A T ∧
      ∀ p q r : Fin 3, ∀ u v : ℝ, 0 ≤ u → u ≤ v → v ≤ T →
        ∃ i : Fin 3, ∃ t ∈ Set.Icc (0 : ℝ) T,
          T / 5 ≤ |A i t - occupation p q r i u v t|) :=
  ⟨fun _ hA => two_switch_upper hT hA, two_switch_lower hT⟩

/-- The sharp lower input is itself a measurable simplex-valued control,
whose cumulative allocation is verified by interval integration. -/
theorem measurable_two_switch_lower {T : ℝ} (hT : 0 < T) :
    ∃ α : Fin 3 → ℝ → ℝ, Measurable.SimplexRates α T ∧
      ∀ p q r : Fin 3, ∀ u v : ℝ, 0 ≤ u → u ≤ v → v ≤ T →
        ∃ i : Fin 3, ∃ t ∈ Set.Icc (0 : ℝ) T,
          T / 5 ≤ |Measurable.cumulative α i t - occupation p q r i u v t| := by
  have hd : 0 < T / 5 := by positivity
  have hh : 5 * (T / 5) = T := by ring
  refine ⟨MeasurableWitness.dilatedRates (T / 5),
    MeasurableWitness.dilatedRates_valid _ _, ?_⟩
  intro p q r u v hu huv hv
  obtain ⟨i, t, ht, he⟩ := scaled_three_block_lower_bound (T / 5) hd p q r u v hu huv
    (by simpa only [hh] using hv)
  refine ⟨i, t, by simpa only [hh] using ht, ?_⟩
  rw [MeasurableWitness.cumulative_dilatedRates _ hd i t ht.1]
  exact he

/-- The sharp minimax statement directly for measurable relaxed controls:
every input admits error `T/5`, and one input forces that error. -/
theorem measurable_three_mode_two_switch_minimax {T : ℝ} (hT : 0 < T) :
    (∀ α : Fin 3 → ℝ → ℝ, Measurable.SimplexRates α T →
      ∃ p q r : Fin 3, ∃ u v : ℝ, 0 ≤ u ∧ u ≤ v ∧ v ≤ T ∧
        ∀ i : Fin 3, ∀ t ∈ Set.Icc (0 : ℝ) T,
          |Measurable.cumulative α i t - occupation p q r i u v t| ≤ T / 5) ∧
    (∃ α : Fin 3 → ℝ → ℝ, Measurable.SimplexRates α T ∧
      ∀ p q r : Fin 3, ∀ u v : ℝ, 0 ≤ u → u ≤ v → v ≤ T →
        ∃ i : Fin 3, ∃ t ∈ Set.Icc (0 : ℝ) T,
          T / 5 ≤ |Measurable.cumulative α i t - occupation p q r i u v t|) :=
  ⟨fun _ hα => measurable_two_switch_upper hT hα, measurable_two_switch_lower hT⟩

end SwitchingControl.ContinuousResults
