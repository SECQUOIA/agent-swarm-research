import Mathlib.LinearAlgebra.Matrix.Determinant.TotallyUnimodular
import Mathlib.Data.ZMod.Basic

/-!
# Parity of signed vectors

Changing the signs of nonzero entries in a vector of zeros and units
preserves its image modulo two, including after multiplication by an integer
matrix. This is the arithmetic step in the signing criterion for TU.
-/
namespace MultilinearGap

open Matrix

/-- A zero or unit integer has the same parity after a change of sign. -/
theorem sign_cast_zmod_two {u v : ℤ}
    (hu : u ∈ Set.range (SignType.cast : SignType → ℤ))
    (hzero : u = 0 → v = 0) (hunit : u ≠ 0 → v = 1 ∨ v = -1) :
    (u : ZMod 2) = (v : ZMod 2) := by
  obtain ⟨s, rfl⟩ := hu
  cases s with
  | zero => simp_all
  | pos => rcases hunit (by norm_num) with rfl | rfl <;> simp [ZMod.neg_eq_self_mod_two]
  | neg => rcases hunit (by norm_num) with rfl | rfl <;> simp [ZMod.neg_eq_self_mod_two]

/-- Coordinatewise congruence modulo two is preserved by an integer matrix. -/
theorem mulVec_cast_zmod_two {m n : Type*} [Fintype n]
    (A : Matrix m n ℤ) {u v : n → ℤ}
    (h : ∀ j, (u j : ZMod 2) = (v j : ZMod 2)) (i : m) :
    ((A *ᵥ u) i : ZMod 2) = ((A *ᵥ v) i : ZMod 2) := by
  simp only [Matrix.mulVec, dotProduct, Int.cast_sum, Int.cast_mul]
  exact Finset.sum_congr rfl fun j _ => by rw [h j]

/-- Signing a zero/unit vector without changing its support preserves every
integer row sum modulo two. -/
theorem mulVec_sign_cast_zmod_two {m n : Type*} [Fintype n]
    (A : Matrix m n ℤ) {u v : n → ℤ}
    (hu : ∀ j, u j ∈ Set.range (SignType.cast : SignType → ℤ))
    (hzero : ∀ j, u j = 0 → v j = 0)
    (hunit : ∀ j, u j ≠ 0 → v j = 1 ∨ v j = -1) (i : m) :
    ((A *ᵥ u) i : ZMod 2) = ((A *ᵥ v) i : ZMod 2) :=
  mulVec_cast_zmod_two A (fun j => sign_cast_zmod_two (hu j) (hzero j) (hunit j)) i

/-- An even zero/unit integer is zero. -/
theorem sign_int_cast_zero {a : ℤ}
    (ha : a ∈ Set.range (SignType.cast : SignType → ℤ))
    (h : (a : ZMod 2) = 0) : a = 0 := by
  obtain ⟨s, rfl⟩ := ha
  cases s <;> norm_num at *

/-- A product of zero/unit integers divided by a unit is still zero or a unit. -/
theorem sign_of_scaled_units {d u v w : ℤ} (h : d * v = w * u)
    (hv : v = 1 ∨ v = -1)
    (hu : u ∈ Set.range (SignType.cast : SignType → ℤ))
    (hw : w ∈ Set.range (SignType.cast : SignType → ℤ)) :
    d ∈ Set.range (SignType.cast : SignType → ℤ) := by
  obtain ⟨su, rfl⟩ := hu
  obtain ⟨sw, rfl⟩ := hw
  rcases hv with rfl | rfl
  · simp only [mul_one] at h
    exact ⟨sw * su, by simpa using h.symm⟩
  · have hd : d = -((sw : ℤ) * (su : ℤ)) := by
      simpa using congrArg Neg.neg h
    exact ⟨-(sw * su), by simpa using hd.symm⟩

end MultilinearGap
