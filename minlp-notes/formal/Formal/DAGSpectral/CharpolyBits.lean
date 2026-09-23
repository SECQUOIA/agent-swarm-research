import Formal.DAGSpectral.RationalMatrixArithmetic
import Mathlib.LinearAlgebra.Matrix.Charpoly.Coeff

namespace DAGSpectral
open ReciprocalAnchor Matrix

/-- An executable coefficient formula avoiding a polynomial-ring evaluator. -/
def rationalCharpolyCoeff {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (k : ℕ) : ℚ :=
  if k ≤ n then (-1 : ℚ)^(n-k) *
    ∑ s ∈ (Finset.univ : Finset (Fin n)).powersetCard (n-k),
      (A.submatrix (Subtype.val : s → Fin n) (Subtype.val : s → Fin n)).det
  else 0

theorem rationalCharpolyCoeff_eq {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (k : ℕ) :
    rationalCharpolyCoeff A k = A.charpoly.coeff k := by
  unfold rationalCharpolyCoeff
  split_ifs with hk
  · have h := A.charpoly_coeff_eq_sum_minors (n-k) (by simp)
    simp only [Fintype.card_fin, Nat.sub_sub_self hk] at h
    exact h.symm
  · symm
    apply Polynomial.coeff_eq_zero_of_natDegree_lt
    simpa only [Matrix.charpoly_natDegree_eq_dim,Fintype.card_fin] using lt_of_not_ge hk

/-- Exponential dependence on the fixed matrix dimension, linear dependence on
input bit length. It bounds every coefficient including all zero coefficients. -/
def charpolyBits (n B : ℕ) : ℕ := 1+2^n*(determinantBits n B+1)

theorem determinantBits_dim_mono {n m : ℕ} (h : n ≤ m) (B : ℕ) :
    determinantBits n B ≤ determinantBits m B := by
  unfold determinantBits
  exact Nat.add_le_add_left (Nat.mul_le_mul (Nat.factorial_le h)
    (Nat.add_le_add_right (Nat.mul_le_mul_right B h) 3)) 1

theorem matrixBits_det_finite {ι : Type*} [Fintype ι] [DecidableEq ι] {B : ℕ}
    {A : Matrix ι ι ℚ} (hA : MatrixBits A B) :
    RationalBits A.det (determinantBits (Fintype.card ι) B) := by
  rw [Matrix.det_apply']
  have hs := rationalBits_finset_sum Finset.univ
    (fun σ : Equiv.Perm ι => ((Equiv.Perm.sign σ : ℤ) : ℚ) * ∏ i, A (σ i) i)
    (B := 1+Fintype.card ι*B) (by
      intro σ _
      apply rationalBits_sign_mul
      simpa only [Finset.card_univ] using
        rationalBits_finset_prod Finset.univ (fun i => A (σ i) i) (fun i _ => hA _ _))
  apply rationalBits_mono hs
  simp only [Finset.card_univ,Fintype.card_perm,determinantBits]
  nlinarith

theorem rationalCharpolyCoeff_bits {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A B) (k : ℕ) :
    RationalBits (rationalCharpolyCoeff A k) (charpolyBits n B) := by
  unfold rationalCharpolyCoeff
  split_ifs with hk
  · have hminor (s : Finset (Fin n)) :
        RationalBits (A.submatrix (Subtype.val : s → Fin n) (Subtype.val : s → Fin n)).det
          (determinantBits n B) := by
      apply rationalBits_mono (matrixBits_det_finite (A := A.submatrix (Subtype.val : s → Fin n)
        (Subtype.val : s → Fin n)) (fun i j => hA i j))
      apply determinantBits_dim_mono
      simpa using Finset.card_le_univ s
    have hs := rationalBits_finset_sum (Finset.univ.powersetCard (n-k))
      (fun s : Finset (Fin n) =>
        (A.submatrix (Subtype.val : s → Fin n) (Subtype.val : s → Fin n)).det)
      (fun s _ => hminor s)
    have hc : (Finset.univ.powersetCard (n-k) : Finset (Finset (Fin n))).card ≤ 2^n := by
      have hsub : (Finset.univ.powersetCard (n-k) : Finset (Finset (Fin n))) ⊆
          Finset.univ.powerset := by
        intro s hs
        exact Finset.mem_powerset.mpr (Finset.mem_powersetCard.mp hs).1
      simpa using Finset.card_le_card hsub
    have hs' : RationalBits (∑ s ∈ Finset.univ.powersetCard (n-k),
        (A.submatrix (Subtype.val : s → Fin n) (Subtype.val : s → Fin n)).det)
        (charpolyBits n B) := rationalBits_mono hs (by
      unfold charpolyBits
      exact Nat.add_le_add_left (Nat.mul_le_mul_right _ hc) 1)
    rcases neg_one_pow_eq_or ℚ (n-k) with h | h
    · simpa [h] using hs'
    · simpa [h] using rationalBits_neg hs'
  · exact rationalBits_mono rationalBits_zero (by unfold charpolyBits; omega)

theorem matrixBits_charpoly_coeff {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A B) (k : ℕ) :
    RationalBits (A.charpoly.coeff k) (charpolyBits n B) := by
  rw [← rationalCharpolyCoeff_eq]
  exact rationalCharpolyCoeff_bits hA k

end DAGSpectral
