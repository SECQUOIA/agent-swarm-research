import Formal.DAGSpectral.CacheStorageExecution
open DAGSpectral DAGSpectral.CoverNormalizationExecution
def assertTrue (b : Bool) (s : String) : IO Unit := unless b do throw (IO.userError s)
#eval do
  let E : Fin 1 → Fin 1 → ArithmeticExpr := fun _ _ => .atom (3/2)
  let M := runMatrix E
  assertTrue (decide (M.copies = 18)) "two actual rational materializations"
  let E0 : Fin 0 → Fin 2 → ArithmeticExpr := fun i _ => Fin.elim0 i
  assertTrue (decide ((runMatrix E0).copies = 6)) "empty-row vector control"
  let L := labelRun (!![-1/3] : Matrix (Fin 1) (Fin 1) ℚ) (1/2)
  assertTrue (decide (L.copies = 24)) "negative-floor stored quotient and signed integer"
  let V : Matrix (Fin 2) (Fin 1) ℚ := !![2;0]
  let tau : Fin 1 → ℚ := ![2]
  let A : Matrix (Fin 2) (Fin 2) ℚ := !![3,0;0,0]
  let N := normalizeRun V tau A
  let atom := atomRun V tau A
  let PA := mulRun N.projector.value A
  assertTrue (decide (atom.copies = N.copies + PA.copies + 21)) "range and boolean-storage composition"
  let atoms : Option (Fin 1) → Matrix (Fin 2) (Fin 2) ℚ := fun _ => A
  let trial := trialRun V tau atoms (1/2)
  assertTrue (decide (trial.copies = trial.prior.copies + (trial.atoms.get 0).copies +
    (trial.labels.get 0).copies + 5)) "trial consumes child counters"
  assertTrue (decide (trial.copies > trial.prior.copies)) "edge cache included"
  IO.println "cache-storage checks passed"
#print axioms DAGSpectral.CoverNormalizationExecution.trialRun_copies_le
#print axioms DAGSpectral.CoverNormalizationExecution.trialStorageBudget_scale
