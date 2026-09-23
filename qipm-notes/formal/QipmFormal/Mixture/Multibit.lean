import QipmFormal.Mixture.Residual

/-!
# Coefficients depending on several bits

The coefficientwise incidence bound used below follows from the manuscript's
bound on the union of incidences in each row. Bounds concern actual residuals.
-/
namespace QipmFormal.Mixture
noncomputable section
open scoped BigOperators
variable {I R C : Type*} [Fintype I] [Fintype R] [Fintype C]

/-- Squared multibit residual bound with the exact total incidence count. -/
theorem multibit_residual_sq [Nonempty I] (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (x : I → C → ℝ) (b : R → ℝ)
    (D : R → Finset C) (J : R → C → Finset I) (s d : ℕ) (B H : ℝ)
    (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hd : ∀ r j, (J r j).card ≤ d)
    (hD : ∀ r j, j ∉ D r → J r j = ∅)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hlocal : ∀ i r j, i ∉ J r j → A' i r j = A r j) :
    sqNorm (residual A (mix (uniformWeight I) x) b) ≤
      4 * B ^ 2 * H ^ 2 * d * s *
        (∑ r, ∑ j, ((J r j).card : ℝ)) / (Fintype.card I : ℝ) ^ 2 := by
  classical
  let f : R → C → I → ℝ := fun r j i => (A r j - A' i r j) * x i j
  have hf (r : R) (j : C) (i : I) : (f r j i) ^ 2 ≤ 4 * B ^ 2 * H ^ 2 := by
    have hdiff : |A r j - A' i r j| ≤ 2 * B :=
      (abs_sub _ _).trans (by linarith [hA r j, hA' i r j])
    have hh : |f r j i| ≤ 2 * B * H := by
      dsimp [f]
      rw [abs_mul]
      exact mul_le_mul hdiff (hx i j) (abs_nonneg _) (by positivity)
    have hh' := (sq_le_sq₀ (abs_nonneg (f r j i)) (by positivity : 0 ≤ 2 * B * H)).mpr hh
    simp only [sq_abs] at hh'
    nlinarith
  have heq (r : R) : residual A (mix (uniformWeight I) x) b r =
      (∑ j ∈ D r, ∑ i ∈ J r j, f r j i) / (Fintype.card I : ℝ) := by
    rw [residual_mix_eq A A' x b _ (uniformWeight_prob I) hfeas r]
    simp only [uniformWeight, ← Finset.mul_sum, div_eq_mul_inv]
    rw [mul_comm]
    congr 1
    rw [← Finset.sum_subset (Finset.subset_univ (D r))]
    · apply Finset.sum_congr rfl
      intro j _
      symm
      apply Finset.sum_subset (Finset.subset_univ (J r j))
      intro i _ hi
      dsimp [f]
      rw [hlocal i r j hi]
      ring
    · intro j _ hj
      apply Finset.sum_eq_zero
      intro i _
      rw [hlocal i r j (by rw [hD r j hj]; simp)]
      ring
  have hrow (r : R) : (∑ j ∈ D r, ∑ i ∈ J r j, f r j i) ^ 2 ≤
      (s : ℝ) * d * (4 * B ^ 2 * H ^ 2) * ∑ j, ((J r j).card : ℝ) := by
    have hinc : (∑ j ∈ D r, ((J r j).card : ℝ)) = ∑ j, ((J r j).card : ℝ) := by
      apply Finset.sum_subset (Finset.subset_univ (D r))
      intro j _ hj
      simp [hD r j hj]
    calc
      _ ≤ ((D r).card : ℝ) * ∑ j ∈ D r, (∑ i ∈ J r j, f r j i) ^ 2 :=
        sum_square_le_card_mul _ _
      _ ≤ (s : ℝ) * ∑ j ∈ D r, (∑ i ∈ J r j, f r j i) ^ 2 :=
        mul_le_mul_of_nonneg_right (Nat.cast_le.mpr (hs r))
          (Finset.sum_nonneg fun _ _ => sq_nonneg _)
      _ ≤ (s : ℝ) * ∑ j ∈ D r, (d : ℝ) * (4 * B ^ 2 * H ^ 2) * (J r j).card := by
        apply mul_le_mul_of_nonneg_left _ (Nat.cast_nonneg _)
        apply Finset.sum_le_sum
        intro j _
        calc
          _ ≤ ((J r j).card : ℝ) * ∑ i ∈ J r j, (f r j i) ^ 2 :=
            sum_square_le_card_mul _ _
          _ ≤ (d : ℝ) * ∑ i ∈ J r j, (f r j i) ^ 2 :=
            mul_le_mul_of_nonneg_right (Nat.cast_le.mpr (hd r j))
              (Finset.sum_nonneg fun _ _ => sq_nonneg _)
          _ ≤ (d : ℝ) * ∑ _i ∈ J r j, (4 * B ^ 2 * H ^ 2) :=
            mul_le_mul_of_nonneg_left (Finset.sum_le_sum fun i _ => hf r j i) (Nat.cast_nonneg _)
          _ = _ := by simp; ring
      _ = _ := by rw [← Finset.mul_sum, hinc]; ring
  unfold sqNorm
  calc
    _ = (∑ r, (∑ j ∈ D r, ∑ i ∈ J r j, f r j i) ^ 2) / (Fintype.card I : ℝ) ^ 2 := by
      simp only [heq, div_pow]
      rw [Finset.sum_div]
    _ ≤ (∑ r, (s : ℝ) * d * (4 * B ^ 2 * H ^ 2) * ∑ j, ((J r j).card : ℝ)) /
        (Fintype.card I : ℝ) ^ 2 :=
      div_le_div_of_nonneg_right (Finset.sum_le_sum fun r _ => hrow r) (sq_nonneg _)
    _ = _ := by rw [← Finset.mul_sum]; ring

/-- Euclidean multibit residual estimate. -/
theorem multibit_residual_bound [Nonempty I] (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (x : I → C → ℝ) (b : R → ℝ)
    (D : R → Finset C) (J : R → C → Finset I) (s d : ℕ) (B H : ℝ)
    (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hd : ∀ r j, (J r j).card ≤ d)
    (hD : ∀ r j, j ∉ D r → J r j = ∅)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hlocal : ∀ i r j, i ∉ J r j → A' i r j = A r j) :
    euclideanNorm (residual A (mix (uniformWeight I) x) b) ≤
      2 * B * H * Real.sqrt ((d : ℝ) * s * (∑ r, ∑ j, ((J r j).card : ℝ))) /
        (Fintype.card I : ℝ) := by
  have hn : 0 < (Fintype.card I : ℝ) := Nat.cast_pos.mpr Fintype.card_pos
  have ht : 0 ≤ (d : ℝ) * s * (∑ r, ∑ j, ((J r j).card : ℝ)) := by positivity
  apply (sq_le_sq₀ (Real.sqrt_nonneg _) (by positivity)).mp
  rw [Real.sq_sqrt (sqNorm_nonneg _)]
  have h := multibit_residual_sq A A' x b D J s d B H hB hH hA hA' hx hs hd hD hfeas hlocal
  calc
    _ ≤ _ := h
    _ = _ := by rw [div_pow, mul_pow, Real.sq_sqrt ht]; ring

omit [Fintype I] [Fintype R] in
/-- The manuscript's row-union assumption implies the coefficientwise bound. -/
theorem coefficient_card_le_row_union [DecidableEq I]
    (J : R → C → Finset I) (d : ℕ)
    (hd : ∀ r, (Finset.univ.biUnion (J r)).card ≤ d) :
    ∀ r j, (J r j).card ≤ d := by
  intro r j
  exact (Finset.card_le_card (Finset.subset_biUnion_of_mem (J r) (Finset.mem_univ j))).trans (hd r)

/-- The manuscript's multibit supplement under its row-union locality hypothesis. -/
theorem multibit_row_union_bound [Nonempty I] [DecidableEq I] (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (x : I → C → ℝ) (b : R → ℝ)
    (D : R → Finset C) (J : R → C → Finset I) (s d : ℕ) (B H : ℝ)
    (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hd : ∀ r, (Finset.univ.biUnion (J r)).card ≤ d)
    (hD : ∀ r j, j ∉ D r → J r j = ∅)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hlocal : ∀ i r j, i ∉ J r j → A' i r j = A r j) :
    euclideanNorm (residual A (mix (uniformWeight I) x) b) ≤
      2 * B * H * Real.sqrt ((d : ℝ) * s * (∑ r, ∑ j, ((J r j).card : ℝ))) /
        (Fintype.card I : ℝ) :=
  multibit_residual_bound A A' x b D J s d B H hB hH hA hA' hx hs
    (coefficient_card_le_row_union J d hd) hD hfeas hlocal

end
end QipmFormal.Mixture
