import Formal.QuadraticPrecision.IsodiametricReflection
import Formal.QuadraticPrecision.IsodiametricWeight
import Formal.QuadraticPrecision.IsodiametricPolarizationMeasure

open Set MeasureTheory Metric
open scoped InnerProductSpace

namespace QuadraticPrecision.Isodiametric

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]

lemma exists_strict_polarization {K : Set E} {D R C : ℝ} (hK : IsCompact K)
    (hKR : K ⊆ closedBall 0 R) (hR : 0 ≤ R) (hD : 0 ≤ D)
    (hdiam : ∀ a ∈ K, ∀ b ∈ K, dist a b ≤ D) (hC : R ^ 2 < C)
    {x : E} (hx : x ∈ (volume.restrict K).support) (hxn : D / 2 < ‖x‖) :
    ∃ e : E, ∃ t : ℝ, ‖e‖ = 1 ∧ 0 < t ∧
      IsodiametricWeight.weightedMeasure C K <
        IsodiametricWeight.weightedMeasure C
          (polarize (reflect e t) {z | ⟪e, z⟫_ℝ ≤ t} K) := by
  obtain ⟨e, t, he, ht, htx, hnorm, hdist⟩ := exists_improving_reflection hD hxn
  have hxK : x ∈ K := by
    have hh := (Measure.support_restrict_subset (μ := volume) (s := K)) hx
    simpa [hK.isClosed.closure_eq] using hh.1
  have hrx : reflect e t x ∉ K := fun hh => (not_le.mpr hdist) (hdiam x hxK _ hh)
  let w : E → ℝ := IsodiametricWeight.weight C
  have hwx : w x < w (reflect e t x) := by
    have hxR : ‖x‖ ≤ R := by simpa using hKR hxK
    have hs : ‖x‖ ^ 2 ≤ R ^ 2 := (sq_le_sq₀ (norm_nonneg _) hR).mpr hxR
    have hsq : ‖reflect e t x‖ ^ 2 < ‖x‖ ^ 2 :=
      (sq_lt_sq₀ (norm_nonneg _) (norm_nonneg _)).mpr hnorm
    dsimp [w, IsodiametricWeight.weight]
    rw [max_eq_right (by linarith : 0 ≤ C - ‖x‖ ^ 2),
      max_eq_right (by linarith : 0 ≤ C - ‖reflect e t x‖ ^ 2)]
    linarith
  let U := {z | reflect e t z ∉ K ∧ t < ⟪e, z⟫_ℝ ∧ w z < w (reflect e t z)}
  have hU : IsOpen U := by
    apply IsOpen.inter (hK.isClosed.isOpen_compl.preimage (reflect_continuous e t))
    exact (isOpen_lt (continuous_const : Continuous (fun _ : E => t))
      (continuous_const.inner continuous_id)).inter
      (isOpen_lt (IsodiametricWeight.continuous_weight C)
        ((IsodiametricWeight.continuous_weight C).comp (reflect_continuous e t)))
  have hxU : x ∈ U := ⟨hrx, htx, hwx⟩
  have hposU : 0 < volume (U ∩ K) := by
    have hh := (Measure.mem_support_iff_forall x).mp hx U (hU.mem_nhds hxU)
    rwa [Measure.restrict_apply hU.measurableSet] at hh
  let H := {z : E | ⟪e, z⟫_ℝ ≤ t}
  let B := {z | z ∈ H ∧ z ∉ K ∧ reflect e t z ∈ K ∧ w (reflect e t z) < w z}
  have hH : MeasurableSet H :=
    (isClosed_le (continuous_const.inner continuous_id) continuous_const).measurableSet
  have hB : MeasurableSet B := by
    exact hH.inter (hK.measurableSet.compl.inter
      ((hK.measurableSet.preimage (reflect_continuous e t).measurable).inter
        (isOpen_lt ((IsodiametricWeight.continuous_weight C).comp
          (reflect_continuous e t)) (IsodiametricWeight.continuous_weight C)).measurableSet))
  have hsub : U ∩ K ⊆ reflect e t ⁻¹' B := by
    intro z hz
    refine ⟨?_, hz.1.1, ?_, ?_⟩
    · change ⟪e, reflect e t z⟫_ℝ ≤ t
      rw [inner_reflect he]
      linarith [hz.1.2.1]
    · simpa only [reflect_involutive he t z] using hz.2
    · simpa only [reflect_involutive he t z] using hz.1.2.2
  have hposB : 0 < volume B := by
    have hh := hposU.trans_le (measure_mono hsub)
    rwa [(reflect_measurePreserving he t).measure_preimage hB.nullMeasurableSet] at hh
  have hw : ∀ z ∈ H, w (reflect e t z) ≤ w z := by
    intro z hz
    apply max_le_max_left
    apply sub_le_sub_left
    have hh := reflect_norm_sq he t z
    have hnon : 0 ≤ t - ⟪e, z⟫_ℝ := sub_nonneg.mpr hz
    nlinarith [mul_nonneg ht.le hnon]
  have hgain := Polarization.integral_polarize_lt (reflectEquiv he t)
    (reflect_involutive he t) (reflect_measurePreserving he t) hH hK.measurableSet
    (reflect_halfspace_ae he t) w (IsodiametricWeight.integrable_weight C) hw hposB
  refine ⟨e, t, he, ht, ?_⟩
  have hP : MeasurableSet (polarize (reflect e t) H K) :=
    Polarization.measurableSet_polarize (reflect_continuous e t).measurable hH hK.measurableSet
  rw [IsodiametricWeight.weightedMeasure_apply C hK.measurableSet,
    IsodiametricWeight.weightedMeasure_apply C hP]
  have hi : (∫ z in K, w z) < ∫ z in polarize (reflect e t) H K, w z := by
    change (∫ z, K.indicator w z) <
      ∫ z, (polarize (reflect e t) H K).indicator w z at hgain
    simpa only [integral_indicator hK.measurableSet, integral_indicator hP] using hgain
  apply (ENNReal.ofReal_lt_ofReal_iff ?_).mpr hi
  exact (integral_nonneg (IsodiametricWeight.weight_nonneg C)).trans_lt hi

end QuadraticPrecision.Isodiametric
