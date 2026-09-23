import Formal.CubicGap.Expectation

/-! Independent finite products of laws, allowing a different state type per coordinate. -/
namespace CubicGap.Law

noncomputable section
open scoped BigOperators
variable {C : Type*} [Fintype C] [DecidableEq C] {A : C → Type*} [∀ c, Fintype (A c)]

/-- The independent product of finitely many finite laws. -/
def pi (μ : ∀ c, Law (A c)) : Law (∀ c, A c) where
  weight w := ∏ c, (μ c).weight (w c)
  nonneg w := Finset.prod_nonneg (fun c _ => (μ c).nonneg (w c))
  mass_one := by
    classical
    rw [← Fintype.prod_sum]
    simp [Law.mass_one]

/-- Products of observables factor under the independent product law. -/
theorem expect_pi_prod (μ : ∀ c, Law (A c)) (f : ∀ c, A c → ℝ) :
    (pi μ).expect (fun w => ∏ c, f c (w c)) = ∏ c, (μ c).expect (f c) := by
  classical
  simp only [Law.expect, pi, ← Finset.prod_mul_distrib]
  exact (Fintype.prod_sum (fun c a => (μ c).weight a * f c a)).symm

/-- Every component of an independent product retains its original law. -/
theorem expect_pi_coordinate (μ : ∀ c, Law (A c)) (c : C) (f : A c → ℝ) :
    (pi μ).expect (fun w => f (w c)) = (μ c).expect f := by
  classical
  let g : ∀ i, A i → ℝ := fun i a => if h : i = c then f (h ▸ a) else 1
  have hg (w : ∀ c, A c) : (∏ i, g i (w i)) = f (w c) := by
    dsimp [g]
    simp
  have he (i : C) : (μ i).expect (g i) = if h : i = c then (μ c).expect f else 1 := by
    by_cases h : i = c
    · subst i
      simp [g]
    · simp [g, h]
  have h := expect_pi_prod μ g
  simp only [hg, he] at h
  simpa using h

end
end CubicGap.Law
