import Formal.SwitchingControl.GridContinuous
import Formal.SwitchingControl.GridWitnesses

/-! Exact grid minimax values for measurable inputs at every positive cell width. -/
namespace SwitchingControl

open GridContinuous

/-- The full-time measurable-input minimax contract. Every time in every cell
is bounded above; a valid measurable input forces the same lower bound against
every word within the switch budget. `E` is the error in units of cell width. -/
def ExactMeasurableGridValue (n budget : ℕ) (E Δ : ℝ) : Prop :=
  (∀ α : Fin 3 → ℝ → ℝ, Measurable.SimplexRates α (n * Δ) →
    ∃ w : Finite.Word, w.length = n ∧ Finite.switches w ≤ budget ∧
      ∀ j : Fin w.length, ∀ i : Fin 3,
        ∀ t ∈ Set.Icc (Δ * j.val) (Δ * (j.val + 1)),
          |Measurable.cumulative α i t - scaledCellOccupation w j i Δ t| ≤ Δ * E) ∧
  (∃ α : Fin 3 → ℝ → ℝ, Measurable.SimplexRates α (n * Δ) ∧
    ∀ w : Finite.Word, w.length = n → Finite.switches w ≤ budget →
      ∃ j : Fin w.length, ∃ i : Fin 3,
        ∃ t ∈ Set.Icc (Δ * j.val) (Δ * (j.val + 1)),
          Δ * E ≤ |Measurable.cumulative α i t - scaledCellOccupation w j i Δ t|)

/-- Lift an endpoint theorem and a realized sharpness profile to the complete
measurable-input grid minimax statement. -/
theorem measurable_grid_of_realized_witness {n budget : ℕ} {E Δ : ℝ}
    (hE : 0 ≤ E) (hΔ : 0 < Δ)
    (hupper : ∀ A : Profile n, ValidProfile A → HasSchedule A budget E)
    (A : Profile n)
    (hlower : ∀ w : Finite.Word, w.length = n → Finite.switches w ≤ budget →
      ∃ j : Fin n, ∃ i : Fin 3,
        E ≤ |A j i - (Finite.countPrefix w (j.val + 1) i : ℝ)|)
    (hreal : ∃ α : Fin 3 → ℝ → ℝ, Measurable.SimplexRates α (n * Δ) ∧
      ∀ j : Fin n, ∀ i : Fin 3,
        Measurable.cumulative α i (Δ * (j.val + 1)) = Δ * A j i) :
    ExactMeasurableGridValue n budget E Δ := by
  constructor
  · exact fun α hα => scaled_measurable_grid_upper_of_endpoint hE hΔ hupper α hα
  · obtain ⟨α, hα, hr⟩ := hreal
    refine ⟨α, hα, ?_⟩
    intro w hw hsw
    obtain ⟨j, i, he⟩ := hlower w hw hsw
    let k : Fin w.length := ⟨j.val, by rw [hw]; exact j.isLt⟩
    refine ⟨k, i, Δ * (k.val + 1), ⟨by dsimp [k]; nlinarith, le_rfl⟩, ?_⟩
    rw [scaledCellOccupation_right w k i hΔ]
    change Δ * E ≤ |Measurable.cumulative α i (Δ * (j.val + 1)) -
      Δ * (Finite.countPrefix w (j.val + 1) i : ℝ)|
    rw [hr j i, ← mul_sub, abs_mul, abs_of_pos hΔ]
    exact mul_le_mul_of_nonneg_left he hΔ.le

/-- Five equal cells, two switches: exact worst-case full-time error `Δ`. -/
theorem five_measurable_grid_exact (Δ : ℝ) (hΔ : 0 < Δ) :
    ExactMeasurableGridValue 5 2 1 Δ :=
  measurable_grid_of_realized_witness (by norm_num) hΔ five_cells
    fiveSharpProfile five_profile_lower (GridWitnesses.five_realization hΔ)

/-- Six equal cells, three switches: exact worst-case full-time error `Δ`. -/
theorem six_measurable_grid_exact (Δ : ℝ) (hΔ : 0 < Δ) :
    ExactMeasurableGridValue 6 3 1 Δ :=
  measurable_grid_of_realized_witness (by norm_num) hΔ six_cells
    sixSharpProfile six_profile_lower (GridWitnesses.six_realization hΔ)

/-- Seven equal cells, three switches: exact worst-case full-time error `4Δ/3`. -/
theorem seven_measurable_grid_exact (Δ : ℝ) (hΔ : 0 < Δ) :
    ExactMeasurableGridValue 7 3 (4 / 3) Δ :=
  measurable_grid_of_realized_witness (by norm_num) hΔ seven_cells
    sevenSharpProfile seven_profile_lower (GridWitnesses.seven_realization hΔ)

end SwitchingControl
