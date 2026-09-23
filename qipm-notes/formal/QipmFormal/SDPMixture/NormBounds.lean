import QipmFormal.SDPMixture.Frobenius

/-! # Operator norm bounds for SDP mixture defects

All operator norms in this file are induced by the Euclidean norm. The
entrywise maximum norm on matrices is deliberately not used.
-/
namespace QipmFormal.SDPMixture

open Matrix
open scoped MatrixOrder Matrix.Norms.L2Operator

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The operator norm induced by the Euclidean vector norm. -/
noncomputable def opNorm (A : Matrix n n ℝ) : ℝ := ‖A‖

lemma opNorm_nonneg (A : Matrix n n ℝ) : 0 ≤ opNorm A := norm_nonneg A

/-- A symmetric matrix between `-k I` and `k I` has operator norm at most `k`. -/
theorem opNorm_le_of_order_bounds {A : Matrix n n ℝ} {k : ℝ}
    (hA : A.IsHermitian) (hk : 0 ≤ k)
    (hlo : (-k) • (1 : Matrix n n ℝ) ≤ A)
    (hhi : A ≤ k • (1 : Matrix n n ℝ)) : opNorm A ≤ k := by
  have hsa : IsSelfAdjoint A := hA.isSelfAdjoint
  have hl : ∀ x ∈ spectrum ℝ A, -k ≤ x := by
    apply (algebraMap_le_iff_le_spectrum hsa).mp
    simpa only [Algebra.algebraMap_eq_smul_one] using hlo
  have hu : ∀ x ∈ spectrum ℝ A, x ≤ k := by
    apply (le_algebraMap_iff_spectrum_le hsa).mp
    simpa only [Algebra.algebraMap_eq_smul_one] using hhi
  have hh : ‖cfc (fun x : ℝ => x) A‖ ≤ k := norm_cfc_le hk fun x hx => by
    simpa only [Real.norm_eq_abs, abs_le] using And.intro (hl x hx) (hu x hx)
  simpa only [opNorm, cfc_id' ℝ A hsa] using hh

/-- A positive semidefinite defect bounded by `k I` has operator width at most `k`. -/
theorem opNorm_le_of_nonneg_le {A : Matrix n n ℝ} {k : ℝ}
    (hA : 0 ≤ A) (hk : 0 ≤ k) (hhi : A ≤ k • (1 : Matrix n n ℝ)) :
    opNorm A ≤ k := by
  apply opNorm_le_of_order_bounds hA.posSemidef.isHermitian hk _ hhi
  exact (smul_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr hk) zero_le_one).trans hA

/-- Every symmetric matrix lies below its operator norm times the identity. -/
theorem le_opNorm_smul_one [Nonempty n] {A : Matrix n n ℝ} (hA : A.IsHermitian) :
    A ≤ opNorm A • (1 : Matrix n n ℝ) := by
  rw [← Algebra.algebraMap_eq_smul_one]
  apply (le_algebraMap_iff_spectrum_le hA.isSelfAdjoint).mpr
  intro x hx
  exact (Real.le_norm_self x).trans (spectrum.norm_le_norm_of_mem hx)

/-- The average diagonal entry lies in the same scalar bounds as the matrix. -/
theorem trace_average_bounds [Nonempty n] {A : Matrix n n ℝ} {k : ℝ}
    (hA : 0 ≤ A) (hhi : A ≤ k • (1 : Matrix n n ℝ)) :
    0 ≤ A.trace / Fintype.card n ∧ A.trace / Fintype.card n ≤ k := by
  have hn : (0 : ℝ) < Fintype.card n := by exact_mod_cast Fintype.card_pos
  refine ⟨div_nonneg hA.posSemidef.trace_nonneg hn.le, ?_⟩
  have ht := (Matrix.le_iff.mp hhi).trace_nonneg
  rw [Matrix.trace_sub, Matrix.trace_smul, Matrix.trace_one, smul_eq_mul] at ht
  exact (div_le_iff₀ hn).mpr (by linarith)

/-- Subtracting any scalar in `[0,k]` from a PSD matrix below `k I` leaves
operator norm at most `k`. -/
theorem opNorm_sub_scalar_le {A : Matrix n n ℝ} {k t : ℝ}
    (hA : 0 ≤ A) (hk : 0 ≤ k) (hhi : A ≤ k • (1 : Matrix n n ℝ))
    (ht0 : 0 ≤ t) (htk : t ≤ k) :
    opNorm (A - t • (1 : Matrix n n ℝ)) ≤ k := by
  have ht : (t • (1 : Matrix n n ℝ)).IsHermitian :=
    isHermitian_one.smul (show IsSelfAdjoint t from isSelfAdjoint_iff.mpr (by simp))
  apply opNorm_le_of_order_bounds (hA.posSemidef.isHermitian.sub ht) hk
  · have htk' : t • (1 : Matrix n n ℝ) ≤ k • (1 : Matrix n n ℝ) :=
      smul_le_smul_of_nonneg_right htk zero_le_one
    have h := neg_le_neg htk'
    simpa only [neg_smul] using h.trans
      (by simpa only [zero_sub] using sub_le_sub_right hA (t • (1 : Matrix n n ℝ)))
  · exact (sub_le_self A (smul_nonneg ht0 zero_le_one)).trans hhi

/-- Point-centering never increases the operator width of a PSD defect. -/
theorem opNorm_recentered_le [Nonempty n] {D : Matrix n n ℝ} (hD : 0 ≤ D) :
    opNorm ((1 + D.trace / Fintype.card n)⁻¹ •
      (D - (D.trace / Fintype.card n) • (1 : Matrix n n ℝ))) ≤ opNorm D := by
  have hb := trace_average_bounds hD (le_opNorm_smul_one hD.posSemidef.isHermitian)
  have hd := opNorm_sub_scalar_le hD (opNorm_nonneg D)
    (le_opNorm_smul_one hD.posSemidef.isHermitian) hb.1 hb.2
  have hi : 0 ≤ (1 + D.trace / Fintype.card n)⁻¹ := inv_nonneg.mpr (by linarith [hb.1])
  have hi1 : (1 + D.trace / Fintype.card n)⁻¹ ≤ 1 :=
    inv_le_one_of_one_le₀ (by linarith [hb.1])
  change ‖(1 + D.trace / Fintype.card n)⁻¹ •
    (D - (D.trace / Fintype.card n) • (1 : Matrix n n ℝ))‖ ≤ _
  rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg hi]
  exact (mul_le_mul_of_nonneg_left hd hi).trans
    (by simpa only [one_mul] using mul_le_mul_of_nonneg_right hi1 (opNorm_nonneg D))

/-- A central sandwich gives the common-parameter operator width. -/
theorem opNorm_defect_le {Z : Matrix n n ℝ} {K : ℝ}
    (hlo : (1 : Matrix n n ℝ) ≤ Z) (hhi : Z ≤ K • (1 : Matrix n n ℝ))
    (hK : 1 ≤ K) : opNorm (Z - 1) ≤ K - 1 := by
  apply opNorm_le_of_nonneg_le (sub_nonneg.mpr hlo) (sub_nonneg.mpr hK)
  simpa only [sub_smul, one_smul] using sub_le_sub_right hhi (1 : Matrix n n ℝ)

/-- The Frobenius neighborhood associated with an operator-width certificate. -/
theorem frobeniusNorm_le_of_opNorm_le {A : Matrix n n ℝ} {k : ℝ}
    (h : opNorm A ≤ k) : frobeniusNorm A ≤ Real.sqrt (Fintype.card n) * k :=
  (frobeniusNorm_le_sqrt_card_mul_opNorm A).trans
    (mul_le_mul_of_nonneg_left h (Real.sqrt_nonneg _))

/-- Both centering conventions satisfy the operator bound of the central sandwich. -/
theorem opNorm_defect_and_recentered_le [Nonempty n] {Z : Matrix n n ℝ} {K : ℝ}
    (hlo : (1 : Matrix n n ℝ) ≤ Z) (hhi : Z ≤ K • (1 : Matrix n n ℝ))
    (hK : 1 ≤ K) :
    opNorm (Z - 1) ≤ K - 1 ∧
      opNorm ((1 + (Z - 1).trace / Fintype.card n)⁻¹ •
        ((Z - 1) - ((Z - 1).trace / Fintype.card n) • (1 : Matrix n n ℝ))) ≤ K - 1 := by
  have h := opNorm_defect_le hlo hhi hK
  exact ⟨h, (opNorm_recentered_le (sub_nonneg.mpr hlo)).trans h⟩

/-- Both centering conventions satisfy the Frobenius bound with factor `sqrt r`. -/
theorem frobeniusNorm_defect_and_recentered_le {Z : Matrix n n ℝ} {K : ℝ}
    (hlo : (1 : Matrix n n ℝ) ≤ Z) (hhi : Z ≤ K • (1 : Matrix n n ℝ))
    (hK : 1 ≤ K) :
    frobeniusNorm (Z - 1) ≤ Real.sqrt (Fintype.card n) * (K - 1) ∧
      frobeniusNorm ((1 + (Z - 1).trace / Fintype.card n)⁻¹ •
        ((Z - 1) - ((Z - 1).trace / Fintype.card n) • (1 : Matrix n n ℝ))) ≤
          Real.sqrt (Fintype.card n) * (K - 1) := by
  have h := frobeniusNorm_le_of_opNorm_le (opNorm_defect_le hlo hhi hK)
  exact ⟨h, (frobeniusNorm_recentered_le _ (sub_nonneg.mpr hlo).posSemidef).trans h⟩

/-- Trace normalization of `Z` agrees exactly with recentering its PSD defect. -/
theorem normalized_defect_eq_recentered [Nonempty n] {Z : Matrix n n ℝ}
    (hZ : (1 : Matrix n n ℝ) ≤ Z) :
    (Z.trace / Fintype.card n)⁻¹ • Z - 1 =
      (1 + (Z - 1).trace / Fintype.card n)⁻¹ •
        ((Z - 1) - ((Z - 1).trace / Fintype.card n) • (1 : Matrix n n ℝ)) := by
  have hn : (Fintype.card n : ℝ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  let t := (Z - 1).trace / (Fintype.card n : ℝ)
  have ht : 0 ≤ t := div_nonneg (sub_nonneg.mpr hZ).posSemidef.trace_nonneg
    (Nat.cast_nonneg _)
  have htrace : Z.trace / Fintype.card n = 1 + t := by
    dsimp [t]
    rw [Matrix.trace_sub, Matrix.trace_one]
    field_simp
    ring
  have hne : 1 + t ≠ 0 := by linarith
  have hi : (1 + t)⁻¹ * t = 1 - (1 + t)⁻¹ := by field_simp; ring
  rw [htrace]
  change (1 + t)⁻¹ • Z - 1 = (1 + t)⁻¹ • ((Z - 1) - t • 1)
  rw [smul_sub, smul_sub, smul_smul, hi, sub_smul, one_smul]
  abel

/-- The central sandwich bounds the operator width at the point's own trace parameter. -/
theorem opNorm_normalized_defect_le [Nonempty n] {Z : Matrix n n ℝ} {K : ℝ}
    (hlo : (1 : Matrix n n ℝ) ≤ Z) (hhi : Z ≤ K • (1 : Matrix n n ℝ))
    (hK : 1 ≤ K) : opNorm ((Z.trace / Fintype.card n)⁻¹ • Z - 1) ≤ K - 1 := by
  rw [normalized_defect_eq_recentered hlo]
  exact (opNorm_defect_and_recentered_le hlo hhi hK).2

/-- The central sandwich bounds the Frobenius width at the point's own trace parameter. -/
theorem frobeniusNorm_normalized_defect_le [Nonempty n] {Z : Matrix n n ℝ} {K : ℝ}
    (hlo : (1 : Matrix n n ℝ) ≤ Z) (hhi : Z ≤ K • (1 : Matrix n n ℝ))
    (hK : 1 ≤ K) : frobeniusNorm ((Z.trace / Fintype.card n)⁻¹ • Z - 1) ≤
      Real.sqrt (Fintype.card n) * (K - 1) := by
  rw [normalized_defect_eq_recentered hlo]
  exact (frobeniusNorm_defect_and_recentered_le hlo hhi hK).2

end QipmFormal.SDPMixture
