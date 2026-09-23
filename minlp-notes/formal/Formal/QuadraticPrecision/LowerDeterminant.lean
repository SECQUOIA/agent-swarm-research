import Formal.QuadraticPrecision.LowerVolume
import Mathlib.Analysis.SpecialFunctions.Log.Base

/-! Exact determinant constants and logarithmic lower bounds for graph lifts. -/
open MeasureTheory
namespace QuadraticPrecision
noncomputable section

/-- The explicit coefficient in the determinant obstruction. -/
def determinantErrorConstant (d : ℕ) (Δ V : ℝ) : ℝ :=
  Δ ^ (1 / (d : ℝ)) * V ^ (2 / (d : ℝ)) / (48 * Real.sqrt d)

theorem determinantErrorConstant_pos {d : ℕ} (hd : 0 < d) {Δ V : ℝ}
    (hΔ : 0 < Δ) (hV : 0 < V) : 0 < determinantErrorConstant d Δ V := by
  unfold determinantErrorConstant
  have hrd : (0 : ℝ) < d := by exact_mod_cast hd
  positivity

/-- The exact contact-volume inequality in logarithmic form. -/
theorem determinant_volume_log_lower {d p : ℕ} (hd : 0 < d) {Δ V ε : ℝ}
    (hΔ : 0 < Δ) (hV : 0 < V) (hε : 0 < ε)
    (hv : V ≤ (2 : ℝ) ^ p * ((2 : ℝ) ^ d *
      (12 * Real.sqrt d * ε) ^ ((d : ℝ) / 2) / Real.sqrt Δ)) :
    (d : ℝ) / 2 * Real.logb 2 (1 / ε) +
      (d : ℝ) / 2 * Real.logb 2 (determinantErrorConstant d Δ V) ≤ p := by
  have hrd : (0 : ℝ) < d := by exact_mod_cast hd
  have hs : 0 < Real.sqrt d := Real.sqrt_pos.mpr hrd
  have hsΔ : 0 < Real.sqrt Δ := Real.sqrt_pos.mpr hΔ
  have hL : 0 < 12 * Real.sqrt d := by positivity
  have hlog := (Real.logb_le_logb (by norm_num : (1 : ℝ) < 2) hV (by positivity)).mpr hv
  rw [Real.logb_mul (by positivity) (by positivity),
    Real.logb_div (by positivity) (ne_of_gt hsΔ),
    Real.logb_mul (by positivity) (by positivity),
    Real.logb_pow, Real.logb_pow,
    Real.logb_rpow_eq_mul_logb_of_pos (mul_pos hL hε),
    Real.logb_mul (ne_of_gt hL) (ne_of_gt hε), Real.sqrt_eq_rpow Δ,
    Real.logb_rpow_eq_mul_logb_of_pos hΔ] at hlog
  norm_num [Real.logb_self_eq_one] at hlog
  have hfour : Real.logb 2 (4 : ℝ) = 2 := by
    have h := Real.logb_pow 2 2 2
    norm_num [Real.logb_self_eq_one] at h
    exact h
  have hden : 48 * Real.sqrt d = 4 * (12 * Real.sqrt d) := by ring
  have hc : (d : ℝ) / 2 * Real.logb 2 (determinantErrorConstant d Δ V) =
      Real.logb 2 V + Real.logb 2 Δ / 2 - d -
        (d : ℝ) / 2 * Real.logb 2 (12 * Real.sqrt d) := by
    rw [determinantErrorConstant, Real.logb_div (by positivity) (by positivity),
      Real.logb_mul (by positivity) (by positivity),
      Real.logb_rpow_eq_mul_logb_of_pos hΔ,
      Real.logb_rpow_eq_mul_logb_of_pos hV, hden,
      Real.logb_mul (by norm_num) (ne_of_gt hL), hfour]
    field_simp
    ring
  rw [hc]
  simp only [one_div, Real.logb_inv]
  linarith

/-- Convert a logarithmic count obstruction to the exact exponential error bound. -/
theorem error_lower_of_log_lower {d p : ℕ} (hd : 0 < d) {C ε : ℝ}
    (hC : 0 < C) (hε : 0 < ε)
    (h : (d : ℝ) / 2 * Real.logb 2 (1 / ε) +
      (d : ℝ) / 2 * Real.logb 2 C ≤ p) :
    C * (2 : ℝ) ^ (-2 * (p : ℝ) / (d : ℝ)) ≤ ε := by
  have hrd : (0 : ℝ) < d := by exact_mod_cast hd
  apply (Real.logb_le_logb (by norm_num : (1 : ℝ) < 2) (by positivity) hε).mp
  rw [Real.logb_mul (ne_of_gt hC) (by positivity), Real.logb_rpow (by norm_num) (by norm_num)]
  have hh : (d : ℝ) / 2 * (Real.logb 2 C - Real.logb 2 ε) ≤ p := by
    simp only [one_div, Real.logb_inv] at h
    linarith
  apply (le_of_mul_le_mul_left ?_ hrd)
  have he : (d : ℝ) * (Real.logb 2 C + -2 * (p : ℝ) / (d : ℝ)) =
      (d : ℝ) * Real.logb 2 C - 2 * p := by field_simp; ring
  rw [he]
  linarith

/-- Any graph lift of a nonsingular quadratic on a positive-volume compact
set has strictly positive error. -/
theorem graph_quadratic_error_pos {d p : ℕ} (hd : 0 < d) {D : Set (Input d)}
    (hD : IsCompact D) (hvol : volume D ≠ 0)
    (M : Matrix (Fin d) (Fin d) ℝ) (hM : M.IsSymm) (hdet : M.det ≠ 0)
    (a : Fin d → ℝ) (b ε : ℝ) (hε : 0 ≤ ε)
    (h : HasGraphLift D (quadraticPolynomial M a b) ε p) : 0 < ε := by
  have hv := graph_quadratic_volume_bound hD M hM hdet a b ε hε h
  have hrd : (0 : ℝ) < d := by exact_mod_cast hd
  have hex : (d : ℝ) / 2 ≠ 0 := ne_of_gt (by positivity)
  by_contra hn
  have hz : ε = 0 := by linarith
  simp only [hz, mul_zero, Real.zero_rpow hex, zero_div, ENNReal.ofReal_zero] at hv
  exact hvol (le_antisymm hv zero_le)

/-- The determinant lower bound in the logarithmic form used by precision rates. -/
theorem graph_quadratic_log_lower {d p : ℕ} (hd : 0 < d) {D : Set (Input d)}
    (hD : IsCompact D) (hvol : volume D ≠ 0)
    (M : Matrix (Fin d) (Fin d) ℝ) (hM : M.IsSymm) (hdet : M.det ≠ 0)
    (a : Fin d → ℝ) (b ε : ℝ) (hε : 0 ≤ ε)
    (h : HasGraphLift D (quadraticPolynomial M a b) ε p) :
    (d : ℝ) / 2 * Real.logb 2 (1 / ε) +
      (d : ℝ) / 2 * Real.logb 2
        (determinantErrorConstant d |M.det| (volume D).toReal) ≤ p := by
  have he := graph_quadratic_error_pos hd hD hvol M hM hdet a b ε hε h
  have hv := graph_quadratic_volume_bound hD M hM hdet a b ε hε h
  have hv' := ENNReal.toReal_mono ENNReal.ofReal_ne_top hv
  rw [ENNReal.toReal_ofReal (by positivity)] at hv'
  exact determinant_volume_log_lower hd (abs_pos.mpr hdet)
    (ENNReal.toReal_pos hvol hD.measure_lt_top.ne) he hv'

/-- The explicit determinant obstruction, with the paper's constant 48√d. -/
theorem graph_quadratic_error_lower {d p : ℕ} (hd : 0 < d) {D : Set (Input d)}
    (hD : IsCompact D) (hvol : volume D ≠ 0)
    (M : Matrix (Fin d) (Fin d) ℝ) (hM : M.IsSymm) (hdet : M.det ≠ 0)
    (a : Fin d → ℝ) (b ε : ℝ) (hε : 0 ≤ ε)
    (h : HasGraphLift D (quadraticPolynomial M a b) ε p) :
    determinantErrorConstant d |M.det| (volume D).toReal *
      (2 : ℝ) ^ (-2 * (p : ℝ) / (d : ℝ)) ≤ ε := by
  exact error_lower_of_log_lower hd
    (determinantErrorConstant_pos hd (abs_pos.mpr hdet)
      (ENNReal.toReal_pos hvol hD.measure_lt_top.ne))
    (graph_quadratic_error_pos hd hD hvol M hM hdet a b ε hε h)
    (graph_quadratic_log_lower hd hD hvol M hM hdet a b ε hε h)

end
end QuadraticPrecision
