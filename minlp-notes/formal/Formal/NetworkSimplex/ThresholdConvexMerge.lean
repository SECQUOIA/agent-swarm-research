import Mathlib

/-! Merging nonnegative weighted copies of an arbitrary nonempty convex set. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators Pointwise

variable {I V : Type*} [Fintype I] [AddCommGroup V] [Module ℝ V]

/-- Finite weighted sums with one independently selected point from each copy. -/
def weightedCopies (C : Set V) (w : I → ℝ) : Set V :=
  {z | ∃ x : I → V, (∀ i, x i ∈ C) ∧ z = ∑ i, w i • x i}

/-- Independent choices from nonnegative weighted copies of a convex set merge
exactly into a single copy scaled by the total weight. Empty families and total
weight zero are included; nonemptiness supplies a representative at zero. -/
theorem weightedCopies_eq_smul (C : Set V) (hC : Convex ℝ C) (hne : C.Nonempty)
    (w : I → ℝ) (hw : ∀ i, 0 ≤ w i) :
    weightedCopies C w = (∑ i, w i) • C := by
  classical
  ext z
  constructor
  · rintro ⟨x, hx, rfl⟩
    by_cases hz : (∑ i, w i) = 0
    · obtain ⟨y, hy⟩ := hne
      have hwz : ∀ i, w i = 0 := fun i =>
        (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => hw j)).mp hz i (Finset.mem_univ i)
      exact Set.mem_smul_set.mpr ⟨y, hy, by simp [hwz]⟩
    · have ht : 0 < ∑ i, w i := lt_of_le_of_ne
        (Finset.sum_nonneg (fun i _ => hw i)) (Ne.symm hz)
      let y : V := ∑ i, (w i / ∑ j, w j) • x i
      have hy : y ∈ C := hC.sum_mem
        (fun i _ => div_nonneg (hw i) ht.le)
        (by rw [← Finset.sum_div, div_self hz]) (fun i _ => hx i)
      refine Set.mem_smul_set.mpr ⟨y, hy, ?_⟩
      simp only [y, Finset.smul_sum, smul_smul]
      apply Finset.sum_congr rfl
      intro i _
      rw [mul_div_cancel₀ _ hz]
  · intro hz
    obtain ⟨x, hx, rfl⟩ := Set.mem_smul_set.mp hz
    exact ⟨fun _ => x, fun _ => hx, by rw [Finset.sum_smul]⟩

/-- Literal Minkowski-sum form of the convex weighted-copy identity. -/
theorem convex_sum_smul_eq (C : Set V) (hC : Convex ℝ C) (hne : C.Nonempty)
    (w : I → ℝ) (hw : ∀ i, 0 ≤ w i) :
    (∑ i, w i • C) = (∑ i, w i) • C := by
  classical
  rw [← weightedCopies_eq_smul C hC hne w hw]
  ext z
  rw [Set.mem_finsetSum]
  constructor
  · rintro ⟨g, hg, he⟩
    have hpoint : ∀ i, ∃ x ∈ C, w i • x = g i := fun i =>
      Set.mem_smul_set.mp (hg (Finset.mem_univ i))
    choose x hx hxe using hpoint
    refine ⟨x, hx, ?_⟩
    simpa only [hxe] using he.symm
  · rintro ⟨x, hx, he⟩
    exact ⟨fun i => w i • x i, fun {i} _ => Set.mem_smul_set.mpr ⟨x i, hx i, rfl⟩, he.symm⟩

/-- If the total weight vanishes, the weighted Minkowski sum is exactly `{0}`. -/
theorem convex_sum_smul_eq_zero (C : Set V) (hC : Convex ℝ C) (hne : C.Nonempty)
    (w : I → ℝ) (hw : ∀ i, 0 ≤ w i) (hzero : ∑ i, w i = 0) :
    (∑ i, w i • C) = {0} := by
  rw [convex_sum_smul_eq C hC hne w hw, hzero, Set.zero_smul_set hne]
  rfl

end NetworkSimplex.Threshold
