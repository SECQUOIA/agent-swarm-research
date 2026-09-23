import Formal.NetworkSimplex.ThreeState
import Formal.ReciprocalAnchor.ManyRationalSize

/-! Executable rational witnesses for the one-, two-, and three-coordinate profiles.
All formulas use only addition, subtraction, and ordered selection, and allow equality. -/

namespace NetworkSimplex
namespace SmallRecovery

open ReciprocalAnchor

def oneProfile (l ls : ℚ) : ℚ := max l ls

theorem oneProfile_correct {l u ls us : ℚ}
    (h : max l ls ≤ min u us) :
    l ≤ oneProfile l ls ∧ oneProfile l ls ≤ u ∧
      ls ≤ oneProfile l ls ∧ oneProfile l ls ≤ us := by
  exact ⟨le_max_left _ _, (le_min_iff.mp h).1, le_max_right _ _,
    (le_min_iff.mp h).2⟩

def twoProfile (l₁ u₂ l₂ ls : ℚ) : ℚ × ℚ :=
  let s := max ls (l₁ + l₂)
  let x := max l₁ (s - u₂)
  (x, s - x)

@[simp] theorem cast_max (a b : ℚ) : ((max a b : ℚ) : ℝ) = max (a : ℝ) b := by
  rcases le_total a b with h | h
  · rw [max_eq_right h, max_eq_right (by exact_mod_cast h)]
  · rw [max_eq_left h, max_eq_left (by exact_mod_cast h)]

@[simp] theorem cast_min (a b : ℚ) : ((min a b : ℚ) : ℝ) = min (a : ℝ) b := by
  rcases le_total a b with h | h
  · rw [min_eq_left h, min_eq_left (by exact_mod_cast h)]
  · rw [min_eq_right h, min_eq_right (by exact_mod_cast h)]

theorem twoProfile_correct {l₁ u₁ l₂ u₂ ls us : ℚ}
    (h : FiveTests l₁ u₁ l₂ u₂ ls us) :
    Hexagon l₁ u₁ l₂ u₂ ls us
      (twoProfile l₁ u₂ l₂ ls).1 (twoProfile l₁ u₂ l₂ ls).2 := by
  simpa [twoProfile] using five_tests_witness h

structure RationalThreeBounds where
  l1 : ℚ
  l2 : ℚ
  l3 : ℚ
  ls : ℚ
  u1 : ℚ
  u2 : ℚ
  u3 : ℚ
  u12 : ℚ
  u13 : ℚ
  u23 : ℚ
  us : ℚ

def RationalThreeBounds.toReal (b : RationalThreeBounds) : ThreeStateBounds :=
  ⟨b.l1, b.l2, b.l3, b.ls, b.u1, b.u2, b.u3, b.u12, b.u13, b.u23, b.us⟩

def threeProfile (b : RationalThreeBounds) : ℚ × ℚ × ℚ :=
  let xy := twoProfile (max b.l1 (b.ls - b.u23)) (min b.u2 (b.u23 - b.l3))
    (max b.l2 (b.ls - b.u13)) (b.ls - b.u3)
  (xy.1, xy.2, max b.l3 (b.ls - xy.1 - xy.2))

theorem threeProfile_correct {b : RationalThreeBounds}
    (h : b.toReal.SixteenTests) :
    b.toReal.Feasible (threeProfile b).1 (threeProfile b).2.1
      (threeProfile b).2.2 := by
  rcases h with ⟨h1, h2, h3, h12, h13, h23, hs, hss, hs1, hs2, hs3,
    hs123, hsp1, hsp2, hsp3, hsp⟩
  simp only [RationalThreeBounds.toReal] at *
  have hfive : FiveTests
      (max (b.l1 : ℝ) (b.ls - b.u23)) (min (b.u1 : ℝ) (b.u13 - b.l3))
      (max (b.l2 : ℝ) (b.ls - b.u13)) (min (b.u2 : ℝ) (b.u23 - b.l3))
      (b.ls - b.u3) (min (b.u12 : ℝ) (b.us - b.l3)) := by
    unfold FiveTests
    and_intros
    all_goals simp only [max_def, min_def]; split_ifs <;> linarith
  have hfiveQ : FiveTests
      ((max b.l1 (b.ls - b.u23) : ℚ) : ℝ)
      ((min b.u1 (b.u13 - b.l3) : ℚ) : ℝ)
      ((max b.l2 (b.ls - b.u13) : ℚ) : ℝ)
      ((min b.u2 (b.u23 - b.l3) : ℚ) : ℝ)
      ((b.ls - b.u3 : ℚ) : ℝ) ((min b.u12 (b.us - b.l3) : ℚ) : ℝ) := by
    simpa using hfive
  have hxy := twoProfile_correct hfiveQ
  rcases hxy with ⟨hxlo, hxhi, hylo, hyhi, hslo, hshi⟩
  simp only [cast_max, cast_min, Rat.cast_sub, max_le_iff, le_min_iff]
    at hxlo hxhi hylo hyhi hshi
  rcases hxlo with ⟨hxlo1, hxlo2⟩
  rcases hxhi with ⟨hxhi1, hxhi2⟩
  rcases hylo with ⟨hylo1, hylo2⟩
  rcases hyhi with ⟨hyhi1, hyhi2⟩
  rcases hshi with ⟨hshi1, hshi2⟩
  simp only [Rat.cast_sub] at hslo
  unfold ThreeStateBounds.Feasible threeProfile
  simp only [cast_max, Rat.cast_sub]
  generalize twoProfile (max b.l1 (b.ls - b.u23)) (min b.u2 (b.u23 - b.l3))
    (max b.l2 (b.ls - b.u13)) (b.ls - b.u3) = xy at *
  simp only [max_def]
  split_ifs <;> (and_intros <;> linarith)


/-- One rational arithmetic operation or ordered selection costs one unit.
Tuple construction, sharing, and state bookkeeping are not charged. -/
private def operation {α : Type} (v : α) : StateM ℕ α := fun s => (v, s + 1)

def oneProfileCounted (l ls : ℚ) : StateM ℕ ℚ := operation (max l ls)

def twoProfileCounted (l₁ u₂ l₂ ls : ℚ) : StateM ℕ (ℚ × ℚ) := do
  let sum ← operation (l₁ + l₂)
  let s ← operation (max ls sum)
  let lower ← operation (s - u₂)
  let x ← operation (max l₁ lower)
  let y ← operation (s - x)
  pure (x, y)

def threeProfileCounted (b : RationalThreeBounds) : StateM ℕ (ℚ × ℚ × ℚ) := do
  let lo1 ← operation (b.ls - b.u23)
  let l1 ← operation (max b.l1 lo1)
  let hi2 ← operation (b.u23 - b.l3)
  let u2 ← operation (min b.u2 hi2)
  let lo2 ← operation (b.ls - b.u13)
  let l2 ← operation (max b.l2 lo2)
  let ls ← operation (b.ls - b.u3)
  let xy ← twoProfileCounted l1 u2 l2 ls
  let rest ← operation (b.ls - xy.1)
  let lower ← operation (rest - xy.2)
  let z ← operation (max b.l3 lower)
  pure (xy.1, xy.2, z)

theorem oneProfileCounted_exact (l ls : ℚ) :
    (oneProfileCounted l ls).run 0 = (oneProfile l ls, 1) := rfl

theorem twoProfileCounted_exact (l₁ u₂ l₂ ls : ℚ) :
    (twoProfileCounted l₁ u₂ l₂ ls).run 0 = (twoProfile l₁ u₂ l₂ ls, 5) := rfl

theorem threeProfileCounted_exact (b : RationalThreeBounds) :
    (threeProfileCounted b).run 0 = (threeProfile b, 15) := rfl

private theorem bits_max {a b : ℚ} {B : ℕ}
    (ha : RationalBits a B) (hb : RationalBits b B) : RationalBits (max a b) B := by
  rcases le_total a b with h | h
  · simpa [max_eq_right h] using hb
  · simpa [max_eq_left h] using ha

private theorem bits_min {a b : ℚ} {B : ℕ}
    (ha : RationalBits a B) (hb : RationalBits b B) : RationalBits (min a b) B := by
  rcases le_total a b with h | h
  · simpa [min_eq_left h] using ha
  · simpa [min_eq_right h] using hb

theorem oneProfile_bits {l ls : ℚ} {B : ℕ}
    (hl : RationalBits l B) (hls : RationalBits ls B) :
    RationalBits (oneProfile l ls) B := bits_max hl hls

theorem twoProfile_bits {l₁ u₂ l₂ ls : ℚ} {B : ℕ}
    (h1 : RationalBits l₁ B) (hu : RationalBits u₂ B)
    (h2 : RationalBits l₂ B) (hs : RationalBits ls B) :
    RationalBits (twoProfile l₁ u₂ l₂ ls).1 (8 * B + 7) ∧
    RationalBits (twoProfile l₁ u₂ l₂ ls).2 (8 * B + 7) := by
  have hsum := rationalBits_add h1 h2
  have ht := bits_max (rationalBits_mono hs (by omega)) hsum
  have hx := bits_max (rationalBits_mono h1 (by omega)) (rationalBits_sub ht hu)
  have hy := rationalBits_sub ht hx
  exact ⟨rationalBits_mono hx (by omega), rationalBits_mono hy (by omega)⟩

def RationalThreeBounds.Bits (b : RationalThreeBounds) (B : ℕ) : Prop :=
  RationalBits b.l1 B ∧ RationalBits b.l2 B ∧ RationalBits b.l3 B ∧
  RationalBits b.ls B ∧ RationalBits b.u1 B ∧ RationalBits b.u2 B ∧
  RationalBits b.u3 B ∧ RationalBits b.u12 B ∧ RationalBits b.u13 B ∧
  RationalBits b.u23 B ∧ RationalBits b.us B

theorem threeProfile_bits {b : RationalThreeBounds} {B : ℕ}
    (h : b.Bits B) :
    RationalBits (threeProfile b).1 (64 * B + 63) ∧
    RationalBits (threeProfile b).2.1 (64 * B + 63) ∧
    RationalBits (threeProfile b).2.2 (64 * B + 63) := by
  rcases h with ⟨h1, h2, h3, hs, _, hu2, hu3, _, hu13, hu23, _⟩
  have ha := bits_max (rationalBits_mono h1 (by omega)) (rationalBits_sub hs hu23)
  have hb := bits_min (rationalBits_mono hu2 (by omega)) (rationalBits_sub hu23 h3)
  have hc := bits_max (rationalBits_mono h2 (by omega)) (rationalBits_sub hs hu13)
  have hd := rationalBits_sub hs hu3
  obtain ⟨hx, hy⟩ := twoProfile_bits ha hb hc hd
  have hz := bits_max (rationalBits_mono h3 (by omega))
    (rationalBits_sub (rationalBits_sub hs hx) hy)
  exact ⟨rationalBits_mono hx (by omega), rationalBits_mono hy (by omega),
    rationalBits_mono hz (by omega)⟩

end SmallRecovery
end NetworkSimplex
