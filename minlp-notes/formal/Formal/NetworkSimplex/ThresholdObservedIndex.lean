import Formal.NetworkSimplex.ThresholdMergeObserved
import Formal.NetworkSimplex.ThresholdExtension
import Formal.NetworkSimplex.ThresholdObservedWork
import Formal.NetworkSimplex.ThresholdRationalRows

/-! Exact finite reindexing of the structurally observed labels. -/
namespace NetworkSimplex
open scoped BigOperators

/-- Increasing observed-label enumeration. The cardinality depends on structural
observations, not on whether an observed label has positive weight. -/
def observedIndex {m : ℕ} (J : Finset (Fin m)) : Fin J.card ≃ {j // j ∈ J} :=
  (J.orderIsoOfFin rfl).toEquiv

def observedStateIndex {m : ℕ} (J : Finset (Fin m)) :
    Option {j // j ∈ J} ≃ Fin (J.card + 1) :=
  (Equiv.optionCongr (observedIndex J).symm).trans (finSuccEquiv J.card).symm

@[simp] theorem observedStateIndex_none {m : ℕ} (J : Finset (Fin m)) :
    observedStateIndex J none = 0 := by
  change (finSuccEquiv J.card).symm none = 0
  exact finSuccEquiv_symm_none

@[simp] theorem observedStateIndex_some {m : ℕ} (J : Finset (Fin m)) (j : {j // j ∈ J}) :
    observedStateIndex J (some j) = ((observedIndex J).symm j).succ := by
  change (finSuccEquiv J.card).symm (some ((observedIndex J).symm j)) = _
  exact finSuccEquiv_symm_some _

/-- Original-coordinate compression retains every flow and product coordinate. -/
def observedPoint {E O : Type*} {m : ℕ} (J : Finset (Fin m))
    (p : OriginalPoint E O m) : OriginalPoint E O J.card :=
  (p.1, (fun j => p.2.1 (observedIndex J j).val, p.2.2))

theorem observedPoint_lift {E O : Type*} {m : ℕ} (J : Finset (Fin m))
    (p : OriginalPoint E O m) (hp : OriginalSimplex p.2.1) :
    liftPoint (observedPoint J p) =
      relabelPoint (observedStateIndex J) (mergedPoint (observedGroup J) (liftPoint p)) := by
  change (p.1, _) = (p.1, _)
  congr 1
  apply Prod.ext
  swap
  · rfl
  funext k
  refine Fin.cases ?_ (fun j => ?_) k
  · change 1 - ∑ j, p.2.1 (observedIndex J j).val =
      groupSum (observedGroup J) (residualWeights p.2.1)
        ((observedStateIndex J).symm 0)
    have hi : (observedStateIndex J).symm 0 = none :=
      (observedStateIndex J).symm_apply_eq.mpr (observedStateIndex_none J).symm
    rw [hi, merged_residual_weight J _ ((residualWeights_simplex _).mpr hp)]
    congr 1
    exact (observedIndex J).sum_comp (fun j => p.2.1 j.val)
  · change p.2.1 (observedIndex J j).val =
      groupSum (observedGroup J) (residualWeights p.2.1)
        ((observedStateIndex J).symm j.succ)
    have hi : (observedStateIndex J).symm j.succ = some (observedIndex J j) := by
      apply (observedStateIndex J).symm_apply_eq.mpr
      simp
    rw [hi, observed_weight]
    rfl

/-- The compressed problem is literally an original-simplex problem with `a`
explicit labels. The original simplex condition must still be checked. -/
theorem original_hull_observed_index_iff {E V O : Type*} {m : ℕ}
    (J : Finset (Fin m)) (A : (E → ℝ) →ₗ[ℝ] (V → ℝ))
    (b : V → ℝ) (u : E → ℝ) (arc : O → E) (label : O → Fin m)
    (hJ : ∀ o, label o ∈ J) (p : OriginalPoint E O m) :
    p ∈ convexHull ℝ (OriginalGraph A b u arc label) ↔
      OriginalSimplex p.2.1 ∧ observedPoint J p ∈ convexHull ℝ
        (OriginalGraph A b u arc (fun o => (observedIndex J).symm ⟨label o, hJ o⟩)) := by
  rw [original_hull_observed_merge_iff J A b u arc label hJ p]
  apply and_congr_right
  intro hp
  rw [original_hull_iff_lift, observedPoint_lift J p hp]
  have he : (fun o => ((observedIndex J).symm ⟨label o, hJ o⟩).succ) =
      observedStateIndex J ∘ (fun o => some ⟨label o, hJ o⟩) := by
    funext o
    simp
  rw [he, relabel_mem_hull_iff]

namespace Chain.Threshold.RationalData

/-- Restrict observed states and merge all remaining mass with the residual.
The selected states are retained even when their weight is zero. -/
def compressObserved {m L : ℕ} (D : RationalData m L) (J : Finset (Fin m)) :
    RationalData J.card L where
  c i := Fin.cases .neither (fun j => D.c i (observedIndex J j).val.succ)
  u i := Fin.cases 0 (fun j => D.u i (observedIndex J j).val.succ)
  v i := Fin.cases 0 (fun j => D.v i (observedIndex J j).val.succ)
  weights := Fin.cases (1 - ∑ j : Fin J.card, D.weights (observedIndex J j).val.succ)
    (fun j => D.weights (observedIndex J j).val.succ)
  xa := D.xa
  xh := D.xh
  observedH := Fin.cases false (fun j => D.observedH (observedIndex J j).val.succ)
  zh := Fin.cases 0 (fun j => D.zh (observedIndex J j).val.succ)

@[simp] theorem compressObserved_residual_class {m L : ℕ} (D : RationalData m L)
    (J : Finset (Fin m)) (i : Fin L) : (D.compressObserved J).c i 0 = .neither := rfl

@[simp] theorem compressObserved_residual_bypass {m L : ℕ} (D : RationalData m L)
    (J : Finset (Fin m)) : (D.compressObserved J).observedH 0 = false := rfl

theorem compressObserved_weights_sum {m L : ℕ} (D : RationalData m L)
    (J : Finset (Fin m)) : ∑ j, (D.compressObserved J).weights j = 1 := by
  rw [Fin.sum_univ_succ]
  simp [compressObserved]

theorem compressObserved_weight {m L : ℕ} (D : RationalData m L)
    (J : Finset (Fin m)) (j : Fin J.card) :
    (D.compressObserved J).weights j.succ = D.weights (observedIndex J j).val.succ := rfl

end Chain.Threshold.RationalData
end NetworkSimplex
