import QipmFormal.ScalarCert.Series

/-!
# Partial sums and the tail estimate

For `0 < z < 1`, with `S n = ∑_{k<n} (2 - 2^{-k}) z^{2k+1}/(2k+1)`,

  `S n ≤ Y z ≤ S n + 2 z^{2n+1} / ((2n+1)(1-z²))`,

the estimate `eq:Y-rational-series` of `appendix-scalar-certificate.tex`
(there indexed by `N = n-1`).
-/

namespace QipmFormal.ScalarCert

open Real Finset

/-- The `k`-th term of the `Y` series. -/
noncomputable def term (z : ℝ) (k : ℕ) : ℝ :=
  (2 - (1/2 : ℝ) ^ k) / (2 * (k : ℝ) + 1) * z ^ (2 * k + 1)

lemma half_pow_le_one (k : ℕ) : ((1:ℝ)/2) ^ k ≤ 1 :=
  pow_le_one₀ (by norm_num) (by norm_num)

lemma half_pow_nonneg (k : ℕ) : (0:ℝ) ≤ ((1:ℝ)/2) ^ k := by positivity

lemma coef_nonneg (k : ℕ) : (0:ℝ) ≤ 2 - (1/2 : ℝ) ^ k := by
  linarith [half_pow_le_one k]

lemma term_nonneg {z : ℝ} (hz : 0 ≤ z) (k : ℕ) : 0 ≤ term z k := by
  have h2 : (0:ℝ) < 2 * (k : ℝ) + 1 := by positivity
  exact mul_nonneg (div_nonneg (coef_nonneg k) h2.le) (pow_nonneg hz _)

lemma summable_term {z : ℝ} (h : |z| < 1) : Summable (term z) :=
  (hasSum_Y h).summable

lemma hasSum_term {z : ℝ} (h : |z| < 1) : HasSum (term z) (Y z) := hasSum_Y h

/-- Partial sums underestimate `Y`. -/
theorem partial_le_Y {z : ℝ} (hz : 0 ≤ z) (h : |z| < 1) (n : ℕ) :
    ∑ k ∈ range n, term z k ≤ Y z :=
  sum_le_hasSum _ (fun i _ => term_nonneg hz i) (hasSum_term h)

/-- The tail estimate. -/
theorem Y_le_partial_add_tail {z : ℝ} (hz : 0 < z) (h1 : z < 1) (n : ℕ) :
    Y z ≤ (∑ k ∈ range n, term z k)
        + 2 * z ^ (2 * n + 1) / ((2 * (n:ℝ) + 1) * (1 - z ^ 2)) := by
  have habs : |z| < 1 := by rwa [abs_of_pos hz]
  have hsum := summable_term habs
  have hz2 : z ^ 2 < 1 := by nlinarith
  have hz2n : (0:ℝ) ≤ z ^ 2 := sq_nonneg z
  have hYeq : Y z = (∑ k ∈ range n, term z k) + ∑' i, term z (i + n) := by
    rw [hsum.sum_add_tsum_nat_add n]; exact ((hasSum_term habs).tsum_eq).symm
  have htailsum : Summable (fun i : ℕ => term z (i + n)) :=
    (summable_nat_add_iff n).mpr hsum
  have hgeo : Summable (fun i : ℕ => 2 * z ^ (2 * n + 1) / (2 * (n:ℝ) + 1) * (z ^ 2) ^ i) :=
    (summable_geometric_of_lt_one hz2n hz2).mul_left _
  have hcmp : ∀ i : ℕ, term z (i + n)
      ≤ 2 * z ^ (2 * n + 1) / (2 * (n:ℝ) + 1) * (z ^ 2) ^ i := by
    intro i
    have hdenpos : (0:ℝ) < 2 * (n:ℝ) + 1 := by positivity
    have hden' : 2 * (n:ℝ) + 1 ≤ 2 * ((i + n : ℕ) : ℝ) + 1 := by
      push_cast; linarith [Nat.cast_nonneg (α := ℝ) i]
    have hnum : (2 - (1/2 : ℝ) ^ (i + n)) ≤ 2 := by
      linarith [half_pow_nonneg (i + n)]
    have hcoef : (2 - (1/2 : ℝ) ^ (i + n)) / (2 * ((i + n : ℕ) : ℝ) + 1)
        ≤ 2 / (2 * (n:ℝ) + 1) := by
      gcongr
    have hpow : z ^ (2 * (i + n) + 1) = z ^ (2 * n + 1) * (z ^ 2) ^ i := by
      rw [← pow_mul, ← pow_add]; ring_nf
    have hp : (0:ℝ) ≤ z ^ (2 * n + 1) * (z ^ 2) ^ i := by positivity
    rw [term, hpow]
    calc (2 - (1/2 : ℝ) ^ (i + n)) / (2 * ((i + n : ℕ) : ℝ) + 1)
              * (z ^ (2 * n + 1) * (z ^ 2) ^ i)
        ≤ 2 / (2 * (n:ℝ) + 1) * (z ^ (2 * n + 1) * (z ^ 2) ^ i) :=
          mul_le_mul_of_nonneg_right hcoef hp
      _ = 2 * z ^ (2 * n + 1) / (2 * (n:ℝ) + 1) * (z ^ 2) ^ i := by ring
  have htail : ∑' i, term z (i + n)
      ≤ 2 * z ^ (2 * n + 1) / ((2 * (n:ℝ) + 1) * (1 - z ^ 2)) := by
    have hle := Summable.tsum_le_tsum hcmp htailsum hgeo
    rw [tsum_mul_left, tsum_geometric_of_lt_one hz2n hz2] at hle
    have hrw : 2 * z ^ (2 * n + 1) / (2 * (n:ℝ) + 1) * (1 - z ^ 2)⁻¹
             = 2 * z ^ (2 * n + 1) / ((2 * (n:ℝ) + 1) * (1 - z ^ 2)) := by
      field_simp
    rwa [hrw] at hle
  rw [hYeq]
  linarith [htail]

end QipmFormal.ScalarCert
