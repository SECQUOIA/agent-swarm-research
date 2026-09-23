import Formal.MatroidSpectral.RepresentationBitCost
import Formal.MatroidSpectral.NormalizationInputExecution
import Formal.MatroidSpectral.Headline
import Formal.MatroidSpectral.ExecutionCostBounds

/-! Original-input execution: row preprocessing is cached before the PSD factor
cache and cover continuation are evaluated. -/
namespace MatroidSpectral
open Matrix DAGSpectral DAGSpectral.NormalizationTrials DAGSpectral.FactorInputExecution
open ReciprocalAnchor

/-- Store the row-index map and every reduced entry before the cover loop uses
them, so later access does not repeat row sorting or original-input lookup. -/
def cachedRowSubmatrix {a m : ℕ} (A : RationalRepresentation a m)
    (S : Finset (Fin a)) : RationalRepresentation S.card m :=
  let indices := Vector.ofFn (S.orderEmbOfFin rfl)
  let entries := Vector.ofFn fun i : Fin S.card =>
    Vector.ofFn fun j : Fin m => A (indices.get i) j
  fun i j => (entries.get i).get j

theorem cachedRowSubmatrix_eq {a m : ℕ} (A : RationalRepresentation a m)
    (S : Finset (Fin a)) :
    cachedRowSubmatrix A S = A.submatrix (S.orderEmbOfFin rfl) id := by
  ext i j
  simp [cachedRowSubmatrix, Matrix.submatrix]

/-- The continuation receives the reduced representation constructed from the
single executed row scan; dependent row-count transport does no arithmetic. -/
def rowCacheThen {a m : ℕ} {α : Type*} (A : RationalRepresentation a m)
    (next : ∀ {q : ℕ}, RationalRepresentation q m → α × ℕ) : α × ℕ :=
  let rows := rowReductionBitRun A
  let reduced := cachedRowSubmatrix A rows.1
  let result := next reduced
  (result.1, rows.2 + result.2)

theorem rowCacheThen_value {a m : ℕ} {α : Type*} (A : RationalRepresentation a m)
    (next : ∀ {q : ℕ}, RationalRepresentation q m → α × ℕ) :
    (rowCacheThen A next).1 = (next (rowReductionRepresentation A)).1 := by
  simp only [rowCacheThen, cachedRowSubmatrix_eq]
  rfl

theorem rowCacheThen_work {a m K W : ℕ} {α : Type*} (A : RationalRepresentation a m)
    (hA : MatrixBits A K) (next : ∀ {q : ℕ}, RationalRepresentation q m → α × ℕ)
    (hnext : ∀ {q : ℕ} (R : RationalRepresentation q m),
      q ≤ a → MatrixBits R K → (next R).2 ≤ W) :
    (rowCacheThen A next).2 ≤ rowReductionBitWork a m K + W := by
  have hq : (rowReductionRun A (List.finRange a)).selected.card ≤ a := by
    simpa using Finset.card_le_univ (rowReductionRun A (List.finRange a)).selected
  simp only [rowCacheThen, cachedRowSubmatrix_eq]
  exact Nat.add_le_add (rowReductionBitRun_work_le hA)
    (hnext (rowReductionRepresentation A) hq (rowReductionRepresentation_bits hA))

def representedInputRun {a m p : ℕ} (A : RationalRepresentation a m)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (inputBits etaBits : ℕ) : List (Finset (Fin m)) × ℕ :=
  rowCacheThen A (fun R => factorCacheThen Q0 Q hQ0 hQ inputBits
    (fun D => Execution.coverRun R D η (normalizationInputWidth p a inputBits etaBits)))

theorem representedInputRun_value {a m p : ℕ} (A : RationalRepresentation a m)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (inputBits etaBits : ℕ) :
    (representedInputRun A Q0 Q hQ0 hQ η inputBits etaBits).1.toFinset =
      representedSpectralCover A Q0 Q hQ0 hQ η := by
  simp only [representedInputRun, rowCacheThen_value]
  rw [factorCacheThen_value Q0 Q hQ0 hQ inputBits _ (by
    intro M N h D
    rw [Execution.coverRun_cast])]
  exact Execution.coverRun_value _ _ _ _

def representedInputWorkBound (a m p inputBits etaBits : ℕ) (η : ℚ) : ℕ :=
  rowReductionBitWork a m inputBits +
    (inputCoefficient p*(m+2)^2*(inputBits+1)^3 +
      Execution.coverWorkBound a p m (p*(m+1))
        (normalizationInputWidth p a inputBits etaBits) η)

/-- Every runtime component is bounded here from original input encodings;
the theorem has no assumed oracle or continuation-cost premise. -/
theorem representedInputRun_work {a m p inputBits etaBits : ℕ}
    (A : RationalRepresentation a m)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (hA : MatrixBits A inputBits) (h0 : MatrixBits Q0 inputBits)
    (he : ∀ e, MatrixBits (Q e) inputBits)
    {η : ℚ} (hηB : RationalBits η etaBits) (hη : 0 < η) :
    (representedInputRun A Q0 Q hQ0 hQ η inputBits etaBits).2 ≤
      representedInputWorkBound a m p inputBits etaBits η := by
  unfold representedInputRun representedInputWorkBound
  apply rowCacheThen_work A hA
  intro q R hq hR
  apply factorCacheThen_work Q0 Q hQ0 hQ h0 he hηB a
  intro M D hM hV hw hD
  let B := normalizationInputWidth p a inputBits etaBits
  have hi : inputBits ≤ B := by
    have := factorBits_input p inputBits
    dsimp [B, normalizationInputWidth]
    omega
  have hr : MatrixBits R B := fun i j => rationalBits_mono (hR i j) hi
  have hη' : RationalBits η B := rationalBits_mono hηB (by
    dsimp [B, normalizationInputWidth]; omega)
  have hsize : p + q + 2 ≤ B := by dsimp [B, normalizationInputWidth]; omega
  exact (Execution.coverRun_work R D hη hr hV hw hD hη' hsize).trans
    (Execution.coverWorkBound_mono hq hM p m B hη)

theorem representedInputRun_isRelativeCover {a m p : ℕ} (A : RationalRepresentation a m)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    {η : ℚ} (hη : 0 < η) (inputBits etaBits : ℕ) :
    IsRelativeCover (η : ℝ) (fun B => ratMatrixReal (Q0 + ∑ e ∈ B, Q e))
      (columnBases A) (representedInputRun A Q0 Q hQ0 hQ η inputBits etaBits).1.toFinset := by
  rw [representedInputRun_value]
  exact representedSpectralCover_isRelativeCover A Q0 Q hQ0 hQ hη

/-- An explicit polynomial envelope in the original input dimensions, entry
widths, tolerance width, and `t`. The finite rank sum and all variable exponents
in `coverWorkPolynomial` depend only on the fixed information dimension `p`. -/
def representedInputPolynomialBound (a m p inputBits etaBits t : ℕ) : ℕ :=
  rowReductionBitWork a m inputBits +
    (inputCoefficient p*(m+2)^2*(inputBits+1)^3 +
      Execution.coverWorkPolynomial a p m (p*(m+1))
        (normalizationInputWidth p a inputBits etaBits) t)

/-- The actual original-input execution has polynomial charged bit work at
fixed information dimension. There is no assumed profile oracle or continuation
bound: every component is discharged by the preceding execution theorems. -/
theorem representedInputRun_polynomial_work {a m p inputBits etaBits : ℕ}
    (A : RationalRepresentation a m)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (hA : MatrixBits A inputBits) (h0 : MatrixBits Q0 inputBits)
    (he : ∀ e, MatrixBits (Q e) inputBits)
    {η : ℚ} (hηB : RationalBits η etaBits) (hη : 0 < η) :
    (representedInputRun A Q0 Q hQ0 hQ η inputBits etaBits).2 ≤
      representedInputPolynomialBound a m p inputBits etaBits ⌈1/η⌉₊ := by
  apply (representedInputRun_work A Q0 Q hQ0 hQ hA h0 he hηB hη).trans
  unfold representedInputWorkBound representedInputPolynomialBound
  exact Nat.add_le_add_left (Nat.add_le_add_left
    (Execution.coverWorkBound_le_polynomial a p m (p*(m+1))
      (normalizationInputWidth p a inputBits etaBits) η) _) _

end MatroidSpectral
