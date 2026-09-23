import Formal.NetworkSimplex.SimplexEncoding

/-! On the full-weight face, the unobserved residual state is identically zero. -/
namespace NetworkSimplex
open scoped BigOperators

/-- The original simplex-inequality hull on its sum-one face equals the full-weight hull.
This explicitly adds and removes the zero residual state, rather than observing it. -/
theorem original_hull_iff_full_of_sum_one {E V O : Type*} {m : ℕ}
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (label : O → Fin m) (p : OriginalPoint E O m)
    (hs : ∑ j, p.2.1 j = 1) :
    p ∈ convexHull ℝ (OriginalGraph A b u arc label) ↔
      p ∈ convexHull ℝ (Graph A b u arc label) := by
  rw [original_mem_hull_iff, mem_convexHull_graph_iff]
  constructor
  · rintro ⟨hp, f, hf, hsum, hobs⟩
    have hzero : f 0 = 0 := (flow_zero_iff A b u _).mp (by
      simpa [residualWeights, hs] using hf 0)
    refine ⟨⟨hp.1, hs⟩, fun j => f j.succ, fun j => hf j.succ, ?_, hobs⟩
    rw [Fin.sum_univ_succ, hzero, zero_add] at hsum
    exact hsum
  · rintro ⟨hp, f, hf, hsum, hobs⟩
    refine ⟨⟨hp.1, hs.le⟩, Fin.cons 0 f, ?_, ?_, ?_⟩
    · intro j
      refine Fin.cases ?_ (fun i => hf i) j
      simp only [Fin.cons_zero, residualWeights, hs, sub_self]
      exact (flow_zero_iff A b u 0).mpr rfl
    · simpa [Fin.sum_univ_succ] using hsum
    · exact hobs

end NetworkSimplex
