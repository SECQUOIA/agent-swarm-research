import Formal.QuadraticPrecision.SpectralSlice

open scoped BigOperators Matrix
open Matrix QuadraticPrecision

namespace InfiniteAggregation

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Restriction of spectral coordinates to the negative eigenvalues. -/
noncomputable def negativeProjectionLinear {H : Matrix ι ι ℝ} (hH : H.IsHermitian) :
    (ι → ℝ) →ₗ[ℝ] ({j // hH.eigenvalues j < 0} → ℝ) where
  toFun x j := spectralCoordinate hH j x
  map_add' x y := by
    funext j
    simp [spectralCoordinate, Matrix.mulVec_add]
  map_smul' c x := by
    funext j
    simp [spectralCoordinate, Matrix.mulVec_smul]

/-- Vanishing negative spectral coordinates leave only nonnegative terms. -/
theorem quadratic_nonneg_of_negativeProjection_eq_zero
    {H : Matrix ι ι ℝ} (hH : H.IsHermitian) (x : ι → ℝ)
    (hx : negativeProjectionLinear hH x = 0) :
    0 ≤ dotProduct x (H *ᵥ x) := by
  rw [spectral_quadratic hH]
  apply Finset.sum_nonneg
  intro j _
  by_cases hj : hH.eigenvalues j < 0
  · have hz : spectralCoordinate hH j x = 0 := congrFun hx ⟨j, hj⟩
    simp [hz]
  · exact mul_nonneg (le_of_not_gt hj) (sq_nonneg _)

/-- Every negative definite linear parameterization has dimension at most the
number of negative eigenvalues of the original symmetric matrix. -/
theorem finrank_le_negativeInertia_of_negative_map
    {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    {V : Type*} [AddCommGroup V] [Module ℝ V]
    (E : V →ₗ[ℝ] (ι → ℝ))
    (hE : ∀ x, x ≠ 0 → dotProduct (E x) (H *ᵥ E x) < 0) :
    Module.finrank ℝ V ≤ negativeInertia hH := by
  classical
  have hi : Function.Injective ((negativeProjectionLinear hH).comp E) := by
    apply LinearMap.ker_eq_bot.mp
    apply LinearMap.ker_eq_bot'.mpr
    intro x hx
    by_contra hn
    exact (not_lt_of_ge (quadratic_nonneg_of_negativeProjection_eq_zero hH (E x) hx))
      (hE x hn)
  have hd := LinearMap.finrank_le_finrank_of_injective hi
  simpa [negativeInertia, Module.finrank_pi] using hd

/-- The genuine negative spectral subspace is strictly negative off zero. -/
theorem negativeEmbedding_quadratic_neg {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (t : {j // hH.eigenvalues j < 0} → ℝ) (ht : t ≠ 0) :
    dotProduct (negativeEmbedding hH t) (H *ᵥ negativeEmbedding hH t) < 0 := by
  classical
  rw [negativeEmbedding_quadratic hH]
  apply Finset.sum_neg'
  · intro j _
    exact mul_nonpos_of_nonpos_of_nonneg (le_of_lt j.property) (sq_nonneg _)
  · obtain ⟨j, hj⟩ : ∃ j, t j ≠ 0 := by
      by_contra hn
      apply ht
      ext j
      simpa using not_exists.mp hn j
    exact ⟨j, Finset.mem_univ _, mul_neg_of_neg_of_pos j.property (sq_pos_of_ne_zero hj)⟩

/-- If a quadratic form is nonnegative on the kernel of one linear functional,
it has at most one negative eigenvalue, counted with multiplicity. -/
theorem negativeInertia_le_one_of_nonneg_on_kernel
    {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (ℓ : (ι → ℝ) →ₗ[ℝ] ℝ)
    (hℓ : ∀ x, ℓ x = 0 → 0 ≤ dotProduct x (H *ᵥ x)) :
    negativeInertia hH ≤ 1 := by
  classical
  have hi : Function.Injective (ℓ.comp (negativeEmbeddingLinear hH)) := by
    apply LinearMap.ker_eq_bot.mp
    apply LinearMap.ker_eq_bot'.mpr
    intro t ht
    by_contra hn
    exact (not_lt_of_ge (hℓ (negativeEmbedding hH t) ht))
      (negativeEmbedding_quadratic_neg hH t hn)
  have hd := LinearMap.finrank_le_finrank_of_injective hi
  simpa [negativeInertia, Module.finrank_pi] using hd

/-- A negative vector forces at least one negative eigenvalue. -/
theorem one_le_negativeInertia_of_negative_vector
    {H : Matrix ι ι ℝ} (hH : H.IsHermitian) (x : ι → ℝ)
    (hx : dotProduct x (H *ᵥ x) < 0) :
    1 ≤ negativeInertia hH := by
  classical
  obtain ⟨j, hj⟩ : ∃ j, hH.eigenvalues j < 0 := by
    by_contra hn
    have hq : 0 ≤ dotProduct x (H *ᵥ x) := by
      rw [spectral_quadratic hH]
      exact Finset.sum_nonneg fun j _ =>
        mul_nonneg (le_of_not_gt (not_exists.mp hn j)) (sq_nonneg _)
    exact (not_lt_of_ge hq) hx
  exact Fintype.card_pos_iff.mpr ⟨⟨j, hj⟩⟩

/-- A negative two-dimensional parameterization forces two negative eigenvalues. -/
theorem two_le_negativeInertia_of_negative_map
    {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (E : (Fin 2 → ℝ) →ₗ[ℝ] (ι → ℝ))
    (hE : ∀ x, x ≠ 0 → dotProduct (E x) (H *ᵥ E x) < 0) :
    2 ≤ negativeInertia hH := by
  simpa using finrank_le_negativeInertia_of_negative_map hH E hE

end InfiniteAggregation
