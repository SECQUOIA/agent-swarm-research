import Formal.DAGSpectral.CriterionSelectContrast

namespace DAGSpectral
open scoped ENNReal NNReal

/-- Zero weights erase infinite costs before extended addition. -/
def rationalWeightedTerm (w : ℚ) (v : Option ℚ) : Option ℚ :=
  if w = 0 then some 0 else v.map (fun q => w * max q 0)

def rationalCostAdd : Option ℚ → Option ℚ → Option ℚ
  | some a, some b => some (max a 0 + max b 0)
  | _, _ => none

def rationalWeightedList : List (ℚ × Option ℚ) → Option ℚ
  | [] => some 0
  | (w,v)::xs => rationalCostAdd (rationalWeightedTerm w v) (rationalWeightedList xs)

theorem rationalCostAdd_value (a b : Option ℚ) :
    rationalCostValue (rationalCostAdd a b) = rationalCostValue a + rationalCostValue b := by
  cases a with
  | none => cases b <;> simp [rationalCostAdd,rationalCostValue]
  | some a =>
    cases b with
    | none => simp [rationalCostAdd,rationalCostValue]
    | some b =>
      simp only [rationalCostAdd,rationalCostValue,Rat.cast_add,Rat.cast_max,Rat.cast_zero]
      rw [ENNReal.ofReal_add (le_max_right _ _) (le_max_right _ _)]
      simp

theorem rationalWeightedTerm_value (w : ℚ) (hw : 0 ≤ w) (v : Option ℚ) :
    rationalCostValue (rationalWeightedTerm w v) =
      ENNReal.ofReal (w : ℝ) * rationalCostValue v := by
  by_cases hz : w = 0
  · simp [rationalWeightedTerm,hz,rationalCostValue]
  have hp : 0 < (w : ℝ) := by exact_mod_cast lt_of_le_of_ne hw (Ne.symm hz)
  cases v with
  | none =>
    simp [rationalWeightedTerm,hz,rationalCostValue,ENNReal.mul_top,
      ENNReal.ofReal_eq_zero,not_le.mpr hp]
  | some q =>
    simp only [rationalWeightedTerm,hz,↓reduceIte,Option.map_some,rationalCostValue,
      Rat.cast_mul,Rat.cast_max,Rat.cast_zero]
    rw [ENNReal.ofReal_mul hp.le]
    simp

theorem rationalWeightedList_value (xs : List (ℚ × Option ℚ))
    (hw : ∀ x ∈ xs, 0 ≤ x.1) :
    rationalCostValue (rationalWeightedList xs) =
      (xs.map fun x => ENNReal.ofReal (x.1 : ℝ) * rationalCostValue x.2).sum := by
  induction xs with
  | nil => simp [rationalWeightedList,rationalCostValue]
  | cons x xs ih =>
    rw [rationalWeightedList,rationalCostAdd_value,rationalWeightedTerm_value _ (hw x (by simp)),
      ih (fun y hy => hw y (by simp [hy]))]
    simp

def rationalWeightedContrastCost {n m : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ) : Option ℚ :=
  rationalWeightedList (List.ofFn fun i => (ws i,rationalContrastCost A (cs i)))

noncomputable def rationalWeights {m : ℕ} (ws : Fin m → ℚ) (hw : ∀ i, 0 ≤ ws i) :
    Fin m → ℝ≥0 := fun i => ⟨(ws i : ℝ), by exact_mod_cast hw i⟩

theorem rationalWeightedContrastCost_value {n m : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).PosSemidef) (cs : Fin m → Fin n → ℚ)
    (ws : Fin m → ℚ) (hw : ∀ i, 0 ≤ ws i) :
    rationalCostValue (rationalWeightedContrastCost A cs ws) =
      weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ)) (ratMatrixReal A) := by
  rw [rationalWeightedContrastCost,rationalWeightedList_value _ (by
    intro x hx
    obtain ⟨i,rfl⟩ := List.mem_ofFn.mp hx
    exact hw i)]
  simp only [List.map_ofFn,Function.comp_def,List.sum_ofFn,weightedContrastCost]
  apply Finset.sum_congr rfl
  intro i _
  rw [rationalContrastCost_value A hA]
  congr 1
  exact ENNReal.ofReal_eq_coe_nnreal (by exact_mod_cast hw i)

def weightedContrastCostLE {n m : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ)
    (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ) : Bool :=
  rationalCostLE (rationalWeightedContrastCost A cs ws) (rationalWeightedContrastCost B cs ws)

theorem weightedContrastCostLE_correct {n m : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).PosSemidef) (hB : (ratMatrixReal B).PosSemidef)
    (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ) (hw : ∀ i, 0 ≤ ws i) :
    weightedContrastCostLE A B cs ws = true ↔
      weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ)) (ratMatrixReal A) ≤
      weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ)) (ratMatrixReal B) := by
  rw [weightedContrastCostLE,rationalCostLE_correct,rationalWeightedContrastCost_value A hA,
    rationalWeightedContrastCost_value B hB]

def selectWeightedContrast {α : Type*} {n m : ℕ}
    (J : α → Matrix (Fin n) (Fin n) ℚ) (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ) :
    List α → Option α := bestBy (fun a b => weightedContrastCostLE (J b) (J a) cs ws)

theorem selectWeightedContrast_spec {α : Type*} {n m : ℕ}
    (J : α → Matrix (Fin n) (Fin n) ℚ) (cs : Fin m → Fin n → ℚ)
    (ws : Fin m → ℚ) (hw : ∀ i, 0 ≤ ws i) (xs : List α)
    (hJ : ∀ a ∈ xs, (ratMatrixReal (J a)).PosSemidef) {b : α}
    (hb : selectWeightedContrast J cs ws xs = some b) :
    b ∈ xs ∧ ∀ a ∈ xs,
      weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ)) (ratMatrixReal (J b)) ≤
      weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ))
        (ratMatrixReal (J a)) := by
  have hh := bestBy_spec (β := OrderDual ℝ≥0∞)
    (fun a b => weightedContrastCostLE (J b) (J a) cs ws)
    (fun a => weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ))
      (ratMatrixReal (J a)))
    (fun a => (ratMatrixReal (J a)).PosSemidef)
    (fun a ha b hb => weightedContrastCostLE_correct _ _ hb ha cs ws hw) xs hJ hb
  exact ⟨hh.1,hh.2.2⟩

theorem IsRelativeCover.selectWeightedContrast_guarantee {α : Type*} [DecidableEq α]
    {n m : ℕ} {η : ℝ} {J : α → Matrix (Fin n) (Fin n) ℚ} {F : Finset α} {xs : List α}
    (h : IsRelativeCover η (fun a => ratMatrixReal (J a)) F xs.toFinset)
    (hJ : ∀ a ∈ F, (ratMatrixReal (J a)).PosSemidef) (hη0 : 0 ≤ η) (hη1 : η < 1)
    (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ) (hw : ∀ i, 0 ≤ ws i)
    {b : α} (hb : selectWeightedContrast J cs ws xs = some b) :
    b ∈ F ∧ ∀ a ∈ F,
      weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ))
        (ratMatrixReal (J b)) ≤ ENNReal.ofReal ((1-η)⁻¹) *
      weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ))
        (ratMatrixReal (J a)) := by
  apply h.bestBy_guarantee (β := OrderDual ℝ≥0∞)
    (fun a b => weightedContrastCostLE (J b) (J a) cs ws)
    (fun a => weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ))
      (ratMatrixReal (J a)))
    (fun a => ENNReal.ofReal ((1-η)⁻¹) *
      weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ))
        (ratMatrixReal (J a)))
    (fun a ha b hb => weightedContrastCostLE_correct _ _ (hJ b hb) (hJ a ha) cs ws hw) ?_ hb
  intro a ha b hb hs
  exact hs.weightedContrastCost_upper (hJ a ha) (hJ b hb) hη0 hη1 _ _

end DAGSpectral
