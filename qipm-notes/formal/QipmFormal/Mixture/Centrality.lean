import QipmFormal.Mixture.Defs

/-! # Centrality of finite probability mixtures

Positive coordinates at a common complementarity parameter obey an exact
pairwise variance formula. This file includes its equality case, scalar
Kantorovich bounds, and point-centered normalization.
-/
namespace QipmFormal.Mixture
noncomputable section
open scoped BigOperators

variable {I : Type*} [Fintype I]

def weightedMean (w t : I → ℝ) : ℝ := ∑ i, w i * t i

def multiplicativeDefect (w t : I → ℝ) : ℝ :=
  weightedMean w t * weightedMean w (fun i => (t i)⁻¹) - 1

theorem weighted_multiplicative_variance (w t : I → ℝ)
    (hw : ProbWeights w) (ht : ∀ i, 0 < t i) :
    multiplicativeDefect w t =
      (1 / 2 : ℝ) * ∑ i, ∑ k, w i * w k * (t i - t k)^2 / (t i * t k) := by
  have hp (i k : I) : w i * w k * (t i - t k)^2 / (t i * t k) =
      w i * t i * (w k * (t k)⁻¹) +
      w i * (t i)⁻¹ * (w k * t k) - 2 * w i * w k := by
    field_simp [ne_of_gt (ht i), ne_of_gt (ht k)]
    ring
  simp_rw [hp, Finset.sum_sub_distrib, Finset.sum_add_distrib,
    ← Finset.mul_sum, ← Finset.sum_mul]
  rw [hw.2]
  unfold multiplicativeDefect weightedMean
  ring_nf
  simp only [← Finset.sum_mul, hw.2]
  ring

theorem multiplicativeDefect_nonneg (w t : I → ℝ)
    (hw : ProbWeights w) (ht : ∀ i, 0 < t i) :
    0 ≤ multiplicativeDefect w t := by
  rw [weighted_multiplicative_variance w t hw ht]
  exact mul_nonneg (by norm_num) (Finset.sum_nonneg fun i _ =>
    Finset.sum_nonneg fun k _ => div_nonneg
      (mul_nonneg (mul_nonneg (hw.1 i) (hw.1 k)) (sq_nonneg _))
      (le_of_lt (mul_pos (ht i) (ht k))))

theorem central_mixture_defect (w x s : I → ℝ) (mu : ℝ)
    (hmu : 0 < mu) (ht : ∀ i, 0 < x i) (hc : ∀ i, x i * s i = mu) :
    weightedMean w x * weightedMean w s / mu - 1 = multiplicativeDefect w x := by
  have hs (i : I) : s i = mu * (x i)⁻¹ := by
    field_simp [ne_of_gt (ht i)]
    nlinarith [hc i]
  have hsf : s = fun i => mu * (x i)⁻¹ := funext hs
  rw [hsf]
  have hm : weightedMean w (fun i => mu * (x i)⁻¹) =
      mu * weightedMean w (fun i => (x i)⁻¹) := by
    unfold weightedMean
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    ring
  rw [hm]
  unfold multiplicativeDefect
  field_simp [ne_of_gt hmu]


theorem multiplicativeDefect_eq_zero_iff (w t : I → ℝ)
    (hw : ProbWeights w) (ht : ∀ i, 0 < t i) :
    multiplicativeDefect w t = 0 ↔
      ∀ i k, 0 < w i → 0 < w k → t i = t k := by
  have hn (i k : I) : 0 ≤ w i * w k * (t i - t k)^2 / (t i * t k) :=
    div_nonneg (mul_nonneg (mul_nonneg (hw.1 i) (hw.1 k)) (sq_nonneg _))
      (le_of_lt (mul_pos (ht i) (ht k)))
  rw [weighted_multiplicative_variance w t hw ht]
  constructor
  · intro h i k hi hk
    have hs : (∑ i, ∑ k, w i * w k * (t i - t k)^2 / (t i * t k)) = 0 := by
      linarith
    have hrow := (Finset.sum_eq_zero_iff_of_nonneg
      (fun i _ => Finset.sum_nonneg (fun k _ => hn i k))).mp hs i (Finset.mem_univ i)
    have hterm := (Finset.sum_eq_zero_iff_of_nonneg (fun k _ => hn i k)).mp
      hrow k (Finset.mem_univ k)
    have hz : (t i - t k)^2 = 0 := by
      have hz := (div_eq_zero_iff).mp hterm
      have hm : w i * w k ≠ 0 := ne_of_gt (mul_pos hi hk)
      rcases hz with hz | hz
      · exact (mul_eq_zero.mp hz).resolve_left hm
      · exact False.elim ((ne_of_gt (mul_pos (ht i) (ht k))) hz)
    nlinarith [sq_nonneg (t i - t k)]
  · intro h
    have hs : (∑ i, ∑ k, w i * w k * (t i - t k)^2 / (t i * t k)) = 0 := by
      apply Finset.sum_eq_zero
      intro i _
      apply Finset.sum_eq_zero
      intro k _
      by_cases hi : w i = 0
      · simp [hi]
      by_cases hk : w k = 0
      · simp [hk]
      have heq := h i k (lt_of_le_of_ne (hw.1 i) (Ne.symm hi))
        (lt_of_le_of_ne (hw.1 k) (Ne.symm hk))
      simp [heq]
    rw [hs, mul_zero]

theorem uniform_multiplicativeDefect_eq_zero_iff [Nonempty I] (t : I → ℝ)
    (ht : ∀ i, 0 < t i) :
    multiplicativeDefect (uniformWeight I) t = 0 ↔ ∀ i k, t i = t k := by
  rw [multiplicativeDefect_eq_zero_iff _ _ (uniformWeight_prob I) ht]
  have hp (i : I) : 0 < uniformWeight I i :=
    inv_pos.mpr (Nat.cast_pos.mpr Fintype.card_pos)
  exact ⟨fun h i k => h i k (hp i) (hp k), fun h i k _ _ => h i k⟩

theorem kantorovich_bound (w t : I → ℝ) (hw : ProbWeights w)
    (alpha beta : ℝ) (ha : 0 < alpha)
    (hl : ∀ i, alpha ≤ t i) (hu : ∀ i, t i ≤ beta) :
    weightedMean w t * weightedMean w (fun i => (t i)⁻¹) ≤
      (alpha + beta)^2 / (4 * alpha * beta) := by
  have hex : Nonempty I := by
    by_contra h
    have : IsEmpty I := not_nonempty_iff.mp h
    have := hw.2
    simp at this
  let i := Classical.choice hex
  have ht (j : I) : 0 < t j := lt_of_lt_of_le ha (hl j)
  have hb : 0 < beta := lt_of_lt_of_le (ht i) (hu i)
  have hp (j : I) : t j + alpha * beta * (t j)⁻¹ ≤ alpha + beta := by
    have hprod := mul_nonneg (sub_nonneg.mpr (hl j)) (sub_nonneg.mpr (hu j))
    have heq : t j + alpha * beta * (t j)⁻¹ =
        (t j ^ 2 + alpha * beta) / t j := by
      field_simp
    rw [heq]
    apply (div_le_iff₀ (ht j)).mpr
    nlinarith
  have hsum := Finset.sum_le_sum (fun j (_ : j ∈ Finset.univ) =>
    mul_le_mul_of_nonneg_left (hp j) (hw.1 j))
  have hid : (∑ j, w j * (t j + alpha * beta * (t j)⁻¹)) =
      weightedMean w t + alpha * beta * weightedMean w (fun j => (t j)⁻¹) := by
    unfold weightedMean
    simp_rw [mul_add, Finset.sum_add_distrib]
    rw [Finset.mul_sum]
    congr 1
    apply Finset.sum_congr rfl
    intro j _
    ring
  rw [hid, ← Finset.sum_mul, hw.2, one_mul] at hsum
  have hx : 0 ≤ weightedMean w t := Finset.sum_nonneg
    (fun j _ => mul_nonneg (hw.1 j) (ht j).le)
  have hy : 0 ≤ weightedMean w (fun j => (t j)⁻¹) := Finset.sum_nonneg
    (fun j _ => mul_nonneg (hw.1 j) (inv_pos.mpr (ht j)).le)
  apply (le_div_iff₀ (by positivity : 0 < 4 * alpha * beta)).mpr
  have hsq := sq_nonneg (weightedMean w t - alpha * beta *
    weightedMean w (fun j => (t j)⁻¹))
  have hsqsum : (weightedMean w t + alpha * beta *
      weightedMean w (fun j => (t j)⁻¹))^2 ≤ (alpha + beta)^2 :=
    pow_le_pow_left₀ (by positivity) hsum 2
  nlinarith


/-- The scalar Kantorovich constant for a positive multiplicative range. -/
def kantorovich (R : ℝ) : ℝ := (R + 1)^2 / (4 * R)

theorem kantorovich_sub_one (R : ℝ) (hR : 0 < R) :
    kantorovich R - 1 = (R - 1)^2 / (4 * R) := by
  unfold kantorovich
  field_simp
  ring

theorem kantorovich_ratio_bound (w t : I → ℝ) (hw : ProbWeights w)
    (alpha R : ℝ) (ha : 0 < alpha) (hR : 0 < R)
    (hl : ∀ i, alpha ≤ t i) (hu : ∀ i, t i ≤ R * alpha) :
    multiplicativeDefect w t ≤ kantorovich R - 1 := by
  have h := kantorovich_bound w t hw alpha (R * alpha) ha hl hu
  have heq : (alpha + R * alpha)^2 / (4 * alpha * (R * alpha)) =
      kantorovich R := by
    unfold kantorovich
    field_simp
    ring
  rw [heq] at h
  exact sub_le_sub_right h 1

theorem kantorovich_pairwise_ratio_bound [Nonempty I] (w t : I → ℝ)
    (hw : ProbWeights w) (ht : ∀ i, 0 < t i) (R : ℝ) (hR : 0 < R)
    (hratio : ∀ i k, t i / t k ≤ R) :
    multiplicativeDefect w t ≤ kantorovich R - 1 := by
  obtain ⟨k, _, hk⟩ := Finset.exists_min_image Finset.univ t Finset.univ_nonempty
  exact kantorovich_ratio_bound w t hw (t k) R (ht k) hR
    (fun i => hk i (Finset.mem_univ i))
    (fun i => (div_le_iff₀ (ht k)).mp (hratio i k))

theorem uniform_multiplicative_variance [Nonempty I] (t : I → ℝ)
    (ht : ∀ i, 0 < t i) :
    multiplicativeDefect (uniformWeight I) t =
      1 / (2 * (Fintype.card I : ℝ)^2) *
        ∑ i, ∑ k, (t i - t k)^2 / (t i * t k) := by
  rw [weighted_multiplicative_variance _ _ (uniformWeight_prob I) ht]
  unfold uniformWeight
  simp_rw [mul_div_assoc, ← Finset.mul_sum]
  ring

/-- Uniform finite mean, including the empty convention only at definition level. -/
def coordinateMean {C : Type*} [Fintype C] (d : C → ℝ) : ℝ :=
  (∑ j, d j) / Fintype.card C

theorem coordinateMean_bounds {C : Type*} [Fintype C] [Nonempty C]
    (d : C → ℝ) (D : ℝ) (hd : ∀ j, 0 ≤ d j ∧ d j ≤ D) :
    0 ≤ coordinateMean d ∧ coordinateMean d ≤ D := by
  have hn : (0 : ℝ) < Fintype.card C := Nat.cast_pos.mpr Fintype.card_pos
  constructor
  · exact div_nonneg (Finset.sum_nonneg fun j _ => (hd j).1) hn.le
  · apply (div_le_iff₀ hn).mpr
    calc
      ∑ j, d j ≤ ∑ _j : C, D := Finset.sum_le_sum (fun j _ => (hd j).2)
      _ = D * Fintype.card C := by simp [mul_comm]

theorem point_centered_defect_identity {C : Type*} [Fintype C] [Nonempty C]
    (p d : C → ℝ) (mu : ℝ) (hmu : 0 < mu)
    (hp : ∀ j, p j = mu * (1 + d j)) (hd : ∀ j, 0 ≤ d j) (j : C) :
    p j / coordinateMean p - 1 =
      (d j - coordinateMean d) / (1 + coordinateMean d) := by
  have hn : (0 : ℝ) < Fintype.card C := Nat.cast_pos.mpr Fintype.card_pos
  have hm : 0 ≤ coordinateMean d :=
    div_nonneg (Finset.sum_nonneg fun j _ => hd j) hn.le
  have hmean : coordinateMean p = mu * (1 + coordinateMean d) := by
    unfold coordinateMean
    simp_rw [hp, mul_add, Finset.sum_add_distrib, mul_one]
    rw [← Finset.mul_sum]
    simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
    field_simp
  rw [hmean, hp]
  field_simp
  ring

theorem point_centered_defect_bound {C : Type*} [Fintype C] [Nonempty C]
    (d : C → ℝ) (D : ℝ) (hd : ∀ j, 0 ≤ d j ∧ d j ≤ D) (j : C) :
    |d j - coordinateMean d| / (1 + coordinateMean d) ≤ D := by
  obtain ⟨hm0, hmD⟩ := coordinateMean_bounds d D hd
  have hD : 0 ≤ D := (hd j).1.trans (hd j).2
  have habs : |d j - coordinateMean d| ≤ D := by
    apply abs_le.mpr
    constructor <;> linarith [(hd j).1, (hd j).2]
  apply (div_le_iff₀ (by linarith : 0 < 1 + coordinateMean d)).mpr
  nlinarith


/-- Direct bridge from the manuscript's maximum/minimum ratio hypothesis. -/
theorem kantorovich_extrema_ratio_bound [Nonempty I] (w t : I → ℝ)
    (hw : ProbWeights w) (ht : ∀ i, 0 < t i) (R : ℝ) (hR : 0 < R)
    (hratio : Finset.univ.sup' Finset.univ_nonempty t /
      Finset.univ.inf' Finset.univ_nonempty t ≤ R) :
    multiplicativeDefect w t ≤ kantorovich R - 1 := by
  have hmin : 0 < Finset.univ.inf' Finset.univ_nonempty t :=
    (Finset.lt_inf'_iff _).mpr (fun i _ => ht i)
  apply kantorovich_ratio_bound w t hw
    (Finset.univ.inf' Finset.univ_nonempty t) R hmin hR
  · intro i
    exact Finset.inf'_le t (Finset.mem_univ i)
  · intro i
    exact (Finset.le_sup' t (Finset.mem_univ i)).trans
      ((div_le_iff₀ hmin).mp hratio)

theorem central_mixture_product_bounds [Nonempty I] (w x s : I → ℝ)
    (hw : ProbWeights w) (mu R : ℝ) (hmu : 0 < mu) (hR : 0 < R)
    (hx : ∀ i, 0 < x i) (hc : ∀ i, x i * s i = mu)
    (hratio : ∀ i k, x i / x k ≤ R) :
    mu ≤ weightedMean w x * weightedMean w s ∧
      weightedMean w x * weightedMean w s ≤ kantorovich R * mu := by
  have hid := central_mixture_defect w x s mu hmu hx hc
  have hlo := multiplicativeDefect_nonneg w x hw hx
  have hhi := kantorovich_pairwise_ratio_bound w x hw hx R hR hratio
  constructor
  · have h : (1 : ℝ) ≤ weightedMean w x * weightedMean w s / mu := by linarith
    simpa using (le_div_iff₀ hmu).mp h
  · apply (div_le_iff₀ hmu).mp
    linarith

theorem central_uniform_variance [Nonempty I] (x s : I → ℝ) (mu : ℝ)
    (hmu : 0 < mu) (hx : ∀ i, 0 < x i) (hc : ∀ i, x i * s i = mu) :
    weightedMean (uniformWeight I) x * weightedMean (uniformWeight I) s / mu - 1 =
      1 / (2 * (Fintype.card I : ℝ)^2) *
        ∑ i, ∑ k, (x i - x k)^2 / (x i * x k) := by
  rw [central_mixture_defect _ _ _ _ hmu hx hc,
    uniform_multiplicative_variance x hx]

theorem point_centered_absolute_defect_identity
    {C : Type*} [Fintype C] [Nonempty C]
    (p d : C → ℝ) (mu : ℝ) (hmu : 0 < mu)
    (hp : ∀ j, p j = mu * (1 + d j)) (hd : ∀ j, 0 ≤ d j) (j : C) :
    |p j / coordinateMean p - 1| =
      |d j - coordinateMean d| / (1 + coordinateMean d) := by
  rw [point_centered_defect_identity p d mu hmu hp hd j, abs_div]
  have hm : 0 ≤ coordinateMean d := div_nonneg
    (Finset.sum_nonneg fun j _ => hd j) (Nat.cast_nonneg _)
  rw [abs_of_pos (by linarith : 0 < 1 + coordinateMean d)]

/-- The finite maximum of coordinate defects is the exact infinity width. -/
theorem point_centered_width_identity {C : Type*} [Fintype C] [Nonempty C]
    (p d : C → ℝ) (mu : ℝ) (hmu : 0 < mu)
    (hp : ∀ j, p j = mu * (1 + d j)) (hd : ∀ j, 0 ≤ d j) :
    Finset.univ.sup' Finset.univ_nonempty (fun j => |p j / coordinateMean p - 1|) =
      Finset.univ.sup' Finset.univ_nonempty (fun j => |d j - coordinateMean d|) /
        (1 + coordinateMean d) := by
  have hm : 0 ≤ coordinateMean d := div_nonneg
    (Finset.sum_nonneg fun j _ => hd j) (Nat.cast_nonneg _)
  have hmpos : 0 < 1 + coordinateMean d := by linarith
  apply le_antisymm
  · apply Finset.sup'_le
    intro j _
    rw [point_centered_absolute_defect_identity p d mu hmu hp hd j]
    exact div_le_div_of_nonneg_right
      (Finset.le_sup' (fun j => |d j - coordinateMean d|) (Finset.mem_univ j)) hmpos.le
  · obtain ⟨j, hj, heq⟩ := Finset.exists_mem_eq_sup' Finset.univ_nonempty
      (fun j => |d j - coordinateMean d|)
    rw [heq, ← point_centered_absolute_defect_identity p d mu hmu hp hd j]
    exact Finset.le_sup' (fun j => |p j / coordinateMean p - 1|) hj


/-- The manuscript's extrema ratio is equivalent to all coordinate ratios. -/
theorem extrema_ratio_iff_pairwise [Nonempty I] (t : I → ℝ)
    (ht : ∀ i, 0 < t i) (R : ℝ) :
    Finset.univ.sup' Finset.univ_nonempty t /
      Finset.univ.inf' Finset.univ_nonempty t ≤ R ↔
      ∀ i k, t i / t k ≤ R := by
  have hmin : 0 < Finset.univ.inf' Finset.univ_nonempty t :=
    (Finset.lt_inf'_iff _).mpr (fun i _ => ht i)
  constructor
  · intro h i k
    calc
      t i / t k ≤ t i / Finset.univ.inf' Finset.univ_nonempty t :=
        div_le_div_of_nonneg_left (ht i).le hmin
          (Finset.inf'_le t (Finset.mem_univ k))
      _ ≤ Finset.univ.sup' Finset.univ_nonempty t /
          Finset.univ.inf' Finset.univ_nonempty t :=
        div_le_div_of_nonneg_right (Finset.le_sup' t (Finset.mem_univ i)) hmin.le
      _ ≤ R := h
  · intro h
    obtain ⟨i, _, hi⟩ := Finset.exists_mem_eq_sup' Finset.univ_nonempty t
    obtain ⟨k, _, hk⟩ := Finset.exists_mem_eq_inf' Finset.univ_nonempty t
    rw [hi, hk]
    exact h i k

end
end QipmFormal.Mixture
