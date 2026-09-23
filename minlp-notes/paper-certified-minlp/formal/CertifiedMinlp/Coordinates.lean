import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-! Rational coordinate boxes and a finite enclosure correction. Infinite endpoints
are represented by constructors, never by real-valued sentinels. -/
namespace CertifiedMinlp

inductive Coordinate where
  | bounded (lower upper : ℚ)
  | lowerBounded (lower : ℚ)
  | upperBounded (upper : ℚ)
  | free
  deriving DecidableEq

def Coordinate.contains (B : Coordinate) (x : ℝ) : Prop :=
  match B with
  | .bounded L U => (L : ℝ) ≤ x ∧ x ≤ (U : ℝ)
  | .lowerBounded L => (L : ℝ) ≤ x
  | .upperBounded U => x ≤ (U : ℝ)
  | .free => True

/-- The enclosure sign condition makes the correction finite. -/
def Coordinate.accepts (B : Coordinate) (lo hi : ℚ) : Prop :=
  lo ≤ hi ∧ match B with
  | .bounded _ _ => True
  | .lowerBounded _ => 0 ≤ lo
  | .upperBounded _ => hi ≤ 0
  | .free => lo = 0 ∧ hi = 0

/-- A rational upper bound on d(z-x), assuming acceptance and enclosures. -/
def Coordinate.correction (B : Coordinate) (z lo hi : ℚ) : ℚ :=
  match B with
  | .bounded L U => max (hi * (z - L)) (lo * (z - U))
  | .lowerBounded L => hi * (z - L)
  | .upperBounded U => lo * (z - U)
  | .free => 0

theorem bounded_shift_le (L U z x d lo hi : ℝ)
    (hxL : L ≤ x) (hxU : x ≤ U) (hzL : L ≤ z) (hzU : z ≤ U)
    (hdL : lo ≤ d) (hdU : d ≤ hi) :
    d * (z - x) ≤ max (hi * (z - L)) (lo * (z - U)) := by
  rcases le_total 0 d with hd | hd
  · have h₁ := mul_le_mul_of_nonneg_left (sub_le_sub_left hxL z) hd
    have h₂ := mul_le_mul_of_nonneg_right hdU (sub_nonneg.mpr hzL)
    exact le_trans (le_trans h₁ h₂) (le_max_left _ _)
  · have h₁ := mul_le_mul_of_nonpos_left (sub_le_sub_left hxU z) hd
    have h₂ := mul_le_mul_of_nonpos_right hdL (sub_nonpos.mpr hzU)
    exact le_trans (le_trans h₁ h₂) (le_max_right _ _)

theorem lower_shift_le (L z x d lo hi : ℝ)
    (hx : L ≤ x) (hz : L ≤ z) (hsign : 0 ≤ lo)
    (hdL : lo ≤ d) (hdU : d ≤ hi) : d * (z - x) ≤ hi * (z - L) := by
  exact le_trans (mul_le_mul_of_nonneg_left (sub_le_sub_left hx z)
    (le_trans hsign hdL)) (mul_le_mul_of_nonneg_right hdU (sub_nonneg.mpr hz))

theorem upper_shift_le (U z x d lo hi : ℝ)
    (hx : x ≤ U) (hz : z ≤ U) (hsign : hi ≤ 0)
    (hdL : lo ≤ d) (hdU : d ≤ hi) : d * (z - x) ≤ lo * (z - U) := by
  exact le_trans (mul_le_mul_of_nonpos_left (sub_le_sub_left hx z)
    (le_trans hdU hsign)) (mul_le_mul_of_nonpos_right hdL (sub_nonpos.mpr hz))

theorem coordinate_correction_sound (B : Coordinate) (z lo hi : ℚ) (x d : ℝ)
    (hz : B.contains z) (hx : B.contains x) (ha : B.accepts lo hi)
    (hdL : (lo : ℝ) ≤ d) (hdU : d ≤ (hi : ℝ)) :
    d * ((z : ℝ) - x) ≤ (B.correction z lo hi : ℝ) := by
  cases B with
  | bounded L U =>
    simpa only [Coordinate.correction, Rat.cast_max, Rat.cast_mul, Rat.cast_sub] using
      bounded_shift_le L U z x d lo hi hx.1 hx.2 hz.1 hz.2 hdL hdU
  | lowerBounded L =>
    have hs : (0 : ℝ) ≤ (lo : ℝ) := by exact_mod_cast ha.2
    simpa only [Coordinate.correction, Rat.cast_mul, Rat.cast_sub] using
      lower_shift_le L z x d lo hi hx hz hs hdL hdU
  | upperBounded U =>
    have hs : (hi : ℝ) ≤ (0 : ℝ) := by exact_mod_cast ha.2
    simpa only [Coordinate.correction, Rat.cast_mul, Rat.cast_sub] using
      upper_shift_le U z x d lo hi hx hz hs hdL hdU
  | free =>
    have hd : d = 0 := by
      obtain ⟨hlo, hhi⟩ := ha.2
      rw [hlo, Rat.cast_zero] at hdL
      rw [hhi, Rat.cast_zero] at hdU
      exact le_antisymm hdU hdL
    simp [hd, Coordinate.correction]

theorem fixed_correction (z lo hi : ℚ) :
    (Coordinate.bounded z z).correction z lo hi = 0 := by
  simp [Coordinate.correction]

/-- A feasible support coordinate makes each accepted correction nonnegative. -/
theorem correction_nonneg (B : Coordinate) (z lo hi : ℚ) (d : ℝ)
    (hz : B.contains z) (ha : B.accepts lo hi)
    (hdL : (lo : ℝ) ≤ d) (hdU : d ≤ (hi : ℝ)) :
    0 ≤ B.correction z lo hi := by
  have h := coordinate_correction_sound B z lo hi z d hz hz ha hdL hdU
  simp only [sub_self, mul_zero] at h
  exact_mod_cast h

end CertifiedMinlp
