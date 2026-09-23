import Formal.MultilinearGap.PaperFoundations

/-! Local nonnegative deficiencies on original nonnegative box scopes.
Expansion constructs a majorant, without changing the incidence graph. -/
namespace MultilinearGap
open CubicGap
noncomputable section
variable {I : Type*} [Fintype I] [DecidableEq I]

def feedbackMonomialMajorant (s : Finset I) (x y : I → ℝ) : ℝ :=
  if h : s.Nonempty then y (Classical.choose (monomial_min_anchor s h x)) else 1

theorem feedbackMonomialMajorant_expect (s : Finset I) (x : I → ℝ)
    (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    μ.expect (fun v => feedbackMonomialMajorant s x (vertexPoint v)) =
      monomialUpper s x := by
  unfold feedbackMonomialMajorant
  split_ifs with h
  · have ha := Classical.choose_spec (monomial_min_anchor s h x)
    rw [hm, monomialUpper_eq_anchor s x _ ha.1 ha.2]
  · have hs : s = ∅ := Finset.not_nonempty_iff_eq_empty.mp h
    simp [hs]

omit [Fintype I] [DecidableEq I] in
theorem monomial_le_feedbackMonomialMajorant (s : Finset I) (x y : I → ℝ)
    (hy : y ∈ cube I) : monomial s y ≤ feedbackMonomialMajorant s x y := by
  unfold feedbackMonomialMajorant
  split_ifs with h
  · exact monomial_le_coordinate s (fun i _ => hy i)
      (Classical.choose_spec (monomial_min_anchor s h x)).1
  · have hs : s = ∅ := Finset.not_nonempty_iff_eq_empty.mp h
    simp [hs, monomial]

omit [Fintype I] [DecidableEq I] in
theorem feedbackMonomialMajorant_congr (s : Finset I) (x y z : I → ℝ)
    (h : ∀ i ∈ s, y i = z i) :
    feedbackMonomialMajorant s x y = feedbackMonomialMajorant s x z := by
  unfold feedbackMonomialMajorant
  split_ifs with hs
  · exact h _ (Classical.choose_spec (monomial_min_anchor s hs x)).1
  · rfl

/-- Affine majorant of the original factor, on its original scope. -/
def feedbackBoxMajorant (l u : I → ℝ) (s : Finset I) (x y : I → ℝ) : ℝ :=
  ∑ t ∈ s.powerset, boxExpansionCoefficient l u s t * feedbackMonomialMajorant t x y

/-- Local nonnegative payoff for an original box monomial. -/
def feedbackBoxDeficiency (l u : I → ℝ) (s : Finset I) (x y : I → ℝ) : ℝ :=
  feedbackBoxMajorant l u s x y - monomial s (boxPoint l u y)

omit [Fintype I] in
theorem feedbackBoxDeficiency_nonneg (l u : I → ℝ)
    (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (s : Finset I) (x y : I → ℝ) (hy : y ∈ cube I) :
    0 ≤ feedbackBoxDeficiency l u s x y := by
  rw [feedbackBoxDeficiency, sub_nonneg, monomial_box_expansion]
  unfold supportPolynomial feedbackBoxMajorant
  exact Finset.sum_le_sum fun t _ => mul_le_mul_of_nonneg_left
    (monomial_le_feedbackMonomialMajorant t x y hy)
    (boxExpansionCoefficient_nonneg l u hl hlu s t)

omit [Fintype I] in
theorem feedbackBoxDeficiency_congr (l u : I → ℝ) (s : Finset I)
    (x y z : I → ℝ) (h : ∀ i ∈ s, y i = z i) :
    feedbackBoxDeficiency l u s x y = feedbackBoxDeficiency l u s x z := by
  unfold feedbackBoxDeficiency feedbackBoxMajorant
  congr 1
  · exact Finset.sum_congr rfl fun t ht => congrArg (_ * ·)
      (feedbackMonomialMajorant_congr t x y z fun i hi =>
        h i ((Finset.mem_powerset.mp ht) hi))
  · exact Finset.prod_congr rfl fun i hi => by simp only [boxPoint, h i hi]

theorem feedbackBoxMajorant_expect (l u : I → ℝ) (s : Finset I)
    (x : I → ℝ) (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    μ.expect (fun v => feedbackBoxMajorant l u s x (vertexPoint v)) =
      ∑ t ∈ s.powerset, boxExpansionCoefficient l u s t * monomialUpper t x := by
  unfold feedbackBoxMajorant Law.expect
  simp only [Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro t ht
  rw [show (∑ v, μ.weight v *
      (boxExpansionCoefficient l u s t * feedbackMonomialMajorant t x (vertexPoint v))) =
      boxExpansionCoefficient l u s t *
        μ.expect (fun v => feedbackMonomialMajorant t x (vertexPoint v)) by
    simp only [Law.expect, Finset.mul_sum]; congr 1; ext v; ring]
  rw [feedbackMonomialMajorant_expect t x μ hm]

theorem feedbackBoxMajorant_threshold (l u : I → ℝ) (s : Finset I)
    (x : I → ℝ) (hx : x ∈ cube I) :
    (thresholdLaw x).expect (fun v => monomial s (boxPoint l u (vertexPoint v))) =
      ∑ t ∈ s.powerset, boxExpansionCoefficient l u s t * monomialUpper t x := by
  simp_rw [monomial_box_expansion]
  rw [polynomial_expect]
  simp_rw [thresholdLaw_monomial_upper _ x hx]

omit [Fintype I] in
theorem feedbackBoxMonomial_maximum [Finite I] (l u : I → ℝ)
    (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    IsGreatest (envelopeValues (fun y => monomial s (boxPoint l u y)) x)
      (∑ t ∈ s.powerset, boxExpansionCoefficient l u s t * monomialUpper t x) := by
  have he : (fun y => monomial s (boxPoint l u y)) =
      supportPolynomial s.powerset (boxExpansionCoefficient l u s) := by
    funext y; exact monomial_box_expansion l u y s
  rw [he]
  exact positive_polynomial_maximum_general _ _
    (fun t _ => boxExpansionCoefficient_nonneg l u hl hlu s t) x hx

/-- No feasible local law exceeds the original factor's gap in deficiency. -/
theorem feedbackBoxDeficiency_le_gap (l u : I → ℝ)
    (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I)
    (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    μ.expect (fun v => feedbackBoxDeficiency l u s x (vertexPoint v)) ≤
      boxHullGap l u (monomial s) (boxPoint l u x) := by
  have hf := separatelyAffine_box_monomial l u s
  have hinf := csInf_le (envelopeValues_isCompact _ hf x).bddBelow
    ((mem_cubeGraph_hull_iff _ hf x _).mpr ⟨μ, hm, rfl⟩)
  simp only [feedbackBoxDeficiency, Law.expect_sub]
  rw [feedbackBoxMajorant_expect l u s x μ hm,
    boxHullGap_eq_of_mem l u hlu _ x hx, hullGap,
    (feedbackBoxMonomial_maximum l u hl hlu s x hx).csSup_eq]
  linarith

/-- A feasible law attains the original box gap as expected deficiency,
including fixed coordinates and empty scopes. -/
theorem feedbackBoxDeficiency_attains_gap (l u : I → ℝ)
    (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    ∃ μ : Law (Vertex I), HasMeans μ x ∧
      μ.expect (fun v => feedbackBoxDeficiency l u s x (vertexPoint v)) =
        boxHullGap l u (monomial s) (boxPoint l u x) := by
  obtain ⟨μ, hm, hv⟩ := (envelope_endpoints_attained_by_laws
    (fun y => monomial s (boxPoint l u y))
    (separatelyAffine_box_monomial l u s) x hx).1
  refine ⟨μ, hm, ?_⟩
  simp only [feedbackBoxDeficiency, Law.expect_sub]
  rw [feedbackBoxMajorant_expect l u s x μ hm, hv,
    boxHullGap_eq_of_mem l u hlu _ x hx, hullGap,
    (feedbackBoxMonomial_maximum l u hl hlu s x hx).csSup_eq]


private theorem feedbackBoxPolynomial_expect (l u : I → ℝ)
    (S : Finset (Finset I)) (a : Finset I → ℝ) (μ : Law (Vertex I)) :
    μ.expect (fun v => supportPolynomial S a (boxPoint l u (vertexPoint v))) =
      ∑ s ∈ S, a s * μ.expect (fun v => monomial s (boxPoint l u (vertexPoint v))) := by
  simp only [supportPolynomial, Law.expect, Finset.mul_sum]
  rw [Finset.sum_comm]
  exact Finset.sum_congr rfl fun s _ => by
    exact Finset.sum_congr rfl fun v _ => by ring

omit [Fintype I] in
/-- All original box factors attain their upper envelopes under one law. -/
theorem feedbackBoxPolynomial_maximum [Finite I] (l u : I → ℝ)
    (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (S : Finset (Finset I)) (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I) :
    IsGreatest (envelopeValues (fun y => supportPolynomial S a (boxPoint l u y)) x)
      (∑ s ∈ S, a s *
        ∑ t ∈ s.powerset, boxExpansionCoefficient l u s t * monomialUpper t x) := by
  let _ := Fintype.ofFinite I
  apply maximum_from_laws _
    (separatelyAffine_boxPoint _ (supportPolynomial_coordinate_affine S a) l u)
  · intro μ hm
    rw [feedbackBoxPolynomial_expect]
    apply Finset.sum_le_sum
    intro s hs
    apply mul_le_mul_of_nonneg_left _ (ha s hs)
    exact (feedbackBoxMonomial_maximum l u hl hlu s x hx).2
      ((mem_cubeGraph_hull_iff _ (separatelyAffine_box_monomial l u s) x _).mpr
        ⟨μ, hm, rfl⟩)
  · refine ⟨thresholdLaw x, thresholdLaw_hasMeans x hx, ?_⟩
    rw [feedbackBoxPolynomial_expect]
    exact Finset.sum_congr rfl fun s _ => by rw [feedbackBoxMajorant_threshold l u s x hx]

/-- The semantic last step of the feedback argument. This lemma assumes a
feasible law with the required local deficiencies; the structural construction
of that law is a separate obligation. No expanded incidence graph is used. -/
theorem feedbackBox_gap_of_local_deficiencies (l u : I → ℝ)
    (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (S : Finset (Finset I)) (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I) (c : ℝ) (hc : 0 < c)
    (μ : Law (Vertex I)) (hm : HasMeans μ x)
    (hdef : ∀ s ∈ S, c * boxHullGap l u (monomial s) (boxPoint l u x) ≤
      μ.expect (fun v => feedbackBoxDeficiency l u s x (vertexPoint v))) :
    boxTermwiseGap S a l u (boxPoint l u x) ≤
      (1 / c) * boxHullGap l u (supportPolynomial S a) (boxPoint l u x) := by
  let f := fun y => supportPolynomial S a (boxPoint l u y)
  have hf : SeparatelyAffine f :=
    separatelyAffine_boxPoint _ (supportPolynomial_coordinate_affine S a) l u
  have hmax := feedbackBoxPolynomial_maximum l u hl hlu S a ha x hx
  have hinf := csInf_le (envelopeValues_isCompact f hf x).bddBelow
    ((mem_cubeGraph_hull_iff f hf x _).mpr ⟨μ, hm, rfl⟩)
  have hsum : c * boxTermwiseGap S a l u (boxPoint l u x) ≤
      (∑ s ∈ S, a s *
        ∑ t ∈ s.powerset, boxExpansionCoefficient l u s t * monomialUpper t x) -
      μ.expect (fun v => f (vertexPoint v)) := by
    rw [boxTermwiseGap, Finset.mul_sum]
    change _ ≤ _ - μ.expect
      (fun v => supportPolynomial S a (boxPoint l u (vertexPoint v)))
    rw [feedbackBoxPolynomial_expect, ← Finset.sum_sub_distrib]
    apply Finset.sum_le_sum
    intro s hs
    have hh := mul_le_mul_of_nonneg_left (hdef s hs) (ha s hs)
    simp only [feedbackBoxDeficiency, Law.expect_sub,
      feedbackBoxMajorant_expect l u s x μ hm] at hh
    nlinarith
  have hbound : c * boxTermwiseGap S a l u (boxPoint l u x) ≤ hullGap f x := by
    rw [hullGap, show sSup (envelopeValues f x) = _ from hmax.csSup_eq]
    linarith
  rw [boxHullGap_eq_of_mem l u hlu _ x hx]
  have := (le_div_iff₀ hc).mpr (by simpa [mul_comm] using hbound)
  simpa [f, div_eq_mul_inv, mul_comm] using this

end
end MultilinearGap
