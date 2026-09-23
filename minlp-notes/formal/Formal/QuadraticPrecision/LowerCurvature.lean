import Formal.QuadraticPrecision.LowerVolume
import Mathlib.Analysis.SpecialFunctions.Log.Base
open MeasureTheory
open scoped BigOperators Matrix
namespace QuadraticPrecision

/-- Squared Euclidean contact distance, before choosing a normed-space model. -/
theorem negative_contact_sum_sq {d : ℕ} (M : Matrix (Fin d) (Fin d) ℝ)
    {μ ε : ℝ} (hμ : 0 < μ)
    (hcurv : ∀ v : Input d, μ * ∑ i, (v i)^2 ≤ -(v ⬝ᵥ M.mulVec v))
    {x y : Input d} (hcontact : -contactQuadratic M (x-y) ≤ 4*ε) :
    (∑ i, (x i-y i)^2) ≤ 8*ε/μ := by
  apply (le_div_iff₀ hμ).mpr
  have hc := hcurv (x-y)
  dsimp [contactQuadratic] at hcontact
  simp only [Pi.sub_apply] at hc
  nlinarith

/-- A negative Hessian bound turns every same-parity contact into a small
Euclidean diameter. It also bounds the coordinate supremum distance. -/
theorem negative_contact_distance {d : ℕ} (M : Matrix (Fin d) (Fin d) ℝ)
    {μ ε : ℝ} (hμ : 0 < μ) (_hε : 0 ≤ ε)
    (hcurv : ∀ v : Input d, μ * ∑ i, (v i)^2 ≤ -(v ⬝ᵥ M.mulVec v))
    {x y : Input d} (hcontact : -contactQuadratic M (x-y) ≤ 4*ε) :
    dist x y ≤ Real.sqrt (8*ε/μ) := by
  apply (dist_pi_le_iff (Real.sqrt_nonneg _)).mpr
  intro i
  have hs : (x i-y i)^2 ≤ ∑ j, ((x-y) j)^2 := by
    exact Finset.single_le_sum (fun j _ => sq_nonneg ((x-y) j)) (Finset.mem_univ i)
  have hb : (x i-y i)^2 ≤ 8*ε/μ :=
    hs.trans (negative_contact_sum_sq M hμ hcurv hcontact)
  rw [Real.dist_eq]
  exact Real.abs_le_sqrt hb

/-- An elementary diameter estimate already gives the optimal precision
exponent. The sharper ball-volume constant is a separate geometric result. -/
theorem epigraph_negative_volume_bound {d p : ℕ} {D : Set (Input d)}
    (hD : IsCompact D) (M : Matrix (Fin d) (Fin d) ℝ)
    (a : Fin d → ℝ) (b ε μ : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε)
    (hcurv : ∀ v : Input d, μ * ∑ i, (v i)^2 ≤ -(v ⬝ᵥ M.mulVec v))
    (h : HasEpigraphLift D (quadraticPolynomial M a b) ε p) :
    volume D ≤ ENNReal.ofReal ((2:ℝ)^p * (Real.sqrt (8*ε/μ))^d) := by
  obtain ⟨S,_,_,hcover,he⟩ := epigraph_quadratic_parity_cover hD M a b ε h
  calc
    volume D ≤ volume (⋃ α, S α) := measure_mono hcover
    _ ≤ ∑ α, volume (S α) := measure_iUnion_fintype_le volume S
    _ ≤ ∑ _α : ParityCode p, ENNReal.ofReal ((Real.sqrt (8*ε/μ))^d) := by
      apply Finset.sum_le_sum
      intro α _
      calc
        volume (S α) ≤ Metric.ediam (S α)^d := by simpa using Real.volume_pi_le_diam_pow (S α)
        _ ≤ (ENNReal.ofReal (Real.sqrt (8*ε/μ)))^d := by
          apply pow_le_pow_left'
          exact Metric.ediam_le_of_forall_dist_le (fun x hx y hy =>
            negative_contact_distance M hμ hε hcurv (he α x hx y hy))
        _ = _ := (ENNReal.ofReal_pow (Real.sqrt_nonneg _) _).symm
    _ = _ := by
      rw [Finset.sum_const, Finset.card_univ, card_parityCode, nsmul_eq_mul]
      rw [← ENNReal.ofReal_natCast, ← ENNReal.ofReal_mul (by positivity)]
      simp

/-- Logarithmic lower bound from the elementary contact diameter estimate. -/
theorem epigraph_negative_log_bound {d p : ℕ} {D : Set (Input d)}
    (hD : IsCompact D) (hvol : 0 < (volume D).toReal)
    (M : Matrix (Fin d) (Fin d) ℝ) (a : Fin d → ℝ) (b ε μ : ℝ)
    (hμ : 0 < μ) (hε : 0 < ε)
    (hcurv : ∀ v : Input d, μ * ∑ i, (v i)^2 ≤ -(v ⬝ᵥ M.mulVec v))
    (h : HasEpigraphLift D (quadraticPolynomial M a b) ε p) :
    (d:ℝ)/2 * Real.logb 2 (1/ε) +
      (Real.logb 2 (volume D).toReal - (d:ℝ)/2 * Real.logb 2 (8/μ)) ≤ p := by
  have hv := epigraph_negative_volume_bound hD M a b ε μ hμ hε.le hcurv h
  have hr : 0 < (2:ℝ)^p * Real.sqrt (8*ε/μ)^d := by positivity
  have hv' := ENNReal.toReal_le_of_le_ofReal hr.le hv
  have hl := (Real.logb_le_logb (by norm_num : (1:ℝ)<2) hvol hr).mpr hv'
  rw [Real.logb_mul (by positivity) (by positivity), Real.logb_pow,
    Real.logb_pow, Real.logb_self_eq_one (by norm_num : (1:ℝ) < 2), mul_one, Real.sqrt_eq_rpow,
    Real.logb_rpow_eq_mul_logb_of_pos (by positivity)] at hl
  have heq : 8*ε/μ = (8/μ)*ε := by ring
  rw [heq, Real.logb_mul (by positivity) hε.ne'] at hl
  simp only [one_div, Real.logb_inv]
  nlinarith
end QuadraticPrecision
