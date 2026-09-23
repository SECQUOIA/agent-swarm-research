import Formal.MatroidSpectral.CoverCardinality
import Formal.MatroidSpectral.RepresentationCost
import Formal.DAGSpectral.NormalizationInput

namespace MatroidSpectral
open Matrix DAGSpectral DAGSpectral.NormalizationTrials
open scoped BigOperators

/-- Semantic domain only. The algorithm never enumerates all bases. -/
noncomputable def columnBases {a m : ℕ} (A : RationalRepresentation a m) :
    Finset (Finset (Fin m)) := by
  classical
  exact Finset.univ.filter (IsColumnBase A)

@[simp] theorem mem_columnBases {a m : ℕ} (A : RationalRepresentation a m)
    (B : Finset (Fin m)) : B ∈ columnBases A ↔ IsColumnBase A B := by
  classical
  simp [columnBases]

theorem columnBases_eq_reduced {a m : ℕ} (A : RationalRepresentation a m) :
    columnBases A = bases (rowReductionRepresentation A) := by
  ext B
  simp only [mem_columnBases,mem_bases,rowReductionRepresentation_isBase_iff]

theorem columnBases_nonempty {a m : ℕ} (A : RationalRepresentation a m) :
    (columnBases A).Nonempty :=
  ⟨independentRows A.transpose,
    (mem_columnBases A _).mpr (independentRows_transpose_isColumnBase A)⟩

/-- Original rational input, including arbitrary redundant rows. Row selection,
PSD factorization, profile interpolation and base recovery are all computed.
The counted execution refines this value and caches its intermediate matrices. -/
def representedSpectralCover {a m p : ℕ} (A : RationalRepresentation a m)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) : Finset (Finset (Fin m)) :=
  spectralBasisSet (rowReductionRepresentation A) (producedData Q0 Q hQ0 hQ) η

theorem representedSpectralCover_isRelativeCover {a m p : ℕ} (A : RationalRepresentation a m)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    {η : ℚ} (hη : 0 < η) :
    IsRelativeCover (η : ℝ) (fun B => ratMatrixReal (Q0 + ∑ e ∈ B, Q e))
      (columnBases A) (representedSpectralCover A Q0 Q hQ0 hQ η) := by
  rw [columnBases_eq_reduced]
  exact spectralBasisSet_isRelativeCover _ _ hη

theorem representedSpectralCover_sound {a m p : ℕ} (A : RationalRepresentation a m)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    {η : ℚ} (hη : 0 < η) {B : Finset (Fin m)}
    (hB : B ∈ representedSpectralCover A Q0 Q hQ0 hQ η) : IsColumnBase A B :=
  (mem_columnBases A B).mp
    ((representedSpectralCover_isRelativeCover A Q0 Q hQ0 hQ hη).1 hB)

theorem representedSpectralCover_nonempty {a m p : ℕ} (A : RationalRepresentation a m)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    {η : ℚ} (hη : 0 < η) :
    (representedSpectralCover A Q0 Q hQ0 hQ η).Nonempty := by
  obtain ⟨B,hB⟩ := columnBases_nonempty A
  obtain ⟨C,hC,_⟩ := (representedSpectralCover_isRelativeCover A Q0 Q hQ0 hQ hη).2 B hB
  exact ⟨C,hC⟩

theorem representedSpectralCover_rank_zero {a m p : ℕ} (A : RationalRepresentation a m)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (hr : A.rank = 0) :
    representedSpectralCover A Q0 Q hQ0 hQ η = {∅} := by
  simp [representedSpectralCover,spectralBasisSet,rowReductionRun_rank,hr]

theorem representedSpectralCover_card {a m p : ℕ} (A : RationalRepresentation a m)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    {η : ℚ} (hη : 0 < η) :
    (representedSpectralCover A Q0 Q hQ0 hQ η).card ≤
      matroidCoverCardinality p (indexedFactorCount (priorAtomMatrices Q0 Q)) A.rank η := by
  simpa only [representedSpectralCover,rowReductionRun_rank] using
    spectralBasisSet_card (rowReductionRepresentation A) (producedData Q0 Q hQ0 hQ) hη

/-- Every original base has one actual output with both PSD inequalities and
exactly the same kernel and range, even when its information is singular. -/
theorem representedSpectralCover_complete {a m p : ℕ} (A : RationalRepresentation a m)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    {η : ℚ} (hη : 0 < η) (hη1 : η < 1) {B : Finset (Fin m)} (hB : IsColumnBase A B) :
    ∃ C ∈ representedSpectralCover A Q0 Q hQ0 hQ η, IsColumnBase A C ∧
      RelativeSandwich (η : ℝ) (ratMatrixReal (Q0 + ∑ e ∈ B, Q e))
        (ratMatrixReal (Q0 + ∑ e ∈ C, Q e)) ∧
      (∀ x, ratMatrixReal (Q0 + ∑ e ∈ B, Q e) *ᵥ x = 0 ↔
        ratMatrixReal (Q0 + ∑ e ∈ C, Q e) *ᵥ x = 0) ∧
      LinearMap.range (ratMatrixReal (Q0 + ∑ e ∈ B, Q e)).mulVecLin =
        LinearMap.range (ratMatrixReal (Q0 + ∑ e ∈ C, Q e)).mulVecLin := by
  obtain ⟨C,hC,hrel⟩ := (representedSpectralCover_isRelativeCover A Q0 Q hQ0 hQ hη).2 B
    ((mem_columnBases A B).mpr hB)
  exact ⟨C,hC,representedSpectralCover_sound A Q0 Q hQ0 hQ hη hC,hrel,
    relative_information_kernel (producedData Q0 Q hQ0 hQ) η hη1 B C hrel,
    relative_information_range (producedData Q0 Q hQ0 hQ) η hη1 B C hrel⟩

end MatroidSpectral
