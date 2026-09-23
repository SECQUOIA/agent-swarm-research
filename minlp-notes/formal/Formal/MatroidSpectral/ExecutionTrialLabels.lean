import Formal.MatroidSpectral.NormalizationExecution
import Formal.MatroidSpectral.ExecutionMarked
import Formal.DAGSpectral.MatrixArithmeticTrace

/-! Exact rational arithmetic and a signed floor compute the shift.
The cost observes the actual rational operands and integer floor result. -/
namespace MatroidSpectral.Execution
open ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost DAGSpectral DAGSpectral.NormalizationTrials

/-- Negating the quotient lets the existing signed-floor routine compute a ceil. -/
def trialShiftExpr (p r q : ℕ) (η : ℚ) : ArithmeticExpr :=
  .op .neg (.op .div
    (.op .mul (.op .mul (.op .mul (.atom 4) (.atom p)) (.atom r)) (.atom q))
    (.atom η)) (.atom 0)

lemma trialShiftExpr_value (p r q : ℕ) (η : ℚ) :
    (trialShiftExpr p r q η).eval = -(4*(p : ℚ)*r*q/η) := rfl

lemma trialShiftExpr_operations (p r q : ℕ) (η : ℚ) :
    (trialShiftExpr p r q η).operations = 5 := rfl

def trialShiftBits (p r q B : ℕ) : ℕ := 64*(p+r+q+B+6)

lemma trialShiftExpr_bits (p r q : ℕ) {η : ℚ} {B : ℕ} (hη : RationalBits η B) :
    RationalBits (trialShiftExpr p r q η).eval (trialShiftBits p r q B) ∧
    ∀ e ∈ (trialShiftExpr p r q η).trace, eventBits (trialShiftBits p r q B) e := by
  have hh : (trialShiftExpr p r q η).leavesBounded (p+r+q+B+4) := by
    refine ⟨⟨⟨⟨⟨?_, ?_⟩, ?_⟩, ?_⟩, ?_⟩, ?_⟩
    · exact rationalBits_mono (show RationalBits 4 3 by unfold RationalBits; decide) (by omega)
    · exact rationalBits_mono (rationalBits_nat p) (by omega)
    · exact rationalBits_mono (rationalBits_nat r) (by omega)
    · exact rationalBits_mono (rationalBits_nat q) (by omega)
    · exact rationalBits_mono hη (by omega)
    · exact rationalBits_mono rationalBits_zero (by omega)
  have hp := (trialShiftExpr p r q η).eval_trace_bits hh
  have hb : arithmeticWidth (trialShiftExpr p r q η).operations (p+r+q+B+4) ≤
      trialShiftBits p r q B := by
    simp only [trialShiftExpr_operations, arithmeticWidth, trialShiftBits]
    norm_num
    omega
  exact ⟨rationalBits_mono hp.1 hb, fun e he => eventBits_mono (hp.2 e he) hb⟩

def trialShiftRun (p r q : ℕ) (η : ℚ) (B : ℕ) : ℕ × ℕ :=
  let quotient := (trialShiftExpr p r q η).run
  let z := Int.floor quotient.1
  ((-z).toNat, traceBitWork (trialShiftBits p r q B) quotient.2 +
    rationalFloorBitCost quotient.1 + 3*(z.natAbs.size+1) + 3*(p+r+q+5))

@[simp] lemma trialShiftRun_value (p r q : ℕ) (η : ℚ) (B : ℕ) :
    (trialShiftRun p r q η B).1 = trialShift p r q η := by
  simp only [trialShiftRun, ArithmeticExpr.run_eq, trialShiftExpr_value, trialShift_eq]
  rw [← Int.ceil_neg, neg_neg, Int.ceil_toNat]

def trialShiftWork (p r q B : ℕ) : ℕ :=
  let K := trialShiftBits p r q B
  5*(256*(K+1)^3)+12*(K+1)^2+3*(K+2)+3*(p+r+q+5)

lemma trialShiftRun_work (p r q : ℕ) {η : ℚ} {B : ℕ} (hη : RationalBits η B) :
    (trialShiftRun p r q η B).2 ≤ trialShiftWork p r q B := by
  have hh := trialShiftExpr_bits p r q hη
  have he := traceBitWork_le hh.2
  have hf := rationalFloorBitCost_le hh.1
  have hz := Nat.size_le.mpr (integerBits_floor hh.1)
  simp only [ArithmeticExpr.trace_length, trialShiftExpr_operations] at he
  simp only [trialShiftRun, ArithmeticExpr.run_eq, trialShiftWork]
  omega

lemma trialShift_integerBits (p r q : ℕ) {η : ℚ} {B : ℕ} (hη : RationalBits η B) :
    IntegerBits (trialShift p r q η : ℤ) (trialShiftBits p r q B+1) := by
  have hh := integerBits_floor (trialShiftExpr_bits p r q hη).1
  have hv := trialShiftRun_value p r q η B
  simp only [trialShiftRun, ArithmeticExpr.run_eq] at hv
  rw [← hv]
  have hn : (-⌊(trialShiftExpr p r q η).eval⌋).toNat ≤
      (-⌊(trialShiftExpr p r q η).eval⌋).natAbs := by omega
  exact hn.trans_lt (by simpa only [Int.natAbs_neg, IntegerBits] using hh)

lemma trialShift_le (p r q : ℕ) (η : ℚ) :
    trialShift p r q η ≤ 4*p*r*q*⌈1/η⌉₊ := by
  rw [trialShift_eq]
  apply Nat.ceil_le.mpr
  have hh := mul_le_mul_of_nonneg_left (Nat.le_ceil (1/η))
    (show 0 ≤ 4*(p : ℚ)*r*q by positivity)
  convert hh using 1 <;> push_cast <;> ring

lemma trialShift_mono_q (p r : ℕ) {q Q : ℕ} (hq : q ≤ Q) {η : ℚ} (hη : 0 ≤ η) :
    trialShift p r q η ≤ trialShift p r Q η := by
  rw [trialShift_eq, trialShift_eq]
  apply Nat.ceil_mono
  gcongr

/-- All floor labels, including entries belonging to rejected atoms. -/
def trialSignedBits (p r q B : ℕ) : ℕ :=
  NormalizationBits.transformBudget p r B (6*B+1) B+(B+r+q+2)+1

lemma trialSigned_integerBits {p m M B : ℕ} (D : FactorData p m M)
    (b : Finset (Fin M)) {q : ℕ} {η : ℚ}
    (hV : ∀ j i, RationalBits (D.vector j i) B)
    (hw : ∀ j, RationalBits (D.weight j) B)
    (hD : ∀ o, MatrixBits (D.atom o) B) (hη : RationalBits η B)
    (e : Fin m) (i : UpperCoord b.card) :
    IntegerBits (trialSigned D q η b e i) (trialSignedBits p b.card q B) := by
  exact integerBits_floor (rationalBits_div
    (CoverBitCost.trialAtom_bits D b hV hw hD (some e)
      (upperCoordEquiv b.card i).val.1 (upperCoordEquiv b.card i).val.2)
    (rationalMesh_bits hη b.card q))

/-- A scalar shift charges its actual integer addition, sign conversion, and
copy sizes. The second term covers reading the stored label and its indices. -/
def shiftedCellWork (m d : ℕ) (z : ℤ) (L : ℕ) : ℕ :=
  let s := z + L
  addCost z.natAbs.size L.size + 3*(s.natAbs.size+1) +
    2*(m+1)*(d+1)*(z.natAbs.size+L.size+s.natAbs.size+m+d+3)

def shiftedWeightsCacheRun {m : ℕ} {κ : Type*} [Fintype κ] [LinearOrder κ]
    (signed : Fin m → κ → ℤ) (L : ℕ) : Vector (List (κ × ℕ)) m × ℕ :=
  let indices := (Finset.univ : Finset κ).sort (· ≤ ·)
  let cells := Vector.ofFn (fun e : Fin m => indices.map (fun i =>
    let z := signed e i
    let s := z+L
    ((i, s.toNat), shiftedCellWork m (Fintype.card κ) z L)))
  (cells.map (fun row => row.map Prod.fst),
    (List.ofFn (fun e : Fin m => ((cells.get e).map Prod.snd).sum)).sum +
      (m+1)^2*(Fintype.card κ+1)^3)

@[simp] lemma shiftedWeightsCacheRun_value {m : ℕ} {κ : Type*}
    [Fintype κ] [LinearOrder κ] (signed : Fin m → κ → ℤ) (L : ℕ) :
    (shiftedWeightsCacheRun signed L).1 = weightCache (shiftedWeight signed L) := by
  simp [shiftedWeightsCacheRun, weightCache, shiftedWeight, Vector.map_ofFn,
    List.map_map, Function.comp_def]

def shiftedWeightsCacheWork (m d S T : ℕ) : ℕ :=
  let U := S+T+1
  m*d*(U+1+3*(U+2)+2*(m+1)*(d+1)*(3*U+m+d+4))+(m+1)^2*(d+1)^3

lemma shiftedCellWork_le (m d : ℕ) {z : ℤ} {L S T : ℕ}
    (hz : IntegerBits z S) (hL : IntegerBits (L : ℤ) T) :
    shiftedCellWork m d z L ≤
      (S+T+1)+1+3*((S+T+1)+2)+
        2*(m+1)*(d+1)*(3*(S+T+1)+m+d+4) := by
  have hs : IntegerBits (z+L) (S+T+1) :=
    integerBits_add (integerBits_mono hz (by omega : S ≤ S+T))
      (integerBits_mono hL (by omega : T ≤ S+T))
  have hzs := Nat.size_le.mpr hz
  have hLs := Nat.size_le.mpr hL
  have hss := Nat.size_le.mpr hs
  simp only [Int.natAbs_natCast] at hLs
  dsimp only [shiftedCellWork, addCost]
  have hm : max z.natAbs.size L.size ≤ S+T+1 := max_le (by omega) (by omega)
  have hr : z.natAbs.size+L.size+(z+(L : ℤ)).natAbs.size+m+d+3 ≤
      3*(S+T+1)+m+d+4 := by omega
  have hg := Nat.mul_le_mul_left (2*(m+1)*(d+1)) hr
  omega

lemma shiftedWeightsCacheRun_work {m : ℕ} {κ : Type*} [Fintype κ] [LinearOrder κ]
    (signed : Fin m → κ → ℤ) (L S T : ℕ)
    (hz : ∀ e i, IntegerBits (signed e i) S) (hL : IntegerBits (L : ℤ) T) :
    (shiftedWeightsCacheRun signed L).2 ≤
      shiftedWeightsCacheWork m (Fintype.card κ) S T := by
  simp only [shiftedWeightsCacheRun, Vector.get_ofFn, List.map_map, Function.comp_def,
    List.sum_ofFn, shiftedWeightsCacheWork]
  apply Nat.add_le_add_right
  have hh (e : Fin m) := List.sum_le_sum
    (l := ((Finset.univ : Finset κ).sort (· ≤ ·)))
    (f := fun i => shiftedCellWork m (Fintype.card κ) (signed e i) L)
    (g := fun _ => (S+T+1)+1+3*((S+T+1)+2)+
      2*(m+1)*(Fintype.card κ+1)*(3*(S+T+1)+m+Fintype.card κ+4))
    (fun i _ => shiftedCellWork_le m (Fintype.card κ) (hz e i) hL)
  have ht := Finset.sum_le_sum (s := Finset.univ) (fun e _ => hh e)
  simpa [Nat.mul_assoc] using ht

def trialWeightCacheWork (p m r q B : ℕ) : ℕ :=
  shiftedWeightsCacheWork m (r*(r+1)/2) (trialSignedBits p r q B) (trialShiftBits p r q B+1)

end MatroidSpectral.Execution
