import Formal.MultilinearGap.Construction
import Formal.MultilinearGap.ExactArithmetic
import Formal.CubicGap.Expectation

/-! Exact moments of the finite dyadic threshold distribution. -/

namespace MultilinearGap
noncomputable section
open scoped BigOperators

/-- Threshold masses, with the remaining geometric tail placed at `L`. -/
def dyadicWeight (L : ℕ) (l : Fin (L + 1)) : ℝ :=
  if l.val < L then 1 / (2 : ℝ) ^ (l.val + 1) else 1 / (2 : ℝ) ^ L

theorem dyadicWeight_sum (L : ℕ) (f : ℕ → ℝ) :
    ∑ l, dyadicWeight L l * f l.val =
      (∑ l ∈ Finset.range L, (1 / (2 : ℝ) ^ (l + 1)) * f l) +
      (1 / (2 : ℝ) ^ L) * f L := by
  rw [Fin.sum_univ_castSucc]
  simp only [dyadicWeight, Fin.val_castSucc, Fin.is_lt, ↓reduceIte, Fin.val_last,
    lt_self_iff_false]
  exact congrArg (fun z => z + 1 / (2 : ℝ)^L * f L)
    (Fin.sum_univ_eq_sum_range (fun l => 1 / (2 : ℝ)^(l+1) * f l) L)

private theorem inv_pow_sum (L : ℕ) :
    (∑ l ∈ Finset.range L, 1 / (2 : ℝ) ^ (l + 1)) + 1 / (2 : ℝ) ^ L = 1 := by
  induction L with
  | zero => norm_num
  | succ L h =>
    rw [Finset.sum_range_succ, pow_succ]
    field_simp at h ⊢
    nlinarith

def dyadicLaw (L : ℕ) : CubicGap.Law (Fin (L + 1)) where
  weight := dyadicWeight L
  nonneg := by intro l; unfold dyadicWeight; split <;> positivity
  mass_one := by
    have h := dyadicWeight_sum L (fun _ => 1)
    simpa only [mul_one, inv_pow_sum] using h

private theorem inv_pow_tail (L q : ℕ) (hq : q ≤ L) :
    (∑ l ∈ Finset.range L, if q ≤ l then 1 / (2 : ℝ) ^ (l + 1) else 0) +
      1 / (2 : ℝ) ^ L = 1 / (2 : ℝ) ^ q := by
  induction L with
  | zero =>
    have he : q = 0 := by omega
    subst q
    simp
  | succ L ih =>
    by_cases h : q ≤ L
    · rw [Finset.sum_range_succ, if_pos h, pow_succ]
      have hh := ih h
      field_simp at hh ⊢
      nlinarith
    · have heq : q = L + 1 := by omega
      subst q
      have hz : (∑ l ∈ Finset.range (L + 1),
          if L + 1 ≤ l then 1 / (2 : ℝ) ^ (l + 1) else 0) = 0 := by
        apply Finset.sum_eq_zero
        intro l hl
        rw [if_neg (by have := Finset.mem_range.mp hl; omega)]
      rw [hz, zero_add]

/-- Every anchor has its prescribed dyadic activation probability. -/
theorem dyadicLaw_tail (L q : ℕ) (hq : q ≤ L) :
    (dyadicLaw L).expect (fun l => if q ≤ l.val then 1 else 0) =
      1 / (2 : ℝ) ^ q := by
  rw [CubicGap.Law.expect]
  change (∑ l, dyadicWeight L l * (if q ≤ l.val then 1 else 0)) = _
  rw [dyadicWeight_sum L (fun l => if q ≤ l then 1 else 0)]
  simp only [mul_ite, mul_one, mul_zero, if_pos hq]
  exact inv_pow_tail L q hq

/-- Failure count at a threshold, before mixing adjacent cutoffs. -/
def dyadicFailures (q l : ℕ) : ℝ := if l < q then 0 else (2 : ℝ) ^ (l - q + 1)

private theorem weight_failure (q l : ℕ) (h : q ≤ l) :
    1 / (2 : ℝ) ^ (l + 1) * (2 : ℝ) ^ (l - q + 1) = 1 / (2 : ℝ) ^ q := by
  have he : l + 1 = q + (l - q + 1) := by omega
  rw [he, pow_add]
  field_simp

/-- The exact failure budget of a cutoff law. -/
theorem dyadicLaw_failures (L q : ℕ) (hq : q ≤ L) :
    (dyadicLaw L).expect (fun l => dyadicFailures q l.val) = cutoffBudget L q := by
  rw [CubicGap.Law.expect]
  change (∑ l, dyadicWeight L l * dyadicFailures q l.val) = _
  rw [dyadicWeight_sum]
  have ht : 1 / (2 : ℝ) ^ L * dyadicFailures q L = 2 / (2 : ℝ) ^ q := by
    rw [dyadicFailures, if_neg (by omega), pow_succ]
    have he : L = q + (L - q) := by omega
    conv_lhs => arg 1; arg 2; rw [he, pow_add]
    field_simp
  rw [ht]
  have hs : (∑ l ∈ Finset.range L, 1 / (2 : ℝ) ^ (l + 1) * dyadicFailures q l) =
      (L - q : ℕ) / (2 : ℝ) ^ q := by
    calc
      _ = ∑ l ∈ Finset.range L, if q ≤ l then 1 / (2 : ℝ) ^ q else 0 := by
        apply Finset.sum_congr rfl
        intro l _
        by_cases h : q ≤ l
        · rw [if_pos h, dyadicFailures, if_neg (by omega), weight_failure q l h]
        · rw [if_neg h, dyadicFailures, if_pos (by omega), mul_zero]
      _ = _ := by
        rw [← Finset.sum_filter]
        have he : (Finset.range L).filter (fun l => q ≤ l) = Finset.Ico q L := by
          ext l; simp; omega
        rw [he]
        simp [div_eq_mul_inv]
  rw [hs, cutoffBudget, Nat.cast_sub hq]
  ring

private theorem powers_sum (k : ℕ) :
    ∑ j ∈ Finset.range k, (2 : ℝ)^(j+1) = (2 : ℝ)^(k+1) - 2 := by
  induction k with
  | zero => norm_num
  | succ k h => rw [Finset.sum_range_succ, h, pow_succ]; ring

private theorem min_powers_sum (k q : ℕ) :
    ∑ j ∈ Finset.range (k + q), min ((2 : ℝ)^(j+1)) ((2 : ℝ)^(k+1)) =
      ((q : ℝ)+1) * (2 : ℝ)^(k+1) - 2 := by
  rw [Finset.sum_range_add]
  have hlo : (∑ j ∈ Finset.range k, min ((2 : ℝ)^(j+1)) ((2 : ℝ)^(k+1))) =
      (2 : ℝ)^(k+1) - 2 := by
    rw [← powers_sum]
    apply Finset.sum_congr rfl
    intro j hj
    rw [min_eq_left (pow_le_pow_right₀ (by norm_num) (by have := Finset.mem_range.mp hj; omega))]
  have hhi : (∑ j ∈ Finset.range q, min ((2 : ℝ)^(k+j+1)) ((2 : ℝ)^(k+1))) =
      (q : ℝ) * (2 : ℝ)^(k+1) := by
    calc
      _ = ∑ _j ∈ Finset.range q, (2 : ℝ)^(k+1) := by
        apply Finset.sum_congr rfl
        intro j _
        rw [min_eq_right (pow_le_pow_right₀ (by norm_num) (by omega))]
      _ = _ := by simp
  rw [hlo, hhi]
  ring

/-- Destroyed active terms when failures meet as many blocks as possible. -/
def dyadicSelected (L q l : ℕ) : ℝ :=
  ∑ j : Fin L, if j.val + 1 ≤ l then min ((2 : ℝ)^(j.val+1)) (dyadicFailures q l) else 0

theorem dyadicSelected_eq (L q l : ℕ) (hl : l ≤ L) :
    dyadicSelected L q l =
      ((q : ℝ)+1) * dyadicFailures q l - 2 * (if q ≤ l then 1 else 0) := by
  by_cases hq : q ≤ l
  · rw [dyadicSelected, dyadicFailures, if_neg (by omega), if_pos hq]
    have hs : (∑ j : Fin L, if j.val + 1 ≤ l then
        min ((2 : ℝ)^(j.val+1)) ((2 : ℝ)^(l-q+1)) else 0) =
        ∑ j ∈ Finset.range l, min ((2 : ℝ)^(j+1)) ((2 : ℝ)^(l-q+1)) := by
      rw [Fin.sum_univ_eq_sum_range (fun j => if j+1 ≤ l then
        min ((2 : ℝ)^(j+1)) ((2 : ℝ)^(l-q+1)) else 0)]
      have hL : L = l + (L-l) := by omega
      conv_lhs => rw [hL, Finset.sum_range_add]
      have ht : (∑ j ∈ Finset.range (L-l), if l+j+1 ≤ l then
          min ((2 : ℝ)^(l+j+1)) ((2 : ℝ)^(l-q+1)) else 0) = 0 := by
        apply Finset.sum_eq_zero
        intro j _
        rw [if_neg (by omega)]
      rw [ht, add_zero]
      apply Finset.sum_congr rfl
      intro j hj
      rw [if_pos (by have := Finset.mem_range.mp hj; omega)]
    rw [hs]
    have he : l = (l-q)+q := by omega
    conv_lhs => arg 1; rw [he]
    rw [min_powers_sum]
    ring
  · have hn : l < q := by omega
    have hz : dyadicFailures q l = 0 := by simp [dyadicFailures, hn]
    rw [hz, if_neg hq]
    simp only [mul_zero, sub_self]
    unfold dyadicSelected
    apply Finset.sum_eq_zero
    intro j _
    rw [hz, min_eq_right (by positivity)]
    simp

/-- The exact expected deficit of a cutoff law. -/
theorem dyadicLaw_selected (L q : ℕ) (hq : q ≤ L) :
    (dyadicLaw L).expect (fun l => dyadicSelected L q l.val) = cutoffDeficit L q := by
  have hf : (fun l : Fin (L+1) => dyadicSelected L q l.val) =
      (fun l => ((q : ℝ)+1) * dyadicFailures q l.val - 2 * (if q ≤ l.val then 1 else 0)) := by
    funext l
    exact dyadicSelected_eq L q l.val (by omega)
  rw [hf, CubicGap.Law.expect_sub, CubicGap.Law.expect_const_mul,
    CubicGap.Law.expect_const_mul, dyadicLaw_failures L q hq, dyadicLaw_tail L q hq,
    cutoffDeficit]
  ring

end
end MultilinearGap
