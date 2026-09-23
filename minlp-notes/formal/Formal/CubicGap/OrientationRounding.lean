import Formal.CubicGap.RoundingIndicators

/-! Endpoint-orientation rounding, with the uniform parameter folded at one half. -/

namespace CubicGap
open MeasureTheory Set MultilinearGap
noncomputable section

/-- Conditional orientation probability after folding the uniform parameter at one half. -/
def orientationProbability (x t : ℝ) : ℝ :=
  if x ≤ 1 / 2 then lowerStep (2 * x) t / 2
  else 1 - lowerStep (2 * (1 - x)) t / 2

theorem orientationProbability_mem (x t : ℝ) :
    orientationProbability x t ∈ Icc (0 : ℝ) 1 := by
  unfold orientationProbability lowerStep
  split_ifs <;> norm_num

theorem orientationProbability_measurable (x : ℝ) :
    Measurable (orientationProbability x) := by
  have h (a : ℝ) : Measurable (lowerStep a) :=
    Measurable.ite measurableSet_Iic measurable_const measurable_const
  unfold orientationProbability
  split
  · exact (h _).div_const 2
  · exact measurable_const.sub ((h _).div_const 2)

theorem orientationProbability_integral {x : ℝ} (hx : x ∈ Icc (0 : ℝ) 1) :
    (∫ t in (0 : ℝ)..1, orientationProbability x t) = x := by
  unfold orientationProbability
  split_ifs with h
  · rw [intervalIntegral.integral_div, integral_lowerStep ⟨by linarith [hx.1], by linarith⟩]
    ring
  · rw [intervalIntegral.integral_sub intervalIntegrable_const
      ((lowerStep_integrable _).div_const 2),
      intervalIntegral.integral_div,
      integral_lowerStep ⟨by linarith [hx.2], by linarith⟩]
    simp

theorem orientationProbability_integrable (x : ℝ) :
    IntervalIntegrable (orientationProbability x) volume 0 1 :=
  intervalIntegrable_of_mem_unitInterval _ (orientationProbability_measurable x)
    (orientationProbability_mem x)

/-- Exact one-low cubic expectation under orientation rounding. -/
theorem orientation_integral_one_low {u v w : ℝ}
    (hu : u ∈ Icc (0 : ℝ) 1) (hv : v ∈ Icc (0 : ℝ) 1)
    (hw : w ∈ Icc (0 : ℝ) 1)
    (hul : u ≤ 1 / 2) (hvh : 1 / 2 < v) (hvw : v ≤ w) :
    (∫ t in (0 : ℝ)..1, orientationProbability u t *
      orientationProbability v t * orientationProbability w t) =
      u - min u (1 - v) / 2 - min u (1 - w) / 4 := by
  have hwh : ¬w ≤ 1 / 2 := by linarith
  have heq (t : ℝ) : orientationProbability u t * orientationProbability v t *
      orientationProbability w t = lowerStep (2 * u) t / 2 -
      lowerStep (2 * min u (1 - v)) t / 4 -
      lowerStep (2 * min u (1 - w)) t / 8 := by
    simp only [orientationProbability, if_pos hul, if_neg (not_le.mpr hvh), if_neg hwh]
    rw [mul_min_of_nonneg _ _ (by norm_num : (0 : ℝ) ≤ 2),
      mul_min_of_nonneg _ _ (by norm_num : (0 : ℝ) ≤ 2)]
    simp only [lowerStep, le_min_iff]
    split_ifs <;> simp_all <;> linarith
  simp_rw [heq]
  rw [intervalIntegral.integral_sub
      (((lowerStep_integrable _).div_const 2).sub ((lowerStep_integrable _).div_const 4))
      ((lowerStep_integrable _).div_const 8),
    intervalIntegral.integral_sub ((lowerStep_integrable _).div_const 2)
      ((lowerStep_integrable _).div_const 4)]
  simp only [intervalIntegral.integral_div]
  rw [integral_lowerStep ⟨by linarith [hu.1], by linarith⟩,
    integral_lowerStep ⟨by have := le_min hu.1 (sub_nonneg.mpr hv.2); linarith,
      by linarith [min_le_left u (1-v)]⟩,
    integral_lowerStep ⟨by have := le_min hu.1 (sub_nonneg.mpr hw.2); linarith,
      by linarith [min_le_left u (1-w)]⟩]
  ring

/-- Exact all-high cubic expectation under orientation rounding. -/
theorem orientation_integral_all_high {u v w : ℝ}
    (hu : u ∈ Icc (0 : ℝ) 1) (hv : v ∈ Icc (0 : ℝ) 1)
    (hw : w ∈ Icc (0 : ℝ) 1)
    (huh : 1 / 2 < u) (huv : u ≤ v) (hvw : v ≤ w) :
    (∫ t in (0 : ℝ)..1, orientationProbability u t *
      orientationProbability v t * orientationProbability w t) =
      u - (1 - v) / 2 - (1 - w) / 4 := by
  have hvh : ¬v ≤ 1 / 2 := by linarith
  have hwh : ¬w ≤ 1 / 2 := by linarith
  have heq (t : ℝ) : orientationProbability u t * orientationProbability v t *
      orientationProbability w t = 1 - lowerStep (2 * (1-u)) t / 2 -
      lowerStep (2 * (1-v)) t / 4 - lowerStep (2 * (1-w)) t / 8 := by
    simp only [orientationProbability, if_neg (not_le.mpr huh), if_neg hvh, if_neg hwh]
    simp only [lowerStep]
    split_ifs <;> simp_all <;> linarith
  simp_rw [heq]
  rw [intervalIntegral.integral_sub
      ((intervalIntegrable_const.sub ((lowerStep_integrable _).div_const 2)).sub
        ((lowerStep_integrable _).div_const 4)) ((lowerStep_integrable _).div_const 8),
    intervalIntegral.integral_sub
      (intervalIntegrable_const.sub ((lowerStep_integrable _).div_const 2))
      ((lowerStep_integrable _).div_const 4),
    intervalIntegral.integral_sub intervalIntegrable_const
      ((lowerStep_integrable _).div_const 2)]
  simp only [intervalIntegral.integral_div]
  rw [integral_lowerStep ⟨by linarith [hu.2], by linarith⟩,
    integral_lowerStep ⟨by linarith [hv.2], by linarith⟩,
    integral_lowerStep ⟨by linarith [hw.2], by linarith⟩]
  norm_num
  ring

/-- Sorted bilinear orientation moment. -/
theorem orientation_integral_pair {u v : ℝ}
    (hu : u ∈ Icc (0 : ℝ) 1) (hv : v ∈ Icc (0 : ℝ) 1) (huv : u ≤ v) :
    (∫ t in (0 : ℝ)..1, orientationProbability u t * orientationProbability v t) =
      u - min u (1 - v) / 2 := by
  by_cases hvl : v ≤ 1 / 2
  · have hul : u ≤ 1 / 2 := huv.trans hvl
    have hmin : min u (1-v) = u := min_eq_left (by linarith)
    have heq (t : ℝ) : orientationProbability u t * orientationProbability v t =
        lowerStep (2*u) t / 4 := by
      simp only [orientationProbability, if_pos hul, if_pos hvl]
      have h := lowerStep_mul_of_le (by linarith : 2*u ≤ 2*v) t
      nlinarith [h]
    simp_rw [heq]
    rw [intervalIntegral.integral_div, integral_lowerStep ⟨by linarith [hu.1], by linarith⟩,
      hmin]
    ring
  · by_cases hul : u ≤ 1 / 2
    · have heq (t : ℝ) : orientationProbability u t * orientationProbability v t =
          lowerStep (2*u) t / 2 - lowerStep (2*min u (1-v)) t / 4 := by
        simp only [orientationProbability, if_pos hul, if_neg hvl]
        rw [mul_min_of_nonneg _ _ (by norm_num : (0 : ℝ) ≤ 2)]
        have h := lowerStep_mul (2*u) (2*(1-v)) t
        nlinarith [h]
      simp_rw [heq]
      rw [intervalIntegral.integral_sub ((lowerStep_integrable _).div_const 2)
        ((lowerStep_integrable _).div_const 4)]
      simp only [intervalIntegral.integral_div]
      rw [integral_lowerStep ⟨by linarith [hu.1], by linarith⟩,
        integral_lowerStep ⟨by have := le_min hu.1 (sub_nonneg.mpr hv.2); linarith,
          by linarith [min_le_left u (1-v)]⟩]
      ring
    · have hmin : min u (1-v) = 1-v := min_eq_right (by linarith)
      have heq (t : ℝ) : orientationProbability u t * orientationProbability v t =
          1 - lowerStep (2*(1-u)) t / 2 - lowerStep (2*(1-v)) t / 4 := by
        simp only [orientationProbability, if_neg hul, if_neg hvl, lowerStep]
        split_ifs <;> simp_all <;> linarith
      simp_rw [heq]
      rw [intervalIntegral.integral_sub
        (intervalIntegrable_const.sub ((lowerStep_integrable _).div_const 2))
        ((lowerStep_integrable _).div_const 4),
        intervalIntegral.integral_sub intervalIntegrable_const
      ((lowerStep_integrable _).div_const 2)]
      simp only [intervalIntegral.integral_div]
      rw [integral_lowerStep ⟨by linarith [hu.2], by linarith⟩,
        integral_lowerStep ⟨by linarith [hv.2], by linarith⟩, hmin]
      norm_num
      ring

/-- Two low coordinates force at least half the smallest mean to be deficient. -/
theorem orientation_integral_two_low {u v w : ℝ}
    (hu : u ∈ Icc (0 : ℝ) 1) (hv : v ∈ Icc (0 : ℝ) 1)
    (_hw : w ∈ Icc (0 : ℝ) 1) (huv : u ≤ v) (hvl : v ≤ 1 / 2) :
    (∫ t in (0 : ℝ)..1, orientationProbability u t *
      orientationProbability v t * orientationProbability w t) ≤ u / 2 := by
  have hpint : IntervalIntegrable
      (fun t => orientationProbability u t * orientationProbability v t) volume 0 1 :=
    intervalIntegrable_of_mem_unitInterval _
      ((orientationProbability_measurable u).mul (orientationProbability_measurable v))
      (fun t => ⟨mul_nonneg (orientationProbability_mem u t).1 (orientationProbability_mem v t).1,
        mul_le_one₀ (orientationProbability_mem u t).2 (orientationProbability_mem v t).1
          (orientationProbability_mem v t).2⟩)
  have htint : IntervalIntegrable
      (fun t => orientationProbability u t * orientationProbability v t *
        orientationProbability w t) volume 0 1 :=
    intervalIntegrable_of_mem_unitInterval _
      (((orientationProbability_measurable u).mul (orientationProbability_measurable v)).mul
        (orientationProbability_measurable w)) (fun t => by
          have h1 := orientationProbability_mem u t
          have h2 := orientationProbability_mem v t
          have h3 := orientationProbability_mem w t
          exact ⟨mul_nonneg (mul_nonneg h1.1 h2.1) h3.1,
            mul_le_one₀ (mul_le_one₀ h1.2 h2.1 h2.2) h3.1 h3.2⟩)
  have h := intervalIntegral.integral_mono (by norm_num : (0 : ℝ) ≤ 1) htint hpint
    (fun t => mul_le_of_le_one_right
      (mul_nonneg (orientationProbability_mem u t).1 (orientationProbability_mem v t).1)
      (orientationProbability_mem w t).2)
  rw [orientation_integral_pair hu hv huv, min_eq_left (by linarith : u ≤ 1-v)] at h
  linarith

variable {I : Type*} [Fintype I] [DecidableEq I]

omit [Fintype I] [DecidableEq I] in
theorem orientationProbability_cube (x : I → ℝ) (t : ℝ) :
    (fun i => orientationProbability (x i) t) ∈ cube I :=
  fun i => orientationProbability_mem (x i) t

/-- A finite binary law using one shared folded parameter and independent conditional coins. -/
def orientationLaw (x : I → ℝ) : Law (Vertex I) :=
  integratedBernoulli (fun t i => orientationProbability (x i) t)
    (orientationProbability_cube x)
    (fun i => orientationProbability_measurable (x i))

theorem orientationLaw_hasMeans (x : I → ℝ) (hx : x ∈ cube I) :
    HasMeans (orientationLaw x) x := by
  intro i
  rw [orientationLaw, integratedBernoulli_mean, orientationProbability_integral (hx i)]

theorem orientationLaw_expect_monomial (x : I → ℝ) (s : Finset I) :
    (orientationLaw x).expect (fun v => monomial s (vertexPoint v)) =
      ∫ t in (0 : ℝ)..1, monomial s (fun i => orientationProbability (x i) t) :=
  integratedBernoulli_expect_monomial _ _ _ _

theorem orientationLaw_expect_pair (x : I → ℝ) (i j : I) (hij : i ≠ j) :
    (orientationLaw x).expect (fun v => monomial {i,j} (vertexPoint v)) =
      ∫ t in (0 : ℝ)..1, orientationProbability (x i) t * orientationProbability (x j) t := by
  rw [orientationLaw_expect_monomial]
  simp [monomial, hij]

theorem orientationLaw_expect_triple (x : I → ℝ) (i j k : I)
    (hij : i ≠ j) (hik : i ≠ k) (hjk : j ≠ k) :
    (orientationLaw x).expect (fun v => monomial {i,j,k} (vertexPoint v)) =
      ∫ t in (0 : ℝ)..1, orientationProbability (x i) t *
        orientationProbability (x j) t * orientationProbability (x k) t := by
  rw [orientationLaw_expect_monomial]
  simp [monomial, hij, hik, hjk, mul_assoc]

end
end CubicGap
