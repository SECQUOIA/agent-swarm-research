import QipmFormal.Mixture.Centrality
import Mathlib.Analysis.SpecialFunctions.Arsinh

/-! # Finite ratio criteria for the SDP mixture certificate

These are scalar identities for the certificate `sqrt r * (kantorovich R - 1)`.
They characterize this worst-case common-parameter bound, not the centrality of
an individual mixture. In particular, point-centered centrality need not force
the ratio criterion. The nested square root is the positive fourth root of `r`.
-/

namespace QipmFormal.SDPMixture

open QipmFormal.Mixture

/-- The exact hyperbolic expression for the scalar Kantorovich defect. -/
theorem kantorovich_sub_one_eq_sinh_sq (R : ℝ) (hR : 0 < R) :
    kantorovich R - 1 = Real.sinh (Real.log R / 2) ^ 2 := by
  have h := Real.cosh_two_mul (x := Real.log R / 2)
  rw [show 2 * (Real.log R / 2) = Real.log R by ring,
    Real.cosh_log hR, Real.cosh_sq] at h
  unfold kantorovich
  field_simp at h ⊢
  nlinarith

/-- Exact finite threshold for the common-parameter Frobenius certificate. -/
theorem common_parameter_ratio_iff (r eta R : ℝ)
    (hr : 0 < r) (heta : 0 ≤ eta) (hR : 1 ≤ R) :
    Real.sqrt r * (kantorovich R - 1) ≤ eta ↔
      Real.log R ≤ 2 * Real.arsinh (Real.sqrt eta / Real.sqrt (Real.sqrt r)) := by
  have hRpos : 0 < R := lt_of_lt_of_le zero_lt_one hR
  have hrpos : 0 < Real.sqrt r := Real.sqrt_pos.mpr hr
  have hrrpos : 0 < Real.sqrt (Real.sqrt r) := Real.sqrt_pos.mpr hrpos
  have hsnonneg : 0 ≤ Real.sinh (Real.log R / 2) :=
    Real.sinh_nonneg_iff.mpr (div_nonneg (Real.log_nonneg hR) (by norm_num))
  have hqnonneg : 0 ≤ Real.sqrt eta / Real.sqrt (Real.sqrt r) := by positivity
  have hsq : (Real.sqrt eta / Real.sqrt (Real.sqrt r)) ^ 2 =
      eta / Real.sqrt r := by
    rw [div_pow, Real.sq_sqrt heta, Real.sq_sqrt hrpos.le]
  rw [kantorovich_sub_one_eq_sinh_sq R hRpos]
  calc
    Real.sqrt r * Real.sinh (Real.log R / 2) ^ 2 ≤ eta ↔
        Real.sinh (Real.log R / 2) ^ 2 ≤ eta / Real.sqrt r := by
          rw [le_div_iff₀ hrpos, mul_comm]
    _ ↔ Real.sinh (Real.log R / 2) ≤
        Real.sqrt eta / Real.sqrt (Real.sqrt r) := by
          rw [← hsq]
          exact sq_le_sq₀ hsnonneg hqnonneg
    _ ↔ Real.log R / 2 ≤
        Real.arsinh (Real.sqrt eta / Real.sqrt (Real.sqrt r)) := by
          simpa only [Real.sinh_arsinh] using
            (Real.sinh_le_sinh (x := Real.log R / 2)
              (y := Real.arsinh (Real.sqrt eta / Real.sqrt (Real.sqrt r))))
    _ ↔ Real.log R ≤
        2 * Real.arsinh (Real.sqrt eta / Real.sqrt (Real.sqrt r)) := by
          rw [div_le_iff₀ (by norm_num : (0 : ℝ) < 2), mul_comm]

/-- On nonnegative arguments, the inverse hyperbolic sine is at most identity. -/
theorem arsinh_le_self (x : ℝ) (hx : 0 ≤ x) : Real.arsinh x ≤ x := by
  have h := Real.self_le_sinh_iff.mpr (Real.arsinh_nonneg_iff.mpr hx)
  simpa only [Real.sinh_arsinh] using h

/-- A finite bound expressing the fourth-root dimension restriction. -/
theorem log_ratio_le_of_common_parameter_bound (r eta R : ℝ)
    (hr : 0 < r) (heta : 0 ≤ eta) (hR : 1 ≤ R)
    (hbound : Real.sqrt r * (kantorovich R - 1) ≤ eta) :
    Real.log R ≤ 2 * Real.sqrt eta / Real.sqrt (Real.sqrt r) := by
  have h := (common_parameter_ratio_iff r eta R hr heta hR).mp hbound
  have ha := arsinh_le_self (Real.sqrt eta / Real.sqrt (Real.sqrt r)) (by positivity)
  calc
    Real.log R ≤ 2 * Real.arsinh (Real.sqrt eta / Real.sqrt (Real.sqrt r)) := h
    _ ≤ 2 * (Real.sqrt eta / Real.sqrt (Real.sqrt r)) := by linarith
    _ = 2 * Real.sqrt eta / Real.sqrt (Real.sqrt r) := by ring

end QipmFormal.SDPMixture
