import Formal.InfiniteAggregation.AccuracyRational
import Formal.InfiniteAggregation.AccuracyRationalMesh
import Formal.InfiniteAggregation.AccuracyUpper
import Formal.InfiniteAggregation.AccuracyModel

/-! The integer cuts impose the rational angular mesh exactly. -/
noncomputable section
namespace InfiniteAggregation

theorem rationalLeft_angle {m : ℕ} (hm : 0 < m) (j : ℕ) :
    rationalLeft m j = ((m : ℝ)^2 + (j : ℝ)^2) •
      angleWeight (Real.arctan ((j : ℝ) / m)) := by
  have hm0 : (m : ℝ) ≠ 0 := by exact_mod_cast hm.ne'
  have hden : 1 + ((j : ℝ) / m)^2 ≠ 0 := by positivity
  have hcos : ((m : ℝ)^2 + (j : ℝ)^2) *
      Real.cos (Real.arctan ((j : ℝ) / m)) ^ 2 = (m : ℝ)^2 := by
    rw [Real.cos_sq_arctan]
    field_simp
  have hsin : Real.sin (Real.arctan ((j : ℝ) / m)) =
      ((j : ℝ) / m) * Real.cos (Real.arctan ((j : ℝ) / m)) := by
    rw [Real.sin_arctan, Real.cos_arctan]; ring
  rw [rationalLeft_formula]
  ext i
  fin_cases i
  · exact hcos.symm
  · change (j : ℝ)^2 = ((m : ℝ)^2 + (j : ℝ)^2) *
      Real.sin (Real.arctan ((j : ℝ) / m))^2
    rw [hsin]
    field_simp at hcos ⊢
    nlinarith
  · change 2 * (m : ℝ) * j = ((m : ℝ)^2 + (j : ℝ)^2) *
      (2 * Real.cos (Real.arctan ((j : ℝ) / m)) *
        Real.sin (Real.arctan ((j : ℝ) / m)))
    rw [hsin]
    field_simp
    nlinarith

theorem rationalRight_angle {m : ℕ} (hm : 0 < m) (j : ℕ) :
    rationalRight m j = ((m : ℝ)^2 + (j : ℝ)^2) •
      angleWeight (Real.pi / 2 - Real.arctan ((j : ℝ) / m)) := by
  have h := rationalLeft_angle hm j
  rw [rationalLeft_formula] at h
  rw [rationalRight_formula]
  ext i
  fin_cases i
  · have h1 := congrFun h 1
    simpa [angleWeight, Real.cos_pi_div_two_sub] using h1
  · have h0 := congrFun h 0
    simpa [angleWeight, Real.sin_pi_div_two_sub] using h0
  · have h2 := congrFun h 2
    simpa [angleWeight, Real.sin_pi_div_two_sub, Real.cos_pi_div_two_sub,
      mul_comm, mul_left_comm, mul_assoc] using h2

private theorem aggregate_weight_smul {r : ℕ} (a : ℝ) (w : Weight) (x : Var r) :
    aggregate (a • w) x = a * aggregate w x := by
  simp only [aggregate, Pi.smul_apply, smul_eq_mul, Finset.mul_sum, mul_assoc]

theorem rational_mesh_tests {r m : ℕ} (hm : 0 < m) {x : Var r}
    (hx : x ∈ relaxation (rationalCuts m)) :
    ∀ t ∈ rationalAngleMesh m, 0 ≤ pointAngularForm x t := by
  intro t ht
  obtain ⟨j, hj, ht | ht⟩ := ht
  · subst t
    have h := hx _ (rationalLeft_mem hj)
    rw [rationalLeft_angle hm j, aggregate_weight_smul] at h
    rw [pointAngularForm_eq_neg_aggregate]
    have hp : 0 < (m : ℝ)^2 + (j : ℝ)^2 := by positivity
    nlinarith
  · subst t
    have h := hx _ (rationalRight_mem hj)
    rw [rationalRight_angle hm j, aggregate_weight_smul] at h
    rw [pointAngularForm_eq_neg_aggregate]
    have hp : 0 < (m : ℝ)^2 + (j : ℝ)^2 := by positivity
    nlinarith

/-- The exact rational construction has the source error constant. -/
theorem hausdorffError_rationalCuts_le {r m : ℕ} (hr : 2 ≤ r) (hm : 0 < m) :
    hausdorffError r (rationalCuts m) ≤
      ENNReal.ofReal (5 * Real.sqrt 2 / (4 * (m : ℝ)^2)) := by
  apply hausdorffError_le_of_repair hr (fun _ hw => rationalCuts_good hr hm hw)
  intro x hx
  have ht := rational_mesh_tests hm hx
  obtain ⟨y, hy, hd⟩ := angle_samples_repair (rationalAngleMesh m)
    (rationalAngleMesh_zero m) (rationalAngleMesh_pi_div_two m)
    (rationalAngleMesh_covers m hm) (x := x) (by
      intro t hmem
      have h := ht t hmem
      rw [pointAngularForm_eq_neg_aggregate] at h
      linarith)
  refine ⟨y, hy, ?_⟩
  convert hd using 1
  ring

/-- The integer mesh retains a uniform inverse-square error bound in the cut budget. -/
theorem rational_error_le_inverse_square {N : ℕ} (hN : 3 ≤ N) :
    5 * Real.sqrt 2 / (4 * (rationalMeshSize N : ℝ)^2) ≤
      20 * Real.sqrt 2 / (N : ℝ)^2 := by
  have hm := rationalMeshSize_pos hN
  have hNm : N ≤ 4 * rationalMeshSize N := by unfold rationalMeshSize; omega
  have hNR : (0 : ℝ) < N := by exact_mod_cast (show 0 < N by omega)
  have hmR : (0 : ℝ) < rationalMeshSize N := by exact_mod_cast hm
  have hNmR : (N : ℝ) ≤ 4 * (rationalMeshSize N : ℝ) := by exact_mod_cast hNm
  apply (div_le_div_iff₀ (by positivity) (by positivity)).mpr
  have hsq : (N : ℝ)^2 ≤ 16 * (rationalMeshSize N : ℝ)^2 := by nlinarith
  have := mul_le_mul_of_nonneg_left hsq (Real.sqrt_nonneg 2)
  nlinarith

theorem hausdorffError_rationalCuts_budget_le {r N : ℕ} (hr : 2 ≤ r) (hN : 3 ≤ N) :
    hausdorffError r (rationalCuts (rationalMeshSize N)) ≤
      ENNReal.ofReal (20 * Real.sqrt 2 / (N : ℝ)^2) :=
  (hausdorffError_rationalCuts_le hr (rationalMeshSize_pos hN)).trans
    (ENNReal.ofReal_le_ofReal (rational_error_le_inverse_square hN))

end InfiniteAggregation
