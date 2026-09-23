import Formal.NetworkSimplex.ThresholdCircuitCriterion
import Formal.NetworkSimplex.ThresholdCircuitInteger

/-! A finite exact integer-certificate criterion with the claimed determinant weights. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open NetworkSimplex.Threshold

/-- Every nonnegative integer cancellation yields a valid inequality. -/
theorem integer_cancel_valid {I : Type*} {s : ℕ} (A : I → Fin m → ℤ)
    (b : I → ℝ) (e : Fin s → I) (p : Fin s → ℕ)
    (hc : ∀ j, ∑ i, (p i : ℤ) * A (e i) j = 0)
    {x : Fin m → ℝ} (hx : ∀ i, ∑ j, (A i j : ℝ) * x j ≤ b i) :
    0 ≤ ∑ i, (p i : ℝ) * b (e i) := by
  have hle := Finset.sum_le_sum (fun i (_ : i ∈ Finset.univ) =>
    mul_le_mul_of_nonneg_left (hx (e i)) (Nat.cast_nonneg (p i) : (0 : ℝ) ≤ p i))
  have hzero : (∑ i, (p i : ℝ) * ∑ j, (A (e i) j : ℝ) * x j) = 0 := by
    simp only [Finset.mul_sum, ← mul_assoc]
    rw [Finset.sum_comm]
    apply Finset.sum_eq_zero
    intro j _
    rw [← Finset.sum_mul]
    have hj : (∑ i, (p i : ℝ) * (A (e i) j : ℝ)) = 0 := by exact_mod_cast hc j
    rw [hj, zero_mul]
  rwa [hzero] at hle

/-- All necessary integer tests fit within m+1 rows and the zero-one determinant bound.
The quantifiers range over finite bounded data for any finite row set. -/
theorem feasible_iff_bounded_integer_tests {I : Type*} [Finite I]
    (A : I → Fin m → ℤ) (hA : RowSignedZeroOne A) (b : I → ℝ) :
    (∃ x : Fin m → ℝ, ∀ i, ∑ j, (A i j : ℝ) * x j ≤ b i) ↔
      ∀ (s : ℕ), s ≤ m + 1 → ∀ e : Fin s ↪ I, ∀ p : Fin s → ℕ,
        (∀ i, 0 < p i ∧ p i ≤ delta01 m) → Finset.univ.gcd p = 1 →
        (∀ j, ∑ i, (p i : ℤ) * A (e i) j = 0) →
        0 ≤ ∑ i, (p i : ℝ) * b (e i) := by
  constructor
  · rintro ⟨x, hx⟩ s _ e p _ _ hc
    exact integer_cancel_valid A b e p hc hx
  · intro ht
    apply (feasible_iff_positiveCircuits (fun i j => (A i j : ℝ)) b).mpr
    intro C
    obtain ⟨p, hp, hg, hc, hscale⟩ := C.exists_primitive_integer_weights A hA
    have hsum : 0 < ∑ i, (p i : ℝ) := by
      have hne : (Finset.univ : Finset (Fin C.size)).Nonempty :=
        ⟨⟨0, C.size_pos⟩, Finset.mem_univ _⟩
      apply Finset.sum_pos
      · intro i _
        exact_mod_cast (hp i).1
      · exact hne
    have htest := ht C.size C.size_le C.index p hp hg hc
    have he : (∑ i, (p i : ℝ) * b (C.index i)) =
        (∑ i, (p i : ℝ)) * ∑ i, C.mass i * b (C.index i) := by
      calc
        _ = ∑ i, ((∑ j, (p j : ℝ)) * C.mass i) * b (C.index i) :=
          Finset.sum_congr rfl (fun i _ => congrArg (fun z => z * b (C.index i)) (hscale i))
        _ = _ := by simp only [Finset.mul_sum, mul_assoc]
    rw [he] at htest
    exact nonneg_of_mul_nonneg_right htest hsum

end NetworkSimplex.Chain.Threshold
