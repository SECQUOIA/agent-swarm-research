import Mathlib

/-! Dyadic bisection uses only rational queries. The correctness interface is
instantiated by the computed characteristic-coefficient test in the final
matrix comparator; it is not an assumed real-number oracle there. -/
namespace DAGSpectral

def dyadicIndex (test : ℚ → Bool) (R : ℚ) : ℕ → ℕ
  | 0 => 0
  | t+1 =>
    let k := dyadicIndex test R t
    if test (R * (2*k+1) / (2:ℚ)^(t+1)) then 2*k+1 else 2*k

theorem dyadicIndex_lt (test : ℚ → Bool) (R : ℚ) (t : ℕ) :
    dyadicIndex test R t < 2^t := by
  induction t with
  | zero => simp [dyadicIndex]
  | succ t ih =>
    simp only [dyadicIndex, pow_succ]
    split_ifs <;> omega

def dyadicLower (test : ℚ → Bool) (R : ℚ) (t : ℕ) : ℚ :=
  R * dyadicIndex test R t / (2:ℚ)^t

theorem dyadicLower_bounds (test : ℚ → Bool) (R : ℚ) {val : ℝ}
    (_hR : 0 < R) (hval : 0 ≤ val) (hvalR : val ≤ (R : ℝ))
    (htest : ∀ q : ℚ, test q = true ↔ (q : ℝ) ≤ val) (t : ℕ) :
    (dyadicLower test R t : ℝ) ≤ val ∧
      val ≤ (dyadicLower test R t : ℝ) + (R : ℝ)/(2:ℝ)^t := by
  induction t with
  | zero => simpa [dyadicLower, dyadicIndex] using And.intro hval hvalR
  | succ t ih =>
    let k := dyadicIndex test R t
    let mid : ℚ := R*(2*k+1)/(2:ℚ)^(t+1)
    have hmid : (mid : ℝ) = (dyadicLower test R t : ℝ) + (R : ℝ)/(2:ℝ)^t/2 := by
      dsimp [mid, k, dyadicLower]
      push_cast
      rw [pow_succ]
      ring
    have hwidth : (R : ℝ)/(2:ℝ)^(t+1) = (R : ℝ)/(2:ℝ)^t/2 := by
      rw [pow_succ, div_mul_eq_div_div]
    by_cases hm : test mid = true
    · have hs : dyadicLower test R (t+1) = mid := by
        simp only [dyadicLower, dyadicIndex, k, mid] at hm ⊢
        rw [if_pos hm]
        push_cast
        rfl
      rw [hs, hmid, hwidth]
      have hl := (htest mid).mp hm
      rw [hmid] at hl
      constructor
      · exact hl
      · linarith [ih.2]
    · have hs : dyadicLower test R (t+1) = dyadicLower test R t := by
        simp only [dyadicLower, dyadicIndex, k, mid] at hm ⊢
        rw [if_neg hm]
        push_cast
        rw [pow_succ]
        ring
      rw [hs, hwidth]
      have hl : val < (mid : ℝ) := lt_of_not_ge (fun hh => hm ((htest mid).mpr hh))
      rw [hmid] at hl
      exact ⟨ih.1, hl.le⟩

/-- A proved separation excludes unequal values in the equality branch. -/
theorem compare_of_approximations {a b x y δ w : ℝ}
    (_hδ : 0 < δ) (_hw : 0 ≤ w) (hnarrow : 2 * w < δ)
    (ha : x ≤ a ∧ a ≤ x + w) (hb : y ≤ b ∧ b ≤ y + w)
    (hsep : a ≠ b → δ ≤ |a - b|) :
    (a = b ↔ |x - y| < δ - w) ∧
      (δ - w ≤ x - y → b < a) ∧ (δ - w ≤ y - x → a < b) := by
  constructor
  · constructor
    · intro he
      subst b
      apply abs_lt.mpr
      constructor <;> linarith [ha.1,ha.2,hb.1,hb.2]
    · intro he
      by_contra hn
      have hs := hsep hn
      rcases le_or_gt a b with hab | hab
      · rw [abs_of_nonpos (sub_nonpos.mpr hab)] at hs
        have he' := (abs_lt.mp he).1
        linarith [ha.1,ha.2,hb.1,hb.2]
      · rw [abs_of_nonneg (sub_nonneg.mpr hab.le)] at hs
        have he' := (abs_lt.mp he).2
        linarith [ha.1,ha.2,hb.1,hb.2]
  · constructor <;> intro h <;> linarith [ha.1,ha.2,hb.1,hb.2]

/-- The numerator bit length suffices; the loop count is logarithmic in the
rational ratio, rather than linear in its numerical magnitude. -/
def eigenBisectionDepth (R δ : ℚ) : ℕ := (4*R/δ).num.natAbs.size

theorem rat_le_natAbs_num (q : ℚ) : q ≤ (q.num.natAbs : ℚ) := by
  calc
    q ≤ |q| := le_abs_self q
    _ = (q.num.natAbs : ℚ) / q.den := by
      conv_lhs => rw [← q.num_div_den]
      rw [abs_div, abs_of_nonneg (show (0 : ℚ) ≤ q.den by positivity)]
      simp
    _ ≤ q.num.natAbs := by
      apply (div_le_iff₀ (by exact_mod_cast q.den_pos)).mpr
      have hden : (1 : ℚ) ≤ q.den := by exact_mod_cast q.den_pos
      nlinarith [show (0 : ℚ) ≤ q.num.natAbs by positivity]

theorem eigenBisectionDepth_narrow {R δ : ℚ} (hR : 0 < R) (hδ : 0 < δ) :
    2 * (R : ℝ)/(2:ℝ)^(eigenBisectionDepth R δ) < (δ : ℝ) := by
  have hn := Nat.lt_size_self (4*R/δ).num.natAbs
  have hpow : 4*R/δ < (2:ℚ)^(eigenBisectionDepth R δ) :=
    (rat_le_natAbs_num _).trans_lt (by exact_mod_cast hn)
  have hh := (div_lt_iff₀ hδ).mp hpow
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hh' : 4*(R : ℝ) < (2:ℝ)^(eigenBisectionDepth R δ)*(δ : ℝ) := by
    exact_mod_cast hh
  apply (div_lt_iff₀ (by positivity)).mpr
  nlinarith

end DAGSpectral
