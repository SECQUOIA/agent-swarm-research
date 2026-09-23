import QipmFormal.ScalarCert.Localization
import QipmFormal.ScalarCert.Bridge

/-!
# The maximizer localization in the `x` coordinate

`eq:cstar-maximizer-location` states the localization both in `v` and in the
original coordinate `x = v/√(2-v²)` (the inverse of `vOf`):

  `4611/5000 < v⋆ < 9701/10000`,   `43/50 < x⋆ < 943/1000`.

The second follows from the first by rational squaring, as the appendix says.
-/

namespace QipmFormal.ScalarCert

open Real Set

/-- `x = v/√(2-v²)`, the inverse of `vOf`. -/
noncomputable def xOf (v : ℝ) : ℝ := v / √(2 - v ^ 2)

lemma two_sub_sq_pos' {v : ℝ} (hv : |v| < 1) : (0:ℝ) < 2 - v ^ 2 := by
  obtain ⟨h1, h2⟩ := abs_lt.mp hv; nlinarith

lemma xOf_nonneg {v : ℝ} (hv0 : 0 ≤ v) : 0 ≤ xOf v :=
  div_nonneg hv0 (Real.sqrt_nonneg _)

lemma xOf_sq {v : ℝ} (hv : |v| < 1) : (xOf v) ^ 2 = v ^ 2 / (2 - v ^ 2) := by
  rw [xOf, div_pow, Real.sq_sqrt (two_sub_sq_pos' hv).le]

/-- `xOf` is strictly increasing on `[0,1)`. -/
theorem xOf_strictMonoOn : StrictMonoOn xOf (Ico 0 1) := by
  intro a ha b hb hab
  have hA : |a| < 1 := by rw [abs_of_nonneg ha.1]; exact ha.2
  have hB : |b| < 1 := by rw [abs_of_nonneg hb.1]; exact hb.2
  have h2a : (0:ℝ) < 2 - a ^ 2 := two_sub_sq_pos' hA
  have h2b : (0:ℝ) < 2 - b ^ 2 := two_sub_sq_pos' hB
  have hsq : (xOf a) ^ 2 < (xOf b) ^ 2 := by
    rw [xOf_sq hA, xOf_sq hB, div_lt_div_iff₀ h2a h2b]
    nlinarith [ha.1, hb.1, hab]
  have hna := xOf_nonneg ha.1
  have hnb := xOf_nonneg hb.1
  nlinarith [hsq, hna, hnb]

/-- `xOf (4611/5000) > 43/50`, by rational squaring. -/
theorem xOf_4611_gt : (43:ℝ)/50 < xOf (4611/5000) := by
  have hv : |(4611:ℝ)/5000| < 1 := by rw [abs_of_pos] <;> norm_num
  have h2 : (0:ℝ) < 2 - ((4611:ℝ)/5000) ^ 2 := two_sub_sq_pos' hv
  have hx0 : (0:ℝ) ≤ xOf (4611/5000) := xOf_nonneg (by norm_num)
  have hsq : ((43:ℝ)/50) ^ 2 < (xOf (4611/5000)) ^ 2 := by
    rw [xOf_sq hv, lt_div_iff₀ h2]; norm_num
  nlinarith [hsq, hx0]

/-- `xOf (9701/10000) < 943/1000`, by rational squaring. -/
theorem xOf_9701_lt : xOf (9701/10000) < (943:ℝ)/1000 := by
  have hv : |(9701:ℝ)/10000| < 1 := by rw [abs_of_pos] <;> norm_num
  have h2 : (0:ℝ) < 2 - ((9701:ℝ)/10000) ^ 2 := two_sub_sq_pos' hv
  have hx0 : (0:ℝ) ≤ xOf (9701/10000) := xOf_nonneg (by norm_num)
  have hsq : (xOf (9701/10000)) ^ 2 < ((943:ℝ)/1000) ^ 2 := by
    rw [xOf_sq hv, div_lt_iff₀ h2]; norm_num
  nlinarith [hsq, hx0]

/-- `xOf` really is the inverse of `vOf` on `(-1,1)`: `xOf (vOf x) = x`. -/
theorem xOf_vOf {x : ℝ} (hx : |x| < 1) : xOf (vOf x) = x := by
  have h2 : (0:ℝ) < 2 - (vOf x) ^ 2 := two_sub_sq_pos' (vOf_lt_one hx)
  have hpos : (0:ℝ) < 1 + x ^ 2 := one_add_sq_pos x
  have hs : (0:ℝ) < √(1 + x ^ 2) := sqrt_one_add_sq_pos' x
  have hrw : √(2 - (vOf x) ^ 2) = √2 / √(1 + x ^ 2) := sqrt_two_sub_vOf_sq x
  have hs2 : (√2 : ℝ) ≠ 0 := by positivity
  have hsne : √(1 + x ^ 2) ≠ 0 := hs.ne'
  rw [xOf, hrw, vOf]
  field_simp

/-- **`eq:cstar-maximizer-location` in the `x` coordinate.** -/
theorem x_localization {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1)
    (h : (68743 : ℝ) / 50000 < ratio v) :
    (43:ℝ)/50 < xOf v ∧ xOf v < (943:ℝ)/1000 := by
  obtain ⟨hlo, hhi⟩ := maximizer_localization hv0 hv1 h
  constructor
  · have := xOf_strictMonoOn (a := 4611/5000) (b := v) (by norm_num) ⟨hv0.le, hv1⟩ hlo
    linarith [xOf_4611_gt]
  · have := xOf_strictMonoOn (a := v) (b := 9701/10000) ⟨hv0.le, hv1⟩ (by norm_num) hhi
    linarith [xOf_9701_lt]

/-- **The full `eq:cstar-maximizer-location`.** -/
theorem cstar_maximizer_location {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1)
    (h : (68743 : ℝ) / 50000 < ratio v) :
    (4611:ℝ)/5000 < v ∧ v < (9701:ℝ)/10000 ∧
    (43:ℝ)/50 < xOf v ∧ xOf v < (943:ℝ)/1000 :=
  ⟨(maximizer_localization hv0 hv1 h).1, (maximizer_localization hv0 hv1 h).2,
   (x_localization hv0 hv1 h).1, (x_localization hv0 hv1 h).2⟩

end QipmFormal.ScalarCert
