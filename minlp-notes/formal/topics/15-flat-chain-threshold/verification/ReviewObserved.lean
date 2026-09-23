import Formal.NetworkSimplex.ThresholdObservedSeparation
import Formal.NetworkSimplex.ThresholdObservedRecovery

namespace ThresholdObservedReview
open NetworkSimplex.Chain.Threshold

def input (residual : ℚ) : RationalData 1 0 where
  c i := Fin.elim0 i
  u i := Fin.elim0 i
  v i := Fin.elim0 i
  weights := ![residual, 0]
  xa i := Fin.elim0 i
  xh := 1
  observedH := fun j => j == 1
  zh := fun _ => 0

def labels : List (Fin 1) := [0, 0]

example : (observedMembership (input 1) labels (generalLibrary labels.toFinset.card)).1 = true := by
  decide +kernel
example : (observedSeparate (input 1) labels (generalLibrary labels.toFinset.card)).1 = none := by
  decide +kernel
example : (observedSeparate (input 0) labels (generalLibrary labels.toFinset.card)).1.isSome =
    true := by
  decide +kernel
example : (observedWitness (input 1) labels (packedBasisLibrary labels.toFinset.card)).1.isSome =
    true := by
  decide +kernel

end ThresholdObservedReview
