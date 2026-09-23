import Formal.PotentialFlow.Certificate

/-! Bregman divergences of the asymmetric cubic edge energy.

This module adds the separate-edge divergence `D_e(y, z)`, its shape (nonnegativity,
a unique zero, strict monotonicity on each side of `y`), the exact network identity
`E(y) - E(x*) = ∑ D_e(y_e, x*_e)`, the resulting per-edge interval certificates,
the enclosure of physical drops and of potential objectives, and the coordinate-free
solvability criterion for nominations. -/

namespace PotentialFlow

noncomputable section

/-- Bregman divergence of the edge energy: the gap at `y` of the tangent line at `z`. -/
def edgeBregman (cp cm y z : ℝ) : ℝ :=
  edgeEnergy cp cm y - edgeEnergy cp cm z - edgeLaw cp cm z * (y - z)

/-- The cubic modulus of `Modulus.lean`, restated for `edgeBregman`. -/
theorem edgeBregman_modulus (cp cm a y z : ℝ) (ha : 0 < a) (hcp : a ≤ cp) (hcm : a ≤ cm) :
    a / 6 * |y - z| ^ 3 ≤ edgeBregman cp cm y z :=
  edge_bregman_modulus cp cm a z y ha hcp hcm

/-- The divergence vanishes on the diagonal. -/
@[simp] theorem edgeBregman_self (cp cm y : ℝ) : edgeBregman cp cm y y = 0 := by
  simp [edgeBregman]

/-- Positive coefficients make the divergence nonnegative. -/
theorem edgeBregman_nonneg {cp cm : ℝ} (hcp : 0 < cp) (hcm : 0 < cm) (y z : ℝ) :
    0 ≤ edgeBregman cp cm y z := by
  refine le_trans ?_ (edgeBregman_modulus cp cm (min cp cm) y z (lt_min hcp hcm)
    (min_le_left _ _) (min_le_right _ _))
  have : 0 < min cp cm := lt_min hcp hcm
  positivity

/-- Off the diagonal the divergence is strictly positive. -/
theorem edgeBregman_pos {cp cm : ℝ} (hcp : 0 < cp) (hcm : 0 < cm) {y z : ℝ} (h : z ≠ y) :
    0 < edgeBregman cp cm y z := by
  have hz : 0 < |y - z| := abs_pos.mpr (sub_ne_zero_of_ne (Ne.symm h))
  have hpos : 0 < min cp cm / 6 * |y - z| ^ 3 :=
    mul_pos (by have := lt_min hcp hcm; positivity) (pow_pos hz 3)
  exact hpos.trans_le (edgeBregman_modulus cp cm (min cp cm) y z (lt_min hcp hcm)
    (min_le_left _ _) (min_le_right _ _))

/-- The divergence vanishes exactly on the diagonal. -/
theorem edgeBregman_eq_zero_iff {cp cm : ℝ} (hcp : 0 < cp) (hcm : 0 < cm) (y z : ℝ) :
    edgeBregman cp cm y z = 0 ↔ z = y := by
  refine ⟨fun h => ?_, fun h => by rw [h]; simp⟩
  by_contra hne
  exact absurd h (edgeBregman_pos hcp hcm hne).ne'

/-- The three-point identity relating two base points of the same divergence. -/
theorem edgeBregman_sub (cp cm y z w : ℝ) :
    edgeBregman cp cm y z - edgeBregman cp cm y w =
      edgeBregman cp cm w z + (edgeLaw cp cm w - edgeLaw cp cm z) * (y - w) := by
  simp only [edgeBregman]; ring

/-- Moving the base point towards `y` from below strictly decreases the divergence,
including across an interval containing zero, where the derivative vanishes. -/
theorem strictAntiOn_edgeBregman {cp cm : ℝ} (hcp : 0 < cp) (hcm : 0 < cm) (y : ℝ) :
    StrictAntiOn (edgeBregman cp cm y) (Set.Iic y) := by
  intro z _ w hw hzw
  have hid := edgeBregman_sub cp cm y z w
  have hpos : 0 < edgeBregman cp cm w z := edgeBregman_pos hcp hcm (ne_of_lt hzw)
  have hmono : edgeLaw cp cm z ≤ edgeLaw cp cm w :=
    edgeLaw_monotone hcp.le hcm.le hzw.le
  have hyw : (0 : ℝ) ≤ y - w := sub_nonneg.mpr (Set.mem_Iic.mp hw)
  have hprod : 0 ≤ (edgeLaw cp cm w - edgeLaw cp cm z) * (y - w) :=
    mul_nonneg (sub_nonneg.mpr hmono) hyw
  linarith

/-- Moving the base point away from `y` from above strictly increases the divergence,
including across an interval containing zero, where the derivative vanishes. -/
theorem strictMonoOn_edgeBregman {cp cm : ℝ} (hcp : 0 < cp) (hcm : 0 < cm) (y : ℝ) :
    StrictMonoOn (edgeBregman cp cm y) (Set.Ici y) := by
  intro z hz w _ hzw
  have hid := edgeBregman_sub cp cm y w z
  have hpos : 0 < edgeBregman cp cm z w := edgeBregman_pos hcp hcm (ne_of_gt hzw)
  have hmono : edgeLaw cp cm z ≤ edgeLaw cp cm w :=
    edgeLaw_monotone hcp.le hcm.le hzw.le
  have hyz : y - z ≤ 0 := sub_nonpos.mpr (Set.mem_Ici.mp hz)
  have hneg : edgeLaw cp cm z - edgeLaw cp cm w ≤ 0 := sub_nonpos.mpr hmono
  have hprod : 0 ≤ (edgeLaw cp cm z - edgeLaw cp cm w) * (y - z) := by nlinarith
  linarith

/-- The uniform-radius endpoints `y ± η` pass the divergence test whenever the
certified gap obeys `6δ ≤ η³ a`. -/
theorem le_edgeBregman_of_radius {cp cm a δ η : ℝ} (y : ℝ) (ha : 0 < a) (hcp : a ≤ cp)
    (hcm : a ≤ cm) (hη : 0 ≤ η) (hδ : 6 * δ ≤ η ^ 3 * a) :
    δ ≤ edgeBregman cp cm y (y - η) ∧ δ ≤ edgeBregman cp cm y (y + η) := by
  have h₁ := edgeBregman_modulus cp cm a y (y - η) ha hcp hcm
  have h₂ := edgeBregman_modulus cp cm a y (y + η) ha hcp hcm
  rw [show y - (y - η) = η by ring, abs_of_nonneg hη] at h₁
  rw [show y - (y + η) = -η by ring, abs_neg, abs_of_nonneg hη] at h₂
  constructor <;> linarith

/-- A value between two bounds has its product with any sign of scale enclosed by the
corresponding signed endpoint products. -/
private theorem mul_mem_minmax {g₁ g₂ t c : ℝ} (h₁ : g₁ ≤ t) (h₂ : t ≤ g₂) :
    min (g₁ * c) (g₂ * c) ≤ t * c ∧ t * c ≤ max (g₁ * c) (g₂ * c) := by
  rcases le_total 0 c with hc | hc
  · exact ⟨(min_le_left _ _).trans (mul_le_mul_of_nonneg_right h₁ hc),
      (mul_le_mul_of_nonneg_right h₂ hc).trans (le_max_right _ _)⟩
  · exact ⟨(min_le_right _ _).trans (mul_le_mul_of_nonpos_right h₂ hc),
      (mul_le_mul_of_nonpos_right h₁ hc).trans (le_max_left _ _)⟩

/-- With positive coefficients the divergence determines its base point above `y`:
it is injective on the closed side `[y, ∞)`. -/
theorem edgeBregman_injOn_Ici {cp cm : ℝ} (hcp : 0 < cp) (hcm : 0 < cm) (y : ℝ) :
    Set.InjOn (edgeBregman cp cm y) (Set.Ici y) :=
  (strictMonoOn_edgeBregman hcp hcm y).injOn

/-- With positive coefficients the divergence determines its base point below `y`:
it is injective on the closed side `(-∞, y]`. -/
theorem edgeBregman_injOn_Iic {cp cm : ℝ} (hcp : 0 < cp) (hcm : 0 < cm) (y : ℝ) :
    Set.InjOn (edgeBregman cp cm y) (Set.Iic y) :=
  (strictAntiOn_edgeBregman hcp hcm y).injOn

namespace Network

variable {n m : ℕ} (G : Network n m)

/-- Conservation and stationarity give the exact Bregman decomposition of the energy gap. -/
theorem energy_sub_eq_sum_edgeBregman {b : Fin n → ℝ} {x y : Fin m → ℝ}
    (hx : G.Feasible b x) (hy : G.Feasible b y)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z) :
    G.energy y - G.energy x =
      ∑ e, edgeBregman (G.positive e) (G.negative e) (y e) (x e) := by
  simp only [edgeBregman, Finset.sum_sub_distrib,
    G.energy_minimizer_stationary hx hy hmin, sub_zero, energy]

/-- Every summand of the Bregman decomposition is nonnegative, so each is at most the gap. -/
theorem edgeBregman_le_energy_sub (hc : G.Positive) {b : Fin n → ℝ} {x y : Fin m → ℝ}
    (hx : G.Feasible b x) (hy : G.Feasible b y)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z) (e : Fin m) :
    edgeBregman (G.positive e) (G.negative e) (y e) (x e) ≤ G.energy y - G.energy x := by
  rw [G.energy_sub_eq_sum_edgeBregman hx hy hmin]
  exact Finset.single_le_sum (fun j _ => edgeBregman_nonneg (hc.1 j) (hc.2 j) _ _)
    (Finset.mem_univ e)

/-- Per-edge interval soundness: outward endpoint tests at a verified gap enclose the
minimizing flow on that edge. The endpoints are arbitrary reals, so rational endpoints
cast to `ℝ` are covered. -/
theorem mem_interval_of_edgeBregman (hc : G.Positive) {b : Fin n → ℝ} {x y : Fin m → ℝ}
    {δ lo hi : ℝ} (hx : G.Feasible b x) (hy : G.Feasible b y)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z)
    (hδ : G.energy y - G.energy x ≤ δ) {e : Fin m}
    (hlo : lo ≤ y e) (hhi : y e ≤ hi)
    (hlB : δ ≤ edgeBregman (G.positive e) (G.negative e) (y e) lo)
    (hhB : δ ≤ edgeBregman (G.positive e) (G.negative e) (y e) hi) :
    lo ≤ x e ∧ x e ≤ hi := by
  have hle : edgeBregman (G.positive e) (G.negative e) (y e) (x e) ≤ δ :=
    (G.edgeBregman_le_energy_sub hc hx hy hmin e).trans hδ
  constructor
  · by_contra hcon
    push Not at hcon
    have h := strictAntiOn_edgeBregman (hc.1 e) (hc.2 e) (y e)
      (Set.mem_Iic.mpr (hcon.le.trans hlo)) (Set.mem_Iic.mpr hlo) hcon
    linarith
  · by_contra hcon
    push Not at hcon
    have h := strictMonoOn_edgeBregman (hc.1 e) (hc.2 e) (y e)
      (Set.mem_Ici.mpr hhi) (Set.mem_Ici.mpr (hhi.trans hcon.le)) hcon
    linarith

/-- The `∀`-edge form of the interval certificate. -/
theorem mem_intervals_of_edgeBregman (hc : G.Positive) {b : Fin n → ℝ}
    {x y l u : Fin m → ℝ} {δ : ℝ} (hx : G.Feasible b x) (hy : G.Feasible b y)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z)
    (hδ : G.energy y - G.energy x ≤ δ)
    (hlo : ∀ e, l e ≤ y e) (hhi : ∀ e, y e ≤ u e)
    (hlB : ∀ e, δ ≤ edgeBregman (G.positive e) (G.negative e) (y e) (l e))
    (hhB : ∀ e, δ ≤ edgeBregman (G.positive e) (G.negative e) (y e) (u e)) :
    ∀ e, l e ≤ x e ∧ x e ≤ u e := fun e =>
  G.mem_interval_of_edgeBregman hc hx hy hmin hδ (hlo e) (hhi e) (hlB e) (hhB e)

/-- Zero verified gap forces the candidate to be the minimizer, so singleton intervals
are valid with no curvature hypothesis. -/
theorem eq_minimizer_of_energy_le (hc : G.Positive) {b : Fin n → ℝ} {x y : Fin m → ℝ}
    (hx : G.Feasible b x) (hy : G.Feasible b y)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z)
    (hle : G.energy y ≤ G.energy x) : y = x :=
  G.energy_minimizer_unique hc hy hx (fun z hz => hle.trans (hmin z hz)) hmin

/-- The uniform certified radius always supplies a valid outer bracket. -/
theorem le_edgeBregman_radius_endpoints {a δ η : ℝ} {y : Fin m → ℝ}
    (ha : 0 < a) (hcp : ∀ e, a ≤ G.positive e) (hcm : ∀ e, a ≤ G.negative e)
    (hη : 0 ≤ η) (hδ : 6 * δ ≤ η ^ 3 * a) (e : Fin m) :
    δ ≤ edgeBregman (G.positive e) (G.negative e) (y e) (y e - η) ∧
      δ ≤ edgeBregman (G.positive e) (G.negative e) (y e) (y e + η) :=
  le_edgeBregman_of_radius (y e) ha (hcp e) (hcm e) hη hδ

/-- Verified flow intervals enclose the physical edge drop, by monotonicity of the edge law. -/
theorem drop_enclosure (hc : G.Positive) {x l u : Fin m → ℝ}
    (hlu : ∀ e, l e ≤ x e ∧ x e ≤ u e) (e : Fin m) :
    edgeLaw (G.positive e) (G.negative e) (l e) ≤
        edgeLaw (G.positive e) (G.negative e) (x e) ∧
      edgeLaw (G.positive e) (G.negative e) (x e) ≤
        edgeLaw (G.positive e) (G.negative e) (u e) :=
  ⟨edgeLaw_monotone (hc.1 e).le (hc.2 e).le (hlu e).1,
    edgeLaw_monotone (hc.1 e).le (hc.2 e).le (hlu e).2⟩

/-- The potential objective of a nomination equals the pairing of any flow moving that
nomination with the physical drops. The identity holds for every potential of the
physical state, hence is gauge independent. -/
theorem potential_objective {x q : Fin m → ℝ} {p a : Fin n → ℝ}
    (hp : G.drops p = fun e => edgeLaw (G.positive e) (G.negative e) (x e))
    (hq : G.loads q = a) :
    ∑ v, p v * a v = ∑ e, edgeLaw (G.positive e) (G.negative e) (x e) * q e := by
  rw [G.feasible_pairing hq p]
  simp only [hp]

/-- Signed interval arithmetic over the flow `q` encloses the potential objective. -/
theorem potential_objective_enclosure (hc : G.Positive) {x l u q : Fin m → ℝ}
    {p a : Fin n → ℝ}
    (hp : G.drops p = fun e => edgeLaw (G.positive e) (G.negative e) (x e))
    (hq : G.loads q = a) (hlu : ∀ e, l e ≤ x e ∧ x e ≤ u e) :
    (∑ e, min (edgeLaw (G.positive e) (G.negative e) (l e) * q e)
        (edgeLaw (G.positive e) (G.negative e) (u e) * q e)) ≤ ∑ v, p v * a v ∧
      (∑ v, p v * a v) ≤ ∑ e, max (edgeLaw (G.positive e) (G.negative e) (l e) * q e)
        (edgeLaw (G.positive e) (G.negative e) (u e) * q e) := by
  rw [G.potential_objective hp hq]
  exact ⟨Finset.sum_le_sum fun e _ =>
      (mul_mem_minmax (G.drop_enclosure hc hlu e).1 (G.drop_enclosure hc hlu e).2).1,
    Finset.sum_le_sum fun e _ =>
      (mul_mem_minmax (G.drop_enclosure hc hlu e).1 (G.drop_enclosure hc hlu e).2).2⟩

/-- A nomination is movable by some conserved flow exactly when it annihilates every
potential vector with zero drops. Disconnected graphs and self-loops are included. -/
theorem exists_loads_iff {a : Fin n → ℝ} :
    (∃ q, G.loads q = a) ↔ ∀ p : Fin n → ℝ, G.drops p = 0 → ∑ v, p v * a v = 0 := by
  constructor
  · rintro ⟨q, hq⟩ p hp
    rw [G.feasible_pairing hq p, hp]
    simp
  · intro h
    have hmem : a ∈ LinearMap.range G.divergenceLinear := by
      rw [← Subspace.forall_mem_dualAnnihilator_apply_eq_zero_iff]
      intro φ hφ
      set p : Fin n → ℝ := (dotProductEquiv ℝ (Fin n)).symm φ with hpdef
      have hφp : dotProductEquiv ℝ (Fin n) p = φ :=
        (dotProductEquiv ℝ (Fin n)).apply_symm_apply φ
      have hdrops : G.drops p = 0 := by
        have hz : ∀ x : Fin m → ℝ, ∑ e, G.drops p e * x e = 0 := by
          intro x
          have hx := (Submodule.mem_dualAnnihilator φ).mp hφ (G.divergenceLinear x) ⟨x, rfl⟩
          rw [← hφp] at hx
          rw [← G.conservation_pairing x p]
          simpa [dotProduct, loads] using hx
        funext e
        have hse := hz (fun j => if j = e then 1 else 0)
        simpa using hse
      have := h p hdrops
      rw [← hφp]
      simpa [dotProduct] using this
    obtain ⟨q, hq⟩ := hmem
    exact ⟨q, hq⟩

end Network

end

end PotentialFlow
