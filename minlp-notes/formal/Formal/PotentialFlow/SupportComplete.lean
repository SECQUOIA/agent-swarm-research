import Formal.PotentialFlow.Bregman
import Formal.PotentialFlow.Support
import Formal.PotentialFlow.RationalBridge
import Formal.PotentialFlow.FieldDuality
import Formal.PotentialFlow.Laplacian

/-! # Completeness and convergence of the support certificates

This module discharges the obligations `CC19` and `CC21` of
`topics/16-potential-flow-certificates/CLAIMS.md`, the completeness and the
convergence halves of `thm:a-cert-support`, and connects `CC20` to the rational
verifier interface.

The soundness half (`CC15`) lives in `Support.lean`. Here we prove the converse:
when the trial energy is strictly above the physical energy, the certified upper
bounds `U_w = lam * E(y) + vᵀ b + (2/3) * ∑ R` cannot be improved. The proof is
entirely finite dimensional and elementary; it uses neither Hahn-Banach separation
nor a general Slater-duality library.

* `Network.exists_support_dual` is the *real* dual attainment statement: either the
  goal is constant on the conservation affine space, or there are `lam > 0`, `v` and
  `R` passing the root test *with equality* whose bound equals the exact support value
  `max_{z ∈ S(y)} wᵀ z`. The multiplier is extracted from a single scalar constraint,
  so no Farkas lemma is needed.
* `RationalNetwork.ratSupportBound_isGLB` is the rational statement: the exact
  decidable rational acceptance predicate `RatSupportAccepted` produces a set of
  rational bounds whose greatest lower bound is exactly the support value. It is
  unconditional in the goal: constant goals are covered by driving `lam` to zero,
  using `RationalNetwork.exists_rat_drops_of_exists_real` to descend a real solution of
  `Aᵀ v = w` to a rational one.
* `Network.supportSet_cubic_bound` is a *quantitative* form of `CC21`: every point of
  `S(y)` is within `(6 (E(y) - E(x*)) / a)^(1/3)` of the physical flow in every
  coordinate. The qualitative convergence statements of the source follow from it
  without any compactness or subsequence argument.
-/

namespace PotentialFlow

noncomputable section

open Filter Topology

/-! ## A quadratic upper bound for the edge divergence -/

private theorem edgeEnergy_neg (cp cm y : ℝ) :
    edgeEnergy cp cm (-y) = edgeEnergy cm cp y := by
  rcases lt_trichotomy y 0 with h | rfl | h
  · rw [edgeEnergy, edgeEnergy, abs_neg, if_pos (by linarith : (0:ℝ) ≤ -y),
      if_neg (not_le.mpr h)]
  · simp [edgeEnergy]
  · rw [edgeEnergy, edgeEnergy, abs_neg, if_neg (not_le.mpr (by linarith : -y < 0)),
      if_pos h.le]

private theorem edgeLaw_neg (cp cm z : ℝ) :
    edgeLaw cp cm (-z) = -edgeLaw cm cp z := by
  rcases lt_trichotomy z 0 with h | rfl | h
  · rw [edgeLaw, edgeLaw, abs_neg, if_pos (by linarith : (0:ℝ) ≤ -z),
      if_neg (not_le.mpr h)]
    ring
  · simp [edgeLaw]
  · rw [edgeLaw, edgeLaw, abs_neg, if_neg (not_le.mpr (by linarith : -z < 0)),
      if_pos h.le]
    ring

private theorem edgeBregman_neg (cp cm y z : ℝ) :
    edgeBregman cp cm (-y) (-z) = edgeBregman cm cp y z := by
  simp only [edgeBregman, edgeEnergy_neg, edgeLaw_neg]
  ring

private theorem same_side_quad {cp M z a : ℝ} (hcp : 0 ≤ cp) (hp : cp ≤ M)
    (hz : 0 ≤ z) :
    cp * (z + a) ^ 3 / 3 - cp * z ^ 3 / 3 - cp * z * z * a ≤ M * (z + |a|) * a ^ 2 := by
  have hM : 0 ≤ M := hcp.trans hp
  rcases le_or_gt 0 a with ha | ha
  · rw [abs_of_nonneg ha]
    nlinarith [mul_nonneg (sub_nonneg.2 hp) (mul_nonneg hz (sq_nonneg a)),
      mul_nonneg (sub_nonneg.2 hp) (pow_nonneg ha 3), mul_nonneg hcp (pow_nonneg ha 3)]
  · rw [abs_of_neg ha]
    have ha3 : a ^ 3 ≤ 0 := by
      have h := mul_nonpos_of_nonpos_of_nonneg ha.le (sq_nonneg a)
      linarith [h]
    nlinarith [mul_nonneg (sub_nonneg.2 hp) (mul_nonneg hz (sq_nonneg a)),
      mul_nonneg hM (neg_nonneg.2 ha3), mul_nonneg hcp (neg_nonneg.2 ha3)]

private theorem cross_side_quad {cp cm M z u : ℝ} (hp : cp ≤ M) (hm : cm ≤ M)
    (hM : 0 ≤ M) (hz : 0 ≤ z) (hu : 0 ≤ u) :
    cm * u ^ 3 / 3 + cp * (2 * z ^ 3 / 3 + z ^ 2 * u) ≤ M * (2 * z + u) * (z + u) ^ 2 := by
  nlinarith [mul_nonneg (sub_nonneg.2 hm) (pow_nonneg hu 3),
    mul_nonneg (sub_nonneg.2 hp) (pow_nonneg hz 3),
    mul_nonneg (sub_nonneg.2 hp) (mul_nonneg (mul_nonneg hz hz) hu),
    mul_nonneg hM (pow_nonneg hz 3), mul_nonneg hM (mul_nonneg (mul_nonneg hz hz) hu),
    mul_nonneg hM (mul_nonneg hz (mul_nonneg hu hu)), mul_nonneg hM (pow_nonneg hu 3)]

private theorem edgeBregman_le_quad_nonneg {cp cm z a : ℝ} (hcp : 0 ≤ cp)
    (hz : 0 ≤ z) :
    edgeBregman cp cm (z + a) z ≤ max cp cm * (|z| + |a|) * a ^ 2 := by
  have hp : cp ≤ max cp cm := le_max_left _ _
  have hm : cm ≤ max cp cm := le_max_right _ _
  have hM : 0 ≤ max cp cm := hcp.trans hp
  have hE1 : edgeEnergy cp cm z = cp * z ^ 3 / 3 := by
    rw [edgeEnergy, if_pos hz, abs_of_nonneg hz]
  have hL1 : edgeLaw cp cm z = cp * z * z := by
    rw [edgeLaw, if_pos hz, abs_of_nonneg hz]
  rw [abs_of_nonneg hz]
  by_cases hza : 0 ≤ z + a
  · have hE2 : edgeEnergy cp cm (z + a) = cp * (z + a) ^ 3 / 3 := by
      rw [edgeEnergy, if_pos hza, abs_of_nonneg hza]
    rw [edgeBregman, hE1, hE2, hL1]
    linarith [same_side_quad hcp hp hz (a := a)]
  · have hlt : z + a < 0 := not_le.mp hza
    have hE2 : edgeEnergy cp cm (z + a) = cm * (-(z + a)) ^ 3 / 3 := by
      rw [edgeEnergy, if_neg hza, abs_of_neg hlt]
    rw [edgeBregman, hE1, hE2, hL1]
    have hu : 0 ≤ -(z + a) := by linarith
    have hav : |a| = -(z + a) + z := by
      rw [abs_of_neg (by linarith : a < 0)]
      ring
    rw [hav]
    linarith [cross_side_quad hp hm hM hz hu]

/-- The edge divergence at a displacement `a` from the base point `z` is quadratic in `a`
with the explicit modulus `max cp cm * (|z| + |a|)`. This is the second-order estimate
driving the first-order optimality argument of the completeness proof. -/
theorem edgeBregman_le_quad (cp cm z a : ℝ) (hcp : 0 ≤ cp) (hcm : 0 ≤ cm) :
    edgeBregman cp cm (z + a) z ≤ max cp cm * (|z| + |a|) * a ^ 2 := by
  rcases le_or_gt 0 z with hz | hz
  · exact edgeBregman_le_quad_nonneg hcp hz
  · have h := edgeBregman_le_quad_nonneg (cp := cm) (cm := cp) (z := -z) (a := -a) hcm
      (by linarith)
    rw [show -z + -a = -(z + a) by ring, edgeBregman_neg] at h
    simpa [max_comm, abs_neg] using h

namespace Network

variable {n m : ℕ} (G : Network n m)

/-- The energy along a segment is dominated by its linearization plus an explicit quadratic
remainder. The coefficient is the sum of the edgewise moduli of `edgeBregman_le_quad`. -/
theorem energy_add_smul_le (z d : Fin m → ℝ) {t : ℝ} (hc : G.Positive)
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    G.energy (z + t • d) ≤ G.energy z
      + t * ∑ e, edgeLaw (G.positive e) (G.negative e) (z e) * d e
      + (∑ e, max (G.positive e) (G.negative e) * (|z e| + |d e|) * d e ^ 2) * t ^ 2 := by
  have key : ∀ e ∈ (Finset.univ : Finset (Fin m)),
      edgeEnergy (G.positive e) (G.negative e) ((z + t • d) e) ≤
        edgeEnergy (G.positive e) (G.negative e) (z e)
          + t * (edgeLaw (G.positive e) (G.negative e) (z e) * d e)
          + max (G.positive e) (G.negative e) * (|z e| + |d e|) * d e ^ 2 * t ^ 2 := by
    intro e _
    have hM : 0 ≤ max (G.positive e) (G.negative e) :=
      (hc.1 e).le.trans (le_max_left _ _)
    have h := edgeBregman_le_quad (G.positive e) (G.negative e) (z e) (t * d e)
      (hc.1 e).le (hc.2 e).le
    have habs : |t * d e| = t * |d e| := by
      rw [abs_mul, abs_of_nonneg ht0]
    have hmono : max (G.positive e) (G.negative e) * (|z e| + t * |d e|) * (t * d e) ^ 2 ≤
        max (G.positive e) (G.negative e) * (|z e| + |d e|) * d e ^ 2 * t ^ 2 := by
      have h1 : t * |d e| ≤ |d e| := by
        nlinarith [abs_nonneg (d e)]
      have h2 : (0:ℝ) ≤ t ^ 2 * d e ^ 2 := by positivity
      nlinarith [mul_nonneg hM h2]
    rw [habs] at h
    have hz : (z + t • d) e = z e + t * d e := by
      simp [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    rw [hz]
    have hbr : edgeBregman (G.positive e) (G.negative e) (z e + t * d e) (z e) =
        edgeEnergy (G.positive e) (G.negative e) (z e + t * d e)
          - edgeEnergy (G.positive e) (G.negative e) (z e)
          - edgeLaw (G.positive e) (G.negative e) (z e) * (t * d e) := by
      simp only [edgeBregman]
      ring_nf
    rw [hbr] at h
    linarith
  have hsum := Finset.sum_le_sum key
  simp only [energy]
  calc ∑ e, edgeEnergy (G.positive e) (G.negative e) ((z + t • d) e)
      ≤ ∑ e, (edgeEnergy (G.positive e) (G.negative e) (z e)
          + t * (edgeLaw (G.positive e) (G.negative e) (z e) * d e)
          + max (G.positive e) (G.negative e) * (|z e| + |d e|) * d e ^ 2 * t ^ 2) := hsum
    _ = _ := by
        rw [Finset.sum_add_distrib, Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.sum_mul]

/-! ## Real dual attainment (CC19, step 1)

The completeness argument of the source invokes Slater duality. We replace it by an
elementary finite-dimensional argument: a second-order expansion of the energy along a
segment, a mixing step with the strictly feasible physical flow, and the extraction of a
multiplier from a *single* scalar constraint, which needs no separation theorem. -/

private theorem continuous_energy_line (z d : Fin m → ℝ) :
    Continuous fun t : ℝ => G.energy (z + t • d) :=
  G.continuous_energy.comp (continuous_const.add (continuous_id.smul continuous_const))

private theorem feasible_add_smul {b : Fin n → ℝ} {z d : Fin m → ℝ}
    (hz : G.Feasible b z) (hd : G.loads d = 0) (t : ℝ) : G.Feasible b (z + t • d) := by
  change G.divergenceLinear (z + t • d) = b
  rw [map_add, map_smul, show G.divergenceLinear z = b from hz,
    show G.divergenceLinear d = 0 from hd, smul_zero, add_zero]

private theorem loads_neg {d : Fin m → ℝ} (hd : G.loads d = 0) : G.loads (-d) = 0 := by
  change G.divergenceLinear (-d) = 0
  rw [map_neg, show G.divergenceLinear d = 0 from hd, neg_zero]

private theorem loads_sub_smul {d d₁ : Fin m → ℝ} (hd : G.loads d = 0)
    (hd₁ : G.loads d₁ = 0) (r : ℝ) : G.loads (d - r • d₁) = 0 := by
  change G.divergenceLinear (d - r • d₁) = 0
  rw [map_sub, map_smul, show G.divergenceLinear d = 0 from hd,
    show G.divergenceLinear d₁ = 0 from hd₁, smul_zero, sub_zero]

private theorem goal_add_smul (w z d : Fin m → ℝ) (t : ℝ) :
    ∑ e, w e * ((z + t • d) e) = (∑ e, w e * z e) + t * ∑ e, w e * d e := by
  rw [Finset.mul_sum, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun e _ => ?_
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  ring

private theorem sum_neg_apply (c d : Fin m → ℝ) :
    ∑ e, c e * ((-d) e) = -∑ e, c e * d e := by
  rw [← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl fun e _ => ?_
  simp only [Pi.neg_apply]
  ring

private theorem sum_sub_smul (c d d₁ : Fin m → ℝ) (r : ℝ) :
    ∑ e, c e * ((d - r • d₁) e) = (∑ e, c e * d e) - r * ∑ e, c e * d₁ e := by
  rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl fun e _ => ?_
  simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
  ring

private theorem sum_convex_comb (w p z : Fin m → ℝ) (μ : ℝ) :
    ∑ e, w e * (((1 - μ) • p + μ • z) e)
      = (1 - μ) * (∑ e, w e * p e) + μ * ∑ e, w e * z e := by
  rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun e _ => ?_
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  ring

/-- If the goal is not constant on the conservation affine space then a maximizer of the
goal on the support set must saturate the energy constraint. -/
private theorem supportSet_max_energy {b : Fin n → ℝ} {y xbar w : Fin m → ℝ}
    (hbar : xbar ∈ G.supportSet b y)
    (hmax : ∀ z ∈ G.supportSet b y, ∑ e, w e * z e ≤ ∑ e, w e * xbar e)
    (hw : ¬ ∃ v, G.drops v = w) : G.energy xbar = G.energy y := by
  refine le_antisymm hbar.2 ?_
  by_contra hlt
  push Not at hlt
  refine hw (G.exists_potential_of_stationary w ?_)
  intro d hd
  have hcont := G.continuous_energy_line xbar d
  have h0 : G.energy (xbar + (0 : ℝ) • d) < G.energy y := by simpa using hlt
  have hev := (hcont.continuousAt (x := 0)).eventually_lt_const h0
  obtain ⟨ε, hε, hball⟩ := Metric.eventually_nhds_iff.mp hev
  have key : ∀ t : ℝ, |t| < ε → t * ∑ e, w e * d e ≤ 0 := by
    intro t ht
    have hlt' : G.energy (xbar + t • d) < G.energy y := by
      refine hball ?_
      rw [Real.dist_eq, sub_zero]
      exact ht
    have hmem : (xbar + t • d) ∈ G.supportSet b y :=
      ⟨G.feasible_add_smul hbar.1 hd t, hlt'.le⟩
    have hle := hmax _ hmem
    rw [goal_add_smul] at hle
    linarith
  have h1 := key (ε / 2) (by rw [abs_of_pos (by linarith)]; linarith)
  have h2 := key (-(ε / 2)) (by rw [abs_of_neg (by linarith)]; linarith)
  have hS1 : ∑ e, w e * d e ≤ 0 :=
    le_of_mul_le_mul_left (by linarith : (ε / 2) * (∑ e, w e * d e) ≤ (ε / 2) * 0)
      (by linarith)
  have hS2 : (0 : ℝ) ≤ ∑ e, w e * d e :=
    le_of_mul_le_mul_left (by linarith : (ε / 2) * 0 ≤ (ε / 2) * ∑ e, w e * d e)
      (by linarith)
  linarith

private theorem first_order_arith {φ K q D t C μ : ℝ}
    (hφ : 0 < φ) (hK : 0 ≤ K) (hq : 0 < q) (hD : 0 ≤ D) (hCq : C * q = K * D)
    (ht0 : 0 < t) (ht1 : t ≤ 1)
    (htq : t * (2 * (K + 1)) ≤ q) (htC : t * (2 * (C + 1)) ≤ φ)
    (hμq : μ * q ≤ K * t ^ 2)
    (hmain : (1 - μ) * (t * φ) ≤ μ * D) : False := by
  have htφ : 0 ≤ t * φ := mul_nonneg ht0.le hφ.le
  have hKt : K * t ^ 2 ≤ K * t := by
    nlinarith [mul_nonneg (mul_nonneg hK ht0.le) (by linarith : (0:ℝ) ≤ 1 - t)]
  have hKt2 : K * t ≤ q / 2 := by linarith
  have hμhalf : μ ≤ 1 / 2 :=
    le_of_mul_le_mul_right (by linarith : μ * q ≤ (1 / 2) * q) hq
  have h2 : (1 / 2) * (t * φ) ≤ μ * D := by
    nlinarith [mul_nonneg (by linarith : (0:ℝ) ≤ 1 / 2 - μ) htφ]
  have hCq2 : (C * t ^ 2) * q = (K * t ^ 2) * D := by linear_combination t ^ 2 * hCq
  have h3 : ((1 / 2) * (t * φ)) * q ≤ (C * t ^ 2) * q := by
    have ha : ((1 / 2) * (t * φ)) * q ≤ (μ * D) * q := mul_le_mul_of_nonneg_right h2 hq.le
    have hb : (μ * q) * D ≤ (K * t ^ 2) * D := mul_le_mul_of_nonneg_right hμq hD
    linarith
  have h5 : (1 / 2) * (t * φ) ≤ C * t ^ 2 := le_of_mul_le_mul_right h3 hq
  have h7 : (1 / 2) * φ ≤ C * t :=
    le_of_mul_le_mul_right (by linarith : ((1 / 2) * φ) * t ≤ (C * t) * t) ht0
  linarith

/-- **First-order optimality.** Every conserved circulation that does not increase the
energy to first order at the maximizer also fails to increase the goal. This is the step
that the source obtains from Slater duality. -/
private theorem first_order (hc : G.Positive) {b : Fin n → ℝ} {x y xbar d w : Fin m → ℝ}
    (hx : G.Feasible b x) (hgap : G.energy x < G.energy y)
    (hbar : xbar ∈ G.supportSet b y) (hbarE : G.energy xbar = G.energy y)
    (hmax : ∀ z ∈ G.supportSet b y, ∑ e, w e * z e ≤ ∑ e, w e * xbar e)
    (hd : G.loads d = 0)
    (hψ : ∑ e, edgeLaw (G.positive e) (G.negative e) (xbar e) * d e ≤ 0) :
    ∑ e, w e * d e ≤ 0 := by
  by_contra hcon
  push Not at hcon
  set φ := ∑ e, w e * d e with hφdef
  set K := ∑ e, max (G.positive e) (G.negative e) * (|xbar e| + |d e|) * d e ^ 2 with hKdef
  have hK : 0 ≤ K := by
    rw [hKdef]
    refine Finset.sum_nonneg fun e _ => ?_
    have hM : (0:ℝ) ≤ max (G.positive e) (G.negative e) := (hc.1 e).le.trans (le_max_left _ _)
    have habs : (0:ℝ) ≤ |xbar e| + |d e| := by positivity
    exact mul_nonneg (mul_nonneg hM habs) (sq_nonneg _)
  set q := G.energy y - G.energy x with hqdef
  have hq : 0 < q := by rw [hqdef]; linarith
  have hxmem : x ∈ G.supportSet b y := ⟨hx, hgap.le⟩
  set D := (∑ e, w e * xbar e) - ∑ e, w e * x e with hDdef
  have hD : 0 ≤ D := by
    rw [hDdef]
    linarith [hmax x hxmem]
  set C := K * D / q with hCdef
  have hC0 : 0 ≤ C := by
    rw [hCdef]
    exact div_nonneg (mul_nonneg hK hD) hq.le
  have hCq : C * q = K * D := by
    rw [hCdef]
    field_simp
  have hKp : (0:ℝ) < 2 * (K + 1) := by linarith
  have hCp : (0:ℝ) < 2 * (C + 1) := by linarith
  set t := min 1 (min (q / (2 * (K + 1))) (φ / (2 * (C + 1)))) with htdef
  have ht0 : 0 < t := by
    rw [htdef]
    exact lt_min one_pos (lt_min (div_pos hq hKp) (div_pos hcon hCp))
  have ht1 : t ≤ 1 := by
    rw [htdef]
    exact min_le_left _ _
  have htq : t * (2 * (K + 1)) ≤ q :=
    (le_div_iff₀ hKp).mp (by rw [htdef]; exact le_trans (min_le_right _ _) (min_le_left _ _))
  have htC : t * (2 * (C + 1)) ≤ φ :=
    (le_div_iff₀ hCp).mp (by rw [htdef]; exact le_trans (min_le_right _ _) (min_le_right _ _))
  have hpfeas : G.Feasible b (xbar + t • d) := G.feasible_add_smul hbar.1 hd t
  have hgoalp : ∑ e, w e * ((xbar + t • d) e) = (∑ e, w e * xbar e) + t * φ := by
    rw [hφdef]
    exact goal_add_smul w xbar d t
  have hpbound := G.energy_add_smul_le xbar d hc ht0.le ht1
  rw [← hKdef] at hpbound
  have hpE : G.energy (xbar + t • d) ≤ G.energy y + K * t ^ 2 := by
    have htψ : t * (∑ e, edgeLaw (G.positive e) (G.negative e) (xbar e) * d e) ≤ 0 :=
      mul_nonpos_of_nonneg_of_nonpos ht0.le hψ
    rw [hbarE] at hpbound
    linarith
  by_cases hple : G.energy (xbar + t • d) ≤ G.energy y
  · have hle := hmax _ ⟨hpfeas, hple⟩
    rw [hgoalp] at hle
    linarith [mul_pos ht0 hcon]
  · push Not at hple
    have hden : 0 < G.energy (xbar + t • d) - G.energy x := by
      rw [hqdef] at hq; linarith
    have hnum : 0 < G.energy (xbar + t • d) - G.energy y := by linarith
    set μ := (G.energy (xbar + t • d) - G.energy y) / (G.energy (xbar + t • d) - G.energy x)
      with hμdef
    have hμ0 : 0 < μ := div_pos hnum hden
    have hμ1 : μ < 1 := by
      rw [hμdef, div_lt_one hden]
      linarith
    have hμid : μ * (G.energy (xbar + t • d) - G.energy x)
        = G.energy (xbar + t • d) - G.energy y := by
      rw [hμdef]
      field_simp
    have hμq : μ * q ≤ K * t ^ 2 := by
      have hqle : q ≤ G.energy (xbar + t • d) - G.energy x := by
        rw [hqdef]; linarith
      nlinarith [mul_nonneg hμ0.le (by linarith : (0:ℝ) ≤
        (G.energy (xbar + t • d) - G.energy x) - q)]
    have hzfeas : G.Feasible b ((1 - μ) • (xbar + t • d) + μ • x) := by
      change G.divergenceLinear _ = b
      rw [map_add, map_smul, map_smul,
        show G.divergenceLinear (xbar + t • d) = b from hpfeas,
        show G.divergenceLinear x = b from hx]
      funext i
      simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
      ring
    have hzE : G.energy ((1 - μ) • (xbar + t • d) + μ • x) ≤ G.energy y := by
      have hconv := (G.convexOn_energy hc).2 (Set.mem_univ (xbar + t • d)) (Set.mem_univ x)
        (by linarith : (0:ℝ) ≤ 1 - μ) hμ0.le (by ring)
      simp only [smul_eq_mul] at hconv
      linarith
    have hmain0 := hmax _ ⟨hzfeas, hzE⟩
    rw [sum_convex_comb, hgoalp] at hmain0
    have hmain : (1 - μ) * (t * φ) ≤ μ * D := by
      rw [hDdef]
      linarith
    exact first_order_arith hcon hK hq hD hCq ht0 ht1 htq htC hμq hmain

/-- **CC19, real dual attainment.** With a trial energy strictly above the physical energy
and a goal that is not constant on the conservation affine space, there are `lam > 0`, a
potential `v` and roots `R` passing the cubic root test *with equality* whose certified
bound is exactly the support value. The multiplier is produced from a one-dimensional
quotient, so no separating hyperplane or Farkas lemma is used. -/
theorem exists_support_dual (hc : G.Positive) {b : Fin n → ℝ} {x y xbar w : Fin m → ℝ}
    (hx : G.Feasible b x) (hgap : G.energy x < G.energy y)
    (hbar : xbar ∈ G.supportSet b y)
    (hmax : ∀ z ∈ G.supportSet b y, ∑ e, w e * z e ≤ ∑ e, w e * xbar e)
    (hw : ¬ ∃ v, G.drops v = w) :
    ∃ (lam : ℝ) (v : Fin n → ℝ) (R : Fin m → ℝ),
      0 < lam ∧ (∀ e, 0 ≤ R e) ∧
      (∀ e, |w e - G.drops v e| ^ 3 = R e ^ 2 *
        (lam * (if 0 ≤ w e - G.drops v e then G.positive e else G.negative e))) ∧
      G.supportBound b y lam v R = ∑ e, w e * xbar e := by
  have hbarE := G.supportSet_max_energy hbar hmax hw
  have hkey : ∀ d : Fin m → ℝ, G.loads d = 0 →
      (∑ e, edgeLaw (G.positive e) (G.negative e) (xbar e) * d e) ≤ 0 →
      ∑ e, w e * d e ≤ 0 :=
    fun d hd hψ => G.first_order hc hx hgap hbar hbarE hmax hd hψ
  have hker : ∀ d : Fin m → ℝ, G.loads d = 0 →
      (∑ e, edgeLaw (G.positive e) (G.negative e) (xbar e) * d e) = 0 →
      ∑ e, w e * d e = 0 := by
    intro d hd hψ
    have h1 := hkey d hd hψ.le
    have h2 := hkey (-d) (G.loads_neg hd) (by rw [sum_neg_apply]; linarith)
    rw [sum_neg_apply] at h2
    linarith
  obtain ⟨d₁, hd₁, hφ₁⟩ : ∃ d, G.loads d = 0 ∧ ∑ e, w e * d e ≠ 0 := by
    by_contra hno
    push Not at hno
    exact hw (G.exists_potential_of_stationary w hno)
  have hψ₁ne : (∑ e, edgeLaw (G.positive e) (G.negative e) (xbar e) * d₁ e) ≠ 0 :=
    fun h => hφ₁ (hker d₁ hd₁ h)
  set ψ₁ := ∑ e, edgeLaw (G.positive e) (G.negative e) (xbar e) * d₁ e with hψ₁def
  set φ₁ := ∑ e, w e * d₁ e with hφ₁def
  set lam := φ₁ / ψ₁ with hlamdef
  have hprop : ∀ d : Fin m → ℝ, G.loads d = 0 →
      ∑ e, w e * d e
        = lam * ∑ e, edgeLaw (G.positive e) (G.negative e) (xbar e) * d e := by
    intro d hd
    have hd' : G.loads (d -
        ((∑ e, edgeLaw (G.positive e) (G.negative e) (xbar e) * d e) / ψ₁) • d₁) = 0 :=
      G.loads_sub_smul hd hd₁ _
    have hψ' : ∑ e, edgeLaw (G.positive e) (G.negative e) (xbar e) *
        ((d - ((∑ e, edgeLaw (G.positive e) (G.negative e) (xbar e) * d e) / ψ₁) • d₁) e)
          = 0 := by
      rw [sum_sub_smul, ← hψ₁def, div_mul_cancel₀ _ hψ₁ne, sub_self]
    have h := hker _ hd' hψ'
    rw [sum_sub_smul, ← hφ₁def] at h
    rw [hlamdef]
    field_simp at h ⊢
    linarith
  have hlam0 : 0 ≤ lam := by
    rcases lt_or_gt_of_ne hψ₁ne with hneg | hpos
    · have h := hkey d₁ hd₁ hneg.le
      rw [← hφ₁def] at h
      rw [hlamdef, show φ₁ / ψ₁ = (-φ₁) / (-ψ₁) from (neg_div_neg_eq _ _).symm]
      exact div_nonneg (by linarith) (by linarith)
    · have h := hkey (-d₁) (G.loads_neg hd₁) (by rw [sum_neg_apply, ← hψ₁def]; linarith)
      rw [sum_neg_apply, ← hφ₁def] at h
      rw [hlamdef]
      exact div_nonneg (by linarith) (by linarith)
  have hlamne : lam ≠ 0 := by
    intro h
    have hrel := hprop d₁ hd₁
    rw [← hφ₁def, ← hψ₁def, h, zero_mul] at hrel
    exact hφ₁ hrel
  have hlam : 0 < lam := hlam0.lt_of_ne (Ne.symm hlamne)
  obtain ⟨v, hv⟩ := G.exists_potential_of_stationary
    (fun e => w e - lam * edgeLaw (G.positive e) (G.negative e) (xbar e)) (by
      intro d hd
      have hsplit : ∑ e, (w e - lam * edgeLaw (G.positive e) (G.negative e) (xbar e)) * d e
          = (∑ e, w e * d e)
            - lam * ∑ e, edgeLaw (G.positive e) (G.negative e) (xbar e) * d e := by
        rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
        exact Finset.sum_congr rfl fun e _ => by ring
      rw [hsplit, hprop d hd, sub_self])
  have hs : ∀ e, w e - G.drops v e
      = lam * edgeLaw (G.positive e) (G.negative e) (xbar e) := by
    intro e
    have h := congrFun hv e
    linarith
  obtain ⟨R, hRdef⟩ : ∃ R : Fin m → ℝ, ∀ e,
      R e = lam * (if 0 ≤ xbar e then G.positive e else G.negative e) * |xbar e| ^ 3 :=
    ⟨_, fun _ => rfl⟩
  have hcoef : ∀ e, 0 < (if 0 ≤ xbar e then G.positive e else G.negative e) := by
    intro e
    by_cases h : 0 ≤ xbar e
    · rw [if_pos h]; exact hc.1 e
    · rw [if_neg h]; exact hc.2 e
  refine ⟨lam, v, R, hlam, fun e => ?_, fun e => ?_, ?_⟩
  · rw [hRdef e]
    exact mul_nonneg (mul_nonneg hlam.le (hcoef e).le) (by positivity)
  · by_cases hu : 0 ≤ xbar e
    · have hlaw : edgeLaw (G.positive e) (G.negative e) (xbar e)
          = G.positive e * xbar e ^ 2 := by
        rw [edgeLaw, if_pos hu, abs_of_nonneg hu]; ring
      have hsval : w e - G.drops v e = lam * (G.positive e * xbar e ^ 2) := by
        rw [hs e, hlaw]
      have hnn : 0 ≤ w e - G.drops v e := by
        rw [hsval]
        exact mul_nonneg hlam.le (mul_nonneg (hc.1 e).le (sq_nonneg _))
      rw [abs_of_nonneg hnn, if_pos hnn, hsval, hRdef e, if_pos hu, abs_of_nonneg hu]
      ring
    · have hu' : xbar e < 0 := not_le.mp hu
      have hune : xbar e ≠ 0 := ne_of_lt hu'
      have hlaw : edgeLaw (G.positive e) (G.negative e) (xbar e)
          = -(G.negative e * xbar e ^ 2) := by
        rw [edgeLaw, if_neg hu, abs_of_neg hu']; ring
      have hsval : w e - G.drops v e = -(lam * (G.negative e * xbar e ^ 2)) := by
        rw [hs e, hlaw]; ring
      have hneg : w e - G.drops v e < 0 := by
        rw [hsval]
        have hpos : 0 < lam * (G.negative e * xbar e ^ 2) :=
          mul_pos hlam (mul_pos (hc.2 e) (by positivity))
        linarith
      rw [abs_of_neg hneg, if_neg (not_le.mpr hneg), hsval, hRdef e, if_neg hu,
        abs_of_neg hu']
      ring
  · have hlawx : ∀ e, edgeLaw (G.positive e) (G.negative e) (xbar e) * xbar e
        = 3 * edgeEnergy (G.positive e) (G.negative e) (xbar e) := by
      intro e
      rw [edgeLaw, edgeEnergy]
      by_cases h : 0 ≤ xbar e
      · simp only [if_pos h, abs_of_nonneg h]; ring
      · simp only [if_neg h, abs_of_neg (not_le.mp h)]; ring
    have hRsum : ∑ e, R e = 3 * lam * G.energy xbar := by
      rw [energy, Finset.mul_sum]
      refine Finset.sum_congr rfl fun e _ => ?_
      rw [hRdef e, edgeEnergy]
      ring
    have hpair : ∑ i, v i * b i = (∑ e, w e * xbar e) - 3 * lam * G.energy xbar := by
      rw [G.feasible_pairing hbar.1 v]
      have hterm : ∀ e, G.drops v e * xbar e
          = w e * xbar e - lam * (3 * edgeEnergy (G.positive e) (G.negative e) (xbar e)) := by
        intro e
        have hdv : G.drops v e
            = w e - lam * edgeLaw (G.positive e) (G.negative e) (xbar e) := by
          linarith [hs e]
        rw [hdv, ← hlawx e]
        ring
      rw [Finset.sum_congr rfl fun e (_ : e ∈ Finset.univ) => hterm e, Finset.sum_sub_distrib]
      congr 1
      rw [energy, Finset.mul_sum]
      exact Finset.sum_congr rfl fun e _ => by ring
    rw [supportBound, hpair, hRsum, hbarE]
    ring

/-! ## Convergence of the support sets (CC21)

The source proves the convergence statement by compactness and a subsequence
argument. We prove instead the *quantitative* estimate `supportSet_cubic_bound`,
which is strictly stronger and much shorter; the qualitative statements of the
source are immediate corollaries of it. -/

/-- **CC21, quantitative core.** Every point of the support set of a trial flow is within
an explicit cube-root distance of the physical flow, in every coordinate. Only a uniform
positive lower bound `a` on the edge coefficients is used. -/
theorem supportSet_cubic_bound {a : ℝ} (ha : 0 < a)
    (hcp : ∀ e, a ≤ G.positive e) (hcm : ∀ e, a ≤ G.negative e)
    {b : Fin n → ℝ} {x y : Fin m → ℝ} (hx : G.Feasible b x)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z) :
    ∀ z ∈ G.supportSet b y, ∀ e, |z e - x e| ^ 3 ≤ 6 * (G.energy y - G.energy x) / a := by
  rintro z ⟨hz, hE⟩ e
  have h := G.energy_minimizer_gap ha hcp hcm hx hz hmin e
  rw [le_div_iff₀ ha]
  nlinarith

/-- **CC21, ball form.** Once the energy gap of the trial flow drops below `a * rho ^ 3 / 6`
its whole support set lies in the `rho`-ball about the physical flow, for the supremum
metric of `Fin m → ℝ`. -/
theorem supportSet_subset_ball {a : ℝ} (ha : 0 < a)
    (hcp : ∀ e, a ≤ G.positive e) (hcm : ∀ e, a ≤ G.negative e)
    {b : Fin n → ℝ} {x y : Fin m → ℝ} (hx : G.Feasible b x)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z)
    {ρ : ℝ} (hρ : 0 < ρ) (hgap : G.energy y - G.energy x < a * ρ ^ 3 / 6) :
    G.supportSet b y ⊆ Metric.ball x ρ := by
  intro z hz
  rw [Metric.mem_ball, dist_pi_lt_iff hρ]
  intro e
  rw [Real.dist_eq]
  have hcube := G.supportSet_cubic_bound ha hcp hcm hx hmin z hz e
  have hlt : |z e - x e| ^ 3 < ρ ^ 3 := by
    have h6 : 6 * (G.energy y - G.energy x) / a < ρ ^ 3 := by
      rw [div_lt_iff₀ ha]
      linarith
    linarith
  by_contra hcon
  have hle : ρ ≤ |z e - x e| := le_of_not_gt hcon
  have : ρ ^ 3 ≤ |z e - x e| ^ 3 := pow_le_pow_left₀ hρ.le hle 3
  linarith

/-- **CC21, sequential form.** For trial energies decreasing to the physical energy, the
support sets are eventually inside every ball about the physical flow. -/
theorem eventually_supportSet_subset_ball {a : ℝ} (ha : 0 < a)
    (hcp : ∀ e, a ≤ G.positive e) (hcm : ∀ e, a ≤ G.negative e)
    {b : Fin n → ℝ} {x : Fin m → ℝ} (hx : G.Feasible b x)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z)
    {yk : ℕ → Fin m → ℝ}
    (hconv : Tendsto (fun k => G.energy (yk k)) atTop (𝓝 (G.energy x)))
    {ρ : ℝ} (hρ : 0 < ρ) :
    ∀ᶠ k in atTop, G.supportSet b (yk k) ⊆ Metric.ball x ρ := by
  have hpos : G.energy x < G.energy x + a * ρ ^ 3 / 6 := by
    have : (0:ℝ) < a * ρ ^ 3 / 6 := by positivity
    linarith
  filter_upwards [hconv.eventually_lt_const hpos] with k hk
  exact G.supportSet_subset_ball ha hcp hcm hx hmin hρ (by linarith)

/-- **CC21, goal form.** Any selection of points from the shrinking support sets has its
linear goal converging to the goal value at the physical flow. -/
theorem tendsto_of_mem_supportSet {a : ℝ} (ha : 0 < a)
    (hcp : ∀ e, a ≤ G.positive e) (hcm : ∀ e, a ≤ G.negative e)
    {b : Fin n → ℝ} {x : Fin m → ℝ} (hx : G.Feasible b x)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z)
    {yk : ℕ → Fin m → ℝ}
    (hconv : Tendsto (fun k => G.energy (yk k)) atTop (𝓝 (G.energy x)))
    (w : Fin m → ℝ) {zk : ℕ → Fin m → ℝ} (hzk : ∀ k, zk k ∈ G.supportSet b (yk k)) :
    Tendsto (fun k => ∑ e, w e * zk k e) atTop (𝓝 (∑ e, w e * x e)) := by
  rw [Metric.tendsto_atTop]
  intro ε hε
  have hW : (0:ℝ) ≤ ∑ e, |w e| := Finset.sum_nonneg fun e _ => abs_nonneg _
  have hWp : (0:ℝ) < (∑ e, |w e|) + 1 := by linarith
  have hρ : (0:ℝ) < ε / ((∑ e, |w e|) + 1) := div_pos hε hWp
  obtain ⟨N, hN⟩ := eventually_atTop.mp
    (G.eventually_supportSet_subset_ball ha hcp hcm hx hmin hconv hρ)
  refine ⟨N, fun k hk => ?_⟩
  have hmem := hN k hk (hzk k)
  have hco : ∀ e, |zk k e - x e| < ε / ((∑ e, |w e|) + 1) := by
    intro e
    have h := (dist_pi_lt_iff hρ).mp (Metric.mem_ball.mp hmem) e
    rwa [Real.dist_eq] at h
  rw [Real.dist_eq]
  have hsplit : (∑ e, w e * zk k e) - ∑ e, w e * x e = ∑ e, w e * (zk k e - x e) := by
    rw [← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun e _ => by ring
  rw [hsplit]
  have hbound : |∑ e, w e * (zk k e - x e)| ≤
      ∑ e, |w e| * (ε / ((∑ e, |w e|) + 1)) := by
    refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun e _ => ?_)
    rw [abs_mul]
    exact mul_le_mul_of_nonneg_left (hco e).le (abs_nonneg _)
  rw [← Finset.sum_mul] at hbound
  have hlast : (∑ e, |w e|) * (ε / ((∑ e, |w e|) + 1)) < ε := by
    rw [mul_div_assoc', div_lt_iff₀ hWp]
    nlinarith
  linarith

/-- **CC21, maxima.** The exact support maxima of a linear goal converge to its value at
the physical flow. -/
theorem tendsto_supportSet_max {a : ℝ} (ha : 0 < a)
    (hcp : ∀ e, a ≤ G.positive e) (hcm : ∀ e, a ≤ G.negative e)
    {b : Fin n → ℝ} {x : Fin m → ℝ} (hx : G.Feasible b x)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z)
    {yk : ℕ → Fin m → ℝ}
    (hconv : Tendsto (fun k => G.energy (yk k)) atTop (𝓝 (G.energy x)))
    (w : Fin m → ℝ) {M : ℕ → ℝ}
    (hM : ∀ k, IsGreatest ((fun z => ∑ e, w e * z e) '' G.supportSet b (yk k)) (M k)) :
    Tendsto M atTop (𝓝 (∑ e, w e * x e)) := by
  choose zk hzk hval using fun k => (hM k).1
  have := G.tendsto_of_mem_supportSet ha hcp hcm hx hmin hconv w hzk
  simpa [funext hval] using this

/-- **CC21, minima.** The exact support minima of a linear goal converge to its value at
the physical flow. -/
theorem tendsto_supportSet_min {a : ℝ} (ha : 0 < a)
    (hcp : ∀ e, a ≤ G.positive e) (hcm : ∀ e, a ≤ G.negative e)
    {b : Fin n → ℝ} {x : Fin m → ℝ} (hx : G.Feasible b x)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z)
    {yk : ℕ → Fin m → ℝ}
    (hconv : Tendsto (fun k => G.energy (yk k)) atTop (𝓝 (G.energy x)))
    (w : Fin m → ℝ) {M : ℕ → ℝ}
    (hM : ∀ k, IsLeast ((fun z => ∑ e, w e * z e) '' G.supportSet b (yk k)) (M k)) :
    Tendsto M atTop (𝓝 (∑ e, w e * x e)) := by
  choose zk hzk hval using fun k => (hM k).1
  have := G.tendsto_of_mem_supportSet ha hcp hcm hx hmin hconv w hzk
  simpa [funext hval] using this

end Network

/-! ## Perturbation estimates for the rational rounding (CC19, step 2) -/

private theorem root_perturb_same {s s' R R' lam lam' c a κ δ B : ℝ}
    (hroot : |s| ^ 3 = R ^ 2 * (lam * c))
    (hR0 : 0 ≤ R) (hκ : 0 < κ) (hRκ : R + κ ≤ R')
    (hlam : 0 < lam) (hlam' : lam ≤ lam') (ha : 0 < a) (hac : a ≤ c)
    (hd : |s' - s| ≤ δ) (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1)
    (hB : |s| ≤ B) (hB1 : 1 ≤ B)
    (hsmall : 7 * B ^ 2 * δ ≤ κ ^ 2 * (lam * a)) :
    |s'| ^ 3 ≤ R' ^ 2 * (lam' * c) := by
  have hs0 : (0:ℝ) ≤ |s| := abs_nonneg s
  have hs'0 : (0:ℝ) ≤ |s'| := abs_nonneg s'
  have habs : |s'| ≤ |s| + δ := by
    have h := abs_sub_abs_le_abs_sub s' s
    linarith
  have hcpos : 0 < c := lt_of_lt_of_le ha hac
  have hsB : |s| ^ 2 ≤ B ^ 2 := by nlinarith
  have hBB : B ≤ B ^ 2 := by nlinarith
  have hδsq : δ ^ 2 ≤ δ := by nlinarith
  have e1 : 3 * |s| ^ 2 * δ ≤ 3 * B ^ 2 * δ := by
    nlinarith [mul_nonneg (sub_nonneg.2 hsB) hδ0]
  have e2 : 3 * |s| * δ ^ 2 ≤ 3 * B ^ 2 * δ := by
    nlinarith [mul_nonneg (sub_nonneg.2 hB) (sq_nonneg δ),
      mul_nonneg (sub_nonneg.2 hBB) (sq_nonneg δ),
      mul_nonneg (sq_nonneg B) (by linarith : (0:ℝ) ≤ δ - δ ^ 2)]
  have e3 : δ ^ 3 ≤ B ^ 2 * δ := by
    nlinarith [mul_nonneg hδ0 (by nlinarith : (0:ℝ) ≤ 1 - δ ^ 2),
      mul_nonneg (by nlinarith : (0:ℝ) ≤ B ^ 2 - 1) hδ0]
  have hcube : |s'| ^ 3 ≤ |s| ^ 3 + 7 * B ^ 2 * δ := by
    have h1 : |s'| ^ 3 ≤ (|s| + δ) ^ 3 := pow_le_pow_left₀ hs'0 habs 3
    nlinarith [h1, e1, e2, e3]
  have hR'2 : R ^ 2 + κ ^ 2 ≤ R' ^ 2 := by
    nlinarith [mul_nonneg hR0 hκ.le,
      mul_nonneg (by linarith : (0:ℝ) ≤ R' - (R + κ)) (by linarith : (0:ℝ) ≤ R' + (R + κ))]
  have hlamc : lam * c ≤ lam' * c := mul_le_mul_of_nonneg_right hlam' hcpos.le
  have hstep : (R ^ 2 + κ ^ 2) * (lam * c) ≤ R' ^ 2 * (lam' * c) :=
    mul_le_mul hR'2 hlamc (by positivity) (sq_nonneg _)
  have hκlam : κ ^ 2 * (lam * a) ≤ κ ^ 2 * (lam * c) := by
    have : lam * a ≤ lam * c := mul_le_mul_of_nonneg_left hac hlam.le
    nlinarith [sq_nonneg κ]
  linarith

private theorem root_perturb_cross {s' R' lam lam' c a κ δ : ℝ}
    (hκ : 0 < κ) (hRκ : κ ≤ R')
    (hlam : 0 < lam) (hlam' : lam ≤ lam') (ha : 0 < a) (hac : a ≤ c)
    (hs' : |s'| ≤ 2 * δ) (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1)
    (hsmall : 8 * δ ≤ κ ^ 2 * (lam * a)) :
    |s'| ^ 3 ≤ R' ^ 2 * (lam' * c) := by
  have hcpos : 0 < c := lt_of_lt_of_le ha hac
  have h1 : |s'| ^ 3 ≤ 8 * δ := by
    have h := pow_le_pow_left₀ (abs_nonneg s') hs' 3
    nlinarith [mul_nonneg hδ0 (by nlinarith : (0:ℝ) ≤ 1 - δ ^ 2)]
  have h2 : κ ^ 2 * (lam * a) ≤ R' ^ 2 * (lam' * c) := by
    refine mul_le_mul ?_ ?_ (by positivity) (sq_nonneg _)
    · nlinarith
    · nlinarith
  linarith

end

/-! ## The rational support certificates and their completeness (CC19, CC20) -/

namespace RationalNetwork

variable {n m : ℕ} (GQ : RationalNetwork n m)

/-- The exact decidable rational acceptance predicate for a support certificate:
`lam > 0`, nonnegative roots, and the cubic root test for `s = w - Aᵀ v`, all in exact
rational arithmetic. -/
def RatSupportAccepted (w : Fin m → ℚ) (lam : ℚ) (v : Fin n → ℚ) (R : Fin m → ℚ) : Prop :=
  0 < lam ∧ (∀ e, 0 ≤ R e) ∧
    ∀ e, |w e - GQ.drops v e| ^ 3 ≤ R e ^ 2 *
      (lam * (if 0 ≤ w e - GQ.drops v e then GQ.positive e else GQ.negative e))

instance (w : Fin m → ℚ) (lam : ℚ) (v : Fin n → ℚ) (R : Fin m → ℚ) :
    Decidable (GQ.RatSupportAccepted w lam v R) := by
  unfold RatSupportAccepted
  infer_instance

/-- The rational support bound attached to accepted rational dual data. -/
def ratSupportBound (b : Fin n → ℚ) (y : Fin m → ℚ) (lam : ℚ) (v : Fin n → ℚ)
    (R : Fin m → ℚ) : ℚ :=
  lam * GQ.energy y + (∑ i, v i * b i) + (2 / 3) * ∑ e, R e

/-- The rational bound is the real bound of the interpreted data. -/
theorem toReal_ratSupportBound (b : Fin n → ℚ) (y : Fin m → ℚ) (lam : ℚ) (v : Fin n → ℚ)
    (R : Fin m → ℚ) :
    ((GQ.ratSupportBound b y lam v R : ℚ) : ℝ)
      = GQ.toReal.supportBound (fun i => (b i : ℝ)) (fun e => (y e : ℝ)) (lam : ℝ)
          (fun i => (v i : ℝ)) (fun e => (R e : ℝ)) := by
  simp only [Network.supportBound, ratSupportBound, GQ.toReal_energy]
  push_cast
  ring

/-- The rational root test is exactly the real root test of the interpreted data. -/
theorem toReal_rootTest (w : Fin m → ℚ) (lam : ℚ) (v : Fin n → ℚ) (R : Fin m → ℚ)
    (e : Fin m) :
    (|(w e : ℝ) - GQ.toReal.drops (fun i => (v i : ℝ)) e| ^ 3 ≤ (R e : ℝ) ^ 2 *
        ((lam : ℝ) * (if 0 ≤ (w e : ℝ) - GQ.toReal.drops (fun i => (v i : ℝ)) e
          then GQ.toReal.positive e else GQ.toReal.negative e)))
      ↔ |w e - GQ.drops v e| ^ 3 ≤ R e ^ 2 *
          (lam * (if 0 ≤ w e - GQ.drops v e then GQ.positive e else GQ.negative e)) := by
  rw [GQ.toReal_drops]
  have hs : (w e : ℝ) - ((GQ.drops v e : ℚ) : ℝ) = ((w e - GQ.drops v e : ℚ) : ℝ) := by
    push_cast
    ring
  by_cases hq : (0:ℚ) ≤ w e - GQ.drops v e
  · rw [if_pos hq, if_pos (show (0:ℝ) ≤ (w e : ℝ) - ((GQ.drops v e : ℚ) : ℝ) by
      rw [hs]; exact_mod_cast hq), hs]
    simp only [toReal]
    exact_mod_cast Iff.rfl
  · rw [if_neg hq, if_neg (show ¬ (0:ℝ) ≤ (w e : ℝ) - ((GQ.drops v e : ℚ) : ℝ) by
      rw [hs]; exact_mod_cast hq), hs]
    simp only [toReal]
    exact_mod_cast Iff.rfl

/-- Accepted rational data are sound: their bound dominates the goal on the whole
support set. This is `CC15` transported to the rational verifier interface. -/
theorem ratSupportBound_sound (hp : ∀ e, 0 < GQ.positive e) (hn : ∀ e, 0 < GQ.negative e)
    {b : Fin n → ℚ} {y : Fin m → ℚ} {w : Fin m → ℚ} {lam : ℚ} {v : Fin n → ℚ}
    {R : Fin m → ℚ} (hacc : GQ.RatSupportAccepted w lam v R) :
    ∀ z ∈ GQ.toReal.supportSet (fun i => (b i : ℝ)) (fun e => (y e : ℝ)),
      ∑ e, (w e : ℝ) * z e ≤ ((GQ.ratSupportBound b y lam v R : ℚ) : ℝ) := by
  have hcpos : GQ.toReal.Positive := by
    refine ⟨fun e => ?_, fun e => ?_⟩
    · change (0:ℝ) < ((GQ.positive e : ℚ) : ℝ)
      exact_mod_cast hp e
    · change (0:ℝ) < ((GQ.negative e : ℚ) : ℝ)
      exact_mod_cast hn e
  intro z hz
  rw [GQ.toReal_ratSupportBound]
  refine GQ.toReal.supportBound_sound hcpos (by exact_mod_cast hacc.1)
    (fun e => by exact_mod_cast hacc.2.1 e) (fun e => ?_) z hz
  exact (GQ.toReal_rootTest w lam v R e).mpr (hacc.2.2 e)

/-- **CC20, rational form.** A goal that is a vector of rational potential drops is
certified exactly, at `lam = 0` and with no roots; the certified number is `vᵀ b`. -/
theorem ratSupportBound_exact_of_drops {b : Fin n → ℚ} {y : Fin m → ℚ} {w : Fin m → ℚ}
    {v : Fin n → ℚ} (hw : w = GQ.drops v) :
    ∀ z ∈ GQ.toReal.supportSet (fun i => (b i : ℝ)) (fun e => (y e : ℝ)),
      ∑ e, (w e : ℝ) * z e
        = ((GQ.ratSupportBound b y 0 v (fun _ => 0) : ℚ) : ℝ) := by
  intro z hz
  have hdrops : (fun e => (w e : ℝ)) = GQ.toReal.drops (fun i => (v i : ℝ)) := by
    funext e
    rw [GQ.toReal_drops, hw]
  have h := GQ.toReal.support_exact_of_drops (b := fun i => (b i : ℝ))
    (y := fun e => (y e : ℝ)) (v := fun i => (v i : ℝ)) (w := fun e => (w e : ℝ))
    hdrops z hz
  rw [h, GQ.toReal.supportBound_zero, ratSupportBound]
  push_cast
  rw [Finset.sum_const, mul_comm]
  simp [mul_comm]

/-- The rational incidence transpose, matching `Network.incidence_transpose`. -/
private theorem rat_incidence_transpose (p : Fin n → ℚ) (e : Fin m) :
    ∑ v, p v * GQ.incidence v e = GQ.drops p e := by
  simp [incidence, drops, mul_sub, Finset.sum_sub_distrib, eq_comm]

open Matrix in
/-- **Rational descent for constant goals.** A rational goal that is a vector of *real*
potential drops is already a vector of *rational* potential drops. Both solvability
statements are the Fredholm alternative `exists_vecMul_iff` for the incidence matrix, over
`ℝ` and over `ℚ`; the annihilation condition descends because rational circulations are in
particular real circulations. -/
theorem exists_rat_drops_of_exists_real (w : Fin m → ℚ)
    (h : ∃ v : Fin n → ℝ, GQ.toReal.drops v = fun e => (w e : ℝ)) :
    ∃ vQ : Fin n → ℚ, GQ.drops vQ = w := by
  classical
  obtain ⟨v, hv⟩ := h
  have hRsolv : ∃ p : Fin n → ℝ,
      p ᵥ* (Matrix.of GQ.toReal.incidence) = fun e => (w e : ℝ) := by
    refine ⟨v, funext fun e => ?_⟩
    have htr := GQ.toReal.incidence_transpose v e
    simp only [Matrix.vecMul, Matrix.of_apply, dotProduct]
    rw [htr, hv]
  rw [exists_vecMul_iff] at hRsolv
  have hQcond : ∀ z : Fin m → ℚ,
      (Matrix.of GQ.incidence) *ᵥ z = 0 → ∑ e, w e * z e = 0 := by
    intro z hz
    have hzR : (Matrix.of GQ.toReal.incidence) *ᵥ (fun e => (z e : ℝ)) = 0 := by
      funext x
      have h1 := congrFun hz x
      simp only [Matrix.mulVec, Matrix.of_apply, dotProduct, Pi.zero_apply] at h1 ⊢
      have hcast : ((∑ e, GQ.incidence x e * z e : ℚ) : ℝ) = ((0 : ℚ) : ℝ) := by rw [h1]
      push_cast at hcast
      simpa [GQ.toReal_incidence] using hcast
    have hR := hRsolv (fun e => (z e : ℝ)) hzR
    have hcast : ((∑ e, w e * z e : ℚ) : ℝ) = 0 := by push_cast; exact hR
    exact_mod_cast hcast
  rw [← exists_vecMul_iff] at hQcond
  obtain ⟨p, hp⟩ := hQcond
  refine ⟨p, funext fun e => ?_⟩
  have hpe := congrFun hp e
  simp only [Matrix.vecMul, Matrix.of_apply, dotProduct] at hpe
  rw [← GQ.rat_incidence_transpose p e]
  exact hpe

/-- The rational energy of a network with positive coefficients is nonnegative. -/
theorem energy_nonneg (hp : ∀ e, 0 < GQ.positive e) (hn : ∀ e, 0 < GQ.negative e)
    (y : Fin m → ℚ) : 0 ≤ GQ.energy y := by
  refine Finset.sum_nonneg fun e _ => ?_
  have hc : (0:ℚ) ≤ (if 0 ≤ y e then GQ.positive e else GQ.negative e) := by
    split
    · exact (hp e).le
    · exact (hn e).le
  have habs : (0:ℚ) ≤ |y e| ^ 3 := by positivity
  exact div_nonneg (mul_nonneg hc habs) (by norm_num)

/-- **CC19, rational approximation.** Rational dual data can always be chosen whose exact
rational bound exceeds the support value by at most `ε`.

For a goal that is a vector of rational potential drops the data are `v` itself with no
roots and a small `lam > 0`; the excess is `lam * E(y)`, which tends to zero.

Otherwise the real dual optimum of `Network.exists_support_dual` is rounded. Perturbing
the multiplier and the potential upwards keeps `lam > 0`, and the roots are chosen
strictly above the real optimal roots, which leaves enough slack in the cubic root test to
absorb the sign changes of `s` at the edges where it vanishes. -/
private theorem exists_rat_support_close
    (hp : ∀ e, 0 < GQ.positive e) (hn : ∀ e, 0 < GQ.negative e)
    {b : Fin n → ℚ} {y : Fin m → ℚ} {w : Fin m → ℚ} {x xbar : Fin m → ℝ}
    (hx : GQ.toReal.Feasible (fun i => (b i : ℝ)) x)
    (hgap : GQ.toReal.energy x < GQ.toReal.energy (fun e => (y e : ℝ)))
    (hbar : xbar ∈ GQ.toReal.supportSet (fun i => (b i : ℝ)) (fun e => (y e : ℝ)))
    (hmax : ∀ z ∈ GQ.toReal.supportSet (fun i => (b i : ℝ)) (fun e => (y e : ℝ)),
      ∑ e, (w e : ℝ) * z e ≤ ∑ e, (w e : ℝ) * xbar e)
    {ε : ℝ} (hε : 0 < ε) :
    ∃ (lam : ℚ) (v : Fin n → ℚ) (R : Fin m → ℚ),
      GQ.RatSupportAccepted w lam v R ∧
      ((GQ.ratSupportBound b y lam v R : ℚ) : ℝ) ≤ (∑ e, (w e : ℝ) * xbar e) + ε := by
  by_cases hwc : ∃ vQ : Fin n → ℚ, GQ.drops vQ = w
  · obtain ⟨vQ, hvQ⟩ := hwc
    have hEQR : (0:ℝ) ≤ ((GQ.energy y : ℚ) : ℝ) := by
      exact_mod_cast GQ.energy_nonneg hp hn y
    obtain ⟨lamq, hlam1, hlam2⟩ := exists_rat_btwn
      (show (0:ℝ) < ε / (((GQ.energy y : ℚ) : ℝ) + 1) from div_pos hε (by linarith))
    have hlamq : 0 < lamq := by exact_mod_cast hlam1
    refine ⟨lamq, vQ, fun _ => 0, ⟨hlamq, fun _ => le_rfl, fun e => ?_⟩, ?_⟩
    · rw [hvQ]
      simp
    · have hdropsR : (fun e => (w e : ℝ)) = GQ.toReal.drops (fun i => (vQ i : ℝ)) := by
        funext e
        rw [GQ.toReal_drops, hvQ]
      have hval := GQ.toReal.goal_constant_of_drops (b := fun i => (b i : ℝ))
        (w := fun e => (w e : ℝ)) (v := fun i => (vQ i : ℝ)) hdropsR hbar.1
      have hbnd : ((GQ.ratSupportBound b y lamq vQ (fun _ => 0) : ℚ) : ℝ)
          = ((lamq : ℚ) : ℝ) * ((GQ.energy y : ℚ) : ℝ)
            + ∑ i, ((vQ i : ℚ) : ℝ) * ((b i : ℚ) : ℝ) := by
        rw [ratSupportBound]
        push_cast
        simp
      rw [hval, hbnd]
      have h2 : ((lamq : ℚ) : ℝ) * ((GQ.energy y : ℚ) : ℝ)
          ≤ (ε / (((GQ.energy y : ℚ) : ℝ) + 1)) * ((GQ.energy y : ℚ) : ℝ) :=
        mul_le_mul_of_nonneg_right hlam2.le hEQR
      have h3 : (ε / (((GQ.energy y : ℚ) : ℝ) + 1)) * ((GQ.energy y : ℚ) : ℝ) ≤ ε := by
        rw [div_mul_eq_mul_div, div_le_iff₀ (by linarith)]
        nlinarith
      linarith
  have hw : ¬ ∃ v : Fin n → ℝ, GQ.toReal.drops v = fun e => (w e : ℝ) := fun h =>
    hwc (GQ.exists_rat_drops_of_exists_real w h)
  rcases Nat.eq_zero_or_pos m with rfl | hm
  · exact absurd ⟨fun _ => 0, funext fun e => e.elim0⟩ hw
  have hcpos : GQ.toReal.Positive := by
    refine ⟨fun e => ?_, fun e => ?_⟩
    · change (0:ℝ) < ((GQ.positive e : ℚ) : ℝ)
      exact_mod_cast hp e
    · change (0:ℝ) < ((GQ.negative e : ℚ) : ℝ)
      exact_mod_cast hn e
  obtain ⟨lam, v, R, hlam, hR0, hroot, hbound⟩ :=
    GQ.toReal.exists_support_dual hcpos hx hgap hbar hmax hw
  have ha : (0:ℝ) < ((GQ.coefficientMinimum hm : ℚ) : ℝ) := by
    exact_mod_cast GQ.coefficientMinimum_positive hm hp hn
  have hap : ∀ e, ((GQ.coefficientMinimum hm : ℚ) : ℝ) ≤ GQ.toReal.positive e := fun e => by
    change ((GQ.coefficientMinimum hm : ℚ) : ℝ) ≤ ((GQ.positive e : ℚ) : ℝ)
    exact_mod_cast GQ.coefficientMinimum_le_positive hm e
  have han : ∀ e, ((GQ.coefficientMinimum hm : ℚ) : ℝ) ≤ GQ.toReal.negative e := fun e => by
    change ((GQ.coefficientMinimum hm : ℚ) : ℝ) ≤ ((GQ.negative e : ℚ) : ℝ)
    exact_mod_cast GQ.coefficientMinimum_le_negative hm e
  set a := ((GQ.coefficientMinimum hm : ℚ) : ℝ) with hadef
  set V := ∑ e, (w e : ℝ) * xbar e with hVdef
  set Ey := GQ.toReal.energy (fun e => (y e : ℝ)) with hEydef
  have hEy0 : 0 ≤ Ey := by
    rw [hEydef]
    exact GQ.toReal.energy_nonneg hcpos _
  have hbsum : (0:ℝ) ≤ ∑ i, |(b i : ℝ)| := Finset.sum_nonneg fun i _ => abs_nonneg _
  have hmnn : (0:ℝ) ≤ (m : ℝ) := Nat.cast_nonneg m
  set Bb := 1 + ∑ e, |(w e : ℝ) - GQ.toReal.drops v e| with hBbdef
  have hBb1 : 1 ≤ Bb := by
    rw [hBbdef]
    have h : (0:ℝ) ≤ ∑ e, |(w e : ℝ) - GQ.toReal.drops v e| :=
      Finset.sum_nonneg fun e _ => abs_nonneg _
    linarith
  have hBbe : ∀ e, |(w e : ℝ) - GQ.toReal.drops v e| ≤ Bb := by
    intro e
    rw [hBbdef]
    have h : |(w e : ℝ) - GQ.toReal.drops v e|
        ≤ ∑ j, |(w j : ℝ) - GQ.toReal.drops v j| :=
      Finset.single_le_sum (f := fun j => |(w j : ℝ) - GQ.toReal.drops v j|)
        (fun j _ => abs_nonneg _) (Finset.mem_univ e)
    linarith
  set T := Ey + (∑ i, |(b i : ℝ)|) + 2 * (m : ℝ) + 1 with hTdef
  have hT : 0 < T := by
    rw [hTdef]; linarith
  have hTne : T ≠ 0 := ne_of_gt hT
  set κ := ε / (2 * T) with hκdef
  have hκ : 0 < κ := by
    rw [hκdef]
    exact div_pos hε (by linarith)
  have hden : (0:ℝ) < 7 * Bb ^ 2 + 8 := by nlinarith
  set δ₀ := min 1 (κ ^ 2 * (lam * a) / (7 * Bb ^ 2 + 8)) with hδ₀def
  have hδ₀ : 0 < δ₀ := by
    rw [hδ₀def]
    exact lt_min one_pos (div_pos (mul_pos (pow_pos hκ 2) (mul_pos hlam ha)) hden)
  set η := min (ε / (2 * T)) (δ₀ / 2) with hηdef
  have hη : 0 < η := by
    rw [hηdef]
    exact lt_min (div_pos hε (by linarith)) (by linarith)
  have hηT : η ≤ ε / (2 * T) := by
    rw [hηdef]; exact min_le_left _ _
  have hηδ : 2 * η ≤ δ₀ := by
    have h := min_le_right (ε / (2 * T)) (δ₀ / 2)
    rw [← hηdef] at h
    linarith
  have hδ1 : 2 * η ≤ 1 := by
    refine le_trans hηδ ?_
    rw [hδ₀def]; exact min_le_left _ _
  have hδsmall : (2 * η) * (7 * Bb ^ 2 + 8) ≤ κ ^ 2 * (lam * a) := by
    refine (le_div_iff₀ hden).mp (le_trans hηδ ?_)
    rw [hδ₀def]; exact min_le_right _ _
  have hp1 : (0:ℝ) ≤ 7 * Bb ^ 2 * (2 * η) := by positivity
  have hp2 : (0:ℝ) ≤ 8 * (2 * η) := by linarith
  have h7 : 7 * Bb ^ 2 * (2 * η) ≤ κ ^ 2 * (lam * a) := by nlinarith
  have h8 : 8 * (2 * η) ≤ κ ^ 2 * (lam * a) := by nlinarith
  obtain ⟨lamq, hlamq1, hlamq2⟩ := exists_rat_btwn (show lam < lam + η by linarith)
  choose vq hvq1 hvq2 using fun i => exists_rat_btwn (show v i < v i + η by linarith)
  choose Rq hRq1 hRq2 using fun e =>
    exists_rat_btwn (show R e + κ < R e + 2 * κ by linarith)
  have hdrop : ∀ e, |((w e : ℝ) - GQ.toReal.drops (fun i => (vq i : ℝ)) e)
      - ((w e : ℝ) - GQ.toReal.drops v e)| ≤ 2 * η := by
    intro e
    simp only [Network.drops]
    rw [abs_le]
    have h1 := hvq1 (GQ.toReal.tail e)
    have h2 := hvq2 (GQ.toReal.tail e)
    have h3 := hvq1 (GQ.toReal.head e)
    have h4 := hvq2 (GQ.toReal.head e)
    constructor <;> linarith
  have hlamle : lam ≤ (lamq : ℝ) := hlamq1.le
  have hrootReal : ∀ e, |(w e : ℝ) - GQ.toReal.drops (fun i => (vq i : ℝ)) e| ^ 3
      ≤ ((Rq e : ℚ) : ℝ) ^ 2 * (((lamq : ℚ) : ℝ) *
        (if 0 ≤ (w e : ℝ) - GQ.toReal.drops (fun i => (vq i : ℝ)) e
          then GQ.toReal.positive e else GQ.toReal.negative e)) := by
    intro e
    have hd := hdrop e
    have hdle := abs_le.mp hd
    have hRκ : R e + κ ≤ ((Rq e : ℚ) : ℝ) := (hRq1 e).le
    have hcross : ∀ _ : True, |(w e : ℝ) - GQ.toReal.drops (fun i => (vq i : ℝ)) e|
        ≤ 2 * (2 * η) → |(w e : ℝ) - GQ.toReal.drops (fun i => (vq i : ℝ)) e| ^ 3
        ≤ ((Rq e : ℚ) : ℝ) ^ 2 * (((lamq : ℚ) : ℝ) * GQ.toReal.positive e) := by
      intro _ hs'
      exact root_perturb_cross hκ (by linarith [hR0 e]) hlam hlamle ha (hap e) hs'
        (by linarith) hδ1 h8
    by_cases h1 : (0:ℝ) ≤ (w e : ℝ) - GQ.toReal.drops v e
    · by_cases h2 : (0:ℝ) ≤ (w e : ℝ) - GQ.toReal.drops (fun i => (vq i : ℝ)) e
      · rw [if_pos h2]
        have hre := hroot e
        rw [if_pos h1] at hre
        exact root_perturb_same hre (hR0 e) hκ hRκ hlam hlamle ha (hap e) hd
          (by linarith) hδ1 (hBbe e) hBb1 h7
      · rw [if_neg h2]
        have h2' : (w e : ℝ) - GQ.toReal.drops (fun i => (vq i : ℝ)) e < 0 := not_le.mp h2
        have hs' : |(w e : ℝ) - GQ.toReal.drops (fun i => (vq i : ℝ)) e| ≤ 2 * (2 * η) := by
          rw [abs_of_neg h2']
          linarith
        exact root_perturb_cross hκ (by linarith [hR0 e]) hlam hlamle ha (han e) hs'
          (by linarith) hδ1 h8
    · have h1' : (w e : ℝ) - GQ.toReal.drops v e < 0 := not_le.mp h1
      by_cases h2 : (0:ℝ) ≤ (w e : ℝ) - GQ.toReal.drops (fun i => (vq i : ℝ)) e
      · rw [if_pos h2]
        have hs' : |(w e : ℝ) - GQ.toReal.drops (fun i => (vq i : ℝ)) e| ≤ 2 * (2 * η) := by
          rw [abs_of_nonneg h2]
          linarith
        exact hcross trivial hs'
      · rw [if_neg h2]
        have hre := hroot e
        rw [if_neg h1] at hre
        exact root_perturb_same hre (hR0 e) hκ hRκ hlam hlamle ha (han e) hd
          (by linarith) hδ1 (hBbe e) hBb1 h7
  refine ⟨lamq, vq, Rq, ⟨?_, fun e => ?_, fun e => ?_⟩, ?_⟩
  · have h : (0:ℝ) < ((lamq : ℚ) : ℝ) := by linarith
    exact_mod_cast h
  · have h : (0:ℝ) ≤ ((Rq e : ℚ) : ℝ) := by linarith [hR0 e, hRq1 e]
    exact_mod_cast h
  · exact (GQ.toReal_rootTest w lamq vq Rq e).mp (hrootReal e)
  · rw [GQ.toReal_ratSupportBound, Network.supportBound, ← hEydef]
    have hb := hbound
    rw [Network.supportBound, ← hEydef] at hb
    have hvsum : ∑ i, ((vq i : ℝ) * (b i : ℝ))
        ≤ (∑ i, v i * (b i : ℝ)) + η * ∑ i, |(b i : ℝ)| := by
      rw [Finset.mul_sum, ← Finset.sum_add_distrib]
      refine Finset.sum_le_sum fun i _ => ?_
      have h1 := (hvq1 i).le
      have h2 := (hvq2 i).le
      have h3 : (b i : ℝ) ≤ |(b i : ℝ)| := le_abs_self _
      nlinarith [mul_nonneg (by linarith : (0:ℝ) ≤ ((vq i : ℚ) : ℝ) - v i)
          (by linarith : (0:ℝ) ≤ |(b i : ℝ)| - (b i : ℝ)),
        mul_nonneg (by linarith : (0:ℝ) ≤ η - (((vq i : ℚ) : ℝ) - v i))
          (abs_nonneg ((b i : ℝ)))]
    have hRsum : ∑ e, ((Rq e : ℚ) : ℝ) ≤ (∑ e, R e) + 2 * (m : ℝ) * κ := by
      calc ∑ e, ((Rq e : ℚ) : ℝ) ≤ ∑ e, (R e + 2 * κ) :=
            Finset.sum_le_sum fun e _ => (hRq2 e).le
        _ = (∑ e, R e) + 2 * (m : ℝ) * κ := by
            rw [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
              nsmul_eq_mul]
            ring
    have hXle : Ey + ∑ i, |(b i : ℝ)| ≤ T := by
      rw [hTdef]; linarith
    have hA : η * (Ey + ∑ i, |(b i : ℝ)|) ≤ ε / 2 := by
      have hmul := mul_le_mul hηT hXle (by linarith) (le_of_lt (div_pos hε (by linarith)))
      have heq : (ε / (2 * T)) * T = ε / 2 := by field_simp
      linarith
    have hB2 : (4 / 3) * (m : ℝ) * κ ≤ ε / 2 := by
      have hmT : (4 / 3) * (m : ℝ) ≤ T := by rw [hTdef]; linarith
      have hmul := mul_le_mul_of_nonneg_right hmT hκ.le
      have heq : T * κ = ε / 2 := by
        rw [hκdef]; field_simp
      linarith
    have hEylam : ((lamq : ℚ) : ℝ) * Ey ≤ lam * Ey + η * Ey := by
      nlinarith [mul_nonneg (by linarith [hlamq2] : (0:ℝ) ≤ lam + η - ((lamq : ℚ) : ℝ)) hEy0]
    linarith

/-- **CC19.** For a trial flow whose energy is strictly above the physical energy, the
exact support value is the greatest lower bound of the valid *rational* certified upper
bounds, for *every* goal. Soundness gives the lower-bound half; the real dual optimum
together with its rational rounding, and the vanishing-multiplier family for constant
goals, give that no larger number is a lower bound. No hypothesis on `w` remains. -/
theorem ratSupportBound_isGLB
    (hp : ∀ e, 0 < GQ.positive e) (hn : ∀ e, 0 < GQ.negative e)
    {b : Fin n → ℚ} {y : Fin m → ℚ} {w : Fin m → ℚ} {x xbar : Fin m → ℝ}
    (hx : GQ.toReal.Feasible (fun i => (b i : ℝ)) x)
    (hgap : GQ.toReal.energy x < GQ.toReal.energy (fun e => (y e : ℝ)))
    (hbar : xbar ∈ GQ.toReal.supportSet (fun i => (b i : ℝ)) (fun e => (y e : ℝ)))
    (hmax : ∀ z ∈ GQ.toReal.supportSet (fun i => (b i : ℝ)) (fun e => (y e : ℝ)),
      ∑ e, (w e : ℝ) * z e ≤ ∑ e, (w e : ℝ) * xbar e) :
    IsGLB {u : ℝ | ∃ (lam : ℚ) (v : Fin n → ℚ) (R : Fin m → ℚ),
        GQ.RatSupportAccepted w lam v R ∧
        u = ((GQ.ratSupportBound b y lam v R : ℚ) : ℝ)}
      (∑ e, (w e : ℝ) * xbar e) := by
  constructor
  · rintro u ⟨lam, v, R, hacc, rfl⟩
    exact GQ.ratSupportBound_sound hp hn hacc xbar hbar
  · intro u hu
    refine le_of_forall_pos_le_add fun ε hε => ?_
    obtain ⟨lam, v, R, hacc, hle⟩ :=
      GQ.exists_rat_support_close hp hn hx hgap hbar hmax hε
    exact le_trans (hu ⟨lam, v, R, hacc, rfl⟩) hle

/-- **CC19, packaged form.** For a rational feasible trial flow `y` whose energy strictly
exceeds that of some feasible `x` — in particular that of the physical flow — every linear
goal attains its maximum on the support set, and that maximum is exactly the greatest
lower bound of the certified bounds of the accepted rational dual data. -/
theorem exists_max_isGLB_ratSupportBound
    (hp : ∀ e, 0 < GQ.positive e) (hn : ∀ e, 0 < GQ.negative e)
    {b : Fin n → ℚ} {y : Fin m → ℚ} {w : Fin m → ℚ} {x : Fin m → ℝ}
    (hy : GQ.loads y = b)
    (hx : GQ.toReal.Feasible (fun i => (b i : ℝ)) x)
    (hgap : GQ.toReal.energy x < GQ.toReal.energy (fun e => (y e : ℝ))) :
    ∃ xbar ∈ GQ.toReal.supportSet (fun i => (b i : ℝ)) (fun e => (y e : ℝ)),
      (∀ z ∈ GQ.toReal.supportSet (fun i => (b i : ℝ)) (fun e => (y e : ℝ)),
          ∑ e, (w e : ℝ) * z e ≤ ∑ e, (w e : ℝ) * xbar e) ∧
        IsGLB {u : ℝ | ∃ (lam : ℚ) (v : Fin n → ℚ) (R : Fin m → ℚ),
            GQ.RatSupportAccepted w lam v R ∧
            u = ((GQ.ratSupportBound b y lam v R : ℚ) : ℝ)}
          (∑ e, (w e : ℝ) * xbar e) := by
  have hcpos : GQ.toReal.Positive := by
    refine ⟨fun e => ?_, fun e => ?_⟩
    · change (0:ℝ) < ((GQ.positive e : ℚ) : ℝ)
      exact_mod_cast hp e
    · change (0:ℝ) < ((GQ.negative e : ℚ) : ℝ)
      exact_mod_cast hn e
  have hyfeas : GQ.toReal.Feasible (fun i => (b i : ℝ)) (fun e => (y e : ℝ)) := by
    ext i
    rw [GQ.toReal_loads, hy]
  obtain ⟨xbar, hbar, hmax⟩ :=
    GQ.toReal.exists_max_on_supportSet hcpos hyfeas (fun e => (w e : ℝ))
  exact ⟨xbar, hbar, hmax, GQ.ratSupportBound_isGLB hp hn hx hgap hbar hmax⟩

end RationalNetwork

end PotentialFlow
