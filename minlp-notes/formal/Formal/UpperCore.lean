import Formal.Model

namespace ExactCounts
open scoped BigOperators

/-- Rational box disaggregation with explicitly retained continuous weights. -/
def WeightedBoxes {J : Type*} [Fintype J] (n p : ℕ)
    (lo hi : J → Fin n → Fin 3 → ℚ) (label : J → Fin p → ℚ)
    (v : Visible n) (z : Code p) (w : J → ℝ) : Prop :=
  (∀ j, 0 ≤ w j) ∧ (∑ j, w j) = 1 ∧
  (∀ i k, (∑ j, w j * (lo j i k : ℝ)) ≤ v i k ∧
    v i k ≤ ∑ j, w j * (hi j i k : ℝ)) ∧
  (∀ l, z l = ∑ j, w j * (label j l : ℝ))

/-- A point in a single box is represented by its unit weight vector. -/
theorem weightedBoxes_single {J : Type*} [Fintype J] [DecidableEq J] {n p : ℕ}
    {lo hi : J → Fin n → Fin 3 → ℚ} {label : J → Fin p → ℚ}
    (j : J) (v : Visible n)
    (hv : ∀ i k, (lo j i k : ℝ) ≤ v i k ∧ v i k ≤ (hi j i k : ℝ)) :
    WeightedBoxes n p lo hi label v (fun l => (label j l : ℝ))
      (fun t => if t = j then 1 else 0) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro t; dsimp; split_ifs <;> norm_num
  · simp
  · simpa using hv
  · simp

/-- A positive weight in a binary slice can only use that exact binary code. -/
theorem binary_weight_support {J : Type*} [Fintype J] {p : ℕ}
    (label : J → Fin p → ℚ) (hlabel : ∀ j l, label j l = 0 ∨ label j l = 1)
    {z : Code p} {w : J → ℝ} (hw : ∀ j, 0 ≤ w j) (hs : ∑ j, w j = 1)
    (hz : ∀ l, z l = ∑ j, w j * (label j l : ℝ)) (hbin : z ∈ BinaryCodes p)
    {j : J} (hj : 0 < w j) : ∀ l, (label j l : ℝ) = z l := by
  intro l
  rcases hbin l with hzero | hone
  · have hsum : ∑ t, w t * (label t l : ℝ) = 0 := by rw [← hz, hzero]
    have hnon : ∀ t ∈ (Finset.univ : Finset J), 0 ≤ w t * (label t l : ℝ) := by
      intro t _; rcases hlabel t l with h | h <;> simp [h, hw]
    have heq := (Finset.sum_eq_zero_iff_of_nonneg hnon).mp hsum j (Finset.mem_univ j)
    have : (label j l : ℝ) = 0 := (mul_eq_zero.mp heq).resolve_left (ne_of_gt hj)
    simpa [hzero] using this
  · have hsum : ∑ t, w t * (1 - (label t l : ℝ)) = 0 := by
      simp_rw [mul_sub, mul_one]
      rw [Finset.sum_sub_distrib, hs, ← hz, hone]; ring
    have hnon : ∀ t ∈ (Finset.univ : Finset J), 0 ≤ w t * (1 - (label t l : ℝ)) := by
      intro t _; rcases hlabel t l with h | h <;> simp [h, hw]
    have heq := (Finset.sum_eq_zero_iff_of_nonneg hnon).mp hsum j (Finset.mem_univ j)
    have : 1 - (label j l : ℝ) = 0 := (mul_eq_zero.mp heq).resolve_left (ne_of_gt hj)
    rw [hone]; linarith

end ExactCounts
