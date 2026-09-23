import Formal.NetworkSimplex.ThresholdMerge

/-! A compact normalized-flow decomposition expands to the original global states. -/
namespace NetworkSimplex
open scoped BigOperators
noncomputable section
variable {E V O K T : Type*} [Fintype K] [Fintype T] [DecidableEq K] [DecidableEq T]

def vertexAtom (arc : O → E) (state : O → K) (flow : E → ℝ) (k : K) : Point E K O :=
  (flow, (fun j => if j = k then 1 else 0,
    fun o => flow (arc o) * (if state o = k then 1 else 0)))

theorem vertexAtom_mem (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (state : O → K) (flow : E → ℝ)
    (hf : Flow A b u 1 flow) (k : K) : vertexAtom arc state flow k ∈ Graph A b u arc state := by
  refine ⟨⟨?_, ?_⟩, hf, fun _ => rfl⟩
  · intro j; simp [vertexAtom]; split_ifs <;> norm_num
  · simp [vertexAtom]

theorem weighted_vertexAtom_flow (arc : O → E) (state : O → K)
    (w : K → ℝ) (flow : K → E → ℝ) :
    (∑ k, w k • vertexAtom arc state (flow k) k).1 = ∑ k, w k • flow k := by
  simp only [Prod.fst_sum, Prod.smul_fst, vertexAtom]

theorem weighted_vertexAtom_product (arc : O → E) (state : O → K)
    (w : K → ℝ) (flow : K → E → ℝ) (o : O) :
    (∑ k, w k • vertexAtom arc state (flow k) k).2.2 o =
      w (state o) * flow (state o) (arc o) := by
  simp only [Prod.snd_sum, Prod.smul_snd, Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
  simp [vertexAtom, mul_ite]

/-- Store one normalized flow per merged state and the original weight vector.
At expansion each original state merely references its group's stored flow.
No division occurs, so zero weights require no exceptional arithmetic. -/
theorem compact_vertex_refinement (A : (E → ℝ) →ₗ[ℝ] (V → ℝ))
    (b : V → ℝ) (u : E → ℝ) (arc : O → E) (state : O → K)
    (g : K → T) (p : Point E K O) (flow : T → E → ℝ)
    (hf : ∀ t, Flow A b u 1 (flow t))
    (ho : ∀ o k, g k = g (state o) → k = state o)
    (hs : ∑ t, groupSum g p.2.1 t • vertexAtom arc (g ∘ state) (flow t) t = mergedPoint g p) :
    (∀ k, vertexAtom arc state (flow (g k)) k ∈ Graph A b u arc state) ∧
      ∑ k, p.2.1 k • vertexAtom arc state (flow (g k)) k = p := by
  constructor
  · intro k; exact vertexAtom_mem A b u arc state _ (hf (g k)) k
  · apply Prod.ext
    · rw [weighted_vertexAtom_flow]
      have hh := congrArg Prod.fst hs
      rw [weighted_vertexAtom_flow] at hh
      change (∑ k, p.2.1 k • flow (g k)) = p.1
      change (∑ k, groupSum g p.2.1 k • flow k) = p.1 at hh
      rw [← hh]
      simp only [groupSum, Finset.sum_smul]
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro k _
      simp [ite_smul]
    · apply Prod.ext
      · funext k
        simp only [Prod.snd_sum, Prod.fst_sum, Prod.smul_snd, Prod.smul_fst,
          Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
        simp [vertexAtom, mul_ite]
      · funext o
        rw [weighted_vertexAtom_product]
        have hh := congrArg (fun q : Point E T O => q.2.2 o) hs
        rw [weighted_vertexAtom_product] at hh
        simp only [Function.comp_apply] at hh
        rw [groupSum_singleton g p.2.1 (state o) (ho o)] at hh
        exact hh

end
end NetworkSimplex
