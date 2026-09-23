import Formal.DAGSpectral.CriterionSelectWeightedPath
open DAGSpectral
def assertTrue (b : Bool) (s : String) : IO Unit := unless b do throw (IO.userError s)
#eval do
  let xs : List (ℚ × Option ℚ) := [(0,none),(2,some (-3)),(3,some 4)]
  let run := rationalWeightedListWithTrace xs
  assertTrue (decide (run.1 = some 12)) "actual mixed fold"
  assertTrue (decide (run.2.length ≤ 7*xs.length)) "fold length"
  assertTrue (decide ((rationalWeightedTermWithTrace 0 none).2.length = 2)) "zero check charge"
  assertTrue (decide ((rationalCostLERun (some (-7)) (some (-2))).1 = true)) "cached clipping comparator"
  let cs : Fin 2 → Fin 2 → ℚ := ![![1,0],![0,1]]
  let ws : Fin 2 → ℚ := ![2,0]
  let A : Matrix (Fin 2) (Fin 2) ℚ := !![2,0;0,0]
  let D : Matrix (Fin 2) (Fin 2) ℚ := !![4,0;0,0]
  let cost := rationalWeightedContrastCostWithTrace A cs ws
  assertTrue (decide (cost.1 = some 1)) "traced singular cost"
  assertTrue (decide (cost.2.length ≤ 2*(contrastOperations 2+7))) "traced contrast length"
  let J : Fin 2 → Matrix (Fin 2) (Fin 2) ℚ := ![A,D]
  let selected := selectWeightedContrastRun J cs ws [0,1]
  assertTrue (decide (selected.1 = some 1)) "traced weighted minimizer"
  assertTrue (decide (selected.2 = (weightedContrastCostLERun D A cs ws).2)) "scan uses actual comparator trace"
  assertTrue (decide ((selectWeightedContrastRun J cs ws []).2 = [])) "empty scan events"
  assertTrue (decide ((selectWeightedContrastRun J cs ws [0]).2 = [])) "singleton scan events"
  let cs0 : Fin 0 → Fin 2 → ℚ := fun i => Fin.elim0 i
  let ws0 : Fin 0 → ℚ := fun i => Fin.elim0 i
  assertTrue (decide ((rationalWeightedContrastCostWithTrace A cs0 ws0) = (some 0,[]))) "zero contrast count"
  let Q : Fin 2 → Matrix (Fin 2) (Fin 2) ℚ := ![A,D]
  let selectedPaths := selectPathsRun (0 : Matrix (Fin 2) (Fin 2) ℚ) Q
    (fun a b => weightedContrastCostLERun b a cs ws) [[0],[1]]
  assertTrue (decide (selectedPaths.1 = some [1])) "actual raw-path weighted selection"
  assertTrue (decide (selectedPaths.2.length = 16 + selected.2.length)) "path sums included in trace"
  IO.println "weighted execution checks passed"
#print axioms DAGSpectral.selectWeightedContrastRun_result
#print axioms DAGSpectral.selectWeightedContrastRun_polynomial_bitWork
#print axioms DAGSpectral.selectPathsRun_weightedContrast_polynomial_bitWork
