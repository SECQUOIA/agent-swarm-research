import QipmFormal.ScalarCert.Elasticity

/-!
# `Y` maps `(0,1)` onto `(0,∞)`

The paper's `c⋆` is a supremum over `y > 0`, while `cstar` here is a supremum
over `v ∈ (0,1)` via `y = Y v`.  The two agree because `Y : (0,1) → (0,∞)` is
onto, which is proved here.

The comparison `artanh v ≤ Y v ≤ 2 artanh v` on `[0,1)` is immediate from the
series, since the `k`-th coefficient `2 - 2^{-k}` lies in `[1,2)`.
-/

namespace QipmFormal.ScalarCert

open Real Set

lemma one_le_coef (k : ℕ) : (1:ℝ) ≤ 2 - (1/2 : ℝ) ^ k := by
  have : ((1:ℝ)/2) ^ k ≤ 1 := pow_le_one₀ (by norm_num) (by norm_num)
  linarith

lemma coef_le_two (k : ℕ) : 2 - (1/2 : ℝ) ^ k ≤ 2 := by
  have : (0:ℝ) ≤ ((1:ℝ)/2) ^ k := by positivity
  linarith

/-- `artanh v ≤ Y v` on `[0,1)`. -/
theorem artanh_le_Y {v : ℝ} (hv0 : 0 ≤ v) (hv : |v| < 1) : artanh v ≤ Y v := by
  refine hasSum_le ?_ (hasSum_artanh hv) (hasSum_Y hv)
  intro k
  have hden : (0:ℝ) < 2 * (k : ℝ) + 1 := by positivity
  have hpow : (0:ℝ) ≤ v ^ (2 * k + 1) := pow_nonneg hv0 _
  have : (1:ℝ) / (2 * (k:ℝ) + 1) ≤ (2 - (1/2 : ℝ) ^ k) / (2 * (k:ℝ) + 1) := by
    gcongr
    exact one_le_coef k
  calc (1 / (2 * (k:ℝ) + 1)) * v ^ (2 * k + 1)
      ≤ ((2 - (1/2 : ℝ) ^ k) / (2 * (k:ℝ) + 1)) * v ^ (2 * k + 1) :=
        mul_le_mul_of_nonneg_right this hpow
    _ = (2 - (1/2 : ℝ) ^ k) / (2 * (k:ℝ) + 1) * v ^ (2 * k + 1) := rfl

/-- `Y v ≤ 2 artanh v` on `[0,1)`. -/
theorem Y_le_two_artanh {v : ℝ} (hv0 : 0 ≤ v) (hv : |v| < 1) : Y v ≤ 2 * artanh v := by
  refine hasSum_le ?_ (hasSum_Y hv) ((hasSum_artanh hv).mul_left 2)
  intro k
  have hden : (0:ℝ) < 2 * (k : ℝ) + 1 := by positivity
  have hpow : (0:ℝ) ≤ v ^ (2 * k + 1) := pow_nonneg hv0 _
  have hc : (2 - (1/2 : ℝ) ^ k) / (2 * (k:ℝ) + 1) ≤ 2 / (2 * (k:ℝ) + 1) := by
    gcongr
    exact coef_le_two k
  calc (2 - (1/2 : ℝ) ^ k) / (2 * (k:ℝ) + 1) * v ^ (2 * k + 1)
      ≤ (2 / (2 * (k:ℝ) + 1)) * v ^ (2 * k + 1) :=
        mul_le_mul_of_nonneg_right hc hpow
    _ = 2 * ((1 / (2 * (k:ℝ) + 1)) * v ^ (2 * k + 1)) := by ring

/-- `Y` is continuous on `(-1,1)`. -/
theorem Y_continuousOn : ContinuousOn Y (Ioo (-1 : ℝ) 1) := by
  intro x hx
  exact ((Y_deriv (abs_lt.mpr hx)).continuousAt).continuousWithinAt

/-- **`Y` maps `(0,1)` onto `(0,∞)`.** -/
theorem Y_surjOn {y : ℝ} (hy : 0 < y) : ∃ v ∈ Ioo (0:ℝ) 1, Y v = y := by
  set a : ℝ := Real.tanh (y / 4) with ha_def
  set b : ℝ := Real.tanh (2 * y) with hb_def
  have ha1' : a < 1 := by rw [ha_def]; exact Real.tanh_lt_one _
  have hb1 : b < 1 := by rw [hb_def]; exact Real.tanh_lt_one _
  have hane : (-1:ℝ) < a := by rw [ha_def]; exact Real.neg_one_lt_tanh _
  have hbne : (-1:ℝ) < b := by rw [hb_def]; exact Real.neg_one_lt_tanh _
  have ha0 : 0 < a := by
    by_contra hcon
    rw [not_lt] at hcon
    have h := Real.artanh_le_artanh hane (by norm_num : (0:ℝ) < 1) hcon
    rw [ha_def, Real.artanh_tanh, Real.artanh_zero] at h
    linarith
  have hab : a < b := by
    by_contra hcon
    rw [not_lt] at hcon
    have h := Real.artanh_le_artanh hbne ha1' hcon
    rw [ha_def, hb_def, Real.artanh_tanh, Real.artanh_tanh] at h
    linarith
  have ha1 : a < 1 := ha1'
  have hb0 : 0 < b := ha0.trans hab
  have haabs : |a| < 1 := by rw [abs_of_pos ha0]; exact ha1
  have hbabs : |b| < 1 := by rw [abs_of_pos hb0]; exact hb1
  -- `Y a ≤ y/2 < y`
  have hYa : Y a < y := by
    have h1 : Y a ≤ 2 * artanh a := Y_le_two_artanh ha0.le haabs
    have h2 : artanh a = y / 4 := by rw [ha_def, Real.artanh_tanh]
    rw [h2] at h1; linarith
  -- `y < 2y ≤ Y b`
  have hYb : y < Y b := by
    have h1 : artanh b ≤ Y b := artanh_le_Y hb0.le hbabs
    have h2 : artanh b = 2 * y := by rw [hb_def, Real.artanh_tanh]
    rw [h2] at h1; linarith
  have hcont : ContinuousOn Y (Icc a b) := by
    refine Y_continuousOn.mono ?_
    intro t ht
    exact ⟨by linarith [ht.1, ha0], by linarith [ht.2, hb1]⟩
  have hsub := intermediate_value_Ioo hab.le hcont
  obtain ⟨v, hv, hvy⟩ := hsub ⟨hYa, hYb⟩
  exact ⟨v, ⟨ha0.trans hv.1, hv.2.trans hb1⟩, hvy⟩

end QipmFormal.ScalarCert
