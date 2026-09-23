import QipmFormal.Mixture.Defs

/-! # Output preservation and elementary encoding operations for mixtures -/
namespace QipmFormal.Mixture
noncomputable section
open scoped BigOperators
variable {I C : Type*} [Fintype I] [Fintype C]

omit [Fintype C] in
theorem mix_nonneg {w : I → ℝ} (hw : ProbWeights w) {x : I → C → ℝ}
    (hx : ∀ i j, 0 ≤ x i j) : ∀ j, 0 ≤ mix w x j := by
  intro j
  exact Finset.sum_nonneg fun i _ => mul_nonneg (hw.1 i) (hx i j)

omit [Fintype C] in
theorem mix_abs_le {w : I → ℝ} (hw : ProbWeights w) {x : I → C → ℝ}
    {H : ℝ} (hx : ∀ i j, |x i j| ≤ H) : ∀ j, |mix w x j| ≤ H := by
  intro j
  calc
    |mix w x j| ≤ ∑ i, |w i * x i j| := Finset.abs_sum_le_sum_abs _ _
    _ = ∑ i, w i * |x i j| := by simp [abs_mul, abs_of_nonneg (hw.1 _)]
    _ ≤ ∑ i, w i * H := Finset.sum_le_sum fun i _ => mul_le_mul_of_nonneg_left (hx i j) (hw.1 i)
    _ = H := by rw [← Finset.sum_mul, hw.2, one_mul]

theorem dot_mix (w : I → ℝ) (x : I → C → ℝ) (c : C → ℝ) :
    dot c (mix w x) = ∑ i, w i * dot c (x i) := by
  simp only [dot, mix, Finset.mul_sum]
  rw [Finset.sum_comm]
  congr 1
  ext i
  exact Finset.sum_congr rfl fun j _ => by ring

theorem mix_objective {w : I → ℝ} (hw : ProbWeights w) {x : I → C → ℝ}
    {c : C → ℝ} {v : ℝ} (hx : ∀ i, dot c (x i) = v) :
    dot c (mix w x) = v := by
  rw [dot_mix]
  simp_rw [hx]
  rw [← Finset.sum_mul, hw.2, one_mul]

theorem mix_affine_score {w : I → ℝ} (hw : ProbWeights w) (x : I → C → ℝ)
    (c : C → ℝ) (a₀ : ℝ) :
    dot c (mix w x) - a₀ = ∑ i, w i * (dot c (x i) - a₀) := by
  simp_rw [mul_sub]
  rw [Finset.sum_sub_distrib, ← Finset.sum_mul, hw.2, one_mul, dot_mix]

theorem mix_signed_margin {w : I → ℝ} (hw : ProbWeights w) {x : I → C → ℝ}
    {c : C → ℝ} {a₀ p γ : ℝ} (hx : ∀ i, γ ≤ p * (dot c (x i) - a₀)) :
    γ ≤ p * (dot c (mix w x) - a₀) := by
  rw [mix_affine_score hw, Finset.mul_sum]
  calc
    γ = ∑ i, w i * γ := by rw [← Finset.sum_mul, hw.2, one_mul]
    _ ≤ ∑ i, p * (w i * (dot c (x i) - a₀)) := by
      apply Finset.sum_le_sum
      intro i _
      calc
        w i * γ ≤ w i * (p * (dot c (x i) - a₀)) := mul_le_mul_of_nonneg_left (hx i) (hw.1 i)
        _ = _ := by ring

omit [Fintype C] in
theorem mix_mem_convex {w : I → ℝ} (hw : ProbWeights w) {x : I → C → ℝ}
    {K : Set (C → ℝ)} (hK : Convex ℝ K) (hx : ∀ i, x i ∈ K) : mix w x ∈ K := by
  have h := hK.sum_mem (t := Finset.univ) (w := w) (z := x)
    (fun i _ => hw.1 i) hw.2 (fun i _ => hx i)
  have heq : mix w x = ∑ i, w i • x i := by
    ext j
    simp [mix, Finset.sum_apply]
  rw [heq]
  exact h

omit [Fintype C] in
theorem mix_pair_margin {w : I → ℝ} (hw : ProbWeights w) {x : I → C → ℝ}
    {u v : C} {p a : ℝ} (hx : ∀ i, a ≤ p * (x i u - x i v)) :
    a ≤ p * (mix w x u - mix w x v) := by
  change a ≤ p * ((∑ i, w i * x i u) - ∑ i, w i * x i v)
  rw [← Finset.sum_sub_distrib, Finset.mul_sum]
  calc
    a = ∑ i, w i * a := by rw [← Finset.sum_mul, hw.2, one_mul]
    _ ≤ _ := Finset.sum_le_sum fun i _ => by
      have := mul_le_mul_of_nonneg_left (hx i) (hw.1 i)
      nlinarith

theorem signed_pair_sq_margin {u v p a : ℝ} (hu : 0 ≤ u) (hv : 0 ≤ v)
    (hp : p = 1 ∨ p = -1) (ha : 0 ≤ a) (h : a ≤ p * (u - v)) :
    a ^ 2 ≤ p * (u ^ 2 - v ^ 2) := by
  rcases hp with rfl | rfl
  · have hsum : a ≤ u + v := by linarith
    have hm := mul_le_mul h hsum ha (by linarith : 0 ≤ 1 * (u-v))
    nlinarith
  · have hsum : a ≤ u + v := by linarith
    have hm := mul_le_mul h hsum ha (by linarith : 0 ≤ -1 * (u-v))
    nlinarith

theorem sqNorm_height {x : C → ℝ} {H : ℝ} (hx : ∀ j, |x j| ≤ H) :
    sqNorm x ≤ (Fintype.card C : ℝ) * H ^ 2 := by
  calc
    sqNorm x ≤ ∑ _j : C, H ^ 2 := Finset.sum_le_sum fun j _ => by
      have := hx j
      have := sq_le_sq₀ (abs_nonneg (x j)) (le_trans (abs_nonneg _) (hx j)) |>.mpr (hx j)
      simpa using this
    _ = _ := by simp

/-- True selects the positive output coordinate and false the negative one. -/
def pairNumerator {P : Type*} [Fintype P] (e : P × Bool ↪ C) (x : C → ℝ) : ℝ :=
  ∑ l, (x (e (l, true)) ^ 2 - x (e (l, false)) ^ 2)

def pairExpectation {P : Type*} [Fintype P] (e : P × Bool ↪ C) (x : C → ℝ) : ℝ :=
  pairNumerator e x / sqNorm x

theorem pair_numerator_abs_le {P : Type*} [Fintype P] (e : P × Bool ↪ C)
    (x : C → ℝ) : |pairNumerator e x| ≤ sqNorm x := by
  classical
  calc
    |pairNumerator e x| ≤ ∑ l, |x (e (l, true)) ^ 2 - x (e (l, false)) ^ 2| :=
      Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ l, (x (e (l, true)) ^ 2 + x (e (l, false)) ^ 2) := by
      apply Finset.sum_le_sum
      intro l _
      apply abs_le.mpr
      constructor <;> nlinarith [sq_nonneg (x (e (l, true))), sq_nonneg (x (e (l, false)))]
    _ = ∑ q : P × Bool, x (e q) ^ 2 := by simp [Fintype.sum_prod_type]
    _ = ∑ j ∈ Finset.univ.map e, x j ^ 2 := by simp [Finset.sum_map]
    _ ≤ sqNorm x := Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _)
      (fun j _ _ => sq_nonneg _)

theorem pair_expectation_abs_le_one {P : Type*} [Fintype P]
    (e : P × Bool ↪ C) {x : C → ℝ} (hx : 0 < sqNorm x) :
    |pairExpectation e x| ≤ 1 := by
  rw [pairExpectation, abs_div, abs_of_pos hx, div_le_one hx]
  exact pair_numerator_abs_le e x

theorem pair_margin_sqNorm_pos {P : Type*} [Nonempty P]
    (e : P × Bool ↪ C) {x : C → ℝ} {p a : ℝ}
    (ha : 0 < a) (h : ∀ l, a ≤ p * (x (e (l, true)) - x (e (l, false)))) :
    0 < sqNorm x := by
  classical
  obtain ⟨l⟩ := ‹Nonempty P›
  by_contra hn
  have hz : sqNorm x = 0 := le_antisymm (le_of_not_gt hn) (sqNorm_nonneg x)
  have hall : ∀ j, x j = 0 := by
    intro j
    have hj : x j ^ 2 ≤ sqNorm x :=
      Finset.single_le_sum (fun i _ => sq_nonneg (x i)) (Finset.mem_univ j)
    rw [hz] at hj
    nlinarith [sq_nonneg (x j)]
  have := h l
  simp only [hall, sub_self, mul_zero] at this
  linarith

theorem pair_decoder_bound {P : Type*} [Fintype P] [Nonempty P]
    (e : P × Bool ↪ C) {x : C → ℝ} {p a H : ℝ}
    (hx : ∀ j, 0 ≤ x j) (hh : ∀ j, |x j| ≤ H)
    (hp : p = 1 ∨ p = -1) (ha : 0 < a)
    (h : ∀ l, a ≤ p * (x (e (l, true)) - x (e (l, false)))) :
    (Fintype.card P : ℝ) * a ^ 2 / ((Fintype.card C : ℝ) * H ^ 2)
      ≤ p * pairExpectation e x := by
  have hn := pair_margin_sqNorm_pos e ha h
  have hh' := sqNorm_height hh
  have hnum : (Fintype.card P : ℝ) * a ^ 2 ≤ p * pairNumerator e x := by
    rw [pairNumerator, Finset.mul_sum]
    calc
      _ = ∑ _l : P, a ^ 2 := by simp
      _ ≤ _ := Finset.sum_le_sum fun l _ => signed_pair_sq_margin
        (hx _) (hx _) hp ha.le (h l)
  calc
    _ ≤ ((Fintype.card P : ℝ) * a ^ 2) / sqNorm x :=
      div_le_div_of_nonneg_left (mul_nonneg (Nat.cast_nonneg _) (sq_nonneg _)) hn hh'
    _ ≤ (p * pairNumerator e x) / sqNorm x := div_le_div_of_nonneg_right hnum hn.le
    _ = _ := by simp only [pairExpectation]; ring

/-- Binary measurement uses a fair coin outside the public output pairs. -/
def pairPositiveProbability {P : Type*} [Fintype P] (e : P × Bool ↪ C)
    (x : C → ℝ) : ℝ := (1 + pairExpectation e x) / 2

theorem pair_probability_valid {P : Type*} [Fintype P]
    (e : P × Bool ↪ C) {x : C → ℝ} (hx : 0 < sqNorm x) :
    0 ≤ pairPositiveProbability e x ∧ pairPositiveProbability e x ≤ 1 := by
  have h := abs_le.mp (pair_expectation_abs_le_one e hx)
  unfold pairPositiveProbability
  constructor <;> linarith

theorem pair_probability_bias {P : Type*} [Fintype P]
    (e : P × Bool ↪ C) (x : C → ℝ) :
    pairPositiveProbability e x - 1 / 2 = pairExpectation e x / 2 := by
  unfold pairPositiveProbability
  ring

/-- The observable is evaluated on the genuinely normalized vector. -/
theorem pair_expectation_normalized {P : Type*} [Fintype P]
    (e : P × Bool ↪ C) (x : C → ℝ) :
    pairNumerator e (fun j => x j / euclideanNorm x) = pairExpectation e x := by
  unfold pairExpectation pairNumerator
  simp only [div_pow, euclideanNorm_sq, ← sub_div, ← Finset.sum_div]

/-- Sum of positive-coordinate probability plus a fair coin on the remaining mass. -/
theorem pair_probability_fair_outside {P : Type*} [Fintype P]
    (e : P × Bool ↪ C) (x : C → ℝ) :
    pairPositiveProbability e x =
      (∑ l, x (e (l, true)) ^ 2) / sqNorm x +
        (1 - (∑ q : P × Bool, x (e q) ^ 2) / sqNorm x) / 2 := by
  simp only [pairPositiveProbability, pairExpectation, pairNumerator,
    Finset.sum_sub_distrib, Fintype.sum_prod_type, Fintype.sum_bool,
    Finset.sum_add_distrib]
  ring

theorem mixture_pair_decoder_bound {P : Type*} [Fintype P] [Nonempty P]
    (e : P × Bool ↪ C) {w : I → ℝ} (hw : ProbWeights w)
    {x : I → C → ℝ} {p a H : ℝ}
    (hx : ∀ i j, 0 ≤ x i j) (hh : ∀ i j, |x i j| ≤ H)
    (hp : p = 1 ∨ p = -1) (ha : 0 < a)
    (hm : ∀ i l, a ≤ p * (x i (e (l, true)) - x i (e (l, false)))) :
    0 < sqNorm (mix w x) ∧
    (Fintype.card P : ℝ) * a ^ 2 / ((Fintype.card C : ℝ) * H ^ 2)
      ≤ p * pairExpectation e (mix w x) := by
  have hm' := fun l => mix_pair_margin hw (fun i => hm i l)
  exact ⟨pair_margin_sqNorm_pos e ha hm',
    pair_decoder_bound e (mix_nonneg hw hx) (mix_abs_le hw hh) hp ha hm'⟩

/-- Negating exactly one input sign reverses product parity. -/
theorem parity_flip [DecidableEq I] (σ : I → ℝ) (i : I) :
    (∏ j, Function.update σ i (-σ i) j) = -(∏ j, σ j) := by
  rw [Finset.prod_update_of_mem (Finset.mem_univ i)]
  have hprod : (∏ j, σ j) = σ i * ∏ j ∈ Finset.univ \ {i}, σ j :=
    Finset.prod_eq_mul_prod_sdiff_singleton i σ (by simp)
  rw [hprod]
  ring

/-- A sign input has a sign-valued product parity. -/
theorem parity_is_sign (σ : I → ℝ) (hσ : ∀ i, σ i = 1 ∨ σ i = -1) :
    (∏ i, σ i) = 1 ∨ (∏ i, σ i) = -1 := by
  classical
  have h : ∀ s : Finset I, (∏ i ∈ s, σ i) = 1 ∨ (∏ i ∈ s, σ i) = -1 := by
    intro s
    induction s using Finset.induction_on with
    | empty => simp
    | @insert i s hi ih =>
      rw [Finset.prod_insert hi]
      rcases hσ i with h₁ | h₁ <;> rcases ih with h₂ | h₂ <;> simp [h₁, h₂]
  exact h Finset.univ

/-- Correct signed scores on flipped inputs give wrong signed scores at the base. -/
theorem single_flip_affine_wrong [DecidableEq I] (σ : I → ℝ)
    {w : I → ℝ} (hw : ProbWeights w) {x : I → C → ℝ}
    {c : C → ℝ} {a₀ γ : ℝ}
    (h : ∀ i, γ ≤ (∏ j, Function.update σ i (-σ i) j) * (dot c (x i) - a₀)) :
    (∏ j, σ j) * (dot c (mix w x) - a₀) ≤ -γ := by
  have hm := mix_signed_margin hw (p := -(∏ j, σ j)) (fun i => by
    simpa only [parity_flip] using h i)
  linarith

omit [Fintype C] in
/-- Half-base interpolation preserves every fixed convex domain. -/
theorem half_base_mem_convex {K : Set (C → ℝ)} (hK : Convex ℝ K)
    {x₀ x₁ : C → ℝ} (h₀ : x₀ ∈ K) (h₁ : x₁ ∈ K) :
    (fun j => (x₀ j + x₁ j) / 2) ∈ K := by
  have h := hK h₀ h₁ (show (0 : ℝ) ≤ 1/2 by norm_num)
    (show (0 : ℝ) ≤ 1/2 by norm_num) (show (1/2 : ℝ) + 1/2 = 1 by norm_num)
  convert h using 1
  ext j
  simp
  ring

theorem half_base_objective (c x₀ x₁ : C → ℝ) {v : ℝ}
    (h₀ : dot c x₀ = v) (h₁ : dot c x₁ = v) :
    dot c (fun j => (x₀ j + x₁ j) / 2) = v := by
  have he : dot c (fun j => (x₀ j + x₁ j) / 2) = (dot c x₀ + dot c x₁) / 2 := by
    simp only [dot, ← mul_div_assoc, mul_add, ← Finset.sum_div, Finset.sum_add_distrib]
  rw [he, h₀, h₁]
  ring

omit [Fintype C] in
theorem half_base_map {D : Type*} [AddCommGroup D] [Module ℝ D]
    (L : (C → ℝ) →ₗ[ℝ] D) (x₀ x₁ : C → ℝ) (h : L x₁ = -L x₀) :
    L (fun j => (x₀ j + x₁ j) / 2) = 0 := by
  have he : (fun j => (x₀ j + x₁ j) / 2) = (1/2 : ℝ) • (x₀ + x₁) := by
    ext j
    simp
    ring
  rw [he, map_smul, map_add, h, add_neg_cancel, smul_zero]

theorem half_base_residual {R : Type*} (A : R → C → ℝ) (x₀ x₁ : C → ℝ)
    (b : R → ℝ) (h₀ : ∀ r, residual A x₀ b r = 0) :
    residual A (fun j => (x₀ j + x₁ j) / 2) b = fun r => residual A x₁ b r / 2 := by
  ext r
  have h := h₀ r
  simp only [residual] at h ⊢
  simp only [← mul_div_assoc, mul_add, ← Finset.sum_div, Finset.sum_add_distrib]
  linarith


omit [Fintype C] in
theorem linearMap_mix {D : Type*} [AddCommGroup D] [Module ℝ D]
    (L : (C → ℝ) →ₗ[ℝ] D) (w : I → ℝ) (x : I → C → ℝ) :
    L (mix w x) = ∑ i, w i • L (x i) := by
  have he : mix w x = ∑ i, w i • x i := by
    ext j
    simp [mix, Finset.sum_apply]
  rw [he, map_sum]
  simp

omit [Fintype C] in
/-- Uniform opposite templates cancel the base template under half-base mixing. -/
theorem half_base_mixture_map {D : Type*} [AddCommGroup D] [Module ℝ D]
    (L : (C → ℝ) →ₗ[ℝ] D) {w : I → ℝ} (hw : ProbWeights w)
    (x₀ : C → ℝ) (x : I → C → ℝ) (h : ∀ i, L (x i) = -L x₀) :
    L (fun j => (x₀ j + mix w x j) / 2) = 0 := by
  apply half_base_map
  rw [linearMap_mix]
  simp_rw [h]
  rw [← Finset.sum_smul, hw.2, one_smul]

theorem half_base_residual_norm {R : Type*} [Fintype R]
    (A : R → C → ℝ) (x₀ x₁ : C → ℝ) (b : R → ℝ)
    (h₀ : ∀ r, residual A x₀ b r = 0) :
    euclideanNorm (residual A (fun j => (x₀ j + x₁ j) / 2) b) =
      euclideanNorm (residual A x₁ b) / 2 := by
  rw [half_base_residual A x₀ x₁ b h₀]
  unfold euclideanNorm sqNorm
  simp only [div_pow, ← Finset.sum_div, Real.sqrt_div (Finset.sum_nonneg
    (fun _ _ => sq_nonneg _))]
  norm_num

end
end QipmFormal.Mixture
