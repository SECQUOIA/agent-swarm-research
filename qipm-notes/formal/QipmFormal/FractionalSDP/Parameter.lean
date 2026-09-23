import QipmFormal.FractionalSDP.Defs

/-! Every sufficiently small objective gap and central parameter occurs on
the rational curve. The inverse choices tend to zero through positive
parameters, so limits along this curve describe the whole central tail. -/

namespace QipmFormal.FractionalSDP
noncomputable section
open Filter Set Topology

private theorem den_pos (t : ℝ) : 0 < denom t := by
  unfold denom
  nlinarith [sq_nonneg (t + 1)]

private theorem edge_pos {t : ℝ} (ht : t ∈ Icc (0 : ℝ) 1) :
    0 < 3 + t - t ^ 2 := by
  nlinarith [mul_nonneg ht.1 (sub_nonneg.mpr ht.2)]

theorem parameter_mu_formula {t : ℝ} (ht : t ∈ Icc (0 : ℝ) 1) :
    mu t = t ^ 2 * (t + 2) / (denom t * (3 + t - t ^ 2)) := by
  have hd := ne_of_gt (den_pos t)
  have he := ne_of_gt (edge_pos ht)
  have hx : 1 - b t - 2 * g t = (3 + t - t ^ 2) / denom t := by
    unfold b g
    field_simp [hd]
    unfold denom
    ring
  unfold mu
  rw [hx]
  unfold q a b g
  field_simp
  ring

theorem parameter_g_continuous : Continuous g := by
  unfold g
  exact (continuous_id.pow 2).div
    (by unfold denom; fun_prop) (fun t => ne_of_gt (den_pos t))

theorem parameter_mu_continuous : ContinuousOn mu (Icc (0 : ℝ) 1) := by
  apply ContinuousOn.congr (f := fun t =>
    t ^ 2 * (t + 2) / (denom t * (3 + t - t ^ 2)))
  · apply ContinuousOn.div
    · fun_prop
    · unfold denom; fun_prop
    · intro t ht
      exact mul_ne_zero (ne_of_gt (den_pos t)) (ne_of_gt (edge_pos ht))
  · intro t ht
    exact parameter_mu_formula ht

@[simp] theorem parameter_g_zero : g 0 = 0 := by norm_num [g, denom]
@[simp] theorem parameter_g_one : g 1 = 1 / 6 := by norm_num [g, denom]
@[simp] theorem parameter_mu_zero : mu 0 = 0 := by norm_num [mu, q, a, b, g, denom]
@[simp] theorem parameter_mu_one : mu 1 = 1 / 6 := by norm_num [mu, q, a, b, g, denom]

theorem parameter_g_surjective {y : ℝ} (hy0 : 0 < y) (hy1 : y < 1 / 6) :
    ∃ t ∈ Ioo (0 : ℝ) 1, g t = y := by
  obtain ⟨t, ht, heq⟩ := intermediate_value_Icc (by norm_num : (0 : ℝ) ≤ 1)
    parameter_g_continuous.continuousOn
    (show y ∈ Icc (g 0) (g 1) by rw [parameter_g_zero, parameter_g_one]; exact ⟨hy0.le, hy1.le⟩)
  refine ⟨t, ⟨lt_of_le_of_ne ht.1 ?_, lt_of_le_of_ne ht.2 ?_⟩, heq⟩
  · intro h; subst t; simp at heq; linarith
  · intro h; subst t; simp at heq; linarith

theorem parameter_mu_surjective {y : ℝ} (hy0 : 0 < y) (hy1 : y < 1 / 6) :
    ∃ t ∈ Ioo (0 : ℝ) 1, mu t = y := by
  obtain ⟨t, ht, heq⟩ := intermediate_value_Icc (by norm_num : (0 : ℝ) ≤ 1)
    parameter_mu_continuous
    (show y ∈ Icc (mu 0) (mu 1) by rw [parameter_mu_zero, parameter_mu_one]; exact ⟨hy0.le, hy1.le⟩)
  refine ⟨t, ⟨lt_of_le_of_ne ht.1 ?_, lt_of_le_of_ne ht.2 ?_⟩, heq⟩
  · intro h; subst t; simp at heq; linarith
  · intro h; subst t; simp at heq; linarith

theorem parameter_g_bound {t : ℝ} (ht : t ∈ Icc (0 : ℝ) 1) :
    t ^ 2 ≤ 6 * g t := by
  have hd := den_pos t
  have hu : denom t ≤ 6 := by
    unfold denom
    nlinarith [ht.1, ht.2, mul_nonneg ht.1 (sub_nonneg.mpr ht.2)]
  unfold g
  rw [← mul_div_assoc]
  apply (le_div_iff₀ hd).mpr
  nlinarith [mul_le_mul_of_nonneg_left hu (sq_nonneg t)]

theorem parameter_mu_bound {t : ℝ} (ht : t ∈ Icc (0 : ℝ) 1) :
    t ^ 2 ≤ 12 * mu t := by
  rw [parameter_mu_formula ht]
  have hd := den_pos t
  have he := edge_pos ht
  have hu : denom t ≤ 6 := by
    unfold denom
    nlinarith [ht.1, ht.2, mul_nonneg ht.1 (sub_nonneg.mpr ht.2)]
  have hv : 3 + t - t ^ 2 ≤ 4 := by nlinarith [sq_nonneg t]
  have hp : denom t * (3 + t - t ^ 2) ≤ 24 := by
    nlinarith [mul_le_mul hu hv he.le (by norm_num : (0 : ℝ) ≤ 6)]
  rw [← mul_div_assoc]
  apply (le_div_iff₀ (mul_pos hd he)).mpr
  nlinarith [mul_le_mul_of_nonneg_left hp (sq_nonneg t), mul_nonneg (sq_nonneg t) ht.1]

private def selectedParameter (f : ℝ → ℝ) (y : ℝ) : ℝ := by
  classical
  exact if h : ∃ t ∈ Ioo (0 : ℝ) 1, f t = y then Classical.choose h else 0

private theorem selectedParameter_spec {f : ℝ → ℝ} {y : ℝ}
    (h : ∃ t ∈ Ioo (0 : ℝ) 1, f t = y) :
    selectedParameter f y ∈ Ioo (0 : ℝ) 1 ∧ f (selectedParameter f y) = y := by
  simp only [selectedParameter, dif_pos h]
  exact Classical.choose_spec h

def muParameter : ℝ → ℝ := selectedParameter mu
def gapParameter : ℝ → ℝ := selectedParameter g

theorem muParameter_spec {y : ℝ} (hy0 : 0 < y) (hy1 : y < 1 / 6) :
    muParameter y ∈ Ioo (0 : ℝ) 1 ∧ mu (muParameter y) = y :=
  selectedParameter_spec (parameter_mu_surjective hy0 hy1)

theorem gapParameter_spec {y : ℝ} (hy0 : 0 < y) (hy1 : y < 1 / 6) :
    gapParameter y ∈ Ioo (0 : ℝ) 1 ∧ g (gapParameter y) = y :=
  selectedParameter_spec (parameter_g_surjective hy0 hy1)

private theorem selectedParameter_tendsto {f : ℝ → ℝ} {C : ℝ}
    (hcover : ∀ y ∈ Ioo (0 : ℝ) (1 / 6), ∃ t ∈ Ioo (0 : ℝ) 1, f t = y)
    (hbound : ∀ t ∈ Icc (0 : ℝ) 1, t ^ 2 ≤ C * f t) :
    Tendsto (selectedParameter f) (𝓝[>] (0 : ℝ)) (𝓝[>] (0 : ℝ)) := by
  have he : ∀ᶠ y : ℝ in 𝓝[>] 0,
      selectedParameter f y ∈ Ioo (0 : ℝ) 1 ∧ f (selectedParameter f y) = y := by
    filter_upwards [Ioo_mem_nhdsGT (by norm_num : (0 : ℝ) < 1 / 6)] with y hy
    exact selectedParameter_spec (hcover y hy)
  apply tendsto_nhdsWithin_iff.mpr
  refine ⟨?_, he.mono (fun _ h => h.1.1)⟩
  apply squeeze_zero' (he.mono (fun _ h => h.1.1.le))
    (g := fun y : ℝ => Real.sqrt (C * y))
  · filter_upwards [he] with y hy
    apply Real.le_sqrt_of_sq_le
    simpa only [hy.2] using hbound _ ⟨hy.1.1.le, hy.1.2.le⟩
  · have h : ContinuousAt (fun y : ℝ => Real.sqrt (C * y)) 0 := by fun_prop
    simpa using h.tendsto.mono_left nhdsWithin_le_nhds

theorem muParameter_tendsto :
    Tendsto muParameter (𝓝[>] (0 : ℝ)) (𝓝[>] (0 : ℝ)) :=
  selectedParameter_tendsto (C := 12)
    (fun _ hy => parameter_mu_surjective hy.1 hy.2)
    (fun _ ht => parameter_mu_bound ht)

theorem gapParameter_tendsto :
    Tendsto gapParameter (𝓝[>] (0 : ℝ)) (𝓝[>] (0 : ℝ)) :=
  selectedParameter_tendsto (C := 6)
    (fun _ hy => parameter_g_surjective hy.1 hy.2)
    (fun _ ht => parameter_g_bound ht)

end
end QipmFormal.FractionalSDP
