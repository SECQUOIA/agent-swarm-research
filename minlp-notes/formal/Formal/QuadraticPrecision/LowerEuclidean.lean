import Formal.QuadraticPrecision.LowerCurvature
import Formal.QuadraticPrecision.LowerDeterminant
import Mathlib.MeasureTheory.Measure.Lebesgue.VolumeOfBalls

open MeasureTheory
open scoped BigOperators Matrix
namespace QuadraticPrecision
noncomputable section

/-- Euclidean unit-ball volume in dimension d. -/
def unitBallVolume (d : ℕ) : ℝ :=
  (volume (Metric.closedBall (0 : EuclideanSpace ℝ (Fin d)) 1)).toReal

theorem unitBallVolume_pos (d : ℕ) : 0 < unitBallVolume d := by
  apply ENNReal.toReal_pos
  · exact ne_of_gt (Metric.measure_closedBall_pos volume 0 (by norm_num : (0:ℝ)<1))
  · exact (isCompact_closedBall (0 : EuclideanSpace ℝ (Fin d)) 1).measure_lt_top.ne

theorem euclidean_image_compact {d : ℕ} {S : Set (Input d)} (hS : IsCompact S) :
    IsCompact (WithLp.toLp 2 '' S : Set (EuclideanSpace ℝ (Fin d))) := by
  exact hS.image (PiLp.continuous_toLp 2 _)

theorem euclidean_image_volume {d : ℕ} {S : Set (Input d)} (hS : IsCompact S) :
    volume (WithLp.toLp 2 '' S : Set (EuclideanSpace ℝ (Fin d))) = volume S := by
  have he := (PiLp.volume_preserving_toLp (Fin d)).measure_preimage
    (euclidean_image_compact hS).measurableSet.nullMeasurableSet
  simpa only [Set.preimage_image_eq _ (WithLp.toLp_injective 2)] using he.symm

theorem negative_contact_euclidean_distance {d : ℕ} (M : Matrix (Fin d) (Fin d) ℝ)
    {μ ε : ℝ} (hμ : 0 < μ)
    (hcurv : ∀ v : Input d, μ * ∑ i, (v i)^2 ≤ -(v ⬝ᵥ M.mulVec v))
    {x y : Input d} (hcontact : -contactQuadratic M (x-y) ≤ 4*ε) :
    dist (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin d)) (WithLp.toLp 2 y) ≤
      Real.sqrt (8*ε/μ) := by
  rw [EuclideanSpace.dist_eq]
  apply Real.sqrt_le_sqrt
  simpa only [Real.dist_eq, sq_abs] using negative_contact_sum_sq M hμ hcurv hcontact

/-- Exact scalar coefficient in the strong-curvature obstruction. -/
def curvatureErrorConstant (d : ℕ) (μ V : ℝ) : ℝ :=
  (μ/2) * (V/unitBallVolume d)^((2:ℝ)/d)

theorem curvatureErrorConstant_pos {d : ℕ} {μ V : ℝ} (hμ : 0 < μ) (hV : 0 < V) :
    0 < curvatureErrorConstant d μ V := by
  unfold curvatureErrorConstant
  have := unitBallVolume_pos d
  positivity

theorem curvature_volume_log_lower {d p : ℕ} (hd : 0 < d) {μ V ε : ℝ}
    (hμ : 0 < μ) (hV : 0 < V) (hε : 0 < ε)
    (hv : V ≤ (2 : ℝ) ^ p * unitBallVolume d * (Real.sqrt (8 * ε / μ) / 2) ^ d) :
    (d:ℝ)/2 * Real.logb 2 (1/ε) +
      (d:ℝ)/2 * Real.logb 2 (curvatureErrorConstant d μ V) ≤ p := by
  have hrd : (0:ℝ) < d := by exact_mod_cast hd
  have ho := unitBallVolume_pos d
  have hl := (Real.logb_le_logb (by norm_num : (1:ℝ)<2) hV (by positivity)).mpr hv
  rw [Real.logb_mul (by positivity) (by positivity),
    Real.logb_mul (by positivity) ho.ne', Real.logb_pow, Real.logb_pow,
    Real.logb_div (by positivity) (by norm_num), Real.sqrt_eq_rpow,
    Real.logb_rpow_eq_mul_logb_of_pos (by positivity),
    Real.logb_div (by positivity) hμ.ne', Real.logb_mul (by norm_num) hε.ne'] at hl
  have h8 : Real.logb 2 (8:ℝ) = 3 := by
    have hh := Real.logb_pow 2 2 3
    norm_num [Real.logb_self_eq_one] at hh
    exact hh
  norm_num [Real.logb_self_eq_one, h8] at hl
  have hc : (d:ℝ)/2 * Real.logb 2 (curvatureErrorConstant d μ V) =
      (d:ℝ)/2 * (Real.logb 2 μ - 1) + Real.logb 2 V - Real.logb 2 (unitBallVolume d) := by
    rw [curvatureErrorConstant, Real.logb_mul (by positivity) (by positivity),
      Real.logb_div hμ.ne' (by norm_num),
      Real.logb_rpow_eq_mul_logb_of_pos (by positivity),
      Real.logb_div hV.ne' ho.ne']
    norm_num [Real.logb_self_eq_one]
    field_simp
    ring
  rw [hc]
  simp only [one_div, Real.logb_inv]
  nlinarith
end
end QuadraticPrecision
