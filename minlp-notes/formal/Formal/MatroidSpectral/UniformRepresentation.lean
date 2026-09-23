import Formal.MatroidSpectral.Representation
import Formal.DAGSpectral.RationalMatrixArithmetic
import Mathlib.LinearAlgebra.Vandermonde

/-! Explicit rational Vandermonde representations for growing-rank uniform
matroids. Entry encodings are polynomial in both dimensions. -/
namespace MatroidSpectral
open Matrix ReciprocalAnchor DAGSpectral

def uniformRepresentation (q m : ℕ) : RationalRepresentation q m :=
  fun i j => ((j.val + 1 : ℕ) : ℚ) ^ i.val

theorem uniform_minor_nonzero {q m : ℕ} (b : Fin q ↪ Fin m) :
    ((uniformRepresentation q m).submatrix id b).det ≠ 0 := by
  have he : (uniformRepresentation q m).submatrix id b =
      (Matrix.vandermonde (fun j => (((b j).val + 1 : ℕ) : ℚ))).transpose := by
    ext i j
    rfl
  rw [he, Matrix.det_transpose, Matrix.det_vandermonde_ne_zero_iff]
  intro i j h
  apply b.injective
  apply Fin.ext
  exact Nat.add_right_cancel (Nat.cast_injective h)

/-- Exactly the prescribed-cardinality subsets are bases. -/
theorem uniform_isBase_iff {q m : ℕ} (B : Finset (Fin m)) :
    IsBase (uniformRepresentation q m) B ↔ B.card = q := by
  constructor
  · exact IsBase.card
  · intro h
    rw [isBase_iff h]
    exact uniform_minor_nonzero (B.orderEmbOfFin h).toEmbedding

theorem uniform_has_base {q m : ℕ} (hq : q ≤ m) :
    ∃ B, IsBase (uniformRepresentation q m) B := by
  let b : Fin q ↪ Fin m := ⟨Fin.castLE hq, Fin.castLE_injective hq⟩
  exact ⟨Finset.univ.image b,
    (orderedMinor_isBase _ b).mpr (uniform_minor_nonzero b)⟩

/-- The displayed rational numbers have a polynomial bit bound even when q grows. -/
theorem uniformRepresentation_bits (q m : ℕ) :
    MatrixBits (uniformRepresentation q m) ((m+1)*(q+1)+1) := by
  intro i j
  change RationalBits (((j.val+1 : ℕ) : ℚ)^i.val) _
  rw [← Nat.cast_pow]
  simp only [RationalBits, Rat.num_natCast, Rat.den_natCast, Int.natAbs_natCast]
  have hb : j.val + 1 ≤ 2^(m+1) := by
    exact (show j.val+1 ≤ m by omega).trans
      ((Nat.lt_two_pow_self (n := m)).le.trans
        (Nat.pow_le_pow_right (by decide) (by omega)))
  have hv : (j.val+1)^i.val ≤ 2^((m+1)*q) := by
    calc
      _ ≤ (2^(m+1))^i.val := Nat.pow_le_pow_left hb _
      _ ≤ (2^(m+1))^q := Nat.pow_le_pow_right (by positivity) i.isLt.le
      _ = _ := (pow_mul _ _ _).symm
  constructor
  · exact hv.trans_lt (Nat.pow_lt_pow_right (by decide) (by nlinarith))
  · exact Nat.one_lt_two_pow (by positivity)

end MatroidSpectral
