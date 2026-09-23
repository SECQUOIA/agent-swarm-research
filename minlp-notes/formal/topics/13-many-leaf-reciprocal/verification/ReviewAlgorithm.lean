import Formal.ReciprocalAnchor.ManyFastEvaluation
import Formal.ReciprocalAnchor.ManyEvaluatorBitCost
open ReciprocalAnchor.ManyLeaf.FastEnvelope
#eval fastLowerMoment (1 : ℚ) 3 2 (![] : Fin 0 → ℚ) ![]
#eval fastLowerMoment (1 : ℚ) 3 1 (![] : Fin 0 → ℚ) ![]
#eval fastLowerMoment (1 : ℚ) 3 3 (![] : Fin 0 → ℚ) ![]
#eval fastLowerMoment (1 : ℚ) 3 2 ![0, 1] ![0, 2]
#eval fastLowerMoment (2 : ℚ) 2 2 (![] : Fin 0 → ℚ) ![]
#eval fastLowerMoment (1 : ℚ) 3 2 ![2/3, 14/29] ![5/3, 40/29]
#print axioms ReciprocalAnchor.ManyLeaf.FastEnvelope.fastLowerMoment_eq
#print axioms ReciprocalAnchor.ManyLeaf.FastEnvelope.buildSegments_cost
#print axioms ReciprocalAnchor.ManyLeaf.BitCost.evaluator_schoolbook_bound
#print axioms ReciprocalAnchor.ManyLeaf.BitCost.evaluator_primitive_bitCost
#print axioms ReciprocalAnchor.ManyLeaf.BitCost.countedEuclid_gcd
