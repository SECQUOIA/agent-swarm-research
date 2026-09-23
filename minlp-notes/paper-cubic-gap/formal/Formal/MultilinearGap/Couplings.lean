import Formal.MultilinearGap.IntegratedLaws
import Formal.MultilinearGap.HarmonicDensity
import Formal.CubicGap.Envelope

/-! Feasible harmonic and opposing-threshold couplings for arbitrary cube points. -/
namespace MultilinearGap

open CubicGap MeasureTheory Set
noncomputable section
variable {I : Type*}

/-- A low coordinate succeeds below its threshold; a high coordinate has a harmonic failure. -/
def harmonicProbability (x : I → ℝ) (M t : ℝ) (i : I) : ℝ :=
  if x i ≤ 1 / 2 then (if t ≤ x i then 1 else 0)
  else 1 - harmonicDensity M (1 - x i) t

/-- Low and high coordinates use opposite threshold directions. -/
def failureThresholdProb (x : I → ℝ) (t : ℝ) (i : I) : ℝ :=
  if x i ≤ 1 / 2 then (if t ≤ x i then 1 else 0)
  else if 1 - x i < t then 1 else 0

theorem harmonicProbability_cube (x : I → ℝ) (hx : x ∈ cube I)
    (M : ℝ) (hM : 1 ≤ M) (t : ℝ) : harmonicProbability x M t ∈ cube I := by
  intro i
  dsimp [harmonicProbability]
  split_ifs
  · exact ⟨zero_le_one, le_rfl⟩
  · exact ⟨le_rfl, zero_le_one⟩
  · have h := harmonicDensity_mem_Icc hM (sub_nonneg.mpr (hx i).2)
      (by linarith [(hx i).1] : 1 - x i ≤ 1) t
    exact ⟨by linarith [h.2], by linarith [h.1]⟩

theorem harmonicProbability_measurable (x : I → ℝ) (M : ℝ) (i : I) :
    Measurable (fun t => harmonicProbability x M t i) := by
  unfold harmonicProbability
  split
  · exact Measurable.ite measurableSet_Iic measurable_const measurable_const
  · exact measurable_const.sub (harmonicDensity_measurable M (1 - x i))

theorem failureThresholdProb_cube (x : I → ℝ) (t : ℝ) :
    failureThresholdProb x t ∈ cube I := by
  intro i
  dsimp [failureThresholdProb]
  split_ifs <;> norm_num

theorem failureThresholdProb_measurable (x : I → ℝ) (i : I) :
    Measurable (fun t => failureThresholdProb x t i) := by
  unfold failureThresholdProb
  split
  · exact Measurable.ite measurableSet_Iic measurable_const measurable_const
  · exact Measurable.ite measurableSet_Ioi measurable_const measurable_const

theorem intervalIntegral_lower_indicator {u : ℝ} (hu : u ∈ Icc (0 : ℝ) 1) :
    (∫ t in (0 : ℝ)..1, if t ≤ u then (1 : ℝ) else 0) = u := by
  change (∫ t in (0 : ℝ)..1, indicator {t | t ≤ u} (fun _ => (1 : ℝ)) t) = u
  rw [intervalIntegral.integral_indicator hu]
  simp

theorem intervalIntegral_upper_indicator {u : ℝ} (hu : u ∈ Icc (0 : ℝ) 1) :
    (∫ t in (0 : ℝ)..1, if u < t then (1 : ℝ) else 0) = 1 - u := by
  have heq (t : ℝ) : (if u < t then (1 : ℝ) else 0) =
      1 - (if t ≤ u then (1 : ℝ) else 0) := by
    split_ifs <;> simp_all
    linarith
  simp_rw [heq]
  rw [intervalIntegral.integral_sub intervalIntegrable_const
    (intervalIntegrable_of_mem_unitInterval _
      (Measurable.ite measurableSet_Iic measurable_const measurable_const)
      (fun t => by split_ifs <;> norm_num)), intervalIntegral_lower_indicator hu]
  simp

theorem intervalIntegral_harmonicProbability (x : I → ℝ) (hx : x ∈ cube I)
    (M : ℝ) (hM : 1 ≤ M) (i : I) :
    (∫ t in (0 : ℝ)..1, harmonicProbability x M t i) = x i := by
  unfold harmonicProbability
  split
  · exact intervalIntegral_lower_indicator (hx i)
  · have hp : 0 ≤ 1 - x i := sub_nonneg.mpr (hx i).2
    have hp1 : 1 - x i ≤ 1 := by linarith [(hx i).1]
    rw [intervalIntegral.integral_sub intervalIntegrable_const
      (harmonicDensity_intervalIntegrable hM hp hp1), intervalIntegral_harmonicDensity hM hp hp1]
    simp

theorem intervalIntegral_failureThresholdProb (x : I → ℝ) (hx : x ∈ cube I) (i : I) :
    (∫ t in (0 : ℝ)..1, failureThresholdProb x t i) = x i := by
  unfold failureThresholdProb
  split
  · exact intervalIntegral_lower_indicator (hx i)
  · rw [intervalIntegral_upper_indicator ⟨sub_nonneg.mpr (hx i).2, by linarith [(hx i).1]⟩]
    ring

variable [Fintype I] [DecidableEq I]

def harmonicLaw (x : I → ℝ) (hx : x ∈ cube I) (M : ℝ) (hM : 1 ≤ M) : Law (Vertex I) :=
  integratedBernoulli (harmonicProbability x M) (harmonicProbability_cube x hx M hM)
    (harmonicProbability_measurable x M)

def failureThresholdLaw (x : I → ℝ) (_hx : x ∈ cube I) : Law (Vertex I) :=
  integratedBernoulli (failureThresholdProb x) (failureThresholdProb_cube x)
    (failureThresholdProb_measurable x)

theorem harmonicLaw_hasMeans (x : I → ℝ) (hx : x ∈ cube I) (M : ℝ) (hM : 1 ≤ M) :
    HasMeans (harmonicLaw x hx M hM) x := by
  intro i
  rw [harmonicLaw, integratedBernoulli_mean, intervalIntegral_harmonicProbability x hx M hM]

theorem failureThresholdLaw_hasMeans (x : I → ℝ) (hx : x ∈ cube I) :
    HasMeans (failureThresholdLaw x hx) x := by
  intro i
  rw [failureThresholdLaw, integratedBernoulli_mean, intervalIntegral_failureThresholdProb x hx]

theorem harmonicLaw_expect_monomial (x : I → ℝ) (hx : x ∈ cube I)
    (M : ℝ) (hM : 1 ≤ M) (s : Finset I) :
    (harmonicLaw x hx M hM).expect (fun v => monomial s (vertexPoint v)) =
      ∫ t in (0 : ℝ)..1, monomial s (harmonicProbability x M t) :=
  integratedBernoulli_expect_monomial _ _ _ _

theorem failureThresholdLaw_expect_monomial (x : I → ℝ) (hx : x ∈ cube I) (s : Finset I) :
    (failureThresholdLaw x hx).expect (fun v => monomial s (vertexPoint v)) =
      ∫ t in (0 : ℝ)..1, monomial s (failureThresholdProb x t) :=
  integratedBernoulli_expect_monomial _ _ _ _

/-- The union of harmonic failures of a finite set of coordinates. -/
def harmonicUnion (x : I → ℝ) (M : ℝ) (s : Finset I) (t : ℝ) : ℝ :=
  1 - ∏ i ∈ s, (1 - harmonicDensity M (1 - x i) t)

omit [Fintype I] [DecidableEq I] in
theorem harmonicUnion_mem_Icc (x : I → ℝ) (hx : x ∈ cube I)
    (M : ℝ) (hM : 1 ≤ M) (s : Finset I) (t : ℝ) :
    harmonicUnion x M s t ∈ Icc (0 : ℝ) 1 := by
  have hb (i : I) : 0 ≤ 1 - harmonicDensity M (1 - x i) t ∧
      1 - harmonicDensity M (1 - x i) t ≤ 1 := by
    have h := harmonicDensity_mem_Icc hM (sub_nonneg.mpr (hx i).2)
      (by linarith [(hx i).1] : 1 - x i ≤ 1) t
    constructor <;> linarith [h.1, h.2]
  have hnonneg := Finset.prod_nonneg (fun i (_ : i ∈ s) => (hb i).1)
  have hle := Finset.prod_le_one (fun i (_ : i ∈ s) => (hb i).1)
    (fun i (_ : i ∈ s) => (hb i).2)
  dsimp [harmonicUnion]
  constructor <;> linarith

omit [Fintype I] [DecidableEq I] in
theorem harmonicUnion_measurable (x : I → ℝ) (M : ℝ) (s : Finset I) :
    Measurable (harmonicUnion x M s) := by
  apply measurable_const.sub
  exact Finset.measurable_prod _ fun i _ =>
    measurable_const.sub (harmonicDensity_measurable M (1 - x i))

omit [Fintype I] [DecidableEq I] in
theorem harmonicUnion_intervalIntegrable (x : I → ℝ) (hx : x ∈ cube I)
    (M : ℝ) (hM : 1 ≤ M) (s : Finset I) {u : ℝ} (hu : u ∈ Icc (0 : ℝ) 1) :
    IntervalIntegrable (harmonicUnion x M s) volume 0 u := by
  apply (intervalIntegrable_of_mem_unitInterval _ (harmonicUnion_measurable x M s)
    (harmonicUnion_mem_Icc x hx M hM s)).mono_set
  simpa only [uIcc_of_le hu.1, uIcc_of_le zero_le_one] using Icc_subset_Icc le_rfl hu.2

/-- For a unique low coordinate, the deficiency is exactly the integrated union of failures. -/
theorem harmonicLaw_unique_low_deficiency (x : I → ℝ) (hx : x ∈ cube I)
    (M : ℝ) (hM : 1 ≤ M) (s : Finset I) (r : I) (hr : r ∈ s)
    (hlow : x r ≤ 1 / 2) (hhigh : ∀ i ∈ s.erase r, 1 / 2 < x i) :
    x r - (harmonicLaw x hx M hM).expect (fun v => monomial s (vertexPoint v)) =
      ∫ t in (0 : ℝ)..x r, harmonicUnion x M (s.erase r) t := by
  rw [harmonicLaw_expect_monomial]
  have hprod (t : ℝ) : monomial s (harmonicProbability x M t) =
      indicator {t | t ≤ x r}
        (fun t => ∏ i ∈ s.erase r, (1 - harmonicDensity M (1 - x i) t)) t := by
    rw [monomial, ← Finset.mul_prod_erase s _ hr]
    have heq : (∏ i ∈ s.erase r, harmonicProbability x M t i) =
        ∏ i ∈ s.erase r, (1 - harmonicDensity M (1 - x i) t) := by
      apply Finset.prod_congr rfl
      intro i hi
      exact if_neg (not_le.mpr (hhigh i hi))
    rw [heq]
    simp only [harmonicProbability, if_pos hlow, indicator_apply, mem_ofPred_eq]
    split_ifs <;> simp
  simp_rw [hprod]
  rw [intervalIntegral.integral_indicator (hx r)]
  have hint := harmonicUnion_intervalIntegrable x hx M hM (s.erase r) (hx r)
  have hprodint : IntervalIntegrable
      (fun t => ∏ i ∈ s.erase r, (1 - harmonicDensity M (1 - x i) t)) volume 0 (x r) := by
    have h := (intervalIntegrable_const (c := (1 : ℝ))).sub hint
    simpa [harmonicUnion] using h
  simp only [harmonicUnion]
  rw [intervalIntegral.integral_sub intervalIntegrable_const hprodint]
  simp

/-- A single high-coordinate failure already supplies this threshold deficiency. -/
theorem failureThresholdLaw_deficiency_lower (x : I → ℝ) (hx : x ∈ cube I)
    (s : Finset I) (r j : I) (hr : r ∈ s) (hj : j ∈ s)
    (hlow : x r ≤ 1 / 2) (hhigh : 1 / 2 < x j) :
    min (x r) (1 - x j) ≤
      x r - (failureThresholdLaw x hx).expect (fun v => monomial s (vertexPoint v)) := by
  have hq (t : ℝ) : failureThresholdProb x t ∈ cube I := failureThresholdProb_cube x t
  have hmon (t : ℝ) : monomial s (failureThresholdProb x t) ∈ Icc (0 : ℝ) 1 := by
    refine ⟨monomial_nonneg s (fun i _ => (hq t i).1), ?_⟩
    exact (monomial_le_coordinate s (fun i _ => hq t i) hr).trans (hq t r).2
  have hm : Measurable (fun t => monomial s (failureThresholdProb x t)) :=
    Finset.measurable_prod _ fun i _ => failureThresholdProb_measurable x i
  have hint := intervalIntegrable_of_mem_unitInterval _ hm hmon
  have hrint := intervalIntegrable_of_mem_unitInterval _ (failureThresholdProb_measurable x r)
    (fun t => hq t r)
  have hcut : min (x r) (1 - x j) ∈ Icc (0 : ℝ) 1 :=
    ⟨le_min (hx r).1 (sub_nonneg.mpr (hx j).2), (min_le_left _ _).trans (hx r).2⟩
  have hlowint := intervalIntegrable_of_mem_unitInterval
    (fun t => if t ≤ min (x r) (1 - x j) then (1 : ℝ) else 0)
    (Measurable.ite measurableSet_Iic measurable_const measurable_const)
    (fun t => by split_ifs <;> norm_num)
  have hbound (t : ℝ) :
      (if t ≤ min (x r) (1 - x j) then (1 : ℝ) else 0) ≤
        failureThresholdProb x t r - monomial s (failureThresholdProb x t) := by
    by_cases ht : t ≤ min (x r) (1 - x j)
    · have htr : t ≤ x r := ht.trans (min_le_left _ _)
      have htj : t ≤ 1 - x j := ht.trans (min_le_right _ _)
      have hz : monomial s (failureThresholdProb x t) = 0 := by
        apply Finset.prod_eq_zero hj
        change (if x j ≤ 1 / 2 then _ else _) = 0
        rw [if_neg (not_le.mpr hhigh), if_neg (not_lt.mpr htj)]
      rw [hz]
      simp only [if_pos ht, failureThresholdProb, if_pos hlow, if_pos htr, sub_zero]
      exact le_rfl
    · rw [if_neg ht]
      exact sub_nonneg.mpr (monomial_le_coordinate s (fun i _ => hq t i) hr)
  have hh := intervalIntegral.integral_mono (by norm_num : (0 : ℝ) ≤ 1)
    hlowint (hrint.sub hint) hbound
  rw [intervalIntegral_lower_indicator hcut,
    intervalIntegral.integral_sub hrint hint,
    intervalIntegral_failureThresholdProb x hx r] at hh
  rw [failureThresholdLaw_expect_monomial]
  exact hh

end
end MultilinearGap
