import Formal.NetworkSimplex.Disaggregation

/-! Adding unused zero-weight states and relabeling the simplex states. -/
namespace NetworkSimplex
open scoped BigOperators

/-- Add states with zero weight while preserving every flow and product coordinate. -/
def zeroExtendPoint {E J O Z : Type*} (p : Point E J O) : Point E (J ⊕ Z) O :=
  (p.1, (Sum.elim p.2.1 (fun _ => 0), p.2.2))

/-- Zero-weight states contribute exactly zero flows, so this embedding preserves
and reflects membership in the full-weight graph hull. -/
theorem zeroExtend_mem_hull_iff {E V J O Z : Type*} [Fintype J] [Fintype Z]
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (state : O → J) (p : Point E J O) :
    zeroExtendPoint (Z := Z) p ∈ convexHull ℝ (Graph A b u arc (Sum.inl ∘ state)) ↔
      p ∈ convexHull ℝ (Graph A b u arc state) := by
  rw [mem_convexHull_graph_iff, mem_convexHull_graph_iff]
  constructor
  · rintro ⟨hp, f, hf, hsum, hobs⟩
    have hz : ∀ z, f (Sum.inr z) = 0 := fun z =>
      (flow_zero_iff A b u _).mp (hf (Sum.inr z))
    refine ⟨⟨fun j => hp.1 (Sum.inl j), ?_⟩, fun j => f (Sum.inl j),
      fun j => hf (Sum.inl j), ?_, hobs⟩
    · simpa [zeroExtendPoint, Fintype.sum_sum_type] using hp.2
    · simpa [zeroExtendPoint, Fintype.sum_sum_type, hz] using hsum
  · rintro ⟨hp, f, hf, hsum, hobs⟩
    refine ⟨⟨?_, ?_⟩, Sum.elim f (fun _ => 0), ?_, ?_, hobs⟩
    · intro j
      cases j with
      | inl j => exact hp.1 j
      | inr z => exact le_rfl
    · simpa [zeroExtendPoint, Fintype.sum_sum_type] using hp.2
    · intro j
      cases j with
      | inl j => exact hf j
      | inr z => exact (flow_zero_iff A b u 0).mpr rfl
    · simpa [zeroExtendPoint, Fintype.sum_sum_type] using hsum

/-- Relabel only the simplex-weight coordinates. -/
def relabelPoint {E J K O : Type*} (e : J ≃ K) (p : Point E J O) : Point E K O :=
  (p.1, (fun k => p.2.1 (e.symm k), p.2.2))

/-- Graph-hull membership is invariant under any bijective state relabeling. -/
theorem relabel_mem_hull_iff {E V J K O : Type*} [Fintype J] [Fintype K]
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (state : O → J) (e : J ≃ K) (p : Point E J O) :
    relabelPoint e p ∈ convexHull ℝ (Graph A b u arc (e ∘ state)) ↔
      p ∈ convexHull ℝ (Graph A b u arc state) := by
  rw [mem_convexHull_graph_iff, mem_convexHull_graph_iff]
  constructor
  · rintro ⟨hp, f, hf, hsum, hobs⟩
    refine ⟨⟨?_, ?_⟩, fun j => f (e j), ?_, ?_, hobs⟩
    · intro j
      simpa [relabelPoint] using hp.1 (e j)
    · simpa [relabelPoint, Equiv.sum_comp] using hp.2
    · intro j
      simpa [relabelPoint] using hf (e j)
    · simpa [relabelPoint, Equiv.sum_comp] using hsum
  · rintro ⟨hp, f, hf, hsum, hobs⟩
    refine ⟨⟨fun k => hp.1 (e.symm k), ?_⟩, fun k => f (e.symm k),
      fun k => hf (e.symm k), ?_, ?_⟩
    · simpa [relabelPoint, Equiv.sum_comp] using hp.2
    · simpa [relabelPoint, Equiv.sum_comp] using hsum
    · simpa only [relabelPoint, Function.comp_apply, Equiv.symm_apply_apply] using hobs

/-- The canonical extension from `m` states to `m + k` states. -/
def finZeroExtendPoint {E O : Type*} {m : ℕ} (k : ℕ) (p : Point E (Fin m) O) :
    Point E (Fin (m + k)) O :=
  relabelPoint finSumFinEquiv (zeroExtendPoint (Z := Fin k) p)

/-- Extra unused labels can be added in the standard `Fin` indexing without
altering any original coordinate or its hull-membership decision. -/
theorem finZeroExtend_mem_hull_iff {E V O : Type*} {m : ℕ} (k : ℕ)
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (state : O → Fin m) (p : Point E (Fin m) O) :
    finZeroExtendPoint k p ∈ convexHull ℝ
      (Graph A b u arc (finSumFinEquiv ∘ Sum.inl ∘ state)) ↔
      p ∈ convexHull ℝ (Graph A b u arc state) := by
  unfold finZeroExtendPoint
  rw [relabel_mem_hull_iff, zeroExtend_mem_hull_iff]

end NetworkSimplex
