import Formal.QuadraticPrecision.Spectral

open scoped BigOperators Matrix
namespace InfiniteAggregation

abbrev HomIndex (r : ℕ) := Option (Fin r ⊕ Fin r)

/-- The homogeneous matrix, with `none` the homogenizing coordinate. -/
noncomputable def homogeneousMatrix (r : ℕ) (w : Fin 3 → ℝ) : Matrix (HomIndex r) (HomIndex r) ℝ
  | none, none => w 2 / 2 - w 0 - w 1
  | some (.inl i), some (.inl j) => if i = j then w 0 else 0
  | some (.inr i), some (.inr j) => if i = j then w 1 else 0
  | some (.inl i), some (.inr j) => if i = j then -w 2 / 2 else 0
  | some (.inr i), some (.inl j) => if i = j then -w 2 / 2 else 0
  | _, _ => 0

theorem homogeneousMatrix_hermitian (r : ℕ) (w : Fin 3 → ℝ) :
    (homogeneousMatrix r w).IsHermitian := by
  ext i j
  cases i with
  | none => cases j <;> simp [homogeneousMatrix, Matrix.conjTranspose_apply]
  | some i =>
    cases j with
    | none => simp [homogeneousMatrix, Matrix.conjTranspose_apply]
    | some j => cases i <;> cases j <;>
        simp [homogeneousMatrix, Matrix.conjTranspose_apply, eq_comm]

theorem homogeneousMatrix_quadratic (r : ℕ) (w : Fin 3 → ℝ)
    (z : HomIndex r → ℝ) :
    z ⬝ᵥ (homogeneousMatrix r w *ᵥ z) =
      (w 2 / 2 - w 0 - w 1) * z none ^ 2 +
      ∑ i, (w 0 * z (some (.inl i)) ^ 2 + w 1 * z (some (.inr i)) ^ 2 -
        w 2 * z (some (.inl i)) * z (some (.inr i))) := by
  simp only [Matrix.mulVec, dotProduct, Fintype.sum_option, Fintype.sum_sum_type]
  simp only [homogeneousMatrix, ite_mul, zero_mul, Finset.sum_ite_eq,
    Finset.mem_univ, if_true, Finset.sum_const_zero, add_zero, zero_add,
    Finset.sum_sub_distrib]
  rw [← Finset.sum_add_distrib]
  congr 1
  · ring
  · rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro i _
    ring

/-- Replicate one two-dimensional coefficient direction in every spatial coordinate. -/
def replicateDirection (r : ℕ) (a b : ℝ) :
    (Fin r → ℝ) →ₗ[ℝ] (HomIndex r → ℝ) where
  toFun y := fun i => match i with
    | none => 0
    | some (.inl j) => a * y j
    | some (.inr j) => b * y j
  map_add' x y := by
    ext i
    cases i with
    | none => simp
    | some i => cases i <;> simp [mul_add]
  map_smul' c y := by
    ext i
    cases i with
    | none => simp
    | some i => cases i <;> simp [mul_left_comm]

theorem replicateDirection_quadratic (r : ℕ) (w : Fin 3 → ℝ) (a b : ℝ)
    (y : Fin r → ℝ) :
    replicateDirection r a b y ⬝ᵥ (homogeneousMatrix r w *ᵥ replicateDirection r a b y) =
      (w 0 * a ^ 2 + w 1 * b ^ 2 - w 2 * a * b) * ∑ i, y i ^ 2 := by
  rw [homogeneousMatrix_quadratic]
  simp only [replicateDirection, LinearMap.coe_mk, AddHom.coe_mk, zero_pow (by decide : 2 ≠ 0),
    mul_zero, zero_add]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem negative_direction_of_discriminant (w : Fin 3 → ℝ)
    (hw : ∀ i, 0 ≤ w i) (hd : 4 * w 0 * w 1 < w 2 ^ 2) :
    ∃ a b : ℝ, w 0 * a ^ 2 + w 1 * b ^ 2 - w 2 * a * b < 0 := by
  by_cases h0 : w 0 = 0
  · refine ⟨w 1 + 1, w 2, ?_⟩
    have hd' : 0 < w 2 ^ 2 := by simpa [h0] using hd
    rw [h0]
    nlinarith
  · have hp : 0 < w 0 := lt_of_le_of_ne (hw 0) (Ne.symm h0)
    refine ⟨w 2, 2 * w 0, ?_⟩
    nlinarith [mul_pos hp (sub_pos.mpr hd)]

end InfiniteAggregation
