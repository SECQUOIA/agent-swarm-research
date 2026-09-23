import Formal.SwitchingControl.MeasurableWitness

/-! Realization of arbitrary finite simplex cell allocations by measurable rates. -/
namespace SwitchingControl.GridRates

open MeasureTheory Set MeasurableWitness

/-- Unit-cell indicators, assigning time zero to the first cell. -/
noncomputable def pulse (j : ℕ) (t : ℝ) : ℝ :=
  if j = 0 then step 1 t else step (j + 1) t - step j t

theorem pulse_measurable (j : ℕ) : _root_.Measurable (pulse j) := by
  unfold pulse
  split_ifs
  · exact step_measurable 1
  · exact (step_measurable _).sub (step_measurable _)

theorem pulse_nonnegative (j : ℕ) (t : ℝ) : 0 ≤ pulse j t := by
  unfold pulse step
  have hj : (j : ℝ) ≤ j + 1 := by linarith
  split_ifs <;> norm_num at *
  all_goals linarith

theorem pulse_sum_succ (n : ℕ) (t : ℝ) :
    ∑ j ∈ Finset.range (n + 1), pulse j t = step (n + 1) t := by
  induction n with
  | zero => simp [pulse]
  | succ n ih =>
    rw [Finset.sum_range_succ, ih]
    simp only [pulse, Nat.add_eq_zero_iff, one_ne_zero, and_false, ↓reduceIte,
      Nat.cast_add, Nat.cast_one]
    ring

theorem pulse_sum {n : ℕ} (hn : 0 < n) (t : ℝ) (ht : t ≤ n) :
    ∑ j : Fin n, pulse j.val t = 1 := by
  rw [Fin.sum_univ_eq_sum_range (fun j => pulse j t) n]
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : n ≠ 0)
  rw [pulse_sum_succ]
  exact if_pos (by simpa using ht)

/-- Per-cell simplex weights determine measurable rates constant on each cell. -/
noncomputable def rates {n : ℕ} (r : Fin n → Fin 3 → ℝ) (i : Fin 3) (t : ℝ) : ℝ :=
  ∑ j, r j i * pulse j.val t

theorem rates_valid {n : ℕ} (hn : 0 < n) (r : Fin n → Fin 3 → ℝ)
    (hr : ∀ j i, 0 ≤ r j i) (hs : ∀ j, ∑ i, r j i = 1) :
    Measurable.SimplexRates (rates r) n := by
  apply Measurable.simplexRates_of_measurable
  · intro i
    exact Finset.measurable_sum _ fun j _ => measurable_const.mul (pulse_measurable j.val)
  · intro t _ i
    exact Finset.sum_nonneg fun j _ => mul_nonneg (hr j i) (pulse_nonnegative j.val t)
  · intro t ht
    unfold rates
    rw [Finset.sum_comm]
    simp only [← Finset.sum_mul, hs, one_mul]
    exact pulse_sum hn t ht.2

theorem pulse_integrable (j : ℕ) (t : ℝ) (ht : 0 ≤ t) :
    IntervalIntegrable (pulse j) volume 0 t := by
  unfold pulse
  split_ifs
  · exact step_integrable _ _ ht
  · exact (step_integrable _ _ ht).sub (step_integrable _ _ ht)

/-- Integrated length of a cell before time `t`. -/
noncomputable def cellLength (j : ℕ) (t : ℝ) : ℝ :=
  if j = 0 then min t 1 else min t (j + 1) - min t j

theorem pulse_integral (j : ℕ) (t : ℝ) (ht : 0 ≤ t) :
    (∫ s in 0..t, pulse j s) = cellLength j t := by
  unfold pulse cellLength
  split_ifs
  · exact step_integral _ _ (by positivity) ht
  · rw [intervalIntegral.integral_sub (step_integrable _ _ ht) (step_integrable _ _ ht),
      step_integral _ _ (by positivity) ht, step_integral _ _ (by positivity) ht]

theorem cumulative_rates {n : ℕ} (r : Fin n → Fin 3 → ℝ) (i : Fin 3)
    (t : ℝ) (ht : 0 ≤ t) :
    Measurable.cumulative (rates r) i t = ∑ j, r j i * cellLength j.val t := by
  unfold Measurable.cumulative rates
  rw [intervalIntegral.integral_finsetSum (fun j _ => (pulse_integrable j.val t ht).const_mul _)]
  apply Finset.sum_congr rfl
  intro j _
  rw [intervalIntegral.integral_const_mul, pulse_integral j.val t ht]

end SwitchingControl.GridRates
