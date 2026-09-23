import Formal.CubicGap.Threshold
import Formal.CubicGap.CountUpper
import Formal.CubicGap.CountLaws
import Formal.CubicGap.Envelope

namespace CubicGap

noncomputable section

theorem two_law_upper (m : ℕ) (μ : Law (Vertex (Fin 2 × Fin m)))
    (hmean : HasMeans μ (thresholdTwoMeans m)) :
    μ.expect (fun v => twoFamily m (vertexPoint v)) ≤ (twoUpper m : ℝ) := by
  have hA := expect_group_count_of_mean m μ
    (fun g : Fin 2 => if g = 0 then (1/2 : ℝ) else 3/4)
    (fun g j => hmean (g,j)) 0
  have hpoint (v : Vertex (Fin 2 × Fin m)) :
      twoFamily m (vertexPoint v) ≤
        (9/4 : ℝ) * m.choose 2 * count (fun i => v (0,i)) := by
    rw [show twoFamily m (vertexPoint v) = _ from twoFamily_binary m v]
    have hb := twoValue_upper
      (show count (fun i => v (0,i)) ≤ m by simpa using count_le (fun i => v (0,i)))
      (show count (fun i => v (1,i)) ≤ m by simpa using count_le (fun i => v (1,i)))
    have hcast := (Rat.cast_le (K := ℝ)).mpr hb
    push_cast at hcast
    exact hcast
  have h := μ.expect_mono hpoint
  simp only [Law.expect_const_mul] at h
  rw [hA] at h
  convert h using 1
  simp [twoUpper]
  ring

/-- Exact concave envelope for every member of the two-group family. -/
theorem two_maximum (m : ℕ) :
    IsGreatest (envelopeValues (twoFamily m) (thresholdTwoMeans m)) (twoUpper m : ℝ) := by
  apply maximum_from_laws _ (twoFamily_coordinate_affine m)
  · exact two_law_upper m
  · exact ⟨twoThreshold m, twoThreshold_mean m, twoThreshold_value m⟩

theorem three_law_upper (m : ℕ) (hm : 0 < m) (coef : Fin 6 → ℚ)
    (hcoef : ∀ i, 0 ≤ coef i) (μ : Law (Vertex (Fin 3 × Fin m)))
    (hmean : HasMeans μ (thresholdThreeMeans m)) :
    μ.expect (fun v => threeFamily m coef (vertexPoint v)) ≤ (orbitUpper m coef : ℝ) := by
  let p : Fin 3 → ℝ := fun g => if g = 0 then 1/4 else if g = 1 then 1/2 else 3/4
  have hA := expect_group_count_of_mean m μ p (fun g j => hmean (g,j)) 0
  have hB := expect_group_count_of_mean m μ p (fun g j => hmean (g,j)) 1
  have hC := expect_group_count_of_mean m μ p (fun g j => hmean (g,j)) 2
  have hpoint (v : Vertex (Fin 3 × Fin m)) :
      threeFamily m coef (vertexPoint v) ≤
        (coef 0 : ℝ) * m.choose 3 / m * count (fun i => v (2,i)) +
        (coef 1 : ℝ) * m.choose 2 * count (fun i => v (1,i)) +
        (coef 2 : ℝ) * m.choose 2 / m * count (fun i => v (1,i)) +
        ((coef 3 : ℝ) + coef 4) * m * count (fun i => v (0,i)) +
        (coef 5 : ℝ) * m.choose 2 / m * count (fun i => v (0,i)) := by
    rw [show threeFamily m coef (vertexPoint v) = _ from threeFamily_binary m coef v]
    have hbound (g : Fin 3) : count (fun i => v (g,i)) ≤ m := by
      simpa using count_le (fun i => v (g,i))
    exact_mod_cast countPhi_upper hm (hbound 0) (hbound 1) (hbound 2) coef hcoef
  have h := μ.expect_mono hpoint
  simp only [Law.expect_add, Law.expect_const_mul] at h
  rw [hA, hB, hC] at h
  have hm' : (m : ℝ) ≠ 0 := by exact_mod_cast Nat.ne_of_gt hm
  convert h using 1
  simp only [orbitUpper, Rat.cast_add, Rat.cast_mul, Rat.cast_div, Rat.cast_natCast]
  norm_num [p, show (2 : Fin 3) ≠ 0 by decide, show (2 : Fin 3) ≠ 1 by decide]
  field_simp
  ring

/-- A single common-threshold law attains the termwise upper bounds simultaneously. -/
theorem three_maximum (m : ℕ) (hm : 0 < m) (coef : Fin 6 → ℚ)
    (hcoef : ∀ i, 0 ≤ coef i) :
    IsGreatest (envelopeValues (threeFamily m coef) (thresholdThreeMeans m))
      (orbitUpper m coef : ℝ) := by
  apply maximum_from_laws _ (threeFamily_coordinate_affine m coef)
  · exact three_law_upper m hm coef hcoef
  · exact ⟨threeThreshold m, threeThreshold_mean m, threeThreshold_value m coef⟩

end
end CubicGap
