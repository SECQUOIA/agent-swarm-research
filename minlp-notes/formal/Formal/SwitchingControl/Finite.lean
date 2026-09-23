import Mathlib

namespace SwitchingControl.Finite

abbrev Mode := Fin 3
abbrev Triple := Mode → ℕ
abbrev History := List Triple
abbrev Word := List Mode

def zero : Triple := ![0, 0, 0]
def unit (i : Mode) : Triple := fun j => if j = i then 1 else 0
def add (x y : Triple) : Triple := fun i => x i + y i

def transitions (two : Bool) : List (Bool × Triple) :=
  if two then
    [(false, ![0, 1, 1]), (false, ![1, 0, 1]), (false, ![1, 1, 0]),
     (true, unit 0), (true, unit 1), (true, unit 2)]
  else [(false, unit 0), (false, unit 1), (false, unit 2), (true, zero)]

def extend (h : History) (d : Triple) : History := h ++ [add (h.getLastD zero) d]

def historiesFrom : ℕ → Bool → History → List History
  | 0, _, h => [h]
  | n + 1, s, h => (transitions s).flatMap fun t => historiesFrom n t.1 (extend h t.2)

def histories (cells : ℕ) : List History := historiesFrom (cells - 1) false [zero]

def countPrefix (w : Word) (j : ℕ) (i : Mode) : ℕ := (w.take j).count i

def switches : Word → ℕ
  | [] => 0
  | [_] => 0
  | a :: b :: rest => (if a = b then 0 else 1) + switches (b :: rest)

def Fits (h : History) (w : Word) : Prop :=
  h.length = w.length ∧ ∀ j : Fin h.length, ∀ i : Mode,
    h[j] i ≤ countPrefix w (j.val + 1) i ∧ countPrefix w (j.val + 1) i ≤ h[j] i + 1

instance (h : History) (w : Word) : Decidable (Fits h w) := by unfold Fits; infer_instance

def Solvable (budget : ℕ) (h : History) : Prop := ∃ w : Word, Fits h w ∧ switches w ≤ budget

def canonical : History :=
  [![0, 0, 0], ![1, 0, 0], ![1, 1, 0], ![1, 1, 1], ![2, 1, 1], ![2, 1, 1], ![2, 1, 2]]

def relabel (p : Triple) (h : History) : History :=
  h.map fun row i => row ⟨p i % 3, Nat.mod_lt _ (by decide)⟩

def exceptional : List History :=
  [relabel ![0, 1, 2] canonical, relabel ![0, 2, 1] canonical,
   relabel ![1, 0, 2] canonical, relabel ![1, 2, 0] canonical,
   relabel ![2, 0, 1] canonical, relabel ![2, 1, 0] canonical]

/-- Every chamber generated from this partial history admits property `P`. -/
def Covered (P : History → Prop) (n : ℕ) (s : Bool) (h : History) : Prop :=
  ∀ h' ∈ historiesFrom n s h, P h'

theorem covered_leaf {P : History → Prop} {s : Bool} {h : History} (hp : P h) :
    Covered P 0 s h := by
  simpa only [Covered, historiesFrom, List.mem_singleton, forall_eq] using hp

theorem covered_step {P : History → Prop} {n : ℕ} {s : Bool} {h : History}
    (hp : ∀ t ∈ transitions s, Covered P n t.1 (extend h t.2)) :
    Covered P (n + 1) s h := by
  intro h' hh
  obtain ⟨t, ht, hh⟩ := List.mem_flatMap.mp hh
  exact hp t ht h' hh

theorem covered_one {P : History → Prop} {n : ℕ} {h : History}
    (h0 : Covered P n false (extend h (unit 0)))
    (h1 : Covered P n false (extend h (unit 1)))
    (h2 : Covered P n false (extend h (unit 2)))
    (h3 : Covered P n true (extend h zero)) : Covered P (n+1) false h := by
  apply covered_step
  intro t ht
  simp only [transitions, Bool.false_eq_true, ↓reduceIte, List.mem_cons,
    List.not_mem_nil, or_false] at ht
  rcases ht with rfl | rfl | rfl | rfl <;> assumption

theorem covered_two {P : History → Prop} {n : ℕ} {h : History}
    (h0 : Covered P n false (extend h ![0, 1, 1]))
    (h1 : Covered P n false (extend h ![1, 0, 1]))
    (h2 : Covered P n false (extend h ![1, 1, 0]))
    (h3 : Covered P n true (extend h (unit 0)))
    (h4 : Covered P n true (extend h (unit 1)))
    (h5 : Covered P n true (extend h (unit 2))) : Covered P (n+1) true h := by
  apply covered_step
  intro t ht
  simp only [transitions, ↓reduceIte, List.mem_cons, List.not_mem_nil, or_false] at ht
  rcases ht with rfl | rfl | rfl | rfl | rfl | rfl <;> assumption

end SwitchingControl.Finite
