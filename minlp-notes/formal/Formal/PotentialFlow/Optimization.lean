import Formal.PotentialFlow.Network
import Formal.PotentialFlow.Modulus

namespace PotentialFlow

noncomputable section

/-- A continuous objective attains its minimum on a closed affine fiber whenever its
sublevel through one feasible point fits in a bounded coordinate box. -/
theorem exists_minimum_of_bounded_sublevel {m n : ℕ}
    (A : (Fin m → ℝ) →ₗ[ℝ] (Fin n → ℝ)) (b : Fin n → ℝ)
    (f : (Fin m → ℝ) → ℝ) (hf : Continuous f)
    (q₀ lo hi : Fin m → ℝ) (hq₀ : A q₀ = b)
    (hbound : ∀ q, f q ≤ f q₀ → q ∈ Set.Icc lo hi) :
    ∃ q, A q = b ∧ ∀ y, A y = b → f q ≤ f y := by
  let K := {q | A q = b} ∩ {q | f q ≤ f q₀}
  have hclosed : IsClosed K :=
    (isClosed_eq A.continuous_of_finiteDimensional continuous_const).inter
      (isClosed_le hf continuous_const)
  have hcompact : IsCompact K :=
    isCompact_Icc.of_isClosed_subset hclosed (fun q hq => hbound q hq.2)
  obtain ⟨q, hq, hmin⟩ := hcompact.exists_isMinOn
    ⟨q₀, hq₀, (show f q₀ ≤ f q₀ from le_rfl)⟩ hf.continuousOn
  refine ⟨q, hq.1, fun y hy => ?_⟩
  by_cases h : f y ≤ f q₀
  · exact hmin ⟨hy, h⟩
  · exact hq.2.trans (le_of_not_ge h)

/-- First-order stationarity along every direction preserving the linear equations. -/
theorem constrained_stationary {m n : ℕ}
    (A : (Fin m → ℝ) →ₗ[ℝ] (Fin n → ℝ)) (b : Fin n → ℝ)
    (f : (Fin m → ℝ) → ℝ) (q y : Fin m → ℝ) (d : ℝ)
    (hq : A q = b) (hy : A y = b)
    (hmin : ∀ z, A z = b → f q ≤ f z)
    (hd : HasDerivAt (fun t : ℝ => f (q + t • (y - q))) d 0) : d = 0 := by
  have hlocal : IsLocalMin (fun t : ℝ => f (q + t • (y - q))) 0 := by
    apply IsMinOn.isLocalMin (s := Set.univ)
    · intro t _
      simpa using hmin (q + t • (y - q)) (by simp [map_add, map_smul, map_sub, hq, hy])
    · exact Filter.univ_mem
  exact hlocal.hasDerivAt_eq_zero hd

/-- Cubic growth gives an elementary coordinate bound without extracting roots. -/
theorem abs_le_of_cubic_bound {a M x : ℝ} (ha : 0 < a) (hM : 0 ≤ M)
    (h : a / 3 * |x| ^ 3 ≤ M) : |x| ≤ 3 * M / a + 1 := by
  have hc : |x| ^ 3 ≤ 3 * M / a := by
    apply (le_div_iff₀ ha).mpr
    nlinarith
  by_cases hx : |x| ≤ 1
  · have : 0 ≤ 3 * M / a := by positivity
    linarith
  · have hx1 : 1 ≤ |x| := le_of_not_ge hx
    have hp : 0 ≤ (|x| - 1) * (|x| ^ 2 + |x|) := by positivity
    nlinarith

namespace Network

variable {n m : ℕ} (G : Network n m)

theorem energy_nonneg (hc : G.Positive) (x : Fin m → ℝ) : 0 ≤ G.energy x :=
  Finset.sum_nonneg fun e _ => edgeEnergy_nonneg (hc.1 e).le (hc.2 e).le

theorem energy_cubic_bound (hc : G.Positive) (x : Fin m → ℝ) (e : Fin m) :
    min (G.positive e) (G.negative e) / 3 * |x e| ^ 3 ≤ G.energy x := by
  have he : min (G.positive e) (G.negative e) / 3 * |x e| ^ 3 ≤
      edgeEnergy (G.positive e) (G.negative e) (x e) := by
    unfold edgeEnergy
    split
    · nlinarith [mul_le_mul_of_nonneg_right (min_le_left (G.positive e) (G.negative e))
        (pow_nonneg (abs_nonneg (x e)) 3)]
    · nlinarith [mul_le_mul_of_nonneg_right (min_le_right (G.positive e) (G.negative e))
        (pow_nonneg (abs_nonneg (x e)) 3)]
  exact he.trans (Finset.single_le_sum
    (fun j _ => edgeEnergy_nonneg (hc.1 j).le (hc.2 j).le) (Finset.mem_univ e))

/-- A feasible positive-coefficient network always has an energy-minimizing flow. -/
theorem exists_energy_minimizer (b : Fin n → ℝ) (hc : G.Positive)
    (y : Fin m → ℝ) (hy : G.Feasible b y) :
    ∃ x, G.Feasible b x ∧ ∀ z, G.Feasible b z → G.energy x ≤ G.energy z := by
  have hcont : Continuous G.energy := by
    apply continuous_finsetSum
    intro e _
    exact (continuous_iff_continuousAt.mpr
      (fun x => (hasDerivAt_edgeEnergy (G.positive e) (G.negative e) x).continuousAt)).comp
      (continuous_apply e)
  let R : Fin m → ℝ := fun e => 3 * G.energy y / min (G.positive e) (G.negative e) + 1
  apply exists_minimum_of_bounded_sublevel G.divergenceLinear b G.energy hcont y (-R) R hy
  intro x hx
  have hb (e : Fin m) : |x e| ≤ R e :=
    abs_le_of_cubic_bound (lt_min (hc.1 e) (hc.2 e)) (G.energy_nonneg hc y)
      ((G.energy_cubic_bound hc x e).trans hx)
  exact ⟨fun e => (abs_le.mp (hb e)).1, fun e => (abs_le.mp (hb e)).2⟩

/-- Energy minimizers are stationary along every feasible flow difference. -/
theorem energy_minimizer_stationary {b : Fin n → ℝ} {x y : Fin m → ℝ}
    (hx : G.Feasible b x) (hy : G.Feasible b y)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z) :
    ∑ e, edgeLaw (G.positive e) (G.negative e) (x e) * (y e - x e) = 0 := by
  apply constrained_stationary G.divergenceLinear b G.energy x y _ hx hy hmin
  change HasDerivAt (fun t : ℝ => ∑ e, edgeEnergy (G.positive e) (G.negative e)
    (x e + t * (y e - x e))) _ 0
  apply HasDerivAt.fun_sum
  intro e _
  have hi : HasDerivAt (fun t : ℝ => x e + t * (y e - x e)) (y e - x e) 0 := by
    simpa using (((hasDerivAt_id (0 : ℝ)).mul_const (y e - x e)).const_add (x e))
  have ho : HasDerivAt (edgeEnergy (G.positive e) (G.negative e))
      (edgeLaw (G.positive e) (G.negative e) (x e)) (x e + 0 * (y e - x e)) := by
    simpa using hasDerivAt_edgeEnergy (G.positive e) (G.negative e) (x e)
  exact ho.comp 0 hi

/-- The energy gap controls the sum of cubed edge errors. -/
theorem energy_minimizer_sum_gap {b : Fin n → ℝ} {x y : Fin m → ℝ} {a : ℝ}
    (ha : 0 < a) (hcp : ∀ e, a ≤ G.positive e) (hcm : ∀ e, a ≤ G.negative e)
    (hx : G.Feasible b x) (hy : G.Feasible b y)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z) :
    ∑ e, a / 6 * |y e - x e| ^ 3 ≤ G.energy y - G.energy x := by
  have h := Finset.sum_le_sum (fun e (_ : e ∈ Finset.univ) =>
    edge_bregman_modulus (G.positive e) (G.negative e) a (x e) (y e)
      ha (hcp e) (hcm e))
  simpa only [Finset.sum_sub_distrib, G.energy_minimizer_stationary hx hy hmin,
    sub_zero, energy] using h

/-- Every individual edge obeys the certified cubic error estimate. -/
theorem energy_minimizer_gap {b : Fin n → ℝ} {x y : Fin m → ℝ} {a : ℝ}
    (ha : 0 < a) (hcp : ∀ e, a ≤ G.positive e) (hcm : ∀ e, a ≤ G.negative e)
    (hx : G.Feasible b x) (hy : G.Feasible b y)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z) (e : Fin m) :
    a / 6 * |y e - x e| ^ 3 ≤ G.energy y - G.energy x :=
  (Finset.single_le_sum (fun j _ => by positivity) (Finset.mem_univ e)).trans
    (G.energy_minimizer_sum_gap ha hcp hcm hx hy hmin)

/-- A sharper estimate can use the selected edge's own smaller coefficient. -/
theorem energy_minimizer_edge_gap {b : Fin n → ℝ} {x y : Fin m → ℝ}
    (hc : G.Positive) (hx : G.Feasible b x) (hy : G.Feasible b y)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z) (e : Fin m) :
    min (G.positive e) (G.negative e) / 6 * |y e - x e| ^ 3 ≤
      G.energy y - G.energy x := by
  let D := fun j => edgeEnergy (G.positive j) (G.negative j) (y j) -
    edgeEnergy (G.positive j) (G.negative j) (x j) -
    edgeLaw (G.positive j) (G.negative j) (x j) * (y j - x j)
  have hb (j : Fin m) : min (G.positive j) (G.negative j) / 6 * |y j - x j| ^ 3 ≤ D j :=
    edge_bregman_modulus _ _ _ _ _ (lt_min (hc.1 j) (hc.2 j)) (min_le_left _ _)
      (min_le_right _ _)
  have hn (j : Fin m) : 0 ≤ D j := by
    have hm : 0 < min (G.positive j) (G.negative j) := lt_min (hc.1 j) (hc.2 j)
    exact (by positivity : 0 ≤ min (G.positive j) (G.negative j) / 6 *
      |y j - x j| ^ 3).trans (hb j)
  have h := (hb e).trans (Finset.single_le_sum (fun j _ => hn j) (Finset.mem_univ e))
  simpa only [D, Finset.sum_sub_distrib, G.energy_minimizer_stationary hx hy hmin,
    sub_zero, energy] using h

/-- The minimizing flow is unique, including on disconnected graphs and with self-loops. -/
theorem energy_minimizer_unique {b : Fin n → ℝ} {x y : Fin m → ℝ}
    (hc : G.Positive) (hx : G.Feasible b x) (hy : G.Feasible b y)
    (hminx : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z)
    (hminy : ∀ z, G.Feasible b z → G.energy y ≤ G.energy z) : x = y := by
  funext e
  have h := G.energy_minimizer_edge_gap hc hx hy hminx e
  have he : G.energy y ≤ G.energy x := hminy x hx
  have hp : 0 < min (G.positive e) (G.negative e) / 6 := by
    exact div_pos (lt_min (hc.1 e) (hc.2 e)) (by norm_num)
  have hzero : |y e - x e| ^ 3 = 0 := by
    have hle : |y e - x e| ^ 3 ≤ 0 := by nlinarith
    exact le_antisymm hle (by positivity)
  have : y e - x e = 0 := abs_eq_zero.mp ((pow_eq_zero_iff (by decide : 3 ≠ 0)).mp hzero)
  linarith

/-- Existence and uniqueness hold without assuming a pre-existing physical solution. -/
theorem exists_unique_energy_minimizer (b : Fin n → ℝ) (hc : G.Positive)
    (y : Fin m → ℝ) (hy : G.Feasible b y) :
    ∃! x, G.Feasible b x ∧ ∀ z, G.Feasible b z → G.energy x ≤ G.energy z := by
  obtain ⟨x, hx, hmin⟩ := G.exists_energy_minimizer b hc y hy
  exact ⟨x, ⟨hx, hmin⟩, fun z hz => G.energy_minimizer_unique hc hz.1 hx hz.2 hmin⟩

/-- Minimization produces node potentials satisfying every nonlinear edge law. -/
theorem energy_minimizer_potential {b : Fin n → ℝ} {x : Fin m → ℝ}
    (hx : G.Feasible b x)
    (hmin : ∀ z, G.Feasible b z → G.energy x ≤ G.energy z) :
    ∃ p, G.drops p = fun e => edgeLaw (G.positive e) (G.negative e) (x e) := by
  apply G.exists_potential_of_stationary
  intro d hd
  have hxd : G.Feasible b (x + d) := by
    change G.divergenceLinear (x + d) = b
    rw [map_add, show G.divergenceLinear x = b from hx,
      show G.divergenceLinear d = 0 from hd, add_zero]
  simpa only [Pi.add_apply, add_sub_cancel_left] using
    G.energy_minimizer_stationary hx hxd hmin

/-- Conversely, conserved flows satisfying the edge laws minimize the energy. -/
theorem physical_flow_minimizer {b p : Fin n → ℝ} {x : Fin m → ℝ}
    (hc : G.Positive) (hx : G.Feasible b x)
    (hlaw : G.drops p = fun e => edgeLaw (G.positive e) (G.negative e) (x e)) :
    ∀ y, G.Feasible b y → G.energy x ≤ G.energy y := by
  intro y hy
  have hs : ∑ e, edgeLaw (G.positive e) (G.negative e) (x e) * (y e - x e) = 0 := by
    have hd : G.loads (y - x) = 0 := by
      change G.divergenceLinear (y - x) = 0
      rw [map_sub, show G.divergenceLinear y = b from hy,
        show G.divergenceLinear x = b from hx, sub_self]
    simpa only [hlaw, Pi.sub_apply] using G.potential_stationary p (y - x) hd
  have he (e : Fin m) : 0 ≤ edgeEnergy (G.positive e) (G.negative e) (y e) -
      edgeEnergy (G.positive e) (G.negative e) (x e) -
      edgeLaw (G.positive e) (G.negative e) (x e) * (y e - x e) := by
    have ha : 0 < min (G.positive e) (G.negative e) := lt_min (hc.1 e) (hc.2 e)
    exact (by positivity : 0 ≤ min (G.positive e) (G.negative e) / 6 *
      |y e - x e| ^ 3).trans (edge_bregman_modulus _ _ _ _ _ ha
        (min_le_left _ _) (min_le_right _ _))
  have h := Finset.sum_nonneg (fun e (_ : e ∈ Finset.univ) => he e)
  simpa only [Finset.sum_sub_distrib, hs, sub_zero, energy, sub_nonneg] using h

/-- Energy minimization and the physical potential equations describe the same flows. -/
theorem energy_minimizer_iff_potential {b : Fin n → ℝ} {x : Fin m → ℝ}
    (hc : G.Positive) (hx : G.Feasible b x) :
    (∀ z, G.Feasible b z → G.energy x ≤ G.energy z) ↔
      ∃ p, G.drops p = fun e => edgeLaw (G.positive e) (G.negative e) (x e) := by
  constructor
  · exact G.energy_minimizer_potential hx
  · rintro ⟨p, hp⟩
    exact G.physical_flow_minimizer hc hx hp

/-- Every feasible positive-coefficient network has exactly one physical edge-flow vector.
Potentials need not be unique because componentwise additive constants do not affect drops. -/
theorem exists_unique_physical_flow (b : Fin n → ℝ) (hc : G.Positive)
    (y : Fin m → ℝ) (hy : G.Feasible b y) :
    ∃! x, G.Feasible b x ∧
      ∃ p, G.drops p = fun e => edgeLaw (G.positive e) (G.negative e) (x e) := by
  obtain ⟨x, ⟨hx, hmin⟩, huniq⟩ := G.exists_unique_energy_minimizer b hc y hy
  refine ⟨x, ⟨hx, G.energy_minimizer_potential hx hmin⟩, ?_⟩
  rintro z ⟨hz, p, hp⟩
  exact huniq z ⟨hz, G.physical_flow_minimizer hc hz hp⟩

end Network

end
end PotentialFlow
