import QipmFormal.FractionalSDP.Center

/-! # Global optimality of the fractional SDP center

A fixed triangular shear bounds the determinant by the product of three positive
quadratic forms. Applying the scalar logarithm tangent inequality to those forms
proves the supporting inequality directly. Stationarity cancels its affine part;
the equality cases prove uniqueness, including vanishing off-block entries.
Thus the result concerns the actual matrix log determinant on the entire feasible
positive definite slice, without assuming matrix log-determinant concavity.
-/

namespace QipmFormal.FractionalSDP
noncomputable section
open Matrix

/-- The scalar logarithm lies below its tangent, with equality only at tangency. -/
theorem log_tangent {x c : ℝ} (hx : 0 < x) (hc : 0 < c) :
    Real.log x - Real.log c ≤ x / c - 1 ∧
      (Real.log x - Real.log c = x / c - 1 ↔ x = c) := by
  rw [← Real.log_div (ne_of_gt hx) (ne_of_gt hc)]
  constructor
  · exact Real.log_le_sub_one_of_pos (div_pos hx hc)
  · constructor
    · intro h
      by_contra hn
      have hn' : x / c ≠ 1 := by simpa [div_eq_one_iff_eq (ne_of_gt hc)] using hn
      exact (ne_of_lt (Real.log_lt_sub_one_of_pos (div_pos hx hc) hn')) h
    · rintro rfl
      simp [ne_of_gt hc]

private theorem point_quad (x y t e r s z : ℝ) :
    star (![r, s, z] : Fin 3 → ℝ) ⬝ᵥ (point x y t e *ᵥ ![r, s, z]) =
      (1 - y - x) * r ^ 2 + y * s ^ 2 + x * z ^ 2 +
        2 * x * r * s + 2 * t * r * z + 2 * e * s * z := by
  simp [point, Matrix.mulVec, dotProduct, Fin.sum_univ_succ]
  ring

/-- The determinant bound after the fixed shear associated with the center. -/
theorem point_det_shear_bound {x y t e c : ℝ} (hp : (point x y t e).PosDef) :
    0 < 1 - y - x ∧ 0 < x ∧ 0 < y - 2 * c * x + c ^ 2 * (1 - y - x) ∧
    (point x y t e).det ≤ x * (1 - y - x) * (y - 2 * c * x + c ^ 2 * (1 - y - x)) := by
  have hA : 0 < 1 - y - x := by simpa [point] using hp.diag_pos (i := 0)
  have hx : 0 < x := by simpa [point] using hp.diag_pos (i := 2)
  have hv : (![(-c), 1, 0] : Fin 3 → ℝ) ≠ 0 := by
    intro h; have := congrFun h 1; norm_num at this
  have hH := hp.dotProduct_mulVec_pos hv
  rw [point_quad] at hH
  have hQ := hp.posSemidef.dotProduct_mulVec_nonneg (![e, -t, 0] : Fin 3 → ℝ)
  rw [point_quad] at hQ
  refine ⟨hA, hx, by nlinarith, ?_⟩
  have hs := mul_nonneg (le_of_lt hx) (sq_nonneg (x - c * (1 - y - x)))
  simp [point, Matrix.det_fin_three] at *
  nlinarith

/-- Vanishing of the removed determinant term forces both off-block entries to vanish. -/
theorem point_det_eq_block {x y t e : ℝ} (hp : (point x y t e).PosDef)
    (hd : (point x y t e).det = x * ((1 - y - x) * y - x ^ 2)) : t = 0 ∧ e = 0 := by
  by_contra hn
  have hv : (![e, -t, 0] : Fin 3 → ℝ) ≠ 0 := by
    intro h
    have he := congrFun h 0
    have ht := congrFun h 1
    simp only [Fin.isValue, Matrix.cons_val_zero, Pi.zero_apply, Matrix.cons_val_one,
      neg_eq_zero] at he ht
    exact hn ⟨ht, he⟩
  have hQ := hp.dotProduct_mulVec_pos hv
  rw [point_quad] at hQ
  simp [point, Matrix.det_fin_three] at hd
  nlinarith


private theorem shear_trace_identity {a b g q m x y : ℝ}
    (ha : a ≠ 0) (hb : b ≠ 0) (hq : q ≠ 0) (hm : m ≠ 0)
    (htrace : a + g + b = 1) (hdet : q = a * g - b ^ 2)
    (hsb : q = b * (g + 2 * b)) (hsg : q / m = 1 - b - 2 * g) :
    (1 - y - x) / a + (y - 2 * (b / a) * x + (b / a) ^ 2 * (1 - y - x)) / (q / a) + x / b - 3 =
      (y - g) / m := by
  have hag : 1 - b - 2 * g = a - g := by linarith
  have hm' : q = (a - g) * m := by
    simpa [hag] using (div_eq_iff hm).mp hsg
  have hf : (1 - y - x) / a + (y - 2 * (b / a) * x + (b / a) ^ 2 * (1 - y - x)) / (q / a) =
      (g * (1 - y - x) - 2 * b * x + a * y) / q := by
    field_simp
    rw [hdet]
    ring
  have hx : x / b = x * (g + 2 * b) / q := by
    field_simp
    rw [hsb]
    ring
  have hc : g + (a - g) * g = 3 * q := by
    nlinarith [congrArg (fun z : ℝ => z * g) htrace]
  rw [hf, hx]
  calc
    (g * (1 - y - x) - 2 * b * x + a * y) / q + x * (g + 2 * b) / q - 3 =
        ((a - g) * y + g - 3 * q) / q := by field_simp; ring
    _ = ((a - g) * (y - g)) / q := by congr 1; nlinarith [hc]
    _ = (y - g) / m := by field_simp; rw [hm']; ring

/-- Global optimality of a positive stationary center for the actual log determinant.
The equality statement proves uniqueness over the entire positive definite affine slice. -/
theorem stationary_center_optimal {a b g q m x y t e : ℝ}
    (ha : 0 < a) (hb : 0 < b) (hq : 0 < q) (hm : 0 < m)
    (htrace : a + g + b = 1) (hdet : q = a * g - b ^ 2)
    (hsb : q = b * (g + 2 * b)) (hsg : q / m = 1 - b - 2 * g)
    (hp : (point x y t e).PosDef) :
    -Real.log (b * q) + g / m ≤ -Real.log (point x y t e).det + y / m ∧
      (-Real.log (b * q) + g / m = -Real.log (point x y t e).det + y / m ↔
        x = b ∧ y = g ∧ t = 0 ∧ e = 0) := by
  let A := 1 - y - x
  let H := y - 2 * (b / a) * x + (b / a) ^ 2 * A
  obtain ⟨hA, hx, hH, hd⟩ := point_det_shear_bound (c := b / a) hp
  have hD := hp.det_pos
  have hqa := div_pos hq ha
  obtain ⟨lA, eA⟩ := log_tangent hA ha
  obtain ⟨lH, eH⟩ := log_tangent hH hqa
  obtain ⟨lx, ex⟩ := log_tangent hx hb
  have lD := Real.log_le_log hD hd
  have hprod : Real.log (x * A * H) = Real.log x + Real.log A + Real.log H := by
    rw [Real.log_mul (ne_of_gt (mul_pos hx hA)) (ne_of_gt hH),
      Real.log_mul (ne_of_gt hx) (ne_of_gt hA)]
  have hbase : Real.log (b * q) = Real.log b + Real.log a + Real.log (q / a) := by
    rw [Real.log_mul (ne_of_gt hb) (ne_of_gt hq),
      Real.log_div (ne_of_gt hq) (ne_of_gt ha)]
    ring
  have hid := shear_trace_identity (x := x) (y := y) (ne_of_gt ha) (ne_of_gt hb)
    (ne_of_gt hq) (ne_of_gt hm) htrace hdet hsb hsg
  change Real.log (point x y t e).det ≤ Real.log (x * A * H) at lD
  rw [hprod] at lD
  change Real.log A - Real.log a ≤ A / a - 1 at lA
  change Real.log H - Real.log (q / a) ≤ H / (q / a) - 1 at lH
  change A / a + H / (q / a) + x / b - 3 = (y - g) / m at hid
  have hsplit : (y - g) / m = y / m - g / m := by ring
  constructor
  · rw [hbase]
    linarith
  · constructor
    · intro heq
      rw [hbase] at heq
      have hx' : x = b := ex.mp (by linarith)
      have hA' : A = a := eA.mp (by linarith)
      have hy' : y = g := by dsimp [A] at hA'; linarith
      have hH' : H = q / a := eH.mp (by linarith)
      have hlog : Real.log (point x y t e).det = Real.log (x * A * H) := by
        rw [hprod]; linarith
      have hdeq : (point x y t e).det = x * A * H :=
        Real.log_injOn_pos hD (mul_pos (mul_pos hx hA) hH) hlog
      have hblock : (point x y t e).det = x * ((1 - y - x) * y - x ^ 2) := by
        rw [hdeq, hx', hA', hH', hy']
        have hat : 1 - g - b = a := by linarith
        rw [hat, ← hdet]
        field_simp
      obtain ⟨ht, he⟩ := point_det_eq_block hp hblock
      exact ⟨hx', hy', ht, he⟩
    · rintro ⟨hx', hy', ht, he⟩
      rw [hx', hy', ht, he]
      have hdeq : (point b g 0 0).det = b * q := by
        simp [point, Matrix.det_fin_three]
        have hat : 1 - g - b = a := by linarith
        rw [← hat] at hdet
        nlinarith [congrArg (fun z : ℝ => b * z) hdet]
      rw [hdeq]


/-- The rational center is the unique log-barrier minimizer, not merely a stationary point. -/
theorem center_unique_minimizer {r x y t e : ℝ} (hr : 0 < r) (hr1 : r < 1)
    (hp : (point x y t e).PosDef) :
    -Real.log (centerMatrix r).det + g r / mu r ≤
        -Real.log (point x y t e).det + y / mu r ∧
      (-Real.log (centerMatrix r).det + g r / mu r =
        -Real.log (point x y t e).det + y / mu r ↔
        x = b r ∧ y = g r ∧ t = 0 ∧ e = 0) := by
  rw [center_det]
  exact stationary_center_optimal (a_pos hr) (b_pos hr) (q_pos hr) (mu_pos hr hr1)
    (center_trace r) rfl (center_stationary_b r) (center_stationary_g hr hr1) hp


/-- On its objective slice, the same center uniquely maximizes the determinant. -/
theorem center_unique_fixed_gap {r x t e : ℝ} (hr : 0 < r) (hr1 : r < 1)
    (hp : (point x (g r) t e).PosDef) :
    -Real.log (centerMatrix r).det ≤ -Real.log (point x (g r) t e).det ∧
      (-Real.log (centerMatrix r).det = -Real.log (point x (g r) t e).det ↔
        x = b r ∧ t = 0 ∧ e = 0) := by
  have h := center_unique_minimizer hr hr1 hp
  simpa only [add_le_add_iff_right, add_left_inj, true_and] using h


/-- Unique global minimization on the matrix-defined feasible set. -/
theorem center_unique_minimizer_matrix {r : ℝ} (hr : 0 < r) (hr1 : r < 1)
    {X : Matrix (Fin 3) (Fin 3) ℝ} (hX : X.PosDef)
    (htrace : X.trace = 1) (heq : X 2 2 = X 0 1) :
    -Real.log (centerMatrix r).det + g r / mu r ≤ -Real.log X.det + X 1 1 / mu r ∧
      (-Real.log (centerMatrix r).det + g r / mu r =
        -Real.log X.det + X 1 1 / mu r ↔ X = centerMatrix r) := by
  have hcoord := feasible_eq_point hX.isHermitian htrace heq
  have hp : (point (X 0 1) (X 1 1) (X 0 2) (X 1 2)).PosDef := hcoord ▸ hX
  have h := center_unique_minimizer hr hr1 hp
  rw [← hcoord] at h
  refine ⟨h.1, h.2.trans ?_⟩
  constructor
  · rintro ⟨hb, hg, ht, he⟩
    rw [hcoord, hb, hg, ht, he]
    rfl
  · intro hcenter
    rw [hcenter]
    simp [centerMatrix, point]


/-- The full SDP center also belongs to the restricted feasible set. -/
theorem center_restricted_feasible {r : ℝ} (hr : 0 < r) :
    (centerMatrix r).PosDef ∧ (centerMatrix r).trace = 1 ∧
      (centerMatrix r) 2 2 = (centerMatrix r) 0 1 ∧
      (centerMatrix r) 0 2 = 0 ∧ (centerMatrix r) 1 2 = 0 := by
  obtain ⟨hp, htrace, heq⟩ := center_feasible hr
  refine ⟨hp, htrace, heq, ?_, ?_⟩ <;> simp [centerMatrix, point]

/-- The restricted SDP has precisely the same unique log-barrier center. -/
theorem center_unique_minimizer_restricted {r : ℝ} (hr : 0 < r) (hr1 : r < 1)
    {X : Matrix (Fin 3) (Fin 3) ℝ} (hX : X.PosDef)
    (htrace : X.trace = 1) (heq : X 2 2 = X 0 1)
    (_ht : X 0 2 = 0) (_he : X 1 2 = 0) :
    -Real.log (centerMatrix r).det + g r / mu r ≤ -Real.log X.det + X 1 1 / mu r ∧
      (-Real.log (centerMatrix r).det + g r / mu r =
        -Real.log X.det + X 1 1 / mu r ↔ X = centerMatrix r) := by
  exact center_unique_minimizer_matrix hr hr1 hX htrace heq

end
end QipmFormal.FractionalSDP
