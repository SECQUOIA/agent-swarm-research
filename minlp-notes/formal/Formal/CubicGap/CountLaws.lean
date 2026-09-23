import Formal.CubicGap.Counts
import Formal.CubicGap.Laws

namespace CubicGap

open scoped BigOperators
noncomputable section

/-- Add a uniform rotation to a finite probability law. -/
def Law.withRotation {ι : Type*} [Fintype ι] (μ : Law ι) (m : ℕ) [NeZero m] :
    Law (ι × Fin m) where
  weight t := μ.weight t.1 / m
  nonneg t := div_nonneg (μ.nonneg t.1) (Nat.cast_nonneg _)
  mass_one := by
    have hm : (m : ℝ) ≠ 0 := by exact_mod_cast NeZero.ne m
    rw [Fintype.sum_prod_type]
    simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    simp_rw [mul_div_cancel₀ _ hm]
    exact μ.mass_one

/-- A count state becomes a binary vector by rotating a fixed success prefix. -/
def countVertex {ι G : Type*} {m : ℕ} [NeZero m]
    (k : ι → G → ℕ) (t : ι × Fin m) : G × Fin m → Bool :=
  fun p => rotate (prefixVertex m (k t.1 p.1)) t.2 p.2

theorem count_countVertex {ι G : Type*} {m : ℕ} [NeZero m]
    (k : ι → G → ℕ) (hk : ∀ i g, k i g ≤ m) (t : ι × Fin m) (g : G) :
    count (fun j => countVertex k t (g, j)) = k t.1 g := by
  exact (count_rotate _ _).trans (count_prefixVertex m _ (hk t.1 g))

theorem expect_countVertex {ι G : Type*} [Fintype ι] {m : ℕ} [NeZero m]
    (μ : Law ι) (k : ι → G → ℕ) (hk : ∀ i g, k i g ≤ m) (g : G) (j : Fin m) :
    (μ.withRotation m).expect (fun t => if countVertex k t (g, j) = true then 1 else 0) =
      μ.expect (fun i => (k i g : ℝ)) / m := by
  unfold Law.expect Law.withRotation
  rw [Fintype.sum_prod_type]
  change (∑ i, ∑ s : Fin m, μ.weight i / m *
    (if rotate (prefixVertex m (k i g)) s j = true then (1 : ℝ) else 0)) = _
  simp_rw [← Finset.mul_sum, sum_rotate]
  simp_rw [count_prefixVertex m _ (hk _ _)]
  rw [Finset.sum_div]
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem expect_withRotation {ι : Type*} [Fintype ι] {m : ℕ} [NeZero m]
    (μ : Law ι) (f : ι → ℝ) :
    (μ.withRotation m).expect (fun t => f t.1) = μ.expect f := by
  have hm : (m : ℝ) ≠ 0 := by exact_mod_cast NeZero.ne m
  unfold Law.expect Law.withRotation
  rw [Fintype.sum_prod_type]
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  apply Finset.sum_congr rfl
  intro i _
  field_simp

theorem expect_count_function {ι G : Type*} [Fintype ι] {m : ℕ} [NeZero m]
    (μ : Law ι) (k : ι → G → ℕ) (hk : ∀ i g, k i g ≤ m) (F : (G → ℕ) → ℝ) :
    (μ.withRotation m).expect
      (fun t => F (fun g => count (fun j => countVertex k t (g, j)))) =
        μ.expect (fun i => F (k i)) := by
  simp_rw [count_countVertex k hk]
  exact expect_withRotation (m := m) μ (fun i => F (k i))

/-- The binary law induced by any finite law of feasible group counts. -/
def Law.liftCounts {ι G : Type*} [Fintype ι] [Fintype G] [DecidableEq G] {m : ℕ} [NeZero m]
    (μ : Law ι) (k : ι → G → ℕ) : Law (Vertex (G × Fin m)) :=
  (μ.withRotation m).map (countVertex k)

theorem liftCounts_mean {ι G : Type*} [Fintype ι] [Fintype G] [DecidableEq G] {m : ℕ} [NeZero m]
    (μ : Law ι) (k : ι → G → ℕ) (hk : ∀ i g, k i g ≤ m) (g : G) (j : Fin m) :
    (μ.liftCounts (m := m) k).expect (fun v => vertexPoint v (g, j)) =
      μ.expect (fun i => (k i g : ℝ)) / m := by
  rw [Law.liftCounts, Law.expect_map]
  exact expect_countVertex μ k hk g j

theorem liftCounts_value {ι G : Type*} [Fintype ι] [Fintype G] [DecidableEq G] {m : ℕ} [NeZero m]
    (μ : Law ι) (k : ι → G → ℕ) (hk : ∀ i g, k i g ≤ m) (F : (G → ℕ) → ℝ) :
    (μ.liftCounts (m := m) k).expect
      (fun v => F (fun g => count (fun j => v (g, j)))) =
        μ.expect (fun i => F (k i)) := by
  rw [Law.liftCounts, Law.expect_map]
  exact expect_count_function μ k hk F

/-- Projecting a binary law to counts sums the individual singleton means. -/
theorem expect_group_count {G : Type*} [Fintype G] [DecidableEq G] (m : ℕ)
    (μ : Law (Vertex (G × Fin m))) (g : G) :
    μ.expect (fun v => (count (fun j => v (g, j)) : ℝ)) =
      ∑ j, μ.expect (fun v => vertexPoint v (g, j)) := by
  simp_rw [← sum_binary]
  simp only [Law.expect, vertexPoint, Finset.mul_sum]
  exact Finset.sum_comm

theorem expect_group_count_of_mean {G : Type*} [Fintype G] [DecidableEq G] (m : ℕ)
    (μ : Law (Vertex (G × Fin m))) (p : G → ℝ)
    (hmean : ∀ g j, μ.expect (fun v => vertexPoint v (g, j)) = p g) (g : G) :
    μ.expect (fun v => (count (fun j => v (g, j)) : ℝ)) = m * p g := by
  rw [expect_group_count]
  simp_rw [hmean]
  simp

end
end CubicGap
