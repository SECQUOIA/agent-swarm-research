import Formal.MatroidSpectral.ExecutionCover
import Mathlib.Data.Nat.Choose.Bounds

/-! Monotonicity used to replace computed ranks and factor counts by original
input dimensions in the final execution bound. -/
namespace MatroidSpectral.Execution
open DAGSpectral DAGSpectral.NormalizationTrials DAGSpectral.CoverNormalizationExecution
open DAGSpectral.BasisInputExecution Elimination

theorem profileCoefficientQueryWork_mono {q Q D E W V : ℕ}
    (hq : q ≤ Q) (hD : D ≤ E) (hW : W ≤ V) (m d B : ℕ) :
    profileCoefficientQueryWork q m d D W B ≤ profileCoefficientQueryWork Q m d E V B := by
  unfold profileCoefficientQueryWork coefficientQueryWork coefficientLoopWork
    interpolationTraceBits interpolationTermBits interpolationWeightBits profileEvaluationBits
    profileEvaluationMatrixBits profileEvaluationWork profileEvaluationStorage
    profileGramExecutionBits profileGramBits profileMonomialBits polynomialDeterminantBits
    determinantBitWork determinantOperandBits iterationBits profileOracleRestrictionWork
  gcongr
  all_goals unfold profileEvaluationMatrixBits profileGramBits profileMonomialBits; gcongr

theorem markedQueryWork_mono {q Q W V : ℕ} (hq : q ≤ Q) (hW : W ≤ V)
    (m d B : ℕ) : markedQueryWork q m d W B ≤ markedQueryWork Q m d V B := by
  unfold markedQueryWork
  apply Nat.add_le_add
  · exact profileCoefficientQueryWork_mono hq (max_le_max (Nat.mul_le_mul hq hW) hq)
      (max_le_max hW le_rfl) _ _ _
  · unfold markerWork
    gcongr

theorem profileWorkBound_mono {q Q W V N T : ℕ} (hq : q ≤ Q) (hW : W ≤ V)
    (hN : N ≤ T) (m d : ℕ) :
    profileWorkBound q m d W N ≤ profileWorkBound Q m d V T := by
  unfold profileWorkBound profileComparisonBound DAGSpectral.ExplicitDAG.keyWorkBound
  dsimp only
  gcongr

theorem normalizationWorkBound_mono {q Q M N : ℕ} (hq : q ≤ Q) (hM : M ≤ N)
    (p m r B : ℕ) :
    normalizationWorkBound p m M r q B ≤ normalizationWorkBound p m N r Q B := by
  unfold normalizationWorkBound basisWorkBound trialStorageBudget labelStorageBudget
    matrixStorageBudget
  dsimp only
  gcongr

theorem trialShift_mono {q Q : ℕ} (hq : q ≤ Q) (p r : ℕ) {η : ℚ} (hη : 0 < η) :
    trialShift p r q η ≤ trialShift p r Q η := by
  rw [trialShift_eq, trialShift_eq]
  apply Nat.ceil_mono
  gcongr

theorem candidateSubsetsWorkBound_mono {M N : ℕ} (hM : M ≤ N) (r : ℕ) :
    candidateSubsetsWorkBound r M ≤ candidateSubsetsWorkBound r N := by
  have hc := Nat.choose_le_choose r hM
  unfold candidateSubsetsWorkBound
  gcongr

theorem candidateCapacity_mono {q Q : ℕ} (hq : q ≤ Q) (p r : ℕ)
    {η : ℚ} (hη : 0 < η) : candidateCapacity q p r η ≤ candidateCapacity Q p r η := by
  have hs := trialShift_mono hq p r hη
  unfold candidateCapacity
  gcongr

theorem candidateWorkBound_mono {q Q M N : ℕ} (hq : q ≤ Q) (hM : M ≤ N)
    (p m r B : ℕ) {η : ℚ} (hη : 0 < η) :
    candidateWorkBound q p m M r B η ≤ candidateWorkBound Q p m N r B η := by
  have hn := normalizationWorkBound_mono hq hM p m r B
  have ht : trialShiftWork p r q B ≤ trialShiftWork p r Q B := by
    unfold trialShiftWork trialShiftBits
    dsimp only
    gcongr
  have hw : trialWeightCacheWork p m r q B ≤ trialWeightCacheWork p m r Q B := by
    unfold trialWeightCacheWork shiftedWeightsCacheWork trialSignedBits trialShiftBits
    dsimp only
    gcongr
  have hs : 2 * trialShift p r q η ≤ 2 * trialShift p r Q η := by
    exact Nat.mul_le_mul_left _ (trialShift_mono hq p r hη)
  have hp := profileWorkBound_mono hq hs (markedQueryWork_mono hq hs m (r*(r+1)/2) B)
    m (r*(r+1)/2)
  unfold candidateWorkBound
  omega

theorem rankWorkBound_mono {q Q M N : ℕ} (hq : q ≤ Q) (hM : M ≤ N)
    (p m r B : ℕ) {η : ℚ} (hη : 0 < η) :
    rankWorkBound q p m M r B η ≤ rankWorkBound Q p m N r B η := by
  have he := candidateSubsetsWorkBound_mono hM r
  have hc := Nat.choose_le_choose r hM
  have ht := candidateWorkBound_mono hq hM p m r B hη
  have hl := candidateCapacity_mono hq p r hη
  unfold rankWorkBound
  gcongr

theorem zeroWorkBound_mono {q Q : ℕ} (hq : q ≤ Q) (p m B : ℕ) :
    zeroWorkBound q p m B ≤ zeroWorkBound Q p m B := by
  have h := profileWorkBound_mono hq (le_refl 0) (markedQueryWork_mono hq (le_refl 0) m 0 B) m 0
  unfold zeroWorkBound
  omega

theorem coverWorkBound_mono {q Q M N : ℕ} (hq : q ≤ Q) (hM : M ≤ N)
    (p m B : ℕ) {η : ℚ} (hη : 0 < η) :
    coverWorkBound q p m M B η ≤ coverWorkBound Q p m N B η := by
  have hz := zeroWorkBound_mono hq p m B
  have hs : (∑ r : Fin p, (rankWorkBound q p m M (r.val+1) B η +
      M.choose (r.val+1) * candidateCapacity q p (r.val+1) η * (columnWork m+1) + 1)) ≤
      ∑ r : Fin p, (rankWorkBound Q p m N (r.val+1) B η +
      N.choose (r.val+1) * candidateCapacity Q p (r.val+1) η * (columnWork m+1) + 1) := by
    apply Finset.sum_le_sum
    intro r _
    have hr := rankWorkBound_mono hq hM p m (r.val+1) B hη
    have hc := Nat.choose_le_choose (r.val+1) hM
    have hl := candidateCapacity_mono hq p (r.val+1) hη
    gcongr
  unfold coverWorkBound
  omega

/-- Polynomial majorants remove digit lengths and maxima from the final
envelope without changing the executed cost observer. -/
def columnWorkPolynomial (m : ℕ) : ℕ := 4*(m+1)*(m+1)

theorem columnWork_le_polynomial (m : ℕ) : columnWork m ≤ columnWorkPolynomial m := by
  have h : Nat.size m ≤ m := Nat.size_le.mpr (Nat.lt_two_pow_self (n := m))
  unfold columnWork columnWorkPolynomial
  gcongr

def profileQueryPolynomial (q m d D W B : ℕ) : ℕ :=
  coefficientQueryWork d D (profileEvaluationBits q m d W (B+1) (D+2))
    (profileEvaluationWork q m d W (B+1) (D+2)) +
      8*(q+1)^2*(m+1)^2*(B+m+1)

theorem profileCoefficientQueryWork_le_polynomial (q m d D W B : ℕ) :
    profileCoefficientQueryWork q m d D W B ≤ profileQueryPolynomial q m d D W B := by
  have h : Nat.size m ≤ m := Nat.size_le.mpr (Nat.lt_two_pow_self (n := m))
  unfold profileCoefficientQueryWork profileQueryPolynomial profileOracleRestrictionWork
  gcongr

def markedQueryPolynomial (q m d W B : ℕ) : ℕ :=
  profileQueryPolynomial q m (d+1) (q*W+q) (W+1) B + markerWork m d W

theorem markedQueryWork_le_polynomial (q m d W B : ℕ) :
    markedQueryWork q m d W B ≤ markedQueryPolynomial q m d W B := by
  unfold markedQueryWork markedQueryPolynomial
  apply Nat.add_le_add_right
  exact (profileCoefficientQueryWork_mono (le_refl q)
    (max_le (by omega) (by omega)) (max_le (by omega) (by omega)) m (d+1) B).trans
      (profileCoefficientQueryWork_le_polynomial q m (d+1) (q*W+q) (W+1) B)

def profileWorkPolynomial (q m d W Q : ℕ) : ℕ :=
  let R := (q*W+1)^d
  R*((m+1)*Q+(m+2)*columnWorkPolynomial m+(d+1)*(q*W+1)) +
    R^2*profileComparisonBound m d W + R*(columnWorkPolynomial m+1)

theorem profileWorkBound_le_polynomial (q m d W Q : ℕ) :
    profileWorkBound q m d W Q ≤ profileWorkPolynomial q m d W Q := by
  have h := columnWork_le_polynomial m
  unfold profileWorkBound profileWorkPolynomial
  dsimp only
  gcongr

def zeroWorkPolynomial (q p m B : ℕ) : ℕ :=
  (m+1)*((2*p*p)*(256*(B+1)^3)+4*p*p)+columnWorkPolynomial m +
    profileWorkPolynomial q m 0 0 (markedQueryPolynomial q m 0 0 B)+1

theorem zeroWorkBound_le_polynomial (q p m B : ℕ) :
    zeroWorkBound q p m B ≤ zeroWorkPolynomial q p m B := by
  have hc := columnWork_le_polynomial m
  have hp := (profileWorkBound_mono (le_refl q) (le_refl 0)
    (markedQueryWork_le_polynomial q m 0 0 B) m 0).trans
      (profileWorkBound_le_polynomial q m 0 0 (markedQueryPolynomial q m 0 0 B))
  unfold zeroWorkBound zeroWorkPolynomial
  omega

def candidateCapacityPolynomial (q p r t : ℕ) : ℕ :=
  (q * (2 * (4*p*r*q*t)) + 1) ^ (r*(r+1)/2)

def candidateWorkPolynomial (q p m M r B t : ℕ) : ℕ :=
  normalizationWorkBound p m M r q B + trialShiftWork p r q B +
    trialWeightCacheWork p m r q B +
    columnWorkPolynomial m + r*(r+1) + 1 +
    profileWorkPolynomial q m (r*(r+1)/2) (2*(4*p*r*q*t))
      (markedQueryPolynomial q m (r*(r+1)/2) (2*(4*p*r*q*t)) B)

def candidateSubsetsPolynomial (r M : ℕ) : ℕ :=
  (M+1)^2 + DAGSpectral.CoverBitCost.enumerationCoefficient r*(M+1)^(r+2)*(M+1) +
    (1+(M+1)^r*((r+1)^2*(2*M+3)+1))

def rankWorkPolynomial (q p m M r B t : ℕ) : ℕ :=
  candidateSubsetsPolynomial r M + (M+1)^r *
    (candidateWorkPolynomial q p m M r B t +
      candidateCapacityPolynomial q p r t*(columnWorkPolynomial m+1)+1)

/-- Every rank sum and exponent depends only on the fixed information
dimension. The tolerance occurs only through the natural parameter `t`. -/
def coverWorkPolynomial (q p m M B t : ℕ) : ℕ :=
  zeroWorkPolynomial q p m B +
    (∑ r : Fin p, (rankWorkPolynomial q p m M (r.val+1) B t +
      (M+1)^(r.val+1)*candidateCapacityPolynomial q p (r.val+1) t*(columnWorkPolynomial m+1)+1)) +
    (p+1)^2+columnWorkPolynomial m+1

theorem choose_le_successor_pow (M r : ℕ) : M.choose r ≤ (M+1)^r :=
  (Nat.choose_le_pow M r).trans (Nat.pow_le_pow_left (Nat.le_succ M) r)

theorem candidateCapacity_le_polynomial (q p r : ℕ) (η : ℚ) :
    candidateCapacity q p r η ≤ candidateCapacityPolynomial q p r ⌈1/η⌉₊ := by
  have h := trialShift_le p r q η
  unfold candidateCapacity candidateCapacityPolynomial
  gcongr

theorem candidateWorkBound_le_polynomial (q p m M r B : ℕ) (η : ℚ) :
    candidateWorkBound q p m M r B η ≤ candidateWorkPolynomial q p m M r B ⌈1/η⌉₊ := by
  have hs := Nat.mul_le_mul_left 2 (trialShift_le p r q η)
  have h := profileWorkBound_mono (le_refl q) hs
    ((markedQueryWork_mono (le_refl q) hs m (r*(r+1)/2) B).trans
      (markedQueryWork_le_polynomial q m (r*(r+1)/2) _ B)) m (r*(r+1)/2)
  have hp := h.trans (profileWorkBound_le_polynomial q m (r*(r+1)/2) _ _)
  have hc := columnWork_le_polynomial m
  unfold candidateWorkBound candidateWorkPolynomial
  omega

theorem candidateSubsetsWorkBound_le_polynomial (r M : ℕ) :
    candidateSubsetsWorkBound r M ≤ candidateSubsetsPolynomial r M := by
  have h := choose_le_successor_pow M r
  unfold candidateSubsetsWorkBound candidateSubsetsPolynomial
  gcongr

theorem rankWorkBound_le_polynomial (q p m M r B : ℕ) (η : ℚ) :
    rankWorkBound q p m M r B η ≤ rankWorkPolynomial q p m M r B ⌈1/η⌉₊ := by
  have hs := candidateSubsetsWorkBound_le_polynomial r M
  have hc := choose_le_successor_pow M r
  have ht := candidateWorkBound_le_polynomial q p m M r B η
  have hl := candidateCapacity_le_polynomial q p r η
  have hw := columnWork_le_polynomial m
  unfold rankWorkBound rankWorkPolynomial
  gcongr

theorem coverWorkBound_le_polynomial (q p m M B : ℕ) (η : ℚ) :
    coverWorkBound q p m M B η ≤ coverWorkPolynomial q p m M B ⌈1/η⌉₊ := by
  have hz := zeroWorkBound_le_polynomial q p m B
  have hw := columnWork_le_polynomial m
  have hs : (∑ r : Fin p, (rankWorkBound q p m M (r.val+1) B η +
      M.choose (r.val+1)*candidateCapacity q p (r.val+1) η*(columnWork m+1)+1)) ≤
      ∑ r : Fin p, (rankWorkPolynomial q p m M (r.val+1) B ⌈1/η⌉₊ +
        (M+1)^(r.val+1)*candidateCapacityPolynomial q p (r.val+1) ⌈1/η⌉₊ *
          (columnWorkPolynomial m+1)+1) := by
    apply Finset.sum_le_sum
    intro r _
    have ht := rankWorkBound_le_polynomial q p m M (r.val+1) B η
    have hc := choose_le_successor_pow M (r.val+1)
    have hl := candidateCapacity_le_polynomial q p (r.val+1) η
    gcongr
  unfold coverWorkBound coverWorkPolynomial
  omega

end MatroidSpectral.Execution
