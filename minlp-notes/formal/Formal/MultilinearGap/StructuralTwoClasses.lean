import Formal.MultilinearGap.StructuralCardinalityTU
import Formal.MultilinearGap.StructuralFactorGaps

/-! Two TU row classes give a factor-two cardinality gap bound. The graph
coloring theorem must supply this partition; it is an explicit input here. -/
namespace MultilinearGap
open CubicGap
noncomputable section
variable {I J : Type*} [Fintype I] [DecidableEq I] [Fintype J]

/-- Original factors in one of the two row classes. -/
abbrev FactorColorClass (color : J → Bool) (b : Bool) := {j : J // color j = b}

/-- The incidence matrix on a single class retains every original coordinate. -/
def colorClassMatrix (scope : J → Finset I) (color : J → Bool) (b : Bool) :
    Matrix (FactorColorClass color b) I ℤ :=
  TUSlab.scopeMatrix (fun j : FactorColorClass color b => scope j.val)

/-- No graph assumption is hidden in this theorem: a genuine TU row partition
is the sufficient hypothesis, and both attaining class laws are constructed. -/
theorem cardinality_two_TU_classes_bound (scope : J → Finset I) (color : J → Bool)
    (hTU : ∀ b, (colorClassMatrix scope color b).IsTotallyUnimodular)
    (φ : J → ℕ → ℝ) (hφ : ∀ j, ConvexCountTable (φ j) (scope j).card)
    (f : J → (I → ℝ) → ℝ) (hf : ∀ j, SeparatelyAffine (f j))
    (hv : ∀ j v, f j (vertexPoint v) = φ j (countOn (scope j) v))
    (x : I → ℝ) (hx : x ∈ cube I) :
    (∑ j, hullGap (f j) x) ≤ 2 * hullGap (factorSum f) x := by
  have hc (b : Bool) := TUSlab.exists_cardinality_scopeLaw
    (fun j : FactorColorClass color b => scope j.val) (hTU b) x hx
  obtain ⟨μ, hm, hμ⟩ := hc false
  obtain ⟨ν, hn, hν⟩ := hc true
  have hmax := factorSum_maximum f hf x (thresholdLaw x) (thresholdLaw_hasMeans x hx)
    (fun j => by
      simpa only [hv] using cardinality_maximum (φ j) (scope j) (hφ j)
        (f j) (hf j) (hv j) x hx)
  apply factorSum_two_law_bound f hf x hx hmax μ ν hm hn
  intro j
  have hmin := (cardinality_minimum (φ j) (scope j) (hφ j) (f j) (hf j)
    (hv j) x hx).csInf_eq
  cases hb : color j with
  | false =>
    left
    rw [hmin]
    simpa only [hv] using hμ ⟨j, hb⟩ (φ j)
  | true =>
    right
    rw [hmin]
    simpa only [hv] using hν ⟨j, hb⟩ (φ j)

/-- The concrete multiaffine cardinality interpolants satisfy the same bound. -/
theorem cardinalityFactor_two_TU_classes_bound (scope : J → Finset I) (color : J → Bool)
    (hTU : ∀ b, (colorClassMatrix scope color b).IsTotallyUnimodular)
    (φ : J → ℕ → ℝ) (hφ : ∀ j, ConvexCountTable (φ j) (scope j).card)
    (x : I → ℝ) (hx : x ∈ cube I) :
    (∑ j, hullGap (cardinalityFactor (φ j) (scope j)) x) ≤
      2 * hullGap (factorSum (fun j => cardinalityFactor (φ j) (scope j))) x :=
  cardinality_two_TU_classes_bound scope color hTU φ hφ _
    (fun j => cardinalityFactor_separatelyAffine (φ j) (scope j))
    (fun j => cardinalityFactor_vertex (φ j) (scope j)) x hx

end
end MultilinearGap
