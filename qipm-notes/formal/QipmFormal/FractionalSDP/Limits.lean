import QipmFormal.FractionalSDP.Defs

/-! Exact leading constants of the four eigenvalue branches at the singular endpoint. -/
namespace QipmFormal.FractionalSDP
noncomputable section
open Filter Topology

private theorem denom_pos' {t : ℝ} (ht : 0 < t) : 0 < denom t := by
  unfold denom
  positivity

private theorem q_formula' {t : ℝ} (ht : 0 < t) :
    q t = t ^ 2 * (t + 2) / denom t ^ 2 := by
  unfold q a g b
  field_simp
  ring

/-- The scaled trace has a rational extension through the singular endpoint. -/
def scaledTrace (t : ℝ) : ℝ :=
  2 * denom t ^ 2 * (3*t^4+8*t^3+13*t^2+18*t+18) / (7*(t+2)^2)

/-- The scaled determinant has a rational extension through the singular endpoint. -/
def scaledDet (t : ℝ) : ℝ :=
  denom t ^ 4 * (t^5+4*t^4+4*t^3+18*t^2+45*t+36) / (7*(t+2)^3)

theorem scaledTrace_eq {t : ℝ} (ht : 0 < t) :
    scaledTrace t = t ^ 4 * diagTrace t := by
  have hd := (denom_pos' ht).ne'
  have ht' := ht.ne'
  have hp : t + 2 ≠ 0 := by positivity
  unfold diagTrace k00 k01 k11
  rw [q_formula' ht]
  unfold scaledTrace b g
  field_simp
  unfold denom
  ring

theorem scaledDet_eq {t : ℝ} (ht : 0 < t) :
    scaledDet t = t ^ 6 * diagDet t := by
  have hd := (denom_pos' ht).ne'
  have ht' := ht.ne'
  have hp : t + 2 ≠ 0 := by positivity
  unfold diagDet k00 k01 k11
  rw [q_formula' ht]
  unfold scaledDet b g
  field_simp
  unfold denom
  ring

theorem limit_scaledTrace : Tendsto scaledTrace (𝓝[>] (0 : ℝ)) (𝓝 (81/7)) := by
  have hc : ContinuousAt scaledTrace 0 := by
    unfold scaledTrace denom
    fun_prop (disch := norm_num)
  convert hc.tendsto.mono_left nhdsWithin_le_nhds using 1
  norm_num [scaledTrace, denom]

theorem limit_scaledDet : Tendsto scaledDet (𝓝[>] (0 : ℝ)) (𝓝 (729/14)) := by
  have hc : ContinuousAt scaledDet 0 := by
    unfold scaledDet denom
    fun_prop (disch := norm_num)
  convert hc.tendsto.mono_left nhdsWithin_le_nhds using 1
  norm_num [scaledDet, denom]

private theorem t_pos_eventually : ∀ᶠ t : ℝ in 𝓝[>] 0, 0 < t :=
  self_mem_nhdsWithin

theorem limit_aHigh : Tendsto aHigh (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have hc : ContinuousAt aHigh 0 := by
    unfold aHigh a g b denom
    fun_prop (disch := norm_num)
  convert hc.tendsto.mono_left nhdsWithin_le_nhds using 1
  norm_num [aHigh, a, g, b, denom]

theorem limit_offLow : Tendsto (fun t : ℝ => t * offLow t) (𝓝[>] 0) (𝓝 3) := by
  have hd : Tendsto denom (𝓝[>] (0 : ℝ)) (𝓝 3) := by
    have hc : ContinuousAt denom 0 := by unfold denom; fun_prop
    simpa [denom] using hc.tendsto.mono_left nhdsWithin_le_nhds
  have h := hd.div limit_aHigh (by norm_num)
  norm_num at h
  apply h.congr'
  filter_upwards [t_pos_eventually] with t ht
  change denom t / aHigh t = _
  unfold offLow b
  have := ht.ne'
  field_simp

theorem limit_offHigh : Tendsto (fun t : ℝ => t ^ 3 * offHigh t)
    (𝓝[>] 0) (𝓝 (27/2)) := by
  have hr : Tendsto (fun t : ℝ => denom t ^ 3 / (t+2))
      (𝓝[>] 0) (𝓝 (27/2)) := by
    have hc : ContinuousAt (fun t : ℝ => denom t ^ 3 / (t+2)) 0 := by
      unfold denom; fun_prop (disch := norm_num)
    convert hc.tendsto.mono_left nhdsWithin_le_nhds using 1
    norm_num [denom]
  have h := limit_aHigh.mul hr
  norm_num at h
  apply h.congr'
  filter_upwards [t_pos_eventually] with t ht
  unfold offHigh
  rw [q_formula' ht]
  unfold b
  have := ht.ne'
  have := (denom_pos' ht).ne'
  field_simp


theorem limit_diagHigh : Tendsto (fun t : ℝ => t ^ 4 * diagHigh t)
    (𝓝[>] 0) (𝓝 (81/7)) := by
  have hid : Tendsto (fun t : ℝ => t) (𝓝[>] 0) (𝓝 0) :=
    tendsto_id.mono_left nhdsWithin_le_nhds
  have hs := ((limit_scaledTrace.pow 2).sub
    (((tendsto_const_nhds (x := (4 : ℝ))).mul (hid.pow 2)).mul limit_scaledDet)).sqrt
  have hh := (limit_scaledTrace.add hs).div_const 2
  have hv : ((81 / 7 : ℝ) + Real.sqrt ((81 / 7)^2 - 4 * 0^2 * (729/14))) / 2 = 81/7 := by
    norm_num [Real.sqrt_sq]
  rw [hv] at hh
  apply hh.congr'
  filter_upwards [t_pos_eventually] with t ht
  rw [scaledTrace_eq ht, scaledDet_eq ht]
  have he : (t ^ 4 * diagTrace t)^2 - 4*t^2*(t^6*diagDet t) =
      (t^4)^2 * (diagTrace t ^ 2 - 4 * diagDet t) := by ring
  rw [he, Real.sqrt_mul (sq_nonneg _), Real.sqrt_sq (by positivity : 0 ≤ t^4)]
  unfold diagHigh
  ring

theorem limit_diagLow : Tendsto (fun t : ℝ => t ^ 2 * diagLow t)
    (𝓝[>] 0) (𝓝 (9/2)) := by
  have h := limit_scaledDet.div limit_diagHigh (by norm_num)
  norm_num at h
  apply h.congr'
  filter_upwards [t_pos_eventually] with t ht
  change scaledDet t / (t ^ 4 * diagHigh t) = _
  rw [scaledDet_eq ht]
  unfold diagLow
  have := ht.ne'
  field_simp

theorem limit_mu_scaled : Tendsto (fun t : ℝ => mu t / t ^ 2)
    (𝓝[>] 0) (𝓝 (2/9)) := by
  have hc : ContinuousAt (fun t : ℝ => (t+2)/((3+t-t^2)*denom t)) 0 := by
    unfold denom; fun_prop (disch := norm_num)
  have h : Tendsto (fun t : ℝ => (t+2)/((3+t-t^2)*denom t))
      (𝓝[>] 0) (𝓝 (2/9)) := by
    convert hc.tendsto.mono_left nhdsWithin_le_nhds using 1
    norm_num [denom]
  apply h.congr'
  filter_upwards [t_pos_eventually] with t ht
  unfold mu
  rw [q_formula' ht]
  unfold b g
  have hd := (denom_pos' ht).ne'
  have ht' := ht.ne'
  have he : 1-t/denom t-2*(t^2/denom t) = (3+t-t^2)/denom t := by
    field_simp
    unfold denom
    ring
  rw [he]
  field_simp


theorem limit_g_scaled : Tendsto (fun t : ℝ => g t / t ^ 2)
    (𝓝[>] 0) (𝓝 (1/3)) := by
  have hc : ContinuousAt (fun t : ℝ => 1/denom t) 0 := by
    unfold denom; fun_prop (disch := norm_num)
  have h : Tendsto (fun t : ℝ => 1/denom t) (𝓝[>] 0) (𝓝 (1/3)) := by
    convert hc.tendsto.mono_left nhdsWithin_le_nhds using 1
    norm_num [denom]
  apply h.congr'
  filter_upwards [t_pos_eventually] with t ht
  unfold g
  have := ht.ne'
  field_simp

/-- Positivity and the real, distinct diagonal roots hold throughout a punctured
right neighborhood, without additional spectral hypotheses. -/
theorem eventually_spectrum_positive : ∀ᶠ t : ℝ in 𝓝[>] 0,
    0 < diagTrace t ∧ 0 < diagDet t ∧
    0 < diagTrace t ^ 2 - 4 * diagDet t ∧
    0 < offLow t ∧ 0 < diagLow t ∧ 0 < offHigh t ∧ 0 < diagHigh t := by
  have hid : Tendsto (fun t : ℝ => t) (𝓝[>] 0) (𝓝 0) :=
    tendsto_id.mono_left nhdsWithin_le_nhds
  have hdisc := (limit_scaledTrace.pow 2).sub
    (((tendsto_const_nhds (x := (4 : ℝ))).mul (hid.pow 2)).mul limit_scaledDet)
  have hp := hdisc.eventually (eventually_gt_nhds (by norm_num :
    (0 : ℝ) < (81/7)^2 - 4*0^2*(729/14)))
  filter_upwards [t_pos_eventually,
    limit_scaledTrace.eventually (eventually_gt_nhds (by norm_num : (0 : ℝ) < 81/7)),
    limit_scaledDet.eventually (eventually_gt_nhds (by norm_num : (0 : ℝ) < 729/14)), hp,
    limit_offLow.eventually (eventually_gt_nhds (by norm_num : (0 : ℝ) < 3)),
    limit_diagLow.eventually (eventually_gt_nhds (by norm_num : (0 : ℝ) < 9/2)),
    limit_offHigh.eventually (eventually_gt_nhds (by norm_num : (0 : ℝ) < 27/2)),
    limit_diagHigh.eventually (eventually_gt_nhds (by norm_num : (0 : ℝ) < 81/7))]
    with t ht htr hdet hd hl hdl hh hdh
  rw [scaledTrace_eq ht] at htr hd
  rw [scaledDet_eq ht] at hdet hd
  have htr' : 0 < diagTrace t := (mul_pos_iff_of_pos_left (by positivity)).mp htr
  have hdet' : 0 < diagDet t := (mul_pos_iff_of_pos_left (by positivity)).mp hdet
  have he : (t^4*diagTrace t)^2 - 4*t^2*(t^6*diagDet t) =
      t^8 * (diagTrace t^2 - 4*diagDet t) := by ring
  rw [he] at hd
  exact ⟨htr', hdet', (mul_pos_iff_of_pos_left (by positivity)).mp hd,
    (mul_pos_iff_of_pos_left ht).mp hl,
    (mul_pos_iff_of_pos_left (by positivity)).mp hdl,
    (mul_pos_iff_of_pos_left (by positivity)).mp hh,
    (mul_pos_iff_of_pos_left (by positivity)).mp hdh⟩

end
end QipmFormal.FractionalSDP
