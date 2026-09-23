import Formal.MatroidSpectral.InputExecution

/-! Small exact execution checks for the assembled original-input producer.
These are regression examples, not substitutes for the universal Lean proofs.
The work observer is evaluated but no wall-clock complexity claim is made. -/
namespace MatroidSpectral.ExecutionExamples
open Matrix DAGSpectral

private theorem zero_psd : (ratMatrixReal (0 : Matrix (Fin 1) (Fin 1) ℚ)).PosSemidef := by
  simpa using (Matrix.PosSemidef.zero : (0 : Matrix (Fin 1) (Fin 1) ℝ).PosSemidef)

private theorem one_psd : (ratMatrixReal (1 : Matrix (Fin 1) (Fin 1) ℚ)).PosSemidef := by
  simpa using (Matrix.PosSemidef.one : (1 : Matrix (Fin 1) (Fin 1) ℝ).PosSemidef)

private def check (label : String) (actual expected : List (Finset (Fin 1))) : IO Unit := do
  unless actual.toFinset == expected.toFinset do
    throw <| IO.userError s!"{label}: unexpected returned bases"
  IO.println s!"PASS {label}: {actual.length} returned list entries"

-- Matroid rank zero retains the empty base even with a nonzero prior.
#eval check "rank zero, nonzero prior"
  (representedInputRun (0 : RationalRepresentation 0 1) 1 (fun _ => 0)
    one_psd (fun _ => zero_psd) (1/2) 2 2).1 [∅]

-- Positive matroid rank and zero information use an original-rank support
-- test and deletion recovery; the empty set must not be accepted.
#eval check "positive matroid rank, zero information"
  (representedInputRun (1 : RationalRepresentation 1 1) 0 (fun _ => 0)
    zero_psd (fun _ => zero_psd) (1/2) 2 2).1 [{0}]

-- A positive-information trial executes the shift, owner marker, exact
-- determinant interpolation, and recovery. The unique original base remains.
#eval check "positive scalar information"
  (representedInputRun (1 : RationalRepresentation 1 1) 0 (fun _ => 1)
    zero_psd (fun _ => one_psd) (3/4) 3 3).1 [{0}]

end MatroidSpectral.ExecutionExamples
