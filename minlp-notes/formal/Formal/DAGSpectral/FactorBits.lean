import Formal.DAGSpectral.RationalFactorization
import Formal.DAGSpectral.BitComplexity

/-! Operand bounds and explicit arithmetic counts for the rational LDL producer.
The dependence on dimension is unrestricted; at fixed dimension every bit bound
is linear in the input bit budget. -/
namespace DAGSpectral
open Matrix ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost

def factorBits (n B : ℕ) : ℕ := 4^n*(B+1)

theorem factorBits_pos (n B : ℕ) : 1 ≤ factorBits n B := by
  unfold factorBits
  exact Nat.mul_pos (by positivity) (by omega)

theorem factorBits_input (n B : ℕ) : B ≤ factorBits n B := by
  have h : 1 ≤ 4^n := Nat.one_le_pow n 4 (by decide)
  unfold factorBits
  nlinarith

theorem factorBits_step (n B : ℕ) : factorBits n (4*B+1) ≤ factorBits (n + 1) B := by
  unfold factorBits
  rw [pow_succ]
  calc
    _ ≤ 4^n*(4*(B+1)) := Nat.mul_le_mul_left _ (by omega)
    _ = _ := by ring

theorem factorBits_mono_dim (n B : ℕ) : factorBits n B ≤ factorBits (n + 1) B := by
  unfold factorBits
  rw [pow_succ]
  nlinarith only [Nat.zero_le (4^n*(B+1))]

theorem rationalSchur_bits {n B : ℕ} {A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ}
    (hA : ∀ i j, RationalBits (A i j) B) (i j : Fin n) :
    RationalBits (rationalSchur A i j) (4*B+1) := by
  have h := rationalBits_sub (hA i.succ j.succ)
    (rationalBits_div (rationalBits_mul (hA i.succ 0) (hA 0 j.succ)) (hA 0 0))
  have he : B+(B+B+B)+1 = 4*B+1 := by omega
  rw [← he]
  exact h

/-- The entries of every factor produced by the actual recursive LDL routine. -/
theorem rationalLDL_bits (n B : ℕ) (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ i j, RationalBits (A i j) B) :
    ∀ f ∈ rationalLDL n A, RationalBits f.1 (factorBits n B) ∧
      ∀ i, RationalBits (f.2 i) (factorBits n B) := by
  induction n generalizing B with
  | zero => simp [rationalLDL]
  | succ n ih =>
    intro f hf
    by_cases hz : A 0 0 = 0
    · rw [rationalLDL,if_pos hz] at hf
      obtain ⟨g,hg,rfl⟩ := List.mem_map.mp hf
      have hg' := ih B (A.submatrix Fin.succ Fin.succ) (fun i j => hA i.succ j.succ) g hg
      refine ⟨rationalBits_mono hg'.1 (factorBits_mono_dim n B), ?_⟩
      intro i
      refine Fin.cases ?_ (fun j => ?_) i
      · exact rationalBits_mono rationalBits_zero (factorBits_pos _ _)
      · exact rationalBits_mono (hg'.2 j) (factorBits_mono_dim n B)
    · rw [rationalLDL,if_neg hz,List.mem_cons] at hf
      rcases hf with rfl | hf
      · refine ⟨rationalBits_mono (hA 0 0) (factorBits_input _ _), fun i => ?_⟩
        apply rationalBits_mono (rationalBits_div (hA i 0) (hA 0 0))
        have hp : 1 ≤ 4^n := Nat.one_le_pow n 4 (by decide)
        unfold factorBits
        rw [pow_succ]
        nlinarith
      · obtain ⟨g,hg,rfl⟩ := List.mem_map.mp hf
        have hg' := ih (4*B+1) (rationalSchur A) (rationalSchur_bits hA) g hg
        refine ⟨rationalBits_mono hg'.1 (factorBits_step n B), ?_⟩
        intro i
        refine Fin.cases ?_ (fun j => ?_) i
        · exact rationalBits_mono rationalBits_zero (factorBits_pos _ _)
        · exact rationalBits_mono (hg'.2 j) (factorBits_step n B)

/-- Three primitive operations compute one Schur entry, in evaluation order. -/
def schurEntryTrace {n : ℕ} (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ)
    (i j : Fin n) : List ArithmeticEvent :=
  [(.mul,A i.succ 0,A 0 j.succ),
   (.div,A i.succ 0*A 0 j.succ,A 0 0),
   (.sub,A i.succ j.succ,A i.succ 0*A 0 j.succ/A 0 0)]

def schurTrace {n : ℕ} (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) :
    List ArithmeticEvent :=
  (List.ofFn fun i : Fin n => (List.ofFn fun j : Fin n => schurEntryTrace A i j).flatten).flatten

/-- The divisions producing the leading factor's actual coordinates. -/
def factorDivisionTrace {n : ℕ} (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) :
    List ArithmeticEvent := List.ofFn fun i => (.div,A i 0,A 0 0)

/-- The same branch and recursive matrices as `rationalLDL`. A pivot equality
is charged as a rational comparison. Copies and zero extension use no arithmetic. -/
def rationalLDLTrace : (n : ℕ) → Matrix (Fin n) (Fin n) ℚ → List ArithmeticEvent
  | 0, _ => []
  | n+1, A => (.compare,A 0 0,0) ::
      if A 0 0 = 0 then rationalLDLTrace n (A.submatrix Fin.succ Fin.succ)
      else factorDivisionTrace A ++ schurTrace A ++ rationalLDLTrace n (rationalSchur A)

/-- An instrumented version returns the same factors and records their arithmetic. -/
def rationalLDLWithTrace : (n : ℕ) → Matrix (Fin n) (Fin n) ℚ →
    List (RationalFactor n) × List ArithmeticEvent
  | 0, _ => ([],[])
  | n+1, A =>
      if A 0 0 = 0 then
        let next := rationalLDLWithTrace n (A.submatrix Fin.succ Fin.succ)
        (next.1.map extendFactor, (.compare,A 0 0,0)::next.2)
      else
        let next := rationalLDLWithTrace n (rationalSchur A)
        ((A 0 0,fun i => A i 0/A 0 0)::next.1.map extendFactor,
          (.compare,A 0 0,0)::(factorDivisionTrace A ++ schurTrace A ++ next.2))

theorem rationalLDLWithTrace_eq (n : ℕ) (A : Matrix (Fin n) (Fin n) ℚ) :
    rationalLDLWithTrace n A = (rationalLDL n A,rationalLDLTrace n A) := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [rationalLDLWithTrace,rationalLDL,rationalLDLTrace]; split <;> simp [ih]

theorem schurTrace_length {n : ℕ} (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) :
    (schurTrace A).length = 3*n*n := by
  simp [schurTrace,schurEntryTrace,List.length_flatten,List.map_ofFn,
    List.sum_ofFn]
  ring

theorem factorDivisionTrace_length {n : ℕ} (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) :
    (factorDivisionTrace A).length = n+1 := by simp [factorDivisionTrace]

/-- A dimension-only bound on the number of rational arithmetic primitives. -/
def factorOperations (n : ℕ) : ℕ := n*(3*n*n+n+1)

theorem rationalLDLTrace_length_le (n : ℕ) (A : Matrix (Fin n) (Fin n) ℚ) :
    (rationalLDLTrace n A).length ≤ factorOperations n := by
  induction n with
  | zero => simp [rationalLDLTrace,factorOperations]
  | succ n ih =>
    simp only [rationalLDLTrace,List.length_cons]
    split
    · have hh := ih (A.submatrix Fin.succ Fin.succ)
      unfold factorOperations at *
      nlinarith
    · simp only [List.length_append,schurTrace_length,factorDivisionTrace_length]
      have hh := ih (rationalSchur A)
      unfold factorOperations at *
      nlinarith

private theorem eventBits_mono {B C : ℕ} {e : ArithmeticEvent}
    (h : eventBits B e) (hBC : B ≤ C) : eventBits C e :=
  ⟨rationalBits_mono h.1 hBC,rationalBits_mono h.2 hBC⟩

theorem schurEntryTrace_bits {n B : ℕ} {A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ}
    (hA : ∀ i j, RationalBits (A i j) B) (i j : Fin n) :
    ∀ e ∈ schurEntryTrace A i j, eventBits (4*B+1) e := by
  intro e he
  simp only [schurEntryTrace,List.mem_cons,List.not_mem_nil,or_false] at he
  rcases he with rfl | rfl | rfl
  · exact ⟨rationalBits_mono (hA _ _) (by omega),rationalBits_mono (hA _ _) (by omega)⟩
  · exact ⟨rationalBits_mono (rationalBits_mul (hA _ _) (hA _ _)) (by omega),
      rationalBits_mono (hA _ _) (by omega)⟩
  · exact ⟨rationalBits_mono (hA _ _) (by omega),
      rationalBits_mono (rationalBits_div (rationalBits_mul (hA _ _) (hA _ _))
        (hA _ _)) (by omega)⟩

theorem schurTrace_bits {n B : ℕ} {A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ}
    (hA : ∀ i j, RationalBits (A i j) B) :
    ∀ e ∈ schurTrace A, eventBits (4*B+1) e := by
  intro e he
  obtain ⟨xs,hxs,he⟩ := List.mem_flatten.mp he
  obtain ⟨i,rfl⟩ := List.mem_ofFn.mp hxs
  obtain ⟨ys,hys,he⟩ := List.mem_flatten.mp he
  obtain ⟨j,rfl⟩ := List.mem_ofFn.mp hys
  exact schurEntryTrace_bits hA i j e he

/-- Every operand of the instrumented producer, including Schur intermediate
products and quotients, has the stated reduced numerator/denominator bound. -/
theorem rationalLDLTrace_bits (n B : ℕ) (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ i j, RationalBits (A i j) B) :
    ∀ e ∈ rationalLDLTrace n A, eventBits (factorBits n B) e := by
  induction n generalizing B with
  | zero => simp [rationalLDLTrace]
  | succ n ih =>
    intro e he
    rw [rationalLDLTrace,List.mem_cons] at he
    rcases he with rfl | he
    · exact ⟨rationalBits_mono (hA _ _) (factorBits_input _ _),
        rationalBits_mono rationalBits_zero (factorBits_pos _ _)⟩
    · split_ifs at he with hz
      · exact eventBits_mono (ih B _ (fun i j => hA i.succ j.succ) e he)
          (factorBits_mono_dim n B)
      · simp only [List.mem_append] at he
        rcases he with (he | he) | he
        · obtain ⟨i,rfl⟩ := List.mem_ofFn.mp he
          exact ⟨rationalBits_mono (hA _ _) (factorBits_input _ _),
            rationalBits_mono (hA _ _) (factorBits_input _ _)⟩
        · exact eventBits_mono (schurTrace_bits hA e he)
            ((factorBits_input n (4*B+1)).trans (factorBits_step n B))
        · exact eventBits_mono (ih (4*B+1) _ (rationalSchur_bits hA) e he)
            (factorBits_step n B)

theorem rationalLDL_bitWork_le (n B : ℕ) (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ i j, RationalBits (A i j) B) :
    traceBitWork (factorBits n B) (rationalLDLTrace n A) ≤
      factorOperations n * (256*(factorBits n B+1)^3) :=
  (traceBitWork_le (rationalLDLTrace_bits n B A hA)).trans
    (Nat.mul_le_mul_right _ (rationalLDLTrace_length_le n A))

end DAGSpectral
