import QipmFormal.ScalarCert.Bridge
import QipmFormal.ScalarCert.Elasticity

/-!
# `Y (vOf x) = ρ x`, the analytic half of `eq:scalar-elementary`

The paper defines, in the original `x` coordinate,

  `ρ x = ∫₀ˣ √(2(1+u²))/(1-u²) du`,

and asserts that the `v`-coordinate function `Y v = 2 artanh v - √2 artanh (v/√2)`
is `ρ` read through the substitution `v = vOf x = √2 x/√(1+x²)`.

This file proves that identity on `(-1,1)`.  The chain rule gives

  `(Y ∘ vOf)' x = Y' (vOf x) · vOf' x
               = (1+x²)²/(1-x²) · √2/((1+x²)√(1+x²))
               = √(2(1+x²))/(1-x²)`,

which is the integrand of `ρ` and also equals `A (vOf x)`; the fundamental
theorem of calculus on `[[0, x]] ⊆ (-1,1)` then finishes the proof, since
`vOf 0 = 0` and `Y 0 = 0`.
-/

namespace QipmFormal.ScalarCert

open Real Set

/-- `ρ x = ∫₀ˣ √(2(1+u²))/(1-u²) du`, the paper's `ρ`. -/
noncomputable def rho (x : ℝ) : ℝ := ∫ u in (0 : ℝ)..x, √(2 * (1 + u ^ 2)) / (1 - u ^ 2)

@[simp] lemma vOf_zero : vOf 0 = 0 := by simp [vOf]

@[simp] lemma rho_zero : rho 0 = 0 := by simp [rho]

/-! ### The derivative of the coordinate change -/

/-- `vOf' x = √2 / ((1+x²) √(1+x²))`. -/
theorem vOf_hasDerivAt (x : ℝ) :
    HasDerivAt vOf (√2 / ((1 + x ^ 2) * √(1 + x ^ 2))) x := by
  have hpos : (0 : ℝ) < 1 + x ^ 2 := one_add_sq_pos x
  have hs : (0 : ℝ) < √(1 + x ^ 2) := sqrt_one_add_sq_pos' x
  have hsq : (√(1 + x ^ 2)) ^ 2 = 1 + x ^ 2 := sq_sqrt_one_add x
  have hnum : HasDerivAt (fun y : ℝ => √2 * y) (√2) x := by
    simpa using (hasDerivAt_id x).const_mul (√2)
  have hinner : HasDerivAt (fun y : ℝ => 1 + y ^ 2) (2 * x) x := by
    simpa using (hasDerivAt_pow 2 x).const_add (1 : ℝ)
  have hden : HasDerivAt (fun y : ℝ => √(1 + y ^ 2)) (x / √(1 + x ^ 2)) x := by
    have h := (Real.hasDerivAt_sqrt hpos.ne').comp x hinner
    rw [Function.comp_def] at h
    exact h.congr_deriv (by field_simp)
  have h := hnum.div hden hs.ne'
  refine (h.congr_deriv ?_).congr_of_eventuallyEq (.of_forall fun y => rfl)
  rw [hsq, div_eq_div_iff (by positivity) (by positivity)]
  field_simp
  linear_combination hsq

/-! ### The derivative of `Y ∘ vOf` -/

/-- The chain-rule value: `Y' (vOf x) · vOf' x = √(2(1+x²))/(1-x²)`. -/
lemma chain_value {x : ℝ} (hx : |x| < 1) :
    2 / ((1 - (vOf x) ^ 2) * (2 - (vOf x) ^ 2)) * (√2 / ((1 + x ^ 2) * √(1 + x ^ 2)))
      = √(2 * (1 + x ^ 2)) / (1 - x ^ 2) := by
  have h1 : (0 : ℝ) < 1 - x ^ 2 := by
    obtain ⟨ha, hb⟩ := abs_lt.mp hx; nlinarith
  have hpos : (0 : ℝ) < 1 + x ^ 2 := one_add_sq_pos x
  have hs : (0 : ℝ) < √(1 + x ^ 2) := sqrt_one_add_sq_pos' x
  have hsq : (√(1 + x ^ 2)) ^ 2 = 1 + x ^ 2 := sq_sqrt_one_add x
  rw [one_sub_vOf_sq, two_sub_vOf_sq, Real.sqrt_mul (by norm_num : (0 : ℝ) ≤ 2)]
  field_simp
  ring_nf
  exact hsq.symm

/-- `(Y ∘ vOf)' x = √(2(1+x²))/(1-x²)`, the integrand of `ρ`. -/
theorem Y_vOf_hasDerivAt {x : ℝ} (hx : |x| < 1) :
    HasDerivAt (fun u : ℝ => Y (vOf u)) (√(2 * (1 + x ^ 2)) / (1 - x ^ 2)) x := by
  have h := (Y_deriv (vOf_lt_one hx)).comp x (vOf_hasDerivAt x)
  rw [Function.comp_def] at h
  exact h.congr_deriv (chain_value hx)

/-! ### The fundamental theorem of calculus -/

lemma abs_lt_one_of_mem_uIcc {x u : ℝ} (hx : |x| < 1) (hu : u ∈ uIcc (0 : ℝ) x) :
    |u| < 1 := by
  obtain ⟨ha, hb⟩ := abs_lt.mp hx
  rw [Set.mem_uIcc] at hu
  rw [abs_lt]
  rcases hu with ⟨h1, h2⟩ | ⟨h1, h2⟩ <;> constructor <;> linarith

lemma rho_integrand_continuousOn {x : ℝ} (hx : |x| < 1) :
    ContinuousOn (fun u : ℝ => √(2 * (1 + u ^ 2)) / (1 - u ^ 2)) (uIcc (0 : ℝ) x) := by
  refine ContinuousOn.div ?_ ?_ ?_
  · exact (Real.continuous_sqrt.comp (by continuity)).continuousOn
  · fun_prop
  · intro u hu
    obtain ⟨ha, hb⟩ := abs_lt.mp (abs_lt_one_of_mem_uIcc hx hu)
    nlinarith

/-- **`Y` is `ρ` in the transformed coordinate**: for `|x| < 1`,
`Y (vOf x) = ∫₀ˣ √(2(1+u²))/(1-u²) du`. -/
theorem Y_vOf_eq_rho {x : ℝ} (hx : |x| < 1) : Y (vOf x) = rho x := by
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt
    (f := fun u : ℝ => Y (vOf u))
    (f' := fun u : ℝ => √(2 * (1 + u ^ 2)) / (1 - u ^ 2))
    (fun u hu => Y_vOf_hasDerivAt (abs_lt_one_of_mem_uIcc hx hu))
    ((rho_integrand_continuousOn hx).intervalIntegrable)
  rw [rho, h, vOf_zero, Y_zero, sub_zero]

/-! ### `A ∘ vOf` is `ρ'` -/

/-- `A (vOf x)` is exactly the integrand of `ρ`, i.e. `ρ' x`. -/
theorem A_vOf_eq_rho_deriv {x : ℝ} (hx : |x| < 1) :
    A (vOf x) = √(2 * (1 + x ^ 2)) / (1 - x ^ 2) := by
  rw [A_vOf hx, Real.sqrt_mul (by norm_num : (0 : ℝ) ≤ 2)]

/-- `ρ` is differentiable on `(-1,1)` with derivative `A ∘ vOf`. -/
theorem rho_hasDerivAt {x : ℝ} (hx : |x| < 1) :
    HasDerivAt rho (A (vOf x)) x := by
  rw [A_vOf_eq_rho_deriv hx]
  refine (Y_vOf_hasDerivAt hx).congr_of_eventuallyEq ?_
  obtain ⟨ha, hb⟩ := abs_lt.mp hx
  filter_upwards [Ioo_mem_nhds ha hb] with y hy
  exact (Y_vOf_eq_rho (abs_lt.mpr ⟨hy.1, hy.2⟩)).symm

end QipmFormal.ScalarCert
