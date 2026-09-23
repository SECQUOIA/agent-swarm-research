import Formal.DAGSpectral.ProfileSpectralDP
import Formal.DAGSpectral.ProfileDPExecution
open DAGSpectral DAGSpectral.ExplicitDAG

-- Parallel edges retain different identities even with identical profiles.
def parallel : ExplicitDAG 2 2 where
  src := fun _ => 0
  dst := fun _ => 1
  forward := by intro e; decide

def noCoordinates (_ : Fin 2) : Fin 0 → ℤ := Fin.elim0
example : parallel.output (fun _ => true) 0 1 ∅ noCoordinates = [[1]] := by decide
example : parallel.output (fun _ => true) 0 1 {0} noCoordinates = [[0]] := by decide
example : parallel.output (fun _ => true) 0 1 {0,1} noCoordinates = [] := by decide
example : parallel.output (fun e => decide (e=0)) 0 1 ∅ noCoordinates = [[0]] := by decide
example : parallel.output (fun _ => true) 1 0 ∅ noCoordinates = [] := by decide

-- Prefix merging works for different path lengths, with no length component in the state.
def shortcut : ExplicitDAG 3 3 where
  src := ![0,1,0]
  dst := ![1,2,2]
  forward := by intro e; fin_cases e <;> decide

def cancelLabel (e : Fin 3) (_ : Fin 1) : ℤ := ![-7,7,0] e
example : shortcut.output (fun _ => true) 0 2 ∅ cancelLabel = [[2]] := by decide
example : shortcut.output (fun _ => true) 0 2 {0} cancelLabel = [[0,1]] := by decide
example : shortcut.edgeExtensions (fun _ => true) 0 ∅ cancelLabel = 3 := by decide
example : shortcut.comparisonBudget (fun _ => true) 0 ∅ cancelLabel = 1 := by decide
example : shortcut.run (fun _ => true) 0 ∅ cancelLabel 2 2 = [] := by decide

-- No-edge graphs still return the unique empty path when source equals sink.
def isolated : ExplicitDAG 2 0 where
  src := Fin.elim0
  dst := Fin.elim0
  forward := fun e => Fin.elim0 e
example : isolated.output (fun _ => true) 0 0 ∅ (fun _ => (0 : Fin 0 → ℤ)) = [[]] := by decide
example : isolated.output (fun _ => true) 0 1 ∅ (fun _ => (0 : Fin 0 → ℤ)) = [] := by decide

#print axioms ExplicitDAG.run_complete
#print axioms ExplicitDAG.edgeExtensions_eq_generated
#print axioms ExplicitDAG.output_coordinate_close
#print axioms ExplicitDAG.comparisonBudget_bound

-- Counted full-scan producer returns the same actual path, with its comparisons.
example : representativesCounted id ([1,1,2,1] : List ℕ) = ([2,1], 5) := by decide
example : shortcut.outputCounted (fun _ => true) 0 ∅ cancelLabel 2 = ([[2]], 1) := by decide
example : isolated.outputCounted (fun _ => true) 0 ∅ (fun _ => (0 : Fin 0 → ℤ)) 0 = ([[]], 0) := by decide
#print axioms representativesCounted_spec
#print axioms ExplicitDAG.runCounted_final_cost
#print axioms ExplicitDAG.outputCounted_spec
