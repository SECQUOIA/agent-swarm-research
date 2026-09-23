import QipmFormal.ScalarCert.Upper

/-!
# The sharpened elasticity bound `K < 107/200` on `E > 2`

This is the step `K < G(4/5) < 107/200` of `appendix-scalar-certificate.tex`.

Writing `L = log K` one has

  `K'/K = 2 Y'/Y - 2v/(1-v²) - 2v/(2-v²) - 2/v`,

and substituting `Y' = 2/((1-v²)(2-v²))` and multiplying by the positive factor
`v(1-v²)(2-v²)/2` turns `K' < 0` into

  `2v / Y v < 2 - v⁴`,   i.e.   `E v > 2/(2 - v⁴)`,

using `v²(2-v²) + v²(1-v²) + (1-v²)(2-v²) = 2 - v⁴`.  Concretely
`deriv K v = (4 v Y v - 2 Y v ² (2 - v⁴)) / (2 v³)` (`K_hasDerivAt`).

The sign condition is verified on `(v₂, 1)` by splitting at `v₃ = 9/10`:
below `v₃` the elasticity already exceeds `99/50` while `2/(2-v⁴) ≤ 2/(2-v₃⁴)
< 1.49`; above `v₃` the elasticity exceeds `2` while `2/(2-v⁴) < 2`.  Hence `K`
is strictly decreasing on `[v₂, 1)`, and `K v₂ < 107/200` finishes.
-/

namespace QipmFormal.ScalarCert

open Real Set

set_option exponentiation.threshold 100000

/-! ### The splitting point `v₃ = 9/10` -/

/-- `v₃ = 9/10`, the point where the two halves of the sign argument meet. -/
noncomputable def v3 : ℝ := 9 / 10

lemma v3_pos : 0 < v3 := by rw [v3]; norm_num
lemma v3_lt_one : v3 < 1 := by rw [v3]; norm_num
lemma v3_cast : v3 = ((9 : ℕ) : ℝ) / ((10 : ℕ) : ℝ) := by rw [v3]; norm_num

/-! ### Two certified lower bounds on `Y`

Scale `10²⁰`, `61` series terms.  Partial sums are already lower bounds for `Y`,
so no tail estimate is needed. -/

set_option maxRecDepth 1000000 in
theorem accLo_v3 : accLo (9 * 9) (10 * 10) (10 ^ 20) 0 60
    = 208979810895530856878 := by decide

set_option maxRecDepth 1000000 in
theorem accLo_v2 : accLo (177 * 177) (200 * 200) (10 ^ 20) 0 60
    = 198650885411520056568 := by decide

/-- `Y v₃ ≥ 2 v₃`, i.e. `E v₃ ≥ 2`.  (The certified lower bound is `v₃ · accLo_v3 = 1.88081829…`;
    the true value is `1.8808184873…`.) -/
theorem Y_v3_ge : 2 * v3 ≤ Y v3 := by
  have h := Y_ge_accLo (a := 9) (b := 10) (s := 10 ^ 20) (z := v3)
    v3_cast (by norm_num) (by norm_num) (by norm_num) 60
  rw [accLo_v3] at h
  push_cast at h
  have hrat : 2 * v3 ≤ v3 * (208979810895530856878 / 10 ^ 20) := by
    rw [v3]; norm_num
  linarith

/-- `Y v₂ ≥ (99/50) v₂`, i.e. `E v₂ ≥ 1.98`.
    (The certified lower bound is `v₂ · accLo_v2 = 1.75806033…`;
    the true value is `1.7580603571…`.) -/
theorem Y_v2_ge : 99 / 50 * v2 ≤ Y v2 := by
  have h := Y_ge_accLo (a := 177) (b := 200) (s := 10 ^ 20) (z := v2)
    v2_cast (by norm_num) (by norm_num) (by norm_num) 60
  rw [accLo_v2] at h
  push_cast at h
  have hrat : 99 / 50 * v2 ≤ v2 * (198650885411520056568 / 10 ^ 20) := by
    rw [v2]; norm_num
  linarith

/-! ### Step A: the sign condition `E v > 2/(2 - v⁴)` on `(v₂, 1)` -/

/-- The sign condition behind `K' < 0`, in the cleared form `2 v < Y v (2 - v⁴)`. -/
theorem two_mul_lt_Y_mul {v : ℝ} (hv : v2 < v) (hv1 : v < 1) :
    2 * v < Y v * (2 - v ^ 4) := by
  have hv0 : 0 < v := v2_pos.trans hv
  have hv4 : v ^ 4 < 1 := pow_lt_one₀ hv0.le hv1 (by norm_num)
  have hY0 : 0 < Y v := Y_pos hv0 hv1
  rcases le_or_gt v v3 with hle | hgt
  · -- below `v₃`: `E v > 99/50` and `2 - v⁴ ≥ 2 - v₃⁴ = 1.3439`
    have hE : E v2 < E v := E_strictMonoOn ⟨v2_pos, v2_lt_one⟩ ⟨hv0, hv1⟩ hv
    have hEv2 : (99 : ℝ) / 50 ≤ E v2 := by
      rw [E, le_div_iff₀ v2_pos]
      linarith [Y_v2_ge]
    have hYv : 99 / 50 * v < Y v := by
      have : (99 : ℝ) / 50 < E v := lt_of_le_of_lt hEv2 hE
      rw [E, lt_div_iff₀ hv0] at this
      linarith
    have hpow : v ^ 4 ≤ v3 ^ 4 := pow_le_pow_left₀ hv0.le hle 4
    have hv34 : v3 ^ 4 = 6561 / 10000 := by rw [v3]; norm_num
    rw [hv34] at hpow
    nlinarith [hYv, hv0, hpow]
  · -- above `v₃`: `E v ≥ 2` and `2 - v⁴ > 1`
    have hE : E v3 < E v := E_strictMonoOn ⟨v3_pos, v3_lt_one⟩ ⟨hv0, hv1⟩ hgt
    have hEv3 : (2 : ℝ) ≤ E v3 := by
      rw [E, le_div_iff₀ v3_pos]
      linarith [Y_v3_ge]
    have hYv : 2 * v < Y v := by
      have : (2 : ℝ) < E v := lt_of_le_of_lt hEv3 hE
      rw [E, lt_div_iff₀ hv0] at this
      linarith
    nlinarith [hY0, hv4, hYv]

/-! ### Step B: `K` is strictly decreasing on `[v₂, 1)` -/

/-- `K' v = (4 v Y v - 2 Y v² (2 - v⁴)) / (2 v³)` on `(0,1)`. -/
theorem K_hasDerivAt {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) :
    HasDerivAt K ((4 * v * Y v - 2 * Y v ^ 2 * (2 - v ^ 4)) / (2 * v ^ 3)) v := by
  have habs : |v| < 1 := by rwa [abs_of_pos hv0]
  have h1 : (0 : ℝ) < 1 - v ^ 2 := one_sub_sq_pos habs
  have h2 : (0 : ℝ) < 2 - v ^ 2 := by nlinarith
  have hYd := Y_deriv habs
  have hY2 : HasDerivAt (fun y : ℝ => Y y ^ 2)
      ((2 : ℕ) * Y v ^ (2 - 1) * (2 / ((1 - v ^ 2) * (2 - v ^ 2)))) v := hYd.pow 2
  have ha : HasDerivAt (fun y : ℝ => 1 - y ^ 2) (-(2 * v)) v := by
    simpa using (hasDerivAt_pow 2 v).const_sub (1 : ℝ)
  have hb : HasDerivAt (fun y : ℝ => 2 - y ^ 2) (-(2 * v)) v := by
    simpa using (hasDerivAt_pow 2 v).const_sub (2 : ℝ)
  have hD : HasDerivAt (fun y : ℝ => 2 * y ^ 2) (4 * v) v :=
    ((hasDerivAt_pow 2 v).const_mul (2 : ℝ)).congr_deriv (by push_cast; ring)
  have hDne : (2 : ℝ) * v ^ 2 ≠ 0 := by positivity
  have h := ((hY2.mul ha).mul hb).div hD hDne
  have hK : K = fun y : ℝ => Y y ^ 2 * (1 - y ^ 2) * (2 - y ^ 2) / (2 * y ^ 2) := rfl
  rw [hK]
  refine h.congr_deriv ?_
  have h1' : (1 : ℝ) - v ^ 2 ≠ 0 := h1.ne'
  have h2' : (2 : ℝ) - v ^ 2 ≠ 0 := h2.ne'
  have hv0' : v ≠ 0 := hv0.ne'
  simp only [Pi.mul_apply]
  push_cast
  field_simp
  ring

/-- `K` is strictly decreasing on `[v₂, 1)`. -/
theorem K_strictAntiOn : StrictAntiOn K (Ico v2 1) := by
  refine strictAntiOn_of_deriv_neg (convex_Ico _ _) ?_ ?_
  · intro x hx
    have hx0 : 0 < x := lt_of_lt_of_le v2_pos hx.1
    exact (K_hasDerivAt hx0 hx.2).continuousAt.continuousWithinAt
  · intro x hx
    rw [interior_Ico] at hx
    have hx0 : 0 < x := v2_pos.trans hx.1
    rw [(K_hasDerivAt hx0 hx.2).deriv]
    have hY0 : 0 < Y x := Y_pos hx0 hx.2
    have hkey := two_mul_lt_Y_mul hx.1 hx.2
    refine div_neg_of_neg_of_pos ?_ (by positivity)
    nlinarith [mul_pos hY0 (sub_pos.mpr hkey)]

/-! ### Step C: `K v₂ < 107/200` -/

/-- The raw ceiling enclosure of `Upper.lean`, restated. -/
lemma Y_v2_upper_raw :
    Y v2 ≤ v2 * (198650845420592013062 / 10 ^ 20) + 1 / 10 ^ 6 := by
  have h := Y_le_accHi (a := 177) (b := 200) (s := 10 ^ 20) (z := v2)
    v2_cast (by norm_num) (by norm_num) (by norm_num) 49
  rw [accHi_v2] at h
  have ht := tail_v2
  push_cast at h ht
  linarith

/-- `K v₂ < 107/200`.  (The certified upper bound is `0.5204401659…`;
    the true value is `0.5204397960…`.) -/
theorem K_v2_lt : K v2 < 107 / 200 := by
  have hY0 : 0 < Y v2 := Y_pos v2_pos v2_lt_one
  have hsq : Y v2 ^ 2
      ≤ (v2 * (198650845420592013062 / 10 ^ 20) + 1 / 10 ^ 6) ^ 2 :=
    pow_le_pow_left₀ hY0.le Y_v2_upper_raw 2
  have h1 : (0 : ℝ) ≤ 1 - v2 ^ 2 := by rw [v2]; norm_num
  have h2 : (0 : ℝ) ≤ 2 - v2 ^ 2 := by rw [v2]; norm_num
  have step := mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_right hsq h1) h2
  have final : (v2 * (198650845420592013062 / 10 ^ 20) + 1 / 10 ^ 6) ^ 2
      * (1 - v2 ^ 2) * (2 - v2 ^ 2) < 107 / 200 * (2 * v2 ^ 2) := by
    rw [v2]; norm_num
  rw [K, div_lt_iff₀ (show (0 : ℝ) < 2 * v2 ^ 2 by rw [v2]; norm_num)]
  linarith

/-! ### Step D: the sharpened bound -/

/-- **The sharpened elasticity bound.**  On the appendix's region `E > 2`,
`K < 107/200`. -/
theorem K_lt {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) (hE : 2 < E v) : K v < 107 / 200 := by
  have hlt : v2 < v := lt_of_two_lt_E hv0 hv1 hE
  have hmem2 : v2 ∈ Ico v2 1 := Set.left_mem_Ico.mpr v2_lt_one
  have hmem : v ∈ Ico v2 1 := ⟨hlt.le, hv1⟩
  have := K_strictAntiOn hmem2 hmem hlt
  linarith [K_v2_lt]

end QipmFormal.ScalarCert
