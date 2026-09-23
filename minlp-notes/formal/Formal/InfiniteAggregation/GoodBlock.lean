import Formal.InfiniteAggregation.GoodMatrix
import Formal.InfiniteAggregation.GoodConvex

open scoped Matrix
namespace InfiniteAggregation

/-- The two by two block replicated in the leading homogeneous matrix. -/
noncomputable def leadingBlock (w : Weight) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![w 0, -w 2 / 2; -w 2 / 2, w 1]

theorem leadingBlock_hermitian (w : Weight) : (leadingBlock w).IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [leadingBlock, Matrix.conjTranspose_apply]

theorem leadingBlock_quadratic (w : Weight) (x : Fin 2 → ℝ) :
    x ⬝ᵥ (leadingBlock w *ᵥ x) =
      w 0 * x 0 ^ 2 + w 1 * x 1 ^ 2 - w 2 * x 0 * x 1 := by
  simp [leadingBlock, Matrix.mulVec, dotProduct, Fin.sum_univ_succ]
  ring

theorem leadingBlock_posSemidef_iff (w : Weight) (hw : ∀ i, 0 ≤ w i) :
    (leadingBlock w).PosSemidef ↔ w 2 ^ 2 ≤ 4 * w 0 * w 1 := by
  constructor
  · intro h
    by_contra hn
    obtain ⟨a,b,hab⟩ := negative_direction_of_discriminant w hw (lt_of_not_ge hn)
    have hh := h.dotProduct_mulVec_nonneg ![a,b]
    simp only [star_trivial, leadingBlock_quadratic, Matrix.cons_val_zero,
      Matrix.cons_val_one] at hh
    linarith
  · intro hd
    apply Matrix.posSemidef_iff_dotProduct_mulVec.mpr
    refine ⟨leadingBlock_hermitian w, ?_⟩
    intro x
    simp only [star_trivial, leadingBlock_quadratic]
    exact leading_nonneg w ⟨hw, hd⟩ (x 0) (x 1)

/-- The homogeneous quadratic is the direct sum of `r` identical leading
blocks and its single homogenizing-coordinate coefficient. -/
theorem homogeneousMatrix_block_decomposition {r : ℕ} (w : Weight)
    (z : HomIndex r → ℝ) :
    z ⬝ᵥ (homogeneousMatrix r w *ᵥ z) =
      (w 2 / 2 - w 0 - w 1) * z none ^ 2 +
        ∑ i, ![z (some (.inl i)), z (some (.inr i))] ⬝ᵥ
          (leadingBlock w *ᵥ ![z (some (.inl i)), z (some (.inr i))]) := by
  simp only [homogeneousMatrix_quadratic, leadingBlock_quadratic,
    Matrix.cons_val_zero, Matrix.cons_val_one]

end InfiniteAggregation
