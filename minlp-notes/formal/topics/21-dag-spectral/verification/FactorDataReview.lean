import Formal.DAGSpectral.FactorInputData
import Formal.DAGSpectral.BasisInputExecution
open DAGSpectral DAGSpectral.FactorInputExecution
def ident : Matrix (Fin 2) (Fin 2) ℚ := 1
theorem ident_psd : (ratMatrixReal ident).PosSemidef := by
  have h : ratMatrixReal ident = (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [ident,ratMatrixReal]
  rw [h]
  exact Matrix.PosSemidef.one
def assertTrue (b : Bool) (s : String) : IO Unit := unless b do throw (IO.userError s)
#eval do
  let Q : Fin 1 → Matrix (Fin 2) (Fin 2) ℚ := fun _ => ident
  let cache := inputRun (priorAtomMatrices ident Q)
  let D := cachedFactorData ident Q ident_psd (fun _ => ident_psd) cache rfl
  if hk : 3 < cache.factors.length then
    let k : Fin cache.factors.length := ⟨3,hk⟩
    assertTrue (decide ((cache.factorAtRun k).2 = 4)) "actual last-factor traversal"
    assertTrue (decide ((cache.factorAtRun k).1.2.2.get 1 = 1)) "counted lookup returns cached coordinate"
  else throw (IO.userError "missing expected cached factor")
  assertTrue (decide (cache.factors.length = 4)) "runtime cache length"
  assertTrue (decide (List.ofFn D.owner = [none,none,some 0,some 0])) "prior and repeated edge labels"
  assertTrue (decide (List.ofFn D.weight = [1,1,1,1])) "cached weights"
  assertTrue (decide (List.ofFn D.vector = [![1,0],![0,1],![1,0],![0,1]])) "cached coordinates"
  let b : Finset (Fin cache.factors.length) := Finset.univ.filter fun j => j.val ≠ 1
  let basis := BasisInputExecution.basisRun D b
  assertTrue (decide (basis.1.labels.toList.map Fin.val = [0,2,3])) "sorted actual basis labels"
  assertTrue (decide (List.ofFn (basis.1.columns 0) = [1,1,0])) "actual first column row"
  assertTrue (decide (List.ofFn (basis.1.columns 1) = [0,0,1])) "actual second column row"
  assertTrue (decide (basis.1.required = {0})) "deduplicated owners exclude prior"
  let emptyBasis := BasisInputExecution.basisRun D ∅
  assertTrue (decide (emptyBasis.1.required = ∅ ∧ emptyBasis.2 > 0)) "empty candidate still charges scans"
  assertTrue (decide ((BasisInputExecution.ownerCheckRun (0 : Fin 1) [some 0,none,some 0]).2 = 6)) "full owner scan after hit"
  let copied := BasisInputExecution.copyValuesRun 7 (fun _ : Fin 1 => (3/2 : ℚ)) [0]
  assertTrue (decide (copied = ([3/2],19))) "actual rational payload and source access charge"
  IO.println "cached factor-data checks passed"
#print axioms DAGSpectral.FactorInputExecution.cachedFactorData_eq
#print axioms DAGSpectral.FactorInputExecution.cachedFactorData_bits
#print axioms DAGSpectral.BasisInputExecution.basisRun_work
#print axioms DAGSpectral.BasisInputExecution.basisRun_required
#print axioms DAGSpectral.FactorInputExecution.InputRun.factorAtRun_steps
