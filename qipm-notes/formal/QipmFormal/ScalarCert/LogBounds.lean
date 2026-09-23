import QipmFormal.ScalarCert.Series

/-!
# Rational bounds for the logarithms of the upper certificate

`appendix-scalar-certificate.tex` bounds `log(69/50)`, `log(19/50)` and
`log 2` by truncations of the positive series
`log((1+q)/(1-q)) = 2 ∑ q^{2j+1}/(2j+1)`, with the geometric tail estimate
`∑_{j≥n} q^{2j+1}/(2j+1) ≤ q^{2n+1}/((2n+1)(1-q²))`.

The constants reproduced here are the appendix's own:
`2(s₀ + s₀³/3) = 1628072/5055477` with `s₀ = 19/119`, and
`2(r₀ + r₀³/3 + r₀⁵/(5(1-r₀²))) = 9064603453/9362506500` with `r₀ = 31/69`.
-/

namespace QipmFormal.ScalarCert

open Real Finset

/-- The `k`-th term of the `artanh` series. -/
noncomputable def aterm (q : ℝ) (k : ℕ) : ℝ := (1 / (2 * (k : ℝ) + 1)) * q ^ (2 * k + 1)

lemma hasSum_aterm {q : ℝ} (hq : |q| < 1) : HasSum (aterm q) (artanh q) := hasSum_artanh hq

lemma aterm_nonneg {q : ℝ} (hq : 0 ≤ q) (k : ℕ) : 0 ≤ aterm q k := by
  have h : (0:ℝ) < 2 * (k : ℝ) + 1 := by positivity
  exact mul_nonneg (by positivity) (pow_nonneg hq _)

/-- Partial sums underestimate `artanh`. -/
theorem partial_le_artanh {q : ℝ} (hq0 : 0 ≤ q) (hq : |q| < 1) (n : ℕ) :
    ∑ k ∈ range n, aterm q k ≤ artanh q :=
  sum_le_hasSum _ (fun i _ => aterm_nonneg hq0 i) (hasSum_aterm hq)

/-- Tail estimate for `artanh`. -/
theorem artanh_le_partial_add_tail {q : ℝ} (hq0 : 0 < q) (hq1 : q < 1) (n : ℕ) :
    artanh q ≤ (∑ k ∈ range n, aterm q k)
        + q ^ (2 * n + 1) / ((2 * (n : ℝ) + 1) * (1 - q ^ 2)) := by
  have habs : |q| < 1 := by rwa [abs_of_pos hq0]
  have hsum := (hasSum_aterm habs).summable
  have hq2 : q ^ 2 < 1 := by nlinarith
  have hq2n : (0:ℝ) ≤ q ^ 2 := sq_nonneg q
  have heq : artanh q = (∑ k ∈ range n, aterm q k) + ∑' i, aterm q (i + n) := by
    rw [hsum.sum_add_tsum_nat_add n]; exact ((hasSum_aterm habs).tsum_eq).symm
  have htailsum : Summable (fun i : ℕ => aterm q (i + n)) :=
    (summable_nat_add_iff n).mpr hsum
  have hgeo : Summable (fun i : ℕ => q ^ (2 * n + 1) / (2 * (n : ℝ) + 1) * (q ^ 2) ^ i) :=
    (summable_geometric_of_lt_one hq2n hq2).mul_left _
  have hcmp : ∀ i : ℕ, aterm q (i + n)
      ≤ q ^ (2 * n + 1) / (2 * (n : ℝ) + 1) * (q ^ 2) ^ i := by
    intro i
    have hdenpos : (0:ℝ) < 2 * (n : ℝ) + 1 := by positivity
    have hden' : 2 * (n : ℝ) + 1 ≤ 2 * ((i + n : ℕ) : ℝ) + 1 := by
      push_cast; linarith [Nat.cast_nonneg (α := ℝ) i]
    have hcoef : (1 : ℝ) / (2 * ((i + n : ℕ) : ℝ) + 1) ≤ 1 / (2 * (n : ℝ) + 1) := by
      gcongr
    have hpow : q ^ (2 * (i + n) + 1) = q ^ (2 * n + 1) * (q ^ 2) ^ i := by
      rw [← pow_mul, ← pow_add]; ring_nf
    have hp : (0:ℝ) ≤ q ^ (2 * n + 1) * (q ^ 2) ^ i := by positivity
    rw [aterm, hpow]
    calc (1 : ℝ) / (2 * ((i + n : ℕ) : ℝ) + 1) * (q ^ (2 * n + 1) * (q ^ 2) ^ i)
        ≤ 1 / (2 * (n : ℝ) + 1) * (q ^ (2 * n + 1) * (q ^ 2) ^ i) :=
          mul_le_mul_of_nonneg_right hcoef hp
      _ = q ^ (2 * n + 1) / (2 * (n : ℝ) + 1) * (q ^ 2) ^ i := by ring
  have htail : ∑' i, aterm q (i + n)
      ≤ q ^ (2 * n + 1) / ((2 * (n : ℝ) + 1) * (1 - q ^ 2)) := by
    have hle := Summable.tsum_le_tsum hcmp htailsum hgeo
    rw [tsum_mul_left, tsum_geometric_of_lt_one hq2n hq2] at hle
    have hrw : q ^ (2 * n + 1) / (2 * (n : ℝ) + 1) * (1 - q ^ 2)⁻¹
             = q ^ (2 * n + 1) / ((2 * (n : ℝ) + 1) * (1 - q ^ 2)) := by field_simp
    rwa [hrw] at hle
  rw [heq]; linarith [htail]

/-- `log((1+q)/(1-q)) = 2 artanh q`. -/
lemma log_eq_two_artanh {q : ℝ} (hq : |q| < 1) :
    Real.log ((1 + q) / (1 - q)) = 2 * artanh q := by
  obtain ⟨h1, h2⟩ := abs_lt.mp hq
  rw [artanh_eq_half_log ⟨h1.le, h2.le⟩]
  ring

/-! ### The three numeric bounds of the appendix -/

/-- `log (69/50) ≥ 1628072/5055477`, from `s₀ = 19/119` and two terms.
This is the appendix's displayed constant `2(s₀ + s₀³/3)`.

Recorded because it reproduces the appendix's own constant.  It is NOT used by
the certificate, which runs at `a = 3449/2500` rather than `a = 69/50`. -/
theorem log_69_50_ge : (1628072 : ℝ) / 5055477 ≤ Real.log (69 / 50) := by
  have hq : |(19:ℝ)/119| < 1 := by rw [abs_of_pos] <;> norm_num
  have hrw : ((1:ℝ) + 19/119) / (1 - 19/119) = 69 / 50 := by norm_num
  have h := partial_le_artanh (q := (19:ℝ)/119) (by norm_num) hq 2
  rw [← hrw, log_eq_two_artanh hq]
  have hsum : ∑ k ∈ range 2, aterm ((19:ℝ)/119) k = 814036 / 5055477 := by
    norm_num [aterm, Finset.sum_range_succ]
  rw [hsum] at h
  linarith

/-- `log (50/19) ≤ 9064603453/9362506500`, from `r₀ = 31/69`, two terms and the
tail.  This is the appendix's displayed constant.

As with `log_69_50_ge`, recorded for fidelity to the appendix but not used by
the certificate. -/
theorem log_50_19_le : Real.log (50 / 19) ≤ (9064603453 : ℝ) / 9362506500 := by
  have hq : |(31:ℝ)/69| < 1 := by rw [abs_of_pos] <;> norm_num
  have hrw : ((1:ℝ) + 31/69) / (1 - 31/69) = 50 / 19 := by norm_num
  have h := artanh_le_partial_add_tail (q := (31:ℝ)/69) (by norm_num) (by norm_num) 2
  rw [← hrw, log_eq_two_artanh hq]
  have hsum : ∑ k ∈ range 2, aterm ((31:ℝ)/69) k = 472564 / 985527 := by
    norm_num [aterm, Finset.sum_range_succ]
  rw [hsum] at h
  have htail : ((31:ℝ)/69) ^ (2 * 2 + 1) / ((2 * ((2:ℕ) : ℝ) + 1) * (1 - ((31:ℝ)/69) ^ 2))
      = 28629151 / 6241671000 := by push_cast; norm_num
  rw [htail] at h
  linarith

/-- `log 2 ≤ 1123/1620`, from `q = 1/3`, two terms and the tail. -/
theorem log_two_le : Real.log 2 ≤ (1123 : ℝ) / 1620 := by
  have hq : |(1:ℝ)/3| < 1 := by rw [abs_of_pos] <;> norm_num
  have hrw : ((1:ℝ) + 1/3) / (1 - 1/3) = 2 := by norm_num
  have h := artanh_le_partial_add_tail (q := (1:ℝ)/3) (by norm_num) (by norm_num) 2
  rw [← hrw, log_eq_two_artanh hq]
  have hsum : ∑ k ∈ range 2, aterm ((1:ℝ)/3) k = 28 / 81 := by
    norm_num [aterm, Finset.sum_range_succ]
  rw [hsum] at h
  have htail : ((1:ℝ)/3) ^ (2 * 2 + 1) / ((2 * ((2:ℕ) : ℝ) + 1) * (1 - ((1:ℝ)/3) ^ 2))
      = 1 / 1080 := by push_cast; norm_num
  rw [htail] at h
  linarith

/-! ### Bounds for the strict upper certificate at `a = 3449/2500`

`(1+q)/(1-q) = 3449/2500` for `q = 949/5949`, and `= 2500/949` for
`q = 1551/3449`; seven terms suffice for both. -/

/-- `log (3449/2500) ≥ 0.3217936`. -/
theorem log_3449_2500_ge : (3217936 : ℝ) / 10 ^ 7 ≤ Real.log (3449 / 2500) := by
  have hq : |(949:ℝ)/5949| < 1 := by rw [abs_of_pos] <;> norm_num
  have hrw : ((1:ℝ) + 949/5949) / (1 - 949/5949) = 3449 / 2500 := by norm_num
  have h := partial_le_artanh (q := (949:ℝ)/5949) (by norm_num) hq 7
  rw [← hrw, log_eq_two_artanh hq]
  have hs : (3217936 : ℝ) / 10 ^ 7 / 2 ≤ ∑ k ∈ range 7, aterm ((949:ℝ)/5949) k := by
    norm_num [aterm, Finset.sum_range_succ]
  linarith

/-- `log (2500/949) ≤ 0.9686373`. -/
theorem log_2500_949_le : Real.log (2500 / 949) ≤ (9686373 : ℝ) / 10 ^ 7 := by
  have hq : |(1551:ℝ)/3449| < 1 := by rw [abs_of_pos] <;> norm_num
  have hrw : ((1:ℝ) + 1551/3449) / (1 - 1551/3449) = 2500 / 949 := by norm_num
  have h := artanh_le_partial_add_tail (q := (1551:ℝ)/3449) (by norm_num) (by norm_num) 7
  rw [← hrw, log_eq_two_artanh hq]
  have hcast : ((7:ℕ) : ℝ) = 7 := by norm_num
  rw [hcast] at h
  have hs : (∑ k ∈ range 7, aterm ((1551:ℝ)/3449) k)
      + ((1551:ℝ)/3449) ^ (2 * 7 + 1) / ((2 * (7:ℝ) + 1) * (1 - ((1551:ℝ)/3449) ^ 2))
      ≤ (9686373 : ℝ) / 10 ^ 7 / 2 := by
    norm_num [aterm, Finset.sum_range_succ]
  linarith

end QipmFormal.ScalarCert
