import Mathlib

namespace PotentialFlow

noncomputable section

def edgeEnergy (cp cm x : ℝ) : ℝ :=
  (if 0 ≤ x then cp else cm) * |x| ^ 3 / 3

def edgeLaw (cp cm x : ℝ) : ℝ :=
  (if 0 ≤ x then cp else cm) * x * |x|

theorem edgeEnergy_nonneg {cp cm x : ℝ} (hcp : 0 ≤ cp) (hcm : 0 ≤ cm) :
    0 ≤ edgeEnergy cp cm x := by
  unfold edgeEnergy
  split <;> positivity

theorem edgeLaw_monotone {cp cm : ℝ} (hcp : 0 ≤ cp) (hcm : 0 ≤ cm) :
    Monotone (edgeLaw cp cm) := by
  intro x y hxy
  by_cases hx : 0 ≤ x
  · have hy : 0 ≤ y := hx.trans hxy
    simp only [edgeLaw, if_pos hx, if_pos hy, abs_of_nonneg hx, abs_of_nonneg hy]
    have hsq : x * x ≤ y * y := mul_self_le_mul_self hx hxy
    nlinarith [mul_le_mul_of_nonneg_left hsq hcp]
  · by_cases hy : 0 ≤ y
    · have hxn : x ≤ 0 := le_of_not_ge hx
      simp only [edgeLaw, if_neg hx, if_pos hy, abs_of_nonpos hxn, abs_of_nonneg hy]
      have hleft : cm * x * (-x) ≤ 0 :=
        mul_nonpos_of_nonpos_of_nonneg (mul_nonpos_of_nonneg_of_nonpos hcm hxn)
          (neg_nonneg.mpr hxn)
      have hright : 0 ≤ cp * y * y := by positivity
      exact hleft.trans hright
    · have hxn : x ≤ 0 := le_of_not_ge hx
      have hyn : y ≤ 0 := le_of_not_ge hy
      simp only [edgeLaw, if_neg hx, if_neg hy, abs_of_nonpos hxn, abs_of_nonpos hyn]
      have hsq : (-y) * (-y) ≤ (-x) * (-x) :=
        mul_self_le_mul_self (neg_nonneg.mpr hyn) (neg_le_neg hxy)
      nlinarith [mul_le_mul_of_nonneg_left hsq hcm]

private theorem positive_fenchel {c a u t : ℝ}
    (hc : 0 < c) (ha : 0 ≤ a) (hu : 0 ≤ u) (ht : 0 ≤ t)
    (hroot : a ^ 3 ≤ u ^ 2 * c) :
    a * t - c * t ^ 3 / 3 ≤ (2 / 3 : ℝ) * u := by
  let r := Real.sqrt (a / c)
  have hr : 0 ≤ r := Real.sqrt_nonneg _
  have hs : c * r ^ 2 = a := by
    dsimp [r]
    rw [Real.sq_sqrt (div_nonneg ha hc.le)]
    field_simp
  have hb : (c * r ^ 3) ^ 2 ≤ u ^ 2 := by
    apply (mul_le_mul_iff_right₀ hc).mp
    calc
      c * (c * r ^ 3) ^ 2 = a ^ 3 := by rw [← hs]; ring
      _ ≤ u ^ 2 * c := hroot
      _ = c * u ^ 2 := by ring
  have hru : c * r ^ 3 ≤ u := by nlinarith
  have hfactor : 0 ≤ c * (t - r) ^ 2 * (t + 2 * r) := by positivity
  have hprod : a * t = c * r ^ 2 * t := by rw [hs]
  nlinarith

theorem fenchel_root_bound {cp cm d x u : ℝ}
    (hcp : 0 < cp) (hcm : 0 < cm) (hu : 0 ≤ u)
    (hroot : |d| ^ 3 ≤ u ^ 2 * (if 0 ≤ d then cp else cm)) :
    d * x - edgeEnergy cp cm x ≤ (2 / 3 : ℝ) * u := by
  by_cases hd : 0 ≤ d
  · simp only [if_pos hd, abs_of_nonneg hd] at hroot
    by_cases hx : 0 ≤ x
    · simpa [edgeEnergy, hx, abs_of_nonneg hx] using
        positive_fenchel hcp hd hu hx hroot
    · have hdx : d * x ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hd (le_of_not_ge hx)
      have he := edgeEnergy_nonneg (x := x) hcp.le hcm.le
      linarith
  · have hdn : 0 ≤ -d := by linarith
    simp only [if_neg hd, abs_of_neg (lt_of_not_ge hd)] at hroot
    by_cases hx : 0 ≤ x
    · have hdx : d * x ≤ 0 := mul_nonpos_of_nonpos_of_nonneg (le_of_not_ge hd) hx
      have he := edgeEnergy_nonneg (x := x) hcp.le hcm.le
      linarith
    · have hxn : 0 ≤ -x := by linarith
      have h := positive_fenchel hcm hdn hu hxn hroot
      simpa [edgeEnergy, hx, abs_of_neg (lt_of_not_ge hx)] using h

end

end PotentialFlow
