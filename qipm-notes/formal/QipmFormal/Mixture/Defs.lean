import Mathlib

/-!
# Finite mixtures and Euclidean residuals

The vector representation is a function on a finite coordinate type. Its
Euclidean squared norm is an explicit sum, not the function type's sup norm.
-/

namespace QipmFormal.Mixture
noncomputable section
open scoped BigOperators

def ProbWeights {I : Type*} [Fintype I] (w : I → ℝ) : Prop :=
  (∀ i, 0 ≤ w i) ∧ ∑ i, w i = 1

def mix {I C : Type*} [Fintype I] (w : I → ℝ) (x : I → C → ℝ) : C → ℝ :=
  fun j => ∑ i, w i * x i j

def dot {C : Type*} [Fintype C] (a x : C → ℝ) : ℝ := ∑ j, a j * x j

def sqNorm {C : Type*} [Fintype C] (x : C → ℝ) : ℝ := ∑ j, x j ^ 2

def euclideanNorm {C : Type*} [Fintype C] (x : C → ℝ) : ℝ :=
  Real.sqrt (sqNorm x)

def residual {R C : Type*} [Fintype C]
    (A : R → C → ℝ) (x : C → ℝ) (b : R → ℝ) : R → ℝ :=
  fun r => (∑ j, A r j * x j) - b r

def uniformWeight (I : Type*) [Fintype I] : I → ℝ :=
  fun _ => (Fintype.card I : ℝ)⁻¹

theorem uniformWeight_prob (I : Type*) [Fintype I] [Nonempty I] :
    ProbWeights (uniformWeight I) := by
  constructor
  · intro i; exact inv_nonneg.mpr (Nat.cast_nonneg _)
  · simp [uniformWeight, ne_of_gt (Nat.cast_pos.mpr (Fintype.card_pos))]

theorem sqNorm_nonneg {C : Type*} [Fintype C] (x : C → ℝ) : 0 ≤ sqNorm x :=
  Finset.sum_nonneg fun _ _ => sq_nonneg _

theorem euclideanNorm_sq {C : Type*} [Fintype C] (x : C → ℝ) :
    euclideanNorm x ^ 2 = sqNorm x := Real.sq_sqrt (sqNorm_nonneg x)

end
end QipmFormal.Mixture
