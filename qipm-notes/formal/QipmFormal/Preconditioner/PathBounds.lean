import QipmFormal.Preconditioner.Path

namespace QipmFormal.Preconditioner

open scoped BigOperators

/-- Discrete Poincaré inequality for a path pinned to zero at its right end. -/
theorem range_path_norm_le (m : ℕ) (x : ℕ → ℝ) (hx : x m = 0) :
    (∑ i ∈ Finset.range m, x i ^ 2) ≤
      (m : ℝ) ^ 2 * ∑ i ∈ Finset.range m, (x i - x (i + 1)) ^ 2 := by
  have hp (i : ℕ) (hi : i < m) :
      x i ^ 2 ≤ (m : ℝ) * ∑ j ∈ Finset.range m, (x j - x (j + 1)) ^ 2 := by
    have ht : ∑ j ∈ Finset.Ico i m, (x j - x (j + 1)) = x i := by
      rw [Finset.sum_Ico_eq_sub _ hi.le, Finset.sum_range_sub',
        Finset.sum_range_sub', hx]
      ring
    have hcs := Finset.sum_mul_sq_le_sq_mul_sq (Finset.Ico i m)
      (fun _ => (1 : ℝ)) (fun j => x j - x (j + 1))
    simp only [one_mul, one_pow, Finset.sum_const, nsmul_eq_mul, mul_one,
      Nat.card_Ico] at hcs
    rw [ht] at hcs
    have hsub : (∑ j ∈ Finset.Ico i m, (x j - x (j + 1)) ^ 2) ≤
        ∑ j ∈ Finset.range m, (x j - x (j + 1)) ^ 2 := by
      apply Finset.sum_le_sum_of_subset_of_nonneg
      · intro j hj
        exact Finset.mem_range.mpr (Finset.mem_Ico.mp hj).2
      · intro j _ _
        exact sq_nonneg _
    have hm : ((m - i : ℕ) : ℝ) ≤ m := by exact_mod_cast Nat.sub_le m i
    exact hcs.trans (mul_le_mul hm hsub (Finset.sum_nonneg fun _ _ => sq_nonneg _)
      (Nat.cast_nonneg _))
  calc
    _ ≤ ∑ _i ∈ Finset.range m,
        (m : ℝ) * ∑ j ∈ Finset.range m, (x j - x (j + 1)) ^ 2 :=
      Finset.sum_le_sum fun i hi => hp i (Finset.mem_range.mp hi)
    _ = _ := by simp [pow_two, mul_assoc]

/-- Elementary upper spectral bound for a path difference operator. -/
theorem range_path_energy_le (m : ℕ) (x : ℕ → ℝ) (hx : x m = 0) :
    (∑ i ∈ Finset.range m, (x i - x (i + 1)) ^ 2) ≤
      4 * ∑ i ∈ Finset.range m, x i ^ 2 := by
  have hshift : ∑ i ∈ Finset.range m, x (i + 1) ^ 2 ≤
      ∑ i ∈ Finset.range m, x i ^ 2 := by
    have h := Finset.sum_range_succ' (fun i => x i ^ 2) m
    rw [Finset.sum_range_succ, hx] at h
    nlinarith [sq_nonneg (x 0)]
  calc
    _ ≤ ∑ i ∈ Finset.range m, (2 * x i ^ 2 + 2 * x (i + 1) ^ 2) := by
      apply Finset.sum_le_sum
      intro i _
      nlinarith [sq_nonneg (x i + x (i + 1))]
    _ = 2 * (∑ i ∈ Finset.range m, x i ^ 2) +
        2 * (∑ i ∈ Finset.range m, x (i + 1) ^ 2) := by
      simp only [Finset.sum_add_distrib, Finset.mul_sum]
    _ ≤ _ := by linarith

/-- Extend a vector by zero beyond its finite domain. -/
def pathZeroExtension {m : ℕ} (x : Fin m → ℝ) (i : ℕ) : ℝ :=
  if h : i < m then x ⟨i, h⟩ else 0

lemma pathZeroExtension_sum_sq {m : ℕ} (x : Fin m → ℝ) :
    (∑ i ∈ Finset.range m, pathZeroExtension x i ^ 2) = ∑ i, x i ^ 2 := by
  rw [← Fin.sum_univ_eq_sum_range]
  apply Finset.sum_congr rfl
  intro i _
  simp [pathZeroExtension, i.isLt]

lemma pathZeroExtension_energy {m : ℕ} (x : Fin m → ℝ) :
    (∑ i ∈ Finset.range m, (pathZeroExtension x i - pathZeroExtension x (i + 1)) ^ 2) =
      ∑ i : Fin m, (x i - if h : i.val + 1 < m then x ⟨i.val + 1, h⟩ else 0) ^ 2 := by
  rw [← Fin.sum_univ_eq_sum_range]
  apply Finset.sum_congr rfl
  intro i _
  simp [pathZeroExtension, i.isLt]

/-- Squared norm bound for the finite path difference operator. -/
theorem fin_path_norm_le {m : ℕ} (x : Fin m → ℝ) :
    (∑ i, x i ^ 2) ≤ (m : ℝ) ^ 2 *
      ∑ i : Fin m, (x i - if h : i.val + 1 < m then x ⟨i.val + 1, h⟩ else 0) ^ 2 := by
  have h := range_path_norm_le m (pathZeroExtension x) (by simp [pathZeroExtension])
  rwa [pathZeroExtension_sum_sq, pathZeroExtension_energy] at h

/-- Squared norm of finite path differences is at most four times the vector's squared norm. -/
theorem fin_path_energy_le {m : ℕ} (x : Fin m → ℝ) :
    (∑ i : Fin m, (x i - if h : i.val + 1 < m then x ⟨i.val + 1, h⟩ else 0) ^ 2) ≤
      4 * ∑ i, x i ^ 2 := by
  have h := range_path_energy_le m (pathZeroExtension x) (by simp [pathZeroExtension])
  rwa [pathZeroExtension_sum_sq, pathZeroExtension_energy] at h

/-- Discrete Poincaré inequality for the grounded path quadratic form. -/
theorem path_norm_le {m : ℕ} (x : Fin m → ℝ) :
    (∑ i, x i ^ 2) ≤ (m : ℝ) ^ 2 * pathEnergy x :=
  fin_path_norm_le x

/-- Upper quadratic-form bound for the grounded path. -/
theorem path_energy_le {m : ℕ} (x : Fin m → ℝ) :
    pathEnergy x ≤ 4 * ∑ i, x i ^ 2 :=
  fin_path_energy_le x

end QipmFormal.Preconditioner
