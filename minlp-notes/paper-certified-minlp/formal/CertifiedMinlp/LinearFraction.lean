import Mathlib.Analysis.Convex.Deriv
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Inv

/-! Exact one-variable linear-fraction recognition on a convex denominator-sign domain. -/

namespace CertifiedMinlp

noncomputable section

def linearFraction (a b c d x : ℝ) : ℝ := (a * x + b) / (c * x + d)

theorem linearFraction_decomposition (a b c d x : ℝ) (hc : c ≠ 0)
    (hx : c * x + d ≠ 0) :
    linearFraction a b c d x = a / c + (b - a * d / c) / (c * x + d) := by
  unfold linearFraction
  have hx' : x * c + d ≠ 0 := by simpa only [mul_comm x c] using hx
  field_simp [hc, hx, hx']
  ring

theorem linearFraction_hasDerivAt (a b c d x : ℝ) (hx : c * x + d ≠ 0) :
    HasDerivAt (linearFraction a b c d)
      ((a * d - b * c) / (c * x + d) ^ 2) x := by
  convert (((hasDerivAt_id x).const_mul a).add_const b).div
    (((hasDerivAt_id x).const_mul c).add_const d) hx using 1 <;>
    first | rfl | (dsimp only [id_eq]; ring)

theorem linearFraction_slope_hasDerivAt (a b c d x : ℝ)
    (hx : c * x + d ≠ 0) :
    HasDerivAt (fun y : ℝ => (a * d - b * c) / (c * y + d) ^ 2)
      (-(2 * c * (a * d - b * c)) / (c * x + d) ^ 3) x := by
  convert (hasDerivAt_const x (a * d - b * c)).div
    ((((hasDerivAt_id x).const_mul c).add_const d).pow 2)
    (pow_ne_zero 2 hx) using 1 <;>
    first | rfl | (dsimp only [id_eq, Pi.pow_apply]; field_simp; ring)

theorem linearFraction_second_derivative (a b c d x : ℝ) (hc : c ≠ 0)
    (hx : c * x + d ≠ 0) :
    deriv (deriv (linearFraction a b c d)) x =
      2 * (b - a * d / c) * c ^ 2 / (c * x + d) ^ 3 := by
  have hn : ∀ᶠ y in nhds x, c * y + d ≠ 0 :=
    (((continuous_id.const_mul c).add continuous_const).continuousAt.eventually_ne hx)
  have he : deriv (linearFraction a b c d) =ᶠ[nhds x]
      (fun y => (a * d - b * c) / (c * y + d) ^ 2) :=
    hn.mono fun y hy => (linearFraction_hasDerivAt a b c d y hy).deriv
  rw [he.deriv_eq, (linearFraction_slope_hasDerivAt a b c d x hx).deriv]
  field_simp
  ring

theorem linearFraction_convexOn {D : Set ℝ} (hD : Convex ℝ D)
    (a b c d : ℝ) (hc : c ≠ 0)
    (hden : ∀ x ∈ D, c * x + d ≠ 0)
    (hsign : ∀ x ∈ D, 0 ≤ (b - a * d / c) / (c * x + d) ^ 3) :
    ConvexOn ℝ D (linearFraction a b c d) := by
  apply convexOn_of_hasDerivWithinAt2_nonneg hD
    (fun x hx => (linearFraction_hasDerivAt a b c d x (hden x hx)).continuousAt.continuousWithinAt)
    (fun x hx => (linearFraction_hasDerivAt a b c d x
      (hden x (interior_subset hx))).hasDerivWithinAt)
    (fun x hx => (linearFraction_slope_hasDerivAt a b c d x
      (hden x (interior_subset hx))).hasDerivWithinAt)
  intro x hx
  have he : -(2 * c * (a * d - b * c)) / (c * x + d) ^ 3 =
      2 * c ^ 2 * ((b - a * d / c) / (c * x + d) ^ 3) := by
    field_simp
    ring
  rw [he]
  exact mul_nonneg (mul_nonneg (by norm_num) (sq_nonneg c)) (hsign x (interior_subset hx))

theorem linearFraction_concaveOn {D : Set ℝ} (hD : Convex ℝ D)
    (a b c d : ℝ) (hc : c ≠ 0)
    (hden : ∀ x ∈ D, c * x + d ≠ 0)
    (hsign : ∀ x ∈ D, (b - a * d / c) / (c * x + d) ^ 3 ≤ 0) :
    ConcaveOn ℝ D (linearFraction a b c d) := by
  apply concaveOn_of_hasDerivWithinAt2_nonpos hD
    (fun x hx => (linearFraction_hasDerivAt a b c d x (hden x hx)).continuousAt.continuousWithinAt)
    (fun x hx => (linearFraction_hasDerivAt a b c d x
      (hden x (interior_subset hx))).hasDerivWithinAt)
    (fun x hx => (linearFraction_slope_hasDerivAt a b c d x
      (hden x (interior_subset hx))).hasDerivWithinAt)
  intro x hx
  have he : -(2 * c * (a * d - b * c)) / (c * x + d) ^ 3 =
      2 * c ^ 2 * ((b - a * d / c) / (c * x + d) ^ 3) := by
    field_simp
    ring
  rw [he]
  exact mul_nonpos_of_nonneg_of_nonpos
    (mul_nonneg (by norm_num) (sq_nonneg c)) (hsign x (interior_subset hx))

theorem linearFraction_zero_residual (a b c d x : ℝ) (hc : c ≠ 0)
    (hx : c * x + d ≠ 0) (hk : b - a * d / c = 0) :
    linearFraction a b c d x = a / c := by
  rw [linearFraction_decomposition a b c d x hc hx, hk]
  simp

theorem linearFraction_constant_denominator (a b d x : ℝ) :
    linearFraction a b 0 d x = a / d * x + b / d := by
  simp only [linearFraction, zero_mul, zero_add, add_div]
  ring

theorem linearFraction_convex_positive {D : Set ℝ} (hD : Convex ℝ D)
    (a b c d : ℝ) (hc : c ≠ 0) (hk : 0 ≤ b - a * d / c)
    (hden : ∀ x ∈ D, 0 < c * x + d) : ConvexOn ℝ D (linearFraction a b c d) := by
  apply linearFraction_convexOn hD a b c d hc
    (fun x hx => ne_of_gt (hden x hx))
  exact fun x hx => div_nonneg hk (le_of_lt (pow_pos (hden x hx) 3))

theorem linearFraction_convex_negative {D : Set ℝ} (hD : Convex ℝ D)
    (a b c d : ℝ) (hc : c ≠ 0) (hk : b - a * d / c ≤ 0)
    (hden : ∀ x ∈ D, c * x + d < 0) : ConvexOn ℝ D (linearFraction a b c d) := by
  apply linearFraction_convexOn hD a b c d hc
    (fun x hx => ne_of_lt (hden x hx))
  intro x hx
  exact div_nonneg_of_nonpos hk (le_of_lt (Odd.pow_neg (by decide : Odd 3) (hden x hx)))

theorem linearFraction_concave_positive {D : Set ℝ} (hD : Convex ℝ D)
    (a b c d : ℝ) (hc : c ≠ 0) (hk : b - a * d / c ≤ 0)
    (hden : ∀ x ∈ D, 0 < c * x + d) : ConcaveOn ℝ D (linearFraction a b c d) := by
  apply linearFraction_concaveOn hD a b c d hc
    (fun x hx => ne_of_gt (hden x hx))
  exact fun x hx => div_nonpos_of_nonpos_of_nonneg hk (le_of_lt (pow_pos (hden x hx) 3))

theorem linearFraction_concave_negative {D : Set ℝ} (hD : Convex ℝ D)
    (a b c d : ℝ) (hc : c ≠ 0) (hk : 0 ≤ b - a * d / c)
    (hden : ∀ x ∈ D, c * x + d < 0) : ConcaveOn ℝ D (linearFraction a b c d) := by
  apply linearFraction_concaveOn hD a b c d hc
    (fun x hx => ne_of_lt (hden x hx))
  intro x hx
  exact div_nonpos_of_nonneg_of_nonpos hk
    (le_of_lt (Odd.pow_neg (by decide : Odd 3) (hden x hx)))

theorem linearFraction_constant_denominator_curvature {D : Set ℝ} (hD : Convex ℝ D)
    (a b d : ℝ) :
    ConvexOn ℝ D (linearFraction a b 0 d) ∧
      ConcaveOn ℝ D (linearFraction a b 0 d) := by
  have he (x y u v : ℝ) (huv : u + v = 1) :
      linearFraction a b 0 d (u * x + v * y) =
        u * linearFraction a b 0 d x + v * linearFraction a b 0 d y := by
    simp only [linearFraction_constant_denominator]
    linear_combination -(b / d) * huv
  exact ⟨⟨hD, fun x _ y _ u v _ _ huv => le_of_eq (he x y u v huv)⟩,
    ⟨hD, fun x _ y _ u v _ _ huv => le_of_eq (he x y u v huv).symm⟩⟩

end

end CertifiedMinlp
