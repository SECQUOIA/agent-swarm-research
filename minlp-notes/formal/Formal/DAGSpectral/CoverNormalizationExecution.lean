import Formal.DAGSpectral.RationalStorage
import Formal.DAGSpectral.NormalizationBits
import Formal.DAGSpectral.CoverProducer
import Formal.DAGSpectral.ProfileBitCost

/-! Eager rational matrix execution with the value and its arithmetic trace
returned together. The stored rows prevent subsequent entry lookups from
repeating an inverse or a matrix product. -/
namespace DAGSpectral
open Matrix ReciprocalAnchor
open scoped BigOperators
namespace CoverNormalizationExecution

theorem flatten_singletons {α : Type*} (xs : List α) :
    (xs.map (fun x => [x])).flatten = xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp [ih]

theorem flatten_ofFn_singletons {α : Type*} {n : ℕ} (f : Fin n → α) :
    (List.ofFn fun i => [f i]).flatten = List.ofFn f := by
  simpa only [List.map_ofFn, Function.comp_def] using flatten_singletons (List.ofFn f)


structure MatrixRun (l m : ℕ) where
  rows : Vector (Vector ℚ m) l
  events : List ArithmeticEvent
  copies : ℕ

def MatrixRun.value {l m : ℕ} (a : MatrixRun l m) : Matrix (Fin l) (Fin m) ℚ :=
  fun i j => (a.rows.get i).get j

def runMatrix {l m : ℕ} (E : Fin l → Fin m → ArithmeticExpr) : MatrixRun l m :=
  let cells := Vector.ofFn fun i => Vector.ofFn fun j => (E i j).run
  { rows := cells.map (fun row => row.map Prod.fst)
    events := (List.ofFn fun i =>
      (List.ofFn fun j => ((cells.get i).get j).2).flatten).flatten
    copies := 2 * (∑ i, ∑ j, RationalStorage.scalarCopy (((cells.get i).get j).1)) +
      2*(l+1)*(m+1) }

@[simp] theorem runMatrix_value {l m : ℕ} (E : Fin l → Fin m → ArithmeticExpr) :
    (runMatrix E).value = fun i j => (E i j).eval := by
  funext i j
  simp [runMatrix, MatrixRun.value, ArithmeticExpr.run_eq]

@[simp] theorem runMatrix_events {l m : ℕ} (E : Fin l → Fin m → ArithmeticExpr) :
    (runMatrix E).events = matrixExprTrace E := by
  simp [runMatrix, matrixExprTrace, ArithmeticExpr.run_eq]

def mulRun {l n m : ℕ} (A : Matrix (Fin l) (Fin n) ℚ)
    (B : Matrix (Fin n) (Fin m) ℚ) : MatrixRun l m := runMatrix (matrixMulEntryExpr A B)

def inverseRun {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : MatrixRun n n :=
  runMatrix (inverseEntryExpr A)

@[simp] theorem mulRun_value {l n m : ℕ} (A : Matrix (Fin l) (Fin n) ℚ)
    (B : Matrix (Fin n) (Fin m) ℚ) : (mulRun A B).value = A*B := by
  ext i j
  simp [mulRun]

@[simp] theorem mulRun_events {l n m : ℕ} (A : Matrix (Fin l) (Fin n) ℚ)
    (B : Matrix (Fin n) (Fin m) ℚ) : (mulRun A B).events = matrixMulTrace A B := by
  simp [mulRun, matrixMulTrace]

@[simp] theorem inverseRun_value {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (inverseRun A).value = rationalMatrixInverse A := by
  ext i j
  simp [inverseRun]

@[simp] theorem inverseRun_events {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (inverseRun A).events = matrixInverseTrace A := by
  simp [inverseRun, matrixInverseTrace]

structure NormalizationRun (p r : ℕ) where
  projector : MatrixRun p p
  transform : MatrixRun r p
  restore : MatrixRun p r
  atom : MatrixRun r r
  events : List ArithmeticEvent
  copies : ℕ

/-- Execute and cache all finite matrices used by one normalization. -/
def normalizeRun {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ) (τ : Fin r → ℚ)
    (A : Matrix (Fin p) (Fin p) ℚ) : NormalizationRun p r :=
  let G := mulRun Vᵀ V
  let Gi := inverseRun G.value
  let L := mulRun Gi.value Vᵀ
  let P := mulRun V L.value
  let T := mulRun (diagonal τ) L.value
  let inverses := Vector.ofFn fun i => (ArithmeticExpr.op .inv (.atom (τ i)) (.atom 0)).run
  let K := mulRun V (diagonal (fun i => (inverses.get i).1))
  let TA := mulRun T.value A
  let ATA := mulRun TA.value T.valueᵀ
  { projector := P, transform := T, restore := K, atom := ATA
    events := G.events ++ Gi.events ++ L.events ++ P.events ++ T.events ++
      (List.ofFn fun i => (inverses.get i).2).flatten ++ K.events ++ TA.events ++ ATA.events
    copies := G.copies + Gi.copies + L.copies + P.copies + T.copies +
      RationalStorage.vectorCopy (fun i => (inverses.get i).1) + (r+1) +
      K.copies + TA.copies + ATA.copies + 1 }

@[simp] theorem normalizeRun_projector {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (τ : Fin r → ℚ) (A : Matrix (Fin p) (Fin p) ℚ) :
    (normalizeRun V τ A).projector.value = rangeProjectorProducer V := by
  simp [normalizeRun, rangeProjectorProducer, gramLeftInverseProducer]

@[simp] theorem normalizeRun_transform {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (τ : Fin r → ℚ) (A : Matrix (Fin p) (Fin p) ℚ) :
    (normalizeRun V τ A).transform.value = normalizerProducer V τ := by
  simp [normalizeRun, normalizerProducer, gramLeftInverseProducer]

@[simp] theorem normalizeRun_restore {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (τ : Fin r → ℚ) (A : Matrix (Fin p) (Fin p) ℚ) :
    (normalizeRun V τ A).restore.value = reconstructorProducer V τ := by
  simp [normalizeRun, reconstructorProducer, ArithmeticExpr.run_eq,
    ArithmeticExpr.eval, primitiveResult]

@[simp] theorem normalizeRun_atom {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (τ : Fin r → ℚ) (A : Matrix (Fin p) (Fin p) ℚ) :
    (normalizeRun V τ A).atom.value = transformProducer V τ A := by
  simp [normalizeRun, transformProducer, normalizerProducer, gramLeftInverseProducer]

@[simp] theorem normalizeRun_events {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (τ : Fin r → ℚ) (A : Matrix (Fin p) (Fin p) ℚ) :
    (normalizeRun V τ A).events = NormalizationBits.normalizationTrace V τ A := by
  simp [normalizeRun, NormalizationBits.normalizationTrace, gramLeftInverseProducer,
    normalizerProducer, ArithmeticExpr.run_eq, ArithmeticExpr.eval, ArithmeticExpr.trace,
    primitiveResult, flatten_ofFn_singletons]

def compareRun (a b : ℚ) : Bool × List ArithmeticEvent :=
  let r := (ArithmeticExpr.op .compare (.atom a) (.atom b)).run
  (decide (r.1 = 1), r.2)

@[simp] theorem compareRun_value (a b : ℚ) : (compareRun a b).1 = decide (a ≤ b) := by
  by_cases h : a ≤ b <;>
    simp [compareRun, ArithmeticExpr.run_eq, ArithmeticExpr.eval, primitiveResult, h]

@[simp] theorem compareRun_events (a b : ℚ) :
    (compareRun a b).2 = [(ManyLeaf.BitCost.RationalPrimitive.compare, a, b)] := rfl

structure AtomRun (p r : ℕ) where
  normalized : NormalizationRun p r
  accepted : Bool
  events : List ArithmeticEvent
  copies : ℕ

def atomRun {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ) (τ : Fin r → ℚ)
    (A : Matrix (Fin p) (Fin p) ℚ) : AtomRun p r :=
  let N := normalizeRun V τ A
  let PA := mulRun N.projector.value A
  let checks := (List.ofFn fun i => (List.ofFn fun j =>
    [compareRun (PA.value i j) (A i j), compareRun (A i j) (PA.value i j)]).flatten).flatten
  let diagonalChecks := List.ofFn fun i => compareRun (N.atom.value i i) (4*p)
  { normalized := N
    accepted := checks.all Prod.fst && diagonalChecks.all Prod.fst
    events := N.events ++ PA.events ++ (checks.map Prod.snd).flatten ++
      (diagonalChecks.map Prod.snd).flatten
    copies := N.copies + PA.copies + 4*p*p + 2*r + 3 }

@[simp] theorem atomRun_normalized {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (τ : Fin r → ℚ) (A : Matrix (Fin p) (Fin p) ℚ) :
    (atomRun V τ A).normalized = normalizeRun V τ A := rfl

theorem all_ofFn {n : ℕ} {α : Type*} (f : Fin n → α) (g : α → Bool) :
    (List.ofFn f).all g = true ↔ ∀ i, g (f i) = true := by
  rw [List.all_eq_true]
  constructor
  · intro h i
    exact h _ (List.mem_ofFn.mpr ⟨i, rfl⟩)
  · intro h a ha
    obtain ⟨i, rfl⟩ := List.mem_ofFn.mp ha
    exact h i

theorem atomRun_accepted_iff {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (τ : Fin r → ℚ) (A : Matrix (Fin p) (Fin p) ℚ) :
    (atomRun V τ A).accepted = true ↔
      rangeProjectorProducer V * A = A ∧ ∀ i, (transformProducer V τ A) i i ≤ 4*p := by
  simp only [atomRun, normalizeRun_projector, normalizeRun_atom, mulRun_value,
    Bool.and_eq_true, List.all_flatten, all_ofFn, List.all_cons, List.all_nil,
    Bool.and_true, compareRun_value, decide_eq_true_eq]
  constructor
  · rintro ⟨h, hd⟩
    refine ⟨?_, hd⟩
    ext i j
    exact le_antisymm (h i j).1 (h i j).2
  · rintro ⟨h, hd⟩
    refine ⟨?_, hd⟩
    intro i j
    rw [h]
    exact ⟨le_rfl, le_rfl⟩

/-- The cached acceptance flag is exactly the producer's rational range and
magnitude test, including negative transformed off-diagonal entries. -/
theorem atomRun_accepted_code {p M : ℕ} (u : Fin M → Fin p → ℚ)
    (w : Fin M → ℚ) (b : Finset (Fin M)) (A : Matrix (Fin p) (Fin p) ℚ) :
    (atomRun (NormalizationTrials.columns u b) (NormalizationTrials.scales w b) A).accepted =
      decide (NormalizationTrials.acceptsAtomCode u w b A) := by
  apply Bool.eq_iff_iff.mpr
  rw [atomRun_accepted_iff, decide_eq_true_eq]
  rfl

open NormalizationBits in
def atomBudget (p r B T Q : ℕ) : ℕ :=
  traceBudget p r B T Q +
  arithmeticWidth (2*p) (projectorBudget p r B + Q + 1) +
  mulBudget p (projectorBudget p r B) Q +
  transformBudget p r B T Q + Q + 4*p + 2

def atomOperations (p r : ℕ) : ℕ :=
  NormalizationBits.normalizationOperations p r + p*p*(2*p) + p*p*2 + r

theorem atomRun_events_length {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (τ : Fin r → ℚ) (A : Matrix (Fin p) (Fin p) ℚ) :
    (atomRun V τ A).events.length = atomOperations p r := by
  simp [atomRun, normalizeRun_events, mulRun_events, compareRun_events,
    List.map_flatten, List.map_ofFn, Function.comp_def, List.length_flatten,
    NormalizationBits.normalizationTrace_length, atomOperations, Nat.mul_assoc, Nat.add_assoc]

private theorem natCast_bits (n : ℕ) : RationalBits (n : ℚ) (n+1) := by
  simp only [RationalBits, Rat.num_natCast, Rat.den_natCast, Int.natAbs_natCast]
  constructor
  · exact (Nat.lt_two_pow_self (n := n)).trans_le
      (Nat.pow_le_pow_right (by decide) (by omega))
  · exact Nat.one_lt_two_pow (by omega)

open NormalizationBits in
theorem atomRun_events_bits {p r B T Q : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    {τ : Fin r → ℚ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hV : MatrixBits V B) (hτ : ∀ i, RationalBits (τ i) T) (hA : MatrixBits A Q) :
    ∀ e ∈ (atomRun V τ A).events, eventBits (atomBudget p r B T Q) e := by
  have hP := projector_bits hV
  have hPA : MatrixBits (rangeProjectorProducer V * A)
      (mulBudget p (projectorBudget p r B) Q) := matrixBits_mul hP hA
  have hN := transform_bits hV hτ hA
  have hconstant : RationalBits (4 * (p : ℚ)) (4*p+1) := by
    simpa using natCast_bits (4*p)
  intro e he
  simp only [atomRun, normalizeRun_events, normalizeRun_projector, mulRun_events,
    normalizeRun_atom, mulRun_value, List.mem_append] at he
  rcases he with ((he | he) | he) | he
  · exact eventBits_mono (normalizationTrace_bits hV hτ hA e he)
      (by unfold atomBudget; omega)
  · exact eventBits_mono (matrixMulTrace_bits (B := projectorBudget p r B+Q+1)
      (by omega) (matrixBits_mono hP (by omega))
      (matrixBits_mono hA (by omega)) e he) (by unfold atomBudget; omega)
  · simp only [List.mem_flatten, List.mem_map, List.mem_ofFn] at he
    obtain ⟨_, ⟨c, hc, rfl⟩, he⟩ := he
    obtain ⟨_, ⟨i, rfl⟩, hc⟩ := hc
    simp only [List.mem_flatten, List.mem_ofFn] at hc
    obtain ⟨_, ⟨j, rfl⟩, hpair⟩ := hc
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hpair
    rcases hpair with rfl | rfl <;> simp only [compareRun_events, List.mem_singleton] at he
    · subst e
      exact ⟨rationalBits_mono (hPA i j) (by unfold atomBudget; omega),
        rationalBits_mono (hA i j) (by unfold atomBudget; omega)⟩
    · subst e
      exact ⟨rationalBits_mono (hA i j) (by unfold atomBudget; omega),
        rationalBits_mono (hPA i j) (by unfold atomBudget; omega)⟩
  · simp only [List.mem_flatten, List.mem_map, List.mem_ofFn] at he
    obtain ⟨_, ⟨_, ⟨i, rfl⟩, rfl⟩, he⟩ := he
    simp only [compareRun_events, List.mem_singleton] at he
    subst e
    exact ⟨rationalBits_mono (hN i i) (by unfold atomBudget; omega),
      rationalBits_mono hconstant (by unfold atomBudget; omega)⟩

open NormalizationBits in
theorem atomRun_bitWork {p r B T Q : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    {τ : Fin r → ℚ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hV : MatrixBits V B) (hτ : ∀ i, RationalBits (τ i) T) (hA : MatrixBits A Q) :
    traceBitWork (atomBudget p r B T Q) (atomRun V τ A).events ≤
      atomOperations p r * (256 * (atomBudget p r B T Q+1)^3) := by
  simpa only [atomRun_events_length] using traceBitWork_le (atomRun_events_bits hV hτ hA)

open NormalizationBits in
def atomBitCoefficient (p r : ℕ) : ℕ :=
  normalizationBitCoefficient p r +
  2^(2*p) * (projectorBudget p r 1 + 4) +
  mulBudget p (projectorBudget p r 1) 1 + transformBudget p r 1 7 1 + 4*p+3

open NormalizationBits in
theorem atomBudget_linear (p r B : ℕ) :
    atomBudget p r B (6*B+1) B ≤ atomBitCoefficient p r * (B+1) := by
  have hn := dyadicTraceBudget_linear p r B
  have hp := projectorBudget_scale (p := p) (r := r)
    (show B ≤ 1*(B+1) by omega) (show 1 ≤ B+1 by omega)
  have hm := mulBudget_scale (n := p) hp
    (show B ≤ 1*(B+1) by omega) (show 1 ≤ B+1 by omega)
  have ht := transformBudget_scale (p := p) (r := r)
    (show B ≤ 1*(B+1) by omega) (show 6*B+1 ≤ 7*(B+1) by omega)
    (show B ≤ 1*(B+1) by omega) (show 1 ≤ B+1 by omega)
  have hw : arithmeticWidth (2*p) (projectorBudget p r B+B+1) ≤
      (2^(2*p)*(projectorBudget p r 1+4))*(B+1) := by
    unfold arithmeticWidth
    calc
      _ ≤ 2^(2*p)*(projectorBudget p r B+B+1+2) := Nat.sub_le _ _
      _ ≤ 2^(2*p)*((projectorBudget p r 1+4)*(B+1)) :=
        Nat.mul_le_mul_left _ (by nlinarith)
      _ = _ := by ring
  unfold atomBudget atomBitCoefficient
  unfold dyadicTraceBudget at hn
  nlinarith

def atomCostCoefficient (p r : ℕ) : ℕ :=
  atomOperations p r * 256 * (atomBitCoefficient p r+1)^3

theorem atomRun_bitWork_polynomial {p r B : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    {w : Fin r → ℚ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hV : MatrixBits V B) (hw : ∀ i, RationalBits (w i) B) (hA : MatrixBits A B) :
    traceBitWork (atomBudget p r B (6*B+1) B)
      (atomRun V (NormalizationBits.actualScales w) A).events ≤
      atomCostCoefficient p r * (B+1)^3 := by
  have hb : atomBudget p r B (6*B+1) B+1 ≤ (atomBitCoefficient p r+1)*(B+1) := by
    have := atomBudget_linear p r B
    nlinarith
  apply (atomRun_bitWork hV (NormalizationBits.actualScales_bits hw) hA).trans
  calc
    _ ≤ atomOperations p r * (256 * ((atomBitCoefficient p r+1)*(B+1))^3) :=
      Nat.mul_le_mul_left _ (Nat.mul_le_mul_left _ (Nat.pow_le_pow_left hb 3))
    _ = _ := by unfold atomCostCoefficient; ring

/-- The dyadic search returns its value and the operations that computed it. -/
def scalesRun {r : ℕ} (w : Fin r → ℚ) : Vector (ℚ × List ArithmeticEvent) r :=
  Vector.ofFn fun i => dyadicScaleRun (w i) (NormalizationBits.actualWeightBits (w i))

@[simp] theorem scalesRun_value {r : ℕ} (w : Fin r → ℚ) (i : Fin r) :
    ((scalesRun w).get i).1 = NormalizationBits.actualScales w i := by
  simp [scalesRun, dyadicScaleRun_spec, NormalizationBits.actualScales]

@[simp] theorem scalesRun_events {r : ℕ} (w : Fin r → ℚ) :
    (List.ofFn fun i => ((scalesRun w).get i).2).flatten =
      NormalizationBits.scalesTrace w := by
  simp [scalesRun, dyadicScaleRun_spec, NormalizationBits.scalesTrace]

def dyadicNormalizeRun {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (w : Fin r → ℚ) (A : Matrix (Fin p) (Fin p) ℚ) : NormalizationRun p r :=
  let S := scalesRun w
  let N := normalizeRun V (fun i => (S.get i).1) A
  { N with
    events := (List.ofFn fun i => (S.get i).2).flatten ++ N.events
    copies := RationalStorage.vectorCopy (fun i => (S.get i).1) + r + 1 + N.copies }

@[simp] theorem dyadicNormalizeRun_events {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (w : Fin r → ℚ) (A : Matrix (Fin p) (Fin p) ℚ) :
    (dyadicNormalizeRun V w A).events = NormalizationBits.dyadicNormalizationTrace V w A := by
  simp [dyadicNormalizeRun, normalizeRun_events, NormalizationBits.dyadicNormalizationTrace]

theorem dyadicNormalizeRun_bitWork {p r B : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    {w : Fin r → ℚ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hV : MatrixBits V B) (hw : ∀ i, RationalBits (w i) B) (hA : MatrixBits A B) :
    traceBitWork (NormalizationBits.dyadicTraceBudget p r B)
      (dyadicNormalizeRun V w A).events ≤
      NormalizationBits.normalizationCostCoefficient p r * (B+1)^4 := by
  rw [dyadicNormalizeRun_events]
  exact NormalizationBits.dyadicNormalization_bitWork_polynomial hV hw hA

/-- Every quotient is evaluated once and stored, together with its floor. -/
structure LabelRun (r : ℕ) where
  quotients : MatrixRun r r
  floors : Vector (Vector ℤ r) r
  floorWork : ℕ
  copies : ℕ

def labelRun {r : ℕ} (A : Matrix (Fin r) (Fin r) ℚ) (h : ℚ) : LabelRun r :=
  let Q := runMatrix fun i j => .op .div (.atom (A i j)) (.atom h)
  let F := Vector.ofFn fun i => Vector.ofFn fun j => ⌊Q.value i j⌋
  { quotients := Q
    floors := F
    floorWork := (List.ofFn fun i =>
      (List.ofFn fun j => rationalFloorBitCost (Q.value i j)).sum).sum
    copies := Q.copies + (∑ i, ∑ j, (((F.get i).get j).natAbs.size + 1)) +
      (r+1)*(r+1) }

def LabelRun.value {r : ℕ} (R : LabelRun r) : UpperCoord r → ℤ := fun z =>
  (R.floors.get (upperCoordEquiv r z).val.1).get (upperCoordEquiv r z).val.2

@[simp] theorem labelRun_quotients {r : ℕ} (A : Matrix (Fin r) (Fin r) ℚ) (h : ℚ) :
    (labelRun A h).quotients.value = fun i j => A i j / h := by
  simp [labelRun, ArithmeticExpr.eval, primitiveResult]
  rfl

@[simp] theorem labelRun_value {r : ℕ} (A : Matrix (Fin r) (Fin r) ℚ) (h : ℚ)
    (z : UpperCoord r) :
    (labelRun A h).value z =
      ⌊A (upperCoordEquiv r z).val.1 (upperCoordEquiv r z).val.2 / h⌋ := by
  simp [labelRun, LabelRun.value, ArithmeticExpr.eval, primitiveResult]

@[simp] theorem labelRun_events {r : ℕ} (A : Matrix (Fin r) (Fin r) ℚ) (h : ℚ) :
    (labelRun A h).quotients.events =
      (List.ofFn fun i => List.ofFn fun j =>
        (ReciprocalAnchor.ManyLeaf.BitCost.RationalPrimitive.div, A i j, h)).flatten := by
  simp [labelRun, matrixExprTrace, ArithmeticExpr.trace, ArithmeticExpr.eval,
    flatten_ofFn_singletons]

@[simp] theorem labelRun_floorWork {r : ℕ} (A : Matrix (Fin r) (Fin r) ℚ) (h : ℚ) :
    (labelRun A h).floorWork = ∑ i, ∑ j, rationalFloorBitCost (A i j / h) := by
  simp [labelRun, ArithmeticExpr.eval, primitiveResult, List.sum_ofFn]

/-- The full square cache also contains the requested upper-triangular labels. -/
theorem labelRun_rationalUpperLabels {m r : ℕ}
    (A : Fin m → Matrix (Fin r) (Fin r) ℚ) (h : ℚ) :
    (fun e => (labelRun (A e) h).value) = rationalUpperLabels h A := by
  funext e z
  exact labelRun_value (A e) h z

structure TrialRun (p r m : ℕ) where
  prior : AtomRun p r
  atoms : Vector (AtomRun p r) m
  labels : Vector (LabelRun r) m
  copies : ℕ

def trialRun {p r m : ℕ} (V : Matrix (Fin p) (Fin r) ℚ) (τ : Fin r → ℚ)
    (A : Option (Fin m) → Matrix (Fin p) (Fin p) ℚ) (h : ℚ) : TrialRun p r m :=
  let prior := atomRun V τ (A none)
  let atoms := Vector.ofFn fun e => atomRun V τ (A (some e))
  let labels := Vector.ofFn fun e => labelRun (atoms.get e).normalized.atom.value h
  { prior := prior
    atoms := atoms
    labels := labels
    copies := prior.copies + (∑ e, (atoms.get e).copies) +
      (∑ e, (labels.get e).copies) + 2*(m+1) + 1 }

@[simp] theorem trialRun_atom {p r m : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (τ : Fin r → ℚ) (A : Option (Fin m) → Matrix (Fin p) (Fin p) ℚ) (h : ℚ)
    (e : Fin m) :
    ((trialRun V τ A h).atoms.get e).normalized.atom.value =
      transformProducer V τ (A (some e)) := by simp [trialRun]

theorem trialRun_labels {p r m : ℕ} (V : Matrix (Fin p) (Fin r) ℚ)
    (τ : Fin r → ℚ) (A : Option (Fin m) → Matrix (Fin p) (Fin p) ℚ) (h : ℚ) :
    (fun e => ((trialRun V τ A h).labels.get e).value) =
      rationalUpperLabels h (fun e => transformProducer V τ (A (some e))) := by
  funext e z
  simp [trialRun, rationalUpperLabels]

end CoverNormalizationExecution
end DAGSpectral
