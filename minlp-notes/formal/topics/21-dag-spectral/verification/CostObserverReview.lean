import Formal.DAGSpectral.BitComplexity
open DAGSpectral ReciprocalAnchor.ManyLeaf.BitCost

def originalObserver (op : RationalPrimitive) (q r : ℚ) (K : ℕ) : ℕ :=
  let L := 2*K+2
  3*multiplicationCost L L + 3*addCost L L +
    normalizationCost (rawNumerator op q r).natAbs (rawDenominator op q r).natAbs

def assertTrue (b : Bool) (s : String) : IO Unit := unless b do throw (IO.userError s)

#eval do
  let ops : List RationalPrimitive := [.add,.sub,.mul,.div,.inv,.compare,.neg]
  for op in ops do
    for (qr : ℚ × ℚ) in ([(0,0),(-3/5,2/7),(2/3,0),(-2/3,-2/3)] : List (ℚ × ℚ)) do
      for K in [0,1,5] do
        assertTrue (decide (primitiveBitCostClosed op qr.1 qr.2 K =
          originalObserver op qr.1 qr.2 K)) "small original finite-loop cost mismatch"
  let K : ℕ := 2^100
  let events : List ArithmeticEvent := [(.add,-3/5,2/7),(.div,2/3,0),(.inv,0,0)]
  let cost := traceBitWork K events
  assertTrue (decide (cost = (events.map fun e : ArithmeticEvent => primitiveBitCostClosed e.1 e.2.1 e.2.2 K).sum))
    "compiled observer replacement"
  assertTrue (decide (cost > K)) "large-width observer was evaluated"
  IO.println "84 original-loop comparisons and large-width observer checks passed"

#print axioms DAGSpectral.primitiveBitCost_closed
#print axioms DAGSpectral.traceBitWork_le
