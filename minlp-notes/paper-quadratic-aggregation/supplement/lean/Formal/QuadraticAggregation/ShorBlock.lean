import Formal.QuadraticAggregation.Model

/-! # The positive semidefinite block constraint in the Shor relaxation -/

open scoped BigOperators Matrix

namespace QuadraticAggregation

variable {n : ℕ}

/-- The rank-one matrix associated with a vector. -/
def outer (x : Vec n) : Mat n := Matrix.of fun i j => x i * x j

/-- The standard Shor lift, with the constant coordinate first. -/
def shorBlock (x : Vec n) (X : Mat n) : Matrix (Unit ⊕ Fin n) (Unit ⊕ Fin n) ℝ :=
  Matrix.fromBlocks 1 (Matrix.of fun _ j => x j) (Matrix.of fun i _ => x i) X

theorem outer_posSemidef (x : Vec n) : (outer x).PosSemidef := by
  simpa [outer, Matrix.vecMulVec] using Matrix.posSemidef_vecMulVec_self_star x

/-- The Schur complement identifies a feasible lift with a PSD covariance matrix. -/
theorem shorBlock_posSemidef_iff (x : Vec n) (X : Mat n) :
    (shorBlock x X).PosSemidef ↔ (X - outer x).PosSemidef := by
  let _ : Invertible (1 : Matrix Unit Unit ℝ) := invertibleOne
  have hrow : (Matrix.of (fun (_ : Unit) j => x j))ᴴ =
      Matrix.of (fun i (_ : Unit) => x i) := by
    ext i j
    simp
  have hprod : Matrix.of (fun i (_ : Unit) => x i) *
      Matrix.of (fun (_ : Unit) j => x j) = outer x := by
    ext i j
    simp [Matrix.mul_apply, outer]
  have h := Matrix.PosDef.fromBlocks₁₁ (A := (1 : Matrix Unit Unit ℝ))
    (Matrix.of (fun (_ : Unit) j => x j)) X Matrix.PosDef.one
  rw [hrow] at h
  simpa only [shorBlock, inv_one, Matrix.mul_one, hprod] using h

theorem shorBlock_affine (x y : Vec n) (X Y : Mat n) (s t : ℝ) (hst : s + t = 1) :
    shorBlock (s • x + t • y) (s • X + t • Y) =
      s • shorBlock x X + t • shorBlock y Y := by
  ext i j
  cases i <;> cases j <;> simp [shorBlock, Matrix.fromBlocks, hst]

end QuadraticAggregation
