import Formal.PotentialFlow.Optimization

/-! # Conserved-energy support certificates for linear goals

This module formalizes the support-certificate obligations `CC14`-`CC18` and `CC20`
of `topics/16-potential-flow-certificates/CLAIMS.md`, which correspond to
`thm:a-cert-support` of the certified-computation appendix.

For a feasible trial flow `y` the *support set* is the conserved sublevel set
`S(y) = {x | A x = b, E(x) ≤ E(y)}`. It contains the physical flow `x*`, it is
nonempty, convex, closed, bounded and compact, and every linear goal attains its
maximum on it. A dual triple `(lam, v, R)` with `lam > 0` certifies the upper bound
`U_w = lam * E(y) + vᵀ b + (2/3) * ∑ R` for the goal `wᵀ x` on `S(y)`, by edgewise
Fenchel duality applied to the scaled coefficients `lam * c`. Applying the same
construction to `-w` gives a two-sided enclosure, in particular for the physical
flow. The degenerate case `lam = 0` is exactly the case of goals that are constant
on the conservation affine space: those are the goals of the form `w = Aᵀ v`, and
then the goal value is the exact number `vᵀ b`, certified with no roots at all.

All data are arbitrary real vectors; rationality is not used anywhere, so a later
module can instantiate these statements with rational certificate data.
-/

namespace PotentialFlow

noncomputable section

/-- Scaling both edge coefficients scales the asymmetric cubic edge energy by the same
factor. This is the reduction that lets `fenchel_root_bound` be applied to `lam * E`. -/
theorem edgeEnergy_smul (lam cp cm t : ℝ) :
    edgeEnergy (lam * cp) (lam * cm) t = lam * edgeEnergy cp cm t := by
  unfold edgeEnergy
  split <;> ring

/-- A scalar factor may be pushed through the sign-dependent coefficient selector. -/
theorem mul_ite_coeff (lam cp cm : ℝ) (P : Prop) [Decidable P] :
    lam * (if P then cp else cm) = if P then lam * cp else lam * cm := by
  split <;> rfl

/-- The asymmetric cubic edge energy is convex whenever both coefficients are
nonnegative: its derivative is the monotone edge law. -/
theorem convexOn_edgeEnergy {cp cm : ℝ} (hcp : 0 ≤ cp) (hcm : 0 ≤ cm) :
    ConvexOn ℝ Set.univ (edgeEnergy cp cm) := by
  have hdiff : Differentiable ℝ (edgeEnergy cp cm) := fun x =>
    (hasDerivAt_edgeEnergy cp cm x).differentiableAt
  have hderiv : deriv (edgeEnergy cp cm) = edgeLaw cp cm :=
    funext fun x => (hasDerivAt_edgeEnergy cp cm x).deriv
  have hmono : Monotone (deriv (edgeEnergy cp cm)) := by
    rw [hderiv]
    exact edgeLaw_monotone hcp hcm
  exact hmono.convexOn_univ_of_deriv hdiff

/-- A linear goal is continuous in the edge-flow vector. -/
theorem continuous_linearGoal {m : ℕ} (w : Fin m → ℝ) :
    Continuous fun x : Fin m → ℝ => ∑ e, w e * x e :=
  continuous_finsetSum _ fun e _ => continuous_const.mul (continuous_apply e)

namespace Network

variable {n m : ℕ} (G : Network n m)

/-! ## The conserved-energy support set (CC14) -/

/-- The conserved-energy support set of a trial flow `y`: the flows conserving the same
nominations whose energy does not exceed the trial energy. -/
def supportSet (b : Fin n → ℝ) (y : Fin m → ℝ) : Set (Fin m → ℝ) :=
  {x | G.Feasible b x ∧ G.energy x ≤ G.energy y}

/-- Membership in the support set is conservation together with the energy inequality. -/
theorem mem_supportSet {b : Fin n → ℝ} {y x : Fin m → ℝ} :
    x ∈ G.supportSet b y ↔ G.Feasible b x ∧ G.energy x ≤ G.energy y := Iff.rfl

/-- The support set is the conservation fiber intersected with an energy sublevel set. -/
theorem supportSet_eq_inter (b : Fin n → ℝ) (y : Fin m → ℝ) :
    G.supportSet b y = {x | G.Feasible b x} ∩ {x | G.energy x ≤ G.energy y} := rfl

/-- Every point of the support set is feasible. -/
theorem supportSet_subset_feasible (b : Fin n → ℝ) (y : Fin m → ℝ) :
    G.supportSet b y ⊆ {x | G.Feasible b x} := fun _ hx => hx.1

/-- A feasible trial flow lies in its own support set. -/
theorem mem_supportSet_self {b : Fin n → ℝ} {y : Fin m → ℝ} (hy : G.Feasible b y) :
    y ∈ G.supportSet b y := ⟨hy, le_rfl⟩

/-- The support set is nonempty as soon as the trial flow is feasible. -/
theorem supportSet_nonempty {b : Fin n → ℝ} {y : Fin m → ℝ} (hy : G.Feasible b y) :
    (G.supportSet b y).Nonempty := ⟨y, G.mem_supportSet_self hy⟩

/-- The support set grows with the trial energy. -/
theorem supportSet_mono (b : Fin n → ℝ) {y z : Fin m → ℝ}
    (h : G.energy y ≤ G.energy z) : G.supportSet b y ⊆ G.supportSet b z :=
  fun _ hx => ⟨hx.1, hx.2.trans h⟩

/-- **CC14.** An energy minimizer on `b` belongs to the support set of every feasible
trial flow. -/
theorem minimizer_mem_supportSet {b : Fin n → ℝ} {x y : Fin m → ℝ}
    (hx : G.Feasible b x) (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z)
    (hy : G.Feasible b y) : x ∈ G.supportSet b y :=
  ⟨hx, hmin y hy⟩

/-- The energy of a minimizer never exceeds the energy of a feasible trial flow. -/
theorem minimizer_energy_le {b : Fin n → ℝ} {x y : Fin m → ℝ}
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z) (hy : G.Feasible b y) :
    G.energy x ≤ G.energy y := hmin y hy

/-! ## Continuity of the energy and of linear goals -/

/-- The total energy is continuous. This is the argument used inline inside
`exists_energy_minimizer`, exposed here as a reusable statement. -/
theorem continuous_energy : Continuous G.energy := by
  apply continuous_finsetSum
  intro e _
  exact (continuous_iff_continuousAt.mpr
    (fun x => (hasDerivAt_edgeEnergy (G.positive e) (G.negative e) x).continuousAt)).comp
    (continuous_apply e)

/-- The total energy is convex on the whole flow space. -/
theorem convexOn_energy (hc : G.Positive) : ConvexOn ℝ Set.univ G.energy := by
  refine ⟨convex_univ, fun x _ z _ a c ha hcnn hac => ?_⟩
  have hpt : ∀ e ∈ (Finset.univ : Finset (Fin m)),
      edgeEnergy (G.positive e) (G.negative e) ((a • x + c • z) e) ≤
        a * edgeEnergy (G.positive e) (G.negative e) (x e) +
          c * edgeEnergy (G.positive e) (G.negative e) (z e) := by
    intro e _
    have h := (convexOn_edgeEnergy (hc.1 e).le (hc.2 e).le).2
      (Set.mem_univ (x e)) (Set.mem_univ (z e)) ha hcnn hac
    simpa [Pi.add_apply, Pi.smul_apply, smul_eq_mul] using h
  calc G.energy (a • x + c • z)
      = ∑ e, edgeEnergy (G.positive e) (G.negative e) ((a • x + c • z) e) := rfl
    _ ≤ ∑ e, (a * edgeEnergy (G.positive e) (G.negative e) (x e)
        + c * edgeEnergy (G.positive e) (G.negative e) (z e)) := Finset.sum_le_sum hpt
    _ = a • G.energy x + c • G.energy z := by
        simp only [energy, smul_eq_mul, Finset.sum_add_distrib, Finset.mul_sum]

/-! ## Soundness of the support bound (CC15) -/

/-- The certified upper bound attached to dual data `(lam, v, R)`. The goal `w` enters
only through the potential `v` and the root witnesses `R`. -/
def supportBound (b : Fin n → ℝ) (y : Fin m → ℝ) (lam : ℝ) (v : Fin n → ℝ)
    (R : Fin m → ℝ) : ℝ :=
  lam * G.energy y + (∑ i, v i * b i) + (2 / 3 : ℝ) * ∑ e, R e

/-- **CC15.** Soundness of the support bound. With strictly positive edge coefficients,
`lam > 0`, nonnegative roots `R` verifying the cubic root test for `s = w - Aᵀ v`,
every point of the support set obeys the goal bound. No optimality of the trial flow
`y` is assumed, and the network may be arbitrary. -/
theorem supportBound_sound {b : Fin n → ℝ} {y : Fin m → ℝ} {v : Fin n → ℝ}
    {w R : Fin m → ℝ} {lam : ℝ} (hc : G.Positive) (hlam : 0 < lam)
    (hR : ∀ e, 0 ≤ R e)
    (hroot : ∀ e, |w e - G.drops v e| ^ 3 ≤ R e ^ 2 *
      (lam * (if 0 ≤ w e - G.drops v e then G.positive e else G.negative e))) :
    ∀ x ∈ G.supportSet b y, ∑ e, w e * x e ≤ G.supportBound b y lam v R := by
  rintro x ⟨hfeas, hE⟩
  have key : ∀ e ∈ (Finset.univ : Finset (Fin m)),
      (w e - G.drops v e) * x e -
          lam * edgeEnergy (G.positive e) (G.negative e) (x e) ≤ (2 / 3 : ℝ) * R e := by
    intro e _
    have hroot' : |w e - G.drops v e| ^ 3 ≤ R e ^ 2 *
        (if 0 ≤ w e - G.drops v e then lam * G.positive e else lam * G.negative e) := by
      rw [← mul_ite_coeff]
      exact hroot e
    have h := fenchel_root_bound (cp := lam * G.positive e) (cm := lam * G.negative e)
      (d := w e - G.drops v e) (x := x e) (u := R e)
      (mul_pos hlam (hc.1 e)) (mul_pos hlam (hc.2 e)) (hR e) hroot'
    rwa [edgeEnergy_smul] at h
  have hsum := Finset.sum_le_sum key
  have henergy : ∑ e, lam * edgeEnergy (G.positive e) (G.negative e) (x e)
      = lam * G.energy x := by
    simp only [energy, Finset.mul_sum]
  have hsplit : ∑ e, (w e - G.drops v e) * x e
      = (∑ e, w e * x e) - ∑ i, v i * b i := by
    rw [G.feasible_pairing hfeas v, ← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun e _ => by ring
  rw [Finset.sum_sub_distrib, henergy, hsplit, ← Finset.mul_sum] at hsum
  have hmono : lam * G.energy x ≤ lam * G.energy y :=
    mul_le_mul_of_nonneg_left hE hlam.le
  simp only [supportBound]
  linarith

/-! ## Two-sided enclosure (CC16) -/

/-- **CC16.** Dual data for `w` and for `-w` give a two-sided enclosure of the goal on
the whole support set. -/
theorem supportBound_two_sided {b : Fin n → ℝ} {y : Fin m → ℝ} {v v' : Fin n → ℝ}
    {w R R' : Fin m → ℝ} {lam lam' : ℝ} (hc : G.Positive)
    (hlam : 0 < lam) (hR : ∀ e, 0 ≤ R e)
    (hroot : ∀ e, |w e - G.drops v e| ^ 3 ≤ R e ^ 2 *
      (lam * (if 0 ≤ w e - G.drops v e then G.positive e else G.negative e)))
    (hlam' : 0 < lam') (hR' : ∀ e, 0 ≤ R' e)
    (hroot' : ∀ e, |(-w e) - G.drops v' e| ^ 3 ≤ R' e ^ 2 *
      (lam' * (if 0 ≤ (-w e) - G.drops v' e then G.positive e else G.negative e))) :
    ∀ x ∈ G.supportSet b y,
      -G.supportBound b y lam' v' R' ≤ ∑ e, w e * x e ∧
        ∑ e, w e * x e ≤ G.supportBound b y lam v R := by
  intro x hx
  refine ⟨?_, G.supportBound_sound hc hlam hR hroot x hx⟩
  have h := G.supportBound_sound (w := fun e => -w e) hc hlam' hR' hroot' x hx
  simp only [neg_mul, Finset.sum_neg_distrib] at h
  linarith

/-- **CC16, physical form.** The two-sided enclosure applies to the physical flow, that is,
to any energy minimizer on the same nominations. -/
theorem support_enclosure_minimizer {b : Fin n → ℝ} {y xs : Fin m → ℝ} {v v' : Fin n → ℝ}
    {w R R' : Fin m → ℝ} {lam lam' : ℝ} (hc : G.Positive)
    (hy : G.Feasible b y) (hxs : G.Feasible b xs)
    (hmin : ∀ z, G.Feasible b z → G.energy xs ≤ G.energy z)
    (hlam : 0 < lam) (hR : ∀ e, 0 ≤ R e)
    (hroot : ∀ e, |w e - G.drops v e| ^ 3 ≤ R e ^ 2 *
      (lam * (if 0 ≤ w e - G.drops v e then G.positive e else G.negative e)))
    (hlam' : 0 < lam') (hR' : ∀ e, 0 ≤ R' e)
    (hroot' : ∀ e, |(-w e) - G.drops v' e| ^ 3 ≤ R' e ^ 2 *
      (lam' * (if 0 ≤ (-w e) - G.drops v' e then G.positive e else G.negative e))) :
    -G.supportBound b y lam' v' R' ≤ ∑ e, w e * xs e ∧
      ∑ e, w e * xs e ≤ G.supportBound b y lam v R :=
  G.supportBound_two_sided hc hlam hR hroot hlam' hR' hroot' xs
    (G.minimizer_mem_supportSet hxs hmin hy)

/-! ## The degenerate case `lam = 0` (CC17, CC20) -/

/-- **CC17(a).** A goal of the form `w = Aᵀ v` is constant on the conservation fiber, with
the exact value `vᵀ b`. -/
theorem goal_constant_of_drops {b : Fin n → ℝ} {w : Fin m → ℝ} {v : Fin n → ℝ}
    (hw : w = G.drops v) {x : Fin m → ℝ} (hx : G.Feasible b x) :
    ∑ e, w e * x e = ∑ i, v i * b i := by
  rw [hw]
  exact (G.feasible_pairing hx v).symm

/-- **CC17(b).** Conversely, a goal that is bounded above on a nonempty conservation fiber
is a vector of potential drops. -/
theorem exists_potential_of_bddAbove {b : Fin n → ℝ} {w y : Fin m → ℝ}
    (hy : G.Feasible b y) (hbdd : ∃ M, ∀ x, G.Feasible b x → ∑ e, w e * x e ≤ M) :
    ∃ v, G.drops v = w := by
  obtain ⟨M, hM⟩ := hbdd
  apply G.exists_potential_of_stationary
  intro d hd
  have hfeas : ∀ t : ℝ, G.Feasible b (y + t • d) := by
    intro t
    change G.divergenceLinear (y + t • d) = b
    rw [map_add, map_smul, show G.divergenceLinear y = b from hy,
      show G.divergenceLinear d = 0 from hd, smul_zero, add_zero]
  have hline : ∀ t : ℝ, (∑ e, w e * y e) + t * ∑ e, w e * d e ≤ M := by
    intro t
    have h := hM _ (hfeas t)
    have hval : ∑ e, w e * ((y + t • d) e)
        = (∑ e, w e * y e) + t * ∑ e, w e * d e := by
      rw [Finset.mul_sum, ← Finset.sum_add_distrib]
      refine Finset.sum_congr rfl fun e _ => ?_
      simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
      ring
    rwa [hval] at h
  by_contra hne
  have h := hline ((M - (∑ e, w e * y e) + 1) / ∑ e, w e * d e)
  rw [div_mul_cancel₀ _ hne] at h
  linarith

/-- **CC17.** On a nonempty conservation fiber, a linear goal is bounded above exactly when
it is a vector of potential drops. -/
theorem bddAbove_goal_iff_exists_potential {b : Fin n → ℝ} {w y : Fin m → ℝ}
    (hy : G.Feasible b y) :
    (∃ M, ∀ x, G.Feasible b x → ∑ e, w e * x e ≤ M) ↔ ∃ v, G.drops v = w := by
  refine ⟨fun h => G.exists_potential_of_bddAbove hy h, ?_⟩
  rintro ⟨v, hv⟩
  exact ⟨∑ i, v i * b i, fun x hx => le_of_eq (G.goal_constant_of_drops hv.symm hx)⟩

/-- At `lam = 0` with no roots the support bound is exactly the rational number `vᵀ b`. -/
theorem supportBound_zero (b : Fin n → ℝ) (y : Fin m → ℝ) (v : Fin n → ℝ) :
    G.supportBound b y 0 v (fun _ => 0) = ∑ i, v i * b i := by
  simp [supportBound]

/-- **CC20.** For a goal `w = Aᵀ v` the value is certified exactly at `lam = 0`, with no
root witnesses, on the whole support set. -/
theorem support_exact_of_drops {b : Fin n → ℝ} {w : Fin m → ℝ} {v : Fin n → ℝ}
    {y : Fin m → ℝ} (hw : w = G.drops v) :
    ∀ x ∈ G.supportSet b y, ∑ e, w e * x e = G.supportBound b y 0 v (fun _ => 0) := by
  intro x hx
  rw [G.supportBound_zero, G.goal_constant_of_drops hw hx.1]

/-! ## Geometry of the support set (CC18) -/

/-- The support set is closed. -/
theorem isClosed_supportSet (b : Fin n → ℝ) (y : Fin m → ℝ) :
    IsClosed (G.supportSet b y) := by
  rw [G.supportSet_eq_inter]
  exact (G.isClosed_feasible b).inter (isClosed_le G.continuous_energy continuous_const)

/-- The support set is convex. -/
theorem convex_supportSet (hc : G.Positive) (b : Fin n → ℝ) (y : Fin m → ℝ) :
    Convex ℝ (G.supportSet b y) := by
  have hsub : Convex ℝ {x : Fin m → ℝ | G.energy x ≤ G.energy y} := by
    simpa using (G.convexOn_energy hc).convex_le (G.energy y)
  rw [G.supportSet_eq_inter]
  exact (G.convex_feasible b).inter hsub

/-- **CC18.** The support set is compact: it is closed and confined to a coordinate box
by the cubic growth of the energy. -/
theorem isCompact_supportSet (hc : G.Positive) (b : Fin n → ℝ) (y : Fin m → ℝ) :
    IsCompact (G.supportSet b y) := by
  set Rb : Fin m → ℝ :=
    fun e => 3 * G.energy y / min (G.positive e) (G.negative e) + 1 with hRb
  have hsub : G.supportSet b y ⊆ Set.Icc (-Rb) Rb := by
    rintro x ⟨-, hE⟩
    have hb : ∀ e, |x e| ≤ Rb e := fun e =>
      abs_le_of_cubic_bound (lt_min (hc.1 e) (hc.2 e)) (G.energy_nonneg hc y)
        ((G.energy_cubic_bound hc x e).trans hE)
    exact ⟨fun e => (abs_le.mp (hb e)).1, fun e => (abs_le.mp (hb e)).2⟩
  exact isCompact_Icc.of_isClosed_subset (G.isClosed_supportSet b y) hsub

/-- The support set is bounded. -/
theorem isBounded_supportSet (hc : G.Positive) (b : Fin n → ℝ) (y : Fin m → ℝ) :
    Bornology.IsBounded (G.supportSet b y) :=
  (G.isCompact_supportSet hc b y).isBounded

/-- **CC18.** Every linear goal attains its maximum on the support set of a feasible
trial flow. -/
theorem exists_max_on_supportSet (hc : G.Positive) {b : Fin n → ℝ} {y : Fin m → ℝ}
    (hy : G.Feasible b y) (w : Fin m → ℝ) :
    ∃ x ∈ G.supportSet b y, ∀ z ∈ G.supportSet b y,
      ∑ e, w e * z e ≤ ∑ e, w e * x e := by
  obtain ⟨x, hx, hmax⟩ := (G.isCompact_supportSet hc b y).exists_isMaxOn
    (G.supportSet_nonempty hy) (continuous_linearGoal w).continuousOn
  exact ⟨x, hx, fun z hz => isMaxOn_iff.mp hmax z hz⟩

end Network

end

end PotentialFlow
