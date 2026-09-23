import Formal.DAGSpectral.TopologicalPath
import Formal.DAGSpectral.RawHeadline

open DAGSpectral

private def src : Fin 2 → Fin 3 := ![2, 0]
private def dst : Fin 2 → Fin 3 := ![0, 1]

private theorem acyclic : RawAcyclic src dst := by
  apply rawAcyclic_of_rank src dst ![1, 2, 0]
  intro e
  fin_cases e <;> decide

-- The input labels are not themselves a topological order.
example : topologicalList src dst = [2, 0, 1] := by decide
example : (kahnOrderCounted src dst 3 Finset.univ).2 = 18 := by decide
example : RawPath src dst 2 1 [0, 1] := by
  have h₀ : RawPath src dst 2 0 [0] := RawPath.snoc RawPath.nil 0 rfl
  exact RawPath.snoc h₀ 1 rfl
example : (topologicallyOrderedGraph src dst acyclic).Path
    (topologicalOrder src dst acyclic 2) (topologicalOrder src dst acyclic 1) [0, 1] := by
  apply RawPath.toOrdered acyclic
  have h₀ : RawPath src dst 2 0 [0] := RawPath.snoc RawPath.nil 0 rfl
  exact RawPath.snoc h₀ 1 rfl

-- A self-loop has no ready vertex; no false complete ordering is produced.
example : topologicalList (fun _ : Fin 1 => (0 : Fin 1)) (fun _ => 0) = [] := by decide
-- Isolated vertices are included; an empty edge array entails zero edge tests.
example : topologicalList (fun e : Fin 0 => e.elim0 : Fin 0 → Fin 3)
    (fun e : Fin 0 => e.elim0) = [0, 1, 2] := by decide
example : (kahnOrderCounted (fun e : Fin 0 => e.elim0 : Fin 0 → Fin 3)
    (fun e : Fin 0 => e.elim0) 3 Finset.univ).2 = 0 := by decide
example : topologicalList (fun e : Fin 0 => e.elim0 : Fin 0 → Fin 0)
    (fun e : Fin 0 => e.elim0) = [] := by decide

#print axioms DAGSpectral.kahnOrder_spec
#print axioms DAGSpectral.topologicalOrder
#print axioms DAGSpectral.checkDAGWithTopologicalOrder
#print axioms DAGSpectral.incomingScan_spec
#print axioms DAGSpectral.readyVerticesCounted_spec
#print axioms DAGSpectral.kahnOrderCounted_order
#print axioms DAGSpectral.topologicalSort_scan_bound
#print axioms DAGSpectral.rawPath_iff_ordered
#print axioms DAGSpectral.rawPath_length_bound
#print axioms DAGSpectral.rawPath_nodup

#eval topologicalList src dst
#eval (topologicalOrder src dst acyclic) 2
#eval (topologicalOrder src dst acyclic).symm 0
#eval (kahnOrderCounted src dst 3 Finset.univ).2

#print axioms DAGSpectral.mem_rawFeasiblePaths
#print axioms DAGSpectral.rawDagSpectralCover_isRelativeCover
#print axioms DAGSpectral.rawDagSpectralCover_empty_iff
#print axioms DAGSpectral.rawDagSpectralCover_kernel
#print axioms DAGSpectral.rawDagSpectralCover_card
