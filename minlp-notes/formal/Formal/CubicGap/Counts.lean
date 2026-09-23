import Mathlib

namespace CubicGap

open scoped BigOperators
noncomputable section


/-- Number of successful coordinates in a binary group. -/
def count {I : Type*} [Fintype I] (v : I → Bool) : ℕ :=
  (Finset.univ.filter fun i => v i = true).card

/-- The elementary symmetric polynomial, with each distinct support counted once. -/
def elementary {I : Type*} [Fintype I] (d : ℕ) (x : I → ℝ) : ℝ :=
  ∑ s ∈ Finset.univ.powersetCard d, ∏ i ∈ s, x i

/-- Evaluating an elementary polynomial at a constant vector. -/
theorem elementary_const {I : Type*} [Fintype I] (d : ℕ) (r : ℝ) :
    elementary d (fun _ : I => r) = ((Fintype.card I).choose d : ℝ) * r ^ d := by
  classical
  unfold elementary
  calc
    _ = ∑ _s ∈ Finset.univ.powersetCard d, r ^ d := by
      apply Finset.sum_congr rfl
      intro s hs
      simp [(Finset.mem_powersetCard.mp hs).2]
    _ = _ := by simp [Finset.card_powersetCard]

theorem count_le {I : Type*} [Fintype I] (v : I → Bool) :
    count v ≤ Fintype.card I := Finset.card_filter_le _ _

theorem sum_binary {I : Type*} [Fintype I] (v : I → Bool) :
    (∑ i, (if v i = true then (1 : ℝ) else 0)) = count v := by
  exact Finset.sum_boole _ _

theorem elementary_binary {I : Type*} [Fintype I] (d : ℕ) (v : I → Bool) :
    elementary d (fun i => if v i = true then 1 else 0) =
      ((count v).choose d : ℝ) := by
  classical
  let S := Finset.univ.filter fun i => v i = true
  have hprod (s : Finset I) :
      (∏ i ∈ s, (if v i = true then (1 : ℝ) else 0)) =
        if s ⊆ S then 1 else 0 := by
    split_ifs with hs
    · apply Finset.prod_eq_one
      intro i hi
      have := Finset.mem_filter.mp (hs hi)
      simp [this.2]
    · have hex : ∃ i ∈ s, v i ≠ true := by
        by_contra! hh
        exact hs (by intro i hi; exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, hh i hi⟩)
      obtain ⟨i, hi, hv⟩ := hex
      exact Finset.prod_eq_zero hi (by simp [hv])
  unfold elementary
  simp_rw [hprod]
  rw [Finset.sum_boole]
  have hfilter : (Finset.univ.powersetCard d).filter (fun s => s ⊆ S) =
      S.powersetCard d := by
    ext s
    simp only [Finset.mem_filter, Finset.mem_powersetCard]
    simp [and_comm]
  rw [hfilter, Finset.card_powersetCard]
  rfl

/-- A prefixVertex containing exactly `k` successes. -/
def prefixVertex (m k : ℕ) (i : Fin m) : Bool := decide (i.val < k)

theorem count_prefixVertex (m k : ℕ) (hk : k ≤ m) : count (prefixVertex m k) = k := by
  classical
  unfold count prefixVertex
  simp only [decide_eq_true_eq]
  have hcard : (Finset.univ.filter (fun i : Fin m => i.val < k)).card =
      (Finset.range k).card := by
    apply Finset.card_bij (fun i _ => i.val)
    · intro i hi
      simpa using (Finset.mem_filter.mp hi).2
    · intro i _ j _ hij
      exact Fin.ext hij
    · intro j hj
      refine ⟨⟨j, lt_of_lt_of_le (Finset.mem_range.mp hj) hk⟩, ?_, rfl⟩
      simpa using hj
  simpa using hcard

/-- Rotate one fixed-count binary vector. A common rotation works for every group. -/
def rotate {m : ℕ} [NeZero m] (v : Fin m → Bool) (s : Fin m) : Fin m → Bool :=
  fun i => v (i + s)

theorem count_rotate {m : ℕ} [NeZero m] (v : Fin m → Bool) (s : Fin m) :
    count (rotate v s) = count v := by
  have h := Equiv.sum_comp (Equiv.addRight s) (fun i => if v i = true then (1 : ℝ) else 0)
  have h' : (count (rotate v s) : ℝ) = count v := by
    rw [← sum_binary, ← sum_binary]
    exact h
  exact_mod_cast h'

theorem sum_rotate {m : ℕ} [NeZero m] (v : Fin m → Bool) (i : Fin m) :
    (∑ s, (if rotate v s i = true then (1 : ℝ) else 0)) = count v := by
  rw [← sum_binary]
  exact Equiv.sum_comp (Equiv.addLeft i) (fun j => if v j = true then (1 : ℝ) else 0)

end
end CubicGap
