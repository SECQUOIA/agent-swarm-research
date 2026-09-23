import Formal.MultilinearGap.FloorDensity
import Formal.MultilinearGap.FloorGain
import Formal.MultilinearGap.Couplings
import Formal.MultilinearGap.EasyTerms

/-! A single exact-marginal coupling for the marginal-floor bound. -/
namespace MultilinearGap

open CubicGap MeasureTheory Set
noncomputable section
variable {I : Type*}

/-- Low coordinates are thresholds; high coordinates use the repaired failure density. -/
def floorProbability (x : I → ℝ) (τ t : ℝ) (i : I) : ℝ :=
  if x i ≤ 1 / 2 then (if t ≤ x i then 1 else 0)
  else 1 - floorFailure τ (1 - x i) t

theorem floorProbability_cube (x : I → ℝ) (hx : x ∈ cube I)
    (τ : ℝ) (hτ : 0 < τ) (t : ℝ) : floorProbability x τ t ∈ cube I := by
  intro i
  dsimp [floorProbability]
  split_ifs with hi ht
  · exact ⟨zero_le_one, le_rfl⟩
  · exact ⟨le_rfl, zero_le_one⟩
  · have h := floorFailure_mem_unitInterval hτ (sub_nonneg.mpr (hx i).2)
      (by linarith : 1 - x i < 1) t
    exact ⟨by linarith [h.2], by linarith [h.1]⟩

theorem floorProbability_measurable (x : I → ℝ) (τ : ℝ) (i : I) :
    Measurable (fun t => floorProbability x τ t i) := by
  unfold floorProbability
  split
  · exact Measurable.ite measurableSet_Iic measurable_const measurable_const
  · exact measurable_const.sub (measurable_floorFailure τ (1 - x i))

theorem intervalIntegral_floorProbability (x : I → ℝ) (hx : x ∈ cube I)
    (τ : ℝ) (hτ : 0 < τ) (i : I) :
    (∫ t in (0 : ℝ)..1, floorProbability x τ t i) = x i := by
  unfold floorProbability
  split
  · exact intervalIntegral_lower_indicator (hx i)
  · have hp : 0 ≤ 1 - x i := sub_nonneg.mpr (hx i).2
    have hp1 : 1 - x i < 1 := by linarith
    rw [intervalIntegral.integral_sub intervalIntegrable_const
      (intervalIntegrable_floorFailure hτ hp hp1), integral_floorFailure hτ hp hp1]
    simp

variable [Fintype I] [DecidableEq I]

/-- A finite law whose coordinate means are exactly the requested point. -/
def floorLaw (x : I → ℝ) (hx : x ∈ cube I) (τ : ℝ) (hτ : 0 < τ) : Law (Vertex I) :=
  integratedBernoulli (floorProbability x τ) (floorProbability_cube x hx τ hτ)
    (floorProbability_measurable x τ)

theorem floorLaw_hasMeans (x : I → ℝ) (hx : x ∈ cube I) (τ : ℝ) (hτ : 0 < τ) :
    HasMeans (floorLaw x hx τ hτ) x := by
  intro i
  rw [floorLaw, integratedBernoulli_mean, intervalIntegral_floorProbability x hx τ hτ]

theorem floorLaw_expect_monomial (x : I → ℝ) (hx : x ∈ cube I)
    (τ : ℝ) (hτ : 0 < τ) (s : Finset I) :
    (floorLaw x hx τ hτ).expect (fun v => monomial s (vertexPoint v)) =
      ∫ t in (0 : ℝ)..1, monomial s (floorProbability x τ t) :=
  integratedBernoulli_expect_monomial _ _ _ _

/-- Conditional probability of a failure among the specified high coordinates. -/
def floorUnion (x : I → ℝ) (τ : ℝ) (s : Finset I) (t : ℝ) : ℝ :=
  1 - ∏ i ∈ s, (1 - floorFailure τ (1 - x i) t)

omit [Fintype I] [DecidableEq I] in
theorem floorUnion_mem_Icc (x : I → ℝ) (hx : x ∈ cube I)
    (τ : ℝ) (hτ : 0 < τ) (s : Finset I)
    (hhigh : ∀ i ∈ s, 1 / 2 < x i) (t : ℝ) :
    floorUnion x τ s t ∈ Icc (0 : ℝ) 1 := by
  have hb (i : I) (hi : i ∈ s) : 0 ≤ 1 - floorFailure τ (1 - x i) t ∧
      1 - floorFailure τ (1 - x i) t ≤ 1 := by
    have h := floorFailure_mem_unitInterval hτ (sub_nonneg.mpr (hx i).2)
      (by linarith [hhigh i hi] : 1 - x i < 1) t
    constructor <;> linarith [h.1, h.2]
  have hnonneg := Finset.prod_nonneg (fun i (hi : i ∈ s) => (hb i hi).1)
  have hle := Finset.prod_le_one (fun i (hi : i ∈ s) => (hb i hi).1)
    (fun i (hi : i ∈ s) => (hb i hi).2)
  dsimp [floorUnion]
  constructor <;> linarith

omit [Fintype I] [DecidableEq I] in
theorem floorUnion_measurable (x : I → ℝ) (τ : ℝ) (s : Finset I) :
    Measurable (floorUnion x τ s) := by
  apply measurable_const.sub
  exact Finset.measurable_prod _ fun i _ =>
    measurable_const.sub (measurable_floorFailure τ (1 - x i))

omit [Fintype I] [DecidableEq I] in
theorem floorUnion_intervalIntegrable (x : I → ℝ) (hx : x ∈ cube I)
    (τ : ℝ) (hτ : 0 < τ) (s : Finset I) (hhigh : ∀ i ∈ s, 1 / 2 < x i)
    {u : ℝ} (hu : u ∈ Icc (0 : ℝ) 1) :
    IntervalIntegrable (floorUnion x τ s) volume 0 u := by
  apply (intervalIntegrable_of_mem_unitInterval _ (floorUnion_measurable x τ s)
    (floorUnion_mem_Icc x hx τ hτ s hhigh)).mono_set
  simpa only [uIcc_of_le hu.1, uIcc_of_le zero_le_one] using Icc_subset_Icc le_rfl hu.2

/-- The unique low anchor reduces the deficiency exactly to an integrated union. -/
theorem floorLaw_unique_low_deficiency (x : I → ℝ) (hx : x ∈ cube I)
    (τ : ℝ) (hτ : 0 < τ) (s : Finset I) (r : I) (hr : r ∈ s)
    (hlow : x r ≤ 1 / 2) (hhigh : ∀ i ∈ s.erase r, 1 / 2 < x i) :
    x r - (floorLaw x hx τ hτ).expect (fun v => monomial s (vertexPoint v)) =
      ∫ t in (0 : ℝ)..x r, floorUnion x τ (s.erase r) t := by
  rw [floorLaw_expect_monomial]
  have hprod (t : ℝ) : monomial s (floorProbability x τ t) =
      indicator {t | t ≤ x r}
        (fun t => ∏ i ∈ s.erase r, (1 - floorFailure τ (1 - x i) t)) t := by
    rw [monomial, ← Finset.mul_prod_erase s _ hr]
    have heq : (∏ i ∈ s.erase r, floorProbability x τ t i) =
        ∏ i ∈ s.erase r, (1 - floorFailure τ (1 - x i) t) := by
      apply Finset.prod_congr rfl
      intro i hi
      exact if_neg (not_le.mpr (hhigh i hi))
    rw [heq]
    simp only [floorProbability, if_pos hlow, indicator_apply, mem_ofPred_eq]
    split_ifs <;> simp
  simp_rw [hprod]
  rw [intervalIntegral.integral_indicator (hx r)]
  have hint := floorUnion_intervalIntegrable x hx τ hτ (s.erase r) hhigh (hx r)
  have hprodint : IntervalIntegrable
      (fun t => ∏ i ∈ s.erase r, (1 - floorFailure τ (1 - x i) t)) volume 0 (x r) := by
    have h := (intervalIntegrable_const (c := (1 : ℝ))).sub hint
    simpa [floorUnion] using h
  simp only [floorUnion]
  rw [intervalIntegral.integral_sub intervalIntegrable_const hprodint]
  simp

omit [Fintype I] [DecidableEq I] in
/-- Clipping one failure makes the union certain; without clipping the exponential
product estimate applies to the original, unreduced failure sum. -/
theorem floorUnion_exp_lower (x : I → ℝ) (hx : x ∈ cube I)
    (τ : ℝ) (hτ : 0 < τ) (s : Finset I) (hhigh : ∀ i ∈ s, 1 / 2 < x i)
    (t : ℝ) :
    1 - Real.exp (-((∑ i ∈ s, (1 - x i)) * floorDensity τ t)) ≤ floorUnion x τ s t := by
  have hb (i : I) (hi : i ∈ s) := floorFailure_mem_unitInterval hτ
    (sub_nonneg.mpr (hx i).2) (by linarith [hhigh i hi] : 1 - x i < 1) t
  have hc (i : I) (hi : i ∈ s) := floorFailure_ge_clipped hτ
    (sub_nonneg.mpr (hx i).2) (by linarith [hhigh i hi] : 1 - x i < 1) t
  by_cases hclip : ∃ i ∈ s, 1 ≤ (1 - x i) * floorDensity τ t
  · obtain ⟨i, hi, hclip⟩ := hclip
    have hq : floorFailure τ (1 - x i) t = 1 := by
      have h := hc i hi
      rw [floorClipped, min_eq_left hclip] at h
      exact le_antisymm (hb i hi).2 h
    have hz : (∏ j ∈ s, (1 - floorFailure τ (1 - x j) t)) = 0 :=
      Finset.prod_eq_zero hi (by rw [hq]; ring)
    simp only [floorUnion, hz, sub_zero]
    linarith [Real.exp_pos (-((∑ i ∈ s, (1 - x i)) * floorDensity τ t))]
  · have hq (i : I) (hi : i ∈ s) :
        (1 - x i) * floorDensity τ t ≤ floorFailure τ (1 - x i) t := by
      have h := hc i hi
      have hi' : (1 - x i) * floorDensity τ t ≤ 1 := by
        by_contra hn
        exact hclip ⟨i, hi, (lt_of_not_ge hn).le⟩
      simpa only [floorClipped, min_eq_right hi'] using h
    have hprod := prod_le_exp_neg_failure_sum s
      (fun i => 1 - floorFailure τ (1 - x i) t)
      (fun i hi => sub_nonneg.mpr (hb i hi).2)
    have hsum : (∑ i ∈ s, (1 - x i)) * floorDensity τ t ≤
        ∑ i ∈ s, floorFailure τ (1 - x i) t := by
      rw [Finset.sum_mul]
      exact Finset.sum_le_sum hq
    simp only [sub_sub_cancel] at hprod
    have he := Real.exp_le_exp.mpr (neg_le_neg hsum)
    dsimp [floorUnion]
    linarith

/-- The actual exact-marginal law supplies the integral lower bound for every
monomial with a unique low coordinate. -/
theorem floorLaw_unique_low_lower (x : I → ℝ) (hx : x ∈ cube I)
    (τ : ℝ) (hτ : 0 < τ) (s : Finset I) (r : I) (hr : r ∈ s)
    (hlow : x r ≤ 1 / 2) (hhigh : ∀ i ∈ s.erase r, 1 / 2 < x i) :
    (∫ t in (0 : ℝ)..x r,
      1 - Real.exp (-(otherFailures s x r / (floorLog τ * (t + τ))))) ≤
      x r - (floorLaw x hx τ hτ).expect (fun v => monomial s (vertexPoint v)) := by
  rw [floorLaw_unique_low_deficiency x hx τ hτ s r hr hlow hhigh]
  have hd := continuous_floorDensity hτ
  have hi : IntervalIntegrable (fun t =>
      1 - Real.exp (-(otherFailures s x r * floorDensity τ t))) volume 0 (x r) :=
    (continuous_const.sub (Real.continuous_exp.comp
      ((continuous_const.mul hd).neg))).intervalIntegrable _ _
  have heq : (∫ t in (0 : ℝ)..x r,
      1 - Real.exp (-(otherFailures s x r / (floorLog τ * (t + τ))))) =
      ∫ t in (0 : ℝ)..x r,
      1 - Real.exp (-(otherFailures s x r * floorDensity τ t)) := by
    apply intervalIntegral.integral_congr_Ioo_of_le (hx r).1
    intro t ht
    simp [floorDensity, max_eq_right ht.1.le, div_eq_mul_inv]
  rw [heq]
  apply intervalIntegral.integral_mono (hx r).1 hi
    (floorUnion_intervalIntegrable x hx τ hτ (s.erase r) hhigh (hx r))
  intro t
  exact floorUnion_exp_lower x hx τ hτ (s.erase r) hhigh t

/-- Every hard monomial receives the same gain whenever its anchor is large
relative to the density shift. -/
theorem floorLaw_unique_low_gain (x : I → ℝ) (hx : x ∈ cube I)
    (τ : ℝ) (hτ : 0 < τ) (s : Finset I) (r : I) (hr : r ∈ s)
    (hlow : x r ≤ 1 / 2) (hhigh : ∀ i ∈ s.erase r, 1 / 2 < x i)
    {e : ℝ} (he : 0 < e) (hu : 0 < x r) (hτu : τ / x r ≤ e) :
    min (x r) (otherFailures s x r) * floorIntegral (floorLog τ) e ≤
      x r - (floorLaw x hx τ hτ).expect (fun v => monomial s (vertexPoint v)) := by
  have hS : 0 ≤ otherFailures s x r :=
    Finset.sum_nonneg fun i _ => sub_nonneg.mpr (hx i).2
  have hg := floor_integral_gain (floorLog_pos hτ) hτ hu he hτu hS
  apply hg.trans
  simpa only [neg_div] using
    floorLaw_unique_low_lower x hx τ hτ s r hr hlow hhigh

end
end MultilinearGap
