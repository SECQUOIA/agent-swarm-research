import Formal.InfiniteAggregation.GoodMatrix
import Formal.InfiniteAggregation.Inertia

open scoped BigOperators Matrix
open QuadraticPrecision
namespace InfiniteAggregation

/-- A failed two by two PSD condition creates one negative direction in every
spatial coordinate, hence at least `r` negative eigenvalues. -/
theorem inertia_ge_dimension_of_bad_discriminant {r : ℕ} (w : Fin 3 → ℝ)
    (hw : ∀ i, 0 ≤ w i) (hd : 4 * w 0 * w 1 < w 2 ^ 2) :
    r ≤ negativeInertia (homogeneousMatrix_hermitian r w) := by
  obtain ⟨a, b, hab⟩ := negative_direction_of_discriminant w hw hd
  have hE : ∀ y : Fin r → ℝ, y ≠ 0 →
      replicateDirection r a b y ⬝ᵥ
        (homogeneousMatrix r w *ᵥ replicateDirection r a b y) < 0 := by
    intro y hy
    rw [replicateDirection_quadratic]
    apply mul_neg_of_neg_of_pos hab
    obtain ⟨i, hi⟩ : ∃ i, y i ≠ 0 := by
      by_contra hn
      apply hy
      ext i
      simpa using not_exists.mp hn i
    exact Finset.sum_pos' (fun j _ => sq_nonneg (y j))
      ⟨i, Finset.mem_univ _, sq_pos_of_ne_zero hi⟩
  simpa using finrank_le_negativeInertia_of_negative_map
    (homogeneousMatrix_hermitian r w) (replicateDirection r a b) hE

theorem discriminant_of_inertia_le_one {r : ℕ} (hr : 2 ≤ r) (w : Fin 3 → ℝ)
    (hw : ∀ i, 0 ≤ w i)
    (hi : negativeInertia (homogeneousMatrix_hermitian r w) ≤ 1) :
    w 2 ^ 2 ≤ 4 * w 0 * w 1 := by
  by_contra hn
  have := inertia_ge_dimension_of_bad_discriminant (r := r) w hw (lt_of_not_ge hn)
  omega

/-- The homogeneous constant is strictly negative for every nonzero multiplier
in the second-order cone. -/
theorem constant_neg_of_goodCone (w : Fin 3 → ℝ) (hw : ∀ i, 0 ≤ w i)
    (hd : w 2 ^ 2 ≤ 4 * w 0 * w 1) (hne : w ≠ 0) :
    w 2 / 2 - w 0 - w 1 < 0 := by
  have hs : 0 < w 0 + w 1 := by
    by_contra hn
    have h0 : w 0 = 0 := by linarith [hw 0, hw 1]
    have h1 : w 1 = 0 := by linarith [hw 0, hw 1]
    have h2 : w 2 = 0 := by nlinarith [sq_nonneg (w 2)]
    apply hne
    ext i
    fin_cases i <;> simp [h0, h1, h2]
  have hb : w 2 ≤ w 0 + w 1 := by
    nlinarith [sq_nonneg (w 0 - w 1), hw 2]
  linarith

end InfiniteAggregation
