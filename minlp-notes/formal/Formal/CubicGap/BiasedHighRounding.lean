import Formal.CubicGap.RoundingIndicators

/-! Globally consistent biased-high rounding and its exact low-degree moments. -/

namespace CubicGap

open MeasureTheory Set MultilinearGap

noncomputable section

/-- Low coordinates use a common threshold. High coordinates independently fail
with probability one half while the common parameter is below twice their failure mean. -/
def biasedHighProbability (x t : ℝ) : ℝ :=
  if x ≤ 1 / 2 then lowerStep x t else 1 - lowerStep (2 * (1 - x)) t / 2

theorem biasedHighProbability_mem_Icc (x t : ℝ) :
    biasedHighProbability x t ∈ Icc (0 : ℝ) 1 := by
  unfold biasedHighProbability lowerStep
  split_ifs <;> norm_num

theorem biasedHighProbability_measurable (x : ℝ) :
    Measurable (biasedHighProbability x) := by
  unfold biasedHighProbability
  split
  · exact lowerStep_measurable x
  · exact measurable_const.sub ((lowerStep_measurable _).div_const 2)

theorem integral_biasedHighProbability {x : ℝ} (hx : x ∈ Icc (0 : ℝ) 1) :
    (∫ t in (0 : ℝ)..1, biasedHighProbability x t) = x := by
  unfold biasedHighProbability
  split_ifs with h
  · exact integral_lowerStep hx
  · rw [intervalIntegral.integral_sub intervalIntegrable_const
      ((lowerStep_integrable _).div_const 2), intervalIntegral.integral_div,
      integral_lowerStep (show 2 * (1 - x) ∈ Icc (0 : ℝ) 1 from
        ⟨by linarith [hx.2], by linarith⟩)]
    norm_num

private theorem integral_step_sub_two {u a b : ℝ}
    (hu : u ∈ Icc (0 : ℝ) 1) (ha : a ∈ Icc (0 : ℝ) 1)
    (hb : b ∈ Icc (0 : ℝ) 1) :
    (∫ t in (0 : ℝ)..1, lowerStep u t - lowerStep a t / 2 - lowerStep b t / 4) =
      u - a / 2 - b / 4 := by
  rw [intervalIntegral.integral_sub
    ((lowerStep_integrable u).sub ((lowerStep_integrable a).div_const 2))
    ((lowerStep_integrable b).div_const 4),
    intervalIntegral.integral_sub (lowerStep_integrable u)
      ((lowerStep_integrable a).div_const 2)]
  simp only [intervalIntegral.integral_div, integral_lowerStep hu,
    integral_lowerStep ha, integral_lowerStep hb]

private theorem min_mem_unit {u v : ℝ} (hu : u ∈ Icc (0 : ℝ) 1)
    (hv : v ∈ Icc (0 : ℝ) 1) : min u v ∈ Icc (0 : ℝ) 1 :=
  ⟨le_min hu.1 hv.1, (min_le_left _ _).trans hu.2⟩

/-- With two low coordinates the biased-high pair equals the smaller mean. -/
theorem integral_biasedHigh_pair_low {u v : ℝ}
    (hu : u ∈ Icc (0 : ℝ) 1) (huv : u ≤ v) (hv : v ≤ 1 / 2) :
    (∫ t in (0 : ℝ)..1, biasedHighProbability u t * biasedHighProbability v t) = u := by
  simp only [biasedHighProbability, if_pos (huv.trans hv), if_pos hv, lowerStep_mul,
    min_eq_left huv]
  exact integral_lowerStep hu

/-- Exact pair expectation when just the smaller coordinate is low. -/
theorem integral_biasedHigh_pair_one_low {u v : ℝ}
    (hu : u ∈ Icc (0 : ℝ) 1) (hv : v ∈ Icc (0 : ℝ) 1)
    (hul : u ≤ 1 / 2) (hvh : 1 / 2 < v) :
    (∫ t in (0 : ℝ)..1, biasedHighProbability u t * biasedHighProbability v t) =
      u - min u (2 * (1 - v)) / 2 := by
  have hv' : 2 * (1 - v) ∈ Icc (0 : ℝ) 1 := ⟨by linarith [hv.2], by linarith⟩
  have heq (t : ℝ) : biasedHighProbability u t * biasedHighProbability v t =
      lowerStep u t - lowerStep (min u (2 * (1 - v))) t / 2 := by
    simp only [biasedHighProbability, if_pos hul, if_neg (not_le.mpr hvh)]
    rw [← lowerStep_mul]
    ring
  simp_rw [heq]
  rw [intervalIntegral.integral_sub (lowerStep_integrable _)
    ((lowerStep_integrable _).div_const 2), intervalIntegral.integral_div,
    integral_lowerStep hu, integral_lowerStep (min_mem_unit hu hv')]

/-- Exact cubic expectation with precisely one low coordinate. -/
theorem integral_biasedHigh_triple_one_low {u v w : ℝ}
    (hu : u ∈ Icc (0 : ℝ) 1) (hv : v ∈ Icc (0 : ℝ) 1)
    (hw : w ∈ Icc (0 : ℝ) 1) (hvw : v ≤ w)
    (hul : u ≤ 1 / 2) (hvh : 1 / 2 < v) :
    (∫ t in (0 : ℝ)..1,
      biasedHighProbability u t * biasedHighProbability v t * biasedHighProbability w t) =
      u - min u (2 * (1 - v)) / 2 - min u (2 * (1 - w)) / 4 := by
  have hv' : 2 * (1 - v) ∈ Icc (0 : ℝ) 1 := ⟨by linarith [hv.2], by linarith⟩
  have hw' : 2 * (1 - w) ∈ Icc (0 : ℝ) 1 := ⟨by linarith [hw.2], by linarith⟩
  have heq (t : ℝ) :
      biasedHighProbability u t * biasedHighProbability v t * biasedHighProbability w t =
      lowerStep u t - lowerStep (min u (2 * (1 - v))) t / 2 -
        lowerStep (min u (2 * (1 - w))) t / 4 := by
    simp only [biasedHighProbability, if_pos hul, if_neg (not_le.mpr hvh),
      if_neg (not_le.mpr (hvh.trans_le hvw))]
    rw [← lowerStep_mul, ← lowerStep_mul]
    have hab := lowerStep_mul (2 * (1 - v)) (2 * (1 - w)) t
    rw [min_eq_right (by linarith : 2 * (1 - w) ≤ 2 * (1 - v))] at hab
    calc
      _ = lowerStep u t - lowerStep u t * lowerStep (2 * (1 - v)) t / 2 -
          lowerStep u t * lowerStep (2 * (1 - w)) t / 2 +
          lowerStep u t * (lowerStep (2 * (1 - v)) t * lowerStep (2 * (1 - w)) t) / 4 := by ring
      _ = _ := by rw [hab]; ring
  simp_rw [heq]
  exact integral_step_sub_two hu (min_mem_unit hu hv') (min_mem_unit hu hw')

/-- Exact pair expectation when both coordinates are high. -/
theorem integral_biasedHigh_pair_high {u v : ℝ}
    (hu : u ∈ Icc (0 : ℝ) 1) (hv : v ∈ Icc (0 : ℝ) 1)
    (huv : u ≤ v) (huh : 1 / 2 < u) :
    (∫ t in (0 : ℝ)..1, biasedHighProbability u t * biasedHighProbability v t) =
      u - (1 - v) / 2 := by
  have hu' : 2 * (1 - u) ∈ Icc (0 : ℝ) 1 := ⟨by linarith [hu.2], by linarith⟩
  have hv' : 2 * (1 - v) ∈ Icc (0 : ℝ) 1 := ⟨by linarith [hv.2], by linarith⟩
  have heq (t : ℝ) : biasedHighProbability u t * biasedHighProbability v t =
      1 - lowerStep (2 * (1 - u)) t / 2 - lowerStep (2 * (1 - v)) t / 4 := by
    simp only [biasedHighProbability, if_neg (not_le.mpr huh),
      if_neg (not_le.mpr (huh.trans_le huv)), lowerStep]
    split_ifs <;> norm_num
    linarith
  simp_rw [heq]
  rw [intervalIntegral.integral_sub
    (intervalIntegrable_const.sub ((lowerStep_integrable _).div_const 2))
    ((lowerStep_integrable _).div_const 4),
    intervalIntegral.integral_sub intervalIntegrable_const ((lowerStep_integrable _).div_const 2)]
  simp only [intervalIntegral.integral_div, integral_lowerStep hu', integral_lowerStep hv']
  norm_num
  ring

/-- Exact cubic expectation when every coordinate is high. -/
theorem integral_biasedHigh_triple_high {u v w : ℝ}
    (hu : u ∈ Icc (0 : ℝ) 1) (hv : v ∈ Icc (0 : ℝ) 1)
    (hw : w ∈ Icc (0 : ℝ) 1) (huv : u ≤ v) (hvw : v ≤ w)
    (huh : 1 / 2 < u) :
    (∫ t in (0 : ℝ)..1,
      biasedHighProbability u t * biasedHighProbability v t * biasedHighProbability w t) =
      u - (1 - v) / 2 - (1 - w) / 4 := by
  have hu' : 2 * (1 - u) ∈ Icc (0 : ℝ) 1 := ⟨by linarith [hu.2], by linarith⟩
  have hv' : 2 * (1 - v) ∈ Icc (0 : ℝ) 1 := ⟨by linarith [hv.2], by linarith⟩
  have hw' : 2 * (1 - w) ∈ Icc (0 : ℝ) 1 := ⟨by linarith [hw.2], by linarith⟩
  have heq (t : ℝ) :
      biasedHighProbability u t * biasedHighProbability v t * biasedHighProbability w t =
      1 - lowerStep (2 * (1 - u)) t / 2 - lowerStep (2 * (1 - v)) t / 4 -
        lowerStep (2 * (1 - w)) t / 8 := by
    simp only [biasedHighProbability, if_neg (not_le.mpr huh),
      if_neg (not_le.mpr (huh.trans_le huv)),
      if_neg (not_le.mpr ((huh.trans_le huv).trans_le hvw)), lowerStep]
    split_ifs <;> norm_num <;> linarith
  simp_rw [heq]
  rw [intervalIntegral.integral_sub
    ((intervalIntegrable_const.sub ((lowerStep_integrable _).div_const 2)).sub
      ((lowerStep_integrable _).div_const 4)) ((lowerStep_integrable _).div_const 8),
    intervalIntegral.integral_sub
      (intervalIntegrable_const.sub ((lowerStep_integrable _).div_const 2))
      ((lowerStep_integrable _).div_const 4),
    intervalIntegral.integral_sub intervalIntegrable_const ((lowerStep_integrable _).div_const 2)]
  simp only [intervalIntegral.integral_div, integral_lowerStep hu',
    integral_lowerStep hv', integral_lowerStep hw']
  norm_num
  ring

variable {I : Type*} [Fintype I] [DecidableEq I]

omit [Fintype I] [DecidableEq I] in
theorem biasedHighProbability_cube (x : I → ℝ) (t : ℝ) :
    (fun i => biasedHighProbability (x i) t) ∈ cube I :=
  fun i => biasedHighProbability_mem_Icc (x i) t

/-- One finite law on the entire cube; all monomials use this same law. -/
def biasedHighLaw (x : I → ℝ) (_hx : x ∈ cube I) : Law (Vertex I) :=
  integratedBernoulli (fun t i => biasedHighProbability (x i) t)
    (biasedHighProbability_cube x)
    (fun i => biasedHighProbability_measurable (x i))

theorem biasedHighLaw_mean (x : I → ℝ) (hx : x ∈ cube I) (i : I) :
    (biasedHighLaw x hx).expect (fun v => vertexPoint v i) = x i := by
  rw [biasedHighLaw, integratedBernoulli_mean, integral_biasedHighProbability (hx i)]

theorem biasedHighLaw_hasMeans (x : I → ℝ) (hx : x ∈ cube I) :
    HasMeans (biasedHighLaw x hx) x := biasedHighLaw_mean x hx

theorem biasedHighLaw_expect_monomial (x : I → ℝ) (hx : x ∈ cube I)
    (s : Finset I) :
    (biasedHighLaw x hx).expect (fun v => monomial s (vertexPoint v)) =
      ∫ t in (0 : ℝ)..1, monomial s (fun i => biasedHighProbability (x i) t) :=
  integratedBernoulli_expect_monomial _ _ _ _

/-- Pair moment of the ambient law as a scalar integral. -/
theorem biasedHighLaw_expect_pair (x : I → ℝ) (hx : x ∈ cube I)
    {i j : I} (hij : i ≠ j) :
    (biasedHighLaw x hx).expect (fun v => monomial {i, j} (vertexPoint v)) =
      ∫ t in (0 : ℝ)..1, biasedHighProbability (x i) t * biasedHighProbability (x j) t := by
  rw [biasedHighLaw_expect_monomial]
  simp [monomial, hij]

/-- Triple moment of the ambient law as a scalar integral. -/
theorem biasedHighLaw_expect_triple (x : I → ℝ) (hx : x ∈ cube I)
    {i j k : I} (hij : i ≠ j) (hik : i ≠ k) (hjk : j ≠ k) :
    (biasedHighLaw x hx).expect (fun v => monomial {i, j, k} (vertexPoint v)) =
      ∫ t in (0 : ℝ)..1, biasedHighProbability (x i) t *
        biasedHighProbability (x j) t * biasedHighProbability (x k) t := by
  rw [biasedHighLaw_expect_monomial]
  simp [monomial, hij, hik, hjk, mul_assoc]

end
end CubicGap
