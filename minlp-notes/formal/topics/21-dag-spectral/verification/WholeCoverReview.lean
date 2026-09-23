import Formal.DAGSpectral.CoverInputExecution
open DAGSpectral DAGSpectral.CoverBitCost

#eval (do
  unless decide ((sublistsCounted 2 ([0,1,2,3] : List ℕ)).1.length = 6) do
    throw (IO.userError "WholeCoverReview check 1 failed") : IO Unit)
#eval (do
  unless decide ((sublistsCounted 3 ([0,1] : List ℕ)).1 = []) do
    throw (IO.userError "WholeCoverReview check 2 failed") : IO Unit)
#eval (do
  unless decide ((sublistsCounted 0 ([] : List ℕ)).1 = [[]]) do
    throw (IO.userError "WholeCoverReview check 3 failed") : IO Unit)
#eval (do
  unless decide ((candidateBasisList 2 4).length = 6) do
    throw (IO.userError "WholeCoverReview check 4 failed") : IO Unit)
#eval (do
  unless decide (pathEqualCounted ([0,1] : List (Fin 3)) [0,2] = (false,9)) do
    throw (IO.userError "WholeCoverReview check 5 failed") : IO Unit)
#eval (do
  unless decide ((dedupCounted ([[0],[1],[0],[]] : List (List (Fin 2)))).1 = [[1],[0],[]]) do
    throw (IO.userError "WholeCoverReview check 6 failed") : IO Unit)
#eval (do
  unless decide ((collectRuns (fun i : Fin 2 => ([[i]],3)) [0,1]).1 = [[0],[1]]) do
    throw (IO.userError "WholeCoverReview check 7 failed") : IO Unit)
#eval (do
  unless decide ((appendPathsCounted ([[0],[1]] : List (List (Fin 2))) [[]]).1 = [[0],[1],[]]) do
    throw (IO.userError "WholeCoverReview check 8 failed") : IO Unit)
#print axioms sublistsCounted_bound
#print axioms candidateBasisList_toFinset
#print axioms coverBitRun_paths
#print axioms coverBitRun_work

open DAGSpectral.NormalizationTrials

def reviewZeroData : FactorData 1 2 0 where
  atom := fun _ => 0
  owner := Fin.elim0
  weight := Fin.elim0
  vector := Fin.elim0
  weight_pos := by intro j; exact Fin.elim0 j
  atom_eq := by intro o; ext i j; simp [factorSum]
  owner_card := by intro o; simp

def reviewGraph : ExplicitDAG 2 2 where
  src := fun _ => 0
  dst := fun _ => 1
  forward := by intro e; decide

-- Zero matrices yield one actual parallel-edge path and no positive-rank candidates.
#eval (do
  unless decide ((zeroBitRun reviewGraph 0 1 reviewZeroData 1).1 = [[1]]) do
    throw (IO.userError "WholeCoverReview check 9 failed") : IO Unit)
#eval (do
  unless decide ((coverBitRun reviewGraph 0 1 reviewZeroData 1 1 (fun _ => 1)
    (fun _ => 1) (fun _ => 1)).1 = [[1]]) do
    throw (IO.userError "WholeCoverReview check 10 failed") : IO Unit)
#eval (do
  unless decide ((coverBitRun reviewGraph 0 0 reviewZeroData 1 1 (fun _ => 1)
    (fun _ => 1) (fun _ => 1)).1 = [[]]) do
    throw (IO.userError "WholeCoverReview check 11 failed") : IO Unit)
#eval (do
  unless decide ((coverBitRun reviewGraph 1 0 reviewZeroData 1 1 (fun _ => 1)
    (fun _ => 1) (fun _ => 1)).1 = []) do
    throw (IO.userError "WholeCoverReview check 12 failed") : IO Unit)

-- The original-input wrapper also executes the zero-matrix boundary.
theorem reviewZeroPSD : (ratMatrixReal (0 : Matrix (Fin 1) (Fin 1) ℚ)).PosSemidef := by
  simp only [ratMatrixReal_zero]
  exact Matrix.PosSemidef.zero
#eval (do
  unless decide ((coverInputRun reviewGraph 0 1 0 (fun _ => 0) reviewZeroPSD
    (fun _ => reviewZeroPSD) 1 1 1).1 = [[1]]) do
    throw (IO.userError "WholeCoverReview check 13 failed") : IO Unit)
#print axioms coverInputRun_paths
#print axioms coverInputRun_isRelativeCover
#print axioms coverInputRun_work

theorem reviewOnePSD : (ratMatrixReal (1 : Matrix (Fin 1) (Fin 1) ℚ)).PosSemidef := by
  simp only [ratMatrixReal_one]
  exact Matrix.PosSemidef.one
-- Positive-rank trials retain both original owners, even for equal numerical atoms.
#eval (do
  unless decide ((coverInputRun reviewGraph 0 1 0 (fun _ => 1) reviewZeroPSD
    (fun _ => reviewOnePSD) (1/2) 2 2).1.toFinset = {[0],[1]}) do
    throw (IO.userError "WholeCoverReview check 14 failed") : IO Unit)
#print axioms coverInputRun_list
#print axioms coverInputRun_polynomial_work
#print axioms ExplicitDAG.outputCachedBitCounted_cost
