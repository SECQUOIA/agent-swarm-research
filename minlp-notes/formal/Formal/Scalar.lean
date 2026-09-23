import Formal.Model

namespace ExactCounts

def boxL : ℚ := (7 / 4) * (1 - 1 / 48) ^ 32
def boxD : ℚ := (7 / 4) * (1 / 48) ^ 32
def boxLo : Fin 3 → Fin 3 → ℚ :=
  ![![0, boxL, 0], ![1 / 48, 0, 0], ![1 - 1 / 48, 0, boxL]]
def boxHi : Fin 3 → Fin 3 → ℚ :=
  ![![1 / 48, 7 / 4, boxD], ![1 - 1 / 48, boxL, boxL], ![1, boxD, 7 / 4]]
def InBox (j : Fin 3) (v : Point) : Prop :=
  ∀ k, (boxLo j k : ℝ) ≤ v k ∧ v k ≤ (boxHi j k : ℝ)

private theorem constants :
    0 ≤ (boxD : ℝ) ∧ (boxD : ℝ) < 1 / 4 ∧
    3 / 4 < (boxL : ℝ) ∧ (boxL : ℝ) < 1 := by
  norm_num [boxD, boxL]

private theorem right_mono {x y : ℝ} (hx : 0 ≤ x) (hxy : x ≤ y) :
    rightValue x ≤ rightValue y := by
  exact mul_le_mul_of_nonneg_left (pow_le_pow_left₀ hx hxy 32) (by norm_num)

private theorem left_mono {x y : ℝ} (hy : y ≤ 1) (hxy : x ≤ y) :
    leftValue y ≤ leftValue x := by
  exact mul_le_mul_of_nonneg_left (pow_le_pow_left₀ (by linarith) (by linarith) 32) (by norm_num)

private theorem endpoint_values :
    rightValue 0 = 0 ∧ rightValue 1 = 7 / 4 ∧
    rightValue (1 / 48) = (boxD : ℝ) ∧ rightValue (1 - 1 / 48) = (boxL : ℝ) ∧
    leftValue 0 = 7 / 4 ∧ leftValue 1 = 0 ∧
    leftValue (1 / 48) = (boxL : ℝ) ∧ leftValue (1 - 1 / 48) = (boxD : ℝ) := by
  norm_num [rightValue, leftValue, boxD, boxL]

private theorem value_nonneg (x : ℝ) : 0 ≤ leftValue x ∧ 0 ≤ rightValue x := by
  constructor <;> dsimp [leftValue, rightValue] <;> positivity

private theorem left_interval {x : ℝ} (hx : 0 ≤ x) (hc : x ≤ 1 / 48) :
    (boxL : ℝ) ≤ leftValue x ∧ leftValue x ≤ 7 / 4 ∧
    0 ≤ rightValue x ∧ rightValue x ≤ (boxD : ℝ) := by
  have a := left_mono (x := x) (y := 1 / 48) (by norm_num) hc
  have b := left_mono (x := 0) (y := x) (by linarith) hx
  have d := right_mono hx hc
  rcases endpoint_values with ⟨_, _, eD, _, e0, _, eL, _⟩
  rw [eL] at a
  rw [e0] at b
  rw [eD] at d
  exact ⟨a, b, (value_nonneg x).2, d⟩

private theorem middle_interval {x : ℝ} (hc : 1 / 48 ≤ x) (hx : x ≤ 1 - 1 / 48) :
    0 ≤ leftValue x ∧ leftValue x ≤ (boxL : ℝ) ∧
    0 ≤ rightValue x ∧ rightValue x ≤ (boxL : ℝ) := by
  have a := left_mono (x := 1 / 48) (y := x) (by linarith) hc
  have b := right_mono (by linarith : 0 ≤ x) hx
  rcases endpoint_values with ⟨_, _, _, eR, _, _, eL, _⟩
  rw [eL] at a
  rw [eR] at b
  exact ⟨(value_nonneg x).1, a, (value_nonneg x).2, b⟩

private theorem right_interval {x : ℝ} (hc : 1 - 1 / 48 ≤ x) (hx : x ≤ 1) :
    0 ≤ leftValue x ∧ leftValue x ≤ (boxD : ℝ) ∧
    (boxL : ℝ) ≤ rightValue x ∧ rightValue x ≤ 7 / 4 := by
  have a := left_mono hx hc
  have b := right_mono (x := 1 - 1 / 48) (y := x) (by norm_num) hc
  have d := right_mono (by linarith : 0 ≤ x) hx
  rcases endpoint_values with ⟨_, e1, _, eL, _, _, _, eD⟩
  rw [eD] at a
  rw [eL] at b
  rw [e1] at d
  exact ⟨(value_nonneg x).1, a, b, d⟩

theorem graph_in_box {x : ℝ} (hx : 0 ≤ x) (hx1 : x ≤ 1) :
    ∃ j, InBox j (graphPoint x) := by
  by_cases h0 : x ≤ 1 / 48
  · refine ⟨0, ?_⟩
    have h := left_interval hx h0
    intro k
    fin_cases k <;> simp [boxLo, boxHi, graphPoint] <;> constructor <;> linarith
  · by_cases h1 : x ≤ 1 - 1 / 48
    · refine ⟨1, ?_⟩
      have hc : 1 / 48 ≤ x := le_of_lt (lt_of_not_ge h0)
      have h := middle_interval hc h1
      intro k
      fin_cases k <;> simp [boxLo, boxHi, graphPoint] <;> constructor <;> linarith
    · refine ⟨2, ?_⟩
      have hc : 1 - 1 / 48 ≤ x := le_of_lt (lt_of_not_ge h1)
      have h := right_interval hc hx1
      intro k
      fin_cases k <;> simp [boxLo, boxHi, graphPoint] <;> constructor <;> linarith

theorem inBox_valid {j : Fin 3} {v : Point} (hv : InBox j v) : ValidPoint v := by
  have h0 := hv 0
  have h1 := hv 1
  have h2 := hv 2
  have hC := constants
  fin_cases j <;> simp only [boxLo, boxHi, one_div, Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk,
    Fin.isValue, Matrix.cons_val', Matrix.cons_val_zero, Matrix.cons_val_fin_one,
    Matrix.cons_val_one, Matrix.cons_val, Rat.cast_zero, Rat.cast_inv, Rat.cast_ofNat,
    Rat.cast_div, Rat.cast_sub, Rat.cast_one, tsub_le_iff_right] at h0 h1 h2
  · have h := left_interval h0.1 (by linarith)
    unfold ValidPoint
    refine ⟨h0.1, by linarith, ?_, ?_⟩ <;> rw [abs_le] <;> constructor <;> linarith
  · have h := middle_interval (x := v 0) (by linarith) (by linarith)
    unfold ValidPoint
    refine ⟨by linarith, by linarith, ?_, ?_⟩ <;> rw [abs_le] <;> constructor <;> linarith
  · have h := right_interval (by linarith) h0.2
    unfold ValidPoint
    refine ⟨by linarith, h0.2, ?_, ?_⟩ <;> rw [abs_le] <;> constructor <;> linarith

theorem integer_mixture_valid (w : Fin 3 → ℝ) (v : Point) (z : ℤ)
    (hw : ∀ j, 0 ≤ w j) (hs : ∑ j, w j = 1)
    (hv : ∀ k, (∑ j, w j * (boxLo j k : ℝ)) ≤ v k ∧
      v k ≤ ∑ j, w j * (boxHi j k : ℝ))
    (hz : (z : ℝ) = ∑ j, w j * (j.val : ℝ)) : ValidPoint v := by
  have h0 := hw 0
  have h1 := hw 1
  have h2 := hw 2
  simp only [Fin.sum_univ_succ, Fin.isValue, Fin.succ_zero_eq_one, Finset.univ_unique,
    Fin.default_eq_zero, Finset.sum_singleton, Fin.succ_one_eq_two, Fin.coe_ofNat_eq_mod,
    Nat.zero_mod, CharP.cast_eq_zero, mul_zero, Fin.val_succ, Nat.cast_add, Nat.cast_one,
    zero_add, mul_one, Fin.val_eq_zero] at hs hz
  have hz0 : (0 : ℝ) ≤ z := by linarith
  have hz2 : (z : ℝ) ≤ 2 := by linarith
  have iz0 : 0 ≤ z := by exact_mod_cast hz0
  have iz2 : z ≤ 2 := by exact_mod_cast hz2
  interval_cases z
  · have hw1 : w 1 = 0 := by norm_num at hz; linarith
    have hw2 : w 2 = 0 := by norm_num at hz; linarith
    have hw0 : w 0 = 1 := by linarith
    apply inBox_valid (j := 0)
    intro k
    simpa [Fin.sum_univ_succ, hw0, hw1, hw2] using hv k
  · have heq : w 0 = w 2 := by norm_num at hz; linarith
    have hx := hv 0
    have hy := hv 1
    have ht := hv 2
    simp [Fin.sum_univ_succ, boxLo, boxHi] at hx hy ht
    have hC := constants
    have hxlo : 1 / 48 ≤ v 0 := by nlinarith
    have hxhi : v 0 ≤ 1 - 1 / 48 := by nlinarith
    have hv1lo : 0 ≤ v 1 := by nlinarith
    have hv2lo : 0 ≤ v 2 := by nlinarith
    have hv1hi : v 1 ≤ 1 := by nlinarith
    have hv2hi : v 2 ≤ 1 := by nlinarith
    have h := middle_interval hxlo hxhi
    unfold ValidPoint
    refine ⟨by linarith, by linarith, ?_, ?_⟩ <;> rw [abs_le] <;> constructor <;> linarith
  · have hw0 : w 0 = 0 := by norm_num at hz; linarith
    have hw1 : w 1 = 0 := by norm_num at hz; linarith
    have hw2 : w 2 = 1 := by linarith
    apply inBox_valid (j := 2)
    intro k
    simpa [Fin.sum_univ_succ, hw0, hw1, hw2] using hv k

/-- Both degree-32 component functions are convex on the input interval. -/
theorem rightValue_convex : ConvexOn ℝ (Set.Icc 0 1) rightValue := by
  have h := (convexOn_pow (𝕜 := ℝ) 32).smul (c := (7 / 4 : ℝ)) (by norm_num)
  apply h.subset (fun x hx => hx.1) (convex_Icc 0 1)

theorem leftValue_convex : ConvexOn ℝ (Set.Icc 0 1) leftValue := by
  refine ⟨convex_Icc 0 1, ?_⟩
  intro x hx y hy a b ha hb hab
  have h := (convexOn_pow (𝕜 := ℝ) 32).2
    (show 1 - x ∈ Set.Ici (0 : ℝ) by simp only [Set.mem_Ici]; linarith [hx.2])
    (show 1 - y ∈ Set.Ici (0 : ℝ) by simp only [Set.mem_Ici]; linarith [hy.2])
    ha hb hab
  simp only [smul_eq_mul] at h ⊢
  have heq : 1 - (a * x + b * y) = a * (1 - x) + b * (1 - y) := by linear_combination -hab
  dsimp [leftValue]
  rw [heq]
  have hh := mul_le_mul_of_nonneg_left h (by norm_num : (0 : ℝ) ≤ 7 / 4)
  simpa only [mul_add, mul_left_comm] using hh

end ExactCounts
