import QipmFormal.FractionalSDP.Limits

/-! Transfer of the rational-parameter spectrum to barrier and gap scales. -/
namespace QipmFormal.FractionalSDP
noncomputable section
open Filter
open scoped Topology

private theorem transfer_pos : ∀ᶠ t : ℝ in nhdsWithin 0 (Set.Ioi 0), 0 < t :=
  self_mem_nhdsWithin

private theorem transfer_id : Tendsto (fun t : ℝ => t)
    (nhdsWithin 0 (Set.Ioi 0)) (𝓝 0) := tendsto_id.mono_left nhdsWithin_le_nhds

/-- Dividing a square root by the positive path parameter commutes with the limit. -/
theorem sqrt_scaled_limit {f : ℝ → ℝ} {c : ℝ}
    (h : Tendsto (fun t => f t / t ^ 2) (nhdsWithin 0 (Set.Ioi 0)) (𝓝 c)) :
    Tendsto (fun t => Real.sqrt (f t) / t)
      (nhdsWithin 0 (Set.Ioi 0)) (𝓝 (Real.sqrt c)) := by
  apply (Real.continuous_sqrt.tendsto c |>.comp h).congr'
  filter_upwards [transfer_pos] with t ht
  change Real.sqrt (f t / t ^ 2) = _
  rw [Real.sqrt_div' _ (sq_nonneg t), Real.sqrt_sq ht.le]

/-- Consecutive divergent powers with a positive larger-order coefficient are ordered. -/
theorem eventually_lt_of_scaled_limits {f h : ℝ → ℝ} {c d : ℝ} (n : ℕ)
    (hf : Tendsto (fun t => t ^ n * f t) (nhdsWithin 0 (Set.Ioi 0)) (𝓝 c))
    (hh : Tendsto (fun t => t ^ (n + 1) * h t) (nhdsWithin 0 (Set.Ioi 0)) (𝓝 d))
    (hd : 0 < d) : ∀ᶠ t in nhdsWithin 0 (Set.Ioi 0), f t < h t := by
  have hf' : Tendsto (fun t => t ^ (n + 1) * f t)
      (nhdsWithin 0 (Set.Ioi 0)) (𝓝 0) := by
    convert transfer_id.mul hf using 1 <;> simp [pow_succ, mul_comm, mul_left_comm]
  filter_upwards [hf'.eventually_lt hh hd, transfer_pos] with t hlt ht
  have hp := pow_pos ht (n + 1)
  nlinarith

private theorem sqrt_two_ninths : Real.sqrt (2 / 9 : ℝ) = Real.sqrt 2 / 3 := by
  rw [Real.sqrt_div (by norm_num : (0 : ℝ) ≤ 2)]
  norm_num

theorem limit_mu_offLow :
    Tendsto (fun t => Real.sqrt (mu t) * offLow t)
      (nhdsWithin 0 (Set.Ioi 0)) (𝓝 (Real.sqrt 2)) := by
  have h := (sqrt_scaled_limit limit_mu_scaled).mul limit_offLow
  rw [sqrt_two_ninths] at h
  have he : Real.sqrt 2 / 3 * 3 = Real.sqrt 2 := by ring
  rw [he] at h
  apply h.congr'
  filter_upwards [transfer_pos] with t ht
  field_simp

theorem limit_mu_diagLow :
    Tendsto (fun t => mu t * diagLow t)
      (nhdsWithin 0 (Set.Ioi 0)) (𝓝 1) := by
  have h := limit_mu_scaled.mul limit_diagLow
  norm_num at h
  apply h.congr'
  filter_upwards [transfer_pos] with t ht
  field_simp

theorem limit_mu_offHigh :
    Tendsto (fun t => mu t * Real.sqrt (mu t) * offHigh t)
      (nhdsWithin 0 (Set.Ioi 0)) (𝓝 (Real.sqrt 2)) := by
  have h := (limit_mu_scaled.mul (sqrt_scaled_limit limit_mu_scaled)).mul limit_offHigh
  rw [sqrt_two_ninths] at h
  have he : (2 / 9 : ℝ) * (Real.sqrt 2 / 3) * (27 / 2) = Real.sqrt 2 := by ring
  rw [he] at h
  apply h.congr'
  filter_upwards [transfer_pos] with t ht
  field_simp [ne_of_gt ht]

theorem limit_mu_diagHigh :
    Tendsto (fun t => mu t ^ 2 * diagHigh t)
      (nhdsWithin 0 (Set.Ioi 0)) (𝓝 (4 / 7 : ℝ)) := by
  have h := (limit_mu_scaled.pow 2).mul limit_diagHigh
  norm_num at h
  apply h.congr'
  filter_upwards [transfer_pos] with t ht
  field_simp [ne_of_gt ht]

theorem eventually_spectrum_ordered :
    ∀ᶠ t in nhdsWithin 0 (Set.Ioi 0),
      offLow t < diagLow t ∧ diagLow t < offHigh t ∧ offHigh t < diagHigh t := by
  have h1 := eventually_lt_of_scaled_limits 1
    (by simpa using limit_offLow) limit_diagLow (by norm_num)
  have h2 := eventually_lt_of_scaled_limits 2 limit_diagLow limit_offHigh (by norm_num)
  have h3 := eventually_lt_of_scaled_limits 3 limit_offHigh limit_diagHigh (by norm_num)
  exact h1.and (h2.and h3)

theorem limit_mu_condition :
    Tendsto (fun t => mu t * Real.sqrt (mu t) * (diagHigh t / offLow t))
      (nhdsWithin 0 (Set.Ioi 0)) (𝓝 (2 * Real.sqrt 2 / 7)) := by
  have h := ((limit_mu_scaled.mul (sqrt_scaled_limit limit_mu_scaled)).mul
    limit_diagHigh).div limit_offLow (by norm_num)
  rw [sqrt_two_ninths] at h
  have he : (2 / 9 : ℝ) * (Real.sqrt 2 / 3) * (81 / 7) / 3 =
      2 * Real.sqrt 2 / 7 := by ring
  rw [he] at h
  apply h.congr'
  filter_upwards [transfer_pos] with t ht
  dsimp only [Pi.div_apply]
  field_simp [ne_of_gt ht]

/-- The gap-normalized spectral condition number has the paper's leading constant. -/
theorem limit_gap_condition :
    Tendsto (fun t => g t * Real.sqrt (g t) * (diagHigh t / offLow t))
      (nhdsWithin 0 (Set.Ioi 0)) (𝓝 (3 * Real.sqrt 3 / 7)) := by
  have hs : Real.sqrt (1 / 3 : ℝ) = Real.sqrt 3 / 3 := by
    apply (Real.sqrt_eq_iff_eq_sq (by norm_num) (by positivity)).mpr
    have h3 := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)
    nlinarith
  have h := ((limit_g_scaled.mul (sqrt_scaled_limit limit_g_scaled)).mul
    limit_diagHigh).div limit_offLow (by norm_num)
  rw [hs] at h
  have he : (1 / 3 : ℝ) * (Real.sqrt 3 / 3) * (81 / 7) / 3 =
      3 * Real.sqrt 3 / 7 := by ring
  rw [he] at h
  apply h.congr'
  filter_upwards [transfer_pos] with t ht
  dsimp only [Pi.div_apply]
  field_simp [ne_of_gt ht]

/-- Condition number on the two-dimensional diagonal restriction, scaled by `mu`. -/
theorem limit_mu_restricted_condition :
    Tendsto (fun t => mu t * (diagHigh t / diagLow t))
      (nhdsWithin 0 (Set.Ioi 0)) (𝓝 (4 / 7 : ℝ)) := by
  have h := (limit_mu_scaled.mul limit_diagHigh).div limit_diagLow (by norm_num)
  norm_num at h
  apply h.congr'
  filter_upwards [transfer_pos] with t ht
  dsimp only [Pi.div_apply]
  field_simp [ne_of_gt ht]

/-- Condition number on the two-dimensional diagonal restriction, scaled by the gap. -/
theorem limit_gap_restricted_condition :
    Tendsto (fun t => g t * (diagHigh t / diagLow t))
      (nhdsWithin 0 (Set.Ioi 0)) (𝓝 (6 / 7 : ℝ)) := by
  have h := (limit_g_scaled.mul limit_diagHigh).div limit_diagLow (by norm_num)
  norm_num at h
  apply h.congr'
  filter_upwards [transfer_pos] with t ht
  dsimp only [Pi.div_apply]
  field_simp [ne_of_gt ht]

end
end QipmFormal.FractionalSDP
