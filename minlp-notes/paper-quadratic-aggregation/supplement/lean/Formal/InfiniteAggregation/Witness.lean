import Formal.InfiniteAggregation.GoodConvex
import Formal.InfiniteAggregation.Rays

/-! Real vector witnesses and indispensable strict aggregation rays. -/

noncomputable section

namespace InfiniteAggregation

open Set

theorem rayWeight_goodCone {τ : ℝ} (hτ : 0 < τ) : GoodCone (rayWeight τ) := by
  constructor
  · intro i
    fin_cases i <;> simp [rayWeight, le_of_lt hτ, inv_nonneg.mpr (le_of_lt hτ)]
  · change (2 : ℝ) ^ 2 ≤ 4 * τ * τ⁻¹
    field_simp
    norm_num

theorem rayWeight_ne_zero (τ : ℝ) : rayWeight τ ≠ 0 := by
  intro h
  have h2 := congrFun h 2
  change (2 : ℝ) = 0 at h2
  norm_num at h2

/-- Prescribed positive definite Gram data are realized in the original variables. -/
theorem witness_exists {r : ℕ} (hr : 2 ≤ r) {τ : ℝ}
    (hτ : τ ∈ Icc (1 : ℝ) 2) :
    ∃ x : Var r, qnorm x.1 = 1 - (1 / 10 : ℝ) / τ ∧
      qnorm x.2 = 1 - (1 / 10 : ℝ) * τ ∧ dot x.1 x.2 = 2 / 5 := by
  obtain ⟨hp, hd⟩ := witness_gram_bounds hτ
  obtain ⟨u, v, hu, hv, huv⟩ := gram_realization hr hp hd.le
  exact ⟨(u, v), hu, hv, huv⟩

/-- The three residuals at the witness have the exact claimed values. -/
theorem witness_eval_formula {r : ℕ} {τ : ℝ} {x : Var r}
    (hp : qnorm x.1 = 1 - (1 / 10 : ℝ) / τ)
    (hq : qnorm x.2 = 1 - (1 / 10 : ℝ) * τ)
    (hc : dot x.1 x.2 = 2 / 5) :
    eval x = (1 / 10 : ℝ) • ![-τ⁻¹, -τ, 1] := by
  ext i
  fin_cases i <;> simp [eval, hp, hq, hc] <;> ring

theorem witness_aggregate_formula {r : ℕ} {τ : ℝ} {x : Var r}
    (hp : qnorm x.1 = 1 - (1 / 10 : ℝ) / τ)
    (hq : qnorm x.2 = 1 - (1 / 10 : ℝ) * τ)
    (hc : dot x.1 x.2 = 2 / 5) (w : Weight) :
    aggregate w x = (1 / 10 : ℝ) * (-w 0 / τ - w 1 * τ + w 2) := by
  rw [aggregate_formula, hp, hq, hc]
  ring

/-- A concrete witness is tight on exactly its own good multiplier ray. -/
theorem witness_slack {r : ℕ} {τ : ℝ} (hτ : 0 < τ) {x : Var r}
    (hp : qnorm x.1 = 1 - (1 / 10 : ℝ) / τ)
    (hq : qnorm x.2 = 1 - (1 / 10 : ℝ) * τ)
    (hc : dot x.1 x.2 = 2 / 5) {w : Weight}
    (hK : GoodCone w) (hw : w ≠ 0) :
    aggregate w x ≤ 0 ∧ (aggregate w x = 0 ↔ SameRay w τ) := by
  rw [witness_aggregate_formula hp hq hc]
  have hn := ray_slack_nonpos (hK.1 0) (hK.1 1) (hK.1 2) hK.2 hτ
  constructor
  · nlinarith
  · rw [mul_eq_zero]
    norm_num
    exact ray_slack_eq_iff hK.1 hw hK.2 hτ

/-- A witness fails hull membership while strictly satisfying every other good ray. -/
theorem witness_separates {r : ℕ} (hr : 2 ≤ r) {τ : ℝ}
    (hτ : τ ∈ Icc (1 : ℝ) 2) :
    ∃ x : Var r, x ∉ convexHull ℝ (feasible r) ∧
      ∀ w : Weight, GoodCone w → w ≠ 0 →
        (aggregate w x < 0 ↔ ¬SameRay w τ) := by
  obtain ⟨x, hp, hq, hc⟩ := witness_exists hr hτ
  have ht : 0 < τ := lt_of_lt_of_le (by norm_num) hτ.1
  refine ⟨x, ?_, ?_⟩
  · intro hx
    have hneg := goodCone_hull_valid (rayWeight_goodCone ht) (rayWeight_ne_zero τ) hx
    have heq := (witness_slack ht hp hq hc (rayWeight_goodCone ht)
      (rayWeight_ne_zero τ)).2.mpr ⟨1, by norm_num, by simp⟩
    linarith
  · intro w hK hw
    obtain ⟨hle, heq⟩ := witness_slack ht hp hq hc hK hw
    exact (lt_iff_le_and_ne).trans (by simp [hle, heq])

/-- Every exact strict aggregation description contains every witness ray. -/
theorem strict_description_contains_rays {r : ℕ} (hr : 2 ≤ r)
    {W : Set Weight} (hW : ∀ w ∈ W, GoodCone w ∧ w ≠ 0)
    (hexact : convexHull ℝ (feasible r) = {x | ∀ w ∈ W, aggregate w x < 0}) :
    ∀ τ ∈ Icc (1 : ℝ) 2, ∃ w ∈ W, SameRay w τ := by
  intro τ hτ
  obtain ⟨x, hx, hs⟩ := witness_separates hr hτ
  by_contra! h
  apply hx
  rw [hexact]
  intro w hw
  exact (hs w (hW w hw).1 (hW w hw).2).2 (h w hw)

end InfiniteAggregation
