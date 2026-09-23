import Formal.ReciprocalAnchor.ManyRationalSize

/-! A bounded rational-comparison producer for dyadic normalization. -/
namespace DAGSpectral
open ReciprocalAnchor

/-- Double the current positive scale until its squared weighted value reaches one.
The fuel is explicit, so the computation never performs an unbounded search. -/
def dyadicSearch (w : ℚ) : ℕ → ℚ → ℚ
  | 0, q => q
  | n+1, q => if 1 ≤ q ^ 2 * w then q else dyadicSearch w n (2 * q)

theorem dyadicSearch_spec (w : ℚ) (n : ℕ) (q : ℚ) (hq : 0 < q)
    (hupper : q ^ 2 * w < 4) (hreach : 1 ≤ ((2 : ℚ) ^ n * q) ^ 2 * w) :
    0 < dyadicSearch w n q ∧
      1 ≤ (dyadicSearch w n q) ^ 2 * w ∧ (dyadicSearch w n q) ^ 2 * w < 4 := by
  induction n generalizing q with
  | zero => simpa [dyadicSearch] using And.intro hq (And.intro hreach hupper)
  | succ n ih =>
    simp only [dyadicSearch]
    split_ifs with h
    · exact ⟨hq,h,hupper⟩
    · apply ih (2 * q) (by positivity)
      · have hh : q ^ 2 * w < 1 := lt_of_not_ge h
        nlinarith
      · convert hreach using 1
        rw [pow_succ]
        ring

theorem dyadicSearch_power (w : ℚ) (n : ℕ) (q : ℚ) :
    ∃ k ≤ n, dyadicSearch w n q = (2 : ℚ) ^ k * q := by
  induction n generalizing q with
  | zero => exact ⟨0,le_rfl,by simp [dyadicSearch]⟩
  | succ n ih =>
    simp only [dyadicSearch]
    split_ifs
    · exact ⟨0,by omega,by simp⟩
    · obtain ⟨k,hk,he⟩ := ih (2 * q)
      refine ⟨k+1,by omega,?_⟩
      rw [he,pow_succ]
      ring

/-- A positive rational with B-bit components lies strictly between 2 ^ -B and 2 ^ B. -/
theorem positive_rational_magnitude {w : ℚ} {B : ℕ}
    (hw : 0 < w) (hb : RationalBits w B) :
    w < (2 : ℚ) ^ B ∧ 1 < w * (2 : ℚ) ^ B := by
  have hn : 1 ≤ w.num := Rat.num_pos.mpr hw
  have hd : (0 : ℚ) < w.den := by exact_mod_cast w.den_pos
  have hd1 : (1 : ℚ) ≤ w.den := by exact_mod_cast w.den_pos
  have hn1 : (1 : ℚ) ≤ w.num := by exact_mod_cast hn
  have hnB : (w.num : ℚ) < (2 : ℚ) ^ B := by
    have hnabs : (w.num : ℚ) = (w.num.natAbs : ℚ) := by
      rw [Nat.cast_natAbs, abs_of_nonneg (by omega : (0 : ℤ) ≤ w.num)]
    have hcast : (w.num.natAbs : ℚ) < (2 : ℚ) ^ B := by exact_mod_cast hb.1
    rw [hnabs]
    exact hcast
  have hdB : (w.den : ℚ) < (2 : ℚ) ^ B := by exact_mod_cast hb.2
  rw [← Rat.num_div_den w]
  constructor
  · apply (div_lt_iff₀ hd).2
    nlinarith [pow_pos (by norm_num : (0 : ℚ)<2) B]
  · rw [div_mul_eq_mul_div]
    apply (lt_div_iff₀ hd).2
    change (1 : ℚ) * (w.den : ℚ) < (w.num : ℚ) * (2 : ℚ) ^ B
    nlinarith [pow_pos (by norm_num : (0 : ℚ)<2) B]

/-- The entire scale computation uses at most 2B comparisons and doublings. -/
def dyadicScale (w : ℚ) (B : ℕ) : ℚ := dyadicSearch w (2 * B) ((2 : ℚ) ^ B)⁻¹

theorem dyadicScale_spec {w : ℚ} {B : ℕ} (hw : 0 < w) (hb : RationalBits w B) :
    0 < dyadicScale w B ∧ 1 ≤ (dyadicScale w B) ^ 2 * w ∧ (dyadicScale w B) ^ 2 * w < 4 := by
  have hp : (0 : ℚ) < (2 : ℚ) ^ B := pow_pos (by norm_num) _
  have hp1 : (1 : ℚ) ≤ (2 : ℚ) ^ B := one_le_pow₀ (by norm_num)
  obtain ⟨hu,hl⟩ := positive_rational_magnitude hw hb
  apply dyadicSearch_spec w (2 * B) _ (by positivity)
  · rw [inv_pow, inv_mul_lt_iff₀ (by positivity)]
    nlinarith [sq_nonneg ((2 : ℚ) ^ B-1)]
  · have he : (2 : ℚ) ^ (2 * B) * ((2 : ℚ) ^ B)⁻¹ = (2 : ℚ) ^ B := by
      rw [two_mul,pow_add]
      field_simp
    rw [he]
    nlinarith [mul_nonneg hw.le (sub_nonneg.mpr hp1)]

theorem dyadicScale_power {w : ℚ} {B : ℕ} :
    ∃ z : ℤ, -(B : ℤ) ≤ z ∧ z ≤ B ∧ dyadicScale w B = (2 : ℚ) ^ z := by
  obtain ⟨k,hk,he⟩ := dyadicSearch_power w (2 * B) ((2 : ℚ) ^ B)⁻¹
  refine ⟨(k : ℤ)-B,by omega,by omega,?_⟩
  change dyadicSearch w (2 * B) _ = _
  rw [he,zpow_sub₀ (by norm_num)]
  simp [div_eq_mul_inv]

end DAGSpectral
