import Formal.CubicGap.Hull
import Formal.CubicGap.Expectation

namespace CubicGap

variable {I : Type*} [Fintype I] [DecidableEq I]

/-- The vertical slice of the actual cube graph's convex hull. -/
def envelopeValues (f : (I → ℝ) → ℝ) (x : I → ℝ) : Set ℝ :=
  {z | (x, z) ∈ convexHull ℝ (cubeGraph f)}

/-- The vertical width of the original continuous graph hull. -/
noncomputable def hullGap {I : Type*} [Fintype I] [DecidableEq I]
    (f : (I → ℝ) → ℝ) (x : I → ℝ) : ℝ :=
  sSup (envelopeValues f x) - sInf (envelopeValues f x)

def HasMeans (μ : Law (Vertex I)) (x : I → ℝ) : Prop :=
  ∀ i, μ.expect (fun v => vertexPoint v i) = x i

/-- A universal lower bound and an attaining law give an exact convex envelope. -/
theorem minimum_from_laws (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) (q : ℝ)
    (hlower : ∀ μ : Law (Vertex I), HasMeans μ x →
      q ≤ μ.expect (fun v => f (vertexPoint v)))
    (hattain : ∃ μ : Law (Vertex I), HasMeans μ x ∧
      μ.expect (fun v => f (vertexPoint v)) = q) :
    IsLeast (envelopeValues f x) q := by
  refine ⟨(mem_cubeGraph_hull_iff f hf x q).mpr hattain, ?_⟩
  intro z hz
  obtain ⟨μ, hmean, hobj⟩ := (mem_cubeGraph_hull_iff f hf x z).mp hz
  rw [← hobj]
  exact hlower μ hmean

/-- A universal upper bound and an attaining law give an exact concave envelope. -/
theorem maximum_from_laws (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) (q : ℝ)
    (hupper : ∀ μ : Law (Vertex I), HasMeans μ x →
      μ.expect (fun v => f (vertexPoint v)) ≤ q)
    (hattain : ∃ μ : Law (Vertex I), HasMeans μ x ∧
      μ.expect (fun v => f (vertexPoint v)) = q) :
    IsGreatest (envelopeValues f x) q := by
  refine ⟨(mem_cubeGraph_hull_iff f hf x q).mpr hattain, ?_⟩
  intro z hz
  obtain ⟨μ, hmean, hobj⟩ := (mem_cubeGraph_hull_iff f hf x z).mp hz
  rw [← hobj]
  exact hupper μ hmean

end CubicGap
