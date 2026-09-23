import Formal.DAGSpectral.BitComplexity

namespace DAGSpectral
open ReciprocalAnchor Matrix

/-- Rational inverse via the explicit determinant and adjugate formulas. -/
def rationalMatrixInverse {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    Matrix (Fin n) (Fin n) ℚ := A.det⁻¹ • A.adjugate

theorem rationalMatrixInverse_eq {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    rationalMatrixInverse A = A⁻¹ := by
  rw [Matrix.inv_def]
  simp [rationalMatrixInverse]

/-- Actual reduced entry sizes of a finite rational matrix. -/
def MatrixBits {ι κ : Type*} (A : Matrix ι κ ℚ) (B : ℕ) : Prop :=
  ∀ i j, RationalBits (A i j) B

theorem rationalBits_finset_prod {ι : Type*} (s : Finset ι) (f : ι → ℚ) {B : ℕ}
    (h : ∀ i ∈ s, RationalBits (f i) B) :
    RationalBits (∏ i ∈ s, f i) (1+s.card*B) := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using rationalBits_one
  | @insert i s hi ih =>
    have hq := h i (by simp)
    have hs := ih (fun j hj => h j (by simp [hj]))
    have hp := rationalBits_mul hq hs
    rw [Finset.prod_insert hi,Finset.card_insert_of_notMem hi]
    convert hp using 1
    ring

theorem rationalBits_sign_mul {q : ℚ} {B : ℕ} (hq : RationalBits q B) (s : ℤˣ) :
    RationalBits ((s:ℤ)*q) B := by
  rcases Int.units_eq_one_or s with rfl | rfl
  · simpa using hq
  · simpa using rationalBits_neg hq

theorem matrixBits_mul {l n m B C : ℕ}
    {A : Matrix (Fin l) (Fin n) ℚ} {D : Matrix (Fin n) (Fin m) ℚ}
    (hA : MatrixBits A B) (hD : MatrixBits D C) :
    MatrixBits (A*D) (1+n*(B+C+1)) := by
  intro i j
  simpa only [Matrix.mul_apply,Finset.card_univ,Fintype.card_fin] using
    rationalBits_finset_sum Finset.univ (fun k => A i k*D k j)
      (fun k _ => rationalBits_mul (hA i k) (hD k j))

theorem matrixBits_transpose {ι κ : Type*} {A : Matrix ι κ ℚ} {B : ℕ}
    (hA : MatrixBits A B) : MatrixBits Aᵀ B := fun i j => hA j i

/-- Leibniz evaluation has dimension-dependent coefficients but linear growth
in the input bit bound. The dimension is fixed in the application. -/
def determinantBits (n B : ℕ) : ℕ := 1+n.factorial*(n*B+3)

theorem matrixBits_det {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A B) : RationalBits A.det (determinantBits n B) := by
  rw [Matrix.det_apply']
  have hs := rationalBits_finset_sum Finset.univ
    (fun σ : Equiv.Perm (Fin n) => ((Equiv.Perm.sign σ : ℤ) : ℚ) * ∏ i, A (σ i) i)
    (B := 1+n*B) (by
      intro σ _
      apply rationalBits_sign_mul
      simpa only [Finset.card_univ,Fintype.card_fin] using
        rationalBits_finset_prod Finset.univ (fun i => A (σ i) i) (fun i _ => hA _ _))
  apply rationalBits_mono hs
  simp only [Finset.card_univ,Fintype.card_perm,Fintype.card_fin,determinantBits]
  nlinarith

theorem matrixBits_adjugate {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A B) : MatrixBits A.adjugate (determinantBits n (B+1)) := by
  intro i j
  rw [Matrix.adjugate_apply]
  apply matrixBits_det
  intro k l
  by_cases hk : k=j
  · subst k
    simp only [Matrix.updateRow_self,Pi.single_apply]
    split_ifs
    · exact rationalBits_mono rationalBits_one (by omega)
    · exact rationalBits_mono rationalBits_zero (by omega)
  · rw [Matrix.updateRow_ne hk]
    exact rationalBits_mono (hA _ _) (by omega)

theorem determinantBits_mono (n : ℕ) {B C : ℕ} (h : B ≤ C) :
    determinantBits n B ≤ determinantBits n C := by
  unfold determinantBits
  exact Nat.add_le_add_left (Nat.mul_le_mul_left _
    (Nat.add_le_add_right (Nat.mul_le_mul_left n h) 3)) 1

def inverseBits (n B : ℕ) : ℕ := 2*determinantBits n (B+1)

theorem matrixBits_inverse {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A B) : MatrixBits (rationalMatrixInverse A) (inverseBits n B) := by
  intro i j
  have hd := rationalBits_inv (matrixBits_det hA)
  have ha := matrixBits_adjugate hA i j
  have hp := rationalBits_mul hd ha
  apply rationalBits_mono hp
  have hm := determinantBits_mono n (Nat.le_succ B)
  simp only [Nat.succ_eq_add_one] at hm
  unfold inverseBits
  omega

end DAGSpectral
