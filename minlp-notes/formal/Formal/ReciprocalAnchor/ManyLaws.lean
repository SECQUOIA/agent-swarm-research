import Formal.ReciprocalAnchor.ManyModel
import Formal.ReciprocalAnchor.Hull

/-! Finite law operations, endpoint extremizers, and necessary hull inequalities. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

variable {a b : ℝ}

theorem Law.mean_bounds (μ : Law a b) : a ≤ μ.mean ∧ μ.mean ≤ b := by
  constructor
  · calc
      a = ∑ i, μ.mass i * a := by rw [← Finset.sum_mul, μ.total, one_mul]
      _ ≤ μ.mean := Finset.sum_le_sum fun i _ =>
        mul_le_mul_of_nonneg_left (μ.bounds i).1 (μ.nonneg i)
  · calc
      μ.mean ≤ ∑ i, μ.mass i * b := Finset.sum_le_sum fun i _ =>
        mul_le_mul_of_nonneg_left (μ.bounds i).2 (μ.nonneg i)
      _ = b := by rw [← Finset.sum_mul, μ.total, one_mul]

theorem Law.reciprocal_upper (μ : Law a b) (ha : 0 < a) (hab : a < b) :
    μ.reciprocal ≤ (a + b - μ.mean) / (a * b) := by
  have h := ReciprocalAnchor.inverse_moment_upper ha hab μ.mass μ.location μ.nonneg μ.bounds
  simpa only [Law.reciprocal, Law.mean, μ.total, mul_one] using h

theorem Law.call_nonneg (μ : Law a b) (s : ℝ) : 0 ≤ μ.call s :=
  Finset.sum_nonneg fun i _ => mul_nonneg (μ.nonneg i) (le_max_right _ _)

theorem Law.mean_sub_le_call (μ : Law a b) (s : ℝ) : μ.mean - s ≤ μ.call s := by
  calc
    μ.mean - s = ∑ i, μ.mass i * (μ.location i - s) := by
      simp [Law.mean, mul_sub, Finset.sum_sub_distrib, ← Finset.sum_mul, μ.total]
    _ ≤ μ.call s := Finset.sum_le_sum fun i _ =>
      mul_le_mul_of_nonneg_left (le_max_left _ _) (μ.nonneg i)

theorem Law.call_left (μ : Law a b) {s : ℝ} (hs : s ≤ a) : μ.call s = μ.mean - s := by
  have hi : ∀ i, max (μ.location i - s) 0 = μ.location i - s :=
    fun i => max_eq_left (sub_nonneg.mpr (hs.trans (μ.bounds i).1))
  simp [Law.call, hi, mul_sub, Finset.sum_sub_distrib, ← Finset.sum_mul, μ.total, Law.mean]

theorem Law.call_right (μ : Law a b) {s : ℝ} (hs : b ≤ s) : μ.call s = 0 := by
  have hi : ∀ i, max (μ.location i - s) 0 = 0 :=
    fun i => max_eq_right (sub_nonpos.mpr ((μ.bounds i).2.trans hs))
  simp [Law.call, hi]

noncomputable def Law.endpoints (a b m : ℝ) (hab : a < b) (hm : a ≤ m ∧ m ≤ b) :
    Law a b where
  size := 2
  mass := ![(b - m) / (b - a), (m - a) / (b - a)]
  location := ![a, b]
  nonneg := by
    intro i
    fin_cases i
    · exact div_nonneg (sub_nonneg.mpr hm.2) (sub_pos.mpr hab).le
    · exact div_nonneg (sub_nonneg.mpr hm.1) (sub_pos.mpr hab).le
  total := by
    simp only [Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one]
    field_simp [ne_of_gt (sub_pos.mpr hab)]
    ring
  bounds := by intro i; fin_cases i <;> simp [hab.le]

theorem Law.endpoints_mean (m : ℝ) (hab : a < b) (hm : a ≤ m ∧ m ≤ b) :
    (Law.endpoints a b m hab hm).mean = m := by
  change (∑ i : Fin 2, ![(b-m)/(b-a), (m-a)/(b-a)] i * ![a,b] i) = m
  simp only [Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one]
  field_simp [ne_of_gt (sub_pos.mpr hab)]
  ring

theorem Law.endpoints_reciprocal (m : ℝ) (ha : 0 < a) (hab : a < b)
    (hm : a ≤ m ∧ m ≤ b) :
    (Law.endpoints a b m hab hm).reciprocal = (a + b - m) / (a * b) := by
  have ha0 := ne_of_gt ha
  have hb0 := ne_of_gt (ha.trans hab)
  have hba := ne_of_gt (sub_pos.mpr hab)
  change (∑ i : Fin 2, ![(b-m)/(b-a), (m-a)/(b-a)] i / ![a,b] i) = _
  simp only [Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one]
  field_simp
  ring

theorem Law.endpoints_call (m s : ℝ) (hab : a < b) (hm : a ≤ m ∧ m ≤ b) :
    (Law.endpoints a b m hab hm).call s =
      (b - m) / (b - a) * max (a - s) 0 + (m - a) / (b - a) * max (b - s) 0 := by
  change (∑ i : Fin 2, ![(b-m)/(b-a), (m-a)/(b-a)] i * max (![a,b] i - s) 0) = _
  simp only [Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one]

theorem call_secant (hab : a < b) {x : ℝ} (hx : a ≤ x ∧ x ≤ b) (s : ℝ) :
    max (x - s) 0 ≤ (b - x) / (b - a) * max (a - s) 0 +
      (x - a) / (b - a) * max (b - s) 0 := by
  have h₁ : 0 ≤ (b - x) / (b - a) :=
    div_nonneg (sub_nonneg.mpr hx.2) (sub_pos.mpr hab).le
  have h₂ : 0 ≤ (x - a) / (b - a) :=
    div_nonneg (sub_nonneg.mpr hx.1) (sub_pos.mpr hab).le
  apply max_le
  · calc
      x - s = (b - x) / (b - a) * (a - s) + (x - a) / (b - a) * (b - s) := by
        field_simp [ne_of_gt (sub_pos.mpr hab)]
        ring
      _ ≤ _ := add_le_add (mul_le_mul_of_nonneg_left (le_max_left _ _) h₁)
        (mul_le_mul_of_nonneg_left (le_max_left _ _) h₂)
  · exact add_nonneg (mul_nonneg h₁ (le_max_right _ _))
      (mul_nonneg h₂ (le_max_right _ _))

theorem Law.call_le_endpoints (μ : Law a b) (hab : a < b) (s : ℝ) :
    μ.call s ≤ (Law.endpoints a b μ.mean hab μ.mean_bounds).call s := by
  calc
    μ.call s ≤ ∑ i, μ.mass i * ((b - μ.location i) / (b - a) * max (a - s) 0 +
        (μ.location i - a) / (b - a) * max (b - s) 0) :=
      Finset.sum_le_sum fun i _ =>
        mul_le_mul_of_nonneg_left (call_secant hab (μ.bounds i) s) (μ.nonneg i)
    _ = (Law.endpoints a b μ.mean hab μ.mean_bounds).call s := by
      rw [Law.endpoints_call]
      simp only [mul_add, Finset.sum_add_distrib, ← mul_assoc, ← Finset.sum_mul]
      have hleft : (∑ i, μ.mass i * ((b - μ.location i) / (b - a))) =
          (b - μ.mean) / (b - a) := by
        simp only [← mul_div_assoc, ← Finset.sum_div, mul_sub, Finset.sum_sub_distrib,
          ← Finset.sum_mul, μ.total, one_mul, Law.mean]
      have hright : (∑ i, μ.mass i * ((μ.location i - a) / (b - a))) =
          (μ.mean - a) / (b - a) := by
        simp only [← mul_div_assoc, ← Finset.sum_div, mul_sub, Finset.sum_sub_distrib,
          ← Finset.sum_mul, μ.total, one_mul, Law.mean]
      rw [hleft, hright]

noncomputable def Law.mix (μ ν : Law a b) (r : ℝ) (hr : 0 ≤ r ∧ r ≤ 1) : Law a b :=
  Law.ofFinite (Sum.elim (fun i => (1 - r) * μ.mass i) (fun i => r * ν.mass i))
    (Sum.elim μ.location ν.location)
    (by intro i; cases i with
        | inl i => exact mul_nonneg (sub_nonneg.mpr hr.2) (μ.nonneg i)
        | inr i => exact mul_nonneg hr.1 (ν.nonneg i))
    (by simp [Fintype.sum_sum_type, ← Finset.mul_sum, μ.total, ν.total])
    (by intro i; cases i with
        | inl i => exact μ.bounds i
        | inr i => exact ν.bounds i)

theorem Law.mix_size (μ ν : Law a b) (r : ℝ) (hr : 0 ≤ r ∧ r ≤ 1) :
    (μ.mix ν r hr).size = μ.size + ν.size := by simp [Law.mix, Law.ofFinite]

theorem Law.mix_mean (μ ν : Law a b) (r : ℝ) (hr : 0 ≤ r ∧ r ≤ 1) :
    (μ.mix ν r hr).mean = (1 - r) * μ.mean + r * ν.mean := by
  unfold Law.mix
  rw [Law.ofFinite_mean]
  simp [Fintype.sum_sum_type, mul_assoc, ← Finset.mul_sum, Law.mean]

theorem Law.mix_reciprocal (μ ν : Law a b) (r : ℝ) (hr : 0 ≤ r ∧ r ≤ 1) :
    (μ.mix ν r hr).reciprocal = (1 - r) * μ.reciprocal + r * ν.reciprocal := by
  unfold Law.mix
  rw [Law.ofFinite_reciprocal]
  simp [Fintype.sum_sum_type, mul_div_assoc, ← Finset.mul_sum, Law.reciprocal]

theorem Law.mix_call (μ ν : Law a b) (r : ℝ) (hr : 0 ≤ r ∧ r ≤ 1) (s : ℝ) :
    (μ.mix ν r hr).call s = (1 - r) * μ.call s + r * ν.call s := by
  unfold Law.mix
  rw [Law.ofFinite_call]
  simp [Fintype.sum_sum_type, mul_assoc, ← Finset.mul_sum, Law.call]

theorem mem_hull_mean_bounds {n : ℕ} {m t : ℝ} {q w : Fin n → ℝ}
    (h : point m t q w ∈ hull n a b) : a ≤ m ∧ m ≤ b := by
  obtain ⟨ι, _, p, x, y, hp, hp1, hx, hy, hm, ht, hq, hw⟩ :=
    mem_hull_has_finite_representation h
  have hb := (Law.ofFinite p x hp hp1 hx).mean_bounds
  rwa [Law.ofFinite_mean, hm] at hb

theorem mem_hull_reciprocal_upper {n : ℕ} {m t : ℝ} {q w : Fin n → ℝ}
    (ha : 0 < a) (hab : a < b) (h : point m t q w ∈ hull n a b) :
    t ≤ (a + b - m) / (a * b) := by
  obtain ⟨ι, _, p, x, y, hp, hp1, hx, hy, hm, ht, hq, hw⟩ :=
    mem_hull_has_finite_representation h
  have hu := ReciprocalAnchor.inverse_moment_upper ha hab p x hp hx
  simpa only [hp1, mul_one, hm, ht] using hu

theorem mem_hull_leaf_projection {n : ℕ} {m t : ℝ} {q w : Fin n → ℝ}
    (h : point m t q w ∈ hull n a b) (j : Fin n) :
    ReciprocalAnchor.point m t (q j) (w j) ∈ ReciprocalAnchor.hull a b := by
  obtain ⟨ι, _, p, x, y, hp, hp1, hx, hy, hm, ht, hq, hw⟩ :=
    mem_hull_has_finite_representation h
  exact ReciprocalAnchor.finite_representation_mem_hull p x (fun i => y i j)
    hp hp1 hx (fun i => hy i j) hm ht (hq j) (hw j)

theorem mem_hull_linearBounds {n : ℕ} {m t : ℝ} {q w : Fin n → ℝ}
    (ha : 0 < a) (hab : a < b) (h : point m t q w ∈ hull n a b) :
    LinearBounds a b m q w := by
  refine ⟨(mem_hull_mean_bounds h).1, (mem_hull_mean_bounds h).2, fun j => ?_⟩
  have hb := (ReciprocalAnchor.conicBounds_of_mem_hull ha hab
    (mem_hull_leaf_projection h j)).1
  exact ⟨hb.1, hb.2.1, hb.2.2.1, hb.2.2.2.1, hb.2.2.2.2.1, hb.2.2.2.2.2.1⟩

end ReciprocalAnchor.ManyLeaf
