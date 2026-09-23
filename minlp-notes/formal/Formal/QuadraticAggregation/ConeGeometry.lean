import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Topology.MetricSpace.HausdorffDistance
import Mathlib.Topology.Order.Compact

/-!
# Uniform separation of closed cones

The compact unit section of a closed cone has positive distance from a closed
set that meets the cone only at zero. Positive scaling extends this separation
to a homogeneous bound. This is the geometric content of Lemma 3 in the
quadratic aggregation note; finite generation is needed only to prove that the
coefficient cone is closed.
-/

namespace QuadraticAggregation

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [FiniteDimensional ℝ E]

/-- Closed cones meeting only at zero have a uniform positive angular separation.
The formulation uses distances to individual points, so no existence of a
nearest point or convexity assumption is required. -/
theorem exists_uniform_cone_separation {P D : Set E}
    (hP : IsClosed P) (hD : IsClosed D) (hD0 : (0 : E) ∈ D)
    (hPsmul : ∀ (a : ℝ), 0 ≤ a → ∀ p ∈ P, a • p ∈ P)
    (hDsmul : ∀ (a : ℝ), 0 ≤ a → ∀ d ∈ D, a • d ∈ D)
    (hPD : ∀ p ∈ P, p ∈ D → p = 0) :
    ∃ κ : ℝ, 0 < κ ∧ ∀ p ∈ P, ∀ d ∈ D, κ * ‖p‖ ≤ ‖p - d‖ := by
  have hcompact : IsCompact (Metric.sphere (0 : E) 1 ∩ P) :=
    (isCompact_sphere 0 1).inter_right hP
  obtain ⟨κ, hκ, hbound⟩ := hcompact.exists_forall_le'
    (Metric.continuous_infDist_pt D).continuousOn (a := 0) (by
      intro p hp
      apply (hD.notMem_iff_infDist_pos ⟨0, hD0⟩).mp
      intro hpd
      have hp0 := hPD p hp.2 hpd
      simpa [hp0] using hp.1)
  refine ⟨κ, hκ, ?_⟩
  intro p hp d hd
  by_cases hp0 : p = 0
  · simp [hp0]
  have hnorm : 0 < ‖p‖ := norm_pos_iff.mpr hp0
  have hunit : ‖p‖⁻¹ • p ∈ Metric.sphere (0 : E) 1 ∩ P := by
    refine ⟨?_, hPsmul _ (inv_nonneg.mpr hnorm.le) p hp⟩
    simp [norm_smul, hnorm.ne']
  have hd' := hDsmul _ (inv_nonneg.mpr hnorm.le) d hd
  have hb := (hbound _ hunit).trans (Metric.infDist_le_dist_of_mem hd')
  rw [dist_eq_norm, ← smul_sub, norm_smul, Real.norm_eq_abs,
    abs_of_nonneg (inv_nonneg.mpr hnorm.le)] at hb
  have hm := mul_le_mul_of_nonneg_left hb hnorm.le
  simpa only [← mul_assoc, mul_inv_cancel₀ hnorm.ne', one_mul, mul_comm ‖p‖ κ] using hm

/-- The distance-to-set version of uniform cone separation. -/
theorem exists_uniform_infDist_cone_separation {P D : Set E}
    (hP : IsClosed P) (hD : IsClosed D) (hD0 : (0 : E) ∈ D)
    (hPsmul : ∀ (a : ℝ), 0 ≤ a → ∀ p ∈ P, a • p ∈ P)
    (hDsmul : ∀ (a : ℝ), 0 ≤ a → ∀ d ∈ D, a • d ∈ D)
    (hPD : ∀ p ∈ P, p ∈ D → p = 0) :
    ∃ κ : ℝ, 0 < κ ∧ ∀ p ∈ P, κ * ‖p‖ ≤ Metric.infDist p D := by
  obtain ⟨κ, hκ, hsep⟩ :=
    exists_uniform_cone_separation hP hD hD0 hPsmul hDsmul hPD
  refine ⟨κ, hκ, ?_⟩
  intro p hp
  exact (Metric.le_infDist ⟨0, hD0⟩).mpr fun d hd ↦ by
    simpa [dist_eq_norm] using hsep p hp d hd

end QuadraticAggregation
