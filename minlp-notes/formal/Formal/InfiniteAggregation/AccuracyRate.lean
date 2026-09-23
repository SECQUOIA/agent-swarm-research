import Formal.InfiniteAggregation.AccuracyConstants

/-! Rate and tolerance consequences of the explicit accuracy bounds. -/

noncomputable section
open Filter Asymptotics

namespace InfiniteAggregation

/-- Two explicit uniform bounds imply the usual asymptotic Theta statement. -/
theorem inverse_square_theta {f : ℕ → ℝ}
    (hlower : ∀ N, 2 ≤ N → accuracyLowerBound N ≤ f N)
    (hupper : ∀ N, 2 ≤ N → f N ≤ accuracyUpperBound N) :
    f =Θ[atTop] (fun N : ℕ => (1 : ℝ) / (N : ℝ) ^ 2) := by
  let c : ℝ := Real.sqrt 2 * (Real.log 2) ^ 2 / 1600
  let C : ℝ := 5 * Real.sqrt 2 * Real.pi ^ 2 / 4
  have hc : 0 < c := by
    dsimp [c]
    have hl : 0 < Real.log 2 := Real.log_pos (by norm_num)
    positivity
  constructor
  · apply IsBigO.of_bound C
    filter_upwards [eventually_ge_atTop 2] with N hN
    have hn : 0 ≤ f N := (accuracyLowerBound_pos (by omega : 0 < N)).le.trans
      (hlower N hN)
    rw [Real.norm_eq_abs, abs_of_nonneg hn, Real.norm_eq_abs,
      abs_of_nonneg (by positivity : 0 ≤ (1 : ℝ) / (N : ℝ) ^ 2)]
    have hu := (hupper N hN).trans (accuracyUpperBound_le_inverse_square hN)
    simpa [C, div_eq_mul_inv] using hu
  · apply IsBigO.of_bound c⁻¹
    filter_upwards [eventually_ge_atTop 2] with N hN
    have hn : 0 ≤ f N := (accuracyLowerBound_pos (by omega : 0 < N)).le.trans
      (hlower N hN)
    rw [Real.norm_eq_abs, abs_of_nonneg (by positivity : 0 ≤ (1 : ℝ) / (N : ℝ) ^ 2),
      Real.norm_eq_abs, abs_of_nonneg hn]
    have h := mul_le_mul_of_nonneg_left (hlower N hN) (inv_nonneg.mpr hc.le)
    have heq : c⁻¹ * accuracyLowerBound N = (1 : ℝ) / (N : ℝ) ^ 2 := by
      change c⁻¹ * (Real.sqrt 2 * (Real.log 2) ^ 2 / (1600 * (N : ℝ) ^ 2)) = _
      have hform : Real.sqrt 2 * (Real.log 2) ^ 2 / (1600 * (N : ℝ) ^ 2) =
          c * ((1 : ℝ) / (N : ℝ) ^ 2) := by dsimp [c]; ring
      rw [hform, ← mul_assoc, inv_mul_cancel₀ (ne_of_gt hc), one_mul]
    rwa [heq] at h

/-- A sufficient cut budget obtained by inverting the explicit upper bound. -/
def accuracyBudget (ε : ℝ) : ℕ :=
  Nat.ceil (Real.sqrt ((5 * Real.sqrt 2 * Real.pi ^ 2 / 16) / ε)) + 1

theorem accuracyBudget_ge_two {ε : ℝ} (hε : 0 < ε) : 2 ≤ accuracyBudget ε := by
  have hp : 0 < Real.sqrt ((5 * Real.sqrt 2 * Real.pi ^ 2 / 16) / ε) := by positivity
  have := Nat.ceil_pos.2 hp
  unfold accuracyBudget
  omega

theorem accuracyBudget_upper {ε : ℝ} (hε : 0 < ε) :
    accuracyUpperBound (accuracyBudget ε) ≤ ε := by
  let K : ℝ := 5 * Real.sqrt 2 * Real.pi ^ 2 / 16
  have hK : 0 < K := by dsimp [K]; positivity
  have hs2 : Real.sqrt (K / ε) ^ 2 = K / ε := Real.sq_sqrt (by positivity)
  have hc := Nat.le_ceil (Real.sqrt (K / ε))
  have hn : (accuracyBudget ε : ℝ) - 1 = (Nat.ceil (Real.sqrt (K / ε)) : ℝ) := by
    simp [accuracyBudget, K]
  have hnp : 0 < (accuracyBudget ε : ℝ) - 1 := by
    have hp := accuracyBudget_ge_two hε
    have hp' : (2 : ℝ) ≤ accuracyBudget ε := by exact_mod_cast hp
    linarith
  have hsq : K / ε ≤ ((accuracyBudget ε : ℝ) - 1) ^ 2 := by
    rw [hn]
    nlinarith [Real.sqrt_nonneg (K / ε)]
  have ht := (div_le_iff₀ hε).1 hsq
  unfold accuracyUpperBound
  apply (div_le_iff₀ (by positivity)).2
  dsimp [K] at ht
  nlinarith

theorem accuracyBudget_size (ε : ℝ) :
    (accuracyBudget ε : ℝ) <
      Real.sqrt ((5 * Real.sqrt 2 * Real.pi ^ 2 / 16) / ε) + 2 := by
  have h := Nat.ceil_lt_add_one
    (Real.sqrt_nonneg ((5 * Real.sqrt 2 * Real.pi ^ 2 / 16) / ε))
  unfold accuracyBudget
  push_cast
  linarith

/-- Any family meeting a tolerance must respect the lower-bound budget. -/
theorem accuracyLowerBound_budget {N : ℕ} (hN : 0 < N) {ε : ℝ} (hε : 0 < ε)
    (h : accuracyLowerBound N ≤ ε) :
    Real.sqrt ((Real.sqrt 2 * (Real.log 2) ^ 2 / 1600) / ε) ≤ N := by
  have hn : 0 < (N : ℝ) := Nat.cast_pos.2 hN
  have hk : 0 ≤ (Real.sqrt 2 * (Real.log 2) ^ 2 / 1600) / ε := by positivity
  have hs := Real.sq_sqrt hk
  have ht := (div_le_iff₀ (show 0 < 1600 * (N : ℝ) ^ 2 by positivity)).1 h
  have hd : (Real.sqrt 2 * (Real.log 2) ^ 2 / 1600) / ε ≤ (N : ℝ) ^ 2 := by
    apply (div_le_iff₀ hε).2
    nlinarith
  nlinarith [Real.sqrt_nonneg ((Real.sqrt 2 * (Real.log 2) ^ 2 / 1600) / ε)]

end InfiniteAggregation
