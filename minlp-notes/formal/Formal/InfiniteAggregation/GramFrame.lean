import Mathlib

namespace InfiniteAggregation

open Matrix

private theorem normSq_nonneg {r : ℕ} (v : Fin r → ℝ) : 0 ≤ v ⬝ᵥ v := by
  exact Finset.sum_nonneg fun i _ => mul_self_nonneg _

private theorem normalize_frame {r : ℕ} (v : Fin r → ℝ) (hv : v ≠ 0) :
    ∃ e : Fin r → ℝ, ∃ P : ℝ, e ⬝ᵥ e = 1 ∧ 0 < P ∧ v = P • e := by
  have hpos : 0 < v ⬝ᵥ v := lt_of_le_of_ne (normSq_nonneg v)
    (Ne.symm (mt dotProduct_self_eq_zero.mp hv))
  let P := Real.sqrt (v ⬝ᵥ v)
  have hp : 0 < P := Real.sqrt_pos.mpr hpos
  have hsq : P ^ 2 = v ⬝ᵥ v := Real.sq_sqrt hpos.le
  refine ⟨P⁻¹ • v, P, ?_, hp, ?_⟩
  · simp only [smul_dotProduct, dotProduct_smul, smul_eq_mul]
    rw [← hsq]
    field_simp
  · rw [smul_smul, mul_inv_cancel₀ hp.ne', one_smul]

/-- A unit vector in dimension at least two has an orthogonal unit vector. -/
theorem exists_unit_perpendicular {r : ℕ} (hr : 2 ≤ r) (e : Fin r → ℝ)
    (he : e ⬝ᵥ e = 1) :
    ∃ f : Fin r → ℝ, f ⬝ᵥ f = 1 ∧ e ⬝ᵥ f = 0 := by
  classical
  have hene : e ≠ 0 := by intro h; simp [h] at he
  obtain ⟨i, hi⟩ : ∃ i, e i ≠ 0 := by
    by_contra h
    push Not at h
    exact hene (funext h)
  obtain ⟨j, hj⟩ := Fintype.exists_ne_of_one_lt_card
    (show 1 < Fintype.card (Fin r) by simp; omega) i
  let v : Fin r → ℝ := Pi.single i (-e j) + Pi.single j (e i)
  have hv : v ≠ 0 := by
    intro h
    have hjzero : e i = 0 := by simpa [v, hj] using congrFun h j
    exact hi hjzero
  have hev : e ⬝ᵥ v = 0 := by
    simp only [v, dotProduct_add, dotProduct_single]
    ring
  obtain ⟨f, P, hf, hp, hve⟩ := normalize_frame v hv
  refine ⟨f, hf, ?_⟩
  rw [hve, dotProduct_smul, smul_eq_mul] at hev
  exact (mul_eq_zero.mp hev).resolve_left hp.ne'

/-- Two vectors admit a positively oriented orthonormal two-vector frame.
This includes linearly dependent vectors and the zero pair. -/
theorem exists_gram_frame {r : ℕ} (hr : 2 ≤ r) (p q : Fin r → ℝ) :
    ∃ e f : Fin r → ℝ, ∃ P Q R : ℝ,
      e ⬝ᵥ e = 1 ∧ f ⬝ᵥ f = 1 ∧ e ⬝ᵥ f = 0 ∧
      0 ≤ P ∧ 0 ≤ R ∧ p = P • e ∧ q = Q • e + R • f := by
  classical
  obtain ⟨e, P, he, hp, hpe⟩ : ∃ e : Fin r → ℝ, ∃ P : ℝ,
      e ⬝ᵥ e = 1 ∧ 0 ≤ P ∧ p = P • e := by
    by_cases hp : p = 0
    · let i : Fin r := ⟨0, by omega⟩
      refine ⟨Pi.single i 1, 0, ?_, le_rfl, ?_⟩
      · simp
      · simp [hp]
    · obtain ⟨e, P, he, hP, hpe⟩ := normalize_frame p hp
      exact ⟨e, P, he, hP.le, hpe⟩
  let Q := e ⬝ᵥ q
  let v := q - Q • e
  have hev : e ⬝ᵥ v = 0 := by simp [v, Q, dotProduct_sub, dotProduct_smul, he]
  by_cases hv : v = 0
  · obtain ⟨f, hf, hef⟩ := exists_unit_perpendicular hr e he
    refine ⟨e, f, P, Q, 0, he, hf, hef, hp, le_rfl, hpe, ?_⟩
    simpa only [zero_smul, add_zero] using sub_eq_zero.mp hv
  · obtain ⟨f, R, hf, hR, hvf⟩ := normalize_frame v hv
    have hef : e ⬝ᵥ f = 0 := by
      rw [hvf, dotProduct_smul, smul_eq_mul] at hev
      exact (mul_eq_zero.mp hev).resolve_left hR.ne'
    refine ⟨e, f, P, Q, R, he, hf, hef, hp, hR.le, hpe, ?_⟩
    rw [← hvf]
    dsimp [v]
    abel

end InfiniteAggregation
