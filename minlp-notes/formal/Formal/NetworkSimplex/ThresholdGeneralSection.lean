import Formal.NetworkSimplex.ThresholdSection

/-! Arbitrary positive section normals, retaining the original coordinate coefficients. -/
namespace NetworkSimplex

/-- Every finite affine description must contain the positive normal of a genuine local section. -/
theorem local_halfplane_description_normal {ι κ : Type*} [Finite ι]
    {ε α β : ℝ} (hε : 0 < ε) (hα : 0 < α) (hβ : 0 < β)
    (A B c : ι → ℝ) (E F d : κ → ℝ)
    (h : ∀ u v, |u| < ε → |v| < ε →
      (((∀ i, 0 ≤ c i + A i * u + B i * v) ∧
        (∀ j, d j + E j * u + F j * v = 0)) ↔ 0 ≤ α * u + β * v)) :
    ∃ i, ∃ t : ℝ, 0 < t ∧ c i = 0 ∧ A i = t * α ∧ B i = t * β := by
  let k := 2 * β / α
  have hk : 0 < k := by dsimp [k]; positivity
  have hk1 : 0 < 1 + k := by positivity
  have he : 0 < ε / (1 + k) := div_pos hε hk1
  have hsmall : ∀ x : ℝ, |x| < ε / (1 + k) → |k * x| < ε ∧ |x| < ε := by
    intro x hx
    have hh := (lt_div_iff₀ hk1).mp hx
    rw [abs_mul, abs_of_pos hk]
    constructor <;> nlinarith [abs_nonneg x]
  obtain ⟨i, t, ht, hc, hA, hB⟩ :=
    local_halfplane_description_positive_multiple he
      (fun i => A i * k) B c (fun j => E j * k) F d (by
        intro u v hu hv
        have heq : α * (k * u) + β * v = β * (2 * u + v) := by
          dsimp [k]
          field_simp
        simpa only [mul_assoc, heq, mul_nonneg_iff_of_pos_left hβ] using
          h (k * u) v (hsmall u hu).1 (hsmall v hv).2)
  refine ⟨i, t / β, div_pos ht hβ, hc, ?_, ?_⟩
  · dsimp [k] at hA
    field_simp at hA ⊢
    nlinarith
  · rw [div_mul_cancel₀ t (ne_of_gt hβ)]
    exact hB

/-- Valid affine equations cannot change either free coefficient of the local section. -/
theorem local_halfplane_equation_normal {ε α β A B c : ℝ}
    (hε : 0 < ε) (hα : 0 < α) (hβ : 0 < β)
    (h : ∀ u v, |u| < ε → |v| < ε → 0 ≤ α * u + β * v →
      c + A * u + B * v = 0) : A = 0 ∧ B = 0 ∧ c = 0 := by
  have hc := h 0 0 (by simpa using hε) (by simpa using hε) (by simp)
  have hu := h (ε / 2) 0 (by rw [abs_of_pos (by positivity)]; linarith)
    (by simpa using hε) (by positivity)
  have hv := h 0 (ε / 2) (by simpa using hε)
    (by rw [abs_of_pos (by positivity)]; linarith) (by positivity)
  simp only [mul_zero, add_zero] at hc hu hv
  refine ⟨?_, ?_, hc⟩ <;> nlinarith

/-- The nearby feasible half-plane has genuine two-dimensional interior. -/
theorem local_halfplane_nonempty_interior {ε α β : ℝ}
    (hε : 0 < ε) (hα : 0 < α) (hβ : 0 < β) :
    (interior {p : ℝ × ℝ | |p.1| < ε ∧ |p.2| < ε ∧ 0 ≤ α * p.1 + β * p.2}).Nonempty := by
  refine ⟨(ε / 2, ε / 2), mem_interior.mpr ?_⟩
  refine ⟨Set.Ioo (ε / 4) (3 * ε / 4) ×ˢ Set.Ioo (ε / 4) (3 * ε / 4), ?_,
    isOpen_Ioo.prod isOpen_Ioo, ?_⟩
  · rintro ⟨u, v⟩ ⟨⟨hu0, hu1⟩, ⟨hv0, hv1⟩⟩
    have hu : 0 < u := by linarith
    have hv : 0 < v := by linarith
    change |u| < ε ∧ |v| < ε ∧ 0 ≤ α * u + β * v
    rw [abs_of_pos hu, abs_of_pos hv]
    exact ⟨by linarith, by linarith, by positivity⟩
  · constructor <;> constructor <;> linarith

end NetworkSimplex
