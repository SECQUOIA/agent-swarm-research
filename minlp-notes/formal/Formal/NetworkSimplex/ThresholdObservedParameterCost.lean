import Formal.NetworkSimplex.ThresholdKeys
import Formal.NetworkSimplex.ThresholdBasisOracle

/-! Explicit quadratic-exponent bounds for the fixed observed-label query overhead. -/
namespace NetworkSimplex.Chain.Threshold

/-- Cached basis enumeration and all its trials have quadratic-exponent overhead. -/
theorem observed_basis_parameter_bound (a : ℕ) :
    normalKeyCount a + normalKeyCount a ^ a * basisTrialCharge (normalKeyCount a) a ≤
      2 ^ (8 * (a + 2) ^ 2) := by
  let B := 2 ^ (a + 2)
  have hK : normalKeyCount a ≤ B := normalKeyCount_le_pow a
  have ha : a + 2 ≤ B := Nat.lt_two_pow_self.le
  have hB : 1 ≤ B := by omega
  have ht : basisTrialCharge (normalKeyCount a) a ≤ 3 * B ^ 2 := by
    have hm := Nat.mul_le_mul hK (show a + 1 ≤ B by omega)
    dsimp only [basisTrialCharge]
    nlinarith
  have hp : normalKeyCount a ^ a ≤ B ^ a := Nat.pow_le_pow_left hK a
  have hb : B ≤ B ^ (a + 2) := by
    calc
      B = B ^ 1 := by simp
      _ ≤ B ^ (a + 2) := Nat.pow_le_pow_right hB (by omega)
  calc
    _ ≤ B + B ^ a * (3 * B ^ 2) := Nat.add_le_add hK (Nat.mul_le_mul hp ht)
    _ ≤ 4 * B ^ (a + 2) := by
      rw [pow_add] at hb ⊢
      nlinarith
    _ = 2 ^ (2 + (a + 2) ^ 2) := by
      dsimp [B]
      rw [← pow_mul]
      change 2 ^ 2 * 2 ^ ((a + 2) * (a + 2)) = _
      rw [← pow_add]
      congr 1
      ring
    _ ≤ 2 ^ (8 * (a + 2) ^ 2) := Nat.pow_le_pow_right (by decide) (by nlinarith)

/-- The complete circuit-library scan has the same quadratic-exponent overhead. -/
theorem observed_circuit_parameter_bound (a : ℕ) :
    2 ^ (4 * (a + 1) ^ 2) * (2 * a + 3) ≤ 2 ^ (8 * (a + 2) ^ 2) := by
  have h : 2 * a + 3 ≤ 2 ^ (2 * a + 3) := Nat.lt_two_pow_self.le
  calc
    _ ≤ 2 ^ (4 * (a + 1) ^ 2) * 2 ^ (2 * a + 3) := Nat.mul_le_mul_left _ h
    _ = 2 ^ (4 * (a + 1) ^ 2 + (2 * a + 3)) := (pow_add _ _ _).symm
    _ ≤ 2 ^ (8 * (a + 2) ^ 2) := Nat.pow_le_pow_right (by decide) (by nlinarith)

end NetworkSimplex.Chain.Threshold
