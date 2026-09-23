import Formal.NetworkSimplex.ThresholdDomainRows
import Formal.NetworkSimplex.ThresholdDomainRun

/-! Executable original-domain expressions and an explicit enumeration of their rows. -/
namespace NetworkSimplex.Chain.Threshold
namespace RationalData
variable {m L : ℕ}

/-- Original rational coordinates, including the opposite flow fixed by balance. -/
def coordinatesRat (D : RationalData m L) : Coordinate m (Fin L) → ℚ
  | .bypassFlow => D.xh
  | .aFlow i => D.xa i
  | .bFlow i => D.oppositeFlow i
  | .aProduct i j => D.u i j.succ
  | .bProduct i j => D.v i j.succ
  | .bypassProduct j => D.zh j.succ
  | .weight j => D.weights j

@[simp] theorem coordinatesRat_cast (D : RationalData m L) (c : Coordinate m (Fin L)) :
    (D.coordinatesRat c : ℝ) = coordinates D.toReal D.toReal.xb c := by
  cases c <;> simp [coordinatesRat, coordinates, toReal, oppositeFlow, ReductionData.xb]

/-- Computable syntax for each original-domain margin; the observation pattern alone
selects the syntax, while candidate values enter only when it is evaluated. -/
def domainExpressionRat (D : RationalData m L) :
    DomainRow m (Fin L) → AffineExpression (Coordinate m (Fin L))
  | .bypassLower => .variable .bypassFlow
  | .bypassUpper => .add (.constant 1) (.neg (.variable .bypassFlow))
  | .aLower i => .variable (.aFlow i)
  | .aUpper i => .add (.constant 1) (.neg (.variable (.aFlow i)))
  | .bLower i => .variable (.bFlow i)
  | .bUpper i => .add (.constant 1) (.neg (.variable (.bFlow i)))
  | .weightLower j => .variable (.weight j)
  | .aProductLower i j => if observesA (D.c i j.succ) then
      .variable (.aProduct i j) else .constant 0
  | .bProductLower i j => if observesB (D.c i j.succ) then
      .variable (.bProduct i j) else .constant 0
  | .bypassProductLower j => if D.observedH j.succ then
      .variable (.bypassProduct j) else .constant 0

@[simp] theorem domainExpressionRat_eq (D : RationalData m L) (r : DomainRow m (Fin L)) :
    D.domainExpressionRat r = domainExpression D.toReal r := by
  cases r <;> rfl

/-- Rational evaluation is exactly the real original-coordinate evaluation. -/
theorem domainExpressionRat_eval_cast (D : RationalData m L) (r : DomainRow m (Fin L)) :
    ((D.domainExpressionRat r).evalRat D.coordinatesRat : ℝ) =
      (domainExpression D.toReal r).eval (coordinates D.toReal D.toReal.xb) := by
  rw [AffineExpression.evalRat_cast, domainExpressionRat_eq]
  congr 1
  funext c
  exact coordinatesRat_cast D c

/-- The explicit traversal includes every flow box, simplex nonnegativity row,
and explicit-label observed-product nonnegativity row exactly once. -/
def domainTags (m L : ℕ) : List (DomainRow m (Fin L)) :=
  [.bypassLower, .bypassUpper] ++
    (List.ofFn fun i : Fin L => [DomainRow.aLower i, .aUpper i, .bLower i, .bUpper i]).flatten ++
    List.ofFn (fun j : Fin (m + 1) => .weightLower j) ++
    (List.ofFn fun i : Fin L => List.ofFn fun j : Fin m => DomainRow.aProductLower i j).flatten ++
    (List.ofFn fun i : Fin L => List.ofFn fun j : Fin m => DomainRow.bProductLower i j).flatten ++
    List.ofFn (fun j : Fin m => .bypassProductLower j)

@[simp] theorem mem_domainTags (r : DomainRow m (Fin L)) : r ∈ domainTags m L := by
  cases r <;> simp [domainTags, List.mem_flatten, List.mem_ofFn, em]

@[simp] theorem domainTags_length :
    (domainTags m L).length = 2 + 4 * L + (m + 1) + 2 * m * L + m := by
  simp [domainTags, List.length_flatten, List.map_ofFn, List.sum_ofFn,
    Finset.sum_const, mul_comm]
  ring

/-- Quantifying over the generated list is exactly quantifying over all original-domain rows. -/
theorem forall_domainTags (P : DomainRow m (Fin L) → Prop) :
    (∀ r ∈ domainTags m L, P r) ↔ ∀ r, P r := by
  exact ⟨fun h r => h r (mem_domainTags r), fun h r _ => h r⟩

end RationalData
end NetworkSimplex.Chain.Threshold
