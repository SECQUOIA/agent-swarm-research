import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.LinearAlgebra.Matrix.Charpoly.Coeff
import Mathlib.Tactic
import Mathlib.LinearAlgebra.AffineSpace.AffineMap

open scoped BigOperators Matrix
open Matrix
namespace QuadraticPrecision
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

noncomputable def spectralCoordinate {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (j : ι) (x : ι → ℝ) : ℝ :=
  (star (hH.eigenvectorUnitary : Matrix ι ι ℝ) *ᵥ x) j

theorem spectral_quadratic {H : Matrix ι ι ℝ} (hH : H.IsHermitian) (x : ι → ℝ) :
    dotProduct x (H *ᵥ x) = ∑ j, hH.eigenvalues j * spectralCoordinate hH j x ^ 2 := by
  conv_lhs => rw [hH.spectral_theorem, Unitary.conjStarAlgAut_apply]
  simp only [← Matrix.mulVec_mulVec, RCLike.ofReal_real_eq_id, Function.id_comp]
  rw [Matrix.dotProduct_mulVec]
  have h : x ᵥ* (hH.eigenvectorUnitary : Matrix ι ι ℝ) =
      star (hH.eigenvectorUnitary : Matrix ι ι ℝ) *ᵥ x := by
    ext j
    simp [Matrix.vecMul, Matrix.mulVec,
      dotProduct, mul_comm]
  rw [h]
  simp only [Matrix.mulVec_diagonal, dotProduct]
  apply Finset.sum_congr rfl
  intro j _
  dsimp [spectralCoordinate]
  ring

theorem spectral_rank {H : Matrix ι ι ℝ} (hH : H.IsHermitian) :
    H.rank = Fintype.card {j // hH.eigenvalues j ≠ 0} :=
  hH.rank_eq_card_non_zero_eigs

noncomputable def negativeInertia {H : Matrix ι ι ℝ} (hH : H.IsHermitian) : ℕ :=
  Fintype.card {j // hH.eigenvalues j < 0}
noncomputable def positiveInertia {H : Matrix ι ι ℝ} (hH : H.IsHermitian) : ℕ :=
  Fintype.card {j // 0 < hH.eigenvalues j}

/-- A positive radius enclosing a linear functional on a finite box. The extra
unit avoids a separate zero-functional branch. Exact extrema are unnecessary. -/
noncomputable def linearBoxRadius (v l u : ι → ℝ) : ℝ :=
  1 + ∑ i, |v i| * max |l i| |u i|

omit [DecidableEq ι] in
theorem linearBoxRadius_pos (v l u : ι → ℝ) : 0 < linearBoxRadius v l u := by
  have : 0 ≤ ∑ i, |v i| * max |l i| |u i| :=
    Finset.sum_nonneg fun i _ => mul_nonneg (abs_nonneg _) (le_max_of_le_left (abs_nonneg _))
  unfold linearBoxRadius
  linarith

omit [DecidableEq ι] in
theorem linearBoxRadius_bound (v l u x : ι → ℝ)
    (hx : ∀ i, x i ∈ Set.Icc (l i) (u i)) :
    |dotProduct v x| ≤ linearBoxRadius v l u := by
  have hi : ∀ i, |x i| ≤ max |l i| |u i| := by
    intro i
    apply abs_le.mpr
    constructor
    · have := neg_abs_le (l i)
      have := le_max_left |l i| |u i|
      linarith [(hx i).1]
    · exact le_trans (hx i).2 (le_trans (le_abs_self _) (le_max_right _ _))
  calc
    |dotProduct v x| ≤ ∑ i, |v i * x i| := Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ i, |v i| * max |l i| |u i| := by
      apply Finset.sum_le_sum
      intro i _
      rw [abs_mul]
      exact mul_le_mul_of_nonneg_left (hi i) (abs_nonneg _)
    _ ≤ linearBoxRadius v l u := by unfold linearBoxRadius; linarith

noncomputable def normalizedLinear (v l u x : ι → ℝ) : ℝ :=
  (dotProduct v x + linearBoxRadius v l u) / (2 * linearBoxRadius v l u)

omit [DecidableEq ι] in
theorem normalizedLinear_mem (v l u x : ι → ℝ)
    (hx : ∀ i, x i ∈ Set.Icc (l i) (u i)) :
    normalizedLinear v l u x ∈ Set.Icc (0 : ℝ) 1 := by
  have hr := linearBoxRadius_pos v l u
  have hb := abs_le.mp (linearBoxRadius_bound v l u x hx)
  dsimp [normalizedLinear]
  constructor
  · exact div_nonneg (by linarith) (by positivity)
  · apply (div_le_one (by positivity : 0 < 2 * linearBoxRadius v l u)).mpr
    linarith

omit [DecidableEq ι] in
theorem normalizedLinear_square (v l u x : ι → ℝ) :
    dotProduct v x ^ 2 = (2 * linearBoxRadius v l u) ^ 2 *
      normalizedLinear v l u x ^ 2 -
      2 * linearBoxRadius v l u * dotProduct v x - linearBoxRadius v l u ^ 2 := by
  have hr := ne_of_gt (linearBoxRadius_pos v l u)
  dsimp [normalizedLinear]
  field_simp
  ring

noncomputable def spectralVector {H : Matrix ι ι ℝ} (hH : H.IsHermitian) (j : ι) : ι → ℝ :=
  star (hH.eigenvectorUnitary : Matrix ι ι ℝ) j

theorem spectralCoordinate_eq_dotProduct {H : Matrix ι ι ℝ}
    (hH : H.IsHermitian) (j : ι) (x : ι → ℝ) :
    spectralCoordinate hH j x = dotProduct (spectralVector hH j) x := rfl

/-- The signed coefficients in the normalized square representation. -/
noncomputable def spectralCoefficient {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) (j : ι) : ℝ :=
  hH.eigenvalues j / 2 * (2 * linearBoxRadius (spectralVector hH j) l u) ^ 2

noncomputable def spectralNormalized {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) (j : ι) (x : ι → ℝ) : ℝ :=
  normalizedLinear (spectralVector hH j) l u x

noncomputable def spectralAffine {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (a : ι → ℝ) (b : ℝ) (l u : ι → ℝ) (x : ι → ℝ) : ℝ :=
  dotProduct x a + b + ∑ j, hH.eigenvalues j / 2 *
    (-2 * linearBoxRadius (spectralVector hH j) l u * spectralCoordinate hH j x -
      linearBoxRadius (spectralVector hH j) l u ^ 2)

theorem spectralCoefficient_pos_iff {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) (j : ι) :
    0 < spectralCoefficient hH l u j ↔ 0 < hH.eigenvalues j := by
  have hr := linearBoxRadius_pos (spectralVector hH j) l u
  dsimp [spectralCoefficient]
  rw [mul_pos_iff_of_pos_right (by positivity), div_pos_iff_of_pos_right (by norm_num)]

theorem spectralCoefficient_neg_iff {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) (j : ι) :
    spectralCoefficient hH l u j < 0 ↔ hH.eigenvalues j < 0 := by
  have hr := linearBoxRadius_pos (spectralVector hH j) l u
  dsimp [spectralCoefficient]
  have hp : 0 < (2 * linearBoxRadius (spectralVector hH j) l u) ^ 2 := by positivity
  constructor
  · intro h
    by_contra hn
    have : 0 ≤ hH.eigenvalues j / 2 * (2 * linearBoxRadius (spectralVector hH j) l u) ^ 2 :=
      mul_nonneg (div_nonneg (le_of_not_gt hn) (by norm_num)) (le_of_lt hp)
    linarith
  · intro h
    exact mul_neg_of_neg_of_pos (div_neg_of_neg_of_pos h (by norm_num)) hp

theorem spectralCoefficient_eq_zero_iff {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) (j : ι) :
    spectralCoefficient hH l u j = 0 ↔ hH.eigenvalues j = 0 := by
  have hr := ne_of_gt (linearBoxRadius_pos (spectralVector hH j) l u)
  simp [spectralCoefficient, hr]

theorem spectralNormalized_mem {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) (j : ι) (x : ι → ℝ) (hx : ∀ i, x i ∈ Set.Icc (l i) (u i)) :
    spectralNormalized hH l u j x ∈ Set.Icc (0 : ℝ) 1 :=
  normalizedLinear_mem _ _ _ _ hx

/-- Normalized signed-square decomposition of the actual quadratic polynomial. -/
theorem spectral_signed_decomposition {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (a : ι → ℝ) (b : ℝ) (l u x : ι → ℝ) :
    dotProduct x (H *ᵥ x) / 2 + dotProduct x a + b =
      spectralAffine hH a b l u x +
        ∑ j, spectralCoefficient hH l u j * spectralNormalized hH l u j x ^ 2 := by
  rw [spectral_quadratic hH]
  simp only [spectralAffine, Finset.sum_div ]
  have hi : ∀ j, hH.eigenvalues j * spectralCoordinate hH j x ^ 2 / 2 =
      hH.eigenvalues j / 2 *
        (-2 * linearBoxRadius (spectralVector hH j) l u * spectralCoordinate hH j x -
          linearBoxRadius (spectralVector hH j) l u ^ 2) +
      spectralCoefficient hH l u j * spectralNormalized hH l u j x ^ 2 := by
    intro j
    have he := normalizedLinear_square (spectralVector hH j) l u x
    dsimp [spectralCoefficient, spectralNormalized]
    rw [spectralCoordinate_eq_dotProduct]
    rw [he]
    ring
  simp_rw [hi]
  simp only [Finset.sum_add_distrib]
  ring

noncomputable def linearFunctional (v : ι → ℝ) : (ι → ℝ) →ᵃ[ℝ] ℝ :=
  (dotProductBilin ℝ ℝ v).toAffineMap

omit [DecidableEq ι] in
@[simp] theorem linearFunctional_apply (v x : ι → ℝ) :
    linearFunctional v x = dotProduct v x := rfl

noncomputable def normalizedLinearMap (v l u : ι → ℝ) : (ι → ℝ) →ᵃ[ℝ] ℝ :=
  (2 * linearBoxRadius v l u)⁻¹ •
    (linearFunctional v + AffineMap.const ℝ (ι → ℝ) (linearBoxRadius v l u))

omit [DecidableEq ι] in
@[simp] theorem normalizedLinearMap_apply (v l u x : ι → ℝ) :
    normalizedLinearMap v l u x = normalizedLinear v l u x := by
  simp [normalizedLinearMap, normalizedLinear, div_eq_mul_inv, mul_comm]
  ring

noncomputable def spectralNormalizedMap {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) (j : ι) : (ι → ℝ) →ᵃ[ℝ] ℝ :=
  normalizedLinearMap (spectralVector hH j) l u

@[simp] theorem spectralNormalizedMap_apply {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) (j : ι) (x : ι → ℝ) :
    spectralNormalizedMap hH l u j x = spectralNormalized hH l u j x :=
  normalizedLinearMap_apply _ _ _ _

omit [Fintype ι] [DecidableEq ι] in
theorem affine_sum_apply {κ : Type*} (s : Finset κ) (f : κ → (ι → ℝ) →ᵃ[ℝ] ℝ)
    (x : ι → ℝ) : (∑ j ∈ s, f j) x = ∑ j ∈ s, f j x := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert j s hj ih => simp [Finset.sum_insert, hj, ih, AffineMap.coe_add]

noncomputable def spectralAffineMap {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (a : ι → ℝ) (b : ℝ) (l u : ι → ℝ) : (ι → ℝ) →ᵃ[ℝ] ℝ :=
  linearFunctional a + AffineMap.const ℝ (ι → ℝ) b +
    ∑ j, (hH.eigenvalues j / 2) •
      ((-2 * linearBoxRadius (spectralVector hH j) l u) • linearFunctional (spectralVector hH j) -
        AffineMap.const ℝ (ι → ℝ) (linearBoxRadius (spectralVector hH j) l u ^ 2))

@[simp] theorem spectralAffineMap_apply {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (a : ι → ℝ) (b : ℝ) (l u x : ι → ℝ) :
    spectralAffineMap hH a b l u x = spectralAffine hH a b l u x := by
  simp [spectralAffineMap, spectralAffine, spectralCoordinate_eq_dotProduct,
    dotProduct_comm, affine_sum_apply]

/-- Only nonzero eigenvalues are retained: there are exactly `rank H` squares. -/
theorem spectral_signed_decomposition_nonzero {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (a : ι → ℝ) (b : ℝ) (l u x : ι → ℝ) :
    dotProduct x (H *ᵥ x) / 2 + dotProduct x a + b =
      spectralAffineMap hH a b l u x +
        ∑ j : {j // hH.eigenvalues j ≠ 0},
          spectralCoefficient hH l u j * spectralNormalizedMap hH l u j x ^ 2 := by
  simp only [spectralAffineMap_apply, spectralNormalizedMap_apply]
  rw [spectral_signed_decomposition hH a b l u x]
  congr 1
  symm
  classical
  rw [← Finset.sum_subtype (p := fun j => hH.eigenvalues j ≠ 0)
    (Finset.univ.filter (fun j => hH.eigenvalues j ≠ 0)) (by simp)
    (fun j => spectralCoefficient hH l u j * spectralNormalized hH l u j x ^ 2)]
  apply Finset.sum_filter_of_ne
  intro j _ hj he
  have hc := (spectralCoefficient_eq_zero_iff hH l u j).mpr he
  simp [hc] at hj

theorem spectral_totalWeight_pos {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) (hr : 0 < H.rank) :
    0 < ∑ j : {j // hH.eigenvalues j ≠ 0}, |spectralCoefficient hH l u j| := by
  classical
  have hn : Nonempty {j // hH.eigenvalues j ≠ 0} :=
    Fintype.card_pos_iff.mp (by rwa [← spectral_rank hH])
  let j := Classical.choice hn
  apply Finset.sum_pos' (fun _ _ => abs_nonneg _)
  refine ⟨j, Finset.mem_univ _, abs_pos.mpr ?_⟩
  exact fun hc => j.property ((spectralCoefficient_eq_zero_iff hH l u j).mp hc)

omit [DecidableEq ι] in
theorem rank_zero_affine {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (hr : H.rank = 0) (a x : ι → ℝ) (b : ℝ) :
    dotProduct x (H *ᵥ x) / 2 + dotProduct x a + b = dotProduct x a + b := by
  classical
  have hn : IsEmpty {j // hH.eigenvalues j ≠ 0} :=
    Fintype.card_eq_zero_iff.mp (by rwa [← spectral_rank hH])
  have hz : hH.eigenvalues = 0 := by
    funext j
    by_contra hj
    exact hn.false ⟨j, hj⟩
  have hh := hH.eigenvalues_eq_zero_iff.mp hz
  simp [hh]

theorem rank_eq_inertia_sum {H : Matrix ι ι ℝ} (hH : H.IsHermitian) :
    H.rank = negativeInertia hH + positiveInertia hH := by
  classical
  rw [spectral_rank hH]
  calc
    _ = Fintype.card {j // hH.eigenvalues j < 0 ∨ 0 < hH.eigenvalues j} :=
      Fintype.card_congr (Equiv.subtypeEquivRight (fun j => ne_iff_lt_or_gt))
    _ = _ := Fintype.card_subtype_or_disjoint _ _ (by
    intro p hp hn j hj
    exact False.elim (lt_asymm (hp j hj) (hn j hj)))

noncomputable def spectralNegativeEquiv {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) :
    {j : {j // hH.eigenvalues j ≠ 0} // spectralCoefficient hH l u j < 0} ≃
      {j // hH.eigenvalues j < 0} where
  toFun j := ⟨j.1.1, (spectralCoefficient_neg_iff hH l u j.1).mp j.2⟩
  invFun j := ⟨⟨j.1, ne_of_lt j.2⟩, (spectralCoefficient_neg_iff hH l u j).mpr j.2⟩
  left_inv _ := rfl
  right_inv _ := rfl

theorem spectral_negative_count {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) :
    Fintype.card {j : {j // hH.eigenvalues j ≠ 0} // spectralCoefficient hH l u j < 0} =
      negativeInertia hH := Fintype.card_congr (spectralNegativeEquiv hH l u)

noncomputable def spectralPositiveEquiv {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) :
    {j : {j // hH.eigenvalues j ≠ 0} // 0 < spectralCoefficient hH l u j} ≃
      {j // 0 < hH.eigenvalues j} where
  toFun j := ⟨j.1.1, (spectralCoefficient_pos_iff hH l u j.1).mp j.2⟩
  invFun j := ⟨⟨j.1, ne_of_gt j.2⟩, (spectralCoefficient_pos_iff hH l u j).mpr j.2⟩
  left_inv _ := rfl
  right_inv _ := rfl

theorem spectral_positive_count {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (l u : ι → ℝ) :
    Fintype.card {j : {j // hH.eigenvalues j ≠ 0} // 0 < spectralCoefficient hH l u j} =
      positiveInertia hH := Fintype.card_congr (spectralPositiveEquiv hH l u)

end QuadraticPrecision
