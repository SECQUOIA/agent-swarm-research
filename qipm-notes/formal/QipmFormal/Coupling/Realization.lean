import QipmFormal.Coupling.Paper
import QipmFormal.Coupling.Positivity
import Mathlib.Analysis.InnerProductSpace.ProdL2

/-!
# Orthogonal coordinates for the actual normal operator

The block system is obtained from a fixed subspace of the original inner-product
space. Its coordinate norm is exactly the original norm, and its off-diagonal
blocks satisfy the adjoint relation needed for noncancellation.
-/
namespace QipmFormal.Coupling
noncomputable section

variable {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
  [FiniteDimensional ℝ V]

namespace OrthogonalRealization

variable (U : Submodule ℝ V)

/-- Ordinary pair coordinates, with their norm specified separately by blockNorm. -/
def coordinates : V ≃ₗ[ℝ] (U × Uᗮ) :=
  U.orthogonalDecomposition.toLinearEquiv.trans (WithLp.linearEquiv 2 ℝ (U × Uᗮ))

@[simp] theorem coordinates_apply (x : V) :
    coordinates U x = (U.orthogonalProjectionOnto x, Uᗮ.orthogonalProjectionOnto x) := by
  simp [coordinates]

@[simp] theorem coordinates_symm_apply (z : U × Uᗮ) :
    (coordinates U).symm z = (z.1 : V) + z.2 := by
  rfl

/-- The coordinate convention used in all filtering estimates is an isometry. -/
theorem coordinates_norm (x : V) :
    blockNorm (coordinates U x).1 (coordinates U x).2 = ‖x‖ := by
  have hn := U.orthogonalDecomposition.norm_map x
  have hs := WithLp.prod_norm_sq_eq_of_L2 (U.orthogonalDecomposition x)
  apply (sq_eq_sq₀ (blockNorm_nonneg _ _) (norm_nonneg x)).mp
  rw [blockNorm_sq]
  rw [hn] at hs
  simpa [coordinates] using hs.symm

/-- Inner products also split exactly across the orthogonal summands. -/
theorem coordinates_inner (x y : V) :
    inner ℝ (coordinates U x).1 (coordinates U y).1 +
      inner ℝ (coordinates U x).2 (coordinates U y).2 = inner ℝ x y := by
  have hi := U.orthogonalDecomposition.inner_map_map x y
  simpa [WithLp.prod_inner_apply, coordinates] using hi

/-- Restriction followed by projection onto an indicated subspace. -/
def block (A B : Submodule ℝ V) (L : V →ₗ[ℝ] V) : A →ₗ[ℝ] B :=
  B.orthogonalProjectionOnto.toLinearMap.comp (L.comp A.subtype)

@[simp] theorem block_apply (A B : Submodule ℝ V) (L : V →ₗ[ℝ] V) (x : A) :
    block A B L x = B.orthogonalProjectionOnto (L x) := rfl

/-- The two off-diagonal blocks of a self-adjoint operator are adjoints. -/
theorem offDiagonal_adjoint (D : V →ₗ[ℝ] V)
    (hD : ∀ x y, inner ℝ x (D y) = inner ℝ (D x) y) (u : U) (v : Uᗮ) :
    inner ℝ u (block Uᗮ U D v) = inner ℝ (block U Uᗮ D u) v := by
  simpa using hD (u : V) (v : V)

/-- In particular, the inactive diagonal block is self-adjoint. -/
theorem inactive_selfAdjoint (D : V →ₗ[ℝ] V)
    (hD : ∀ x y, inner ℝ x (D y) = inner ℝ (D x) y) (x y : Uᗮ) :
    inner ℝ (block Uᗮ Uᗮ D x) y = inner ℝ x (block Uᗮ Uᗮ D y) := by
  simpa using (hD (x : V) (y : V)).symm

/-- Positive semidefiniteness passes to each diagonal restriction. -/
theorem diagonal_nonnegative (A : Submodule ℝ V) (D : V →ₗ[ℝ] V)
    (hD : ∀ x, 0 ≤ inner ℝ x (D x)) (x : A) :
    0 ≤ inner ℝ x (block A A D x) := by
  simpa using hD (x : V)

/-- The actual operator whose inverse is represented by the block equations. -/
def normalOperator (μ : ℝ) (C D : V →ₗ[ℝ] V) : V →ₗ[ℝ] V := μ⁻¹ • C + μ • D

/-- A supported leading term has no inactive coordinate. -/
lemma supported_coordinates (C : V →ₗ[ℝ] V)
    (hrange : ∀ x, C x ∈ U) (hzero : ∀ v : Uᗮ, C v = 0) (z : U × Uᗮ) :
    coordinates U (C ((coordinates U).symm z)) = (block U U C z.1, 0) := by
  rw [coordinates_symm_apply, map_add, hzero, add_zero, coordinates_apply]
  apply Prod.ext
  · rfl
  · exact Uᗮ.orthogonalProjectionOnto_eq_zero_iff.mpr
      (by simpa using hrange (z.1 : V))

/-- The finite-dimensional normal operator gives exactly the paper's blocks. -/
theorem normalOperator_coordinates (μ : ℝ) (C D : V →ₗ[ℝ] V)
    (hrange : ∀ x, C x ∈ U) (hzero : ∀ v : Uᗮ, C v = 0)
    (E : Uᗮ ≃ₗ[ℝ] Uᗮ) (hE : E.toLinearMap = block Uᗮ Uᗮ D)
    (z : U × Uᗮ) :
    coordinates U (normalOperator μ C D ((coordinates U).symm z)) =
      blockOperator μ (block U U C) (block U U D) (block U Uᗮ D)
        (block Uᗮ U D) E z := by
  have hc := supported_coordinates U C hrange hzero z
  have he : E z.2 = block Uᗮ Uᗮ D z.2 := congrArg (fun L : Uᗮ →ₗ[ℝ] Uᗮ => L z.2) hE
  simp only [normalOperator, LinearMap.add_apply, LinearMap.smul_apply, map_add,
    map_smul, hc]
  simp only [coordinates_symm_apply, coordinates_apply, map_add, blockOperator,
    LinearMap.coe_mk, AddHom.coe_mk, Prod.smul_mk, Prod.mk_add_mk, he, block_apply]
  simp

/-- Transport an actual inverse operator through the canonical coordinates. -/
def coordinateEquiv (H : V ≃ₗ[ℝ] V) : (U × Uᗮ) ≃ₗ[ℝ] (U × Uᗮ) :=
  (coordinates U).symm.trans (H.trans (coordinates U))

@[simp] theorem coordinateEquiv_apply (H : V ≃ₗ[ℝ] V) (z : U × Uᗮ) :
    coordinateEquiv U H z = coordinates U (H ((coordinates U).symm z)) := rfl

@[simp] theorem coordinateEquiv_symm_apply (H : V ≃ₗ[ℝ] V) (x : V) :
    (coordinateEquiv U H).symm (coordinates U x) = coordinates U (H.symm x) := by
  simp [coordinateEquiv]

/-- The actual first inverse has exactly the block inverse norm. -/
theorem inverse_norm (H : V ≃ₗ[ℝ] V) (x : V) :
    blockNorm ((coordinateEquiv U H).symm (coordinates U x)).1
      ((coordinateEquiv U H).symm (coordinates U x)).2 = ‖H.symm x‖ := by
  rw [coordinateEquiv_symm_apply, coordinates_norm]

/-- The norm identity also holds for the actual second inverse. -/
theorem second_inverse_norm (H : V ≃ₗ[ℝ] V) (x : V) :
    blockNorm ((coordinateEquiv U H).symm ((coordinateEquiv U H).symm
      (coordinates U x))).1
      ((coordinateEquiv U H).symm ((coordinateEquiv U H).symm
        (coordinates U x))).2 = ‖H.symm (H.symm x)‖ := by
  rw [coordinateEquiv_symm_apply, coordinateEquiv_symm_apply, coordinates_norm]

/-- Data for the block theorem constructed from the original operators. -/
def realizeFamily (C D : ℝ → V →ₗ[ℝ] V) (E : ℝ → Uᗮ ≃ₗ[ℝ] Uᗮ)
    (S : ℝ → U ≃ₗ[ℝ] U) (H : ℝ → V ≃ₗ[ℝ] V) : BlockFamily U Uᗮ where
  C μ := block U U (C μ)
  D μ := block U U (D μ)
  F μ := block U Uᗮ (D μ)
  T μ := block Uᗮ U (D μ)
  E := E
  S := S
  H μ := coordinateEquiv U (H μ)

/-- The hypotheses on original operators imply the exact model predicate. -/
theorem realizeFamily_valid (C D : ℝ → V →ₗ[ℝ] V)
    (E : ℝ → Uᗮ ≃ₗ[ℝ] Uᗮ) (S : ℝ → U ≃ₗ[ℝ] U) (H : ℝ → V ≃ₗ[ℝ] V)
    (μ : ℝ) (hμ : μ ≠ 0) (hrange : ∀ x, C μ x ∈ U)
    (hzero : ∀ v : Uᗮ, C μ v = 0)
    (hE : (E μ).toLinearMap = block Uᗮ Uᗮ (D μ))
    (hS : HasSchurFactor μ (block U U (C μ)) (block U U (D μ))
      (block U Uᗮ (D μ)) (block Uᗮ U (D μ)) (E μ) (S μ))
    (hH : ∀ x, H μ x = normalOperator μ (C μ) (D μ) x) :
    (realizeFamily U C D E S H).ValidAt μ := by
  refine ⟨hμ, hS, ?_⟩
  intro z
  change coordinates U (H μ ((coordinates U).symm z)) = _
  rw [hH]
  exact normalOperator_coordinates U μ (C μ) (D μ) hrange hzero (E μ) hE z

/-- An active right-hand side is exactly `(b,0)` in the canonical coordinates. -/
theorem coordinates_active (b : U) : coordinates U (b : V) = (b, 0) := by
  apply (coordinates U).symm.injective
  rw [LinearEquiv.symm_apply_apply, coordinates_symm_apply]
  simp

/-- The family interface computes the original-space first inverse norm. -/
theorem realized_firstInverseNorm (C D : ℝ → V →ₗ[ℝ] V)
    (E : ℝ → Uᗮ ≃ₗ[ℝ] Uᗮ) (S : ℝ → U ≃ₗ[ℝ] U) (H : ℝ → V ≃ₗ[ℝ] V)
    (b : U) (μ : ℝ) :
    (realizeFamily U C D E S H).firstInverseNorm b μ = ‖(H μ).symm (b : V)‖ := by
  have hn := inverse_norm U (H μ) (b : V)
  rw [coordinates_active] at hn
  exact hn

/-- The family interface computes the original-space second inverse norm. -/
theorem realized_secondInverseNorm (C D : ℝ → V →ₗ[ℝ] V)
    (E : ℝ → Uᗮ ≃ₗ[ℝ] Uᗮ) (S : ℝ → U ≃ₗ[ℝ] U) (H : ℝ → V ≃ₗ[ℝ] V)
    (b : U) (μ : ℝ) :
    (realizeFamily U C D E S H).secondInverseNorm b μ =
      ‖(H μ).symm ((H μ).symm (b : V))‖ := by
  have hn := second_inverse_norm U (H μ) (b : V)
  rw [coordinates_active] at hn
  exact hn

/-- Positivity of an original operator passes to its orthogonal block form. -/
theorem normal_positive_blocks (μ : ℝ) (C D : V →ₗ[ℝ] V)
    (hrange : ∀ x, C x ∈ U) (hzero : ∀ v : Uᗮ, C v = 0)
    (hpos : ∀ x, x ≠ 0 → 0 < inner ℝ x (normalOperator μ C D x)) :
    ∀ u v, u ≠ 0 ∨ v ≠ 0 →
      0 < blockQuadratic μ (block U U C) (block U U D) (block U Uᗮ D)
        (block Uᗮ U D) (block Uᗮ Uᗮ D) u v := by
  intro u v huv
  let x := (coordinates U).symm (u, v)
  have hx : x ≠ 0 := by
    intro hz
    have hh := congrArg (coordinates U) hz
    have hh' : (u, v) = (0 : U × Uᗮ) := by
      simpa only [x, LinearEquiv.apply_symm_apply, map_zero] using hh
    rcases huv with hu | hv
    · exact hu (by simpa using congrArg Prod.fst hh')
    · exact hv (by simpa using congrArg Prod.snd hh')
  have hp := hpos x hx
  have hi := coordinates_inner U x (normalOperator μ C D x)
  have hc := supported_coordinates U C hrange hzero (u, v)
  have hd : coordinates U (normalOperator μ C D x) =
      (μ⁻¹ • block U U C u + μ • (block U U D u + block Uᗮ U D v),
        μ • (block U Uᗮ D u + block Uᗮ Uᗮ D v)) := by
    simp only [normalOperator, LinearMap.add_apply, LinearMap.smul_apply, map_add, map_smul]
    change μ⁻¹ • coordinates U (C ((coordinates U).symm (u, v))) +
      μ • coordinates U (D ((coordinates U).symm (u, v))) = _
    rw [hc]
    simp [block_apply]
  rw [hd] at hi
  have hcoord : coordinates U x = (u, v) := (coordinates U).apply_symm_apply _
  rw [hcoord] at hi
  rw [← hi] at hp
  exact hp

omit [FiniteDimensional ℝ V] in
/-- Symmetry and range support already imply vanishing on the orthogonal complement. -/
theorem vanishes_orthogonal_of_range (C : V →ₗ[ℝ] V)
    (hC : ∀ x y, inner ℝ x (C y) = inner ℝ (C x) y)
    (hrange : ∀ x, C x ∈ U) (v : Uᗮ) : C v = 0 := by
  apply (inner_self_eq_zero (𝕜 := ℝ)).mp
  rw [hC]
  exact U.inner_right_of_mem_orthogonal (hrange _) v.property

/-- Positivity of the original normal matrix supplies both invertible factors. -/
theorem normal_positive_factors (μ : ℝ) (C D : V →ₗ[ℝ] V)
    (hμ : 0 < μ) (hrange : ∀ x, C x ∈ U) (hzero : ∀ v : Uᗮ, C v = 0)
    (hpos : ∀ x, x ≠ 0 → 0 < inner ℝ x (normalOperator μ C D x)) :
    ∃ (E : Uᗮ ≃ₗ[ℝ] Uᗮ) (S : U ≃ₗ[ℝ] U),
      E.toLinearMap = block Uᗮ Uᗮ D ∧
      HasSchurFactor μ (block U U C) (block U U D) (block U Uᗮ D)
        (block Uᗮ U D) E S :=
  positive_blocks_have_factors μ _ _ _ _ _ hμ
    (normal_positive_blocks U μ C D hrange hzero hpos)

/-- The realized ξ is precisely the parameter computed in the original space. -/
theorem realized_xi (C D : ℝ → V →ₗ[ℝ] V)
    (E : ℝ → Uᗮ ≃ₗ[ℝ] Uᗮ) (S : ℝ → U ≃ₗ[ℝ] U) (H : ℝ → V ≃ₗ[ℝ] V)
    (α : ℝ → ℝ) (b : U) (μ : ℝ) :
    (realizeFamily U C D E S H).xi α b μ = α μ * ‖(H μ).symm (b : V)‖ / ‖(b : V)‖ := by
  rw [BlockFamily.xi, realized_firstInverseNorm]
  rfl

/-- The realized ρ is precisely the parameter computed in the original space. -/
theorem realized_rho (C D : ℝ → V →ₗ[ℝ] V)
    (E : ℝ → Uᗮ ≃ₗ[ℝ] Uᗮ) (S : ℝ → U ≃ₗ[ℝ] U) (H : ℝ → V ≃ₗ[ℝ] V)
    (α : ℝ → ℝ) (b : U) (μ : ℝ) :
    (realizeFamily U C D E S H).rho α b μ =
      α μ * ‖(H μ).symm ((H μ).symm (b : V))‖ / ‖(H μ).symm (b : V)‖ := by
  rw [BlockFamily.rho, realized_firstInverseNorm, realized_secondInverseNorm]

end OrthogonalRealization
end
end QipmFormal.Coupling
