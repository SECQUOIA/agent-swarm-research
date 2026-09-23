import Formal.DAGSpectral.TopologicalMaterializeCost
open DAGSpectral
def s : Fin 2 → Fin 3 := ![2,1]
def t : Fin 2 → Fin 3 := ![1,0]
theorem ac : RawAcyclic s t := rawAcyclic_of_rank s t (fun x => 2-x.val) (by
  intro e
  fin_cases e <;> decide)
def assertTrue (b : Bool) (s : String) : IO Unit := unless b do throw (IO.userError s)
#eval do
  let xs := topologicalList s t
  assertTrue (decide (xs = [2,1,0])) "reverse-numbered raw graph"
  let scan := topologicalEndpointScan xs s t [0,1]
  assertTrue (decide (scan.1 = [(0,1),(1,2)])) "preserved edge identity"
  assertTrue (decide (scan.2 ≤ 2*(2*(3+1)+1)+1)) "scan-work bound"
  let graph := materializedTopologicalGraph s t ac
  assertTrue (decide (graph.src 0 = 0 ∧ graph.dst 0 = 1 ∧ graph.src 1 = 1 ∧ graph.dst 1 = 2)) "materialized endpoint cache"
  assertTrue (decide (topologicalIndexScan (2 : Fin 3) [0,1] = (2,3))) "missing-index length boundary"
  assertTrue (decide (topologicalIndexScan (1 : Fin 3) [1,1] = (0,1))) "first occurrence"
  assertTrue (decide (topologicalEndpointScan xs s t [] = ([],1))) "empty edges"
  IO.println "topological materialization checks passed"
#print axioms DAGSpectral.materializedTopologicalGraph_eq
#print axioms DAGSpectral.topological_materialization_scan_bound
