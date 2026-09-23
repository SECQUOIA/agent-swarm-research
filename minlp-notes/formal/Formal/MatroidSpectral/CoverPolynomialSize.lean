import Formal.MatroidSpectral.Headline
import Mathlib.Data.Nat.Choose.Bounds

/-! An explicit polynomial bound on the number of returned bases, in the
original ground-set size and inverse tolerance at fixed information dimension. -/
namespace MatroidSpectral
open Matrix DAGSpectral
open scoped BigOperators

lemma trialCeil_le (p r q : ℕ) (η : ℚ) :
    ⌈4*(p : ℚ)*r*q/η⌉₊ ≤ 4*p*r*q*⌈1/η⌉₊ := by
  apply Nat.ceil_le.mpr
  have hh := mul_le_mul_of_nonneg_left (Nat.le_ceil (1/η))
    (show 0 ≤ 4*(p : ℚ)*r*q by positivity)
  convert hh using 1 <;> push_cast <;> ring

/-- The sum indexed by information rank is bounded uniformly without fixing
matroid rank or the number of factor labels. -/
theorem matroidCoverCardinality_polynomial (p M q : ℕ) (η : ℚ) :
    matroidCoverCardinality p M q η ≤
      1+p*(M+1)^p*(8*p^2*q^2*⌈1/η⌉₊+1)^(p*(p+1)/2) := by
  unfold matroidCoverCardinality
  have hrank (r : Fin p) : r.val+1 ≤ p := by omega
  have hterm (r : Fin p) :
      M.choose (r.val+1)*
        (2*q*⌈4*(p : ℚ)*(r.val+1)*q/η⌉₊+1)^((r.val+1)*(r.val+2)/2) ≤
      (M+1)^p*(8*p^2*q^2*⌈1/η⌉₊+1)^(p*(p+1)/2) := by
    have hchoose : M.choose (r.val+1) ≤ (M+1)^p := by
      calc
        _ ≤ M^(r.val+1) := Nat.choose_le_pow _ _
        _ ≤ (M+1)^(r.val+1) := Nat.pow_le_pow_left (by omega) _
        _ ≤ (M+1)^p := Nat.pow_le_pow_right (by omega) (hrank r)
    have hceil : ⌈4*(p : ℚ)*(r.val+1)*q/η⌉₊ ≤ 4*p*p*q*⌈1/η⌉₊ := by
      have hh := trialCeil_le p (r.val+1) q η
      push_cast at hh
      exact hh.trans (by gcongr; exact hrank r)
    have hbase : 2*q*⌈4*(p : ℚ)*(r.val+1)*q/η⌉₊+1 ≤
        8*p^2*q^2*⌈1/η⌉₊+1 := by
      calc
        _ ≤ 2*q*(4*p*p*q*⌈1/η⌉₊)+1 := by gcongr
        _ = _ := by ring
    have hexp : (r.val+1)*(r.val+2)/2 ≤ p*(p+1)/2 := by
      apply Nat.div_le_div_right
      have := hrank r
      nlinarith
    exact Nat.mul_le_mul hchoose ((Nat.pow_le_pow_left hbase _).trans
      (Nat.pow_le_pow_right (by omega) hexp))
  have hh := Finset.sum_le_sum (s := Finset.univ) (fun r _ => hterm r)
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at hh
  nlinarith

/-- Original-input cardinality, with the factor count eliminated. -/
theorem representedSpectralCover_card_polynomial {a m p : ℕ} (A : RationalRepresentation a m)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    {η : ℚ} (hη : 0 < η) :
    (representedSpectralCover A Q0 Q hQ0 hQ η).card ≤
      1+p*(p*(m+1)+1)^p*(8*p^2*A.rank^2*⌈1/η⌉₊+1)^(p*(p+1)/2) := by
  apply (representedSpectralCover_card A Q0 Q hQ0 hQ hη).trans
  apply (matroidCoverCardinality_polynomial p
    (indexedFactorCount (priorAtomMatrices Q0 Q)) A.rank η).trans
  have hm := indexedFactorCount_le (priorAtomMatrices Q0 Q)
  gcongr

/-- A bound using only information dimension, ground-set size, and tolerance. -/
theorem representedSpectralCover_card_ground_polynomial {a m p : ℕ}
    (A : RationalRepresentation a m)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    {η : ℚ} (hη : 0 < η) :
    (representedSpectralCover A Q0 Q hQ0 hQ η).card ≤
      1+p*(p*(m+1)+1)^p*(8*p^2*m^2*⌈1/η⌉₊+1)^(p*(p+1)/2) := by
  apply (representedSpectralCover_card_polynomial A Q0 Q hQ0 hQ hη).trans
  have hr := Matrix.rank_le_width A
  gcongr

end MatroidSpectral
