import Formal.DAGSpectral.FactorInputExecution
open DAGSpectral DAGSpectral.FactorInputExecution
def assertTrue (b : Bool) (s : String) : IO Unit := unless b do throw (IO.userError s)
#eval do
  let A : Matrix (Fin 2) (Fin 2) ℚ := !![2,1;1,2]
  let run := ldlRun 2 A
  assertTrue (decide ((run.factors.map factorView) = [(2,![1,1/2]),(3/2,![0,1])])) "actual Schur factors"
  assertTrue (decide (run.events = rationalLDLTrace 2 A)) "actual LDL arithmetic charge trace"
  let singular := ldlRun 2 (!![0,0;0,3] : Matrix (Fin 2) (Fin 2) ℚ)
  assertTrue (decide ((singular.factors.map factorView) = [(3,![0,1])])) "zero pivot branch"
  assertTrue (decide ((ldlRun 2 (0 : Matrix (Fin 2) (Fin 2) ℚ)).factors = [])) "zero owner"
  let indefinite := ldlRun 1 (!![-2] : Matrix (Fin 1) (Fin 1) ℚ)
  assertTrue (decide ((indefinite.factors.map factorView) = [(-2,![1])])) "negative pivot equality branch"
  assertTrue (decide (indefinite.copies = 33)) "Schur cache and both leading materializations"
  assertTrue (decide ((ldlRun 1 (0 : Matrix (Fin 1) (Fin 1) ℚ)).copies = 9)) "zero-pivot empty Schur storage"
  assertTrue (decide ((ldlRun 0 (fun i _ => Fin.elim0 i)).factors = [])) "empty dimension"
  let atoms : Fin 3 → Matrix (Fin 2) (Fin 2) ℚ := ![0,A,!![0,0;0,3]]
  let cache := inputRun atoms
  assertTrue (decide ((cache.factors.map fun f : Fin 3 × StoredFactor 2 => f.1) = [1,1,2])) "owner repeats preserved"
  assertTrue (decide ((cache.factors.map fun f : Fin 3 × StoredFactor 2 => factorView f.2) = [(2,![1,1/2]),(3/2,![0,1]),(3,![0,1])])) "owner-local flatten order"
  assertTrue (decide ((cachedLookup cache.factors 1).1.map (fun f : Fin 3 × StoredFactor 2 => f.2.1) = some (3/2))) "lookup cached factor"
  assertTrue (decide ((cachedLookup cache.factors 3).1 = none)) "lookup range boundary"
  assertTrue (decide ((cachedLookup cache.factors 3).2 = 4)) "lookup linear steps"
  assertTrue (decide ((inputRun (fun i : Fin 0 => Fin.elim0 i) : InputRun 2 0).factors = [])) "empty owners"
  IO.println "factor-input execution checks passed"
#print axioms DAGSpectral.FactorInputExecution.inputRun_indexed
#print axioms DAGSpectral.FactorInputExecution.ldlRun_eq_instrumented
#print axioms DAGSpectral.FactorInputExecution.inputBitWork_polynomial
