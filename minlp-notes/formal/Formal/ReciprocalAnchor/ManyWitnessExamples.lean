import Formal.ReciprocalAnchor.ManyFastWitness

/-! Kernel evaluation of every coordinate emitted for the exact two-leaf example. -/
namespace ReciprocalAnchor.ManyLeaf

private def exampleOutput := fastWitnessOutput 1 3 2 (31 / 50)
  (![2 / 3, 14 / 29] : Fin 2 → ℚ) ![5 / 3, 40 / 29]

private def weightedOutput (values : List ℚ) : ℚ :=
  (List.zipWith (· * ·) exampleOutput.mass.toList values).sum

set_option maxRecDepth 16384 in
/-- The actual producer returns all graph coordinates and every required moment. -/
theorem executable_two_leaf_graph_witness :
    exampleOutput.mass.toList.sum = 1 ∧
      weightedOutput exampleOutput.location.toList = 2 ∧
      weightedOutput exampleOutput.inverse.toList = 31 / 50 ∧
      ((exampleOutput.leaves.get 0).1.map weightedOutput) = some (2 / 3) ∧
      ((exampleOutput.leaves.get 1).1.map weightedOutput) = some (14 / 29) ∧
      ((exampleOutput.products.get 0).map weightedOutput) = some (5 / 3) ∧
      ((exampleOutput.products.get 1).map weightedOutput) = some (40 / 29) := by
  decide +kernel

end ReciprocalAnchor.ManyLeaf
