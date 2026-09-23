import Formal.NetworkSimplex.ThresholdPreprocessCost

/-! Operand bounds for the actual cofactor compiler and its validation sums. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators

theorem rawCofactorTrace_factorial {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : RowSignedZeroOne A) (c : CofactorCandidate m N)
    (i : Fin (c.size.val + 1)) :
    ((rawCofactorTrace A c).get i).1.natAbs ≤ m.factorial := by
  simp only [rawCofactorTrace, Vector.get_ofFn]
  exact (determinantTrace_abs c.size.val _ (fun j k => rowSigned_abs hA _ _)).trans
    (Nat.factorial_le (by omega))

/-- The cached normalization quotients are bounded even for rejected candidates
and for the all-zero cofactor vector. -/
theorem compileCircuit_weight_factorial {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : RowSignedZeroOne A) (c : CofactorCandidate m N)
    (i : Fin (c.size.val + 1)) :
    (compileCircuit A c).weight i ≤ m.factorial := by
  simp only [CompiledCircuit.weight, compileCircuit, compileCircuitCounted, Vector.get_map]
  exact (Nat.div_le_self _ _).trans (rawCofactorTrace_factorial A hA c i)

theorem validation_product_factorial {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : RowSignedZeroOne A) (c : CofactorCandidate m N)
    (i : Fin (c.size.val + 1)) (j : Fin m) :
    (((compileCircuit A c).weight i : ℤ) * A (c.support i) j).natAbs ≤
      m.factorial := by
  rw [Int.natAbs_mul, Int.natAbs_natCast]
  exact (Nat.mul_le_mul (compileCircuit_weight_factorial A hA c i)
    (rowSigned_abs hA _ _)).trans_eq (mul_one _)

/-- An arbitrary partial sum covers any order used to evaluate the cancellation
check, without relying on cancellation in the final result. -/
theorem validation_partial_factorial {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : RowSignedZeroOne A) (c : CofactorCandidate m N)
    (part : Finset (Fin (c.size.val + 1))) (j : Fin m) :
    (∑ i ∈ part, ((compileCircuit A c).weight i : ℤ) * A (c.support i) j).natAbs ≤
      (m + 1).factorial := by
  apply (Int.natAbs_sum_le _ _).trans
  calc
    _ ≤ ∑ _i ∈ part, m.factorial :=
      Finset.sum_le_sum (fun i _ => validation_product_factorial A hA c i j)
    _ ≤ (m + 1) * m.factorial := by
      simp only [Finset.sum_const, smul_eq_mul]
      apply Nat.mul_le_mul_right
      have hc := (Finset.card_le_univ part).trans_eq (Fintype.card_fin _)
      have hs := c.size.isLt
      omega
    _ = _ := (Nat.factorial_succ m).symm

/-- The compiler's raw cofactor, divisor, and stored quotient fit the same width. -/
theorem compileCircuit_normalization_bits {m N : ℕ}
    (A : Matrix (Fin N) (Fin m) ℤ) (hA : RowSignedZeroOne A)
    (c : CofactorCandidate m N) :
    (∀ i, ((rawCofactorTrace A c).get i).1.natAbs < 2 ^ circuitBits (m + 1)) ∧
    (gcdTrace (c.size.val + 1)
      ((rawCofactorTrace A c).map (fun r => r.1.natAbs)).get).1 <
        2 ^ circuitBits (m + 1) ∧
    ∀ i, (compileCircuit A c).weight i < 2 ^ circuitBits (m + 1) := by
  have hf : m.factorial < 2 ^ circuitBits (m + 1) :=
    (Nat.factorial_le (by omega : m ≤ m + 1)).trans_lt
      (factorial_lt_circuitBits (m + 1))
  refine ⟨fun i => (rawCofactorTrace_factorial A hA c i).trans_lt hf, ?_,
    fun i => (compileCircuit_weight_factorial A hA c i).trans_lt hf⟩
  apply gcdTrace_value_lt
  intro i
  simpa only [Vector.get_map] using (rawCofactorTrace_factorial A hA c i).trans_lt hf

/-- All multiplication inputs and outputs and all partial cancellation sums in
the actual validation expression fit the width used by `preprocessingBitWork`. -/
theorem validation_operands_bits {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (hA : RowSignedZeroOne A) (c : CofactorCandidate m N)
    (part : Finset (Fin (c.size.val + 1))) (i : Fin (c.size.val + 1)) (j : Fin m) :
    (compileCircuit A c).weight i < 2 ^ circuitBits (m + 1) ∧
    (A (c.support i) j).natAbs < 2 ^ circuitBits (m + 1) ∧
    (((compileCircuit A c).weight i : ℤ) * A (c.support i) j).natAbs <
      2 ^ circuitBits (m + 1) ∧
    (∑ k ∈ part, ((compileCircuit A c).weight k : ℤ) * A (c.support k) j).natAbs <
      2 ^ circuitBits (m + 1) := by
  have hf := factorial_lt_circuitBits (m + 1)
  have hf' := (Nat.factorial_le (by omega : m ≤ m + 1)).trans_lt hf
  exact ⟨(compileCircuit_weight_factorial A hA c i).trans_lt hf',
    ((rowSigned_abs hA _ _).trans (Nat.factorial_pos _)).trans_lt hf,
    (validation_product_factorial A hA c i j).trans_lt hf',
    (validation_partial_factorial A hA c part j).trans_lt hf⟩

/-- The Euclidean calls launched by the actual recursive gcd fold. -/
inductive GcdEuclidCall : (n : ℕ) → (Fin n → ℕ) → ℕ → ℕ → Prop
  | head (n : ℕ) (v : Fin (n + 1) → ℕ) :
      GcdEuclidCall (n + 1) v (v 0) (gcdTrace n (fun i => v i.succ)).1
  | tail {n a b : ℕ} (v : Fin (n + 1) → ℕ) :
      GcdEuclidCall n (fun i => v i.succ) a b → GcdEuclidCall (n + 1) v a b

theorem gcdEuclidCall_bits {n a b B : ℕ} {v : Fin n → ℕ}
    (h : GcdEuclidCall n v a b) (hv : ∀ i, v i < 2 ^ B) :
    a < 2 ^ B ∧ b < 2 ^ B := by
  induction h with
  | head n v => exact ⟨hv 0, gcdTrace_value_lt n B _ (fun i => hv i.succ)⟩
  | tail v _ ih => exact ih (fun i => hv i.succ)

/-- Every dividend, divisor, remainder, and quotient encountered during the
compiler's gcd normalization fits its stated bit budget. -/
theorem compileCircuit_euclid_operands_bits {m N a b x y : ℕ}
    (A : Matrix (Fin N) (Fin m) ℤ) (hA : RowSignedZeroOne A)
    (c : CofactorCandidate m N)
    (hcall : GcdEuclidCall (c.size.val + 1)
      ((rawCofactorTrace A c).map (fun r => r.1.natAbs)).get a b)
    (hstep : EuclidReachable a b x y) :
    x < 2 ^ circuitBits (m + 1) ∧ y < 2 ^ circuitBits (m + 1) ∧
    x % y < 2 ^ circuitBits (m + 1) ∧ x / y < 2 ^ circuitBits (m + 1) := by
  have hb := gcdEuclidCall_bits hcall (B := circuitBits (m + 1)) (fun i => by
    simpa only [Vector.get_map] using (compileCircuit_normalization_bits A hA c).1 i)
  exact ⟨(euclidReachable_bits hb.1 hb.2 hstep).1,
    (euclidReachable_bits hb.1 hb.2 hstep).2,
    euclidReachable_division_bits hb.1 hb.2 hstep⟩

/-- The unreduced signed-subset universe also has the same quadratic exponential
preprocessing bound; no row-sign consistency assumption is needed for counting. -/
theorem signed_preprocessingWork_exp {m : ℕ}
    (A : Matrix (Fin (2 ^ (m + 1))) (Fin m) ℤ) (hA : RowSignedZeroOne A) :
    preprocessingWork A ≤ 2 ^ (8 * (m + 2) ^ 2) := by
  have hc := cofactorCandidates_length_exp m (2 ^ (m + 1))
    (Nat.one_le_pow _ _ (by decide))
    (Nat.pow_le_pow_right (by decide) (by omega : m + 1 ≤ m + 2))
  calc
    _ ≤ (cofactorCandidates m _).length * candidateWork m := preprocessingWork_le A hA
    _ ≤ 2 ^ (4 * (m + 1) ^ 2) * 2 ^ (4 * (m + 2) ^ 2) :=
      Nat.mul_le_mul hc (candidateWork_exp m)
    _ ≤ _ := by
      rw [← pow_add]
      apply Nat.pow_le_pow_right (by decide)
      have hs := Nat.pow_le_pow_left (show m + 1 ≤ m + 2 by omega) 2
      omega

theorem signed_preprocessingBitWork_exp {m : ℕ}
    (A : Matrix (Fin (2 ^ (m + 1))) (Fin m) ℤ) (hA : RowSignedZeroOne A) :
    preprocessingBitWork A ≤ 2 ^ (14 * (m + 2) ^ 2) := by
  calc
    _ ≤ 2 ^ (8 * (m + 2) ^ 2) * 2 ^ (6 * (m + 2) ^ 2) :=
      Nat.mul_le_mul (signed_preprocessingWork_exp A hA) (scalarBitWork_exp m)
    _ = _ := by rw [← pow_add]; congr 1; ring

end NetworkSimplex.Threshold
