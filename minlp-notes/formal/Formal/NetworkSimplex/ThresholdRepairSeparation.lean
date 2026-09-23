import Formal.NetworkSimplex.ThresholdRepairExamples
import Formal.NetworkSimplex.ThresholdBranchValidity
import Formal.NetworkSimplex.ThresholdPattern

/-! The two McCormick-feasible queries violate valid, unit-coefficient chain cuts. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators

noncomputable section

private theorem first_base_class (i : Fin 3) : firstRepairData.c i 0 = .neither := by
  fin_cases i <;> decide +kernel

private theorem second_base_class (i : Fin 3) : secondRepairData.c i 0 = .neither := by
  fin_cases i <;> norm_num [secondRepairData, secondRepairObserved]

theorem firstRepair_not_mem_hull :
    firstRepairData.graphPoint ∉ convexHull ℝ firstRepairData.graph := by
  intro h
  have hv := firstRepair_branch.nonneg_of_hull firstRepairData 11 firstRepairRows
    first_base_class rfl h
  rw [firstRepair_circuit_value] at hv
  norm_num at hv

theorem secondRepair_not_mem_hull :
    secondRepairData.graphPoint ∉ convexHull ℝ secondRepairData.graph := by
  intro h
  have hv := secondRepair_branch.nonneg_of_hull secondRepairData 15 secondRepairRows
    second_base_class rfl h
  rw [secondRepair_circuit_value] at hv
  norm_num at hv

private theorem singletonPartitionExpression_eval (D : ReductionData 3 (Fin 3))
    (hc : ∀ i, D.c i 0 = .neither) :
    (singletonPartitionExpression D).eval (coordinates D D.xb) =
      ∑ k, (ThreeStateCircuits.weight 11 k : ℝ) * D.rowRhs (firstRepairRows k) := by
  have hw : ThreeStateCircuits.weight 11 = ![1,1,1,0,0,0,0,0,0,0,1] := by decide +kernel
  simp only [singletonPartitionExpression, AffineExpression.eval, AffineExpression.eval_sum]
  simp_rw [rowExpression_eval D D.xb hc]
  rw [hw]
  norm_num [Fin.sum_univ_succ, firstRepairRows]
  ring

private theorem pairTriangleExpression_eval (D : ReductionData 3 (Fin 3))
    (hc : ∀ i, D.c i 0 = .neither) :
    (pairTriangleExpression D).eval (coordinates D D.xb) =
      ∑ k, (ThreeStateCircuits.weight 15 k : ℝ) * D.rowRhs (secondRepairRows k) := by
  have hw : ThreeStateCircuits.weight 15 = ![0,0,0,1,1,1,0,0,0,0,2] := by decide +kernel
  simp only [pairTriangleExpression, AffineExpression.eval, AffineExpression.eval_sum]
  simp_rw [rowExpression_eval D D.xb hc]
  rw [hw]
  norm_num [Fin.sum_univ_succ, secondRepairRows]
  ring

/-- The first fixed repaired expression is valid throughout its original-coordinate hull. -/
theorem firstRepaired_valid (D : ReductionData 3 (Fin 3))
    (hc : D.c = firstRepairData.c) (hh : D.observedH = firstRepairData.observedH)
    (h : D.graphPoint ∈ convexHull ℝ D.graph) :
    0 ≤ firstRepairedExpression.eval (coordinates D D.xb) := by
  have hc0 : ∀ i, D.c i 0 = .neither := by intro i; rw [hc]; exact first_base_class i
  have hh0 : D.observedH 0 = false := by rw [hh]; rfl
  have hb : ThreeBranch D 11 firstRepairRows :=
    ThreeBranch.pattern_transfer firstRepairData D 11 firstRepairRows
      firstRepair_branch hc.symm hh.symm
  have he : singletonPartitionExpression firstRepairData = singletonPartitionExpression D := by
    simp only [singletonPartitionExpression,
      rowExpression_eq_of_pattern_eq firstRepairData D hc.symm hh.symm]
  rw [firstRepairedExpression, AffineExpression.eval, he,
    balanceExpression_eval D D.xb 0 (by simp [ReductionData.xb]), add_zero,
    singletonPartitionExpression_eval D hc0]
  exact hb.nonneg_of_hull D 11 firstRepairRows hc0 hh0 h

/-- The opposite correction is likewise valid throughout the second observation pattern. -/
theorem secondRepaired_valid (D : ReductionData 3 (Fin 3))
    (hc : D.c = secondRepairData.c) (hh : D.observedH = secondRepairData.observedH)
    (h : D.graphPoint ∈ convexHull ℝ D.graph) :
    0 ≤ secondRepairedExpression.eval (coordinates D D.xb) := by
  have hc0 : ∀ i, D.c i 0 = .neither := by intro i; rw [hc]; exact second_base_class i
  have hh0 : D.observedH 0 = false := by rw [hh]; rfl
  have hb : ThreeBranch D 15 secondRepairRows :=
    ThreeBranch.pattern_transfer secondRepairData D 15 secondRepairRows
      secondRepair_branch hc.symm hh.symm
  have he : pairTriangleExpression secondRepairData = pairTriangleExpression D := by
    simp only [pairTriangleExpression,
      rowExpression_eq_of_pattern_eq secondRepairData D hc.symm hh.symm]
  rw [secondRepairedExpression, AffineExpression.eval, AffineExpression.eval, he,
    balanceExpression_eval D D.xb 0 (by simp [ReductionData.xb]), neg_zero, add_zero,
    pairTriangleExpression_eval D hc0]
  exact hb.nonneg_of_hull D 15 secondRepairRows hc0 hh0 h

end
end NetworkSimplex.Chain.Threshold
