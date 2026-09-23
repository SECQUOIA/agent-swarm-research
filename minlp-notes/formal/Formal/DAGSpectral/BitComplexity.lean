import Formal.ReciprocalAnchor.ManyBitCost

/-! Explicit rational arithmetic traces in the repository's schoolbook bit-cost
model. These are mathematical loop charges, not timings of Lean's Rat backend. -/
namespace DAGSpectral
open ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost

abbrev ArithmeticEvent := RationalPrimitive × ℚ × ℚ

/-- Evaluate the same schoolbook charge without constructing a unary list of
every digit position in the (possibly very loose) width budget. -/
def primitiveBitCostClosed (op : RationalPrimitive) (q r : ℚ) (K : ℕ) : ℕ :=
  let L := 2*K+2
  let a := (rawNumerator op q r).natAbs
  let b := (rawDenominator op q r).natAbs
  let digits := max a.size b.size
  3*(2*L*(L+L+1)) + 3*(L+1) +
    ((countedEuclid a b).2+2)*(digits*(3*digits+3))

/-- This compiler rewrite is justified by equality in Lean. It changes only
how the cost observer is evaluated, including for positive-rank trials. -/
@[csimp] theorem primitiveBitCost_closed : primitiveBitCost = primitiveBitCostClosed := by
  funext op q r K
  simp only [primitiveBitCost,primitiveBitCostClosed,multiplicationCost_eq,
    normalizationCost,divisionCost_eq,addCost,max_self]

def eventBits (K : ℕ) (e : ArithmeticEvent) : Prop :=
  RationalBits e.2.1 K ∧ RationalBits e.2.2 K

def traceBitWork (K : ℕ) (es : List ArithmeticEvent) : ℕ :=
  (es.map fun e => primitiveBitCost e.1 e.2.1 e.2.2 K).sum

theorem traceBitWork_le {K : ℕ} {es : List ArithmeticEvent}
    (he : ∀ e ∈ es, eventBits K e) :
    traceBitWork K es ≤ es.length * (256 * (K+1)^3) := by
  induction es with
  | nil => simp [traceBitWork]
  | cons e es ih =>
    have h := primitiveBitCost_le (he e (by simp)).1 (he e (by simp)).2 e.1
    have ht := ih (fun z hz => he z (by simp [hz]))
    simp only [traceBitWork,List.map_cons,List.sum_cons,List.length_cons] at *
    nlinarith

theorem rationalBits_two : RationalBits 2 2 := by unfold RationalBits; decide

theorem rationalBits_two_pow (n : ℕ) : RationalBits ((2:ℚ)^n) (2*n+1) := by
  induction n with
  | zero => simpa using rationalBits_one
  | succ n ih =>
    rw [pow_succ]
    convert rationalBits_mul ih rationalBits_two using 1
    omega

/-- One arbitrary rational primitive increases a uniform operand budget at most
by the recurrence K ↦ 2K+2. -/
def primitiveResult : RationalPrimitive → ℚ → ℚ → ℚ
  | .add, q, r => q+r
  | .sub, q, r => q-r
  | .mul, q, r => q*r
  | .div, q, r => q/r
  | .inv, q, _ => q⁻¹
  | .compare, q, r => if q ≤ r then 1 else 0
  | .neg, q, _ => -q

theorem primitiveResult_bits {K : ℕ} {q r : ℚ}
    (hq : RationalBits q K) (hr : RationalBits r K) (op : RationalPrimitive) :
    RationalBits (primitiveResult op q r) (2*K+2) := by
  have hK := rationalBits_pos hq
  cases op with
  | add => exact rationalBits_mono (rationalBits_add hq hr) (by omega)
  | sub => exact rationalBits_mono (rationalBits_sub hq hr) (by omega)
  | mul => exact rationalBits_mono (rationalBits_mul hq hr) (by omega)
  | div => exact rationalBits_mono (rationalBits_div hq hr) (by omega)
  | inv => exact rationalBits_mono (rationalBits_inv hq) (by omega)
  | neg => exact rationalBits_mono (rationalBits_neg hq) (by omega)
  | compare =>
    simp only [primitiveResult]
    split_ifs
    · exact rationalBits_mono rationalBits_one (by omega)
    · exact rationalBits_mono rationalBits_zero (by omega)

/-- At fixed arithmetic depth the uniform size budget stays linear in input
bits. This bound is for dimension-dependent preprocessing, not long path sums. -/
def arithmeticWidth (depth bits : ℕ) : ℕ := 2^depth*(bits+2)-2

theorem arithmeticWidth_zero (B : ℕ) : arithmeticWidth 0 B = B := by
  simp [arithmeticWidth]

theorem arithmeticWidth_step (d B : ℕ) :
    arithmeticWidth (d+1) B = 2*arithmeticWidth d B+2 := by
  have hp : 1 ≤ 2^d := Nat.one_le_pow d 2 (by decide)
  unfold arithmeticWidth
  rw [pow_succ]
  have ht : 2 ≤ 2^d*(B+2) := by nlinarith
  have he : 2^d*2*(B+2) = 2*(2^d*(B+2)) := by ring
  rw [he]
  omega

end DAGSpectral
