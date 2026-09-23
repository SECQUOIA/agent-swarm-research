import Formal.PotentialFlow.Bregman

/-! Curvature floors of the asymmetric cubic edge energy and the resulting
conservation-aware quadratic certificates.

The second derivative of the edge energy is `2 c_e^{sgn t} |t|`, so a verified
interval `[l_e, u_e]` that stays on one side of the origin supplies a strictly
positive lower bound for it. `curvatureFloor` is that bound, and it is zero
exactly when the interval straddles the origin.

The module proves the scalar Taylor estimate `h_e (y - z)^2 / 2 ≤ D_e(y, z)` on
such an interval, the summed quadratic error bound `(1/2) ∑ h_e (x*_e - y_e)^2 ≤ δ`
for a verified energy gap `δ`, and the goal radius `|wᵀ(x* - y)| ≤ r` whenever
`r ≥ 0` and `r^2 ≥ 2 δ C`, where `C` is the Laplacian factor of a residual
`s = w - Aᵀv` that vanishes on the zero-curvature edges. A zero verified gap
forces `x* = y`, so every goal is then exact. -/

namespace PotentialFlow

noncomputable section

/-- The minimum of the edge-energy second derivative `2 c^{sgn t} |t|` over the
interval `[l, u]`, as used by `eq:a-cert-curvature`. It is zero exactly when the
interval contains the origin. -/
def curvatureFloor (cp cm l u : ℝ) : ℝ :=
  if 0 < l then 2 * cp * l else if u < 0 then -(2 * cm * u) else 0

/-- The curvature floor of an edge with nonnegative coefficients is nonnegative.
No relation between `l` and `u` is needed. -/
theorem curvatureFloor_nonneg {cp cm : ℝ} (hcp : 0 ≤ cp) (hcm : 0 ≤ cm) (l u : ℝ) :
    0 ≤ curvatureFloor cp cm l u := by
  unfold curvatureFloor
  split_ifs with hl hu
  · positivity
  · nlinarith
  · exact le_rfl

/-- Scalar Taylor bound of `thm:a-cert-hessian`: on an interval `[l, u]` containing
both points, the curvature floor is a valid quadratic lower bound for the edge
Bregman divergence. The interval may straddle the origin, in which case the floor
is `0` and the statement reduces to nonnegativity of the divergence. -/
theorem curvatureFloor_le_edgeBregman {cp cm l u y z : ℝ} (hcp : 0 < cp) (hcm : 0 < cm)
    (hly : l ≤ y) (hyu : y ≤ u) (hlz : l ≤ z) (hzu : z ≤ u) :
    curvatureFloor cp cm l u / 2 * (y - z) ^ 2 ≤ edgeBregman cp cm y z := by
  unfold curvatureFloor
  split_ifs with hl hu
  · have hy0 : 0 ≤ y := hl.le.trans hly
    have hz0 : 0 ≤ z := hl.le.trans hlz
    have hE : edgeBregman cp cm y z = cp / 3 * ((y - z) ^ 2 * (y + 2 * z)) := by
      simp only [edgeBregman, edgeEnergy, edgeLaw, if_pos hy0, if_pos hz0,
        abs_of_nonneg hy0, abs_of_nonneg hz0]
      ring
    rw [hE]
    nlinarith [mul_nonneg (mul_nonneg hcp.le (sq_nonneg (y - z)))
      (by linarith : (0 : ℝ) ≤ y + 2 * z - 3 * l)]
  · have hy0 : y < 0 := hyu.trans_lt hu
    have hz0 : z < 0 := hzu.trans_lt hu
    have hE : edgeBregman cp cm y z = -(cm / 3) * ((y - z) ^ 2 * (y + 2 * z)) := by
      simp only [edgeBregman, edgeEnergy, edgeLaw, if_neg (not_le.mpr hy0),
        if_neg (not_le.mpr hz0), abs_of_neg hy0, abs_of_neg hz0]
      ring
    rw [hE]
    nlinarith [mul_nonneg (mul_nonneg hcm.le (sq_nonneg (y - z)))
      (by linarith : (0 : ℝ) ≤ 3 * u - y - 2 * z)]
  · simpa using edgeBregman_nonneg hcp hcm y z

namespace Network

variable {n m : ℕ} (G : Network n m)

/-- The difference of two feasible flows is annihilated by every vector of
potential drops, so a linear goal and its residual `s = w - Aᵀv` agree on it. -/
theorem sum_goal_eq_sum_residual_of_feasible {b : Fin n → ℝ} {x y w s : Fin m → ℝ} {v : Fin n → ℝ}
    (hx : G.Feasible b x) (hy : G.Feasible b y)
    (hs : ∀ e, s e = w e - G.drops v e) :
    ∑ e, w e * (x e - y e) = ∑ e, s e * (x e - y e) := by
  have hd : G.loads (x - y) = 0 := by
    change G.divergenceLinear (x - y) = 0
    rw [map_sub, show G.divergenceLinear x = b from hx,
      show G.divergenceLinear y = b from hy, sub_self]
  have hstat : ∑ e, G.drops v e * (x e - y e) = 0 := by
    simpa only [Pi.sub_apply] using G.potential_stationary v (x - y) hd
  have hsplit : ∑ e, s e * (x e - y e) =
      ∑ e, w e * (x e - y e) - ∑ e, G.drops v e * (x e - y e) := by
    rw [← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun e _ => by rw [hs e]; ring
  rw [hsplit, hstat, sub_zero]

/-- Equation `eq:a-cert-quadratic-error`: a verified energy gap `δ` bounds the
curvature-weighted quadratic error between the candidate and the minimizer. -/
theorem sum_curvature_le_gap (hc : G.Positive) {b : Fin n → ℝ} {x y l u h : Fin m → ℝ}
    {δ : ℝ} (hx : G.Feasible b x) (hy : G.Feasible b y)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z)
    (hδ : G.energy y - G.energy x ≤ δ)
    (hly : ∀ e, l e ≤ y e) (hyu : ∀ e, y e ≤ u e)
    (hlx : ∀ e, l e ≤ x e) (hxu : ∀ e, x e ≤ u e)
    (hh : ∀ e, h e = curvatureFloor (G.positive e) (G.negative e) (l e) (u e)) :
    (1 / 2) * ∑ e, h e * (x e - y e) ^ 2 ≤ δ := by
  have hterm : ∀ e : Fin m, h e / 2 * (x e - y e) ^ 2 ≤
      edgeBregman (G.positive e) (G.negative e) (y e) (x e) := by
    intro e
    have hb := curvatureFloor_le_edgeBregman (l := l e) (u := u e) (hc.1 e) (hc.2 e)
      (hly e) (hyu e) (hlx e) (hxu e)
    rw [hh e, show (x e - y e) ^ 2 = (y e - x e) ^ 2 by ring]
    exact hb
  calc (1 / 2) * ∑ e, h e * (x e - y e) ^ 2
      = ∑ e, h e / 2 * (x e - y e) ^ 2 := by
        rw [Finset.mul_sum]
        exact Finset.sum_congr rfl fun e _ => by ring
    _ ≤ ∑ e, edgeBregman (G.positive e) (G.negative e) (y e) (x e) :=
        Finset.sum_le_sum fun e _ => hterm e
    _ = G.energy y - G.energy x := (G.energy_sub_eq_sum_edgeBregman hx hy hmin).symm
    _ ≤ δ := hδ

/-- Equation `eq:a-cert-goal-radius`: with a verified gap `δ`, curvature floors `h`,
a residual `s = w - Aᵀv` vanishing on the zero-curvature edges, and the Laplacian
factor `C = ∑_{h_e ≠ 0} s_e^2 / h_e`, every `r ≥ 0` with `2 δ C ≤ r^2` certifies the
goal radius. Empty positive-curvature sets, `C = 0` and `r = 0` are included. -/
theorem abs_sum_goal_le (hc : G.Positive) {b : Fin n → ℝ} {x y l u h w s : Fin m → ℝ}
    {v : Fin n → ℝ} {δ C r : ℝ} (hx : G.Feasible b x) (hy : G.Feasible b y)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z)
    (hδ : G.energy y - G.energy x ≤ δ)
    (hly : ∀ e, l e ≤ y e) (hyu : ∀ e, y e ≤ u e)
    (hlx : ∀ e, l e ≤ x e) (hxu : ∀ e, x e ≤ u e)
    (hh : ∀ e, h e = curvatureFloor (G.positive e) (G.negative e) (l e) (u e))
    (hs : ∀ e, s e = w e - G.drops v e) (hZ : ∀ e, h e = 0 → s e = 0)
    (hC : C = ∑ e, if h e = 0 then 0 else s e ^ 2 / h e)
    (hr : 0 ≤ r) (hrC : 2 * δ * C ≤ r ^ 2) :
    |∑ e, w e * (x e - y e)| ≤ r := by
  classical
  have hnn : ∀ e : Fin m, 0 ≤ h e := fun e => by
    rw [hh e]; exact curvatureFloor_nonneg (hc.1 e).le (hc.2 e).le _ _
  set P : Finset (Fin m) := Finset.univ.filter fun e => h e ≠ 0 with hP
  have hmemP : ∀ e ∈ P, h e ≠ 0 := fun e he => (Finset.mem_filter.mp he).2
  have hsplit : ∑ e ∈ P, s e * (x e - y e) = ∑ e, s e * (x e - y e) := by
    refine Finset.sum_subset (Finset.filter_subset _ _) fun e _ he => ?_
    have hz : h e = 0 := by
      by_contra hne
      exact he (Finset.mem_filter.mpr ⟨Finset.mem_univ e, hne⟩)
    rw [hZ e hz, zero_mul]
  have hCf : ∑ e ∈ P, s e ^ 2 / h e = C := by
    rw [hC, hP, Finset.sum_filter]
    exact Finset.sum_congr rfl fun e _ => by by_cases he : h e = 0 <;> simp [he]
  have hCS : (∑ e ∈ P, s e * (x e - y e)) ^ 2 ≤
      (∑ e ∈ P, s e ^ 2 / h e) * ∑ e ∈ P, h e * (x e - y e) ^ 2 :=
    Finset.sum_sq_le_sum_mul_sum_of_sq_le_mul (r := fun e => s e * (x e - y e))
      (f := fun e => s e ^ 2 / h e) (g := fun e => h e * (x e - y e) ^ 2) P
      (fun e _ => div_nonneg (sq_nonneg _) (hnn e))
      (fun e _ => mul_nonneg (hnn e) (sq_nonneg _))
      (fun e he => by
        have hprod : s e ^ 2 / h e * (h e * (x e - y e) ^ 2) =
            (s e * (x e - y e)) ^ 2 := by
          field_simp [hmemP e he]
        exact hprod.ge)
  have hQP : ∑ e ∈ P, h e * (x e - y e) ^ 2 ≤ ∑ e, h e * (x e - y e) ^ 2 :=
    Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
      fun e _ _ => mul_nonneg (hnn e) (sq_nonneg _)
  have hQtot : ∑ e, h e * (x e - y e) ^ 2 ≤ 2 * δ := by
    have := G.sum_curvature_le_gap hc hx hy hmin hδ hly hyu hlx hxu hh
    linarith
  have hC0 : 0 ≤ C := by
    rw [← hCf]
    exact Finset.sum_nonneg fun e _ => div_nonneg (sq_nonneg _) (hnn e)
  have hsq : (∑ e, w e * (x e - y e)) ^ 2 ≤ r ^ 2 := by
    rw [G.sum_goal_eq_sum_residual_of_feasible hx hy hs, ← hsplit]
    calc (∑ e ∈ P, s e * (x e - y e)) ^ 2
        ≤ (∑ e ∈ P, s e ^ 2 / h e) * ∑ e ∈ P, h e * (x e - y e) ^ 2 := hCS
      _ ≤ C * (2 * δ) := by
          rw [hCf]
          exact mul_le_mul_of_nonneg_left (hQP.trans hQtot) hC0
      _ = 2 * δ * C := by ring
      _ ≤ r ^ 2 := hrC
  nlinarith [abs_nonneg (∑ e, w e * (x e - y e)),
    sq_abs (∑ e, w e * (x e - y e)), hsq, hr]

/-- A zero verified gap makes every linear goal exact, with no curvature, residual
or potential hypothesis: strict convexity already forces `x* = y`. -/
theorem goal_exact_of_energy_le (hc : G.Positive) {b : Fin n → ℝ} {x y : Fin m → ℝ}
    (hx : G.Feasible b x) (hy : G.Feasible b y)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z)
    (hle : G.energy y ≤ G.energy x) (w : Fin m → ℝ) :
    x = y ∧ ∑ e, w e * (x e - y e) = 0 := by
  have hxy : x = y := (G.eq_minimizer_of_energy_le hc hx hy hmin hle).symm
  refine ⟨hxy, ?_⟩
  rw [hxy]
  simp

end Network

end

end PotentialFlow
