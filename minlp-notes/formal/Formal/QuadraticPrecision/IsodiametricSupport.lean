import Formal.QuadraticPrecision.IsodiametricWeight
import Mathlib.MeasureTheory.Measure.Support

/-! A weighted-volume excess supplies a genuine support point outside a ball. -/
open Set MeasureTheory Metric
noncomputable section
namespace QuadraticPrecision.Isodiametric
open IsodiametricWeight
variable {E : Type*} [NormedAddCommGroup E]
  [SecondCountableTopology E] [MeasureSpace E] [BorelSpace E]

lemma exists_support_outside_ball {K : Set E} {r C : ℝ}
    (hbig : weightedMeasure C (closedBall (0 : E) r) < weightedMeasure C K) :
    ∃ x ∈ (volume.restrict K).support, r < ‖x‖ := by
  have hpos : 0 < volume (K \ closedBall (0 : E) r) := by
    by_contra! hn
    have hz : volume (K \ closedBall (0 : E) r) = 0 := le_antisymm hn (zero_le)
    have hwz : weightedMeasure C (K \ closedBall (0 : E) r) = 0 :=
      withDensity_absolutelyContinuous volume _ hz
    have hle := measure_le_inter_add_sdiff (weightedMeasure (E := E) C) K
      (closedBall 0 r)
    rw [hwz, add_zero] at hle
    exact (not_le.mpr hbig) (hle.trans (measure_mono inter_subset_right))
  have hp : 0 < volume.restrict K ((closedBall (0 : E) r)ᶜ) := by
    rw [Measure.restrict_apply measurableSet_closedBall.compl]
    have heq : (closedBall (0 : E) r)ᶜ ∩ K = K \ closedBall 0 r := by
      ext x
      simp only [mem_inter_iff, mem_compl_iff, mem_sdiff]
      tauto
    rw [heq]
    exact hpos
  obtain ⟨x, hx, hs⟩ := (volume.restrict K).nonempty_inter_support_of_pos hp
  refine ⟨x, hs, ?_⟩
  simpa only [mem_compl_iff, mem_closedBall, dist_zero_right, not_le] using hx

end QuadraticPrecision.Isodiametric
