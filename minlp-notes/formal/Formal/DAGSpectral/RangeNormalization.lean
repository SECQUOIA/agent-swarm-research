import Formal.DAGSpectral.RatMatrix
import Mathlib.Analysis.Matrix.Order
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.Tactic

/-! Rational rectangular normalization with exact range reconstruction. -/
namespace DAGSpectral
open Matrix
open scoped Matrix BigOperators
variable {I J : Type*} [Fintype I] [Fintype J] [DecidableEq J]

noncomputable def gramLeftInverse (V : Matrix I J ℚ) : Matrix J I ℚ := (Vᵀ * V)⁻¹ * Vᵀ
noncomputable def rangeProjector (V : Matrix I J ℚ) : Matrix I I ℚ := V * gramLeftInverse V
noncomputable def normalizer (V : Matrix I J ℚ) (τ : J → ℚ) : Matrix J I ℚ :=
  diagonal τ * gramLeftInverse V
noncomputable def reconstructor (V : Matrix I J ℚ) (τ : J → ℚ) : Matrix I J ℚ :=
  V * diagonal (fun i => (τ i)⁻¹)

theorem gram_isUnit (V : Matrix I J ℚ) (hV : Function.Injective V.mulVec) :
    IsUnit (Vᵀ * V) := by
  apply Matrix.mulVec_injective_iff_isUnit.mp
  intro x y hxy
  have hz : (Vᵀ * V) *ᵥ (x-y) = 0 := by rw [mulVec_sub, hxy, sub_self]
  rw [← mulVec_mulVec] at hz
  have hd := congrArg (dotProduct (x-y)) hz
  rw [dotProduct_mulVec, vecMul_transpose, dotProduct_zero,
    dotProduct_self_eq_zero] at hd
  have he : V *ᵥ x = V *ᵥ y := by simpa only [mulVec_sub, sub_eq_zero] using hd
  exact hV he

theorem gramLeftInverse_mul (V : Matrix I J ℚ) (hV : Function.Injective V.mulVec) :
    gramLeftInverse V * V = 1 := by
  rw [gramLeftInverse, Matrix.mul_assoc]
  exact Matrix.nonsing_inv_mul _ ((Matrix.isUnit_iff_isUnit_det _).mp (gram_isUnit V hV))

theorem rangeProjector_idempotent (V : Matrix I J ℚ) (hV : Function.Injective V.mulVec) :
    rangeProjector V * rangeProjector V = rangeProjector V := by
  simp only [rangeProjector, Matrix.mul_assoc]
  rw [← Matrix.mul_assoc (gramLeftInverse V), gramLeftInverse_mul V hV, Matrix.one_mul]

theorem rangeProjector_symmetric (V : Matrix I J ℚ) :
    (rangeProjector V)ᵀ = rangeProjector V := by
  simp only [rangeProjector, gramLeftInverse, transpose_mul, transpose_transpose,
    transpose_nonsing_inv]
  simp only [Matrix.mul_assoc]

theorem normalizer_reconstructor (V : Matrix I J ℚ) (hV : Function.Injective V.mulVec)
    (τ : J → ℚ) (hτ : ∀ i, τ i ≠ 0) : normalizer V τ * reconstructor V τ = 1 := by
  have hd : diagonal τ * diagonal (fun i => (τ i)⁻¹) = (1 : Matrix J J ℚ) := by
    rw [diagonal_mul_diagonal]
    simp [hτ]
  rw [normalizer, reconstructor, Matrix.mul_assoc,
    ← Matrix.mul_assoc (gramLeftInverse V), gramLeftInverse_mul V hV, Matrix.one_mul, hd]

theorem reconstructor_normalizer (V : Matrix I J ℚ)
    (τ : J → ℚ) (hτ : ∀ i, τ i ≠ 0) :
    reconstructor V τ * normalizer V τ = rangeProjector V := by
  have hd : diagonal (fun i => (τ i)⁻¹) * diagonal τ = (1 : Matrix J J ℚ) := by
    rw [diagonal_mul_diagonal]
    simp [hτ]
  rw [reconstructor, normalizer, Matrix.mul_assoc,
    ← Matrix.mul_assoc (diagonal (fun i => (τ i)⁻¹)), hd, Matrix.one_mul]
  rfl

/-- Congruence is reversible only for matrices passing the exact range test. -/
theorem reconstruct_retained (V : Matrix I J ℚ) (τ : J → ℚ) (hτ : ∀ i, τ i ≠ 0)
    (Q : Matrix I I ℚ) (hQ : Qᵀ = Q) (hrange : rangeProjector V * Q = Q) :
    reconstructor V τ * (normalizer V τ * Q * (normalizer V τ)ᵀ) *
      (reconstructor V τ)ᵀ = Q := by
  have hr : Q * rangeProjector V = Q := by
    have he := congrArg Matrix.transpose hrange
    simpa only [transpose_mul, hQ, rangeProjector_symmetric] using he
  calc
    _ = (reconstructor V τ * normalizer V τ) * Q *
        (reconstructor V τ * normalizer V τ)ᵀ := by
      simp only [transpose_mul, Matrix.mul_assoc]
    _ = rangeProjector V * Q * rangeProjector V := by
      rw [reconstructor_normalizer V τ hτ, rangeProjector_symmetric]
    _ = Q := by rw [hrange, hr]

theorem normalizer_mul_columns (V : Matrix I J ℚ) (hV : Function.Injective V.mulVec)
    (τ : J → ℚ) : normalizer V τ * V = diagonal τ := by
  rw [normalizer, Matrix.mul_assoc, gramLeftInverse_mul V hV, Matrix.mul_one]

theorem normalizer_reconstructor_real (V : Matrix I J ℚ)
    (hV : Function.Injective V.mulVec) (τ : J → ℚ) (hτ : ∀ i, τ i ≠ 0) :
    ratMatrixReal (normalizer V τ) * ratMatrixReal (reconstructor V τ) = 1 := by
  simpa only [ratMatrixReal_mul, ratMatrixReal_one] using
    congrArg ratMatrixReal (normalizer_reconstructor V hV τ hτ)

theorem gramLeftInverse_mul_real (V : Matrix I J ℚ) (hV : Function.Injective V.mulVec) :
    ratMatrixReal (gramLeftInverse V) * ratMatrixReal V = 1 := by
  simpa only [ratMatrixReal_mul, ratMatrixReal_one] using
    congrArg ratMatrixReal (gramLeftInverse_mul V hV)

omit [Fintype I] [DecidableEq J] in
theorem ratMatrixReal_mulVec_injective_iff [Finite I] (V : Matrix I J ℚ) :
    Function.Injective (ratMatrixReal V).mulVec ↔ Function.Injective V.mulVec := by
  classical
  let := Fintype.ofFinite I
  constructor
  · intro h x y hxy
    have he := congrArg (fun z : I → ℚ => fun i => (z i : ℝ)) hxy
    have hx : (fun j => (x j : ℝ)) = fun j => (y j : ℝ) := by
      apply h
      simpa only [ratMatrixReal_mulVec] using he
    funext j
    exact_mod_cast congrFun hx j
  · intro h x y hxy
    have he := congrArg (fun z => ratMatrixReal (gramLeftInverse V) *ᵥ z) hxy
    simpa only [mulVec_mulVec, gramLeftInverse_mul_real V h, one_mulVec] using he

theorem reconstruct_retained_real (V : Matrix I J ℚ) (τ : J → ℚ) (hτ : ∀ i, τ i ≠ 0)
    (Q : Matrix I I ℚ) (hQ : Qᵀ = Q) (hrange : rangeProjector V * Q = Q) :
    ratMatrixReal (reconstructor V τ) *
      (ratMatrixReal (normalizer V τ) * ratMatrixReal Q *
        (ratMatrixReal (normalizer V τ))ᵀ) * (ratMatrixReal (reconstructor V τ))ᵀ =
      ratMatrixReal Q := by
  simpa only [ratMatrixReal_mul, ratMatrixReal_transpose] using
    congrArg ratMatrixReal (reconstruct_retained V τ hτ Q hQ hrange)

omit [Fintype I] in
theorem reconstructor_mul_diagonal (V : Matrix I J ℚ)
    (τ : J → ℚ) (hτ : ∀ i, τ i ≠ 0) : reconstructor V τ * diagonal τ = V := by
  rw [reconstructor, Matrix.mul_assoc, diagonal_mul_diagonal]
  simp [hτ]

/-- A rectangular congruence with a left inverse has exactly the column range
of its outer matrix when its middle matrix is positive definite. -/
theorem congruence_range_of_posDef (K : Matrix I J ℝ) (T : Matrix J I ℝ)
    (hTK : T * K = 1) (A : Matrix J J ℝ) (hA : A.PosDef) :
    LinearMap.range (K*A*Kᵀ).mulVecLin = LinearMap.range K.mulVecLin := by
  have hKT : Kᵀ*Tᵀ=1 := by
    have he := congrArg Matrix.transpose hTK
    simpa only [transpose_mul, transpose_one] using he
  have hid : (K*A*Kᵀ)*(Tᵀ*A⁻¹)=K := by
    calc
      _ = K * A * (Kᵀ*Tᵀ) * A⁻¹ := by simp only [Matrix.mul_assoc]
      _ = K := by
        rw [hKT, Matrix.mul_one, Matrix.mul_assoc,
          Matrix.mul_nonsing_inv A ((Matrix.isUnit_iff_isUnit_det A).mp hA.isUnit),
          Matrix.mul_one]
  ext y
  constructor
  · rintro ⟨x, rfl⟩
    exact ⟨A *ᵥ (Kᵀ *ᵥ x), by simp only [mulVecLin_apply, mulVec_mulVec, Matrix.mul_assoc]⟩
  · rintro ⟨x, rfl⟩
    exact ⟨(Tᵀ*A⁻¹)*ᵥx, by simp only [mulVecLin_apply, mulVec_mulVec, hid]⟩

omit [Fintype I] in
theorem reconstructor_range_real (V : Matrix I J ℚ)
    (τ : J → ℚ) (hτ : ∀ i, τ i ≠ 0) :
    LinearMap.range (ratMatrixReal (reconstructor V τ)).mulVecLin =
      LinearMap.range (ratMatrixReal V).mulVecLin := by
  have he : ratMatrixReal (reconstructor V τ) * ratMatrixReal (diagonal τ) = ratMatrixReal V := by
    simpa only [ratMatrixReal_mul] using congrArg ratMatrixReal (reconstructor_mul_diagonal V τ hτ)
  ext y
  constructor
  · rintro ⟨x, rfl⟩
    refine ⟨ratMatrixReal (diagonal (fun i => (τ i)⁻¹)) *ᵥ x, ?_⟩
    simp only [reconstructor, ratMatrixReal_mul, mulVecLin_apply, mulVec_mulVec]
  · rintro ⟨x, rfl⟩
    exact ⟨ratMatrixReal (diagonal τ)*ᵥx,
      by simp only [mulVecLin_apply, mulVec_mulVec, he]⟩

/-- Exact range follows from the original rational range test and a positive
normalized matrix, using the actual Gram inverse construction. -/
theorem retained_range_of_normalized_posDef (V : Matrix I J ℚ)
    (hV : Function.Injective V.mulVec) (τ : J → ℚ) (hτ : ∀ i, τ i ≠ 0)
    (Q : Matrix I I ℚ) (hQ : Qᵀ = Q) (hrange : rangeProjector V * Q = Q)
    (hA : (ratMatrixReal (normalizer V τ * Q * (normalizer V τ)ᵀ)).PosDef) :
    LinearMap.range (ratMatrixReal Q).mulVecLin =
      LinearMap.range (ratMatrixReal V).mulVecLin := by
  rw [← reconstruct_retained_real V τ hτ Q hQ hrange]
  rw [congruence_range_of_posDef _ (ratMatrixReal (normalizer V τ))
    (normalizer_reconstructor_real V hV τ hτ) _
    (by simpa only [ratMatrixReal_mul, ratMatrixReal_transpose] using hA)]
  exact reconstructor_range_real V τ hτ

theorem retained_range_of_normalized_floor (V : Matrix I J ℚ)
    (hV : Function.Injective V.mulVec) (τ : J → ℚ) (hτ : ∀ i, τ i ≠ 0)
    (Q : Matrix I I ℚ) (hQ : Qᵀ = Q) (hrange : rangeProjector V * Q = Q)
    (hfloor : (ratMatrixReal (normalizer V τ * Q * (normalizer V τ)ᵀ) - 1).PosSemidef) :
    LinearMap.range (ratMatrixReal Q).mulVecLin =
      LinearMap.range (ratMatrixReal V).mulVecLin := by
  apply retained_range_of_normalized_posDef V hV τ hτ Q hQ hrange
  simpa only [add_sub_cancel] using Matrix.PosDef.one.add_posSemidef hfloor

/-- The selected weighted columns become exactly the diagonal floor. -/
theorem normalizer_selected_diagonal (V : Matrix I J ℚ) (hV : Function.Injective V.mulVec)
    (τ w : J → ℚ) :
    normalizer V τ * (V * diagonal w * Vᵀ) * (normalizer V τ)ᵀ =
      diagonal (fun i => τ i ^ 2 * w i) := by
  calc
    _ = (normalizer V τ * V) * diagonal w * (normalizer V τ * V)ᵀ := by
      simp only [transpose_mul, Matrix.mul_assoc]
    _ = diagonal τ * diagonal w * diagonal τ := by
      rw [normalizer_mul_columns V hV τ, diagonal_transpose]
    _ = _ := by
      rw [diagonal_mul_diagonal, diagonal_mul_diagonal]
      congr 1
      funext i
      ring

omit [Fintype I] in
theorem weighted_column_sum (V : Matrix I J ℚ) (w : J → ℚ) :
    V * diagonal w * Vᵀ = ∑ j, w j • vecMulVec (V.col j) (V.col j) := by
  ext i k
  rw [Matrix.mul_apply]
  simp only [Matrix.sum_apply, Matrix.smul_apply, smul_eq_mul, vecMulVec_apply,
    Matrix.mul_diagonal, transpose_apply]
  apply Finset.sum_congr rfl
  intro j _
  simp only [Matrix.col_apply]
  ring

end DAGSpectral
