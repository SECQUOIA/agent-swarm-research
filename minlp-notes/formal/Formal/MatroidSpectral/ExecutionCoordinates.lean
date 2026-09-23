import Formal.MatroidSpectral.ProfileCardinality
import Mathlib.Data.Nat.Pairing

namespace MatroidSpectral.Execution

/-- Order the explicitly labelled upper triangle by a computable natural key. -/
@[instance_reducible] private def coordinateOrder (r : ℕ) :
    LinearOrder (DAGSpectral.UpperCoord r) :=
  LinearOrder.lift' (fun i => Nat.pair i.1.val i.2.val) (by
    intro ⟨j,i⟩ ⟨k,l⟩ h
    obtain ⟨hj,hi⟩ := Nat.pair_eq_pair.mp h
    have he : j = k := Fin.ext hj
    subst k
    have he : i = l := Fin.ext hi
    subst l
    rfl)

instance upperCoordLinearOrder (r : ℕ) : LinearOrder (DAGSpectral.UpperCoord r) :=
  { coordinateOrder r with
    toDecidableEq := upperCoordDecidableEq r
    compare_eq_compareOfLessAndEq := by
      have he : upperCoordDecidableEq r = (coordinateOrder r).toDecidableEq :=
        Subsingleton.elim _ _
      intro a b
      exact ((coordinateOrder r).compare_eq_compareOfLessAndEq a b).trans
        (congrArg (fun d => @compareOfLessAndEq _ a b (coordinateOrder r).toLT
          ((coordinateOrder r).toDecidableLT a b) d) he.symm) }

end MatroidSpectral.Execution
