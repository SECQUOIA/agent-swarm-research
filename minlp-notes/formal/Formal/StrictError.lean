import Formal.IntegerPolyhedron

/-! Strict unit error holds for every integer slice of the explicit formulation. -/
namespace ExactCounts

/-- The input stays in the unit interval and both output errors are strictly below one. -/
def StrictValidPoint (v : Point) : Prop :=
  0 ≤ v 0 ∧ v 0 ≤ 1 ∧
  |v 1 - leftValue (v 0)| < 1 ∧ |v 2 - rightValue (v 0)| < 1

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

theorem inBox_strict_valid {j : Fin 3} {v : Point} (hv : InBox j v) : StrictValidPoint v := by
  have h0 := hv 0
  have h1 := hv 1
  have h2 := hv 2
  have hC := constants
  fin_cases j <;> simp only [boxLo, boxHi, one_div, Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk,
    Fin.isValue, Matrix.cons_val', Matrix.cons_val_zero, Matrix.cons_val_fin_one,
    Matrix.cons_val_one, Matrix.cons_val, Rat.cast_zero, Rat.cast_inv, Rat.cast_ofNat,
    Rat.cast_div, Rat.cast_sub, Rat.cast_one, tsub_le_iff_right] at h0 h1 h2
  · have h := left_interval h0.1 (by linarith)
    unfold StrictValidPoint
    refine ⟨h0.1, by linarith, ?_, ?_⟩ <;> rw [abs_lt] <;> constructor <;> linarith
  · have h := middle_interval (x := v 0) (by linarith) (by linarith)
    unfold StrictValidPoint
    refine ⟨by linarith, by linarith, ?_, ?_⟩ <;> rw [abs_lt] <;> constructor <;> linarith
  · have h := right_interval (by linarith) h0.2
    unfold StrictValidPoint
    refine ⟨by linarith, h0.2, ?_, ?_⟩ <;> rw [abs_lt] <;> constructor <;> linarith

theorem integer_mixture_strict_valid (w : Fin 3 → ℝ) (v : Point) (z : ℤ)
    (hw : ∀ j, 0 ≤ w j) (hs : ∑ j, w j = 1)
    (hv : ∀ k, (∑ j, w j * (boxLo j k : ℝ)) ≤ v k ∧
      v k ≤ ∑ j, w j * (boxHi j k : ℝ))
    (hz : (z : ℝ) = ∑ j, w j * (j.val : ℝ)) : StrictValidPoint v := by
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
    apply inBox_strict_valid (j := 0)
    intro k
    simpa [Fin.sum_univ_succ, hw0, hw1, hw2] using hv k
  · have heq : w 0 = w 2 := by norm_num at hz; linarith
    have hC := constants
    have hmix : w 0 * (7 / 4) + w 1 * (boxL : ℝ) + w 2 * (boxD : ℝ) < 1 := by
      by_cases hz : w 0 = 0
      · have hz2 : w 2 = 0 := heq.symm.trans hz
        have ho : w 1 = 1 := by linarith only [hs, hz, hz2]
        simpa [hz, hz2, ho] using hC.2.2.2
      · have hp : 0 < w 0 * (1 / 4 - (boxD : ℝ)) :=
          mul_pos (lt_of_le_of_ne h0 (Ne.symm hz)) (sub_pos.mpr hC.2.1)
        have hq : 0 ≤ w 1 * (1 - (boxL : ℝ)) :=
          mul_nonneg h1 (sub_nonneg.mpr hC.2.2.2.le)
        rw [← heq] at hs ⊢
        nlinarith only [hp, hq, hs]
    have hx := hv 0
    have hy := hv 1
    have ht := hv 2
    simp [Fin.sum_univ_succ, boxLo, boxHi] at hx hy ht
    have hxlo : 1 / 48 ≤ v 0 := by nlinarith
    have hxhi : v 0 ≤ 1 - 1 / 48 := by nlinarith
    have hv1lo : 0 ≤ v 1 := by nlinarith
    have hv2lo : 0 ≤ v 2 := by nlinarith
    have hv1hi : v 1 < 1 := by linarith
    have hv2hi : v 2 < 1 := by nlinarith
    have h := middle_interval hxlo hxhi
    unfold StrictValidPoint
    refine ⟨by linarith, by linarith, ?_, ?_⟩ <;> rw [abs_lt] <;> constructor <;> linarith
  · have hw0 : w 0 = 0 := by norm_num at hz; linarith
    have hw1 : w 1 = 0 := by norm_num at hz; linarith
    have hw2 : w 2 = 1 := by linarith
    apply inBox_strict_valid (j := 2)
    intro k
    simpa [Fin.sum_univ_succ, hw0, hw1, hw2] using hv k

/-- Every feasible integer code in the explicit product formulation has strict error. -/
theorem integerSystem_strict_sound {n : ℕ} {v : Visible n} {z : Code n}
    {a : Fin (n * 3) → ℝ} (hz : z ∈ IntegerCodes n)
    (hy : IntegerSystem (v, z, a)) : ∀ i, StrictValidPoint (v i) := by
  obtain ⟨k, rfl⟩ := hz
  intro i
  obtain ⟨hw, hs, hv, he⟩ := hy i
  apply integer_mixture_strict_valid (fun j => a (finProdFinEquiv (i, j)))
    (v i) (k i) hw hs
  · exact hv 0
  · simpa using he 0

/-- The concrete thirteen-inequality-per-coordinate system has strict unit error. -/
theorem integerRows_strict_sound {n : ℕ} {v : Visible n} {z : Code n}
    {a : Fin (n * 3) → ℝ} (hz : z ∈ IntegerCodes n)
    (hy : (v, z, a) ∈ rationalPolyhedron integerRows) : ∀ i, StrictValidPoint (v i) :=
  integerSystem_strict_sound hz ((integerRows_iff _).mp hy)

end ExactCounts
