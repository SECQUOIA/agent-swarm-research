import Formal.NetworkSimplex.ThresholdSection

/-! The coordinate - section lemma for every nonzero real normal, including zero components. -/
namespace NetworkSimplex

private theorem linear_small {ε A B D x y : ℝ} (hε : 0 < ε)
    (hD : |A| + |B| < D) (hx : |x| < ε / D) (hy : |y| < ε / D) :
    |A * x + B * y| < ε := by
  have hD0 : 0 < D := lt_of_le_of_lt (by positivity) hD
  have he : 0 < ε / D := div_pos hε hD0
  have hx' := mul_le_mul_of_nonneg_left hx.le (abs_nonneg A)
  have hy' := mul_le_mul_of_nonneg_left hy.le (abs_nonneg B)
  calc
    _ ≤ |A * x| + |B * y| := abs_add_le _ _
    _ = |A| * |x| + |B| * |y| := by rw [abs_mul, abs_mul]
    _ ≤ (|A| + |B|) * (ε / D) := by nlinarith
    _ < D * (ε / D) := mul_lt_mul_of_pos_right hD he
    _ = ε := mul_div_cancel₀ ε (ne_of_gt hD0)

/-- Every nonzero normal is forced, with positive scaling, in a finite affine
description of its local halfplane. No sign restriction is imposed on either component. -/
theorem local_halfplane_description_arbitrary_normal {ι κ : Type*} [Finite ι]
    {ε α β : ℝ} (hε : 0 < ε) (hn : α ≠ 0 ∨ β ≠ 0)
    (A B c : ι → ℝ) (E F d : κ → ℝ)
    (h : ∀ u v, |u| < ε → |v| < ε →
      (((∀ i, 0 ≤ c i + A i * u + B i * v) ∧
        (∀ j, d j + E j * u + F j * v = 0)) ↔ 0 ≤ α * u + β * v)) :
    ∃ i, ∃ t : ℝ, 0 < t ∧ c i = 0 ∧ A i = t * α ∧ B i = t * β := by
  have hnorm : 0 < α ^ 2 + β ^ 2 := by
    rcases hn with hα | hβ
    · nlinarith [sq_pos_of_ne_zero hα, sq_nonneg β]
    · nlinarith [sq_pos_of_ne_zero hβ, sq_nonneg α]
  let D := 1 + |2 * α + β| + |α| + |2 * β - α| + |β|
  have hD : 0 < D := by dsimp [D]; positivity
  have hε' : 0 < ε / D := div_pos hε hD
  obtain ⟨i, t, ht, hc, hA, hB⟩ := local_halfplane_description_positive_multiple hε'
    (fun i => A i * (2 * α + β) + B i * (2 * β - α))
    (fun i => A i * α + B i * β) c
    (fun j => E j * (2 * α + β) + F j * (2 * β - α))
    (fun j => E j * α + F j * β) d (by
      intro x y hx hy
      have hu : |(2 * α + β) * x + α * y| < ε := linear_small hε
        (by dsimp [D]; linarith [abs_nonneg (2 * β - α), abs_nonneg β]) hx hy
      have hv : |(2 * β - α) * x + β * y| < ε := linear_small hε
        (by dsimp [D]; linarith [abs_nonneg (2 * α + β), abs_nonneg α]) hx hy
      have hh := h ((2 * α + β) * x + α * y) ((2 * β - α) * x + β * y) hu hv
      have heq : α * ((2 * α + β) * x + α * y) + β * ((2 * β - α) * x + β * y) =
          (α ^ 2 + β ^ 2) * (2 * x + y) := by ring
      rw [heq, mul_nonneg_iff_of_pos_left hnorm] at hh
      have hlinear : ∀ a b c : ℝ,
          c + (a * (2 * α + β) + b * (2 * β - α)) * x + (a * α + b * β) * y =
            c + a * ((2 * α + β) * x + α * y) + b * ((2 * β - α) * x + β * y) := by
        intros; ring
      simp only [hlinear]
      exact hh)
  have hcross : A i * β = B i * α := by nlinarith
  refine ⟨i, t / (α ^ 2 + β ^ 2), div_pos ht hnorm, hc, ?_, ?_⟩
  · rw [div_mul_eq_mul_div]
    apply (eq_div_iff (ne_of_gt hnorm)).mpr
    nlinarith [congrArg (fun z : ℝ => z * β) hcross,
      congrArg (fun z : ℝ => z * α) hB]
  · rw [div_mul_eq_mul_div]
    apply (eq_div_iff (ne_of_gt hnorm)).mpr
    nlinarith [congrArg (fun z : ℝ => z * α) hcross,
      congrArg (fun z : ℝ => z * β) hB]

/-- Affine equations valid on any nontrivial local halfplane vanish on its coordinate plane. -/
theorem local_halfplane_equation_arbitrary_normal {ε α β A B c : ℝ}
    (hε : 0 < ε) (hn : α ≠ 0 ∨ β ≠ 0)
    (h : ∀ u v, |u| < ε → |v| < ε → 0 ≤ α * u + β * v →
      c + A * u + B * v = 0) : A = 0 ∧ B = 0 ∧ c = 0 := by
  have hnorm : 0 < α ^ 2 + β ^ 2 := by
    rcases hn with hα | hβ
    · nlinarith [sq_pos_of_ne_zero hα, sq_nonneg β]
    · nlinarith [sq_pos_of_ne_zero hβ, sq_nonneg α]
  let D := 1 + |2 * α + β| + |α| + |2 * β - α| + |β|
  have hD : 0 < D := by dsimp [D]; positivity
  have hz := local_halfplane_equation_zero (div_pos hε hD)
    (A := A * (2 * α + β) + B * (2 * β - α)) (B := A * α + B * β) (c := c) (by
      intro x y hx hy hh
      have hu : |(2 * α + β) * x + α * y| < ε := linear_small hε
        (by dsimp [D]; linarith [abs_nonneg (2 * β - α), abs_nonneg β]) hx hy
      have hv : |(2 * β - α) * x + β * y| < ε := linear_small hε
        (by dsimp [D]; linarith [abs_nonneg (2 * α + β), abs_nonneg α]) hx hy
      have hfeas : 0 ≤ α * ((2 * α + β) * x + α * y) + β * ((2 * β - α) * x + β * y) := by
        have heq : α * ((2 * α + β) * x + α * y) + β * ((2 * β - α) * x + β * y) =
            (α ^ 2 + β ^ 2) * (2 * x + y) := by ring
        rw [heq]
        exact mul_nonneg hnorm.le hh
      have he := h _ _ hu hv hfeas
      nlinarith [he])
  have hc : A * β = B * α := by nlinarith [hz.1, hz.2.1]
  have hA : A * (α ^ 2 + β ^ 2) = 0 := by
    nlinarith [congrArg (fun z : ℝ => z * β) hc,
      congrArg (fun z : ℝ => z * α) hz.2.1]
  have hB : B * (α ^ 2 + β ^ 2) = 0 := by
    nlinarith [congrArg (fun z : ℝ => z * α) hc,
      congrArg (fun z : ℝ => z * β) hz.2.1]
  exact ⟨(mul_eq_zero.mp hA).resolve_right (ne_of_gt hnorm),
    (mul_eq_zero.mp hB).resolve_right (ne_of_gt hnorm), hz.2.2⟩

end NetworkSimplex
