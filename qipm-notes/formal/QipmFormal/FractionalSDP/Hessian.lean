import QipmFormal.FractionalSDP.Defs
import QipmFormal.FractionalSDP.HessianCalculus

namespace QipmFormal.FractionalSDP
noncomputable section
open Matrix

/-- Squared Frobenius norm, without a choice of tangent coordinates. -/
def frobeniusSq (X : Matrix (Fin 3) (Fin 3) ℝ) : ℝ :=
  ∑ i, ∑ j, (X i j) ^ 2

theorem tangent_frobeniusSq (u v w z : ℝ) :
    frobeniusSq (tangent u v w z) =
      4 * u ^ 2 + 2 * u * v + 2 * v ^ 2 + 2 * w ^ 2 + 2 * z ^ 2 := by
  simp [frobeniusSq, tangent, Fin.sum_univ_succ]
  ring

/-- These four coordinates describe the entire equality - constrained tangent space. -/
theorem tangent_characterization (X : Matrix (Fin 3) (Fin 3) ℝ) :
    X.IsSymm ∧ X.trace = 0 ∧ X 2 2 = X 0 1 ↔
      ∃ u v w z, X = tangent u v w z := by
  constructor
  · rintro ⟨hs, ht, he⟩
    refine ⟨X 0 1, X 1 1, X 0 2, X 1 2, ?_⟩
    have hsym (i j : Fin 3) : X j i = X i j := congrFun (congrFun hs i) j
    have htrace : X 0 0 + X 1 1 + X 2 2 = 0 := by
      simpa [Matrix.trace, Fin.sum_univ_succ, add_assoc] using ht
    ext i j
    fin_cases i <;> fin_cases j
    · change X 0 0 = -X 1 1 - X 0 1
      linarith
    · rfl
    · rfl
    · exact hsym 0 1
    · rfl
    · rfl
    · exact hsym 0 2
    · exact hsym 1 2
    · exact he
  · rintro ⟨u, v, w, z, rfl⟩
    refine ⟨?_, ?_, by simp [tangent]⟩
    · ext i j
      fin_cases i <;> fin_cases j <;> simp [tangent, Matrix.transpose_apply]
    · simp [Matrix.trace, tangent, Fin.sum_univ_succ]

theorem restricted_tangent_characterization (X : Matrix (Fin 3) (Fin 3) ℝ) :
    X.IsSymm ∧ X.trace = 0 ∧ X 2 2 = X 0 1 ∧ X 0 2 = 0 ∧ X 1 2 = 0 ↔
      ∃ u v, X = tangent u v 0 0 := by
  constructor
  · rintro ⟨hs, ht, he, hw, hz⟩
    obtain ⟨u, v, w, z, hX⟩ := (tangent_characterization X).mp ⟨hs, ht, he⟩
    subst X
    change w = 0 at hw
    change z = 0 at hz
    exact ⟨u, v, by rw [hw, hz]⟩
  · rintro ⟨u, v, rfl⟩
    obtain ⟨hs, ht, he⟩ := (tangent_characterization (tangent u v 0 0)).mpr
      ⟨u, v, 0, 0, rfl⟩
    exact ⟨hs, ht, he, by simp [tangent], by simp [tangent]⟩

/-- The determinant along an arbitrary feasible line is an explicit cubic. -/
theorem determinant_tangent_line (B G u v w z s : ℝ) :
    (point B G 0 0 + s • tangent u v w z).det =
    cubic (B * ((1 - G - B) * G - B ^ 2))
      (u * ((1 - G - B) * G - B ^ 2) + B * ((-G - 2 * B) * u + (1 - B - 2 * G) * v))
      (u * ((-G - 2 * B) * u + (1 - B - 2 * G) * v) + B * (-u ^ 2 - u * v - v ^ 2)
        -G * w ^ 2 + 2 * B * w * z - (1 - G - B) * z ^ 2)
      (u * (-u ^ 2 - u * v - v ^ 2) - v * w ^ 2 + 2 * u * w * z + (u + v) * z ^ 2) s := by
  simp [Matrix.det_fin_three, point, tangent, cubic]
  ring

/-- The exact log-determinant Hessian on the feasible tangent space. -/
theorem point_logdet_second (B G u v w z : ℝ) (hB : B ≠ 0)
    (hQ : (1 - G - B) * G - B ^ 2 ≠ 0) :
    HasDerivAt
      (deriv (fun s : ℝ => -Real.log ((point B G 0 0 + s • tangent u v w z).det)))
      ((B⁻¹ ^ 2 + (-G - 2 * B) ^ 2 / ((1 - G - B) * G - B ^ 2) ^ 2
          + 2 / ((1 - G - B) * G - B ^ 2)) * u ^ 2
        + 2 * ((-G - 2 * B) * (1 - B - 2 * G) / ((1 - G - B) * G - B ^ 2) ^ 2
          + 1 / ((1 - G - B) * G - B ^ 2)) * u * v
        + ((1 - B - 2 * G) ^ 2 / ((1 - G - B) * G - B ^ 2) ^ 2
          + 2 / ((1 - G - B) * G - B ^ 2)) * v ^ 2
        + 2 / (B * ((1 - G - B) * G - B ^ 2)) *
          (G * w ^ 2 - 2 * B * w * z + (1 - G - B) * z ^ 2)) 0 := by
  simp_rw [determinant_tangent_line]
  convert cubic_second_log _ _ _ _ (mul_ne_zero hB hQ) using 1
  generalize hQdef : ((1 - G - B) * G - B ^ 2) = Q at *
  field_simp [hB, hQ]
  rw [← hQdef]
  ring

theorem a_eq_one_sub_g_sub_b (t : ℝ) : a t = 1 - g t - b t := by
  have hd : denom t ≠ 0 := by
    unfold denom
    nlinarith [sq_nonneg (t + 1)]
  unfold a g b
  field_simp
  unfold denom
  ring

/-- At the actual central matrix, the coordinate quadratic form is the second
line derivative of the log-determinant barrier, not an assumed Hessian. -/
theorem center_logdet_second (t u v w z : ℝ) (hB : b t ≠ 0) (hQ : q t ≠ 0) :
    HasDerivAt
      (deriv (fun s : ℝ => -Real.log ((centerMatrix t + s • tangent u v w z).det)))
      (k00 t * u ^ 2 + 2 * k01 t * u * v + k11 t * v ^ 2
        + 2 / (b t * q t) * (g t * w ^ 2 - 2 * b t * w * z + a t * z ^ 2)) 0 := by
  have hq : q t = (1 - g t - b t) * g t - b t ^ 2 := by
    rw [q, a_eq_one_sub_g_sub_b]
  simpa only [centerMatrix, k00, k01, k11, hq, a_eq_one_sub_g_sub_b] using
    point_logdet_second (b t) (g t) u v w z hB (by rwa [← hq])


open scoped Matrix.Norms.Frobenius

/-- The actual matrix log-determinant is smooth at every invertible matrix. -/
theorem logdet_contDiffAt (X : Matrix (Fin 3) (Fin 3) ℝ) (hX : X.det ≠ 0) :
    ContDiffAt ℝ ⊤ (fun Y : Matrix (Fin 3) (Fin 3) ℝ => -Real.log Y.det) X := by
  have he (i j : Fin 3) : ContDiff ℝ ⊤
      (fun Y : Matrix (Fin 3) (Fin 3) ℝ => Y i j) := by
    let L : Matrix (Fin 3) (Fin 3) ℝ →ₗ[ℝ] ℝ :=
      { toFun := fun Y => Y i j
        map_add' := by intros; rfl
        map_smul' := by intros; rfl }
    exact L.toContinuousLinearMap.contDiff
  have hd : ContDiff ℝ ⊤ (fun Y : Matrix (Fin 3) (Fin 3) ℝ => Y.det) := by
    simp only [Matrix.det_fin_three]
    exact (((((he 0 0).mul (he 1 1)).mul (he 2 2)).sub
      (((he 0 0).mul (he 1 2)).mul (he 2 1))).sub
      (((he 0 1).mul (he 1 0)).mul (he 2 2))).add
      (((he 0 1).mul (he 1 2)).mul (he 2 0)) |>.add
      (((he 0 2).mul (he 1 0)).mul (he 2 1)) |>.sub
      (((he 0 2).mul (he 1 1)).mul (he 2 0))
  exact (hd.contDiffAt.log hX).neg

theorem center_det_ne (t : ℝ) (hb : b t ≠ 0) (hq : q t ≠ 0) :
    (centerMatrix t).det ≠ 0 := by
  have hdet : (centerMatrix t).det = b t * q t := by
    simp [centerMatrix, point, Matrix.det_fin_three, q, a_eq_one_sub_g_sub_b]
    ring
  rw [hdet]
  exact mul_ne_zero hb hq

/-- The second Fréchet derivative of the actual matrix barrier, evaluated twice
on any feasible tangent direction, equals the computed quadratic form. -/
theorem center_iteratedFDeriv_two (t u v w z : ℝ) (hb : b t ≠ 0) (hq : q t ≠ 0) :
    iteratedFDeriv ℝ 2 (fun Y : Matrix (Fin 3) (Fin 3) ℝ => -Real.log Y.det)
      (centerMatrix t) (fun _ => tangent u v w z) =
      k00 t * u ^ 2 + 2 * k01 t * u * v + k11 t * v ^ 2
        + 2 / (b t * q t) * (g t * w ^ 2 - 2 * b t * w * z + a t * z ^ 2) := by
  rw [← line_second_eq_iteratedFDeriv
    ((logdet_contDiffAt (centerMatrix t) (center_det_ne t hb hq)).of_le (by norm_num))]
  exact (center_logdet_second t u v w z hb hq).deriv

end
end QipmFormal.FractionalSDP
