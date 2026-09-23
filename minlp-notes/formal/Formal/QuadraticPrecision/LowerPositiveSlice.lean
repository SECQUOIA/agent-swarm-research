import Formal.QuadraticPrecision.LowerNegativeSlice
import Formal.QuadraticPrecision.SpectralPositiveSlice
import Formal.QuadraticPrecision.OutputReflection

open scoped BigOperators Matrix
open Matrix MeasureTheory
namespace QuadraticPrecision

noncomputable def positiveFinEquiv {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}
    (hH : H.IsHermitian) : {j // 0 < hH.eigenvalues j} ≃ Fin (positiveInertia hH) :=
  Fintype.equivFin _

noncomputable def positiveFinLinear {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}
    (hH : H.IsHermitian) : Input (positiveInertia hH) →ₗ[ℝ] Input n :=
  (positiveEmbeddingLinear hH).comp
    ({ toFun := fun t j => t (positiveFinEquiv hH j)
       map_add' := by intros; rfl
       map_smul' := by intros; rfl } :
      Input (positiveInertia hH) →ₗ[ℝ] ({j // 0 < hH.eigenvalues j} → ℝ))

@[simp] theorem positiveFinLinear_apply {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}
    (hH : H.IsHermitian) (t : Input (positiveInertia hH)) :
    positiveFinLinear hH t = positiveEmbedding hH (fun j => t (positiveFinEquiv hH j)) := rfl

/-- An actual finite positive-inertia slice, its restricted quadratic, and a
strict curvature bound, all constructed from the original Hessian and box. -/
theorem exists_positive_quadratic_slice {n : ℕ}
    (H : Matrix (Fin n) (Fin n) ℝ) (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (hlu : ∀ i, l i < u i) :
    ∃ (ρ μ : ℝ) (A : Input (positiveInertia hH) →ᵃ[ℝ] Input n)
      (M : Matrix (Fin (positiveInertia hH)) (Fin (positiveInertia hH)) ℝ)
      (a' : Input (positiveInertia hH)) (b' : ℝ),
      0 < ρ ∧ 0 < μ ∧ Function.Injective A ∧
      (∀ t ∈ Set.Icc (fun _ => -ρ) (fun _ => ρ), A t ∈ Set.Icc l u) ∧
      (quadraticPolynomial H a b ∘ A = quadraticPolynomial M a' b') ∧
      (∀ t, μ * ∑ i, (t i)^2 ≤ t ⬝ᵥ M *ᵥ t) := by
  classical
  obtain ⟨ρ, hρ, hbox⟩ := positiveEmbedding_small_box hH l u hlu
  obtain ⟨μ, hμ, hcurv⟩ := positiveEmbedding_coercive hH
  let c : Input n := fun i => (l i+u i)/2
  let T := LinearMap.toMatrix' (positiveFinLinear hH)
  let A : Input (positiveInertia hH) →ᵃ[ℝ] Input n :=
    (positiveFinLinear hH).toAffineMap + AffineMap.const ℝ _ c
  have hA (t) : A t = c + T *ᵥ t := by
    simp [A, T, LinearMap.toMatrix'_mulVec, add_comm]
  refine ⟨ρ, μ, A, Tᵀ * H * T,
    (1/2:ℝ) • ((c ᵥ* H + H *ᵥ c) ᵥ* T) + a ᵥ* T,
    quadraticPolynomial H a b c, hρ, hμ, ?_, ?_, ?_, ?_⟩
  · intro s t h
    have he : positiveFinLinear hH s = positiveFinLinear hH t := by
      simpa [A] using h
    rw [positiveFinLinear_apply, positiveFinLinear_apply] at he
    have hn := positiveEmbedding_injective hH he
    funext i
    simpa using congrFun hn ((positiveFinEquiv hH).symm i)
  · intro t ht
    have hb := hbox (fun j => t (positiveFinEquiv hH j)) (fun j =>
      abs_le.mpr ⟨ht.1 _, ht.2 _⟩)
    constructor
    · intro i; simpa [hA, c, T, LinearMap.toMatrix'_mulVec] using (hb i).1
    · intro i; simpa [hA, c, T, LinearMap.toMatrix'_mulVec] using (hb i).2
  · funext t
    change quadraticPolynomial H a b (A t) = _
    rw [hA]
    exact quadraticPolynomial_affine H a c b T t
  · intro t
    have hc := hcurv (fun j => t (positiveFinEquiv hH j))
    have hs : (∑ j : {j // 0 < hH.eigenvalues j}, t (positiveFinEquiv hH j)^2) =
        ∑ i, t i^2 := Equiv.sum_comp (positiveFinEquiv hH) (fun i => t i ^ 2)
    rw [hs] at hc
    have ht : T *ᵥ t = positiveEmbedding hH (fun j => t (positiveFinEquiv hH j)) := by
      simp [T, LinearMap.toMatrix'_mulVec]
    rw [← ht] at hc
    rw [← mulVec_mulVec, ← mulVec_mulVec, dotProduct_transpose_mulVec]
    rw [dotProduct_comm (H *ᵥ (T *ᵥ t)) (T *ᵥ t)]
    linarith

/-- The positive-inertia logarithmic lower bound for the original quadratic
and original box. The additive constant is independent of tolerance and lift. -/
theorem hypograph_positive_inertia_lower {n : ℕ}
    (H : Matrix (Fin n) (Fin n) ℝ) (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (hlu : ∀ i, l i < u i) :
    ∃ c : ℝ, ∀ ε : ℝ, 0 < ε → ∀ p : ℕ,
      HasHypographLift (Set.Icc l u) (quadraticPolynomial H a b) ε p →
      (positiveInertia hH : ℝ) / 2 * Real.logb 2 (1 / ε) + c ≤ p := by
  obtain ⟨ρ, μ, A, M, a', b', hρ, hμ, _, hbox, hpoly, hcurv⟩ :=
    exists_positive_quadratic_slice H hH a l u b hlu
  let D : Set (Input (positiveInertia hH)) := Set.Icc (fun _ => -ρ) (fun _ => ρ)
  have hvol : 0 < (volume D).toReal := by
    rw [Real.volume_Icc_pi_toReal (by intro i; linarith :
      (fun _ : Fin (positiveInertia hH) => -ρ) ≤ fun _ => ρ)]
    exact Finset.prod_pos (fun _ _ => by linarith)
  refine ⟨Real.logb 2 (volume D).toReal -
    (positiveInertia hH : ℝ) / 2 * Real.logb 2 (8 / μ), ?_⟩
  intro ε hε p h
  have hpull := h.pullback A D (convex_Icc _ _) hbox
  rw [hpoly] at hpull
  have hn := hpull.neg
  have hpolyneg : (fun x => -quadraticPolynomial M a' b' x) =
      quadraticPolynomial (-M) (-a') (-b') := by
    funext x
    simp [quadraticPolynomial, contactQuadratic, Matrix.neg_mulVec, dotProduct_neg,
      neg_dotProduct]
    ring
  rw [hpolyneg] at hn
  apply epigraph_negative_log_bound isCompact_Icc hvol (-M) (-a') (-b') ε μ hμ hε _ hn
  intro t
  simpa only [Matrix.neg_mulVec, dotProduct_neg, neg_neg] using hcurv t

end QuadraticPrecision
