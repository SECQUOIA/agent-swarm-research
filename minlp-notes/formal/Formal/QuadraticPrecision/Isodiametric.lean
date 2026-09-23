import Formal.QuadraticPrecision.IsodiametricCompact
import Formal.QuadraticPrecision.IsodiametricStrict
import Formal.QuadraticPrecision.IsodiametricSupport
import Mathlib.MeasureTheory.Measure.Lebesgue.VolumeOfBalls

/-!
The sharp Euclidean isodiametric inequality. The proof maximizes a compactly
supported radial weighted measure among compact sets with bounded diameter.
A support point outside the half-diameter ball yields a strictly improving
polarization, contradicting maximality. Letting the radial cutoff grow removes
the weight. No convexity or regularity of the original set is required beyond
compactness.
-/
open Set MeasureTheory Metric
open scoped InnerProductSpace
noncomputable section
namespace QuadraticPrecision.Isodiametric
open IsodiametricWeight
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]

/-- Among compact sets of diameter at most `D`, the ball of radius `D/2`
has maximal Euclidean volume. -/
theorem volume_le_closedBall_half_diameter {S : Set E} {D : ℝ}
    (hS : IsCompact S) (hD : 0 ≤ D)
    (hdiam : ∀ x ∈ S, ∀ y ∈ S, dist x y ≤ D) :
    volume S ≤ volume (closedBall (0 : E) (D / 2)) := by
  by_contra! hvol
  obtain ⟨R, hR, hSR⟩ := hS.isBounded.subset_closedBall_lt 0 (0 : E)
  obtain ⟨C, hC, hCS⟩ := exists_weightedMeasure_lt hS.measurableSet
    measurableSet_closedBall hR.le hSR measure_closedBall_lt_top.ne hvol
  obtain ⟨K, hK, hKR, hKD, hmax⟩ :=
    exists_compact_measure_maximizer (weightedMeasure (E := E) C)
      (closedBall (0 : E) R) (isCompact_closedBall _ _) D
  have hCK : weightedMeasure C (closedBall (0 : E) (D / 2)) < weightedMeasure C K :=
    hCS.trans_le (hmax S hS hSR hdiam)
  obtain ⟨x, hx, hxn⟩ := exists_support_outside_ball hCK
  obtain ⟨e, t, he, ht, hgain⟩ :=
    exists_strict_polarization hK hKR hR.le hD hKD hC hx hxn
  let H := {z : E | ⟪e, z⟫_ℝ ≤ t}
  have hH : IsClosed H := isClosed_le (continuous_const.inner continuous_id) continuous_const
  have hP := polarize_compact (reflect_involutive he t) (reflect_continuous e t) hH hK
  exact (not_lt.mpr (hmax _ hP (polarize_bounded he ht.le hKR)
    (polarize_diameter he hKD))) hgain

/-- The exact unit-ball constant in dimension `d>0`. -/
theorem volume_le_unitBall_mul_half_diameter_pow {d : ℕ} (hd : 0 < d)
    {S : Set (EuclideanSpace ℝ (Fin d))} {D : ℝ}
    (hS : IsCompact S) (hD : 0 ≤ D)
    (hdiam : ∀ x ∈ S, ∀ y ∈ S, dist x y ≤ D) :
    volume S ≤ volume (closedBall (0 : EuclideanSpace ℝ (Fin d)) 1) *
      ENNReal.ofReal (D / 2) ^ d := by
  let : Nonempty (Fin d) := Fin.pos_iff_nonempty.mp hd
  have h := volume_le_closedBall_half_diameter hS hD hdiam
  simpa only [EuclideanSpace.volume_closedBall, Fintype.card_fin, ENNReal.ofReal_one,
    one_pow, one_mul, mul_comm] using h

end QuadraticPrecision.Isodiametric
