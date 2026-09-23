import Formal.DAGSpectral.FactorInputData
import Formal.DAGSpectral.CoverPolynomialCost
import Formal.DAGSpectral.Headline

namespace DAGSpectral
open Matrix ReciprocalAnchor NormalizationTrials FactorInputExecution
open NormalizationBits CoverNormalizationExecution
namespace CoverBitCost

/-- A common width budget derived from input encodings and explicit graph size. -/
def inputWidth (p v inputBits etaBits : ℕ) : ℕ :=
  factorBits p inputBits + etaBits + p + max 1 (v-1) + 3

/-- The original-input implementation executes LDL once per atom and captures
the resulting cache. All subsequent factor reads use its stored labels, and
the trial enumerator receives the cache's actual length. -/
def coverInputRun {v m p : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (inputBits etaBits : ℕ) : List (List (Fin m)) × ℕ :=
  let cache := inputRun (priorAtomMatrices Q0 Q)
  let D := cachedFactorData Q0 Q hQ0 hQ cache rfl
  let B := inputWidth p v inputBits etaBits
  let result := coverBitRun G s t D η B
    (fun r => atomBudget p r B (6*B+1) B)
    (fun r => transformBudget p r B (6*B+1) B)
    (fun r => B+r+max 1 (v-1)+2)
  (result.1,traceBitWork (factorBits p inputBits) cache.events+cache.copies+result.2)

theorem coverBitRun_cast {v m p M N : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (h : M = N) (η : ℚ) (B : ℕ) (K F C : ℕ → ℕ) :
    coverBitRun G s t (castFactorData h D) η B K F C =
      coverBitRun G s t D η B K F C := by
  subst N
  rfl

theorem coverInputRun_list {v m p : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (inputBits etaBits : ℕ) :
    let B := inputWidth p v inputBits etaBits
    (coverInputRun G s t Q0 Q hQ0 hQ η inputBits etaBits).1 =
      (coverBitRun G s t (producedData Q0 Q hQ0 hQ) η B
        (fun r => atomBudget p r B (6*B+1) B)
        (fun r => transformBudget p r B (6*B+1) B)
        (fun r => B+r+max 1 (v-1)+2)).1 := by
  simp only [coverInputRun,cachedFactorData_eq,coverBitRun_cast]

theorem coverInputRun_paths {v m p : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (inputBits etaBits : ℕ) :
    (coverInputRun G s t Q0 Q hQ0 hQ η inputBits etaBits).1.toFinset =
      dagSpectralCover G s t Q0 Q hQ0 hQ η := by
  simp only [coverInputRun,cachedFactorData_eq,coverBitRun_cast,coverBitRun_paths,
    dagSpectralCover]

theorem coverInputRun_isRelativeCover {v m p : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (hη : 0 < η) (inputBits etaBits : ℕ) :
    IsRelativeCover (η : ℝ) (pathMatrix (ratMatrixReal Q0) (fun e => ratMatrixReal (Q e)))
      (feasiblePaths G s t)
      (coverInputRun G s t Q0 Q hQ0 hQ η inputBits etaBits).1.toFinset := by
  rw [coverInputRun_paths]
  exact dagSpectralCover_isRelativeCover G s t Q0 Q hQ0 hQ η hη

theorem coverInputRun_work {v m p inputBits etaBits : ℕ}
    (G : ExplicitDAG v m) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (h0 : MatrixBits Q0 inputBits) (he : ∀ e, MatrixBits (Q e) inputBits)
    {η : ℚ} (hηB : RationalBits η etaBits) (hη : 0 < η) :
    (coverInputRun G s t Q0 Q hQ0 hQ η inputBits etaBits).2 ≤
      inputCoefficient p*(m+2)^2*(inputBits+1)^3 +
        coverWorkBound v m p (indexedFactorCount (priorAtomMatrices Q0 Q))
          (inputWidth p v inputBits etaBits) η := by
  let cache := inputRun (priorAtomMatrices Q0 Q)
  let D := cachedFactorData Q0 Q hQ0 hQ cache rfl
  let B := inputWidth p v inputBits etaBits
  have hFB : factorBits p inputBits ≤ B := by dsimp [B,inputWidth]; omega
  have hIB : inputBits ≤ B := (factorBits_input p inputBits).trans hFB
  have hDB (k : Fin cache.factors.length) := cachedFactorData_bits Q0 Q hQ0 hQ cache rfl h0 he k
  have hV : ∀ k i, RationalBits (D.vector k i) B :=
    fun k i => rationalBits_mono ((hDB k).2 i) hFB
  have hw : ∀ k, RationalBits (D.weight k) B :=
    fun k => rationalBits_mono (hDB k).1 hFB
  have hA : ∀ o, MatrixBits (D.atom o) B := by
    intro o
    cases o with
    | none => exact fun i j => rationalBits_mono (h0 i j) hIB
    | some e => exact fun i j => rationalBits_mono (he e i j) hIB
  have hr := coverBitRun_polynomial_work G s t D hV hw hA
    (rationalBits_mono hηB (by dsimp [B,inputWidth]; omega)) hη
    (by dsimp [B,inputWidth]; omega)
  have hi := inputBitWork_polynomial (priorAtomMatrices Q0 Q) (Fin.cases h0 he)
  have hsum := Nat.add_le_add hi hr
  simpa only [coverInputRun,cache,D,B,inputBitWork,InputRun.bitWork,
    inputRun_count,Nat.add_assoc] using hsum

theorem coverWorkBound_mono_labels {M L : ℕ} (h : M ≤ L)
    (v m p B : ℕ) (η : ℚ) :
    coverWorkBound v m p M B η ≤ coverWorkBound v m p L B η := by
  have hs : allCandidateWorkBound v m p M B η ≤ allCandidateWorkBound v m p L B η := by
    unfold allCandidateWorkBound
    apply Finset.sum_le_sum
    intro r _
    unfold candidateWorkBound trialWorkBound BasisInputExecution.basisWorkBound
    dsimp only
    gcongr
  unfold coverWorkBound coverLoopBound rankLoopBound
  dsimp only
  gcongr

/-- An explicit bound involving only the original input sizes. Its finite rank
sums and every exponent depend only on fixed dimension `p`. The accuracy
parameter enters through `ceil(1/eta)`, and the path-length bound is at most
`v+1`, so the expression is polynomially bounded in these input parameters. -/
noncomputable def originalInputWorkBound (v m p inputBits etaBits : ℕ) (η : ℚ) : ℕ :=
  inputCoefficient p*(m+2)^2*(inputBits+1)^3 +
    coverWorkBound v m p (p*(m+1)) (inputWidth p v inputBits etaBits) η

theorem coverInputRun_polynomial_work {v m p inputBits etaBits : ℕ}
    (G : ExplicitDAG v m) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (h0 : MatrixBits Q0 inputBits) (he : ∀ e, MatrixBits (Q e) inputBits)
    {η : ℚ} (hηB : RationalBits η etaBits) (hη : 0 < η) :
    (coverInputRun G s t Q0 Q hQ0 hQ η inputBits etaBits).2 ≤
      originalInputWorkBound v m p inputBits etaBits η := by
  apply (coverInputRun_work G s t Q0 Q hQ0 hQ h0 he hηB hη).trans
  exact Nat.add_le_add_left
    (coverWorkBound_mono_labels (indexedPriorAtomCount_le Q0 Q) _ _ _ _ _) _

end CoverBitCost
end DAGSpectral
