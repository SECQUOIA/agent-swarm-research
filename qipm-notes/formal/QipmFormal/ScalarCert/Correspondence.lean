import QipmFormal.ScalarCert.Rho

/-!
# The correspondence of `eq:scalar-elementary`

Collects the three identities that connect the closed forms `Y`, `A`, `P`
used throughout this development to the paper's original objects: the barrier
`b t = -log(1-t²)`, the arclength `ρ x = ∫₀ˣ √(2(1+u²))/(1-u²) du`, and
`p = b' ∘ ρ⁻¹`.

With `v = vOf x = √2 x/√(1+x²)`:

* `Y (vOf x) = ρ x`                  — so `Y` is `ρ` in the transformed coordinate;
* `HasDerivAt ρ (A (vOf x)) x`       — so `A ∘ vOf = ρ'`;
* `P (vOf x) = b' x`                 — so `P ∘ vOf = b'`.

The last two are exactly `A = p' ∘ Y` and `P = p ∘ Y`: by definition
`p (ρ x) = b' x`, and differentiating `p ∘ ρ = b'` gives
`p' (ρ x) = b'' x / ρ' x = ρ' x`, because
`b'' x = 2(1+x²)/(1-x²)²` and `ρ' x = √(2(1+x²))/(1-x²)`.
-/

namespace QipmFormal.ScalarCert

open Real Set

/-- `b'' t = 2(1+t²)/(1-t²)²`. -/
theorem bb_hasDerivAt_deriv {t : ℝ} (ht : |t| < 1) :
    HasDerivAt (fun u : ℝ => 2 * u / (1 - u ^ 2)) (2 * (1 + t ^ 2) / (1 - t ^ 2) ^ 2) t := by
  have h1 : (0:ℝ) < 1 - t ^ 2 := by
    obtain ⟨ha, hb⟩ := abs_lt.mp ht; nlinarith
  have hnum : HasDerivAt (fun u : ℝ => 2 * u) 2 t := by
    simpa using (hasDerivAt_id t).const_mul (2:ℝ)
  have hden : HasDerivAt (fun u : ℝ => 1 - u ^ 2) (-(2 * t)) t := by
    simpa using ((hasDerivAt_pow 2 t).const_sub 1)
  have h := hnum.div hden h1.ne'
  have heq : (2 * (1 - t ^ 2) - 2 * t * -(2 * t)) / (1 - t ^ 2) ^ 2
      = 2 * (1 + t ^ 2) / (1 - t ^ 2) ^ 2 := by ring
  rw [heq] at h
  exact h

/-- `p' (ρ x) = b'' x / ρ' x = ρ' x`, the identity behind `A = p' ∘ Y`. -/
theorem bb_second_div_rho_deriv {x : ℝ} (hx : |x| < 1) :
    2 * (1 + x ^ 2) / (1 - x ^ 2) ^ 2 / (√(2 * (1 + x ^ 2)) / (1 - x ^ 2))
      = √(2 * (1 + x ^ 2)) / (1 - x ^ 2) := by
  have h1 : (0:ℝ) < 1 - x ^ 2 := by
    obtain ⟨ha, hb⟩ := abs_lt.mp hx; nlinarith
  have hpos : (0:ℝ) < 2 * (1 + x ^ 2) := by positivity
  have hs : (0:ℝ) < √(2 * (1 + x ^ 2)) := Real.sqrt_pos.mpr hpos
  have hsq : √(2 * (1 + x ^ 2)) * √(2 * (1 + x ^ 2)) = 2 * (1 + x ^ 2) :=
    Real.mul_self_sqrt hpos.le
  field_simp
  nlinarith [hsq, h1, hs]

/-- `ρ` is strictly increasing on `(-1,1)`. -/
theorem rho_strictMonoOn : StrictMonoOn rho (Ioo (-1 : ℝ) 1) := by
  refine strictMonoOn_of_deriv_pos (convex_Ioo _ _) ?_ ?_
  · intro x hx
    exact ((rho_hasDerivAt (abs_lt.mpr hx)).continuousAt).continuousWithinAt
  · intro x hx
    rw [interior_Ioo] at hx
    have hx' : |x| < 1 := abs_lt.mpr hx
    rw [(rho_hasDerivAt hx').deriv]
    exact A_pos (vOf_lt_one hx')

/-- **The correspondence of `eq:scalar-elementary`.**
With `v = vOf x = √2 x/√(1+x²)` and `|x| < 1`. -/
theorem scalar_elementary {x : ℝ} (hx : |x| < 1) :
    Y (vOf x) = rho x ∧
    HasDerivAt rho (A (vOf x)) x ∧
    P (vOf x) = deriv bb x :=
  ⟨Y_vOf_eq_rho hx, rho_hasDerivAt hx, P_vOf_eq_bb_deriv hx⟩

end QipmFormal.ScalarCert
