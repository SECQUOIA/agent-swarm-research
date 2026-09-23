import Formal.NetworkSimplex.ThresholdRepairData
import Formal.NetworkSimplex.ThresholdRows

/-! Two original-coordinate queries requiring opposite bypass-coefficient repairs. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open AffineExpression

noncomputable section

def firstRepairRows : Fin 11 → ProfileRow 3 (Fin 3) :=
  ![.endpointA 0, .endpointA 1, .endpointA 2, .totalLower, .totalLower, .totalLower,
    .totalLower, .totalLower, .totalLower, .totalLower, .totalLower]

def secondRepairRows : Fin 11 → ProfileRow 3 (Fin 3) :=
  ![.totalLower, .totalLower, .totalLower, .endpointB 0, .endpointB 1, .endpointB 2,
    .totalLower, .totalLower, .totalLower, .totalLower, .totalLower]

def singletonPartitionExpression (D : ReductionData 3 (Fin 3)) :
    AffineExpression (Coordinate 3 (Fin 3)) :=
  .add (sum (fun i : Fin 3 => rowExpression D (.endpointA i))) (rowExpression D .totalLower)

def pairTriangleExpression (D : ReductionData 3 (Fin 3)) :
    AffineExpression (Coordinate 3 (Fin 3)) :=
  .add (sum (fun i : Fin 3 => rowExpression D (.endpointB i)))
    (.add (rowExpression D .totalLower) (rowExpression D .totalLower))

def firstRepairedExpression : AffineExpression (Coordinate 3 (Fin 3)) :=
  .add (singletonPartitionExpression firstRepairData) (balanceExpression 0)

def secondRepairedExpression : AffineExpression (Coordinate 3 (Fin 3)) :=
  .add (pairTriangleExpression secondRepairData) (.neg (balanceExpression 0))

theorem firstRepair_branch : ThreeBranch firstRepairData 11 firstRepairRows := by
  unfold ThreeBranch
  simp only [funext_iff]
  decide +kernel

theorem secondRepair_branch : ThreeBranch secondRepairData 15 secondRepairRows := by
  unfold ThreeBranch
  simp only [funext_iff]
  decide +kernel

private theorem firstRepair_endpoint (i : Fin 3) :
    firstRepairData.rowRhs (.endpointA i) = 1 / 10 := by
  change (1 - firstRepairData.xh) - residual (firstRepairData.c i)
    (firstRepairData.u i) (firstRepairData.v i) (firstRepairData.xa i) = 1 / 10
  rw [firstRepair_residual]
  norm_num [firstRepairData]

private theorem firstRepair_totalLower : firstRepairData.rowRhs .totalLower = -1 / 2 := by
  norm_num [ReductionData.rowRhs, ReductionData.total, firstRepairData]

private theorem secondRepair_endpoint (i : Fin 3) :
    secondRepairData.rowRhs (.endpointB i) = 3 / 20 := secondRepair_residual i

private theorem secondRepair_totalLower : secondRepairData.rowRhs .totalLower = -1 / 4 := by
  norm_num [ReductionData.rowRhs, ReductionData.total, secondRepairData]

private theorem firstRepair_unobservedZero (i : Fin 3) : firstRepairData.c i 0 = .neither := by
  simp [firstRepairData, show (0 : Fin 4) ≠ i.succ by
    intro h; have hv := congrArg Fin.val h; simp at hv]

private theorem secondRepair_unobservedZero (i : Fin 3) : secondRepairData.c i 0 = .neither := by
  simp [secondRepairData, secondRepairObserved]

theorem firstRepair_circuit_value :
    (∑ k, (ThreeStateCircuits.weight 11 k : ℝ) * firstRepairData.rowRhs (firstRepairRows k)) =
      -1 / 5 := by
  have hw : ThreeStateCircuits.weight 11 = ![1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1] := by
    decide +kernel
  rw [hw]
  norm_num [Fin.sum_univ_succ, firstRepairRows, firstRepair_endpoint, firstRepair_totalLower]

theorem secondRepair_circuit_value :
    (∑ k, (ThreeStateCircuits.weight 15 k : ℝ) * secondRepairData.rowRhs (secondRepairRows k)) =
      -1 / 20 := by
  have hw : ThreeStateCircuits.weight 15 = ![0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 2] := by
    decide +kernel
  rw [hw]
  norm_num [Fin.sum_univ_succ, secondRepairRows, secondRepair_endpoint, secondRepair_totalLower]

theorem firstRepair_expression_value :
    (singletonPartitionExpression firstRepairData).eval
      (coordinates firstRepairData firstRepairData.xb) = -1 / 5 := by
  simp only [singletonPartitionExpression, AffineExpression.eval, AffineExpression.eval_sum]
  simp_rw [rowExpression_eval firstRepairData firstRepairData.xb firstRepair_unobservedZero]
  norm_num [firstRepair_endpoint, firstRepair_totalLower]

theorem secondRepair_expression_value :
    (pairTriangleExpression secondRepairData).eval
      (coordinates secondRepairData secondRepairData.xb) = -1 / 20 := by
  simp only [pairTriangleExpression, AffineExpression.eval, AffineExpression.eval_sum]
  simp_rw [rowExpression_eval secondRepairData secondRepairData.xb secondRepair_unobservedZero]
  norm_num [secondRepair_endpoint, secondRepair_totalLower]

theorem firstRepair_bypass_coefficient :
    (singletonPartitionExpression firstRepairData).coefficient .bypassFlow = -2 := by
  decide +kernel

theorem secondRepair_bypass_coefficient :
    (pairTriangleExpression secondRepairData).coefficient .bypassFlow = 2 := by
  decide +kernel

/-- Unit means unit flow and product coefficients; simplex weights are not restricted. -/
def ExampleFlowProductUnit (e : AffineExpression (Coordinate 3 (Fin 3))) : Prop :=
  ∀ c : Coordinate 3 (Fin 3), match c with
    | .weight _ => True
    | _ => (e.coefficient c).natAbs ≤ 1

theorem firstRepaired_unit : ExampleFlowProductUnit firstRepairedExpression := by
  intro c
  cases c with
  | bypassFlow => decide +kernel
  | aFlow i => revert i; decide +kernel
  | bFlow i => revert i; decide +kernel
  | aProduct i j => revert i j; decide +kernel
  | bProduct i j => revert i j; decide +kernel
  | bypassProduct j => revert j; decide +kernel
  | weight _ => trivial

theorem secondRepaired_unit : ExampleFlowProductUnit secondRepairedExpression := by
  intro c
  cases c with
  | bypassFlow => decide +kernel
  | aFlow i => revert i; decide +kernel
  | bFlow i => revert i; decide +kernel
  | aProduct i j => revert i j; decide +kernel
  | bProduct i j => revert i j; decide +kernel
  | bypassProduct j => revert j; decide +kernel
  | weight _ => trivial

theorem firstRepaired_value :
    firstRepairedExpression.eval (coordinates firstRepairData firstRepairData.xb) = -1 / 5 := by
  rw [firstRepairedExpression, AffineExpression.eval, firstRepair_expression_value,
    balanceExpression_eval firstRepairData firstRepairData.xb 0 (by
      norm_num [firstRepairData, ReductionData.xb])]
  ring

theorem secondRepaired_value :
    secondRepairedExpression.eval (coordinates secondRepairData secondRepairData.xb) = -1 / 20 := by
  rw [secondRepairedExpression, AffineExpression.eval, AffineExpression.eval,
    secondRepair_expression_value,
    balanceExpression_eval secondRepairData secondRepairData.xb 0 (by
      norm_num [secondRepairData, ReductionData.xb])]
  ring

end
end NetworkSimplex.Chain.Threshold
