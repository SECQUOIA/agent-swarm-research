import Formal.MultilinearGap.OriginalBoxTransfer
import Formal.MultilinearGap.PhysicalEnvelope

/-! # PB26: the expansion is a proof device, and exactly how far that goes

This file discharges PB26 of the positive-box package
(`formal/topics/18-positive-box/CLAIMS.md`): the interpretation of the
unequal-box transfer of PB23/PB24.  Nothing here argues by box inclusion; the
original box is never compared with a larger common-aspect box.  The only
geometry used is the affine bijection `originalBoxPoint` of PB23, which carries
`[1, rho]^n` **onto** the original box, and the vertex-law semantics of the
envelopes.

**Part 1: the pulled-back laws are the same endpoint laws.**  The transfer map
carries the vertex of `[1, rho]^n` indexed by a binary point `v` to the vertex of
`∏ [l i, u i]` indexed by the *same* `v` (`originalBoxPoint_vertex`), so the two
boxes share one vertex index set (`originalBoxPoint_image_vertices`).  A law `μ`
on that index set therefore has the same expectation for a function of the
original box and for its pull-back (`pullbackLaw_expect`), and its ambient means
`p` transfer to the original-box means `originalBoxPoint rho l u (boxPoint 1 rho p)`
(`pullbackLaw_means`).  Sampling the certificate needs no expanded polynomial.

**Part 2: simultaneity.**  On `[1, rho]^n` the monomials are the physical
monomials of `PhysicalEnvelope` (`monomial_commonAspect`), and the single
common-threshold law `thresholdLaw p` maximizes all of them at once
(`thresholdLaw_maximizes_commonAspect_monomial`), independently of the support.

**Part 3: the key equality, and the exact half that fails.**  The general
principle is `envelope_sSup_sum_of_common_max`: if one law attains the concave
envelope of every summand, the concave envelope of the sum is the sum of the
concave envelopes.  Applied with the common-threshold law, this gives the
concave-side equality for one original monomial and its expansion
(`originalMonomial_concaveEnvelope_eq_sum`) -- an equality, where PB24 only
proves the inequality `boxHullGap_monomial_le_expansion`.  Hence the source's
statement: for **every** rounding law, the original monomial's deficiency equals
the sum of its expanded monomials' deficiencies
(`originalMonomial_deficiency_eq_sum`).

The convex side has the dual principle (`envelope_sInf_sum_of_common_min`) but
**no common attaining law**, and the equality genuinely fails there.  The convex
envelope of an ambient monomial is attained by an adjacent-count law that depends
on the support (`boxEnvelope_sInf_commonAspect_monomial`), and at the means
`(1/2, 1/2, 1/2)` no single law attains the convex envelope of all three pairwise
physical monomials at once (`no_common_minimizing_law`).  For the monomial
`z 0 * z 1 * z 2` on `[1, 3/2]^3` transferred from `[1, 2]^3`, evaluated at the
centre, the expanded convex envelopes sum to `29/16` while the original monomial's
convex envelope is `15/8` (`convexEnvelope_expansion_values`,
`convexEnvelope_expansion_lt`); the concave envelopes agree at `35/16`, so the
gaps are `5/16` against `3/8` (`boxHullGap_originalMonomial_expansion_values`,
`boxHullGap_originalMonomial_lt_sum_expansion`).  The interpretation paragraph is
therefore correct exactly as the source states it -- an equality of
*deficiencies under a rounding law* -- and would be **false** if read as an
equality of hull gaps.

**Part 4: the per-monomial guarantee in the original coordinates.**  Because the
deficiencies are equal and the expanded gaps dominate the original gap, a
per-physical-monomial capture guarantee on `[1, rho]^n` transfers verbatim to
each original monomial on the original box
(`originalMonomial_capture_of_physMonomial_capture`,
`originalBox_monomial_capture`).  Neither statement mentions the expansion: the
conclusion is a bound on `boxHullGap l u (monomial s)` in terms of the deficiency
of the *same* law on the original box.
-/

namespace MultilinearGap

open CubicGap

noncomputable section

/-! ## The common-attaining-law principle

The general fact behind PB26: envelopes of a sum are in general strictly inside
the sum of the envelopes, but a law attaining every summand's optimum at once
closes the gap. -/

section CommonLaw

variable {I J : Type*} [Fintype I] [DecidableEq I]

private theorem expect_finsetSum (μ : Law (Vertex I)) (S : Finset J)
    (g : J → Vertex I → ℝ) :
    μ.expect (fun v => ∑ j ∈ S, g j v) = ∑ j ∈ S, μ.expect (g j) := by
  simp only [Law.expect, Finset.mul_sum]
  rw [Finset.sum_comm]

/-- The concave envelope of a sum equals the sum of the concave envelopes as soon
as **one** law with the prescribed means maximizes every summand. -/
theorem envelope_sSup_sum_of_common_max (S : Finset J) (g : J → (I → ℝ) → ℝ)
    (hg : ∀ j ∈ S, SeparatelyAffine (g j)) {p : I → ℝ} {ν : Law (Vertex I)}
    (hν : HasMeans ν p)
    (hmax : ∀ j ∈ S, ∀ μ : Law (Vertex I), HasMeans μ p →
      μ.expect (fun v => g j (vertexPoint v)) ≤ ν.expect (fun v => g j (vertexPoint v))) :
    sSup (envelopeValues (fun y => ∑ j ∈ S, g j y) p) =
      ∑ j ∈ S, sSup (envelopeValues (g j) p) := by
  have hterm : ∀ j ∈ S,
      sSup (envelopeValues (g j) p) = ν.expect (fun v => g j (vertexPoint v)) :=
    fun j hj => (maximum_from_laws (g j) (hg j hj) p _ (fun μ hm => hmax j hj μ hm)
      ⟨ν, hν, rfl⟩).csSup_eq
  have hsum : IsGreatest (envelopeValues (fun y => ∑ j ∈ S, g j y) p)
      (ν.expect fun v => ∑ j ∈ S, g j (vertexPoint v)) := by
    refine maximum_from_laws _ (separatelyAffine_sum S g hg) p _ ?_ ⟨ν, hν, rfl⟩
    intro μ hm
    rw [expect_finsetSum, expect_finsetSum]
    exact Finset.sum_le_sum fun j hj => hmax j hj μ hm
  rw [hsum.csSup_eq, expect_finsetSum]
  exact Finset.sum_congr rfl fun j hj => (hterm j hj).symm

/-- The dual principle: the convex envelope of a sum equals the sum of the convex
envelopes as soon as one law with the prescribed means minimizes every summand.
This is the hypothesis that fails on the convex side of the positive-box
expansion; see `no_common_minimizing_law`. -/
theorem envelope_sInf_sum_of_common_min (S : Finset J) (g : J → (I → ℝ) → ℝ)
    (hg : ∀ j ∈ S, SeparatelyAffine (g j)) {p : I → ℝ} {ν : Law (Vertex I)}
    (hν : HasMeans ν p)
    (hmin : ∀ j ∈ S, ∀ μ : Law (Vertex I), HasMeans μ p →
      ν.expect (fun v => g j (vertexPoint v)) ≤ μ.expect (fun v => g j (vertexPoint v))) :
    sInf (envelopeValues (fun y => ∑ j ∈ S, g j y) p) =
      ∑ j ∈ S, sInf (envelopeValues (g j) p) := by
  have hterm : ∀ j ∈ S,
      sInf (envelopeValues (g j) p) = ν.expect (fun v => g j (vertexPoint v)) :=
    fun j hj => (minimum_from_laws (g j) (hg j hj) p _ (fun μ hm => hmin j hj μ hm)
      ⟨ν, hν, rfl⟩).csInf_eq
  have hsum : IsLeast (envelopeValues (fun y => ∑ j ∈ S, g j y) p)
      (ν.expect fun v => ∑ j ∈ S, g j (vertexPoint v)) := by
    refine minimum_from_laws _ (separatelyAffine_sum S g hg) p _ ?_ ⟨ν, hν, rfl⟩
    intro μ hm
    rw [expect_finsetSum, expect_finsetSum]
    exact Finset.sum_le_sum fun j hj => hmin j hj μ hm
  rw [hsum.csInf_eq, expect_finsetSum]
  exact Finset.sum_congr rfl fun j hj => (hterm j hj).symm

end CommonLaw

/-! ## Part 1: the pulled-back laws are the same endpoint laws -/

section Pullback

variable {I : Type*} [Fintype I] [DecidableEq I]

omit [Fintype I] [DecidableEq I] in
/-- PB26(1): the transfer map sends the vertex of `[1, rho]^n` indexed by `v` to
the vertex of the original box indexed by the **same** `v`. -/
theorem originalBoxPoint_vertex {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (v : Vertex I) :
    originalBoxPoint rho l u
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (vertexPoint v)) =
      boxPoint l u (vertexPoint v) :=
  originalBoxPoint_commonAspect hrho hl (vertexPoint v)

omit [Fintype I] [DecidableEq I] in
/-- PB26(1): the two boxes share one vertex set; the transfer map carries the
vertices of `[1, rho]^n` onto the vertices of the original box. -/
theorem originalBoxPoint_image_vertices {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) :
    originalBoxPoint rho l u ''
        (Set.range fun v : Vertex I =>
          boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (vertexPoint v)) =
      Set.range fun v : Vertex I => boxPoint l u (vertexPoint v) := by
  ext z
  constructor
  · rintro ⟨_, ⟨v, rfl⟩, rfl⟩
    exact ⟨v, (originalBoxPoint_vertex (u := u) hrho hl v).symm⟩
  · rintro ⟨v, rfl⟩
    exact ⟨_, ⟨v, rfl⟩, originalBoxPoint_vertex (u := u) hrho hl v⟩

/-- PB26(1): a law on the shared vertex set has the same expectation for a
function on the original box and for its pull-back to `[1, rho]^n`.  Sampling the
rounding law therefore needs no expanded polynomial. -/
theorem pullbackLaw_expect {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (f : (I → ℝ) → ℝ) (μ : Law (Vertex I)) :
    μ.expect (fun v => f (originalBoxPoint rho l u
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (vertexPoint v)))) =
      μ.expect fun v => f (boxPoint l u (vertexPoint v)) :=
  congrArg μ.expect (funext fun v => congrArg f (originalBoxPoint_vertex (u := u) hrho hl v))

/-- PB26(1): a law with ambient means `p` pushes forward to the original-box
means `originalBoxPoint rho l u (boxPoint 1 rho p)`, the transfer image of the
ambient point. -/
theorem pullbackLaw_means {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) {p : I → ℝ} (μ : Law (Vertex I)) (hm : HasMeans μ p) (i : I) :
    μ.expect (fun v => boxPoint l u (vertexPoint v) i) =
      originalBoxPoint rho l u (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p) i := by
  have hbox : ∀ v : Vertex I,
      boxPoint l u (vertexPoint v) i = l i + (u i - l i) * vertexPoint v i := fun _ => rfl
  rw [originalBoxPoint_commonAspect hrho hl p]
  simp only [hbox, Law.expect_add, Law.expect_const, Law.expect_const_mul, hm i]
  rfl

end Pullback

/-! ## Part 2: common-threshold rounding attains every ambient monomial at once -/

section Simultaneity

variable {I : Type*} [Fintype I] [DecidableEq I]

omit [Fintype I] [DecidableEq I] in
/-- A monomial of the common-aspect box `[1, rho]^n`, read in cube coordinates,
is the physical monomial of `PhysicalEnvelope` with shift `rho - 1`. -/
theorem monomial_commonAspect (rho : ℝ) (t : Finset I) (q : I → ℝ) :
    monomial t (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) q) = physMonomial (rho - 1) t q :=
  rfl

/-- PB26(2): one common-threshold law simultaneously maximizes **every** monomial
of `[1, rho]^n`, whatever its support. -/
theorem thresholdLaw_maximizes_commonAspect_monomial {rho : ℝ} (hrho : 1 ≤ rho)
    {p : I → ℝ} (hp : p ∈ cube I) (t : Finset I) (μ : Law (Vertex I)) (hm : HasMeans μ p) :
    μ.expect (fun v => monomial t
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (vertexPoint v))) ≤
      (thresholdLaw p).expect fun v => monomial t
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (vertexPoint v)) := by
  simp only [monomial_commonAspect]
  exact thresholdLaw_maximizes_physMonomial p hp (rho - 1) (by linarith) t μ hm

/-- PB26(2): the concave envelope of an ambient monomial is attained by the
common-threshold law, and its value is the physical concave envelope
`physUpper`. -/
theorem thresholdLaw_attains_commonAspect_monomial {rho : ℝ} (hrho : 1 ≤ rho)
    {p : I → ℝ} (hp : p ∈ cube I) (t : Finset I) :
    IsGreatest (boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => rho) (monomial t)
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p))
      ((thresholdLaw p).expect fun v => monomial t
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (vertexPoint v))) := by
  rw [boxEnvelopeValues_eq_of_mem _ _ (fun _ => hrho) _ p hp]
  simp only [monomial_commonAspect]
  rw [thresholdLaw_physMonomial (rho - 1) t p hp]
  exact physMonomial_maximum (rho - 1) (by linarith) t p hp

/-- The value of that common maximum: the physical concave envelope. -/
theorem thresholdLaw_commonAspect_monomial {rho : ℝ} {p : I → ℝ} (hp : p ∈ cube I)
    (t : Finset I) :
    (thresholdLaw p).expect (fun v => monomial t
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (vertexPoint v))) =
      physUpper (rho - 1) t p := by
  simp only [monomial_commonAspect]
  exact thresholdLaw_physMonomial (rho - 1) t p hp

omit [Fintype I] [DecidableEq I] in
/-- The value of that common maximum, as a supremum. -/
theorem boxEnvelope_sSup_commonAspect_monomial [Finite I] {rho : ℝ} (hrho : 1 ≤ rho)
    {p : I → ℝ} (hp : p ∈ cube I) (t : Finset I) :
    sSup (boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => rho) (monomial t)
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p)) = physUpper (rho - 1) t p := by
  classical
  let _ := Fintype.ofFinite I
  rw [(thresholdLaw_attains_commonAspect_monomial hrho hp t).csSup_eq,
    thresholdLaw_commonAspect_monomial hp t]

omit [Fintype I] [DecidableEq I] in
/-- For contrast, the convex envelope of an ambient monomial is the physical
convex envelope `physLower` of PB11, attained by an adjacent-count law whose
count is concentrated on the two integers adjacent to the mean sum **of that
support**.  Unlike the concave side, this attaining law depends on the support;
see `no_common_minimizing_law`. -/
theorem boxEnvelope_sInf_commonAspect_monomial [Finite I] {rho : ℝ} (hrho : 1 ≤ rho)
    {p : I → ℝ} (hp : p ∈ cube I) (t : Finset I) :
    sInf (boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => rho) (monomial t)
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p)) = physLower (rho - 1) t p := by
  classical
  let _ := Fintype.ofFinite I
  rw [boxEnvelopeValues_eq_of_mem _ _ (fun _ => hrho) _ p hp]
  simp only [monomial_commonAspect]
  exact (physMonomial_minimum (rho - 1) (by linarith) t p hp).csInf_eq

end Simultaneity

/-! ## Part 3: the key equality, on the concave side

The concave envelope of the original monomial is *exactly* the positive
combination of the concave envelopes of its expanded monomials, because the one
common-threshold law of Part 2 attains every summand's maximum at once. -/

section ConcaveEquality

variable {I : Type*} [Fintype I] [DecidableEq I]

omit [Fintype I] in
/-- The PB23 expansion read in cube coordinates: an original monomial is the
nonnegative combination of the physical monomials of the subsets of its
support. -/
theorem monomial_originalBox_expand_cube {rho : ℝ} (hrho : 1 < rho) {l u : I → ℝ}
    (hl : ∀ i, 0 < l i) (s : Finset I) (q : I → ℝ) :
    monomial s (boxPoint l u q) =
      ∑ t ∈ s.powerset, originalExpansionCoefficient rho l u s t *
        physMonomial (rho - 1) t q := by
  rw [← originalBoxPoint_commonAspect hrho hl q, monomial_originalBox_expansion]
  rfl

omit [Fintype I] in
/-- PB26(3), concave side: the concave envelope of an original monomial on the
original box **equals** the positive combination of the concave envelopes of its
expanded monomials on `[1, rho]^n`.  This is an equality, not the inequality of
`boxHullGap_monomial_le_expansion`; the reason is the simultaneity of Part 2. -/
theorem originalMonomial_concaveEnvelope_eq_sum [Finite I] {rho : ℝ} (hrho : 1 < rho)
    {l u : I → ℝ} (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) (hasp : ∀ i, u i ≤ rho * l i)
    {p : I → ℝ} (hp : p ∈ cube I) (s : Finset I) :
    sSup (boxEnvelopeValues l u (monomial s) (boxPoint l u p)) =
      ∑ t ∈ s.powerset, originalExpansionCoefficient rho l u s t *
        sSup (boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => rho) (monomial t)
          (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p)) := by
  let _ := Fintype.ofFinite I
  have hτ0 : (0 : ℝ) ≤ rho - 1 := by linarith
  have hcnn : ∀ t : Finset I, 0 ≤ originalExpansionCoefficient rho l u s t := fun t =>
    originalExpansionCoefficient_nonneg hrho hl hlu hasp s t
  set g : Finset I → (I → ℝ) → ℝ :=
    fun t q => originalExpansionCoefficient rho l u s t * physMonomial (rho - 1) t q with hgdef
  have hga : ∀ t ∈ s.powerset, SeparatelyAffine (g t) := by
    intro t _ y i r
    simp only [hgdef]
    rw [physMonomial_coordinate_affine (rho - 1) t y i r]
    ring
  have hmax : ∀ t ∈ s.powerset, ∀ μ : Law (Vertex I), HasMeans μ p →
      μ.expect (fun v => g t (vertexPoint v)) ≤
        (thresholdLaw p).expect (fun v => g t (vertexPoint v)) := by
    intro t _ μ hm
    simp only [hgdef, Law.expect_const_mul]
    exact mul_le_mul_of_nonneg_left
      (thresholdLaw_maximizes_physMonomial p hp (rho - 1) hτ0 t μ hm) (hcnn t)
  have hfun : (fun q => monomial s (boxPoint l u q)) = fun q => ∑ t ∈ s.powerset, g t q :=
    funext fun q => monomial_originalBox_expand_cube hrho hl s q
  have hterm : ∀ t ∈ s.powerset, sSup (envelopeValues (g t) p) =
      originalExpansionCoefficient rho l u s t *
        sSup (boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => rho) (monomial t)
          (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p)) := by
    intro t ht
    rw [boxEnvelope_sSup_commonAspect_monomial hrho.le hp t]
    refine IsGreatest.csSup_eq ?_
    refine maximum_from_laws _ (hga t ht) p _ ?_
      ⟨thresholdLaw p, thresholdLaw_hasMeans p hp, ?_⟩
    · intro μ hm
      simp only [hgdef, Law.expect_const_mul]
      exact mul_le_mul_of_nonneg_left
        (physMonomial_expect_le (rho - 1) hτ0 t p μ hm) (hcnn t)
    · simp only [hgdef, Law.expect_const_mul, thresholdLaw_physMonomial (rho - 1) t p hp]
  rw [boxEnvelopeValues_eq_of_mem l u hlu (monomial s) p hp, hfun,
    envelope_sSup_sum_of_common_max s.powerset g hga (thresholdLaw_hasMeans p hp) hmax]
  exact Finset.sum_congr rfl hterm

/-- PB26(3), as the source states it: for **every** rounding law with the
prescribed means -- the same law on both boxes, by Part 1 -- the deficiency of an
original monomial equals the positive combination of the deficiencies of its
expanded monomials.  No hull gaps appear: see `convexEnvelope_expansion_lt` for
why the hull-gap form of this equality is false.

No hypothesis is needed on `μ`: linearity of expectation and the concave-side
equality do all the work.  In the intended reading `μ` is a rounding law with the
prescribed means `p`, and then both sides are genuine deficiencies. -/
theorem originalMonomial_deficiency_eq_sum {rho : ℝ} (hrho : 1 < rho)
    {l u : I → ℝ} (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) (hasp : ∀ i, u i ≤ rho * l i)
    {p : I → ℝ} (hp : p ∈ cube I) (μ : Law (Vertex I)) (s : Finset I) :
    sSup (boxEnvelopeValues l u (monomial s) (boxPoint l u p)) -
        μ.expect (fun v => monomial s (boxPoint l u (vertexPoint v))) =
      ∑ t ∈ s.powerset, originalExpansionCoefficient rho l u s t *
        (sSup (boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => rho) (monomial t)
            (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p)) -
          μ.expect (fun v => monomial t
            (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (vertexPoint v)))) := by
  have hexp : μ.expect (fun v => monomial s (boxPoint l u (vertexPoint v))) =
      ∑ t ∈ s.powerset, originalExpansionCoefficient rho l u s t *
        μ.expect (fun v => monomial t
          (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (vertexPoint v))) := by
    have h1 : (fun v : Vertex I => monomial s (boxPoint l u (vertexPoint v))) =
        fun v => ∑ t ∈ s.powerset, originalExpansionCoefficient rho l u s t *
          physMonomial (rho - 1) t (vertexPoint v) :=
      funext fun v => monomial_originalBox_expand_cube hrho hl s (vertexPoint v)
    rw [h1, expect_finsetSum]
    exact Finset.sum_congr rfl fun t _ => by
      simp only [monomial_commonAspect, Law.expect_const_mul]
  rw [hexp, originalMonomial_concaveEnvelope_eq_sum hrho hl hlu hasp hp s,
    ← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl fun t _ => (mul_sub _ _ _).symm

end ConcaveEquality

/-! ## Part 3, convex side: the equality genuinely fails

The dual principle `envelope_sInf_sum_of_common_min` needs a law that minimizes
every summand at once.  On the convex side no such law exists: the convex
envelope of a physical monomial is attained by an *adjacent-count* law, whose
count is concentrated on the two integers adjacent to the mean sum **of its own
support**, and different supports ask for incompatible laws.  The first theorem
below shows the obstruction at the three pairwise monomials in dimension three,
and the second turns it into a numerical counterexample: the concave-side
equality of `originalMonomial_concaveEnvelope_eq_sum` has no convex-side
analogue, so the hull-gap inequality `boxHullGap_monomial_le_expansion` of PB24
is strict. -/

section ConvexFailure

/-- PB26(3), the obstruction: at the means `(1/2, 1/2, 1/2)` no law attains the
convex envelope `physLower` of all three pairwise physical monomials at once.
Attaining it for the pair `{i, j}` forces the second moment `E[y i * y j]` to
vanish, and three vanishing pairwise moments are incompatible with three means
one half, since `(K - 1) (K - 2) ≥ 0` for the integer success count `K`. -/
theorem no_common_minimizing_law :
    ¬ ∃ μ : Law (Vertex (Fin 3)), HasMeans μ (fun _ => (1 : ℝ) / 2) ∧
      ∀ i j : Fin 3, i ≠ j →
        μ.expect (fun v => physMonomial 1 ({i, j} : Finset (Fin 3)) (vertexPoint v)) =
          physLower 1 ({i, j} : Finset (Fin 3)) (fun _ => (1 : ℝ) / 2) := by
  rintro ⟨μ, hm, hattain⟩
  have hpair : ∀ i j : Fin 3, i ≠ j →
      μ.expect (fun v => vertexPoint v i * vertexPoint v j) = 0 := by
    intro i j hij
    have hval : physLower 1 ({i, j} : Finset (Fin 3)) (fun _ => (1 : ℝ) / 2) = 2 := by
      simp [physLower, countFloor, countFrac, meanSum, Finset.sum_pair hij]
      norm_num
    have hfun :
        (fun v : Vertex (Fin 3) => physMonomial 1 ({i, j} : Finset (Fin 3)) (vertexPoint v)) =
          fun v => 1 + (vertexPoint v i + (vertexPoint v j +
            vertexPoint v i * vertexPoint v j)) := by
      funext v
      rw [physMonomial, Finset.prod_pair hij]
      ring
    have h1 := hattain i j hij
    rw [hval, hfun] at h1
    simp only [Law.expect_add, Law.expect_const, hm i, hm j] at h1
    norm_num at h1
    linarith
  have hnn : (0 : ℝ) ≤ μ.expect (fun v =>
      2 * (vertexPoint v 0 * vertexPoint v 1) + (2 * (vertexPoint v 0 * vertexPoint v 2) +
        (2 * (vertexPoint v 1 * vertexPoint v 2) + ((-2) * vertexPoint v 0 +
          ((-2) * vertexPoint v 1 + ((-2) * vertexPoint v 2 + 2)))))) := by
    refine μ.expect_nonneg fun v => ?_
    cases h0 : v 0 <;> cases h1 : v 1 <;> cases h2 : v 2 <;>
      simp [vertexPoint, h0, h1, h2]
  simp only [Law.expect_add, Law.expect_const_mul, Law.expect_const,
    hpair 0 1 (by decide), hpair 0 2 (by decide), hpair 1 2 (by decide),
    hm 0, hm 1, hm 2] at hnn
  norm_num at hnn

/-- The centre of the cube in dimension three. -/
private theorem half_mem_cube : (fun _ => (1 : ℝ) / 2) ∈ cube (Fin 3) :=
  fun _ => ⟨by norm_num, by norm_num⟩

/-- The two convex-envelope values of the counterexample: the original monomial
`z 0 * z 1 * z 2` on `[1, 3/2]^3` at the centre has convex envelope `15/8`, while
the positive combination of the convex envelopes of its eight expanded monomials
on `[1, 2]^3` is only `29/16`. -/
theorem convexEnvelope_expansion_values :
    ∑ t ∈ (Finset.univ : Finset (Fin 3)).powerset,
        originalExpansionCoefficient 2 (fun _ => (1 : ℝ)) (fun _ => 3 / 2) Finset.univ t *
          sInf (boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (monomial t)
            (boxPoint (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (fun _ => 1 / 2))) = 29 / 16 ∧
      sInf (boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => (3 : ℝ) / 2)
          (monomial (Finset.univ : Finset (Fin 3)))
          (boxPoint (fun _ => (1 : ℝ)) (fun _ => (3 : ℝ) / 2) (fun _ => 1 / 2))) = 15 / 8 := by
  have hsum : ∀ t : Finset (Fin 3),
      sInf (boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (monomial t)
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (fun _ => 1 / 2))) =
          physLower 1 t (fun _ => (1 : ℝ) / 2) := by
    intro t
    rw [boxEnvelope_sInf_commonAspect_monomial (by norm_num) half_mem_cube t]
    norm_num
  constructor
  · simp only [hsum]
    rw [show ((Finset.univ : Finset (Fin 3)).powerset) =
      {∅, {0}, {1}, {2}, {0, 1}, {0, 2}, {1, 2}, {0, 1, 2}} from by decide]
    rw [Finset.sum_insert (by decide), Finset.sum_insert (by decide),
      Finset.sum_insert (by decide), Finset.sum_insert (by decide),
      Finset.sum_insert (by decide), Finset.sum_insert (by decide),
      Finset.sum_insert (by decide), Finset.sum_singleton]
    simp [originalExpansionCoefficient, originalBoxShare, physLower, countFloor, countFrac,
      meanSum,
      show ((Finset.univ \ ({0} : Finset (Fin 3))).card) = 2 from by decide,
      show ((Finset.univ \ ({1} : Finset (Fin 3))).card) = 2 from by decide,
      show ((Finset.univ \ ({2} : Finset (Fin 3))).card) = 2 from by decide,
      show ((Finset.univ \ ({0, 1} : Finset (Fin 3))).card) = 1 from by decide,
      show ((Finset.univ \ ({0, 2} : Finset (Fin 3))).card) = 1 from by decide,
      show ((Finset.univ \ ({1, 2} : Finset (Fin 3))).card) = 1 from by decide,
      show ((Finset.univ \ ({0, 1, 2} : Finset (Fin 3))).card) = 0 from by decide]
    norm_num
  · rw [boxEnvelope_sInf_commonAspect_monomial (by norm_num) half_mem_cube Finset.univ]
    norm_num [physLower, countFloor, countFrac, meanSum]

/-- PB26(3), convex side: **the equality fails**.  The positive combination of
the convex envelopes of the expanded monomials is *strictly below* the convex
envelope of the original monomial, so the concave-side equality has no dual. -/
theorem convexEnvelope_expansion_lt :
    ∑ t ∈ (Finset.univ : Finset (Fin 3)).powerset,
        originalExpansionCoefficient 2 (fun _ => (1 : ℝ)) (fun _ => 3 / 2) Finset.univ t *
          sInf (boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (monomial t)
            (boxPoint (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (fun _ => 1 / 2)))
      < sInf (boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => (3 : ℝ) / 2)
          (monomial (Finset.univ : Finset (Fin 3)))
          (boxPoint (fun _ => (1 : ℝ)) (fun _ => (3 : ℝ) / 2) (fun _ => 1 / 2))) := by
  obtain ⟨h1, h2⟩ := convexEnvelope_expansion_values
  rw [h1, h2]
  norm_num

/-- The concave envelope of the counterexample monomial at the same point:
`35/16`, attained by common-threshold rounding. -/
theorem concaveEnvelope_expansion_value :
    sSup (boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => (3 : ℝ) / 2)
        (monomial (Finset.univ : Finset (Fin 3)))
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => (3 : ℝ) / 2) (fun _ => 1 / 2))) = 35 / 16 := by
  rw [boxEnvelope_sSup_commonAspect_monomial (by norm_num) half_mem_cube Finset.univ,
    show ((3 : ℝ) / 2 - 1) = 1 / 2 from by norm_num, physUpper,
    show ((Finset.univ : Finset (Fin 3)).powerset) =
      {∅, {0}, {1}, {2}, {0, 1}, {0, 2}, {1, 2}, {0, 1, 2}} from by decide]
  rw [Finset.sum_insert (by decide), Finset.sum_insert (by decide),
    Finset.sum_insert (by decide), Finset.sum_insert (by decide),
    Finset.sum_insert (by decide), Finset.sum_insert (by decide),
    Finset.sum_insert (by decide), Finset.sum_singleton]
  simp [monomialUpper, Finset.inf'_const]
  norm_num

private theorem hullGap_expansion_split :
    ∑ t ∈ (Finset.univ : Finset (Fin 3)).powerset,
        originalExpansionCoefficient 2 (fun _ => (1 : ℝ)) (fun _ => 3 / 2) Finset.univ t *
          boxHullGap (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (monomial t)
            (boxPoint (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (fun _ => 1 / 2)) =
      (∑ t ∈ (Finset.univ : Finset (Fin 3)).powerset,
          originalExpansionCoefficient 2 (fun _ => (1 : ℝ)) (fun _ => 3 / 2) Finset.univ t *
            sSup (boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (monomial t)
              (boxPoint (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (fun _ => 1 / 2)))) -
        ∑ t ∈ (Finset.univ : Finset (Fin 3)).powerset,
          originalExpansionCoefficient 2 (fun _ => (1 : ℝ)) (fun _ => 3 / 2) Finset.univ t *
            sInf (boxEnvelopeValues (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (monomial t)
              (boxPoint (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (fun _ => 1 / 2))) := by
  rw [← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl fun t _ => by rw [boxHullGap, mul_sub]

/-- PB26(3), the consequence in exact numbers: the gap of the original monomial
`z 0 * z 1 * z 2` on `[1, 3/2]^3` at the centre is `5/16`, while the positive
combination of the gaps of its eight expanded monomials on `[1, 2]^3` is `3/8`.
The concave envelopes agree (`35/16` on both sides, by
`originalMonomial_concaveEnvelope_eq_sum`); the whole discrepancy is the convex
side. -/
theorem boxHullGap_originalMonomial_expansion_values :
    boxHullGap (fun _ => (1 : ℝ)) (fun _ => (3 : ℝ) / 2)
        (monomial (Finset.univ : Finset (Fin 3)))
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => (3 : ℝ) / 2) (fun _ => 1 / 2)) = 5 / 16 ∧
      ∑ t ∈ (Finset.univ : Finset (Fin 3)).powerset,
          originalExpansionCoefficient 2 (fun _ => (1 : ℝ)) (fun _ => 3 / 2) Finset.univ t *
            boxHullGap (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (monomial t)
              (boxPoint (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (fun _ => 1 / 2)) = 3 / 8 := by
  obtain ⟨hconvex, horiginal⟩ := convexEnvelope_expansion_values
  have hsup := originalMonomial_concaveEnvelope_eq_sum (rho := 2) (l := fun _ => (1 : ℝ))
    (u := fun _ => (3 : ℝ) / 2) (by norm_num) (fun _ => by norm_num) (fun _ => by norm_num)
    (fun _ => by norm_num) half_mem_cube Finset.univ
  refine ⟨?_, ?_⟩
  · rw [boxHullGap, concaveEnvelope_expansion_value, horiginal]
    norm_num
  · rw [hullGap_expansion_split, ← hsup, concaveEnvelope_expansion_value, hconvex]
    norm_num

/-- PB26(3), the consequence: the hull-gap inequality of PB24
(`boxHullGap_monomial_le_expansion`) is **strict** at this point, `5/16 < 3/8`.
Reading the interpretation paragraph as an equality of hull gaps would therefore
be false; the correct reading is the equality of deficiencies
`originalMonomial_deficiency_eq_sum`. -/
theorem boxHullGap_originalMonomial_lt_sum_expansion :
    boxHullGap (fun _ => (1 : ℝ)) (fun _ => (3 : ℝ) / 2)
        (monomial (Finset.univ : Finset (Fin 3)))
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => (3 : ℝ) / 2) (fun _ => 1 / 2))
      < ∑ t ∈ (Finset.univ : Finset (Fin 3)).powerset,
          originalExpansionCoefficient 2 (fun _ => (1 : ℝ)) (fun _ => 3 / 2) Finset.univ t *
            boxHullGap (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (monomial t)
              (boxPoint (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (fun _ => 1 / 2)) := by
  obtain ⟨h1, h2⟩ := boxHullGap_originalMonomial_expansion_values
  rw [h1, h2]
  norm_num

end ConvexFailure

/-! ## Part 4: the per-monomial guarantee in the original coordinates

The concave-side equality of Part 3 is exactly what is needed to carry a
per-physical-monomial capture guarantee on `[1, rho]^n` to each monomial of the
original polynomial on the original box.  The conclusions below mention no
expansion: the bound is on the hull gap of one original monomial, in terms of the
deficiency of the *same* rounding law read on the original box (Part 1). -/

section Capture

variable {I : Type*} [Fintype I] [DecidableEq I]

/-- PB26(4): if a law captures at least `1 / U` of the gap of **every** physical
monomial on `[1, rho]^n` -- the guarantee PB20/PB21 provide for the `rho/(rho+2)`
mixture with `U = rho + 2` -- then the same law captures at least `1 / U` of the
gap of every **original** monomial on the original box.  No expanded polynomial
is formed. -/
theorem originalMonomial_capture_of_physMonomial_capture {rho U : ℝ} (hrho : 1 < rho)
    {l u : I → ℝ} (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) (hasp : ∀ i, u i ≤ rho * l i)
    {p : I → ℝ} (hp : p ∈ cube I) (μ : Law (Vertex I))
    (hcap : ∀ t : Finset I, hullGap (physMonomial (rho - 1) t) p ≤
      U * (physUpper (rho - 1) t p -
        μ.expect fun v => physMonomial (rho - 1) t (vertexPoint v)))
    (s : Finset I) :
    boxHullGap l u (monomial s) (boxPoint l u p) ≤
      U * (sSup (boxEnvelopeValues l u (monomial s) (boxPoint l u p)) -
        μ.expect fun v => monomial s (boxPoint l u (vertexPoint v))) := by
  have hcnn : ∀ t : Finset I, 0 ≤ originalExpansionCoefficient rho l u s t := fun t =>
    originalExpansionCoefficient_nonneg hrho hl hlu hasp s t
  have hx : boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p ∈
      coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho) :=
    boxPoint_mem _ _ p (fun _ => hrho.le) hp
  have h1 := boxHullGap_monomial_le_expansion hrho hl hlu hasp s hx
  rw [originalBoxPoint_commonAspect hrho hl p] at h1
  have h2 : ∀ t : Finset I,
      boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho) (monomial t)
          (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p) =
        hullGap (physMonomial (rho - 1) t) p := by
    intro t
    rw [boxHullGap_eq_of_mem _ _ (fun _ => hrho.le) _ p hp]
    exact congrArg (fun f => hullGap f p) (funext fun q => monomial_commonAspect rho t q)
  have hdef : sSup (boxEnvelopeValues l u (monomial s) (boxPoint l u p)) -
        μ.expect (fun v => monomial s (boxPoint l u (vertexPoint v))) =
      ∑ t ∈ s.powerset, originalExpansionCoefficient rho l u s t *
        (physUpper (rho - 1) t p -
          μ.expect fun v => physMonomial (rho - 1) t (vertexPoint v)) := by
    rw [originalMonomial_deficiency_eq_sum hrho hl hlu hasp hp μ s]
    refine Finset.sum_congr rfl fun t _ => ?_
    rw [boxEnvelope_sSup_commonAspect_monomial hrho.le hp t]
    simp only [monomial_commonAspect]
  calc boxHullGap l u (monomial s) (boxPoint l u p)
      ≤ ∑ t ∈ s.powerset, originalExpansionCoefficient rho l u s t *
          boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho) (monomial t)
            (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p) := h1
    _ ≤ ∑ t ∈ s.powerset, originalExpansionCoefficient rho l u s t *
          (U * (physUpper (rho - 1) t p -
            μ.expect fun v => physMonomial (rho - 1) t (vertexPoint v))) := by
        refine Finset.sum_le_sum fun t _ => ?_
        rw [h2 t]
        exact mul_le_mul_of_nonneg_left (hcap t) (hcnn t)
    _ = U * (sSup (boxEnvelopeValues l u (monomial s) (boxPoint l u p)) -
          μ.expect fun v => monomial s (boxPoint l u (vertexPoint v))) := by
        rw [hdef, Finset.mul_sum]
        exact Finset.sum_congr rfl fun t _ => by ring

/-- PB26(4), packaged: a uniform per-physical-monomial capture guarantee on
`[1, rho]^n` gives, at **every** point of **every** strictly positive box of
aspect ratio at most `rho`, one vertex law with the prescribed original-box means
that captures at least `1 / U` of the gap of every original monomial.  The
statement mentions neither the expansion nor the ambient box: the law is a law on
the vertices of the original box and the deficiency is measured there. -/
theorem originalBox_monomial_capture {rho U : ℝ} (hrho : 1 < rho)
    {l u : I → ℝ} (hl : ∀ i, 0 < l i) (hlu : ∀ i, l i ≤ u i) (hasp : ∀ i, u i ≤ rho * l i)
    (hcap : ∀ q ∈ cube I, ∃ μ : Law (Vertex I), HasMeans μ q ∧
      ∀ t : Finset I, hullGap (physMonomial (rho - 1) t) q ≤
        U * (physUpper (rho - 1) t q -
          μ.expect fun v => physMonomial (rho - 1) t (vertexPoint v)))
    {z : I → ℝ} (hz : z ∈ coordinateBox l u) :
    ∃ μ : Law (Vertex I),
      (∀ i, μ.expect (fun v => boxPoint l u (vertexPoint v) i) = z i) ∧
      ∀ s : Finset I, boxHullGap l u (monomial s) z ≤
        U * (sSup (boxEnvelopeValues l u (monomial s) z) -
          μ.expect fun v => monomial s (boxPoint l u (vertexPoint v))) := by
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint l u hlu z hz
  obtain ⟨μ, hm, hcapμ⟩ := hcap p hp
  refine ⟨μ, fun i => ?_, fun s =>
    originalMonomial_capture_of_physMonomial_capture hrho hl hlu hasp hp μ hcapμ s⟩
  rw [pullbackLaw_means hrho hl μ hm i, originalBoxPoint_commonAspect hrho hl p]

end Capture

end

end MultilinearGap
