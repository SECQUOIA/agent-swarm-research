import Mathlib.Analysis.SpecialFunctions.SmoothTransition
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Tactic

/-! The exact smooth schedule used in QCPM v2, including its zero endpoint extension. -/
noncomputable section
namespace QipmFormal.QCPM
open MeasureTheory Set

/-- The exponential bump, extended by zero outside `(0,1)`. -/
def bump (t : ℝ) : ℝ := expNegInvGlue (t * (1 - t))

def normalizer : ℝ := ∫ t in (0 : ℝ)..1, bump t

def progress (t : ℝ) : ℝ := (∫ s in (0 : ℝ)..t, bump s) / normalizer

def schedule (ε t : ℝ) : ℝ := ε + (1 - ε) * (1 - progress t)

theorem bump_contDiff {n : ℕ∞} : ContDiff ℝ n bump :=
  expNegInvGlue.contDiff.comp (contDiff_id.mul (contDiff_const.sub contDiff_id))

theorem bump_continuous : Continuous bump := (bump_contDiff (n := 0)).continuous

/-- The definition is zero at both endpoints and everywhere outside the open interval. -/
theorem bump_zero_outside {t : ℝ} (ht : t ∉ Ioo (0 : ℝ) 1) : bump t = 0 := by
  apply expNegInvGlue.zero_of_nonpos
  by_cases h : t ≤ 0
  · exact mul_nonpos_of_nonpos_of_nonneg h (by linarith)
  · have h1 : 1 ≤ t := by
      by_contra! h1
      exact ht ⟨lt_of_not_ge h, h1⟩
    exact mul_nonpos_of_nonneg_of_nonpos (by linarith) (by linarith)

theorem bump_nonneg (t : ℝ) : 0 ≤ bump t := expNegInvGlue.nonneg _

theorem bump_pos {t : ℝ} (ht : t ∈ Ioo (0 : ℝ) 1) : 0 < bump t :=
  expNegInvGlue.pos_of_pos (mul_pos ht.1 (sub_pos.mpr ht.2))

theorem bump_eq_exp {t : ℝ} (ht : t ∈ Ioo (0 : ℝ) 1) :
    bump t = Real.exp (-1 / (t * (1 - t))) := by
  simp [bump, expNegInvGlue, not_le.mpr (mul_pos ht.1 (sub_pos.mpr ht.2)), div_eq_mul_inv, mul_comm]

@[simp] theorem bump_zero : bump 0 = 0 := by simp [bump]
@[simp] theorem bump_one : bump 1 = 0 := by simp [bump]

theorem normalizer_pos : 0 < normalizer := by
  apply intervalIntegral.integral_pos (by norm_num) bump_continuous.continuousOn
  · intro x _; exact bump_nonneg x
  · exact ⟨1 / 2, by norm_num, bump_pos (by norm_num)⟩

theorem progress_continuous : Continuous progress :=
  (intervalIntegral.differentiable_integral_of_continuous bump_continuous).continuous.div_const _

@[simp] theorem progress_zero : progress 0 = 0 := by simp [progress]
@[simp] theorem progress_one : progress 1 = 1 := by
  exact div_self (ne_of_gt normalizer_pos)

theorem progress_mono : MonotoneOn progress (Icc (0 : ℝ) 1) := by
  intro s hs t ht hst
  apply div_le_div_of_nonneg_right _ normalizer_pos.le
  exact intervalIntegral.integral_mono_interval le_rfl hs.1 hst
    (Filter.Eventually.of_forall bump_nonneg) (bump_continuous.intervalIntegrable _ _)

theorem progress_mem {t : ℝ} (ht : t ∈ Icc (0 : ℝ) 1) : progress t ∈ Icc (0 : ℝ) 1 := by
  constructor
  · simpa using progress_mono (show (0 : ℝ) ∈ Icc 0 1 by norm_num) ht ht.1
  · simpa using progress_mono ht (show (1 : ℝ) ∈ Icc 0 1 by norm_num) ht.2

theorem schedule_continuous (ε : ℝ) : Continuous (schedule ε) :=
  continuous_const.add (continuous_const.mul (continuous_const.sub progress_continuous))

@[simp] theorem schedule_zero (ε : ℝ) : schedule ε 0 = 1 := by simp [schedule]
@[simp] theorem schedule_one (ε : ℝ) : schedule ε 1 = ε := by simp [schedule]

theorem schedule_mem {ε t : ℝ} (hε : ε ≤ 1) (ht : t ∈ Icc (0 : ℝ) 1) :
    schedule ε t ∈ Icc ε 1 := by
  have hg := progress_mem ht
  unfold schedule
  constructor <;> nlinarith [hg.1, hg.2,
    mul_nonneg (sub_nonneg.mpr hε) (sub_nonneg.mpr hg.2),
    mul_nonneg (sub_nonneg.mpr hε) hg.1]

theorem schedule_antitone {ε : ℝ} (hε : ε ≤ 1) :
    AntitoneOn (schedule ε) (Icc (0 : ℝ) 1) := by
  intro s hs t ht hst
  have hg := progress_mono hs ht hst
  unfold schedule
  nlinarith

/-- On the terminal interval the bump has an exponentially small pointwise bound. -/
theorem bump_tail_le {u t : ℝ} (hu : 0 < u) (ht : t ∈ Icc (1 - u) 1) :
    bump t ≤ Real.exp (-1 / u) := by
  have harg : t * (1 - t) ≤ u := by
    have hnon : 0 ≤ 1 - t := sub_nonneg.mpr ht.2
    nlinarith [ht.1, mul_nonneg hnon hnon]
  calc
    bump t ≤ expNegInvGlue u := expNegInvGlue.monotone harg
    _ = Real.exp (-1 / u) := by simp [expNegInvGlue, not_le.mpr hu, div_eq_mul_inv]

/-- The remaining progress is exactly the normalized bump integral. -/
theorem progress_tail (t : ℝ) :
    1 - progress t = (∫ s in t..1, bump s) / normalizer := by
  have h := intervalIntegral.integral_add_adjacent_intervals (μ := volume)
    (bump_continuous.intervalIntegrable 0 t) (bump_continuous.intervalIntegrable t 1)
  unfold progress
  apply (eq_div_iff (ne_of_gt normalizer_pos)).mpr
  rw [sub_mul, one_mul, div_mul_cancel₀ _ (ne_of_gt normalizer_pos)]
  dsimp [normalizer]
  linarith

/-- Exact tail estimate for the actual Algorithm 1 schedule. -/
theorem progress_tail_le {u : ℝ} (hu : 0 < u) :
    1 - progress (1 - u) ≤ u / normalizer * Real.exp (-1 / u) := by
  rw [progress_tail]
  have hi := intervalIntegral.integral_mono_on (μ := volume) (show 1 - u ≤ (1 : ℝ) by linarith)
    (bump_continuous.intervalIntegrable (1 - u) 1)
    (continuous_const.intervalIntegrable (1 - u) 1)
    (fun t ht => bump_tail_le hu ht)
  simp only [intervalIntegral.integral_const, smul_eq_mul] at hi
  have hi' : (∫ s in (1 - u)..1, bump s) ≤ u * Real.exp (-1 / u) := by
    convert hi using 1
    ring
  exact (div_le_div_of_nonneg_right hi' normalizer_pos.le).trans_eq (by ring)

/-- Width of the terminal interval in the manuscript. -/
def endpointWidth (ε : ℝ) : ℝ := 1 / (2 * Real.log (1 / ε))

theorem endpoint_log_ge_one {ε : ℝ} (hε : 0 < ε)
    (hsmall : ε ≤ Real.exp (-1)) : 1 ≤ Real.log (1 / ε) := by
  have h := Real.log_le_log hε hsmall
  rw [Real.log_exp] at h
  rw [one_div, Real.log_inv]
  linarith

theorem endpointWidth_pos {ε : ℝ} (hε : 0 < ε)
    (hsmall : ε ≤ Real.exp (-1)) : 0 < endpointWidth ε := by
  have := endpoint_log_ge_one hε hsmall
  unfold endpointWidth
  positivity

theorem endpointWidth_le_half {ε : ℝ} (hε : 0 < ε)
    (hsmall : ε ≤ Real.exp (-1)) : endpointWidth ε ≤ 1 / 2 := by
  have h := endpoint_log_ge_one hε hsmall
  exact one_div_le_one_div_of_le (by norm_num) (by linarith)

theorem endpoint_exp {ε : ℝ} (hε : 0 < ε) : Real.exp (-1 / endpointWidth ε) = ε ^ 2 := by
  have he : -1 / endpointWidth ε = 2 * Real.log ε := by
    unfold endpointWidth
    simp only [one_div, Real.log_inv, div_inv_eq_mul]
    ring
  rw [he, show (2 : ℝ) = (2 : ℕ) from rfl, Real.exp_nat_mul, Real.exp_log hε]

/-- Explicit sufficient conditions replace the manuscript's "sufficiently small" qualification. -/
theorem schedule_terminal_le {ε t : ℝ} (hε : 0 < ε)
    (hc : ε ≤ normalizer) (hsmall : ε ≤ Real.exp (-1))
    (ht : t ∈ Icc (1 - endpointWidth ε) 1) : schedule ε t ≤ 2 * ε := by
  have hu := endpointWidth_pos hε hsmall
  have hu2 := endpointWidth_le_half hε hsmall
  have hε1 : ε ≤ 1 := hsmall.trans (by
    simpa only [Real.exp_zero] using
      (Real.exp_le_exp.mpr (show (-1 : ℝ) ≤ 0 by norm_num)))
  have htail := progress_tail_le hu
  rw [endpoint_exp hε] at htail
  have hubound : endpointWidth ε * ε ≤ normalizer := by
    calc
      endpointWidth ε * ε ≤ 1 * ε := mul_le_mul_of_nonneg_right (by linarith) hε.le
      _ ≤ normalizer := by simpa using hc
  have htailε : 1 - progress (1 - endpointWidth ε) ≤ ε := by
    apply htail.trans
    apply (mul_le_mul_iff_left₀ normalizer_pos).mp
    have heq : (endpointWidth ε / normalizer * ε ^ 2) * normalizer = endpointWidth ε * ε ^ 2 := by
      field_simp [ne_of_gt normalizer_pos]
    rw [heq]
    nlinarith [mul_le_mul_of_nonneg_right hubound hε.le]
  have hstart : 1 - endpointWidth ε ∈ Icc (0 : ℝ) 1 := ⟨by linarith, by linarith⟩
  have htm : t ∈ Icc (0 : ℝ) 1 := ⟨by linarith [ht.1], ht.2⟩
  have hm := schedule_antitone hε1 hstart htm ht.1
  apply hm.trans
  unfold schedule
  have hn := mul_le_mul_of_nonneg_left htailε (sub_nonneg.mpr hε1)
  nlinarith [sq_nonneg ε]

/-- The accuracy restriction used by the norm bound implies the exponential threshold. -/
theorem le_exp_neg_one_of_le_quarter {ε : ℝ} (hε : ε ≤ 1 / 4) :
    ε ≤ Real.exp (-1) := by
  apply hε.trans
  rw [Real.exp_neg, ← one_div]
  apply one_div_le_one_div_of_le (Real.exp_pos 1)
  linarith [Real.exp_one_lt_three]

theorem endpoint_log_ge_one_quarter {ε : ℝ} (hε : 0 < ε) (hε4 : ε ≤ 1 / 4) :
    1 ≤ Real.log (1 / ε) :=
  endpoint_log_ge_one hε (le_exp_neg_one_of_le_quarter hε4)

/-- The norm bound therefore only needs `ε ≤ min (1/4) normalizer`. -/
theorem schedule_terminal_le_quarter {ε t : ℝ} (hε : 0 < ε) (hε4 : ε ≤ 1 / 4)
    (hc : ε ≤ normalizer) (ht : t ∈ Icc (1 - endpointWidth ε) 1) :
    schedule ε t ≤ 2 * ε :=
  schedule_terminal_le hε hc (le_exp_neg_one_of_le_quarter hε4) ht

/-- In particular, the terminal bound holds for every sufficiently small positive accuracy. -/
theorem exists_schedule_terminal_threshold :
    ∃ δ > (0 : ℝ), ∀ ε, 0 < ε → ε ≤ δ →
      ∀ t ∈ Icc (1 - endpointWidth ε) 1, schedule ε t ≤ 2 * ε := by
  refine ⟨min normalizer (Real.exp (-1)),
    lt_min normalizer_pos (Real.exp_pos _), ?_⟩
  intro ε hε hδ t ht
  exact schedule_terminal_le hε (hδ.trans (min_le_left _ _))
    (hδ.trans (min_le_right _ _)) ht

end QipmFormal.QCPM
