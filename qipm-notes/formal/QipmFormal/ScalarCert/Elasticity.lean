import QipmFormal.ScalarCert.Inverse

/-!
# Elasticity `E` and the coefficient `K`

In the `v` coordinate the paper's elasticity `E(y) = y p'(y)/p(y)` and its
companion `K(y)` are

  `E v = Y v / v`,   `K v = Y v ^ 2 * (1 - v^2) * (2 - v^2) / (2 * v^2)`.

With `B v = √2 * v / √((1 - v²)(2 - v²))` one has `K = (Y/B)^2`, so the
appendix facts `E ≥ 1` and `0 < K < 1` are exactly `v < Y v` and `Y v < B v`.
-/

namespace QipmFormal.ScalarCert

open Real Set

/-! ### The derivative of `artanh` -/

/-- `artanh` is differentiable on `(-1,1)` with derivative `1/(1-x²)`. -/
theorem hasDerivAt_artanh {x : ℝ} (hx : |x| < 1) :
    HasDerivAt artanh (1 / (1 - x ^ 2)) x := by
  obtain ⟨h1, h2⟩ := abs_lt.mp hx
  have hne1 : (1 : ℝ) + x ≠ 0 := by linarith
  have hne2 : (1 : ℝ) - x ≠ 0 := by linarith
  have hA : HasDerivAt (fun y : ℝ => log (1 + y)) (1 / (1 + x)) x := by
    have h := ((hasDerivAt_id x).const_add (1 : ℝ)).log hne1
    simpa using h
  have hB : HasDerivAt (fun y : ℝ => log (1 - y)) (-1 / (1 - x)) x := by
    have h := ((hasDerivAt_id x).const_sub (1 : ℝ)).log hne2
    simpa using h
  have key : HasDerivAt (fun y : ℝ => 1 / 2 * (log (1 + y) - log (1 - y)))
      (1 / (1 - x ^ 2)) x := by
    have h := (hA.sub hB).const_mul (1 / 2 : ℝ)
    have hpos : (0 : ℝ) < 1 - x ^ 2 := by nlinarith
    have hval : (1 : ℝ) / 2 * (1 / (1 + x) - -1 / (1 - x)) = 1 / (1 - x ^ 2) := by
      field_simp
      ring
    rw [hval] at h
    simpa using h
  refine key.congr_of_eventuallyEq ?_
  filter_upwards [Ioo_mem_nhds h1 h2] with y hy
  obtain ⟨hy1, hy2⟩ := hy
  rw [artanh_eq_half_log ⟨hy1.le, hy2.le⟩,
    Real.log_div (by linarith) (by linarith)]

/-! ### The derivative of `Y` -/

lemma sqrt_two_pos : (0 : ℝ) < √2 := Real.sqrt_pos.mpr (by norm_num)

lemma abs_div_sqrt_two_lt_one {v : ℝ} (hv : |v| < 1) : |v / √2| < 1 := by
  rw [abs_div, abs_of_pos sqrt_two_pos, div_lt_one sqrt_two_pos]
  calc |v| < 1 := hv
    _ ≤ √2 := by
        rw [show (1 : ℝ) = √1 by simp]
        exact Real.sqrt_le_sqrt (by norm_num)

/-- `Y' v = 2 / ((1 - v²)(2 - v²))` on `(-1,1)`. -/
theorem Y_deriv {v : ℝ} (hv : |v| < 1) :
    HasDerivAt Y (2 / ((1 - v ^ 2) * (2 - v ^ 2))) v := by
  have hs2 : (0 : ℝ) < √2 := sqrt_two_pos
  have hsq2 : (√2 : ℝ) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have h1 : (0 : ℝ) < 1 - v ^ 2 := one_sub_sq_pos hv
  have h2 : (0 : ℝ) < 2 - v ^ 2 := by nlinarith
  have hw : |v / √2| < 1 := abs_div_sqrt_two_lt_one hv
  have hinner : HasDerivAt (fun y : ℝ => y / √2) (1 / √2) v := by
    simpa using (hasDerivAt_id v).div_const (√2)
  have hA : HasDerivAt (fun y : ℝ => 2 * artanh y) (2 * (1 / (1 - v ^ 2))) v :=
    (hasDerivAt_artanh hv).const_mul 2
  have hB0 : HasDerivAt (fun y : ℝ => artanh (y / √2))
      (1 / (1 - (v / √2) ^ 2) * (1 / √2)) v := by
    have h := (hasDerivAt_artanh hw).comp v hinner
    rwa [Function.comp_def] at h
  have hB : HasDerivAt (fun y : ℝ => √2 * artanh (y / √2))
      (√2 * (1 / (1 - (v / √2) ^ 2) * (1 / √2))) v := hB0.const_mul (√2)
  have h := hA.sub hB
  have hval : 2 * (1 / (1 - v ^ 2)) - √2 * (1 / (1 - (v / √2) ^ 2) * (1 / √2))
      = 2 / ((1 - v ^ 2) * (2 - v ^ 2)) := by
    have hd : (v / √2) ^ 2 = v ^ 2 / 2 := by
      rw [div_pow, hsq2]
    rw [hd]
    have h3 : (1 : ℝ) - v ^ 2 / 2 = (2 - v ^ 2) / 2 := by ring
    rw [h3]
    field_simp
    ring
  rw [hval] at h
  exact h

/-! ### `v < Y v` -/

/-- Strict lower bound `v < Y v` on `(0,1)`, from the `k = 0` term of the series. -/
theorem lt_Y {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : v < Y v := by
  have habs : |v| < 1 := by rwa [abs_of_pos hv0]
  have hpart := partial_le_Y hv0.le habs 2
  have hsum : ∑ k ∈ Finset.range 2, term v k = v + v ^ 3 / 2 := by
    simp [Finset.sum_range_succ, term]
    ring
  rw [hsum] at hpart
  have : (0 : ℝ) < v ^ 3 / 2 := by positivity
  linarith

/-! ### The comparison function `B` -/

/-- `B v = √2 v / √((1 - v²)(2 - v²))`; it satisfies `K = (Y/B)²`. -/
noncomputable def B (v : ℝ) : ℝ := √2 * v / √((1 - v ^ 2) * (2 - v ^ 2))

lemma G_pos {v : ℝ} (hv : |v| < 1) : (0 : ℝ) < (1 - v ^ 2) * (2 - v ^ 2) := by
  have h1 : (0 : ℝ) < 1 - v ^ 2 := one_sub_sq_pos hv
  have h2 : (0 : ℝ) < 2 - v ^ 2 := by nlinarith
  positivity

lemma sqrtG_pos {v : ℝ} (hv : |v| < 1) : (0 : ℝ) < √((1 - v ^ 2) * (2 - v ^ 2)) :=
  Real.sqrt_pos.mpr (G_pos hv)

lemma sq_sqrtG {v : ℝ} (hv : |v| < 1) :
    √((1 - v ^ 2) * (2 - v ^ 2)) ^ 2 = (1 - v ^ 2) * (2 - v ^ 2) :=
  Real.sq_sqrt (G_pos hv).le

@[simp] lemma B_zero : B 0 = 0 := by simp [B]

/-- `B' v = √2 (2 - v⁴) / ((1-v²)(2-v²))^{3/2}`, the `3/2` power written as
`((1-v²)(2-v²)) * √((1-v²)(2-v²))`. -/
theorem B_deriv {v : ℝ} (hv : |v| < 1) :
    HasDerivAt B
      (√2 * (2 - v ^ 4) /
        (((1 - v ^ 2) * (2 - v ^ 2)) * √((1 - v ^ 2) * (2 - v ^ 2)))) v := by
  have hG : (0 : ℝ) < (1 - v ^ 2) * (2 - v ^ 2) := G_pos hv
  have hs : (0 : ℝ) < √((1 - v ^ 2) * (2 - v ^ 2)) := sqrtG_pos hv
  have hsq : √((1 - v ^ 2) * (2 - v ^ 2)) ^ 2 = (1 - v ^ 2) * (2 - v ^ 2) := sq_sqrtG hv
  -- derivative of the inside `G`
  have hGd : HasDerivAt (fun y : ℝ => (1 - y ^ 2) * (2 - y ^ 2))
      (-6 * v + 4 * v ^ 3) v := by
    have h1 : HasDerivAt (fun y : ℝ => 1 - y ^ 2) (-(2 * v)) v := by
      simpa using ((hasDerivAt_pow 2 v)).const_sub (1 : ℝ)
    have h2 : HasDerivAt (fun y : ℝ => 2 - y ^ 2) (-(2 * v)) v := by
      simpa using ((hasDerivAt_pow 2 v)).const_sub (2 : ℝ)
    exact (h1.mul h2).congr_deriv (by ring)
  -- derivative of `√G`
  have hsd : HasDerivAt (fun y : ℝ => √((1 - y ^ 2) * (2 - y ^ 2)))
      ((-6 * v + 4 * v ^ 3) / (2 * √((1 - v ^ 2) * (2 - v ^ 2)))) v := by
    have h := (Real.hasDerivAt_sqrt hG.ne').comp v hGd
    rw [Function.comp_def] at h
    exact h.congr_deriv (by ring)
  -- derivative of the numerator
  have hnd : HasDerivAt (fun y : ℝ => √2 * y) (√2) v := by
    simpa using (hasDerivAt_id v).const_mul (√2)
  have h := hnd.div hsd hs.ne'
  have hval :
      (√2 * √((1 - v ^ 2) * (2 - v ^ 2)) -
          √2 * v * ((-6 * v + 4 * v ^ 3) / (2 * √((1 - v ^ 2) * (2 - v ^ 2))))) /
        √((1 - v ^ 2) * (2 - v ^ 2)) ^ 2
      = √2 * (2 - v ^ 4) /
          (((1 - v ^ 2) * (2 - v ^ 2)) * √((1 - v ^ 2) * (2 - v ^ 2))) := by
    rw [div_eq_div_iff (by positivity) (by positivity)]
    field_simp
    nlinarith [hsq, hs, Real.sq_sqrt (show (0:ℝ) ≤ 2 by norm_num)]
  rw [hval] at h
  exact h

/-! ### `Y v < B v` on `(0,1)` -/

/-- The polynomial inequality behind `B' > Y'`: `v⁸ - 6v⁴ + 6v² > 0` on `(0,1)`. -/
lemma poly_pos {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) :
    (0 : ℝ) < v ^ 8 - 6 * v ^ 4 + 6 * v ^ 2 := by
  have h6 : (0 : ℝ) < v ^ 6 - 6 * v ^ 2 + 6 := by
    nlinarith [pow_nonneg hv0.le 6, sq_nonneg v]
  have hm := mul_pos (pow_pos hv0 2) h6
  nlinarith [hm]

/-- `B' > Y'` on `(0,1)`. -/
lemma Y_deriv_lt_B_deriv {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) :
    2 / ((1 - v ^ 2) * (2 - v ^ 2))
      < √2 * (2 - v ^ 4) /
          (((1 - v ^ 2) * (2 - v ^ 2)) * √((1 - v ^ 2) * (2 - v ^ 2))) := by
  have habs : |v| < 1 := by rwa [abs_of_pos hv0]
  have hG : (0 : ℝ) < (1 - v ^ 2) * (2 - v ^ 2) := G_pos habs
  have hs : (0 : ℝ) < √((1 - v ^ 2) * (2 - v ^ 2)) := sqrtG_pos habs
  have hs2 : (0 : ℝ) < √2 := sqrt_two_pos
  have hs2sq : (√2 : ℝ) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hv4 : (0 : ℝ) < 2 - v ^ 4 := by
    have : v ^ 4 < 1 := pow_lt_one₀ hv0.le hv1 (by norm_num)
    linarith
  have hc : (0 : ℝ) < √2 * (2 - v ^ 4) / 2 := by positivity
  have hkey : 2 * √((1 - v ^ 2) * (2 - v ^ 2)) < √2 * (2 - v ^ 4) := by
    have hlt : √((1 - v ^ 2) * (2 - v ^ 2)) < √2 * (2 - v ^ 4) / 2 := by
      rw [Real.sqrt_lt' hc]
      have hsq : (√2 * (2 - v ^ 4) / 2) ^ 2 = (2 - v ^ 4) ^ 2 / 2 := by
        have : (√2 * (2 - v ^ 4) / 2) ^ 2 = (√2) ^ 2 * (2 - v ^ 4) ^ 2 / 4 := by ring
        rw [this, hs2sq]; ring
      rw [hsq]
      nlinarith [poly_pos hv0 hv1]
    linarith
  rw [div_lt_div_iff₀ hG (by positivity)]
  nlinarith [mul_lt_mul_of_pos_right hkey hG]

/-- `Y v < B v` on `(0,1)`: both vanish at `0` and `B` grows faster. -/
theorem Y_lt_B {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : Y v < B v := by
  have hmono : StrictMonoOn (fun y : ℝ => B y - Y y) (Ico (0 : ℝ) 1) := by
    refine strictMonoOn_of_deriv_pos (convex_Ico 0 1) ?_ ?_
    · intro x hx
      have habs : |x| < 1 := by rw [abs_of_nonneg hx.1]; exact hx.2
      exact ((B_deriv habs).sub (Y_deriv habs)).continuousAt.continuousWithinAt
    · intro x hx
      rw [interior_Ico] at hx
      have habs : |x| < 1 := by rw [abs_of_pos hx.1]; exact hx.2
      have hd : HasDerivAt (fun y : ℝ => B y - Y y)
          (√2 * (2 - x ^ 4) /
              (((1 - x ^ 2) * (2 - x ^ 2)) * √((1 - x ^ 2) * (2 - x ^ 2)))
            - 2 / ((1 - x ^ 2) * (2 - x ^ 2))) x :=
        (B_deriv habs).sub (Y_deriv habs)
      rw [hd.deriv]
      have := Y_deriv_lt_B_deriv hx.1 hx.2
      linarith
  have h0 : (0 : ℝ) ∈ Ico (0 : ℝ) 1 := ⟨le_refl 0, one_pos⟩
  have hv : v ∈ Ico (0 : ℝ) 1 := ⟨hv0.le, hv1⟩
  have := hmono h0 hv hv0
  simp only [B_zero, Y_zero, sub_zero] at this
  linarith

/-! ### `K` and `E` -/

/-- `K v = Y v² (1 - v²)(2 - v²) / (2 v²)`, the `v`-coordinate form of `K(y)`. -/
noncomputable def K (v : ℝ) : ℝ := Y v ^ 2 * (1 - v ^ 2) * (2 - v ^ 2) / (2 * v ^ 2)

/-- `E v = Y v / v`, the `v`-coordinate form of the elasticity `y p'(y)/p(y)`. -/
noncomputable def E (v : ℝ) : ℝ := Y v / v

lemma B_sq {v : ℝ} (hv : |v| < 1) :
    B v ^ 2 = 2 * v ^ 2 / ((1 - v ^ 2) * (2 - v ^ 2)) := by
  rw [B, div_pow, sq_sqrtG hv, mul_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]

/-- `K = (Y/B)²`, so `0 < K < 1` is exactly `0 < Y < B`. -/
theorem K_pos_lt_one {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : 0 < K v ∧ K v < 1 := by
  have habs : |v| < 1 := by rwa [abs_of_pos hv0]
  have hG : (0 : ℝ) < (1 - v ^ 2) * (2 - v ^ 2) := G_pos habs
  have h1 : (0 : ℝ) < 1 - v ^ 2 := one_sub_sq_pos habs
  have h2 : (0 : ℝ) < 2 - v ^ 2 := by nlinarith
  have hY : 0 < Y v := Y_pos hv0 hv1
  refine ⟨?_, ?_⟩
  · rw [K]
    exact div_pos (mul_pos (mul_pos (pow_pos hY 2) h1) h2) (by positivity)
  · rw [K, div_lt_one (by positivity)]
    have hsq : Y v ^ 2 < 2 * v ^ 2 / ((1 - v ^ 2) * (2 - v ^ 2)) := by
      rw [← B_sq habs]
      nlinarith [Y_lt_B hv0 hv1, hY]
    rw [lt_div_iff₀ hG] at hsq
    nlinarith [hsq]

/-- The elasticity exceeds `1` on `(0,1)`. -/
theorem one_lt_E {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : 1 < E v := by
  rw [E, lt_div_iff₀ hv0]
  simpa using lt_Y hv0 hv1

/-- The appendix's `E ≥ 1`. -/
theorem one_le_E {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : 1 ≤ E v :=
  (one_lt_E hv0 hv1).le

end QipmFormal.ScalarCert
