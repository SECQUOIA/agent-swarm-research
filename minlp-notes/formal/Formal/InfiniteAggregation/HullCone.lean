import Formal.InfiniteAggregation.HullModel
import Formal.InfiniteAggregation.Good

/-! Separating the explicit hull regions with actual good multipliers. -/

noncomputable section

namespace InfiniteAggregation

private theorem weight_ne_zero_of_second_pos {w : Weight} (hw : 0 < w 1) : w ≠ 0 := by
  intro h
  rw [h] at hw
  simp at hw

private theorem coordinate_cone (i : Fin 2) :
    GoodCone (if i = 0 then ![1, 0, 0] else ![0, 1, 0]) := by
  fin_cases i <;> norm_num [GoodCone, Fin.forall_fin_succ] <;> rfl

/-- Strict validity against the whole rotated cone forces the strict scalar hull condition. -/
theorem strict_cone_tests {p q c : ℝ}
    (h : ∀ w : Weight, GoodCone w → w ≠ 0 → w 0 * p + w 1 * q - w 2 * c > 0) :
    0 < p ∧ 0 < q ∧ c < Real.sqrt (p * q) := by
  have hp : 0 < p := by
    have ht := h ![1, 0, 0] (coordinate_cone 0) (by
      intro heq
      have hh := congrFun heq 0
      norm_num at hh)
    simpa using ht
  have hq : 0 < q := by
    have ht := h ![0, 1, 0] (coordinate_cone 1) (by
      intro heq
      have hh := congrFun heq 1
      norm_num at hh)
    simpa using ht
  have hpq : 0 < p * q := mul_pos hp hq
  have hs : 0 < Real.sqrt (p * q) := Real.sqrt_pos.2 hpq
  have hs2 := Real.sq_sqrt hpq.le
  let w : Weight := ![q, p, 2 * Real.sqrt (p * q)]
  have hw : GoodCone w := by
    constructor
    · intro i
      fin_cases i
      · exact hq.le
      · exact hp.le
      · change 0 ≤ 2 * Real.sqrt (p * q)
        positivity
    · change (2 * Real.sqrt (p * q)) ^ 2 ≤ 4 * q * p
      nlinarith
  have ht := h w hw (weight_ne_zero_of_second_pos (by simpa [w] using hp))
  change q * p + p * q - 2 * Real.sqrt (p * q) * c > 0 at ht
  refine ⟨hp, hq, ?_⟩
  nlinarith

/-- Weak cone tests retain the degenerate cases with a zero norm slack. -/
theorem weak_cone_tests {p q c : ℝ}
    (h : ∀ w : Weight, GoodCone w → w ≠ 0 → 0 ≤ w 0 * p + w 1 * q - w 2 * c) :
    0 ≤ p ∧ 0 ≤ q ∧ c ≤ Real.sqrt (p * q) := by
  have hp : 0 ≤ p := by
    have ht := h ![1, 0, 0] (coordinate_cone 0) (by
      intro heq
      have hh := congrFun heq 0
      norm_num at hh)
    simpa using ht
  have hq : 0 ≤ q := by
    have ht := h ![0, 1, 0] (coordinate_cone 1) (by
      intro heq
      have hh := congrFun heq 1
      norm_num at hh)
    simpa using ht
  refine ⟨hp, hq, ?_⟩
  by_cases hc : c ≤ 0
  · exact hc.trans (Real.sqrt_nonneg _)
  have hc : 0 < c := lt_of_not_ge hc
  have hp' : 0 < p := by
    by_contra hn
    have hp0 : p = 0 := le_antisymm (not_lt.mp hn) hp
    let w : Weight := ![(q + 1) ^ 2, c ^ 2, 2 * (q + 1) * c]
    have hw : GoodCone w := by
      constructor
      · intro i
        fin_cases i
        · exact sq_nonneg (q + 1)
        · exact sq_nonneg c
        · change 0 ≤ 2 * (q + 1) * c
          positivity
      · change (2 * (q + 1) * c) ^ 2 ≤ 4 * (q + 1) ^ 2 * c ^ 2
        nlinarith
    have ht := h w hw (weight_ne_zero_of_second_pos (by simpa [w] using sq_pos_of_pos hc))
    change 0 ≤ (q + 1) ^ 2 * p + c ^ 2 * q - (2 * (q + 1) * c) * c at ht
    rw [hp0] at ht
    have hpos := mul_nonneg hq (sq_nonneg c)
    nlinarith [sq_pos_of_pos hc]
  have hq' : 0 < q := by
    by_contra hn
    have hq0 : q = 0 := le_antisymm (not_lt.mp hn) hq
    let w : Weight := ![c ^ 2, (p + 1) ^ 2, 2 * (p + 1) * c]
    have hw : GoodCone w := by
      constructor
      · intro i
        fin_cases i
        · exact sq_nonneg c
        · exact sq_nonneg (p + 1)
        · change 0 ≤ 2 * (p + 1) * c
          positivity
      · change (2 * (p + 1) * c) ^ 2 ≤ 4 * c ^ 2 * (p + 1) ^ 2
        nlinarith
    have ht := h w hw (weight_ne_zero_of_second_pos (by change 0 < (p + 1) ^ 2; positivity))
    change 0 ≤ c ^ 2 * p + (p + 1) ^ 2 * q - (2 * (p + 1) * c) * c at ht
    rw [hq0] at ht
    have hpos := mul_nonneg hp (sq_nonneg c)
    nlinarith [sq_pos_of_pos hc]
  have hpq := mul_pos hp' hq'
  have hs : 0 < Real.sqrt (p * q) := Real.sqrt_pos.2 hpq
  have hs2 := Real.sq_sqrt hpq.le
  let w : Weight := ![q, p, 2 * Real.sqrt (p * q)]
  have hw : GoodCone w := by
    constructor
    · intro i
      fin_cases i
      · exact hq
      · exact hp
      · change 0 ≤ 2 * Real.sqrt (p * q)
        positivity
    · change (2 * Real.sqrt (p * q)) ^ 2 ≤ 4 * q * p
      nlinarith
  have ht := h w hw (weight_ne_zero_of_second_pos (by simpa [w] using hp'))
  change 0 ≤ q * p + p * q - 2 * Real.sqrt (p * q) * c at ht
  nlinarith

theorem goodCone_strict_intersection_subset_hullRegion {r : ℕ} :
    {x : Var r | ∀ w : Weight, GoodCone w → w ≠ 0 → aggregate w x < 0} ⊆ hullRegion r := by
  intro x hx
  have h := strict_cone_tests (p := 1 - qnorm x.1) (q := 1 - qnorm x.2)
    (c := 1 / 2 - dot x.1 x.2) (fun w hw hne => by
      have ht := hx w hw hne
      rw [aggregate_formula] at ht
      nlinarith)
  exact ⟨by linarith [h.1], by linarith [h.2.1], by linarith [h.2.2]⟩

theorem goodCone_weak_intersection_subset_closedRegion {r : ℕ} :
    {x : Var r | ∀ w : Weight, GoodCone w → w ≠ 0 → aggregate w x ≤ 0} ⊆ closedRegion r := by
  intro x hx
  have h := weak_cone_tests (p := 1 - qnorm x.1) (q := 1 - qnorm x.2)
    (c := 1 / 2 - dot x.1 x.2) (fun w hw hne => by
      have ht := hx w hw hne
      rw [aggregate_formula] at ht
      nlinarith)
  exact ⟨by linarith [h.1], by linarith [h.2.1], by linarith [h.2.2]⟩

theorem convexHull_subset_hullRegion {r : ℕ} :
    convexHull ℝ (feasible r) ⊆ hullRegion r := by
  intro x hx
  apply goodCone_strict_intersection_subset_hullRegion
  intro w hw hne
  exact goodCone_hull_valid hw hne hx

end InfiniteAggregation
