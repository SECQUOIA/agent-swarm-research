import QipmFormal.ScalarCert.Final

/-!
# Every scalar-dilation maximizer lies in a certified interval

This file formalises the appendix subsection "Every scalar-dilation maximizer
lies in a certified interval", i.e. `eq:cstar-maximizer-location`.

With `a₀ = 68743/50000`, `k = 107/200`, `p = 571/250` and `q = 773/250`:

* four rational logarithm bounds (`log_a0_ge`, `log_two_le'`,
  `log_571_250_le`, `log_773_250_le`) come from the `artanh` series of
  `LogBounds.lean`;
* the tangent-line bound `log E ≤ log c + E/c - 1` makes `h_{a₀,1}` positive
  on `(0,2]`, and `h_{a₀,k}` positive on `(0,p]` and on `[q,∞)`;
* `key_ineq` turns `a₀ < ratio v` into `h_{a₀,k}(E v) < 0`, so `E v` must lie
  strictly between `p` and `q` (the case `E v ≤ 2` is excluded with `k = 1`);
* `E` is strictly increasing, and the scaled-integer evaluator certifies
  `E (4611/5000) < p` and `E (9701/10000) > q`, which localises `v`.
-/

namespace QipmFormal.ScalarCert

open Real Set Finset

set_option exponentiation.threshold 1000000

/-! ### Four rational logarithm bounds

Each uses `q = (z-1)/(z+1)` in `log ((1+q)/(1-q)) = 2 artanh q`.  The true
values are

```
log(68743/50000) = 0.31835190775289348500…
log 2            = 0.69314718055994530942…
log(571/250)     = 0.82592829179376378351…
log(773/250)     = 1.12881813072517552840…
```

so every bound below is on the correct side with margin at least `2.8e-9`. -/

/-- `log (68743/50000) ≥ 0.3183519`, from `q = 18743/118743` and five terms. -/
theorem log_a0_ge : (3183519 : ℝ) / 10 ^ 7 ≤ Real.log (68743 / 50000) := by
  have hq : |(18743:ℝ)/118743| < 1 := by rw [abs_of_pos] <;> norm_num
  have hrw : ((1:ℝ) + 18743/118743) / (1 - 18743/118743) = 68743 / 50000 := by norm_num
  have h := partial_le_artanh (q := (18743:ℝ)/118743) (by norm_num) hq 5
  rw [← hrw, log_eq_two_artanh hq]
  have hs : (3183519 : ℝ) / 10 ^ 7 / 2 ≤ ∑ k ∈ range 5, aterm ((18743:ℝ)/118743) k := by
    norm_num [aterm, Finset.sum_range_succ]
  linarith

/-- `log 2 ≤ 0.6931472`, from `q = 1/3`, six terms and the tail. -/
theorem log_two_le' : Real.log 2 ≤ (6931472 : ℝ) / 10 ^ 7 := by
  have hq : |(1:ℝ)/3| < 1 := by rw [abs_of_pos] <;> norm_num
  have hrw : ((1:ℝ) + 1/3) / (1 - 1/3) = 2 := by norm_num
  have h := artanh_le_partial_add_tail (q := (1:ℝ)/3) (by norm_num) (by norm_num) 6
  rw [← hrw, log_eq_two_artanh hq]
  have hcast : ((6:ℕ) : ℝ) = 6 := by norm_num
  rw [hcast] at h
  have hs : (∑ k ∈ range 6, aterm ((1:ℝ)/3) k)
      + ((1:ℝ)/3) ^ (2 * 6 + 1) / ((2 * (6:ℝ) + 1) * (1 - ((1:ℝ)/3) ^ 2))
      ≤ (6931472 : ℝ) / 10 ^ 7 / 2 := by
    norm_num [aterm, Finset.sum_range_succ]
  linarith

/-- `log (571/250) ≤ 0.8259283`, from `q = 321/821`, seven terms and the tail. -/
theorem log_571_250_le : Real.log (571 / 250) ≤ (8259283 : ℝ) / 10 ^ 7 := by
  have hq : |(321:ℝ)/821| < 1 := by rw [abs_of_pos] <;> norm_num
  have hrw : ((1:ℝ) + 321/821) / (1 - 321/821) = 571 / 250 := by norm_num
  have h := artanh_le_partial_add_tail (q := (321:ℝ)/821) (by norm_num) (by norm_num) 7
  rw [← hrw, log_eq_two_artanh hq]
  have hcast : ((7:ℕ) : ℝ) = 7 := by norm_num
  rw [hcast] at h
  have hs : (∑ k ∈ range 7, aterm ((321:ℝ)/821) k)
      + ((321:ℝ)/821) ^ (2 * 7 + 1) / ((2 * (7:ℝ) + 1) * (1 - ((321:ℝ)/821) ^ 2))
      ≤ (8259283 : ℝ) / 10 ^ 7 / 2 := by
    norm_num [aterm, Finset.sum_range_succ]
  linarith

/-- `log (773/250) ≤ 1.1288182`, from `q = 523/1023`, eight terms and the tail. -/
theorem log_773_250_le : Real.log (773 / 250) ≤ (11288182 : ℝ) / 10 ^ 7 := by
  have hq : |(523:ℝ)/1023| < 1 := by rw [abs_of_pos] <;> norm_num
  have hrw : ((1:ℝ) + 523/1023) / (1 - 523/1023) = 773 / 250 := by norm_num
  have h := artanh_le_partial_add_tail (q := (523:ℝ)/1023) (by norm_num) (by norm_num) 8
  rw [← hrw, log_eq_two_artanh hq]
  have hcast : ((8:ℕ) : ℝ) = 8 := by norm_num
  rw [hcast] at h
  have hs : (∑ k ∈ range 8, aterm ((523:ℝ)/1023) k)
      + ((523:ℝ)/1023) ^ (2 * 8 + 1) / ((2 * (8:ℝ) + 1) * (1 - ((523:ℝ)/1023) ^ 2))
      ≤ (11288182 : ℝ) / 10 ^ 7 / 2 := by
    norm_num [aterm, Finset.sum_range_succ]
  linarith

/-! ### Positivity of `h` outside the window `(571/250, 773/250)`

All three bounds use only the tangent-line bound `log E ≤ log c + E/c - 1`:
after it the lower bound for `hgen` is affine in `E`, so it suffices to check
its value at the endpoint towards which it decreases. -/

/-- `h_{a₀,1} > 0` on `(0,2]`.  The tangent is taken at `c = 2`; the resulting
affine lower bound has `E`-coefficient `(a₀-1) - 1/2 = -0.12514 < 0` and value
`647/10⁷ > 0` at `E = 2`. -/
theorem hgen_one_pos_a0 {E : ℝ} (hE0 : 0 < E) (hE2 : E ≤ 2) :
    0 < hgen (68743 / 50000) 1 E := by
  have htan := log_le_tangent hE0 (show (0:ℝ) < 2 by norm_num)
  have h1 := log_a0_ge
  have h2 := log_two_le'
  rw [hgen]
  nlinarith [htan, h1, h2, hE2]

/-- `h_{a₀,107/200} > 0` on `(0,571/250]`.  Tangent at `c = 571/250`;
`E`-coefficient `(a₀-1) - 250/571 ≈ -0.0630 < 0` and value
`40213/(2·10⁹) > 0` at `E = 571/250`. -/
theorem hgen_k_pos_left {E : ℝ} (hE0 : 0 < E) (hEp : E ≤ 571 / 250) :
    0 < hgen (68743 / 50000) (107 / 200) E := by
  have htan := log_le_tangent hE0 (show (0:ℝ) < 571 / 250 by norm_num)
  have h1 := log_a0_ge
  have h2 := log_571_250_le
  rw [hgen]
  nlinarith [htan, h1, h2, hEp]

/-- `h_{a₀,107/200} > 0` on `[773/250, ∞)`.  Tangent at `c = 773/250`;
`E`-coefficient `(a₀-1) - 250/773 ≈ +0.0514 > 0` and value
`34173/(2·10⁹) > 0` at `E = 773/250`. -/
theorem hgen_k_pos_right {E : ℝ} (hEq : 773 / 250 ≤ E) :
    0 < hgen (68743 / 50000) (107 / 200) E := by
  have hE0 : (0:ℝ) < E := by linarith
  have htan := log_le_tangent hE0 (show (0:ℝ) < 773 / 250 by norm_num)
  have h1 := log_a0_ge
  have h2 := log_773_250_le
  rw [hgen]
  nlinarith [htan, h1, h2, hEq]

/-! ### `a₀ < ratio v` forces `h_{a₀,k}(E v) < 0` -/

/-- If the dilation ratio at `v` exceeds `a₀`, then `h_{a₀,k}(E v) < 0` for any
admissible exponent `k`.  This is `key_ineq` combined with monotonicity of
`log` and `0 < E v - k`. -/
theorem hgen_neg_of_a0_lt {v k a : ℝ} (hv0 : 0 < v) (hv1 : v < 1)
    (h : (68743 : ℝ) / 50000 < ratio v) (hk0 : 0 ≤ k) (hkE : k < E v)
    (ha : 0 ≤ a) (hav : a < v) (hg : StrictMonoOn (g k) (Ioo a 1)) :
    hgen (68743 / 50000) k (E v) < 0 := by
  have hlog : Real.log (68743 / 50000) ≤ Real.log (ratio v) :=
    Real.log_le_log (by norm_num) h.le
  have hklog : k * Real.log (68743 / 50000) ≤ k * Real.log (ratio v) :=
    mul_le_mul_of_nonneg_left hlog hk0
  have hEk : (0:ℝ) ≤ E v - k := by linarith
  have hmul : ((68743:ℝ) / 50000 - 1) * (E v - k) ≤ (ratio v - 1) * (E v - k) :=
    mul_le_mul_of_nonneg_right (by linarith) hEk
  have hkey := key_ineq (k := k) (a := a) hv0 hv1 ha hav hg
  rw [hgen]
  linarith

/-- A dilation ratio above `a₀` forces `E v > 2`; this is the `k = 1` case. -/
theorem two_lt_E_of_a0_lt {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1)
    (h : (68743 : ℝ) / 50000 < ratio v) : 2 < E v := by
  by_contra hcon
  rw [not_lt] at hcon
  have hE1 : 1 < E v := one_lt_E hv0 hv1
  have hneg := hgen_neg_of_a0_lt (k := 1) (a := 0) hv0 hv1 h zero_le_one hE1 le_rfl hv0
    g_one_strictMonoOn
  linarith [hgen_one_pos_a0 (lt_trans one_pos hE1) hcon]

/-- The `k = 107/200` case, valid once `E v > 2`. -/
theorem hgen_k_neg_of_a0_lt {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1)
    (h : (68743 : ℝ) / 50000 < ratio v) :
    hgen (68743 / 50000) (107 / 200) (E v) < 0 := by
  have hE := two_lt_E_of_a0_lt hv0 hv1 h
  have hv2 := lt_of_two_lt_E hv0 hv1 hE
  have hgK : StrictMonoOn (g (107 / 200)) (Ioo v2 1) := by
    refine g_strictMonoOn_of_K_lt v2_pos.le le_rfl ?_
    intro w hw1 hw2
    exact lt_trans (K_strictAntiOn (left_mem_Ico.mpr v2_lt_one) ⟨hw1.le, hw2⟩ hw1) K_v2_lt
  exact hgen_neg_of_a0_lt hv0 hv1 h (by norm_num) (by linarith) v2_pos.le hv2 hgK

/-- **The elasticity window.**  A dilation ratio above `a₀` is possible only for
`571/250 < E v < 773/250`. -/
theorem E_mem_window {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1)
    (h : (68743 : ℝ) / 50000 < ratio v) : 571 / 250 < E v ∧ E v < 773 / 250 := by
  have hneg := hgen_k_neg_of_a0_lt hv0 hv1 h
  have hE0 : (0:ℝ) < E v := lt_trans one_pos (one_lt_E hv0 hv1)
  constructor
  · by_contra hcon
    rw [not_lt] at hcon
    linarith [hgen_k_pos_left hE0 hcon]
  · by_contra hcon
    rw [not_lt] at hcon
    linarith [hgen_k_pos_right hcon]

/-! ### Certified enclosures of `Y` at the two endpoints

Scale `10³⁰`; 201 series terms at `4611/5000` and 401 at `9701/10000`. -/

set_option maxRecDepth 4000000 in
theorem accHi_4611 : accHi (4611 * 4611) (5000 * 5000) (10 ^ 30) 0 200
    = 2283134394146982789799779649384 := by decide

set_option maxRecDepth 4000000 in
theorem accLo_9701 : accLo (9701 * 9701) (10000 * 10000) (10 ^ 30) 0 400
    = 3092080373333924096876196971547 := by decide

set_option maxRecDepth 4000000 in
theorem pow_4611_nat : 4611 ^ 403 * 10 ^ 10 ≤ 5000 ^ 403 := by decide

lemma cast_4611 : (4611 : ℝ) / 5000 = ((4611 : ℕ) : ℝ) / ((5000 : ℕ) : ℝ) := by norm_num
lemma cast_9701 : (9701 : ℝ) / 10000 = ((9701 : ℕ) : ℝ) / ((10000 : ℕ) : ℝ) := by norm_num

lemma pow_4611 : ((4611:ℝ) / 5000) ^ 403 ≤ 1 / 10 ^ 10 := by
  rw [div_pow, div_le_div_iff₀ (by positivity) (by positivity), one_mul]
  exact_mod_cast pow_4611_nat

lemma tail_4611 :
    2 * ((4611:ℝ) / 5000) ^ (2 * (200 + 1) + 1)
        / ((2 * ((200 : ℕ) + 1 : ℝ) + 1) * (1 - ((4611:ℝ) / 5000) ^ 2))
      ≤ 1 / 10 ^ 11 := by
  have hden : (2 * ((200 : ℕ) + 1 : ℝ) + 1) * (1 - ((4611:ℝ) / 5000) ^ 2)
      = 1506687637 / 25000000 := by push_cast; norm_num
  have hnn : (0:ℝ) ≤ ((4611:ℝ) / 5000) ^ 403 := by positivity
  have hp := pow_4611
  rw [show 2 * (200 + 1) + 1 = 403 from rfl, hden, div_le_iff₀ (by norm_num)]
  linarith

/-- A rational upper bound for `Y (4611/5000)`, from 201 terms plus the tail. -/
theorem Y_4611_le :
    Y ((4611:ℝ) / 5000)
      ≤ (4611 / 5000) * (2283134394146982789799779649384 / 10 ^ 30) + 1 / 10 ^ 11 := by
  have h := Y_le_accHi (a := 4611) (b := 5000) (s := 10 ^ 30) (z := (4611:ℝ) / 5000)
    cast_4611 (by norm_num) (by norm_num) (by norm_num) 200
  rw [accHi_4611] at h
  have ht := tail_4611
  push_cast at h ht
  linarith

/-- `Y (9701/10000) ≥ 2.9996271701712`; no tail is needed for a lower bound. -/
theorem Y_9701_ge :
    (9701 / 10000) * (3092080373333924096876196971547 / 10 ^ 30)
      ≤ Y ((9701:ℝ) / 10000) := by
  have h := Y_ge_accLo (a := 9701) (b := 10000) (s := 10 ^ 30) (z := (9701:ℝ) / 10000)
    cast_9701 (by norm_num) (by norm_num) (by norm_num) 400
  rw [accLo_9701] at h
  push_cast at h
  linarith

/-- `E (4611/5000) < 571/250`, because `Y (4611/5000) < (571/250)·(4611/5000)`. -/
theorem E_4611_lt : E ((4611:ℝ) / 5000) < 571 / 250 := by
  have h := Y_4611_le
  rw [E, div_lt_iff₀ (by norm_num : (0:ℝ) < 4611 / 5000)]
  have hnum : (4611 / 5000 : ℝ) * (2283134394146982789799779649384 / 10 ^ 30) + 1 / 10 ^ 11
      < 571 / 250 * (4611 / 5000) := by norm_num
  linarith

/-- `E (9701/10000) > 773/250`, because `Y (9701/10000) > (773/250)·(9701/10000)`. -/
theorem E_9701_gt : (773:ℝ) / 250 < E ((9701:ℝ) / 10000) := by
  have h := Y_9701_ge
  rw [E, lt_div_iff₀ (by norm_num : (0:ℝ) < 9701 / 10000)]
  have hnum : (773 : ℝ) / 250 * (9701 / 10000)
      < (9701 / 10000 : ℝ) * (3092080373333924096876196971547 / 10 ^ 30) := by norm_num
  linarith

/-! ### The localization -/

/-- **The certified interval of `eq:cstar-maximizer-location`.**
If the dilation ratio at `v ∈ (0,1)` exceeds `a₀ = 68743/50000`, then
`4611/5000 < v < 9701/10000`.

Any point attaining `cstar` satisfies the threshold hypothesis by
`cstar_bounds`.  Existence of such a point is proved separately in
`Attainment.lean`. -/
theorem maximizer_localization {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1)
    (h : (68743 : ℝ) / 50000 < ratio v) : 4611 / 5000 < v ∧ v < 9701 / 10000 := by
  obtain ⟨hp, hq⟩ := E_mem_window hv0 hv1 h
  have hmv : v ∈ Ioo (0:ℝ) 1 := ⟨hv0, hv1⟩
  have hm1 : ((4611:ℝ) / 5000) ∈ Ioo (0:ℝ) 1 := ⟨by norm_num, by norm_num⟩
  have hm2 : ((9701:ℝ) / 10000) ∈ Ioo (0:ℝ) 1 := ⟨by norm_num, by norm_num⟩
  refine ⟨?_, ?_⟩
  · refine (E_strictMonoOn.lt_iff_lt hm1 hmv).mp ?_
    linarith [E_4611_lt]
  · refine (E_strictMonoOn.lt_iff_lt hmv hm2).mp ?_
    linarith [E_9701_gt]

end QipmFormal.ScalarCert
