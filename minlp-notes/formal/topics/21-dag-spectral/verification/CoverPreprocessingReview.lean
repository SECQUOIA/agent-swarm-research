import Formal.DAGSpectral.CoverCacheCost
import Formal.DAGSpectral.CoverIndependenceExecution
import Formal.DAGSpectral.CriterionSelectWeighted

open DAGSpectral DAGSpectral.CoverNormalizationExecution
open Matrix

def v : Matrix (Fin 2) (Fin 1) ℚ := !![2; 0]
def a : Matrix (Fin 2) (Fin 2) ℚ := !![3, 0; 0, 0]
def tau : Fin 1 → ℚ := ![2]
def assertTrue (b : Bool) (s : String) : IO Unit := unless b do throw (IO.userError s)

#eval do
  let n := normalizeRun v tau a
  assertTrue (decide (n.transform.value = !![1, 0])) "cached transform"
  assertTrue (decide (n.restore.value = !![1; 0])) "cached restore"
  assertTrue (decide (n.atom.value = !![3])) "cached congruence"
  assertTrue (decide (n.events = NormalizationBits.normalizationTrace v tau a)) "whole normalization trace"
  assertTrue (independenceRun v).independent "rectangular independent columns"
  assertTrue (!(independenceRun (!![1, 1; 0, 0] : Matrix (Fin 2) (Fin 2) ℚ)).independent) "dependent columns"
  assertTrue (independenceRun (fun (_ : Fin 2) (i : Fin 0) => Fin.elim0 i)).independent "rank zero determinant"
  assertTrue (!(atomRun v tau !![0, 0; 0, 1]).accepted) "range rejection"
  assertTrue (atomRun v tau !![8, 0; 0, 0]).accepted "closed magnitude boundary"
  assertTrue (!(atomRun v tau !![9, 0; 0, 0]).accepted) "magnitude rejection"
  let labels := labelRun (!![1, -1/3; -1/3, 1] : Matrix (Fin 2) (Fin 2) ℚ) (1/2)
  assertTrue (decide ((labels.floors.get 0).get 1 = -1)) "negative floor"
  assertTrue (decide ((labels.floors.get 0).get 0 = 2)) "exact floor boundary"
  assertTrue (decide (labels.quotients.events.length = 4)) "all square entries charged"
  let scales := scalesRun (![1/64] : Fin 1 → ℚ)
  assertTrue (decide ((scales.get 0).1 = 8)) "executed dyadic scale"
  let atoms : Option (Fin 1) → Matrix (Fin 2) (Fin 2) ℚ := fun _ => a
  let cache := trialRun v tau atoms (1/2)
  assertTrue (decide ((((cache.labels.get 0).floors.get 0).get 0) = 6)) "cached atom to labels"
  IO.println "preprocessing boundary checks passed"

#eval do
  assertTrue (decide (rationalWeightedTerm 0 none = some 0)) "zero times infinity"
  assertTrue (decide (rationalWeightedTerm 2 (some (-3)) = some 0)) "finite negative clipping"
  assertTrue (decide (rationalWeightedList [(0,none),(2,some (-3)),(3,some 4)] = some 12)) "weighted aggregation"
  assertTrue (decide (rationalWeightedList [(1,none),(0,some 4)] = none)) "positive infinite term"
  assertTrue (decide (rationalWeightedList [] = some 0)) "empty weighted family"
  let cs : Fin 2 → Fin 2 → ℚ := ![![1,0],![0,1]]
  let ws : Fin 2 → ℚ := ![2,0]
  let A : Matrix (Fin 2) (Fin 2) ℚ := !![2,0;0,0]
  assertTrue (decide (rationalWeightedContrastCost A cs ws = some 1)) "singular matrix with zero unsupported weight"
  assertTrue (decide (rationalWeightedContrastCost A cs (![2,1] : Fin 2 → ℚ) = none)) "positive unsupported contrast"
  let J : Fin 2 → Matrix (Fin 2) (Fin 2) ℚ := ![A, !![4,0;0,0]]
  assertTrue (decide (selectWeightedContrast J cs ws [0,1] = some 1)) "actual weighted selector minimizes"
  assertTrue (decide (selectWeightedContrast J cs ws [] = none)) "empty selection"
  IO.println "weighted criterion boundary checks passed"

#print axioms DAGSpectral.CoverNormalizationExecution.normalizeRun_events
#print axioms DAGSpectral.CoverNormalizationExecution.atomRun_accepted_iff
#print axioms DAGSpectral.CoverNormalizationExecution.trialRun_labels
#print axioms DAGSpectral.CoverNormalizationExecution.independenceRun_value
#print axioms DAGSpectral.rationalWeightedContrastCost_value
#print axioms DAGSpectral.IsRelativeCover.selectWeightedContrast_guarantee
