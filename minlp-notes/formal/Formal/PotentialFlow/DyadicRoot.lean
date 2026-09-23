import Mathlib

/-!
# Dyadic upper enclosures of `k`-th roots of nonnegative rationals

For a nonnegative rational `a / b` and an exponent `k ≥ 1`, a dyadic upper enclosure of the
`k`-th root of `a / b` at precision `q` is `j / 2 ^ q`, where `j` is the least natural number
with `j ^ k * b ≥ a * 2 ^ (k * q)`.  Its excess over the exact root is less than `2 ^ (-q)`.

This file gives an explicit computable construction of `j`: a fuelled binary search for the
integer floor of a `k`-th root (`natFloorRoot`), followed by one exact upward comparison
(`dyadicRootUpper`).  No `Nat.find` is used, so the definition reduces in the kernel.  The
least-element property is `dyadicRootUpper_spec`, the enclosure property is
`dyadicRootUpper_ge`, and the accuracy statement is `dyadicRootUpper_excess`.  The rational
wrapper `dyadicRootUpperQ` restates both for an input `x : ℚ` with `0 ≤ x`.

This is claim `CC39` of the potential-flow certificate package, formalising `eq:a-cert-root`
of the certified-computation appendix.  Only correctness of the construction is claimed here;
no bit-cost model is formalised.
-/

namespace PotentialFlow

/-- Fuelled binary search for the integer floor of the `k`-th root of `n`.

Each step recurses on `n / 2 ^ k`, doubles the result, and corrects it by at most one.  The
`fuel` argument makes the recursion structural; `natFloorRoot` supplies enough of it. -/
def natFloorRootAux (k : ℕ) : ℕ → ℕ → ℕ
  | 0, _ => 0
  | fuel + 1, n =>
      if n = 0 then 0
      else
        let s := 2 * natFloorRootAux k fuel (n / 2 ^ k)
        if (s + 1) ^ k ≤ n then s + 1 else s

/-- With at least `n` units of fuel, `natFloorRootAux k fuel n` is the integer floor of the
`k`-th root of `n`. -/
theorem natFloorRootAux_spec (k : ℕ) (hk : 0 < k) :
    ∀ fuel n : ℕ, n ≤ fuel →
      natFloorRootAux k fuel n ^ k ≤ n ∧ n < (natFloorRootAux k fuel n + 1) ^ k := by
  have hk' : k ≠ 0 := hk.ne'
  intro fuel
  induction fuel with
  | zero =>
      intro n hn
      have hn0 : n = 0 := Nat.le_zero.mp hn
      subst hn0
      simp [natFloorRootAux, zero_pow hk']
  | succ fuel ih =>
      intro n hn
      by_cases h0 : n = 0
      · subst h0
        simp [natFloorRootAux, zero_pow hk']
      · have hpos : 0 < n := Nat.pos_of_ne_zero h0
        have hpow : 0 < 2 ^ k := Nat.two_pow_pos k
        have h2 : 1 < 2 ^ k := Nat.one_lt_two_pow hk'
        have hlt : n / 2 ^ k < n := Nat.div_lt_self hpos h2
        have hle : n / 2 ^ k ≤ fuel := by omega
        obtain ⟨ht1, ht2⟩ := ih _ hle
        set t := natFloorRootAux k fuel (n / 2 ^ k) with ht
        have hlow : (2 * t) ^ k ≤ n := by
          calc (2 * t) ^ k = 2 ^ k * t ^ k := by rw [mul_pow]
            _ ≤ 2 ^ k * (n / 2 ^ k) := Nat.mul_le_mul_left _ ht1
            _ ≤ n := Nat.mul_div_le n (2 ^ k)
        have hhigh : n < (2 * t + 2) ^ k := by
          have hstep : n < (n / 2 ^ k + 1) * 2 ^ k :=
            (Nat.div_lt_iff_lt_mul hpow).mp (Nat.lt_succ_self _)
          calc n < (n / 2 ^ k + 1) * 2 ^ k := hstep
            _ ≤ (t + 1) ^ k * 2 ^ k := Nat.mul_le_mul_right _ ht2
            _ = (2 * (t + 1)) ^ k := by rw [mul_pow]; ring
            _ = (2 * t + 2) ^ k := by ring_nf
        simp only [natFloorRootAux, if_neg h0, ← ht]
        split
        · next hcase =>
            refine ⟨hcase, ?_⟩
            have hrw : 2 * t + 1 + 1 = 2 * t + 2 := by omega
            rw [hrw]
            exact hhigh
        · next hcase =>
            exact ⟨hlow, Nat.lt_of_not_le hcase⟩

/-- The integer floor of the `k`-th root of `n`, computed by binary search. -/
def natFloorRoot (k n : ℕ) : ℕ := natFloorRootAux k n n

/-- `natFloorRoot k n` is the integer floor of the `k`-th root of `n`, for `0 < k`. -/
theorem natFloorRoot_spec (k n : ℕ) (hk : 0 < k) :
    natFloorRoot k n ^ k ≤ n ∧ n < (natFloorRoot k n + 1) ^ k :=
  natFloorRootAux_spec k hk n n le_rfl

/-- The numerator of the dyadic upper enclosure of the `k`-th root of `a / b` at precision
`q`: the least `j : ℕ` with `a * 2 ^ (k * q) ≤ j ^ k * b`.

It is computed as the integer floor of the `k`-th root of `a * 2 ^ (k * q) / b`, corrected
upwards by one when that floor does not already satisfy the exact inequality. -/
def dyadicRootUpper (a b k q : ℕ) : ℕ :=
  let r := natFloorRoot k (a * 2 ^ (k * q) / b)
  if a * 2 ^ (k * q) ≤ r ^ k * b then r else r + 1

/-- `dyadicRootUpper a b k q` is the least natural number `j` satisfying the exact integer
test `a * 2 ^ (k * q) ≤ j ^ k * b` of `eq:a-cert-root`. -/
theorem dyadicRootUpper_spec (a b k q : ℕ) (hb : 0 < b) (hk : 0 < k) :
    IsLeast {j : ℕ | a * 2 ^ (k * q) ≤ j ^ k * b} (dyadicRootUpper a b k q) := by
  obtain ⟨hr1, hr2⟩ := natFloorRoot_spec k (a * 2 ^ (k * q) / b) hk
  set r := natFloorRoot k (a * 2 ^ (k * q) / b) with hrdef
  have hmem : a * 2 ^ (k * q) ≤ (r + 1) ^ k * b := by
    have hstep : a * 2 ^ (k * q) < (a * 2 ^ (k * q) / b + 1) * b :=
      (Nat.div_lt_iff_lt_mul hb).mp (Nat.lt_succ_self _)
    have hmono : (a * 2 ^ (k * q) / b + 1) * b ≤ (r + 1) ^ k * b :=
      Nat.mul_le_mul_right _ hr2
    omega
  have hlower : ∀ j : ℕ, a * 2 ^ (k * q) ≤ j ^ k * b → r ≤ j := by
    intro j hj
    have hdiv : a * 2 ^ (k * q) / b ≤ j ^ k := by
      have := Nat.div_le_div_right (c := b) hj
      rwa [Nat.mul_div_cancel _ hb] at this
    exact (Nat.pow_le_pow_iff_left hk.ne').mp (hr1.trans hdiv)
  simp only [dyadicRootUpper, ← hrdef]
  split
  · next hcase =>
      exact ⟨hcase, fun j hj => hlower j hj⟩
  · next hcase =>
      refine ⟨hmem, fun j hj => ?_⟩
      have hrj : r ≤ j := hlower j hj
      rcases eq_or_lt_of_le hrj with heq | hlt
      · exact absurd (heq ▸ hj) hcase
      · exact hlt

/-- The dyadic number `j / 2 ^ q` built from `j = dyadicRootUpper a b k q` lies above the
exact `k`-th root of `a / b`: its `k`-th power is at least `a / b`. -/
theorem dyadicRootUpper_ge (a b k q : ℕ) (hb : 0 < b) (hk : 0 < k) :
    (a : ℝ) / b ≤ ((dyadicRootUpper a b k q : ℝ) / 2 ^ q) ^ k := by
  have h := (dyadicRootUpper_spec a b k q hb hk).1
  have hbR : (0 : ℝ) < b := by exact_mod_cast hb
  have hR : (a : ℝ) * 2 ^ (k * q) ≤ (dyadicRootUpper a b k q : ℝ) ^ k * b := by
    exact_mod_cast h
  rw [div_pow, ← pow_mul, mul_comm q k, div_le_div_iff₀ hbR (by positivity)]
  exact hR

/-- Accuracy of the dyadic enclosure: there is an exact `k`-th root `r ≥ 0` of `a / b`, the
enclosure `j / 2 ^ q` is at least `r`, and it exceeds `r` by less than `2 ^ (-q)`. -/
theorem dyadicRootUpper_excess (a b k q : ℕ) (hb : 0 < b) (hk : 0 < k) :
    ∃ r : ℝ, 0 ≤ r ∧ r ^ k = (a : ℝ) / b ∧
      r ≤ (dyadicRootUpper a b k q : ℝ) / 2 ^ q ∧
      (dyadicRootUpper a b k q : ℝ) / 2 ^ q < r + 1 / 2 ^ q := by
  have hbR : (0 : ℝ) < b := by exact_mod_cast hb
  have hx : (0 : ℝ) ≤ (a : ℝ) / b := by positivity
  refine ⟨((a : ℝ) / b) ^ ((k : ℝ)⁻¹), Real.rpow_nonneg hx _,
    Real.rpow_inv_natCast_pow hx hk.ne', ?_, ?_⟩
  · refine le_of_pow_le_pow_left₀ hk.ne' (by positivity) ?_
    rw [Real.rpow_inv_natCast_pow hx hk.ne']
    exact dyadicRootUpper_ge a b k q hb hk
  · set r := ((a : ℝ) / b) ^ ((k : ℝ)⁻¹) with hrdef
    have hrnn : 0 ≤ r := Real.rpow_nonneg hx _
    have hrpow : r ^ k = (a : ℝ) / b := Real.rpow_inv_natCast_pow hx hk.ne'
    rcases Nat.eq_zero_or_pos (dyadicRootUpper a b k q) with hj0 | hjpos
    · have hq : (0 : ℝ) < 1 / 2 ^ q := by positivity
      rw [hj0]
      simp only [Nat.cast_zero, zero_div]
      linarith
    · obtain ⟨i, hi⟩ := Nat.exists_eq_succ_of_ne_zero hjpos.ne'
      have hnotmem : ¬ a * 2 ^ (k * q) ≤ i ^ k * b := by
        intro hmem
        have := (dyadicRootUpper_spec a b k q hb hk).2 hmem
        omega
      have hcast : (i : ℝ) ^ k * b < (a : ℝ) * 2 ^ (k * q) := by
        have : i ^ k * b < a * 2 ^ (k * q) := Nat.lt_of_not_le hnotmem
        exact_mod_cast this
      have hstrict : ((i : ℝ) / 2 ^ q) ^ k < (a : ℝ) / b := by
        rw [div_pow, ← pow_mul, mul_comm q k, div_lt_div_iff₀ (by positivity) hbR]
        exact hcast
      have hlt : (i : ℝ) / 2 ^ q < r := by
        rw [← hrpow] at hstrict
        exact (pow_lt_pow_iff_left₀ (by positivity) hrnn hk.ne').mp hstrict
      have hsplit : (dyadicRootUpper a b k q : ℝ) / 2 ^ q = (i : ℝ) / 2 ^ q + 1 / 2 ^ q := by
        rw [hi]
        push_cast
        ring
      rw [hsplit]
      linarith

/-- The dyadic upper enclosure of the `k`-th root of a nonnegative rational `x`, at
precision `q`, as a rational number. -/
def dyadicRootUpperQ (x : ℚ) (k q : ℕ) : ℚ :=
  (dyadicRootUpper x.num.toNat x.den k q : ℚ) / 2 ^ q

/-- For `0 ≤ x`, the natural-number data `x.num.toNat` and `x.den` present `x` itself. -/
theorem cast_numToNat_div_den {x : ℚ} (hx : 0 ≤ x) :
    ((x.num.toNat : ℝ)) / (x.den : ℝ) = (x : ℝ) := by
  have hnum : ((x.num.toNat : ℤ) : ℝ) = (x.num : ℝ) := by
    rw [Int.toNat_of_nonneg (Rat.num_nonneg.mpr hx)]
  rw [Rat.cast_def]
  push_cast at hnum ⊢
  rw [hnum]

/-- The rational enclosure is above the exact `k`-th root of `x`. -/
theorem dyadicRootUpperQ_ge {x : ℚ} (hx : 0 ≤ x) (k q : ℕ) (hk : 0 < k) :
    (x : ℝ) ≤ ((dyadicRootUpperQ x k q : ℚ) : ℝ) ^ k := by
  have hden : 0 < x.den := x.den_pos
  have h := dyadicRootUpper_ge x.num.toNat x.den k q hden hk
  rw [cast_numToNat_div_den hx] at h
  have hcast : ((dyadicRootUpperQ x k q : ℚ) : ℝ)
      = (dyadicRootUpper x.num.toNat x.den k q : ℝ) / 2 ^ q := by
    rw [dyadicRootUpperQ]
    push_cast
    ring
  rw [hcast]
  exact h

/-- Accuracy of the rational enclosure: it lies above the exact `k`-th root of `x` and
exceeds it by less than `2 ^ (-q)`. -/
theorem dyadicRootUpperQ_excess {x : ℚ} (hx : 0 ≤ x) (k q : ℕ) (hk : 0 < k) :
    ∃ r : ℝ, 0 ≤ r ∧ r ^ k = (x : ℝ) ∧
      r ≤ ((dyadicRootUpperQ x k q : ℚ) : ℝ) ∧
      ((dyadicRootUpperQ x k q : ℚ) : ℝ) < r + 1 / 2 ^ q := by
  have hden : 0 < x.den := x.den_pos
  obtain ⟨r, hr0, hrpow, hrle, hrlt⟩ :=
    dyadicRootUpper_excess x.num.toNat x.den k q hden hk
  have hcast : ((dyadicRootUpperQ x k q : ℚ) : ℝ)
      = (dyadicRootUpper x.num.toNat x.den k q : ℝ) / 2 ^ q := by
    rw [dyadicRootUpperQ]
    push_cast
    ring
  rw [cast_numToNat_div_den hx] at hrpow
  exact ⟨r, hr0, hrpow, by rw [hcast]; exact hrle, by rw [hcast]; exact hrlt⟩

/-- Sanity check: the cube-root enclosure of `2` at `q = 4` is `21 / 16`, since
`20 ^ 3 = 8000 < 8192 = 2 * 2 ^ 12 ≤ 9261 = 21 ^ 3`. -/
theorem dyadicRootUpper_cube_two : dyadicRootUpper 2 1 3 4 = 21 := by decide +kernel

/-- Sanity check: the square-root enclosure of `2` at `q = 4` is `23 / 16`. -/
theorem dyadicRootUpper_sqrt_two : dyadicRootUpper 2 1 2 4 = 23 := by decide +kernel

/-- Sanity check: a zero numerator gives the zero enclosure. -/
theorem dyadicRootUpper_zero_num : dyadicRootUpper 0 5 2 3 = 0 := by decide +kernel

/-- Sanity check: at `q = 0` the square-root enclosure of `2` is the integer `2`. -/
theorem dyadicRootUpper_sqrt_two_zero : dyadicRootUpper 2 1 2 0 = 2 := by decide +kernel

/-- Sanity check with a nontrivial denominator: the square-root enclosure of `7 / 3` at
`q = 5` is `49 / 32`. -/
theorem dyadicRootUpper_sqrt_seven_thirds : dyadicRootUpper 7 3 2 5 = 49 := by decide +kernel

end PotentialFlow
