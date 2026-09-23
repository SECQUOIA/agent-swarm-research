import Formal.MatroidSpectral.Elimination
import Formal.MatroidSpectral.DeterminantBits

/-! Integer size bounds for the cached Bird recurrence and rational evaluation
by clearing one common denominator. -/
namespace MatroidSpectral.Elimination
open Matrix DAGSpectral ReciprocalAnchor
open scoped BigOperators

lemma integer_sum_bound {n M : ℕ} (s : Finset (Fin n)) {f : Fin n → ℤ}
    (hf : ∀ k ∈ s, (f k).natAbs ≤ M) : (∑ k ∈ s, f k).natAbs ≤ n*M := by
  calc
    (∑ k ∈ s, f k).natAbs ≤ ∑ k ∈ s, (f k).natAbs := Int.natAbs_sum_le _ _
    _ ≤ ∑ _k ∈ s, M := Finset.sum_le_sum (fun k hk => hf k hk)
    _ = s.card*M := by simp
    _ ≤ n*M := Nat.mul_le_mul_right _ (by simpa using Finset.card_le_univ s)

/-- Includes every partial sum actually formed by `sumRun`, not just the final
sum. Lists need not be duplicate-free. -/
lemma sumRun_int_bound {P : ℕ} (xs : List (ScalarRun ℤ))
    (hx : ∀ x ∈ xs, x.value.natAbs ≤ P) :
    (sumRun xs).value.natAbs ≤ xs.length*P := by
  induction xs with
  | nil => simp [sumRun, atom]
  | cons x xs ih =>
      have hh := ih (fun y hy => hx y (by simp [hy]))
      have hhead := hx x (by simp)
      simp only [sumRun, add, List.length_cons]
      exact (Int.natAbs_add_le _ _).trans (by nlinarith)

lemma sumRun_tail_int_bound {n P : ℕ} (xs : List (ScalarRun ℤ))
    (hlen : xs.length ≤ n) (hx : ∀ x ∈ xs, x.value.natAbs ≤ P) (k : ℕ) :
    (sumRun (xs.drop k)).value.natAbs ≤ n*P := by
  have hh := sumRun_int_bound (xs.drop k)
    (fun x hx' => hx x (List.mem_of_mem_drop hx'))
  exact hh.trans (Nat.mul_le_mul_right _ (by simp only [List.length_drop]; omega))

/-- All sums in one recurrence step have only `n` terms. -/
lemma integer_step_bound {n M P : ℕ} {A F : Matrix (Fin n) (Fin n) ℤ}
    (hA : ∀ i j, (A i j).natAbs ≤ M) (hF : ∀ i j, (F i j).natAbs ≤ P)
    (i j : Fin n) :
    (BirdDet.Spec.stepEntry A F i j).natAbs ≤ 2*n*P*M := by
  have hd := integer_sum_bound (Finset.Ioi i) (fun k _ => hF k k)
  have hp := integer_sum_bound (M := P*M) (Finset.Ioi i)
    (fun k _ => show (F i k*A k j).natAbs ≤ P*M by
      rw [Int.natAbs_mul]; exact Nat.mul_le_mul (hF i k) (hA k j))
  change ((-(∑ k ∈ Finset.Ioi i, F k k))*A i j +
    ∑ k ∈ Finset.Ioi i, F i k*A k j).natAbs ≤ _
  calc
    _ ≤ ((-(∑ k ∈ Finset.Ioi i, F k k))*A i j).natAbs +
      (∑ k ∈ Finset.Ioi i, F i k*A k j).natAbs := Int.natAbs_add_le _ _
    _ ≤ (n*P)*M+n*(P*M) := by
      rw [Int.natAbs_mul, Int.natAbs_neg]
      exact Nat.add_le_add (Nat.mul_le_mul hd (hA i j)) hp
    _ = _ := by ring

lemma integer_step_pow_bound {n K L : ℕ} {A F : Matrix (Fin n) (Fin n) ℤ}
    (hA : ∀ i j, (A i j).natAbs ≤ 2 ^ K)
    (hF : ∀ i j, (F i j).natAbs ≤ 2 ^ L) (i j : Fin n) :
    (BirdDet.Spec.stepEntry A F i j).natAbs ≤ 2 ^ (L+K+n+1) := by
  calc
    _ ≤ 2*n*2 ^ L*2 ^ K := integer_step_bound hA hF i j
    _ ≤ 2*2 ^ n*2 ^ L*2 ^ K := by gcongr; exact (Nat.lt_two_pow_self (n := n)).le
    _ = 2 ^ (L+K+n+1) := by simp only [pow_add, pow_one]; ring

/-- Linear growth in the number of Bird iterations, hence polynomial in the
variable matrix order. No factorial appears in this executed-state bound. -/
def iterationBits (n K t : ℕ) : ℕ := K+t*(K+n+1)

lemma iterateRun_natAbs_le {n K : ℕ} (A : StoredMatrix ℤ n)
    (hA : ∀ i j, (view A i j).natAbs ≤ 2 ^ K) (t : ℕ) (i j : Fin n) :
    (view (iterateRun A t).matrix i j).natAbs ≤ 2 ^ (iterationBits n K t) := by
  induction t generalizing i j with
  | zero => simpa [iterateRun, iterationBits] using hA i j
  | succ t ih =>
      have hall : ∀ i j, (view (iterateRun A t).matrix i j).natAbs ≤
          2 ^ (iterationBits n K t) := by
        intro i j
        exact ih i j
      simpa [iterateRun, iterationBits, Nat.succ_mul, Nat.add_assoc,
        Nat.add_comm, Nat.add_left_comm] using integer_step_pow_bound hA hall i j

/-- Tail sums, products, and the final addition in an executed entry remain
within a polynomial bit bound. The two quantified sum bounds cover the recursive
partial sums formed by `sumRun`. -/
theorem entryRun_intermediate_bounds {n K L : ℕ} (A F : StoredMatrix ℤ n)
    (hA : ∀ i j, (view A i j).natAbs ≤ 2 ^ K)
    (hF : ∀ i j, (view F i j).natAbs ≤ 2 ^ L) (i j : Fin n) :
    (∀ k : Fin n, ((if i < k then view F i k else 0)*view A k j).natAbs ≤
      2 ^ (L+K)) ∧
    (∀ k : ℕ, (sumRun ((List.ofFn fun z : Fin n =>
      atom (if i < z then view F z z else 0)).drop k)).value.natAbs ≤ 2 ^ (L+n)) ∧
    (∀ k : ℕ, (sumRun ((List.ofFn fun z : Fin n =>
      mul (atom (if i < z then view F i z else 0)) (atom (view A z j))).drop k)).value.natAbs
        ≤ 2 ^ (L+K+n)) ∧
    (entryRun A F i j).value.natAbs ≤ 2 ^ (L+K+n+1) := by
  have hm (k : Fin n) :
      ((if i < k then view F i k else 0)*view A k j).natAbs ≤ 2 ^ (L+K) := by
    rw [Int.natAbs_mul, pow_add]
    apply Nat.mul_le_mul _ (hA k j)
    split_ifs
    · exact hF i k
    · simp
  refine ⟨hm, ?_, ?_, ?_⟩
  · intro k
    have hh := sumRun_tail_int_bound (n := n)
      (List.ofFn fun z : Fin n => atom (if i < z then view F z z else 0))
      (by simp) (P := 2 ^ L) (by
        intro x hx
        obtain ⟨z, rfl⟩ := List.mem_ofFn.mp hx
        simp only [atom]
        split_ifs
        · exact hF z z
        · simp) k
    exact hh.trans (by
      rw [pow_add, Nat.mul_comm (2 ^ L)]
      exact Nat.mul_le_mul_right _ (Nat.lt_two_pow_self (n := n)).le)
  · intro k
    have hh := sumRun_tail_int_bound (n := n)
      (List.ofFn fun z : Fin n =>
        mul (atom (if i < z then view F i z else 0)) (atom (view A z j)))
      (by simp) (P := 2 ^ (L+K)) (by
        intro x hx
        obtain ⟨z, rfl⟩ := List.mem_ofFn.mp hx
        exact hm z) k
    exact hh.trans (by
      rw [pow_add 2 (L+K) n, Nat.mul_comm (2 ^ (L+K))]
      exact Nat.mul_le_mul_right _ (Nat.lt_two_pow_self (n := n)).le)
  · rw [entryRun_value]
    exact integer_step_pow_bound hA hF i j

/-- Rational determinant evaluation uses integer Bird execution and one final
rational division. The common denominator is cached before entries are built. -/
def rationalDeterminant {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : ℚ :=
  let D := matrixDenominator A
  let Z : StoredMatrix ℤ n := Vector.ofFn fun i => Vector.ofFn fun j =>
    (A i j).num * (D / (A i j).den : ℕ)
  ((determinantRun n Z).value : ℚ) / (D : ℚ) ^ n

theorem rationalDeterminant_correct {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    rationalDeterminant A = A.det := by
  simp only [rationalDeterminant, determinantRun_correct]
  have hz : view (Vector.ofFn fun i => Vector.ofFn fun j =>
      (A i j).num * (matrixDenominator A / (A i j).den : ℕ)) = integerMatrix A := by
    ext i j
    simp [view, integerMatrix]
  rw [hz, det_eq_integerMatrix_div]

/-- Every stored integer in any executed Bird stage has this polynomial bit
bound in the original rational input size and matrix order. -/
theorem cleared_iterate_bound {n B t : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A B) (ht : t ≤ n) (i j : Fin n) :
    (view (iterateRun (store (integerMatrix A)) t).matrix i j).natAbs ≤
      2 ^ (iterationBits n (B+n*n*B) n) := by
  have hh := iterateRun_natAbs_le (store (integerMatrix A))
    (by simpa using integerMatrix_natAbs_le hA) t i j
  exact hh.trans (Nat.pow_le_pow_right (by decide) (by
    unfold iterationBits
    exact Nat.add_le_add_left (Nat.mul_le_mul_right _ ht) _))

end MatroidSpectral.Elimination
