import Formal.MultilinearGap.IntegratedLaws
import Formal.MultilinearGap.GeneralGaps

/-! Independent-rounding estimates for terms outside the one-low-coordinate case. -/

namespace MultilinearGap

open scoped BigOperators
open CubicGap

noncomputable section

/-- The absolute constant in the independent-rounding estimate. -/
def easyConstant : ℝ := 1 - Real.exp (-1)

theorem easyConstant_pos : 0 < easyConstant := by
  have : Real.exp (-1 : ℝ) < 1 := by simp
  exact sub_pos.mpr this

theorem easyConstant_le_one : easyConstant ≤ 1 := by
  dsimp [easyConstant]
  linarith [Real.exp_pos (-1)]

/-- Independent success probabilities are bounded by the exponential of the
negative total failure probability. -/
theorem prod_le_exp_neg_failure_sum {I : Type*} (s : Finset I) (x : I → ℝ)
    (hx : ∀ i ∈ s, 0 ≤ x i) :
    ∏ i ∈ s, x i ≤ Real.exp (-(∑ i ∈ s, (1 - x i))) := by
  calc
    _ ≤ ∏ i ∈ s, Real.exp (x i - 1) := Finset.prod_le_prod hx fun i _ => by
      simpa using Real.add_one_le_exp (x i - 1)
    _ = _ := by rw [← Real.exp_sum]; congr 1; simp [Finset.sum_sub_distrib]

/-- The concave failure function lies above its chord on `[0,1]` and is
increasing after one. -/
theorem one_sub_exp_neg_ge (S : ℝ) (hS : 0 ≤ S) :
    easyConstant * min 1 S ≤ 1 - Real.exp (-S) := by
  by_cases hS1 : S ≤ 1
  · have h := convexOn_exp.2 (Set.mem_univ (-1 : ℝ)) (Set.mem_univ (0 : ℝ))
      hS (show 0 ≤ 1 - S by linarith) (show S + (1 - S) = 1 by ring)
    simp only [smul_eq_mul, mul_neg, mul_one, mul_zero, add_zero, Real.exp_zero] at h
    rw [min_eq_right hS1]
    dsimp [easyConstant]
    nlinarith
  · rw [min_eq_left (le_of_not_ge hS1)]
    have h := Real.exp_le_exp.mpr (show -S ≤ (-1 : ℝ) by linarith)
    simpa [easyConstant] using sub_le_sub_left h 1

/-- For an anchor of mean at least one half, independent rounding captures a
fixed fraction of the termwise gap. -/
theorem independent_deficiency_high {I : Type*} (s : Finset I) (x : I → ℝ)
    (hx : ∀ i ∈ s, 0 ≤ x i ∧ x i ≤ 1) (u : ℝ)
    (hu : 1 / 2 ≤ u) (hu1 : u ≤ 1) :
    easyConstant * min u (∑ i ∈ s, (1 - x i)) / 2 ≤
      u * (1 - ∏ i ∈ s, x i) := by
  let S := ∑ i ∈ s, (1 - x i)
  have hS : 0 ≤ S := Finset.sum_nonneg fun i hi => sub_nonneg.mpr (hx i hi).2
  have he := one_sub_exp_neg_ge S hS
  have hp := prod_le_exp_neg_failure_sum s x (fun i hi => (hx i hi).1)
  have hm : min u S ≤ min 1 S := min_le_min hu1 le_rfl
  have hn : 0 ≤ min 1 S := le_min (by norm_num) hS
  have hc := easyConstant_pos.le
  have h1 := mul_le_mul_of_nonneg_left hm hc
  have h2 := mul_le_mul_of_nonneg_right hu (mul_nonneg hc hn)
  have h3 := mul_le_mul_of_nonneg_left (show easyConstant * min 1 S ≤
      1 - ∏ i ∈ s, x i by dsimp [S] at he ⊢; linarith) (show 0 ≤ u by linarith)
  dsimp [S] at *
  nlinarith

/-- If a second coordinate has mean at most one half, independent rounding
already captures half the anchor mean. -/
theorem independent_deficiency_second_low {I : Type*}
    (s : Finset I) (x : I → ℝ) (hx : ∀ i ∈ s, 0 ≤ x i ∧ x i ≤ 1)
    (u : ℝ) (hu : 0 ≤ u) (b : I) (hb : b ∈ s) (hxb : x b ≤ 1 / 2) :
    easyConstant * min u (∑ i ∈ s, (1 - x i)) / 2 ≤
      u * (1 - ∏ i ∈ s, x i) := by
  classical
  have hp : ∏ i ∈ s, x i ≤ x b := by
    simpa using Finset.prod_le_prod_of_subset_of_le_one
      (Finset.singleton_subset_iff.mpr hb) (fun i hi => (hx i hi).1)
      (fun i hi _ => (hx i hi).2)
  have hS : 0 ≤ ∑ i ∈ s, (1 - x i) :=
    Finset.sum_nonneg fun i hi => sub_nonneg.mpr (hx i hi).2
  have hm : 0 ≤ min u (∑ i ∈ s, (1 - x i)) := le_min hu hS
  have hc := mul_le_mul_of_nonneg_right easyConstant_le_one hm
  have hp' := mul_le_mul_of_nonneg_left (show (1 / 2 : ℝ) ≤
    1 - ∏ i ∈ s, x i by linarith) hu
  have hm' := min_le_left u (∑ i ∈ s, (1 - x i))
  nlinarith

/-- Factoring out the anchor identifies the independent law's deficiency. -/
theorem bernoulli_deficiency_eq {I : Type*} [Fintype I] [DecidableEq I]
    (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) (i : I) (hi : i ∈ s) :
    x i - (bernoulliLaw x hx).expect (fun v => monomial s (vertexPoint v)) =
      x i * (1 - ∏ j ∈ s.erase i, x j) := by
  rw [bernoulliLaw_expect_monomial, monomial,
    ← Finset.mul_prod_erase s x hi]
  ring

/-- The independent law handles terms with no low anchor or with a second low
coordinate, at the same absolute constant. -/
theorem bernoulli_easy_gap {I : Type*} [Fintype I] [DecidableEq I]
    (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) (i : I) (hi : i ∈ s)
    (hmin : ∀ j ∈ s, x i ≤ x j)
    (heasy : 1 / 2 ≤ x i ∨ ∃ j ∈ s.erase i, x j ≤ 1 / 2) :
    easyConstant * hullGap (monomial s) x / 2 ≤
      x i - (bernoulliLaw x hx).expect (fun v => monomial s (vertexPoint v)) := by
  rw [bernoulli_deficiency_eq s x hx i hi]
  have hg := monomial_gap_le_min s x hx i hi hmin
  have hc := mul_le_mul_of_nonneg_left hg easyConstant_pos.le
  have hb : easyConstant * min (x i) (otherFailures s x i) / 2 ≤
      x i * (1 - ∏ j ∈ s.erase i, x j) := by
    rcases heasy with hhigh | ⟨j, hj, hjlow⟩
    · exact independent_deficiency_high (s.erase i) x (fun j _ => hx j)
        (x i) hhigh (hx i).2
    · exact independent_deficiency_second_low (s.erase i) x (fun j _ => hx j)
        (x i) (hx i).1 j hj hjlow
  linarith

end
end MultilinearGap
