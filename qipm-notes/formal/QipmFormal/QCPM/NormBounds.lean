import Mathlib

/-!
# Integral bounds for the corrected QCPM simulation norm

The terminal-window argument is separated from the concrete potential and schedule.
All positivity and integrability hypotheses needed by real division and integration
are explicit. `normIntegral` is the corrected clock's pulled-back norm.
-/

namespace QipmFormal.QCPM

open Set MeasureTheory

noncomputable def normIntegral (a eta : ℝ) (S mu : ℝ → ℝ) : ℝ :=
  (1 / (a * eta)) * ∫ t in (0 : ℝ)..1, S t / mu t ^ 3

/-- A nonnegative integrand dominates a constant on a terminal window. -/
theorem integral_terminal_lower {f : ℝ → ℝ} {w B : ℝ}
    (hw0 : 0 ≤ w) (hw1 : w ≤ 1)
    (hf : IntervalIntegrable f volume 0 1)
    (hnonneg : ∀ t ∈ Icc (0 : ℝ) 1, 0 ≤ f t)
    (hwindow : ∀ t ∈ Icc (1 - w) 1, B ≤ f t) :
    w * B ≤ ∫ t in (0 : ℝ)..1, f t := by
  have hsub : Icc (1 - w) 1 ⊆ Icc (0 : ℝ) 1 := by
    intro t ht
    exact ⟨by linarith [ht.1], ht.2⟩
  have h01 : (0 : ℝ) ≤ 1 := by norm_num
  have hw : 1 - w ≤ 1 := by linarith
  have hfi : IntervalIntegrable f volume (1 - w) 1 := by
    apply hf.mono_set
    simpa only [uIcc_of_le h01, uIcc_of_le hw] using hsub
  have hlow := intervalIntegral.integral_mono_on (show 1 - w ≤ 1 by linarith)
    (intervalIntegrable_const (c := B)) hfi hwindow
  have htail := intervalIntegral.integral_mono_interval
    (show (0 : ℝ) ≤ 1 - w by linarith) (show 1 - w ≤ 1 by linarith)
    (le_refl (1 : ℝ))
    ((ae_restrict_mem measurableSet_Ioc).mono fun t ht =>
      hnonneg t ⟨le_of_lt ht.1, ht.2⟩) hf
  have hconst : (∫ _t in (1 - w)..1, B) = w * B := by
    simp only [intervalIntegral.integral_const, smul_eq_mul]
    ring
  rw [hconst] at hlow
  exact hlow.trans htail

/-- The general terminal-window estimate; the factor 64 is 8 from the
potential witness and 8 from cubing the upper bound `mu ≤ 2 eps`. -/
theorem normIntegral_terminal_lower {a eta d eps w : ℝ} {S mu : ℝ → ℝ}
    (ha : 0 < a) (heta : 0 < eta) (hd : 0 ≤ d) (heps : 0 < eps)
    (hw0 : 0 ≤ w) (hw1 : w ≤ 1)
    (hf : IntervalIntegrable (fun t => S t / mu t ^ 3) volume 0 1)
    (hS : ∀ t ∈ Icc (0 : ℝ) 1, 0 ≤ S t)
    (hmu : ∀ t ∈ Icc (0 : ℝ) 1, 0 < mu t)
    (hwindow : ∀ t ∈ Icc (1 - w) 1, mu t ≤ 2 * eps ∧ d / 8 ≤ S t) :
    d * w / (64 * a * eta * eps ^ 3) ≤ normIntegral a eta S mu := by
  have hlow : w * (d / (64 * eps ^ 3)) ≤ ∫ t in (0 : ℝ)..1, S t / mu t ^ 3 := by
    apply integral_terminal_lower hw0 hw1 hf
    · intro t ht
      exact div_nonneg (hS t ht) (le_of_lt (pow_pos (hmu t ht) 3))
    · intro t ht
      have ht' : t ∈ Icc (0 : ℝ) 1 := ⟨by linarith [ht.1], ht.2⟩
      obtain ⟨hup, hs⟩ := hwindow t ht
      have hm := hmu t ht'
      have hc : mu t ^ 3 ≤ 8 * eps ^ 3 := by
        calc
          mu t ^ 3 ≤ (2 * eps) ^ 3 := pow_le_pow_left₀ hm.le hup 3
          _ = 8 * eps ^ 3 := by ring
      have h1 : d / (64 * eps ^ 3) = (d / 8) / (8 * eps ^ 3) := by ring
      rw [h1]
      exact (div_le_div_of_nonneg_left (by positivity) (by positivity) hc).trans
        (div_le_div_of_nonneg_right hs (by positivity))
  have hscaled := mul_le_mul_of_nonneg_left hlow (show 0 ≤ 1 / (a * eta) by positivity)
  unfold normIntegral
  calc
    d * w / (64 * a * eta * eps ^ 3) =
        1 / (a * eta) * (w * (d / (64 * eps ^ 3))) := by
      field_simp
    _ ≤ _ := hscaled

/-- The manuscript's logarithmic endpoint window gives the factor 128. -/
theorem normIntegral_log_window_lower {a eta d eps : ℝ} {S mu : ℝ → ℝ}
    (ha : 0 < a) (heta : 0 < eta) (hd : 0 ≤ d) (heps : 0 < eps)
    (hlog : 1 ≤ Real.log (1 / eps))
    (hf : IntervalIntegrable (fun t => S t / mu t ^ 3) volume 0 1)
    (hS : ∀ t ∈ Icc (0 : ℝ) 1, 0 ≤ S t)
    (hmu : ∀ t ∈ Icc (0 : ℝ) 1, 0 < mu t)
    (hwindow : ∀ t ∈ Icc (1 - 1 / (2 * Real.log (1 / eps))) 1,
      mu t ≤ 2 * eps ∧ d / 8 ≤ S t) :
    d / (128 * a * eta * eps ^ 3 * Real.log (1 / eps)) ≤
      normIntegral a eta S mu := by
  have hl : 0 < Real.log (1 / eps) := by linarith
  have hw : 1 / (2 * Real.log (1 / eps)) ≤ 1 :=
    (div_le_one (by positivity)).2 (by linarith)
  have h := normIntegral_terminal_lower ha heta hd heps (by positivity) hw hf hS hmu hwindow
  convert h using 1
  field_simp
  ring

/-- A uniform derivative bound supplies the Lipschitz contract used below. -/
theorem speed_bound_of_derivative {mu : ℝ → ℝ} {L : ℝ}
    (hdiff : ∀ t ∈ Icc (0 : ℝ) 1, DifferentiableAt ℝ mu t)
    (hderiv : ∀ t ∈ Icc (0 : ℝ) 1, |deriv mu t| ≤ L) :
    ∀ s ∈ Icc (0 : ℝ) 1, ∀ t ∈ Icc (0 : ℝ) 1,
      |mu s - mu t| ≤ L * |s - t| := by
  intro s hs t ht
  simpa only [Real.norm_eq_abs] using
    (convex_Icc (0 : ℝ) 1).norm_image_sub_le_of_norm_deriv_le
      hdiff (fun u hu => by simpa only [Real.norm_eq_abs] using hderiv u hu) ht hs

/-- A speed bound alone gives a terminal window. Monotonicity is unnecessary. -/
theorem speed_terminal_window {mu : ℝ → ℝ} {eps L : ℝ}
    (heps : 0 < eps) (heps4 : eps ≤ 1 / 4) (hL : 0 < L)
    (hstart : mu 0 = 1) (hend : mu 1 = eps)
    (hspeed : ∀ s ∈ Icc (0 : ℝ) 1, ∀ t ∈ Icc (0 : ℝ) 1,
      |mu s - mu t| ≤ L * |s - t|) :
    eps / L ≤ 1 ∧ ∀ t ∈ Icc (1 - eps / L) 1, mu t ≤ 2 * eps := by
  have hends := hspeed 0 (by constructor <;> norm_num) 1 (by constructor <;> norm_num)
  rw [hstart, hend] at hends
  have hLlower : 1 - eps ≤ L := by
    have h := (le_abs_self (1 - eps)).trans hends
    norm_num at h
    linarith
  have hw : eps / L ≤ 1 := (div_le_one hL).2 (by linarith)
  refine ⟨hw, ?_⟩
  intro t ht
  have ht0 : 0 ≤ t := by linarith [ht.1]
  have h := hspeed t ⟨ht0, ht.2⟩ 1 (by constructor <;> norm_num)
  rw [hend, abs_of_nonpos (sub_nonpos.mpr ht.2)] at h
  have hstep : L * (1 - t) ≤ eps := by
    have h1 : 1 - t ≤ eps / L := by linarith [ht.1]
    have h2 := (le_div_iff₀ hL).mp h1
    nlinarith
  have hleft := (le_abs_self (mu t - eps)).trans h
  linarith

/-- The schedule-independent norm--speed bound, with a Lipschitz contract. -/
theorem normIntegral_speed_lower {a eta d eps L : ℝ} {S mu : ℝ → ℝ}
    (ha : 0 < a) (heta : 0 < eta) (hd : 0 ≤ d)
    (heps : 0 < eps) (heps4 : eps ≤ 1 / 4) (hL : 0 < L)
    (hstart : mu 0 = 1) (hend : mu 1 = eps)
    (hspeed : ∀ s ∈ Icc (0 : ℝ) 1, ∀ t ∈ Icc (0 : ℝ) 1,
      |mu s - mu t| ≤ L * |s - t|)
    (hf : IntervalIntegrable (fun t => S t / mu t ^ 3) volume 0 1)
    (hmu : ∀ t ∈ Icc (0 : ℝ) 1, 0 < mu t)
    (hwitness : ∀ t ∈ Icc (0 : ℝ) 1, d / 2 * (1 - mu t) ^ 2 ≤ S t) :
    d / (64 * a * eta * L * eps ^ 2) ≤ normIntegral a eta S mu := by
  obtain ⟨hw, hterminal⟩ := speed_terminal_window heps heps4 hL hstart hend hspeed
  have hS : ∀ t ∈ Icc (0 : ℝ) 1, 0 ≤ S t := by
    intro t ht
    exact (mul_nonneg (by positivity) (sq_nonneg _)).trans (hwitness t ht)
  have hwindow : ∀ t ∈ Icc (1 - eps / L) 1, mu t ≤ 2 * eps ∧ d / 8 ≤ S t := by
    intro t ht
    have ht' : t ∈ Icc (0 : ℝ) 1 := ⟨by linarith [ht.1], ht.2⟩
    have hm := hterminal t ht
    refine ⟨hm, ?_⟩
    have hsquare : (1 / 4 : ℝ) ≤ (1 - mu t) ^ 2 := by nlinarith
    have hprod := mul_le_mul_of_nonneg_left hsquare (show 0 ≤ d / 2 by positivity)
    have hwit := hwitness t ht'
    nlinarith
  have h := normIntegral_terminal_lower ha heta hd heps (by positivity) hw hf hS hmu hwindow
  convert h using 1
  field_simp

/-- A bounded spatial envelope gives the manuscript's global upper certificate. -/
theorem normIntegral_upper {a eta eps B : ℝ} {S mu : ℝ → ℝ}
    (ha : 0 < a) (heta : 0 < eta) (heps : 0 < eps) (hB : 0 ≤ B)
    (hf : IntervalIntegrable (fun t => S t / mu t ^ 3) volume 0 1)
    (hmu : ∀ t ∈ Icc (0 : ℝ) 1, eps ≤ mu t)
    (hS : ∀ t ∈ Icc (0 : ℝ) 1, S t ≤ B) :
    normIntegral a eta S mu ≤ B / (a * eta * eps ^ 3) := by
  have hbound : ∀ t ∈ Icc (0 : ℝ) 1, S t / mu t ^ 3 ≤ B / eps ^ 3 := by
    intro t ht
    have hm := hmu t ht
    have hmpos : 0 < mu t := heps.trans_le hm
    have hpow : eps ^ 3 ≤ mu t ^ 3 := pow_le_pow_left₀ heps.le hm 3
    exact (div_le_div_of_nonneg_right (hS t ht) (by positivity)).trans
      (div_le_div_of_nonneg_left hB (by positivity) hpow)
  have hi := intervalIntegral.integral_mono_on (show (0 : ℝ) ≤ 1 by norm_num)
    hf (intervalIntegrable_const (c := B / eps ^ 3)) hbound
  simp only [intervalIntegral.integral_const, sub_zero, smul_eq_mul, one_mul] at hi
  have hs := mul_le_mul_of_nonneg_left hi (show 0 ≤ 1 / (a * eta) by positivity)
  unfold normIntegral
  calc
    1 / (a * eta) * (∫ t in (0 : ℝ)..1, S t / mu t ^ 3) ≤
        1 / (a * eta) * (B / eps ^ 3) := hs
    _ = B / (a * eta * eps ^ 3) := by field_simp

end QipmFormal.QCPM
