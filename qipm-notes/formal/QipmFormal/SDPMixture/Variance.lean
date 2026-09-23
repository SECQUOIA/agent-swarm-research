import QipmFormal.SDPMixture.Defs

/-! # Exact matrix multiplicative variance and its equality case -/
namespace QipmFormal.SDPMixture
noncomputable section
open scoped BigOperators MatrixOrder
open Matrix

variable {I n : Type*} [Fintype I] [Fintype n] [DecidableEq n]
  {w : I → ℝ} {X : I → Matrix n n ℝ}

omit [Fintype n] [DecidableEq n] in
theorem matrixMix_posSemidef (hw : ∀ i, 0 ≤ w i)
    (hX : ∀ i, (X i).PosSemidef) : (matrixMix w X).PosSemidef :=
  Matrix.posSemidef_sum _ fun i _ => (hX i).smul (hw i)

omit [Fintype n] [DecidableEq n] in
theorem matrixMix_posDef [Finite n] (hw : Mixture.ProbWeights w)
    (hX : ∀ i, (X i).PosDef) : (matrixMix w X).PosDef := by
  let := Fintype.ofFinite n
  have hnonneg := matrixMix_posSemidef hw.1 fun i => (hX i).posSemidef
  obtain ⟨i, _, hi⟩ := (Finset.sum_pos_iff_of_nonneg (fun i _ => hw.1 i)).mp
    (show 0 < ∑ i, w i by rw [hw.2]; norm_num)
  refine Matrix.PosDef.of_dotProduct_mulVec_pos hnonneg.isHermitian fun x hx => ?_
  simp only [matrixMix, Matrix.sum_mulVec, dotProduct_sum, Matrix.smul_mulVec,
    dotProduct_smul, smul_eq_mul]
  apply (Finset.sum_pos_iff_of_nonneg (fun j _ =>
    mul_nonneg (hw.1 j) ((hX j).posSemidef.dotProduct_mulVec_nonneg x))).mpr
  exact ⟨i, Finset.mem_univ _, mul_pos hi ((hX i).dotProduct_mulVec_pos hx)⟩

theorem inverseMix_posDef (hw : Mixture.ProbWeights w)
    (hX : ∀ i, (X i).PosDef) : (inverseMix w X).PosDef :=
  matrixMix_posDef hw fun i => (hX i).inv

/-- Algebraic expansion before normalization; no matrices are assumed to commute. -/
theorem variance_identity (hw : Mixture.ProbWeights w)
    (hX : ∀ i, (X i).PosDef) :
    variance w X = matrixMix w X * inverseMix w X * matrixMix w X - matrixMix w X := by
  have hterm (i : I) :
      (X i - matrixMix w X) * (X i)⁻¹ * (X i - matrixMix w X) =
      X i - matrixMix w X - matrixMix w X +
        matrixMix w X * (X i)⁻¹ * matrixMix w X := by
    have hu := (Matrix.isUnit_iff_isUnit_det _).mp (hX i).isUnit
    simp only [sub_mul, mul_sub, Matrix.mul_nonsing_inv _ hu,
      one_mul, mul_assoc, Matrix.nonsing_inv_mul _ hu, mul_one]
    noncomm_ring
  simp only [variance, hterm, smul_add, smul_sub, Finset.sum_add_distrib,
    Finset.sum_sub_distrib, ← Finset.sum_smul, hw.2, one_smul]
  rw [show (∑ i, w i • (matrixMix w X * (X i)⁻¹ * matrixMix w X)) =
    matrixMix w X * inverseMix w X * matrixMix w X by
      change (∑ i, w i • (matrixMix w X * (X i)⁻¹ * matrixMix w X)) =
        matrixMix w X * (∑ i, w i • (X i)⁻¹) * matrixMix w X
      simp only [Matrix.mul_sum, Matrix.sum_mul, Matrix.mul_smul, Matrix.smul_mul]]
  change matrixMix w X - matrixMix w X - matrixMix w X + _ = _
  abel

theorem variance_posSemidef (hw : Mixture.ProbWeights w)
    (hX : ∀ i, (X i).PosDef) : (variance w X).PosSemidef := by
  apply Matrix.posSemidef_sum
  intro i _
  apply Matrix.PosSemidef.smul _ (hw.1 i)
  have hd := (hX i).isHermitian.sub (matrixMix_posDef hw hX).isHermitian
  simpa only [hd.eq] using
    (hX i).inv.posSemidef.conjTranspose_mul_mul_same (X i - matrixMix w X)

/-- The positive square root of the average is invertible. -/
theorem sqrt_matrixMix_isUnit (hw : Mixture.ProbWeights w)
    (hX : ∀ i, (X i).PosDef) : IsUnit (CFC.sqrt (matrixMix w X)) :=
  CFC.isUnit_sqrt_iff_isStrictlyPositive.mpr
    (Matrix.isStrictlyPositive_iff_posDef.mpr (matrixMix_posDef hw hX))

/-- The exact matrix multiplicative variance after the inverse-square-root congruence. -/
theorem normalized_variance_identity (hw : Mixture.ProbWeights w)
    (hX : ∀ i, (X i).PosDef) :
    centralMatrix w X - 1 =
      (CFC.sqrt (matrixMix w X))⁻¹ * variance w X * (CFC.sqrt (matrixMix w X))⁻¹ := by
  let B := CFC.sqrt (matrixMix w X)
  have hBB : B * B = matrixMix w X :=
    CFC.sqrt_mul_sqrt_self _ (matrixMix_posDef hw hX).posSemidef.nonneg
  have hu := (Matrix.isUnit_iff_isUnit_det _).mp (sqrt_matrixMix_isUnit hw hX)
  have hleft : B⁻¹ * B = 1 := Matrix.nonsing_inv_mul _ hu
  have hright : B * B⁻¹ = 1 := Matrix.mul_nonsing_inv _ hu
  rw [variance_identity hw hX]
  change B * inverseMix w X * B - 1 =
    B⁻¹ * (matrixMix w X * inverseMix w X * matrixMix w X - matrixMix w X) * B⁻¹
  rw [← hBB]
  simp only [mul_sub, sub_mul, ← mul_assoc, hleft, one_mul]
  simp only [mul_assoc, hright, mul_one]

theorem one_le_centralMatrix (hw : Mixture.ProbWeights w)
    (hX : ∀ i, (X i).PosDef) : (1 : Matrix n n ℝ) ≤ centralMatrix w X := by
  rw [Matrix.le_iff, normalized_variance_identity hw hX]
  have hs := (CFC.sqrt_nonneg (matrixMix w X)).posSemidef.inv.isHermitian
  simpa only [hs.eq] using
    (variance_posSemidef hw hX).conjTranspose_mul_mul_same
      (CFC.sqrt (matrixMix w X))⁻¹

omit [DecidableEq n] in
/-- A positive-definite quadratic congruence vanishes only for the zero matrix. -/
theorem posDef_congruence_eq_zero_iff {A D : Matrix n n ℝ} (hA : A.PosDef)
    (hD : D.IsHermitian) : D * A * D = 0 ↔ D = 0 := by
  classical
  constructor
  · intro hz
    let B := CFC.sqrt A
    have hBB : B * B = A := CFC.sqrt_mul_sqrt_self _ hA.posSemidef.nonneg
    have hB : B.IsHermitian := (CFC.sqrt_nonneg A).posSemidef.isHermitian
    have hu : IsUnit B := CFC.isUnit_sqrt_iff_isStrictlyPositive.mpr
      (Matrix.isStrictlyPositive_iff_posDef.mpr hA)
    have hBD : B * D = 0 := Matrix.conjTranspose_mul_self_eq_zero.mp (by
      rw [Matrix.conjTranspose_mul, hD.eq, hB.eq]
      simpa only [mul_assoc, ← hBB] using hz)
    have hh := congrArg (fun T => B⁻¹ * T) hBD
    simpa only [← mul_assoc, Matrix.nonsing_inv_mul _
      ((Matrix.isUnit_iff_isUnit_det _).mp hu), one_mul, mul_zero] using hh
  · rintro rfl
    simp

/-- Zero weights impose no restriction on the associated matrix. -/
theorem variance_eq_zero_iff (hw : Mixture.ProbWeights w)
    (hX : ∀ i, (X i).PosDef) :
    variance w X = 0 ↔ ∀ i, 0 < w i → X i = matrixMix w X := by
  have hd i := (hX i).isHermitian.sub (matrixMix_posDef hw hX).isHermitian
  have ht i : ((X i - matrixMix w X) * (X i)⁻¹ *
      (X i - matrixMix w X)).PosSemidef := by
    simpa only [(hd i).eq] using
      (hX i).inv.posSemidef.conjTranspose_mul_mul_same (X i - matrixMix w X)
  constructor
  · intro hz i hi
    have hsum := (Finset.sum_eq_zero_iff_of_nonneg
      (fun i (_ : i ∈ Finset.univ) => ((ht i).smul (hw.1 i)).nonneg)).mp hz i
      (Finset.mem_univ i)
    have hterm := (smul_eq_zero.mp hsum).resolve_left (ne_of_gt hi)
    exact sub_eq_zero.mp ((posDef_congruence_eq_zero_iff (hX i).inv (hd i)).mp hterm)
  · intro h
    apply Finset.sum_eq_zero
    intro i _
    by_cases hi : w i = 0
    · simp [hi]
    · rw [h i (lt_of_le_of_ne (hw.1 i) (Ne.symm hi))]
      simp

/-- Equality in the lower central bound characterizes constant positive-weight support. -/
theorem centralMatrix_eq_one_iff (hw : Mixture.ProbWeights w)
    (hX : ∀ i, (X i).PosDef) :
    centralMatrix w X = 1 ↔ ∀ i, 0 < w i → X i = matrixMix w X := by
  rw [← variance_eq_zero_iff hw hX]
  constructor
  · intro hz
    have hh := normalized_variance_identity hw hX
    rw [hz, sub_self] at hh
    let B := CFC.sqrt (matrixMix w X)
    have hu := (Matrix.isUnit_iff_isUnit_det _).mp (sqrt_matrixMix_isUnit hw hX)
    have hr : B * B⁻¹ = 1 := Matrix.mul_nonsing_inv _ hu
    have hl : B⁻¹ * B = 1 := Matrix.nonsing_inv_mul _ hu
    have he := congrArg (fun T => B * T * B) hh.symm
    change B * (B⁻¹ * variance w X * B⁻¹) * B = B * 0 * B at he
    have hc : B * (B⁻¹ * variance w X * B⁻¹) * B = variance w X := by
      calc
        _ = (B * B⁻¹) * variance w X * (B⁻¹ * B) := by noncomm_ring
        _ = variance w X := by rw [hr, hl, one_mul, mul_one]
    simpa only [hc, mul_zero, zero_mul] using he
  · intro hz
    have hh := normalized_variance_identity hw hX
    rw [hz, mul_zero, zero_mul] at hh
    exact sub_eq_zero.mp hh

end
end QipmFormal.SDPMixture
