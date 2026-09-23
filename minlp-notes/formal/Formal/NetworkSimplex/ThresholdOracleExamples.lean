import Formal.NetworkSimplex.ThresholdThreePacked

/-! Kernel-checked executions: missing groups, a genuine circuit rejection, and
a violated zero-normal original row. -/
namespace NetworkSimplex.Chain.Threshold.Examples

def noGadgets (xh : ℚ) : RationalData 3 0 where
  c i := Fin.elim0 i
  u i := Fin.elim0 i
  v i := Fin.elim0 i
  weights := fun _ => 1 / 4
  xa i := Fin.elim0 i
  xh := xh
  observedH := fun _ => false
  zh := fun _ => 0

example : (threeOracle (noGadgets (1 / 2))).1 = none := by decide +kernel

example : (threeOracle (noGadgets 2)).1.isSome = true := by decide +kernel

/-- No gadget contributes a positive pair direction, so its group stays absent. -/
example : (packedGroup (noGadgets (1 / 2))).table.get (threeKey 3) = none := by decide +kernel

def badEmptyEndpoint : RationalData 3 1 where
  c := fun _ _ => .neither
  u := fun _ _ => 0
  v := fun _ _ => 0
  weights := fun _ => 1 / 4
  xa := fun _ => -1
  xh := 1 / 2
  observedH := fun _ => false
  zh := fun _ => 0

/-- The zero-direction check returns the actual violated endpoint row. -/
example : ((threeOracle badEmptyEndpoint).1.map
    (fun rows => rows.map fun t => (t.1, t.2.payload))) =
      some [(1, ProfileRow.endpointB (0 : Fin 1))] := by decide +kernel

end NetworkSimplex.Chain.Threshold.Examples
