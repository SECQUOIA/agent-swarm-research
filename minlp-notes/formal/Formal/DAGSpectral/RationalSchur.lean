import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Tactic

/-! Rational positive-semidefinite Schur elimination, including zero pivots. -/
namespace DAGSpectral
open Matrix

/-- Rational Schur complement at the leading diagonal entry. -/
def rationalSchur {n : ℕ} (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) :
    Matrix (Fin n) (Fin n) ℚ :=
  fun i j => A i.succ j.succ - A i.succ 0 * A 0 j.succ / A 0 0

theorem rationalPSD_diag_nonneg {n : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : A.PosSemidef) (i : Fin n) : 0 ≤ A i i := hA.diag_nonneg

private theorem rationalPSD_symmetric {n : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : A.PosSemidef) (i j : Fin n) : A i j = A j i := by
  have h := congrArg (fun M => M j i) hA.isHermitian
  simpa using h

/-- A zero diagonal entry in a rational PSD matrix forces its entire row to zero. -/
theorem rationalPSD_zero_row {n : ℕ} {A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ}
    (hA : A.PosSemidef) (h0 : A 0 0 = 0) (j : Fin (n + 1)) : A 0 j = 0 := by
  classical
  have hs := rationalPSD_symmetric hA 0 j
  have hq (t : ℚ) : 0 ≤ 2*t*A 0 j + A j j := by
    have h := hA.2 (Finsupp.single 0 t + Finsupp.single j 1)
    simpa [Finsupp.sum_add_index, add_mul, mul_add, h0, ← hs, two_mul,
      mul_comm, mul_left_comm, mul_assoc, add_assoc] using h
  by_contra hn
  have h := hq (-(A j j+1)/(2*A 0 j))
  have he : 2 * (-(A j j+1)/(2*A 0 j)) * A 0 j + A j j = -1 := by
    field_simp
    ring
  rw [he] at h
  norm_num at h

theorem rationalPSD_zero_col {n : ℕ} {A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ}
    (hA : A.PosSemidef) (h0 : A 0 0 = 0) (i : Fin (n + 1)) : A i 0 = 0 := by
  rw [rationalPSD_symmetric hA i 0]
  exact rationalPSD_zero_row hA h0 i

private def rationalSchurEmbedding {n : ℕ}
    (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) : Matrix (Fin (n + 1)) (Fin n) ℚ :=
  fun k j => Fin.cases (-A 0 j.succ/A 0 0) (fun i => if i=j then 1 else 0) k

private theorem rationalSchur_mul_embedding {n : ℕ}
    (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) (i : Fin (n + 1)) (j : Fin n) :
    (A * rationalSchurEmbedding A) i j = A i j.succ - A i 0*A 0 j.succ/A 0 0 := by
  classical
  simp [Matrix.mul_apply, rationalSchurEmbedding, Fin.sum_univ_succ]
  ring

/-- Congruence by the explicit rational elimination embedding gives the Schur matrix. -/
theorem rationalSchur_posSemidef {n : ℕ} {A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ}
    (hA : A.PosSemidef) (ha : 0 < A 0 0) : (rationalSchur A).PosSemidef := by
  have h := hA.conjTranspose_mul_mul_same (rationalSchurEmbedding A)
  have he : (rationalSchurEmbedding A)ᴴ * A * rationalSchurEmbedding A =
      rationalSchur A := by
    rw [Matrix.mul_assoc]
    ext i j
    simp only [Matrix.mul_apply, Fin.sum_univ_succ, Matrix.conjTranspose_apply]
    simp [rationalSchurEmbedding, rationalSchur]
    field_simp
    ring
  rwa [he] at h

end DAGSpectral
