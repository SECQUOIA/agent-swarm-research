import Formal.MatroidSpectral.Representation
import Formal.DAGSpectral.CriteriaEigen
import Formal.DAGSpectral.RangeObstruction
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

/-! Exact witnesses delimiting determinant support and attainable profiles.
These examples rule out particular substitutions in the proof, not every
possible algorithm for a broader input model. -/
namespace MatroidSpectral
namespace Boundaries
open Matrix
open scoped BigOperators

def positiveRow : RationalRepresentation 1 2 := fun _ _ => 1
def mixedRow : RationalRepresentation 1 2 := fun _ e => if e = 0 then 1 else -1

theorem singleton_isBase {m : ℕ} (A : RationalRepresentation 1 m) (e : Fin m)
    (h : A 0 e ≠ 0) : IsBase A {e} := by
  have hb := (orderedMinor_isBase A (fun _ => e)).mpr
    (show (A.submatrix id (fun _ => e)).det ≠ 0 by simpa using h)
  simpa using hb

theorem both_common_singletons (e : Fin 2) :
    IsBase positiveRow {e} ∧ IsBase mixedRow {e} := by
  constructor <;> apply singleton_isBase <;> fin_cases e <;>
    norm_num [positiveRow, mixedRow]

/-- Different representations can cancel even when both singleton bases exist. -/
theorem mixed_determinant_cancels :
    (positiveRow * mixedRow.transpose).det = 0 := by
  norm_num [positiveRow, mixedRow, Matrix.det_fin_one, Matrix.mul_apply,
    Fin.sum_univ_two, Matrix.transpose_apply]

/-- Squared minors for a single rational representation are positive instead. -/
theorem squared_determinant_positive :
    (positiveRow * positiveRow.transpose).det = 2 := by
  norm_num [positiveRow, Matrix.det_fin_one, Matrix.mul_apply,
    Fin.sum_univ_two, Matrix.transpose_apply]

def fieldWitness (R : Type*) [OfNat R 0] [OfNat R 1] : Matrix (Fin 3) (Fin 3) R :=
  fun i j => if i.val + j.val = 2 then 0 else 1

theorem rational_fieldWitness_det : (fieldWitness ℚ).det = -2 := by
  norm_num [fieldWitness, Matrix.det_fin_three]
  try decide

theorem mod_two_fieldWitness_det : (fieldWitness (ZMod 2)).det = 0 := by
  norm_num [fieldWitness, Matrix.det_fin_three]
  try decide

theorem finite_field_changes_independence :
    (fieldWitness ℚ).det ≠ 0 ∧ (fieldWitness (ZMod 2)).det = 0 := by
  rw [rational_fieldWitness_det, mod_two_fieldWitness_det]
  norm_num

/-- The positive rational constant coefficient 2 disappears modulo 2. -/
theorem positive_coefficient_can_vanish :
    (0 : ℚ) < (positiveRow * positiveRow.transpose).det ∧ (2 : ZMod 2) = 0 := by
  rw [squared_determinant_positive]
  constructor
  · norm_num
  · decide

def scalarInformation (e : Fin 2) : ℚ := if e = 0 then 1 else 3

theorem scalar_base_value (B : Finset (Fin 2)) (hB : IsBase positiveRow B) :
    (∑ e ∈ B, scalarInformation e) = 1 ∨
      (∑ e ∈ B, scalarInformation e) = 3 := by
  obtain ⟨e, rfl⟩ := Finset.card_eq_one.mp hB.card
  fin_cases e <;> simp [scalarInformation]

theorem projected_integer_unattained :
    ¬ ∃ B : Finset (Fin 2), IsBase positiveRow B ∧
      (∑ e ∈ B, scalarInformation e) = 2 := by
  rintro ⟨B, hB, h⟩
  rcases scalar_base_value B hB with h₁ | h₃ <;> linarith

/-- Nevertheless 2 is an integer point and a convex combination of the two
attained values. Convexifying first changes the feasible profile set. -/
theorem projected_integer_in_interval :
    (1 : ℚ) ≤ 2 ∧ (2 : ℚ) ≤ 3 ∧
      (2 : ℚ) = (1 / 2 : ℚ) * 1 + (1 - (1 / 2 : ℚ)) * 3 := by
  norm_num

theorem projected_endpoints_attained :
    IsBase positiveRow {(0 : Fin 2)} ∧ IsBase positiveRow {(1 : Fin 2)} ∧
    scalarInformation 0 = 1 ∧ scalarInformation 1 = 3 := by
  exact ⟨(both_common_singletons 0).1, (both_common_singletons 1).1,
    by norm_num [scalarInformation], by norm_num [scalarInformation]⟩

open DAGSpectral
open scoped MatrixOrder

def diagonalTwo (a b : ℝ) : RealMatrix 2 := diagonal (fun i => if i = 0 then a else b)

theorem diagonalTwo_psd {a b : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) :
    (diagonalTwo a b).PosSemidef := by
  apply Matrix.PosSemidef.diagonal
  intro i
  change 0 ≤ (if i = 0 then a else b)
  split_ifs <;> assumption

theorem scalar_le_diagonalTwo (a b t : ℝ) :
    t • (1 : RealMatrix 2) ≤ diagonalTwo a b ↔ t ≤ a ∧ t ≤ b := by
  change (diagonalTwo a b - t • (1 : RealMatrix 2)).PosSemidef ↔ _
  have he : diagonalTwo a b - t • (1 : RealMatrix 2) =
      diagonal (fun i : Fin 2 => if i = 0 then a-t else b-t) := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [diagonalTwo]
  rw [he, Matrix.posSemidef_diagonal_iff]
  simp [Fin.forall_fin_two, sub_nonneg]

theorem minimum_diagonalTwo (a b : ℝ) :
    minimumEigenvalue (diagonalTwo a b) = min a b := by
  have hh : (diagonalTwo a b).IsHermitian := Matrix.isHermitian_diagonal _
  rw [minimumEigenvalue_of_hermitian hh]
  apply le_antisymm
  · have h := (scalar_le_hermitianMinimum_iff hh (hermitianMinimum hh)).mp le_rfl
    exact le_min ((scalar_le_diagonalTwo a b _).mp h).1
      ((scalar_le_diagonalTwo a b _).mp h).2
  · apply (scalar_le_hermitianMinimum_iff hh _).mpr
    exact (scalar_le_diagonalTwo a b _).mpr ⟨min_le_left _ _, min_le_right _ _⟩

/-- All three profiles are actual singleton bases of the rank-one uniform matroid. -/
def threeUniform : RationalRepresentation 1 3 := fun _ _ => 1

theorem threeUniform_singleton (e : Fin 3) : IsBase threeUniform {e} :=
  singleton_isBase _ _ (by norm_num [threeUniform])

theorem interior_profile_midpoint :
    diagonalTwo 2 2 = (1/2 : ℝ) • diagonalTwo 1 3 + (1/2 : ℝ) • diagonalTwo 3 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [diagonalTwo]

theorem interior_profile_determinant_strict :
    (diagonalTwo 1 3).det < (diagonalTwo 2 2).det ∧
      (diagonalTwo 3 1).det < (diagonalTwo 2 2).det := by
  norm_num [diagonalTwo, Matrix.det_diagonal, Fin.prod_univ_two]

theorem interior_profile_eigenvalue_strict :
    minimumEigenvalue (diagonalTwo 1 3) < minimumEigenvalue (diagonalTwo 2 2) ∧
      minimumEigenvalue (diagonalTwo 3 1) < minimumEigenvalue (diagonalTwo 2 2) := by
  simp only [minimum_diagonalTwo]
  norm_num

def threeInformation (e : Fin 3) : RealMatrix 2 :=
  if e = 0 then diagonalTwo 1 3 else if e = 1 then diagonalTwo 2 2 else diagonalTwo 3 1

theorem threeInformation_psd (e : Fin 3) : (threeInformation e).PosSemidef := by
  fin_cases e <;> simp only [threeInformation] <;> norm_num <;>
    exact diagonalTwo_psd (by norm_num) (by norm_num)

/-- The interior profile is the unique optimum among actual feasible singleton designs. -/
theorem interior_profile_unique_optimum (e : Fin 3) (he : e ≠ 1) :
    IsBase threeUniform {e} ∧ IsBase threeUniform {(1 : Fin 3)} ∧
      (threeInformation e).det < (threeInformation 1).det ∧
      minimumEigenvalue (threeInformation e) < minimumEigenvalue (threeInformation 1) := by
  refine ⟨threeUniform_singleton e, threeUniform_singleton 1, ?_⟩
  fin_cases e
  · simpa [threeInformation] using
      And.intro interior_profile_determinant_strict.1 interior_profile_eigenvalue_strict.1
  · exact (he rfl).elim
  · simpa [threeInformation] using
      And.intro interior_profile_determinant_strict.2 interior_profile_eigenvalue_strict.2

/-- The same dominated-matrix counterexample is feasible for represented bases. -/
theorem dominated_base_deletion_loses_cover {η : ℝ} (hη : η < 1 / 2) :
    IsBase positiveRow {(0 : Fin 2)} ∧ IsBase positiveRow {(1 : Fin 2)} ∧
      Loewner (twoPathInformation [0]) (twoPathInformation [1]) ∧
      ¬RelativeSandwich η (twoPathInformation [0]) (twoPathInformation [1]) := by
  exact ⟨(both_common_singletons 0).1, (both_common_singletons 1).1,
    twoPath_dominated, (dominated_path_deletion_loses_cover hη).2.2.2⟩

/-- Distinct rational singular ranges persist inside the same two-base family. -/
theorem rational_singular_base_obstruction {ε : ℝ} (hε : 0 < ε) :
    ∃ t : ℚ, t ≠ 0 ∧
      (∀ i j, |tiltedRankOne (t : ℝ) i j - tiltedRankOne 0 i j| < ε) ∧
      ∀ c : ℝ, 0 < c →
        ¬Loewner (c • tiltedRankOne 0) (tiltedRankOne (t : ℝ)) ∧
        ¬Loewner (c • tiltedRankOne (t : ℝ)) (tiltedRankOne 0) :=
  arbitrarily_close_rational_distinct_ranges hε

end Boundaries
end MatroidSpectral
