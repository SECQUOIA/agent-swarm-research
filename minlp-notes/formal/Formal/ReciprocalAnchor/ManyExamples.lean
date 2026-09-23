import Formal.ReciprocalAnchor.ManyGeometry
import Formal.ReciprocalAnchor.ManyIntegrals
import Formal.ReciprocalAnchor.Joint

/-! Exact three-atom optimum for the two-leaf obstruction. -/
namespace ReciprocalAnchor.ManyLeaf

noncomputable section

def exampleQ : Fin 2 → ℝ := ![2 / 3, 14 / 29]
def exampleW : Fin 2 → ℝ := ![5 / 3, 40 / 29]

def exampleLaw : Law 1 3 where
  size := 3
  mass := ![1 / 3, 16 / 87, 14 / 29]
  location := ![1, 25 / 16, 20 / 7]
  nonneg := by intro i; fin_cases i <;> norm_num
  total := by norm_num [Fin.sum_univ_succ]
  bounds := by intro i; fin_cases i <;> norm_num

theorem example_mean : exampleLaw.mean = 2 := by
  change (∑ i : Fin 3, ![(1 / 3 : ℝ), 16 / 87, 14 / 29] i *
    ![1, 25 / 16, 20 / 7] i) = 2
  norm_num [Fin.sum_univ_succ]

theorem example_reciprocal : exampleLaw.reciprocal = 31 / 50 := by
  change (∑ i : Fin 3, ![(1 / 3 : ℝ), 16 / 87, 14 / 29] i /
    ![1, 25 / 16, 20 / 7] i) = 31 / 50
  norm_num [Fin.sum_univ_succ]

theorem example_call_formula (s : ℝ) : exampleLaw.call s =
    (1 / 3 : ℝ) * max (1 - s) 0 + (16 / 87) * max (25 / 16 - s) 0 +
      (14 / 29) * max (20 / 7 - s) 0 := by
  change (∑ i : Fin 3, ![(1 / 3 : ℝ), 16 / 87, 14 / 29] i *
    max (![1, 25 / 16, 20 / 7] i - s) 0) = _
  simp [Fin.sum_univ_succ]
  ring

theorem example_call_eq_envelope (s : ℝ) : exampleLaw.call s = envelope 2 exampleQ exampleW s := by
  have hu (i : Fin 6) : line 2 exampleQ exampleW i s ≤ envelope 2 exampleQ exampleW s :=
    line_le_envelope 2 exampleQ exampleW i s
  by_cases h₁ : s ≤ 1
  · have hc : exampleLaw.call s = 2 - s := by
      rw [example_call_formula, max_eq_left (by linarith),
        max_eq_left (by linarith), max_eq_left (by linarith)]
      ring
    rw [hc]
    apply le_antisymm
    · exact mean_sub_le_envelope _ _ _ _
    · apply envelope_le
      intro i
      fin_cases i <;> norm_num [line, exampleQ, exampleW] <;> linarith
  · by_cases h₂ : s ≤ 25 / 16
    · have hc : exampleLaw.call s = 5 / 3 - (2 / 3) * s := by
        rw [example_call_formula, max_eq_right (by linarith),
          max_eq_left (by linarith), max_eq_left (by linarith)]
        ring
      rw [hc]
      apply le_antisymm
      · simpa [line, exampleQ, exampleW] using hu 0
      · apply envelope_le
        intro i
        fin_cases i <;> norm_num [line, exampleQ, exampleW] <;> linarith
    · by_cases h₃ : s ≤ 20 / 7
      · have hc : exampleLaw.call s = 40 / 29 - (14 / 29) * s := by
          rw [example_call_formula, max_eq_right (by linarith),
            max_eq_right (by linarith), max_eq_left (by linarith)]
          ring
        rw [hc]
        apply le_antisymm
        · simpa [line, exampleQ, exampleW] using hu 1
        · apply envelope_le
          intro i
          fin_cases i <;> norm_num [line, exampleQ, exampleW] <;> linarith
      · have hc : exampleLaw.call s = 0 := by
          rw [example_call_formula, max_eq_right (by linarith),
            max_eq_right (by linarith), max_eq_right (by linarith)]
          ring
        rw [hc]
        apply le_antisymm
        · exact envelope_nonneg _ _ _ _
        · apply envelope_le
          intro i
          fin_cases i <;> norm_num [line, exampleQ, exampleW] <;> linarith

/-- Deterministic leaves on the common three-atom law. -/
def exampleLeaves : Fin 3 → Fin 2 → ℝ := ![![0, 0], ![1, 0], ![1, 1]]

theorem example_leaf_bounds (i : Fin 3) (j : Fin 2) :
    0 ≤ exampleLeaves i j ∧ exampleLeaves i j ≤ 1 := by
  fin_cases i <;> fin_cases j <;> norm_num [exampleLeaves]

theorem example_leaf_mass (j : Fin 2) :
    (∑ i, exampleLaw.mass i * exampleLeaves i j) = exampleQ j := by
  change (∑ i : Fin 3, ![(1 / 3 : ℝ), 16 / 87, 14 / 29] i * exampleLeaves i j) = _
  fin_cases j <;> norm_num [exampleLeaves, exampleQ, Fin.sum_univ_succ]

theorem example_leaf_moment (j : Fin 2) :
    (∑ i, exampleLaw.mass i * (exampleLaw.location i * exampleLeaves i j)) = exampleW j := by
  change (∑ i : Fin 3, ![(1 / 3 : ℝ), 16 / 87, 14 / 29] i *
    (![1, 25 / 16, 20 / 7] i * exampleLeaves i j)) = _
  fin_cases j <;> norm_num [exampleLeaves, exampleW, Fin.sum_univ_succ]

theorem example_optimum_in_hull : point 2 (31 / 50) exampleQ exampleW ∈ hull 2 1 3 := by
  exact finite_representation_mem_hull exampleLaw.mass exampleLaw.location exampleLeaves
    exampleLaw.nonneg exampleLaw.total exampleLaw.bounds example_leaf_bounds
    example_mean example_reciprocal example_leaf_mass example_leaf_moment

theorem example_lowerMoment : lowerMoment 1 3 2 exampleQ exampleW = 31 / 50 := by
  have h := exampleLaw.reciprocal_eq_call_integral (by norm_num) (by norm_num)
  simp only [example_call_eq_envelope, example_mean, example_reciprocal] at h
  exact h.symm

theorem example_candidate_gap : lowerMoment 1 3 2 exampleQ exampleW - 3 / 5 = 1 / 50 := by
  rw [example_lowerMoment]
  norm_num

/-- Equality in a weighted two-tangent bound forces every positive-mass atom
onto one of the two tangent locations. -/
theorem equality_deficit_support {ι : Type*} [Fintype ι] (p x y : ι → ℝ)
    (hp : ∀ i, 0 ≤ p i) (hx : ∀ i, 0 < x i)
    (hy : ∀ i, 0 ≤ y i ∧ y i ≤ 1) {u v : ℝ} (hu : 0 < u) (hv : 0 < v)
    (hz : (∑ i, p i * ((1 - y i) * tangentDeficit (x i) u +
      y i * tangentDeficit (x i) v)) = 0) (i : ι) (hpi : 0 < p i) :
    x i = u ∨ x i = v := by
  have hn (j : ι) (a : ℝ) (ha : 0 < a) : 0 ≤ tangentDeficit (x j) a := by
    unfold tangentDeficit
    exact div_nonneg (sq_nonneg _) (mul_nonneg (hx j).le (sq_nonneg a))
  have hterm := (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => mul_nonneg (hp j)
    (add_nonneg (mul_nonneg (by linarith [(hy j).2]) (hn j u hu))
      (mul_nonneg (hy j).1 (hn j v hv))))).mp hz i (Finset.mem_univ i)
  have hzero := (mul_eq_zero.mp hterm).resolve_left (ne_of_gt hpi)
  by_contra h
  push Not at h
  have hU : 0 < tangentDeficit (x i) u :=
    div_pos (sq_pos_of_ne_zero (sub_ne_zero.mpr h.1)) (mul_pos (hx i) (sq_pos_of_pos hu))
  have hV : 0 < tangentDeficit (x i) v :=
    div_pos (sq_pos_of_ne_zero (sub_ne_zero.mpr h.2)) (mul_pos (hx i) (sq_pos_of_pos hv))
  by_cases hy1 : y i = 1
  · simp only [hy1, sub_self, zero_mul, one_mul, zero_add] at hzero
    linarith
  · have hpositive := mul_pos (sub_pos.mpr (lt_of_le_of_ne (hy i).2 hy1)) hU
    have hnonneg := mul_nonneg (hy i).1 hV.le
    linarith

theorem first_equality_law_support {ι : Type*} [Fintype ι] (p x y : ι → ℝ)
    (hp : ∀ i, 0 ≤ p i) (hp1 : ∑ i, p i = 1) (hx : ∀ i, 0 < x i)
    (hy : ∀ i, 0 ≤ y i ∧ y i ≤ 1) (hm : ∑ i, p i * x i = 2)
    (ht : ∑ i, p i / x i = 3 / 5) (hq : ∑ i, p i * y i = 2 / 3)
    (hw : ∑ i, p i * (x i * y i) = 5 / 3) (i : ι) (hpi : 0 < p i) :
    x i = 1 ∨ x i = 5 / 2 := by
  apply equality_deficit_support p x y hp hx hy (by norm_num) (by norm_num) ?_ i hpi
  have he (j : ι) : p j * ((1 - y j) * tangentDeficit (x j) 1 +
      y j * tangentDeficit (x j) (5 / 2)) = p j / x j - 2 * p j + p j * x j +
        (6 / 5) * (p j * y j) - (21 / 25) * (p j * (x j * y j)) := by
    rw [← first_deficit_identity (ne_of_gt (hx j))]
    unfold g₁
    ring
  simp_rw [he]
  rw [Finset.sum_sub_distrib, Finset.sum_add_distrib, Finset.sum_add_distrib,
    Finset.sum_sub_distrib, ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.mul_sum,
    hp1, hm, ht, hq, hw]
  norm_num

theorem second_equality_law_support {ι : Type*} [Fintype ι] (p x y : ι → ℝ)
    (hp : ∀ i, 0 ≤ p i) (hp1 : ∑ i, p i = 1) (hx : ∀ i, 0 < x i)
    (hy : ∀ i, 0 ≤ y i ∧ y i ≤ 1) (hm : ∑ i, p i * x i = 2)
    (ht : ∑ i, p i / x i = 3 / 5) (hq : ∑ i, p i * y i = 14 / 29)
    (hw : ∑ i, p i * (x i * y i) = 40 / 29) (i : ι) (hpi : 0 < p i) :
    x i = 6 / 5 ∨ x i = 20 / 7 := by
  apply equality_deficit_support p x y hp hx hy (by norm_num) (by norm_num) ?_ i hpi
  have he (j : ι) : p j * ((1 - y j) * tangentDeficit (x j) (6 / 5) +
      y j * tangentDeficit (x j) (20 / 7)) = p j / x j - (5 / 3) * p j +
        (25 / 36) * (p j * x j) + (29 / 30) * (p j * y j) -
          (2059 / 3600) * (p j * (x j * y j)) := by
    rw [← second_deficit_identity (ne_of_gt (hx j))]
    unfold g₂
    ring
  simp_rw [he]
  rw [Finset.sum_sub_distrib, Finset.sum_add_distrib, Finset.sum_add_distrib,
    Finset.sum_sub_distrib, ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.mul_sum,
    ← Finset.mul_sum, hp1, hm, ht, hq, hw]
  norm_num

/-- The equality supports of the two separate one-leaf hulls are disjoint. -/
theorem equality_supports_disjoint (x : ℝ) :
    ¬ ((x = 1 ∨ x = 5 / 2) ∧ (x = 6 / 5 ∨ x = 20 / 7)) := by
  rintro ⟨h | h, h' | h'⟩ <;> norm_num [h] at h'

/-- The proposed reciprocal value cannot be realized on a common anchor law. -/
theorem example_candidate_not_hull : point 2 (3 / 5) exampleQ exampleW ∉ hull 2 1 3 := by
  intro h
  obtain ⟨ι, _, p, x, y, hp, hp1, hx, hy, hm, ht, hq, hw⟩ :=
    mem_hull_has_finite_representation h
  have hpos : 0 < ∑ i, p i := by rw [hp1]; norm_num
  obtain ⟨i, _, hpi⟩ := (Finset.sum_pos_iff_of_nonneg (fun i _ => hp i)).mp hpos
  have hxpos (j : ι) : 0 < x j := by linarith [(hx j).1]
  have hfirst := first_equality_law_support p x (fun i => y i 0) hp hp1 hxpos
    (fun i => hy i 0) hm ht (by simpa [exampleQ] using hq 0)
    (by simpa [exampleW] using hw 0) i hpi
  have hsecond := second_equality_law_support p x (fun i => y i 1) hp hp1 hxpos
    (fun i => hy i 1) hm ht (by simpa [exampleQ] using hq 1)
    (by simpa [exampleW] using hw 1) i hpi
  exact equality_supports_disjoint (x i) ⟨hfirst, hsecond⟩

/-- Both separate hulls accept the candidate that the common-law hull rejects. -/
theorem example_separate_hulls_inexact :
    ReciprocalAnchor.point 2 (3 / 5) (exampleQ 0) (exampleW 0) ∈
      ReciprocalAnchor.hull 1 3 ∧
    ReciprocalAnchor.point 2 (3 / 5) (exampleQ 1) (exampleW 1) ∈
      ReciprocalAnchor.hull 1 3 ∧
    point 2 (3 / 5) exampleQ exampleW ∉ hull 2 1 3 := by
  exact ⟨ReciprocalAnchor.first_leaf_in_hull, ReciprocalAnchor.second_leaf_in_hull,
    example_candidate_not_hull⟩

end
end ReciprocalAnchor.ManyLeaf
