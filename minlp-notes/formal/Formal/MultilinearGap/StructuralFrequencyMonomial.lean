import Formal.MultilinearGap.StructuralFactorGaps
import Formal.MultilinearGap.GeneralGaps

/-!
# Original monomials as convex cardinality factors

The final jump table represents a nonnegative weighted monomial, including
empty and singleton supports. The transfer theorem specializes a separately
proved cardinality bound without changing the original term supports.
-/
namespace MultilinearGap
open CubicGap
noncomputable section
variable {I : Type*} [Fintype I] [DecidableEq I]

/-- The value is zero below the last attainable count and `a` at that count. -/
def monomialCountTable (d : ℕ) (a : ℝ) (k : ℕ) : ℝ := if d ≤ k then a else 0

theorem monomialCountTable_convex (d : ℕ) (a : ℝ) (ha : 0 ≤ a) :
    ConvexCountTable (monomialCountTable d a) d := by
  intro k hk
  have h₀ : ¬d ≤ k := by omega
  have h₁ : ¬d ≤ k + 1 := by omega
  simp only [monomialCountTable, if_neg h₀, if_neg h₁, sub_zero, sub_self]
  split_ifs <;> linarith

omit [Fintype I] [DecidableEq I] in
theorem monomialCountTable_vertex (s : Finset I) (a : ℝ) (v : Vertex I) :
    monomialCountTable s.card a (countOn s v) = a * monomial s (vertexPoint v) := by
  classical
  by_cases h : ∀ i ∈ s, v i = true
  · have hc : countOn s v = s.card := by
      simp only [countOn, Finset.filter_eq_self.mpr h]
    have hm : monomial s (vertexPoint v) = 1 :=
      Finset.prod_eq_one (fun i hi => by simp [vertexPoint, h i hi])
    simp [monomialCountTable, hc, hm]
  · obtain ⟨i, hi⟩ := not_forall.mp h
    obtain ⟨hi, hv⟩ := Classical.not_imp.mp hi
    have hm : monomial s (vertexPoint v) = 0 :=
      Finset.prod_eq_zero hi (by simp [vertexPoint, hv])
    have hc : ¬s.card ≤ countOn s v := by
      intro hc
      have he : s.filter (fun j => v j = true) = s :=
        Finset.eq_of_subset_of_card_le (Finset.filter_subset _ _) hc
      have hh : i ∈ s.filter (fun j => v j = true) := by rw [he]; exact hi
      exact hv (Finset.mem_filter.mp hh).2
    simp [monomialCountTable, hc, hm]

omit [Fintype I] in
/-- Equal binary tables have equal envelope slices when both functions are
separately affine. -/
theorem envelopeValues_eq_of_vertex_eq [Finite I] (f g : (I → ℝ) → ℝ)
    (hf : SeparatelyAffine f) (hg : SeparatelyAffine g)
    (hfg : ∀ v : Vertex I, f (vertexPoint v) = g (vertexPoint v)) (x : I → ℝ) :
    envelopeValues f x = envelopeValues g x := by
  let := Fintype.ofFinite I
  ext q
  change (x, q) ∈ convexHull ℝ (cubeGraph f) ↔ (x, q) ∈ convexHull ℝ (cubeGraph g)
  rw [mem_cubeGraph_hull_iff _ hf, mem_cubeGraph_hull_iff _ hg]
  simp_rw [hfg]

omit [Fintype I] in
private theorem scaled_monomial_separatelyAffine (s : Finset I) (a : ℝ) :
    SeparatelyAffine (fun y => a * monomial s y) := by
  intro y i t
  dsimp only
  rw [monomial_coordinate_affine]
  ring

theorem cardinalityFactor_monomial_envelope (s : Finset I) (a : ℝ) (x : I → ℝ) :
    envelopeValues (cardinalityFactor (monomialCountTable s.card a) s) x =
      envelopeValues (fun y => a * monomial s y) x := by
  apply envelopeValues_eq_of_vertex_eq _ _
    (cardinalityFactor_separatelyAffine _ _) (scaled_monomial_separatelyAffine _ _)
  intro v
  rw [cardinalityFactor_vertex, monomialCountTable_vertex]

theorem cardinalityFactor_monomial_gap (s : Finset I) (a : ℝ) (ha : 0 ≤ a)
    (x : I → ℝ) (hx : x ∈ cube I) :
    hullGap (cardinalityFactor (monomialCountTable s.card a) s) x =
      a * hullGap (monomial s) x := by
  calc
    _ = hullGap (fun y => a * monomial s y) x := by
      simp only [hullGap, cardinalityFactor_monomial_envelope]
    _ = _ := hullGap_monomial_scale s x hx a ha

/-- Specializing a proved cardinality-factor inequality to the last-jump
 tables yields the inequality for the original weighted monomial supports. -/
theorem weightedTermwiseGap_le_of_cardinality_bound (S : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I) (C : ℝ)
    (hbound : ∀ φ : {s // s ∈ S} → ℕ → ℝ,
      (∀ s, ConvexCountTable (φ s) s.val.card) →
      (∑ s, hullGap (cardinalityFactor (φ s) s.val) x) ≤
        C * hullGap (factorSum fun s => cardinalityFactor (φ s) s.val) x) :
    weightedTermwiseGap S a x ≤ C * hullGap (supportPolynomial S a) x := by
  let φ : {s // s ∈ S} → ℕ → ℝ := fun s => monomialCountTable s.val.card (a s.val)
  have h := hbound φ (fun s => monomialCountTable_convex _ _ (ha s.val s.property))
  have hsum : (∑ s, hullGap (cardinalityFactor (φ s) s.val) x) =
      weightedTermwiseGap S a x := by
    calc
      _ = ∑ s : {s // s ∈ S}, a s.val * hullGap (monomial s.val) x := by
        apply Finset.sum_congr rfl
        intro s _
        exact cardinalityFactor_monomial_gap s.val (a s.val) (ha s.val s.property) x hx
      _ = _ := Finset.sum_attach S (fun s => a s * hullGap (monomial s) x)
  have he : envelopeValues (factorSum fun s => cardinalityFactor (φ s) s.val) x =
      envelopeValues (supportPolynomial S a) x := by
    apply envelopeValues_eq_of_vertex_eq _ _
      (factorSum_separatelyAffine _ (fun _ => cardinalityFactor_separatelyAffine _ _))
      (supportPolynomial_coordinate_affine S a)
    intro v
    simp only [factorSum, cardinalityFactor_vertex, φ, monomialCountTable_vertex]
    exact Finset.sum_attach S (fun s => a s * monomial s (vertexPoint v))
  rw [hsum] at h
  simpa only [hullGap, he] using h

end
end MultilinearGap
