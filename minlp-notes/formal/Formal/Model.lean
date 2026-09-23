import Mathlib

/-! The representation model for the exact convex box-count theorem. -/
namespace ExactCounts

noncomputable section

variable {n p q : ℕ}

abbrev Point := Fin 3 → ℝ
abbrev Visible (n : ℕ) := Fin n → Point
abbrev Code (p : ℕ) := Fin p → ℝ
abbrev Ambient (n p q : ℕ) := Visible n × Code p × (Fin q → ℝ)

def leftValue (x : ℝ) : ℝ := (7 / 4 : ℝ) * (1 - x) ^ 32
def rightValue (x : ℝ) : ℝ := (7 / 4 : ℝ) * x ^ 32
def graphPoint (x : ℝ) : Point := ![x, leftValue x, rightValue x]
def graph (x : Fin n → ℝ) : Visible n := fun i => graphPoint (x i)
def InDomain (x : Fin n → ℝ) : Prop := ∀ i, 0 ≤ x i ∧ x i ≤ 1

def ValidPoint (v : Point) : Prop :=
  0 ≤ v 0 ∧ v 0 ≤ 1 ∧
  |v 1 - leftValue (v 0)| ≤ 1 ∧ |v 2 - rightValue (v 0)| ≤ 1

def Valid (v : Visible n) : Prop := ∀ i, ValidPoint (v i)
def IntegerCodes (p : ℕ) : Set (Code p) :=
  {z | ∃ k : Fin p → ℤ, z = fun i => (k i : ℝ)}
def BinaryCodes (p : ℕ) : Set (Code p) := {z | ∀ i, z i = 0 ∨ z i = 1}

def Admissible (C : Set (Ambient n p q)) (codes : Set (Code p)) : Prop :=
  (∀ x, InDomain x → ∃ z ∈ codes, ∃ a, (graph x, z, a) ∈ C) ∧
  (∀ v z a, z ∈ codes → (v, z, a) ∈ C → Valid v)

def HasIntegerLift (n p : ℕ) : Prop :=
  ∃ q, ∃ C : Set (Ambient n p q), Convex ℝ C ∧ Admissible C (IntegerCodes p)

def HasBinaryLift (n p : ℕ) : Prop :=
  ∃ q, ∃ C : Set (Ambient n p q), Convex ℝ C ∧ Admissible C (BinaryCodes p)

end
end ExactCounts
