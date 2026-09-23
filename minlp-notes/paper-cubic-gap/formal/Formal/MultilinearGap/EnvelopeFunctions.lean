import Formal.MultilinearGap.Attainment
import Mathlib.Analysis.Convex.Function

/-! Identification of graph-hull slice endpoints with convex and concave envelopes. -/
namespace MultilinearGap

open CubicGap
noncomputable section

variable {E : Type*} [AddCommGroup E] [Module ℝ E]

/-- An attained lower endpoint of every graph-hull slice is exactly the
greatest convex underestimator on the original convex domain. -/
theorem graphHull_lower_envelope (S : Set E) (hS : Convex ℝ S) (f v : E → ℝ)
    (hv : ∀ x ∈ S, IsLeast
      {z : ℝ | (x, z) ∈ convexHull ℝ {p : E × ℝ | p.1 ∈ S ∧ p.2 = f p.1}} (v x)) :
    ConvexOn ℝ S v ∧ (∀ x ∈ S, v x ≤ f x) ∧
      ∀ g : E → ℝ, ConvexOn ℝ S g → (∀ x ∈ S, g x ≤ f x) →
        ∀ x ∈ S, g x ≤ v x := by
  refine ⟨⟨hS, ?_⟩, ?_, ?_⟩
  · intro x hx y hy a b ha hb hab
    exact (hv _ (hS hx hy ha hb hab)).2
      ((convex_convexHull ℝ _) (hv x hx).1 (hv y hy).1 ha hb hab)
  · intro x hx
    exact (hv x hx).2 (subset_convexHull ℝ _ ⟨hx, rfl⟩)
  · intro g hg hgf x hx
    have hsub : {p : E × ℝ | p.1 ∈ S ∧ p.2 = f p.1} ⊆
        {p : E × ℝ | p.1 ∈ S ∧ g p.1 ≤ p.2} := by
      rintro p ⟨hp, he⟩
      exact ⟨hp, he ▸ hgf p.1 hp⟩
    exact (convexHull_min hsub hg.convex_epigraph (hv x hx).1).2

/-- The upper endpoints are exactly the least concave overestimator. -/
theorem graphHull_upper_envelope (S : Set E) (hS : Convex ℝ S) (f w : E → ℝ)
    (hw : ∀ x ∈ S, IsGreatest
      {z : ℝ | (x, z) ∈ convexHull ℝ {p : E × ℝ | p.1 ∈ S ∧ p.2 = f p.1}} (w x)) :
    ConcaveOn ℝ S w ∧ (∀ x ∈ S, f x ≤ w x) ∧
      ∀ g : E → ℝ, ConcaveOn ℝ S g → (∀ x ∈ S, f x ≤ g x) →
        ∀ x ∈ S, w x ≤ g x := by
  refine ⟨⟨hS, ?_⟩, ?_, ?_⟩
  · intro x hx y hy a b ha hb hab
    exact (hw _ (hS hx hy ha hb hab)).2
      ((convex_convexHull ℝ _) (hw x hx).1 (hw y hy).1 ha hb hab)
  · intro x hx
    exact (hw x hx).2 (subset_convexHull ℝ _ ⟨hx, rfl⟩)
  · intro g hg hfg x hx
    have hsub : {p : E × ℝ | p.1 ∈ S ∧ p.2 = f p.1} ⊆
        {p : E × ℝ | p.1 ∈ S ∧ p.2 ≤ g p.1} := by
      rintro p ⟨hp, he⟩
      exact ⟨hp, he ▸ hfg p.1 hp⟩
    exact (convexHull_min hsub hg.convex_hypograph (hw x hx).1).2

variable {I : Type*} [Finite I] [DecidableEq I]

omit [Finite I] [DecidableEq I] in
theorem coordinateBox_convex (l u : I → ℝ) : Convex ℝ (coordinateBox l u) := by
  intro x hx y hy a b ha hb hab i
  have hx' := hx i
  have hy' := hy i
  change l i ≤ a * x i + b * y i ∧ a * x i + b * y i ≤ u i
  have hl : a * l i + b * l i = l i := by rw [← add_mul, hab, one_mul]
  have hu : a * u i + b * u i = u i := by rw [← add_mul, hab, one_mul]
  constructor
  · nlinarith [mul_le_mul_of_nonneg_left hx'.1 ha,
      mul_le_mul_of_nonneg_left hy'.1 hb]
  · nlinarith [mul_le_mul_of_nonneg_left hx'.2 ha,
      mul_le_mul_of_nonneg_left hy'.2 hb]

omit [Finite I] [DecidableEq I] in
theorem cube_convex : Convex ℝ (cube I) :=
  coordinateBox_convex (fun _ => 0) (fun _ => 1)

/-- The lower continuous graph-hull slice endpoint is the greatest convex
underestimator of a separately affine function on the cube. -/
theorem cube_convex_envelope (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f) :
    ConvexOn ℝ (cube I) (fun x => sInf (envelopeValues f x)) ∧
      (∀ x ∈ cube I, sInf (envelopeValues f x) ≤ f x) ∧
      ∀ g : (I → ℝ) → ℝ, ConvexOn ℝ (cube I) g →
        (∀ x ∈ cube I, g x ≤ f x) →
        ∀ x ∈ cube I, g x ≤ sInf (envelopeValues f x) := by
  exact graphHull_lower_envelope (cube I) cube_convex f _
    (fun x hx => (envelopeValues_endpoints f hf x hx).1)

/-- The upper continuous graph-hull slice endpoint is the least concave
overestimator on the cube. -/
theorem cube_concave_envelope (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f) :
    ConcaveOn ℝ (cube I) (fun x => sSup (envelopeValues f x)) ∧
      (∀ x ∈ cube I, f x ≤ sSup (envelopeValues f x)) ∧
      ∀ g : (I → ℝ) → ℝ, ConcaveOn ℝ (cube I) g →
        (∀ x ∈ cube I, f x ≤ g x) →
        ∀ x ∈ cube I, sSup (envelopeValues f x) ≤ g x := by
  exact graphHull_upper_envelope (cube I) cube_convex f _
    (fun x hx => (envelopeValues_endpoints f hf x hx).2)

/-- Box lower endpoints have the same envelope interpretation, including
fixed coordinates and without requiring nonnegative box endpoints. -/
theorem box_convex_envelope (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f) :
    ConvexOn ℝ (coordinateBox l u) (fun x => sInf (boxEnvelopeValues l u f x)) ∧
      (∀ x ∈ coordinateBox l u, sInf (boxEnvelopeValues l u f x) ≤ f x) ∧
      ∀ g : (I → ℝ) → ℝ, ConvexOn ℝ (coordinateBox l u) g →
        (∀ x ∈ coordinateBox l u, g x ≤ f x) →
        ∀ x ∈ coordinateBox l u, g x ≤ sInf (boxEnvelopeValues l u f x) := by
  exact graphHull_lower_envelope (coordinateBox l u) (coordinateBox_convex l u) f _
    (fun x hx => (boxEnvelopeValues_endpoints l u hlu f hf x hx).1)

/-- Box upper endpoints are the least concave overestimator. -/
theorem box_concave_envelope (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f) :
    ConcaveOn ℝ (coordinateBox l u) (fun x => sSup (boxEnvelopeValues l u f x)) ∧
      (∀ x ∈ coordinateBox l u, f x ≤ sSup (boxEnvelopeValues l u f x)) ∧
      ∀ g : (I → ℝ) → ℝ, ConcaveOn ℝ (coordinateBox l u) g →
        (∀ x ∈ coordinateBox l u, f x ≤ g x) →
        ∀ x ∈ coordinateBox l u, sSup (boxEnvelopeValues l u f x) ≤ g x := by
  exact graphHull_upper_envelope (coordinateBox l u) (coordinateBox_convex l u) f _
    (fun x hx => (boxEnvelopeValues_endpoints l u hlu f hf x hx).2)

end
end MultilinearGap
