import QipmFormal.SDPMixture.Variance
import QipmFormal.Mixture.Centrality

namespace QipmFormal.SDPMixture
noncomputable section
open scoped MatrixOrder BigOperators
open Matrix
variable {n : Type*} [Fintype n] [DecidableEq n]

omit [Fintype n] in
/-- A strictly positive scalar lower bound makes a matrix positive definite. -/
theorem posDef_of_scalar_lower {X : Matrix n n ℝ} {m : ℝ}
    (hm : 0 < m) (hX : m • (1 : Matrix n n ℝ) ≤ X) : X.PosDef := by
  have h := (Matrix.PosDef.one (n := n) (R := ℝ)).smul hm
  have h' := h.add_posSemidef (Matrix.le_iff.mp hX)
  simpa using h'

/-- The one-matrix arithmetic--harmonic inequality uses no cross-matrix commutation. -/
theorem arithmetic_harmonic_bound {X : Matrix n n ℝ} {m M : ℝ}
    (hm : 0 < m) (hlo : m • (1 : Matrix n n ℝ) ≤ X)
    (hhi : X ≤ M • (1 : Matrix n n ℝ)) :
    X + (m * M) • X⁻¹ ≤ (m + M) • (1 : Matrix n n ℝ) := by
  have hX := posDef_of_scalar_lower hm hlo
  have hinv : X * X⁻¹ = 1 := Matrix.mul_nonsing_inv _ (isUnit_iff_ne_zero.mpr hX.det_pos.ne')
  have hinv' : X⁻¹ * X = 1 := Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr hX.det_pos.ne')
  have hc : Commute (X - m • (1 : Matrix n n ℝ)) (M • (1 : Matrix n n ℝ) - X) :=
    ((Commute.one_right X).smul_right M).sub_right (Commute.refl X) |>.sub_left
      (((Commute.one_left _).smul_left m).sub_right ((Commute.one_left X).smul_left m))
  have hp := Commute.mul_nonneg (sub_nonneg.mpr hlo) (sub_nonneg.mpr hhi) hc
  have hcInv : Commute X X⁻¹ := by unfold Commute SemiconjBy; rw [hinv, hinv']
  have hc' : Commute ((X - m • (1 : Matrix n n ℝ)) *
      (M • (1 : Matrix n n ℝ) - X)) X⁻¹ :=
    (hcInv.sub_left ((Commute.one_left _).smul_left m)).mul_left
      (((Commute.one_left _).smul_left M).sub_left hcInv)
  have hp' := Commute.mul_nonneg hp hX.posSemidef.inv.nonneg hc'
  apply sub_nonneg.mp
  convert hp' using 1
  simp only [mul_sub, sub_mul, smul_mul_assoc, mul_smul_comm, one_mul, mul_one]
  simp only [mul_assoc, hinv, mul_one, smul_sub, smul_smul]
  simp only [add_smul, mul_smul]
  rw [smul_comm M m]
  abel

variable {I : Type*} [Fintype I]

omit [Fintype n] in
theorem matrixMix_scalar_lower [Finite n] {w : I → ℝ} {X : I → Matrix n n ℝ} {m : ℝ}
    (hw : Mixture.ProbWeights w) (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i) :
    m • (1 : Matrix n n ℝ) ≤ matrixMix w X := by
  let := Fintype.ofFinite n
  calc
    m • (1 : Matrix n n ℝ) = ∑ i, w i • (m • (1 : Matrix n n ℝ)) := by
      rw [← Finset.sum_smul, hw.2, one_smul]
    _ ≤ matrixMix w X := Finset.sum_le_sum fun i _ =>
      smul_le_smul_of_nonneg_left (hlo i) (hw.1 i)

/-- The averaged one-matrix arithmetic--harmonic bound. -/
theorem matrixMix_arithmetic_harmonic {w : I → ℝ} {X : I → Matrix n n ℝ} {m M : ℝ}
    (hw : Mixture.ProbWeights w) (hm : 0 < m)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i)
    (hhi : ∀ i, X i ≤ M • (1 : Matrix n n ℝ)) :
    matrixMix w X + (m * M) • inverseMix w X ≤ (m + M) • (1 : Matrix n n ℝ) := by
  have h := Finset.sum_le_sum (s := Finset.univ) fun i _ =>
    smul_le_smul_of_nonneg_left (arithmetic_harmonic_bound hm (hlo i) (hhi i)) (hw.1 i)
  simpa [matrixMix, inverseMix, smul_add, Finset.sum_add_distrib, smul_comm _ (m * M),
    ← Finset.smul_sum, ← Finset.sum_smul, hw.2] using h

/-- Completing the square bounds the matrix quadratic without diagonalization. -/
theorem quadratic_bound (A : Matrix n n ℝ) (hA : IsSelfAdjoint A) (c : ℝ) :
    c • A - A * A ≤ (c ^ 2 / 4) • (1 : Matrix n n ℝ) := by
  have hB : IsSelfAdjoint (A - (c / 2) • (1 : Matrix n n ℝ)) :=
    hA.sub ((isSelfAdjoint_iff.mpr (star_trivial _)).smul (IsSelfAdjoint.one _))
  have hp := star_mul_self_nonneg (A - (c / 2) • (1 : Matrix n n ℝ))
  rw [hB.star_eq] at hp
  apply sub_nonneg.mp
  convert hp using 1
  simp only [sub_mul, mul_sub, smul_mul_assoc, mul_smul_comm, one_mul, mul_one,
    smul_sub, smul_smul]
  have hc : c ^ 2 / 4 = c / 2 * (c / 2) := by ring
  rw [hc]
  have hc' : c • A = (c / 2) • A + (c / 2) • A := by rw [← add_smul]; congr 1; ring
  rw [hc']
  abel

/-- Sharp noncommutative Kantorovich upper bound for the central matrix. -/
theorem centralMatrix_le {w : I → ℝ} {X : I → Matrix n n ℝ} {m M : ℝ}
    (hw : Mixture.ProbWeights w) (hm : 0 < m) (hmM : m ≤ M)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i)
    (hhi : ∀ i, X i ≤ M • (1 : Matrix n n ℝ)) :
    centralMatrix w X ≤ ((m + M) ^ 2 / (4 * m * M)) • (1 : Matrix n n ℝ) := by
  let A := matrixMix w X
  let Q := CFC.sqrt A
  have hA : A.PosDef := posDef_of_scalar_lower hm (matrixMix_scalar_lower hw hlo)
  have hQ : Q * Q = A := CFC.sqrt_mul_sqrt_self A hA.posSemidef.nonneg
  have havg := matrixMix_arithmetic_harmonic hw hm hlo hhi
  have hconj := conjugate_le_conjugate_of_nonneg havg (CFC.sqrt_nonneg A)
  change Q * (A + (m * M) • inverseMix w X) * Q ≤ Q * ((m + M) • 1) * Q at hconj
  have hQAQ : Q * A * Q = A * A := by
    rw [← hQ]; noncomm_ring
  simp only [mul_add, add_mul, mul_smul_comm, smul_mul_assoc, mul_one, hQ, hQAQ] at hconj
  have hscaled : (m * M) • centralMatrix w X ≤ ((m + M) ^ 2 / 4) • (1 : Matrix n n ℝ) := by
    exact (le_sub_iff_add_le'.mpr hconj).trans (quadratic_bound A hA.isHermitian (m + M))
  have hp : 0 < m * M := mul_pos hm (hm.trans_le hmM)
  apply (smul_le_smul_iff_of_pos_left hp).mp
  rw [smul_smul]
  convert hscaled using 1
  congr 1
  field_simp [hm.ne', (hm.trans_le hmM).ne']

/-- The endpoint expression is the paper's dimensionless Kantorovich constant. -/
theorem kantorovich_ratio_eq {m M : ℝ} (hm : 0 < m) (hM : 0 < M) :
    (m + M) ^ 2 / (4 * m * M) = Mixture.kantorovich (M / m) := by
  unfold Mixture.kantorovich
  field_simp
  ring

/-- Both sides of the noncommutative central sandwich, with the paper's ratio. -/
theorem centralMatrix_sandwich {w : I → ℝ} {X : I → Matrix n n ℝ} {m M : ℝ}
    (hw : Mixture.ProbWeights w) (hm : 0 < m) (hmM : m ≤ M)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i)
    (hhi : ∀ i, X i ≤ M • (1 : Matrix n n ℝ)) :
    (1 : Matrix n n ℝ) ≤ centralMatrix w X ∧
      centralMatrix w X ≤ Mixture.kantorovich (M / m) • (1 : Matrix n n ℝ) := by
  constructor
  · exact one_le_centralMatrix hw fun i => posDef_of_scalar_lower hm (hlo i)
  · rw [← kantorovich_ratio_eq hm (hm.trans_le hmM)]
    exact centralMatrix_le hw hm hmM hlo hhi

/-- The exact excess in the ratio bound. -/
theorem centralMatrix_sub_one_le {w : I → ℝ} {X : I → Matrix n n ℝ} {m M : ℝ}
    (hw : Mixture.ProbWeights w) (hm : 0 < m) (hmM : m ≤ M)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i)
    (hhi : ∀ i, X i ≤ M • (1 : Matrix n n ℝ)) :
    centralMatrix w X - 1 ≤ (((M / m - 1) ^ 2) / (4 * (M / m))) • (1 : Matrix n n ℝ) := by
  have h := sub_le_sub_right (centralMatrix_sandwich hw hm hmM hlo hhi).2 1
  have heq : Mixture.kantorovich (M / m) • (1 : Matrix n n ℝ) - 1 =
      (Mixture.kantorovich (M / m) - 1) • (1 : Matrix n n ℝ) := by
    simp [sub_smul]
  rw [heq, Mixture.kantorovich_sub_one _ (div_pos (hm.trans_le hmM) hm)] at h
  exact h

/-- Inversion of a nonzero scalar matrix. -/
theorem scalar_matrix_inv (c : ℝ) (hc : c ≠ 0) :
    (c • (1 : Matrix n n ℝ))⁻¹ = c⁻¹ • (1 : Matrix n n ℝ) := by
  apply Matrix.inv_eq_right_inv
  simp [smul_smul, hc]

/-- Equal endpoint mixtures attain the upper bound in every matrix dimension. -/
theorem endpoint_mixture_sharp {m M : ℝ} (hm : 0 < m) (hM : 0 < M) :
    centralMatrix (fun _ : Fin 2 => (1 / 2 : ℝ))
      ![m • (1 : Matrix n n ℝ), M • (1 : Matrix n n ℝ)] =
      ((m + M) ^ 2 / (4 * m * M)) • (1 : Matrix n n ℝ) := by
  have ha : 0 ≤ (m + M) / 2 := by positivity
  have hmix : matrixMix (fun _ : Fin 2 => (1 / 2 : ℝ))
      ![m • (1 : Matrix n n ℝ), M • (1 : Matrix n n ℝ)] =
      ((m + M) / 2) • (1 : Matrix n n ℝ) := by
    simp only [matrixMix, Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one,
      smul_smul, ← add_smul]
    congr 1
    ring
  have himix : inverseMix (fun _ : Fin 2 => (1 / 2 : ℝ))
      ![m • (1 : Matrix n n ℝ), M • (1 : Matrix n n ℝ)] =
      ((m⁻¹ + M⁻¹) / 2) • (1 : Matrix n n ℝ) := by
    simp only [inverseMix, matrixMix, Fin.sum_univ_two, Matrix.cons_val_zero,
      Matrix.cons_val_one, scalar_matrix_inv m hm.ne',
      scalar_matrix_inv M hM.ne', smul_smul, ← add_smul]
    congr 1
    ring
  rw [centralMatrix, hmix, himix]
  simp only [mul_smul_comm, mul_one, smul_mul_assoc,
    CFC.sqrt_mul_sqrt_self _ (smul_nonneg ha zero_le_one), smul_smul]
  congr 1
  field_simp
  ring

omit [Fintype n] in
/-- The sharp endpoint example satisfies all sandwich hypotheses. -/
theorem endpoint_mixture_admissible [Finite n] {m M : ℝ} (hmM : m ≤ M) :
    Mixture.ProbWeights (fun _ : Fin 2 => (1 / 2 : ℝ)) ∧
      ∀ i : Fin 2, m • (1 : Matrix n n ℝ) ≤
        (![m • (1 : Matrix n n ℝ), M • (1 : Matrix n n ℝ)] i) ∧
        (![m • (1 : Matrix n n ℝ), M • (1 : Matrix n n ℝ)] i) ≤
          M • (1 : Matrix n n ℝ) := by
  let := Fintype.ofFinite n
  constructor
  · constructor
    · norm_num
    · norm_num [Fin.sum_univ_two]
  · intro i
    fin_cases i <;> dsimp
    · exact ⟨le_rfl, smul_le_smul_of_nonneg_right hmM zero_le_one⟩
    · exact ⟨smul_le_smul_of_nonneg_right hmM zero_le_one, le_rfl⟩

/-- In positive dimension, no smaller universal scalar upper bound is possible. -/
theorem endpoint_mixture_forces_constant [Nonempty n] {m M k : ℝ}
    (hm : 0 < m) (hM : 0 < M)
    (hk : centralMatrix (fun _ : Fin 2 => (1 / 2 : ℝ))
      ![m • (1 : Matrix n n ℝ), M • (1 : Matrix n n ℝ)] ≤
        k • (1 : Matrix n n ℝ)) :
    (m + M) ^ 2 / (4 * m * M) ≤ k := by
  rw [endpoint_mixture_sharp hm hM] at hk
  obtain ⟨i⟩ := ‹Nonempty n›
  have hd := (Matrix.le_iff.mp hk).diag_nonneg (i := i)
  simpa using hd
end
end QipmFormal.SDPMixture
