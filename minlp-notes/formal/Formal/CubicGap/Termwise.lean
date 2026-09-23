import Formal.CubicGap.Envelope
import Formal.CubicGap.Polynomial

namespace CubicGap

noncomputable section

variable {I : Type*} [Fintype I] [DecidableEq I]

omit [Fintype I] [DecidableEq I] in
/-- A finite law of actual cube points supplies a point of the original graph hull. -/
theorem cube_law_attainment {α : Type*} [Fintype α]
    (μ : Law α) (f : (I → ℝ) → ℝ) (y : α → I → ℝ) (x : I → ℝ) (q : ℝ)
    (hy : ∀ a, y a ∈ cube I) (hmean : ∀ i, μ.expect (fun a => y a i) = x i)
    (hvalue : μ.expect (fun a => f (y a)) = q) : q ∈ envelopeValues f x := by
  have hbar : μ.barycenter (fun a => (y a, f (y a))) = (x, q) := by
    apply Prod.ext
    · ext i
      simpa [Law.barycenter, Law.expect, Prod.fst_sum, Finset.sum_apply] using hmean i
    · simpa [Law.barycenter, Law.expect, Prod.snd_sum] using hvalue
  have hmem := (Law.mem_convexHull_range_iff (fun a => (y a, f (y a))) (x, q)).mpr
    ⟨μ, hbar⟩
  exact convexHull_mono (by rintro _ ⟨a, rfl⟩; exact ⟨hy a, rfl⟩) hmem

theorem monomial_expect_nonneg (s : Finset I) (μ : Law (Vertex I)) :
    0 ≤ μ.expect (fun v => monomial s (vertexPoint v)) := by
  apply μ.expect_nonneg
  intro v
  apply monomial_nonneg
  intro i _
  simp only [vertexPoint]
  split <;> norm_num

theorem monomial_expect_lower (s : Finset I) (μ : Law (Vertex I)) (x : I → ℝ)
    (hmean : HasMeans μ x) :
    (∑ i ∈ s, x i) - (s.card - 1 : ℝ) ≤
      μ.expect (fun v => monomial s (vertexPoint v)) := by
  have h := μ.expect_mono (fun v => monomial_lower s (x := vertexPoint v)
    (by intro i _; simp only [vertexPoint]; split <;> norm_num))
  have hsum : μ.expect (fun v => ∑ i ∈ s, vertexPoint v i) = ∑ i ∈ s, x i := by
    simp only [Law.expect, Finset.mul_sum]
    rw [Finset.sum_comm]
    exact Finset.sum_congr rfl (fun i _ => hmean i)
  simpa only [Law.expect_sub, Law.expect_const, hsum] using h

/-- Mix the mutually exclusive success patterns of two selected coordinates. -/
def pairLaw (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) (hab : a + b ≤ 1) : Law (Fin 3) where
  weight := ![a, b, 1-a-b]
  nonneg t := by fin_cases t <;> simp <;> linarith
  mass_one := by simp [Fin.sum_univ_succ]

def pairPoint (x : I → ℝ) (i j : I) (t : Fin 3) : I → ℝ :=
  Function.update (Function.update x i (if t = 0 then 1 else 0)) j
    (if t = 1 then 1 else 0)

omit [Fintype I] [DecidableEq I] in
/-- If two factors have total mean at most one, the exact monomial lower envelope is zero. -/
theorem monomial_minimum_zero_of_pair [Finite I] (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I)
    (i j : I) (hij : i ≠ j) (hi : i ∈ s) (hj : j ∈ s)
    (hab : x i + x j ≤ 1) : IsLeast (envelopeValues (monomial s) x) 0 := by
  classical
  let := Fintype.ofFinite I
  let μ := pairLaw (x i) (x j) (hx i).1 (hx j).1 hab
  have hy (t : Fin 3) : pairPoint x i j t ∈ cube I := by
    intro l
    by_cases hlj : l = j
    · subst l
      simp only [pairPoint, Function.update_self]
      split <;> norm_num
    · by_cases hli : l = i
      · subst l
        simp only [pairPoint, Function.update_of_ne hlj, Function.update_self]
        split <;> norm_num
      · simpa [pairPoint, Function.update_of_ne hlj, Function.update_of_ne hli] using hx l
  have hmean (l : I) : μ.expect (fun t => pairPoint x i j t l) = x l := by
    by_cases hlj : l = j
    · subst l
      simp [μ, Law.expect, pairLaw, pairPoint]
    · by_cases hli : l = i
      · subst l
        simp [μ, Law.expect, pairLaw, pairPoint, hlj]
      · simp [μ, Law.expect, pairLaw, pairPoint, Fin.sum_univ_succ, hlj, hli]
        ring
  have hzero (t : Fin 3) : monomial s (pairPoint x i j t) = 0 := by
    unfold monomial
    by_cases ht : t = 0
    · apply Finset.prod_eq_zero hj
      simp [pairPoint, ht]
    · apply Finset.prod_eq_zero hi
      simp [pairPoint, hij, ht]
  have hattain := cube_law_attainment μ (monomial s) (pairPoint x i j) x 0 hy hmean
    (by simp_rw [hzero]; exact μ.expect_const 0)
  refine ⟨hattain, ?_⟩
  intro z hz
  obtain ⟨ν, _, hobj⟩ := (mem_cubeGraph_hull_iff (monomial s)
    (monomial_coordinate_affine s) x z).mp hz
  rw [← hobj]
  exact monomial_expect_nonneg s ν

/-- The three single-failure patterns and the all-success pattern. -/
def tripleLaw (a b c : ℝ) (ha : a ≤ 1) (hb : b ≤ 1) (hc : c ≤ 1)
    (hsum : 2 ≤ a + b + c) : Law (Fin 4) where
  weight := ![1-a, 1-b, 1-c, a+b+c-2]
  nonneg t := by fin_cases t <;> simp <;> linarith
  mass_one := by simp [Fin.sum_univ_succ]; ring

def triplePoint (x : I → ℝ) (i j k : I) (t : Fin 4) : I → ℝ :=
  Function.update
    (Function.update (Function.update x i (if t = 0 then 0 else 1)) j
      (if t = 1 then 0 else 1)) k (if t = 2 then 0 else 1)

omit [Fintype I] in
/-- The exact lower envelope of three distinct factors when their means sum to at least two. -/
theorem triple_monomial_minimum [Finite I] (x : I → ℝ) (hx : x ∈ cube I)
    (i j k : I) (hij : i ≠ j) (hik : i ≠ k) (hjk : j ≠ k)
    (hsum : 2 ≤ x i + x j + x k) :
    IsLeast (envelopeValues (monomial {i, j, k}) x) (x i + x j + x k - 2) := by
  let := Fintype.ofFinite I
  let μ := tripleLaw (x i) (x j) (x k) (hx i).2 (hx j).2 (hx k).2 hsum
  have hy (t : Fin 4) : triplePoint x i j k t ∈ cube I := by
    intro l
    by_cases hlk : l = k
    · subst l
      simp only [triplePoint, Function.update_self]
      split <;> norm_num
    · by_cases hlj : l = j
      · subst l
        simp only [triplePoint, Function.update_of_ne hlk, Function.update_self]
        split <;> norm_num
      · by_cases hli : l = i
        · subst l
          simp only [triplePoint, Function.update_of_ne hlk, Function.update_of_ne hlj,
            Function.update_self]
          split <;> norm_num
        · simpa [triplePoint, Function.update_of_ne hlk, Function.update_of_ne hlj,
            Function.update_of_ne hli] using hx l
  have hmean (l : I) : μ.expect (fun t => triplePoint x i j k t l) = x l := by
    by_cases hlk : l = k
    · subst l
      simp [μ, Law.expect, tripleLaw, triplePoint, Fin.sum_univ_succ]
      ring
    · by_cases hlj : l = j
      · subst l
        simp [μ, Law.expect, tripleLaw, triplePoint, Fin.sum_univ_succ, hlk]
        ring
      · by_cases hli : l = i
        · subst l
          simp [μ, Law.expect, tripleLaw, triplePoint, Fin.sum_univ_succ, hlk, hlj]
          ring
        · simp [μ, Law.expect, tripleLaw, triplePoint, Fin.sum_univ_succ, hlk, hlj, hli]
          ring
  have hvalue : μ.expect (fun t => monomial {i,j,k} (triplePoint x i j k t)) =
      x i + x j + x k - 2 := by
    simp [μ, Law.expect, tripleLaw, triplePoint, monomial, Fin.sum_univ_succ,
      hij, hik, hjk]
  have hattain := cube_law_attainment μ (monomial {i,j,k}) (triplePoint x i j k) x
    (x i + x j + x k - 2) hy hmean hvalue
  refine ⟨hattain, ?_⟩
  intro z hz
  obtain ⟨ν, hν, hobj⟩ := (mem_cubeGraph_hull_iff (monomial {i,j,k})
    (monomial_coordinate_affine {i,j,k}) x z).mp hz
  rw [← hobj]
  have h := monomial_expect_lower {i,j,k} ν x hν
  norm_num [hij, hik, hjk, add_assoc] at h ⊢
  exact h

end
end CubicGap
