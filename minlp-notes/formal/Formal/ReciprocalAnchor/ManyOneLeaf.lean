import Formal.ReciprocalAnchor.ManyGeometry
import Formal.ReciprocalAnchor.ManyIntegrals
import Formal.ReciprocalAnchor.Allocation

/-! The conditional-mean two-atom law realizes the one-leaf call envelope. -/

namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

/-- Zero-mass atoms are placed at the left endpoint. -/
noncomputable def conditionalLocation (a r z : ℝ) : ℝ := if r = 0 then a else z / r

theorem conditionalLocation_bounds {a b r z : ℝ} (hab : a ≤ b) (hr : 0 ≤ r)
    (hz : a * r ≤ z ∧ z ≤ b * r) :
    a ≤ conditionalLocation a r z ∧ conditionalLocation a r z ≤ b := by
  unfold conditionalLocation
  split_ifs with h
  · exact ⟨le_rfl, hab⟩
  · have hp : 0 < r := lt_of_le_of_ne hr (Ne.symm h)
    exact ⟨(le_div_iff₀ hp).mpr hz.1, (div_le_iff₀ hp).mpr hz.2⟩

theorem conditionalLocation_moment {a b r z : ℝ}
    (hz : a * r ≤ z ∧ z ≤ b * r) : r * conditionalLocation a r z = z := by
  unfold conditionalLocation
  split_ifs with h
  · subst r
    have hz0 : z = 0 := by
      simp only [mul_zero] at hz
      exact le_antisymm hz.2 hz.1
    simp [hz0]
  · field_simp

theorem conditionalLocation_call {a b r z : ℝ} (hr : 0 ≤ r)
    (hz : a * r ≤ z ∧ z ≤ b * r) (s : ℝ) :
    r * max (conditionalLocation a r z - s) 0 = max (z - r * s) 0 := by
  rw [mul_max_of_nonneg _ _ hr, mul_sub, conditionalLocation_moment hz, mul_zero]

theorem conditionalLocation_reciprocal (a r z : ℝ) :
    r / conditionalLocation a r z = r ^ 2 / z := by
  unfold conditionalLocation
  split_ifs with h
  · simp [h]
  · rw [div_div_eq_mul_div]
    ring

/-- The one-leaf law uses the two conditional means, with masses `q` and `1-q`. -/
noncomputable def Law.oneLeaf (a b m q w : ℝ)
    (h : LinearBounds a b m (fun _ : Fin 1 => q) (fun _ => w)) : Law a b where
  size := 2
  mass := ![q, 1 - q]
  location := ![conditionalLocation a q w, conditionalLocation a (1 - q) (m - w)]
  nonneg := by
    intro i
    have hj := h.2.2 0
    fin_cases i
    · exact hj.1
    · exact sub_nonneg.mpr hj.2.1
  total := by simp
  bounds := by
    intro i
    obtain ⟨hq, hq1, hw, hw', hc, hc'⟩ := h.2.2 0
    have hab := h.1.trans h.2.1
    fin_cases i
    · exact conditionalLocation_bounds hab hq ⟨hw, hw'⟩
    · exact conditionalLocation_bounds hab (sub_nonneg.mpr hq1) ⟨hc, hc'⟩

theorem Law.oneLeaf_mean {a b m q w : ℝ}
    (h : LinearBounds a b m (fun _ : Fin 1 => q) (fun _ => w)) :
    (Law.oneLeaf a b m q w h).mean = m := by
  obtain ⟨_, _, hw, hw', hc, hc'⟩ := h.2.2 0
  change (∑ i : Fin 2, ![q, 1 - q] i *
    ![conditionalLocation a q w, conditionalLocation a (1 - q) (m - w)] i) = m
  simp only [Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one]
  rw [conditionalLocation_moment ⟨hw, hw'⟩, conditionalLocation_moment ⟨hc, hc'⟩]
  ring

theorem Law.oneLeaf_reciprocal {a b m q w : ℝ}
    (h : LinearBounds a b m (fun _ : Fin 1 => q) (fun _ => w)) :
    (Law.oneLeaf a b m q w h).reciprocal = q ^ 2 / w + (1 - q) ^ 2 / (m - w) := by
  change (∑ i : Fin 2, ![q, 1 - q] i /
    ![conditionalLocation a q w, conditionalLocation a (1 - q) (m - w)] i) = _
  simp only [Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one,
    conditionalLocation_reciprocal]

theorem Law.oneLeaf_call {a b m q w : ℝ}
    (h : LinearBounds a b m (fun _ : Fin 1 => q) (fun _ => w)) (s : ℝ) :
    (Law.oneLeaf a b m q w h).call s =
      envelope m (fun _ : Fin 1 => q) (fun _ => w) s := by
  obtain ⟨hq, hq1, hw, hw', hc, hc'⟩ := h.2.2 0
  change (∑ i : Fin 2, ![q, 1 - q] i *
    max (![conditionalLocation a q w, conditionalLocation a (1 - q) (m - w)] i - s) 0) = _
  simp only [Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one]
  rw [conditionalLocation_call hq ⟨hw, hw'⟩,
    conditionalLocation_call (sub_nonneg.mpr hq1) ⟨hc, hc'⟩]
  apply le_antisymm
  · have h0 := envelope_nonneg m (fun _ : Fin 1 => q) (fun _ => w) s
    have hm := mean_sub_le_envelope m (fun _ : Fin 1 => q) (fun _ => w) s
    have hl := leaf_le_envelope m (fun _ : Fin 1 => q) (fun _ => w) s 0
    have hr := complement_le_envelope m (fun _ : Fin 1 => q) (fun _ => w) s 0
    rcases le_total 0 (w - q * s) with hA | hA <;>
      rcases le_total 0 (m - w - (1 - q) * s) with hB | hB <;>
      simp only [max_eq_left hA, max_eq_right hA, max_eq_left hB, max_eq_right hB] <;>
      linarith
  · apply envelope_le_iff.mpr
    have hA := le_max_left (w - q * s) 0
    have hA0 := le_max_right (w - q * s) 0
    have hB := le_max_left (m - w - (1 - q) * s) 0
    have hB0 := le_max_right (m - w - (1 - q) * s) 0
    refine ⟨by linarith, by linarith, fun _ => ⟨by linarith, by linarith⟩⟩

/-- The integral lower bound reduces exactly to the two one-leaf perspectives. -/
theorem oneLeaf_lowerMoment {a b m q w : ℝ} (ha : 0 < a) (hab : a ≤ b)
    (h : LinearBounds a b m (fun _ : Fin 1 => q) (fun _ => w)) :
    lowerMoment a b m (fun _ : Fin 1 => q) (fun _ => w) =
      q ^ 2 / w + (1 - q) ^ 2 / (m - w) := by
  have hi := (Law.oneLeaf a b m q w h).reciprocal_eq_call_integral ha hab
  rw [Law.oneLeaf_mean h, Law.oneLeaf_reciprocal h] at hi
  simp_rw [Law.oneLeaf_call h] at hi
  exact hi.symm

private theorem square_le_mul_perspective {a r z : ℝ} (ha : 0 < a)
    (hr : 0 ≤ r) (hz : a * r ≤ z) : r ^ 2 ≤ z * (r ^ 2 / z) := by
  by_cases hz0 : z = 0
  · have hr0 : r = 0 := by nlinarith
    simp [hz0, hr0]
  · rw [mul_div_cancel₀ _ hz0]

/-- Under the linear support bounds, the lower moment is exactly the two-SOC condition. -/
theorem oneLeaf_lowerMoment_le_iff_soc {a b m t q w : ℝ}
    (ha : 0 < a) (hab : a ≤ b)
    (h : LinearBounds a b m (fun _ : Fin 1 => q) (fun _ => w)) :
    lowerMoment a b m (fun _ : Fin 1 => q) (fun _ => w) ≤ t ↔
      ReciprocalAnchor.SOCBounds m t q w := by
  rw [oneLeaf_lowerMoment ha hab h]
  obtain ⟨hq, hq1, hw, _, hc, _⟩ := h.2.2 0
  have hq0 := sub_nonneg.mpr hq1
  have hw0 := (mul_nonneg ha.le hq).trans hw
  have hc0 := (mul_nonneg ha.le hq0).trans hc
  constructor
  · intro ht
    exact ⟨q ^ 2 / w, (1 - q) ^ 2 / (m - w),
      div_nonneg (sq_nonneg q) hw0, div_nonneg (sq_nonneg (1 - q)) hc0,
      square_le_mul_perspective ha hq hw, square_le_mul_perspective ha hq0 hc, ht⟩
  · rintro ⟨u, v, hu, hv, hqu, hqv, huv⟩
    exact (add_le_add (ReciprocalAnchor.perspective_le_of_soc hw0 hu hqu)
      (ReciprocalAnchor.perspective_le_of_soc hc0 hv hqv)).trans huv

/-- The one-leaf envelope and secant bounds recover the existing conic description. -/
theorem oneLeaf_conicBounds_iff {a b m t q w : ℝ}
    (ha : 0 < a) (hab : a ≤ b)
    (h : LinearBounds a b m (fun _ : Fin 1 => q) (fun _ => w)) :
    ReciprocalAnchor.ConicBounds a b m t q w ↔
      lowerMoment a b m (fun _ : Fin 1 => q) (fun _ => w) ≤ t ∧
        t ≤ (a + b - m) / (a * b) := by
  obtain ⟨hq, hq1, hw, hw', hc, hc'⟩ := h.2.2 0
  constructor
  · intro hs
    exact ⟨(oneLeaf_lowerMoment_le_iff_soc ha hab h).mpr hs.2, hs.1.2.2.2.2.2.2⟩
  · rintro ⟨hl, hu⟩
    exact ⟨⟨hq, hq1, hw, hw', hc, hc', hu⟩,
      (oneLeaf_lowerMoment_le_iff_soc ha hab h).mp hl⟩

end ReciprocalAnchor.ManyLeaf
