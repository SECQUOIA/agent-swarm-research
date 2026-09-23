import Formal.DAGSpectral.ProfileCount
import Mathlib.Algebra.BigOperators.Fin

/-! The independent coordinates of a symmetric r-by-r matrix. -/
namespace DAGSpectral
open scoped BigOperators

/-- A column followed by a row no larger than the column. -/
def UpperCoord (r : ℕ) := Σ j : Fin r, Fin (j.val + 1)

instance (r : ℕ) : Fintype (UpperCoord r) :=
  inferInstanceAs (Fintype (Σ j : Fin r, Fin (j.val + 1)))

/-- These indices are exactly the upper-triangular matrix entries. -/
def upperCoordEquiv (r : ℕ) : UpperCoord r ≃ {ij : Fin r × Fin r // ij.1 ≤ ij.2} where
  toFun z := ⟨(⟨z.2.val, by have := z.2.isLt; have := z.1.isLt; omega⟩, z.1),
    by change z.2.val ≤ z.1.val; omega⟩
  invFun z := ⟨z.val.2, ⟨z.val.1.val, by
    have := z.property
    change z.val.1.val ≤ z.val.2.val at this
    omega⟩⟩
  left_inv z := by cases z; rfl
  right_inv z := by cases z; rfl

private theorem twice_sum_initial (r : ℕ) :
    2 * (∑ j : Fin r, (j.val + 1)) = r * (r + 1) := by
  induction r with
  | zero => simp
  | succ r ih =>
    rw [Fin.sum_univ_castSucc]
    simp only [Fin.val_castSucc, Fin.val_last]
    nlinarith

theorem card_upperCoord (r : ℕ) : Fintype.card (UpperCoord r) = r * (r + 1) / 2 := by
  have hc : Fintype.card (UpperCoord r) = ∑ j : Fin r, (j.val + 1) := by
    change Fintype.card (Σ j : Fin r, Fin (j.val + 1)) = _
    convert Fintype.card_sigma (α := fun j : Fin r => Fin (j.val + 1)) using 1
    simp
  rw [hc, ← twice_sum_initial r, Nat.mul_div_cancel_left _ (by decide : 0 < 2)]

noncomputable def upperCoordIndex (r : ℕ) : UpperCoord r ≃ Fin (r * (r + 1) / 2) :=
  Fintype.equivFinOfCardEq (card_upperCoord r)

/-- The exact upper-triangle exponent in the state count. -/
theorem card_upper_profiles_le (p r N : ℕ) {η : ℝ}
    (hr : 0 < r) (hN : 0 < N) (hη : 0 < η) :
    Fintype.card (DAGSpectral.BoundedProfile (r * (r + 1) / 2)
      (coordinateRange p N (spectralMesh η r N))) ≤
      coordinateCount p r N η ^ (r * (r + 1) / 2) :=
  card_spectral_profiles_le _ p r N hr hN hη

end DAGSpectral
