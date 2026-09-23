import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Data.Fintype.Fin
import Mathlib.Tactic.FinCases

namespace CubicGap

/-- Integer count polynomial for the 192-variable cubic example. -/
def largeValue (a b c : ℕ) : ℤ :=
  2 * (c.choose 3 : ℤ) + 3 * (b : ℤ) * (c.choose 2 : ℤ) +
    120 * (b.choose 2 : ℤ) + 105 * (a : ℤ) * c +
    70 * (a : ℤ) * b + 63 * (a.choose 2 : ℤ)

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c0 : ∀ a b : Fin 65,
    105 * largeValue a b 0 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 0 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c1 : ∀ a b : Fin 65,
    105 * largeValue a b 1 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 1 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c2 : ∀ a b : Fin 65,
    105 * largeValue a b 2 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 2 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c3 : ∀ a b : Fin 65,
    105 * largeValue a b 3 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 3 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c4 : ∀ a b : Fin 65,
    105 * largeValue a b 4 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 4 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c5 : ∀ a b : Fin 65,
    105 * largeValue a b 5 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 5 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c6 : ∀ a b : Fin 65,
    105 * largeValue a b 6 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 6 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c7 : ∀ a b : Fin 65,
    105 * largeValue a b 7 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 7 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c8 : ∀ a b : Fin 65,
    105 * largeValue a b 8 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 8 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c9 : ∀ a b : Fin 65,
    105 * largeValue a b 9 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 9 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c10 : ∀ a b : Fin 65,
    105 * largeValue a b 10 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 10 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c11 : ∀ a b : Fin 65,
    105 * largeValue a b 11 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 11 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c12 : ∀ a b : Fin 65,
    105 * largeValue a b 12 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 12 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c13 : ∀ a b : Fin 65,
    105 * largeValue a b 13 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 13 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c14 : ∀ a b : Fin 65,
    105 * largeValue a b 14 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 14 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c15 : ∀ a b : Fin 65,
    105 * largeValue a b 15 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 15 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c16 : ∀ a b : Fin 65,
    105 * largeValue a b 16 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 16 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c17 : ∀ a b : Fin 65,
    105 * largeValue a b 17 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 17 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c18 : ∀ a b : Fin 65,
    105 * largeValue a b 18 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 18 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c19 : ∀ a b : Fin 65,
    105 * largeValue a b 19 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 19 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c20 : ∀ a b : Fin 65,
    105 * largeValue a b 20 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 20 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c21 : ∀ a b : Fin 65,
    105 * largeValue a b 21 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 21 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c22 : ∀ a b : Fin 65,
    105 * largeValue a b 22 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 22 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c23 : ∀ a b : Fin 65,
    105 * largeValue a b 23 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 23 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c24 : ∀ a b : Fin 65,
    105 * largeValue a b 24 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 24 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c25 : ∀ a b : Fin 65,
    105 * largeValue a b 25 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 25 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c26 : ∀ a b : Fin 65,
    105 * largeValue a b 26 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 26 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c27 : ∀ a b : Fin 65,
    105 * largeValue a b 27 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 27 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c28 : ∀ a b : Fin 65,
    105 * largeValue a b 28 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 28 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c29 : ∀ a b : Fin 65,
    105 * largeValue a b 29 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 29 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c30 : ∀ a b : Fin 65,
    105 * largeValue a b 30 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 30 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c31 : ∀ a b : Fin 65,
    105 * largeValue a b 31 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 31 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c32 : ∀ a b : Fin 65,
    105 * largeValue a b 32 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 32 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c33 : ∀ a b : Fin 65,
    105 * largeValue a b 33 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 33 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c34 : ∀ a b : Fin 65,
    105 * largeValue a b 34 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 34 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c35 : ∀ a b : Fin 65,
    105 * largeValue a b 35 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 35 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c36 : ∀ a b : Fin 65,
    105 * largeValue a b 36 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 36 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c37 : ∀ a b : Fin 65,
    105 * largeValue a b 37 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 37 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c38 : ∀ a b : Fin 65,
    105 * largeValue a b 38 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 38 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c39 : ∀ a b : Fin 65,
    105 * largeValue a b 39 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 39 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c40 : ∀ a b : Fin 65,
    105 * largeValue a b 40 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 40 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c41 : ∀ a b : Fin 65,
    105 * largeValue a b 41 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 41 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c42 : ∀ a b : Fin 65,
    105 * largeValue a b 42 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 42 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c43 : ∀ a b : Fin 65,
    105 * largeValue a b 43 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 43 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c44 : ∀ a b : Fin 65,
    105 * largeValue a b 44 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 44 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c45 : ∀ a b : Fin 65,
    105 * largeValue a b 45 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 45 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c46 : ∀ a b : Fin 65,
    105 * largeValue a b 46 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 46 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c47 : ∀ a b : Fin 65,
    105 * largeValue a b 47 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 47 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c48 : ∀ a b : Fin 65,
    105 * largeValue a b 48 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 48 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c49 : ∀ a b : Fin 65,
    105 * largeValue a b 49 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 49 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c50 : ∀ a b : Fin 65,
    105 * largeValue a b 50 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 50 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c51 : ∀ a b : Fin 65,
    105 * largeValue a b 51 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 51 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c52 : ∀ a b : Fin 65,
    105 * largeValue a b 52 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 52 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c53 : ∀ a b : Fin 65,
    105 * largeValue a b 53 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 53 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c54 : ∀ a b : Fin 65,
    105 * largeValue a b 54 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 54 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c55 : ∀ a b : Fin 65,
    105 * largeValue a b 55 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 55 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c56 : ∀ a b : Fin 65,
    105 * largeValue a b 56 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 56 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c57 : ∀ a b : Fin 65,
    105 * largeValue a b 57 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 57 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c58 : ∀ a b : Fin 65,
    105 * largeValue a b 58 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 58 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c59 : ∀ a b : Fin 65,
    105 * largeValue a b 59 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 59 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c60 : ∀ a b : Fin 65,
    105 * largeValue a b 60 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 60 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c61 : ∀ a b : Fin 65,
    105 * largeValue a b 61 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 61 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c62 : ∀ a b : Fin 65,
    105 * largeValue a b 62 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 62 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c63 : ∀ a b : Fin 65,
    105 * largeValue a b 63 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 63 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c64 : ∀ a b : Fin 65,
    105 * largeValue a b 64 ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * 64 - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

/-- The proposed affine function minorizes the cubic count polynomial at every
vertex count triple in the 192-variable example. -/
theorem large_minorant (a b c : Fin 65) :
    105 * largeValue a b c ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * (c : ℤ) - 51743768 := by
  fin_cases c
  · exact large_minorant_c0 a b
  · exact large_minorant_c1 a b
  · exact large_minorant_c2 a b
  · exact large_minorant_c3 a b
  · exact large_minorant_c4 a b
  · exact large_minorant_c5 a b
  · exact large_minorant_c6 a b
  · exact large_minorant_c7 a b
  · exact large_minorant_c8 a b
  · exact large_minorant_c9 a b
  · exact large_minorant_c10 a b
  · exact large_minorant_c11 a b
  · exact large_minorant_c12 a b
  · exact large_minorant_c13 a b
  · exact large_minorant_c14 a b
  · exact large_minorant_c15 a b
  · exact large_minorant_c16 a b
  · exact large_minorant_c17 a b
  · exact large_minorant_c18 a b
  · exact large_minorant_c19 a b
  · exact large_minorant_c20 a b
  · exact large_minorant_c21 a b
  · exact large_minorant_c22 a b
  · exact large_minorant_c23 a b
  · exact large_minorant_c24 a b
  · exact large_minorant_c25 a b
  · exact large_minorant_c26 a b
  · exact large_minorant_c27 a b
  · exact large_minorant_c28 a b
  · exact large_minorant_c29 a b
  · exact large_minorant_c30 a b
  · exact large_minorant_c31 a b
  · exact large_minorant_c32 a b
  · exact large_minorant_c33 a b
  · exact large_minorant_c34 a b
  · exact large_minorant_c35 a b
  · exact large_minorant_c36 a b
  · exact large_minorant_c37 a b
  · exact large_minorant_c38 a b
  · exact large_minorant_c39 a b
  · exact large_minorant_c40 a b
  · exact large_minorant_c41 a b
  · exact large_minorant_c42 a b
  · exact large_minorant_c43 a b
  · exact large_minorant_c44 a b
  · exact large_minorant_c45 a b
  · exact large_minorant_c46 a b
  · exact large_minorant_c47 a b
  · exact large_minorant_c48 a b
  · exact large_minorant_c49 a b
  · exact large_minorant_c50 a b
  · exact large_minorant_c51 a b
  · exact large_minorant_c52 a b
  · exact large_minorant_c53 a b
  · exact large_minorant_c54 a b
  · exact large_minorant_c55 a b
  · exact large_minorant_c56 a b
  · exact large_minorant_c57 a b
  · exact large_minorant_c58 a b
  · exact large_minorant_c59 a b
  · exact large_minorant_c60 a b
  · exact large_minorant_c61 a b
  · exact large_minorant_c62 a b
  · exact large_minorant_c63 a b
  · exact large_minorant_c64 a b

end CubicGap
