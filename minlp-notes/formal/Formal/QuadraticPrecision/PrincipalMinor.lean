import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.LinearAlgebra.Matrix.Charpoly.Coeff

namespace QuadraticPrecision

open Matrix Polynomial

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The first nonzero characteristic coefficient of a real symmetric matrix
occurs at its nullity. -/
theorem charpoly_coeff_nullity_ne_zero (H : Matrix n n ℝ) (hH : H.IsHermitian) :
    H.charpoly.coeff (Fintype.card n - H.rank) ≠ 0 := by
  classical
  let s : Finset n := Finset.univ.filter (fun i => hH.eigenvalues i ≠ 0)
  have hr : H.rank = s.card := by
    rw [hH.rank_eq_card_non_zero_eigs]
    exact Fintype.card_subtype _
  have hpoly : H.charpoly =
      (∏ i ∈ s, (X - C (hH.eigenvalues i))) * X ^ (Fintype.card n - s.card) := by
    rw [hH.charpoly_eq]
    simp only [RCLike.ofReal_real_eq_id, id_eq]
    have heq := Finset.prod_filter_mul_prod_filter_not (s := Finset.univ)
      (p := fun i => hH.eigenvalues i ≠ 0) (f := fun i => (X - C (hH.eigenvalues i) : ℝ[X]))
    rw [← heq]
    congr 1
    have he : ∀ i ∈ Finset.univ.filter (fun i => ¬ hH.eigenvalues i ≠ 0),
        (X - C (hH.eigenvalues i) : ℝ[X]) = X := by
      intro i hi
      simp only [Finset.mem_filter, not_not] at hi
      simp [hi.2]
    rw [Finset.prod_congr rfl he, Finset.prod_const]
    congr 1
    have hc := Finset.card_filter_add_card_filter_not (s := Finset.univ)
      (p := fun i => hH.eigenvalues i ≠ 0)
    simp only [Finset.card_univ] at hc
    change (Finset.univ.filter (fun i => hH.eigenvalues i ≠ 0)).card +
      (Finset.univ.filter (fun i => ¬ hH.eigenvalues i ≠ 0)).card = Fintype.card n at hc
    exact Nat.eq_sub_of_add_eq' hc
  rw [hr, hpoly, Polynomial.coeff_mul_X_pow']
  simp only [Nat.sub_self, le_refl, ite_true, Polynomial.coeff_zero_prod]
  apply Finset.prod_ne_zero_iff.mpr
  intro i hi
  simpa using (Finset.mem_filter.mp hi).2

/-- A real symmetric matrix has a nonsingular principal submatrix whose size
is its rank. This includes the empty minor when the rank is zero. -/
theorem exists_principal_minor_rank (H : Matrix n n ℝ) (hH : H.IsHermitian) :
    ∃ s : Finset n, s.card = H.rank ∧
      (H.submatrix (Subtype.val : s → n) (Subtype.val : s → n)).det ≠ 0 := by
  classical
  have hc := charpoly_coeff_nullity_ne_zero H hH
  rw [Matrix.charpoly_coeff_eq_sum_minors H H.rank H.rank_le_card_width] at hc
  have hs : (∑ s ∈ Finset.univ.powersetCard H.rank,
      (H.submatrix (Subtype.val : s → n) (Subtype.val : s → n)).det) ≠ 0 := by
    intro h
    exact hc (by rw [h, mul_zero])
  obtain ⟨s, hmem, hdet⟩ := Finset.exists_ne_zero_of_sum_ne_zero hs
  exact ⟨s, (Finset.mem_powersetCard.mp hmem).2, hdet⟩

end QuadraticPrecision
