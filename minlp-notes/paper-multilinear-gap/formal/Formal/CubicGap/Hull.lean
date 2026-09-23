import Formal.CubicGap.Laws

/-! Separately affine graph hulls on a cube are exactly their binary graph hulls. -/

namespace CubicGap

variable {I : Type*} [Finite I] [DecidableEq I]

def cube (I : Type*) : Set (I → ℝ) := {x | ∀ i, 0 ≤ x i ∧ x i ≤ 1}

def cubeGraph (f : (I → ℝ) → ℝ) : Set ((I → ℝ) × ℝ) :=
  {p | p.1 ∈ cube I ∧ p.2 = f p.1}

def SeparatelyAffine (f : (I → ℝ) → ℝ) : Prop :=
  ∀ (x : I → ℝ) (i : I) (t : ℝ),
    f (Function.update x i t) =
      (1 - t) * f (Function.update x i 0) + t * f (Function.update x i 1)

/-- Eliminate the possibly fractional coordinates one at a time. -/
theorem graph_mem_vertex_hull (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) (hx : x ∈ cube I) :
    (x, f x) ∈ convexHull ℝ (vertexGraph f) := by
  let := Fintype.ofFinite I
  have aux : ∀ (s : Finset I) (y : I → ℝ), y ∈ cube I →
      (∀ i, i ∉ s → y i = 0 ∨ y i = 1) →
      (y, f y) ∈ convexHull ℝ (vertexGraph f) := by
    intro s
    induction s using Finset.induction_on with
    | empty =>
      intro y _ hy
      have heq : vertexPoint (fun i => decide (y i = 1)) = y := by
        funext i
        rcases hy i (by simp) with h | h <;> simp [vertexPoint, h]
      apply subset_convexHull
      exact ⟨fun i => decide (y i = 1), by simp only [heq]⟩
    | @insert i s hi ih =>
      intro y hy hbinary
      have h0 : Function.update y i 0 ∈ cube I := by
        intro j
        by_cases hji : j = i
        · subst j; simp
        · simpa [Function.update_of_ne hji] using hy j
      have h1 : Function.update y i 1 ∈ cube I := by
        intro j
        by_cases hji : j = i
        · subst j; simp
        · simpa [Function.update_of_ne hji] using hy j
      have hb0 : ∀ j, j ∉ s → Function.update y i 0 j = 0 ∨
          Function.update y i 0 j = 1 := by
        intro j hj
        by_cases hji : j = i
        · subst j; simp
        · simpa [Function.update_of_ne hji] using
            hbinary j (by simp [hj, hji])
      have hb1 : ∀ j, j ∉ s → Function.update y i 1 j = 0 ∨
          Function.update y i 1 j = 1 := by
        intro j hj
        by_cases hji : j = i
        · subst j; simp
        · simpa [Function.update_of_ne hji] using
            hbinary j (by simp [hj, hji])
      have hcomb := (convex_convexHull ℝ (vertexGraph f)) (ih _ h0 hb0) (ih _ h1 hb1)
        (sub_nonneg.mpr (hy i).2) (hy i).1 (by ring : (1 - y i) + y i = 1)
      have heq : (1 - y i) • (Function.update y i 0, f (Function.update y i 0)) +
          y i • (Function.update y i 1, f (Function.update y i 1)) = (y, f y) := by
        apply Prod.ext
        · ext j
          by_cases hji : j = i
          · subst j; simp
          · simp [Function.update_of_ne hji]
            ring
        · have h := hf y i (y i)
          simpa using h.symm
      rwa [heq] at hcomb
  exact aux Finset.univ x hx (by simp)

/-- The continuous graph introduces no new points beyond convex combinations of
binary graph points. This is the finite-law bridge used for envelope certificates. -/
theorem cubeGraph_hull_eq_vertexGraph_hull (f : (I → ℝ) → ℝ)
    (hf : SeparatelyAffine f) :
    convexHull ℝ (cubeGraph f) = convexHull ℝ (vertexGraph f) := by
  apply Set.Subset.antisymm
  · apply convexHull_min _ (convex_convexHull ℝ _)
    rintro ⟨x, z⟩ ⟨hx, hz⟩
    change z = f x at hz
    rw [hz]
    exact graph_mem_vertex_hull f hf x hx
  · apply convexHull_mono
    rintro _ ⟨v, rfl⟩
    refine ⟨?_, rfl⟩
    intro i
    simp only [vertexPoint]
    split <;> norm_num

/-- Exact law characterization of every point in the original continuous graph hull. -/
theorem mem_cubeGraph_hull_iff [Fintype I] (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) (z : ℝ) :
    (x, z) ∈ convexHull ℝ (cubeGraph f) ↔
      ∃ μ : Law (Vertex I), (∀ i, μ.expect (fun v => vertexPoint v i) = x i) ∧
        μ.expect (fun v => f (vertexPoint v)) = z := by
  rw [cubeGraph_hull_eq_vertexGraph_hull f hf]
  exact mem_vertexGraph_hull_iff f x z

end CubicGap
