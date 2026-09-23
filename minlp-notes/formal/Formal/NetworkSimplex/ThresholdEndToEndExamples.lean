import Formal.NetworkSimplex.ThresholdPositiveAtoms
import Formal.NetworkSimplex.ThresholdSeparation
import Formal.NetworkSimplex.ThresholdOnePacked

/-! Kernel-checked boundary executions through the original-domain and witness interfaces. -/
namespace NetworkSimplex.Chain.Threshold.EndToEndExamples

def zeroWeightState : RationalData 1 1 where
  c := fun _ _ => .neither
  u := fun _ _ => 0
  v := fun _ _ => 0
  weights := ![1, 0]
  xa := fun _ => 1 / 3
  xh := 1 / 2
  observedH := fun _ => false
  zh := fun _ => 0

example : zeroWeightState.domainRun.1 = true := by decide +kernel
example : (oneOracle zeroWeightState).1 = none := by decide +kernel
example : (membershipRun zeroWeightState (generalLibrary 1)).1 = true := by decide +kernel
example : (checkedWitness zeroWeightState (packedBasisLibrary 1)).1.isSome = true := by
  decide +kernel
example : positiveStates zeroWeightState = [0] := by decide +kernel

/-- A profile can be feasible even when the original weights fail normalization. -/
def badSimplex : RationalData 1 1 :=
  { zeroWeightState with weights := ![1, 1] }

example : (oneOracle badSimplex).1 = none := by decide +kernel
example : badSimplex.domainRun.1 = false := by decide +kernel
example : (membershipRun badSimplex (generalLibrary 1)).1 = false := by decide +kernel
example : (checkedWitness badSimplex (packedBasisLibrary 1)).1 = none := by decide +kernel

example : (separateGeneral zeroWeightState (generalLibrary 1)).1 = none := by decide +kernel
example : ((separateGeneral badSimplex (generalLibrary 1)).1.map
    (fun cut => match cut with | .inl _ => true | .inr _ => false)) = some true := by
  decide +kernel

end NetworkSimplex.Chain.Threshold.EndToEndExamples
