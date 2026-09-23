import Formal.NetworkSimplex.ThresholdCircuitPreprocess
import Formal.ReciprocalAnchor.ManyBitCost

/-! Arithmetic and schoolbook bit-operation budgets for executable preprocessing. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators

/-- A common bit width for all determinant minors and normalized coefficients. -/
def circuitBits (m : ℕ) : ℕ := (m + 1) ^ 2 + 1

theorem factorial_lt_circuitBits (m : ℕ) : m.factorial < 2 ^ circuitBits m := by
  have hm : m ≤ 2 ^ (m + 1) :=
    Nat.lt_two_pow_self.le.trans (Nat.pow_le_pow_right (by decide) (by omega))
  calc
    _ ≤ m ^ m := Nat.factorial_le_pow m
    _ ≤ (2 ^ (m + 1)) ^ m := Nat.pow_le_pow_left hm _
    _ = 2 ^ ((m + 1) * m) := (pow_mul ..).symm
    _ < _ := Nat.pow_lt_pow_right (by decide) (by dsimp [circuitBits]; nlinarith)

theorem rowSigned_abs {m N : ℕ} {A : Matrix (Fin N) (Fin m) ℤ}
    (hA : RowSignedZeroOne A) (i : Fin N) (j : Fin m) : (A i j).natAbs ≤ 1 := by
  rcases hA i with hp | hn
  · rcases hp j with h | h <;> simp [h]
  · rcases hn j with h | h <;> simp [h]

theorem rawCofactorTrace_bits {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : RowSignedZeroOne A) (c : CofactorCandidate m N) (i : Fin (c.size.val + 1)) :
    ((rawCofactorTrace A c).get i).1.natAbs < 2 ^ circuitBits m := by
  simp only [rawCofactorTrace, Vector.get_ofFn]
  have hd := determinantTrace_abs c.size.val
    ((A.submatrix c.support c.columns).submatrix i.succAbove id)
    (fun j k => rowSigned_abs hA _ _)
  exact (hd.trans (Nat.factorial_le (by omega))).trans_lt
    (factorial_lt_circuitBits m)

/-- Uniform per-candidate charge for compilation and full validation. -/
def candidateWork (m : ℕ) : ℕ :=
  (m + 1) * ((m + 2).factorial + 2 * circuitBits m + 2) + 3 * (m + 1) ^ 2

/-- Full validation has one positivity test per coefficient and, per coordinate,
a weighted dot product followed by one comparison. Short-circuiting only reduces it. -/
def validationWork {m N : ℕ} (c : CofactorCandidate m N) : ℕ :=
  (c.size.val + 1) + m * (2 * (c.size.val + 1) + 1)

theorem compileCircuitCounted_cost {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : RowSignedZeroOne A) (c : CofactorCandidate m N) :
    (compileCircuitCounted A c).2 + validationWork c ≤ candidateWork m := by
  have hs : c.size.val ≤ m := by omega
  have hd : (∑ i, ((rawCofactorTrace A c).get i).2) ≤
      (c.size.val + 1) * (m + 2).factorial := by
    calc
      _ ≤ ∑ _i : Fin (c.size.val + 1), (m + 2).factorial := by
        apply Finset.sum_le_sum
        intro i _
        simp only [rawCofactorTrace, Vector.get_ofFn]
        exact (determinantTrace_factorial _ _).trans
          (Nat.factorial_le (by omega))
      _ = _ := by simp
  have hg := gcdTrace_cost (c.size.val + 1) (circuitBits m)
    ((rawCofactorTrace A c).map (fun r => r.1.natAbs)).get
    (fun i => by simpa only [Vector.get_map] using rawCofactorTrace_bits A hA c i)
  have hv : validationWork c ≤ 3 * (m + 1) ^ 2 := by
    dsimp [validationWork]
    nlinarith
  have hdet := Nat.mul_le_mul_right (m + 2).factorial (Nat.add_le_add_right hs 1)
  have hgcd := Nat.mul_le_mul_left (2 * circuitBits m) (Nat.add_le_add_right hs 1)
  simp only [compileCircuitCounted, candidateWork]
  nlinarith

/-- Every enumerated candidate is compiled and checked at most once. -/
def preprocessingWork {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ) : ℕ :=
  ((cofactorCandidates m N).map fun c =>
    (compileCircuitCounted A c).2 + validationWork c).sum

theorem preprocessingWork_le {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : RowSignedZeroOne A) :
    preprocessingWork A ≤ (cofactorCandidates m N).length * candidateWork m := by
  unfold preprocessingWork
  induction cofactorCandidates m N with
  | nil => simp
  | cons c cs ih =>
    simp only [List.map_cons, List.sum_cons, List.length_cons]
    have hc := compileCircuitCounted_cost A hA c
    nlinarith

theorem candidateWork_polynomial_factorial (m : ℕ) :
    candidateWork m ≤ 16 * (m + 2) ^ 4 * (m + 2).factorial := by
  have hf : 1 ≤ (m + 2).factorial := Nat.factorial_pos _
  have hp : (m + 1) * (1 + 2 * circuitBits m + 2) + 3 * (m + 1) ^ 2 ≤
      16 * (m + 2) ^ 4 := by
    dsimp [circuitBits]
    nlinarith [sq_nonneg (m : ℤ)]
  have hq := Nat.mul_le_mul_right (m + 2).factorial hp
  have hr := Nat.mul_le_mul_left ((m + 1) * (2 * circuitBits m + 2) +
    3 * (m + 1) ^ 2) hf
  dsimp [candidateWork]
  nlinarith

theorem candidateWork_exp (m : ℕ) : candidateWork m ≤ 2 ^ (4 * (m + 2) ^ 2) := by
  have hm : m + 2 ≤ 2 ^ (m + 2) := Nat.lt_two_pow_self.le
  calc
    _ ≤ 16 * (m + 2) ^ 4 * (m + 2).factorial := candidateWork_polynomial_factorial m
    _ ≤ 16 * ((2 ^ (m + 2)) ^ 4) * ((2 ^ (m + 2)) ^ (m + 2)) := by
      apply Nat.mul_le_mul
      · exact Nat.mul_le_mul_left 16 (Nat.pow_le_pow_left hm _)
      · exact (Nat.factorial_le_pow _).trans (Nat.pow_le_pow_left hm _)
    _ = 2 ^ (4 + (m + 2) * 4 + (m + 2) * (m + 2)) := by
      rw [← pow_mul, ← pow_mul]
      norm_num [pow_add]
    _ ≤ _ := Nat.pow_le_pow_right (by decide) (by nlinarith)

theorem preprocessingWork_exp {m : ℕ}
    (A : Matrix (Fin (2 ^ m + m + 1)) (Fin m) ℤ) (hA : RowSignedZeroOne A) :
    preprocessingWork A ≤ 2 ^ (8 * (m + 2) ^ 2) := by
  have hc := cofactorCandidates_length_exp m (2 ^ m + m + 1)
    (Nat.succ_le_succ (Nat.zero_le _)) (normal_universe_bound m)
  calc
    _ ≤ (cofactorCandidates m _).length * candidateWork m := preprocessingWork_le A hA
    _ ≤ 2 ^ (4 * (m + 1) ^ 2) * 2 ^ (4 * (m + 2) ^ 2) :=
      Nat.mul_le_mul hc (candidateWork_exp m)
    _ ≤ _ := by
      rw [← pow_add]
      apply Nat.pow_le_pow_right (by decide)
      have hs := Nat.pow_le_pow_left (show m + 1 ≤ m + 2 by omega) 2
      omega

/-- Schoolbook bit budget; the width also covers the full validation dot products.
This is the explicit integer-arithmetic model, not a runtime claim about Lean's VM. -/
def preprocessingBitWork {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ) : ℕ :=
  preprocessingWork A * ReciprocalAnchor.ManyLeaf.BitCost.rationalStepCost (circuitBits (m + 1))

theorem scalarBitWork_exp (m : ℕ) :
    ReciprocalAnchor.ManyLeaf.BitCost.rationalStepCost (circuitBits (m + 1)) ≤
      2 ^ (6 * (m + 2) ^ 2) := by
  have hb : circuitBits (m + 1) + 1 ≤ 2 * (m + 2) ^ 2 := by
    dsimp [circuitBits]
    rw [show m + 1 + 1 = m + 2 by omega]
    have hs := Nat.pow_le_pow_left (show 2 ≤ m + 2 by omega) 2
    norm_num at hs
    omega
  have hm : m + 2 ≤ 2 ^ (m + 2) := Nat.lt_two_pow_self.le
  calc
    _ ≤ 256 * (circuitBits (m + 1) + 1) ^ 3 :=
      ReciprocalAnchor.ManyLeaf.BitCost.rationalStepCost_le _
    _ ≤ 256 * (2 * (m + 2) ^ 2) ^ 3 := Nat.mul_le_mul_left 256 (Nat.pow_le_pow_left hb _)
    _ = 2048 * (m + 2) ^ 6 := by ring
    _ ≤ 2048 * (2 ^ (m + 2)) ^ 6 := Nat.mul_le_mul_left _ (Nat.pow_le_pow_left hm _)
    _ = 2 ^ (11 + (m + 2) * 6) := by norm_num [pow_add, pow_mul]
    _ ≤ _ := Nat.pow_le_pow_right (by decide) (by nlinarith)

theorem preprocessingBitWork_exp {m : ℕ}
    (A : Matrix (Fin (2 ^ m + m + 1)) (Fin m) ℤ) (hA : RowSignedZeroOne A) :
    preprocessingBitWork A ≤ 2 ^ (14 * (m + 2) ^ 2) := by
  calc
    _ ≤ 2 ^ (8 * (m + 2) ^ 2) * 2 ^ (6 * (m + 2) ^ 2) :=
      Nat.mul_le_mul (preprocessingWork_exp A hA) (scalarBitWork_exp m)
    _ = _ := by rw [← pow_add]; congr 1; ring

end NetworkSimplex.Threshold
