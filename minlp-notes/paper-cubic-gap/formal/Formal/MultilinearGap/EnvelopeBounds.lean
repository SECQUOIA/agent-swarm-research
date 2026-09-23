import Formal.CubicGap.Envelope
import Formal.CubicGap.Polynomial

namespace MultilinearGap

open CubicGap

noncomputable section

variable {I : Type*} [Fintype I] [DecidableEq I]

/-- The term-by-term gap uses the actual envelope width of every distinct
squarefree monomial, all with coefficient one. -/
def termwiseGap (supports : Finset (Finset I)) (x : I → ℝ) : ℝ :=
  ∑ s ∈ supports, hullGap (monomial s) x

/-- Convert a bound for every admissible binary law into a bound for the
width of the original continuous graph hull. -/
theorem hullGap_le_of_laws (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) (U B : ℝ)
    (hmax : IsGreatest (envelopeValues f x) U)
    (hlower : ∀ μ : Law (Vertex I), HasMeans μ x →
      U - B ≤ μ.expect (fun v => f (vertexPoint v))) :
    hullGap f x ≤ B := by
  have hbound : ∀ z ∈ envelopeValues f x, U - B ≤ z := by
    intro z hz
    obtain ⟨μ, hmean, hvalue⟩ := (mem_cubeGraph_hull_iff f hf x z).mp hz
    rw [← hvalue]
    exact hlower μ hmean
  have hinf : U - B ≤ sInf (envelopeValues f x) :=
    le_csInf ⟨U, hmax.1⟩ hbound
  rw [hullGap, hmax.csSup_eq]
  linarith

/-- A strict gap between an original graph value and an attained upper
envelope proves that the denominator of the gap ratio is positive. -/
theorem hullGap_pos_of_graph_lt (f : (I → ℝ) → ℝ) (x : I → ℝ)
    (hx : x ∈ cube I) (U : ℝ)
    (hmax : IsGreatest (envelopeValues f x) U)
    (hbounded : BddBelow (envelopeValues f x)) (hstrict : f x < U) :
    0 < hullGap f x := by
  have hgraph : f x ∈ envelopeValues f x :=
    subset_convexHull ℝ _ ⟨hx, rfl⟩
  have hinf := csInf_le hbounded hgraph
  rw [hullGap, hmax.csSup_eq]
  linarith

end
end MultilinearGap
