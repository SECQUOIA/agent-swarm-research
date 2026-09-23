import Formal.MultilinearGap.StructuralCycleTU
import Formal.MultilinearGap.StructuralTwoClasses
import Formal.MultilinearGap.StructuralTreewidthColoring
import Formal.MultilinearGap.StructuralCommonAspect
import Formal.MultilinearGap.StructuralFrequencyMonomial

/-! Actual all-cycle factor colorings yield two TU row classes and their
cardinality gap bound. The separate graph theorem supplies the coloring. -/
namespace MultilinearGap
open CubicGap TreewidthGraph
noncomputable section
set_option linter.unusedFintypeInType false
variable {I J : Type*} [Fintype I] [DecidableEq I] [Fintype J]

/-- Rows are original factors and columns are original variables. -/
def structuralScopeGraph (scope : J → Finset I) : SimpleGraph (J ⊕ I) :=
  CycleTU.matrixGraph (TUSlab.scopeMatrix scope)

def structuralFactorColor (color : J → Bool) : J ⊕ I → Bool :=
  Sum.elim color (fun _ => false)

omit [Fintype I] [Fintype J] in
/-- Restricting to one factor color transports every simple cycle into a
monochromatic simple cycle of the original incidence graph. -/
theorem colorClassMatrix_totallyUnimodular (scope : J → Finset I) (color : J → Bool)
    (hgood : Good CycleTU.rowFactor (structuralFactorColor color) (structuralScopeGraph scope))
    (b : Bool) : (colorClassMatrix scope color b).IsTotallyUnimodular := by
  classical
  apply CycleTU.totallyUnimodular_of_even_cycles
  · intro r i
    simp only [colorClassMatrix, TUSlab.scopeMatrix]
    split_ifs <;> simp
  · let e : CycleTU.matrixGraph (colorClassMatrix scope color b) →g
        structuralScopeGraph scope := {
      toFun := Sum.map Subtype.val id
      map_rel' := by
        intro v w h
        cases v <;> cases w <;> simp_all only [CycleTU.matrixGraph,
          structuralScopeGraph, StructuralTreewidth.incidenceGraph,
          colorClassMatrix, TUSlab.scopeMatrix, Sum.map_inl, Sum.map_inr, id_eq] }
    have he : Function.Injective e := Sum.map_injective.mpr
      ⟨Subtype.val_injective, Function.injective_id⟩
    intro v q hq
    have hm : Monochromatic CycleTU.rowFactor (structuralFactorColor color) b (q.map e) := by
      intro w hw hf
      rw [SimpleGraph.Walk.support_map] at hw
      obtain ⟨z, _, rfl⟩ := List.mem_map.mp hw
      cases z with
      | inl j => exact j.property
      | inr i => simp [e, CycleTU.rowFactor] at hf
    have hp := hgood (e v) (q.map e) (hq.map he) b hm
    rw [cycleParity_map] at hp
    have hf : CycleTU.rowFactor ∘ e = CycleTU.rowFactor := by
      funext z
      cases z <;> rfl
    rwa [hf] at hp

/-- The all-cycle factor coloring is sufficient for the actual scalar gap
bound, with both class distributions constructed through TU integrality. -/
theorem cardinality_gap_of_good_factor_coloring (scope : J → Finset I) (color : J → Bool)
    (hgood : Good CycleTU.rowFactor (structuralFactorColor color) (structuralScopeGraph scope))
    (φ : J → ℕ → ℝ) (hφ : ∀ j, ConvexCountTable (φ j) (scope j).card)
    (f : J → (I → ℝ) → ℝ) (hf : ∀ j, SeparatelyAffine (f j))
    (hv : ∀ j v, f j (vertexPoint v) = φ j (countOn (scope j) v))
    (x : I → ℝ) (hx : x ∈ cube I) :
    (∑ j, hullGap (f j) x) ≤ 2 * hullGap (factorSum f) x :=
  cardinality_two_TU_classes_bound scope color
    (colorClassMatrix_totallyUnimodular scope color hgood) φ hφ f hf hv x hx

/-- The actual incidence-treewidth hypothesis supplies both TU laws. -/
theorem treewidthTwo_cardinality_bound (scope : J → Finset I)
    (hwidth : StructuralTreewidth.HasTreewidthAtMost (structuralScopeGraph scope) 2)
    (φ : J → ℕ → ℝ) (hφ : ∀ j, ConvexCountTable (φ j) (scope j).card)
    (f : J → (I → ℝ) → ℝ) (hf : ∀ j, SeparatelyAffine (f j))
    (hv : ∀ j v, f j (vertexPoint v) = φ j (countOn (scope j) v))
    (x : I → ℝ) (hx : x ∈ cube I) :
    (∑ j, hullGap (f j) x) ≤ 2 * hullGap (factorSum f) x := by
  have hbip : ∀ a b, (structuralScopeGraph scope).Adj a b →
      CycleTU.rowFactor a ≠ CycleTU.rowFactor b := by
    intro a b hab
    cases a <;> cases b <;>
      simp_all [structuralScopeGraph, CycleTU.matrixGraph,
        StructuralTreewidth.incidenceGraph, CycleTU.rowFactor]
  obtain ⟨c, hc⟩ := StructuralTreewidth.exists_good_of_treewidth_two
    CycleTU.rowFactor hbip hwidth
  have hgood : Good CycleTU.rowFactor (structuralFactorColor fun j => c (.inl j))
      (structuralScopeGraph scope) := by
    intro v p hp b hm
    apply hc v p hp b
    intro z hz hfz
    cases z with
    | inl j => exact hm (.inl j) hz rfl
    | inr i => simp [CycleTU.rowFactor] at hfz
  exact cardinality_gap_of_good_factor_coloring scope _ hgood φ hφ f hf hv x hx

/-- Swapping the two incidence sides preserves the original treewidth
hypothesis; the matrix convention puts factors first. -/
theorem structuralScopeGraph_treewidth_of_incidence (scope : J → Finset I) (width : ℕ)
    (hwidth : StructuralTreewidth.HasTreewidthAtMost
      (StructuralTreewidth.incidenceGraph fun i j => i ∈ scope j) width) :
    StructuralTreewidth.HasTreewidthAtMost (structuralScopeGraph scope) width := by
  classical
  let e : structuralScopeGraph scope →g
      StructuralTreewidth.incidenceGraph (fun i j => i ∈ scope j) := {
    toFun := Sum.swap
    map_rel' := by
      intro v w h
      cases v <;> cases w <;>
        simp_all [structuralScopeGraph, CycleTU.matrixGraph,
          StructuralTreewidth.incidenceGraph, TUSlab.scopeMatrix] }
  apply hwidth.of_injective_hom e
  intro v w h
  have hh := congrArg Sum.swap h
  change v.swap.swap = w.swap.swap at hh
  simpa using hh

/-- The sharp flower belongs to the graph class in the final gap theorem. -/
theorem treewidthTwo_flower_membership (n : ℕ) :
    StructuralTreewidth.HasTreewidthAtMost
      (structuralScopeGraph fun s : {s // s ∈ StructuralSharpness.supports n} => s.val) 2 :=
  structuralScopeGraph_treewidth_of_incidence _ 2
    (StructuralTreewidth.flower_supports_treewidth_le_two n)

omit [Fintype I] [Fintype J] in
/-- Deleting incidences preserves the actual treewidth certificate. -/
theorem structuralScopeGraph_treewidth_mono (scope small : J → Finset I)
    (hsub : ∀ j, small j ⊆ scope j)
    (hwidth : StructuralTreewidth.HasTreewidthAtMost (structuralScopeGraph scope) 2) :
    StructuralTreewidth.HasTreewidthAtMost (structuralScopeGraph small) 2 := by
  apply hwidth.mono
  intro v w h
  cases v <;> cases w <;>
    simp_all only [structuralScopeGraph, CycleTU.matrixGraph, StructuralTreewidth.incidenceGraph,
      TUSlab.scopeMatrix, ite_eq_left_iff, zero_ne_one, imp_false, not_not]
  all_goals apply hsub; assumption

/-- Sharp constant two on common-aspect physical boxes, retaining each
original factor. Fixed coordinates and ratio one are allowed. -/
theorem treewidthTwo_commonAspect_bound (scope : J → Finset I)
    (hwidth : StructuralTreewidth.HasTreewidthAtMost (structuralScopeGraph scope) 2)
    (a : J → ℝ) (ha : ∀ j, 0 ≤ a j)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (rho : J → ℝ) (hrho : ∀ j, 0 ≤ rho j)
    (hr : ∀ j i, i ∈ varyingBoxSupport l u (scope j) → u i = rho j * l i)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    (∑ j, a j * boxHullGap l u (monomial (scope j)) x) ≤
      2 * boxHullGap l u (factorSum fun j y => a j * monomial (scope j) y) x := by
  apply commonAspect_original_box_transfer scope a ha l u hl hlu rho hrho hr 2 _ x hx
  intro f φ hf hφ hv p hp
  exact treewidthTwo_cardinality_bound _
    (structuralScopeGraph_treewidth_mono scope _ (fun _ => Finset.filter_subset _ _) hwidth)
    φ hφ f hf hv p hp

/-- Original nonnegative monomials on the unit cube. -/
theorem treewidthTwo_monomial_bound (S : Finset (Finset I))
    (hwidth : StructuralTreewidth.HasTreewidthAtMost
      (structuralScopeGraph fun s : {s // s ∈ S} => s.val) 2)
    (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s) (x : I → ℝ) (hx : x ∈ cube I) :
    weightedTermwiseGap S a x ≤ 2 * hullGap (supportPolynomial S a) x := by
  apply weightedTermwiseGap_le_of_cardinality_bound S a ha x hx 2
  intro φ hφ
  exact treewidthTwo_cardinality_bound _ hwidth φ hφ _
    (fun s => cardinalityFactor_separatelyAffine (φ s) s.val)
    (fun s v => cardinalityFactor_vertex (φ s) s.val v) x hx

/-- Arbitrary zero-lower boxes, with the original factor graph unchanged. -/
theorem treewidthTwo_zeroLower_bound (S : Finset (Finset I))
    (hwidth : StructuralTreewidth.HasTreewidthAtMost
      (structuralScopeGraph fun s : {s // s ∈ S} => s.val) 2)
    (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (u : I → ℝ) (hu : ∀ i, 0 ≤ u i) (x : I → ℝ)
    (hx : x ∈ coordinateBox (fun _ => 0) u) :
    boxTermwiseGap S a (fun _ => 0) u x ≤
      2 * boxHullGap (fun _ => 0) u (supportPolynomial S a) x :=
  zeroLower_gap_bound_transfer S 2 (treewidthTwo_monomial_bound S hwidth) a ha u hu x hx

end
end MultilinearGap
