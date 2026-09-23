import Mathlib

/-! Scalar asymptotics for the optimized harmonic mixture. -/
namespace MultilinearGap

open Filter Real
open scoped Topology
noncomputable section

/-- The logarithmic scale used for the sharp degree upper bound. -/
def sharpLambda (d : ℕ) : ℝ := max (exp 6) (1 + log d)

/-- Threshold inverse gain in the optimized mixture. -/
def sharpA (Λ : ℝ) : ℝ := Λ / (log Λ)^2

/-- Harmonic gain using the elementary union bound `S / (1 + S)`. -/
def sharpH (Λ : ℝ) : ℝ :=
  (1 - 1 / log Λ) / (1 + 1 / (log Λ)^2) *
    (log Λ - 3 * log (log Λ)) / Λ

/-- Sum of the three inverse gains, hence the mixture's gap bound. -/
def sharpZ (Λ : ℝ) : ℝ := 1 / sharpH Λ + sharpA Λ + 2 / (1 - exp (-1))

lemma tendsto_log_div_self :
    Tendsto (fun x : ℝ => log x / x) atTop (𝓝 0) := by
  simpa using tendsto_pow_log_div_mul_add_atTop 1 0 1 one_ne_zero

/-- The normalized harmonic gain tends to one. -/
theorem tendsto_sharpH_normalized :
    Tendsto (fun Λ : ℝ => sharpH Λ / (log Λ / Λ)) atTop (𝓝 1) := by
  have hi : Tendsto (fun Λ : ℝ => 1 / log Λ) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop tendsto_log_atTop
  have hj : Tendsto (fun Λ : ℝ => log (log Λ) / log Λ) atTop (𝓝 0) :=
    tendsto_log_div_self.comp tendsto_log_atTop
  have ht := (((tendsto_const_nhds (x := (1:ℝ))).sub hi).div
    ((tendsto_const_nhds (x := (1:ℝ))).add (hi.pow 2)) (by norm_num : (1:ℝ) + 0^2 ≠ 0)).mul
      ((tendsto_const_nhds (x := (1:ℝ))).sub (hj.const_mul 3))
  have ht' : Tendsto (fun Λ : ℝ => (1 - 1 / log Λ) /
      (1 + (1 / log Λ)^2) * (1 - 3 * (log (log Λ) / log Λ)))
      atTop (𝓝 1) := by simpa using ht
  apply ht'.congr'
  filter_upwards [eventually_gt_atTop (1 : ℝ)] with Λ hΛ
  have hΛ0 : Λ ≠ 0 := ne_of_gt (lt_trans zero_lt_one hΛ)
  have hb : log Λ ≠ 0 := ne_of_gt (log_pos hΛ)
  dsimp [sharpH]
  field_simp [hΛ0, hb]

/-- The optimized mixture has leading constant one in its own scale. -/
theorem tendsto_sharpZ_normalized :
    Tendsto (fun Λ : ℝ => sharpZ Λ / (Λ / log Λ)) atTop (𝓝 1) := by
  have hh := (tendsto_const_nhds (x := (1:ℝ))).div tendsto_sharpH_normalized
    (by norm_num : (1:ℝ) ≠ 0)
  have hi : Tendsto (fun Λ : ℝ => 1 / log Λ) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop tendsto_log_atTop
  have hc := tendsto_log_div_self.const_mul (2 / (1 - exp (-1)))
  have ht : Tendsto (fun Λ : ℝ => 1 / (sharpH Λ / (log Λ / Λ)) +
      1 / log Λ + (2 / (1 - exp (-1))) * (log Λ / Λ)) atTop (𝓝 1) := by
    simpa using (hh.add hi).add hc
  apply ht.congr'
  filter_upwards [eventually_gt_atTop (1 : ℝ)] with Λ hΛ
  have hΛ0 : Λ ≠ 0 := ne_of_gt (lt_trans zero_lt_one hΛ)
  have hb : log Λ ≠ 0 := ne_of_gt (log_pos hΛ)
  simp only [sharpZ, sharpA, add_div, div_div, one_div, inv_div]
  field_simp [hΛ0, hb]

lemma tendsto_log_add_one_div_log :
    Tendsto (fun x : ℝ => log (x + 1) / log x) atTop (𝓝 1) := by
  have h := (tendsto_log_comp_add_sub_log 1).div_atTop tendsto_log_atTop
  have ht : Tendsto (fun x : ℝ => (log (x+1)-log x)/log x + 1)
      atTop (𝓝 1) := by simpa using h.add_const 1
  apply ht.congr'
  filter_upwards [eventually_gt_atTop (1 : ℝ)] with x hx
  field_simp [ne_of_gt (log_pos hx)]
  ring

lemma tendsto_add_one_scale :
    Tendsto (fun x : ℝ => ((1+x)/log (1+x))/(x/log x)) atTop (𝓝 1) := by
  have hi : Tendsto (fun x : ℝ => 1/x) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop tendsto_id
  have hn : Tendsto (fun x : ℝ => 1/x+1) atTop (𝓝 1) := by
    simpa using hi.add_const 1
  have ht := hn.div tendsto_log_add_one_div_log (by norm_num : (1:ℝ) ≠ 0)
  simp only [div_one] at ht
  apply ht.congr'
  filter_upwards [eventually_gt_atTop (1 : ℝ)] with x hx
  have hx0 : x ≠ 0 := ne_of_gt (lt_trans zero_lt_one hx)
  have hl : log x ≠ 0 := ne_of_gt (log_pos hx)
  have hl1 : log (x+1) ≠ 0 := ne_of_gt (log_pos (by linarith))
  dsimp
  rw [add_comm 1 x]
  field_simp
  ring

lemma sharpLambda_eventually :
    ∀ᶠ d : ℕ in atTop, sharpLambda d = 1 + log d := by
  have hd : Tendsto (fun d : ℕ => 1 + log d) atTop atTop := by
    simpa [add_comm] using
      (tendsto_log_atTop.comp tendsto_natCast_atTop_atTop).atTop_add
        (tendsto_const_nhds (x := (1:ℝ)))
  filter_upwards [hd.eventually (eventually_ge_atTop (exp 6))] with d hd
  exact max_eq_right hd

lemma tendsto_sharpLambda : Tendsto sharpLambda atTop atTop := by
  unfold sharpLambda
  apply tendsto_atTop_mono (fun d : ℕ => le_max_right (exp 6) (1+log d))
  simpa [add_comm] using
    (tendsto_log_atTop.comp tendsto_natCast_atTop_atTop).atTop_add
      (tendsto_const_nhds (x := (1:ℝ)))

/-- The sharp scale agrees asymptotically with `log d / log (log d)`. -/
theorem tendsto_sharpLambda_scale :
    Tendsto (fun d : ℕ => (sharpLambda d / log (sharpLambda d)) /
      (log d / log (log d))) atTop (𝓝 1) := by
  apply (tendsto_add_one_scale.comp
    (tendsto_log_atTop.comp tendsto_natCast_atTop_atTop)).congr'
  filter_upwards [sharpLambda_eventually] with d hd
  simp only [Function.comp_apply, hd]

/-- The optimized degree bound has the claimed leading constant one. -/
theorem tendsto_sharpZ_degree_normalized :
    Tendsto (fun d : ℕ => sharpZ (sharpLambda d) /
      (log d / log (log d))) atTop (𝓝 1) := by
  have ht := (tendsto_sharpZ_normalized.comp tendsto_sharpLambda).mul
    tendsto_sharpLambda_scale
  simp only [one_mul] at ht
  apply ht.congr'
  filter_upwards [tendsto_sharpLambda.eventually (eventually_gt_atTop (1:ℝ))] with d hd
  have hΛ : sharpLambda d ≠ 0 := ne_of_gt (lt_trans zero_lt_one hd)
  have hb : log (sharpLambda d) ≠ 0 := ne_of_gt (log_pos hd)
  dsimp
  field_simp [hΛ, hb]

/-- Positivity of the logarithmic interval length from the explicit cutoff six. -/
lemma log_interval_pos {b : ℝ} (hb : 6 ≤ b) : 0 < b - 3 * log b := by
  have hb0 : 0 < b := by linarith
  have hlog6 : log 6 < 2 := by
    apply (log_lt_iff_lt_exp (by norm_num : (0:ℝ) < 6)).mpr
    have he := exp_one_gt_d9
    have hp := exp_pos 1
    rw [show (2:ℝ) = 1+1 by norm_num, exp_add]
    nlinarith
  have ht := log_le_sub_one_of_pos (div_pos hb0 (by norm_num : (0:ℝ) < 6))
  rw [log_div (ne_of_gt hb0) (by norm_num : (6:ℝ) ≠ 0)] at ht
  linarith

lemma sharpLambda_ge_exp (d : ℕ) : exp 6 ≤ sharpLambda d := le_max_left _ _

lemma log_ge_six {Λ : ℝ} (hΛ : exp 6 ≤ Λ) : 6 ≤ log Λ := by
  simpa using log_le_log (exp_pos 6) hΛ

lemma sharpH_pos {Λ : ℝ} (hΛ : exp 6 ≤ Λ) : 0 < sharpH Λ := by
  have hΛ0 : 0 < Λ := lt_of_lt_of_le (exp_pos 6) hΛ
  have hb := log_ge_six hΛ
  have hb0 : 0 < log Λ := by linarith
  have hi : 1 / log Λ < 1 := (div_lt_one hb0).mpr (by linarith)
  unfold sharpH
  exact div_pos (mul_pos (div_pos (by linarith) (by positivity))
    (log_interval_pos hb)) hΛ0

lemma sharpA_pos {Λ : ℝ} (hΛ : exp 6 ≤ Λ) : 0 < sharpA Λ := by
  have hΛ0 : 0 < Λ := lt_of_lt_of_le (exp_pos 6) hΛ
  have hb := log_ge_six hΛ
  unfold sharpA
  exact div_pos hΛ0 (sq_pos_of_pos (by linarith))

lemma sharp_interval_log {Λ : ℝ} (hΛ : exp 6 ≤ Λ) :
    log ((1 / log Λ) * sharpA Λ) = log Λ - 3 * log (log Λ) := by
  have hΛ0 : 0 < Λ := lt_of_lt_of_le (exp_pos 6) hΛ
  have hb := log_ge_six hΛ
  have hb0 : 0 < log Λ := by linarith
  have he : (1 / log Λ) * sharpA Λ = Λ / (log Λ)^3 := by
    unfold sharpA
    field_simp
  rw [he, log_div (ne_of_gt hΛ0) (ne_of_gt (pow_pos hb0 3)), log_pow]
  norm_num

lemma sharp_interval_nonempty {Λ : ℝ} (hΛ : exp 6 ≤ Λ) :
    1 < (1 / log Λ) * sharpA Λ := by
  have hb : 0 < log Λ := lt_of_lt_of_le (by norm_num : (0:ℝ) < 6) (log_ge_six hΛ)
  apply (log_pos_iff (mul_nonneg (by positivity) (sharpA_pos hΛ).le)).mp
  rw [sharp_interval_log hΛ]
  exact log_interval_pos (log_ge_six hΛ)

lemma sharpA_gt_one {Λ : ℝ} (hΛ : exp 6 ≤ Λ) : 1 < sharpA Λ := by
  have hb := log_ge_six hΛ
  have hi : 1 / log Λ ≤ 1 := (div_le_one (by linarith)).mpr (by linarith)
  have h := mul_le_mul_of_nonneg_right hi (sharpA_pos hΛ).le
  simpa using lt_of_lt_of_le (sharp_interval_nonempty hΛ) h

lemma sharpH_eq_gain {Λ : ℝ} (hΛ : exp 6 ≤ Λ) :
    sharpH Λ = (1 - 1 / log Λ) / (1 + sharpA Λ / Λ) *
      log ((1 / log Λ) * sharpA Λ) / Λ := by
  rw [sharp_interval_log hΛ]
  have hΛ0 : Λ ≠ 0 := ne_of_gt (lt_of_lt_of_le (exp_pos 6) hΛ)
  have ha : sharpA Λ / Λ = 1 / (log Λ)^2 := by
    unfold sharpA
    field_simp
  rw [ha]
  rfl

lemma independent_gain_pos : 0 < 1 - exp (-1 : ℝ) := by
  have h : exp (-1 : ℝ) < exp 0 := exp_lt_exp.mpr (by norm_num)
  rw [exp_zero] at h
  exact sub_pos.mpr h

lemma sharpZ_pos {Λ : ℝ} (hΛ : exp 6 ≤ Λ) : 0 < sharpZ Λ := by
  unfold sharpZ
  exact add_pos (add_pos (div_pos one_pos (sharpH_pos hΛ)) (sharpA_pos hΛ))
    (div_pos (by norm_num) independent_gain_pos)

end
end MultilinearGap
