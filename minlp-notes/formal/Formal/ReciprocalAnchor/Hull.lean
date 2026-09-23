import Formal.ReciprocalAnchor.Allocation
import Formal.ReciprocalAnchor.Moments
import Formal.ReciprocalAnchor.Representation
import Formal.ReciprocalAnchor.PSD

/-! Exact one-leaf reciprocal hull, with all zero-mass boundary cases. -/

namespace ReciprocalAnchor

theorem conicBounds_of_mem_hull {a b m t q w : ℝ} (ha : 0 < a) (hab : a < b)
    (h : point m t q w ∈ hull a b) : ConicBounds a b m t q w := by
  obtain ⟨ι, _, p, x, y, hp, hp1, hx, hy, hm, ht, hq, hw⟩ :=
    mem_hull_has_finite_representation h
  let p₁ : ι → ℝ := fun i => p i * y i
  let p₀ : ι → ℝ := fun i => p i * (1 - y i)
  have hp₁ : ∀ i, 0 ≤ p₁ i := fun i => mul_nonneg (hp i) (hy i).1
  have hp₀ : ∀ i, 0 ≤ p₀ i := fun i => mul_nonneg (hp i) (sub_nonneg.mpr (hy i).2)
  have hm₁ : ∑ i, p₁ i = q := hq
  have hm₀ : ∑ i, p₀ i = 1 - q := by
    simp [p₀, mul_sub, Finset.sum_sub_distrib, hp1, hq]
  have hv₁ : ∑ i, p₁ i * x i = w := by
    simpa [p₁, mul_comm, mul_left_comm, mul_assoc] using hw
  have hv₀ : ∑ i, p₀ i * x i = m - w := by
    simp only [p₀, mul_sub, mul_one, sub_mul, Finset.sum_sub_distrib, hm]
    rw [hv₁]
  have hmassq : 0 ≤ q := hm₁ ▸ Finset.sum_nonneg (fun i _ => hp₁ i)
  have hmassq0 : 0 ≤ 1 - q := hm₀ ▸ Finset.sum_nonneg (fun i _ => hp₀ i)
  have hb₁ := moment_bounds ha hab p₁ x hp₁ hx
  have hb₀ := moment_bounds ha hab p₀ x hp₀ hx
  rw [hm₁, hv₁] at hb₁
  rw [hm₀, hv₀] at hb₀
  have hu := inverse_moment_upper ha hab p x hp hx
  rw [hp1, hm, ht] at hu
  have hparts : (∑ i, p₁ i / x i) + (∑ i, p₀ i / x i) = t := by
    rw [← Finset.sum_add_distrib, ← ht]
    apply Finset.sum_congr rfl
    intro i _
    dsimp [p₁, p₀]
    ring
  refine ⟨⟨hmassq, by linarith, hb₁.1, hb₁.2.1, hb₀.1, hb₀.2.1, ?_⟩,
    ∑ i, p₁ i / x i, ∑ i, p₀ i / x i, ?_, ?_, hb₁.2.2.1, hb₀.2.2.1,
    hparts.le⟩
  · simpa using hu
  · exact Finset.sum_nonneg fun i _ => div_nonneg (hp₁ i) (ha.le.trans (hx i).1)
  · exact Finset.sum_nonneg fun i _ => div_nonneg (hp₀ i) (ha.le.trans (hx i).1)

theorem mem_hull_of_conicBounds {a b m t q w : ℝ} (ha : 0 < a) (hab : a < b)
    (h : ConicBounds a b m t q w) : point m t q w ∈ hull a b := by
  obtain ⟨t₁, t₀, h₁l, h₁u, h₀l, h₀u, hsum⟩ := allocate_moments ha hab h
  obtain ⟨p₁, x₁, hp₁, hm₁, hv₁, ht₁⟩ := momentMeasure_of_bounds ha hab h.1.1
    ⟨h.1.2.2.1, h.1.2.2.2.1⟩ ⟨h₁l, h₁u⟩
  obtain ⟨p₀, x₀, hp₀, hm₀, hv₀, ht₀⟩ := momentMeasure_of_bounds ha hab
    (sub_nonneg.mpr h.1.2.1) ⟨h.1.2.2.2.2.1, h.1.2.2.2.2.2.1⟩ ⟨h₀l, h₀u⟩
  apply finite_representation_mem_hull (Sum.elim p₁ p₀) (Sum.elim x₁ x₀)
    (Sum.elim (fun _ => 1) (fun _ => 0))
  · intro i
    cases i with
    | inl i => exact (hp₁ i).1
    | inr i => exact (hp₀ i).1
  · simp [Fintype.sum_sum_type, hm₁, hm₀]
  · intro i
    cases i with
    | inl i => exact (hp₁ i).2
    | inr i => exact (hp₀ i).2
  · intro i
    cases i <;> norm_num
  · simp [Fintype.sum_sum_type, hv₁, hv₀]
  · simpa [Fintype.sum_sum_type, ht₁, ht₀] using hsum
  · simpa [Fintype.sum_sum_type] using hm₁
  · simpa [Fintype.sum_sum_type] using hv₁

/-- The proposed two rotated SOC formulation equals the full original graph hull. -/
theorem mem_hull_iff_conicBounds {a b m t q w : ℝ} (ha : 0 < a) (hab : a < b) :
    point m t q w ∈ hull a b ↔ ConicBounds a b m t q w :=
  ⟨conicBounds_of_mem_hull ha hab, mem_hull_of_conicBounds ha hab⟩

/-- The matrix in the paper is an actual positive semidefinite matrix condition. -/
theorem mem_hull_iff_psd {a b m t q w : ℝ} (ha : 0 < a) (hab : a < b) :
    point m t q w ∈ hull a b ↔ LinearBounds a b m t q w ∧
      (arrowMatrix w (m - w) q (1 - q) t).PosSemidef := by
  rw [mem_hull_iff_conicBounds ha hab]
  constructor
  · rintro ⟨hlinear, hsoc⟩
    have hw : 0 ≤ w := (mul_nonneg ha.le hlinear.1).trans hlinear.2.2.1
    have hv : 0 ≤ m - w := (mul_nonneg ha.le (sub_nonneg.mpr hlinear.2.1)).trans
      hlinear.2.2.2.2.1
    exact ⟨hlinear, (reciprocal_anchor_psd_iff_soc hw hv).mpr hsoc⟩
  · rintro ⟨hlinear, hpsd⟩
    have hw : 0 ≤ w := (mul_nonneg ha.le hlinear.1).trans hlinear.2.2.1
    have hv : 0 ≤ m - w := (mul_nonneg ha.le (sub_nonneg.mpr hlinear.2.1)).trans
      hlinear.2.2.2.2.1
    exact ⟨hlinear, (reciprocal_anchor_psd_iff_soc hw hv).mp hpsd⟩

end ReciprocalAnchor
