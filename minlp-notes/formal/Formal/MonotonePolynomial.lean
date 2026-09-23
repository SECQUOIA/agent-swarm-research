import Formal.PolynomialFamily
import Formal.Scalar

namespace ExactCounts

open Polynomial

/-- Adding a linear term makes the decreasing component nondecreasing on the input interval. -/
noncomputable def monotoneLeftValue (x : ℝ) : ℝ := leftValue x + 56 * x

/-- The monotone component remains a rational polynomial of degree 32. -/
noncomputable def monotoneLeftPoly : ℚ[X] := leftPoly + C 56 * X

@[simp] theorem aeval_monotoneLeftPoly (x : ℝ) :
    aeval x monotoneLeftPoly = monotoneLeftValue x := by
  simp [monotoneLeftPoly, monotoneLeftValue]

@[simp] theorem monotoneLeftPoly_natDegree : monotoneLeftPoly.natDegree = 32 := by
  rw [monotoneLeftPoly, natDegree_add_eq_left_of_natDegree_lt]
  · exact leftPoly_natDegree
  · simp

theorem hasDerivAt_monotoneLeftValue (x : ℝ) :
    HasDerivAt monotoneLeftValue (56 * (1 - (1 - x) ^ 31)) x := by
  have h := (((hasDerivAt_id x).const_sub 1).pow 32).const_mul (7 / 4 : ℝ)
  have h' := h.add ((hasDerivAt_id x).const_mul 56)
  change HasDerivAt monotoneLeftValue
    ((7 / 4 : ℝ) * (32 * (1 - x) ^ 31 * -1) + 56 * 1) x at h'
  exact h'.congr_deriv (by ring)

theorem deriv_monotoneLeftValue (x : ℝ) :
    deriv monotoneLeftValue x = 56 * (1 - (1 - x) ^ 31) :=
  (hasDerivAt_monotoneLeftValue x).deriv

theorem monotoneLeftValue_monotone : MonotoneOn monotoneLeftValue (Set.Icc 0 1) := by
  apply monotoneOn_of_deriv_nonneg (convex_Icc 0 1)
  · exact (continuous_iff_continuousAt.mpr
      (fun x => (hasDerivAt_monotoneLeftValue x).continuousAt)).continuousOn
  · exact fun x _ => (hasDerivAt_monotoneLeftValue x).differentiableAt.differentiableWithinAt
  · intro x hx
    have hx' : x ∈ Set.Icc (0 : ℝ) 1 := interior_subset hx
    rw [deriv_monotoneLeftValue]
    have hp : (1 - x) ^ 31 ≤ 1 := pow_le_one₀ (by linarith [hx'.2]) (by linarith [hx'.1])
    positivity

theorem rightValue_monotone : MonotoneOn rightValue (Set.Icc 0 1) := by
  intro x hx y _ hxy
  exact mul_le_mul_of_nonneg_left (pow_le_pow_left₀ hx.1 hxy 32) (by norm_num)

theorem monotoneLeftValue_convex : ConvexOn ℝ (Set.Icc 0 1) monotoneLeftValue := by
  refine ⟨convex_Icc 0 1, ?_⟩
  intro x hx y hy a b ha hb hab
  have h := leftValue_convex.2 hx hy ha hb hab
  simp only [smul_eq_mul] at h ⊢
  dsimp [monotoneLeftValue]
  nlinarith

/-- Monotonicity and convexity do not require nonnegative monomial coefficients. -/
theorem monotoneLeftPoly_coeff_three : monotoneLeftPoly.coeff 3 = -8680 := by
  have h : (1 - (X : ℚ[X])) ^ 32 = (X + C (-1)) ^ 32 := by
    have he : 1 - (X : ℚ[X]) = -(X + C (-1)) := by simp; ring
    rw [he, neg_pow]
    norm_num
  rw [monotoneLeftPoly, coeff_add, leftPoly, coeff_C_mul, h, coeff_X_add_C_pow]
  norm_num [coeff_C_mul, Nat.choose]

theorem monotoneLeftPoly_not_nonnegative_coefficients :
    ¬ ∀ k, 0 ≤ monotoneLeftPoly.coeff k := by
  intro h
  have h3 := h 3
  rw [monotoneLeftPoly_coeff_three] at h3
  norm_num at h3

end ExactCounts
