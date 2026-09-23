import Formal.InfiniteAggregation.Good
import Formal.InfiniteAggregation.Witness
import Formal.InfiniteAggregation.ClosedObstruction
import Formal.InfiniteAggregation.Cardinality

/-! The strict and closed obstruction theorems for the source notion of goodness. -/

noncomputable section

open Set

namespace InfiniteAggregation

theorem rayWeight_good {r : ℕ} (hr : 2 ≤ r) {τ : ℝ} (hτ : 0 < τ) :
    Good r (rayWeight τ) :=
  (good_iff_goodCone hr _).2 ⟨rayWeight_goodCone hτ, rayWeight_ne_zero τ⟩

/-- Exact strict descriptions must include every prescribed positive ray. -/
theorem good_strict_description_contains_rays {r : ℕ} (hr : 2 ≤ r)
    {W : Set Weight} (hW : ∀ w ∈ W, Good r w)
    (hexact : convexHull ℝ (feasible r) = {x | ∀ w ∈ W, aggregate w x < 0}) :
    ∀ τ ∈ Icc (1 : ℝ) 2, ∃ w ∈ W, SameRay w τ :=
  strict_description_contains_rays hr (fun w hw => (good_iff_goodCone hr w).1 (hW w hw))
    hexact

/-- This conclusion counts distinct rays by a scale-invariant normalization. -/
theorem good_strict_description_uncountable_rays {r : ℕ} (hr : 2 ≤ r)
    {W : Set Weight} (hW : ∀ w ∈ W, Good r w)
    (hexact : convexHull ℝ (feasible r) = {x | ∀ w ∈ W, aggregate w x < 0}) :
    ¬(normalizeRay '' W).Countable :=
  ray_cover_uncountable_normalized (good_strict_description_contains_rays hr hW hexact)

theorem no_countable_good_strict_description {r : ℕ} (hr : 2 ≤ r)
    {W : Set Weight} (hcount : W.Countable) (hW : ∀ w ∈ W, Good r w) :
    convexHull ℝ (feasible r) ≠ {x | ∀ w ∈ W, aggregate w x < 0} := by
  intro hexact
  exact good_strict_description_uncountable_rays hr hW hexact (hcount.image normalizeRay)

theorem no_finite_good_strict_description {r : ℕ} (hr : 2 ≤ r)
    {W : Set Weight} (hfinite : W.Finite) (hW : ∀ w ∈ W, Good r w) :
    convexHull ℝ (feasible r) ≠ {x | ∀ w ∈ W, aggregate w x < 0} :=
  no_countable_good_strict_description hr hfinite.countable hW

/-- Hull validity extends to weak validity on the closure by continuity. -/
theorem good_closedHull_valid {r : ℕ} {w : Weight} (hw : Good r w) {x : Var r}
    (hx : x ∈ closure (convexHull ℝ (feasible r))) : aggregate w x ≤ 0 := by
  apply closure_minimal (t := {y : Var r | aggregate w y ≤ 0}) ?_
    (isClosed_le (continuous_aggregate w) continuous_const) hx
  intro y hy
  exact (hw.2.2 y hy).le

theorem finite_good_closed_obstruction {r : ℕ} (hr : 2 ≤ r)
    {W : Set Weight} (hfinite : W.Finite) (hW : ∀ w ∈ W, Good r w) :
    ∃ x : Var r, (∀ w ∈ W, aggregate w x < 0) ∧
      x ∉ closure (convexHull ℝ (feasible r)) :=
  finite_goodCone_closed_obstruction hr hfinite
    (fun w hw => (good_iff_goodCone hr w).1 (hW w hw))

theorem no_finite_good_closed_description {r : ℕ} (hr : 2 ≤ r)
    {W : Set Weight} (hfinite : W.Finite) (hW : ∀ w ∈ W, Good r w) :
    closure (convexHull ℝ (feasible r)) ≠ {x | ∀ w ∈ W, aggregate w x ≤ 0} :=
  no_finite_goodCone_closed_description hr hfinite
    (fun w hw => (good_iff_goodCone hr w).1 (hW w hw))

end InfiniteAggregation
