import Formal.MultilinearGap.StructuralCardinality

/-! The multiaffine interpolant of a binary table, used for cardinality factors. -/

namespace MultilinearGap
open CubicGap
noncomputable section
variable {I : Type*} [Fintype I] [DecidableEq I]

/-- Tensor-product affine interpolation of a table on the binary vertices. -/
def vertexInterpolation (g : Vertex I → ℝ) (x : I → ℝ) : ℝ :=
  ∑ v, (∏ i, if v i then x i else 1 - x i) * g v

private theorem interpolation_weight_update (v : Vertex I) (x : I → ℝ)
    (i : I) (t : ℝ) :
    (∏ j, if v j then Function.update x i t j else 1 - Function.update x i t j) =
      (if v i then t else 1 - t) *
        ∏ j ∈ Finset.univ.erase i, if v j then x j else 1 - x j := by
  rw [← Finset.mul_prod_erase _ _ (Finset.mem_univ i), Function.update_self]
  congr 1
  apply Finset.prod_congr rfl
  intro j hj
  rw [Function.update_of_ne (Finset.ne_of_mem_erase hj)]

theorem vertexInterpolation_separatelyAffine (g : Vertex I → ℝ) :
    SeparatelyAffine (vertexInterpolation g) := by
  intro x i t
  simp only [vertexInterpolation, Finset.mul_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro v _
  simp only [interpolation_weight_update]
  cases v i <;> simp <;> ring

omit [DecidableEq I] in
private theorem interpolation_weight_vertex (v w : Vertex I) :
    (∏ i, if v i then vertexPoint w i else 1 - vertexPoint w i) =
      if v = w then (1 : ℝ) else 0 := by
  classical
  by_cases h : v = w
  · subst v
    rw [if_pos rfl]
    apply Finset.prod_eq_one
    intro i _
    cases hw : w i <;> simp [vertexPoint, hw]
  · rw [if_neg h]
    obtain ⟨i, hi⟩ : ∃ i, v i ≠ w i := Function.ne_iff.mp h
    apply Finset.prod_eq_zero (Finset.mem_univ i)
    cases hv : v i <;> cases hw : w i <;> simp_all [vertexPoint]

theorem vertexInterpolation_vertex (g : Vertex I → ℝ) (v : Vertex I) :
    vertexInterpolation g (vertexPoint v) = g v := by
  simp [vertexInterpolation, interpolation_weight_vertex]

theorem vertexInterpolation_eq_bernoulli (g : Vertex I → ℝ) (x : I → ℝ)
    (hx : x ∈ cube I) :
    vertexInterpolation g x = (bernoulliLaw x hx).expect g := rfl

/-- The cardinality factor is its vertex-table interpolant, not `φ (sum x)`. -/
def cardinalityFactor (φ : ℕ → ℝ) (s : Finset I) : (I → ℝ) → ℝ :=
  vertexInterpolation (fun v => φ (countOn s v))

theorem cardinalityFactor_vertex (φ : ℕ → ℝ) (s : Finset I) (v : Vertex I) :
    cardinalityFactor φ s (vertexPoint v) = φ (countOn s v) :=
  vertexInterpolation_vertex _ _

theorem cardinalityFactor_separatelyAffine (φ : ℕ → ℝ) (s : Finset I) :
    SeparatelyAffine (cardinalityFactor φ s) := vertexInterpolation_separatelyAffine _

theorem cardinalityFactor_minimum (φ : ℕ → ℝ) (s : Finset I)
    (hφ : ConvexCountTable φ s.card) (x : I → ℝ) (hx : x ∈ cube I) :
    IsLeast (envelopeValues (cardinalityFactor φ s) x) (cardinalityLower φ s x) :=
  cardinality_minimum φ s hφ _ (cardinalityFactor_separatelyAffine φ s)
    (cardinalityFactor_vertex φ s) x hx

end
end MultilinearGap
