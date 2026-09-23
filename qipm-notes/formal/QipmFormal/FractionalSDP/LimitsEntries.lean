import QipmFormal.FractionalSDP.LimitsTransfer

/-! The central-point and coordinate-Hessian asymptotics used in the spectral proof. -/
namespace QipmFormal.FractionalSDP
noncomputable section
open Filter Topology

private theorem pos_eventually : ∀ᶠ t : ℝ in 𝓝[>] 0, 0 < t := self_mem_nhdsWithin

private theorem denom_pos {t : ℝ} (ht : 0 < t) : 0 < denom t := by
  unfold denom; positivity

private theorem q_eq {t : ℝ} (ht : 0 < t) :
    q t = t^2*(t+2)/denom t^2 := by
  unfold q a g b
  field_simp
  ring

theorem limit_a : Tendsto a (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have hc : ContinuousAt a 0 := by unfold a denom; fun_prop (disch := norm_num)
  convert hc.tendsto.mono_left nhdsWithin_le_nhds using 1
  norm_num [a, denom]

theorem limit_b_scaled : Tendsto (fun t : ℝ => b t / t) (𝓝[>] 0) (𝓝 (1/3)) := by
  apply limit_g_scaled.congr'
  filter_upwards [pos_eventually] with t ht
  unfold b g
  field_simp

theorem limit_q_scaled : Tendsto (fun t : ℝ => q t / t^2) (𝓝[>] 0) (𝓝 (2/9)) := by
  have hc : ContinuousAt (fun t : ℝ => (t+2)/denom t^2) 0 := by
    unfold denom; fun_prop (disch := norm_num)
  have h : Tendsto (fun t : ℝ => (t+2)/denom t^2) (𝓝[>] 0) (𝓝 (2/9)) := by
    convert hc.tendsto.mono_left nhdsWithin_le_nhds using 1
    norm_num [denom]
  apply h.congr'
  filter_upwards [pos_eventually] with t ht
  rw [q_eq ht]
  have := ht.ne'
  field_simp

theorem limit_k00_scaled : Tendsto (fun t : ℝ => t^2*k00 t) (𝓝[>] 0) (𝓝 27) := by
  have hc : ContinuousAt (fun t : ℝ => 2*(t+3)*denom t^2/(t+2)) 0 := by
    unfold denom; fun_prop (disch := norm_num)
  have h : Tendsto (fun t : ℝ => 2*(t+3)*denom t^2/(t+2)) (𝓝[>] 0) (𝓝 27) := by
    convert hc.tendsto.mono_left nhdsWithin_le_nhds using 1
    norm_num [denom]
  apply h.congr'
  filter_upwards [pos_eventually] with t ht
  have hd := (denom_pos ht).ne'
  have ht' := ht.ne'
  have hp : t+2 ≠ 0 := by positivity
  unfold k00
  rw [q_eq ht]
  unfold b g
  field_simp
  ring

theorem limit_k01_scaled : Tendsto (fun t : ℝ => t^3*k01 t) (𝓝[>] 0) (𝓝 (-27/2)) := by
  have hc : ContinuousAt (fun t : ℝ => (t^2-3)*denom t^2/(t+2)) 0 := by
    unfold denom; fun_prop (disch := norm_num)
  have h : Tendsto (fun t : ℝ => (t^2-3)*denom t^2/(t+2)) (𝓝[>] 0) (𝓝 (-27/2)) := by
    convert hc.tendsto.mono_left nhdsWithin_le_nhds using 1
    norm_num [denom]
  apply h.congr'
  filter_upwards [pos_eventually] with t ht
  have hd := (denom_pos ht).ne'
  have ht' := ht.ne'
  have hp : t+2 ≠ 0 := by positivity
  unfold k01
  rw [q_eq ht]
  unfold b g
  field_simp
  unfold denom
  ring

theorem limit_k11_scaled : Tendsto (fun t : ℝ => t^4*k11 t) (𝓝[>] 0) (𝓝 (81/4)) := by
  have hc : ContinuousAt (fun t : ℝ => denom t^2*(t^4-t^2+6*t+9)/(t+2)^2) 0 := by
    unfold denom; fun_prop (disch := norm_num)
  have h : Tendsto (fun t : ℝ => denom t^2*(t^4-t^2+6*t+9)/(t+2)^2) (𝓝[>] 0) (𝓝 (81/4)) := by
    convert hc.tendsto.mono_left nhdsWithin_le_nhds using 1
    norm_num [denom]
  apply h.congr'
  filter_upwards [pos_eventually] with t ht
  have hd := (denom_pos ht).ne'
  have ht' := ht.ne'
  have hp : t+2 ≠ 0 := by positivity
  unfold k11
  rw [q_eq ht]
  unfold b g
  field_simp
  unfold denom
  ring

/-- The off-diagonal entry requires the negative coefficient, as in the paper. -/
theorem limit_mu_k01 : Tendsto (fun t => mu t * Real.sqrt (mu t) * k01 t)
    (𝓝[>] 0) (𝓝 (-Real.sqrt 2)) := by
  have h := (limit_mu_scaled.mul (sqrt_scaled_limit limit_mu_scaled)).mul limit_k01_scaled
  have hs : Real.sqrt (2/9 : ℝ) = Real.sqrt 2 / 3 := by
    rw [Real.sqrt_div (by norm_num : (0 : ℝ) ≤ 2)]; norm_num
  rw [hs] at h
  have he : (2/9 : ℝ) * (Real.sqrt 2/3) * (-27/2) = -Real.sqrt 2 := by ring
  rw [he] at h
  apply h.congr'
  filter_upwards [pos_eventually] with t ht
  field_simp [ht.ne']

theorem limit_mu_k00 : Tendsto (fun t => mu t*k00 t) (𝓝[>] 0) (𝓝 6) := by
  have h := limit_mu_scaled.mul limit_k00_scaled
  norm_num at h
  apply h.congr'
  filter_upwards [pos_eventually] with t ht
  field_simp [ht.ne']

theorem limit_mu_k11 : Tendsto (fun t => mu t^2*k11 t) (𝓝[>] 0) (𝓝 1) := by
  have h := (limit_mu_scaled.pow 2).mul limit_k11_scaled
  norm_num at h
  apply h.congr'
  filter_upwards [pos_eventually] with t ht
  field_simp [ht.ne']

theorem limit_mu_over_gap : Tendsto (fun t => mu t / g t) (𝓝[>] 0) (𝓝 (2/3)) := by
  have h := limit_mu_scaled.div limit_g_scaled (by norm_num)
  norm_num at h
  apply h.congr'
  filter_upwards [pos_eventually] with t ht
  dsimp only [Pi.div_apply]
  field_simp [ht.ne']

theorem limit_q_over_mu : Tendsto (fun t => q t / mu t) (𝓝[>] 0) (𝓝 1) := by
  have h := limit_q_scaled.div limit_mu_scaled (by norm_num)
  norm_num at h
  apply h.congr'
  filter_upwards [pos_eventually] with t ht
  dsimp only [Pi.div_apply]
  field_simp [ht.ne']

theorem limit_q_over_gap : Tendsto (fun t => q t / g t) (𝓝[>] 0) (𝓝 (2/3)) := by
  have h := limit_q_scaled.div limit_g_scaled (by norm_num)
  norm_num at h
  apply h.congr'
  filter_upwards [pos_eventually] with t ht
  dsimp only [Pi.div_apply]
  field_simp [ht.ne']

theorem limit_b_over_sqrt_mu_half :
    Tendsto (fun t => b t / Real.sqrt (mu t / 2)) (𝓝[>] 0) (𝓝 1) := by
  have hm : Tendsto (fun t => (mu t / 2) / t^2) (𝓝[>] 0) (𝓝 (1/9)) := by
    convert limit_mu_scaled.div_const 2 using 1 <;> ring_nf
  have hs := sqrt_scaled_limit hm
  have hv : Real.sqrt (1/9 : ℝ) = 1/3 := by
    rw [Real.sqrt_div (by norm_num : (0 : ℝ) ≤ 1)]
    norm_num
  rw [hv] at hs
  have h := limit_b_scaled.div hs (by norm_num)
  norm_num at h
  apply h.congr'
  filter_upwards [pos_eventually] with t ht
  dsimp only [Pi.div_apply]
  rw [Real.sqrt_div' _ (by norm_num)]
  field_simp [ht.ne']

theorem limit_b_over_sqrt_gap_third :
    Tendsto (fun t => b t / Real.sqrt (g t / 3)) (𝓝[>] 0) (𝓝 1) := by
  have hm : Tendsto (fun t => (g t / 3) / t^2) (𝓝[>] 0) (𝓝 (1/9)) := by
    convert limit_g_scaled.div_const 3 using 1 <;> ring_nf
  have hs := sqrt_scaled_limit hm
  have hv : Real.sqrt (1/9 : ℝ) = 1/3 := by
    rw [Real.sqrt_div (by norm_num : (0 : ℝ) ≤ 1)]
    norm_num
  rw [hv] at hs
  have h := limit_b_scaled.div hs (by norm_num)
  norm_num at h
  apply h.congr'
  filter_upwards [pos_eventually] with t ht
  dsimp only [Pi.div_apply]
  rw [Real.sqrt_div' _ (by norm_num)]
  field_simp [ht.ne']

theorem limit_mu_coordinate_determinant :
    Tendsto (fun t => mu t^3*(k00 t*k11 t-k01 t^2)) (𝓝[>] 0) (𝓝 4) := by
  have h := (limit_mu_scaled.pow 3).mul limit_scaledDet
  have h' := h.mul_const 7
  norm_num at h'
  apply h'.congr'
  filter_upwards [pos_eventually] with t ht
  rw [scaledDet_eq ht]
  unfold diagDet
  field_simp [ht.ne']

end
end QipmFormal.FractionalSDP
