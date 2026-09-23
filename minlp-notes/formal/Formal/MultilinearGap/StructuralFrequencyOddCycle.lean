import Formal.MultilinearGap.StructuralFrequencySlab

/-! Even fractional cycles admit a nonzero alternating perturbation and therefore
cannot occur at an extreme point of a degree slab. -/
namespace MultilinearGap.FrequencySlab
open Set
open scoped BigOperators
noncomputable section
variable {V E : Type*} [Finite V] [Fintype E]

/-- An indexed fractional cycle in an extreme degree-slab point has odd length.
The row and edge data describe the actual incidences of the cycle. -/
theorem extreme_indexed_cycle_odd {S : V → Finset E} {lo hi : V → ℤ}
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ)
    {n : ℕ} [NeZero n] (edge : Fin n → E) (row : Fin n → V)
    (hedge : Function.Injective edge)
    (hfrac : ∀ i, edge i ∈ fractional x)
    (hinc : ∀ i e, e ∈ S (row i) ∧ e ∈ fractional x ↔
      e = edge i ∨ e = edge (i - 1))
    (hout : ∀ v, (∀ i, row i ≠ v) → ∀ i, edge i ∉ S v) : Odd n := by
  classical
  let : Fintype V := Fintype.ofFinite V
  by_contra hn
  have heven : Even n := Nat.not_odd_iff_even.mp hn
  have hn2 : 2 ≤ n := by
    obtain ⟨k, hk⟩ := heven
    have hp := NeZero.pos n
    omega
  let sign : Fin n → ℝ := fun i => if i.val % 2 = 0 then 1 else -1
  have hsign (i : Fin n) : sign i + sign (i - 1) = 0 := by
    have hnmod := Nat.even_iff.mp heven
    by_cases hi : i = 0
    · subst i
      have hm : (n - 1) % 2 ≠ 0 := by omega
      simp [sign, Fin.val_neg, Nat.mod_eq_of_lt hn2, hm, show n ≠ 1 by omega]
    · have hival : i.val ≠ 0 := fun h => hi (Fin.ext h)
      rw [show sign i = if i.val % 2 = 0 then 1 else -1 from rfl,
        show sign (i - 1) = if (i - 1).val % 2 = 0 then 1 else -1 from rfl,
        Fin.val_sub_one_of_ne_zero hi]
      split_ifs <;> (try omega) <;> norm_num
  let d : E → ℝ := fun e => ∑ i : Fin n, if edge i = e then sign i else 0
  have hdval (i : Fin n) : d (edge i) = sign i := by
    dsimp [d]
    rw [Finset.sum_eq_single i]
    · simp
    · intro j _ hji
      exact if_neg (fun h => hji (hedge h))
    · simp
  have hdz (e : E) (he : ∀ i, edge i ≠ e) : d e = 0 := by
    apply Finset.sum_eq_zero
    intro i _
    exact if_neg (he i)
  have hdzero : d = 0 := by
    apply extreme_kernel_eq_zero hx
    · intro e he
      apply hdz
      intro i hi
      exact he (hi ▸ hfrac i)
    · intro v hv
      by_cases hvr : ∃ i, row i = v
      · obtain ⟨i, rfl⟩ := hvr
        have hi_ne : i ≠ i - 1 := by
          intro h
          have hone : (1 : Fin n) = 0 := sub_eq_self.mp h.symm
          have hv := congrArg Fin.val hone
          simp [Nat.mod_eq_of_lt hn2] at hv
        have hpair : S (row i) ∩ fractional x = {edge i, edge (i - 1)} := by
          ext e
          simpa only [Finset.mem_inter, Finset.mem_insert, Finset.mem_singleton] using hinc i e
        have hsum : degree S d (row i) = ∑ e ∈ S (row i) ∩ fractional x, d e := by
          symm
          apply Finset.sum_subset Finset.inter_subset_left
          intro e he hne
          apply hdz
          intro j hje
          exact hne (Finset.mem_inter.mpr ⟨he, hje ▸ hfrac j⟩)
        rw [hsum, hpair, Finset.sum_pair (fun h => hi_ne (hedge h)), hdval, hdval]
        exact hsign i
      · apply Finset.sum_eq_zero
        intro e he
        apply hdz
        intro i hie
        exact hout v (by simpa using hvr) i (hie ▸ he)
  have hzero := congrFun hdzero (edge 0)
  rw [hdval] at hzero
  norm_num [sign] at hzero

end
end MultilinearGap.FrequencySlab
