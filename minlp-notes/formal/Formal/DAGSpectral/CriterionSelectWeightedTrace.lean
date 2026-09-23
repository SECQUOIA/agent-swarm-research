import Formal.DAGSpectral.CriterionSelectWeighted
import Formal.DAGSpectral.RationalContrastTrace

/-! Actual traces for weighted contrast costs. The fold's bit budget grows
linearly with the number of contrasts, rather than exponentially with its depth. -/
namespace DAGSpectral
open Matrix ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost

/-- Every finite option payload satisfies the stated bit bound. -/
def WeightedOptionBits (B : ℕ) (v : Option ℚ) : Prop :=
  ∀ q, v = some q → RationalBits q B

theorem weightedOptionBits_mono {B C : ℕ} {v : Option ℚ}
    (h : WeightedOptionBits B v) (hBC : B ≤ C) : WeightedOptionBits C v :=
  fun q hq => rationalBits_mono (h q hq) hBC

def clipZeroWithTrace (q : ℚ) : ℚ × List ArithmeticEvent :=
  (if q ≤ 0 then 0 else q, [(.compare, q, 0)])

@[simp] theorem clipZeroWithTrace_value (q : ℚ) : (clipZeroWithTrace q).1 = max q 0 := by
  simp only [clipZeroWithTrace, max_def]

theorem rationalBits_max_zero {q : ℚ} {B : ℕ} (hq : RationalBits q B) :
    RationalBits (max q 0) B := by
  rw [max_def]
  split_ifs
  · exact rationalBits_mono rationalBits_zero (rationalBits_pos hq)
  · exact hq

def rationalWeightedTermWithTrace (w : ℚ) (v : Option ℚ) :
    Option ℚ × List ArithmeticEvent :=
  let check : List ArithmeticEvent := [(.compare, w, 0), (.compare, 0, w)]
  if w = 0 then (some 0, check)
  else match v with
    | none => (none, check)
    | some q =>
      let clipped := clipZeroWithTrace q
      (some (w * clipped.1), check ++ clipped.2 ++ [(.mul, w, clipped.1)])

@[simp] theorem rationalWeightedTermWithTrace_value (w : ℚ) (v : Option ℚ) :
    (rationalWeightedTermWithTrace w v).1 = rationalWeightedTerm w v := by
  unfold rationalWeightedTermWithTrace rationalWeightedTerm
  split_ifs <;> cases v <;> simp

theorem rationalWeightedTermWithTrace_length (w : ℚ) (v : Option ℚ) :
    (rationalWeightedTermWithTrace w v).2.length ≤ 4 := by
  unfold rationalWeightedTermWithTrace
  split_ifs <;> cases v <;> simp [clipZeroWithTrace]

theorem rationalWeightedTermWithTrace_bits {K : ℕ} (hK : 0 < K) {w : ℚ} {v : Option ℚ}
    (hw : RationalBits w K) (hv : WeightedOptionBits K v) :
    WeightedOptionBits (2*K) (rationalWeightedTermWithTrace w v).1 ∧
      ∀ e ∈ (rationalWeightedTermWithTrace w v).2, eventBits K e := by
  have hz := rationalBits_mono rationalBits_zero hK
  unfold rationalWeightedTermWithTrace
  split_ifs with hzero
  · constructor
    · intro q hq
      cases hq
      exact rationalBits_mono hz (by omega)
    · intro e he
      simp only [List.mem_cons, List.not_mem_nil, or_false] at he
      rcases he with rfl | rfl
      · exact ⟨hw, hz⟩
      · exact ⟨hz, hw⟩
  · cases v with
    | none =>
      constructor
      · intro q hq; cases hq
      · intro e he
        simp only [List.mem_cons, List.not_mem_nil, or_false] at he
        rcases he with rfl | rfl
        · exact ⟨hw, hz⟩
        · exact ⟨hz, hw⟩
    | some q =>
      have hq := hv q rfl
      have hm := rationalBits_max_zero hq
      constructor
      · intro z hz'
        simp only [clipZeroWithTrace_value, Option.some.injEq] at hz'
        subst z
        simpa only [two_mul] using rationalBits_mul hw hm
      · intro e he
        simp only [clipZeroWithTrace, List.mem_append, List.mem_cons,
          List.not_mem_nil, or_false] at he
        rcases he with ((rfl | rfl) | rfl) | rfl
        · exact ⟨hw, hz⟩
        · exact ⟨hz, hw⟩
        · exact ⟨hq, hz⟩
        · exact ⟨hw, by simpa only [max_def] using hm⟩

def rationalCostAddWithTrace (a b : Option ℚ) : Option ℚ × List ArithmeticEvent :=
  match a, b with
  | some x, some y =>
    let cx := clipZeroWithTrace x
    let cy := clipZeroWithTrace y
    (some (cx.1 + cy.1), cx.2 ++ cy.2 ++ [(.add, cx.1, cy.1)])
  | _, _ => (none, [])

@[simp] theorem rationalCostAddWithTrace_value (a b : Option ℚ) :
    (rationalCostAddWithTrace a b).1 = rationalCostAdd a b := by
  cases a <;> cases b <;> simp [rationalCostAddWithTrace, rationalCostAdd]

theorem rationalCostAddWithTrace_length (a b : Option ℚ) :
    (rationalCostAddWithTrace a b).2.length ≤ 3 := by
  cases a <;> cases b <;> simp [rationalCostAddWithTrace, clipZeroWithTrace]

theorem rationalCostAddWithTrace_bits {A B : ℕ} {a b : Option ℚ}
    (ha : WeightedOptionBits A a) (hb : WeightedOptionBits B b) :
    WeightedOptionBits (A+B+1) (rationalCostAddWithTrace a b).1 ∧
      ∀ e ∈ (rationalCostAddWithTrace a b).2, eventBits (A+B+1) e := by
  cases a with
  | none => simp [rationalCostAddWithTrace, WeightedOptionBits]
  | some x =>
    cases b with
    | none => simp [rationalCostAddWithTrace, WeightedOptionBits]
    | some y =>
      have hx := ha x rfl
      have hy := hb y rfl
      have hcx := rationalBits_max_zero hx
      have hcy := rationalBits_max_zero hy
      constructor
      · intro z hz
        simp only [rationalCostAddWithTrace, clipZeroWithTrace_value, Option.some.injEq] at hz
        subst z
        exact rationalBits_add hcx hcy
      · intro e he
        simp only [rationalCostAddWithTrace, clipZeroWithTrace, List.mem_append,
          List.mem_cons, List.not_mem_nil, or_false] at he
        have hz := rationalBits_mono rationalBits_zero (show 1 ≤ A+B+1 by omega)
        rcases he with (rfl | rfl) | rfl
        · exact ⟨rationalBits_mono hx (by omega), hz⟩
        · exact ⟨rationalBits_mono hy (by omega), hz⟩
        · exact ⟨rationalBits_mono (by simpa only [max_def] using hcx) (by omega),
            rationalBits_mono (by simpa only [max_def] using hcy) (by omega)⟩

def rationalWeightedListWithTrace : List (ℚ × Option ℚ) → Option ℚ × List ArithmeticEvent
  | [] => (some 0, [])
  | (w, v) :: xs =>
    let head := rationalWeightedTermWithTrace w v
    let tail := rationalWeightedListWithTrace xs
    let total := rationalCostAddWithTrace head.1 tail.1
    (total.1, head.2 ++ tail.2 ++ total.2)

@[simp] theorem rationalWeightedListWithTrace_value (xs : List (ℚ × Option ℚ)) :
    (rationalWeightedListWithTrace xs).1 = rationalWeightedList xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
    rcases x with ⟨w, v⟩
    simp only [rationalWeightedListWithTrace, rationalWeightedList,
      rationalCostAddWithTrace_value, rationalWeightedTermWithTrace_value, ih]

theorem rationalWeightedListWithTrace_length (xs : List (ℚ × Option ℚ)) :
    (rationalWeightedListWithTrace xs).2.length ≤ 7 * xs.length := by
  induction xs with
  | nil => simp [rationalWeightedListWithTrace]
  | cons x xs ih =>
    rcases x with ⟨w, v⟩
    have hh := rationalWeightedTermWithTrace_length w v
    have ha := rationalCostAddWithTrace_length
      (rationalWeightedTermWithTrace w v).1 (rationalWeightedListWithTrace xs).1
    simp only [rationalWeightedListWithTrace, List.length_append, List.length_cons]
    omega

def weightedFoldWidth (m K : ℕ) : ℕ := 1 + m * (2*K+1)

theorem rationalWeightedListWithTrace_bits {xs : List (ℚ × Option ℚ)} {K : ℕ}
    (hK : 0 < K) (h : ∀ x ∈ xs, RationalBits x.1 K ∧ WeightedOptionBits K x.2) :
    WeightedOptionBits (weightedFoldWidth xs.length K) (rationalWeightedListWithTrace xs).1 ∧
      ∀ e ∈ (rationalWeightedListWithTrace xs).2, eventBits (weightedFoldWidth xs.length K) e := by
  induction xs with
  | nil =>
    constructor
    · intro q hq
      cases hq
      simpa [weightedFoldWidth] using rationalBits_zero
    · simp [rationalWeightedListWithTrace]
  | cons x xs ih =>
    rcases x with ⟨w, v⟩
    have hh := rationalWeightedTermWithTrace_bits hK (h (w,v) (by simp)).1 (h (w,v) (by simp)).2
    have ht := ih (fun x hx => h x (by simp [hx]))
    have ha := rationalCostAddWithTrace_bits hh.1 ht.1
    have heq : 2*K + weightedFoldWidth xs.length K + 1 =
        weightedFoldWidth ((w,v)::xs).length K := by
      simp only [weightedFoldWidth, List.length_cons]
      ring
    rw [heq] at ha
    refine ⟨ha.1, ?_⟩
    intro e he
    simp only [rationalWeightedListWithTrace, List.mem_append] at he
    rcases he with (he | he) | he
    · exact eventBits_mono (hh.2 e he) (by
        simp only [weightedFoldWidth, List.length_cons, Nat.add_mul, Nat.one_mul]; omega)
    · exact eventBits_mono (ht.2 e he) (by
        simp only [weightedFoldWidth, List.length_cons, Nat.add_mul, Nat.one_mul]; omega)
    · exact ha.2 e he

/-- Compute each contrast once and retain its optional value and actual events. -/
def weightedContrastInputsWithTrace {n m : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ) :
    List (ℚ × Option ℚ) × List ArithmeticEvent :=
  let runs := List.ofFn fun i : Fin m =>
    let c := rationalContrastWithTrace A (cs i)
    ((ws i, if c.1.1 then some c.1.2 else none), c.2)
  (runs.map Prod.fst, (runs.map Prod.snd).flatten)

@[simp] theorem weightedContrastInputsWithTrace_value {n m : ℕ}
    (A : Matrix (Fin n) (Fin n) ℚ) (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ) :
    (weightedContrastInputsWithTrace A cs ws).1 =
      List.ofFn (fun i => (ws i, rationalContrastCost A (cs i))) := by
  simp only [weightedContrastInputsWithTrace, List.map_ofFn, Function.comp_def,
    rationalContrastWithTrace_value, rationalContrastCost]

theorem weightedContrastInputsWithTrace_length {n m : ℕ}
    (A : Matrix (Fin n) (Fin n) ℚ) (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ) :
    (weightedContrastInputsWithTrace A cs ws).2.length ≤ m * contrastOperations n := by
  simp only [weightedContrastInputsWithTrace, List.map_ofFn, Function.comp_def,
    List.length_flatten, List.sum_ofFn]
  calc
    _ ≤ ∑ _i : Fin m, contrastOperations n :=
      Finset.sum_le_sum (fun i _ => rationalContrastWithTrace_length A (cs i))
    _ = _ := by simp

def weightedContrastInputBits (n B : ℕ) : ℕ := contrastTraceBits n B + B + 1

theorem weightedContrastInputsWithTrace_bits {n m B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} {cs : Fin m → Fin n → ℚ} {ws : Fin m → ℚ}
    (hA : MatrixBits A B) (hc : ∀ i j, RationalBits (cs i j) B)
    (hw : ∀ i, RationalBits (ws i) B) :
    (∀ x ∈ (weightedContrastInputsWithTrace A cs ws).1,
      RationalBits x.1 (weightedContrastInputBits n B) ∧
      WeightedOptionBits (weightedContrastInputBits n B) x.2) ∧
      ∀ e ∈ (weightedContrastInputsWithTrace A cs ws).2,
        eventBits (weightedContrastInputBits n B) e := by
  have hb : B ≤ weightedContrastInputBits n B := by unfold weightedContrastInputBits; omega
  have hv : contrastTraceBits n B ≤ weightedContrastInputBits n B := by
    unfold weightedContrastInputBits; omega
  constructor
  · intro x hx
    rw [weightedContrastInputsWithTrace_value] at hx
    obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hx
    refine ⟨rationalBits_mono (hw i) hb, ?_⟩
    intro q hq
    unfold rationalContrastCost at hq
    split_ifs at hq
    · cases hq
      exact rationalBits_mono (rationalContrastWithTrace_bits hB hA (hc i)).1 hv
  · intro e he
    simp only [weightedContrastInputsWithTrace, List.map_ofFn, Function.comp_def] at he
    obtain ⟨row, hrow, he⟩ := List.mem_flatten.mp he
    obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hrow
    exact eventBits_mono ((rationalContrastWithTrace_bits hB hA (hc i)).2 e he) hv

/-- Full weighted producer: zero weights erase non-estimable costs in the fold. -/
def rationalWeightedContrastCostWithTrace {n m : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ) : Option ℚ × List ArithmeticEvent :=
  let inputs := weightedContrastInputsWithTrace A cs ws
  let total := rationalWeightedListWithTrace inputs.1
  (total.1, inputs.2 ++ total.2)

@[simp] theorem rationalWeightedContrastCostWithTrace_value {n m : ℕ}
    (A : Matrix (Fin n) (Fin n) ℚ) (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ) :
    (rationalWeightedContrastCostWithTrace A cs ws).1 = rationalWeightedContrastCost A cs ws := by
  simp only [rationalWeightedContrastCostWithTrace, rationalWeightedListWithTrace_value,
    weightedContrastInputsWithTrace_value, rationalWeightedContrastCost]

theorem rationalWeightedContrastCostWithTrace_length {n m : ℕ}
    (A : Matrix (Fin n) (Fin n) ℚ) (cs : Fin m → Fin n → ℚ) (ws : Fin m → ℚ) :
    (rationalWeightedContrastCostWithTrace A cs ws).2.length ≤ m * (contrastOperations n + 7) := by
  have hi := weightedContrastInputsWithTrace_length A cs ws
  have ht := rationalWeightedListWithTrace_length (weightedContrastInputsWithTrace A cs ws).1
  have hlen : (weightedContrastInputsWithTrace A cs ws).1.length = m := by
    rw [weightedContrastInputsWithTrace_value, List.length_ofFn]
  rw [hlen] at ht
  simp only [rationalWeightedContrastCostWithTrace, List.length_append]
  nlinarith

def weightedContrastTraceBits (n m B : ℕ) : ℕ :=
  weightedContrastInputBits n B + weightedFoldWidth m (weightedContrastInputBits n B)

theorem rationalWeightedContrastCostWithTrace_bits {n m B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} {cs : Fin m → Fin n → ℚ} {ws : Fin m → ℚ}
    (hA : MatrixBits A B) (hc : ∀ i j, RationalBits (cs i j) B)
    (hw : ∀ i, RationalBits (ws i) B) :
    WeightedOptionBits (weightedContrastTraceBits n m B)
      (rationalWeightedContrastCostWithTrace A cs ws).1 ∧
      ∀ e ∈ (rationalWeightedContrastCostWithTrace A cs ws).2,
        eventBits (weightedContrastTraceBits n m B) e := by
  have hi := weightedContrastInputsWithTrace_bits hB hA hc hw
  have hK : 0 < weightedContrastInputBits n B := by unfold weightedContrastInputBits; omega
  have ht := rationalWeightedListWithTrace_bits hK hi.1
  have hlen : (weightedContrastInputsWithTrace A cs ws).1.length = m := by
    rw [weightedContrastInputsWithTrace_value, List.length_ofFn]
  rw [hlen] at ht
  have htop : weightedFoldWidth m (weightedContrastInputBits n B) ≤
      weightedContrastTraceBits n m B := by unfold weightedContrastTraceBits; omega
  refine ⟨weightedOptionBits_mono ht.1 htop, ?_⟩
  intro e he
  simp only [rationalWeightedContrastCostWithTrace, List.mem_append] at he
  rcases he with he | he
  · exact eventBits_mono (hi.2 e he) (by unfold weightedContrastTraceBits; omega)
  · exact eventBits_mono (ht.2 e he) htop

theorem rationalWeightedContrastCostWithTrace_bitWork {n m B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} {cs : Fin m → Fin n → ℚ} {ws : Fin m → ℚ}
    (hA : MatrixBits A B) (hc : ∀ i j, RationalBits (cs i j) B)
    (hw : ∀ i, RationalBits (ws i) B) :
    traceBitWork (weightedContrastTraceBits n m B)
      (rationalWeightedContrastCostWithTrace A cs ws).2 ≤
      m * (contrastOperations n + 7) * (256 * (weightedContrastTraceBits n m B + 1) ^ 3) :=
  (traceBitWork_le (rationalWeightedContrastCostWithTrace_bits hB hA hc hw).2).trans
    (Nat.mul_le_mul_right _ (rationalWeightedContrastCostWithTrace_length A cs ws))

end DAGSpectral
