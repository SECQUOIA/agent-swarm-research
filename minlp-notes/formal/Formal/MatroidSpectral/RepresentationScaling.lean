import Formal.MatroidSpectral.RepresentationReduction

namespace MatroidSpectral
open Matrix

theorem columnMinor_smul {q m : ℕ} (A : RationalRepresentation q m)
    (c : ℚ) (B : Finset (Fin m)) :
    columnMinor (c • A) B = c ^ q * columnMinor A B := by
  unfold columnMinor
  split_ifs with h
  · change (c • A.submatrix id (B.orderEmbOfFin h)).det = _
    simp only [Matrix.det_smul,Fintype.card_fin]
  · simp

theorem isBase_smul_iff {q m : ℕ} (A : RationalRepresentation q m)
    (c : ℚ) (hc : c ≠ 0) (B : Finset (Fin m)) :
    IsBase (c • A) B ↔ IsBase A B := by
  simp [IsBase,columnMinor_smul,hc]

theorem columnIndependent_smul_iff {a m : ℕ} (A : RationalRepresentation a m)
    (c : ℚ) (hc : c ≠ 0) (B : Finset (Fin m)) :
    ColumnIndependent (c • A) B ↔ ColumnIndependent A B := by
  change LinearIndependent ℚ ((fun _ : B => Units.mk0 c hc) • (fun j : B => A.col j)) ↔ _
  exact LinearIndependent.units_smul_iff _ _

/-- A common nonzero denominator multiplier preserves every dependency and
every original base, including the zero-rank case. -/
theorem isColumnBase_smul_iff {a m : ℕ} (A : RationalRepresentation a m)
    (c : ℚ) (hc : c ≠ 0) (B : Finset (Fin m)) :
    IsColumnBase (c • A) B ↔ IsColumnBase A B := by
  simp only [IsColumnBase,columnIndependent_smul_iff A c hc,
    Matrix.rank_smul_of_mem_nonZeroDivisors A (mem_nonZeroDivisors_of_ne_zero hc)]

end MatroidSpectral
