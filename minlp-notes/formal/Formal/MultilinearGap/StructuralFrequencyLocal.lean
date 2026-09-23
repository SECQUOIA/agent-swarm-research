import Formal.MultilinearGap.StructuralCardinalityUpper

/-! Exact cardinality-factor endpoints at a point with two half coordinates. -/
namespace MultilinearGap
open CubicGap
noncomputable section
variable {I : Type*} [Fintype I] [DecidableEq I]

/-- An integral coordinate is fixed on every state with nonzero probability. -/
theorem law_integral_coordinate (μ : Law (Vertex I)) {x : I → ℝ}
    (hm : HasMeans μ x) {v : Vertex I} (hw : μ.weight v ≠ 0) {i : I}
    (hi : x i = 0 ∨ x i = 1) : vertexPoint v i = x i := by
  rcases hi with hi | hi
  · have hz : ∑ w, μ.weight w * vertexPoint w i = 0 := (hm i).trans hi
    have hp (w : Vertex I) : 0 ≤ μ.weight w * vertexPoint w i := by
      apply mul_nonneg (μ.nonneg w)
      simp only [vertexPoint]
      split <;> norm_num
    have hv := (Finset.sum_eq_zero_iff_of_nonneg (fun w _ => hp w)).mp hz v
      (Finset.mem_univ v)
    exact ((mul_eq_zero.mp hv).resolve_left hw).trans hi.symm
  · have hz : μ.expect (fun w => 1 - vertexPoint w i) = 0 := by
      rw [Law.expect_sub, Law.expect_const, hm i, hi]
      ring
    have hp (w : Vertex I) : 0 ≤ μ.weight w * (1 - vertexPoint w i) := by
      apply mul_nonneg (μ.nonneg w)
      simp only [vertexPoint]
      split <;> norm_num
    have hv := (Finset.sum_eq_zero_iff_of_nonneg (fun w _ => hp w)).mp hz v
      (Finset.mem_univ v)
    have he := (mul_eq_zero.mp hv).resolve_left hw
    rw [hi]
    linarith

/-- The deterministic number of ones on an integral support. -/
def integralOnes (s : Finset I) (x : I → ℝ) : ℕ := (s.filter fun i => x i = 1).card

/-- On an integral support every feasible nonzero-weight state has the fixed count. -/
theorem countOn_integral (s : Finset I) (x : I → ℝ)
    (hx : ∀ i ∈ s, x i = 0 ∨ x i = 1) (μ : Law (Vertex I))
    (hm : HasMeans μ x) {v : Vertex I} (hw : μ.weight v ≠ 0) :
    countOn s v = integralOnes s x := by
  unfold countOn integralOnes
  congr 1
  ext i
  simp only [Finset.mem_filter]
  constructor
  · rintro ⟨hi, hv⟩
    have he := law_integral_coordinate μ hm hw (hx i hi)
    exact ⟨hi, by simpa [vertexPoint, hv] using he.symm⟩
  · rintro ⟨hi, hx1⟩
    have he := law_integral_coordinate μ hm hw (hx i hi)
    refine ⟨hi, ?_⟩
    cases hv : v i <;> simp_all [vertexPoint]

omit [DecidableEq I] [Fintype I] in
/-- Sum of the means on an integral support. -/
theorem meanSum_integral (s : Finset I) (x : I → ℝ)
    (hx : ∀ i ∈ s, x i = 0 ∨ x i = 1) :
    meanSum s x = integralOnes s x := by
  classical
  rw [meanSum, integralOnes, ← Finset.sum_boole]
  apply Finset.sum_congr rfl
  intro i hi
  rcases hx i hi with h | h <;> simp [h]

/-- Removing the two half coordinates leaves the integral part of the support. -/
def halfIntegralRest (s : Finset I) (i j : I) : Finset I := (s.erase i).erase j

omit [Fintype I] in
/-- The mean count is the integral count plus one. -/
theorem meanSum_two_halves (s : Finset I) (x : I → ℝ) (i j : I)
    (hi : i ∈ s) (hj : j ∈ s) (hij : i ≠ j)
    (hxi : x i = 1 / 2) (hxj : x j = 1 / 2)
    (hrest : ∀ a ∈ halfIntegralRest s i j, x a = 0 ∨ x a = 1) :
    meanSum s x = (integralOnes (halfIntegralRest s i j) x : ℝ) + 1 := by
  classical
  have hj' : j ∈ s.erase i := Finset.mem_erase.mpr ⟨Ne.symm hij, hj⟩
  have he₁ := Finset.sum_erase_add s x hi
  have he₂ := Finset.sum_erase_add (s.erase i) x hj'
  have he₃ := meanSum_integral (halfIntegralRest s i j) x hrest
  dsimp [meanSum, halfIntegralRest] at *
  rw [hxi] at he₁
  rw [hxj] at he₂
  linarith

omit [Fintype I] in
/-- The lower count-table interpolation collapses to the integer mean. -/
theorem cardinalityLower_two_halves (φ : ℕ → ℝ) (s : Finset I) (x : I → ℝ)
    (i j : I) (hi : i ∈ s) (hj : j ∈ s) (hij : i ≠ j)
    (hxi : x i = 1 / 2) (hxj : x j = 1 / 2)
    (hrest : ∀ a ∈ halfIntegralRest s i j, x a = 0 ∨ x a = 1) :
    cardinalityLower φ s x = φ (integralOnes (halfIntegralRest s i j) x + 1) := by
  classical
  have hs := meanSum_two_halves s x i j hi hj hij hxi hxj hrest
  have hf : countFloor s x = integralOnes (halfIntegralRest s i j) x + 1 := by
    unfold countFloor
    rw [hs, ← Nat.cast_add_one]
    exact Nat.floor_natCast _
  simp [cardinalityLower, countFrac, hf, hs]


omit [DecidableEq I] [Fintype I] in
/-- At integral means the lower endpoint is the fixed support count. -/
theorem cardinalityLower_integral (φ : ℕ → ℝ) (s : Finset I) (x : I → ℝ)
    (hx : ∀ i ∈ s, x i = 0 ∨ x i = 1) :
    cardinalityLower φ s x = φ (integralOnes s x) := by
  classical
  have hm := meanSum_integral s x hx
  have hf : countFloor s x = integralOnes s x := by
    unfold countFloor
    rw [hm]
    exact Nat.floor_natCast _
  simp [cardinalityLower, countFrac, hm, hf]

/-- The threshold upper value at two half coordinates is the average of the
endpoint counts. Coordinates outside the support can be arbitrary. -/
theorem thresholdLaw_cardinality_two_halves (φ : ℕ → ℝ) (s : Finset I)
    (x : I → ℝ) (hx : x ∈ cube I) (i j : I)
    (hi : i ∈ s) (hj : j ∈ s) (hij : i ≠ j)
    (hxi : x i = 1 / 2) (hxj : x j = 1 / 2)
    (hrest : ∀ a ∈ halfIntegralRest s i j, x a = 0 ∨ x a = 1) :
    (thresholdLaw x).expect (fun v => φ (countOn s v)) =
      (φ (integralOnes (halfIntegralRest s i j) x) +
        φ (integralOnes (halfIntegralRest s i j) x + 2)) / 2 := by
  let k := integralOnes (halfIntegralRest s i j) x
  have hm := thresholdLaw_hasMeans x hx
  have hsame (v : Vertex I) (hw : (thresholdLaw x).weight v ≠ 0) : v i = v j := by
    have hforward (a b : I) (ha : x a = 1 / 2) (hb : x b = 1 / 2)
        (hv : v a = true) : v b = true := by
      exact thresholdLaw_support_of_min (s := {a,b}) (a := a) (by simp) x hx
        (fun t ht => by
          simp only [Finset.mem_insert, Finset.mem_singleton] at ht
          rcases ht with rfl | rfl <;> simp [ha, hb]) v hw hv b (by simp)
    cases hvi : v i <;> cases hvj : v j <;> try rfl
    · have := hforward j i hxj hxi hvj
      simp [hvi] at this
    · have := hforward i j hxi hxj hvi
      simp [hvj] at this
  have he : (thresholdLaw x).expect (fun v => φ (countOn s v)) =
      (thresholdLaw x).expect (fun v => φ k + vertexPoint v i * (φ (k+2) - φ k)) := by
    apply Finset.sum_congr rfl
    intro v _
    by_cases hw : (thresholdLaw x).weight v = 0
    · simp [hw]
    congr 1
    dsimp only
    have hr := countOn_integral (halfIntegralRest s i j) x hrest (thresholdLaw x) hm hw
    have hj' : j ∈ s.erase i := Finset.mem_erase.mpr ⟨hij.symm, hj⟩
    rw [countOn_erase_add hi, countOn_erase_add hj']
    change φ (countOn (halfIntegralRest s i j) v + _ + _) = _
    rw [hr, hsame v hw]
    cases hvj : v j <;> simp [vertexPoint, hsame v hw, hvj, k, Nat.add_assoc]
  rw [he, Law.expect_add, Law.expect_const, Law.expect_mul_const, hm i, hxi]
  dsimp [k]
  ring

end
end MultilinearGap
