import Formal.PotentialFlow.Scalar

namespace PotentialFlow

private theorem cubic_same_side (p a x y : ℝ) (ha : 0 ≤ a) (hp : a ≤ p)
    (hx : 0 ≤ x) (hy : 0 ≤ y) :
    a / 6 * |y - x| ^ 3 ≤ p * y ^ 3 / 3 - p * x ^ 3 / 3 - p * x ^ 2 * (y - x) := by
  apply sub_nonneg.mp
  by_cases h : x ≤ y
  · rw [abs_of_nonneg (sub_nonneg.mpr h)]
    calc
      0 ≤ (p - a) / 3 * (y - x) ^ 2 * (y + 2 * x) +
          a / 6 * (y - x) ^ 2 * (y + 5 * x) := by positivity
      _ = _ := by ring
  · rw [abs_of_nonpos (sub_nonpos.mpr (le_of_not_ge h))]
    calc
      0 ≤ (p - a) / 3 * (y - x) ^ 2 * (y + 2 * x) +
          a / 6 * (y - x) ^ 2 * (3 * y + 3 * x) := by positivity
      _ = _ := by ring

private theorem cubic_crossing (p q a s t : ℝ) (ha : 0 ≤ a) (hp : a ≤ p)
    (hq : a ≤ q) (hs : 0 ≤ s) (ht : 0 ≤ t) :
    a / 6 * (s + t) ^ 3 ≤ q * t ^ 3 / 3 + p * (2 * s ^ 3 / 3 + s ^ 2 * t) := by
  apply sub_nonneg.mp
  calc
    0 ≤ (p-a) * (2 * s^3 / 3 + s^2*t) + (q-a) * t^3 / 3 +
        a / 24 * (4*t*(t-2*s)^2 + s*(2*t-s)^2 + 11*s^3) := by positivity
    _ = _ := by ring

theorem edge_bregman_modulus (cp cm a x y : ℝ) (ha : 0 < a)
    (hcp : a ≤ cp) (hcm : a ≤ cm) :
    a / 6 * |y - x| ^ 3 ≤
      edgeEnergy cp cm y - edgeEnergy cp cm x - edgeLaw cp cm x * (y - x) := by
  by_cases hx : 0 ≤ x
  · by_cases hy : 0 ≤ y
    · simpa only [edgeEnergy, edgeLaw, if_pos hx, if_pos hy, abs_of_nonneg hx,
        abs_of_nonneg hy, ← sq, mul_assoc] using cubic_same_side cp a x y ha.le hcp hx hy
    · have hy' : y ≤ 0 := le_of_not_ge hy
      have h := cubic_crossing cp cm a x (-y) ha.le hcp hcm hx (neg_nonneg.mpr hy')
      simp only [edgeEnergy, edgeLaw, if_pos hx, if_neg hy, abs_of_nonneg hx,
        abs_of_nonpos hy', abs_of_nonpos (by linarith : y - x ≤ 0)]
      convert h using 1 <;> ring
  · have hx' : x ≤ 0 := le_of_not_ge hx
    by_cases hy : 0 ≤ y
    · have h := cubic_crossing cm cp a (-x) y ha.le hcm hcp (neg_nonneg.mpr hx') hy
      simp only [edgeEnergy, edgeLaw, if_neg hx, if_pos hy, abs_of_nonpos hx',
        abs_of_nonneg hy, abs_of_nonneg (by linarith : 0 ≤ y - x)]
      convert h using 1 <;> ring
    · have hy' : y ≤ 0 := le_of_not_ge hy
      have h := cubic_same_side cm a (-x) (-y) ha.le hcm
        (neg_nonneg.mpr hx') (neg_nonneg.mpr hy')
      simp only [edgeEnergy, edgeLaw, if_neg hx, if_neg hy, abs_of_nonpos hx',
        abs_of_nonpos hy']
      rw [show -y - -x = -(y-x) by ring, abs_neg] at h
      convert h using 1; ring

open Filter Topology in
theorem hasDerivAt_edgeEnergy (cp cm x : ℝ) :
    HasDerivAt (edgeEnergy cp cm) (edgeLaw cp cm x) x := by
  rcases lt_trichotomy x 0 with hx | rfl | hx
  · have h := ((((hasDerivAt_id x).pow 3).const_mul (-cm)).div_const 3)
    have heq : (fun t : ℝ => -cm * t ^ 3 / 3) =ᶠ[𝓝 x] edgeEnergy cp cm := by
      filter_upwards [Iio_mem_nhds hx] with t ht
      simp only [Set.mem_Iio] at ht
      simp [edgeEnergy, not_le.mpr ht, abs_of_neg ht]; ring
    have hr : edgeLaw cp cm x = -cm * (3 * x ^ 2 * 1) / 3 := by
      simp only [edgeLaw, if_neg (not_le.mpr hx), abs_of_neg hx]
      ring
    rw [hr]
    exact h.congr_of_eventuallyEq heq.symm
  · simp only [edgeLaw, le_refl, if_true, mul_zero, abs_zero]
    rw [hasDerivAt_iff_tendsto_slope_zero]
    have hp : Tendsto (fun t : ℝ => cp * t ^ 2 / 3) (𝓝[≠] 0) (𝓝 0) := by
      have h : ContinuousAt (fun t : ℝ => cp * t ^ 2 / 3) 0 := by fun_prop
      simpa using h.tendsto.mono_left nhdsWithin_le_nhds
    have hm : Tendsto (fun t : ℝ => -cm * t ^ 2 / 3) (𝓝[≠] 0) (𝓝 0) := by
      have h : ContinuousAt (fun t : ℝ => -cm * t ^ 2 / 3) 0 := by fun_prop
      simpa using h.tendsto.mono_left nhdsWithin_le_nhds
    apply (hp.if' hm (p := fun t => 0 ≤ t)).congr'
    filter_upwards [self_mem_nhdsWithin] with t ht
    have ht0 : t ≠ 0 := ht
    by_cases htpos : 0 ≤ t
    · simp [edgeEnergy, htpos, abs_of_nonneg htpos, smul_eq_mul]
      field_simp
    · simp [edgeEnergy, htpos, abs_of_neg (lt_of_not_ge htpos), smul_eq_mul]
      field_simp
  · have h := ((((hasDerivAt_id x).pow 3).const_mul cp).div_const 3)
    have heq : (fun t : ℝ => cp * t ^ 3 / 3) =ᶠ[𝓝 x] edgeEnergy cp cm := by
      filter_upwards [Ioi_mem_nhds hx] with t ht
      simp only [Set.mem_Ioi] at ht
      simp [edgeEnergy, ht.le, abs_of_pos ht]
    have hr : edgeLaw cp cm x = cp * (3 * x ^ 2 * 1) / 3 := by
      simp only [edgeLaw, if_pos hx.le, abs_of_pos hx]
      ring
    rw [hr]
    exact h.congr_of_eventuallyEq heq.symm

end PotentialFlow
