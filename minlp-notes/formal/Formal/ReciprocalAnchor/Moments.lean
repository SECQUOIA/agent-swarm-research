import Mathlib

/-! Exact first and inverse moments of a finite positive measure on an interval. -/

namespace ReciprocalAnchor

open Finset

/-- Three atoms suffice for every admissible mass and pair of moments. -/
def MomentMeasure (a b rho v tau : ℝ) : Prop :=
  ∃ w x : Fin 3 → ℝ,
    (∀ i, 0 ≤ w i ∧ a ≤ x i ∧ x i ≤ b) ∧
    ∑ i, w i = rho ∧ ∑ i, w i * x i = v ∧ ∑ i, w i / x i = tau

private theorem reciprocal_secant {a b x : ℝ} (ha : 0 < a) (hab : a < b)
    (hx : a ≤ x ∧ x ≤ b) : 1 / x ≤ (a + b - x) / (a * b) := by
  have hb : 0 < b := lt_trans ha hab
  have hp : 0 < x := lt_of_lt_of_le ha hx.1
  apply (div_le_div_iff₀ hp (mul_pos ha hb)).2
  nlinarith [mul_nonneg (sub_nonneg.mpr hx.1) (sub_nonneg.mpr hx.2)]

/-- The reciprocal secant bounds every finite positive measure. -/
theorem inverse_moment_upper {ι : Type*} [Fintype ι] {a b : ℝ}
    (ha : 0 < a) (hab : a < b) (w x : ι → ℝ)
    (hw : ∀ i, 0 ≤ w i) (hx : ∀ i, a ≤ x i ∧ x i ≤ b) :
    (∑ i, w i / x i) ≤
      ((a + b) * (∑ i, w i) - ∑ i, w i * x i) / (a * b) := by
  calc
    (∑ i, w i / x i) ≤ ∑ i, w i * ((a + b - x i) / (a * b)) := by
      apply sum_le_sum
      intro i _
      simpa only [mul_one_div] using mul_le_mul_of_nonneg_left
        (reciprocal_secant ha hab (hx i)) (hw i)
    _ = _ := by simp only [← mul_div_assoc, ← sum_div]; congr 1; simp only [mul_sub,
      sum_sub_distrib, ← sum_mul]; ring

private theorem square_sum_identity {ι : Type*} [Fintype ι]
    (w x : ι → ℝ) (hx : ∀ i, x i ≠ 0) (c : ℝ) :
    (∑ i, w i * (x i - c) ^ 2 / x i) =
      (∑ i, w i * x i) - 2 * c * (∑ i, w i) + c ^ 2 * (∑ i, w i / x i) := by
  calc
    _ = ∑ i, (w i * x i - 2 * c * w i + c ^ 2 * (w i / x i)) := by
      apply sum_congr rfl
      intro i _
      field_simp [hx i]
      ring
    _ = _ := by simp only [sum_add_distrib, sum_sub_distrib, ← mul_sum]

/-- Weighted Cauchy--Schwarz, expressed without square roots or probability measures. -/
theorem inverse_moment_soc {ι : Type*} [Fintype ι]
    (w x : ι → ℝ) (hw : ∀ i, 0 ≤ w i) (hx : ∀ i, 0 < x i) :
    (∑ i, w i) ^ 2 ≤ (∑ i, w i * x i) * (∑ i, w i / x i) := by
  let rho := ∑ i, w i
  let v := ∑ i, w i * x i
  let tau := ∑ i, w i / x i
  have hr : 0 ≤ rho := sum_nonneg fun i _ => hw i
  have hv : 0 ≤ v := sum_nonneg fun i _ => mul_nonneg (hw i) (hx i).le
  by_cases hv0 : v = 0
  · have hwi : ∀ i, w i = 0 := by
      intro i
      have hsum : ∑ i, w i * x i = 0 := hv0
      have he : w i * x i = 0 := (sum_eq_zero_iff_of_nonneg
        (fun j _ => mul_nonneg (hw j) (hx j).le)).mp hsum i (mem_univ i)
      exact (mul_eq_zero.mp he).resolve_right (ne_of_gt (hx i))
    simp [hwi]
  · have hvp : 0 < v := lt_of_le_of_ne hv (Ne.symm hv0)
    have hs : 0 ≤ v - 2 * (v / rho) * rho + (v / rho) ^ 2 * tau := by
      rw [← square_sum_identity w x (fun i => ne_of_gt (hx i)) (v / rho)]
      exact sum_nonneg fun i _ => div_nonneg (mul_nonneg (hw i) (sq_nonneg _)) (hx i).le
    by_cases hr0 : rho = 0
    · change rho ^ 2 ≤ v * tau
      rw [hr0]
      simpa only [zero_pow (by decide : 2 ≠ 0)] using
        mul_nonneg hv (show 0 ≤ tau from sum_nonneg fun i _ => div_nonneg (hw i) (hx i).le)
    · have hid : (v - 2 * (v / rho) * rho + (v / rho) ^ 2 * tau) * rho ^ 2 =
          v * (v * tau - rho ^ 2) := by field_simp; ring
      have hprod := mul_nonneg hs (sq_nonneg rho)
      rw [hid] at hprod
      have := nonneg_of_mul_nonneg_right hprod hvp
      exact sub_nonneg.mp this

/-- All first and inverse moment constraints for an arbitrary finite positive measure. -/
theorem moment_bounds {ι : Type*} [Fintype ι] {a b : ℝ}
    (ha : 0 < a) (hab : a < b) (w x : ι → ℝ)
    (hw : ∀ i, 0 ≤ w i) (hx : ∀ i, a ≤ x i ∧ x i ≤ b) :
    (a * (∑ i, w i) ≤ ∑ i, w i * x i) ∧
    ((∑ i, w i * x i) ≤ b * (∑ i, w i)) ∧
    ((∑ i, w i) ^ 2 ≤ (∑ i, w i * x i) * (∑ i, w i / x i)) ∧
    ((∑ i, w i / x i) ≤
      ((a + b) * (∑ i, w i) - ∑ i, w i * x i) / (a * b)) := by
  refine ⟨?_, ?_, inverse_moment_soc w x hw (fun i => lt_of_lt_of_le ha (hx i).1),
    inverse_moment_upper ha hab w x hw hx⟩
  · rw [mul_sum]
    exact sum_le_sum fun i _ => by
      simpa only [mul_comm a] using mul_le_mul_of_nonneg_left (hx i).1 (hw i)
  · rw [mul_sum]
    exact sum_le_sum fun i _ => by
      simpa only [mul_comm b] using mul_le_mul_of_nonneg_left (hx i).2 (hw i)

private theorem interpolate {L U t : ℝ} (hLU : L ≤ U) (ht : L ≤ t ∧ t ≤ U) :
    ∃ α : ℝ, 0 ≤ α ∧ α ≤ 1 ∧ t = (1 - α) * L + α * U := by
  by_cases h : L = U
  · refine ⟨0, le_rfl, by norm_num, ?_⟩
    have : t = L := le_antisymm (ht.2.trans_eq h.symm) ht.1
    simpa using this
  · have hp : 0 < U - L := sub_pos.mpr (lt_of_le_of_ne hLU h)
    refine ⟨(t - L) / (U - L), div_nonneg (sub_nonneg.mpr ht.1) hp.le, ?_, ?_⟩
    · apply (div_le_one hp).2
      linarith [ht.2]
    · field_simp
      ring

/-- Explicit three-atom interpolation between the point mass and endpoint masses. -/
theorem momentMeasure_interpolation {a b rho c α : ℝ}
    (ha : 0 < a) (hab : a < b) (hr : 0 ≤ rho)
    (hc : a ≤ c ∧ c ≤ b) (hα : 0 ≤ α ∧ α ≤ 1) :
    MomentMeasure a b rho (rho * c)
      ((1 - α) * (rho / c) + α * (((a + b) * rho - rho * c) / (a * b))) := by
  have hb : b ≠ 0 := ne_of_gt (lt_trans ha hab)
  have ha0 : a ≠ 0 := ne_of_gt ha
  have hc0 : c ≠ 0 := ne_of_gt (lt_of_lt_of_le ha hc.1)
  have hba : 0 < b - a := sub_pos.mpr hab
  refine ⟨![rho * (1 - α), α * rho * (b - c) / (b - a),
    α * rho * (c - a) / (b - a)], ![c, a, b], ?_, ?_, ?_, ?_⟩
  · intro i
    fin_cases i
    · exact ⟨mul_nonneg hr (sub_nonneg.mpr hα.2), hc⟩
    · exact ⟨div_nonneg (mul_nonneg (mul_nonneg hα.1 hr)
        (sub_nonneg.mpr hc.2)) hba.le, le_rfl, hab.le⟩
    · exact ⟨div_nonneg (mul_nonneg (mul_nonneg hα.1 hr)
        (sub_nonneg.mpr hc.1)) hba.le, hab.le, le_rfl⟩
  all_goals simp only [Fin.sum_univ_succ, Fin.sum_univ_zero, Matrix.cons_val_zero,
    Matrix.cons_val_succ, add_zero]
  all_goals field_simp
  all_goals ring

/-- Every inverse moment between the sharp lower and upper bounds has three atoms. -/
theorem momentMeasure_of_bounds {a b rho v tau : ℝ}
    (ha : 0 < a) (hab : a < b) (hr : 0 ≤ rho)
    (hv : a * rho ≤ v ∧ v ≤ b * rho)
    (ht : rho ^ 2 / v ≤ tau ∧ tau ≤ ((a + b) * rho - v) / (a * b)) :
    MomentMeasure a b rho v tau := by
  by_cases hr0 : rho = 0
  · have hv0 : v = 0 := by rw [hr0] at hv; simp only [mul_zero] at hv; exact le_antisymm hv.2 hv.1
    have ht0 : tau = 0 := by
      have hz : 0 ≤ tau ∧ tau ≤ 0 := by simpa [hr0, hv0] using ht
      exact le_antisymm hz.2 hz.1
    subst rho; subst v; subst tau
    refine ⟨0, fun _ => a, ?_, by simp, by simp, by simp⟩
    intro i
    exact ⟨le_rfl, le_rfl, hab.le⟩
  · have hrp : 0 < rho := lt_of_le_of_ne hr (Ne.symm hr0)
    have hvp : 0 < v := lt_of_lt_of_le (mul_pos ha hrp) hv.1
    have hc : a ≤ v / rho ∧ v / rho ≤ b :=
      ⟨(le_div_iff₀ hrp).2 hv.1, (div_le_iff₀ hrp).2 hv.2⟩
    have hv_id : rho * (v / rho) = v := by field_simp
    have hL : rho / (v / rho) = rho ^ 2 / v := by field_simp
    obtain ⟨α, hα0, hα1, hα⟩ := interpolate (ht.1.trans ht.2) ht
    have h := momentMeasure_interpolation ha hab hr hc ⟨hα0, hα1⟩
    rw [hv_id, hL, ← hα] at h
    exact h

/-- Exact inverse-moment interval, including the zero-mass boundary. -/
theorem momentMeasure_iff {a b rho v tau : ℝ}
    (ha : 0 < a) (hab : a < b) (hr : 0 ≤ rho)
    (hv : a * rho ≤ v ∧ v ≤ b * rho) :
    MomentMeasure a b rho v tau ↔
      rho ^ 2 / v ≤ tau ∧ tau ≤ ((a + b) * rho - v) / (a * b) := by
  refine ⟨?_, momentMeasure_of_bounds ha hab hr hv⟩
  rintro ⟨w, x, hwx, hw, hx, ht⟩
  have hp : ∀ i, 0 < x i := fun i => lt_of_lt_of_le ha (hwx i).2.1
  have hs := inverse_moment_soc w x (fun i => (hwx i).1) hp
  have hu := inverse_moment_upper ha hab w x (fun i => (hwx i).1)
    (fun i => (hwx i).2)
  rw [hw, hx, ht] at hs hu
  refine ⟨?_, hu⟩
  by_cases hv0 : v = 0
  · rw [hv0, div_zero]
    rw [← ht]
    exact sum_nonneg fun i _ => div_nonneg (hwx i).1 (hp i).le
  · have hvn : 0 ≤ v := (mul_nonneg ha.le hr).trans hv.1
    exact (div_le_iff₀ (lt_of_le_of_ne hvn (Ne.symm hv0))).2 (by nlinarith [hs])

end ReciprocalAnchor
