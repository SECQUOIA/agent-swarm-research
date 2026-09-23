import Mathlib

/-! # A good aggregate cannot exclude two well separated witness parameters -/

namespace InfiniteAggregation

/-- The exclusion interval of a perturbed good aggregate has a uniformly small
squared diameter on the parameter interval `[1,2]`. -/
theorem positive_perturbed_slacks_gap_sq {a b c τ σ η : ℝ}
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c) (hcone : c ^ 2 ≤ 4 * a * b)
    (hτ : τ ∈ Set.Icc (1 : ℝ) 2) (hσ : σ ∈ Set.Icc (1 : ℝ) 2)
    (hη : 0 ≤ η)
    (hτslack : 0 < (1 / 10) * (-a / τ - b * τ + c) + c * η)
    (hσslack : 0 < (1 / 10) * (-a / σ - b * σ + c) + c * η) :
    (τ - σ) ^ 2 < 16 * ((1 + 10 * η) ^ 2 - 1) := by
  have hτpos : 0 < τ := lt_of_lt_of_le (by norm_num) hτ.1
  have hσpos : 0 < σ := lt_of_lt_of_le (by norm_num) hσ.1
  have hcpos : 0 < c := by
    by_contra hn
    have hz : c = 0 := le_antisymm (le_of_not_gt hn) hc
    subst c
    have : 0 ≤ a / τ := div_nonneg ha hτpos.le
    have : 0 ≤ b * τ := mul_nonneg hb hτpos.le
    rw [neg_div] at hτslack
    nlinarith [hτslack]
  let k := 1 + 10 * η
  have hk : 1 ≤ k := by dsimp [k]; linarith
  have ht : a + b * τ ^ 2 < c * k * τ := by
    have h := mul_pos hτslack hτpos
    field_simp at h
    dsimp [k]
    nlinarith [h]
  have hs : a + b * σ ^ 2 < c * k * σ := by
    have h := mul_pos hσslack hσpos
    field_simp at h
    dsimp [k]
    nlinarith [h]
  have hprod : (a + b * τ ^ 2) * (a + b * σ ^ 2) <
      (c * k * τ) * (c * k * σ) :=
    lt_of_le_of_lt (mul_le_mul_of_nonneg_left hs.le (by positivity))
      (mul_lt_mul_of_pos_right ht (by positivity))
  have hbase : a * b * (τ + σ) ^ 2 ≤
      (a + b * τ ^ 2) * (a + b * σ ^ 2) := by
    nlinarith only [sq_nonneg (a - b * τ * σ)]
  have hscaled := mul_le_mul_of_nonneg_right hcone (sq_nonneg (τ + σ))
  have hmain : c ^ 2 * (τ + σ) ^ 2 < 4 * c ^ 2 * k ^ 2 * (τ * σ) := by
    nlinarith only [hscaled, hbase, hprod]
  have hcancel : (τ + σ) ^ 2 < 4 * k ^ 2 * (τ * σ) := by
    have hcp : 0 < c ^ 2 := sq_pos_of_pos hcpos
    apply (mul_lt_mul_iff_right₀ hcp).mp
    nlinarith only [hmain]
  have hp : τ * σ ≤ 4 := by nlinarith [hτ.1, hτ.2, hσ.1, hσ.2]
  have hk2 : 0 ≤ k ^ 2 - 1 := by nlinarith
  have hbound := mul_le_mul_of_nonneg_right hp hk2
  dsimp [k] at *
  nlinarith only [hcancel, hbound]

/-- With perturbation `1/(400 N²)`, one good aggregate can exclude at most one
member of a witness grid of spacing `1/N`. -/
theorem positive_perturbed_slacks_gap {a b c τ σ N : ℝ}
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c) (hcone : c ^ 2 ≤ 4 * a * b)
    (hτ : τ ∈ Set.Icc (1 : ℝ) 2) (hσ : σ ∈ Set.Icc (1 : ℝ) 2)
    (hN : 1 ≤ N)
    (hτslack : 0 < (1 / 10) * (-a / τ - b * τ + c) + c / (400 * N ^ 2))
    (hσslack : 0 < (1 / 10) * (-a / σ - b * σ + c) + c / (400 * N ^ 2)) :
    |τ - σ| < 1 / N := by
  have hNpos : 0 < N := lt_of_lt_of_le (by norm_num) hN
  have hη : 0 ≤ 1 / (400 * N ^ 2) := by positivity
  have hg := positive_perturbed_slacks_gap_sq ha hb hc hcone hτ hσ hη
    (by simpa [div_eq_mul_inv] using hτslack)
    (by simpa [div_eq_mul_inv] using hσslack)
  have hi : 0 < 1 / N := by positivity
  have hi1 : 1 / N ≤ 1 := (div_le_one hNpos).mpr hN
  have hi2 : (1 / N) ^ 2 ≤ 1 := by nlinarith
  have hi4 : (1 / N) ^ 4 ≤ (1 / N) ^ 2 := by
    nlinarith [mul_nonneg (sq_nonneg (1 / N)) (sub_nonneg.mpr hi2)]
  have hid : 1 / (400 * N ^ 2) = (1 / N) ^ 2 / 400 := by field_simp
  rw [hid] at hg
  have hgap : (τ - σ) ^ 2 < (1 / N) ^ 2 := by nlinarith
  exact (sq_lt_sq₀ (abs_nonneg _) hi.le).mp (by simpa using hgap)

end InfiniteAggregation
