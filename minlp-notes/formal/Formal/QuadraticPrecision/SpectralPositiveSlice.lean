import Formal.QuadraticPrecision.SpectralSlice

open scoped BigOperators Matrix
open Matrix
namespace QuadraticPrecision
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

noncomputable def positiveExtend {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (t : {j // 0 < hH.eigenvalues j} → ℝ) : ι → ℝ :=
  fun j => if hj : 0 < hH.eigenvalues j then t ⟨j, hj⟩ else 0

noncomputable def positiveEmbedding {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (t : {j // 0 < hH.eigenvalues j} → ℝ) : ι → ℝ :=
  (hH.eigenvectorUnitary : Matrix ι ι ℝ) *ᵥ positiveExtend hH t

theorem positiveEmbedding_coordinate {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (t : {j // 0 < hH.eigenvalues j} → ℝ) (j : ι) :
    spectralCoordinate hH j (positiveEmbedding hH t) = positiveExtend hH t j := by
  change (star (hH.eigenvectorUnitary : Matrix ι ι ℝ) *ᵥ
    ((hH.eigenvectorUnitary : Matrix ι ι ℝ) *ᵥ positiveExtend hH t)) j = _
  rw [Matrix.mulVec_mulVec, Unitary.coe_star_mul_self, Matrix.one_mulVec]

theorem positiveEmbedding_injective {H : Matrix ι ι ℝ} (hH : H.IsHermitian) :
    Function.Injective (positiveEmbedding hH) := by
  intro s t he
  funext j
  have hc := congrArg (spectralCoordinate hH j) he
  simp only [positiveEmbedding_coordinate, positiveExtend, dif_pos j.property] at hc
  exact hc

theorem positiveEmbedding_quadratic {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (t : {j // 0 < hH.eigenvalues j} → ℝ) :
    dotProduct (positiveEmbedding hH t) (H *ᵥ positiveEmbedding hH t) =
      ∑ j : {j // 0 < hH.eigenvalues j}, hH.eigenvalues j * t j ^ 2 := by
  classical
  rw [spectral_quadratic hH]
  simp_rw [positiveEmbedding_coordinate]
  have hf : (∑ j ∈ Finset.univ.filter (fun j => 0 < hH.eigenvalues j),
      hH.eigenvalues j * positiveExtend hH t j ^ 2) =
      ∑ j, hH.eigenvalues j * positiveExtend hH t j ^ 2 := by
    apply Finset.sum_filter_of_ne
    intro j _ hj
    by_contra hn
    simp [positiveExtend, hn] at hj
  rw [← hf, Finset.sum_subtype (p := fun j => 0 < hH.eigenvalues j) (F := inferInstance)
    (Finset.univ.filter (fun j => 0 < hH.eigenvalues j)) (by simp)]
  apply Finset.sum_congr rfl
  intro j _
  simp [positiveExtend, j.property]

theorem positiveEmbedding_coercive {H : Matrix ι ι ℝ} (hH : H.IsHermitian) :
    ∃ m : ℝ, 0 < m ∧ ∀ t : {j // 0 < hH.eigenvalues j} → ℝ,
      m * (∑ j, t j ^ 2) ≤
        dotProduct (positiveEmbedding hH t) (H *ᵥ positiveEmbedding hH t) := by
  classical
  obtain ⟨m, hm, hb⟩ := finite_positive_lower_bound
    (fun j : {j // 0 < hH.eigenvalues j} => hH.eigenvalues j)
    (fun j => j.property)
  refine ⟨m, hm, fun t => ?_⟩
  rw [positiveEmbedding_quadratic, Finset.mul_sum]
  apply Finset.sum_le_sum
  intro j _
  exact mul_le_mul_of_nonneg_right (hb j) (sq_nonneg _)

/-- The actual positive eigenspace contains a full parameter box whose image
lies in the original box. No slice or factorization is assumed. -/
theorem positiveEmbedding_small_box {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) (hlu : ∀ i, l i < u i) :
    ∃ ρ : ℝ, 0 < ρ ∧ ∀ t : {j // 0 < hH.eigenvalues j} → ℝ,
      (∀ j, |t j| ≤ ρ) → ∀ i,
      (l i + u i) / 2 + positiveEmbedding hH t i ∈ Set.Icc (l i) (u i) := by
  obtain ⟨ρ, hρ, hb⟩ := matrix_small_box (hH.eigenvectorUnitary : Matrix ι ι ℝ) l u hlu
  refine ⟨ρ, hρ, fun t ht => hb (positiveExtend hH t) ?_⟩
  intro j
  dsimp [positiveExtend]
  split_ifs with hj
  · exact ht ⟨j, hj⟩
  · simpa using le_of_lt hρ

noncomputable def positiveExtendLinear {H : Matrix ι ι ℝ} (hH : H.IsHermitian) :
    ({j // 0 < hH.eigenvalues j} → ℝ) →ₗ[ℝ] (ι → ℝ) where
  toFun := positiveExtend hH
  map_add' s t := by
    funext j
    dsimp [positiveExtend]
    split_ifs <;> simp
  map_smul' c t := by
    funext j
    dsimp [positiveExtend]
    split_ifs <;> simp

noncomputable def positiveEmbeddingLinear {H : Matrix ι ι ℝ} (hH : H.IsHermitian) :
    ({j // 0 < hH.eigenvalues j} → ℝ) →ₗ[ℝ] (ι → ℝ) :=
  Matrix.mulVecLin (hH.eigenvectorUnitary : Matrix ι ι ℝ) ∘ₗ positiveExtendLinear hH

@[simp] theorem positiveEmbeddingLinear_apply {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (t : {j // 0 < hH.eigenvalues j} → ℝ) :
    positiveEmbeddingLinear hH t = positiveEmbedding hH t := rfl

noncomputable def positiveSliceMap {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) : ({j // 0 < hH.eigenvalues j} → ℝ) →ᵃ[ℝ] (ι → ℝ) :=
  (positiveEmbeddingLinear hH).toAffineMap +
    AffineMap.const ℝ _ (fun i => (l i + u i) / 2)

@[simp] theorem positiveSliceMap_apply {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) (t : {j // 0 < hH.eigenvalues j} → ℝ) (i : ι) :
    positiveSliceMap hH l u t i = (l i + u i) / 2 + positiveEmbedding hH t i := by
  simp [positiveSliceMap, add_comm]

theorem positiveSliceMap_injective {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) : Function.Injective (positiveSliceMap hH l u) := by
  intro s t h
  apply positiveEmbedding_injective hH
  funext i
  have hi := congrFun h i
  simp only [positiveSliceMap_apply, add_right_inj] at hi
  exact hi

end QuadraticPrecision
