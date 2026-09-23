import Formal.MatroidSpectral.EliminationExecution

/-! Operand traces and polynomial schoolbook charges for the executed determinant.
The trace is a cost observer; the bound is not a timing claim for Lean's backend. -/
namespace MatroidSpectral.Elimination
open Matrix DAGSpectral ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost
open scoped BigOperators

def IntPairBound (M : ℕ) (e : ℤ × ℤ) : Prop :=
  e.1.natAbs ≤ M ∧ e.2.natAbs ≤ M

lemma intPairBound_mono {M N : ℕ} {e : ℤ × ℤ} (h : IntPairBound M e) (hMN : M ≤ N) :
    IntPairBound N e := ⟨h.1.trans hMN, h.2.trans hMN⟩

lemma sumRun_operands_bound {P M : ℕ} (xs : List (ScalarRun ℤ))
    (hvals : ∀ x ∈ xs, x.value.natAbs ≤ P)
    (hevents : ∀ x ∈ xs, ∀ e ∈ x.operands, IntPairBound M e)
    (hP : P ≤ M) (hlen : xs.length * P ≤ M) :
    ∀ e ∈ (sumRun xs).operands, IntPairBound M e := by
  induction xs with
  | nil => simp [sumRun, atom]
  | cons x xs ih =>
      have htail : xs.length * P ≤ M := by
        simp only [List.length_cons] at hlen
        nlinarith
      have hv := sumRun_int_bound xs (fun y hy => hvals y (by simp [hy]))
      have hi := ih (fun y hy => hvals y (by simp [hy]))
        (fun y hy => hevents y (by simp [hy])) htail
      intro e he
      simp only [sumRun, add, List.mem_append, List.mem_singleton] at he
      rcases he with (he | he) | rfl
      · exact hevents x (by simp) e he
      · exact hi e he
      · exact ⟨(hvals x (by simp)).trans hP, hv.trans htail⟩

lemma entryRun_operands_bound {n M P : ℕ} (A F : StoredMatrix ℤ n)
    (hA : ∀ i j, (view A i j).natAbs ≤ M)
    (hF : ∀ i j, (view F i j).natAbs ≤ P)
    (hM : 1 ≤ M) (hP : 1 ≤ P) (i j : Fin n) :
    ∀ e ∈ (entryRun A F i j).operands, IntPairBound (2*n*P*M) e := by
  have hn : 1 ≤ n := by have := i.isLt; omega
  let diag := List.ofFn fun k : Fin n => atom (if i < k then view F k k else 0)
  let weighted := List.ofFn fun k : Fin n =>
    mul (atom (if i < k then view F i k else 0)) (atom (view A k j))
  have hdiag : ∀ x ∈ diag, x.value.natAbs ≤ P := by
    intro x hx
    obtain ⟨k, rfl⟩ := List.mem_ofFn.mp hx
    simp only [atom]
    split_ifs
    · exact hF k k
    · simp
  have hweighted : ∀ x ∈ weighted, x.value.natAbs ≤ P*M := by
    intro x hx
    obtain ⟨k, rfl⟩ := List.mem_ofFn.mp hx
    simp only [mul, atom, Int.natAbs_mul]
    apply Nat.mul_le_mul _ (hA k j)
    split_ifs
    · exact hF i k
    · simp
  have hdp : (sumRun diag).value.natAbs ≤ n*P := by
    simpa [diag] using sumRun_int_bound diag hdiag
  have hwp : (sumRun weighted).value.natAbs ≤ n*(P*M) := by
    simpa [weighted] using sumRun_int_bound weighted hweighted
  have hnp : P ≤ n*P := by nlinarith
  have hpm : P*M ≤ 2*n*P*M := by nlinarith
  have hnpm : n*P*M ≤ 2*n*P*M := by nlinarith
  have hpbound : P ≤ 2*n*P*M := by nlinarith
  have hmbound : M ≤ 2*n*P*M := by nlinarith
  have hdpbound : n*P ≤ 2*n*P*M := by nlinarith
  have hdtrace := sumRun_operands_bound diag hdiag
    (M := 2*n*P*M) (by
      intro x hx e he
      obtain ⟨k, rfl⟩ := List.mem_ofFn.mp hx
      simp [atom] at he) hpbound (by simpa [diag] using hdpbound)
  have hwtrace := sumRun_operands_bound weighted hweighted
    (M := 2*n*P*M) (by
      intro x hx e he
      obtain ⟨k, rfl⟩ := List.mem_ofFn.mp hx
      simp only [mul, atom, List.nil_append, List.mem_singleton] at he
      subst e
      constructor
      · split_ifs
        · exact (hF i k).trans hpbound
        · simp
      · exact (hA k j).trans hmbound) hpm (by simpa [weighted, Nat.mul_assoc] using hnpm)
  intro e he
  change e ∈ (add (mul (neg (sumRun diag)) (atom (view A i j)))
    (sumRun weighted)).operands at he
  simp only [add, mul, neg, atom, List.mem_append, List.mem_singleton, List.mem_nil_iff,
    or_false] at he
  rcases he with (((he | rfl) | rfl) | he) | rfl
  · exact hdtrace e he
  · exact ⟨hdp.trans hdpbound, by simp⟩
  · exact ⟨by simpa using hdp.trans hdpbound, (hA i j).trans hmbound⟩
  · exact hwtrace e he
  · constructor
    · rw [Int.natAbs_mul, Int.natAbs_neg]
      exact (Nat.mul_le_mul hdp (hA i j)).trans hnpm
    · exact hwp.trans (by simpa [Nat.mul_assoc] using hnpm)

lemma entryRun_operands_pow_bound {n K L : ℕ} (A F : StoredMatrix ℤ n)
    (hA : ∀ i j, (view A i j).natAbs ≤ 2 ^ K)
    (hF : ∀ i j, (view F i j).natAbs ≤ 2 ^ L) (i j : Fin n) :
    ∀ e ∈ (entryRun A F i j).operands, IntPairBound (2 ^ (L+K+n+1)) e := by
  have hh := entryRun_operands_bound A F hA hF
    (Nat.one_le_pow _ _ (by decide)) (Nat.one_le_pow _ _ (by decide)) i j
  have hb : 2*n*2 ^ L*2 ^ K ≤ 2 ^ (L+K+n+1) := by
    calc
      _ ≤ 2*2 ^ n*2 ^ L*2 ^ K := by
        gcongr
        exact (Nat.lt_two_pow_self (n := n)).le
      _ = _ := by simp only [pow_add, pow_one]; ring
  exact fun e he => intPairBound_mono (hh e he) hb

lemma stepRun_operands_bound {n K L : ℕ} (A F : StoredMatrix ℤ n)
    (hA : ∀ i j, (view A i j).natAbs ≤ 2 ^ K)
    (hF : ∀ i j, (view F i j).natAbs ≤ 2 ^ L) :
    ∀ e ∈ (stepRun A F).operands, IntPairBound (2 ^ (L+K+n+1)) e := by
  intro e he
  simp only [stepRun, Vector.getElem_ofFn] at he
  obtain ⟨row, hrow, he⟩ := List.mem_flatten.mp he
  obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hrow
  obtain ⟨cell, hcell, he⟩ := List.mem_flatten.mp he
  obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hcell
  exact entryRun_operands_pow_bound A F hA hF i j e he

lemma iterateRun_operands_bound {n K : ℕ} (A : StoredMatrix ℤ n)
    (hA : ∀ i j, (view A i j).natAbs ≤ 2 ^ K) (t : ℕ) :
    ∀ e ∈ (iterateRun A t).operands, IntPairBound (2 ^ (iterationBits n K t)) e := by
  induction t with
  | zero => simp [iterateRun]
  | succ t ih =>
      intro e he
      simp only [iterateRun, List.mem_append] at he
      rcases he with he | he
      · exact intPairBound_mono (ih e he)
          (Nat.pow_le_pow_right (by decide) (by unfold iterationBits; nlinarith))
      · have hh := stepRun_operands_bound A (iterateRun A t).matrix hA
          (iterateRun_natAbs_le A hA t) e he
        simpa [iterationBits, Nat.succ_mul, Nat.add_assoc, Nat.add_comm,
          Nat.add_left_comm] using hh

lemma determinantRun_operands_bound {n K : ℕ} (A : StoredMatrix ℤ n)
    (hA : ∀ i j, (view A i j).natAbs ≤ 2 ^ K) :
    ∀ e ∈ (determinantRun n A).operands,
      IntPairBound (2 ^ (iterationBits n K n)) e := by
  cases n with
  | zero => simp [determinantRun, atom]
  | succ n =>
      intro e he
      simp only [determinantRun, List.mem_append, List.mem_singleton] at he
      have hmono : 2 ^ (iterationBits (n+1) K n) ≤
          2 ^ (iterationBits (n+1) K (n+1)) :=
        Nat.pow_le_pow_right (by decide) (by unfold iterationBits; nlinarith)
      rcases he with he | rfl
      · exact intPairBound_mono (iterateRun_operands_bound A hA n e he) hmono
      · exact ⟨(iterateRun_natAbs_le A hA n 0 0).trans hmono, by simp⟩

lemma sumRun_operands_length {R : Type*} [CommRing R] (xs : List (ScalarRun R))
    (hx : ∀ x ∈ xs, x.operands.length = x.operations) :
    (sumRun xs).operands.length = (sumRun xs).operations := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      simp only [sumRun, add, List.length_append, List.length_singleton]
      rw [hx x (by simp), ih (fun y hy => hx y (by simp [hy]))]

@[simp] theorem entryRun_operands_length {R : Type*} [CommRing R] {n : ℕ}
    (A F : StoredMatrix R n) (i j : Fin n) :
    (entryRun A F i j).operands.length = (entryRun A F i j).operations := by
  unfold entryRun
  simp only [add, mul, neg, atom, List.length_append, List.length_singleton, List.length_nil]
  rw [sumRun_operands_length _ (by
    intro x hx
    obtain ⟨k, rfl⟩ := List.mem_ofFn.mp hx
    rfl), sumRun_operands_length _ (by
    intro x hx
    obtain ⟨k, rfl⟩ := List.mem_ofFn.mp hx
    rfl)]

@[simp] theorem stepRun_operands_length {R : Type*} [CommRing R] {n : ℕ}
    (A F : StoredMatrix R n) :
    (stepRun A F).operands.length = (stepRun A F).operations := by
  simp [stepRun, List.length_flatten, List.map_ofFn, Function.comp_def]

@[simp] theorem iterateRun_operands_length {R : Type*} [CommRing R] {n : ℕ}
    (A : StoredMatrix R n) (t : ℕ) :
    (iterateRun A t).operands.length = (iterateRun A t).operations := by
  induction t with
  | zero => rfl
  | succ t ih => simp [iterateRun, ih]

@[simp] theorem determinantRun_operands_length {R : Type*} [CommRing R]
    (n : ℕ) (A : StoredMatrix R n) :
    (determinantRun n A).operands.length = (determinantRun n A).operations := by
  cases n with
  | zero => rfl
  | succ n => simp [determinantRun]

lemma productNatOperands_length (xs : List ℕ) :
    (productNatOperands xs).length = xs.length := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp [productNatOperands, ih]

lemma productNatOperands_bound (xs : List ℕ) (hxs : ∀ x ∈ xs, 1 ≤ x) :
    ∀ e ∈ productNatOperands xs, e.1 ≤ xs.prod ∧ e.2 ≤ xs.prod := by
  induction xs with
  | nil => simp [productNatOperands]
  | cons x xs ih =>
      have hx := hxs x (by simp)
      have ht : 1 ≤ xs.prod := by
        exact List.one_le_prod (fun y hy => hxs y (by simp [hy]))
      have hi := ih (fun y hy => hxs y (by simp [hy]))
      have htail : xs.prod ≤ x*xs.prod := by nlinarith
      intro e he
      simp only [productNatOperands, List.mem_append, List.mem_singleton] at he
      rcases he with he | rfl
      · exact ⟨(hi e he).1.trans htail, (hi e he).2.trans htail⟩
      · simpa using And.intro (show x ≤ x*xs.prod by nlinarith) htail

@[simp] theorem powerNatOperands_length (x n : ℕ) : (powerNatOperands x n).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [powerNatOperands, ih]

lemma powerNatOperands_bound {x : ℕ} (hx : 1 ≤ x) (n : ℕ) :
    ∀ e ∈ powerNatOperands x n, e.1 ≤ x^n ∧ e.2 ≤ x^n := by
  induction n with
  | zero => simp [powerNatOperands]
  | succ n ih =>
      have hp : 1 ≤ x^n := Nat.one_le_pow _ _ hx
      have hm : x^n ≤ x^(n+1) := by rw [pow_succ]; nlinarith
      intro e he
      simp only [powerNatOperands, List.mem_append, List.mem_singleton] at he
      rcases he with he | rfl
      · exact ⟨(ih e he).1.trans hm, (ih e he).2.trans hm⟩
      · simp only [powerNatRun_value]
        exact ⟨hm, by rw [pow_succ]; nlinarith⟩

/-- A single polynomial width covers clearing, every Bird primitive, the final
power, and rational reconstruction, including order zero. -/
def determinantOperandBits (n B : ℕ) : ℕ := 2+iterationBits n (B+n*n*B) (n+1)

lemma rationalBits_int_of_natAbs_le {x : ℤ} {K : ℕ} (hx : x.natAbs ≤ 2 ^ K) :
    RationalBits (x : ℚ) (K+1) := by
  have hnum : x.natAbs < 2^(K+1) := hx.trans_lt (by
    rw [pow_succ]
    have hp : 0 < 2 ^ K := by positivity
    omega)
  simpa using rationalBits_fraction (n := x) (d := 1) (by decide) hnum
    (show Int.natAbs 1 < 2^(K+1) by simp)

lemma rationalBits_nat_of_le {x K : ℕ} (hx : x ≤ 2 ^ K) :
    RationalBits (x : ℚ) (K+1) := by
  exact_mod_cast rationalBits_int_of_natAbs_le (x := (x : ℤ)) (by simpa using hx)

lemma determinantOperandBits_stage_le (n B : ℕ) :
    iterationBits n (B+n*n*B) n + 1 ≤ determinantOperandBits n B := by
  unfold determinantOperandBits iterationBits
  nlinarith

lemma determinantOperandBits_denom_le (n B : ℕ) :
    n*n*B+1 ≤ determinantOperandBits n B := by
  unfold determinantOperandBits iterationBits
  omega

lemma determinantOperandBits_power_le (n B : ℕ) :
    n*(n*n*B)+1 ≤ determinantOperandBits n B := by
  unfold determinantOperandBits iterationBits
  nlinarith [Nat.zero_le (n*B), Nat.zero_le (n*n), Nat.zero_le (n*n*n*B)]

lemma determinantOperandBits_input_le (n B : ℕ) : B ≤ determinantOperandBits n B := by
  unfold determinantOperandBits iterationBits
  omega

lemma rationalDeterminantRun_operands_length {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (rationalDeterminantRun A).operands.length = (rationalDeterminantRun A).operations := by
  simp [rationalDeterminantRun, denominatorOperands, clearingOperands, List.length_flatten,
    List.map_ofFn, Function.comp_def, productNatOperands_length]
  ring

lemma rationalDeterminantRun_operands_bits {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A B) :
    ∀ e ∈ (rationalDeterminantRun A).operands,
      RationalBits e.1 (determinantOperandBits n B) ∧
      RationalBits e.2 (determinantOperandBits n B) := by
  let W := determinantOperandBits n B
  have hin : B+1 ≤ W := by dsimp [W, determinantOperandBits, iterationBits]; omega
  have hD : matrixDenominator A ≤ 2^(n*n*B) := matrixDenominator_le hA
  have hDbits : RationalBits (matrixDenominator A : ℚ) W :=
    rationalBits_mono (rationalBits_nat_of_le hD) (determinantOperandBits_denom_le n B)
  have hpow : (matrixDenominator A)^n ≤ 2^(n*(n*n*B)) := by
    calc
      _ ≤ (2^(n*n*B))^n := Nat.pow_le_pow_left hD n
      _ = _ := by rw [← pow_mul]; congr 1; ring
  have hpowbits : RationalBits (((matrixDenominator A)^n : ℕ) : ℚ) W :=
    rationalBits_mono (rationalBits_nat_of_le hpow) (determinantOperandBits_power_le n B)
  have hden : ∀ e ∈ denominatorOperands A, RationalBits e.1 W ∧ RationalBits e.2 W := by
    intro e he
    obtain ⟨d, hd, rfl⟩ := List.mem_map.mp he
    have hh := productNatOperands_bound
      ((List.ofFn fun i : Fin n => List.ofFn fun j : Fin n => (A i j).den).flatten)
      (by
        intro x hx
        obtain ⟨row, hrow, hx⟩ := List.mem_flatten.mp hx
        obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hrow
        obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hx
        exact (A i j).den_pos) d hd
    have hprod : ((List.ofFn fun i : Fin n =>
        List.ofFn fun j : Fin n => (A i j).den).flatten).prod = matrixDenominator A := by
      simp [List.prod_flatten, List.map_ofFn, Function.comp_def, List.prod_ofFn,
        matrixDenominator]
    rw [hprod] at hh
    exact ⟨rationalBits_mono (rationalBits_nat_of_le (hh.1.trans hD))
      (determinantOperandBits_denom_le n B),
      rationalBits_mono (rationalBits_nat_of_le (hh.2.trans hD))
        (determinantOperandBits_denom_le n B)⟩
  have hclear : ∀ e ∈ clearingOperands A (matrixDenominator A),
      RationalBits e.1 W ∧ RationalBits e.2 W := by
    intro e he
    obtain ⟨row, hrow, he⟩ := List.mem_flatten.mp he
    obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hrow
    obtain ⟨cell, hcell, he⟩ := List.mem_flatten.mp he
    obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hcell
    simp only [List.mem_cons, List.not_mem_nil, or_false] at he
    rcases he with rfl | rfl
    · exact ⟨hDbits, rationalBits_mono (rationalBits_nat_of_le (hA i j).2.le) hin⟩
    · exact ⟨rationalBits_mono (rationalBits_int_of_natAbs_le (hA i j).1.le) hin,
        rationalBits_mono (rationalBits_nat_of_le ((Nat.div_le_self _ _).trans hD))
          (determinantOperandBits_denom_le n B)⟩
  let Z := (clearingRun A (matrixDenominator A)).matrix
  have hZ : ∀ i j, (view Z i j).natAbs ≤ 2^(B+n*n*B) := by
    simpa [Z] using integerMatrix_natAbs_le hA
  have hztrace : ∀ e ∈ (determinantRun n Z).operands.map intPairRat,
      RationalBits e.1 W ∧ RationalBits e.2 W := by
    intro e he
    obtain ⟨z, hz, rfl⟩ := List.mem_map.mp he
    have hh := determinantRun_operands_bound Z hZ z hz
    exact ⟨rationalBits_mono (rationalBits_int_of_natAbs_le hh.1)
      (determinantOperandBits_stage_le n B),
      rationalBits_mono (rationalBits_int_of_natAbs_le hh.2)
        (determinantOperandBits_stage_le n B)⟩
  have hvalue : RationalBits ((determinantRun n Z).value : ℚ) W := by
    rw [determinantRun_correct]
    apply rationalBits_mono (rationalBits_int_of_natAbs_le (integer_det_natAbs_le hZ))
    dsimp [W, determinantOperandBits, iterationBits]
    nlinarith [Nat.zero_le (n*n*n*B), Nat.zero_le (n*B)]
  have hpowers : ∀ e ∈ (powerNatOperands (matrixDenominator A) n).map natPairRat,
      RationalBits e.1 W ∧ RationalBits e.2 W := by
    intro e he
    obtain ⟨z, hz, rfl⟩ := List.mem_map.mp he
    have hh := powerNatOperands_bound (matrixDenominator_pos A) n z hz
    exact ⟨rationalBits_mono (rationalBits_nat_of_le (hh.1.trans hpow))
      (determinantOperandBits_power_le n B),
      rationalBits_mono (rationalBits_nat_of_le (hh.2.trans hpow))
        (determinantOperandBits_power_le n B)⟩
  intro e he
  simp only [rationalDeterminantRun, denominatorRun_value, powerNatRun_value,
    List.mem_append, List.mem_singleton] at he
  rcases he with (((he | he) | he) | he) | rfl
  · exact hden e he
  · exact hclear e he
  · exact hztrace e he
  · exact hpowers e he
  · exact ⟨hvalue, hpowbits⟩

/-- Reduced numerator and denominator widths. -/
def scalarWidth (q : ℚ) : ℕ := max q.num.natAbs.size q.den.size

def pairWidth (e : ℚ × ℚ) : ℕ := max (scalarWidth e.1) (scalarWidth e.2)

def operandWork (es : List (ℚ × ℚ)) : ℕ :=
  (es.map fun e => 256*(pairWidth e+1)^3).sum

def traceWidth (es : List (ℚ × ℚ)) : ℕ := (es.map pairWidth).foldr max 0

def inputWidth {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : ℕ :=
  Finset.univ.sup fun i => Finset.univ.sup fun j => scalarWidth (A i j)

/-- Copying and index work is charged per executed arithmetic event and input
cell. Each lookup may scan a full stored matrix, so this also permits sequential
storage rather than assuming unit-cost random access. The observer's trace-list
construction is not part of the arithmetic algorithm. The caller supplies a
stored input matrix; synthesizing its entries is charged by the caller. -/
def determinantBitRun {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : ℚ × ℕ :=
  let result := rationalDeterminantRun A
  let width := max (inputWidth A) (traceWidth result.operands)
  (result.value, operandWork result.operands +
    16*(result.operations+n*n+1)*(n*n+1)*(width+n+1))

def determinantBitWork (n B : ℕ) : ℕ :=
  8*(n+1)^4*(256*(determinantOperandBits n B+1)^3) +
    160*(n+1)^6*(determinantOperandBits n B+n+1)

@[simp] theorem determinantBitRun_value {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (determinantBitRun A).1 = A.det := rationalDeterminantRun_correct A

lemma scalarWidth_le {q : ℚ} {B : ℕ} (hq : RationalBits q B) : scalarWidth q ≤ B := by
  exact max_le (rationalBits_iff_size q B |>.mp hq).1
    (rationalBits_iff_size q B |>.mp hq).2

lemma pairWidth_le {e : ℚ × ℚ} {B : ℕ}
    (h : RationalBits e.1 B ∧ RationalBits e.2 B) : pairWidth e ≤ B :=
  max_le (scalarWidth_le h.1) (scalarWidth_le h.2)

lemma traceWidth_le {es : List (ℚ × ℚ)} {B : ℕ}
    (h : ∀ e ∈ es, pairWidth e ≤ B) : traceWidth es ≤ B := by
  induction es with
  | nil => simp [traceWidth]
  | cons e es ih =>
      exact max_le (h e (by simp)) (ih (fun z hz => h z (by simp [hz])))

lemma operandWork_le {es : List (ℚ × ℚ)} {B : ℕ}
    (h : ∀ e ∈ es, pairWidth e ≤ B) :
    operandWork es ≤ es.length*(256*(B+1)^3) := by
  induction es with
  | nil => simp [operandWork]
  | cons e es ih =>
      have hh := h e (by simp)
      have ht := ih (fun z hz => h z (by simp [hz]))
      have he : 256*(pairWidth e+1)^3 ≤ 256*(B+1)^3 := by gcongr
      simp only [operandWork, List.map_cons, List.sum_cons, List.length_cons] at *
      nlinarith

lemma inputWidth_le {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A B) : inputWidth A ≤ B := by
  exact Finset.sup_le fun i _ => Finset.sup_le fun j _ => scalarWidth_le (hA i j)

/-- The charge uses actual executed operation counts and actual reduced widths.
All loop widths are discharged from the original input hypothesis. -/
theorem determinantBitRun_work {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : MatrixBits A B) : (determinantBitRun A).2 ≤ determinantBitWork n B := by
  have hw : ∀ e ∈ (rationalDeterminantRun A).operands,
      pairWidth e ≤ determinantOperandBits n B :=
    fun e he => pairWidth_le (rationalDeterminantRun_operands_bits hA e he)
  have ht := traceWidth_le hw
  have hi := (inputWidth_le hA).trans (determinantOperandBits_input_le n B)
  have hwidth := max_le hi ht
  have hoperations := rationalDeterminantRun_operations_le A
  have harithmetic := operandWork_le hw
  rw [rationalDeterminantRun_operands_length] at harithmetic
  have harithmetic' : operandWork (rationalDeterminantRun A).operands ≤
      8*(n+1)^4*(256*(determinantOperandBits n B+1)^3) :=
    harithmetic.trans (Nat.mul_le_mul_right _ hoperations)
  have hop : (rationalDeterminantRun A).operations+n*n+1 ≤ 10*(n+1)^4 := by
    nlinarith [Nat.zero_le (n*n*n), Nat.zero_le (n*n*n*n)]
  have hn : n*n+1 ≤ (n+1)^2 := by nlinarith
  have hstorage : 16*((rationalDeterminantRun A).operations+n*n+1)*(n*n+1)*
      (max (inputWidth A) (traceWidth (rationalDeterminantRun A).operands)+n+1) ≤
      160*(n+1)^6*(determinantOperandBits n B+n+1) := by
    calc
      _ ≤ 16*(10*(n+1)^4)*((n+1)^2)*(determinantOperandBits n B+n+1) := by
        gcongr
      _ = _ := by ring
  exact Nat.add_le_add harithmetic' hstorage

/-- The width budget itself is polynomial, including when the matrix order
varies with the matroid rank. -/
theorem determinantOperandBits_le (n B : ℕ) :
    determinantOperandBits n B ≤ 4*(n+1)^3*(B+1) := by
  unfold determinantOperandBits iterationBits
  nlinarith [Nat.zero_le (n*n*n*B), Nat.zero_le (n*n*B), Nat.zero_le (n*B),
    Nat.zero_le (n*n*n)]

lemma determinantOperandBits_mono {n m B C : ℕ} (hn : n ≤ m) (hB : B ≤ C) :
    determinantOperandBits n B ≤ determinantOperandBits m C := by
  unfold determinantOperandBits iterationBits
  gcongr

lemma determinantBitWork_mono {n m B C : ℕ} (hn : n ≤ m) (hB : B ≤ C) :
    determinantBitWork n B ≤ determinantBitWork m C := by
  have hw := determinantOperandBits_mono hn hB
  unfold determinantBitWork
  gcongr

/-- Every event's charge covers all rational primitive kinds in the existing
schoolbook model, and thus also covers integer addition and multiplication. -/
lemma primitiveBitCost_le_pair_charge (e : ℚ × ℚ) (op : RationalPrimitive) :
    primitiveBitCost op e.1 e.2 (pairWidth e) ≤ 256*(pairWidth e+1)^3 := by
  have hleft : RationalBits e.1 (pairWidth e) := by
    apply (rationalBits_iff_size _ _).mpr
    constructor <;> simp only [pairWidth, scalarWidth] <;> omega
  have hright : RationalBits e.2 (pairWidth e) := by
    apply (rationalBits_iff_size _ _).mpr
    constructor <;> simp only [pairWidth, scalarWidth] <;> omega
  exact primitiveBitCost_le hleft hright op

/-- The same charge dominates binary long division on integer operand widths. -/
lemma divisionCost_le_pair_charge (e : ℤ × ℤ) :
    divisionCost e.1.natAbs.size e.2.natAbs.size ≤
      256*(pairWidth (intPairRat e)+1)^3 := by
  have hl : e.1.natAbs.size ≤ pairWidth (intPairRat e) := by
    simp [pairWidth, scalarWidth, intPairRat]
  have hr : e.2.natAbs.size ≤ pairWidth (intPairRat e) := by
    simp [pairWidth, scalarWidth, intPairRat]
  have hh := divisionCost_mono hl hr
  apply hh.trans
  rw [divisionCost_eq]
  nlinarith [Nat.zero_le ((pairWidth (intPairRat e))^3)]

end MatroidSpectral.Elimination
