import Formal.ReciprocalAnchor.Model

namespace ReciprocalAnchor

/-- A fixed anchor leaves only the normalized leaf coordinate free. -/
theorem graph_degenerate_convex (a : ℝ) : Convex ℝ (graph a a) := by
  rintro p ⟨x, y, hx0, hx1, hy0, hy1, rfl⟩
    p' ⟨x', y', hx0', hx1', hy0', hy1', rfl⟩ r s hr hs hrs
  have hx : x = a := le_antisymm hx1 hx0
  have hx' : x' = a := le_antisymm hx1' hx0'
  subst x
  subst x'
  refine ⟨a, r * y + s * y', le_rfl, le_rfl,
    add_nonneg (mul_nonneg hr hy0) (mul_nonneg hs hy0'), ?_, ?_⟩
  · nlinarith [mul_le_mul_of_nonneg_left hy1 hr, mul_le_mul_of_nonneg_left hy1' hs]
  · ext i
    fin_cases i
    · change r * a + s * a = a
      rw [← add_mul, hrs, one_mul]
    · change r * (1 / a) + s * (1 / a) = 1 / a
      rw [← add_mul, hrs, one_mul]
    · rfl
    · change r * (a * y) + s * (a * y') = a * (r * y + s * y')
      ring

/-- When the anchor interval collapses, its graph is already convex. -/
theorem hull_degenerate (a : ℝ) : hull a a = graph a a :=
  (graph_degenerate_convex a).convexHull_eq

/-- The exact linear hull in the omitted zero-width interval case. -/
theorem mem_hull_degenerate_iff (a m t q w : ℝ) :
    point m t q w ∈ hull a a ↔ m = a ∧ t = 1 / a ∧ 0 ≤ q ∧ q ≤ 1 ∧ w = a * q := by
  rw [hull_degenerate]
  constructor
  · rintro ⟨x, y, hx0, hx1, hy0, hy1, he⟩
    have hx : x = a := le_antisymm hx1 hx0
    subst x
    have hm := congr_fun he 0
    have ht := congr_fun he 1
    have hq := congr_fun he 2
    have hw := congr_fun he 3
    change m = a at hm
    change t = 1 / a at ht
    change q = y at hq
    change w = a * y at hw
    exact ⟨hm, ht, hq.symm ▸ hy0, hq.symm ▸ hy1, hw.trans (congrArg (a * ·) hq.symm)⟩
  · rintro ⟨rfl, rfl, hq0, hq1, rfl⟩
    exact ⟨_, q, le_rfl, le_rfl, hq0, hq1, rfl⟩

end ReciprocalAnchor
