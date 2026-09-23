import Mathlib

/-! Integer cofactor cancellation certificates and primitive normalization. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators

/-- Prepending a zero column makes the rectangular support matrix square. -/
def paddedMatrix {s : ℕ} (A : Matrix (Fin (s + 1)) (Fin s) ℤ) :
    Matrix (Fin (s + 1)) (Fin (s + 1)) ℤ :=
  fun i => Fin.cases 0 (A i)

/-- Signed maximal row minors of a matrix with one more row than column. -/
def cofactorVector {s : ℕ} (A : Matrix (Fin (s + 1)) (Fin s) ℤ) (i : Fin (s + 1)) : ℤ :=
  (-1) ^ (i : ℕ) * (A.submatrix i.succAbove id).det

theorem cofactorVector_eq_adjugate {s : ℕ}
    (A : Matrix (Fin (s + 1)) (Fin s) ℤ) (i : Fin (s + 1)) :
    cofactorVector A i = (paddedMatrix A).adjugate 0 i := by
  rw [Matrix.adjugate_fin_succ_eq_det_submatrix]
  simp [cofactorVector, paddedMatrix, Matrix.submatrix]

/-- Laplace cofactors cancel each column of the original rectangular matrix. -/
theorem cofactorVector_cancels {s : ℕ}
    (A : Matrix (Fin (s + 1)) (Fin s) ℤ) (j : Fin s) :
    ∑ i, cofactorVector A i * A i j = 0 := by
  have h := congrFun (congrFun (Matrix.adjugate_mul (paddedMatrix A)) 0) j.succ
  simpa [Matrix.mul_apply, ← cofactorVector_eq_adjugate, paddedMatrix,
    Matrix.one_apply, Fin.succ_ne_zero, eq_comm] using h

theorem cofactorVector_natAbs {s : ℕ}
    (A : Matrix (Fin (s + 1)) (Fin s) ℤ) (i : Fin (s + 1)) :
    (cofactorVector A i).natAbs = (A.submatrix i.succAbove id).det.natAbs := by
  simp [cofactorVector, Int.natAbs_mul, Int.natAbs_pow]

theorem cofactorVector_ne_zero {s : ℕ}
    (A : Matrix (Fin (s + 1)) (Fin s) ℤ) (i : Fin (s + 1))
    (hi : (A.submatrix i.succAbove id).det ≠ 0) : cofactorVector A i ≠ 0 := by
  exact mul_ne_zero (pow_ne_zero _ (by norm_num)) hi

/-- Cancellation extends to every column represented in the selected column span. -/
theorem cofactorVector_cancels_span {s : ℕ} {J : Type*}
    (A : Matrix (Fin (s + 1)) (Fin s) ℤ)
    (B : Matrix (Fin (s + 1)) J ℚ) (coeff : Fin s → J → ℚ)
    (hspan : ∀ i j, B i j = ∑ k, (A i k : ℚ) * coeff k j) (j : J) :
    ∑ i, (cofactorVector A i : ℚ) * B i j = 0 := by
  simp_rw [hspan, Finset.mul_sum]
  rw [Finset.sum_comm]
  have hc (k : Fin s) : (∑ i, (cofactorVector A i : ℚ) * (A i k : ℚ)) = 0 := by
    exact_mod_cast cofactorVector_cancels A k
  simp_rw [← mul_assoc, ← Finset.sum_mul, hc, zero_mul]
  simp

/-- Primitive natural weights obtained by dividing by their common divisor. -/
def primitiveWeights {I : Type*} [Fintype I] (w : I → ℕ) (i : I) : ℕ :=
  w i / Finset.univ.gcd w

theorem primitiveWeights_gcd {I : Type*} [Fintype I] (w : I → ℕ)
    (hw : ∃ i, w i ≠ 0) : Finset.univ.gcd (primitiveWeights w) = 1 := by
  classical
  obtain ⟨i, hi⟩ := hw
  exact Finset.gcd_div_eq_one (Finset.mem_univ i) hi

theorem primitiveWeights_le {I : Type*} [Fintype I] (w : I → ℕ) (i : I) :
    primitiveWeights w i ≤ w i := Nat.div_le_self _ _

theorem primitiveWeights_mul_gcd {I : Type*} [Fintype I] (w : I → ℕ) (i : I) :
    primitiveWeights w i * Finset.univ.gcd w = w i := by
  classical
  exact Nat.div_mul_cancel (Finset.gcd_dvd (Finset.mem_univ i))

theorem primitiveWeights_pos {I : Type*} [Fintype I] (w : I → ℕ) (i : I)
    (hi : 0 < w i) : 0 < primitiveWeights w i := by
  have h := primitiveWeights_mul_gcd w i
  exact Nat.pos_of_mul_pos_right (h ▸ hi)

/-- Dividing an integer cancellation certificate by the common divisor preserves cancellation. -/
theorem primitiveWeights_cancels {I J : Type*} [Fintype I]
    (w : I → ℕ) (A : I → J → ℤ) (hw : ∃ i, w i ≠ 0)
    (hc : ∀ j, ∑ i, (w i : ℤ) * A i j = 0) (j : J) :
    ∑ i, (primitiveWeights w i : ℤ) * A i j = 0 := by
  classical
  have hg : Finset.univ.gcd w ≠ 0 := by
    intro hg
    obtain ⟨i, hi⟩ := hw
    have he := primitiveWeights_mul_gcd w i
    rw [hg, mul_zero] at he
    exact hi he.symm
  have h : (∑ i, (primitiveWeights w i : ℤ) * A i j) *
      ((Finset.univ.gcd w : ℕ) : ℤ) = 0 := by
    rw [Finset.sum_mul]
    calc
      _ = ∑ i, (w i : ℤ) * A i j := by
        apply Finset.sum_congr rfl
        intro i _
        have he : (primitiveWeights w i : ℤ) * ((Finset.univ.gcd w : ℕ) : ℤ) = w i := by
          exact_mod_cast primitiveWeights_mul_gcd w i
        calc
          _ = ((primitiveWeights w i : ℤ) * ((Finset.univ.gcd w : ℕ) : ℤ)) * A i j := by ring
          _ = _ := by rw [he]
      _ = 0 := hc j
  exact (mul_eq_zero.mp h).resolve_right (by exact_mod_cast hg)

end NetworkSimplex.Threshold
