import Formal.QuadraticAggregation.ShorBlock

/-!
# The Shor semidefinite relaxation

The projection is expressed by a positive semidefinite slack `Y = X - x xᵀ`.
The block-matrix equivalence below identifies this definition with the standard
Shor relaxation of the closed quadratic system.
-/

open scoped BigOperators Matrix
open Matrix Set

namespace QuadraticAggregation

variable {n m : ℕ}

/-- Trace pairing of real symmetric matrices, written without requiring symmetry. -/
def tracePair (A Y : Mat n) : ℝ := (A * Y).trace

@[simp] theorem tracePair_zero_right (A : Mat n) : tracePair A 0 = 0 := by
  simp [tracePair]

@[simp] theorem tracePair_zero_left (Y : Mat n) : tracePair 0 Y = 0 := by
  simp [tracePair]

theorem tracePair_add_right (A X Y : Mat n) :
    tracePair A (X + Y) = tracePair A X + tracePair A Y := by
  simp [tracePair, Matrix.mul_add]

theorem tracePair_smul_right (A Y : Mat n) (s : ℝ) :
    tracePair A (s • Y) = s * tracePair A Y := by
  simp [tracePair]

theorem tracePair_outer (A : Mat n) (x : Vec n) : tracePair A (outer x) = q A x := by
  simp only [tracePair, Matrix.trace, Matrix.diag, Matrix.mul_apply, outer,
    q, dotProduct, Matrix.mulVec, Finset.mul_sum, Matrix.of_apply]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- The trace pairing of two positive semidefinite matrices is nonnegative. -/
theorem tracePair_nonneg {A Y : Mat n} (hA : A.PosSemidef) (hY : Y.PosSemidef) :
    0 ≤ tracePair A Y := by
  open scoped MatrixOrder in
    obtain ⟨B, rfl⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hY.nonneg
  change 0 ≤ (A * (Bᴴ * B)).trace
  rw [← Matrix.mul_assoc, Matrix.trace_mul_cycle]
  exact (hA.mul_mul_conjTranspose_same B).trace_nonneg

namespace System

/-- The projection of the Shor relaxation, using a PSD covariance slack. -/
def shorProjection (D : System n m) : Set (Vec n) :=
  {x | ∃ Y : Mat n, Y.PosSemidef ∧ ∀ i, D.eval x i + tracePair (D.A i) Y ≤ 0}

theorem tracePair_aggA (D : System n m) (w : Vec m) (Y : Mat n) :
    tracePair (D.aggA w) Y = ∑ i, w i * tracePair (D.A i) Y := by
  simp [tracePair, aggA, Matrix.sum_mul]

theorem closedFeasible_subset_shorProjection (D : System n m) :
    D.closedFeasible ⊆ D.shorProjection := by
  intro x hx
  exact ⟨0, Matrix.PosSemidef.zero, by simpa [closedFeasible] using hx⟩

theorem feasible_subset_shorProjection (D : System n m) :
    D.feasible ⊆ D.shorProjection := by
  intro x hx
  exact D.closedFeasible_subset_shorProjection (fun i => (hx i).le)

/-- Identification with the usual lifted block PSD formulation. -/
theorem mem_shorProjection_iff (D : System n m) (x : Vec n) :
    x ∈ D.shorProjection ↔ ∃ X : Mat n, (shorBlock x X).PosSemidef ∧
      ∀ i, tracePair (D.A i) X + 2 * (D.b i ⬝ᵥ x) + D.c i ≤ 0 := by
  constructor
  · rintro ⟨Y, hY, hi⟩
    refine ⟨outer x + Y, (shorBlock_posSemidef_iff x _).mpr ?_, ?_⟩
    · simpa using hY
    · intro i
      have h := hi i
      simp only [tracePair_add_right, tracePair_outer, eval] at *
      linarith
  · rintro ⟨X, hX, hi⟩
    refine ⟨X - outer x, (shorBlock_posSemidef_iff x X).mp hX, ?_⟩
    intro i
    have heq : tracePair (D.A i) X =
        tracePair (D.A i) (X - outer x) + q (D.A i) x := by
      rw [← tracePair_outer, ← tracePair_add_right, sub_add_cancel]
    have h := hi i
    rw [heq] at h
    simp only [eval]
    linarith

/-- The lifted PSD constraints and affine inequalities give a convex projection. -/
theorem convex_shorProjection (D : System n m) : Convex ℝ D.shorProjection := by
  intro x hx y hy s t hs ht hst
  obtain ⟨X, hX, hiX⟩ := (D.mem_shorProjection_iff x).mp hx
  obtain ⟨Y, hY, hiY⟩ := (D.mem_shorProjection_iff y).mp hy
  apply (D.mem_shorProjection_iff _).mpr
  refine ⟨s • X + t • Y, ?_, ?_⟩
  · rw [shorBlock_affine x y X Y s t hst]
    exact (hX.smul hs).add (hY.smul ht)
  · intro i
    have h := add_nonpos (mul_nonpos_of_nonneg_of_nonpos hs (hiX i))
      (mul_nonpos_of_nonneg_of_nonpos ht (hiY i))
    simp only [tracePair_add_right, tracePair_smul_right, dotProduct_add,
      dotProduct_smul, smul_eq_mul]
    calc
      s * tracePair (D.A i) X + t * tracePair (D.A i) Y +
          2 * (s * (D.b i ⬝ᵥ x) + t * (D.b i ⬝ᵥ y)) + D.c i =
          s * (tracePair (D.A i) X + 2 * (D.b i ⬝ᵥ x) + D.c i) +
          t * (tracePair (D.A i) Y + 2 * (D.b i ⬝ᵥ y) + D.c i) := by
            nlinarith [congrArg (fun r : ℝ => r * D.c i) hst]
      _ ≤ 0 := h

end System
end QuadraticAggregation
