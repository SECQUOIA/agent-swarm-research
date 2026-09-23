import Formal.CubicGap.Termwise

namespace CubicGap

noncomputable section

variable {I : Type*}

/-- Put all support coordinates at one simultaneously, with the remaining atom
adjusted to preserve every original mean. -/
def upperMonomialPoint [DecidableEq I] (s : Finset I) (x : I → ℝ) (a : ℝ)
    (t : Bool) : I → ℝ :=
  fun j => if j ∈ s then (if t then 1 else (x j-a)/(1-a)) else x j

def upperMonomialLaw (a : ℝ) (ha : 0 ≤ a) (ha1 : a ≤ 1) : Law Bool where
  weight t := if t then a else 1-a
  nonneg t := by cases t <;> simp <;> linarith
  mass_one := by simp

/-- The upper envelope of a nonempty monomial is its smallest coordinate mean. -/
theorem monomial_maximum_of_min_coordinate [Finite I] (s : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) (i : I) (hi : i ∈ s) (hmin : ∀ j ∈ s, x i ≤ x j) :
    IsGreatest (envelopeValues (monomial s) x) (x i) := by
  classical
  let := Fintype.ofFinite I
  have hupper : ∀ z ∈ envelopeValues (monomial s) x, z ≤ x i := by
    intro z hz
    obtain ⟨ν, hmean, hobj⟩ := (mem_cubeGraph_hull_iff (monomial s)
      (monomial_coordinate_affine s) x z).mp hz
    rw [← hobj, ← hmean i]
    exact ν.expect_mono fun v => monomial_le_coordinate s
      (by intro j _; simp only [vertexPoint]; split <;> norm_num) hi
  refine ⟨?_, hupper⟩
  by_cases ha : x i = 1
  · have hprod : monomial s x = 1 := by
      apply Finset.prod_eq_one
      intro j hj
      have := hmin j hj
      have := (hx j).2
      linarith
    have hm : (x, monomial s x) ∈ convexHull ℝ (cubeGraph (monomial s)) :=
      subset_convexHull ℝ _ ⟨hx, rfl⟩
    simpa only [envelopeValues, Set.mem_ofPred_eq, hprod, ha] using hm
  · have halt : x i < 1 := lt_of_le_of_ne (hx i).2 ha
    have hden : 0 < 1-x i := by linarith
    have hden0 : 1-x i ≠ 0 := ne_of_gt hden
    let μ := upperMonomialLaw (x i) (hx i).1 (hx i).2
    let y := upperMonomialPoint s x (x i)
    have hy (t : Bool) : y t ∈ cube I := by
      intro j
      by_cases hj : j ∈ s
      · cases t with
        | false =>
          simp only [y, upperMonomialPoint, if_pos hj, Bool.false_eq_true, if_false]
          refine ⟨div_nonneg (sub_nonneg.mpr (hmin j hj)) hden.le, ?_⟩
          apply (div_le_one hden).mpr
          linarith [(hx j).2]
        | true => simp [y, upperMonomialPoint, hj]
      · simpa [y, upperMonomialPoint, hj] using hx j
    have hmean (j : I) : μ.expect (fun t => y t j) = x j := by
      by_cases hj : j ∈ s
      · simp [μ, Law.expect, upperMonomialLaw, y, upperMonomialPoint, hj]
        field_simp
        ring
      · simp [μ, Law.expect, upperMonomialLaw, y, upperMonomialPoint, hj]
        ring
    have hzero : monomial s (y false) = 0 := by
      apply Finset.prod_eq_zero hi
      simp [y, upperMonomialPoint, hi]
    have hone : monomial s (y true) = 1 := by
      apply Finset.prod_eq_one
      intro j hj
      simp [y, upperMonomialPoint, hj]
    apply cube_law_attainment μ (monomial s) y x (x i) hy hmean
    simp [μ, Law.expect, upperMonomialLaw, hzero, hone]

end
end CubicGap
