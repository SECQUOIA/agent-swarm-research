import QipmFormal.Mixture.Residual
import QipmFormal.Mixture.Decoder

/-! # Pair-decoder soundness forces incidence cost

The contract concerns the actual normalized squared-amplitude observable.
The mixture's nonzero norm is derived from strictly positive pair margins.
-/
namespace QipmFormal.Mixture
noncomputable section
open scoped BigOperators

variable {I R C P : Type*} [Fintype I] [Fintype R] [Fintype C] [Fintype P]

/-- Correct signed expectation on all nonzero, objective-exact points in the tube. -/
def PairSound (A : R → C → ℝ) (b : R → ℝ) (c : C → ℝ)
    (e : P × Bool ↪ C) (v p η : ℝ) : Prop :=
  ∀ z : C → ℝ, (∀ j, 0 ≤ z j) → dot c z = v → 0 < sqNorm z →
    euclideanNorm (residual A z b) ≤ η * euclideanNorm b →
    0 ≤ p * pairExpectation e z

/-- Every probability weighting of wrong-margin neighbors obeys the frontier. -/
theorem weighted_pair_soundness_frontier [DecidableEq I] [Nonempty P]
    (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (x : I → C → ℝ) (b : R → ℝ) (w : I → ℝ)
    (D : R → Finset C) (label : R → C → I) (s : ℕ) (B H : ℝ)
    (c : C → ℝ) (e : P × Bool ↪ C) (v p a η : ℝ)
    (hw : ProbWeights w) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j)
    (hxpos : ∀ i j, 0 ≤ x i j) (hobj : ∀ i, dot c (x i) = v)
    (hmargin : ∀ i l, a ≤ -p * (x i (e (l, true)) - x i (e (l, false))))
    (hp : p = 1 ∨ p = -1) (ha : 0 < a) (hη : 0 ≤ η)
    (hsound : PairSound A b c e v p η) :
    η ^ 2 * sqNorm b <
      4 * s * B ^ 2 * H ^ 2 * ∑ i, (incidence D label i : ℝ) * (w i) ^ 2 := by
  have hneg : -p = 1 ∨ -p = -1 := by rcases hp with rfl | rfl <;> norm_num
  have hm := mixture_pair_decoder_bound e hw hxpos hx hneg ha hmargin
  have hden : 0 < (Fintype.card C : ℝ) * H ^ 2 :=
    lt_of_lt_of_le hm.1 (sqNorm_height (mix_abs_le hw hx))
  have hwrong : p * pairExpectation e (mix w x) < 0 := by
    have hpos : 0 < (Fintype.card P : ℝ) * a ^ 2 /
        ((Fintype.card C : ℝ) * H ^ 2) := by positivity
    nlinarith [hm.2]
  have hr := weighted_residual_bound A A' x b w D label s B H hw hB hH
    hA hA' hx hs hfeas hlocal
  by_contra! hcost
  have ht : euclideanNorm (residual A (mix w x) b) ≤ η * euclideanNorm b := by
    have hsq : euclideanNorm (residual A (mix w x) b) ^ 2 ≤
        (η * euclideanNorm b) ^ 2 := by
      rw [mul_pow, euclideanNorm_sq, euclideanNorm_sq]
      exact hr.trans hcost
    exact (sq_le_sq₀ (Real.sqrt_nonneg _) (mul_nonneg hη (Real.sqrt_nonneg _))).mp hsq
  have hgood := hsound (mix w x) (mix_nonneg hw hxpos) (mix_objective hw hobj) hm.1 ht
  linarith

end
end QipmFormal.Mixture
