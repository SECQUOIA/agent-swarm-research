import Formal.ReciprocalAnchor.Model

/-! Allocate the total reciprocal moment between the two leaf endpoint measures. -/

namespace ReciprocalAnchor

theorem lower_le_upper {a b rho v : ℝ} (ha : 0 < a) (hab : a < b)
    (hr : 0 ≤ rho) (hav : a * rho ≤ v) (hvb : v ≤ b * rho) :
    rho ^ 2 / v ≤ ((a + b) * rho - v) / (a * b) := by
  have hb : 0 < b := lt_trans ha hab
  have hv : 0 ≤ v := le_trans (mul_nonneg ha.le hr) hav
  by_cases hv0 : v = 0
  · have hr0 : rho = 0 := by nlinarith
    simp [hv0, hr0]
  · have hvp : 0 < v := lt_of_le_of_ne hv (Ne.symm hv0)
    apply (div_le_div_iff₀ hvp (mul_pos ha hb)).mpr
    nlinarith [mul_nonneg (sub_nonneg.mpr hav) (sub_nonneg.mpr hvb)]

theorem perspective_le_of_soc {rho v tau : ℝ} (hv : 0 ≤ v) (ht : 0 ≤ tau)
    (h : rho ^ 2 ≤ v * tau) : rho ^ 2 / v ≤ tau := by
  by_cases hzero : v = 0
  · simpa [hzero] using ht
  · apply (div_le_iff₀ (lt_of_le_of_ne hv (Ne.symm hzero))).mpr
    nlinarith

theorem split_interval {l₁ u₁ l₀ u₀ t : ℝ}
    (h₁ : l₁ ≤ u₁) (h₀ : l₀ ≤ u₀) (hl : l₁ + l₀ ≤ t)
    (hu : t ≤ u₁ + u₀) :
    ∃ t₁ t₀ : ℝ, l₁ ≤ t₁ ∧ t₁ ≤ u₁ ∧ l₀ ≤ t₀ ∧ t₀ ≤ u₀ ∧ t₁ + t₀ = t := by
  refine ⟨max l₁ (t - u₀), t - max l₁ (t - u₀), le_max_left _ _, ?_, ?_, ?_, by ring⟩
  · exact max_le h₁ (by linarith)
  · have h : max l₁ (t - u₀) ≤ t - l₀ := max_le (by linarith) (by linarith)
    linarith
  · have h := le_max_right l₁ (t - u₀)
    linarith

theorem allocate_moments {a b m t q w : ℝ} (ha : 0 < a) (hab : a < b)
    (h : ConicBounds a b m t q w) :
    ∃ t₁ t₀ : ℝ,
      q ^ 2 / w ≤ t₁ ∧ t₁ ≤ ((a + b) * q - w) / (a * b) ∧
      (1 - q) ^ 2 / (m - w) ≤ t₀ ∧
      t₀ ≤ ((a + b) * (1 - q) - (m - w)) / (a * b) ∧ t₁ + t₀ = t := by
  rcases h with ⟨⟨hq, hq1, haw, hwb, ham, hmb, ht⟩, s₁, s₀, hs₁, hs₀, hc₁, hc₀, hst⟩
  have hq0 : 0 ≤ 1 - q := by linarith
  have hw : 0 ≤ w := le_trans (mul_nonneg ha.le hq) haw
  have hmw : 0 ≤ m - w := le_trans (mul_nonneg ha.le hq0) ham
  apply split_interval (lower_le_upper ha hab hq haw hwb)
    (lower_le_upper ha hab hq0 ham hmb)
  · linarith [perspective_le_of_soc hw hs₁ hc₁, perspective_le_of_soc hmw hs₀ hc₀]
  · convert ht using 1
    ring

end ReciprocalAnchor
