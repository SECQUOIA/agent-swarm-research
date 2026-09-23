import Formal.PotentialFlow.RationalData
import Formal.PotentialFlow.Network

/-! Exact transport of rational certificate checks to the real network model. -/
namespace PotentialFlow
namespace RationalNetwork

variable {n m : ℕ} (G : RationalNetwork n m)

/-- Interpret the rational coefficients as real numbers without changing the graph. -/
def toReal : Network n m where
  tail := G.tail
  head := G.head
  positive e := G.positive e
  negative e := G.negative e

@[simp] theorem toReal_loads (x : Fin m → ℚ) (v : Fin n) :
    G.toReal.loads (fun e => (x e : ℝ)) v = (G.loads x v : ℝ) := by
  simp only [Network.loads_apply, Network.incidence, toReal, loads]
  push_cast
  simp_rw [sub_mul, ite_mul, one_mul, zero_mul]
  rw [Finset.sum_sub_distrib]
  simp [apply_ite]

@[simp] theorem toReal_drops (p : Fin n → ℚ) (e : Fin m) :
    G.toReal.drops (fun v => (p v : ℝ)) e = (G.drops p e : ℝ) := by
  simp [Network.drops, toReal, drops]

@[simp] theorem toReal_energy (x : Fin m → ℚ) :
    G.toReal.energy (fun e => (x e : ℝ)) = (G.energy x : ℝ) := by
  simp [Network.energy, edgeEnergy, toReal, energy, apply_ite]

@[simp] theorem toReal_dualLower (b p : Fin n → ℚ) (u : Fin m → ℚ) :
    G.toReal.dualLower (fun v => (b v : ℝ)) (fun v => (p v : ℝ))
      (fun e => (u e : ℝ)) =
      (((∑ v, b v * p v) - (2 / 3 : ℚ) * ∑ e, u e : ℚ) : ℝ) := by
  simp [Network.dualLower, mul_comm]

theorem accepted_positive {hm : 0 < m} {b : Fin n → ℚ}
    {C : RationalCertificate n m} (h : G.Accepted hm b C) : G.toReal.Positive := by
  constructor
  · intro e
    change 0 < (G.positive e : ℝ)
    exact_mod_cast (h.1 e).1
  · intro e
    change 0 < (G.negative e : ℝ)
    exact_mod_cast (h.1 e).2

theorem accepted_feasible {hm : 0 < m} {b : Fin n → ℚ}
    {C : RationalCertificate n m} (h : G.Accepted hm b C) :
    G.toReal.Feasible (fun v => (b v : ℝ)) (fun e => (C.flow e : ℝ)) := by
  ext v
  rw [G.toReal_loads, h.2.1]

theorem accepted_roots {hm : 0 < m} {b : Fin n → ℚ}
    {C : RationalCertificate n m} (h : G.Accepted hm b C) (e : Fin m) :
    0 ≤ (C.rootUpper e : ℝ) ∧
    |G.toReal.drops (fun v => (C.potentials v : ℝ)) e| ^ 3 ≤
      (C.rootUpper e : ℝ) ^ 2 *
        (if 0 ≤ G.toReal.drops (fun v => (C.potentials v : ℝ)) e
         then G.toReal.positive e else G.toReal.negative e) := by
  rw [G.toReal_drops]
  constructor
  · exact_mod_cast (h.2.2.1 e).1
  · simpa only [toReal, apply_ite, Rat.cast_nonneg, Rat.cast_mul,
      Rat.cast_pow, Rat.cast_abs] using
      (show ((|G.drops C.potentials e| ^ 3 : ℚ) : ℝ) ≤
        ((C.rootUpper e ^ 2 *
          (if 0 ≤ G.drops C.potentials e then G.positive e else G.negative e) : ℚ) : ℝ)
        from by exact_mod_cast (h.2.2.1 e).2)

theorem accepted_gap {hm : 0 < m} {b : Fin n → ℚ}
    {C : RationalCertificate n m} (h : G.Accepted hm b C) :
    (C.gap : ℝ) = G.toReal.energy (fun e => (C.flow e : ℝ)) -
      G.toReal.dualLower (fun v => (b v : ℝ)) (fun v => (C.potentials v : ℝ))
        (fun e => (C.rootUpper e : ℝ)) := by
  rw [G.toReal_energy, G.toReal_dualLower]
  exact_mod_cast h.2.2.2.1

theorem accepted_gap_nonneg {hm : 0 < m} {b : Fin n → ℚ}
    {C : RationalCertificate n m} (h : G.Accepted hm b C) : 0 ≤ (C.gap : ℝ) := by
  exact_mod_cast h.2.2.2.2.1

theorem accepted_radius {hm : 0 < m} {b : Fin n → ℚ}
    {C : RationalCertificate n m} (h : G.Accepted hm b C) :
    0 ≤ (C.radius : ℝ) ∧
    6 * (C.gap : ℝ) ≤ (C.radius : ℝ) ^ 3 * (G.coefficientMinimum hm : ℝ) := by
  constructor
  · exact_mod_cast h.2.2.2.2.2.1
  · exact_mod_cast h.2.2.2.2.2.2

theorem accepted_coefficientMinimum {hm : 0 < m} {b : Fin n → ℚ}
    {C : RationalCertificate n m} (h : G.Accepted hm b C) :
    0 < (G.coefficientMinimum hm : ℝ) ∧
    (∀ e, (G.coefficientMinimum hm : ℝ) ≤ G.toReal.positive e) ∧
    (∀ e, (G.coefficientMinimum hm : ℝ) ≤ G.toReal.negative e) := by
  refine ⟨?_, ?_, ?_⟩
  · exact_mod_cast G.coefficientMinimum_positive hm (fun e => (h.1 e).1)
      (fun e => (h.1 e).2)
  · intro e
    change (G.coefficientMinimum hm : ℝ) ≤ (G.positive e : ℝ)
    exact_mod_cast G.coefficientMinimum_le_positive hm e
  · intro e
    change (G.coefficientMinimum hm : ℝ) ≤ (G.negative e : ℝ)
    exact_mod_cast G.coefficientMinimum_le_negative hm e

end RationalNetwork
end PotentialFlow
