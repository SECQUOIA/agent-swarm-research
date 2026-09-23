import QipmFormal.Mixture.Residual
import QipmFormal.Mixture.Decoder
import QipmFormal.Mixture.Incidence

/-! # Residual soundness forces an incidence resource cost -/

namespace QipmFormal.Mixture
noncomputable section
open scoped BigOperators

variable {I R C : Type*} [Fintype I] [Fintype R] [Fintype C]

/-- A public affine decoder is sound throughout the stated relative residual tube.
The objective and nonnegativity are part of the contract. -/
def AffineSound (A : R → C → ℝ) (b : R → ℝ) (c a : C → ℝ)
    (v a₀ p η : ℝ) : Prop :=
  ∀ z : C → ℝ, (∀ j, 0 ≤ z j) → dot c z = v →
    euclideanNorm (residual A z b) ≤ η * euclideanNorm b →
    0 ≤ p * (dot a z - a₀)

theorem weighted_affine_soundness_frontier [DecidableEq I]
    (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (x : I → C → ℝ) (b : R → ℝ) (w : I → ℝ)
    (D : R → Finset C) (label : R → C → I) (s : ℕ) (B H : ℝ)
    (c a : C → ℝ) (v a₀ p γ η : ℝ)
    (hw : ProbWeights w) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j)
    (hxpos : ∀ i j, 0 ≤ x i j) (hobj : ∀ i, dot c (x i) = v)
    (hmargin : ∀ i, γ ≤ -p * (dot a (x i) - a₀))
    (hγ : 0 < γ) (hη : 0 ≤ η) (hsound : AffineSound A b c a v a₀ p η) :
    η ^ 2 * sqNorm b <
      4 * s * B ^ 2 * H ^ 2 * ∑ i, (incidence D label i : ℝ) * (w i) ^ 2 := by
  have hr := weighted_residual_bound A A' x b w D label s B H hw hB hH
    hA hA' hx hs hfeas hlocal
  by_contra! hcost
  have ht : euclideanNorm (residual A (mix w x) b) ≤ η * euclideanNorm b := by
    have hsq : euclideanNorm (residual A (mix w x) b) ^ 2 ≤
        (η * euclideanNorm b) ^ 2 := by
      rw [mul_pow, euclideanNorm_sq, euclideanNorm_sq]
      exact hr.trans hcost
    exact (sq_le_sq₀ (Real.sqrt_nonneg _) (mul_nonneg hη (Real.sqrt_nonneg _))).mp hsq
  have hgood := hsound (mix w x) (mix_nonneg hw hxpos) (mix_objective hw hobj) ht
  have hbad := mix_signed_margin hw hmargin
  nlinarith

/-- Algebraic rearrangement for the uniform and sensitive-subset frontiers.
Only this divided form needs strictly positive row sparsity. -/
theorem uniform_resource_product {M B H η b₂ N s : ℝ}
    (hN : 0 < N) (hs : 0 < s)
    (hcost : η ^ 2 * b₂ < 4 * s * B ^ 2 * H ^ 2 * (M / N ^ 2)) :
    η ^ 2 * b₂ / (4 * s) * N ^ 2 < M * B ^ 2 * H ^ 2 := by
  have hN2 : 0 < N ^ 2 := sq_pos_of_pos hN
  have h4s : 0 < 4 * s := by positivity
  have hc : η ^ 2 * b₂ * N ^ 2 < 4 * s * B ^ 2 * H ^ 2 * M := by
    apply (lt_div_iff₀ hN2).mp
    simpa only [mul_div_assoc] using hcost
  calc
    η ^ 2 * b₂ / (4 * s) * N ^ 2 = (η ^ 2 * b₂ * N ^ 2) / (4 * s) := by ring
    _ < M * B ^ 2 * H ^ 2 := (div_lt_iff₀ h4s).mpr (by nlinarith [hc])

theorem harmonic_resource_product {M : I → ℝ} [Nonempty I]
    (hM : ∀ i, 0 < M i) {B H η b₂ s : ℝ} (hs : 0 < s)
    (hcost : η ^ 2 * b₂ < 4 * s * B ^ 2 * H ^ 2 * (reciprocalMass M)⁻¹) :
    η ^ 2 * b₂ / (4 * s) * reciprocalMass M < B ^ 2 * H ^ 2 := by
  have hS := reciprocalMass_pos hM
  have h4s : 0 < 4 * s := by positivity
  have hc : η ^ 2 * b₂ * reciprocalMass M < 4 * s * B ^ 2 * H ^ 2 := by
    apply (lt_div_iff₀ hS).mp
    simpa only [div_eq_mul_inv] using hcost
  calc
    η ^ 2 * b₂ / (4 * s) * reciprocalMass M =
        (η ^ 2 * b₂ * reciprocalMass M) / (4 * s) := by ring
    _ < B ^ 2 * H ^ 2 := (div_lt_iff₀ h4s).mpr (by nlinarith [hc])

omit [Fintype C] in
theorem sum_incidence_eq_total [DecidableEq I]
    (D : R → Finset C) (label : R → C → I) :
    (∑ i, (incidence D label i : ℝ)) = totalIncidence D := by
  have h := incidence_sum D label (fun _ => (1 : ℝ))
  simpa [totalIncidence, Nat.cast_sum] using h.symm

/-- The harmonic-incidence residual estimate, derived from the actual local matrices. -/
theorem harmonic_residual_bound [DecidableEq I] [Nonempty I]
    (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (x : I → C → ℝ) (b : R → ℝ)
    (D : R → Finset C) (label : R → C → I) (s : ℕ) (B H : ℝ)
    (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j)
    (hM : ∀ i, 0 < (incidence D label i : ℝ)) :
    euclideanNorm (residual A
      (mix (harmonicWeight (fun i => (incidence D label i : ℝ))) x) b) ≤
      2 * B * H * Real.sqrt ((s : ℝ) / reciprocalMass (fun i => (incidence D label i : ℝ))) := by
  have hh := weighted_residual_bound A A' x b
    (harmonicWeight (fun i => (incidence D label i : ℝ))) D label s B H
    (harmonicWeight_prob hM) hB hH hA hA' hx hs hfeas hlocal
  rw [harmonicWeight_cost hM] at hh
  apply euclideanNorm_le_of_sqNorm_le _ _ (by positivity)
  calc
    _ ≤ _ := hh
    _ = _ := by
      rw [mul_pow, mul_pow, mul_pow,
        Real.sq_sqrt (div_nonneg (Nat.cast_nonneg _) (reciprocalMass_pos hM).le)]
      ring

/-- Uniform affine soundness gives the manuscript's strict product frontier. -/
theorem uniform_affine_soundness_product [Nonempty I]
    (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (x : I → C → ℝ) (b : R → ℝ)
    (D : R → Finset C) (label : R → C → I) (s : ℕ) (B H : ℝ)
    (c a : C → ℝ) (v a₀ p γ η : ℝ)
    (hB : 0 ≤ B) (hH : 0 ≤ H) (hspos : 0 < s)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j)
    (hxpos : ∀ i j, 0 ≤ x i j) (hobj : ∀ i, dot c (x i) = v)
    (hmargin : ∀ i, γ ≤ -p * (dot a (x i) - a₀))
    (hγ : 0 < γ) (hη : 0 ≤ η) (hsound : AffineSound A b c a v a₀ p η) :
    η ^ 2 * sqNorm b / (4 * s) * (Fintype.card I : ℝ) ^ 2 <
      (totalIncidence D : ℝ) * B ^ 2 * H ^ 2 := by
  classical
  have h := weighted_affine_soundness_frontier A A' x b (uniformWeight I)
    D label s B H c a v a₀ p γ η (uniformWeight_prob I) hB hH hA hA' hx hs
    hfeas hlocal hxpos hobj hmargin hγ hη hsound
  rw [uniform_incidence_cost, sum_incidence_eq_total] at h
  exact uniform_resource_product (Nat.cast_pos.mpr Fintype.card_pos)
    (Nat.cast_pos.mpr hspos) h

/-- The optimized strict frontier includes the actual harmonic mixture and soundness. -/
theorem harmonic_affine_soundness_product [DecidableEq I] [Nonempty I]
    (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (x : I → C → ℝ) (b : R → ℝ)
    (D : R → Finset C) (label : R → C → I) (s : ℕ) (B H : ℝ)
    (c a : C → ℝ) (v a₀ p γ η : ℝ)
    (hB : 0 ≤ B) (hH : 0 ≤ H) (hspos : 0 < s)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j)
    (hxpos : ∀ i j, 0 ≤ x i j) (hobj : ∀ i, dot c (x i) = v)
    (hmargin : ∀ i, γ ≤ -p * (dot a (x i) - a₀))
    (hγ : 0 < γ) (hη : 0 ≤ η) (hsound : AffineSound A b c a v a₀ p η)
    (hM : ∀ i, 0 < (incidence D label i : ℝ)) :
    η ^ 2 * sqNorm b / (4 * s) * reciprocalMass (fun i => (incidence D label i : ℝ)) <
      B ^ 2 * H ^ 2 := by
  have h := weighted_affine_soundness_frontier A A' x b
    (harmonicWeight (fun i => (incidence D label i : ℝ)))
    D label s B H c a v a₀ p γ η (harmonicWeight_prob hM) hB hH hA hA' hx hs
    hfeas hlocal hxpos hobj hmargin hγ hη hsound
  rw [harmonicWeight_cost hM] at h
  exact harmonic_resource_product hM (Nat.cast_pos.mpr hspos) h

end
end QipmFormal.Mixture
