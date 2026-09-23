import Formal.DAGSpectral.CriteriaEigen
import Mathlib.Algebra.Polynomial.Degree.Support

open Matrix Polynomial Unitary
open scoped BigOperators
namespace DAGSpectral
noncomputable section

private theorem coeff_product_nonneg {ι : Type*} (s : Finset ι) (f : ι → ℝ[X])
    (h : ∀ i ∈ s, ∀ k, 0 ≤ (f i).coeff k) : ∀ k, 0 ≤ (∏ i ∈ s, f i).coeff k := by
  classical
  induction s using Finset.induction_on with
  | empty => intro k; simp only [Finset.prod_empty, coeff_one]; split_ifs <;> norm_num
  | @insert i s hi ih =>
    intro k
    rw [Finset.prod_insert hi, coeff_mul]
    exact Finset.sum_nonneg fun j _ => mul_nonneg (h i (Finset.mem_insert_self _ _) _)
      (ih (fun a ha => h a (Finset.mem_insert_of_mem ha)) _)

private theorem monic_eval_pos_of_coeff_nonneg {P : ℝ[X]} (hP : P.Monic)
    (hc : ∀ k, 0 ≤ P.coeff k) {x : ℝ} (hx : 0 < x) : 0 < P.eval x := by
  rw [Polynomial.eval_eq_sum, Polynomial.sum_def]
  apply Finset.sum_pos'
  · intro i _
    exact mul_nonneg (hc i) (pow_nonneg hx.le _)
  · refine ⟨P.natDegree, Polynomial.natDegree_mem_support_of_nonzero hP.ne_zero, ?_⟩
    rw [Polynomial.coeff_natDegree, hP.leadingCoeff, one_mul]
    exact pow_pos hx _

/-- The characteristic polynomial of -A is the product of X plus the actual
real eigenvalues of A. No ordering of eigenvalues is needed. -/
theorem charpoly_neg_eq_prod {n : Type*} [Fintype n] [DecidableEq n]
    {A : Matrix n n ℝ} (hA : A.IsHermitian) :
    (-A).charpoly = ∏ i, (X + C (hA.eigenvalues i)) := by
  have he : -A = Unitary.conjStarAlgAut ℝ _ hA.eigenvectorUnitary
      (diagonal (fun i => -hA.eigenvalues i)) := by
    rw [← Matrix.diagonal_neg, map_neg]
    congr 1
    simpa using hA.spectral_theorem
  rw [he, conjStarAlgAut_apply, charpoly_mul_comm, ← mul_assoc]
  simp [charpoly_diagonal]

/-- A finite exact coefficient test for real symmetric positive semidefiniteness. -/
theorem posSemidef_iff_charpoly_neg_coeff_nonneg {n : Type*} [Fintype n] [DecidableEq n]
    {A : Matrix n n ℝ} (hA : A.IsHermitian) :
    A.PosSemidef ↔ ∀ k, 0 ≤ (-A).charpoly.coeff k := by
  constructor
  · intro hApos
    rw [charpoly_neg_eq_prod hA]
    apply coeff_product_nonneg
    intro i _ k
    rw [coeff_add]
    have hx : 0 ≤ (X : ℝ[X]).coeff k := by simp only [coeff_X]; split_ifs <;> norm_num
    have hc : 0 ≤ (C (hA.eigenvalues i)).coeff k := by
      simp only [coeff_C]
      split_ifs
      · exact hApos.eigenvalues_nonneg i
      · exact le_rfl
    exact add_nonneg hx hc
  · intro hc
    apply hA.posSemidef_iff_eigenvalues_nonneg.mpr
    intro i
    by_contra hn
    change ¬ (0 : ℝ) ≤ hA.eigenvalues i at hn
    have hp : 0 < -hA.eigenvalues i := by linarith
    have he := monic_eval_pos_of_coeff_nonneg (Matrix.charpoly_monic (-A)) hc hp
    have hz : (-A).charpoly.eval (-hA.eigenvalues i) = 0 := by
      rw [charpoly_neg_eq_prod hA, Polynomial.eval_prod]
      apply Finset.prod_eq_zero (Finset.mem_univ i)
      simp
    linarith

end
end DAGSpectral
