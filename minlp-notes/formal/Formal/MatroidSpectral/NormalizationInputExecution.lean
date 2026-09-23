import Formal.MatroidSpectral.NormalizationEnumeration
import Formal.DAGSpectral.FactorInputData

/-! Original rational-input factorization is executed once and its cache is
passed to the actual continuation. The continuation supplies the remaining
algorithm, rather than receiving an assumed factorization oracle. -/
namespace MatroidSpectral
open Matrix DAGSpectral DAGSpectral.NormalizationTrials DAGSpectral.FactorInputExecution
open ReciprocalAnchor

def normalizationInputWidth (p q inputBits etaBits : ℕ) : ℕ :=
  factorBits p inputBits + etaBits + p + q + 3

def factorCacheThen {p m : ℕ} {α : Type*}
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (inputBits : ℕ) (next : ∀ {M : ℕ}, FactorData p m M → α × ℕ) : α × ℕ :=
  let cache := inputRun (priorAtomMatrices Q0 Q)
  let D := cachedFactorData Q0 Q hQ0 hQ cache rfl
  let result := next D
  (result.1,traceBitWork (factorBits p inputBits) cache.events+cache.copies+result.2)

/-- Relabelling a dependent length is erased; this value theorem uses only
that invariance of the actual continuation. -/
theorem factorCacheThen_value {p m : ℕ} {α : Type*}
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (inputBits : ℕ) (next : ∀ {M : ℕ}, FactorData p m M → α × ℕ)
    (hcast : ∀ {M N : ℕ} (h : M = N) (D : FactorData p m M),
      (next (castFactorData h D)).1 = (next D).1) :
    (factorCacheThen Q0 Q hQ0 hQ inputBits next).1 =
      (next (producedData Q0 Q hQ0 hQ)).1 := by
  simp only [factorCacheThen,cachedFactorData_eq,hcast]

theorem cachedFactorData_input_bounds {p m inputBits etaBits : ℕ}
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (h0 : MatrixBits Q0 inputBits) (he : ∀ e, MatrixBits (Q e) inputBits)
    {η : ℚ} (hη : RationalBits η etaBits) (q : ℕ) :
    let cache := inputRun (priorAtomMatrices Q0 Q)
    let D := cachedFactorData Q0 Q hQ0 hQ cache rfl
    let B := normalizationInputWidth p q inputBits etaBits
    cache.factors.length ≤ p * (m + 1) ∧
      (∀ j i, RationalBits (D.vector j i) B) ∧
      (∀ j, RationalBits (D.weight j) B) ∧
      (∀ o, MatrixBits (D.atom o) B) ∧ RationalBits η B ∧ p+q+2 ≤ B := by
  dsimp only
  let B := normalizationInputWidth p q inputBits etaBits
  have hf : factorBits p inputBits ≤ B := by dsimp [B,normalizationInputWidth]; omega
  have hi : inputBits ≤ B := (factorBits_input p inputBits).trans hf
  refine ⟨?_,?_,?_,?_,?_,?_⟩
  · rw [inputRun_count]
    exact indexedPriorAtomCount_le Q0 Q
  · intro j i
    exact rationalBits_mono ((cachedFactorData_bits Q0 Q hQ0 hQ _ rfl h0 he j).2 i) hf
  · intro j
    exact rationalBits_mono (cachedFactorData_bits Q0 Q hQ0 hQ _ rfl h0 he j).1 hf
  · intro o
    cases o with
    | none => exact fun i j => rationalBits_mono (h0 i j) hi
    | some e => exact fun i j => rationalBits_mono (he e i j) hi
  · exact rationalBits_mono hη (by dsimp [normalizationInputWidth]; omega)
  · dsimp [normalizationInputWidth]
    omega

/-- Original-input accounting composes with a proved bound on the executed
continuation. Its hypotheses include the actual cached coordinates and labels. -/
theorem factorCacheThen_work {p m inputBits etaBits W : ℕ} {α : Type*}
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (h0 : MatrixBits Q0 inputBits) (he : ∀ e, MatrixBits (Q e) inputBits)
    {η : ℚ} (hη : RationalBits η etaBits) (q : ℕ)
    (next : ∀ {M : ℕ}, FactorData p m M → α × ℕ)
    (hnext : ∀ {M : ℕ} (D : FactorData p m M),
      M ≤ p * (m + 1) →
      (∀ j i, RationalBits (D.vector j i) (normalizationInputWidth p q inputBits etaBits)) →
      (∀ j, RationalBits (D.weight j) (normalizationInputWidth p q inputBits etaBits)) →
      (∀ o, MatrixBits (D.atom o) (normalizationInputWidth p q inputBits etaBits)) →
      (next D).2 ≤ W) :
    (factorCacheThen Q0 Q hQ0 hQ inputBits next).2 ≤
      inputCoefficient p*(m+2)^2*(inputBits+1)^3 + W := by
  obtain ⟨hM,hV,hw,hA,_⟩ := cachedFactorData_input_bounds Q0 Q hQ0 hQ h0 he hη q
  have hn := hnext (cachedFactorData Q0 Q hQ0 hQ _ rfl) hM hV hw hA
  have hf := inputBitWork_polynomial (priorAtomMatrices Q0 Q) (Fin.cases h0 he)
  have hh := Nat.add_le_add hf hn
  simpa only [factorCacheThen,inputBitWork,InputRun.bitWork] using hh

end MatroidSpectral
