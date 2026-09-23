import Mathlib

/-! Finite residue counts used by the attaining distribution. -/

namespace MultilinearGap

open scoped BigOperators

/-- Each residue occurs exactly `a` times in `a` complete periods. -/
theorem sum_residue_indicator (a b : ℕ) (t : Fin b) :
    (∑ i : Fin (a * b), if i.val % b = t.val then (1 : ℝ) else 0) = a := by
  rw [← finProdFinEquiv.sum_comp]
  rw [Fintype.sum_prod_type]
  simp only [finProdFinEquiv, Equiv.coe_fn_mk, Nat.add_mul_mod_self_left,
    Nat.mod_eq_of_lt, Fin.is_lt]
  simp [Fin.val_inj]

/-- The same count when the length is supplied through a divisibility hypothesis. -/
theorem sum_residue_indicator_of_dvd (N D : ℕ) (hdiv : D ∣ N) (t : Fin D) :
    (∑ i : Fin N, if i.val % D = t.val then (1 : ℝ) else 0) = (N / D : ℕ) := by
  obtain ⟨a, rfl⟩ := hdiv
  rw [Nat.mul_comm D a, sum_residue_indicator]
  have hD : 0 < D := lt_of_le_of_lt (Nat.zero_le t.val) t.is_lt
  rw [Nat.mul_div_cancel _ hD]

/-- The number of coordinates outside a fixed residue class. -/
theorem sum_residue_complement (a b : ℕ) (t : Fin b) :
    (∑ i : Fin (a * b), if i.val % b = t.val then (0 : ℝ) else 1) =
      ((a * b : ℕ) : ℝ) - a := by
  have h (i : Fin (a * b)) : (if i.val % b = t.val then (0 : ℝ) else 1) =
      1 - (if i.val % b = t.val then (1 : ℝ) else 0) := by
    split_ifs <;> norm_num
  simp only [h, Finset.sum_sub_distrib]
  rw [sum_residue_indicator]
  simp

/-- Exactly one choice of residue hits a fixed coordinate. -/
theorem sum_coordinate_residue_indicator (D i : ℕ) (hD : 0 < D) :
    (∑ t : Fin D, if i % D = t.val then (1 : ℝ) else 0) = 1 := by
  let r : Fin D := ⟨i % D, Nat.mod_lt i hD⟩
  have h (t : Fin D) : i % D = t.val ↔ t = r := by
    simp [r, Fin.ext_iff, eq_comm]
  simp only [h]
  simp

/-- Summing the binary coordinates of the residue construction gives `D - 1`. -/
theorem sum_coordinate_residue_complement (D i : ℕ) (hD : 0 < D) :
    (∑ t : Fin D, if i % D = t.val then (0 : ℝ) else 1) = (D : ℝ) - 1 := by
  have h (t : Fin D) : (if i % D = t.val then (0 : ℝ) else 1) =
      1 - (if i % D = t.val then (1 : ℝ) else 0) := by
    split_ifs <;> norm_num
  simp only [h, Finset.sum_sub_distrib]
  rw [sum_coordinate_residue_indicator D i hD]
  simp

/-- A block whose length is a positive multiple of the period meets every residue. -/
theorem block_product_residue_zero (S D b t : ℕ) (_hD : 0 < D)
    (hdiv : D ∣ S) (hS : 0 < S) (ht : t < D) :
    (∏ r : Fin S, if (b * S + r.val) % D = t then (0 : ℝ) else 1) = 0 := by
  have hDS : D ≤ S := Nat.le_of_dvd hS hdiv
  let r : Fin S := ⟨t, lt_of_lt_of_le ht hDS⟩
  apply Finset.prod_eq_zero (Finset.mem_univ r)
  have hmul : D ∣ b * S := dvd_mul_of_dvd_right hdiv b
  simp [r, Nat.add_mod, Nat.mod_eq_zero_of_dvd hmul, Nat.mod_eq_of_lt ht]

end MultilinearGap
