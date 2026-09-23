import QipmFormal.ScalarCert.Defs

/-!
# Power series for `artanh` and for the transform `Y`

`Y z = Σ_{k} (2 - 2^{-k}) z^{2k+1} / (2k+1)`, the series `eq:Y-rational-series`
of `appendix-scalar-certificate.tex`.  The `√2` cancels exactly, which is why
the paper works with this series rather than with the logarithms directly.
-/

namespace QipmFormal.ScalarCert

open Real

/-- Power series for `artanh` on `(-1,1)`. -/
theorem hasSum_artanh {x : ℝ} (h : |x| < 1) :
    HasSum (fun k : ℕ => (1 / (2 * (k : ℝ) + 1)) * x ^ (2 * k + 1)) (artanh x) := by
  obtain ⟨hx1, hx2⟩ := abs_lt.mp h
  have h1p : (0 : ℝ) < 1 + x := by linarith
  have h1m : (0 : ℝ) < 1 - x := by linarith
  have hEq : artanh x = 1 / 2 * (log (1 + x) - log (1 - x)) := by
    rw [artanh_eq_half_log ⟨hx1.le, hx2.le⟩, Real.log_div h1p.ne' h1m.ne']
  rw [hEq]
  have := (hasSum_log_sub_log_of_abs_lt_one h).mul_left (1 / 2)
  refine this.congr_fun ?_
  intro k
  ring

/-- `(√2)^(2k+1) = 2^k * √2`. -/
lemma sqrt_two_pow (k : ℕ) : (√2 : ℝ) ^ (2 * k + 1) = 2 ^ k * √2 := by
  rw [pow_succ, pow_mul, Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2)]

/-- The series of `eq:Y-rational-series`. -/
theorem hasSum_Y {v : ℝ} (h : |v| < 1) :
    HasSum (fun k : ℕ => (2 - (1/2 : ℝ) ^ k) / (2 * (k : ℝ) + 1) * v ^ (2 * k + 1)) (Y v) := by
  have h2 : (0:ℝ) < √2 := Real.sqrt_pos.mpr (by norm_num)
  have hw : |v / √2| < 1 := by
    rw [abs_div, abs_of_pos h2]
    rw [div_lt_one h2]
    calc |v| < 1 := h
      _ ≤ √2 := by
          rw [show (1:ℝ) = √1 by simp]
          exact Real.sqrt_le_sqrt (by norm_num)
  have hA := (hasSum_artanh h).mul_left 2
  have hB := (hasSum_artanh hw).mul_left (√2)
  have := hA.sub hB
  rw [show Y v = 2 * artanh v - √2 * artanh (v / √2) from rfl]
  refine this.congr_fun ?_
  intro k
  have hden : (2 * (k:ℝ) + 1) ≠ 0 := by positivity
  have hsne : (√2 : ℝ) ≠ 0 := h2.ne'
  have h2k : ((2:ℝ)) ^ k ≠ 0 := by positivity
  have hpow : (v / √2) ^ (2 * k + 1) = v ^ (2 * k + 1) / (2 ^ k * √2) := by
    rw [div_pow, sqrt_two_pow]
  have hhalf : ((1:ℝ) / 2) ^ k = 1 / 2 ^ k := by
    rw [div_pow, one_pow]
  rw [hpow, hhalf]
  field_simp

end QipmFormal.ScalarCert
