import Mathlib.Data.Int.Interval
import Mathlib.Algebra.Order.Floor.Ring
import Mathlib.Algebra.BigOperators.Group.List.Basic
import Mathlib.Data.Rat.Floor
import Mathlib.Tactic

/-! Signed floor labels and residual bounds for paths of bounded length. -/
namespace DAGSpectral
noncomputable section

def floorLabel (h x : ℝ) : ℤ := ⌊x / h⌋
def pathLabel (h : ℝ) (xs : List ℝ) : ℤ := (xs.map (floorLabel h)).sum

theorem floor_residual {h : ℝ} (hh : 0 < h) (x : ℝ) :
    0 ≤ x - h * (floorLabel h x : ℝ) ∧ x - h * (floorLabel h x : ℝ) < h := by
  have h₁ := Int.floor_le (x / h)
  have h₂ := Int.lt_floor_add_one (x / h)
  rw [le_div_iff₀ hh] at h₁
  rw [div_lt_iff₀ hh] at h₂
  unfold floorLabel
  constructor <;> nlinarith

theorem path_residual_nonneg {h : ℝ} (hh : 0 < h) (xs : List ℝ) :
    0 ≤ xs.sum - h * (pathLabel h xs : ℝ) := by
  induction xs with
  | nil => simp [pathLabel]
  | cons x xs ih =>
    have hx := (floor_residual hh x).1
    simp only [pathLabel, List.map_cons, List.sum_cons, Int.cast_add] at *
    linarith

theorem path_residual_lt_length {h : ℝ} (hh : 0 < h) (xs : List ℝ)
    (hne : xs ≠ []) :
    xs.sum - h * (pathLabel h xs : ℝ) < xs.length * h := by
  induction xs with
  | nil => contradiction
  | cons x xs ih =>
    have hx := (floor_residual hh x).2
    by_cases hn : xs = []
    · subst xs
      simpa [pathLabel] using hx
    · have hi := ih hn
      simp only [pathLabel, List.map_cons, List.sum_cons, Int.cast_add,
        List.length_cons, Nat.cast_add, Nat.cast_one] at *
      linarith

/-- Empty and unequal-length paths are included; positive N supplies strictness. -/
theorem path_residual_bounds {h : ℝ} (hh : 0 < h) {N : ℕ} (hN : 0 < N)
    (xs : List ℝ) (hlen : xs.length ≤ N) :
    0 ≤ xs.sum - h * (pathLabel h xs : ℝ) ∧
      xs.sum - h * (pathLabel h xs : ℝ) < N * h := by
  refine ⟨path_residual_nonneg hh xs, ?_⟩
  by_cases hn : xs = []
  · subst xs
    simp only [pathLabel, List.map_nil, List.sum_nil, Int.cast_zero, mul_zero, sub_zero]
    positivity
  · exact (path_residual_lt_length hh xs hn).trans_le
      (mul_le_mul_of_nonneg_right (by exact_mod_cast hlen) hh.le)

/-- Equal signed floor profiles control differences, without positivity of entries. -/
theorem equal_label_sum_close {h : ℝ} (hh : 0 < h) {N : ℕ} (hN : 0 < N)
    (xs ys : List ℝ) (hx : xs.length ≤ N) (hy : ys.length ≤ N)
    (heq : pathLabel h xs = pathLabel h ys) : |xs.sum - ys.sum| < N * h := by
  obtain ⟨hlx, hux⟩ := path_residual_bounds hh hN xs hx
  obtain ⟨hly, huy⟩ := path_residual_bounds hh hN ys hy
  rw [heq] at hlx hux
  exact abs_lt.mpr ⟨by linarith, by linarith⟩

/-- The mesh used in a rank-r trial. -/
def spectralMesh (η : ℝ) (r N : ℕ) : ℝ := η / (r * N)

theorem spectralMesh_pos {η : ℝ} (hη : 0 < η) {r N : ℕ}
    (hr : 0 < r) (hN : 0 < N) : 0 < spectralMesh η r N := by
  unfold spectralMesh
  positivity

theorem rank_mul_mesh {η : ℝ} {r N : ℕ} (hr : 0 < r) (hN : 0 < N) :
    (r : ℝ) * N * spectralMesh η r N = η := by
  unfold spectralMesh
  field_simp

/-- Exact rational arithmetic gives precisely the same labels as real arithmetic. -/
theorem floorLabel_ratCast (h x : ℚ) :
    floorLabel (h : ℝ) (x : ℝ) = ⌊x / h⌋ := by
  unfold floorLabel
  rw [← Rat.cast_div, Rat.floor_cast]

theorem pathLabel_ratCast (h : ℚ) (xs : List ℚ) :
    pathLabel (h : ℝ) (xs.map (fun x : ℚ => (x : ℝ))) =
      (xs.map (fun x => ⌊x / h⌋)).sum := by
  induction xs with
  | nil => simp [pathLabel]
  | cons x xs ih =>
    simpa only [pathLabel, List.map_cons, List.sum_cons, floorLabel_ratCast] using
      congrArg (fun z => ⌊x / h⌋ + z) ih

end
end DAGSpectral
