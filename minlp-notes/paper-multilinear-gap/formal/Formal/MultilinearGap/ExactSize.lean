import Formal.MultilinearGap.FamilySize
import Mathlib.Analysis.SpecialFunctions.Log.Base
import Mathlib.Analysis.Asymptotics.Defs

/-! Exact size and sparsity of the dyadic witness family. -/
namespace MultilinearGap
open scoped BigOperators
noncomputable section

private theorem sum_blockCount (L : ℕ) :
    (∑ j : Fin L, blockCount L j) + 2 = 2 ^ (L + 1) := by
  simp only [blockCount]
  induction L with
  | zero => simp
  | succ L ih =>
    rw [Fin.sum_univ_castSucc]
    simp only [Fin.val_castSucc, Fin.val_last]
    rw [pow_succ (2 : ℕ) (L + 1)]
    omega

/-- The number of distinct squarefree monomials, including the empty family at L = 0. -/
theorem supports_card (L : ℕ) : (supports L).card = 2 ^ (L + 1) - 2 := by
  rw [supports, Finset.card_image_of_injective _ (support_injective L)]
  simp only [Finset.card_univ, Fintype.card_sigma, Fintype.card_fin]
  have h := sum_blockCount L
  omega

/-- The stated maximum degree is attained at the first level. -/
theorem exists_support_card_eq (L : ℕ) (hL : 0 < L) :
    ∃ e ∈ supports L, e.card = 2 ^ (L - 1) + 1 := by
  let j : Fin L := ⟨0, hL⟩
  let b : Fin (blockCount L j) := ⟨0, by simp [blockCount, j]⟩
  refine ⟨support L j b, ?_, ?_⟩
  · exact Finset.mem_image.mpr ⟨⟨j, b⟩, Finset.mem_univ _, rfl⟩
  · rw [support_card]; rfl

/-- Exact maximum support size, with the necessary positive-level hypothesis. -/
theorem supports_max_degree (L : ℕ) (hL : 0 < L) :
    (supports L).sup Finset.card = 2 ^ (L - 1) + 1 := by
  apply le_antisymm
  · exact Finset.sup_le (fun e he => support_card_le L e he)
  · obtain ⟨e, he, hcard⟩ := exists_support_card_eq L hL
    rw [← hcard]
    exact Finset.le_sup he

/-- Total incidences of variables in monomials. -/
theorem supports_occurrences (L : ℕ) :
    (∑ e ∈ supports L, e.card) = L * 2 ^ L + 2 ^ (L + 1) - 2 := by
  rw [supports, Finset.sum_image (fun a _ b _ h => support_injective L h)]
  rw [Fintype.sum_sigma]
  simp only [support_card, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    smul_eq_mul, mul_add, mul_one, blockCount_mul_blockSize, Finset.sum_add_distrib]
  have h := sum_blockCount L
  omega

/-- There are fewer than twice as many monomials as coordinates. -/
theorem supports_card_lt_twice_dimension (L : ℕ) :
    (supports L).card < 2 * Fintype.card (Coord L) := by
  rw [supports_card, coord_card, pow_succ]
  have h : 0 < 2 ^ L := by positivity
  omega

/-- Explicit sparsity bound, stronger than the claimed O(n log n) estimate. -/
theorem supports_occurrences_le_dimension_log (L : ℕ) (hL : 2 ≤ L) :
    (∑ e ∈ supports L, e.card) ≤
      2 * Fintype.card (Coord L) * Nat.log 2 (Fintype.card (Coord L)) := by
  have hlog : L ≤ Nat.log 2 (Fintype.card (Coord L)) :=
    Nat.le_log_of_pow_le (by decide) (by rw [coord_card]; omega)
  have hdim : 2 ^ L ≤ Fintype.card (Coord L) := by rw [coord_card]; omega
  have hprod := Nat.mul_le_mul hdim hlog
  rw [supports_occurrences, pow_succ]
  calc
    L * 2 ^ L + 2 ^ L * 2 - 2 ≤ L * 2 ^ L + 2 ^ L * 2 := Nat.sub_le _ _
    _ ≤ 2 * (2 ^ L * L) := by nlinarith [Nat.mul_le_mul_right (2 ^ L) hL]
    _ ≤ _ := by simpa [Nat.mul_assoc] using Nat.mul_le_mul_left 2 hprod

/-- Real-log form of the explicit occurrence bound. -/
theorem supports_occurrences_le_dimension_real_log (L : ℕ) (hL : 2 ≤ L) :
    ((∑ e ∈ supports L, e.card) : ℝ) ≤
      (2 / Real.log 2) * (Fintype.card (Coord L) : ℝ) *
        Real.log (Fintype.card (Coord L)) := by
  have h := supports_occurrences_le_dimension_log L hL
  have hc : ((∑ e ∈ supports L, e.card) : ℝ) ≤
      2 * (Fintype.card (Coord L) : ℝ) *
        (Nat.log 2 (Fintype.card (Coord L)) : ℝ) := by exact_mod_cast h
  have hr := Real.natLog_le_logb (Fintype.card (Coord L)) 2
  norm_num only [Nat.cast_ofNat] at hr
  calc
    _ ≤ _ := hc
    _ ≤ 2 * (Fintype.card (Coord L) : ℝ) *
        Real.logb 2 (Fintype.card (Coord L)) :=
      mul_le_mul_of_nonneg_left hr (by positivity)
    _ = _ := by rw [Real.logb]; ring

/-- The occurrence count is O(n_L log n_L), as L tends to infinity. -/
theorem supports_occurrences_isBigO :
    (fun L : ℕ => ((∑ e ∈ supports L, e.card) : ℝ)) =O[Filter.atTop]
      (fun L : ℕ => (Fintype.card (Coord L) : ℝ) *
        Real.log (Fintype.card (Coord L))) := by
  apply Asymptotics.IsBigO.of_bound (2 / Real.log 2)
  filter_upwards [Filter.eventually_ge_atTop 2] with L hL
  have hn : (1 : ℝ) ≤ (Fintype.card (Coord L) : ℝ) := by
    have : 1 ≤ Fintype.card (Coord L) := by
      rw [coord_card]
      have hp : 0 < 2 ^ L := by positivity
      omega
    exact_mod_cast this
  rw [Real.norm_eq_abs, abs_of_nonneg (by positivity), Real.norm_eq_abs,
    abs_of_nonneg (mul_nonneg (by positivity) (Real.log_nonneg hn))]
  simpa [mul_assoc] using supports_occurrences_le_dimension_real_log L hL

end
end MultilinearGap
