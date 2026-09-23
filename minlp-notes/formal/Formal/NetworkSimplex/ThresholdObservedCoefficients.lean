import Formal.NetworkSimplex.ThresholdObservedReal
import Formal.NetworkSimplex.ThresholdAffineSubstitution
import Formal.NetworkSimplex.ThresholdUnitDescription

/-! Actual affine pullback from observed-state compression to original coordinates. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
variable {m : ℕ} {I : Type*}

/-- Retained coordinates have their original indices. This auxiliary map sends
state zero to state zero; its affine substitution is handled separately below. -/
def observedCoordinate (J : Finset (Fin m)) : Coordinate J.card I → Coordinate m I
  | .bypassFlow => .bypassFlow
  | .aFlow i => .aFlow i
  | .bFlow i => .bFlow i
  | .aProduct i j => .aProduct i (observedIndex J j).val
  | .bProduct i j => .bProduct i (observedIndex J j).val
  | .bypassProduct j => .bypassProduct (observedIndex J j).val
  | .weight j => .weight (Fin.cases 0 (fun k => (observedIndex J k).val.succ) j)

/-- Merged residual mass is exactly one minus the retained explicit weights.
Only weight expressions change; flows and retained products are direct lookups. -/
def observedSubstitution (J : Finset (Fin m)) :
    Coordinate J.card I → AffineExpression (Coordinate m I)
  | .weight j => Fin.cases
      (.add (.constant 1) (.neg (AffineExpression.sum fun k : Fin J.card =>
        .variable (.weight (observedIndex J k).val.succ))))
      (fun k => .variable (.weight (observedIndex J k).val.succ)) j
  | q => .variable (observedCoordinate J q)

def observedPullback (J : Finset (Fin m)) (e : AffineExpression (Coordinate J.card I)) :
    AffineExpression (Coordinate m I) := e.substitute (observedSubstitution J)

theorem observedSubstitution_eval {L : ℕ} (J : Finset (Fin m))
    (E : ReductionData m (Fin L)) (q : Coordinate J.card (Fin L)) :
    (observedSubstitution J q).eval (coordinates E E.xb) =
      coordinates (E.compressObserved J) (E.compressObserved J).xb q := by
  cases q with
  | weight j => refine Fin.cases ?_ (fun k => ?_) j <;>
      simp [observedSubstitution, AffineExpression.eval, coordinates,
        ReductionData.compressObserved, sub_eq_add_neg]
  | _ => rfl

theorem observedPullback_eval {L : ℕ} (J : Finset (Fin m))
    (e : AffineExpression (Coordinate J.card (Fin L))) (E : ReductionData m (Fin L)) :
    (observedPullback J e).eval (coordinates E E.xb) =
      e.eval (coordinates (E.compressObserved J) (E.compressObserved J).xb) := by
  rw [observedPullback, AffineExpression.eval_substitute]
  congr 1
  funext q
  exact observedSubstitution_eval J E q

private theorem observedIndex_val_injective (J : Finset (Fin m)) :
    Function.Injective (fun j => (observedIndex J j).val) :=
  Subtype.val_injective.comp (observedIndex J).injective

/-- At a retained flow or product coordinate, every substituted variable has the
same coefficient as its original compressed variable. -/
theorem observedSubstitution_coefficient_image [DecidableEq I] (J : Finset (Fin m))
    (q : Coordinate J.card I) (hq : FlowOrProduct q) (s : Coordinate J.card I) :
    (observedSubstitution J s).coefficient (observedCoordinate J q) = if s = q then 1 else 0 := by
  have hinj := observedIndex_val_injective J
  have he (j k : Fin J.card) : (observedIndex J j).val = (observedIndex J k).val ↔ j = k :=
    hinj.eq_iff
  cases s with
  | weight j =>
    refine Fin.cases ?_ (fun k => ?_) j
    all_goals cases q <;> simp_all [FlowOrProduct, observedSubstitution,
      observedCoordinate, AffineExpression.coefficient]
  | _ => cases q <;> simp_all [FlowOrProduct, observedSubstitution,
      observedCoordinate, AffineExpression.coefficient]

/-- Retained flow/product coefficients are preserved exactly. -/
theorem observedPullback_coefficient_image [DecidableEq I] (J : Finset (Fin m))
    (e : AffineExpression (Coordinate J.card I)) (q : Coordinate J.card I)
    (hq : FlowOrProduct q) :
    (observedPullback J e).coefficient (observedCoordinate J q) = e.coefficient q := by
  exact AffineExpression.coefficient_substitute (observedSubstitution J) q
    (observedCoordinate J q) (observedSubstitution_coefficient_image J q hq) e

/-- An omitted explicit label occurs in no substituted flow/product expression. -/
theorem observedSubstitution_omitted [DecidableEq I] (J : Finset (Fin m))
    (j : Fin m) (hj : j ∉ J) (s : Coordinate J.card I) :
    (∀ i, (observedSubstitution J s).coefficient (.aProduct i j) = 0 ∧
      (observedSubstitution J s).coefficient (.bProduct i j) = 0) ∧
      (observedSubstitution J s).coefficient (.bypassProduct j) = 0 := by
  have hne (k : Fin J.card) : (observedIndex J k).val ≠ j := by
    intro he
    exact hj (he ▸ (observedIndex J k).property)
  cases s with
  | weight k => refine Fin.cases ?_ (fun l => ?_) k <;>
      simp [observedSubstitution, AffineExpression.coefficient]
  | _ => simp [observedSubstitution, observedCoordinate, AffineExpression.coefficient, hne]

/-- Pulling back through observed-label compression preserves the unit bounds.
Omitted product coordinates receive coefficient zero. -/
theorem observedPullback_unit [DecidableEq I] (J : Finset (Fin m))
    (e : AffineExpression (Coordinate J.card I)) (he : UnitFlowProducts e) :
    UnitFlowProducts (observedPullback J e) := by
  intro z hz
  have retained (q : Coordinate J.card I) (hq : FlowOrProduct q) :
      -1 ≤ (observedPullback J e).coefficient (observedCoordinate J q) ∧
      (observedPullback J e).coefficient (observedCoordinate J q) ≤ 1 := by
    rw [observedPullback_coefficient_image J e q hq]
    exact he q hq
  cases z with
  | bypassFlow => exact retained .bypassFlow trivial
  | aFlow i => exact retained (.aFlow i) trivial
  | bFlow i => exact retained (.bFlow i) trivial
  | weight j => exact False.elim hz
  | aProduct i j =>
    by_cases hj : j ∈ J
    · let k := (observedIndex J).symm ⟨j, hj⟩
      have hk : (observedIndex J k).val = j := by simp [k]
      simpa only [observedCoordinate, hk] using retained (.aProduct i k) trivial
    · have hh := AffineExpression.coefficient_substitute_zero (observedSubstitution J)
        (.aProduct i j) (fun s => ((observedSubstitution_omitted J j hj s).1 i).1) e
      change (observedPullback J e).coefficient (.aProduct i j) = 0 at hh
      rw [hh]; norm_num
  | bProduct i j =>
    by_cases hj : j ∈ J
    · let k := (observedIndex J).symm ⟨j, hj⟩
      have hk : (observedIndex J k).val = j := by simp [k]
      simpa only [observedCoordinate, hk] using retained (.bProduct i k) trivial
    · have hh := AffineExpression.coefficient_substitute_zero (observedSubstitution J)
        (.bProduct i j) (fun s => ((observedSubstitution_omitted J j hj s).1 i).2) e
      change (observedPullback J e).coefficient (.bProduct i j) = 0 at hh
      rw [hh]; norm_num
  | bypassProduct j =>
    by_cases hj : j ∈ J
    · let k := (observedIndex J).symm ⟨j, hj⟩
      have hk : (observedIndex J k).val = j := by simp [k]
      simpa only [observedCoordinate, hk] using retained (.bypassProduct k) trivial
    · have hh := AffineExpression.coefficient_substitute_zero (observedSubstitution J)
        (.bypassProduct j) (fun s => (observedSubstitution_omitted J j hj s).2) e
      change (observedPullback J e).coefficient (.bypassProduct j) = 0 at hh
      rw [hh]; norm_num

end NetworkSimplex.Chain.Threshold
