import Formal.QuadraticPrecision.Spectral

open scoped BigOperators Matrix
open Matrix
namespace QuadraticPrecision
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

noncomputable def negativeExtend {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (t : {j // hH.eigenvalues j < 0} → ℝ) : ι → ℝ :=
  fun j => if hj : hH.eigenvalues j < 0 then t ⟨j, hj⟩ else 0

noncomputable def negativeEmbedding {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (t : {j // hH.eigenvalues j < 0} → ℝ) : ι → ℝ :=
  (hH.eigenvectorUnitary : Matrix ι ι ℝ) *ᵥ negativeExtend hH t

theorem negativeEmbedding_coordinate {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (t : {j // hH.eigenvalues j < 0} → ℝ) (j : ι) :
    spectralCoordinate hH j (negativeEmbedding hH t) = negativeExtend hH t j := by
  change (star (hH.eigenvectorUnitary : Matrix ι ι ℝ) *ᵥ
    ((hH.eigenvectorUnitary : Matrix ι ι ℝ) *ᵥ negativeExtend hH t)) j = _
  rw [Matrix.mulVec_mulVec, Unitary.coe_star_mul_self, Matrix.one_mulVec]

theorem negativeEmbedding_injective {H : Matrix ι ι ℝ} (hH : H.IsHermitian) :
    Function.Injective (negativeEmbedding hH) := by
  intro s t he
  funext j
  have hc := congrArg (spectralCoordinate hH j) he
  simp only [negativeEmbedding_coordinate, negativeExtend, dif_pos j.property] at hc
  exact hc

/-- A uniform strictly positive lower bound for finitely many positive reals,
including the empty family. -/
theorem finite_positive_lower_bound {κ : Type*} [Finite κ] (f : κ → ℝ)
    (hf : ∀ i, 0 < f i) : ∃ m : ℝ, 0 < m ∧ ∀ i, m ≤ f i := by
  classical
  let := Fintype.ofFinite κ
  suffices ∀ s : Finset κ, ∃ m : ℝ, 0 < m ∧ ∀ i ∈ s, m ≤ f i by
    obtain ⟨m, hm, hb⟩ := this Finset.univ
    exact ⟨m, hm, fun i => hb i (Finset.mem_univ i)⟩
  intro s
  induction s using Finset.induction_on with
  | empty => exact ⟨1, by norm_num, by simp⟩
  | @insert i s hi ih =>
    obtain ⟨m, hm, hb⟩ := ih
    refine ⟨min m (f i), lt_min hm (hf i), ?_⟩
    intro j hj
    rcases Finset.mem_insert.mp hj with rfl | hj
    · exact min_le_right _ _
    · exact le_trans (min_le_left _ _) (hb j hj)

theorem negativeEmbedding_quadratic {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (t : {j // hH.eigenvalues j < 0} → ℝ) :
    dotProduct (negativeEmbedding hH t) (H *ᵥ negativeEmbedding hH t) =
      ∑ j : {j // hH.eigenvalues j < 0}, hH.eigenvalues j * t j ^ 2 := by
  classical
  rw [spectral_quadratic hH]
  simp_rw [negativeEmbedding_coordinate]
  have hf : (∑ j ∈ Finset.univ.filter (fun j => hH.eigenvalues j < 0),
      hH.eigenvalues j * negativeExtend hH t j ^ 2) =
      ∑ j, hH.eigenvalues j * negativeExtend hH t j ^ 2 := by
    apply Finset.sum_filter_of_ne
    intro j _ hj
    by_contra hn
    simp [negativeExtend, hn] at hj
  rw [← hf, Finset.sum_subtype (p := fun j => hH.eigenvalues j < 0) (F := inferInstance)
    (Finset.univ.filter (fun j => hH.eigenvalues j < 0)) (by simp)]
  apply Finset.sum_congr rfl
  intro j _
  simp [negativeExtend, j.property]

theorem negativeEmbedding_coercive {H : Matrix ι ι ℝ} (hH : H.IsHermitian) :
    ∃ m : ℝ, 0 < m ∧ ∀ t : {j // hH.eigenvalues j < 0} → ℝ,
      dotProduct (negativeEmbedding hH t) (H *ᵥ negativeEmbedding hH t) ≤
        -m * ∑ j, t j ^ 2 := by
  classical
  obtain ⟨m, hm, hb⟩ := finite_positive_lower_bound
    (fun j : {j // hH.eigenvalues j < 0} => -hH.eigenvalues j)
    (fun j => neg_pos.mpr j.property)
  refine ⟨m, hm, fun t => ?_⟩
  rw [negativeEmbedding_quadratic, Finset.mul_sum]
  apply Finset.sum_le_sum
  intro j _
  exact mul_le_mul_of_nonneg_right (by linarith [hb j]) (sq_nonneg _)

omit [Fintype ι] [DecidableEq ι] in
/-- Every linear image of a sufficiently small full box fits in the interior
of a given nondegenerate box, centered at its midpoint. -/
theorem matrix_small_box [Finite ι] {κ : Type*} [Fintype κ] (T : Matrix ι κ ℝ)
    (l u : ι → ℝ) (hlu : ∀ i, l i < u i) :
    ∃ ρ : ℝ, 0 < ρ ∧ ∀ t : κ → ℝ, (∀ j, |t j| ≤ ρ) →
      ∀ i, (l i + u i) / 2 + (T *ᵥ t) i ∈ Set.Icc (l i) (u i) := by
  let := Fintype.ofFinite ι
  obtain ⟨ρ, hρ, hb⟩ := finite_positive_lower_bound
    (fun i => ((u i - l i) / 2) / (1 + ∑ j, |T i j|)) (by
      intro i
      have hs : 0 ≤ ∑ j, |T i j| := Finset.sum_nonneg (fun j _ => abs_nonneg _)
      exact div_pos (by linarith [hlu i]) (by linarith))
  refine ⟨ρ, hρ, fun t ht i => ?_⟩
  have hs : 0 ≤ ∑ j, |T i j| := Finset.sum_nonneg (fun j _ => abs_nonneg _)
  have hd : 0 < 1 + ∑ j, |T i j| := by linarith
  have hb' := (le_div_iff₀ hd).mp (hb i)
  have hprod : |(T *ᵥ t) i| ≤ ρ * ∑ j, |T i j| := by
    calc
      |(T *ᵥ t) i| ≤ ∑ j, |T i j * t j| := Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ j, ρ * |T i j| := by
        apply Finset.sum_le_sum
        intro j _
        rw [abs_mul, mul_comm ρ]
        exact mul_le_mul_of_nonneg_left (ht j) (abs_nonneg _)
      _ = ρ * ∑ j, |T i j| := (Finset.mul_sum _ _ _).symm
  have ha := abs_le.mp hprod
  constructor <;> linarith

/-- The actual negative eigenspace contains a full parameter box whose image
lies in the original box. No slice or factorization is assumed. -/
theorem negativeEmbedding_small_box {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) (hlu : ∀ i, l i < u i) :
    ∃ ρ : ℝ, 0 < ρ ∧ ∀ t : {j // hH.eigenvalues j < 0} → ℝ,
      (∀ j, |t j| ≤ ρ) → ∀ i,
      (l i + u i) / 2 + negativeEmbedding hH t i ∈ Set.Icc (l i) (u i) := by
  obtain ⟨ρ, hρ, hb⟩ := matrix_small_box (hH.eigenvectorUnitary : Matrix ι ι ℝ) l u hlu
  refine ⟨ρ, hρ, fun t ht => hb (negativeExtend hH t) ?_⟩
  intro j
  dsimp [negativeExtend]
  split_ifs with hj
  · exact ht ⟨j, hj⟩
  · simpa using le_of_lt hρ

noncomputable def negativeExtendLinear {H : Matrix ι ι ℝ} (hH : H.IsHermitian) :
    ({j // hH.eigenvalues j < 0} → ℝ) →ₗ[ℝ] (ι → ℝ) where
  toFun := negativeExtend hH
  map_add' s t := by
    funext j
    dsimp [negativeExtend]
    split_ifs <;> simp
  map_smul' c t := by
    funext j
    dsimp [negativeExtend]
    split_ifs <;> simp

noncomputable def negativeEmbeddingLinear {H : Matrix ι ι ℝ} (hH : H.IsHermitian) :
    ({j // hH.eigenvalues j < 0} → ℝ) →ₗ[ℝ] (ι → ℝ) :=
  Matrix.mulVecLin (hH.eigenvectorUnitary : Matrix ι ι ℝ) ∘ₗ negativeExtendLinear hH

@[simp] theorem negativeEmbeddingLinear_apply {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (t : {j // hH.eigenvalues j < 0} → ℝ) :
    negativeEmbeddingLinear hH t = negativeEmbedding hH t := rfl

noncomputable def negativeSliceMap {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) : ({j // hH.eigenvalues j < 0} → ℝ) →ᵃ[ℝ] (ι → ℝ) :=
  (negativeEmbeddingLinear hH).toAffineMap +
    AffineMap.const ℝ _ (fun i => (l i + u i) / 2)

@[simp] theorem negativeSliceMap_apply {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) (t : {j // hH.eigenvalues j < 0} → ℝ) (i : ι) :
    negativeSliceMap hH l u t i = (l i + u i) / 2 + negativeEmbedding hH t i := by
  simp [negativeSliceMap, add_comm]

theorem negativeSliceMap_injective {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) : Function.Injective (negativeSliceMap hH l u) := by
  intro s t h
  apply negativeEmbedding_injective hH
  funext i
  have hi := congrFun h i
  simp only [negativeSliceMap_apply, add_right_inj] at hi
  exact hi

end QuadraticPrecision
