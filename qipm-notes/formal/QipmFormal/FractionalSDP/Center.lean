import QipmFormal.FractionalSDP.Defs

/-! Exact interior centers for the fractional SDP. -/
namespace QipmFormal.FractionalSDP
noncomputable section

lemma denom_pos (t : ℝ) : 0 < denom t := by
  unfold denom
  nlinarith [sq_nonneg (t + 1)]

lemma center_trace (t : ℝ) : a t + g t + b t = 1 := by
  unfold a g b
  field_simp [(denom_pos t).ne']
  unfold denom
  ring

lemma a_pos {t : ℝ} (ht : 0 < t) : 0 < a t := by
  exact div_pos (by linarith) (denom_pos t)
lemma b_pos {t : ℝ} (ht : 0 < t) : 0 < b t := by
  exact div_pos ht (denom_pos t)
lemma g_pos {t : ℝ} (ht : 0 < t) : 0 < g t := by
  exact div_pos (sq_pos_of_pos ht) (denom_pos t)

lemma q_formula (t : ℝ) : q t = t ^ 2 * (t + 2) / denom t ^ 2 := by
  unfold q a g b
  field_simp
  ring

lemma q_pos {t : ℝ} (ht : 0 < t) : 0 < q t := by
  rw [q_formula]
  have hd := denom_pos t
  positivity

lemma gap_gradient_formula (t : ℝ) :
    1 - b t - 2 * g t = (3 + t - t ^ 2) / denom t := by
  unfold b g
  field_simp [(denom_pos t).ne']
  unfold denom
  ring

lemma gap_gradient_pos {t : ℝ} (ht : 0 < t) (ht1 : t < 1) :
    0 < 1 - b t - 2 * g t := by
  rw [gap_gradient_formula]
  exact div_pos (by nlinarith [mul_pos ht (sub_pos.mpr ht1)]) (denom_pos t)

lemma mu_pos {t : ℝ} (ht : 0 < t) (ht1 : t < 1) : 0 < mu t := by
  exact div_pos (q_pos ht) (gap_gradient_pos ht ht1)

lemma center_stationary_b (t : ℝ) : q t = b t * (g t + 2 * b t) := by
  unfold q a g b
  field_simp
  ring

lemma center_stationary_g {t : ℝ} (ht : 0 < t) (ht1 : t < 1) :
    q t / mu t = 1 - b t - 2 * g t := by
  unfold mu
  field_simp [(q_pos ht).ne', (gap_gradient_pos ht ht1).ne']

lemma center_root_equation (t : ℝ) :
    3 * b t ^ 2 + 2 * g t * b t + g t ^ 2 - g t = 0 := by
  have h := center_stationary_b t
  have htrace := center_trace t
  unfold q at h
  nlinarith [congrArg (fun x : ℝ => x * g t) htrace]

lemma center_positive_root {t : ℝ} (ht : 0 < t) :
    b t = (-g t + Real.sqrt (3 * g t - 2 * g t ^ 2)) / 3 := by
  have hb := b_pos ht
  have hg := g_pos ht
  have he := center_root_equation t
  have hs : 3 * g t - 2 * g t ^ 2 = (3 * b t + g t) ^ 2 := by
    nlinarith
  rw [hs, Real.sqrt_sq (by positivity)]
  ring

lemma point_det (x y u v : ℝ) :
    (point x y u v).det = x * ((1-y-x)*y-x^2) -
      (y*u^2 - 2*x*u*v + (1-y-x)*v^2) := by
  simp [point, Matrix.det_fin_three]
  ring

lemma center_det (t : ℝ) : (centerMatrix t).det = b t * q t := by
  rw [centerMatrix, point_det]
  have h : 1 - g t - b t = a t := by linarith [center_trace t]
  simp [h, q]

lemma center_det_pos {t : ℝ} (ht : 0 < t) : 0 < (centerMatrix t).det := by
  rw [center_det]
  exact mul_pos (b_pos ht) (q_pos ht)

lemma center_entries (t : ℝ) :
    centerMatrix t = !![a t, b t, 0; b t, g t, 0; 0, 0, b t] := by
  have h : 1 - g t - b t = a t := by linarith [center_trace t]
  simp [centerMatrix, point, h]

lemma center_posDef {t : ℝ} (ht : 0 < t) : (centerMatrix t).PosDef := by
  rw [center_entries]
  apply Matrix.PosDef.of_dotProduct_mulVec_pos
  · ext i j
    fin_cases i <;> fin_cases j <;> simp [Matrix.conjTranspose]
  · intro v hv
    have ha := a_pos ht
    have hb := b_pos ht
    have hq := q_pos ht
    have hid : a t * (v 0)^2 + 2*b t*v 0*v 1 + g t*(v 1)^2 + b t*(v 2)^2 =
        a t * (v 0 + b t / a t * v 1)^2 + q t / a t * (v 1)^2 + b t*(v 2)^2 := by
      unfold q
      field_simp
      ring
    have hnon : 0 ≤ a t * (v 0 + b t / a t * v 1)^2 := mul_nonneg ha.le (sq_nonneg _)
    have hnon1 : 0 ≤ q t / a t * (v 1)^2 := mul_nonneg (div_pos hq ha).le (sq_nonneg _)
    have hnon2 : 0 ≤ b t * (v 2)^2 := mul_nonneg hb.le (sq_nonneg _)
    have hstrict : 0 < a t * (v 0 + b t / a t * v 1)^2 + q t / a t * (v 1)^2 + b t*(v 2)^2 := by
      by_contra h
      have hz1 : v 1 = 0 := by
        have : (v 1)^2 = 0 := by nlinarith [div_pos hq ha]
        nlinarith [sq_nonneg (v 1)]
      have hz2 : v 2 = 0 := by
        have : (v 2)^2 = 0 := by nlinarith
        nlinarith [sq_nonneg (v 2)]
      have hz0 : v 0 = 0 := by
        simp only [hz1, mul_zero, add_zero, zero_pow, ne_eq, OfNat.ofNat_ne_zero,
          not_false_eq_true, hz2] at h
        have : (v 0)^2 = 0 := by nlinarith [sq_nonneg (v 0)]
        exact (sq_eq_zero_iff).mp this
      apply hv
      ext i
      fin_cases i <;> simp [hz0, hz1, hz2]
    have hcalc : dotProduct (star v) (Matrix.mulVec (!![a t, b t, 0; b t, g t, 0; 0, 0, b t]) v) =
        a t * (v 0)^2 + 2*b t*v 0*v 1 + g t*(v 1)^2 + b t*(v 2)^2 := by
      simp [dotProduct, Matrix.mulVec, Fin.sum_univ_succ]
      ring
    rw [hcalc, hid]
    exact hstrict

/-- These coordinates cover every matrix in the affine feasible space. -/
lemma feasible_eq_point {X : Matrix (Fin 3) (Fin 3) ℝ}
    (hX : X.IsHermitian) (htrace : X.trace = 1) (heq : X 2 2 = X 0 1) :
    X = point (X 0 1) (X 1 1) (X 0 2) (X 1 2) := by
  have h10 : X 1 0 = X 0 1 := by simpa using hX.apply 0 1
  have h20 : X 2 0 = X 0 2 := by simpa using hX.apply 0 2
  have h21 : X 2 1 = X 1 2 := by simpa using hX.apply 1 2
  have h00 : X 0 0 = 1 - X 1 1 - X 0 1 := by
    simp [Matrix.trace, Matrix.diag, Fin.sum_univ_succ, heq] at htrace
    linarith
  ext i j
  fin_cases i <;> fin_cases j <;> simp [point, h00, h10, h20, h21, heq]

lemma point_trace (x y u v : ℝ) : (point x y u v).trace = 1 := by
  simp [point, Matrix.trace, Matrix.diag, Fin.sum_univ_succ]

lemma center_feasible {t : ℝ} (ht : 0 < t) :
    (centerMatrix t).PosDef ∧ (centerMatrix t).trace = 1 ∧
      centerMatrix t 2 2 = centerMatrix t 0 1 := by
  exact ⟨center_posDef ht, point_trace _ _ _ _, rfl⟩

end
end QipmFormal.FractionalSDP
