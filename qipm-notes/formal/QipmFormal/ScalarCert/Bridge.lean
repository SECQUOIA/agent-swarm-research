import QipmFormal.ScalarCert.Inverse

/-!
# Bridge to the original `x` coordinate

`eq:scalar-elementary` introduces `v = √2 x / √(1+x²)`.  This file proves the
algebraic half of the correspondence with the barrier

  `b t = -log (1 - t²)`,        `b' t = 2t/(1-t²)`,

namely that in the `x` coordinate

  `P (vOf x) = 2x/(1-x²) = b' x`,
  `A (vOf x) = √2 √(1+x²) / (1-x²)`.

Together with `Y (vOf x) = ρ x` (the remaining, analytic half — see
`Elasticity.lean` for `Y'`) these are the identities
`P v = p (Y v)` and `A v = p' (Y v)` of the paper, since `p = b' ∘ ρ⁻¹`.
-/

namespace QipmFormal.ScalarCert

open Real Set

/-- The barrier `b t = -log(1-t²)` of `02-exact-distance.tex`. -/
noncomputable def bb (t : ℝ) : ℝ := -Real.log (1 - t ^ 2)

/-- The coordinate change `v = √2 x / √(1+x²)` of `eq:scalar-elementary`. -/
noncomputable def vOf (x : ℝ) : ℝ := √2 * x / √(1 + x ^ 2)

lemma one_add_sq_pos (x : ℝ) : (0:ℝ) < 1 + x ^ 2 := by positivity

lemma sqrt_one_add_sq_pos' (x : ℝ) : (0:ℝ) < √(1 + x ^ 2) :=
  Real.sqrt_pos.mpr (one_add_sq_pos x)

lemma sq_sqrt_one_add (x : ℝ) : (√(1 + x ^ 2)) ^ 2 = 1 + x ^ 2 :=
  Real.sq_sqrt (one_add_sq_pos x).le

/-- `(vOf x)² = 2x²/(1+x²)`. -/
lemma vOf_sq (x : ℝ) : (vOf x) ^ 2 = 2 * x ^ 2 / (1 + x ^ 2) := by
  rw [vOf, div_pow, mul_pow, Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2), sq_sqrt_one_add]

lemma one_sub_vOf_sq (x : ℝ) : 1 - (vOf x) ^ 2 = (1 - x ^ 2) / (1 + x ^ 2) := by
  rw [vOf_sq]
  field_simp
  ring

lemma two_sub_vOf_sq (x : ℝ) : 2 - (vOf x) ^ 2 = 2 / (1 + x ^ 2) := by
  rw [vOf_sq]
  field_simp
  ring

/-- `√(2 - (vOf x)²) = √2 / √(1+x²)`. -/
lemma sqrt_two_sub_vOf_sq (x : ℝ) : √(2 - (vOf x) ^ 2) = √2 / √(1 + x ^ 2) := by
  rw [two_sub_vOf_sq, Real.sqrt_div (by norm_num : (0:ℝ) ≤ 2)]

/-- `vOf` maps `(-1,1)` into `(-1,1)`. -/
lemma vOf_lt_one {x : ℝ} (hx : |x| < 1) : |vOf x| < 1 := by
  have h1 : (0:ℝ) < 1 - x ^ 2 := by
    obtain ⟨h1, h2⟩ := abs_lt.mp hx; nlinarith
  have hs : 1 - (vOf x) ^ 2 > 0 := by
    rw [one_sub_vOf_sq]; positivity
  have hlt : (vOf x) ^ 2 < 1 := by linarith
  exact (sq_lt_one_iff_abs_lt_one _).mp hlt

/-- `A (vOf x) = √2 √(1+x²)/(1-x²)`. -/
theorem A_vOf {x : ℝ} (hx : |x| < 1) :
    A (vOf x) = √2 * √(1 + x ^ 2) / (1 - x ^ 2) := by
  have h1 : (0:ℝ) < 1 - x ^ 2 := by
    obtain ⟨h1, h2⟩ := abs_lt.mp hx; nlinarith
  have hs : (0:ℝ) < √(1 + x ^ 2) := sqrt_one_add_sq_pos' x
  rw [A, sqrt_two_sub_vOf_sq, one_sub_vOf_sq]
  field_simp
  linear_combination -sq_sqrt_one_add x

/-- `P (vOf x) = 2x/(1-x²)`, which is `b' x`. -/
theorem P_vOf {x : ℝ} (hx : |x| < 1) : P (vOf x) = 2 * x / (1 - x ^ 2) := by
  have h1 : (0:ℝ) < 1 - x ^ 2 := by
    obtain ⟨h1, h2⟩ := abs_lt.mp hx; nlinarith
  have hs : (0:ℝ) < √(1 + x ^ 2) := sqrt_one_add_sq_pos' x
  have h2 : (√2 : ℝ) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  rw [P, A_vOf hx, vOf]
  field_simp
  linear_combination x * h2

/-- `b' t = 2t/(1-t²)`. -/
theorem bb_hasDerivAt {t : ℝ} (ht : |t| < 1) :
    HasDerivAt bb (2 * t / (1 - t ^ 2)) t := by
  have h1 : (0:ℝ) < 1 - t ^ 2 := by
    obtain ⟨h1, h2⟩ := abs_lt.mp ht; nlinarith
  have hd : HasDerivAt (fun u : ℝ => 1 - u ^ 2) (-(2 * t)) t := by
    simpa using ((hasDerivAt_pow 2 t).const_sub 1)
  have h := (hd.log h1.ne').neg
  have hrw : -(-(2 * t) / (1 - t ^ 2)) = 2 * t / (1 - t ^ 2) := by ring
  rw [← hrw]
  exact h

/-- `P (vOf x)` is exactly the derivative of the barrier at `x`. -/
theorem P_vOf_eq_bb_deriv {x : ℝ} (hx : |x| < 1) :
    P (vOf x) = deriv bb x := by
  rw [P_vOf hx, (bb_hasDerivAt hx).deriv]

end QipmFormal.ScalarCert
