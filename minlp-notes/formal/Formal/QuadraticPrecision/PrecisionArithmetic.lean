import Formal.QuadraticPrecision.IntervalLower
import Formal.QuadraticPrecision.CountMinimum

/-! Precision choices and bounded additive count errors. These arithmetic
interfaces do not replace existence or lower bounds for actual lifts. -/
namespace QuadraticPrecision
noncomputable section

/-- Uniform bounded additive error at all sufficiently small positive accuracies. -/
def HasPrecisionRate (feasible : ℝ → ℕ → Prop) (r : ℕ) : Prop :=
  ∃ C : ℝ, 0 ≤ C ∧ ∃ ε₀ : ℝ, 0 < ε₀ ∧
    ∀ ε, 0 < ε → ε ≤ ε₀ → ∃ p, IsMinimumCount (feasible ε) p ∧
      |(p : ℝ) - (r : ℝ) / 2 * Real.logb 2 (1 / ε)| ≤ C

/-- The normalized square threshold gives the precise depth for total weight A. -/
def precisionDepth (A ε : ℝ) : ℕ := squarePrecisionCount (ε / A)

theorem precisionDepth_sufficient {A ε : ℝ} (hA : 0 < A) (hε : 0 < ε) :
    A * ((1 / 4 : ℝ)^(precisionDepth A ε) / 4) ≤ ε := by
  have h := squarePrecisionCount_sufficient (div_pos hε hA)
  simpa only [precisionDepth, mul_comm] using (le_div_iff₀ hA).mp h

/-- The chosen depth differs from half the precision logarithm by a constant
for all sufficiently small positive accuracies. -/
theorem precisionDepth_bounds {A ε : ℝ} (hA : 0 < A) (hε : 0 < ε)
    (hsmall : ε ≤ A / 4) :
    (Real.logb 2 (1 / ε) + Real.logb 2 A - 2) / 2 ≤ (precisionDepth A ε : ℝ) ∧
    (precisionDepth A ε : ℝ) < (Real.logb 2 (1 / ε) + Real.logb 2 A) / 2 := by
  have hratio : 4 ≤ A / ε := (le_div_iff₀ hε).mpr (by linarith)
  have hfour : Real.logb 2 (4 : ℝ) = 2 := by
    have h := Real.logb_pow 2 2 2
    norm_num [Real.logb_self_eq_one] at h ⊢
    exact h
  have hlog := (Real.logb_le_logb (by norm_num : (1 : ℝ) < 2)
    (by norm_num : (0 : ℝ) < 4) (div_pos hA hε)).mpr hratio
  rw [hfour] at hlog
  have heq : Real.logb 2 (1 / (ε / A)) = Real.logb 2 (1 / ε) + Real.logb 2 A := by
    rw [one_div_div, Real.logb_div (ne_of_gt hA) (ne_of_gt hε)]
    simp only [one_div, Real.logb_inv]
    ring
  have hnonneg : 0 ≤ (Real.logb 2 (1 / (ε / A)) - 2) / 2 := by
    rw [one_div_div]
    linarith
  constructor
  · simpa only [precisionDepth, squarePrecisionCount, heq] using
      Nat.le_ceil ((Real.logb 2 (1 / (ε / A)) - 2) / 2)
  · have h := Nat.ceil_lt_add_one hnonneg
    change (precisionDepth A ε : ℝ) < _ at h
    rw [heq] at h
    linarith

/-- A logarithmic lower bound and the actual depth construction imply the
bounded-additive-error law, uniformly over every small positive tolerance. -/
theorem precisionRate_of_bounds (feasible : ℝ → ℕ → Prop) (r : ℕ)
    (A c : ℝ) (hA : 0 < A)
    (lower : ∀ ε, 0 < ε → ε ≤ A / 4 → ∀ p, feasible ε p →
      (r : ℝ) / 2 * Real.logb 2 (1 / ε) + c ≤ p)
    (upper : ∀ ε, 0 < ε → feasible ε (r * precisionDepth A ε)) :
    HasPrecisionRate feasible r := by
  refine ⟨|c| + |(r : ℝ) / 2 * Real.logb 2 A|, by positivity,
    A / 4, by positivity, ?_⟩
  intro ε hε hsmall
  obtain ⟨p, hp⟩ := exists_minimumCount ⟨_, upper ε hε⟩
  refine ⟨p, hp, ?_⟩
  have hl := lower ε hε hsmall p hp.1
  have hu : (p : ℝ) ≤ (r : ℝ) * (precisionDepth A ε : ℝ) := by
    exact_mod_cast hp.2 _ (upper ε hε)
  have hd := (precisionDepth_bounds hA hε hsmall).2.le
  have hmul := mul_le_mul_of_nonneg_left hd (Nat.cast_nonneg r : (0 : ℝ) ≤ r)
  apply abs_le.mpr
  constructor
  · have h := neg_abs_le c
    have hn : 0 ≤ |(r : ℝ) / 2 * Real.logb 2 A| := abs_nonneg _
    linarith
  · have h := le_abs_self ((r : ℝ) / 2 * Real.logb 2 A)
    have hn : 0 ≤ |c| := abs_nonneg _
    nlinarith

/-- Explicit linear-description size bound at the selected depth. The actual
systems have at most the expression on the left; this proves their claimed
logarithmic size for every sufficiently small positive accuracy. -/
theorem precisionDepth_linear_size (n r : ℕ) {A ε : ℝ} (hA : 0 < A)
    (hε : 0 < ε) (hsmall : ε ≤ min (A / 4) 1) :
    (2 * (n : ℝ) + r * (11 + 10 * (precisionDepth A ε : ℝ)) + 2) ≤
      (2 * n + 11 * r + 2 + 5 * r * |Real.logb 2 A| + 5 * r) *
        (1 + Real.logb 2 (1 / ε)) := by
  have hdepth := (precisionDepth_bounds hA hε (hsmall.trans (min_le_left _ _))).2.le
  have hone : 1 ≤ 1 / ε := (le_div_iff₀ hε).mpr (by
    simpa using hsmall.trans (min_le_right _ _))
  have hlog : 0 ≤ Real.logb 2 (1 / ε) := by
    have hh := (Real.logb_le_logb (by norm_num : (1 : ℝ) < 2)
      (by norm_num : (0 : ℝ) < 1) (by positivity : (0 : ℝ) < 1 / ε)).mpr hone
    simpa only [Real.logb_one] using hh
  have hr : (0 : ℝ) ≤ r := Nat.cast_nonneg r
  have hn : (0 : ℝ) ≤ n := Nat.cast_nonneg n
  have ha := le_abs_self (Real.logb 2 A)
  have hmul := mul_le_mul_of_nonneg_left hdepth (by positivity : (0 : ℝ) ≤ 10 * r)
  have hpos := mul_nonneg
    (by positivity : 0 ≤ 2 * (n : ℝ) + 11*r + 2 + 5*r*|Real.logb 2 A|) hlog
  nlinarith [mul_nonneg hr (sub_nonneg.mpr ha)]

end
end QuadraticPrecision
