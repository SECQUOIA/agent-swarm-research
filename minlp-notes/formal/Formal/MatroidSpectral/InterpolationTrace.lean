import Formal.MatroidSpectral.InterpolationExecution
import Formal.DAGSpectral.MatrixArithmeticTrace

namespace MatroidSpectral

open scoped BigOperators
open DAGSpectral

/-- The coefficient table and its actual multiplication/subtraction operands. -/
def interpolationNumeratorTrace (D : ℕ) : List ℚ → List ℚ × List ArithmeticEvent
  | [] => (interpolationNumeratorTable D [], [])
  | x :: xs =>
    let previous := interpolationNumeratorTrace D xs
    let cells := List.ofFn (fun k : Fin (D + 1) =>
      let a := if k.val = 0 then 0 else previous.1.getD (k.val - 1) 0
      let b := previous.1.getD k.val 0
      let product := x * b
      ((a - product, [(.mul, x, b), (.sub, a, product)]) : ℚ × List ArithmeticEvent))
    (cells.map Prod.fst, previous.2 ++ cells.flatMap Prod.snd)

theorem interpolationNumeratorTrace_value (D : ℕ) (xs : List ℚ) :
    (interpolationNumeratorTrace D xs).1 = interpolationNumeratorTable D xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
    simp [interpolationNumeratorTrace, interpolationNumeratorTable, ih, Function.comp_def]

theorem interpolationNumeratorTrace_length (D : ℕ) (xs : List ℚ) :
    (interpolationNumeratorTrace D xs).2.length = 2 * (D + 1) * xs.length := by
  induction xs with
  | nil => simp [interpolationNumeratorTrace]
  | cons x xs ih =>
    simp [interpolationNumeratorTrace, List.length_flatMap, ih, List.sum_ofFn]
    ring

def interpolationDenominatorExpr (D : ℕ) (t : Fin (D + 1)) : ArithmeticExpr :=
  prodExpr ((interpolationOtherNodes D t).map (fun x =>
    .op .sub (.atom (interpolationNode t)) (.atom x)))

theorem interpolationOtherNodes_length (D : ℕ) (t : Fin (D + 1)) :
    (interpolationOtherNodes D t).length = D := by
  classical
  simp only [interpolationOtherNodes, List.length_map]
  have h := List.toFinset_card_of_nodup ((List.nodup_finRange (D + 1)).filter (fun j => j ≠ t))
  have he : ((List.finRange (D + 1)).filter (fun j => j ≠ t)).toFinset =
      Finset.univ.erase t := by ext j; simp
  rw [he] at h
  simpa using h.symm

theorem interpolationDenominatorExpr_value (D : ℕ) (t : Fin (D + 1)) :
    (interpolationDenominatorExpr D t).eval =
      ((interpolationOtherNodes D t).map (fun x => interpolationNode t - x)).prod := by
  simp [interpolationDenominatorExpr, List.map_map, Function.comp_def,
    ArithmeticExpr.eval, primitiveResult]

theorem interpolationDenominatorExpr_operations (D : ℕ) (t : Fin (D + 1)) :
    (interpolationDenominatorExpr D t).operations = 2 * D := by
  simp [interpolationDenominatorExpr, prodExpr_operations, List.map_map, Function.comp_def,
    ArithmeticExpr.operations, interpolationOtherNodes_length]
  omega

def interpolationWeightTrace (D : ℕ) (t : Fin (D + 1)) (k : ℕ) :
    ℚ × List ArithmeticEvent :=
  let numerator := interpolationNumeratorTrace D (interpolationOtherNodes D t)
  let denominator := (interpolationDenominatorExpr D t).run
  let a := numerator.1.getD k 0
  (a / denominator.1, numerator.2 ++ denominator.2 ++ [(.div, a, denominator.1)])

theorem interpolationWeightTrace_value (D : ℕ) (t : Fin (D + 1)) (k : ℕ) :
    (interpolationWeightTrace D t k).1 = interpolationWeightRun D t k := by
  simp [interpolationWeightTrace, interpolationWeightRun, interpolationNumeratorTrace_value,
    ArithmeticExpr.run_eq, interpolationDenominatorExpr_value]

theorem interpolationWeightTrace_length (D : ℕ) (t : Fin (D + 1)) (k : ℕ) :
    (interpolationWeightTrace D t k).2.length = (2 * (D + 1) + 2) * D + 1 := by
  simp [interpolationWeightTrace, interpolationNumeratorTrace_length,
    ArithmeticExpr.run_eq, interpolationDenominatorExpr_operations,
    interpolationOtherNodes_length]
  ring

section OrderedCoordinates

variable {κ : Type*} [Fintype κ] [LinearOrder κ]

def interpolationCoordinateList (κ : Type*) [Fintype κ] [LinearOrder κ] : List κ :=
  Finset.univ.sort (· ≤ ·)

@[simp] theorem interpolationCoordinateList_mem (i : κ) :
    i ∈ interpolationCoordinateList κ := by simp [interpolationCoordinateList]

@[simp] theorem interpolationCoordinateList_length :
    (interpolationCoordinateList κ).length = Fintype.card κ := by
  simp [interpolationCoordinateList]

@[instance_reducible] def interpolationGridOrder (D : ℕ) : LinearOrder (κ → Fin (D + 1)) :=
  LinearOrder.lift' (fun t => (interpolationCoordinateList κ).map t) (by
    intro a b h
    funext i
    exact List.map_inj_left.mp h i (interpolationCoordinateList_mem i))

def interpolationGridList (κ : Type*) [Fintype κ] [LinearOrder κ] (D : ℕ) :
    List (κ → Fin (D + 1)) :=
  letI : LinearOrder (κ → Fin (D + 1)) := interpolationGridOrder (κ := κ) D
  (Finset.univ : Finset (κ → Fin (D + 1))).sort (interpolationGridOrder D).le

theorem interpolationGridList_length (D : ℕ) :
    (interpolationGridList κ D).length = (D + 1) ^ Fintype.card κ := by
  simp [interpolationGridList]

theorem interpolationGridList_sum (D : ℕ) (f : (κ → Fin (D + 1)) → ℚ) :
    ((interpolationGridList κ D).map f).sum = ∑ t, f t := by
  let : LinearOrder (κ → Fin (D + 1)) := interpolationGridOrder (κ := κ) D
  exact (List.sum_toFinset f
    (Finset.sort_nodup Finset.univ (interpolationGridOrder D).le)).symm.trans
    (by rw [Finset.sort_toFinset])

def interpolationTermTrace (D : ℕ) (value : ℚ)
    (t z : κ → Fin (D + 1)) : ℚ × List ArithmeticEvent :=
  let weights := (interpolationCoordinateList κ).map
    (fun i => interpolationWeightTrace D (t i) (z i).val)
  let product := (prodExpr (weights.map (fun w => .atom w.1))).run
  (value * product.1, weights.flatMap Prod.snd ++ product.2 ++ [(.mul, value, product.1)])

theorem interpolationTermTrace_value (D : ℕ) (value : ℚ)
    (t z : κ → Fin (D + 1)) :
    (interpolationTermTrace D value t z).1 =
      value * ∏ i, interpolationWeightRun D (t i) (z i).val := by
  simp only [interpolationTermTrace, ArithmeticExpr.run_eq, prodExpr_eval,
    List.map_map, Function.comp_def, ArithmeticExpr.eval, interpolationWeightTrace_value]
  congr 1
  exact (List.prod_toFinset _ (Finset.sort_nodup _ _)).symm.trans
    (by rw [Finset.sort_toFinset])

theorem interpolationTermTrace_length (D : ℕ) (value : ℚ)
    (t z : κ → Fin (D + 1)) :
    (interpolationTermTrace D value t z).2.length =
      Fintype.card κ * ((2 * (D + 1) + 2) * D + 2) + 1 := by
  simp [interpolationTermTrace, ArithmeticExpr.run_eq, prodExpr_operations,
    ArithmeticExpr.operations, List.length_flatMap, List.map_map, Function.comp_def,
    interpolationWeightTrace_length]
  ring

/-- The trace includes interpolation arithmetic; each oracle value is read once
per grid node. The caller separately accounts for producing those grid values. -/
def interpolateCoefficientTrace (D : ℕ)
    (values : (κ → Fin (D + 1)) → ℚ) (z : κ → Fin (D + 1)) :
    ℚ × List ArithmeticEvent :=
  let terms := (interpolationGridList κ D).map
    (fun t => interpolationTermTrace D (values t) t z)
  let total := (sumExpr (terms.map (fun t => .atom t.1))).run
  (total.1, terms.flatMap Prod.snd ++ total.2)

theorem interpolateCoefficientTrace_value (D : ℕ)
    (values : (κ → Fin (D + 1)) → ℚ) (z : κ → Fin (D + 1)) :
    (interpolateCoefficientTrace D values z).1 = interpolateCoefficientRun D values z := by
  simp [interpolateCoefficientTrace, ArithmeticExpr.run_eq, List.map_map, Function.comp_def,
    ArithmeticExpr.eval, interpolationTermTrace_value,
    interpolationGridList_sum, interpolateCoefficientRun]

theorem interpolateCoefficientTrace_length (D : ℕ)
    (values : (κ → Fin (D + 1)) → ℚ) (z : κ → Fin (D + 1)) :
    (interpolateCoefficientTrace D values z).2.length =
      (D + 1) ^ Fintype.card κ *
        (Fintype.card κ * ((2 * (D + 1) + 2) * D + 2) + 2) := by
  simp [interpolateCoefficientTrace, ArithmeticExpr.run_eq, sumExpr_operations,
    ArithmeticExpr.operations, List.length_flatMap, List.map_map, Function.comp_def,
    interpolationTermTrace_length, interpolationGridList_length]
  ring

end OrderedCoordinates
end MatroidSpectral
