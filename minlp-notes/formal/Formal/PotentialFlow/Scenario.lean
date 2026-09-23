import Formal.PotentialFlow.Optimization

/-!
# Posterior endpoint-scenario recovery

This module proves the posterior scenario results of `prop:a-cert-signs`
(obligations CC10-CC13 of the deterministic potential-flow certificate package).

* `edgeLaw_strong_monotone` (CC10) is the scalar strong-monotonicity inequality
  with cubic modulus, for arbitrary signs and at zero.
* `Scenario` bundles the data and hypotheses of the posterior argument: the
  envelope law, the selected endpoint-scenario law on the same directed graph,
  the selection rule driven by the signs of a trial flow, envelope membership of
  the coefficients, and verified flow intervals.
* `Scenario.constitutive_residual` (CC11) bounds the disagreement between the two
  edge laws at the envelope physical flow.
* `Scenario.scenario_error_sq` (CC12, per edge) and `Scenario.scenario_error_sup`
  (CC12, sup-norm form) bound the scenario flow error by the total residual.
* `Scenario.exact_of_compatible` (CC13) gives exact optimality under the
  compatibility alternatives of `eq:a-cert-compatible`.

Nothing in the argument uses connectivity: self-loops, parallel edges and
disconnected graphs are allowed throughout, and every boundary case (zero flows,
zero trial flow, degenerate intervals, zero residual) is covered.
-/

namespace PotentialFlow

noncomputable section

variable {n m : ℕ}

/-! ## Scalar strong monotonicity (CC10) -/

/-- The signed square is strongly monotone with cubic modulus and constant `1 / 2`. -/
private theorem cube_abs_le_signed_sq_sub (u v : ℝ) :
    |u - v| ^ 3 / 2 ≤ (u * |u| - v * |v|) * (u - v) := by
  rcases le_or_gt 0 u with hu | hu
  · rcases le_or_gt 0 v with hv | hv
    · rw [abs_of_nonneg hu, abs_of_nonneg hv]
      rcases abs_cases (u - v) with ⟨he, _⟩ | ⟨he, _⟩ <;> rw [he] <;>
        nlinarith [mul_nonneg (sq_nonneg (u - v)) hu, mul_nonneg (sq_nonneg (u - v)) hv]
    · have huv : 0 ≤ u - v := by linarith
      rw [abs_of_nonneg hu, abs_of_nonpos hv.le, abs_of_nonneg huv]
      nlinarith [mul_nonneg huv (sq_nonneg (u + v))]
  · rcases le_or_gt 0 v with hv | hv
    · have huv : u - v ≤ 0 := by linarith
      rw [abs_of_nonpos hu.le, abs_of_nonneg hv, abs_of_nonpos huv]
      nlinarith [mul_nonneg (neg_nonneg.mpr huv) (sq_nonneg (u + v))]
    · rw [abs_of_nonpos hu.le, abs_of_nonpos hv.le]
      rcases abs_cases (u - v) with ⟨he, _⟩ | ⟨he, _⟩ <;> rw [he] <;>
        nlinarith [mul_nonneg (sq_nonneg (u - v)) (neg_nonneg.mpr hu.le),
          mul_nonneg (sq_nonneg (u - v)) (neg_nonneg.mpr hv.le)]

/-- Splitting off a symmetric cubic part of the edge law. -/
private theorem edgeLaw_eq_add (cp cm a t : ℝ) :
    edgeLaw cp cm t = edgeLaw (cp - a) (cm - a) t + a * t * |t| := by
  unfold edgeLaw
  split_ifs <;> ring

/-- **CC10.** The edge law is strongly monotone with cubic modulus: for every
strictly positive lower bound `a` on both coefficients and all real `u`, `v`,
`a / 2 * |u - v| ^ 3 ≤ (G(u) - G(v)) * (u - v)`. Opposite signs and the value
zero are included. -/
theorem edgeLaw_strong_monotone {cp cm a : ℝ} (ha : 0 < a) (hcp : a ≤ cp) (hcm : a ≤ cm)
    (u v : ℝ) :
    a / 2 * |u - v| ^ 3 ≤ (edgeLaw cp cm u - edgeLaw cp cm v) * (u - v) := by
  have hmono := edgeLaw_monotone (cp := cp - a) (cm := cm - a) (by linarith) (by linarith)
  have hrest : 0 ≤ (edgeLaw (cp - a) (cm - a) u - edgeLaw (cp - a) (cm - a) v) * (u - v) := by
    rcases le_total v u with h | h
    · exact mul_nonneg (sub_nonneg.mpr (hmono h)) (by linarith)
    · nlinarith [sub_nonpos.mpr (hmono h)]
  have hcube := mul_le_mul_of_nonneg_left (cube_abs_le_signed_sq_sub u v) ha.le
  rw [edgeLaw_eq_add cp cm a u, edgeLaw_eq_add cp cm a v]
  nlinarith [hrest, hcube]

/-- The symmetric form of CC10 used for the selected scenario law. -/
theorem symmetric_strong_monotone {beta a : ℝ} (ha : 0 < a) (hb : a ≤ beta) (u v : ℝ) :
    a / 2 * |u - v| ^ 3 ≤ (beta * u * |u| - beta * v * |v|) * (u - v) := by
  simpa [edgeLaw] using edgeLaw_strong_monotone ha hb hb u v

namespace Network

variable (G : Network n m)

/-- A flow is *physical* for the law `G` and the nominations `b` when it conserves `b`
and its edge laws are realized by node potentials. -/
def IsPhysical (b : Fin n → ℝ) (x : Fin m → ℝ) : Prop :=
  G.Feasible b x ∧ ∃ p, G.drops p = fun e => edgeLaw (G.positive e) (G.negative e) (x e)

/-- A physical flow minimizes the energy on its conservation fiber. -/
theorem isPhysical_minimizer {b : Fin n → ℝ} {x : Fin m → ℝ} (hc : G.Positive)
    (h : G.IsPhysical b x) (z : Fin m → ℝ) (hz : G.Feasible b z) : G.energy x ≤ G.energy z := by
  obtain ⟨hx, p, hp⟩ := h
  exact G.physical_flow_minimizer hc hx hp z hz

/-- There is at most one physical flow for given nominations. -/
theorem isPhysical_unique {b : Fin n → ℝ} {x z : Fin m → ℝ} (hc : G.Positive)
    (hx : G.IsPhysical b x) (hz : G.IsPhysical b z) : x = z :=
  G.energy_minimizer_unique hc hx.1 hz.1 (G.isPhysical_minimizer hc hx)
    (G.isPhysical_minimizer hc hz)

/-- The edge laws of a physical flow annihilate every conserved circulation. -/
theorem isPhysical_stationary {b : Fin n → ℝ} {x : Fin m → ℝ} (h : G.IsPhysical b x)
    (d : Fin m → ℝ) (hd : G.loads d = 0) :
    ∑ e, edgeLaw (G.positive e) (G.negative e) (x e) * d e = 0 := by
  obtain ⟨-, p, hp⟩ := h
  simpa only [hp] using G.potential_stationary p d hd

end Network

/-! ## The posterior endpoint scenario -/

/-- Data and hypotheses of the posterior endpoint-scenario recovery of
`prop:a-cert-signs`: an envelope law `G`, a selected symmetric scenario law `S` on
the same directed graph, shared nominations `b`, the trial flow `y` whose signs
drive the endpoint selection, the envelope physical flow `xstar`, the coefficient
envelope `[lo, hi]` and the verified flow intervals `[l, u]`. -/
structure Scenario (n m : ℕ) where
  /-- The envelope law. -/
  G : Network n m
  /-- The selected endpoint-scenario law. -/
  S : Network n m
  /-- The fixed nominations, shared by both laws. -/
  b : Fin n → ℝ
  /-- The trial flow whose signs select the scenario coefficients. -/
  y : Fin m → ℝ
  /-- The physical flow of the envelope law. -/
  xstar : Fin m → ℝ
  /-- The selected symmetric coefficient of each edge. -/
  beta : Fin m → ℝ
  /-- The lower envelope bound on the coefficients. -/
  lo : Fin m → ℝ
  /-- The upper envelope bound on the coefficients. -/
  hi : Fin m → ℝ
  /-- The verified lower flow endpoint. -/
  l : Fin m → ℝ
  /-- The verified upper flow endpoint. -/
  u : Fin m → ℝ
  /-- The envelope coefficients are strictly positive. -/
  envelope_positive : G.Positive
  /-- Both laws live on the same directed graph. -/
  tail_eq : S.tail = G.tail
  /-- Both laws live on the same directed graph. -/
  head_eq : S.head = G.head
  /-- The scenario law is symmetric with coefficient `beta`. -/
  scenario_pos : S.positive = beta
  /-- The scenario law is symmetric with coefficient `beta`. -/
  scenario_neg : S.negative = beta
  /-- The selection rule reads the sign of the trial flow. -/
  select : ∀ e, beta e = if 0 ≤ y e then G.positive e else G.negative e
  /-- Envelope membership of the positive coefficients. -/
  lo_le_positive : ∀ e, lo e ≤ G.positive e
  /-- Envelope membership of the negative coefficients. -/
  lo_le_negative : ∀ e, lo e ≤ G.negative e
  /-- Envelope membership of the positive coefficients. -/
  positive_le_hi : ∀ e, G.positive e ≤ hi e
  /-- Envelope membership of the negative coefficients. -/
  negative_le_hi : ∀ e, G.negative e ≤ hi e
  /-- The verified interval contains the trial flow. -/
  l_le_y : ∀ e, l e ≤ y e
  /-- The verified interval contains the trial flow. -/
  y_le_u : ∀ e, y e ≤ u e
  /-- The verified interval contains the envelope physical flow. -/
  l_le_xstar : ∀ e, l e ≤ xstar e
  /-- The verified interval contains the envelope physical flow. -/
  xstar_le_u : ∀ e, xstar e ≤ u e
  /-- `xstar` is the physical flow of the envelope law on the nominations `b`. -/
  xstar_physical : G.IsPhysical b xstar

namespace Scenario

variable (D : Scenario n m)

/-- The endpoint magnitude bound `a_e` of the source. -/
def bnd (e : Fin m) : ℝ := if 0 ≤ D.y e then max 0 (-(D.l e)) else max 0 (D.u e)

/-- The constitutive residual `r_e = (hi_e - lo_e) a_e ^ 2` of the source. -/
def resid (e : Fin m) : ℝ := (D.hi e - D.lo e) * D.bnd e ^ 2

/-- The selected coefficients are strictly positive. -/
theorem beta_pos (e : Fin m) : 0 < D.beta e := by
  rw [D.select e]
  split
  · exact D.envelope_positive.1 e
  · exact D.envelope_positive.2 e

/-- The scenario law is the symmetric cubic law with coefficient `beta`. -/
theorem scenario_law (e : Fin m) (t : ℝ) :
    edgeLaw (D.S.positive e) (D.S.negative e) t = D.beta e * t * |t| := by
  simp [D.scenario_pos, D.scenario_neg, edgeLaw]

/-- The scenario law has strictly positive coefficients. -/
theorem scenario_positive : D.S.Positive :=
  ⟨fun e => by simpa only [D.scenario_pos] using D.beta_pos e,
    fun e => by simpa only [D.scenario_neg] using D.beta_pos e⟩

/-- Both laws share the incidence structure. -/
theorem incidence_eq : D.S.incidence = D.G.incidence := by
  funext v e
  simp [Network.incidence, D.tail_eq, D.head_eq]

/-- Both laws share the divergence map. -/
theorem loads_eq (x : Fin m → ℝ) : D.S.loads x = D.G.loads x := by
  funext v
  simp only [Network.loads_apply, D.incidence_eq]

/-- Both laws share the potential-difference map. -/
theorem drops_eq (p : Fin n → ℝ) : D.S.drops p = D.G.drops p := by
  funext e
  simp [Network.drops, D.tail_eq, D.head_eq]

/-- Conservation for the scenario law is conservation for the envelope law. -/
theorem feasible_of_scenario {x : Fin m → ℝ} (h : D.S.Feasible D.b x) : D.G.Feasible D.b x := by
  have hx : D.S.loads x = D.b := h
  rwa [D.loads_eq] at hx

/-- The residual is nonnegative. -/
theorem resid_nonneg (e : Fin m) : 0 ≤ D.resid e :=
  mul_nonneg (by linarith [(D.lo_le_positive e).trans (D.positive_le_hi e)]) (sq_nonneg _)

/-- Two coefficients drawn from the same envelope differ by at most the envelope width,
so the associated cubic laws differ by at most `(hi - lo) a ^ 2` on `[-a, a]`. -/
private theorem residual_step {c1 c2 lo hi x a : ℝ}
    (h1lo : lo ≤ c1) (h1hi : c1 ≤ hi) (h2lo : lo ≤ c2) (h2hi : c2 ≤ hi)
    (hx : |x| ≤ a) : abs (c1 * x * |x| - c2 * x * |x|) ≤ (hi - lo) * a ^ 2 := by
  have habs : |c1 - c2| ≤ hi - lo := abs_sub_le_iff.mpr ⟨by linarith, by linarith⟩
  have hxx : abs (x * |x|) = |x| ^ 2 := by rw [abs_mul, abs_abs]; ring
  have hxa : |x| ^ 2 ≤ a ^ 2 := by nlinarith [abs_nonneg x]
  calc abs (c1 * x * |x| - c2 * x * |x|)
      = |c1 - c2| * |x| ^ 2 := by
        rw [show c1 * x * |x| - c2 * x * |x| = (c1 - c2) * (x * |x|) by ring, abs_mul, hxx]
    _ ≤ (hi - lo) * a ^ 2 :=
        mul_le_mul habs hxa (sq_nonneg _) (by linarith)

/-- **CC11.** The selected scenario law and the envelope law disagree at the envelope
physical flow by at most the residual `resid e`. A disagreement is possible only when
`xstar e` lies on the opposite side of zero from the trial flow `y e`, and then
`|xstar e| ≤ bnd e`. -/
theorem constitutive_residual (e : Fin m) :
    |D.beta e * D.xstar e * |D.xstar e| -
      edgeLaw (D.G.positive e) (D.G.negative e) (D.xstar e)| ≤ D.resid e := by
  rcases le_or_gt 0 (D.y e) with hy | hy
  · have hbeta : D.beta e = D.G.positive e := by rw [D.select e, if_pos hy]
    rcases le_or_gt 0 (D.xstar e) with hx | hx
    · simp only [edgeLaw, if_pos hx, hbeta, sub_self, abs_zero]
      exact D.resid_nonneg e
    · have hbnd : |D.xstar e| ≤ D.bnd e := by
        rw [bnd, if_pos hy, abs_of_neg hx]
        exact le_max_of_le_right (by linarith [D.l_le_xstar e])
      simp only [edgeLaw, if_neg (not_le.mpr hx), hbeta, resid]
      exact residual_step (D.lo_le_positive e) (D.positive_le_hi e) (D.lo_le_negative e)
        (D.negative_le_hi e) hbnd
  · have hbeta : D.beta e = D.G.negative e := by rw [D.select e, if_neg (not_le.mpr hy)]
    rcases le_or_gt 0 (D.xstar e) with hx | hx
    · have hbnd : |D.xstar e| ≤ D.bnd e := by
        rw [bnd, if_neg (not_le.mpr hy), abs_of_nonneg hx]
        exact le_max_of_le_right (D.xstar_le_u e)
      simp only [edgeLaw, if_pos hx, hbeta, resid]
      exact residual_step (D.lo_le_negative e) (D.negative_le_hi e) (D.lo_le_positive e)
        (D.positive_le_hi e) hbnd
    · simp only [edgeLaw, if_neg (not_le.mpr hx), hbeta, sub_self, abs_zero]
      exact D.resid_nonneg e

/-- **CC12** in its per-edge form. If `xhat` is the physical flow of the selected
scenario law on the same nominations and `betaL > 0` bounds every envelope coefficient
from below, then each edge satisfies
`|xhat e - xstar e| ^ 2 ≤ (2 / betaL) * ∑ j, resid j`. -/
theorem scenario_error_sq {xhat : Fin m → ℝ} {betaL : ℝ} (hhat : D.S.IsPhysical D.b xhat)
    (hL : 0 < betaL) (hLp : ∀ e, betaL ≤ D.G.positive e) (hLm : ∀ e, betaL ≤ D.G.negative e)
    (e : Fin m) :
    |xhat e - D.xstar e| ^ 2 ≤ 2 / betaL * ∑ j, D.resid j := by
  have hbetaL : ∀ j, betaL ≤ D.beta j := by
    intro j
    rw [D.select j]
    split
    · exact hLp j
    · exact hLm j
  set d : Fin m → ℝ := xhat - D.xstar with hd_def
  have hdapp : ∀ j, d j = xhat j - D.xstar j := fun _ => rfl
  -- the difference of the two states is a conserved circulation for both laws
  have hG : D.G.loads d = 0 := by
    have hhatG : D.G.Feasible D.b xhat := D.feasible_of_scenario hhat.1
    change D.G.divergenceLinear d = 0
    rw [hd_def, map_sub, show D.G.divergenceLinear xhat = D.b from hhatG,
      show D.G.divergenceLinear D.xstar = D.b from D.xstar_physical.1, sub_self]
  have hS : D.S.loads d = 0 := by rw [D.loads_eq]; exact hG
  -- both laws annihilate it
  have hstat1 : ∑ j, D.beta j * xhat j * |xhat j| * d j = 0 := by
    simpa only [D.scenario_law] using D.S.isPhysical_stationary hhat d hS
  have hstat2 : ∑ j, edgeLaw (D.G.positive j) (D.G.negative j) (D.xstar j) * d j = 0 :=
    D.G.isPhysical_stationary D.xstar_physical d hG
  -- the maximal coordinate of the difference
  obtain ⟨k, -, hk⟩ :=
    Finset.exists_max_image (Finset.univ : Finset (Fin m)) (fun j => |d j|) ⟨e, Finset.mem_univ e⟩
  set M : ℝ := |d k| with hM_def
  have hM : ∀ j, |d j| ≤ M := fun j => hk j (Finset.mem_univ j)
  have hMnn : 0 ≤ M := abs_nonneg _
  have hR : 0 ≤ ∑ j, D.resid j := Finset.sum_nonneg fun j _ => D.resid_nonneg j
  -- strong monotonicity of the scenario law against the residual pairing
  have hlow : betaL / 2 * ∑ j, |d j| ^ 3 ≤
      (∑ j, D.beta j * xhat j * |xhat j| * d j) -
        ∑ j, D.beta j * D.xstar j * |D.xstar j| * d j := by
    rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
    refine Finset.sum_le_sum fun j _ => ?_
    have h := symmetric_strong_monotone hL (hbetaL j) (xhat j) (D.xstar j)
    rw [← hdapp j] at h
    nlinarith [h]
  have hhigh : (∑ j, edgeLaw (D.G.positive j) (D.G.negative j) (D.xstar j) * d j) -
      ∑ j, D.beta j * D.xstar j * |D.xstar j| * d j ≤ M * ∑ j, D.resid j := by
    rw [← Finset.sum_sub_distrib, Finset.mul_sum]
    refine Finset.sum_le_sum fun j _ => ?_
    have hr : abs (edgeLaw (D.G.positive j) (D.G.negative j) (D.xstar j) -
        D.beta j * D.xstar j * |D.xstar j|) ≤ D.resid j := by
      rw [abs_sub_comm]
      exact D.constitutive_residual j
    calc edgeLaw (D.G.positive j) (D.G.negative j) (D.xstar j) * d j -
          D.beta j * D.xstar j * |D.xstar j| * d j
        = (edgeLaw (D.G.positive j) (D.G.negative j) (D.xstar j) -
            D.beta j * D.xstar j * |D.xstar j|) * d j := by ring
      _ ≤ abs ((edgeLaw (D.G.positive j) (D.G.negative j) (D.xstar j) -
            D.beta j * D.xstar j * |D.xstar j|) * d j) := le_abs_self _
      _ = abs (edgeLaw (D.G.positive j) (D.G.negative j) (D.xstar j) -
            D.beta j * D.xstar j * |D.xstar j|) * |d j| := abs_mul _ _
      _ ≤ D.resid j * M := mul_le_mul hr (hM j) (abs_nonneg _) (D.resid_nonneg j)
      _ = M * D.resid j := mul_comm _ _
  have hcube : M ^ 3 ≤ ∑ j, |d j| ^ 3 :=
    Finset.single_le_sum (f := fun j => |d j| ^ 3) (fun j _ => by positivity) (Finset.mem_univ k)
  have hfin : betaL / 2 * M ^ 3 ≤ M * ∑ j, D.resid j := by
    have h1 : betaL / 2 * M ^ 3 ≤ betaL / 2 * ∑ j, |d j| ^ 3 := by
      have : (0 : ℝ) ≤ betaL / 2 := by linarith
      exact mul_le_mul_of_nonneg_left hcube this
    linarith [hlow, hhigh, hstat1, hstat2]
  -- conclude, dividing by the maximal coordinate when it is nonzero
  rw [← hdapp e, div_mul_eq_mul_div, le_div_iff₀ hL]
  rcases eq_or_lt_of_le hMnn with hM0 | hM0
  · have hde : |d e| = 0 := le_antisymm (by rw [hM0]; exact hM e) (abs_nonneg _)
    rw [hde]
    nlinarith [hR]
  · have hM2 : betaL * M ^ 2 ≤ 2 * ∑ j, D.resid j := by nlinarith [hfin, hM0]
    have hsq : |d e| ^ 2 ≤ M ^ 2 := by nlinarith [hM e, abs_nonneg (d e)]
    nlinarith [mul_nonneg hL.le (sub_nonneg.mpr hsq), hM2]

/-- **CC12** in sup-norm form: the squared `‖·‖_∞` error of the scenario flow is at most
`(2 / betaL) * ∑ j, resid j`, on any network with at least one edge. -/
theorem scenario_error_sup {xhat : Fin m → ℝ} {betaL : ℝ} (hhat : D.S.IsPhysical D.b xhat)
    (hL : 0 < betaL) (hLp : ∀ e, betaL ≤ D.G.positive e) (hLm : ∀ e, betaL ≤ D.G.negative e)
    (hne : (Finset.univ : Finset (Fin m)).Nonempty) :
    (Finset.univ.sup' hne fun j => |xhat j - D.xstar j|) ^ 2 ≤ 2 / betaL * ∑ j, D.resid j := by
  obtain ⟨k, -, hk⟩ := Finset.exists_mem_eq_sup' hne fun j => |xhat j - D.xstar j|
  rw [hk]
  exact D.scenario_error_sq hhat hL hLp hLm k

/-- The compatibility alternatives of `eq:a-cert-compatible`: on each edge, either the
envelope law is already symmetric with the selected coefficient, or the verified interval
fixes the sign of the flow consistently with the selection, or the interval is the single
point zero. -/
def Compatible (e : Fin m) : Prop :=
  (D.G.positive e = D.beta e ∧ D.G.negative e = D.beta e) ∨
    (0 ≤ D.l e ∧ D.beta e = D.G.positive e) ∨
    (D.u e ≤ 0 ∧ D.beta e = D.G.negative e) ∨
    (D.l e = 0 ∧ D.u e = 0)

/-- Under compatibility the two laws agree at the envelope physical flow. Non-strict signs
suffice because both laws vanish at zero. -/
theorem law_eq_of_compatible {e : Fin m} (h : D.Compatible e) :
    edgeLaw (D.G.positive e) (D.G.negative e) (D.xstar e) =
      edgeLaw (D.S.positive e) (D.S.negative e) (D.xstar e) := by
  rw [D.scenario_law e]
  rcases h with ⟨hp, hn⟩ | ⟨hl, hb⟩ | ⟨hu, hb⟩ | ⟨hl, hu⟩
  · simp [edgeLaw, hp, hn]
  · have hx : 0 ≤ D.xstar e := hl.trans (D.l_le_xstar e)
    simp [edgeLaw, if_pos hx, hb]
  · have hx : D.xstar e ≤ 0 := (D.xstar_le_u e).trans hu
    rcases eq_or_lt_of_le hx with h0 | h0
    · simp [edgeLaw, h0]
    · simp [edgeLaw, not_le.mpr h0, hb]
  · have hx : D.xstar e = 0 :=
      le_antisymm (by rw [← hu]; exact D.xstar_le_u e) (by rw [← hl]; exact D.l_le_xstar e)
    simp [edgeLaw, hx]

/-- **CC13.** If every edge satisfies one of the compatibility alternatives, the selected
scenario is exactly optimal: its physical flow is the envelope physical flow. -/
theorem exact_of_compatible {xhat : Fin m → ℝ} (hhat : D.S.IsPhysical D.b xhat)
    (h : ∀ e, D.Compatible e) : xhat = D.xstar := by
  obtain ⟨hfeas, p, hp⟩ := D.xstar_physical
  have hphys : D.S.IsPhysical D.b D.xstar := by
    refine ⟨?_, p, ?_⟩
    · change D.S.loads D.xstar = D.b
      rw [D.loads_eq]
      exact hfeas
    · rw [D.drops_eq, hp]
      exact funext fun e => D.law_eq_of_compatible (h e)
  exact D.S.isPhysical_unique D.scenario_positive hhat hphys

end Scenario

end

end PotentialFlow
