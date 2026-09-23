import Formal.DAGSpectral.ProfileDPBitExecution
open DAGSpectral DAGSpectral.ExplicitDAG

def reviewParallel : ExplicitDAG 2 2 where
  src := fun _ => 0
  dst := fun _ => 1
  forward := by intro e; decide

def reviewLabel (_ : Fin 2) (_ : Fin 1) : ℤ := -3
example : (reviewParallel.outputBitCounted (fun _ => true) 0 ∅ reviewLabel 1).1 = [[1]] := by native_decide
example : (reviewParallel.outputBitCounted (fun _ => true) 0 {0} reviewLabel 1).1 = [[0]] := by native_decide
example : (reviewParallel.outputBitCounted (fun _ => true) 0 {0,1} reviewLabel 1).1 = [] := by native_decide
example : (reviewParallel.outputBitCounted (fun _ => true) 0 ∅ reviewLabel 1).2 ≤
    reviewParallel.dpBitWork (fun _ => true) 0 ∅ reviewLabel := by native_decide
example : compareAllBitCounted id (fun a b : ℕ => a+b) 1 [1,2,3] = (false,9) := by native_decide
example : IntegerBits ⌊(-7/2 : ℚ)⌋ 3 := by unfold IntegerBits; native_decide
#print axioms ExplicitDAG.outputBitCounted_paths
#print axioms ExplicitDAG.outputBitCounted_work
#print axioms ExplicitDAG.spectral_rational_dpBitWork

-- Terminal checks scan only requested owners, including an empty request.
example : terminalOwnerCheck (∅ : Finset (Fin 3)) [0,1,2] = true := by native_decide
example : terminalOwnerCheck ({0,2} : Finset (Fin 3)) [0,1,2] = true := by native_decide
example : terminalOwnerCheck ({0,2} : Finset (Fin 3)) [0,1] = false := by native_decide
#print axioms terminalOwnerCheck_eq
