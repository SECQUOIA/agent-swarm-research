import Formal.DAGSpectral.RationalMatrixArithmetic

/-! Concrete scalar payload sizes for copying stored rational vectors and matrices.
The extra unit stores the sign/tag; container control is charged by callers. -/
namespace DAGSpectral.RationalStorage
open ReciprocalAnchor
open scoped BigOperators

def scalarCopy (q : ℚ) : ℕ := q.num.natAbs.size + q.den.size + 1
def vectorCopy {n : ℕ} (x : Fin n → ℚ) : ℕ := ∑ i, scalarCopy (x i)
def matrixCopy {l m : ℕ} (A : Matrix (Fin l) (Fin m) ℚ) : ℕ :=
  ∑ i, vectorCopy (A i)

theorem scalarCopy_le {q : ℚ} {B : ℕ} (h : RationalBits q B) :
    scalarCopy q ≤ 2*B+1 := by
  have hh := (rationalBits_iff_size q B).mp h
  unfold scalarCopy
  omega

theorem vectorCopy_le {n B : ℕ} {x : Fin n → ℚ} (h : ∀ i, RationalBits (x i) B) :
    vectorCopy x ≤ n*(2*B+1) := by
  exact (Finset.sum_le_sum (fun i _ => scalarCopy_le (h i))).trans (by simp)

theorem matrixCopy_le {l m B : ℕ} {A : Matrix (Fin l) (Fin m) ℚ}
    (h : MatrixBits A B) : matrixCopy A ≤ l*m*(2*B+1) := by
  have hh := Finset.sum_le_sum (s := Finset.univ) (fun i _ => vectorCopy_le (h i))
  simpa only [matrixCopy, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    nsmul_eq_mul, Nat.cast_id, Nat.mul_assoc] using hh
end DAGSpectral.RationalStorage
