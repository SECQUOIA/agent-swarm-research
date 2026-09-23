import Formal.ReciprocalAnchor.Model

/-! Finite probability representations of the original reciprocal graph hull. -/

namespace ReciprocalAnchor

theorem finite_representation_mem_hull {ι : Type*} [Fintype ι]
    {a b m t q w : ℝ} (p x y : ι → ℝ)
    (hp : ∀ i, 0 ≤ p i) (hp1 : ∑ i, p i = 1)
    (hx : ∀ i, a ≤ x i ∧ x i ≤ b) (hy : ∀ i, 0 ≤ y i ∧ y i ≤ 1)
    (hm : ∑ i, p i * x i = m) (ht : ∑ i, p i / x i = t)
    (hq : ∑ i, p i * y i = q) (hw : ∑ i, p i * (x i * y i) = w) :
    point m t q w ∈ hull a b := by
  apply mem_convexHull_of_exists_fintype p (fun i => point (x i) (1 / x i) (y i) (x i * y i))
    hp hp1
  · intro i
    exact ⟨x i, y i, (hx i).1, (hx i).2, (hy i).1, (hy i).2, rfl⟩
  · ext j
    fin_cases j <;> simp [point, Finset.sum_apply, smul_eq_mul, ← div_eq_mul_inv, hm, ht, hq, hw]

theorem mem_hull_has_finite_representation {a b m t q w : ℝ}
    (h : point m t q w ∈ hull a b) :
    ∃ (ι : Type) (_ : Fintype ι) (p x y : ι → ℝ),
      (∀ i, 0 ≤ p i) ∧ (∑ i, p i = 1) ∧
      (∀ i, a ≤ x i ∧ x i ≤ b) ∧ (∀ i, 0 ≤ y i ∧ y i ≤ 1) ∧
      (∑ i, p i * x i = m) ∧ (∑ i, p i / x i = t) ∧
      (∑ i, p i * y i = q) ∧ (∑ i, p i * (x i * y i) = w) := by
  classical
  obtain ⟨ι, hι, p, z, hp, hp1, hz, hsum⟩ := mem_convexHull_iff_exists_fintype.mp h
  have hi : ∀ i, ∃ x y : ℝ, a ≤ x ∧ x ≤ b ∧ 0 ≤ y ∧ y ≤ 1 ∧
      z i = point x (1 / x) y (x * y) := hz
  choose x y hx hx' hy hy' heq using hi
  refine ⟨ι, hι, p, x, y, hp, hp1, fun i => ⟨hx i, hx' i⟩,
    fun i => ⟨hy i, hy' i⟩, ?_, ?_, ?_, ?_⟩
  · have := congrFun hsum 0
    simpa [heq, point, Finset.sum_apply, smul_eq_mul] using this
  · have := congrFun hsum 1
    simpa [heq, point, Finset.sum_apply, smul_eq_mul, div_eq_mul_inv] using this
  · have := congrFun hsum 2
    simpa [heq, point, Finset.sum_apply, smul_eq_mul] using this
  · have := congrFun hsum 3
    simpa [heq, point, Finset.sum_apply, smul_eq_mul] using this

end ReciprocalAnchor
