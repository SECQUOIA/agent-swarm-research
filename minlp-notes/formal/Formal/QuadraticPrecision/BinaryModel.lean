import Formal.QuadraticPrecision.Model
import Formal.QuadraticPrecision.LinearSystem

/-! Binary linear lifts use an actual finite family of real affine rows.
The binary bounds make every integer-feasible code binary as well. -/
namespace QuadraticPrecision
noncomputable section

def BinaryCode {p : ℕ} (z : Fin p → ℝ) : Prop := ∀ i, z i = 0 ∨ z i = 1

structure BinaryLinearLift (n p q : ℕ) where
  system : LinearSystem (LiftPoint n p q)
  code_bounds : ∀ v ∈ system.feasible, ∀ i, 0 ≤ v.2.2.2 i ∧ v.2.2.2 i ≤ 1

namespace BinaryLinearLift
variable {n p q : ℕ}

def relaxation (L : BinaryLinearLift n p q) : Set (Input n × ℝ) :=
  {v | ∃ z : Fin p → ℝ, BinaryCode z ∧ ∃ a : Fin q → ℝ,
    (v.1, v.2, a, z) ∈ L.system.feasible}

def toIntegerLift (L : BinaryLinearLift n p q) : ConvexIntegerLift n p q :=
  ⟨L.system.feasible, L.system.convex⟩

theorem relaxation_eq_integer (L : BinaryLinearLift n p q) :
    L.relaxation = L.toIntegerLift.relaxation := by
  classical
  ext v
  constructor
  · rintro ⟨z, hz, a, ha⟩
    let k : Fin p → ℤ := fun i => if z i = 0 then 0 else 1
    have hk : (fun i => (k i : ℝ)) = z := by
      funext i
      rcases hz i with h | h <;> simp [k, h]
    refine ⟨k, a, ?_⟩
    simpa only [hk, toIntegerLift] using ha
  · rintro ⟨k, a, ha⟩
    refine ⟨fun i => (k i : ℝ), ?_, a, ha⟩
    intro i
    have hb := L.code_bounds _ ha i
    change 0 ≤ (k i : ℝ) ∧ (k i : ℝ) ≤ 1 at hb
    have h0 : 0 ≤ k i := by exact_mod_cast hb.1
    have h1 : k i ≤ 1 := by exact_mod_cast hb.2
    have h : k i = 0 ∨ k i = 1 := by omega
    rcases h with h | h <;> simp [h]

end BinaryLinearLift

variable {n : ℕ}
def HasBinaryGraphLift (D : Set (Input n)) (f : Input n → ℝ) (ε : ℝ) (p : ℕ) : Prop :=
  ∃ q, ∃ L : BinaryLinearLift n p q, IsGraphRelaxation D f ε L.relaxation

def HasBinaryEpigraphLift (D : Set (Input n)) (f : Input n → ℝ) (ε : ℝ) (p : ℕ) : Prop :=
  ∃ q, ∃ L : BinaryLinearLift n p q, IsEpigraphRelaxation D f ε L.relaxation

def HasBinaryHypographLift (D : Set (Input n)) (f : Input n → ℝ) (ε : ℝ) (p : ℕ) : Prop :=
  ∃ q, ∃ L : BinaryLinearLift n p q, IsHypographRelaxation D f ε L.relaxation

theorem HasBinaryGraphLift.toInteger {D : Set (Input n)} {f : Input n → ℝ} {ε : ℝ} {p : ℕ}
    (h : HasBinaryGraphLift D f ε p) : HasGraphLift D f ε p := by
  obtain ⟨q, L, h⟩ := h
  exact ⟨q, L.toIntegerLift, L.relaxation_eq_integer ▸ h⟩

theorem HasBinaryEpigraphLift.toInteger {D : Set (Input n)} {f : Input n → ℝ} {ε : ℝ} {p : ℕ}
    (h : HasBinaryEpigraphLift D f ε p) : HasEpigraphLift D f ε p := by
  obtain ⟨q, L, h⟩ := h
  exact ⟨q, L.toIntegerLift, L.relaxation_eq_integer ▸ h⟩

theorem HasBinaryHypographLift.toInteger {D : Set (Input n)} {f : Input n → ℝ} {ε : ℝ} {p : ℕ}
    (h : HasBinaryHypographLift D f ε p) : HasHypographLift D f ε p := by
  obtain ⟨q, L, h⟩ := h
  exact ⟨q, L.toIntegerLift, L.relaxation_eq_integer ▸ h⟩

end
end QuadraticPrecision
