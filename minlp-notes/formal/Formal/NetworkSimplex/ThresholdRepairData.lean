import Formal.NetworkSimplex.ProfileHull

/-! Exact query data for the two three-label bypass-coefficient repair examples. -/

namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators

noncomputable def firstRepairData : ReductionData 3 (Fin 3) where
  c := fun i j => if j = i.succ then .aOnly else .neither
  u := fun _ _ => 0
  v := fun _ _ => 0
  weights := ![0, 1 / 3, 1 / 3, 1 / 3]
  xa := fun _ => 2 / 5
  xh := 1 / 2
  observedH := fun _ => false
  zh := fun _ => 0

/-- The observed pairs are `{1,2}`, `{1,3}`, and `{2,3}`. -/
def secondRepairObserved (i : Fin 3) (j : Fin 4) : Prop :=
  (i.val = 0 ∧ (j.val = 1 ∨ j.val = 2)) ∨
  (i.val = 1 ∧ (j.val = 1 ∨ j.val = 3)) ∨
  (i.val = 2 ∧ (j.val = 2 ∨ j.val = 3))

instance (i : Fin 3) (j : Fin 4) : Decidable (secondRepairObserved i j) :=
  inferInstanceAs (Decidable (_ ∨ _ ∨ _))

noncomputable def secondRepairData : ReductionData 3 (Fin 3) where
  c := fun i j => if secondRepairObserved i j then .bOnly else .neither
  u := fun _ _ => 0
  v := fun i j => if secondRepairObserved i j then 1 / 20 else 0
  weights := fun _ => 1 / 4
  xa := fun _ => 1 / 20
  xh := 1 / 2
  observedH := fun _ => false
  zh := fun _ => 0

theorem firstRepair_originalDomain : firstRepairData.OriginalDomain := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · constructor
    · intro j; fin_cases j <;> norm_num [firstRepairData]
    · norm_num [firstRepairData, Fin.sum_univ_succ]
  · apply (flow_iff 3 _ 1).mpr
    constructor
    · intro e
      rcases e with ⟨i, b⟩ | e
      · cases b <;> norm_num [pack, firstRepairData, ReductionData.xb]
      · norm_num [pack, firstRepairData]
    · intro i
      norm_num [firstRepairData, ReductionData.xb]
  · intro i
    constructor <;> intro j _ <;> norm_num [firstRepairData]
  · intro j hj
    norm_num [firstRepairData] at hj

theorem secondRepair_originalDomain : secondRepairData.OriginalDomain := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · constructor
    · intro j; norm_num [secondRepairData]
    · norm_num [secondRepairData]
  · apply (flow_iff 3 _ 1).mpr
    constructor
    · intro e
      rcases e with ⟨i, b⟩ | e
      · cases b <;> norm_num [pack, secondRepairData, ReductionData.xb]
      · norm_num [pack, secondRepairData]
    · intro i
      norm_num [secondRepairData, ReductionData.xb]
  · intro i
    constructor
    · intro j _; norm_num [secondRepairData]
    · intro j _
      change 0 ≤ if secondRepairObserved i j then (1 : ℝ) / 20 else 0
      split_ifs <;> norm_num
  · intro j hj
    norm_num [secondRepairData] at hj

theorem firstRepair_residual (i : Fin 3) :
    residual (firstRepairData.c i) (firstRepairData.u i) (firstRepairData.v i)
      (firstRepairData.xa i) = 2 / 5 := by
  simp [firstRepairData, residual]

theorem secondRepair_residual (i : Fin 3) :
    residual (secondRepairData.c i) (secondRepairData.u i) (secondRepairData.v i)
      (secondRepairData.xa i) = 3 / 20 := by
  fin_cases i <;>
    norm_num [secondRepairData, secondRepairObserved, residual, observesA,
      Fin.sum_univ_succ, reduceCtorEq]

/-- The separate McCormick inequalities for a unit-capacity arc and a simplex coordinate. -/
def productMcCormick (x weight z : ℝ) : Prop :=
  0 ≤ z ∧ z ≤ x ∧ z ≤ weight ∧ x + weight - 1 ≤ z

/-- All and only the selected A, B, and bypass observations are checked. -/
def separateMcCormick {m L : ℕ} (D : ReductionData m (Fin L)) : Prop :=
  (∀ i j, observesA (D.c i j) → productMcCormick (D.xa i) (D.weights j) (D.u i j)) ∧
  (∀ i j, observesB (D.c i j) → productMcCormick (D.xb i) (D.weights j) (D.v i j)) ∧
  (∀ j, D.observedH j = true → productMcCormick D.xh (D.weights j) (D.zh j))

theorem firstRepair_separateMcCormick : separateMcCormick firstRepairData := by
  refine ⟨?_, ?_, ?_⟩
  · intro i j hj
    change observesA (if j = i.succ then .aOnly else .neither) at hj
    by_cases h : j = i.succ
    · subst j
      fin_cases i <;> norm_num [firstRepairData, productMcCormick, Matrix.cons_val_two]
    · rw [if_neg h] at hj
      rcases hj with hj | hj <;> cases hj
  · intro i j hj
    change observesB (if j = i.succ then .aOnly else .neither) at hj
    split_ifs at hj <;> rcases hj with hj | hj <;> cases hj
  · intro j; simp [firstRepairData]

theorem secondRepair_separateMcCormick : separateMcCormick secondRepairData := by
  refine ⟨?_, ?_, ?_⟩
  · intro i j hj
    change observesA (if secondRepairObserved i j then .bOnly else .neither) at hj
    split_ifs at hj <;> rcases hj with hj | hj <;> cases hj
  · intro i j hj
    change observesB (if secondRepairObserved i j then .bOnly else .neither) at hj
    by_cases h : secondRepairObserved i j
    · norm_num [secondRepairData, productMcCormick, ReductionData.xb, h]
    · rw [if_neg h] at hj
      rcases hj with hj | hj <;> cases hj
  · intro j; simp [secondRepairData]

end NetworkSimplex.Chain.Threshold
