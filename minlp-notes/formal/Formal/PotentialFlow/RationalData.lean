import Mathlib

/-! Exact rational conditions checked by an asymmetric-cubic flow certificate. -/
namespace PotentialFlow

structure RationalNetwork (n m : ℕ) where
  tail : Fin m → Fin n
  head : Fin m → Fin n
  positive : Fin m → ℚ
  negative : Fin m → ℚ

structure RationalCertificate (n m : ℕ) where
  flow : Fin m → ℚ
  potentials : Fin n → ℚ
  rootUpper : Fin m → ℚ
  gap : ℚ
  radius : ℚ

namespace RationalNetwork

def loads {n m : ℕ} (G : RationalNetwork n m) (x : Fin m → ℚ) (v : Fin n) : ℚ :=
  (∑ e, if G.tail e = v then x e else 0) - (∑ e, if G.head e = v then x e else 0)

def drops {n m : ℕ} (G : RationalNetwork n m) (p : Fin n → ℚ) (e : Fin m) : ℚ :=
  p (G.tail e) - p (G.head e)

def energy {n m : ℕ} (G : RationalNetwork n m) (x : Fin m → ℚ) : ℚ :=
  ∑ e, (if 0 ≤ x e then G.positive e else G.negative e) * |x e| ^ 3 / 3

def coefficientMinimum {n m : ℕ} (G : RationalNetwork n m) (hm : 0 < m) : ℚ :=
  Finset.univ.inf' (Finset.univ_nonempty_iff.mpr ⟨Sum.inl ⟨0, hm⟩⟩)
    (Sum.elim G.positive G.negative)

theorem coefficientMinimum_le_positive {n m : ℕ} (G : RationalNetwork n m)
    (hm : 0 < m) (e : Fin m) : G.coefficientMinimum hm ≤ G.positive e :=
  Finset.inf'_le _ (Finset.mem_univ (Sum.inl e))

theorem coefficientMinimum_le_negative {n m : ℕ} (G : RationalNetwork n m)
    (hm : 0 < m) (e : Fin m) : G.coefficientMinimum hm ≤ G.negative e :=
  Finset.inf'_le _ (Finset.mem_univ (Sum.inr e))

theorem coefficientMinimum_positive {n m : ℕ} (G : RationalNetwork n m)
    (hm : 0 < m) (hp : ∀ e, 0 < G.positive e) (hn : ∀ e, 0 < G.negative e) :
    0 < G.coefficientMinimum hm := by
  rw [coefficientMinimum, Finset.lt_inf'_iff]
  intro e _
  cases e with
  | inl e => exact hp e
  | inr e => exact hn e

/-- All numerical checks use rationals. Dimensions and edge indices are enforced
by the finite types; `hm` is the verifier's nonempty-edge requirement. -/
def Accepted {n m : ℕ} (G : RationalNetwork n m) (hm : 0 < m)
    (b : Fin n → ℚ) (C : RationalCertificate n m) : Prop :=
  (∀ e, 0 < G.positive e ∧ 0 < G.negative e) ∧
  G.loads C.flow = b ∧
  (∀ e, 0 ≤ C.rootUpper e ∧
    |G.drops C.potentials e| ^ 3 ≤ C.rootUpper e ^ 2 *
      (if 0 ≤ G.drops C.potentials e then G.positive e else G.negative e)) ∧
  C.gap = G.energy C.flow - ((∑ v, b v * C.potentials v) - (2 / 3) * ∑ e, C.rootUpper e) ∧
  0 ≤ C.gap ∧ 0 ≤ C.radius ∧ 6 * C.gap ≤ C.radius ^ 3 * G.coefficientMinimum hm

instance {n m : ℕ} (G : RationalNetwork n m) (hm : 0 < m) (b : Fin n → ℚ)
    (C : RationalCertificate n m) : Decidable (G.Accepted hm b C) := by
  unfold Accepted
  infer_instance

end RationalNetwork
end PotentialFlow
