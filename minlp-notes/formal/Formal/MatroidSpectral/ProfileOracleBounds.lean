import Formal.MatroidSpectral.ProfileOracleEvaluation

namespace MatroidSpectral

theorem profileEvaluationBits_mono {q q' m m' d d' W W' B B' N N' : ℕ}
    (hq : q ≤ q') (hm : m ≤ m') (hd : d ≤ d') (hW : W ≤ W')
    (hB : B ≤ B') (hN : N ≤ N') :
    profileEvaluationBits q m d W B N ≤ profileEvaluationBits q' m' d' W' B' N' := by
  unfold profileEvaluationBits polynomialDeterminantBits profileEvaluationMatrixBits
    profileGramBits profileMonomialBits
  gcongr

theorem profileEvaluationWork_mono {q q' m m' d d' W W' B B' N N' : ℕ}
    (hq : q ≤ q') (hm : m ≤ m') (hd : d ≤ d') (hW : W ≤ W')
    (hB : B ≤ B') (hN : N ≤ N') :
    profileEvaluationWork q m d W B N ≤ profileEvaluationWork q' m' d' W' B' N' := by
  have hG : profileEvaluationMatrixBits m d W B N ≤
      profileEvaluationMatrixBits m' d' W' B' N' := by
    unfold profileEvaluationMatrixBits profileGramBits profileMonomialBits
    gcongr
  have hdet := Elimination.determinantBitWork_mono hq hG
  unfold profileEvaluationWork profileEvaluationStorage profileGramExecutionBits
    profileGramBits profileMonomialBits
  gcongr

theorem interpolationTraceBits_mono {d d' D D' B B' : ℕ}
    (hd : d ≤ d') (hD : D ≤ D') (hB : B ≤ B') :
    interpolationTraceBits d D B ≤ interpolationTraceBits d' D' B' := by
  unfold interpolationTraceBits interpolationTermBits interpolationWeightBits
  gcongr
  omega

theorem coefficientQueryWork_mono {d d' D D' B B' E E' : ℕ}
    (hd : d ≤ d') (hD : D ≤ D') (hB : B ≤ B') (hE : E ≤ E') :
    coefficientQueryWork d D B E ≤ coefficientQueryWork d' D' B' E' := by
  have ht := interpolationTraceBits_mono hd hD hB
  unfold coefficientQueryWork coefficientLoopWork
  gcongr <;> omega

theorem profileCoefficientQueryWork_mono {q q' m m' d d' D D' W W' B B' : ℕ}
    (hq : q ≤ q') (hm : m ≤ m') (hd : d ≤ d') (hD : D ≤ D')
    (hW : W ≤ W') (hB : B ≤ B') :
    profileCoefficientQueryWork q m d D W B ≤
      profileCoefficientQueryWork q' m' d' D' W' B' := by
  have hbits := profileEvaluationBits_mono hq hm hd hW
    (Nat.add_le_add_right hB 1) (Nat.add_le_add_right hD 2)
  have hwork := profileEvaluationWork_mono hq hm hd hW
    (Nat.add_le_add_right hB 1) (Nat.add_le_add_right hD 2)
  have hquery := coefficientQueryWork_mono hd hD hbits hwork
  have hsize := Nat.size_le_size hm
  unfold profileCoefficientQueryWork profileOracleRestrictionWork
  gcongr

end MatroidSpectral
