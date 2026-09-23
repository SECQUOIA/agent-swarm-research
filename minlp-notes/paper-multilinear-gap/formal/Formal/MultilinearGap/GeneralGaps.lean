import Formal.MultilinearGap.EnvelopeBounds
import Formal.CubicGap.TermwiseUpper
import Formal.MultilinearGap.IntegratedLaws

/-! Bounds for actual continuous graph-hull gaps of positive squarefree polynomials. -/
namespace MultilinearGap
open CubicGap
noncomputable section
variable {I : Type*} [Fintype I] [DecidableEq I]

/-- Coefficients weight the individual monomial envelope widths. -/
def weightedTermwiseGap (supports : Finset (Finset I))
    (coefficient : Finset I → ℝ) (x : I → ℝ) : ℝ :=
  ∑ s ∈ supports, coefficient s * hullGap (monomial s) x

/-- The failures of the coordinates other than the chosen anchor. -/
def otherFailures (s : Finset I) (x : I → ℝ) (i : I) : ℝ :=
  ∑ j ∈ s.erase i, (1 - x j)

theorem polynomial_expect (supports : Finset (Finset I)) (a : Finset I → ℝ)
    (μ : Law (Vertex I)) :
    μ.expect (fun v => supportPolynomial supports a (vertexPoint v)) =
      ∑ s ∈ supports, a s * μ.expect (fun v => monomial s (vertexPoint v)) := by
  simp only [supportPolynomial, Law.expect, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro s _
  apply Finset.sum_congr rfl
  intro v _
  ring

omit [Fintype I] [DecidableEq I] in
theorem polynomial_envelope_bddBelow [Finite I] (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s) (x : I → ℝ) :
    BddBelow (envelopeValues (supportPolynomial supports a) x) := by
  classical
  let := Fintype.ofFinite I
  refine ⟨0, ?_⟩
  intro z hz
  obtain ⟨μ, _, hv⟩ := (mem_cubeGraph_hull_iff _
    (supportPolynomial_coordinate_affine supports a) x z).mp hz
  rw [← hv]
  apply μ.expect_nonneg
  intro v
  exact supportPolynomial_nonneg supports a ha (by
    intro i; simp only [vertexPoint]; split <;> norm_num)

/-- The elementary monomial gap bound needs no formula for its lower envelope. -/
theorem monomial_gap_le_min (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I)
    (i : I) (hi : i ∈ s) (hmin : ∀ j ∈ s, x i ≤ x j) :
    hullGap (monomial s) x ≤ min (x i) (otherFailures s x i) := by
  have hmax := monomial_maximum_of_min_coordinate s x hx i hi hmin
  have hnonneg : ∀ z ∈ envelopeValues (monomial s) x, 0 ≤ z := by
    intro z hz
    obtain ⟨μ, _, hv⟩ := (mem_cubeGraph_hull_iff _
      (monomial_coordinate_affine s) x z).mp hz
    rw [← hv]
    exact monomial_expect_nonneg s μ
  have hlower : ∀ z ∈ envelopeValues (monomial s) x,
      x i - otherFailures s x i ≤ z := by
    intro z hz
    obtain ⟨μ, hm, hv⟩ := (mem_cubeGraph_hull_iff _
      (monomial_coordinate_affine s) x z).mp hz
    have hb := monomial_expect_lower s μ x hm
    rw [hv] at hb
    have hs := Finset.sum_erase_add s x hi
    have hc := Finset.card_erase_add_one hi
    have hcast : ((s.erase i).card : ℝ) + 1 = s.card := by exact_mod_cast hc
    simp only [otherFailures, Finset.sum_sub_distrib, Finset.sum_const,
      nsmul_eq_mul, mul_one]
    linarith
  have h0 := le_csInf ⟨x i, hmax.1⟩ hnonneg
  have h1 := le_csInf ⟨x i, hmax.1⟩ hlower
  rw [hullGap, hmax.csSup_eq]
  exact le_min (by linarith) (by linarith)

/-- A law attaining every monomial maximum also attains their positive sum. -/
theorem polynomial_maximum_of_common_law (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (x : I → ℝ) (anchor : Finset I → I)
    (hanchor : ∀ s ∈ supports, anchor s ∈ s)
    (μ : Law (Vertex I)) (hm : HasMeans μ x)
    (hv : ∀ s ∈ supports, μ.expect (fun v => monomial s (vertexPoint v)) =
      x (anchor s)) :
    IsGreatest (envelopeValues (supportPolynomial supports a) x)
      (∑ s ∈ supports, a s * x (anchor s)) := by
  apply maximum_from_laws _ (supportPolynomial_coordinate_affine supports a)
  · intro ν hν
    rw [polynomial_expect]
    apply Finset.sum_le_sum
    intro s hs
    apply mul_le_mul_of_nonneg_left _ (ha s hs)
    rw [← hν (anchor s)]
    exact ν.expect_mono fun v => monomial_le_coordinate s
      (by intro j _; simp only [vertexPoint]; split <;> norm_num) (hanchor s hs)
  · refine ⟨μ, hm, ?_⟩
    rw [polynomial_expect]
    exact Finset.sum_congr rfl fun s hs => by rw [hv s hs]

/-- A common feasible law with enough deficiency in every monomial bounds the
termwise width by the width of the actual polynomial graph hull. -/
theorem coupling_gap_bound_of_maximum (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (x : I → ℝ) (anchor : Finset I → I) (c : ℝ) (hc : 0 < c)
    (hmax : IsGreatest (envelopeValues (supportPolynomial supports a) x)
      (∑ s ∈ supports, a s * x (anchor s)))
    (μ : Law (Vertex I)) (hm : HasMeans μ x)
    (hdef : ∀ s ∈ supports, c * hullGap (monomial s) x ≤
      x (anchor s) - μ.expect (fun v => monomial s (vertexPoint v))) :
    weightedTermwiseGap supports a x ≤
      (1 / c) * hullGap (supportPolynomial supports a) x := by
  have hattain : μ.expect (fun v => supportPolynomial supports a (vertexPoint v)) ∈
      envelopeValues (supportPolynomial supports a) x :=
    (mem_cubeGraph_hull_iff _ (supportPolynomial_coordinate_affine supports a) x _).mpr
      ⟨μ, hm, rfl⟩
  have hinf := csInf_le (polynomial_envelope_bddBelow supports a ha x) hattain
  have hsum : c * weightedTermwiseGap supports a x ≤
      (∑ s ∈ supports, a s * x (anchor s)) -
        μ.expect (fun v => supportPolynomial supports a (vertexPoint v)) := by
    rw [weightedTermwiseGap, polynomial_expect, Finset.mul_sum,
      ← Finset.sum_sub_distrib]
    apply Finset.sum_le_sum
    intro s hs
    have hh := mul_le_mul_of_nonneg_left (hdef s hs) (ha s hs)
    nlinarith
  have hbound : c * weightedTermwiseGap supports a x ≤
      hullGap (supportPolynomial supports a) x := by
    rw [hullGap, hmax.csSup_eq]
    linarith
  have := (le_div_iff₀ hc).mpr (by simpa [mul_comm] using hbound)
  simpa [div_eq_mul_inv, mul_comm] using this

/-- A common threshold makes every coordinate success event nested. -/
def thresholdProb (x : I → ℝ) (t : ℝ) (i : I) : ℝ :=
  if t ≤ x i then 1 else 0

omit [Fintype I] [DecidableEq I] in
theorem thresholdProb_mem_cube (x : I → ℝ) (t : ℝ) :
    thresholdProb x t ∈ cube I := by
  intro i
  simp only [thresholdProb]
  split <;> norm_num

omit [Fintype I] [DecidableEq I] in
theorem thresholdProb_measurable (x : I → ℝ) (i : I) :
    Measurable (fun t => thresholdProb x t i) :=
  measurable_const.ite measurableSet_Iic measurable_const

omit [Fintype I] [DecidableEq I] in
theorem thresholdProb_integral (x : I → ℝ) (hx : x ∈ cube I) (i : I) :
    (∫ t in (0 : ℝ)..1, thresholdProb x t i) = x i := by
  change (∫ t in (0 : ℝ)..1, Set.indicator {t : ℝ | t ≤ x i}
    (fun _ => (1 : ℝ)) t) = x i
  rw [intervalIntegral.integral_indicator (hx i)]
  simp

def thresholdLaw (x : I → ℝ) : Law (Vertex I) :=
  integratedBernoulli (thresholdProb x) (thresholdProb_mem_cube x)
    (thresholdProb_measurable x)

theorem thresholdLaw_hasMeans (x : I → ℝ) (hx : x ∈ cube I) :
    HasMeans (thresholdLaw x) x := by
  intro i
  rw [thresholdLaw, integratedBernoulli_mean, thresholdProb_integral x hx]

theorem thresholdLaw_monomial (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I)
    (i : I) (hi : i ∈ s) (hmin : ∀ j ∈ s, x i ≤ x j) :
    (thresholdLaw x).expect (fun v => monomial s (vertexPoint v)) = x i := by
  have heq (t : ℝ) : monomial s (thresholdProb x t) = thresholdProb x t i := by
    by_cases ht : t ≤ x i
    · have hj : ∀ j ∈ s, t ≤ x j := fun j hj => ht.trans (hmin j hj)
      simp only [monomial, thresholdProb, if_pos ht]
      exact Finset.prod_eq_one fun j hj' => if_pos (hj j hj')
    · rw [show thresholdProb x t i = 0 by simp [thresholdProb, ht]]
      exact Finset.prod_eq_zero hi (by simp [thresholdProb, ht])
  rw [thresholdLaw, integratedBernoulli_expect_monomial]
  simp_rw [heq]
  exact thresholdProb_integral x hx i

omit [Fintype I] [DecidableEq I] in
/-- Positive squarefree monomials attain all their upper envelopes together. -/
theorem positive_polynomial_maximum [Finite I] (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I) (anchor : Finset I → I)
    (hanchor : ∀ s ∈ supports, anchor s ∈ s)
    (hmin : ∀ s ∈ supports, ∀ j ∈ s, x (anchor s) ≤ x j) :
    IsGreatest (envelopeValues (supportPolynomial supports a) x)
      (∑ s ∈ supports, a s * x (anchor s)) := by
  classical
  let := Fintype.ofFinite I
  exact polynomial_maximum_of_common_law supports a ha x anchor hanchor
    (thresholdLaw x) (thresholdLaw_hasMeans x hx)
    (fun s hs => thresholdLaw_monomial s x hx (anchor s) (hanchor s hs) (hmin s hs))

/-- Any feasible coupling has nonnegative deficiency from a monomial maximum. -/
theorem monomial_deficiency_nonneg (s : Finset I) (x : I → ℝ)
    (i : I) (hi : i ∈ s) (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    0 ≤ x i - μ.expect (fun v => monomial s (vertexPoint v)) := by
  apply sub_nonneg.mpr
  rw [← hm i]
  exact μ.expect_mono fun v => monomial_le_coordinate s
    (by intro j _; simp only [vertexPoint]; split <;> norm_num) hi

/-- A fully semantic coupling bound, with the common upper envelope proved by
an explicit threshold law. -/
theorem coupling_gap_bound (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I) (anchor : Finset I → I)
    (hanchor : ∀ s ∈ supports, anchor s ∈ s)
    (hmin : ∀ s ∈ supports, ∀ j ∈ s, x (anchor s) ≤ x j)
    (c : ℝ) (hc : 0 < c) (μ : Law (Vertex I)) (hm : HasMeans μ x)
    (hdef : ∀ s ∈ supports, c * hullGap (monomial s) x ≤
      x (anchor s) - μ.expect (fun v => monomial s (vertexPoint v))) :
    weightedTermwiseGap supports a x ≤
      (1 / c) * hullGap (supportPolynomial supports a) x :=
  coupling_gap_bound_of_maximum supports a ha x anchor c hc
    (positive_polynomial_maximum supports a ha x hx anchor hanchor hmin) μ hm hdef

omit [Fintype I] [DecidableEq I] in
/-- Monomial expectations stay in the unit interval, including the empty monomial. -/
theorem monomial_envelope_bounds [Finite I] (s : Finset I) (x : I → ℝ)
    {z : ℝ} (hz : z ∈ envelopeValues (monomial s) x) : 0 ≤ z ∧ z ≤ 1 := by
  classical
  let := Fintype.ofFinite I
  obtain ⟨μ, _, hv⟩ := (mem_cubeGraph_hull_iff _
    (monomial_coordinate_affine s) x z).mp hz
  rw [← hv]
  refine ⟨monomial_expect_nonneg s μ, ?_⟩
  rw [← μ.expect_const 1]
  apply μ.expect_mono
  intro v
  exact Finset.prod_le_one
    (fun i _ => by simp only [vertexPoint]; split <;> norm_num)
    (fun i _ => by simp only [vertexPoint]; split <;> norm_num)

/-- The width of a positive sum is at most the sum of its individual widths. -/
theorem hullGap_le_weightedTermwiseGap (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I) :
    hullGap (supportPolynomial supports a) x ≤ weightedTermwiseGap supports a x := by
  have hne : (envelopeValues (supportPolynomial supports a) x).Nonempty :=
    ⟨supportPolynomial supports a x, subset_convexHull ℝ _ ⟨hx, rfl⟩⟩
  have hbounds : ∀ z ∈ envelopeValues (supportPolynomial supports a) x,
      (∑ s ∈ supports, a s * sInf (envelopeValues (monomial s) x)) ≤ z ∧
      z ≤ (∑ s ∈ supports, a s * sSup (envelopeValues (monomial s) x)) := by
    intro z hz
    obtain ⟨μ, hm, hv⟩ := (mem_cubeGraph_hull_iff _
      (supportPolynomial_coordinate_affine supports a) x z).mp hz
    have hmemb (s : Finset I) : μ.expect (fun v => monomial s (vertexPoint v)) ∈
        envelopeValues (monomial s) x :=
      (mem_cubeGraph_hull_iff _ (monomial_coordinate_affine s) x _).mpr ⟨μ, hm, rfl⟩
    rw [← hv, polynomial_expect]
    constructor
    · apply Finset.sum_le_sum
      intro s hs
      apply mul_le_mul_of_nonneg_left _ (ha s hs)
      exact csInf_le ⟨0, fun z hz => (monomial_envelope_bounds s x hz).1⟩ (hmemb s)
    · apply Finset.sum_le_sum
      intro s hs
      apply mul_le_mul_of_nonneg_left _ (ha s hs)
      exact le_csSup ⟨1, fun z hz => (monomial_envelope_bounds s x hz).2⟩ (hmemb s)
  have hinf := le_csInf hne (fun z hz => (hbounds z hz).1)
  have hsup := csSup_le hne (fun z hz => (hbounds z hz).2)
  rw [weightedTermwiseGap]
  simp only [hullGap, mul_sub, Finset.sum_sub_distrib]
  linarith

/-- The common monomial upper value includes the constant empty monomial. -/
def monomialUpper (s : Finset I) (x : I → ℝ) : ℝ :=
  if h : s.Nonempty then s.inf' h x else 1

omit [Fintype I] [DecidableEq I] in
theorem monomialUpper_eq_anchor (s : Finset I) (x : I → ℝ)
    (i : I) (hi : i ∈ s) (hmin : ∀ j ∈ s, x i ≤ x j) :
    monomialUpper s x = x i := by
  rw [monomialUpper, dif_pos ⟨i, hi⟩]
  exact le_antisymm (Finset.inf'_le x hi) (Finset.le_inf' _ _ hmin)

omit [Fintype I] [DecidableEq I] in
@[simp] theorem monomialUpper_empty (x : I → ℝ) : monomialUpper ∅ x = 1 := by
  simp [monomialUpper]

omit [Fintype I] [DecidableEq I] in
theorem monomial_min_anchor (s : Finset I) (hs : s.Nonempty) (x : I → ℝ) :
    ∃ i ∈ s, ∀ j ∈ s, x i ≤ x j := by
  obtain ⟨i, hi, hv⟩ := Finset.exists_mem_eq_inf' hs x
  exact ⟨i, hi, fun j hj => hv ▸ Finset.inf'_le x hj⟩

theorem thresholdLaw_monomial_upper (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    (thresholdLaw x).expect (fun v => monomial s (vertexPoint v)) = monomialUpper s x := by
  by_cases hs : s.Nonempty
  · obtain ⟨i, hi, hmin⟩ := monomial_min_anchor s hs x
    rw [monomialUpper_eq_anchor s x i hi hmin]
    exact thresholdLaw_monomial s x hx i hi hmin
  · have : s = ∅ := Finset.not_nonempty_iff_eq_empty.mp hs
    subst s
    simp [monomial]

theorem monomial_expect_le_upper (s : Finset I) (x : I → ℝ)
    (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    μ.expect (fun v => monomial s (vertexPoint v)) ≤ monomialUpper s x := by
  by_cases hs : s.Nonempty
  · obtain ⟨i, hi, hmin⟩ := monomial_min_anchor s hs x
    rw [monomialUpper_eq_anchor s x i hi hmin]
    exact sub_nonneg.mp (monomial_deficiency_nonneg s x i hi μ hm)
  · have : s = ∅ := Finset.not_nonempty_iff_eq_empty.mp hs
    subst s
    simp [monomial]

omit [Fintype I] [DecidableEq I] in
theorem positive_polynomial_maximum_general [Finite I] (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I) :
    IsGreatest (envelopeValues (supportPolynomial supports a) x)
      (∑ s ∈ supports, a s * monomialUpper s x) := by
  classical
  let := Fintype.ofFinite I
  apply maximum_from_laws _ (supportPolynomial_coordinate_affine supports a)
  · intro μ hm
    rw [polynomial_expect]
    exact Finset.sum_le_sum fun s hs =>
      mul_le_mul_of_nonneg_left (monomial_expect_le_upper s x μ hm) (ha s hs)
  · refine ⟨thresholdLaw x, thresholdLaw_hasMeans x hx, ?_⟩
    rw [polynomial_expect]
    simp_rw [thresholdLaw_monomial_upper _ x hx]

@[simp] theorem monomial_gap_empty (x : I → ℝ) (hx : x ∈ cube I) :
    hullGap (monomial ∅) x = 0 := by
  have hval : ∀ z ∈ envelopeValues (monomial (∅ : Finset I)) x, z = 1 := by
    intro z hz
    obtain ⟨μ, _, hv⟩ := (mem_cubeGraph_hull_iff _
      (monomial_coordinate_affine ∅) x z).mp hz
    simpa [monomial] using hv.symm
  have hne : (envelopeValues (monomial (∅ : Finset I)) x).Nonempty :=
    ⟨monomial ∅ x, subset_convexHull ℝ _ ⟨hx, rfl⟩⟩
  have hset : envelopeValues (monomial (∅ : Finset I)) x = {1} := by
    apply Set.eq_singleton_iff_unique_mem.mpr
    obtain ⟨z, hz⟩ := hne
    exact ⟨hval z hz ▸ hz, hval⟩
  simp [hullGap, hset]

/-- Coupling bound for every positive squarefree polynomial, including constants. -/
theorem coupling_gap_bound_general (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I) (c : ℝ) (hc : 0 < c)
    (μ : Law (Vertex I)) (hm : HasMeans μ x)
    (hdef : ∀ s ∈ supports, c * hullGap (monomial s) x ≤
      monomialUpper s x - μ.expect (fun v => monomial s (vertexPoint v))) :
    weightedTermwiseGap supports a x ≤
      (1 / c) * hullGap (supportPolynomial supports a) x := by
  have hmax := positive_polynomial_maximum_general supports a ha x hx
  have hattain : μ.expect (fun v => supportPolynomial supports a (vertexPoint v)) ∈
      envelopeValues (supportPolynomial supports a) x :=
    (mem_cubeGraph_hull_iff _ (supportPolynomial_coordinate_affine supports a) x _).mpr
      ⟨μ, hm, rfl⟩
  have hinf := csInf_le (polynomial_envelope_bddBelow supports a ha x) hattain
  have hsum : c * weightedTermwiseGap supports a x ≤
      (∑ s ∈ supports, a s * monomialUpper s x) -
        μ.expect (fun v => supportPolynomial supports a (vertexPoint v)) := by
    rw [weightedTermwiseGap, polynomial_expect, Finset.mul_sum,
      ← Finset.sum_sub_distrib]
    apply Finset.sum_le_sum
    intro s hs
    have hh := mul_le_mul_of_nonneg_left (hdef s hs) (ha s hs)
    nlinarith
  have hbound : c * weightedTermwiseGap supports a x ≤
      hullGap (supportPolynomial supports a) x := by
    rw [hullGap, hmax.csSup_eq]
    linarith
  have := (le_div_iff₀ hc).mpr (by simpa [mul_comm] using hbound)
  simpa [div_eq_mul_inv, mul_comm] using this

omit [Fintype I] [DecidableEq I] in
theorem envelopeValues_monomial_scale [Finite I] (s : Finset I) (x : I → ℝ) (c : ℝ) :
    envelopeValues (fun y => c * monomial s y) x =
      (fun z => c * z) '' envelopeValues (monomial s) x := by
  classical
  let := Fintype.ofFinite I
  have hcf : SeparatelyAffine (fun y => c * monomial s y) := by
    intro y i t
    dsimp only
    rw [monomial_coordinate_affine]
    ring
  ext z
  constructor
  · intro hz
    obtain ⟨μ, hm, hv⟩ := (mem_cubeGraph_hull_iff _ hcf x z).mp hz
    rw [Law.expect_const_mul] at hv
    exact ⟨μ.expect (fun v => monomial s (vertexPoint v)),
      (mem_cubeGraph_hull_iff _ (monomial_coordinate_affine s) x _).mpr ⟨μ, hm, rfl⟩,
      hv⟩
  · rintro ⟨q, hq, rfl⟩
    obtain ⟨μ, hm, hv⟩ := (mem_cubeGraph_hull_iff _
      (monomial_coordinate_affine s) x q).mp hq
    exact (mem_cubeGraph_hull_iff _ hcf x _).mpr
      ⟨μ, hm, by rw [Law.expect_const_mul, hv]⟩

/-- Nonnegative coefficients scale actual envelope widths. -/
theorem hullGap_monomial_scale (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I)
    (c : ℝ) (hc : 0 ≤ c) :
    hullGap (fun y => c * monomial s y) x = c * hullGap (monomial s) x := by
  have hne : (envelopeValues (monomial s) x).Nonempty :=
    ⟨monomial s x, subset_convexHull ℝ _ ⟨hx, rfl⟩⟩
  rw [hullGap, envelopeValues_monomial_scale]
  rcases eq_or_lt_of_le hc with hzero | hpos
  · subst c
    simp [hne.image_const]
  · have hsup := (OrderIso.mulLeft₀ c hpos).map_csSup' hne
      ⟨1, fun z hz => (monomial_envelope_bounds s x hz).2⟩
    have hinf := (OrderIso.mulLeft₀ c hpos).map_csInf' hne
      ⟨0, fun z hz => (monomial_envelope_bounds s x hz).1⟩
    change c * sSup (envelopeValues (monomial s) x) =
      sSup ((fun z => c * z) '' envelopeValues (monomial s) x) at hsup
    change c * sInf (envelopeValues (monomial s) x) =
      sInf ((fun z => c * z) '' envelopeValues (monomial s) x) at hinf
    rw [← hsup, ← hinf, hullGap, mul_sub]

/-- The weighted definition equals the sum of the actual scaled-term gaps. -/
theorem weightedTermwiseGap_eq_term_gaps (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I) :
    weightedTermwiseGap supports a x =
      ∑ s ∈ supports, hullGap (fun y => a s * monomial s y) x := by
  unfold weightedTermwiseGap
  exact Finset.sum_congr rfl fun s hs => (hullGap_monomial_scale s x hx (a s) (ha s hs)).symm

end
end MultilinearGap
