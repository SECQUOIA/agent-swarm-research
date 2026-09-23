import QipmFormal.ScalarCert.Enclosures
import QipmFormal.ScalarCert.Certificate

/-!
# The strict lower certificate

The witness of `appendix-scalar-certificate.tex`, §"The strict lower
certificate":  `v₀ = 3787/4000`, `w₀ = 9797031/10⁷`, `a₀ = 68743/50000`.

The five displayed enclosures and the two margins of
`eq:lower-certificate-margins` are proved here with the paper's own constants,
and combined with `ratio_gt_of_witness` to give `a₀ < ratio v₀`.
-/

namespace QipmFormal.ScalarCert

open Real Set

set_option exponentiation.threshold 1000000

/-- `v₀ = 3787/4000`. -/
noncomputable def v0 : ℝ := 3787 / 4000
/-- `w₀ = 9797031/10⁷`. -/
noncomputable def w0 : ℝ := 9797031 / 10 ^ 7
/-- `a₀ = 68743/50000`. -/
noncomputable def a0 : ℝ := 68743 / 50000

lemma v0_pos : 0 < v0 := by rw [v0]; norm_num
lemma v0_lt_one : v0 < 1 := by rw [v0]; norm_num
lemma w0_pos : 0 < w0 := by rw [w0]; norm_num
lemma w0_lt_one : w0 < 1 := by rw [w0]; norm_num
lemma v0_abs : |v0| < 1 := by rw [abs_of_pos v0_pos]; exact v0_lt_one
lemma w0_abs : |w0| < 1 := by rw [abs_of_pos w0_pos]; exact w0_lt_one

lemma v0_cast : v0 = ((3787 : ℕ) : ℝ) / ((4000 : ℕ) : ℝ) := by rw [v0]; norm_num
lemma w0_cast : w0 = ((9797031 : ℕ) : ℝ) / ((10 ^ 7 : ℕ) : ℝ) := by rw [w0]; norm_num

/-! ### Kernel-evaluated facts

Scale `10⁴⁰`; 401 series terms at `v₀`, 801 at `w₀` (more are needed at `w₀`
because it is closer to `1`). -/

set_option maxRecDepth 4000000 in
theorem accLo_v0 : accLo (3787 * 3787) (4000 * 4000) (10 ^ 40) 0 400
    = 25917684095385256719822647335332941562636 := by decide

set_option maxRecDepth 4000000 in
theorem accHi_v0 : accHi (3787 * 3787) (4000 * 4000) (10 ^ 40) 0 400
    = 25917684095385256719822647335332941562652 := by decide

set_option maxRecDepth 4000000 in
theorem accLo_w0 : accLo (9797031 * 9797031) (10 ^ 7 * 10 ^ 7) (10 ^ 40) 0 800
    = 34434720900986994098716914895868377674240 := by decide

set_option maxRecDepth 4000000 in
theorem pow_v0_nat : 3787 ^ 803 * 10 ^ 19 ≤ 4000 ^ 803 := by decide

/-! ### The tail at `v₀` -/

lemma pow_v0 : v0 ^ 803 ≤ 1 / 10 ^ 19 := by
  rw [v0, div_pow, div_le_div_iff₀ (by positivity) (by positivity), one_mul]
  exact_mod_cast pow_v0_nat

lemma tail_v0 :
    2 * v0 ^ (2 * (400 + 1) + 1) / ((2 * ((400 : ℕ) + 1 : ℝ) + 1) * (1 - v0 ^ 2))
      ≤ 1 / 10 ^ 20 := by
  have hden : (2 * ((400 : ℕ) + 1 : ℝ) + 1) * (1 - v0 ^ 2) = 1331880693 / 16000000 := by
    rw [v0]; push_cast; norm_num
  have hnn : (0:ℝ) ≤ v0 ^ 803 := pow_nonneg v0_pos.le _
  have hp := pow_v0
  rw [show 2 * (400 + 1) + 1 = 803 from rfl, hden, div_le_iff₀ (by norm_num)]
  linarith

/-! ### The displayed enclosures of the appendix -/

lemma Y_v0_lower_raw : v0 * (25917684095385256719822647335332941562636 / 10 ^ 40) ≤ Y v0 := by
  have h := Y_ge_accLo (a := 3787) (b := 4000) (s := 10 ^ 40) (z := v0)
    v0_cast (by norm_num) (by norm_num) (by norm_num) 400
  rw [accLo_v0] at h; push_cast at h; linarith

lemma Y_v0_upper_raw :
    Y v0 ≤ v0 * (25917684095385256719822647335332941562652 / 10 ^ 40) + 1 / 10 ^ 20 := by
  have h := Y_le_accHi (a := 3787) (b := 4000) (s := 10 ^ 40) (z := v0)
    v0_cast (by norm_num) (by norm_num) (by norm_num) 400
  rw [accHi_v0] at h
  have ht := tail_v0
  push_cast at h ht; linarith

lemma Y_w0_lower_raw : w0 * (34434720900986994098716914895868377674240 / 10 ^ 40) ≤ Y w0 := by
  have h := Y_ge_accLo (a := 9797031) (b := 10 ^ 7) (s := 10 ^ 40) (z := w0)
    w0_cast (by norm_num) (by norm_num) (by norm_num) 800
  rw [accLo_w0] at h; push_cast at h; linarith

/-- `2453756741730599/10¹⁵ < Y v₀`, the appendix's displayed lower bound. -/
theorem Y_v0_gt : (2453756741730599 : ℝ) / 10 ^ 15 < Y v0 := by
  have h := Y_v0_lower_raw
  have : (2453756741730599 : ℝ) / 10 ^ 15
      < v0 * (25917684095385256719822647335332941562636 / 10 ^ 40) := by
    rw [v0]; norm_num
  linarith

/-- `Y v₀ < 12268783708653/(5·10¹²)`, the appendix's displayed upper bound. -/
theorem Y_v0_lt : Y v0 < (12268783708653 : ℝ) / (5 * 10 ^ 12) := by
  have h := Y_v0_upper_raw
  have : v0 * (25917684095385256719822647335332941562652 / 10 ^ 40) + 1 / 10 ^ 20
      < (12268783708653 : ℝ) / (5 * 10 ^ 12) := by
    rw [v0]; norm_num
  linarith

/-- `134943211257327/(4·10¹³) < Y w₀`, the appendix's displayed lower bound. -/
theorem Y_w0_gt : (134943211257327 : ℝ) / (4 * 10 ^ 13) < Y w0 := by
  have h := Y_w0_lower_raw
  have : (134943211257327 : ℝ) / (4 * 10 ^ 13)
      < w0 * (34434720900986994098716914895868377674240 / 10 ^ 40) := by
    rw [w0]; norm_num
  linarith

/-- `405367307458211/(4·10¹³) < A v₀`, the appendix's displayed lower bound,
by rational squaring with `q = 5252771738568124759020057/(5·10²⁴)`. -/
theorem A_v0_gt : (405367307458211 : ℝ) / (4 * 10 ^ 13) < A v0 := by
  have hq : (5252771738568124759020057 / 5000000000000000000000000 : ℝ) / (1 - v0 ^ 2) ≤ A v0 :=
    le_A v0_abs (by norm_num) (by rw [v0]; norm_num)
  have : (405367307458211 : ℝ) / (4 * 10 ^ 13)
      < (5252771738568124759020057 / 5000000000000000000000000 : ℝ) / (1 - v0 ^ 2) := by
    rw [v0]; norm_num
  linarith

/-- `A w₀ < 25381942601625079/10¹⁵`, the appendix's displayed upper bound,
by rational squaring with `r = 10198930511825198233293417/10²⁵`. -/
theorem A_w0_lt : A w0 < (25381942601625079 : ℝ) / 10 ^ 15 := by
  have hr : A w0 ≤ (10198930511825198233293417 / 10000000000000000000000000 : ℝ) / (1 - w0 ^ 2) :=
    A_le w0_abs (by norm_num) (by rw [w0]; norm_num)
  have : (10198930511825198233293417 / 10000000000000000000000000 : ℝ) / (1 - w0 ^ 2)
      < (25381942601625079 : ℝ) / 10 ^ 15 := by
    rw [w0]; norm_num
  linarith

/-! ### The two margins of `eq:lower-certificate-margins` -/

/-- `Y w₀ - a₀ Y v₀ > 2071874360571/(2.5·10¹⁷)`. -/
theorem margin_one : (2071874360571 : ℝ) / 250000000000000000 < Y w0 - a0 * Y v0 := by
  have h1 := Y_v0_lt
  have h2 := Y_w0_gt
  have ha0 : (0:ℝ) < a0 := by rw [a0]; norm_num
  have hstep : a0 * Y v0 < a0 * ((12268783708653 : ℝ) / (5 * 10 ^ 12)) :=
    mul_lt_mul_of_pos_left h1 ha0
  have hrat : (2071874360571 : ℝ) / 250000000000000000
      ≤ (134943211257327 : ℝ) / (4 * 10 ^ 13) - a0 * ((12268783708653 : ℝ) / (5 * 10 ^ 12)) := by
    rw [a0]; norm_num
  linarith

/-- `Y v₀ A v₀ - w₀ A w₀ > 2049519399569150216498389/(4·10²⁸)`. -/
theorem margin_two :
    (2049519399569150216498389 : ℝ) / 40000000000000000000000000000 < Y v0 * A v0 - w0 * A w0 := by
  have hY := Y_v0_gt
  have hA := A_v0_gt
  have hAw := A_w0_lt
  have hYnn : (0:ℝ) ≤ (2453756741730599 : ℝ) / 10 ^ 15 := by norm_num
  have hAnn : (0:ℝ) ≤ (405367307458211 : ℝ) / (4 * 10 ^ 13) := by norm_num
  have hprod : (2453756741730599 : ℝ) / 10 ^ 15 * ((405367307458211 : ℝ) / (4 * 10 ^ 13))
      < Y v0 * A v0 :=
    mul_lt_mul'' hY hA hYnn hAnn
  have hw : w0 * A w0 < w0 * ((25381942601625079 : ℝ) / 10 ^ 15) :=
    mul_lt_mul_of_pos_left hAw w0_pos
  have hrat : (2049519399569150216498389 : ℝ) / 40000000000000000000000000000
      ≤ (2453756741730599 : ℝ) / 10 ^ 15 * ((405367307458211 : ℝ) / (4 * 10 ^ 13))
        - w0 * ((25381942601625079 : ℝ) / 10 ^ 15) := by
    rw [w0]; norm_num
  linarith

/-! ### The strict lower certificate -/

lemma margin_one' : a0 * Y v0 < Y w0 := by have := margin_one; norm_num at this ⊢; linarith

lemma margin_two' : P w0 < Y v0 * A v0 := by
  have h := margin_two
  have hP : P w0 = w0 * A w0 := rfl
  rw [hP]; norm_num at h ⊢; linarith

/-- The dilation ratio at `v₀` exceeds `a₀ = 68743/50000`. -/
theorem a0_lt_ratio_v0 : a0 < ratio v0 :=
  ratio_gt_of_witness v0_pos v0_lt_one w0_pos w0_lt_one margin_one' margin_two'

/-- **Strict lower certificate.**  Some `v ∈ (0,1)` has dilation ratio above
`68743/50000`.  Unconditional: it uses no boundedness hypothesis. -/
theorem exists_ratio_gt : ∃ v ∈ Ioo (0:ℝ) 1, (68743 : ℝ) / 50000 < ratio v :=
  ⟨v0, ⟨v0_pos, v0_lt_one⟩, a0_lt_ratio_v0⟩

/-- If the dilation ratios are bounded above, then `68743/50000 < c⋆`.
The boundedness hypothesis is what the upper certificate would supply; it is
not proved here. -/
theorem a0_lt_cstar (hbdd : BddAbove (ratio '' Ioo 0 1)) :
    (68743 : ℝ) / 50000 < cstar :=
  lt_cstar_of_ratio v0_pos v0_lt_one hbdd a0_lt_ratio_v0

end QipmFormal.ScalarCert
