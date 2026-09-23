import Formal.ReciprocalAnchor.ManyFastOperandSize
import Formal.ReciprocalAnchor.ManyEuclidCost

/-! A schoolbook bit-cost model, separate from Lean's compiled rational backend.

A digit scan charges one operation per visited digit. Addition scans the larger
operand plus a carry digit. Multiplication forms each shifted row and adds it to
an accumulator. Binary long division compares and conditionally subtracts on
each dividend digit. These are explicit loop charges; no runtime claim is made
about Lean's implementation of `Rat` or machine-word instructions.
-/
namespace ReciprocalAnchor.ManyLeaf.BitCost
open scoped BigOperators

/-- A carry-propagating addition or signed comparison scans the larger operand. -/
def addCost (B C : ℕ) : ℕ := max B C + 1

/-- Each multiplier digit creates and adds a row in a B+C+1 digit register. -/
def multiplicationCost (B C : ℕ) : ℕ :=
  Finset.sum (Finset.range B) (fun _i => 2 * (B + C + 1))

/-- Long division consumes B dividend digits. Each step compares and subtracts
C+1 digit registers and shifts a C+1 digit register. -/
def divisionCost (B C : ℕ) : ℕ :=
  Finset.sum (Finset.range B) (fun _i => 3 * (C + 1))

theorem multiplicationCost_eq (B C : ℕ) :
    multiplicationCost B C = 2 * B * (B + C + 1) := by
  simp only [multiplicationCost, Finset.sum_const, Finset.card_range, nsmul_eq_mul, Nat.cast_id]
  ring

theorem divisionCost_eq (B C : ℕ) : divisionCost B C = B * (3 * C + 3) := by
  simp only [divisionCost, Finset.sum_const, Finset.card_range, nsmul_eq_mul, Nat.cast_id]
  ring

/-- At most 2L gcd divisions and two final exact divisions normalize an L-bit fraction.
The Euclidean iteration bound is established independently in `ManyEuclidCost`. -/
def normalizationBudget (L : ℕ) : ℕ := (2 * L + 2) * divisionCost L L

/-- The exact Euclidean iteration count, followed by two exact quotient operations. -/
def normalizationCost (a b : ℕ) : ℕ :=
  ((countedEuclid a b).2 + 2) * divisionCost (max a.size b.size) (max a.size b.size)

theorem divisionCost_mono {B C D E : ℕ} (hB : B ≤ D) (hC : C ≤ E) :
    divisionCost B C ≤ divisionCost D E := by
  simp only [divisionCost_eq]
  exact Nat.mul_le_mul hB (by omega)

theorem normalizationCost_le {a b L : ℕ} (ha : a.size ≤ L) (hb : b.size ≤ L) :
    normalizationCost a b ≤ normalizationBudget L := by
  have hmax : max a.size b.size ≤ L := max_le ha hb
  unfold normalizationCost normalizationBudget
  apply Nat.mul_le_mul
  · have h := countedEuclid_cost_max a b
    omega
  · exact divisionCost_mono hmax hmax

/-- A common conservative charge covers sign handling, three cross-products,
addition/comparison, and normalization of a rational primitive. Intermediate raw
numerators and denominators have at most 2K+2 digits for K-bit operands. -/
def rationalStepCost (K : ℕ) : ℕ :=
  let L := 2 * K + 2
  3 * multiplicationCost L L + 3 * addCost L L + normalizationBudget L

theorem rationalStepCost_le (K : ℕ) : rationalStepCost K ≤ 256 * (K + 1) ^ 3 := by
  simp only [rationalStepCost, normalizationBudget, multiplicationCost_eq,
    divisionCost_eq, addCost, max_self]
  nlinarith [Nat.zero_le (K ^ 3), Nat.zero_le (K ^ 2)]

/-- Raw fractions for arithmetic primitives; signs are retained until normalization. -/
inductive RationalPrimitive
  | add | sub | mul | div | inv | compare | neg
  deriving DecidableEq

def rawNumerator : RationalPrimitive → ℚ → ℚ → ℤ
  | .add, q, r => q.num * r.den + r.num * q.den
  | .sub, q, r => q.num * r.den - r.num * q.den
  | .mul, q, r => q.num * r.num
  | .div, q, r => q.num * r.den
  | .inv, q, _ => q.den
  | .compare, q, r => q.num * r.den - r.num * q.den
  | .neg, q, _ => -q.num

def rawDenominator : RationalPrimitive → ℚ → ℚ → ℤ
  | .add, q, r => q.den * r.den
  | .sub, q, r => q.den * r.den
  | .mul, q, r => q.den * r.den
  | .div, q, r => q.den * r.num
  | .inv, q, _ => q.num
  | .compare, _, _ => 1
  | .neg, q, _ => q.den

/-- Actual unreduced components also have bounded size; the gcd cost is therefore
controlled before reduction, rather than only for the final canonical rational. -/
theorem raw_components_size {q r : ℚ} {K : ℕ}
    (hq : RationalBits q K) (hr : RationalBits r K) (op : RationalPrimitive) :
    (rawNumerator op q r).natAbs.size ≤ 2 * K + 2 ∧
      (rawDenominator op q r).natAbs.size ≤ 2 * K + 2 := by
  have hqN := hq.1
  have hqD := hq.2
  have hrN := hr.1
  have hrD := hr.2
  have hprod {x y : ℕ} (hx : x < 2 ^ K) (hy : y < 2 ^ K) :
      x * y < 2 ^ (2 * K) := by
    simpa only [two_mul, pow_add] using Nat.mul_lt_mul'' hx hy
  have hadd {x y : ℤ} (hx : x.natAbs < 2 ^ (2 * K))
      (hy : y.natAbs < 2 ^ (2 * K)) : (x + y).natAbs < 2 ^ (2 * K + 2) := by
    have h := Int.natAbs_add_le x y
    rw [pow_add]
    norm_num
    omega
  have hsub {x y : ℤ} (hx : x.natAbs < 2 ^ (2 * K))
      (hy : y.natAbs < 2 ^ (2 * K)) : (x - y).natAbs < 2 ^ (2 * K + 2) := by
    simpa only [sub_eq_add_neg, Int.natAbs_neg] using hadd hx
      (show (-y).natAbs < 2 ^ (2 * K) by simpa using hy)
  have hmul {x y : ℤ} (hx : x.natAbs < 2 ^ K) (hy : y.natAbs < 2 ^ K) :
      (x * y).natAbs < 2 ^ (2 * K) := by
    rw [Int.natAbs_mul]
    exact hprod hx hy
  have hcast (x : ℕ) : (x : ℤ).natAbs = x := Int.natAbs_natCast x
  have hsmall {x : ℕ} (hx : x < 2 ^ (2 * K)) : x < 2 ^ (2 * K + 2) :=
    hx.trans_le (Nat.pow_le_pow_right (by decide) (by omega))
  have hsingle {x : ℕ} (hx : x < 2 ^ K) : x < 2 ^ (2 * K + 2) :=
    hx.trans_le (Nat.pow_le_pow_right (by decide) (by omega))
  rw [Nat.size_le, Nat.size_le]
  cases op <;> simp only [rawNumerator, rawDenominator]
  · exact ⟨hadd (hmul hqN (by simpa using hrD)) (hmul hrN (by simpa using hqD)),
      hsmall (hmul (by simpa using hqD) (by simpa using hrD))⟩
  · exact ⟨hsub (hmul hqN (by simpa using hrD)) (hmul hrN (by simpa using hqD)),
      hsmall (hmul (by simpa using hqD) (by simpa using hrD))⟩
  · exact ⟨hsmall (hmul hqN hrN),
      hsmall (hmul (by simpa using hqD) (by simpa using hrD))⟩
  · exact ⟨hsmall (hmul hqN (by simpa using hrD)),
      hsmall (hmul (by simpa using hqD) hrN)⟩
  · simpa only [Int.natAbs_natCast] using And.intro (hsingle hqD) (hsingle hqN)
  · refine ⟨hsub (hmul hqN (by simpa using hrD)) (hmul hrN (by simpa using hqD)), ?_⟩
    simp only [Int.natAbs_one]
    exact (by norm_num : 1 < 2 ^ 2).trans_le
      (Nat.pow_le_pow_right (by decide) (by omega))
  · simpa only [Int.natAbs_neg, Int.natAbs_natCast] using
      And.intro (hsingle hqN) (hsingle hqD)

/-- The modeled charge uses the actual raw integer components and actual gcd iteration count. -/
def primitiveBitCost (op : RationalPrimitive) (q r : ℚ) (K : ℕ) : ℕ :=
  let L := 2 * K + 2
  3 * multiplicationCost L L + 3 * addCost L L +
    normalizationCost (rawNumerator op q r).natAbs (rawDenominator op q r).natAbs

theorem primitiveBitCost_le {q r : ℚ} {K : ℕ}
    (hq : RationalBits q K) (hr : RationalBits r K) (op : RationalPrimitive) :
    primitiveBitCost op q r K ≤ 256 * (K + 1) ^ 3 := by
  obtain ⟨hn, hd⟩ := raw_components_size hq hr op
  apply le_trans _ (rationalStepCost_le K)
  exact Nat.add_le_add_left (normalizationCost_le hn hd) _

/-- Uniform operand bounds turn a proved rational-operation count into a bit-work bound. -/
def bitWorkBudget (operations bits : ℕ) : ℕ := operations * rationalStepCost bits

theorem bitWorkBudget_le {operations bits count bound : ℕ}
    (hc : operations ≤ count) (hb : bits ≤ bound) :
    bitWorkBudget operations bits ≤ count * (256 * (bound + 1) ^ 3) := by
  unfold bitWorkBudget
  apply Nat.mul_le_mul hc
  exact (rationalStepCost_le bits).trans
    (Nat.mul_le_mul_left _ (Nat.pow_le_pow_left (Nat.succ_le_succ hb) 3))

/-- The exact evaluator's scalar size bound, polynomial in leaves and input bits. -/
abbrev evaluatorBits := FastEnvelope.evaluatorBits

/-- Source construction and segment arithmetic add at most twenty-four operations per
input line and twenty setup operations to the independently counted envelope.
This deliberately includes both the producer and its separate charge traversal. -/
def evaluatorOperations (n : ℕ) : ℕ :=
  (2 * n + 2) * ((2 * n + 2).log2 + 61) + 20

/-- Charge of the actual evaluator: returned construction charge, sixteen operations
per output segment including summation, six per source line, and eight setup
operations, including the final addition. -/
def actualEvaluatorCharge {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) : ℕ :=
  let produced := FastEnvelope.buildSegments (FastEnvelope.sourceLines m q w) a b
  produced.2 + 16 * produced.1.length + 6 * (FastEnvelope.sourceLines m q w).length + 8

theorem actualEvaluatorCharge_le {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) :
    actualEvaluatorCharge a b m q w ≤ evaluatorOperations n := by
  have hc := FastEnvelope.buildSegments_cost (FastEnvelope.sourceLines m q w) a b
  have hl := FastEnvelope.buildSegments_length (FastEnvelope.sourceLines m q w) a b
  have hs : (FastEnvelope.sourceLines m q w).length = 2 * n + 2 := by
    simp [FastEnvelope.sourceLines]
  rw [hs] at hc hl
  simp only [actualEvaluatorCharge, hs, evaluatorOperations]
  nlinarith

/-- The evaluated output and construction-dependent operation charge satisfy an
explicit schoolbook bit budget. Operand-family bounds are supplied by
`ManyFastOperandSize`; this does not claim refinement of Lean's compiled backend. -/
def actualEvaluatorBitWork {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) (B : ℕ) : ℕ :=
  bitWorkBudget (actualEvaluatorCharge a b m q w) (evaluatorBits n B)

theorem actualEvaluatorBitWork_le {n B : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) :
    actualEvaluatorBitWork a b m q w B ≤
      evaluatorOperations n * (256 * (evaluatorBits n B + 1) ^ 3) :=
  bitWorkBudget_le (actualEvaluatorCharge_le a b m q w) le_rfl

/-- A polynomial envelope of the explicit bit-work bound, eliminating the logarithm. -/
theorem actualEvaluatorBitWork_polynomial {n B : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) :
    actualEvaluatorBitWork a b m q w B ≤
      ((2 * n + 2) * (2 * n + 63) + 20) *
        (256 * (5 * B + 6 + (2 * n + 2) * (52 * B + 70)) ^ 3) := by
  have h := actualEvaluatorBitWork_le (B := B) a b m q w
  have he : evaluatorBits n B + 1 = 5 * B + 6 + (2 * n + 2) * (52 * B + 70) := by
    unfold evaluatorBits FastEnvelope.evaluatorBits
    omega
  rw [he] at h
  apply h.trans
  apply Nat.mul_le_mul_right
  unfold evaluatorOperations
  have hl := Nat.log2_le_self (2 * n + 2)
  nlinarith

end ReciprocalAnchor.ManyLeaf.BitCost


