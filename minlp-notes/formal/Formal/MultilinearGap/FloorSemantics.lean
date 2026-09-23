import Formal.MultilinearGap.GeneralGaps
import Formal.MultilinearGap.MonomialEnvelope
import Formal.MultilinearGap.Attainment

/-! Exact gap and deficiency semantics for the marginal-floor argument. -/

namespace MultilinearGap

open CubicGap

noncomputable section

variable {I : Type*} [Fintype I] [DecidableEq I]

/-- A nonempty monomial has exactly the smaller of its anchor mean and the
other coordinates' total failure mean as its hull width. Singletons are included. -/
theorem monomial_gap_eq_min_otherFailures (s : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) (i : I) (hi : i ∈ s) (hmin : ∀ j ∈ s, x i ≤ x j) :
    hullGap (monomial s) x = min (x i) (otherFailures s x i) := by
  rw [monomial_hullGap_of_min_coordinate s x hx i hi hmin]
  have hs := Finset.sum_erase_add s x hi
  have hc : ((s.erase i).card : ℝ) + 1 = s.card := by
    exact_mod_cast Finset.card_erase_add_one hi
  have he : (∑ j ∈ s, x j) - (s.card - 1 : ℝ) = x i - otherFailures s x i := by
    simp only [otherFailures, Finset.sum_sub_distrib, Finset.sum_const, nsmul_eq_mul, mul_one]
    linarith
  rw [he]
  by_cases h : x i ≤ otherFailures s x i
  · rw [min_eq_left h, max_eq_left (by linarith), sub_zero]
  · rw [min_eq_right (le_of_not_ge h), max_eq_right (by linarith)]
    ring

omit [Fintype I] [DecidableEq I] in
/-- The random anchor deficiency is nonnegative at every binary vertex. -/
theorem anchor_deficiency_nonneg (s : Finset I) (i : I) (hi : i ∈ s) (v : Vertex I) :
    0 ≤ vertexPoint v i - monomial s (vertexPoint v) := by
  apply sub_nonneg.mpr
  exact monomial_le_coordinate s
    (by intro j _; simp only [vertexPoint]; split <;> norm_num) hi

/-- Expected total anchor deficiency for one common finite law. -/
def weightedAnchorDeficiency (supports : Finset (Finset I)) (a : Finset I → ℝ)
    (anchor : Finset I → I) (μ : Law (Vertex I)) : ℝ :=
  μ.expect (fun v => ∑ s ∈ supports,
    a s * (vertexPoint v (anchor s) - monomial s (vertexPoint v)))

theorem weightedAnchorDeficiency_eq (supports : Finset (Finset I)) (a : Finset I → ℝ)
    (anchor : Finset I → I) (μ : Law (Vertex I)) (x : I → ℝ) (hm : HasMeans μ x) :
    weightedAnchorDeficiency supports a anchor μ =
      (∑ s ∈ supports, a s * x (anchor s)) -
        μ.expect (fun v => supportPolynomial supports a (vertexPoint v)) := by
  have hsum : weightedAnchorDeficiency supports a anchor μ =
      ∑ s ∈ supports, μ.expect (fun v =>
        a s * (vertexPoint v (anchor s) - monomial s (vertexPoint v))) := by
    simp only [weightedAnchorDeficiency, Law.expect, Finset.mul_sum]
    rw [Finset.sum_comm]
  rw [hsum]
  have hmean (i : I) : μ.expect (fun v => vertexPoint v i) = x i := hm i
  simp only [Law.expect_const_mul, Law.expect_sub, hmean, polynomial_expect,
    mul_sub, Finset.sum_sub_distrib]

/-- Every common law's expected weighted deficiency is bounded by the actual
continuous graph-hull width. -/
theorem weightedAnchorDeficiency_le_hullGap (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I) (anchor : Finset I → I)
    (hanchor : ∀ s ∈ supports, anchor s ∈ s)
    (hmin : ∀ s ∈ supports, ∀ j ∈ s, x (anchor s) ≤ x j)
    (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    weightedAnchorDeficiency supports a anchor μ ≤
      hullGap (supportPolynomial supports a) x := by
  have hmax := positive_polynomial_maximum supports a ha x hx anchor hanchor hmin
  have hmem : μ.expect (fun v => supportPolynomial supports a (vertexPoint v)) ∈
      envelopeValues (supportPolynomial supports a) x :=
    (mem_cubeGraph_hull_iff _ (supportPolynomial_coordinate_affine supports a) x _).mpr
      ⟨μ, hm, rfl⟩
  rw [weightedAnchorDeficiency_eq supports a anchor μ x hm, hullGap, hmax.csSup_eq]
  exact sub_le_sub_left (csInf_le (polynomial_envelope_bddBelow supports a ha x) hmem) _

/-- The maximum deficiency is attained, using compactness of the actual hull
slice to obtain a minimizing finite vertex law. -/
theorem exists_weightedAnchorDeficiency_eq_hullGap (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I) (anchor : Finset I → I)
    (hanchor : ∀ s ∈ supports, anchor s ∈ s)
    (hmin : ∀ s ∈ supports, ∀ j ∈ s, x (anchor s) ≤ x j) :
    ∃ μ : Law (Vertex I), HasMeans μ x ∧
      weightedAnchorDeficiency supports a anchor μ = hullGap (supportPolynomial supports a) x := by
  obtain ⟨μ, hm, hv⟩ := (envelope_endpoints_attained_by_laws
    (supportPolynomial supports a) (supportPolynomial_coordinate_affine supports a) x hx).1
  refine ⟨μ, hm, ?_⟩
  rw [weightedAnchorDeficiency_eq supports a anchor μ x hm, hv, hullGap,
    (positive_polynomial_maximum supports a ha x hx anchor hanchor hmin).csSup_eq]

/-- The hull width is exactly the maximum over common finite laws with the
prescribed means, with no attainment hypothesis. -/
theorem hullGap_isGreatest_weightedAnchorDeficiency (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I) (anchor : Finset I → I)
    (hanchor : ∀ s ∈ supports, anchor s ∈ s)
    (hmin : ∀ s ∈ supports, ∀ j ∈ s, x (anchor s) ≤ x j) :
    IsGreatest {d : ℝ | ∃ μ : Law (Vertex I), HasMeans μ x ∧
      weightedAnchorDeficiency supports a anchor μ = d}
      (hullGap (supportPolynomial supports a) x) := by
  refine ⟨exists_weightedAnchorDeficiency_eq_hullGap supports a ha x hx anchor hanchor hmin, ?_⟩
  rintro d ⟨μ, hm, rfl⟩
  exact weightedAnchorDeficiency_le_hullGap supports a ha x hx anchor hanchor hmin μ hm

end
end MultilinearGap
