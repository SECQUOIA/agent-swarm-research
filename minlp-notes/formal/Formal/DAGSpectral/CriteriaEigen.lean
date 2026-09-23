import Formal.DAGSpectral.CriteriaBasic

open scoped MatrixOrder
open Matrix Unitary
namespace DAGSpectral
noncomputable section
variable {n : Type*} [Fintype n] [DecidableEq n] [Nonempty n]

/-- The actual smallest eigenvalue of a Hermitian matrix. -/
def hermitianMinimum {A : Matrix n n ℝ} (hA : A.IsHermitian) : ℝ :=
  Finset.univ.inf' Finset.univ_nonempty hA.eigenvalues

omit [Nonempty n] in
theorem scalar_le_hermitian_iff {A : Matrix n n ℝ} (hA : A.IsHermitian) (t : ℝ) :
    t • (1 : Matrix n n ℝ) ≤ A ↔ ∀ i, t ≤ hA.eigenvalues i := by
  rw [Matrix.le_iff]
  have he : A - t • (1 : Matrix n n ℝ) =
      Unitary.conjStarAlgAut ℝ _ hA.eigenvectorUnitary
        (diagonal hA.eigenvalues - t • (1 : Matrix n n ℝ)) := by
    rw [map_sub, map_smul, map_one]
    congr 1
    simpa using hA.spectral_theorem
  rw [he]
  have hd : diagonal hA.eigenvalues - t • (1 : Matrix n n ℝ) =
      diagonal (fun i => hA.eigenvalues i - t) := by
    ext i j
    by_cases h : i=j <;> simp [h]
  rw [hd]
  simp [isUnit_coe.posSemidef_star_right_conjugate_iff, posSemidef_diagonal_iff]

theorem scalar_le_hermitianMinimum_iff {A : Matrix n n ℝ} (hA : A.IsHermitian) (t : ℝ) :
    t ≤ hermitianMinimum hA ↔ t • (1 : Matrix n n ℝ) ≤ A := by
  rw [scalar_le_hermitian_iff hA]
  simp [hermitianMinimum, Finset.le_inf'_iff]

theorem hermitianMinimum_mono {A B : Matrix n n ℝ} (hA : A.IsHermitian)
    (hB : B.IsHermitian) (hAB : A ≤ B) : hermitianMinimum hA ≤ hermitianMinimum hB := by
  apply (scalar_le_hermitianMinimum_iff hB _).mpr
  exact ((scalar_le_hermitianMinimum_iff hA _).mp le_rfl).trans hAB

/-- The criterion is defined on all matrices; only its PSD restriction is used. -/
def minimumEigenvalue (A : Matrix n n ℝ) : ℝ :=
  if hA : A.IsHermitian then hermitianMinimum hA else 0

@[simp] theorem minimumEigenvalue_of_hermitian {A : Matrix n n ℝ} (hA : A.IsHermitian) :
    minimumEigenvalue A = hermitianMinimum hA := dif_pos hA

theorem minimumEigenvalue_nonneg {A : Matrix n n ℝ} (hA : A.PosSemidef) :
    0 ≤ minimumEigenvalue A := by
  rw [minimumEigenvalue_of_hermitian hA.isHermitian,
    scalar_le_hermitianMinimum_iff, zero_smul]
  exact hA.nonneg

theorem minimumEigenvalue_mono {A B : Matrix n n ℝ} (hA : A.PosSemidef)
    (hB : B.PosSemidef) (hAB : A ≤ B) : minimumEigenvalue A ≤ minimumEigenvalue B := by
  rw [minimumEigenvalue_of_hermitian hA.isHermitian, minimumEigenvalue_of_hermitian hB.isHermitian]
  exact hermitianMinimum_mono hA.isHermitian hB.isHermitian hAB

omit [Nonempty n] [Fintype n] [DecidableEq n] in
private theorem matrix_smul_mono {A B : Matrix n n ℝ} (h : A ≤ B)
    {c : ℝ} (hc : 0 ≤ c) : c • A ≤ c • B := by
  change (c • B-c • A).PosSemidef
  have hs : (B-A).PosSemidef := h
  simpa only [smul_sub] using hs.smul hc

@[simp] theorem minimumEigenvalue_zero : minimumEigenvalue (0 : Matrix n n ℝ) = 0 := by
  rw [minimumEigenvalue_of_hermitian isHermitian_zero]
  have hz : (isHermitian_zero : (0 : Matrix n n ℝ).IsHermitian).eigenvalues = 0 :=
    isHermitian_zero.eigenvalues_eq_zero_iff.mpr rfl
  simp [hermitianMinimum, hz]

theorem minimumEigenvalue_smul {A : Matrix n n ℝ} (hA : A.PosSemidef)
    {c : ℝ} (hc : 0 ≤ c) : minimumEigenvalue (c • A) = c * minimumEigenvalue A := by
  by_cases hz : c = 0
  · rw [hz, zero_smul, minimumEigenvalue_zero, zero_mul]
  have hp : 0 < c := lt_of_le_of_ne hc (Ne.symm hz)
  have hCA := hA.smul hc
  rw [minimumEigenvalue_of_hermitian hA.isHermitian,
    minimumEigenvalue_of_hermitian hCA.isHermitian]
  apply le_antisymm
  · have hb := (scalar_le_hermitianMinimum_iff hCA.isHermitian _).mp le_rfl
    have hi := matrix_smul_mono hb (inv_nonneg.mpr hc)
    have he : (hermitianMinimum hCA.isHermitian/c) • (1 : Matrix n n ℝ) ≤ A := by
      simpa [smul_smul, hz, div_eq_mul_inv, mul_comm] using hi
    have hh := (scalar_le_hermitianMinimum_iff hA.isHermitian _).mpr he
    nlinarith [(div_le_iff₀ hp).mp hh]
  · apply (scalar_le_hermitianMinimum_iff hCA.isHermitian _).mpr
    have hh := matrix_smul_mono
      ((scalar_le_hermitianMinimum_iff hA.isHermitian _).mp le_rfl) hc
    simpa only [smul_smul] using hh

theorem minimumEigenvalue_pos_iff {A : Matrix n n ℝ} (hA : A.PosSemidef) :
    0 < minimumEigenvalue A ↔ A.PosDef := by
  rw [minimumEigenvalue_of_hermitian hA.isHermitian,
    hA.isHermitian.posDef_iff_eigenvalues_pos]
  simp [hermitianMinimum, Finset.lt_inf'_iff]

theorem minimumEigenvalue_eq_zero_iff {A : Matrix n n ℝ} (hA : A.PosSemidef) :
    minimumEigenvalue A = 0 ↔ A.det = 0 := by
  have he := minimumEigenvalue_pos_iff hA
  rw [hA.posDef_iff_det_ne_zero] at he
  constructor
  · intro hz
    by_contra hd
    have hp := he.mpr hd
    linarith
  · intro hz
    have hn : ¬ 0 < minimumEigenvalue A := by
      intro hp
      exact he.mp hp hz
    exact le_antisymm (le_of_not_gt hn) (minimumEigenvalue_nonneg hA)


theorem minimumEigenvalue_attained {A : Matrix n n ℝ} (hA : A.IsHermitian) :
    ∃ i, minimumEigenvalue A = hA.eigenvalues i := by
  rw [minimumEigenvalue_of_hermitian hA]
  have hh : Finset.univ.inf' Finset.univ_nonempty hA.eigenvalues ≤ hermitianMinimum hA := le_rfl
  obtain ⟨i, hi, he⟩ := (Finset.inf'_le_iff Finset.univ_nonempty).mp hh
  refine ⟨i, le_antisymm ?_ he⟩
  exact Finset.inf'_le hA.eigenvalues hi

end
end DAGSpectral
