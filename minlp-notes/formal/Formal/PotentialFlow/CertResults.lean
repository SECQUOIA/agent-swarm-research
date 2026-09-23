import Formal.PotentialFlow.Bisection
import Formal.PotentialFlow.Curvature
import Formal.PotentialFlow.Laplacian
import Formal.PotentialFlow.Results

/-! # Exact rational acceptance conditions for the Bregman and curvature witnesses

`RationalNetwork.Accepted` already packages the primal-dual checks of the saved
potential-flow package into one decidable rational predicate whose acceptance
bounds the energy error and the uniform flow radius of the unique physical flow.

This module extends that predicate twice, in the same verifier-facing style:

* `RationalNetwork.IntervalAccepted` adds the per-edge Bregman endpoint tests of
  `CC03`. Acceptance encloses the physical flow in the supplied rational
  intervals and, by monotonicity of the edge law, encloses every physical edge
  drop between the endpoint values (`CC07`). The endpoints produced by the exact
  bisection of `Bisection.lean` are always accepted, and a zero verified gap
  makes the singleton intervals at the trial flow accepted (`CC04`).
* `RationalNetwork.GoalAccepted` adds the conservation-aware curvature checks of
  `CC22`-`CC23`: rational curvature floors of the accepted interval, a rational
  goal residual `s = w - Aᵀv` vanishing on the zero-curvature edges, and the
  rational curvature factor. Acceptance bounds `|wᵀ(x* - y)|` by the certified
  radius.

Both predicates carry a `Decidable` instance, so a verifier decides them by exact
rational arithmetic; `CertExample` exhibits a two-edge instance whose acceptance
is proved by kernel evaluation. `goalAccepted_sound` collects in one statement
everything an accepted triple proves about the physical flow.

No optimizer output, no pre-existing physical solution and no numerical tolerance
appears as a hypothesis of the four headline soundness theorems
(`intervalAccepted_sound`, `goalAccepted_sound`, `goalAccepted_radius_sound`,
`gap_zero_sound`): each produces the physical flow existentially. The first three
require only acceptance; `gap_zero_sound` additionally requires `C.gap = 0`, an
exact condition on the certificate data. This does **not** extend
to every lemma in the file — `intervalAccepted_drop_enclosure`,
`intervalAccepted_mem` and `goalAccepted_abs_sum_le` take an explicit `x` with
feasibility and minimality, which is a supplied physical solution. An earlier
version of this paragraph claimed the property for *any* soundness theorem, which
was false for those three. -/

namespace PotentialFlow

/-- Rational per-edge flow intervals supplied alongside a `RationalCertificate`. -/
structure IntervalCertificate (n m : ℕ) where
  /-- Lower endpoint of the certified interval on each edge. -/
  lower : Fin m → ℚ
  /-- Upper endpoint of the certified interval on each edge. -/
  upper : Fin m → ℚ

/-- Rational data of a linear goal: the goal vector, the potential used to form the
residual `s = w - Aᵀv`, and the certified goal radius. -/
structure GoalCertificate (n m : ℕ) where
  /-- The linear goal `w` paired with the flow. -/
  goal : Fin m → ℚ
  /-- The potential `v` whose drops are subtracted from the goal. -/
  potentials : Fin n → ℚ
  /-- The certified radius `r` for `|wᵀ(x* - y)|`. -/
  radius : ℚ

/-- `curvatureFloor` evaluated in exact rational arithmetic. -/
def ratCurvatureFloor (cp cm l u : ℚ) : ℚ :=
  if 0 < l then 2 * cp * l else if u < 0 then -(2 * cm * u) else 0

/-- The rational curvature floor is the real curvature floor of the cast arguments. -/
theorem ratCurvatureFloor_cast (cp cm l u : ℚ) :
    ((ratCurvatureFloor cp cm l u : ℚ) : ℝ) =
      curvatureFloor (cp : ℝ) (cm : ℝ) (l : ℝ) (u : ℝ) := by
  have hl : ((0 : ℝ) < (l : ℝ)) ↔ (0 < l) := by exact_mod_cast Iff.rfl
  have hu : (((u : ℝ)) < 0) ↔ (u < 0) := by exact_mod_cast Iff.rfl
  simp only [ratCurvatureFloor, curvatureFloor, hl, hu]
  split_ifs <;> push_cast <;> ring

/-- A rational endpoint test transfers verbatim to the real divergence. -/
theorem cast_le_edgeBregman {cp cm y z δ : ℚ} (h : δ ≤ ratBregman cp cm y z) :
    (δ : ℝ) ≤ edgeBregman (cp : ℝ) (cm : ℝ) (y : ℝ) (z : ℝ) := by
  rw [← ratBregman_cast]
  exact_mod_cast h

namespace RationalNetwork

variable {n m : ℕ} (G : RationalNetwork n m)

/-! ## The Bregman interval certificate -/

/-- The exact rational interval certificate: the primal-dual checks of `Accepted`
together with, on every edge, the ordering `l_e ≤ y_e ≤ u_e` and the two outward
Bregman endpoint tests `δ ≤ D_e(y_e, l_e)` and `δ ≤ D_e(y_e, u_e)`. Every check is
an exact rational (in)equality. -/
def IntervalAccepted (hm : 0 < m) (b : Fin n → ℚ) (C : RationalCertificate n m)
    (I : IntervalCertificate n m) : Prop :=
  G.Accepted hm b C ∧ ∀ e, I.lower e ≤ C.flow e ∧ C.flow e ≤ I.upper e ∧
    C.gap ≤ ratBregman (G.positive e) (G.negative e) (C.flow e) (I.lower e) ∧
    C.gap ≤ ratBregman (G.positive e) (G.negative e) (C.flow e) (I.upper e)

instance decidableIntervalAccepted (hm : 0 < m) (b : Fin n → ℚ)
    (C : RationalCertificate n m) (I : IntervalCertificate n m) :
    Decidable (G.IntervalAccepted hm b C I) := by
  unfold IntervalAccepted
  infer_instance

variable {hm : 0 < m} {b : Fin n → ℚ} {C : RationalCertificate n m}

/-- The certified gap bounds the real energy error of the trial flow against any
feasible flow. This is the transported form of the dual bound of `Accepted`. -/
theorem accepted_energy_sub_le {x : Fin m → ℝ} (h : G.Accepted hm b C)
    (hx : G.toReal.Feasible (fun v => (b v : ℝ)) x) :
    G.toReal.energy (fun e => (C.flow e : ℝ)) - G.toReal.energy x ≤ (C.gap : ℝ) := by
  rw [G.accepted_gap h]
  exact G.toReal.energy_error_le_gap (G.accepted_positive h) hx
    (fun e => (G.accepted_roots h e).1) (fun e => (G.accepted_roots h e).2)

/-- `CC03` transported: an accepted interval certificate encloses the minimizing flow
on every edge. The minimizer is not assumed to be known; only feasibility and
minimality of `x` are used, and both are supplied by `accepted_sound`. -/
theorem intervalAccepted_mem {I : IntervalCertificate n m} {x : Fin m → ℝ}
    (h : G.IntervalAccepted hm b C I)
    (hx : G.toReal.Feasible (fun v => (b v : ℝ)) x)
    (hmin : ∀ z, G.toReal.Feasible (fun v => (b v : ℝ)) z →
      G.toReal.energy x ≤ G.toReal.energy z) (e : Fin m) :
    ((I.lower e : ℚ) : ℝ) ≤ x e ∧ x e ≤ ((I.upper e : ℚ) : ℝ) :=
  G.toReal.mem_interval_of_edgeBregman (G.accepted_positive h.1) hx
    (G.accepted_feasible h.1) hmin (G.accepted_energy_sub_le h.1 hx)
    (by exact_mod_cast (h.2 e).1) (by exact_mod_cast (h.2 e).2.1)
    (cast_le_edgeBregman (h.2 e).2.2.1) (cast_le_edgeBregman (h.2 e).2.2.2)

/-- `CC07` transported: the physical edge drop lies between the edge law evaluated at
the two certified endpoints. -/
theorem intervalAccepted_drop_enclosure {I : IntervalCertificate n m} {x : Fin m → ℝ}
    (h : G.IntervalAccepted hm b C I)
    (hx : G.toReal.Feasible (fun v => (b v : ℝ)) x)
    (hmin : ∀ z, G.toReal.Feasible (fun v => (b v : ℝ)) z →
      G.toReal.energy x ≤ G.toReal.energy z) (e : Fin m) :
    edgeLaw (G.toReal.positive e) (G.toReal.negative e) ((I.lower e : ℚ) : ℝ) ≤
        edgeLaw (G.toReal.positive e) (G.toReal.negative e) (x e) ∧
      edgeLaw (G.toReal.positive e) (G.toReal.negative e) (x e) ≤
        edgeLaw (G.toReal.positive e) (G.toReal.negative e) ((I.upper e : ℚ) : ℝ) :=
  G.toReal.drop_enclosure (G.accepted_positive h.1)
    (fun j => G.intervalAccepted_mem h hx hmin j) e

/-- Soundness of the Bregman interval certificate. Acceptance of exact rational data
implies that the unique physical flow exists, is the unique energy minimizer, lies in
every certified interval, and has every edge drop enclosed by the edge law evaluated
at the two endpoints. -/
theorem intervalAccepted_sound {I : IntervalCertificate n m}
    (h : G.IntervalAccepted hm b C I) :
    ∃ x : Fin m → ℝ,
      G.toReal.Feasible (fun v => (b v : ℝ)) x ∧
      (∀ z, G.toReal.Feasible (fun v => (b v : ℝ)) z →
        G.toReal.energy x ≤ G.toReal.energy z) ∧
      (∀ z, G.toReal.Feasible (fun v => (b v : ℝ)) z →
        (∀ w, G.toReal.Feasible (fun v => (b v : ℝ)) w →
          G.toReal.energy z ≤ G.toReal.energy w) → z = x) ∧
      (∀ e, ((I.lower e : ℚ) : ℝ) ≤ x e ∧ x e ≤ ((I.upper e : ℚ) : ℝ)) ∧
      (∀ e, edgeLaw (G.toReal.positive e) (G.toReal.negative e) ((I.lower e : ℚ) : ℝ) ≤
          edgeLaw (G.toReal.positive e) (G.toReal.negative e) (x e) ∧
        edgeLaw (G.toReal.positive e) (G.toReal.negative e) (x e) ≤
          edgeLaw (G.toReal.positive e) (G.toReal.negative e) ((I.upper e : ℚ) : ℝ)) := by
  obtain ⟨x, hx, hmin, huniq, -, -, -, -⟩ := G.accepted_sound h.1
  exact ⟨x, hx, hmin, huniq, fun e => G.intervalAccepted_mem h hx hmin e,
    fun e => G.intervalAccepted_drop_enclosure h hx hmin e⟩

/-- The interval built from the outer endpoints returned by `k` bisection steps on each
edge, started from the certified uniform radius. -/
def bracketInterval (C : RationalCertificate n m) (k : ℕ) : IntervalCertificate n m where
  lower := fun e =>
    (lowerBracket (G.positive e) (G.negative e) (C.flow e) C.gap C.radius k).2
  upper := fun e =>
    (upperBracket (G.positive e) (G.negative e) (C.flow e) C.gap C.radius k).2

/-- `CC06` composed with `CC03`: the endpoints produced by `k` steps of the exact
rational bisection are always accepted, for every step count and every accepted
primal-dual certificate. No extra hypothesis is needed: the certified uniform radius
supplies the initial outer bracket. -/
theorem intervalAccepted_bracketInterval (h : G.Accepted hm b C) (k : ℕ) :
    G.IntervalAccepted hm b C (G.bracketInterval C k) := by
  refine ⟨h, fun e => ?_⟩
  have ha : 0 < G.coefficientMinimum hm :=
    G.coefficientMinimum_positive hm (fun j => (h.1 j).1) (fun j => (h.1 j).2)
  obtain ⟨hminus, hplus⟩ := le_ratBregman_of_radius (cp := G.positive e)
    (cm := G.negative e) (C.flow e) ha (G.coefficientMinimum_le_positive hm e)
    (G.coefficientMinimum_le_negative hm e) h.2.2.2.2.2.1 h.2.2.2.2.2.2
  obtain ⟨hu1, hu2, -, -, hu5, -⟩ :=
    upperBracket_invariant h.2.2.2.2.1 h.2.2.2.2.2.1 hplus k
  obtain ⟨hl1, hl2, -, -, hl5, -⟩ :=
    lowerBracket_invariant h.2.2.2.2.1 h.2.2.2.2.2.1 hminus k
  exact ⟨hl2.trans hl1, hu1.trans hu2, hl5, hu5⟩

/-- `CC04`: with a zero verified gap the singleton intervals at the trial flow are
accepted, with no curvature or bisection hypothesis. -/
theorem intervalAccepted_singleton (h : G.Accepted hm b C) (hgap : C.gap = 0) :
    G.IntervalAccepted hm b C ⟨C.flow, C.flow⟩ :=
  ⟨h, fun e => ⟨le_rfl, le_rfl, by simp [hgap], by simp [hgap]⟩⟩

/-- The zero-gap case in transported form: the trial flow is the physical flow. -/
theorem gap_zero_sound (h : G.Accepted hm b C) (hgap : C.gap = 0) :
    ∃ x : Fin m → ℝ,
      G.toReal.Feasible (fun v => (b v : ℝ)) x ∧
      (∀ z, G.toReal.Feasible (fun v => (b v : ℝ)) z →
        G.toReal.energy x ≤ G.toReal.energy z) ∧
      x = fun e => ((C.flow e : ℚ) : ℝ) := by
  obtain ⟨x, hx, hmin, -, -, -, -, -⟩ := G.accepted_sound h
  refine ⟨x, hx, hmin, funext fun e => le_antisymm ?_ ?_⟩
  · exact (G.intervalAccepted_mem (G.intervalAccepted_singleton h hgap) hx hmin e).2
  · exact (G.intervalAccepted_mem (G.intervalAccepted_singleton h hgap) hx hmin e).1

/-! ## The curvature goal certificate -/

/-- The rational curvature floors of a certified interval, edge by edge. -/
def curvatures (I : IntervalCertificate n m) : Fin m → ℚ := fun e =>
  ratCurvatureFloor (G.positive e) (G.negative e) (I.lower e) (I.upper e)

/-- The rational goal residual `s = w - Aᵀv` of a goal certificate. -/
def residuals (W : GoalCertificate n m) : Fin m → ℚ := fun e =>
  W.goal e - G.drops W.potentials e

/-- The rational curvature factor `∑_{h_e ≠ 0} s_e² / h_e`. The zero-curvature edges
contribute nothing, so no division by zero occurs. -/
def ratFactor (I : IntervalCertificate n m) (W : GoalCertificate n m) : ℚ :=
  ∑ e, if G.curvatures I e = 0 then 0 else G.residuals W e ^ 2 / G.curvatures I e

/-- The rational curvature floors are the real curvature floors of the cast interval. -/
theorem curvatures_cast (I : IntervalCertificate n m) (e : Fin m) :
    ((G.curvatures I e : ℚ) : ℝ) = curvatureFloor (G.toReal.positive e)
      (G.toReal.negative e) ((I.lower e : ℚ) : ℝ) ((I.upper e : ℚ) : ℝ) :=
  ratCurvatureFloor_cast _ _ _ _

/-- The rational residual is the real residual of the cast goal and potential. -/
theorem residuals_cast (W : GoalCertificate n m) (e : Fin m) :
    ((G.residuals W e : ℚ) : ℝ) = ((W.goal e : ℚ) : ℝ) -
      G.toReal.drops (fun v => ((W.potentials v : ℚ) : ℝ)) e := by
  rw [G.toReal_drops, residuals]
  push_cast
  ring

/-- The rational curvature factor is the real curvature factor of the cast data. -/
theorem ratFactor_cast (I : IntervalCertificate n m) (W : GoalCertificate n m) :
    ((G.ratFactor I W : ℚ) : ℝ) =
      curvatureFactor (fun e => ((G.curvatures I e : ℚ) : ℝ))
        (fun e => ((G.residuals W e : ℚ) : ℝ)) := by
  rw [curvatureFactor, ratFactor, Rat.cast_sum]
  refine Finset.sum_congr rfl fun e _ => ?_
  by_cases he : G.curvatures I e = 0
  · simp [he]
  · rw [if_neg he, if_neg (by exact_mod_cast he : ¬((G.curvatures I e : ℚ) : ℝ) = 0)]
    push_cast
    ring

/-- The exact rational goal certificate: an accepted interval certificate, the
zero-curvature condition `h_e = 0 → s_e = 0`, a nonnegative radius, and the rational
inequality `2 δ C ≤ r²`. Every check is exact rational arithmetic. -/
def GoalAccepted (hm : 0 < m) (b : Fin n → ℚ) (C : RationalCertificate n m)
    (I : IntervalCertificate n m) (W : GoalCertificate n m) : Prop :=
  G.IntervalAccepted hm b C I ∧ (∀ e, G.curvatures I e = 0 → G.residuals W e = 0) ∧
    0 ≤ W.radius ∧ 2 * C.gap * G.ratFactor I W ≤ W.radius ^ 2

instance decidableGoalAccepted (hm : 0 < m) (b : Fin n → ℚ)
    (C : RationalCertificate n m) (I : IntervalCertificate n m)
    (W : GoalCertificate n m) : Decidable (G.GoalAccepted hm b C I W) := by
  unfold GoalAccepted
  infer_instance

/-- `CC23` transported: an accepted goal certificate bounds the goal error of the
minimizing flow by the certified radius. -/
theorem goalAccepted_abs_sum_le {I : IntervalCertificate n m} {W : GoalCertificate n m}
    {x : Fin m → ℝ} (hg : G.GoalAccepted hm b C I W)
    (hx : G.toReal.Feasible (fun v => (b v : ℝ)) x)
    (hmin : ∀ z, G.toReal.Feasible (fun v => (b v : ℝ)) z →
      G.toReal.energy x ≤ G.toReal.energy z) :
    |∑ e, ((W.goal e : ℚ) : ℝ) * (x e - ((C.flow e : ℚ) : ℝ))| ≤ ((W.radius : ℚ) : ℝ) := by
  have hmem := fun e => G.intervalAccepted_mem hg.1 hx hmin e
  refine G.toReal.abs_sum_goal_le (G.accepted_positive hg.1.1) hx
    (G.accepted_feasible hg.1.1) hmin (G.accepted_energy_sub_le hg.1.1 hx)
    (l := fun e => ((I.lower e : ℚ) : ℝ)) (u := fun e => ((I.upper e : ℚ) : ℝ))
    (h := fun e => ((G.curvatures I e : ℚ) : ℝ))
    (s := fun e => ((G.residuals W e : ℚ) : ℝ))
    (v := fun v => ((W.potentials v : ℚ) : ℝ))
    (C := ((G.ratFactor I W : ℚ) : ℝ))
    (fun e => by exact_mod_cast (hg.1.2 e).1) (fun e => by exact_mod_cast (hg.1.2 e).2.1)
    (fun e => (hmem e).1) (fun e => (hmem e).2) (G.curvatures_cast I)
    (G.residuals_cast W) (fun e he => ?_) (G.ratFactor_cast I W) ?_ ?_
  · exact_mod_cast hg.2.1 e (by exact_mod_cast he)
  · exact_mod_cast hg.2.2.1
  · exact_mod_cast hg.2.2.2

/-- Soundness of an accepted triple, in the style of `accepted_sound`. Acceptance of
exact rational data implies that the unique physical flow exists, is the unique energy
minimizer, admits a potential, has energy within the certified gap of the trial flow,
lies within the certified uniform radius, lies in every certified interval, has every
edge drop enclosed by the endpoint edge-law values, and has goal error at most the
certified goal radius. No optimizer output, no pre-existing physical solution and no
numerical tolerance is a hypothesis. -/
theorem goalAccepted_sound {I : IntervalCertificate n m} {W : GoalCertificate n m}
    (hg : G.GoalAccepted hm b C I W) :
    ∃ x : Fin m → ℝ,
      G.toReal.Feasible (fun v => (b v : ℝ)) x ∧
      (∀ z, G.toReal.Feasible (fun v => (b v : ℝ)) z →
        G.toReal.energy x ≤ G.toReal.energy z) ∧
      (∀ z, G.toReal.Feasible (fun v => (b v : ℝ)) z →
        (∀ w, G.toReal.Feasible (fun v => (b v : ℝ)) w →
          G.toReal.energy z ≤ G.toReal.energy w) → z = x) ∧
      (∃ p, G.toReal.drops p = fun e =>
        edgeLaw (G.toReal.positive e) (G.toReal.negative e) (x e)) ∧
      (0 ≤ G.toReal.energy (fun e => ((C.flow e : ℚ) : ℝ)) - G.toReal.energy x ∧
        G.toReal.energy (fun e => ((C.flow e : ℚ) : ℝ)) - G.toReal.energy x ≤
          ((C.gap : ℚ) : ℝ)) ∧
      (∀ e, |((C.flow e : ℚ) : ℝ) - x e| ≤ ((C.radius : ℚ) : ℝ)) ∧
      (∀ e, ((I.lower e : ℚ) : ℝ) ≤ x e ∧ x e ≤ ((I.upper e : ℚ) : ℝ)) ∧
      (∀ e, edgeLaw (G.toReal.positive e) (G.toReal.negative e) ((I.lower e : ℚ) : ℝ) ≤
          edgeLaw (G.toReal.positive e) (G.toReal.negative e) (x e) ∧
        edgeLaw (G.toReal.positive e) (G.toReal.negative e) (x e) ≤
          edgeLaw (G.toReal.positive e) (G.toReal.negative e) ((I.upper e : ℚ) : ℝ)) ∧
      |∑ e, ((W.goal e : ℚ) : ℝ) * (x e - ((C.flow e : ℚ) : ℝ))| ≤ ((W.radius : ℚ) : ℝ) := by
  obtain ⟨x, hx, hmin, huniq, hp, hgapb, hrad, -⟩ := G.accepted_sound hg.1.1
  exact ⟨x, hx, hmin, huniq, hp, hgapb, hrad,
    fun e => G.intervalAccepted_mem hg.1 hx hmin e,
    fun e => G.intervalAccepted_drop_enclosure hg.1 hx hmin e,
    G.goalAccepted_abs_sum_le hg hx hmin⟩

/-- The goal-radius conclusion alone, in existential form. -/
theorem goalAccepted_radius_sound {I : IntervalCertificate n m}
    {W : GoalCertificate n m} (hg : G.GoalAccepted hm b C I W) :
    ∃ x : Fin m → ℝ,
      G.toReal.Feasible (fun v => (b v : ℝ)) x ∧
      (∀ z, G.toReal.Feasible (fun v => (b v : ℝ)) z →
        G.toReal.energy x ≤ G.toReal.energy z) ∧
      |∑ e, ((W.goal e : ℚ) : ℝ) * (x e - ((C.flow e : ℚ) : ℝ))| ≤
        ((W.radius : ℚ) : ℝ) := by
  obtain ⟨x, hx, hmin, -, -, -, -, -, -, hw⟩ := G.goalAccepted_sound hg
  exact ⟨x, hx, hmin, hw⟩

end RationalNetwork

/-! ## A worked two-edge instance

Two parallel unit-coefficient edges carrying a total nomination of `2`. The trial flow
`(3/2, 1/2)` is not optimal, so the verified gap `1/2` is strictly positive and all the
interval and curvature checks are non-trivial. Acceptance is decided by kernel
evaluation of the `Decidable` instances above. -/

namespace CertExample

/-- Two parallel edges from node `0` to node `1`, all coefficients equal to one. -/
def network : RationalNetwork 2 2 where
  tail := ![0, 0]
  head := ![1, 1]
  positive := ![1, 1]
  negative := ![1, 1]

/-- Two units injected at node `0` and withdrawn at node `1`. -/
def nominations : Fin 2 → ℚ := ![2, -2]

/-- A suboptimal trial flow with the integral potential `(1, 0)` and verified gap `1/2`. -/
def certificate : RationalCertificate 2 2 where
  flow := ![3 / 2, 1 / 2]
  potentials := ![1, 0]
  rootUpper := ![1, 1]
  gap := 1 / 2
  radius := 3 / 2

/-- Rational intervals passing the outward Bregman endpoint tests at the gap `1/2`. -/
def interval : IntervalCertificate 2 2 where
  lower := ![3 / 4, -3 / 4]
  upper := ![9 / 4, 5 / 4]

/-- The goal selecting the first edge, with the zero potential and radius `5/6`. -/
def goalCert : GoalCertificate 2 2 where
  goal := ![1, 0]
  potentials := ![0, 0]
  radius := 5 / 6

set_option maxRecDepth 4000 in
/-- The interval certificate is accepted; the checks reduce in the kernel. -/
theorem interval_accepted :
    network.IntervalAccepted (by decide : 0 < 2) nominations certificate interval := by
  decide +kernel

set_option maxRecDepth 4000 in
/-- The goal certificate is accepted; the checks reduce in the kernel. The first edge
has curvature floor `3/2`, the second straddles the origin and has floor `0`, where the
residual vanishes, so the rational factor is `2/3` and `2 · (1/2) · (2/3) ≤ (5/6)²`. -/
theorem goal_accepted :
    network.GoalAccepted (by decide : 0 < 2) nominations certificate interval goalCert := by
  decide +kernel

/-- The verified gap of the worked instance is strictly positive, so the interval and
curvature checks are not the degenerate zero-gap case. -/
theorem gap_pos : (0 : ℚ) < certificate.gap := by norm_num [certificate]

/-- The instantiated real conclusion: the unique physical flow of the two-edge network
lies in the certified intervals and its first-edge error against the trial flow is at
most `5/6`. -/
theorem worked_example_verified :
    ∃ x : Fin 2 → ℝ,
      network.toReal.Feasible (fun v => ((nominations v : ℚ) : ℝ)) x ∧
      (∀ z, network.toReal.Feasible (fun v => ((nominations v : ℚ) : ℝ)) z →
        network.toReal.energy x ≤ network.toReal.energy z) ∧
      (∀ e, ((interval.lower e : ℚ) : ℝ) ≤ x e ∧ x e ≤ ((interval.upper e : ℚ) : ℝ)) ∧
      |x 0 - (3 / 2 : ℝ)| ≤ (5 / 6 : ℝ) := by
  obtain ⟨x, hx, hmin, -, -, -, -, hI, -, hw⟩ := network.goalAccepted_sound goal_accepted
  refine ⟨x, hx, hmin, hI, ?_⟩
  simpa [goalCert, certificate, Fin.sum_univ_two] using hw

end CertExample

end PotentialFlow
