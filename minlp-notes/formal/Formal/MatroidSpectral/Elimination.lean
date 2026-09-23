import Mathlib.LinearAlgebra.Matrix.Determinant.Bird.Correctness
import Mathlib.Algebra.Ring.Parity
import Mathlib.Tactic

/-! A cached, division-free determinant algorithm. The recurrence is Bird's;
each complete matrix is stored before the next step. The counter records ring
additions, multiplications, and negations, not machine instructions. -/
namespace MatroidSpectral.Elimination
open Matrix
open scoped BigOperators
variable {R : Type*} [CommRing R]

structure ScalarRun (R : Type*) where
  value : R
  operations : ℕ
  operands : List (R × R) := []

def atom (x : R) : ScalarRun R := ⟨x, 0, []⟩
def add (x y : ScalarRun R) : ScalarRun R :=
  ⟨x.value + y.value, x.operations + y.operations + 1,
    x.operands ++ y.operands ++ [(x.value, y.value)]⟩
def mul (x y : ScalarRun R) : ScalarRun R :=
  ⟨x.value * y.value, x.operations + y.operations + 1,
    x.operands ++ y.operands ++ [(x.value, y.value)]⟩
def neg (x : ScalarRun R) : ScalarRun R :=
  ⟨-x.value, x.operations + 1, x.operands ++ [(x.value, 0)]⟩

def sumRun : List (ScalarRun R) → ScalarRun R
  | [] => atom 0
  | x :: xs => add x (sumRun xs)

@[simp] theorem sumRun_value (xs : List (ScalarRun R)) :
    (sumRun xs).value = (xs.map ScalarRun.value).sum := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp [sumRun, add, ih]

@[simp] theorem sumRun_operations (xs : List (ScalarRun R)) :
    (sumRun xs).operations = (xs.map ScalarRun.operations).sum + xs.length := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp [sumRun, add, ih]; omega

abbrev StoredMatrix (R : Type*) (n : ℕ) := Vector (Vector R n) n

def store {n : ℕ} (A : Matrix (Fin n) (Fin n) R) : StoredMatrix R n :=
  Vector.ofFn fun i => Vector.ofFn (A i)

def view {n : ℕ} (A : StoredMatrix R n) : Matrix (Fin n) (Fin n) R :=
  fun i j => A[i.val][j.val]

omit [CommRing R] in
@[simp] theorem view_store {n : ℕ} (A : Matrix (Fin n) (Fin n) R) :
    view (store A) = A := by ext i j; simp [view, store]

/-- Zero terms outside the strict upper triangle retain their arithmetic charge. -/
def entryRun {n : ℕ} (A F : StoredMatrix R n) (i j : Fin n) : ScalarRun R :=
  add (mul (neg (sumRun (List.ofFn fun k : Fin n =>
    atom (if i < k then view F k k else 0)))) (atom (view A i j)))
    (sumRun (List.ofFn fun k : Fin n =>
      mul (atom (if i < k then view F i k else 0)) (atom (view A k j))))

@[simp] theorem entryRun_value {n : ℕ} (A F : StoredMatrix R n) (i j : Fin n) :
    (entryRun A F i j).value = BirdDet.Spec.stepEntry (view A) (view F) i j := by
  simp [entryRun, add, mul, neg, atom, BirdDet.Spec.stepEntry, List.map_ofFn,
    Function.comp_def, List.sum_ofFn, ← Finset.sum_filter, Finset.filter_lt_eq_Ioi]

@[simp] theorem entryRun_operations {n : ℕ} (A F : StoredMatrix R n) (i j : Fin n) :
    (entryRun A F i j).operations = 3 * n + 3 := by
  simp [entryRun, add, mul, neg, atom, List.map_ofFn, Function.comp_def, List.sum_ofFn]
  omega

structure MatrixRun (R : Type*) (n : ℕ) where
  matrix : StoredMatrix R n
  operations : ℕ
  operands : List (R × R) := []

/-- `results` stores each entry once, for both values and counters. -/
def stepRun {n : ℕ} (A F : StoredMatrix R n) : MatrixRun R n :=
  let results := Vector.ofFn fun i => Vector.ofFn fun j => entryRun A F i j
  ⟨results.map (fun row => row.map ScalarRun.value),
    ∑ i : Fin n, ∑ j : Fin n, results[i.val][j.val].operations,
    (List.ofFn fun i => (List.ofFn fun j => results[i.val][j.val].operands).flatten).flatten⟩

@[simp] theorem stepRun_value {n : ℕ} (A F : StoredMatrix R n) :
    view (stepRun A F).matrix = BirdDet.Spec.stepEntry (view A) (view F) := by
  ext i j
  simpa only [view, stepRun, Vector.getElem_map, Vector.getElem_ofFn] using
    entryRun_value A F i j

@[simp] theorem stepRun_operations {n : ℕ} (A F : StoredMatrix R n) :
    (stepRun A F).operations = n * n * (3 * n + 3) := by
  simp [stepRun, Nat.mul_assoc]

/-- Iteration stores the preceding matrix once and never recomputes it. -/
def iterateRun {n : ℕ} (A : StoredMatrix R n) : ℕ → MatrixRun R n
  | 0 => ⟨A, 0, []⟩
  | t + 1 =>
      let previous := iterateRun A t
      let next := stepRun A previous.matrix
      ⟨next.matrix, previous.operations + next.operations, previous.operands ++ next.operands⟩

@[simp] theorem iterateRun_value {n : ℕ} (A : StoredMatrix R n) (t : ℕ) :
    view (iterateRun A t).matrix = (BirdDet.Spec.stepEntry (view A))^[t] (view A) := by
  induction t with
  | zero => rfl
  | succ t ih => simp [iterateRun, ih, Function.iterate_succ_apply']

@[simp] theorem iterateRun_operations {n : ℕ} (A : StoredMatrix R n) (t : ℕ) :
    (iterateRun A t).operations = t * (n * n * (3 * n + 3)) := by
  induction t with
  | zero => simp [iterateRun]
  | succ t ih => simp [iterateRun, ih]; ring

/-- Parity computes the final sign without ring exponentiation. -/
def determinantRun : (n : ℕ) → StoredMatrix R n → ScalarRun R
  | 0, _ => atom 1
  | k + 1, A =>
      let result := iterateRun A k
      let x := view result.matrix 0 0
      ⟨if Even k then x else -x, result.operations + 1, result.operands ++ [(x, 0)]⟩

private theorem sumFrom_eq_sum_Ico {n lo : ℕ} (f : ℕ → R) :
    BirdDet.sumFrom n lo f = ∑ k ∈ Finset.Ico lo n, f k := by
  induction lo using BirdDet.sumFrom_induct n with
  | step lo hlo ih => rw [BirdDet.sumFrom_step n lo f hlo, ih,
      ← Finset.sum_eq_sum_Ico_succ_bot hlo f]
  | stop lo hlo => rw [BirdDet.sumFrom_stop n lo f hlo,
      Finset.Ico_eq_empty hlo, Finset.sum_empty]

private theorem sumFrom_fin_tail {n : ℕ} (i : Fin n) (f : ℕ → R) :
    BirdDet.sumFrom n (i.val + 1) f = ∑ k ∈ Finset.Ioi i, f k.val := by
  rw [sumFrom_eq_sum_Ico]
  calc
    _ = ∑ k ∈ (Finset.range n).filter (i.val < ·), f k := by congr; ext; aesop
    _ = ∑ k ∈ Finset.range n, if i.val < k then f k else 0 := by rw [Finset.sum_filter]
    _ = ∑ k : Fin n, if i.val < k.val then f k.val else 0 := by rw [← Fin.sum_univ_eq_sum_range]
    _ = _ := by simp [← Finset.sum_filter, Finset.filter_lt_eq_Ioi]

/-- Relates the public flat-array specification to the cached recurrence. -/
theorem birdSpec_correct {n : ℕ} (A : Matrix (Fin n) (Fin n) R) :
    BirdDet.Spec.birdDet A = A.det := by
  let a := Array.ofFn fun k : Fin (n * n) => A k.divNat k.modNat
  have ha : a.size = n * n := Array.size_ofFn
  have hview : Matrix.ofArray a ha = A := Matrix.ofArray_ofFn A
  have hiter (t : ℕ) (i j : Fin n) :
      ((BirdDet.stepEntry n a)^[t] (BirdDet.get n a)) i.val j.val =
        (BirdDet.Spec.stepEntry A)^[t] A i j := by
    induction t generalizing i j with
    | zero =>
        have hh := congrFun (congrFun hview i) j
        rw [Matrix.ofArray_eq_of_getD] at hh
        exact hh
    | succ t ih =>
        have hv (u v : Fin n) : BirdDet.get n a u.val v.val = A u v := by
          have hh := congrFun (congrFun hview u) v
          rw [Matrix.ofArray_eq_of_getD] at hh
          exact hh
        simp_rw [Function.iterate_succ_apply', BirdDet.stepEntry_eq,
          BirdDet.Spec.stepEntry_eq, sumFrom_fin_tail, ih, Matrix.of_apply, hv]
  have hd := BirdDet.det_eq_birdDet a ha
  rw [hview] at hd
  rw [hd]
  cases n with
  | zero => rfl
  | succ k =>
      simp only [BirdDet.Spec.birdDetSpec_succ, BirdDet.birdDet_succ]
      exact congrArg (fun x : R => (-1) ^ k * x) (hiter k 0 0).symm

theorem determinantRun_correct (n : ℕ) (A : StoredMatrix R n) :
    (determinantRun n A).value = (view A).det := by
  rw [← birdSpec_correct]
  cases n with
  | zero => rfl
  | succ k =>
      simp only [determinantRun, BirdDet.Spec.birdDetSpec_succ, neg_one_pow_eq_ite]
      rw [← iterateRun_value]
      split_ifs <;> simp

/-- A uniform polynomial bound with variable matrix dimension. Storage, index
work, and bit costs are separate from this ring arithmetic counter. -/
theorem determinantRun_operations_le (n : ℕ) (A : StoredMatrix R n) :
    (determinantRun n A).operations ≤ 4 * (n + 1) ^ 4 := by
  cases n with
  | zero => simp [determinantRun, atom]
  | succ k =>
      simp only [determinantRun, iterateRun_operations]
      nlinarith [sq_nonneg (k : ℤ)]

end MatroidSpectral.Elimination
