import Formal.QuadraticPrecision.SpectralSlice
import Formal.QuadraticPrecision.LowerCurvature

open scoped BigOperators Matrix
open Matrix MeasureTheory
namespace QuadraticPrecision

/-- The actual coefficients after a translated linear restriction. -/
theorem quadraticPolynomial_affine {n d : ℕ} (H : Matrix (Fin n) (Fin n) ℝ)
    (a c : Input n) (b : ℝ) (T : Matrix (Fin n) (Fin d) ℝ) (x : Input d) :
    quadraticPolynomial H a b (c + T *ᵥ x) =
      quadraticPolynomial (Tᵀ * H * T)
        ((1/2:ℝ) • ((c ᵥ* H + H *ᵥ c) ᵥ* T) + a ᵥ* T)
        (quadraticPolynomial H a b c) x := by
  simp only [quadraticPolynomial, contactQuadratic, mulVec_add, add_dotProduct,
    dotProduct_add, smul_dotProduct, ← mulVec_mulVec]
  rw [dotProduct_transpose_mulVec]
  simp only [add_vecMul, add_dotProduct, ← dotProduct_mulVec]
  rw [dotProduct_comm (H *ᵥ c) (T *ᵥ x),
    dotProduct_comm (H *ᵥ (T *ᵥ x)) (T *ᵥ x)]
  ring

noncomputable def negativeFinEquiv {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}
    (hH : H.IsHermitian) : {j // hH.eigenvalues j < 0} ≃ Fin (negativeInertia hH) :=
  Fintype.equivFin _

noncomputable def negativeFinLinear {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}
    (hH : H.IsHermitian) : Input (negativeInertia hH) →ₗ[ℝ] Input n :=
  (negativeEmbeddingLinear hH).comp
    ({ toFun := fun t j => t (negativeFinEquiv hH j)
       map_add' := by intros; rfl
       map_smul' := by intros; rfl } :
      Input (negativeInertia hH) →ₗ[ℝ] ({j // hH.eigenvalues j < 0} → ℝ))

@[simp] theorem negativeFinLinear_apply {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}
    (hH : H.IsHermitian) (t : Input (negativeInertia hH)) :
    negativeFinLinear hH t = negativeEmbedding hH (fun j => t (negativeFinEquiv hH j)) := rfl

/-- An actual finite negative-inertia slice, its restricted quadratic, and a
strict curvature bound, all constructed from the original Hessian and box. -/
theorem exists_negative_quadratic_slice {n : ℕ}
    (H : Matrix (Fin n) (Fin n) ℝ) (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (hlu : ∀ i, l i < u i) :
    ∃ (ρ μ : ℝ) (A : Input (negativeInertia hH) →ᵃ[ℝ] Input n)
      (M : Matrix (Fin (negativeInertia hH)) (Fin (negativeInertia hH)) ℝ)
      (a' : Input (negativeInertia hH)) (b' : ℝ),
      0 < ρ ∧ 0 < μ ∧ Function.Injective A ∧
      (∀ t ∈ Set.Icc (fun _ => -ρ) (fun _ => ρ), A t ∈ Set.Icc l u) ∧
      (quadraticPolynomial H a b ∘ A = quadraticPolynomial M a' b') ∧
      (∀ t, μ * ∑ i, (t i)^2 ≤ -(t ⬝ᵥ M *ᵥ t)) := by
  classical
  obtain ⟨ρ, hρ, hbox⟩ := negativeEmbedding_small_box hH l u hlu
  obtain ⟨μ, hμ, hcurv⟩ := negativeEmbedding_coercive hH
  let c : Input n := fun i => (l i+u i)/2
  let T := LinearMap.toMatrix' (negativeFinLinear hH)
  let A : Input (negativeInertia hH) →ᵃ[ℝ] Input n :=
    (negativeFinLinear hH).toAffineMap + AffineMap.const ℝ _ c
  have hA (t) : A t = c + T *ᵥ t := by
    simp [A, T, LinearMap.toMatrix'_mulVec, add_comm]
  refine ⟨ρ, μ, A, Tᵀ * H * T,
    (1/2:ℝ) • ((c ᵥ* H + H *ᵥ c) ᵥ* T) + a ᵥ* T,
    quadraticPolynomial H a b c, hρ, hμ, ?_, ?_, ?_, ?_⟩
  · intro s t h
    have he : negativeFinLinear hH s = negativeFinLinear hH t := by
      simpa [A] using h
    rw [negativeFinLinear_apply, negativeFinLinear_apply] at he
    have hn := negativeEmbedding_injective hH he
    funext i
    simpa using congrFun hn ((negativeFinEquiv hH).symm i)
  · intro t ht
    have hb := hbox (fun j => t (negativeFinEquiv hH j)) (fun j =>
      abs_le.mpr ⟨ht.1 _, ht.2 _⟩)
    constructor
    · intro i; simpa [hA, c, T, LinearMap.toMatrix'_mulVec] using (hb i).1
    · intro i; simpa [hA, c, T, LinearMap.toMatrix'_mulVec] using (hb i).2
  · funext t
    change quadraticPolynomial H a b (A t) = _
    rw [hA]
    exact quadraticPolynomial_affine H a c b T t
  · intro t
    have hc := hcurv (fun j => t (negativeFinEquiv hH j))
    have hs : (∑ j : {j // hH.eigenvalues j < 0}, t (negativeFinEquiv hH j)^2) =
        ∑ i, t i^2 := Equiv.sum_comp (negativeFinEquiv hH) (fun i => t i ^ 2)
    rw [hs] at hc
    have ht : T *ᵥ t = negativeEmbedding hH (fun j => t (negativeFinEquiv hH j)) := by
      simp [T, LinearMap.toMatrix'_mulVec]
    rw [← ht] at hc
    rw [← mulVec_mulVec, ← mulVec_mulVec, dotProduct_transpose_mulVec]
    rw [dotProduct_comm (H *ᵥ (T *ᵥ t)) (T *ᵥ t)]
    linarith

/-- The negative-inertia logarithmic lower bound for the original quadratic
and original box. The additive constant is independent of tolerance and lift. -/
theorem epigraph_negative_inertia_lower {n : ℕ}
    (H : Matrix (Fin n) (Fin n) ℝ) (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (hlu : ∀ i, l i < u i) :
    ∃ c : ℝ, ∀ ε : ℝ, 0 < ε → ∀ p : ℕ,
      HasEpigraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε p →
      (negativeInertia hH : ℝ) / 2 * Real.logb 2 (1 / ε) + c ≤ p := by
  obtain ⟨ρ, μ, A, M, a', b', hρ, hμ, _, hbox, hpoly, hcurv⟩ :=
    exists_negative_quadratic_slice H hH a l u b hlu
  let D : Set (Input (negativeInertia hH)) := Set.Icc (fun _ => -ρ) (fun _ => ρ)
  have hvol : 0 < (volume D).toReal := by
    rw [Real.volume_Icc_pi_toReal (by intro i; linarith :
      (fun _ : Fin (negativeInertia hH) => -ρ) ≤ fun _ => ρ)]
    exact Finset.prod_pos (fun _ _ => by linarith)
  refine ⟨Real.logb 2 (volume D).toReal -
    (negativeInertia hH : ℝ) / 2 * Real.logb 2 (8 / μ), ?_⟩
  intro ε hε p h
  have hpull := h.pullback A D (convex_Icc _ _) hbox
  rw [hpoly] at hpull
  exact epigraph_negative_log_bound isCompact_Icc hvol M a' b' ε μ hμ hε hcurv hpull

end QuadraticPrecision
