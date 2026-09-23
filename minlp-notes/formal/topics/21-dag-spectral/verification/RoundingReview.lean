import Formal.DAGSpectral.UpperTriangle
import Formal.DAGSpectral.Perturbation

open DAGSpectral
open Matrix
open scoped BigOperators

-- Signed rational floor, including a value strictly between -1 and 0.
example : floorLabel ((1 / 2 : ℚ) : ℝ) ((-1 / 3 : ℚ) : ℝ) = -1 := by
  rw [floorLabel_ratCast]
  norm_num

-- Empty paths need positive N, rather than a positive path length.
example : 0 ≤ ([] : List ℝ).sum - (1 / 2) * (pathLabel (1 / 2) [] : ℝ) ∧
    ([] : List ℝ).sum - (1 / 2) * (pathLabel (1 / 2) [] : ℝ) < 1 * (1 / 2) := by
  simpa only [Nat.cast_one] using
    path_residual_bounds (h := 1 / 2) (N := 1) (by norm_num) (by norm_num) [] (by simp)

-- Different lengths, a negative edge, and a shared signed profile.
example : |([-1 / 4, 1 / 4] : List ℝ).sum - ([-1 / 4] : List ℝ).sum| <
    (2 : ℝ) * (1 / 2) := by
  apply equal_label_sum_close (h := 1 / 2) (by norm_num) (by norm_num)
    [-1 / 4, 1 / 4] [-1 / 4] (by simp) (by simp)
  norm_num [pathLabel, floorLabel]

example : coordinateCount 1 1 1 (1 / 2) = 19 := by
  norm_num [coordinateCount]

example : (coordinateRange 1 1 (1 / 2)).card = 18 := by
  norm_num [coordinateRange, Int.card_Icc]
  rfl

example : Fintype.card (UpperCoord 0) = 0 := by
  rw [card_upperCoord]
example : Fintype.card (UpperCoord 3) = 6 := by
  rw [card_upperCoord]

example (D : RealMatrix 0) (x : Fin 0 → ℝ) :
    |x ⬝ᵥ (D *ᵥ x)| ≤ 0 := by
  have hb := entrywise_quadratic_bound D (a := 0) (by norm_num)
    (by intro i; exact Fin.elim0 i) x
  exact hb.trans_eq (by simp)

-- Singular information is retained by the kernel conclusion.
example {n : ℕ} {B : RealMatrix n} (hB : B.PosSemidef)
    (h : RelativeSandwich (1 / 2) (0 : RealMatrix n) B) (x : Fin n → ℝ) :
    B *ᵥ x = 0 := by
  exact (h.kernel_iff Matrix.PosSemidef.zero hB (by norm_num) x).mp (by simp)

#print axioms floorLabel_ratCast
#print axioms pathLabel_ratCast
#print axioms equal_label_sum_close
#print axioms coordinateRange_card_le
#print axioms card_upperCoord
#print axioms RelativeSandwich.kernel_iff
#print axioms relativeSandwich_of_entrywise
