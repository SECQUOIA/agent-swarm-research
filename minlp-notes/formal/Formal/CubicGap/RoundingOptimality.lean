import Formal.MultilinearGap.MonomialEnvelope
import Mathlib.Analysis.SpecificLimits.Basic

/-! Feasible marginal configurations and limiting obstructions for fixed mixtures
of endpoint orientation, independent rounding, and low/high rounding. -/
namespace CubicGap
namespace RoundingOptimality
open Filter Real
open scoped Topology
noncomputable section

/-- Positive parameters tending to zero, with every term at most one eighth. -/
def smallParameter (n : ℕ) : ℝ := 1 / ((n : ℝ) + 8)

theorem smallParameter_bounds (n : ℕ) :
    0 < smallParameter n ∧ smallParameter n ≤ 1 / 8 := by
  have hn : (0 : ℝ) ≤ n := Nat.cast_nonneg n
  constructor
  · exact div_pos (by norm_num) (by linarith)
  · apply (div_le_iff₀ (by linarith : (0 : ℝ) < n + 8)).mpr
    linarith

theorem tendsto_smallParameter : Tendsto smallParameter atTop (𝓝 0) := by
  exact tendsto_const_nhds.div_atTop
    (tendsto_atTop_add_const_right atTop 8 tendsto_natCast_atTop_atTop)

/-- The one-low cubic obstruction is an actual cube point for every parameter. -/
def oneLowPoint (t : ℝ) : Fin 3 → ℝ := ![t, 1 - t ^ 2, 1 - t ^ 2]

/-- The all-high cubic obstruction approaches its classification boundary from above. -/
def allHighPoint (t : ℝ) : Fin 3 → ℝ := ![1 / 2 + t, 1 - (1 / 2 + t) / 2, 1 - (1 / 2 + t) / 2]

theorem oneLowPoint_cube (t : ℝ) (ht : 0 < t) (ht8 : t ≤ 1 / 8) :
    oneLowPoint t ∈ cube (Fin 3) := by
  intro i
  fin_cases i <;> simp [oneLowPoint, abs_of_pos ht] <;> constructor <;> nlinarith [sq_nonneg t]

theorem oneLowPoint_sorted (t : ℝ) (ht : 0 < t) (ht8 : t ≤ 1 / 8) :
    t ≤ 1 - t ^ 2 ∧ t ≤ 1 / 2 ∧ 1 / 2 < 1 - t ^ 2 := by
  constructor
  · nlinarith [sq_nonneg t]
  constructor <;> nlinarith [sq_nonneg t]

theorem allHighPoint_cube (t : ℝ) (ht : 0 < t) (ht8 : t ≤ 1 / 8) :
    allHighPoint t ∈ cube (Fin 3) := by
  intro i
  fin_cases i <;> simp [allHighPoint] <;> constructor <;> linarith

theorem allHighPoint_sorted (t : ℝ) (ht : 0 < t) (ht8 : t ≤ 1 / 8) :
    1 / 2 < 1 / 2 + t ∧ 1 / 2 + t ≤ 1 - (1 / 2 + t) / 2 := by
  constructor <;> linarith

/-- Evaluation of the three deficiency formulas on the one-low curve. -/
theorem oneLow_normalized_formulas (t : ℝ) (ht : 0 < t) (ht8 : t ≤ 1 / 8) :
    (min t (t ^ 2) / 2 + min t (t ^ 2) / 4) / min t (t ^ 2 + t ^ 2) = 3 / 8 ∧
    (t * (t ^ 2 + t ^ 2 - t ^ 2 * t ^ 2)) / min t (t ^ 2 + t ^ 2) = t - t ^ 3 / 2 ∧
    (min t (2 * t ^ 2) / 2 + min t (2 * t ^ 2) / 4) / min t (t ^ 2 + t ^ 2) = 3 / 4 := by
  have ht2 : t ^ 2 ≤ t := by nlinarith
  have ht22 : 2 * t ^ 2 ≤ t := by nlinarith
  have htadd : t ^ 2 + t ^ 2 ≤ t := by nlinarith
  rw [min_eq_right ht2, min_eq_right ht22, min_eq_right htadd]
  have htne : t ≠ 0 := ht.ne'
  constructor
  · field_simp; ring
  constructor <;> field_simp <;> ring

/-- Evaluation on the all-high curve, whose smallest mean is `1/2+t`. -/
theorem allHigh_normalized_formulas (t : ℝ) (ht : 0 < t) (ht8 : t ≤ 1 / 8) :
    (((1 / 2 + t) / 2) / 2 + ((1 / 2 + t) / 2) / 4) /
      min (1 / 2 + t) ((1 / 2 + t) / 2 + (1 / 2 + t) / 2) = 3 / 8 ∧
    ((1 / 2 + t) * ((1 / 2 + t) / 2 + (1 / 2 + t) / 2 - ((1 / 2 + t) / 2) * ((1 / 2 + t) / 2))) / 
      min (1 / 2 + t) ((1 / 2 + t) / 2 + (1 / 2 + t) / 2) = (1 / 2 + t) - (1 / 2 + t) ^ 2 / 4 := by
  have hu : (0 : ℝ) < 1 / 2 + t := by linarith
  have hsum : (1 / 2 + t) / 2 + (1 / 2 + t) / 2 = 1 / 2 + t := by ring
  rw [hsum, min_self]
  constructor <;> field_simp <;> ring

/-- The independent-rounding fraction tends to zero on the one-low sequence. -/
theorem tendsto_oneLow_independent :
    Tendsto (fun n => smallParameter n - (smallParameter n) ^ 3 / 2) atTop (𝓝 0) := by
  simpa using tendsto_smallParameter.sub ((tendsto_smallParameter.pow 3).div_const 2)

/-- The independent-rounding fraction tends to `7/16` on the all-high sequence. -/
theorem tendsto_allHigh_independent :
    Tendsto (fun n => (1 / 2 + smallParameter n) - (1 / 2 + smallParameter n) ^ 2 / 4)
      atTop (𝓝 (7 / 16)) := by
  have hu : Tendsto (fun n => (1 / 2 : ℝ) + smallParameter n) atTop (𝓝 (1 / 2)) := by
    simpa using tendsto_const_nhds.add tendsto_smallParameter
  convert hu.sub ((hu.pow 2).div_const 4) using 1
  norm_num

/-- Applying a uniform estimate on the two feasible sequences gives both limit constraints. -/
theorem limit_constraints (w r v α : ℝ)
    (hone : ∀ n, α ≤ 3 * w / 8 + r * (smallParameter n - (smallParameter n) ^ 3 / 2) + 3 * v / 4)
    (hhigh : ∀ n, α ≤
      3 * w / 8 + r * ((1 / 2 + smallParameter n) -
        (1 / 2 + smallParameter n) ^ 2 / 4) + 3 * v / 8) :
    α ≤ 3 * w / 8 + 3 * v / 4 ∧ α ≤ 3 * w / 8 + 7 * r / 16 + 3 * v / 8 := by
  constructor
  · have hlim := ((tendsto_const_nhds (x := 3 * w / 8)).add
      (tendsto_oneLow_independent.const_mul r)).add
      (tendsto_const_nhds (x := 3 * v / 4))
    have h := ge_of_tendsto' hlim hone
    simpa using h
  · have hlim := ((tendsto_const_nhds (x := 3 * w / 8)).add
      (tendsto_allHigh_independent.const_mul r)).add
      (tendsto_const_nhds (x := 3 * v / 8))
    have h := ge_of_tendsto' hlim hhigh
    nlinarith [h]

/-- The linear obstruction produced by the three feasible limiting configurations. -/
theorem weighted_obstruction (w r v α : ℝ) (hsum : w + r + v = 1)
    (hbilinear : α ≤ w / 2 + r / 2)
    (honeLow : α ≤ 3 * w / 8 + 3 * v / 4)
    (hallHigh : α ≤ 3 * w / 8 + 7 * r / 16 + 3 * v / 8) :
    α ≤ 12 / 31 := by
  linarith

/-- Equality forces precisely the advertised weights. -/
theorem optimal_weights_unique (w r v : ℝ) (hsum : w + r + v = 1)
    (hbilinear : 12 / 31 ≤ w / 2 + r / 2)
    (honeLow : 12 / 31 ≤ 3 * w / 8 + 3 * v / 4)
    (hallHigh : 12 / 31 ≤ 3 * w / 8 + 7 * r / 16 + 3 * v / 8) :
    w = 18 / 31 ∧ r = 6 / 31 ∧ v = 7 / 31 := by
  constructor
  · linarith
  constructor <;> linarith

end
end RoundingOptimality
end CubicGap
