import Formal.DAGSpectral.RationalMatrixArithmetic

/-! Polynomial bounds for rational determinant encodings with variable dimension.
The common denominator is a product over entries, so the Leibniz formula is used
only to bound the value, never as an algorithm for evaluating it. -/
namespace MatroidSpectral
open Matrix ReciprocalAnchor DAGSpectral

/-- A common positive denominator for all entries, including the empty matrix. -/
def matrixDenominator {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : ℕ :=
  ∏ i, ∏ j, (A i j).den

lemma matrixDenominator_pos {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    0 < matrixDenominator A := by
  exact Finset.prod_pos (fun i _ => Finset.prod_pos (fun j _ => (A i j).den_pos))

lemma entry_den_dvd {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (i j : Fin n) :
    (A i j).den ∣ matrixDenominator A := by
  exact (Finset.dvd_prod_of_mem (fun j => (A i j).den) (Finset.mem_univ j)).trans
    (Finset.dvd_prod_of_mem (fun i => ∏ j, (A i j).den) (Finset.mem_univ i))

lemma matrixDenominator_le {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A B) : matrixDenominator A ≤ 2 ^ (n*n*B) := by
  calc
    matrixDenominator A ≤ ∏ _i : Fin n, ∏ _j : Fin n, 2 ^ B :=
      Finset.prod_le_prod' (fun i _ => Finset.prod_le_prod' (fun j _ => (hA i j).2.le))
    _ = 2 ^ (n*n*B) := by
      simp only [Finset.prod_const, Finset.card_univ, Fintype.card_fin, ← pow_mul]
      congr 1
      ring

/-- Clearing all denominators using integer division, which is exact. -/
def integerMatrix {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : Matrix (Fin n) (Fin n) ℤ :=
  fun i j => (A i j).num * (matrixDenominator A / (A i j).den : ℕ)

lemma integerMatrix_cast {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (integerMatrix A).map (Int.castRingHom ℚ) = (matrixDenominator A : ℚ) • A := by
  ext i j
  simp only [Matrix.map_apply, integerMatrix, Int.coe_castRingHom, Int.cast_mul,
    Int.cast_natCast, Matrix.smul_apply, smul_eq_mul]
  have he : ((matrixDenominator A / (A i j).den : ℕ) : ℚ) =
      (matrixDenominator A : ℚ) / ((A i j).den : ℚ) := by
    exact Nat.cast_div (entry_den_dvd A i j) (by exact_mod_cast (A i j).den_ne_zero)
  rw [he]
  conv_rhs => rw [← Rat.num_div_den (A i j)]
  ring

lemma integerMatrix_natAbs_le {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A B) (i j : Fin n) :
    (integerMatrix A i j).natAbs ≤ 2 ^ (B+n*n*B) := by
  simp only [integerMatrix, Int.natAbs_mul, Int.natAbs_natCast, pow_add]
  exact Nat.mul_le_mul (hA i j).1.le
    ((Nat.div_le_self _ _).trans (matrixDenominator_le hA))

lemma integer_det_natAbs_le {n K : ℕ} {A : Matrix (Fin n) (Fin n) ℤ}
    (hA : ∀ i j, (A i j).natAbs ≤ 2 ^ K) :
    A.det.natAbs ≤ 2^(n*n+n*K) := by
  have ht (σ : Equiv.Perm (Fin n)) :
      (((Equiv.Perm.sign σ : ℤ) * ∏ i, A (σ i) i)).natAbs ≤ 2^(n*K) := by
    have hu : (Equiv.Perm.sign σ : ℤ).natAbs = 1 := by
      rcases Int.units_eq_one_or (Equiv.Perm.sign σ) with h | h <;> simp [h]
    simp only [Int.natAbs_mul, hu, one_mul]
    rw [show (∏ i, A (σ i) i).natAbs = ∏ i, (A (σ i) i).natAbs from map_prod Int.natAbsHom _ _]
    calc
      ∏ i, (A (σ i) i).natAbs ≤ ∏ _i : Fin n, 2^K :=
        Finset.prod_le_prod' (fun i _ => hA _ _)
      _ = 2^(n*K) := by simp [← pow_mul, Nat.mul_comm]
  have hf : n.factorial ≤ 2^(n*n) := by
    calc
      n.factorial ≤ n^n := Nat.factorial_le_pow n
      _ ≤ (2^n)^n := Nat.pow_le_pow_left (Nat.le_of_lt n.lt_two_pow_self) n
      _ = 2^(n*n) := by rw [pow_mul]
  rw [Matrix.det_apply']
  calc
    (∑ σ : Equiv.Perm (Fin n), (Equiv.Perm.sign σ : ℤ) * ∏ i, A (σ i) i).natAbs
        ≤ ∑ σ : Equiv.Perm (Fin n),
            ((Equiv.Perm.sign σ : ℤ) * ∏ i, A (σ i) i).natAbs := Int.natAbs_sum_le _ _
    _ ≤ ∑ _σ : Equiv.Perm (Fin n), 2^(n*K) := Finset.sum_le_sum (fun σ _ => ht σ)
    _ = n.factorial * 2^(n*K) := by simp [Fintype.card_perm]
    _ ≤ 2^(n*n) * 2^(n*K) := Nat.mul_le_mul_right _ hf
    _ = 2^(n*n+n*K) := (pow_add _ _ _).symm

/-- This polynomial works with varying matrix order; no factorial occurs. -/
def polynomialDeterminantBits (n B : ℕ) : ℕ := 1+n*n+n*(B+n*n*B)

/-- Exact rational reconstruction from the determinant of the cleared matrix. -/
lemma det_eq_integerMatrix_div {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    A.det = ((integerMatrix A).det : ℚ) / (matrixDenominator A : ℚ)^n := by
  have hD : matrixDenominator A ≠ 0 := ne_of_gt (matrixDenominator_pos A)
  have hh := congrArg Matrix.det (integerMatrix_cast A)
  have hm := (Int.castRingHom ℚ).map_det (integerMatrix A)
  change ((integerMatrix A).det : ℚ) = ((integerMatrix A).map (Int.castRingHom ℚ)).det at hm
  rw [← hm, Matrix.det_smul] at hh
  simp only [Fintype.card_fin] at hh
  exact (eq_div_iff (pow_ne_zero _ (by exact_mod_cast hD))).mpr
    (by simpa [mul_comm] using hh.symm)

lemma matrixBits_det_polynomial {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A B) : RationalBits A.det (polynomialDeterminantBits n B) := by
  have hD : matrixDenominator A ≠ 0 := ne_of_gt (matrixDenominator_pos A)
  rw [det_eq_integerMatrix_div A]
  have hn := integer_det_natAbs_le (integerMatrix_natAbs_le hA)
  have hd : (matrixDenominator A)^n ≤ 2^(n*(n*n*B)) := by
    calc
      (matrixDenominator A)^n ≤ (2^(n*n*B))^n := Nat.pow_le_pow_left (matrixDenominator_le hA) n
      _ = 2^(n*(n*n*B)) := by rw [← pow_mul]; congr 1; ring
  have hp : n*(n*n*B) ≤ n*n+n*(B+n*n*B) := by nlinarith
  have hs (a : ℕ) : 2^a < 2^(1+a) := by rw [pow_add]; simp
  have hnum : (integerMatrix A).det.natAbs < 2^(polynomialDeterminantBits n B) :=
    hn.trans_lt (by simpa [polynomialDeterminantBits, Nat.add_assoc] using hs (n*n+n*(B+n*n*B)))
  have hden : (matrixDenominator A)^n < 2^(polynomialDeterminantBits n B) :=
    (hd.trans (Nat.pow_le_pow_right (by decide) hp)).trans_lt
      (by simpa [polynomialDeterminantBits, Nat.add_assoc] using hs (n*n+n*(B+n*n*B)))
  simpa only [Int.cast_pow, Int.cast_natCast, Int.natAbs_pow, Int.natAbs_natCast] using
    rationalBits_fraction (n := (integerMatrix A).det) (d := (matrixDenominator A : ℤ)^n)
      (pow_ne_zero _ (by exact_mod_cast hD)) hnum (by simpa using hden)

lemma polynomialDeterminantBits_mono (n : ℕ) {B C : ℕ} (h : B ≤ C) :
    polynomialDeterminantBits n B ≤ polynomialDeterminantBits n C := by
  unfold polynomialDeterminantBits
  gcongr

lemma polynomialDeterminantBits_le (n B : ℕ) :
    polynomialDeterminantBits n B ≤ (n+1)^3 * (B+1) := by
  unfold polynomialDeterminantBits
  nlinarith [Nat.zero_le (n*n*B), Nat.zero_le (n*B), Nat.zero_le (n*n*n)]

lemma matrixBits_adjugate_polynomial {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A B) : MatrixBits A.adjugate (polynomialDeterminantBits n (B+1)) := by
  intro i j
  rw [Matrix.adjugate_apply]
  apply matrixBits_det_polynomial
  intro k l
  by_cases hk : k = j
  · subst k
    simp only [Matrix.updateRow_self, Pi.single_apply]
    split_ifs
    · exact rationalBits_mono rationalBits_one (by omega)
    · exact rationalBits_mono rationalBits_zero (by omega)
  · rw [Matrix.updateRow_ne hk]
    exact rationalBits_mono (hA _ _) (by omega)

/-- The inverse output has a polynomial encoding even for variable order.
This lemma does not assert a running time for the adjugate definition. -/
lemma matrixBits_inverse_polynomial {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A B) : MatrixBits A⁻¹ (2*polynomialDeterminantBits n (B+1)) := by
  intro i j
  rw [Matrix.inv_def]
  simp only [Ring.inverse_eq_inv, Matrix.smul_apply, smul_eq_mul]
  have hd := rationalBits_inv (matrixBits_det_polynomial hA)
  have ha := matrixBits_adjugate_polynomial hA i j
  apply rationalBits_mono (rationalBits_mul hd ha)
  have hm := polynomialDeterminantBits_mono n (Nat.le_succ B)
  simp only [Nat.succ_eq_add_one] at hm
  omega

end MatroidSpectral
