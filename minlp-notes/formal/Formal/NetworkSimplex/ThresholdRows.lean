import Formal.NetworkSimplex.Reduction
import Formal.NetworkSimplex.Circuits

/-! Symbolic original-coordinate affine expressions for the actual reduced rows. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators

inductive Coordinate (m : ℕ) (I : Type*) where
  | bypassFlow
  | aFlow : I → Coordinate m I
  | bFlow : I → Coordinate m I
  | aProduct : I → Fin m → Coordinate m I
  | bProduct : I → Fin m → Coordinate m I
  | bypassProduct : Fin m → Coordinate m I
  | weight : Fin (m + 1) → Coordinate m I
  deriving DecidableEq, Fintype

inductive AffineExpression (C : Type*) where
  | constant : ℚ → AffineExpression C
  | variable : C → AffineExpression C
  | add : AffineExpression C → AffineExpression C → AffineExpression C
  | neg : AffineExpression C → AffineExpression C

namespace AffineExpression
variable {C : Type*}

def eval (x : C → ℝ) : AffineExpression C → ℝ
  | .constant a => (a : ℝ)
  | .variable c => x c
  | .add e f => e.eval x + f.eval x
  | .neg e => -e.eval x

def evalRat (x : C → ℚ) : AffineExpression C → ℚ
  | .constant a => a
  | .variable c => x c
  | .add e f => e.evalRat x + f.evalRat x
  | .neg e => -e.evalRat x

theorem evalRat_cast (x : C → ℚ) (e : AffineExpression C) :
    (e.evalRat x : ℝ) = e.eval (fun c => (x c : ℝ)) := by
  induction e with
  | constant a => rfl
  | «variable» c => rfl
  | add e f he hf => simp [evalRat, eval, he, hf]
  | neg e he => simp [evalRat, eval, he]

@[simp] theorem eval_ite (x : C → ℝ) (p : Prop) [Decidable p] (e f : AffineExpression C) :
    (if p then e else f).eval x = if p then e.eval x else f.eval x := by
  split_ifs <;> rfl

def coefficient [DecidableEq C] (c : C) : AffineExpression C → ℤ
  | .constant _ => 0
  | .variable d => if d = c then 1 else 0
  | .add e f => e.coefficient c + f.coefficient c
  | .neg e => -e.coefficient c

@[simp] theorem coefficient_ite [DecidableEq C] (c : C) (p : Prop) [Decidable p]
    (e f : AffineExpression C) :
    (if p then e else f).coefficient c = if p then e.coefficient c else f.coefficient c := by
  split_ifs <;> rfl

def sumList : List (AffineExpression C) → AffineExpression C
  | [] => .constant 0
  | e :: rest => .add e (sumList rest)

def sum {n : ℕ} (f : Fin n → AffineExpression C) : AffineExpression C :=
  sumList (List.ofFn f)

@[simp] theorem eval_sumList (x : C → ℝ) (es : List (AffineExpression C)) :
    (sumList es).eval x = (es.map (eval x)).sum := by
  induction es with
  | nil => simp [sumList, eval]
  | cons e es ih => simp [sumList, eval, ih]

@[simp] theorem coefficient_sumList [DecidableEq C] (c : C) (es : List (AffineExpression C)) :
    (sumList es).coefficient c = (es.map (coefficient c)).sum := by
  induction es with
  | nil => rfl
  | cons e es ih => simp [sumList, coefficient, ih]

@[simp] theorem eval_sum {n : ℕ} (x : C → ℝ) (f : Fin n → AffineExpression C) :
    (sum f).eval x = ∑ j, (f j).eval x := by
  simp [sum, List.map_ofFn, List.sum_ofFn]

@[simp] theorem coefficient_sum [DecidableEq C] {n : ℕ} (c : C)
    (f : Fin n → AffineExpression C) : (sum f).coefficient c = ∑ j, (f j).coefficient c := by
  simp [sum, List.map_ofFn, List.sum_ofFn]

/-- The recursively defined coefficient agrees with the response to changing one coordinate. -/
theorem eval_update [DecidableEq C] (e : AffineExpression C) (x : C → ℝ) (c : C) (d : ℝ) :
    e.eval (Function.update x c (x c + d)) = e.eval x + (e.coefficient c : ℝ) * d := by
  induction e with
  | constant a => simp [eval, coefficient]
  | «variable» a => by_cases h : a = c <;> simp [eval, coefficient, h, Function.update]
  | add e f he hf => simp only [eval, coefficient, Int.cast_add, he, hf]; ring
  | neg e he => simp only [eval, coefficient, Int.cast_neg, he]; ring
end AffineExpression

variable {m : ℕ} {I : Type*}

/-- Original coordinate values, with the unrecorded opposite flow supplied separately. -/
def coordinates (D : ReductionData m I) (xb : I → ℝ) : Coordinate m I → ℝ
  | .bypassFlow => D.xh
  | .aFlow i => D.xa i
  | .bFlow i => xb i
  | .aProduct i j => D.u i j.succ
  | .bProduct i j => D.v i j.succ
  | .bypassProduct j => D.zh j.succ
  | .weight j => D.weights j

open AffineExpression in
def residualExpression (D : ReductionData m I) (i : I) : AffineExpression (Coordinate m I) :=
  .add (.add (.variable (.aFlow i))
    (.neg (sum fun j => if observesA (D.c i j.succ) then
      .variable (.aProduct i j) else .constant 0)))
    (sum fun j => if D.c i j.succ = .bOnly then .variable (.bProduct i j) else .constant 0)

def totalExpression : AffineExpression (Coordinate m I) :=
  .add (.constant 1) (.neg (.variable .bypassFlow))

/-- Every row is the literal source row; no artificial box-subset rows are inserted. -/
def rowExpression (D : ReductionData m I) : ProfileRow m I → AffineExpression (Coordinate m I)
  | .lower _ => .constant 0
  | .upper j => .variable (.weight j.succ)
  | .totalLower => .add (.variable (.weight 0)) (.neg totalExpression)
  | .totalUpper => totalExpression
  | .bypassLower j => if D.observedH j.succ then
      .add (.variable (.bypassProduct j)) (.neg (.variable (.weight j.succ))) else .constant 0
  | .bypassUpper j => if D.observedH j.succ then
      .add (.variable (.weight j.succ)) (.neg (.variable (.bypassProduct j))) else .constant 0
  | .aLower i j => if D.c i j.succ = .aOnly then .neg (.variable (.aProduct i j)) else .constant 0
  | .bLower i j => if D.c i j.succ = .bOnly then .neg (.variable (.bProduct i j)) else .constant 0
  | .bothLower i j => if D.c i j.succ = .both then
      .neg (.add (.variable (.aProduct i j)) (.variable (.bProduct i j))) else .constant 0
  | .bothUpper i j => if D.c i j.succ = .both then
      .add (.variable (.aProduct i j)) (.variable (.bProduct i j)) else .constant 0
  | .endpointB i => residualExpression D i
  | .endpointA i => .add totalExpression (.neg (residualExpression D i))

theorem residualExpression_eval (D : ReductionData m I) (xb : I → ℝ) (i : I)
    (hc : D.c i 0 = .neither) :
    (residualExpression D i).eval (coordinates D xb) =
      residual (D.c i) (D.u i) (D.v i) (D.xa i) := by
  have he (j : Fin m) :
      AffineExpression.eval (coordinates D xb)
        (if observesA (D.c i j.succ) then .variable (.aProduct i j) else .constant 0) =
        if observesA (D.c i j.succ) then D.u i j.succ else 0 := by
    by_cases h : observesA (D.c i j.succ) <;> simp [h, AffineExpression.eval, coordinates]
  simp [residualExpression, AffineExpression.eval, coordinates, residual,
    Fin.sum_univ_succ, hc, he, sub_eq_add_neg, show ¬observesA StateClass.neither by decide]

theorem rowExpression_eval (D : ReductionData m I) (xb : I → ℝ)
    (hc : ∀ i, D.c i 0 = .neither) (r : ProfileRow m I) :
    (rowExpression D r).eval (coordinates D xb) = D.rowRhs r := by
  cases r <;> simp only [rowExpression, ReductionData.rowRhs] <;> (try split_ifs) <;>
    simp [totalExpression, AffineExpression.eval, coordinates, ReductionData.total,
      residualExpression_eval D xb _ (hc _), sub_eq_add_neg]

/-- Row expressions depend only on the observation pattern, not on the query values. -/
theorem rowExpression_eq_of_pattern_eq (D E : ReductionData m I)
    (hc : D.c = E.c) (hh : D.observedH = E.observedH) (r : ProfileRow m I) :
    rowExpression D r = rowExpression E r := by
  cases r <;> simp [rowExpression, residualExpression, hc, hh]

/-- A fixed source expression evaluates correctly at every point of the same instance. -/
theorem rowExpression_eval_other (D E : ReductionData m I) (xb : I → ℝ)
    (hpattern : D.c = E.c) (hh : D.observedH = E.observedH)
    (hc : ∀ i, E.c i 0 = .neither) (r : ProfileRow m I) :
    (rowExpression D r).eval (coordinates E xb) = E.rowRhs r := by
  rw [rowExpression_eq_of_pattern_eq D E hpattern hh r]
  exact rowExpression_eval E xb hc r

def rowCoefficient [DecidableEq I] (D : ReductionData m I) (r : ProfileRow m I)
    (c : Coordinate m I) : ℤ := (rowExpression D r).coefficient c

/-- The actual balance equation used to change an ambient inequality representative. -/
def balanceExpression (i : I) : AffineExpression (Coordinate m I) :=
  .add (.add (.add (.variable (.aFlow i)) (.variable (.bFlow i)))
    (.variable .bypassFlow)) (.constant (-1))

theorem balanceExpression_eval (D : ReductionData m I) (xb : I → ℝ) (i : I)
    (h : D.xa i + xb i = 1 - D.xh) :
    (balanceExpression (m := m) i).eval (coordinates D xb) = 0 := by
  simp only [balanceExpression, AffineExpression.eval, coordinates, Rat.cast_neg, Rat.cast_one]
  linarith

def normalVector : ProfileNormal m → Fin m → ℤ
  | .subset s, j => if j ∈ s then 1 else 0
  | .negativeSingleton k, j => if j = k then -1 else 0
  | .negativeTotal, _ => -1

/-- One actual source row is chosen for each participating normal. -/
def ThreeBranch (D : ReductionData 3 I) (c : Fin 16) (r : Fin 11 → ProfileRow 3 I) : Prop :=
  ∀ k, ThreeStateCircuits.weight c k ≠ 0 →
    normalVector (D.rowNormal (r k)) = ThreeStateCircuits.normal k

private theorem sum_predicate_indicator {n : ℕ} (p : Fin n → Prop) [DecidablePred p] (j : Fin n) :
    (∑ k, if p k then (if k = j then (1 : ℤ) else 0) else 0) = if p j then 1 else 0 := by
  rw [Finset.sum_eq_single j]
  · simp
  · intro k _ hk
    simp [hk]
  · simp

section Coefficients
variable [DecidableEq I]

@[simp] theorem residual_coefficient_bypass (D : ReductionData m I) (i : I) :
    (residualExpression D i).coefficient .bypassFlow = 0 := by
  simp [residualExpression, AffineExpression.coefficient, apply_ite]

@[simp] theorem residual_coefficient_aFlow (D : ReductionData m I) (i k : I) :
    (residualExpression D i).coefficient (.aFlow k) = if i = k then 1 else 0 := by
  simp [residualExpression, AffineExpression.coefficient, apply_ite]

@[simp] theorem residual_coefficient_bFlow (D : ReductionData m I) (i k : I) :
    (residualExpression D i).coefficient (.bFlow k) = 0 := by
  simp [residualExpression, AffineExpression.coefficient, apply_ite]

@[simp] theorem residual_coefficient_aProduct (D : ReductionData m I) (i k : I) (j : Fin m) :
    (residualExpression D i).coefficient (.aProduct k j) =
      if i = k ∧ observesA (D.c i j.succ) then -1 else 0 := by
  by_cases hik : i = k
  · subst k
    simp [residualExpression, AffineExpression.coefficient, apply_ite, sum_predicate_indicator]
  · simp [residualExpression, AffineExpression.coefficient, apply_ite, hik]

@[simp] theorem residual_coefficient_bProduct (D : ReductionData m I) (i k : I) (j : Fin m) :
    (residualExpression D i).coefficient (.bProduct k j) =
      if i = k ∧ D.c i j.succ = .bOnly then 1 else 0 := by
  by_cases hik : i = k
  · subst k
    simp [residualExpression, AffineExpression.coefficient, apply_ite, sum_predicate_indicator]
  · simp [residualExpression, AffineExpression.coefficient, apply_ite, hik]

@[simp] theorem residual_coefficient_bypassProduct (D : ReductionData m I) (i : I) (j : Fin m) :
    (residualExpression D i).coefficient (.bypassProduct j) = 0 := by
  simp [residualExpression, AffineExpression.coefficient, apply_ite]

end Coefficients
end NetworkSimplex.Chain.Threshold
