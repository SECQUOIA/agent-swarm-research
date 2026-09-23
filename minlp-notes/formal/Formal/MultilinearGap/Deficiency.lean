import Formal.CubicGap.Expectation

/-! A finite-law upper bound for the dyadic counterexample. -/

namespace MultilinearGap

open scoped BigOperators

private theorem dyadic_sum_bound (k : ℕ) :
    ∑ j ∈ Finset.range k, (2 : ℝ) ^ (j + 1) ≤ 2 ^ (k + 1) := by
  induction k with
  | zero => simp
  | succ k hk =>
    rw [Finset.sum_range_succ]
    calc
      _ ≤ 2 ^ (k + 1) + 2 ^ (k + 1) := add_le_add hk (le_refl ((2 : ℝ) ^ (k + 1)))
      _ = 2 ^ (k + 1 + 1) := by rw [pow_succ]; ring

/-- A deterministic bound, with no assumptions on how the selected scales depend
on the nonnegative deficiency `r`. -/
theorem dyadic_selected_bound (S : Finset ℕ) (r : ℝ) (hr : 0 ≤ r) (s : ℕ) :
    ∑ j ∈ S, min ((2 : ℝ) ^ (j + 1)) r ≤
      (s : ℝ) * r + 2 / (2 : ℝ) ^ s * ∑ j ∈ S, (2 : ℝ) ^ (j + 1) := by
  classical
  by_cases hS : S.Nonempty
  · let m := S.max' hS
    have hm : ∀ j ∈ S, j ≤ m := fun j hj => Finset.le_max' S j hj
    have hmS : m ∈ S := Finset.max'_mem S hS
    have hmax : (2 : ℝ) ^ (m + 1) ≤ ∑ j ∈ S, (2 : ℝ) ^ (j + 1) :=
      Finset.single_le_sum (f := fun j => (2 : ℝ) ^ (j + 1)) (fun j _ => by positivity) hmS
    by_cases hs : s ≤ m + 1
    · let k := m + 1 - s
      have hks : k + s = m + 1 := Nat.sub_add_cancel hs
      let A := S.filter (fun j => j < k)
      let B := S.filter (fun j => ¬j < k)
      have hA : A ⊆ Finset.range k := by
        intro j hj
        exact Finset.mem_range.mpr (Finset.mem_filter.mp hj).2
      have hB : B ⊆ Finset.Ico k (m + 1) := by
        intro j hj
        rcases Finset.mem_filter.mp hj with ⟨hj, hk⟩
        exact Finset.mem_Ico.mpr ⟨by omega, by have := hm j hj; omega⟩
      have hcard : B.card ≤ s := by
        have := Finset.card_le_card hB
        rw [Nat.card_Ico] at this
        omega
      have hlow : ∑ j ∈ A, min ((2 : ℝ) ^ (j + 1)) r ≤ 2 ^ (k + 1) := by
        calc
          _ ≤ ∑ j ∈ A, (2 : ℝ) ^ (j + 1) :=
            Finset.sum_le_sum fun j _ => min_le_left _ _
          _ ≤ ∑ j ∈ Finset.range k, (2 : ℝ) ^ (j + 1) :=
            Finset.sum_le_sum_of_subset_of_nonneg hA (fun _ _ _ => by positivity)
          _ ≤ _ := dyadic_sum_bound k
      have hhigh : ∑ j ∈ B, min ((2 : ℝ) ^ (j + 1)) r ≤ (s : ℝ) * r := by
        calc
          _ ≤ ∑ _j ∈ B, r := Finset.sum_le_sum fun j _ => min_le_right _ _
          _ = (B.card : ℝ) * r := by simp
          _ ≤ _ := mul_le_mul_of_nonneg_right (by exact_mod_cast hcard) hr
      have hpow : (2 : ℝ) ^ (k + 1) = 2 / (2 : ℝ) ^ s * (2 : ℝ) ^ (m + 1) := by
        rw [← hks, pow_add, pow_succ]
        field_simp
        rw [pow_add]
      calc
        _ = (∑ j ∈ A, min ((2 : ℝ) ^ (j + 1)) r) +
            ∑ j ∈ B, min ((2 : ℝ) ^ (j + 1)) r := by
          exact (Finset.sum_filter_add_sum_filter_not S (fun j => j < k) _).symm
        _ ≤ 2 ^ (k + 1) + (s : ℝ) * r := add_le_add hlow hhigh
        _ ≤ _ := by
          rw [hpow]
          nlinarith [mul_le_mul_of_nonneg_left hmax
            (show 0 ≤ 2 / (2 : ℝ) ^ s by positivity)]
    · have hcard : S.card ≤ s := by
        have hsub : S ⊆ Finset.range (m + 1) := by
          intro j hj
          exact Finset.mem_range.mpr (by have := hm j hj; omega)
        have := Finset.card_le_card hsub
        simp only [Finset.card_range] at this
        omega
      calc
        _ ≤ ∑ _j ∈ S, r := Finset.sum_le_sum fun j _ => min_le_right _ _
        _ = (S.card : ℝ) * r := by simp
        _ ≤ (s : ℝ) * r := mul_le_mul_of_nonneg_right (by exact_mod_cast hcard) hr
        _ ≤ _ := le_add_of_nonneg_right (by positivity)
  · have : S = ∅ := Finset.not_nonempty_iff_eq_empty.mp hS
    simp [this, mul_nonneg (Nat.cast_nonneg s) hr]

/-- The deterministic bound indexed by `Fin L`. -/
theorem dyadic_pointwise_bound {L : ℕ} (a : Fin L → Bool)
    (r : ℝ) (hr : 0 ≤ r) (s : ℕ) :
    (∑ j, if a j then min ((2 : ℝ) ^ (j.val + 1)) r else 0) ≤
      (s : ℝ) * r + 2 / (2 : ℝ) ^ s *
        ∑ j, if a j then (2 : ℝ) ^ (j.val + 1) else 0 := by
  classical
  let T := Finset.univ.filter (fun j : Fin L => a j = true)
  have hsum (f : ℕ → ℝ) :
      ∑ j ∈ T.image Fin.val, f j = ∑ j : Fin L, if a j then f j.val else 0 := by
    rw [Finset.sum_image]
    · simp [T, Finset.sum_filter]
    · intro i hi j hj hij
      exact Fin.ext hij
  have h := dyadic_selected_bound (T.image Fin.val) r hr s
  simpa only [hsum] using h

/-- Any finite joint law with dyadic activation means and mean deficiency one
has total expected deficiency at most `s + 2 L / 2^s`. -/
theorem dyadic_deficiency_bound {Ω : Type*} [Fintype Ω] {L : ℕ}
    (μ : CubicGap.Law Ω) (a : Ω → Fin L → Bool) (r : Ω → ℝ)
    (hr : ∀ ω, 0 ≤ r ω)
    (ha : ∀ j, μ.expect (fun ω => if a ω j then 1 else 0) =
      1 / (2 : ℝ) ^ (j.val + 1))
    (hmean : μ.expect r = 1) (s : ℕ) :
    μ.expect (fun ω => ∑ j, if a ω j then
      min ((2 : ℝ) ^ (j.val + 1)) (r ω) else 0) ≤
      (s : ℝ) + 2 * (L : ℝ) / (2 : ℝ) ^ s := by
  have hscale (j : Fin L) :
      μ.expect (fun ω => if a ω j then (2 : ℝ) ^ (j.val + 1) else 0) = 1 := by
    have heq : (fun ω => if a ω j then (2 : ℝ) ^ (j.val + 1) else 0) =
        (fun ω => (if a ω j then 1 else 0) * (2 : ℝ) ^ (j.val + 1)) := by
      funext ω
      split <;> simp_all
    rw [heq, μ.expect_mul_const, ha]
    field_simp
  have h := μ.expect_mono (fun ω => dyadic_pointwise_bound (a ω) (r ω) (hr ω) s)
  simp only [μ.expect_add, μ.expect_const_mul, μ.expect_sum, hmean,
    hscale, Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul,
    mul_one] at h
  rw [μ.expect_sum]
  convert h using 1
  ring

end MultilinearGap
