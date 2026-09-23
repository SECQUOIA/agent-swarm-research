import Mathlib

open scoped BigOperators Matrix
open Matrix

namespace QipmFormal.Preconditioner

/-- Grounded unsigned path incidence, with the root first. -/
def pathIncidence (m : ℕ) : Matrix (Fin m) (Fin m) ℝ :=
  fun i j => (if i = j then 1 else 0) - (if i.val = j.val + 1 then 1 else 0)

/-- The normal matrix of the grounded path incidence. -/
def pathMatrix (m : ℕ) : Matrix (Fin m) (Fin m) ℝ :=
  pathIncidence m * (pathIncidence m)ᵀ

def pathDifference {m : ℕ} (x : Fin m → ℝ) (i : Fin m) : ℝ :=
  x i - if h : i.val + 1 < m then x ⟨i.val + 1, h⟩ else 0

def pathEnergy {m : ℕ} (x : Fin m → ℝ) : ℝ := ∑ i, (pathDifference x i)^2

def alternatingSign {m : ℕ} (i : Fin m) : ℝ := (-1) ^ i.val

def alternatingMatrix (m : ℕ) : Matrix (Fin m) (Fin m) ℝ :=
  Matrix.diagonal alternatingSign

def pathRamp (m : ℕ) (i : Fin m) : ℝ := (m : ℝ) - i.val

lemma pathIncidence_transpose_mulVec {m : ℕ} (x : Fin m → ℝ) :
    (pathIncidence m)ᵀ *ᵥ x = pathDifference x := by
  ext i
  simp only [mulVec, dotProduct, transpose_apply, pathIncidence, sub_mul, Finset.sum_sub_distrib]
  have hdiag : (∑ j : Fin m, (if j = i then (1 : ℝ) else 0) * x j) = x i := by simp
  rw [hdiag]
  unfold pathDifference
  congr 1
  split_ifs with h
  · rw [Finset.sum_eq_single (⟨i.val + 1, h⟩ : Fin m)]
    · simp
    · intro j _ hj
      have hne : j.val ≠ i.val + 1 := fun he => hj (Fin.ext he)
      simp [hne]
    · simp
  · apply Finset.sum_eq_zero
    intro j _
    have hne : j.val ≠ i.val + 1 := by omega
    simp [hne]

lemma pathMatrix_quadratic {m : ℕ} (x : Fin m → ℝ) :
    x ⬝ᵥ (pathMatrix m *ᵥ x) = pathEnergy x := by
  unfold pathMatrix
  rw [← mulVec_mulVec]
  rw [← dotProduct_transpose_mulVec]
  simp only [pathIncidence_transpose_mulVec, pathEnergy, dotProduct, pow_two]

lemma pathRamp_difference (m : ℕ) (i : Fin m) :
    pathDifference (pathRamp m) i = 1 := by
  unfold pathDifference pathRamp
  split_ifs with h
  · simp only [Nat.cast_add, Nat.cast_one]
    ring
  · have hi : i.val + 1 = m := by omega
    have hi' : (i.val : ℝ) + 1 = m := by exact_mod_cast hi
    linarith

lemma pathRamp_energy (m : ℕ) : pathEnergy (pathRamp m) = m := by
  simp [pathEnergy, pathRamp_difference]

lemma pathRamp_ne_zero {m : ℕ} (hm : 0 < m) : pathRamp m ≠ 0 := by
  intro h
  have hz := congrFun h (⟨0, hm⟩ : Fin m)
  have hm' : (0 : ℝ) < m := by exact_mod_cast hm
  simp [pathRamp] at hz
  linarith

lemma alternatingSign_sq {m : ℕ} (i : Fin m) : alternatingSign i ^ 2 = 1 := by
  unfold alternatingSign
  rw [← pow_mul, Nat.mul_comm, pow_mul]
  norm_num

lemma alternatingMatrix_mulVec {m : ℕ} (x : Fin m → ℝ) :
    alternatingMatrix m *ᵥ x = fun i => alternatingSign i * x i := by
  ext i
  simp [alternatingMatrix, mulVec_diagonal]

lemma alternatingMatrix_sq (m : ℕ) : alternatingMatrix m * alternatingMatrix m = 1 := by
  rw [alternatingMatrix, diagonal_mul_diagonal]
  ext i j
  simp [← pow_two, alternatingSign_sq]

lemma alternatingMatrix_transpose (m : ℕ) : (alternatingMatrix m)ᵀ = alternatingMatrix m := by
  simp [alternatingMatrix]

lemma alternating_pathRamp_difference_sq (m : ℕ) (i : Fin m) :
    (pathDifference (alternatingMatrix m *ᵥ pathRamp m) i)^2 =
      (2 * ((m : ℝ) - i.val) - 1)^2 := by
  rw [alternatingMatrix_mulVec]
  unfold pathDifference
  split_ifs with h
  · simp only [alternatingSign, pathRamp, Nat.cast_add, Nat.cast_one, pow_add, pow_one]
    calc
      _ = ((-1 : ℝ)^i.val * (2 * ((m : ℝ) - i.val) - 1))^2 := by congr 1; ring
      _ = _ := by rw [mul_pow, show ((-1 : ℝ)^i.val)^2 = 1 from alternatingSign_sq i, one_mul]
  · have hi : i.val + 1 = m := by omega
    have hi' : (i.val : ℝ) + 1 = m := by exact_mod_cast hi
    have hr : pathRamp m i = 1 := by unfold pathRamp; linarith
    simp only [sub_zero, hr, mul_one, alternatingSign_sq]
    rw [show (m : ℝ) - i.val = 1 by linarith]
    norm_num

lemma sum_odd_squares (m : ℕ) :
    (∑ i : Fin m, (2 * ((m : ℝ) - i.val) - 1)^2) =
      (m : ℝ) * (4 * (m : ℝ)^2 - 1) / 3 := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [Fin.sum_univ_succ]
    simp only [Fin.val_zero, Fin.val_succ, Nat.cast_add, Nat.cast_one]
    have heq : (∑ i : Fin m, (2 * ((m : ℝ) + 1 - ((i.val : ℝ) + 1)) - 1)^2) =
        ∑ i : Fin m, (2 * ((m : ℝ) - i.val) - 1)^2 := by
      apply Finset.sum_congr rfl
      intro i _
      congr 1
      ring
    rw [heq, ih]
    ring

lemma alternating_pathRamp_energy (m : ℕ) :
    pathEnergy (alternatingMatrix m *ᵥ pathRamp m) =
      (m : ℝ) * (4 * (m : ℝ)^2 - 1) / 3 := by
  simp only [pathEnergy, alternating_pathRamp_difference_sq, sum_odd_squares]

lemma pathIncidence_det (m : ℕ) : (pathIncidence m).det = 1 := by
  have htri : (pathIncidence m).IsLowerTriangular := by
    intro i j hij
    have hijval : i.val < j.val := hij
    have hij' : i ≠ j := by exact ne_of_lt hij
    have hnext : i.val ≠ j.val + 1 := by omega
    simp [pathIncidence, hij', hnext]
  rw [det_of_isLowerTriangular _ htri]
  simp [pathIncidence]

lemma pathIncidence_isUnit (m : ℕ) : IsUnit (pathIncidence m) := by
  rw [isUnit_iff_isUnit_det, pathIncidence_det]
  exact isUnit_one

lemma pathMatrix_posDef (m : ℕ) : (pathMatrix m).PosDef := by
  have h := (pathIncidence_isUnit m).posDef_star_right_conjugate_iff.mpr
    (show (1 : Matrix (Fin m) (Fin m) ℝ).PosDef from Matrix.PosDef.one)
  simpa [pathMatrix, star_eq_conjTranspose, conjTranspose_eq_transpose_of_trivial] using h

lemma alternating_pathRamp_energy_lower {m : ℕ} (hm : 1 ≤ m) :
    (m : ℝ)^3 ≤ pathEnergy (alternatingMatrix m *ᵥ pathRamp m) := by
  rw [alternating_pathRamp_energy]
  have hm' : (1 : ℝ) ≤ m := by exact_mod_cast hm
  have hsq : (1 : ℝ) ≤ (m : ℝ)^2 := by nlinarith
  nlinarith [mul_nonneg (show (0 : ℝ) ≤ m by positivity) (sub_nonneg.mpr hsq)]

lemma alternatingMatrix_orthogonal (m : ℕ) :
    (alternatingMatrix m)ᵀ * alternatingMatrix m = 1 := by
  rw [alternatingMatrix_transpose, alternatingMatrix_sq]

/-- Incidence matrix whose edges all have negative sign; the grounded root remains +1. -/
def negativePathIncidence (m : ℕ) : Matrix (Fin m) (Fin m) ℝ :=
  fun i j => (if i = j then 1 else 0) + (if i.val = j.val + 1 then 1 else 0)

lemma alternating_pathIncidence (m : ℕ) :
    alternatingMatrix m * pathIncidence m * alternatingMatrix m = negativePathIncidence m := by
  ext i j
  simp only [alternatingMatrix, mul_diagonal, diagonal_mul, pathIncidence, negativePathIncidence]
  by_cases hij : i = j
  · subst j
    simp [← pow_two, alternatingSign_sq]
  · by_cases hnext : i.val = j.val + 1
    · have hsign : alternatingSign i = - alternatingSign j := by
        simp [alternatingSign, hnext, pow_succ]
      simp [hij, hnext, hsign, ← pow_two, alternatingSign_sq]
    · simp [hij, hnext]

lemma alternating_pathMatrix (m : ℕ) :
    alternatingMatrix m * pathMatrix m * alternatingMatrix m =
      negativePathIncidence m * (negativePathIncidence m)ᵀ := by
  rw [← alternating_pathIncidence, transpose_mul, transpose_mul,
    alternatingMatrix_transpose]
  simp only [pathMatrix]
  simp only [Matrix.mul_assoc]
  rw [← Matrix.mul_assoc (alternatingMatrix m) (alternatingMatrix m), alternatingMatrix_sq, one_mul]

end QipmFormal.Preconditioner
