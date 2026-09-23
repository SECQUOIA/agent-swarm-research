import Formal.DAGSpectral.CriteriaEigen
import Formal.DAGSpectral.RatMatrix
import Formal.DAGSpectral.EigenCompareSeparation
import Mathlib.LinearAlgebra.Eigenspace.Charpoly
import Mathlib.LinearAlgebra.Charpoly.ToMatrix

/-! A rational matrix whose eigenvalues include every cross-matrix difference.
This converts exact equality of eigenvalues into the zero-root case of a
single fixed-degree characteristic polynomial. -/
namespace DAGSpectral
open Matrix
variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The Kronecker difference, written entrywise to keep rational computation explicit. -/
def eigenDifferenceMatrix {R : Type*} [Ring R] (A B : Matrix n n R) :
    Matrix (n × n) (n × n) R :=
  fun i j => (if i.2 = j.2 then A i.1 j.1 else 0) -
    (if i.1 = j.1 then B i.2 j.2 else 0)

theorem eigenDifferenceMatrix_mulVec (A B : Matrix n n ℝ) (u v : n → ℝ) :
    eigenDifferenceMatrix A B *ᵥ (fun i => u i.1 * v i.2) =
      fun i => (A *ᵥ u) i.1 * v i.2 - u i.1 * (B *ᵥ v) i.2 := by
  ext i
  simp only [mulVec, dotProduct, eigenDifferenceMatrix, sub_mul,
    Finset.sum_sub_distrib, Fintype.sum_prod_type]
  have hleft : (∑ k, ∑ l, (if i.2 = l then A i.1 k else 0) * (u k * v l)) =
      (∑ k, A i.1 k * u k) * v i.2 := by
    simp [ite_mul, Finset.sum_mul, mul_assoc]
  have hright : (∑ k, ∑ l, (if i.1 = k then B i.2 l else 0) * (u k * v l)) =
      u i.1 * ∑ l, B i.2 l * v l := by
    rw [Finset.sum_comm]
    simp [Finset.mul_sum, mul_left_comm, mul_comm]
  exact congrArg₂ (· - ·) hleft hright

theorem eigenDifferenceMatrix_isRoot {A B : Matrix n n ℝ} {u v : n → ℝ}
    {a b : ℝ} (hu : u ≠ 0) (hv : v ≠ 0)
    (hAu : A *ᵥ u = a • u) (hBv : B *ᵥ v = b • v) :
    (eigenDifferenceMatrix A B).charpoly.IsRoot (a-b) := by
  have hn : (fun i : n × n => u i.1 * v i.2) ≠ 0 := by
    obtain ⟨i, hi⟩ := Function.ne_iff.mp hu
    obtain ⟨j, hj⟩ := Function.ne_iff.mp hv
    intro h
    have hh := congrFun h (i,j)
    exact mul_ne_zero hi hj hh
  have he : Module.End.HasEigenvector (eigenDifferenceMatrix A B).toLin' (a-b)
      (fun i : n × n => u i.1 * v i.2) := by
    refine ⟨?_, hn⟩
    rw [Module.End.mem_eigenspace_iff]
    change eigenDifferenceMatrix A B *ᵥ _ = _
    rw [eigenDifferenceMatrix_mulVec, hAu, hBv]
    ext i
    simp only [Pi.smul_apply, smul_eq_mul]
    ring
  have hh := (Module.End.hasEigenvalue_iff_isRoot_charpoly _ _).mp
    (Module.End.hasEigenvalue_of_hasEigenvector he)
  simpa only [Matrix.charpoly_toLin'] using hh

omit [Fintype n] in
theorem ratMatrixReal_eigenDifference (A B : Matrix n n ℚ) :
    ratMatrixReal (eigenDifferenceMatrix A B) =
      eigenDifferenceMatrix (ratMatrixReal A) (ratMatrixReal B) := by
  ext i j
  simp only [ratMatrixReal_apply, eigenDifferenceMatrix]
  split_ifs <;> push_cast <;> rfl

/-- The characteristic polynomial has fixed degree `card(n)^2`. -/
noncomputable def eigenDifferencePolynomial (A B : Matrix n n ℚ) : Polynomial ℚ :=
  (eigenDifferenceMatrix A B).charpoly

theorem eigenDifferencePolynomial_ne_zero (A B : Matrix n n ℚ) :
    eigenDifferencePolynomial A B ≠ 0 :=
  (Matrix.charpoly_monic _).ne_zero

theorem eigenDifferencePolynomial_degree (A B : Matrix n n ℚ) :
    (eigenDifferencePolynomial A B).natDegree = Fintype.card n ^ 2 := by
  simp [eigenDifferencePolynomial, Matrix.charpoly_natDegree_eq_dim, pow_two]

variable [Nonempty n]

theorem minimumEigenvalue_difference_root (A B : Matrix n n ℚ)
    (hA : (ratMatrixReal A).IsHermitian) (hB : (ratMatrixReal B).IsHermitian) :
    (eigenDifferencePolynomial A B).eval₂ (Rat.castHom ℝ)
      (minimumEigenvalue (ratMatrixReal A) - minimumEigenvalue (ratMatrixReal B)) = 0 := by
  obtain ⟨i, hi⟩ := minimumEigenvalue_attained hA
  obtain ⟨j, hj⟩ := minimumEigenvalue_attained hB
  rw [hi, hj]
  have hu := (WithLp.ofLp_eq_zero 2).ne.2 (hA.eigenvectorBasis.orthonormal.ne_zero i)
  have hv := (WithLp.ofLp_eq_zero 2).ne.2 (hB.eigenvectorBasis.orthonormal.ne_zero j)
  have hr := eigenDifferenceMatrix_isRoot hu hv
    (hA.mulVec_eigenvectorBasis i) (hB.mulVec_eigenvectorBasis j)
  rw [← ratMatrixReal_eigenDifference] at hr
  simpa only [eigenDifferencePolynomial, ratMatrixReal, Matrix.charpoly_map,
    Polynomial.IsRoot, Polynomial.eval_map] using hr

/-- Distinct least eigenvalues are separated by an explicitly computed positive rational.
Repeated eigenvalues and an arbitrarily large zero-root multiplicity are allowed. -/
theorem minimumEigenvalue_separation (A B : Matrix n n ℚ)
    (hA : (ratMatrixReal A).IsHermitian) (hB : (ratMatrixReal B).IsHermitian)
    (hne : minimumEigenvalue (ratMatrixReal A) ≠ minimumEigenvalue (ratMatrixReal B)) :
    (ratRootSeparation (eigenDifferencePolynomial A B) : ℝ) ≤
      |minimumEigenvalue (ratMatrixReal A) - minimumEigenvalue (ratMatrixReal B)| :=
  ratPolynomial_nonzero_root_bound (eigenDifferencePolynomial_ne_zero A B)
    (sub_ne_zero.mpr hne) (minimumEigenvalue_difference_root A B hA hB)

end DAGSpectral
