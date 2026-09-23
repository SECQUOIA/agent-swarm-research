import Formal.PotentialFlow.Scalar

/-! Finite directed networks, conservation, and the incidence transpose identity. -/

namespace PotentialFlow

/-- Coefficients are carried with the directed network; positivity is stated where needed. -/
structure Network (n m : ℕ) where
  tail : Fin m → Fin n
  head : Fin m → Fin n
  positive : Fin m → ℝ
  negative : Fin m → ℝ

namespace Network

variable {n m : ℕ} (G : Network n m)

/-- Signed incidence, including cancellation for a self-loop. -/
def incidence (v : Fin n) (e : Fin m) : ℝ :=
  (if G.tail e = v then 1 else 0) - (if G.head e = v then 1 else 0)

/-- The divergence map uses outgoing flow minus incoming flow. -/
def divergenceLinear : (Fin m → ℝ) →ₗ[ℝ] (Fin n → ℝ) where
  toFun x v := ∑ e, G.incidence v e * x e
  map_add' x y := by
    ext v
    simp only [Pi.add_apply, mul_add, Finset.sum_add_distrib]
  map_smul' c x := by
    ext v
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    simp_rw [← mul_assoc, mul_comm _ c, mul_assoc]
    rw [← Finset.mul_sum]

/-- Net external nomination induced by an edge-flow vector. -/
def loads (x : Fin m → ℝ) : Fin n → ℝ := G.divergenceLinear x

/-- A flow is feasible exactly when it conserves the prescribed nominations. -/
def Feasible (b : Fin n → ℝ) (x : Fin m → ℝ) : Prop := G.loads x = b

/-- Potential difference in the orientation used for positive flow. -/
def drops (p : Fin n → ℝ) (e : Fin m) : ℝ := p (G.tail e) - p (G.head e)

theorem loads_apply (x : Fin m → ℝ) (v : Fin n) :
    G.loads x v = ∑ e, G.incidence v e * x e := rfl

theorem incidence_transpose (p : Fin n → ℝ) (e : Fin m) :
    ∑ v, p v * G.incidence v e = G.drops p e := by
  simp [incidence, drops, mul_sub, Finset.sum_sub_distrib, eq_comm]

/-- The finite incidence matrix and its transpose obey the exact pairing identity. -/
theorem conservation_pairing (x : Fin m → ℝ) (p : Fin n → ℝ) :
    ∑ v, p v * G.loads x v = ∑ e, G.drops p e * x e := by
  simp_rw [loads_apply, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro e _
  simp_rw [← mul_assoc]
  rw [← Finset.sum_mul, incidence_transpose]

theorem feasible_pairing {b : Fin n → ℝ} {x : Fin m → ℝ}
    (hx : G.Feasible b x) (p : Fin n → ℝ) :
    ∑ v, p v * b v = ∑ e, G.drops p e * x e := by
  rw [← hx]
  exact G.conservation_pairing x p

/-- Every induced nomination is balanced, even for disconnected networks and self-loops. -/
theorem sum_loads (x : Fin m → ℝ) : ∑ v, G.loads x v = 0 := by
  have h := G.conservation_pairing x (fun _ => 1)
  simpa [drops] using h

theorem isClosed_feasible (b : Fin n → ℝ) : IsClosed {x | G.Feasible b x} := by
  exact isClosed_eq G.divergenceLinear.continuous_of_finiteDimensional continuous_const

theorem convex_feasible (b : Fin n → ℝ) : Convex ℝ {x | G.Feasible b x} := by
  exact (convex_singleton b).linear_preimage G.divergenceLinear

/-- A vector orthogonal to every conserved circulation is a vector of potential differences. -/
theorem exists_potential_of_stationary (c : Fin m → ℝ)
    (h : ∀ d : Fin m → ℝ, G.loads d = 0 → ∑ e, c e * d e = 0) :
    ∃ p : Fin n → ℝ, G.drops p = c := by
  let L : Module.Dual ℝ (Fin m → ℝ) := dotProductEquiv ℝ (Fin m) c
  have hL : L ∈ G.divergenceLinear.ker.dualAnnihilator := by
    rw [Submodule.mem_dualAnnihilator]
    intro d hd
    exact h d hd
  rw [← LinearMap.range_dualMap_eq_dualAnnihilator_ker] at hL
  obtain ⟨f, hf⟩ := hL
  let p := (dotProductEquiv ℝ (Fin n)).symm f
  have hp : dotProductEquiv ℝ (Fin n) p = f :=
    (dotProductEquiv ℝ (Fin n)).apply_symm_apply f
  have hpair : G.divergenceLinear.dualMap (dotProductEquiv ℝ (Fin n) p) =
      dotProductEquiv ℝ (Fin m) (G.drops p) := by
    apply LinearMap.ext
    intro x
    exact G.conservation_pairing x p
  refine ⟨p, (dotProductEquiv ℝ (Fin m)).injective ?_⟩
  rw [← hpair, hp]
  exact hf

/-- Potential differences annihilate all zero-divergence circulations. -/
theorem potential_stationary (p : Fin n → ℝ) (d : Fin m → ℝ)
    (hd : G.loads d = 0) : ∑ e, G.drops p e * d e = 0 := by
  rw [← G.conservation_pairing d p, hd]
  simp

/-- The asymmetric cubic energy summed over all edges. -/
noncomputable def energy (x : Fin m → ℝ) : ℝ :=
  ∑ e, edgeEnergy (G.positive e) (G.negative e) (x e)

/-- A rational root enclosure can be used directly, without evaluating any square root. -/
noncomputable def dualLower (_G : Network n m) (b p : Fin n → ℝ) (u : Fin m → ℝ) : ℝ :=
  (∑ v, p v * b v) - (2 / 3 : ℝ) * ∑ e, u e

/-- Positive and negative coefficients of every edge are strictly positive. -/
def Positive : Prop := (∀ e, 0 < G.positive e) ∧ (∀ e, 0 < G.negative e)

/-- Conserved flows satisfy the dual lower bound for any potential vector and verified roots. -/
theorem dual_lower_bound {b p : Fin n → ℝ} {u x : Fin m → ℝ}
    (hc : G.Positive) (hx : G.Feasible b x)
    (hu : ∀ e, 0 ≤ u e)
    (hroot : ∀ e, |G.drops p e| ^ 3 ≤ u e ^ 2 *
      (if 0 ≤ G.drops p e then G.positive e else G.negative e)) :
    G.dualLower b p u ≤ G.energy x := by
  have h := Finset.sum_le_sum (s := Finset.univ) (fun e _ =>
    fenchel_root_bound (x := x e) (hc.1 e) (hc.2 e) (hu e) (hroot e))
  rw [Finset.sum_sub_distrib, ← Finset.mul_sum, ← G.feasible_pairing hx p] at h
  dsimp [dualLower, energy]
  linarith

/-- The certified primal-dual gap is nonnegative for every feasible candidate. -/
theorem gap_nonneg {b p : Fin n → ℝ} {u y : Fin m → ℝ}
    (hc : G.Positive) (hy : G.Feasible b y)
    (hu : ∀ e, 0 ≤ u e)
    (hroot : ∀ e, |G.drops p e| ^ 3 ≤ u e ^ 2 *
      (if 0 ≤ G.drops p e then G.positive e else G.negative e)) :
    0 ≤ G.energy y - G.dualLower b p u :=
  sub_nonneg.mpr (G.dual_lower_bound hc hy hu hroot)

/-- The same gap bounds the energy error relative to any other feasible flow. -/
theorem energy_error_le_gap {b p : Fin n → ℝ} {u y x : Fin m → ℝ}
    (hc : G.Positive) (hx : G.Feasible b x)
    (hu : ∀ e, 0 ≤ u e)
    (hroot : ∀ e, |G.drops p e| ^ 3 ≤ u e ^ 2 *
      (if 0 ≤ G.drops p e then G.positive e else G.negative e)) :
    G.energy y - G.energy x ≤ G.energy y - G.dualLower b p u :=
  sub_le_sub_left (G.dual_lower_bound hc hx hu hroot) _

end Network
end PotentialFlow
