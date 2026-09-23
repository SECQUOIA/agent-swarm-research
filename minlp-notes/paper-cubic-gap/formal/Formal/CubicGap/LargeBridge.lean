import Formal.CubicGap.Finite
import Formal.CubicGap.LargeFinite
import Mathlib.Tactic

namespace CubicGap

theorem threeValue64_eq_largeValue (a b c : ℕ) :
    threeValue64 a b c = (largeValue a b c : ℚ) := by
  simp [threeValue64, countPhi, coefficients64, largeValue]

/-- The integer certificate gives the rational affine minorant used for expectations. -/
theorem minorant64 (a b c : Fin 65) :
    (871710 * (a : ℚ) + 900446 * (b : ℚ) + 899046 * (c : ℚ) - 51743768) / 105 ≤
      threeValue64 a b c := by
  rw [threeValue64_eq_largeValue]
  have h := large_minorant a b c
  have hq : 871710 * (a : ℚ) + 900446 * (b : ℚ) + 899046 * (c : ℚ) - 51743768 ≤
      105 * (largeValue a b c : ℚ) := by
    exact_mod_cast h
  linarith

end CubicGap
