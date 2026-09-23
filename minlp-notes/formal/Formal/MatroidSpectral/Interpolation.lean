import Mathlib.LinearAlgebra.Lagrange
import Mathlib.Algebra.MvPolynomial.Eval
import Mathlib.Algebra.BigOperators.Ring.Finset

namespace MatroidSpectral

open scoped BigOperators
open Polynomial

/-- Positive integer nodes, represented exactly in the rational field. -/
def interpolationNode {D : ℕ} (t : Fin (D + 1)) : ℚ := (t.val + 1 : ℕ)

theorem interpolationNode_injective (D : ℕ) :
    Function.Injective (@interpolationNode D) := by
  intro a b h
  apply Fin.ext
  unfold interpolationNode at h
  exact Nat.add_right_cancel (by exact_mod_cast h : a.val + 1 = b.val + 1)

noncomputable def interpolationWeight (D : ℕ) (t : Fin (D + 1)) (k : ℕ) : ℚ :=
  (Lagrange.basis Finset.univ interpolationNode t).coeff k

/-- A tensor Lagrange solve. Only the supplied grid values enter this formula. -/
noncomputable def interpolateCoefficient {κ : Type*} [Fintype κ] [DecidableEq κ] (D : ℕ)
    (values : (κ → Fin (D + 1)) → ℚ) (z : κ →₀ ℕ) : ℚ :=
  ∑ t : κ → Fin (D + 1), values t * ∏ i, interpolationWeight D (t i) (z i)

theorem interpolationWeight_moment (D k n : ℕ) (hn : n ≤ D) :
    (∑ t : Fin (D + 1), interpolationNode t ^ n * interpolationWeight D t k) =
      if n = k then 1 else 0 := by
  have hi := Lagrange.eq_interpolate
    (s := (Finset.univ : Finset (Fin (D+1))))
    (v := @interpolationNode D) (f := (Polynomial.X : ℚ[X]) ^ n)
    (interpolationNode_injective D).injOn
    (by
      simp only [Polynomial.degree_X_pow, Finset.card_univ, Fintype.card_fin]
      exact_mod_cast (show n < D + 1 by omega))
  have hc := congrArg (fun P : ℚ[X] => P.coeff k) hi
  simpa only [Lagrange.interpolate_apply, Polynomial.finsetSum_coeff,
    Polynomial.eval_pow, Polynomial.eval_X, ← Polynomial.C_pow,
    Polynomial.coeff_C_mul, interpolationWeight, Polynomial.coeff_X_pow,
    eq_comm] using hc.symm

theorem interpolation_tensor_moment {κ : Type*} [Fintype κ] [DecidableEq κ] (D : ℕ)
    (a z : κ →₀ ℕ) (ha : ∀ i, a i ≤ D) :
    (∑ t : κ → Fin (D+1),
      (∏ i, interpolationNode (t i) ^ a i) *
        ∏ i, interpolationWeight D (t i) (z i)) = if a = z then 1 else 0 := by
  classical
  simp_rw [← Finset.prod_mul_distrib]
  rw [← Fintype.prod_sum (fun i t =>
    interpolationNode t ^ a i * interpolationWeight D t (z i))]
  simp_rw [interpolationWeight_moment D _ _ (ha _)]
  by_cases h : a = z
  · subst z
    simp
  · have he : ∃ i, a i ≠ z i := by
      by_contra! hn
      exact h (Finsupp.ext hn)
    obtain ⟨i, hi⟩ := he
    rw [if_neg h]
    exact Finset.prod_eq_zero (Finset.mem_univ i) (if_neg hi)

/-- Exact coefficient recovery for every polynomial with the specified coordinate
degree bound, including the zero-variable and constant-polynomial cases. -/
theorem interpolateCoefficient_eq_coeff {κ : Type*} [Fintype κ] [DecidableEq κ] (D : ℕ)
    (P : MvPolynomial κ ℚ)
    (hP : ∀ a ∈ P.support, ∀ i, a i ≤ D) (z : κ →₀ ℕ) :
    interpolateCoefficient D
      (fun t => MvPolynomial.eval (fun i => interpolationNode (t i)) P) z =
        P.coeff z := by
  classical
  unfold interpolateCoefficient
  simp_rw [MvPolynomial.eval_eq', Finset.sum_mul]
  rw [Finset.sum_comm]
  simp_rw [mul_assoc, ← Finset.mul_sum]
  calc
    _ = ∑ a ∈ P.support, P.coeff a * (if a = z then 1 else 0) := by
      apply Finset.sum_congr rfl
      intro a ha
      rw [interpolation_tensor_moment D a z (hP a ha)]
    _ = P.coeff z := by simp [eq_comm]

end MatroidSpectral
