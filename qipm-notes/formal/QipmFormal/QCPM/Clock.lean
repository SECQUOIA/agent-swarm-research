import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Order.Hom.Set
import Mathlib.Topology.Order.MonotoneContinuity
import Mathlib.Tactic

/-!
# The corrected QCPM clock

The time-dependent kinetic coefficient is `a * mu t`. Its normalizing clock
is the integral of that coefficient divided by `eta`. The norm identity below
is a genuine change of variables for a clock-time potential envelope `V`.
The pullback hypothesis explicitly connects `V` with the original envelope `S`;
no claim about quantum simulation or an operator-valued evolution is assumed.
-/

open Set MeasureTheory

namespace QipmFormal.QCPM

/-- Clock that makes the kinetic coefficient constant. -/
noncomputable def correctedClock (a eta : ℝ) (mu : ℝ → ℝ) (t : ℝ) : ℝ :=
  (a / eta) * ∫ u in (0 : ℝ)..t, mu u

@[simp] theorem correctedClock_zero (a eta : ℝ) (mu : ℝ → ℝ) :
    correctedClock a eta mu 0 = 0 := by simp [correctedClock]

/-- Continuity only on the physical time interval is needed. -/
theorem correctedClock_continuousOn {a eta : ℝ} {mu : ℝ → ℝ}
    (hmu : ContinuousOn mu (Icc 0 1)) :
    ContinuousOn (correctedClock a eta mu) (Icc 0 1) := by
  have hi : IntegrableOn mu (uIcc 0 1) := by
    simpa only [uIcc_of_le (show (0 : ℝ) ≤ 1 by norm_num)] using
      hmu.integrableOn_Icc
  have hc : ContinuousOn (fun t => ∫ u in (0 : ℝ)..t, mu u) (uIcc (0 : ℝ) 1) :=
    intervalIntegral.continuousOn_primitive_interval hi
  change ContinuousOn (fun t => (a / eta) * ∫ u in (0 : ℝ)..t, mu u) (Icc 0 1)
  simpa only [uIcc_of_le (show (0 : ℝ) ≤ 1 by norm_num)] using hc.const_mul (a / eta)


/-- The clock derivative on the interior of the physical time interval. -/
theorem correctedClock_hasDerivAt {a eta t : ℝ} {mu : ℝ → ℝ}
    (hmu : ContinuousOn mu (Icc 0 1)) (ht : t ∈ Ioo 0 1) :
    HasDerivAt (correctedClock a eta mu) ((a / eta) * mu t) t := by
  have hsub : uIcc 0 t ⊆ Icc (0 : ℝ) 1 := by
    rw [uIcc_of_le ht.1.le]
    exact Icc_subset_Icc le_rfl ht.2.le
  have hint : IntervalIntegrable mu volume 0 t :=
    (hmu.mono hsub).intervalIntegrable
  have hcont : ContinuousAt mu t :=
    (hmu.mono Ioo_subset_Icc_self).continuousAt (isOpen_Ioo.mem_nhds ht)
  have hmeas : StronglyMeasurableAtFilter mu (nhds t) volume :=
    ContinuousOn.stronglyMeasurableAtFilter isOpen_Ioo
      (hmu.mono Ioo_subset_Icc_self) t ht
  exact (intervalIntegral.integral_hasDerivAt_right hint hmeas hcont).const_mul (a / eta)

/-- Positivity makes the corrected clock invertible on its image. -/
theorem correctedClock_strictMonoOn {a eta : ℝ} {mu : ℝ → ℝ}
    (ha : 0 < a) (heta : 0 < eta)
    (hmu : ContinuousOn mu (Icc 0 1)) (hpos : ∀ t ∈ Icc 0 1, 0 < mu t) :
    StrictMonoOn (correctedClock a eta mu) (Icc 0 1) := by
  apply strictMonoOn_of_deriv_pos (convex_Icc 0 1) (correctedClock_continuousOn hmu)
  intro t ht
  have ht' : t ∈ Ioo (0 : ℝ) 1 := by simpa only [interior_Icc] using ht
  rw [(correctedClock_hasDerivAt hmu ht').deriv]
  exact mul_pos (div_pos ha heta) (hpos t ⟨ht'.1.le, ht'.2.le⟩)

/-- The clock maps the entire physical interval onto the entire clock interval. -/
theorem correctedClock_image {a eta : ℝ} {mu : ℝ → ℝ}
    (ha : 0 < a) (heta : 0 < eta)
    (hmu : ContinuousOn mu (Icc 0 1)) (hpos : ∀ t ∈ Icc 0 1, 0 < mu t) :
    correctedClock a eta mu '' Icc 0 1 = Icc 0 (correctedClock a eta mu 1) := by
  simpa only [correctedClock_zero] using
    (correctedClock_continuousOn hmu).image_Icc_of_monotoneOn
      (show (0 : ℝ) ≤ 1 by norm_num)
      (correctedClock_strictMonoOn ha heta hmu hpos).monotoneOn

/-- The terminal clock time is positive. -/
theorem correctedClock_one_pos {a eta : ℝ} {mu : ℝ → ℝ}
    (ha : 0 < a) (heta : 0 < eta)
    (hmu : ContinuousOn mu (Icc 0 1)) (hpos : ∀ t ∈ Icc 0 1, 0 < mu t) :
    0 < correctedClock a eta mu 1 := by
  have h := correctedClock_strictMonoOn ha heta hmu hpos
    (show (0 : ℝ) ∈ Icc 0 1 by norm_num)
    (show (1 : ℝ) ∈ Icc 0 1 by norm_num) (show (0 : ℝ) < 1 by norm_num)
  simpa only [correctedClock_zero] using h

/-- Exact change of variables for the corrected potential envelope.

`V` is the potential supremum in clock time and `S` is the original supremum.
The pullback divides by `h(t)^2`, with `h(t) = a * mu(t)^2`. This theorem
includes the Jacobian; it does not merely simplify its pointwise expression.
-/
theorem correctedClock_norm_identity {a eta : ℝ} {mu S V : ℝ → ℝ}
    (ha : 0 < a) (heta : 0 < eta)
    (hmu : ContinuousOn mu (Icc 0 1)) (hpos : ∀ t ∈ Icc 0 1, 0 < mu t)
    (hV : ContinuousOn V (Icc 0 (correctedClock a eta mu 1)))
    (hpull : ∀ t ∈ Icc 0 1,
      V (correctedClock a eta mu t) = S t / (a * mu t ^ 2) ^ 2) :
    (∫ tau in (0 : ℝ)..correctedClock a eta mu 1, V tau) =
      (1 / (a * eta)) * ∫ t in (0 : ℝ)..1, S t / mu t ^ 3 := by
  have hc : ContinuousOn (correctedClock a eta mu) (uIcc 0 1) := by
    simpa only [uIcc_of_le (show (0 : ℝ) ≤ 1 by norm_num)] using
      correctedClock_continuousOn (a := a) (eta := eta) hmu
  have hd : ∀ t ∈ Ioo (min (0 : ℝ) 1) (max (0 : ℝ) 1),
      HasDerivWithinAt (correctedClock a eta mu) ((a / eta) * mu t) (Ioi t) t := by
    intro t ht
    exact (correctedClock_hasDerivAt hmu (by simpa using ht)).hasDerivWithinAt
  have hdc : ContinuousOn (fun t => (a / eta) * mu t) (uIcc 0 1) := by
    simpa only [uIcc_of_le (show (0 : ℝ) ≤ 1 by norm_num)] using
      hmu.const_mul (a / eta)
  have hVc : ContinuousOn V (correctedClock a eta mu '' uIcc 0 1) := by
    simpa only [uIcc_of_le (show (0 : ℝ) ≤ 1 by norm_num),
      correctedClock_image ha heta hmu hpos] using hV
  have hchange := intervalIntegral.integral_comp_mul_deriv'' hc hd hdc hVc
  rw [correctedClock_zero] at hchange
  rw [← hchange, ← intervalIntegral.integral_const_mul]
  apply intervalIntegral.integral_congr
  intro t ht
  have ht' : t ∈ Icc (0 : ℝ) 1 := by simpa using ht
  dsimp only [Function.comp_def]
  rw [hpull t ht']
  field_simp [ha.ne', heta.ne', (hpos t ht').ne']

/-- Canonical inverse time, used only on the image of the physical interval. -/
noncomputable def correctedTime (a eta : ℝ) (mu : ℝ → ℝ) : ℝ → ℝ :=
  Function.invFunOn (correctedClock a eta mu) (Icc 0 1)

/-- The canonical inverse cancels the clock on physical time. -/
theorem correctedTime_clock {a eta : ℝ} {mu : ℝ → ℝ}
    (ha : 0 < a) (heta : 0 < eta)
    (hmu : ContinuousOn mu (Icc 0 1)) (hpos : ∀ t ∈ Icc 0 1, 0 < mu t)
    {t : ℝ} (ht : t ∈ Icc 0 1) :
    correctedTime a eta mu (correctedClock a eta mu t) = t :=
  (correctedClock_strictMonoOn ha heta hmu hpos).injOn.leftInvOn_invFunOn ht

/-- The inverse clock stays in the physical interval. -/
theorem correctedTime_mapsTo {a eta : ℝ} {mu : ℝ → ℝ}
    (ha : 0 < a) (heta : 0 < eta)
    (hmu : ContinuousOn mu (Icc 0 1)) (hpos : ∀ t ∈ Icc 0 1, 0 < mu t) :
    MapsTo (correctedTime a eta mu) (Icc 0 (correctedClock a eta mu 1)) (Icc 0 1) := by
  rw [← correctedClock_image ha heta hmu hpos]
  exact (surjOn_image (correctedClock a eta mu) (Icc 0 1)).mapsTo_invFunOn

/-- The canonical inverse is continuous, including both endpoints. -/
theorem correctedTime_continuousOn {a eta : ℝ} {mu : ℝ → ℝ}
    (ha : 0 < a) (heta : 0 < eta)
    (hmu : ContinuousOn mu (Icc 0 1)) (hpos : ∀ t ∈ Icc 0 1, 0 < mu t) :
    ContinuousOn (correctedTime a eta mu) (Icc 0 (correctedClock a eta mu 1)) := by
  let e : Icc (0 : ℝ) 1 ≃o Icc (0 : ℝ) (correctedClock a eta mu 1) :=
    ((correctedClock_strictMonoOn ha heta hmu hpos).orderIso
      (correctedClock a eta mu) (Icc 0 1)).trans
      (OrderIso.setCongr _ _ (correctedClock_image ha heta hmu hpos))
  have he : ∀ t : Icc (0 : ℝ) 1, (e t : ℝ) = correctedClock a eta mu t := by
    intro t
    rfl
  apply continuousOn_iff_continuous_domRestrict.mpr
  have hcont := continuous_subtype_val.comp e.symm.continuous
  apply hcont.congr
  intro tau
  change (e.symm tau : ℝ) = correctedTime a eta mu tau
  have heq : correctedClock a eta mu (e.symm tau) = tau := by
    rw [← he]
    exact congrArg Subtype.val (e.apply_symm_apply tau)
  rw [← heq]
  exact (correctedTime_clock ha heta hmu hpos (e.symm tau).property).symm

/-- The actual transformed scalar envelope, using the canonical inverse clock. -/
noncomputable def correctedEnvelope (a eta : ℝ) (mu S : ℝ → ℝ) (tau : ℝ) : ℝ :=
  S (correctedTime a eta mu tau) / (a * mu (correctedTime a eta mu tau) ^ 2) ^ 2

/-- The canonical transformed envelope is continuous on the clock interval. -/
theorem correctedEnvelope_continuousOn {a eta : ℝ} {mu S : ℝ → ℝ}
    (ha : 0 < a) (heta : 0 < eta)
    (hmu : ContinuousOn mu (Icc 0 1)) (hpos : ∀ t ∈ Icc 0 1, 0 < mu t)
    (hS : ContinuousOn S (Icc 0 1)) :
    ContinuousOn (correctedEnvelope a eta mu S) (Icc 0 (correctedClock a eta mu 1)) := by
  have hi := correctedTime_continuousOn ha heta hmu hpos
  have hm := correctedTime_mapsTo ha heta hmu hpos
  apply (hS.comp hi hm).div (((hmu.comp hi hm).pow 2).const_mul a |>.pow 2)
  intro tau htau
  exact pow_ne_zero 2 (mul_ne_zero ha.ne' (pow_ne_zero 2 (hpos _ (hm htau)).ne'))

/-- Exact norm formula with the inverse clock and envelope constructed explicitly. -/
theorem correctedEnvelope_integral {a eta : ℝ} {mu S : ℝ → ℝ}
    (ha : 0 < a) (heta : 0 < eta)
    (hmu : ContinuousOn mu (Icc 0 1)) (hpos : ∀ t ∈ Icc 0 1, 0 < mu t)
    (hS : ContinuousOn S (Icc 0 1)) :
    (∫ tau in (0 : ℝ)..correctedClock a eta mu 1, correctedEnvelope a eta mu S tau) =
      (1 / (a * eta)) * ∫ t in (0 : ℝ)..1, S t / mu t ^ 3 := by
  apply correctedClock_norm_identity ha heta hmu hpos
    (correctedEnvelope_continuousOn ha heta hmu hpos hS)
  intro t ht
  simp only [correctedEnvelope, correctedTime_clock ha heta hmu hpos ht]

/-- Chain rule in the corrected clock, for a scalar time-dependent quantity. -/
theorem correctedClock_chainRule {a eta t q : ℝ} {mu psi : ℝ → ℝ}
    (hmu : ContinuousOn mu (Icc 0 1)) (ht : t ∈ Ioo 0 1)
    (hpsi : HasDerivAt psi q (correctedClock a eta mu t)) :
    HasDerivAt (fun u => psi (correctedClock a eta mu u))
      (q * ((a / eta) * mu t)) t :=
  hpsi.comp t (correctedClock_hasDerivAt hmu ht)

/-- Multiplying time by a varying coefficient introduces an extra derivative term. -/
theorem productClock_hasDerivAt {a eta t m' : ℝ} {mu : ℝ → ℝ}
    (hmu : HasDerivAt mu m' t) :
    HasDerivAt (fun u => (a / eta) * (u * mu u))
      ((a / eta) * (mu t + t * m')) t := by
  simpa only [one_mul, id_eq, Pi.mul_apply] using ((hasDerivAt_id t).mul hmu).const_mul (a / eta)

/-- The product clock fails to have the required derivative wherever the
schedule changes at a nonzero time. -/
theorem productClock_derivative_ne {a eta t m' : ℝ} {mu : ℝ → ℝ}
    (ha : a ≠ 0) (heta : eta ≠ 0) (ht : t ≠ 0) (hm' : m' ≠ 0)
    (hmu : HasDerivAt mu m' t) :
    deriv (fun u => (a / eta) * (u * mu u)) t ≠ (a / eta) * mu t := by
  rw [(productClock_hasDerivAt (a := a) (eta := eta) hmu).deriv]
  intro h
  have hzero : (a / eta) * (t * m') = 0 := by nlinarith [h]
  exact mul_ne_zero (div_ne_zero ha heta) (mul_ne_zero ht hm') hzero

/-- Dividing by the clock derivative normalizes the kinetic coefficient. -/
theorem correctedClock_kinetic_coefficient {a eta mu : ℝ}
    (ha : a ≠ 0) (heta : eta ≠ 0) (hmu : mu ≠ 0) :
    (a * mu / eta)⁻¹ * (a * mu / (2 * eta)) = 1 / 2 := by
  field_simp

/-- The same normalization changes `f / (eta * mu * h)` into `f / h^2`. -/
theorem correctedClock_potential_coefficient {a eta mu f : ℝ}
    (ha : a ≠ 0) (heta : eta ≠ 0) (hmu : mu ≠ 0) :
    (a * mu / eta)⁻¹ * (f / (eta * mu * (a * mu ^ 2))) =
      f / (a * mu ^ 2) ^ 2 := by
  field_simp

end QipmFormal.QCPM
