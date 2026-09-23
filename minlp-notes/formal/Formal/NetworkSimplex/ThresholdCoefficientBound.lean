import Formal.NetworkSimplex.ThresholdDeterminant
import Mathlib

/-! Original-coordinate coefficient bounds and exact expansion of grouped minima. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators

/-- Summing at most `m + 1` unit-coefficient rows with integer weights at most
`delta01 m` gives the stated integer original-coordinate bound. -/
theorem weighted_coefficient_natAbs_le {I : Type*} [Fintype I] {m : ℕ}
    (w : I → ℕ) (c : I → ℤ) (hsize : Fintype.card I ≤ m + 1)
    (hw : ∀ i, w i ≤ delta01 m) (hc : ∀ i, (c i).natAbs ≤ 1) :
    (∑ i, (w i : ℤ) * c i).natAbs ≤ (m + 1) * delta01 m := by
  calc
    _ ≤ ∑ i, ((w i : ℤ) * c i).natAbs := Int.natAbs_sum_le _ _
    _ ≤ ∑ _ : I, delta01 m := by
      apply Finset.sum_le_sum
      intro i _
      simpa only [Int.natAbs_mul, Int.natAbs_natCast, mul_one] using
        Nat.mul_le_mul (hw i) (hc i)
    _ = Fintype.card I * delta01 m := by simp
    _ ≤ (m + 1) * delta01 m := Nat.mul_le_mul_right _ hsize

/-- Absolute-value form of the original-coordinate integer coefficient bound. -/
theorem weighted_coefficient_abs_le {I : Type*} [Fintype I] {m : ℕ}
    (w : I → ℕ) (c : I → ℤ) (hsize : Fintype.card I ≤ m + 1)
    (hw : ∀ i, w i ≤ delta01 m) (hc : ∀ i, (c i).natAbs ≤ 1) :
    |∑ i, (w i : ℤ) * c i| ≤ ((m + 1) * delta01 m : ℕ) := by
  have h := weighted_coefficient_natAbs_le w c hsize hw hc
  have h' : ((∑ i, (w i : ℤ) * c i).natAbs : ℤ) ≤ ((m + 1) * delta01 m : ℕ) := by
    exact_mod_cast h
  simpa only [Int.natCast_natAbs] using h'

/-- Minimum of the right-hand sides grouped under one normal. -/
noncomputable def groupMinimum {J : Type*} [Fintype J] [Nonempty J] (b : J → ℝ) : ℝ :=
  Finset.univ.inf' Finset.univ_nonempty b

theorem groupMinimum_le {J : Type*} [Fintype J] [Nonempty J] (b : J → ℝ) (j : J) :
    groupMinimum b ≤ b j := Finset.inf'_le b (Finset.mem_univ j)

theorem groupMinimum_attained {J : Type*} [Fintype J] [Nonempty J] (b : J → ℝ) :
    ∃ j, groupMinimum b = b j := by
  obtain ⟨j, _, hj⟩ := Finset.exists_mem_eq_inf' Finset.univ_nonempty b
  exact ⟨j, hj⟩

/-- Nonnegative weights permit every independently selected original row branch. -/
theorem weighted_groupMinimum_le_branch {I : Type*} [Fintype I]
    {J : I → Type*} [∀ i, Fintype (J i)] [∀ i, Nonempty (J i)]
    (w : I → ℝ) (hw : ∀ i, 0 ≤ w i) (b : ∀ i, J i → ℝ) (choice : ∀ i, J i) :
    (∑ i, w i * groupMinimum (b i)) ≤ ∑ i, w i * b i (choice i) := by
  apply Finset.sum_le_sum
  intro i _
  exact mul_le_mul_of_nonneg_left (groupMinimum_le (b i) (choice i)) (hw i)

/-- Simultaneous minimizers exist because the row choice in each group is independent. -/
theorem weighted_groupMinimum_attained {I : Type*} [Fintype I]
    {J : I → Type*} [∀ i, Fintype (J i)] [∀ i, Nonempty (J i)]
    (w : I → ℝ) (b : ∀ i, J i → ℝ) :
    ∃ choice : ∀ i, J i, (∑ i, w i * groupMinimum (b i)) =
      ∑ i, w i * b i (choice i) := by
  choose choice hc using fun i => groupMinimum_attained (b i)
  refine ⟨choice, ?_⟩
  exact Finset.sum_congr rfl (fun i _ => congrArg (w i * ·) (hc i))

/-- The weighted sum of group minima is exactly the minimum of all affine branches. -/
theorem weighted_groupMinimum_eq_minimum {I : Type*} [Fintype I] [DecidableEq I]
    {J : I → Type*} [∀ i, Fintype (J i)] [∀ i, Nonempty (J i)]
    (w : I → ℝ) (hw : ∀ i, 0 ≤ w i) (b : ∀ i, J i → ℝ) :
    (∑ i, w i * groupMinimum (b i)) =
      groupMinimum (fun choice : ∀ i, J i => ∑ i, w i * b i (choice i)) := by
  classical
  apply le_antisymm
  · apply Finset.le_inf'
    intro choice _
    exact weighted_groupMinimum_le_branch w hw b choice
  · obtain ⟨choice, hc⟩ := weighted_groupMinimum_attained w b
    exact (groupMinimum_le _ choice).trans_eq hc.symm

/-- A grouped certificate is equivalent to every fixed original-row branch.
The chosen branch is therefore valid wherever the grouped certificate is valid,
even if different rows attain the minima at a different query. -/
theorem weighted_groupMinimum_nonneg_iff {I : Type*} [Fintype I]
    {J : I → Type*} [∀ i, Fintype (J i)] [∀ i, Nonempty (J i)]
    (w : I → ℝ) (hw : ∀ i, 0 ≤ w i) (b : ∀ i, J i → ℝ) :
    0 ≤ (∑ i, w i * groupMinimum (b i)) ↔
      ∀ choice : ∀ i, J i, 0 ≤ ∑ i, w i * b i (choice i) := by
  constructor
  · intro h choice
    exact h.trans (weighted_groupMinimum_le_branch w hw b choice)
  · intro h
    obtain ⟨choice, hc⟩ := weighted_groupMinimum_attained w b
    rw [hc]
    exact h choice

/-- Minima chosen at an infeasible query give a fixed branch that remains valid
throughout the feasible set, even when its active rows change elsewhere. -/
theorem exists_violated_valid_branch {I X : Type*} [Fintype I]
    {J : I → Type*} [∀ i, Fintype (J i)] [∀ i, Nonempty (J i)]
    (w : I → ℝ) (hw : ∀ i, 0 ≤ w i) (b : ∀ i, J i → X → ℝ)
    (S : Set X) (x₀ : X)
    (hvalid : ∀ x ∈ S, 0 ≤ ∑ i, w i * groupMinimum (fun j => b i j x))
    (hviolated : (∑ i, w i * groupMinimum (fun j => b i j x₀)) < 0) :
    ∃ choice : ∀ i, J i,
      (∀ x ∈ S, 0 ≤ ∑ i, w i * b i (choice i) x) ∧
      (∑ i, w i * b i (choice i) x₀) < 0 := by
  obtain ⟨choice, he⟩ := weighted_groupMinimum_attained w (fun i j => b i j x₀)
  refine ⟨choice, ?_, he ▸ hviolated⟩
  intro x hx
  exact (weighted_groupMinimum_nonneg_iff w hw (fun i j => b i j x)).mp
    (hvalid x hx) choice

end NetworkSimplex.Threshold
