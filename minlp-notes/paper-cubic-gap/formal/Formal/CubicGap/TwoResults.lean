import Formal.CubicGap.Envelope
import Formal.CubicGap.CountLaws
import Formal.CubicGap.Families

namespace CubicGap

noncomputable section

def twoMeans (m : ℕ) (i : Fin 2 × Fin m) : ℝ := ![1 / 2, 3 / 4] i.1

theorem two_law_lower (m : ℕ) (a c d q : ℚ)
    (hminor : ∀ A C : Fin (m + 1), a * (A : ℚ) + c * (C : ℚ) + d ≤
      twoValue m A C)
    (hq : a * ((m : ℚ)/2) + c * (3*(m : ℚ)/4) + d = q)
    (μ : Law (Vertex (Fin 2 × Fin m))) (hmean : HasMeans μ (twoMeans m)) :
    (q : ℝ) ≤ μ.expect (fun v => twoFamily m (vertexPoint v)) := by
  have hA := expect_group_count_of_mean m μ ![(1 / 2 : ℝ), 3 / 4]
    (fun g j => hmean (g,j)) 0
  have hC := expect_group_count_of_mean m μ ![(1 / 2 : ℝ), 3 / 4]
    (fun g j => hmean (g,j)) 1
  have hpoint (v : Vertex (Fin 2 × Fin m)) :
      (a : ℝ) * (count (fun i => v (0,i)) : ℝ) +
        (c : ℝ) * (count (fun i => v (1,i)) : ℝ) + d ≤
      twoFamily m (vertexPoint v) := by
    rw [show twoFamily m (vertexPoint v) = _ from twoFamily_binary m v]
    have hb (g : Fin 2) : count (fun i => v (g,i)) < m+1 :=
      Nat.lt_succ_of_le (by simpa using count_le (fun i => v (g,i)))
    exact_mod_cast hminor ⟨_, hb 0⟩ ⟨_, hb 1⟩
  have h := μ.expect_mono hpoint
  simp only [Law.expect_add, Law.expect_const_mul, Law.expect_const] at h
  rw [hA, hC] at h
  have hqr : (a : ℝ) * ((m : ℝ)/2) + (c : ℝ) * (3*(m : ℝ)/4) + d = q := by
    have hh := congrArg (fun r : ℚ => (r : ℝ)) hq
    push_cast at hh
    exact hh
  norm_num only [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons] at h
  convert h using 1; nlinarith [hqr]

theorem two_fixed_count_attains (m : ℕ) [NeZero m] (A C : Fin (m + 1))
    (hA : (A : ℝ) / m = 1 / 2) (hC : (C : ℝ) / m = 3 / 4) :
    ∃ μ : Law (Vertex (Fin 2 × Fin m)), HasMeans μ (twoMeans m) ∧
      μ.expect (fun v => twoFamily m (vertexPoint v)) = (twoValue m A C : ℝ) := by
  let ν : Law (Fin 1) := Law.point 0
  let k : Fin 1 → Fin 2 → ℕ := fun _ => ![A.val, C.val]
  have hk : ∀ i g, k i g ≤ m := by
    intro i g
    fin_cases g
    · exact Nat.le_of_lt_succ A.isLt
    · exact Nat.le_of_lt_succ C.isLt
  refine ⟨ν.liftCounts (m := m) k, ?_, ?_⟩
  · rintro ⟨g,j⟩
    rw [liftCounts_mean ν k hk]
    simp only [ν, Law.expect_point, twoMeans]
    fin_cases g
    · simpa [k] using hA
    · simpa [k] using hC
  · simp_rw [show ∀ v, twoFamily m (vertexPoint v) =
        (twoValue m (count fun i => v (0,i)) (count fun i => v (1,i)) : ℝ)
      from twoFamily_binary m]
    rw [liftCounts_value ν k hk (fun counts => (twoValue m (counts 0) (counts 1) : ℝ))]
    simp [ν, k]

theorem two_exact_from_certificate (m : ℕ) [NeZero m] (a c d q : ℚ)
    (hminor : ∀ A C : Fin (m + 1), a * (A : ℚ) + c * (C : ℚ) + d ≤
      twoValue m A C)
    (hq : a * ((m : ℚ)/2) + c * (3*(m : ℚ)/4) + d = q)
    (A C : Fin (m + 1)) (hA : (A : ℝ) / m = 1 / 2) (hC : (C : ℝ) / m = 3 / 4)
    (hvalue : twoValue m A C = q) :
    IsLeast (envelopeValues (twoFamily m) (twoMeans m)) (q : ℝ) := by
  apply minimum_from_laws _ (twoFamily_coordinate_affine m)
  · exact two_law_lower m a c d q hminor hq
  · obtain ⟨μ, hm, hv⟩ := two_fixed_count_attains m A C hA hC
    exact ⟨μ, hm, hv.trans (by rw [hvalue])⟩

/-- Exact lower envelope of the eight-variable member. -/
theorem two_minimum4 : IsLeast (envelopeValues (twoFamily 4) (twoMeans 4)) 11 := by
  apply two_exact_from_certificate 4 9 4 (-19) 11
    (by intro A C; simpa using two_minorant4 A C) (by norm_num) 2 3
    (by norm_num) (by norm_num)
  exact two_arithmetic4.1

/-- Exact lower envelope of the sixteen-variable member. -/
theorem two_minimum8 : IsLeast (envelopeValues (twoFamily 8) (twoMeans 8)) 120 := by
  apply two_exact_from_certificate 8 47 20 (-188) 120
    (by intro A C; simpa using two_minorant8 A C) (by norm_num) 4 6
    (by norm_num) (by norm_num)
  exact two_arithmetic8.1

/-- Exact lower envelope of the twenty-four-variable member. -/
theorem two_minimum12 : IsLeast (envelopeValues (twoFamily 12) (twoMeans 12)) 441 := by
  apply two_exact_from_certificate 12 (231/2) 48 (-684) 441
    (by intro A C; simpa using two_minorant12 A C) (by norm_num) 6 9
    (by norm_num) (by norm_num)
  exact two_arithmetic12.1

/-- Exact lower envelope used in the explicit factor-two counterexample. -/
theorem two_minimum16 : IsLeast (envelopeValues (twoFamily 16) (twoMeans 16)) 1088 := by
  apply two_exact_from_certificate 16 214 (177/2) (-1686) 1088
    (by intro A C; simpa using two_minorant16 A C) (by norm_num) 8 12
    (by norm_num) (by norm_num)
  exact two_arithmetic16.1

end
end CubicGap
