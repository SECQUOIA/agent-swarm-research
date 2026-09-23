import Mathlib.Analysis.Calculus.LocalExtr.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Topology.Order.Compact
import Mathlib.Tactic

/-! A quadratic angular sampling estimate. -/

namespace InfiniteAggregation

noncomputable def angularForm (a b c t : ℝ) : ℝ :=
  a * Real.cos t ^ 2 + 2 * b * Real.cos t * Real.sin t + c * Real.sin t ^ 2

lemma angularForm_continuous (a b c : ℝ) : Continuous (angularForm a b c) := by
  unfold angularForm
  fun_prop

lemma angularForm_hasDerivAt (a b c t : ℝ) :
    HasDerivAt (angularForm a b c)
      (2 * ((c - a) * Real.cos t * Real.sin t +
        b * (Real.cos t ^ 2 - Real.sin t ^ 2))) t := by
  have h₁ := ((Real.hasDerivAt_cos t).pow 2).const_mul a
  have h₂ := ((Real.hasDerivAt_cos t).const_mul (2 * b)).mul (Real.hasDerivAt_sin t)
  have h₃ := ((Real.hasDerivAt_sin t).pow 2).const_mul c
  unfold angularForm
  convert (h₁.add h₂).add h₃ using 1 <;> first | rfl | ring

lemma angularForm_rotation (a b c t s : ℝ)
    (h : (c - a) * Real.cos t * Real.sin t +
      b * (Real.cos t ^ 2 - Real.sin t ^ 2) = 0) :
    angularForm a b c s = angularForm a b c t +
      (a + c - 2 * angularForm a b c t) * Real.sin (s - t) ^ 2 := by
  have hu := Real.sin_sq_add_cos_sq t
  have hv := Real.sin_sq_add_cos_sq (s - t)
  have hsin : Real.sin s = Real.sin (s - t) * Real.cos t +
      Real.cos (s - t) * Real.sin t := by
    rw [← Real.sin_add]; congr 1; ring
  have hcos : Real.cos s = Real.cos (s - t) * Real.cos t -
      Real.sin (s - t) * Real.sin t := by
    rw [← Real.cos_add]; congr 1; ring
  unfold angularForm
  rw [hsin, hcos]
  linear_combination
    (a * Real.cos t ^ 2 + 2 * b * Real.cos t * Real.sin t + c * Real.sin t ^ 2) * hv +
    (a + c) * Real.sin (s - t) ^ 2 * hu +
    2 * Real.sin (s - t) * Real.cos (s - t) * h

lemma angularForm_lower (a b c t : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c)
    (hb : -(3 / 2 : ℝ) ≤ b) (ht : t ∈ Set.Icc 0 (Real.pi / 2)) :
    -(3 / 2 : ℝ) ≤ angularForm a b c t := by
  have hs : 0 ≤ Real.sin t := Real.sin_nonneg_of_mem_Icc ⟨ht.1, by
    linarith [Real.pi_pos, ht.1, ht.2]⟩
  have hcos : 0 ≤ Real.cos t := Real.cos_nonneg_of_mem_Icc ⟨by
    linarith [Real.pi_pos, ht.1], ht.2⟩
  have hprod := mul_nonneg hcos hs
  have hunit := Real.sin_sq_add_cos_sq t
  have hsmall : 2 * Real.cos t * Real.sin t ≤ 1 := by
    nlinarith [sq_nonneg (Real.cos t - Real.sin t)]
  have hbprod := mul_nonneg (show 0 ≤ b + 3 / 2 by linarith) hprod
  unfold angularForm
  nlinarith [mul_nonneg ha (sq_nonneg (Real.cos t)),
    mul_nonneg hc (sq_nonneg (Real.sin t))]

theorem angular_sample_lower_bound (a b c ρ : ℝ) (samples : Set ℝ)
    (ha : a ∈ Set.Icc 0 1) (hc : c ∈ Set.Icc 0 1)
    (hb : -(3 / 2 : ℝ) ≤ b)
    (hcover : ∀ t ∈ Set.Icc 0 (Real.pi / 2), ∃ s ∈ samples, |s - t| ≤ ρ)
    (hsamples : ∀ s ∈ samples, 0 ≤ angularForm a b c s)
    (t : ℝ) (ht : t ∈ Set.Icc 0 (Real.pi / 2)) :
    -5 * ρ ^ 2 ≤ angularForm a b c t := by
  obtain ⟨u, hu, hmin⟩ := isCompact_Icc.exists_isMinOn
    (Set.nonempty_Icc.mpr (by positivity : (0 : ℝ) ≤ Real.pi / 2))
    (angularForm_continuous a b c).continuousOn
  by_cases hzero : u = 0
  · have hm := hmin ht
    simp [hzero, angularForm] at hm
    unfold angularForm
    nlinarith [sq_nonneg ρ, ha.1]
  by_cases hend : u = Real.pi / 2
  · have hm := hmin ht
    simp [hend, angularForm] at hm
    unfold angularForm
    nlinarith [sq_nonneg ρ, hc.1]
  have hinter : u ∈ Set.Ioo 0 (Real.pi / 2) :=
    ⟨lt_of_le_of_ne hu.1 (Ne.symm hzero), lt_of_le_of_ne hu.2 hend⟩
  have hder := (hmin.isLocalMin (Icc_mem_nhds hinter.1 hinter.2)).hasDerivAt_eq_zero
    (angularForm_hasDerivAt a b c u)
  have hstat : (c - a) * Real.cos u * Real.sin u +
      b * (Real.cos u ^ 2 - Real.sin u ^ 2) = 0 := by linarith
  obtain ⟨s, hs, hdist⟩ := hcover u hu
  have hsnon := hsamples s hs
  rw [angularForm_rotation a b c u s hstat] at hsnon
  have hlo := angularForm_lower a b c u ha.1 hc.1 hb hu
  have hcoef : a + c - 2 * angularForm a b c u ≤ 5 := by
    linarith [ha.2, hc.2]
  have hsq : Real.sin (s - u) ^ 2 ≤ ρ ^ 2 := by
    have habs := Real.abs_sin_le_abs (x := s - u)
    have hρ : 0 ≤ ρ := le_trans (abs_nonneg _) hdist
    have hsin := le_trans habs hdist
    simpa only [sq_abs] using (sq_le_sq₀ (abs_nonneg _) hρ).mpr hsin
  have hmul := mul_le_mul_of_nonneg_right hcoef (sq_nonneg (Real.sin (s - u)))
  have hm : angularForm a b c u ≤ angularForm a b c t := hmin ht
  nlinarith

end InfiniteAggregation
