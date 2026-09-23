import Mathlib

/-!
# Scalar-dilation certificate: verified scaled-integer series evaluator

The power series behind `Y` is

  `Y z = ∑ j, (2 - 2⁻ʲ) * z ^ (2 * j + 1) / (2 * j + 1) = z * ∑ j, cⱼ * z ^ (2 * j)`

with rational coefficients `cⱼ = (2 ^ (j + 1) - 1) / (2 ^ j * (2 * j + 1))`.

This file provides two `ℕ`-valued accumulators, `accLo` (round down) and `accHi`
(round up), that evaluate a partial sum of `∑ᵢ c_{j+i} * z ^ (2 * i)` at `z = a / b`
in fixed point with scale `s`, together with the proofs that they bracket the exact
real partial sum.  Both are structurally recursive, so `decide` can evaluate them in
the kernel.
-/

namespace QipmFormal.ScalarCert

/-- Numerator of the `j`-th series coefficient: `2 ^ (j + 1) - 1`. -/
def cnum (j : ℕ) : ℕ := 2 ^ (j + 1) - 1

/-- Denominator of the `j`-th series coefficient: `2 ^ j * (2 * j + 1)`. -/
def cden (j : ℕ) : ℕ := 2 ^ j * (2 * j + 1)

lemma cden_pos (j : ℕ) : 0 < cden j := by
  unfold cden; positivity

lemma cast_cden_ne_zero (j : ℕ) : ((cden j : ℝ)) ≠ 0 := by
  exact_mod_cast (cden_pos j).ne'

/-- The `j`-th coefficient of the series, in closed form:
`(2 ^ (j + 1) - 1) / (2 ^ j * (2 * j + 1)) = (2 - (1 / 2) ^ j) / (2 * j + 1)`. -/
lemma cast_cnum_div_cden (j : ℕ) :
    (cnum j : ℝ) / (cden j : ℝ) = (2 - (1 / 2 : ℝ) ^ j) / (2 * j + 1) := by
  have hcnum : (cnum j : ℝ) = 2 ^ (j + 1) - 1 := by
    have : (1 : ℕ) ≤ 2 ^ (j + 1) := Nat.one_le_two_pow
    simp [cnum, Nat.cast_sub this]
  have hcden : (cden j : ℝ) = 2 ^ j * (2 * j + 1) := by
    simp [cden]
  have h2 : (2 : ℝ) ^ j ≠ 0 := by positivity
  have h3 : (2 * (j : ℝ) + 1) ≠ 0 := by positivity
  rw [hcnum, hcden, div_pow, one_pow]
  field_simp
  ring

/-! ### Rounding helpers -/

/-- Casting a `ℕ`-ceiling division `(n + m - 1) / m` to `ℝ` overestimates `n / m`. -/
lemma le_cast_ceilDiv (n : ℕ) {m : ℕ} (hm : 0 < m) :
    (n : ℝ) / (m : ℝ) ≤ (((n + m - 1) / m : ℕ) : ℝ) := by
  have h : n ≤ m * ((n + m - 1) / m) := by
    simpa [Nat.ceilDiv_eq_add_pred_div, smul_eq_mul] using
      le_smul_ceilDiv (α := ℕ) (β := ℕ) (b := n) hm
  have hm' : (0 : ℝ) < (m : ℝ) := by exact_mod_cast hm
  rw [div_le_iff₀ hm']
  calc (n : ℝ) ≤ ((m * ((n + m - 1) / m) : ℕ) : ℝ) := by exact_mod_cast h
    _ = (((n + m - 1) / m : ℕ) : ℝ) * (m : ℝ) := by push_cast; ring

/-! ### The scaled-integer accumulators -/

/-- Round-down accumulator for `∑ i ∈ range (k+1), c_{j+i} * (a2 / b2) ^ i`, scaled by `s`.

Here `a2` and `b2` stand for `a * a` and `b * b`, so that `a2 / b2 = z ^ 2`. -/
def accLo (a2 b2 s : ℕ) : ℕ → ℕ → ℕ
  | j, 0 => cnum j * s / cden j
  | j, (k + 1) => cnum j * s / cden j + a2 * accLo a2 b2 s (j + 1) k / b2

/-- Round-up counterpart of `accLo`, using the ceiling division `(n + m - 1) / m`. -/
def accHi (a2 b2 s : ℕ) : ℕ → ℕ → ℕ
  | j, 0 => (cnum j * s + cden j - 1) / cden j
  | j, (k + 1) =>
      (cnum j * s + cden j - 1) / cden j +
        (a2 * accHi a2 b2 s (j + 1) k + b2 - 1) / b2

lemma accLo_zero (a2 b2 s j : ℕ) : accLo a2 b2 s j 0 = cnum j * s / cden j := rfl

lemma accLo_succ (a2 b2 s j k : ℕ) :
    accLo a2 b2 s j (k + 1) =
      cnum j * s / cden j + a2 * accLo a2 b2 s (j + 1) k / b2 := rfl

lemma accHi_zero (a2 b2 s j : ℕ) :
    accHi a2 b2 s j 0 = (cnum j * s + cden j - 1) / cden j := rfl

lemma accHi_succ (a2 b2 s j k : ℕ) :
    accHi a2 b2 s j (k + 1) =
      (cnum j * s + cden j - 1) / cden j +
        (a2 * accHi a2 b2 s (j + 1) k + b2 - 1) / b2 := rfl

/-! ### Bounds on the head term -/

lemma head_lo_le (j : ℕ) {s : ℕ} (hs : 0 < s) :
    ((cnum j * s / cden j : ℕ) : ℝ) / (s : ℝ) ≤ (cnum j : ℝ) / (cden j : ℝ) := by
  have hs' : (0 : ℝ) < (s : ℝ) := by exact_mod_cast hs
  have hcd := cast_cden_ne_zero j
  calc ((cnum j * s / cden j : ℕ) : ℝ) / (s : ℝ)
      ≤ (((cnum j * s : ℕ) : ℝ) / (cden j : ℝ)) / (s : ℝ) := by
        gcongr
        exact Nat.cast_div_le
    _ = (cnum j : ℝ) / (cden j : ℝ) := by
        push_cast
        field_simp

lemma le_head_hi (j : ℕ) {s : ℕ} (hs : 0 < s) :
    (cnum j : ℝ) / (cden j : ℝ) ≤ (((cnum j * s + cden j - 1) / cden j : ℕ) : ℝ) / (s : ℝ) := by
  have hs' : (0 : ℝ) < (s : ℝ) := by exact_mod_cast hs
  have hcd := cast_cden_ne_zero j
  calc (cnum j : ℝ) / (cden j : ℝ)
      = (((cnum j * s : ℕ) : ℝ) / (cden j : ℝ)) / (s : ℝ) := by
        push_cast
        field_simp
    _ ≤ (((cnum j * s + cden j - 1) / cden j : ℕ) : ℝ) / (s : ℝ) := by
        gcongr
        exact le_cast_ceilDiv _ (cden_pos j)

/-! ### The series partial sum and the shift identity -/

/-- Partial sum `∑ i ∈ range (k+1), c_{j+i} * z ^ (2 * i)` of the (coefficient) series. -/
noncomputable def partialSum (z : ℝ) (j k : ℕ) : ℝ :=
  ∑ i ∈ Finset.range (k + 1), ((cnum (j + i) : ℝ) / (cden (j + i) : ℝ)) * z ^ (2 * i)

lemma partialSum_succ (z : ℝ) (j k : ℕ) :
    partialSum z j (k + 1) =
      (cnum j : ℝ) / (cden j : ℝ) + z ^ 2 * partialSum z (j + 1) k := by
  have h : ∀ i ∈ Finset.range (k + 1),
      ((cnum (j + (i + 1)) : ℝ) / (cden (j + (i + 1)) : ℝ)) * z ^ (2 * (i + 1))
        = z ^ 2 * (((cnum (j + 1 + i) : ℝ) / (cden (j + 1 + i) : ℝ)) * z ^ (2 * i)) := by
    intro i _
    have hj : j + (i + 1) = j + 1 + i := by omega
    rw [hj]
    ring
  unfold partialSum
  rw [Finset.sum_range_succ', Finset.sum_congr rfl h, ← Finset.mul_sum]
  simp only [Nat.add_zero, Nat.mul_zero, pow_zero, mul_one]
  ring

/-! ### Correctness of the accumulators -/

/-- Round-down correctness.  Note that no positivity assumption on `a`, `b` is needed
here: the floor accumulator is a lower bound for every `z = a / b`. -/
theorem accLo_le_partialSum {a b s : ℕ} {z : ℝ} (hz : z = (a : ℝ) / (b : ℝ))
    (hs : 0 < s) (k : ℕ) (j : ℕ) :
    (accLo (a * a) (b * b) s j k : ℝ) / (s : ℝ) ≤ partialSum z j k := by
  have hs' : (0 : ℝ) < (s : ℝ) := by exact_mod_cast hs
  have hsq : ((a * a : ℕ) : ℝ) / ((b * b : ℕ) : ℝ) = z ^ 2 := by
    rw [hz, div_pow]; push_cast; ring
  induction k generalizing j with
  | zero => simpa [partialSum, accLo_zero] using head_lo_le j hs
  | succ k ih =>
    rw [partialSum_succ, accLo_succ, Nat.cast_add, add_div]
    refine add_le_add (head_lo_le j hs) ?_
    calc ((a * a * accLo (a * a) (b * b) s (j + 1) k / (b * b) : ℕ) : ℝ) / (s : ℝ)
        ≤ (((a * a * accLo (a * a) (b * b) s (j + 1) k : ℕ) : ℝ) / ((b * b : ℕ) : ℝ))
            / (s : ℝ) := by
          gcongr
          exact Nat.cast_div_le
      _ = z ^ 2 * ((accLo (a * a) (b * b) s (j + 1) k : ℝ) / (s : ℝ)) := by
          rw [← hsq]; push_cast; ring
      _ ≤ z ^ 2 * partialSum z (j + 1) k := by
          gcongr
          exact ih (j + 1)

theorem partialSum_le_accHi {a b s : ℕ} {z : ℝ} (hz : z = (a : ℝ) / (b : ℝ))
    (ha : 0 < a) (hab : a < b) (hs : 0 < s) (k : ℕ) (j : ℕ) :
    partialSum z j k ≤ (accHi (a * a) (b * b) s j k : ℝ) / (s : ℝ) := by
  have hb : 0 < b := ha.trans hab
  have hb2 : 0 < b * b := Nat.mul_pos hb hb
  have hs' : (0 : ℝ) < (s : ℝ) := by exact_mod_cast hs
  have hsq : ((a * a : ℕ) : ℝ) / ((b * b : ℕ) : ℝ) = z ^ 2 := by
    rw [hz, div_pow]; push_cast; ring
  induction k generalizing j with
  | zero => simpa [partialSum, accHi_zero] using le_head_hi j hs
  | succ k ih =>
    rw [partialSum_succ, accHi_succ, Nat.cast_add, add_div]
    refine add_le_add (le_head_hi j hs) ?_
    calc z ^ 2 * partialSum z (j + 1) k
        ≤ z ^ 2 * ((accHi (a * a) (b * b) s (j + 1) k : ℝ) / (s : ℝ)) := by
          gcongr
          exact ih (j + 1)
      _ = (((a * a * accHi (a * a) (b * b) s (j + 1) k : ℕ) : ℝ) / ((b * b : ℕ) : ℝ))
            / (s : ℝ) := by
          rw [← hsq]; push_cast; ring
      _ ≤ (((a * a * accHi (a * a) (b * b) s (j + 1) k + b * b - 1) / (b * b) : ℕ) : ℝ)
            / (s : ℝ) := by
          gcongr
          exact le_cast_ceilDiv _ hb2

/-! ### Main statements, and the `j = 0` specialisations -/

set_option linter.unusedVariables false in
/-- `accLo` underestimates the scaled partial sum: with `z = a / b` and scale `s`,
`accLo (a*a) (b*b) s j k / s` is a lower bound for `∑ i ≤ k, c_{j+i} * z ^ (2 * i)`.

The hypotheses `ha`, `hab` are kept only for symmetry with `le_accHi`; the floor
bound holds for any `a`, `b` (see `accLo_le_partialSum`). -/
theorem accLo_le {a b s : ℕ} {z : ℝ} (hz : z = (a : ℝ) / (b : ℝ))
    (ha : 0 < a) (hab : a < b) (hs : 0 < s) (j k : ℕ) :
    (accLo (a * a) (b * b) s j k : ℝ) / (s : ℝ) ≤
      ∑ i ∈ Finset.range (k + 1), ((cnum (j + i) : ℝ) / (cden (j + i) : ℝ)) * z ^ (2 * i) :=
  accLo_le_partialSum hz hs k j

/-- `accHi` overestimates the scaled partial sum. -/
theorem le_accHi {a b s : ℕ} {z : ℝ} (hz : z = (a : ℝ) / (b : ℝ))
    (ha : 0 < a) (hab : a < b) (hs : 0 < s) (j k : ℕ) :
    ∑ i ∈ Finset.range (k + 1), ((cnum (j + i) : ℝ) / (cden (j + i) : ℝ)) * z ^ (2 * i) ≤
      (accHi (a * a) (b * b) s j k : ℝ) / (s : ℝ) :=
  partialSum_le_accHi hz ha hab hs k j

/-- The `j = 0` case of `accLo_le`: a lower bound for `∑ i ≤ k, cᵢ * z ^ (2 * i)`. -/
theorem accLo_le₀ {a b s : ℕ} {z : ℝ} (hz : z = (a : ℝ) / (b : ℝ))
    (ha : 0 < a) (hab : a < b) (hs : 0 < s) (k : ℕ) :
    (accLo (a * a) (b * b) s 0 k : ℝ) / (s : ℝ) ≤
      ∑ i ∈ Finset.range (k + 1), ((cnum i : ℝ) / (cden i : ℝ)) * z ^ (2 * i) := by
  simpa using accLo_le hz ha hab hs 0 k

/-- The `j = 0` case of `le_accHi`: an upper bound for `∑ i ≤ k, cᵢ * z ^ (2 * i)`. -/
theorem le_accHi₀ {a b s : ℕ} {z : ℝ} (hz : z = (a : ℝ) / (b : ℝ))
    (ha : 0 < a) (hab : a < b) (hs : 0 < s) (k : ℕ) :
    ∑ i ∈ Finset.range (k + 1), ((cnum i : ℝ) / (cden i : ℝ)) * z ^ (2 * i) ≤
      (accHi (a * a) (b * b) s 0 k : ℝ) / (s : ℝ) := by
  simpa using le_accHi hz ha hab hs 0 k

end QipmFormal.ScalarCert
