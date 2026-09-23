import Formal.MultilinearGap.EasyTerms
import Formal.MultilinearGap.Mixture
import Formal.MultilinearGap.Couplings
import Formal.MultilinearGap.AsymptoticScalars
import Formal.MultilinearGap.HarmonicLawGain

/-! The common rounding law gives the sharp upper estimate for actual graph-hull gaps. -/

namespace MultilinearGap

open CubicGap Real

noncomputable section

variable {I : Type*} [Fintype I] [DecidableEq I]

theorem sharpM_ge_one {Λ : ℝ} (hΛ : exp 6 ≤ Λ) : 1 ≤ exp (Λ - 1) := by
  apply Real.one_le_exp
  have : (1 : ℝ) ≤ exp 6 := Real.one_le_exp (by norm_num)
  linarith

/-- One law works for all supports of the polynomial simultaneously. -/
def sharpLaw (x : I → ℝ) (hx : x ∈ cube I) (Λ : ℝ) (hΛ : exp 6 ≤ Λ) :
    Law (Vertex I) :=
  threeMix (harmonicLaw x hx (exp (Λ - 1)) (sharpM_ge_one hΛ))
    (failureThresholdLaw x hx) (bernoulliLaw x hx)
    (1 / sharpH Λ) (sharpA Λ) (2 / easyConstant)
    (div_pos one_pos (sharpH_pos hΛ)) (sharpA_pos hΛ)
    (div_pos (by norm_num) easyConstant_pos)

theorem sharpLaw_hasMeans (x : I → ℝ) (hx : x ∈ cube I)
    (Λ : ℝ) (hΛ : exp 6 ≤ Λ) : HasMeans (sharpLaw x hx Λ hΛ) x := by
  intro i
  apply threeMix_expect_common
  · exact harmonicLaw_hasMeans x hx (exp (Λ - 1)) (sharpM_ge_one hΛ) i
  · exact failureThresholdLaw_hasMeans x hx i
  · exact bernoulliLaw_mean x hx i

/-- The same mixture captures each nonempty support's envelope width. -/
theorem sharpLaw_deficiency_nonempty (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I)
    (Λ : ℝ) (hΛ : exp 6 ≤ Λ) (i : I) (hi : i ∈ s)
    (hmin : ∀ j ∈ s, x i ≤ x j) (hdegree : (s.card : ℝ) ≤ exp (Λ - 1)) :
    hullGap (monomial s) x / sharpZ Λ ≤
      x i - (sharpLaw x hx Λ hΛ).expect (fun v => monomial s (vertexPoint v)) := by
  let μH := harmonicLaw x hx (exp (Λ - 1)) (sharpM_ge_one hΛ)
  let μT := failureThresholdLaw x hx
  let μI := bernoulliLaw x hx
  let f := fun v => monomial s (vertexPoint v)
  let T := hullGap (monomial s) x
  have hnH : 0 ≤ x i - μH.expect f := monomial_deficiency_nonneg s x i hi μH
    (harmonicLaw_hasMeans x hx _ _)
  have hnT : 0 ≤ x i - μT.expect f := monomial_deficiency_nonneg s x i hi μT
    (failureThresholdLaw_hasMeans x hx)
  have hnI : 0 ≤ x i - μI.expect f := monomial_deficiency_nonneg s x i hi μI
    (fun j => bernoulliLaw_mean x hx j)
  have hgood : T ≤ (1 / sharpH Λ) * (x i - μH.expect f) ∨
      T ≤ sharpA Λ * (x i - μT.expect f) ∨
      T ≤ (2 / easyConstant) * (x i - μI.expect f) := by
    by_cases hT : T ≤ 0
    · exact Or.inl (hT.trans (mul_nonneg (by positivity [sharpH_pos hΛ]) hnH))
    have hTpos : 0 < T := lt_of_not_ge hT
    by_cases heasy : 1 / 2 ≤ x i ∨ ∃ j ∈ s.erase i, x j ≤ 1 / 2
    · right; right
      have he := bernoulli_easy_gap s x hx i hi hmin heasy
      rw [div_mul_eq_mul_div]
      apply (le_div_iff₀ easyConstant_pos).mpr
      dsimp [T, μI, f]
      linarith
    · have hlow : x i ≤ 1 / 2 := by
        have : ¬1 / 2 ≤ x i := fun h => heasy (Or.inl h)
        linarith
      have hhigh : ∀ j ∈ s.erase i, 1 / 2 < x j := by
        intro j hj
        exact lt_of_not_ge (fun h => heasy (Or.inr ⟨j, hj, h⟩))
      have hbound := monomial_gap_le_min s x hx i hi hmin
      have hTu : T ≤ x i := hbound.trans (min_le_left _ _)
      have hTS : T ≤ otherFailures s x i := hbound.trans (min_le_right _ _)
      by_cases hlarge : ∃ j ∈ s.erase i, T / sharpA Λ ≤ 1 - x j
      · right; left
        obtain ⟨j, hj, hjlarge⟩ := hlarge
        have hTdiv : T / sharpA Λ ≤ T :=
          div_le_self hTpos.le (sharpA_gt_one hΛ).le
        have hh := failureThresholdLaw_deficiency_lower x hx s i j hi
          (Finset.mem_of_mem_erase hj) hlow (hhigh j hj)
        have hsmall : T / sharpA Λ ≤ x i - μT.expect f :=
          (le_min (hTdiv.trans hTu) hjlarge).trans hh
        exact (div_le_iff₀ (sharpA_pos hΛ)).mp hsmall |>.trans_eq (mul_comm _ _)
      · left
        have hsmall : ∀ j ∈ s.erase i, 1 - x j ≤ T / sharpA Λ := by
          intro j hj
          exact (lt_of_not_ge (fun h => hlarge ⟨j, hj, h⟩)).le
        have hc : ((s.erase i).card : ℝ) ≤ s.card := by
          exact_mod_cast (Finset.card_erase_le (s := s) (a := i))
        have hcard : ((s.erase i).card : ℝ) ≤ exp (Λ - 1) := hc.trans hdegree
        have hh := harmonicLaw_sharp_gain x hx Λ hΛ s i hi hlow hhigh T hTpos
          hTu hTS hcard hsmall
        have hdiv := (le_div_iff₀ (sharpH_pos hΛ)).mpr (by
          simpa [mul_comm] using hh)
        simpa [div_eq_mul_inv, mul_comm, μH, f] using hdiv
  have hm := threeMix_deficiency_ge μH μT μI
    (1 / sharpH Λ) (sharpA Λ) (2 / easyConstant)
    (div_pos one_pos (sharpH_pos hΛ)) (sharpA_pos hΛ)
    (div_pos (by norm_num) easyConstant_pos) f (x i) T hnH hnT hnI hgood
  exact hm

/-- The shared rounding law works for every support, including constant terms. -/
theorem sharpLaw_deficiency (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I)
    (Λ : ℝ) (hΛ : exp 6 ≤ Λ) (hdegree : (s.card : ℝ) ≤ exp (Λ - 1)) :
    (1 / sharpZ Λ) * hullGap (monomial s) x ≤
      monomialUpper s x -
        (sharpLaw x hx Λ hΛ).expect (fun v => monomial s (vertexPoint v)) := by
  by_cases hs : s.Nonempty
  · obtain ⟨i, hi, hmin⟩ := monomial_min_anchor s hs x
    rw [monomialUpper_eq_anchor s x i hi hmin]
    simpa [div_eq_mul_inv, mul_comm] using
      sharpLaw_deficiency_nonempty s x hx Λ hΛ i hi hmin hdegree
  · have : s = ∅ := Finset.not_nonempty_iff_eq_empty.mp hs
    subst s
    simp [monomial_gap_empty x hx, monomial]

/-- The sharp cube upper bound for every positive squarefree polynomial. -/
theorem sharp_cube_gap_bound (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I) (Λ : ℝ) (hΛ : exp 6 ≤ Λ)
    (hdegree : ∀ s ∈ supports, (s.card : ℝ) ≤ exp (Λ - 1)) :
    weightedTermwiseGap supports a x ≤
      sharpZ Λ * hullGap (supportPolynomial supports a) x := by
  have h := coupling_gap_bound_general supports a ha x hx (1 / sharpZ Λ)
    (div_pos one_pos (sharpZ_pos hΛ)) (sharpLaw x hx Λ hΛ)
    (sharpLaw_hasMeans x hx Λ hΛ)
    (fun s hs => sharpLaw_deficiency s x hx Λ hΛ (hdegree s hs))
  simpa using h

end
end MultilinearGap
