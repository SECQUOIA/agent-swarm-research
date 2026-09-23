import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Tactic

/-! Exact scalar-pivot elimination for symmetric quadratic forms. -/
namespace CertifiedMinlp.QuadraticElimination

open scoped BigOperators

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

/-- The ordinary matrix quadratic form, written as a double finite sum. -/
def value {n : ℕ} (M : Matrix (Fin n) (Fin n) K) (x : Fin n → K) : K :=
  ∑ i, ∑ j, M i j * x i * x j

/-- Nonnegativity of the actual quadratic form at every vector. -/
def Nonnegative {n : ℕ} (M : Matrix (Fin n) (Fin n) K) : Prop :=
  ∀ x, 0 ≤ value M x

def tail {n : ℕ} (M : Matrix (Fin (n + 1)) (Fin (n + 1)) K) :
    Matrix (Fin n) (Fin n) K := fun i j => M i.succ j.succ

def rowValue {n : ℕ} (M : Matrix (Fin (n + 1)) (Fin (n + 1)) K)
    (x : Fin n → K) : K := ∑ j, M 0 j.succ * x j

def schur {n : ℕ} (M : Matrix (Fin (n + 1)) (Fin (n + 1)) K) :
    Matrix (Fin n) (Fin n) K :=
  fun i j => M i.succ j.succ - M 0 i.succ * M 0 j.succ / M 0 0

omit [LinearOrder K] [IsStrictOrderedRing K] in
lemma value_cons {n : ℕ} (M : Matrix (Fin (n + 1)) (Fin (n + 1)) K)
    (hs : M.IsSymm) (t : K) (x : Fin n → K) :
    value M (Fin.cons t x) =
      M 0 0 * t ^ 2 + 2 * t * rowValue M x + value (tail M) x := by
  have hsym (i j) : M i j = M j i := hs.apply j i
  simp only [value, Fin.sum_univ_succ, Fin.cons_zero, Fin.cons_succ, tail]
  rw [Finset.sum_add_distrib]
  simp_rw [hsym _ 0]
  simp only [rowValue, Finset.mul_sum]
  ring_nf
  rw [Finset.sum_mul]
  ring

lemma value_schur {n : ℕ} (M : Matrix (Fin (n + 1)) (Fin (n + 1)) K)
    (x : Fin n → K) :
    value (schur M) x = value (tail M) x - (rowValue M x) ^ 2 / M 0 0 := by
  simp only [value, schur, tail, sub_mul, Finset.sum_sub_distrib]
  congr 1
  simp only [rowValue, pow_two, Finset.sum_mul, Finset.mul_sum, Finset.sum_div]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  ring

lemma square_completion {n : ℕ} (M : Matrix (Fin (n + 1)) (Fin (n + 1)) K)
    (hs : M.IsSymm) (hp : M 0 0 ≠ 0) (t : K) (x : Fin n → K) :
    value M (Fin.cons t x) =
      M 0 0 * (t + rowValue M x / M 0 0) ^ 2 + value (schur M) x := by
  rw [value_cons M hs, value_schur]
  field_simp
  ring

omit [Field K] [LinearOrder K] [IsStrictOrderedRing K] in
lemma tail_symmetric {n : ℕ} {M : Matrix (Fin (n + 1)) (Fin (n + 1)) K}
    (hs : M.IsSymm) : (tail M).IsSymm := by
  ext i j
  exact hs.apply _ _

lemma schur_symmetric {n : ℕ} {M : Matrix (Fin (n + 1)) (Fin (n + 1)) K}
    (hs : M.IsSymm) : (schur M).IsSymm := by
  ext i j
  simp only [Matrix.transpose_apply, schur, hs.apply j.succ i.succ]
  ring

/-- A strictly positive pivot reduces nonnegativity exactly to its Schur complement. -/
theorem positive_pivot_iff {n : ℕ}
    (M : Matrix (Fin (n + 1)) (Fin (n + 1)) K) (hs : M.IsSymm)
    (hp : 0 < M 0 0) : Nonnegative M ↔ Nonnegative (schur M) := by
  constructor
  · intro h x
    have htest := h (Fin.cons (-rowValue M x / M 0 0) x)
    rw [square_completion M hs (ne_of_gt hp)] at htest
    simpa [neg_div] using htest
  · intro h x
    rw [← Fin.cons_self_tail x, square_completion M hs (ne_of_gt hp)]
    exact add_nonneg (mul_nonneg hp.le (sq_nonneg _)) (h _)

omit [IsStrictOrderedRing K] in
lemma diagonal_nonnegative {n : ℕ}
    {M : Matrix (Fin n) (Fin n) K} (h : Nonnegative M) (i : Fin n) : 0 ≤ M i i := by
  have ht := h (Pi.single i 1)
  simpa [value, Pi.single_apply] using ht

omit [IsStrictOrderedRing K] in
/-- A negative diagonal entry supplies a rejecting coordinate vector. -/
theorem negative_diagonal_rejects {n : ℕ}
    {M : Matrix (Fin n) (Fin n) K} (i : Fin n) (hi : M i i < 0) : ¬ Nonnegative M := by
  exact fun h => (not_lt_of_ge (diagonal_nonnegative h i)) hi

/-- A zero pivot in a nonnegative symmetric form forces every off-diagonal
entry in the pivot row to vanish. -/
theorem zero_pivot_row {n : ℕ}
    (M : Matrix (Fin (n + 1)) (Fin (n + 1)) K) (hs : M.IsSymm)
    (hp : M 0 0 = 0) (h : Nonnegative M) (i : Fin n) : M 0 i.succ = 0 := by
  by_contra hr
  let d := M i.succ i.succ
  let b := M 0 i.succ
  have hb : b ≠ 0 := hr
  have ht := h (Fin.cons (-(d + 1) / (2 * b)) (Pi.single i 1))
  rw [value_cons M hs] at ht
  have hv : value (tail M) (Pi.single i 1) = d := by
    simp [value, tail, Pi.single_apply, d]
  have hrw : rowValue M (Pi.single i 1) = b := by
    simp [rowValue, Pi.single_apply, b]
  rw [hp, hv, hrw] at ht
  have he : 2 * (-(d + 1) / (2 * b)) * b = -(d + 1) := by
    field_simp
  rw [he] at ht
  simp only [zero_mul, zero_add] at ht
  linarith

/-- Deletion of an identically zero pivot row and column preserves the exact form. -/
theorem zero_pivot_iff {n : ℕ}
    (M : Matrix (Fin (n + 1)) (Fin (n + 1)) K) (hs : M.IsSymm)
    (hp : M 0 0 = 0) :
    Nonnegative M ↔ (∀ i : Fin n, M 0 i.succ = 0) ∧ Nonnegative (tail M) := by
  constructor
  · intro h
    refine ⟨zero_pivot_row M hs hp h, fun x => ?_⟩
    have ht := h (Fin.cons 0 x)
    simpa [value_cons M hs, hp] using ht
  · rintro ⟨hr, h⟩ x
    rw [← Fin.cons_self_tail x, value_cons M hs, hp]
    have hz : rowValue M (Fin.tail x) = 0 := by simp [rowValue, hr]
    rw [hz]
    simpa using h (Fin.tail x)

/-- Exact rational-arithmetic PSD elimination, with a fixed first-coordinate pivot.
The same definition over another ordered field supports the semantic proof. -/
def check : (n : ℕ) → Matrix (Fin n) (Fin n) K → Bool
  | 0, _ => true
  | n + 1, M =>
    if M 0 0 < 0 then false
    else if M 0 0 = 0 then
      decide (∀ i : Fin n, M 0 i.succ = 0) && check n (tail M)
    else check n (schur M)

/-- The executable elimination test is sound and complete for symmetric matrices. -/
theorem check_iff : ∀ (n : ℕ) (M : Matrix (Fin n) (Fin n) K),
    M.IsSymm → (check n M = true ↔ Nonnegative M) := by
  intro n
  induction n with
  | zero =>
    intro M hs
    simp [check, Nonnegative, value]
  | succ n ih =>
    intro M hs
    by_cases hn : M 0 0 < 0
    · simp [check, hn, negative_diagonal_rejects 0 hn]
    · by_cases hz : M 0 0 = 0
      · simpa only [check, hn, hz, lt_self_iff_false, ↓reduceIte,
          Bool.and_eq_true, decide_eq_true_eq,
          ih (tail M) (tail_symmetric hs)] using (zero_pivot_iff M hs hz).symm
      · have hp : 0 < M 0 0 := lt_of_le_of_ne (le_of_not_gt hn) (Ne.symm hz)
        simpa only [check, hn, hz, ↓reduceIte, ih (schur M) (schur_symmetric hs)] using
          (positive_pivot_iff M hs hp).symm

/-- Coefficientwise interpretation of a rational matrix in the real numbers. -/
def realMatrix {n : ℕ} (M : Matrix (Fin n) (Fin n) ℚ) : Matrix (Fin n) (Fin n) ℝ :=
  fun i j => M i j

lemma realMatrix_tail {n : ℕ} (M : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) :
    realMatrix (tail M) = tail (realMatrix M) := rfl

lemma realMatrix_schur {n : ℕ} (M : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) :
    realMatrix (schur M) = schur (realMatrix M) := by
  ext i j
  simp [realMatrix, schur]

lemma realMatrix_symmetric {n : ℕ} {M : Matrix (Fin n) (Fin n) ℚ}
    (hs : M.IsSymm) : (realMatrix M).IsSymm := by
  ext i j
  simp only [Matrix.transpose_apply, realMatrix, hs.apply i j]

/-- Every comparison and Schur operation in the rational checker agrees exactly
with its real interpretation; there is no floating-point or tolerance premise. -/
theorem check_realMatrix : ∀ (n : ℕ) (M : Matrix (Fin n) (Fin n) ℚ),
    check n (realMatrix M) = check n M := by
  intro n
  induction n with
  | zero => intro M; rfl
  | succ n ih =>
    intro M
    have hn : (realMatrix M) 0 0 < 0 ↔ M 0 0 < 0 := by
      simp [realMatrix]
    have hz : (realMatrix M) 0 0 = 0 ↔ M 0 0 = 0 := by
      simp [realMatrix]
    have hr : (∀ i : Fin n, (realMatrix M) 0 i.succ = 0) ↔
        (∀ i : Fin n, M 0 i.succ = 0) := by simp [realMatrix]
    simp only [check, hn, hz, hr, ← realMatrix_tail, ← realMatrix_schur, ih]

/-- Rational elimination decides nonnegativity on all real vectors. -/
theorem rational_check_iff_real_nonnegative {n : ℕ} (M : Matrix (Fin n) (Fin n) ℚ)
    (hs : M.IsSymm) : check n M = true ↔ Nonnegative (realMatrix M) := by
  rw [← check_realMatrix]
  exact check_iff n _ (realMatrix_symmetric hs)

/-- For a symmetric rational quadratic form, testing rational vectors and testing
all real vectors give exactly the same condition. -/
theorem rational_nonnegative_iff_real {n : ℕ} (M : Matrix (Fin n) (Fin n) ℚ)
    (hs : M.IsSymm) : Nonnegative M ↔ Nonnegative (realMatrix M) := by
  rw [← check_iff n M hs, rational_check_iff_real_nonnegative M hs]

/-- A rank-one matrix exercises a positive pivot followed by a zero pivot. -/
example : check 2 (!![(1 : ℚ), 1; 1, 1]) = true := by
  norm_num [check, schur, tail, Fin.forall_fin_succ]

/-- A zero diagonal with a nonzero off-diagonal entry must be rejected. -/
example : check 2 (!![(0 : ℚ), 1; 1, 0]) = false := by
  norm_num [check, schur, tail, Fin.forall_fin_succ]

/-- A negative Schur pivot is rejected even when the original diagonal is positive. -/
example : check 2 (!![(1 : ℚ), 2; 2, 1]) = false := by
  norm_num [check, schur, tail, Fin.forall_fin_succ]

end CertifiedMinlp.QuadraticElimination
