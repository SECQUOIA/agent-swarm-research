import Mathlib

/-! Finite counting and an equally spaced grid for the aggregation lower bound. -/

noncomputable section

namespace InfiniteAggregation

/-- If every member of a family of at most `N` cuts excludes at most one of
`N + 1` points, some point satisfies every cut. -/
theorem exists_unviolated_of_card_le {α : Type*} {N : ℕ} (W : Finset α)
    (hcard : W.card ≤ N) (violates : α → Fin (N + 1) → Prop)
    (hone : ∀ w ∈ W, ∀ i j, violates w i → violates w j → i = j) :
    ∃ i, ∀ w ∈ W, ¬ violates w i := by
  classical
  by_contra h
  push Not at h
  choose f hfmem hf using h
  have hinj : Function.Injective f := by
    intro i j hij
    exact hone (f i) (hfmem i) i j (hf i) (hij ▸ hf j)
  have hle : N + 1 ≤ W.card := by
    have := Finset.card_le_card_of_injOn f
      (s := Finset.univ) (t := W) (fun i _ => hfmem i) hinj.injOn
    simpa using this
  omega

/-- The `N + 1` equally spaced parameters in `[1, 2]`. -/
def accuracyGrid (N : ℕ) (i : Fin (N + 1)) : ℝ := 1 + (i.val : ℝ) / N

theorem accuracyGrid_mem_Icc {N : ℕ} (hN : 0 < N) (i : Fin (N + 1)) :
    accuracyGrid N i ∈ Set.Icc (1 : ℝ) 2 := by
  have hNr : (0 : ℝ) < N := by exact_mod_cast hN
  have hi : (i.val : ℝ) ≤ N := by exact_mod_cast (Nat.le_of_lt_succ i.isLt)
  constructor
  · dsimp [accuracyGrid]
    exact le_add_of_nonneg_right (div_nonneg (Nat.cast_nonneg _) hNr.le)
  · dsimp [accuracyGrid]
    have := (div_le_one hNr).2 hi
    linarith

theorem accuracyGrid_separated {N : ℕ} (hN : 0 < N)
    {i j : Fin (N + 1)} (hij : i ≠ j) :
    1 / (N : ℝ) ≤ |accuracyGrid N i - accuracyGrid N j| := by
  have hNr : (0 : ℝ) < N := by exact_mod_cast hN
  have hne : i.val ≠ j.val := fun h => hij (Fin.ext h)
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · have hstep : (i.val : ℝ) + 1 ≤ j.val := by exact_mod_cast hlt
    have hdiff : accuracyGrid N i - accuracyGrid N j ≤ 0 := by
      dsimp [accuracyGrid]
      have := (div_le_div_iff_of_pos_right hNr).2 (by linarith : (i.val : ℝ) ≤ j.val)
      linarith
    rw [abs_of_nonpos hdiff]
    dsimp [accuracyGrid]
    have := (div_le_div_iff_of_pos_right hNr).2 (show (1 : ℝ) ≤ j.val - i.val by linarith)
    rw [sub_div] at this
    linarith
  · have hstep : (j.val : ℝ) + 1 ≤ i.val := by exact_mod_cast hgt
    have hdiff : 0 ≤ accuracyGrid N i - accuracyGrid N j := by
      dsimp [accuracyGrid]
      have := (div_le_div_iff_of_pos_right hNr).2 (by linarith : (j.val : ℝ) ≤ i.val)
      linarith
    rw [abs_of_nonneg hdiff]
    dsimp [accuracyGrid]
    have := (div_le_div_iff_of_pos_right hNr).2 (show (1 : ℝ) ≤ i.val - j.val by linarith)
    rw [sub_div] at this
    linarith

end InfiniteAggregation
