import Mathlib

/-!
# Residual propagation along a realized sequence of nonsingular systems

The operators act in one fixed normed coordinate space. The right-hand sides
must be nonzero: this makes both normalizations and the candidate scalar valid.
-/

namespace QipmFormal.Refresh
noncomputable section
open scoped BigOperators

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

def solution (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E) (t : ℕ) : E :=
  (H t).symm (f t)

def solutionNorm (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E) (t : ℕ) : ℝ :=
  ‖solution H f t‖

def ray (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E) (t : ℕ) : E :=
  (solutionNorm H f t)⁻¹ • solution H f t

def normalizedOperator (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E) (t : ℕ) : E →L[ℝ] E :=
  (solutionNorm H f t / ‖f t‖) • (H t : E →L[ℝ] E)

def normalizedInverse (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E) (t : ℕ) : E →L[ℝ] E :=
  (‖f t‖ / solutionNorm H f t) • ((H t).symm : E →L[ℝ] E)

def stepVariation (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E) (j : ℕ) : ℝ :=
  ‖normalizedOperator H f (j + 1) (ray H f (j + 1) - ray H f j)‖

theorem solution_equation (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E) (t : ℕ) :
    H t (solution H f t) = f t := by simp [solution]

theorem solutionNorm_pos (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E)
    (hf : ∀ t, f t ≠ 0) (t : ℕ) : 0 < solutionNorm H f t := by
  apply norm_pos_iff.mpr
  intro h
  have := solution_equation H f t
  rw [h, map_zero] at this
  exact hf t this.symm

theorem normalizedInverse_apply_operator (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E)
    (hf : ∀ t, f t ≠ 0) (t : ℕ) (x : E) :
    normalizedInverse H f t (normalizedOperator H f t x) = x := by
  have hq := ne_of_gt (solutionNorm_pos H f hf t)
  have hr := norm_ne_zero_iff.mpr (hf t)
  simp [normalizedInverse, normalizedOperator, smul_smul, hq, hr]

theorem normalizedOperator_apply_inverse (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E)
    (hf : ∀ t, f t ≠ 0) (t : ℕ) (x : E) :
    normalizedOperator H f t (normalizedInverse H f t x) = x := by
  have hq := ne_of_gt (solutionNorm_pos H f hf t)
  have hr := norm_ne_zero_iff.mpr (hf t)
  simp [normalizedInverse, normalizedOperator, smul_smul, hq, hr]

theorem normalizedOperator_ray (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E)
    (hf : ∀ t, f t ≠ 0) (t : ℕ) :
    normalizedOperator H f t (ray H f t) = ‖f t‖⁻¹ • f t := by
  have hq := ne_of_gt (solutionNorm_pos H f hf t)
  simp only [normalizedOperator, ray, smul_apply, ContinuousLinearEquiv.coe_coe,
    map_smul, solution_equation, smul_smul]
  congr 1
  field_simp

theorem norm_ray (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E)
    (hf : ∀ t, f t ≠ 0) (t : ℕ) : ‖ray H f t‖ = 1 := by
  have hq := ne_of_gt (solutionNorm_pos H f hf t)
  rw [ray, norm_smul, Real.norm_eq_abs, abs_of_pos
    (inv_pos.mpr (solutionNorm_pos H f hf t))]
  change (solutionNorm H f t)⁻¹ * solutionNorm H f t = 1
  exact inv_mul_cancel₀ hq

theorem normalized_residual (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E)
    (hf : ∀ t, f t ≠ 0) (t : ℕ) (x : E) :
    ‖normalizedOperator H f t ((solutionNorm H f t)⁻¹ • x - ray H f t)‖ =
      ‖H t x - f t‖ / ‖f t‖ := by
  have hq := ne_of_gt (solutionNorm_pos H f hf t)
  have hr := norm_ne_zero_iff.mpr (hf t)
  have heq : normalizedOperator H f t
      ((solutionNorm H f t)⁻¹ • x - ray H f t) =
      ‖f t‖⁻¹ • (H t x - f t) := by
    simp only [normalizedOperator, ray, smul_apply,
      ContinuousLinearEquiv.coe_coe, ← smul_sub, map_smul, map_sub,
      solution_equation, smul_smul]
    congr 1
    field_simp
  rw [heq, norm_smul, Real.norm_eq_abs, abs_of_nonneg (inv_nonneg.mpr (norm_nonneg _))]
  exact (div_eq_inv_mul _ _).symm

/-- A directed cross-gain bound propagates any vector's residual. -/
theorem propagate_norm (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E)
    (hf : ∀ t, f t ≠ 0) (t j : ℕ) (G : ℝ)
    (hG : ‖(normalizedOperator H f t).comp (normalizedInverse H f j)‖ ≤ G)
    (x : E) :
    ‖normalizedOperator H f t x‖ ≤ G * ‖normalizedOperator H f j x‖ := by
  have h := ((normalizedOperator H f t).comp (normalizedInverse H f j)).le_of_opNorm_le
    hG (normalizedOperator H f j x)
  simpa only [ContinuousLinearMap.comp_apply, normalizedInverse_apply_operator H f hf] using h

/-- Telescoping the normalized directions charges each step in its own operator norm. -/
theorem ray_difference_bound (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E)
    (hf : ∀ t, f t ≠ 0) (s t : ℕ) (hst : s ≤ t) (G : ℝ)
    (hG : ∀ j, s ≤ j → j ≤ t →
      ‖(normalizedOperator H f t).comp (normalizedInverse H f j)‖ ≤ G) :
    ‖normalizedOperator H f t (ray H f t - ray H f s)‖ ≤
      G * ∑ j ∈ Finset.Ico s t, stepVariation H f j := by
  rw [← Finset.sum_Ico_sub (f := ray H f) hst, map_sum]
  calc
    ‖∑ j ∈ Finset.Ico s t,
        normalizedOperator H f t (ray H f (j + 1) - ray H f j)‖ ≤
        ∑ j ∈ Finset.Ico s t,
          ‖normalizedOperator H f t (ray H f (j + 1) - ray H f j)‖ :=
      norm_sum_le _ _
    _ ≤ ∑ j ∈ Finset.Ico s t, G * stepVariation H f j := by
      apply Finset.sum_le_sum
      intro j hj
      obtain ⟨hsj, hjt⟩ := Finset.mem_Ico.mp hj
      exact propagate_norm H f hf t (j + 1) G (hG _ (by omega) (by omega)) _
    _ = _ := (Finset.mul_sum _ _ _).symm

/-- Residual bound for the explicit scalar `q_t / q_s`; minimizing over scalars
can only improve it. This is the analytic estimate used in the refresh count. -/
theorem candidate_residual_bound (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E)
    (hf : ∀ t, f t ≠ 0) (s t : ℕ) (hst : s ≤ t) (zhat : E) (ε G : ℝ)
    (hε : ‖H s zhat - f s‖ / ‖f s‖ ≤ ε)
    (hG : ∀ j, s ≤ j → j ≤ t →
      ‖(normalizedOperator H f t).comp (normalizedInverse H f j)‖ ≤ G) :
    ‖H t ((solutionNorm H f t / solutionNorm H f s) • zhat) - f t‖ / ‖f t‖ ≤
      G * (ε + ∑ j ∈ Finset.Ico s t, stepVariation H f j) := by
  have hG0 : 0 ≤ G := (norm_nonneg _).trans (hG s le_rfl hst)
  have hqt := ne_of_gt (solutionNorm_pos H f hf t)
  rw [← normalized_residual H f hf t]
  have hscale : (solutionNorm H f t)⁻¹ •
      ((solutionNorm H f t / solutionNorm H f s) • zhat) =
      (solutionNorm H f s)⁻¹ • zhat := by
    rw [smul_smul]
    congr 1
    field_simp
  rw [hscale]
  have hsplit : (solutionNorm H f s)⁻¹ • zhat - ray H f t =
      ((solutionNorm H f s)⁻¹ • zhat - ray H f s) +
      (ray H f s - ray H f t) := by abel
  rw [hsplit, map_add]
  calc
    _ ≤ ‖normalizedOperator H f t ((solutionNorm H f s)⁻¹ • zhat - ray H f s)‖ +
        ‖normalizedOperator H f t (ray H f s - ray H f t)‖ := norm_add_le _ _
    _ ≤ G * ε + G * ∑ j ∈ Finset.Ico s t, stepVariation H f j := by
      apply add_le_add
      · exact (propagate_norm H f hf t s G (hG s le_rfl hst) _).trans
          (mul_le_mul_of_nonneg_left (by rwa [normalized_residual H f hf s]) hG0)
      · rw [← neg_sub (ray H f t) (ray H f s), map_neg, norm_neg]
        exact ray_difference_bound H f hf s t hst G hG
    _ = _ := (mul_add _ _ _).symm

/-- The finite-prefix version requires no hypotheses on right-hand sides after
the tested iteration. Extending that finite prefix by its final nonzero value
lets us reuse the all-indices estimate without changing any relevant quantity. -/
theorem candidate_residual_bound_on (H : ℕ → E ≃L[ℝ] E) (f : ℕ → E)
    (s t : ℕ) (hf : ∀ j, j ≤ t → f j ≠ 0) (hst : s ≤ t) (zhat : E) (ε G : ℝ)
    (hε : ‖H s zhat - f s‖ / ‖f s‖ ≤ ε)
    (hG : ∀ j, s ≤ j → j ≤ t →
      ‖(normalizedOperator H f t).comp (normalizedInverse H f j)‖ ≤ G) :
    ‖H t ((solutionNorm H f t / solutionNorm H f s) • zhat) - f t‖ / ‖f t‖ ≤
      G * (ε + ∑ j ∈ Finset.Ico s t, stepVariation H f j) := by
  let f' : ℕ → E := fun j => if j ≤ t then f j else f t
  have hf' : ∀ j, f' j ≠ 0 := by
    intro j
    dsimp [f']
    split_ifs with hj
    · exact hf j hj
    · exact hf t le_rfl
  have hq (j : ℕ) (hj : j ≤ t) : solutionNorm H f' j = solutionNorm H f j := by
    simp [solutionNorm, solution, f', hj]
  have hr (j : ℕ) (hj : j ≤ t) : ray H f' j = ray H f j := by
    simp [ray, solutionNorm, solution, f', hj]
  have hm (j : ℕ) (hj : j ≤ t) :
      normalizedOperator H f' j = normalizedOperator H f j := by
    simp [normalizedOperator, solutionNorm, solution, f', hj]
  have hn (j : ℕ) (hj : j ≤ t) :
      normalizedInverse H f' j = normalizedInverse H f j := by
    simp [normalizedInverse, solutionNorm, solution, f', hj]
  have hε' : ‖H s zhat - f' s‖ / ‖f' s‖ ≤ ε := by
    simpa [f', hst] using hε
  have hG' : ∀ j, s ≤ j → j ≤ t →
      ‖(normalizedOperator H f' t).comp (normalizedInverse H f' j)‖ ≤ G := by
    intro j hsj hjt
    rw [hm t le_rfl, hn j hjt]
    exact hG j hsj hjt
  have hsum : ∑ j ∈ Finset.Ico s t, stepVariation H f' j =
      ∑ j ∈ Finset.Ico s t, stepVariation H f j := by
    apply Finset.sum_congr rfl
    intro j hj
    have hjt := (Finset.mem_Ico.mp hj).2
    have hj' : j + 1 ≤ t := by omega
    simp only [stepVariation, hm (j + 1) hj', hr (j + 1) hj', hr j (by omega)]
  have h := candidate_residual_bound H f' hf' s t hst zhat ε G hε' hG'
  rw [hq t le_rfl, hq s hst, hsum] at h
  simpa only [f', if_pos (show t ≤ t from le_rfl)] using h

end
end QipmFormal.Refresh
