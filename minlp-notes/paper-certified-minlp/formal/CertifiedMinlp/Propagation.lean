import CertifiedMinlp.Coordinates

/-! Finite rational propagation, with explicit endpoint and update operations. -/
namespace CertifiedMinlp
namespace Propagation

/-- Missing endpoints are `none`; zero times an unbounded variable is zero. -/
def termLower (c : ℚ) (B : Coordinate) : Option ℚ :=
  if c = 0 then some 0 else if 0 < c then
    match B with
    | .bounded l _ | .lowerBounded l => some (c * l)
    | _ => none
  else
    match B with
    | .bounded _ u | .upperBounded u => some (c * u)
    | _ => none

def termUpper (c : ℚ) (B : Coordinate) : Option ℚ := termLower (-c) B |>.map Neg.neg

theorem termLower_sound (c r : ℚ) (B : Coordinate) (x : ℝ)
    (hx : B.contains x) (hr : termLower c B = some r) : (r : ℝ) ≤ c * x := by
  unfold termLower at hr
  split_ifs at hr with hc hp
  · simp only [Option.some.injEq] at hr
    simp [← hr, hc]
  · have hc' : (0 : ℝ) ≤ c := by exact_mod_cast le_of_lt hp
    cases B <;> simp_all only [Coordinate.contains, Option.some.injEq, reduceCtorEq]
    all_goals rw [← hr, Rat.cast_mul]; exact mul_le_mul_of_nonneg_left (by tauto) hc'
  · have hc' : (c : ℝ) ≤ 0 := by exact_mod_cast le_of_not_gt hp
    cases B <;> simp_all only [Coordinate.contains, Option.some.injEq, reduceCtorEq]
    all_goals rw [← hr, Rat.cast_mul]; exact mul_le_mul_of_nonpos_left (by tauto) hc'

theorem termUpper_sound (c r : ℚ) (B : Coordinate) (x : ℝ)
    (hx : B.contains x) (hr : termUpper c B = some r) : (c : ℝ) * x ≤ r := by
  unfold termUpper at hr
  cases he : termLower (-c) B with
  | none => simp [he] at hr
  | some q =>
    have h := termLower_sound (-c) q B x hx he
    simp only [Rat.cast_neg, neg_mul] at h
    simp only [he, Option.map_some, Option.some.injEq] at hr
    rw [← hr, Rat.cast_neg]
    linarith

def tightenLower (B : Coordinate) (l : ℚ) : Coordinate :=
  match B with
  | .bounded a b => .bounded (max a l) b
  | .lowerBounded a => .lowerBounded (max a l)
  | .upperBounded b => .bounded l b
  | .free => .lowerBounded l

def tightenUpper (B : Coordinate) (u : ℚ) : Coordinate :=
  match B with
  | .bounded a b => .bounded a (min b u)
  | .lowerBounded a => .bounded a u
  | .upperBounded b => .upperBounded (min b u)
  | .free => .upperBounded u

theorem contains_tightenLower (B : Coordinate) (l : ℚ) (x : ℝ) :
    (tightenLower B l).contains x ↔ B.contains x ∧ (l : ℝ) ≤ x := by
  cases B <;> simp [tightenLower, Coordinate.contains, and_assoc, and_comm]

theorem contains_tightenUpper (B : Coordinate) (u : ℚ) (x : ℝ) :
    (tightenUpper B u).contains x ↔ B.contains x ∧ x ≤ (u : ℝ) := by
  cases B <;> simp [tightenUpper, Coordinate.contains, and_assoc]

variable {n : ℕ}
abbrev Box (n : ℕ) := Fin n → Coordinate

def Contains (B : Box n) (x : Fin n → ℝ) : Prop := ∀ i, (B i).contains (x i)

structure Row (n : ℕ) where
  coeff : Fin n → ℚ
  rhs : ℚ
  upper : Bool

def Row.Holds (r : Row n) (x : Fin n → ℝ) : Prop :=
  if r.upper then ∑ i, (r.coeff i : ℝ) * x i ≤ r.rhs
  else (r.rhs : ℝ) ≤ ∑ i, (r.coeff i : ℝ) * x i

structure Instruction (n : ℕ) where
  coord : Fin n
  bound : ℚ
  upper : Bool

def Instruction.apply (s : Instruction n) (B : Box n) : Box n :=
  Function.update B s.coord
    (if s.upper then tightenUpper (B s.coord) s.bound
     else tightenLower (B s.coord) s.bound)

def Instruction.Holds (s : Instruction n) (x : Fin n → ℝ) : Prop :=
  if s.upper then x s.coord ≤ (s.bound : ℝ) else (s.bound : ℝ) ≤ x s.coord

theorem apply_preserves (s : Instruction n) (B : Box n) (x : Fin n → ℝ)
    (hx : Contains B x) (hs : s.Holds x) : Contains (s.apply B) x := by
  intro i
  by_cases hi : i = s.coord
  · subst i
    simp only [Instruction.apply, Function.update_self]
    cases hu : s.upper
    · simp only [Instruction.Holds, hu, Bool.false_eq_true, ↓reduceIte] at hs ⊢
      exact (contains_tightenLower _ _ _).mpr ⟨hx _, hs⟩
    · simp only [Instruction.Holds, hu, ↓reduceIte] at hs ⊢
      exact (contains_tightenUpper _ _ _).mpr ⟨hx _, hs⟩
  · simpa [Instruction.apply, Function.update_of_ne hi] using hx i

/-- Endpoint witnesses certify every term other than the selected coordinate. -/
def ResidualLower (B : Box n) (r : Row n) (k : Fin n) (v : Fin n → ℚ) : Prop :=
  ∀ j, j ≠ k → termLower (r.coeff j) (B j) = some (v j)

def ResidualUpper (B : Box n) (r : Row n) (k : Fin n) (v : Fin n → ℚ) : Prop :=
  ∀ j, j ≠ k → termUpper (r.coeff j) (B j) = some (v j)

def residual (k : Fin n) (v : Fin n → ℚ) : ℚ := ∑ j ∈ Finset.univ.erase k, v j

theorem residualLower_sound (B : Box n) (r : Row n) (k : Fin n) (v : Fin n → ℚ)
    (x : Fin n → ℝ) (hx : Contains B x) (hv : ResidualLower B r k v) :
    (residual k v : ℝ) ≤ ∑ j ∈ Finset.univ.erase k, (r.coeff j : ℝ) * x j := by
  simp only [residual, Rat.cast_sum]
  apply Finset.sum_le_sum
  intro j hj
  exact termLower_sound _ _ _ _ (hx j) (hv j (Finset.mem_erase.mp hj).1)

theorem residualUpper_sound (B : Box n) (r : Row n) (k : Fin n) (v : Fin n → ℚ)
    (x : Fin n → ℝ) (hx : Contains B x) (hv : ResidualUpper B r k v) :
    ∑ j ∈ Finset.univ.erase k, (r.coeff j : ℝ) * x j ≤ (residual k v : ℝ) := by
  simp only [residual, Rat.cast_sum]
  apply Finset.sum_le_sum
  intro j hj
  exact termUpper_sound _ _ _ _ (hx j) (hv j (Finset.mem_erase.mp hj).1)

/-- Division reverses direction exactly for a negative selected coefficient. -/
def rowInstruction (r : Row n) (k : Fin n) (v : Fin n → ℚ) : Instruction n :=
  ⟨k, (r.rhs - residual k v) / r.coeff k, r.upper == decide (0 < r.coeff k)⟩

theorem rowInstruction_sound (B : Box n) (r : Row n) (k : Fin n) (v : Fin n → ℚ)
    (x : Fin n → ℝ) (hx : Contains B x) (hr : r.Holds x) (hc : r.coeff k ≠ 0)
    (hv : if r.upper then ResidualLower B r k v else ResidualUpper B r k v) :
    (rowInstruction r k v).Holds x := by
  have hsum := Finset.sum_erase_add (Finset.univ : Finset (Fin n))
    (fun j => (r.coeff j : ℝ) * x j) (Finset.mem_univ k)
  have hc' : (r.coeff k : ℝ) ≠ 0 := by exact_mod_cast hc
  cases hu : r.upper <;>
    simp only [Row.Holds, hu, Bool.false_eq_true, ↓reduceIte] at hr hv
  · have hrest := residualUpper_sound B r k v x hx hv
    have hprod : (r.rhs : ℝ) - residual k v ≤ (r.coeff k : ℝ) * x k := by linarith
    by_cases hp : 0 < r.coeff k
    · have hp' : (0 : ℝ) < r.coeff k := by exact_mod_cast hp
      simpa [Instruction.Holds, rowInstruction, hu, hp] using
        (div_le_iff₀ hp').mpr (by simpa [mul_comm] using hprod)
    · have hn' : (r.coeff k : ℝ) < 0 := lt_of_le_of_ne
        (by exact_mod_cast le_of_not_gt hp) hc'
      simpa [Instruction.Holds, rowInstruction, hu, hp] using
        (le_div_iff_of_neg hn').mpr (by simpa [mul_comm] using hprod)
  · have hrest := residualLower_sound B r k v x hx hv
    have hprod : (r.coeff k : ℝ) * x k ≤ (r.rhs : ℝ) - residual k v := by linarith
    by_cases hp : 0 < r.coeff k
    · have hp' : (0 : ℝ) < r.coeff k := by exact_mod_cast hp
      simpa [Instruction.Holds, rowInstruction, hu, hp] using
        (le_div_iff₀ hp').mpr (by simpa [mul_comm] using hprod)
    · have hn' : (r.coeff k : ℝ) < 0 := lt_of_le_of_ne
        (by exact_mod_cast le_of_not_gt hp) hc'
      simpa [Instruction.Holds, rowInstruction, hu, hp] using
        (div_le_iff_of_neg hn').mpr (by simpa [mul_comm] using hprod)

/-- Rounding changes only the rational bound and leaves its direction fixed. -/
def roundInstruction (s : Instruction n) : Instruction n :=
  { s with bound := if s.upper then (⌊s.bound⌋ : ℤ) else (⌈s.bound⌉ : ℤ) }

theorem roundInstruction_sound (s : Instruction n) (x : Fin n → ℝ)
    (hs : s.Holds x) (hz : ∃ z : ℤ, x s.coord = z) :
    (roundInstruction s).Holds x := by
  obtain ⟨z, hz⟩ := hz
  cases hu : s.upper
  · have hb : s.bound ≤ (z : ℚ) := by
      have : (s.bound : ℝ) ≤ z := by simpa [Instruction.Holds, hu, hz] using hs
      exact_mod_cast this
    have hceil : ⌈s.bound⌉ ≤ z := Int.ceil_le.mpr hb
    have : (⌈s.bound⌉ : ℝ) ≤ z := by exact_mod_cast hceil
    simpa [Instruction.Holds, roundInstruction, hu, hz] using this
  · have hb : (z : ℚ) ≤ s.bound := by
      have : (z : ℝ) ≤ s.bound := by simpa [Instruction.Holds, hu, hz] using hs
      exact_mod_cast this
    have hfloor : z ≤ ⌊s.bound⌋ := Int.le_floor.mpr hb
    have : (z : ℝ) ≤ ⌊s.bound⌋ := by exact_mod_cast hfloor
    simpa [Instruction.Holds, roundInstruction, hu, hz] using this

/-- Declared data give a concrete mixed-integer feasible set. Equalities can be
represented by their two weak inequalities. -/
structure Problem (n : ℕ) where
  declared : Box n
  rows : List (Row n)
  integers : Finset (Fin n)
  binaries : Finset (Fin n)
  fixed : Fin n → Option ℚ

def Problem.Feasible (p : Problem n) (x : Fin n → ℝ) : Prop :=
  Contains p.declared x ∧ (∀ r ∈ p.rows, r.Holds x) ∧
  (∀ i ∈ p.integers, ∃ z : ℤ, x i = z) ∧
  (∀ i ∈ p.binaries, x i = 0 ∨ x i = 1) ∧
  (∀ i q, p.fixed i = some q → x i = q)

/-- The admitted steps carry rational endpoint checks, never a premise that the
new box already contains the feasible set. Rounding may be applied repeatedly. -/
inductive Admitted (p : Problem n) (B : Box n) : Instruction n → Prop where
  | row (r : Row n) (k : Fin n) (v : Fin n → ℚ)
      (hr : r ∈ p.rows) (hc : r.coeff k ≠ 0)
      (hv : if r.upper then ResidualLower B r k v else ResidualUpper B r k v) :
      Admitted p B (rowInstruction r k v)
  | currentLower (k : Fin n) (q : ℚ) (hq : termLower 1 (B k) = some q) :
      Admitted p B ⟨k, q, false⟩
  | currentUpper (k : Fin n) (q : ℚ) (hq : termUpper 1 (B k) = some q) :
      Admitted p B ⟨k, q, true⟩
  | round (s : Instruction n) (hs : Admitted p B s) (hi : s.coord ∈ p.integers) :
      Admitted p B (roundInstruction s)
  | binaryLower (k : Fin n) (hk : k ∈ p.binaries) : Admitted p B ⟨k, 0, false⟩
  | binaryUpper (k : Fin n) (hk : k ∈ p.binaries) : Admitted p B ⟨k, 1, true⟩
  | fixedLower (k : Fin n) (q : ℚ) (hq : p.fixed k = some q) :
      Admitted p B ⟨k, q, false⟩
  | fixedUpper (k : Fin n) (q : ℚ) (hq : p.fixed k = some q) :
      Admitted p B ⟨k, q, true⟩

theorem admitted_sound (p : Problem n) (B : Box n) (s : Instruction n)
    (hs : Admitted p B s) (x : Fin n → ℝ) (hx : p.Feasible x) (hB : Contains B x) :
    s.Holds x := by
  induction hs with
  | row r k v hr hc hv => exact rowInstruction_sound B r k v x hB (hx.2.1 r hr) hc hv
  | currentLower k q hq =>
    simpa [Instruction.Holds] using termLower_sound 1 q (B k) (x k) (hB k) hq
  | currentUpper k q hq =>
    simpa [Instruction.Holds] using termUpper_sound 1 q (B k) (x k) (hB k) hq
  | round s _ hi ih => exact roundInstruction_sound s x ih (hx.2.2.1 s.coord hi)
  | binaryLower k hk =>
    rcases hx.2.2.2.1 k hk with h | h <;> simp [Instruction.Holds, h]
  | binaryUpper k hk =>
    rcases hx.2.2.2.1 k hk with h | h <;> simp [Instruction.Holds, h]
  | fixedLower k q hq => simp [Instruction.Holds, hx.2.2.2.2 k q hq]
  | fixedUpper k q hq => simp [Instruction.Holds, hx.2.2.2.2 k q hq]

/-- A finite propagation transcript is checked against each intermediate box. -/
inductive Transcript (p : Problem n) : Box n → Box n → Prop where
  | nil (B : Box n) : Transcript p B B
  | cons (B C : Box n) (s : Instruction n) (hs : Admitted p B s)
      (rest : Transcript p (s.apply B) C) : Transcript p B C

theorem transcript_preserves (p : Problem n) (B C : Box n)
    (h : Transcript p B C) (x : Fin n → ℝ) (hx : p.Feasible x)
    (hB : Contains B x) : Contains C x := by
  induction h with
  | nil => exact hB
  | cons B _ s hs _ ih =>
    exact ih (apply_preserves s B x hB (admitted_sound p B s hs x hx hB))

/-- No sweep limit is required: every finite accepted propagation sequence is sound. -/
theorem propagation_preserves_feasible (p : Problem n) (B : Box n)
    (h : Transcript p p.declared B) : ∀ x, p.Feasible x → Contains B x :=
  fun x hx => transcript_preserves p p.declared B h x hx hx.1

theorem empty_interval_infeasible (p : Problem n) (B : Box n)
    (h : Transcript p p.declared B) (k : Fin n) (l u : ℚ)
    (hk : B k = .bounded l u) (hempty : u < l) : ¬ ∃ x, p.Feasible x := by
  rintro ⟨x, hx⟩
  have hc := propagation_preserves_feasible p B h x hx k
  rw [hk] at hc
  have hreal : (u : ℝ) < l := by exact_mod_cast hempty
  exact (not_le_of_gt hreal) (hc.1.trans hc.2)

/-- Exact fixed coordinates substitute without changing any affine row value. -/
theorem fixed_substitution (c : Fin n → ℚ) (x : Fin n → ℝ) (k : Fin n) (q : ℚ)
    (hx : x k = q) :
    ∑ j, (c j : ℝ) * x j =
      ∑ j ∈ Finset.univ.erase k, (c j : ℝ) * x j + (c k : ℝ) * q := by
  rw [← hx]
  exact (Finset.sum_erase_add _ _ (Finset.mem_univ k)).symm

theorem constant_row_iff (r : Row n) (hc : ∀ i, r.coeff i = 0) (x : Fin n → ℝ) :
    r.Holds x ↔ if r.upper then 0 ≤ r.rhs else r.rhs ≤ 0 := by
  simp only [Row.Holds, hc, Rat.cast_zero, zero_mul, Finset.sum_const_zero]
  split <;> norm_cast

end Propagation
end CertifiedMinlp
