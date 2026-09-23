import Formal.NetworkSimplex.ThresholdSeparation
import Formal.NetworkSimplex.ThresholdPositiveAtoms
import Formal.NetworkSimplex.ThresholdOnePacked
import Formal.NetworkSimplex.ThresholdTwoPacked
import Formal.NetworkSimplex.ThresholdObservedCache
import Formal.NetworkSimplex.ThresholdObservedRecovery

namespace ThresholdAlgorithmReview
open NetworkSimplex.Chain.Threshold

def zeroDim (w : ℚ) : RationalData 0 0 where
  c i := Fin.elim0 i
  u i := Fin.elim0 i
  v i := Fin.elim0 i
  weights := fun _ => w
  xa i := Fin.elim0 i
  xh := 1
  observedH := fun _ => false
  zh := fun _ => 0

-- Zero-dimensional recovery includes the empty active basis.
example : (checkedWitness (zeroDim 1) (packedBasisLibrary 0)).1.isSome = true := by
  decide +kernel

-- An invalid original residual weight cannot pass the domain stage.
example : ((zeroDim 0).domainSeparator).1.isSome = true := by decide +kernel
example : (checkedWitness (zeroDim 0) (packedBasisLibrary 0)).1 = none := by
  decide +kernel

def zeroWeight : RationalData 1 0 where
  c i := Fin.elim0 i
  u i := Fin.elim0 i
  v i := Fin.elim0 i
  weights := ![1, 0]
  xa i := Fin.elim0 i
  xh := 1
  observedH := fun _ => false
  zh := fun _ => 0

example : positiveStates zeroWeight = [0] := by decide +kernel
example : (checkedWitness zeroWeight (packedBasisLibrary 1)).1.isSome = true := by
  decide +kernel

def observedZeroWeight : RationalData 1 0 :=
  { zeroWeight with observedH := fun j => j == 1 }

-- Duplicate observation labels are indexed once, including a zero-weight label.
example : (observedZeroWeight.observedCache [0, 0]).labels.toList = [0] := by
  decide +kernel
example : (observedZeroWeight.observedCache [0, 0]).data.weights 1 = 0 ∧
    (observedZeroWeight.observedCache [0, 0]).data.observedH 1 = true := by
  decide +kernel

-- Compression creates residual mass one, but cannot repair an invalid original simplex.
example : (observedMembership (zeroDim 0) [] (generalLibrary 0)).1 = false := by
  decide +kernel
example : (observedWitness (zeroDim 0) [] (packedBasisLibrary 0)).1 = none := by
  decide +kernel
end ThresholdAlgorithmReview
