import Formal.PotentialFlow.Optimization

namespace PotentialFlow.Network

variable {n m : ℕ} (G : PotentialFlow.Network n m)

/-- A primal-dual certificate bounds every edge error at the true minimizer. -/
theorem certificate_radius {b p : Fin n → ℝ} {u y x : Fin m → ℝ}
    {a gap radius : ℝ} (ha : 0 < a)
    (hcp : ∀ e, a ≤ G.positive e) (hcm : ∀ e, a ≤ G.negative e)
    (hy : G.Feasible b y) (hx : G.Feasible b x)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z)
    (hu : ∀ e, 0 ≤ u e)
    (hroot : ∀ e, |G.drops p e| ^ 3 ≤ u e ^ 2 *
      (if 0 ≤ G.drops p e then G.positive e else G.negative e))
    (hgap : gap = G.energy y - G.dualLower b p u)
    (hr : 0 ≤ radius) (hbound : 6 * gap ≤ radius ^ 3 * a) :
    ∀ e, |y e - x e| ≤ radius := by
  have hc : G.Positive := ⟨fun e => ha.trans_le (hcp e), fun e => ha.trans_le (hcm e)⟩
  have hg : G.energy y - G.energy x ≤ gap := by
    rw [hgap]
    exact G.energy_error_le_gap hc hx hu hroot
  intro e
  have hb := G.energy_minimizer_gap ha hcp hcm hx hy hmin e
  have hp : |y e - x e| ^ 3 ≤ radius ^ 3 := by nlinarith
  exact (pow_le_pow_iff_left₀ (abs_nonneg _) hr (by decide : 3 ≠ 0)).mp hp

/-- The flow enclosure also encloses every physical pressure drop. -/
theorem certificate_pressure {y x : Fin m → ℝ} {radius : ℝ}
    (hc : G.Positive) (h : ∀ e, |y e - x e| ≤ radius) :
    ∀ e, PotentialFlow.edgeLaw (G.positive e) (G.negative e) (y e - radius) ≤
      PotentialFlow.edgeLaw (G.positive e) (G.negative e) (x e) ∧
      PotentialFlow.edgeLaw (G.positive e) (G.negative e) (x e) ≤
      PotentialFlow.edgeLaw (G.positive e) (G.negative e) (y e + radius) := by
  intro e
  have he := abs_le.mp (h e)
  have hmono := PotentialFlow.edgeLaw_monotone (hc.1 e).le (hc.2 e).le
  exact ⟨hmono (by linarith), hmono (by linarith)⟩

end PotentialFlow.Network
