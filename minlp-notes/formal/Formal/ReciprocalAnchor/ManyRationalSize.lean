import Mathlib

/-! Bounds on the actual reduced numerator and denominator of rational arithmetic. -/

namespace ReciprocalAnchor

/-- Both components of a rational number use at most `B` binary digits. -/
def RationalBits (q : ℚ) (B : ℕ) : Prop :=
  q.num.natAbs < 2 ^ B ∧ q.den < 2 ^ B

theorem rationalBits_iff_size (q : ℚ) (B : ℕ) :
    RationalBits q B ↔ q.num.natAbs.size ≤ B ∧ q.den.size ≤ B := by
  simp [RationalBits, Nat.size_le]

/-- Reduction of a nonzero-denominator fraction cannot enlarge either component. -/
theorem reduced_fraction_bounds (n d : ℤ) (hd : d ≠ 0) :
    ((n : ℚ) / d).num.natAbs ≤ n.natAbs ∧
      ((n : ℚ) / d).den ≤ d.natAbs := by
  obtain ⟨c, hn, he⟩ := Rat.exists_eq_mul_div_num_and_eq_mul_div_den n hd
  have hc : c ≠ 0 := by
    intro h
    have hd0 : d = 0 := by simpa only [h, zero_mul] using he
    exact hd hd0
  have hc' : 1 ≤ c.natAbs := Nat.one_le_iff_ne_zero.mpr (Int.natAbs_ne_zero.mpr hc)
  constructor
  · conv_rhs => rw [hn, Int.natAbs_mul]
    exact Nat.le_mul_of_pos_left _ hc'
  · conv_rhs => rw [he, Int.natAbs_mul, Int.natAbs_natCast]
    exact Nat.le_mul_of_pos_left _ hc'

theorem rationalBits_fraction {n d : ℤ} {B : ℕ} (hd : d ≠ 0)
    (hn : n.natAbs < 2 ^ B) (hden : d.natAbs < 2 ^ B) :
    RationalBits ((n : ℚ) / d) B := by
  obtain ⟨hn', hd'⟩ := reduced_fraction_bounds n d hd
  exact ⟨hn'.trans_lt hn, hd'.trans_lt hden⟩

theorem rationalBits_pos {q : ℚ} {B : ℕ} (h : RationalBits q B) : 0 < B := by
  by_contra hb
  have hB : B = 0 := by omega
  have := q.den_pos
  simp [RationalBits, hB] at h

theorem rationalBits_mono {q : ℚ} {B C : ℕ} (h : RationalBits q B) (hBC : B ≤ C) :
    RationalBits q C := by
  have hp : 2 ^ B ≤ 2 ^ C := Nat.pow_le_pow_right (by decide) hBC
  exact ⟨h.1.trans_le hp, h.2.trans_le hp⟩

theorem rationalBits_neg {q : ℚ} {B : ℕ} (h : RationalBits q B) :
    RationalBits (-q) B := by simpa [RationalBits] using h

theorem rationalBits_zero : RationalBits 0 1 := by unfold RationalBits; decide

theorem rationalBits_one : RationalBits 1 1 := by unfold RationalBits; decide

theorem rationalBits_add {q r : ℚ} {B C : ℕ}
    (hq : RationalBits q B) (hr : RationalBits r C) :
    RationalBits (q + r) (B + C + 1) := by
  have he : q + r = ((q.num * r.den + r.num * q.den : ℤ) : ℚ) /
      ((q.den * r.den : ℕ) : ℚ) := by
    conv_lhs => rw [← Rat.num_div_den q, ← Rat.num_div_den r]
    push_cast
    rw [div_add_div _ _ (by exact_mod_cast q.den_nz) (by exact_mod_cast r.den_nz)]
    ring
  rw [he]
  have hd : (q.den : ℤ) * r.den ≠ 0 := mul_ne_zero (by exact_mod_cast q.den_nz)
    (by exact_mod_cast r.den_nz)
  have h1 := Nat.mul_lt_mul'' hq.1 hr.2
  have h2 := Nat.mul_lt_mul'' hr.1 hq.2
  have h3 := Nat.mul_lt_mul'' hq.2 hr.2
  have hn := Int.natAbs_add_le (q.num * r.den) (r.num * q.den)
  simp only [Int.natAbs_mul, Int.natAbs_natCast] at hn
  have hn' : (q.num * r.den + r.num * q.den : ℤ).natAbs < 2 ^ (B + C + 1) := by
    rw [pow_add, pow_add]
    norm_num
    nlinarith
  have hd' : ((q.den : ℤ) * r.den).natAbs < 2 ^ (B + C + 1) := by
    simp only [Int.natAbs_mul, Int.natAbs_natCast]
    rw [pow_add, pow_add]
    norm_num
    nlinarith [Nat.two_pow_pos (B + C)]
  simpa only [Int.cast_mul, Int.cast_natCast, Nat.cast_mul] using
    rationalBits_fraction hd hn' hd'

theorem rationalBits_sub {q r : ℚ} {B C : ℕ}
    (hq : RationalBits q B) (hr : RationalBits r C) :
    RationalBits (q - r) (B + C + 1) := by
  simpa [sub_eq_add_neg] using rationalBits_add hq (rationalBits_neg hr)

theorem rationalBits_mul {q r : ℚ} {B C : ℕ}
    (hq : RationalBits q B) (hr : RationalBits r C) :
    RationalBits (q * r) (B + C) := by
  have he : q * r = ((q.num * r.num : ℤ) : ℚ) /
      (((q.den : ℤ) * r.den : ℤ) : ℚ) := by
    push_cast
    rw [mul_div_mul_comm, Rat.num_div_den, Rat.num_div_den]
  rw [he]
  apply rationalBits_fraction
  · exact mul_ne_zero (by exact_mod_cast q.den_nz) (by exact_mod_cast r.den_nz)
  · simpa only [Int.natAbs_mul, pow_add] using Nat.mul_lt_mul'' hq.1 hr.1
  · simpa only [Int.natAbs_mul, Int.natAbs_natCast, pow_add] using
      Nat.mul_lt_mul'' hq.2 hr.2

theorem rationalBits_inv {q : ℚ} {B : ℕ} (hq : RationalBits q B) :
    RationalBits q⁻¹ B := by
  by_cases hq0 : q = 0
  · simpa [hq0] using rationalBits_mono rationalBits_zero (rationalBits_pos hq)
  · have hn : q.num ≠ 0 := by simpa using hq0
    have he : q⁻¹ = (q.den : ℚ) / q.num := by
      nth_rw 1 [← Rat.num_div_den q]
      rw [inv_div]
    rw [he]
    exact rationalBits_fraction hn (by simpa using hq.2) hq.1

theorem rationalBits_div {q r : ℚ} {B C : ℕ}
    (hq : RationalBits q B) (hr : RationalBits r C) :
    RationalBits (q / r) (B + C) := by
  simpa [div_eq_mul_inv] using rationalBits_mul hq (rationalBits_inv hr)

/-- Sequential summation has linear bit growth in the number of summands. -/
theorem rationalBits_list_sum {xs : List ℚ} {B : ℕ}
    (h : ∀ q ∈ xs, RationalBits q B) :
    RationalBits xs.sum (1 + xs.length * (B + 1)) := by
  induction xs with
  | nil => simpa using rationalBits_zero
  | cons q xs ih =>
    have hq := h q (by simp)
    have hx := ih (fun r hr => h r (by simp [hr]))
    have hs := rationalBits_add hq hx
    convert hs using 1 <;> simp [List.sum_cons, Nat.mul_add, Nat.add_mul]
    omega

/-- The same linear bound for a sum over any finite index set. -/
theorem rationalBits_finset_sum {ι : Type*} (s : Finset ι) (f : ι → ℚ) {B : ℕ}
    (h : ∀ i ∈ s, RationalBits (f i) B) :
    RationalBits (∑ i ∈ s, f i) (1 + s.card * (B + 1)) := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using rationalBits_zero
  | @insert i s hi ih =>
    have hi' := h i (by simp)
    have hs := ih (fun j hj => h j (by simp [hj]))
    have hsum := rationalBits_add hi' hs
    rw [Finset.sum_insert hi, Finset.card_insert_of_notMem hi]
    convert hsum using 1
    ring

/-- Intersections of two input affine lines have linear bit size. -/
theorem rationalBits_intersection {a b c d : ℚ} {B : ℕ}
    (ha : RationalBits a B) (hb : RationalBits b B)
    (hc : RationalBits c B) (hd : RationalBits d B) :
    RationalBits ((c - a) / (b - d)) (4 * B + 2) := by
  convert rationalBits_div (rationalBits_sub hc ha) (rationalBits_sub hb hd) using 1
  omega

/-- The exact affine-piece integral used for reciprocal separation has linear bit size. -/
theorem rationalBits_integral_piece {a b l r : ℚ} {B : ℕ}
    (ha : RationalBits a B) (hb : RationalBits b B)
    (hl : RationalBits l B) (hr : RationalBits r B) :
    RationalBits (a * (l⁻¹ * l⁻¹ - r⁻¹ * r⁻¹) +
      2 * b * (l⁻¹ - r⁻¹)) (8 * B + 5) := by
  have htwo : RationalBits 2 2 := by unfold RationalBits; decide
  have hl' := rationalBits_inv hl
  have hr' := rationalBits_inv hr
  have hfirst := rationalBits_mul ha
    (rationalBits_sub (rationalBits_mul hl' hl') (rationalBits_mul hr' hr'))
  have hsecond := rationalBits_mul (rationalBits_mul htwo hb) (rationalBits_sub hl' hr')
  convert rationalBits_add hfirst hsecond using 1
  omega

end ReciprocalAnchor
