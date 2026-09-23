import Mathlib

/-!
# Exact-center block elimination

The products in this file are used only for linear equations, never for a
product norm. The norm identities use the real inner products of the two
summands. Invertibility of the lower block and Schur complement is explicit;
no central-path regularity or positive-definiteness theorem is assumed silently.
-/

namespace QipmFormal.Coupling

noncomputable section

variable {U K : Type*} [AddCommGroup U] [Module ℝ U]
  [AddCommGroup K] [Module ℝ K]

/-- The exact-center normal matrix in active/inactive coordinates. -/
def blockOperator (μ : ℝ) (C D : U →ₗ[ℝ] U) (F : U →ₗ[ℝ] K)
    (T : K →ₗ[ℝ] U) (E : K ≃ₗ[ℝ] K) : (U × K) →ₗ[ℝ] (U × K) where
  toFun z := (μ⁻¹ • C z.1 + μ • (D z.1 + T z.2), μ • (F z.1 + E z.2))
  map_add' x y := by ext <;> simp <;> module
  map_smul' a x := by ext <;> simp <;> module

variable (μ : ℝ) (C D : U →ₗ[ℝ] U) (F : U →ₗ[ℝ] K)
  (T : K →ₗ[ℝ] U) (E : K ≃ₗ[ℝ] K) (S : U ≃ₗ[ℝ] U)

/-- The Schur-complement identity specifying the invertible upper factor. -/
def HasSchurFactor : Prop :=
  ∀ u, S u = C u + μ ^ 2 • (D u - T (E.symm (F u)))

/-- Explicit elimination for an arbitrary right-hand side. -/
def blockSolve (z : U × K) : U × K :=
  let u := S.symm (μ • z.1 - μ • T (E.symm z.2))
  (u, E.symm (μ⁻¹ • z.2 - F u))

theorem blockOperator_solve (hμ : μ ≠ 0) (hS : HasSchurFactor μ C D F T E S)
    (z : U × K) :
    blockOperator μ C D F T E (blockSolve μ F T E S z) = z := by
  let u := S.symm (μ • z.1 - μ • T (E.symm z.2))
  have hu : C u + μ ^ 2 • (D u - T (E.symm (F u))) =
      μ • z.1 - μ • T (E.symm z.2) := by
    rw [← hS u]
    exact S.apply_symm_apply _
  have hu' := congrArg (fun x : U => μ⁻¹ • x) hu
  simp only [smul_sub, smul_add, smul_smul] at hu'
  have hm : μ⁻¹ * μ ^ 2 = μ := by field_simp
  simp only [hm, inv_mul_cancel₀ hμ, one_smul] at hu'
  apply Prod.ext
  · change μ⁻¹ • C u + μ • (D u + T (E.symm (μ⁻¹ • z.2 - F u))) = z.1
    simp only [map_sub, map_smul]
    have hm' : μ * μ⁻¹ = 1 := mul_inv_cancel₀ hμ
    simp only [smul_add, smul_sub, smul_smul, hm', one_smul]
    calc
      _ = (μ⁻¹ • C u + (μ • D u - μ • T (E.symm (F u)))) + T (E.symm z.2) := by abel
      _ = z.1 := by rw [hu']; abel
  · change μ • (F u + E (E.symm (μ⁻¹ • z.2 - F u))) = z.2
    rw [E.apply_symm_apply]
    simp [smul_smul, hμ]

theorem blockOperator_injective (hμ : μ ≠ 0)
    (hS : HasSchurFactor μ C D F T E S) :
    Function.Injective (blockOperator μ C D F T E) := by
  apply (blockOperator μ C D F T E).ker_eq_bot.mp
  apply LinearMap.ker_eq_bot'.mpr
  rintro ⟨u, v⟩ hz
  have hz₁ : μ⁻¹ • C u + μ • (D u + T v) = 0 := congrArg Prod.fst hz
  have hz₂ : μ • (F u + E v) = 0 := congrArg Prod.snd hz
  have hv : v = - E.symm (F u) := by
    have hh : F u + E v = 0 := (smul_eq_zero.mp hz₂).resolve_left hμ
    have hh' : E v = - F u := eq_neg_of_add_eq_zero_right hh
    have := congrArg E.symm hh'
    simpa using this
  have hu : u = 0 := by
    apply S.injective
    rw [map_zero, hS u]
    have hh := congrArg (fun x : U => μ • x) hz₁
    rw [hv] at hh
    simp only [map_neg, smul_add, smul_smul, mul_inv_cancel₀ hμ, one_smul,
      smul_zero] at hh
    convert hh using 1; module
  simp [hu, hv]

/-- Invertibility follows from elimination, not from an assumed inverse of H. -/
theorem blockOperator_bijective (hμ : μ ≠ 0)
    (hS : HasSchurFactor μ C D F T E S) :
    Function.Bijective (blockOperator μ C D F T E) :=
  ⟨blockOperator_injective μ C D F T E S hμ hS,
    fun z => ⟨blockSolve μ F T E S z, blockOperator_solve μ C D F T E S hμ hS z⟩⟩

/-- The genuine inverse equivalence supplied by the block proof. -/
def blockEquiv (hμ : μ ≠ 0) (hS : HasSchurFactor μ C D F T E S) :
    (U × K) ≃ₗ[ℝ] (U × K) :=
  LinearEquiv.ofBijective _ (blockOperator_bijective μ C D F T E S hμ hS)

/-- The inverse supplied by elimination agrees with the explicit solve. -/
theorem blockEquiv_symm_apply (hμ : μ ≠ 0)
    (hS : HasSchurFactor μ C D F T E S) (z : U × K) :
    (blockEquiv μ C D F T E S hμ hS).symm z = blockSolve μ F T E S z := by
  apply (blockEquiv μ C D F T E S hμ hS).injective
  rw [LinearEquiv.apply_symm_apply]
  exact (blockOperator_solve μ C D F T E S hμ hS z).symm

/-- The active component of the rescaled first inverse. -/
def couplingP (S : U ≃ₗ[ℝ] U) (b : U) : U := S.symm b

/-- The active-to-inactive coupling. -/
def couplingG (F : U →ₗ[ℝ] K) (E : K ≃ₗ[ℝ] K) (S : U ≃ₗ[ℝ] U)
    (b : U) : K := E.symm (F (couplingP S b))

/-- The active component of the rescaled second inverse. -/
def couplingQ (F : U →ₗ[ℝ] K) (T : K →ₗ[ℝ] U)
    (E : K ≃ₗ[ℝ] K) (S : U ≃ₗ[ℝ] U) (b : U) : U :=
  S.symm (couplingP S b + T (E.symm (couplingG F E S b)))

/-- Equation (coupling-first-inverse), for the actual inverse of the block map. -/
theorem first_inverse (hμ : μ ≠ 0) (hS : HasSchurFactor μ C D F T E S) (b : U) :
    (blockEquiv μ C D F T E S hμ hS).symm (b, 0) =
      (μ • couplingP S b, -μ • couplingG F E S b) := by
  rw [blockEquiv_symm_apply]
  simp [blockSolve, couplingP, couplingG]

/-- Equation (coupling-second-inverse), obtained by applying the same inverse twice. -/
theorem second_inverse (hμ : μ ≠ 0) (hS : HasSchurFactor μ C D F T E S) (b : U) :
    (blockEquiv μ C D F T E S hμ hS).symm
      ((blockEquiv μ C D F T E S hμ hS).symm (b, 0)) =
    (μ ^ 2 • couplingQ F T E S b,
      -E.symm (couplingG F E S b) - μ ^ 2 • E.symm (F (couplingQ F T E S b))) := by
  rw [first_inverse, blockEquiv_symm_apply]
  have hu : S.symm (μ • (μ • couplingP S b) -
      μ • T (E.symm (-μ • couplingG F E S b))) = μ ^ 2 • couplingQ F T E S b := by
    simp only [map_smul, map_sub, couplingQ, map_add, smul_add, smul_smul]
    module
  change (S.symm _, E.symm (μ⁻¹ • (-μ • couplingG F E S b) - F (S.symm _))) = _
  rw [hu]
  apply Prod.ext
  · rfl
  · simp [map_sub, smul_smul, hμ]

/-- Vanishing coupling is exactly membership in the image of the kernel of F. -/
theorem couplingG_eq_zero_iff (b : U) :
    couplingG F E S b = 0 ↔ ∃ p, F p = 0 ∧ S p = b := by
  constructor
  · intro h
    refine ⟨S.symm b, ?_, S.apply_symm_apply b⟩
    apply E.symm.injective
    simpa [couplingG, couplingP] using h
  · rintro ⟨p, hp, rfl⟩
    simp [couplingG, couplingP, hp]

/-- Every right-hand side decouples exactly when the off-diagonal block vanishes. -/
theorem couplingG_all_eq_zero_iff :
    (∀ b, couplingG F E S b = 0) ↔ F = 0 := by
  constructor
  · intro h
    ext p
    have hh := h (S p)
    simpa [couplingG, couplingP] using congrArg E hh
  · rintro rfl
    simp [couplingG]

end

section InnerProduct

variable {U K : Type*} [NormedAddCommGroup U] [InnerProductSpace ℝ U]
  [NormedAddCommGroup K] [InnerProductSpace ℝ K]
  (F : U →ₗ[ℝ] K) (T : K →ₗ[ℝ] U) (E : K ≃ₗ[ℝ] K)

/-- The limiting second-inverse numerator cannot cancel. All norms here are the
real inner-product norms, not a sup norm on block coordinates. -/
theorem coupling_inner_identity
    (hT : ∀ u v, inner ℝ u (T v) = inner ℝ (F u) v)
    (hE : ∀ x y, inner ℝ (E x) y = inner ℝ x (E y)) (p : U) :
    inner ℝ p (p + T (E.symm (E.symm (F p)))) =
      ‖p‖ ^ 2 + ‖E.symm (F p)‖ ^ 2 := by
  rw [inner_add_right, hT]
  have h : inner ℝ (F p) (E.symm (E.symm (F p))) =
      inner ℝ (E.symm (F p)) (E.symm (F p)) := by
    conv_lhs => arg 2; rw [← E.apply_symm_apply (F p)]
    rw [hE, E.apply_symm_apply]
  rw [h]
  simp only [real_inner_self_eq_norm_sq]

/-- Noncancellation needs self-adjointness of E and the adjoint relation T=F*. -/
theorem coupling_numerator_ne_zero
    (hT : ∀ u v, inner ℝ u (T v) = inner ℝ (F u) v)
    (hE : ∀ x y, inner ℝ (E x) y = inner ℝ x (E y))
    {p : U} (hp : p ≠ 0) : p + T (E.symm (E.symm (F p))) ≠ 0 := by
  intro hz
  have hi := coupling_inner_identity F T E hT hE p
  rw [hz, inner_zero_right] at hi
  have hpos : 0 < ‖p‖ ^ 2 := sq_pos_of_pos (norm_pos_iff.mpr hp)
  nlinarith [sq_nonneg ‖E.symm (F p)‖]

/-- In particular the limiting q is nonzero for every nonzero right-hand side. -/
theorem couplingQ_ne_zero (S : U ≃ₗ[ℝ] U)
    (hT : ∀ u v, inner ℝ u (T v) = inner ℝ (F u) v)
    (hE : ∀ x y, inner ℝ (E x) y = inner ℝ x (E y))
    {b : U} (hb : b ≠ 0) : couplingQ F T E S b ≠ 0 := by
  have hp : couplingP S b ≠ 0 := by simpa [couplingP] using hb
  have hn := coupling_numerator_ne_zero F T E hT hE hp
  intro hz
  apply hn
  have hh := congrArg S hz
  simpa only [couplingQ, couplingG, S.apply_symm_apply, map_zero] using hh

end InnerProduct
end QipmFormal.Coupling
