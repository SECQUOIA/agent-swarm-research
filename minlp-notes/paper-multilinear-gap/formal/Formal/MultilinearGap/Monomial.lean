import Formal.CubicGap.TermwiseUpper

namespace MultilinearGap

open CubicGap

noncomputable section

variable {I : Type*} [DecidableEq I]

/-- Mutually exclusive failures of the leaves, with the remaining mass on an
anchor failure, attain the zero lower envelope. -/
theorem monomial_minimum_zero_of_anchor [Finite I] (s : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) (a : I) (ha : a ∈ s) (δ : ℝ) (hδ : 0 ≤ δ)
    (hanchor : x a = (s.erase a).card * δ)
    (hleaves : ∀ i ∈ s.erase a, x i = 1 - δ)
    (hmass : (s.erase a).card * δ ≤ 1) :
    IsLeast (envelopeValues (monomial s) x) 0 := by
  classical
  let := Fintype.ofFinite I
  let L := {i // i ∈ s.erase a}
  let μ : Law (Option L) := {
    weight := fun t => match t with | none => 1 - (s.erase a).card * δ | some _ => δ
    nonneg := by intro t; cases t <;> dsimp <;> linarith
    mass_one := by simp [Fintype.sum_option, L] }
  let y : Option L → I → ℝ := fun t j =>
    if j ∈ s then match t with
      | none => if j = a then 0 else 1
      | some i => if j = i.val then 0 else 1
    else x j
  have hy (t : Option L) : y t ∈ cube I := by
    intro j
    by_cases hj : j ∈ s
    · cases t <;> simp only [y, if_pos hj] <;> split <;> norm_num
    · simpa [y, hj] using hx j
  have hmean (j : I) : μ.expect (fun t => y t j) = x j := by
    by_cases hj : j ∈ s
    · by_cases hja : j = a
      · subst j
        have hne (i : L) : a ≠ i.val := by
          exact Ne.symm (Finset.mem_erase.mp i.property).1
        simp [μ, Law.expect, Fintype.sum_option, y, ha, hne, L, hanchor]
      · have hjL : j ∈ s.erase a := Finset.mem_erase.mpr ⟨hja, hj⟩
        let jL : L := ⟨j, hjL⟩
        have heq (i : L) : j = i.val ↔ i = jL := by
          constructor
          · intro h; apply Subtype.ext; exact h.symm
          · intro h; subst i; rfl
        simp only [Law.expect, μ, Fintype.sum_option, y, if_pos hj, if_neg hja]
        simp_rw [heq, mul_ite, mul_zero, mul_one]
        have hite (i : L) : (if i = jL then (0 : ℝ) else δ) =
            δ - (if i = jL then δ else 0) := by split <;> simp_all
        simp_rw [hite]
        simp [Finset.sum_sub_distrib, L, hleaves j hjL]
    · have heq : (fun t => y t j) = fun _ => x j := by funext t; simp [y, hj]
      rw [heq, μ.expect_const]
  have hzero (t : Option L) : monomial s (y t) = 0 := by
    cases t with
    | none =>
      apply Finset.prod_eq_zero ha
      simp [y, ha]
    | some i =>
      have hi : i.val ∈ s := Finset.mem_of_mem_erase i.property
      apply Finset.prod_eq_zero hi
      simp [y, hi]
  refine ⟨cube_law_attainment μ (monomial s) y x 0 hy hmean ?_, ?_⟩
  · simp_rw [hzero]
    exact μ.expect_const 0
  · intro z hz
    obtain ⟨ν, _, hobj⟩ := (mem_cubeGraph_hull_iff (monomial s)
      (monomial_coordinate_affine s) x z).mp hz
    rw [← hobj]
    exact monomial_expect_nonneg s ν

end
end MultilinearGap
