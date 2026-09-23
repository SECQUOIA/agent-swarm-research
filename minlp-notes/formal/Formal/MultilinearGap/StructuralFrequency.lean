import Formal.MultilinearGap.GeneralGaps
import Formal.MultilinearGap.MonomialEnvelope
import Formal.MultilinearGap.Attainment

/-!
# Frequency-two incidence and exact coverage semantics

These identities express actual scalar graph-hull widths as baseline-subtracted
coverage. They do not assume or assert the graph rounding theorem.
-/
namespace MultilinearGap
open CubicGap
noncomputable section
variable {I : Type*} [Fintype I] [DecidableEq I]

/-- Every coordinate occurs in at most two original supports. -/
def FrequencyTwo (S : Finset (Finset I)) : Prop :=
  ∀ i, (S.filter fun s => i ∈ s).card ≤ 2

/-- A loopless multigraph; distinct edge labels may have the same endpoints. -/
structure FrequencyGraph (V E : Type*) where
  left : E → V
  right : E → V
  loopless : ∀ e, left e ≠ right e

namespace FrequencyGraph
variable {V E : Type*} [Fintype V] [Fintype E] [DecidableEq V] [DecidableEq E]

def incident (G : FrequencyGraph V E) (v : V) : Finset E :=
  Finset.univ.filter fun e => G.left e = v ∨ G.right e = v

omit [Fintype V] [DecidableEq E] in
@[simp] theorem mem_incident (G : FrequencyGraph V E) (v : V) (e : E) :
    e ∈ G.incident v ↔ G.left e = v ∨ G.right e = v := by simp [incident]

theorem incident_rows (G : FrequencyGraph V E) (e : E) :
    (Finset.univ.filter fun v => e ∈ G.incident v) = {G.left e, G.right e} := by
  ext v
  simp [eq_comm]

/-- Parallel edges do not change the number of rows incident to one edge. -/
theorem incident_rows_card (G : FrequencyGraph V E) (e : E) :
    (Finset.univ.filter fun v => e ∈ G.incident v).card = 2 := by
  rw [incident_rows]
  simp [G.loopless e]

/-- Taking one monomial for each distinct incidence support preserves frequency two. -/
theorem frequencyTwo_incident_image (G : FrequencyGraph V E) :
    FrequencyTwo (Finset.univ.image G.incident) := by
  intro e
  have hsub : ((Finset.univ.image G.incident).filter fun s => e ∈ s) ⊆
      {G.incident (G.left e), G.incident (G.right e)} := by
    intro s hs
    obtain ⟨hs, he⟩ := Finset.mem_filter.mp hs
    obtain ⟨v, _, rfl⟩ := Finset.mem_image.mp hs
    rcases (G.mem_incident v e).mp he with hv | hv
    · simp [hv]
    · simp [hv]
  exact (Finset.card_le_card hsub).trans (by
    by_cases h : G.incident (G.left e) = G.incident (G.right e) <;> simp [h])
end FrequencyGraph

def failureComplement (p : I → ℝ) : I → ℝ := fun i => 1 - p i

omit [Fintype I] [DecidableEq I] in
@[simp] theorem failureComplement_involutive (p : I → ℝ) :
    failureComplement (failureComplement p) = p := by
  funext i
  simp [failureComplement]

omit [Fintype I] [DecidableEq I] in
theorem failureComplement_mem_cube {p : I → ℝ} (hp : p ∈ cube I) :
    failureComplement p ∈ cube I := by
  intro i
  have := hp i
  constructor <;> dsimp [failureComplement] <;> linarith

/-- The nested-event coverage baseline, zero for an empty support. -/
def failureBaseline (s : Finset I) (p : I → ℝ) : ℝ :=
  1 - monomialUpper s (failureComplement p)

omit [Fintype I] [DecidableEq I] in
/-- The baseline is the largest incident failure probability. -/
theorem failureBaseline_eq_anchor (s : Finset I) (p : I → ℝ) (i : I)
    (hi : i ∈ s) (hmax : ∀ j ∈ s, p j ≤ p i) : failureBaseline s p = p i := by
  rw [failureBaseline, monomialUpper_eq_anchor s (failureComplement p) i hi
    (fun j hj => by dsimp [failureComplement]; linarith [hmax j hj])]
  simp [failureComplement]

omit [Fintype I] [DecidableEq I] in
theorem coordinate_le_failureBaseline (s : Finset I) (p : I → ℝ) (i : I)
    (hi : i ∈ s) : p i ≤ failureBaseline s p := by
  obtain ⟨j, hj, hmin⟩ := monomial_min_anchor s ⟨i, hi⟩ (failureComplement p)
  have hmax : ∀ k ∈ s, p k ≤ p j := by
    intro k hk
    have hh := hmin k hk
    dsimp [failureComplement] at hh
    linarith
  rw [failureBaseline_eq_anchor s p j hj hmax]
  exact hmax i hi

omit [Fintype I] [DecidableEq I] in
/-- The baseline cannot decrease after a mean-preserving finite decomposition. -/
theorem failureBaseline_le_expect {Ω : Type*} [Fintype Ω] (μ : Law Ω)
    (z : Ω → I → ℝ) (p : I → ℝ)
    (hm : ∀ i, μ.expect (fun w => z w i) = p i) (s : Finset I) :
    failureBaseline s p ≤ μ.expect (fun w => failureBaseline s (z w)) := by
  by_cases hs : s.Nonempty
  · obtain ⟨i, hi, hmin⟩ := monomial_min_anchor s hs (failureComplement p)
    have hmax : ∀ j ∈ s, p j ≤ p i := by
      intro j hj
      have hh := hmin j hj
      dsimp [failureComplement] at hh
      linarith
    rw [failureBaseline_eq_anchor s p i hi hmax, ← hm i]
    exact μ.expect_mono fun w => coordinate_le_failureBaseline s (z w) i hi
  · have he := Finset.not_nonempty_iff_eq_empty.mp hs
    subst s
    simp [failureBaseline]

/-- The individual union bound, attainable separately for each factor. -/
def failureCap (s : Finset I) (p : I → ℝ) : ℝ := min 1 (∑ i ∈ s, p i)

def failureCovered (s : Finset I) (v : Vertex I) : ℝ :=
  if ∃ i ∈ s, v i = true then 1 else 0

def complementVertex (v : Vertex I) : Vertex I := fun i => !(v i)

omit [Fintype I] [DecidableEq I] in
@[simp] theorem vertexPoint_complement (v : Vertex I) (i : I) :
    vertexPoint (complementVertex v) i = 1 - vertexPoint v i := by
  cases h : v i <;> simp [complementVertex, vertexPoint, h]

theorem complementLaw_hasMeans (μ : Law (Vertex I)) {p : I → ℝ}
    (hm : HasMeans μ p) : HasMeans (μ.map complementVertex) (failureComplement p) := by
  intro i
  rw [Law.expect_map]
  change μ.expect (fun v => vertexPoint (complementVertex v) i) = 1 - p i
  simp_rw [vertexPoint_complement]
  rw [Law.expect_sub, Law.expect_const, hm i]

omit [Fintype I] [DecidableEq I] in
theorem monomial_complement_eq_uncovered (s : Finset I) (v : Vertex I) :
    monomial s (vertexPoint (complementVertex v)) = 1 - failureCovered s v := by
  by_cases h : ∃ i ∈ s, v i = true
  · obtain ⟨i, hi, hv⟩ := h
    rw [failureCovered, if_pos ⟨i, hi, hv⟩]
    simp only [sub_self]
    exact Finset.prod_eq_zero hi (by simp [complementVertex, vertexPoint, hv])
  · rw [failureCovered, if_neg h, sub_zero]
    apply Finset.prod_eq_one
    intro i hi
    have hv : v i = false := by
      cases hv : v i
      · rfl
      · exact False.elim (h ⟨i, hi, hv⟩)
    simp [complementVertex, vertexPoint, hv]

/-- The exact c-b identity, including constant and singleton supports. -/
theorem monomial_gap_eq_failureCap_sub_baseline (s : Finset I)
    (p : I → ℝ) (hp : p ∈ cube I) :
    hullGap (monomial s) (failureComplement p) = failureCap s p - failureBaseline s p := by
  have hx := failureComplement_mem_cube hp
  have hsum : (∑ i ∈ s, failureComplement p i) - (s.card - 1 : ℝ) =
      1 - ∑ i ∈ s, p i := by
    simp [failureComplement, Finset.sum_sub_distrib]
  have hmin := (monomial_minimum s _ hx).csInf_eq
  have hmax : sSup (envelopeValues (monomial s) (failureComplement p)) =
      monomialUpper s (failureComplement p) := by
    by_cases hs : s.Nonempty
    · obtain ⟨i, hi, hleast⟩ := monomial_min_anchor s hs (failureComplement p)
      rw [monomialUpper_eq_anchor s _ i hi hleast]
      exact (monomial_maximum_of_min_coordinate s _ hx i hi hleast).csSup_eq
    · have he := Finset.not_nonempty_iff_eq_empty.mp hs
      subst s
      have hc : envelopeValues (monomial (∅ : Finset I)) (failureComplement p) = {1} := by
        ext z
        constructor
        · intro hz
          obtain ⟨μ, _, hv⟩ := (mem_cubeGraph_hull_iff _
            (monomial_coordinate_affine ∅) _ z).mp hz
          simpa [monomial] using hv.symm
        · intro hz
          have hz' : z = 1 := hz
          subst z
          simpa using (monomial_minimum ∅ _ hx).1
      simp [hc]
  rw [hullGap, hmax, hmin, hsum, failureCap, failureBaseline]
  rcases le_total (∑ i ∈ s, p i) 1 with h | h
  · rw [min_eq_right h, max_eq_right (by linarith)]
    ring
  · rw [min_eq_left h, max_eq_left (by linarith)]
    ring

def shiftedCoverage (S : Finset (Finset I)) (a : Finset I → ℝ)
    (p : I → ℝ) (μ : Law (Vertex I)) : ℝ :=
  ∑ s ∈ S, a s * (μ.expect (failureCovered s) - failureBaseline s p)

theorem shiftedCoverage_eq (S : Finset (Finset I)) (a : Finset I → ℝ)
    (p : I → ℝ) (μ : Law (Vertex I)) :
    shiftedCoverage S a p μ = (∑ s ∈ S, a s * monomialUpper s (failureComplement p)) -
      (μ.map complementVertex).expect (fun v => supportPolynomial S a (vertexPoint v)) := by
  rw [polynomial_expect, ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro s hs
  rw [Law.expect_map]
  change a s * (μ.expect (failureCovered s) - failureBaseline s p) =
    a s * monomialUpper s (failureComplement p) -
      a s * μ.expect (fun v => monomial s (vertexPoint (complementVertex v)))
  simp_rw [monomial_complement_eq_uncovered]
  rw [Law.expect_sub, Law.expect_const, failureBaseline]
  ring

/-- Every feasible failure law gives a lower bound on the actual scalar gap. -/
theorem shiftedCoverage_le_hullGap (S : Finset (Finset I)) (a : Finset I → ℝ)
    (ha : ∀ s ∈ S, 0 ≤ a s) (p : I → ℝ) (hp : p ∈ cube I)
    (μ : Law (Vertex I)) (hm : HasMeans μ p) :
    shiftedCoverage S a p μ ≤ hullGap (supportPolynomial S a) (failureComplement p) := by
  rw [shiftedCoverage_eq, hullGap,
    (positive_polynomial_maximum_general S a ha _ (failureComplement_mem_cube hp)).csSup_eq]
  have hmem : (μ.map complementVertex).expect
      (fun v => supportPolynomial S a (vertexPoint v)) ∈
      envelopeValues (supportPolynomial S a) (failureComplement p) :=
    (mem_cubeGraph_hull_iff _ (supportPolynomial_coordinate_affine S a) _ _).mpr
      ⟨_, complementLaw_hasMeans μ hm, rfl⟩
  exact sub_le_sub_left (csInf_le (polynomial_envelope_bddBelow S a ha _) hmem) _

/-- The maximum shifted coverage is exactly the actual scalar graph-hull gap. -/
theorem hullGap_isGreatest_shiftedCoverage (S : Finset (Finset I)) (a : Finset I → ℝ)
    (ha : ∀ s ∈ S, 0 ≤ a s) (p : I → ℝ) (hp : p ∈ cube I) :
    IsGreatest {q | ∃ μ : Law (Vertex I), HasMeans μ p ∧ q = shiftedCoverage S a p μ}
      (hullGap (supportPolynomial S a) (failureComplement p)) := by
  constructor
  · obtain ⟨ν, hm, hv⟩ := (envelope_endpoints_attained_by_laws (supportPolynomial S a)
      (supportPolynomial_coordinate_affine S a) _ (failureComplement_mem_cube hp)).1
    let μ := ν.map complementVertex
    have hm' : HasMeans μ p := by
      simpa only [failureComplement_involutive] using complementLaw_hasMeans ν hm
    refine ⟨μ, hm', ?_⟩
    have hcomp : (μ.map complementVertex).expect
        (fun v => supportPolynomial S a (vertexPoint v)) =
        ν.expect (fun v => supportPolynomial S a (vertexPoint v)) := by
      simp only [μ, Law.expect_map, Function.comp_def]
      have hdouble (v : Vertex I) : complementVertex (complementVertex v) = v := by
        funext i
        simp [complementVertex]
      simp_rw [hdouble]
    rw [shiftedCoverage_eq, hcomp, hv, hullGap,
      (positive_polynomial_maximum_general S a ha _ (failureComplement_mem_cube hp)).csSup_eq]
  · rintro q ⟨μ, hm, rfl⟩
    exact shiftedCoverage_le_hullGap S a ha p hp μ hm

theorem weightedTermwiseGap_failure (S : Finset (Finset I)) (a : Finset I → ℝ)
    (p : I → ℝ) (hp : p ∈ cube I) :
    weightedTermwiseGap S a (failureComplement p) =
      ∑ s ∈ S, a s * (failureCap s p - failureBaseline s p) := by
  unfold weightedTermwiseGap
  simp_rw [monomial_gap_eq_failureCap_sub_baseline _ p hp]
end
end MultilinearGap
