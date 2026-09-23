import Formal.MultilinearGap.Construction
import Formal.MultilinearGap.Deficiency

/-! The dyadic family's lower graph-hull bound for every feasible finite law. -/
namespace MultilinearGap

open CubicGap
open scoped BigOperators

/-- The prescribed leaf marginals force mean failure count one. -/
theorem failureCount_expect (L : ℕ) (μ : Law (Vertex (Coord L)))
    (hmean : ∀ i, μ.expect (fun v => vertexPoint v i) = means L i) :
    μ.expect (failureCount L) = 1 := by
  unfold failureCount
  rw [μ.expect_sum]
  simp only [μ.expect_sub, μ.expect_const, hmean, means, sub_sub_cancel]
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul,
    Nat.cast_pow, Nat.cast_ofNat]
  field_simp

/-- No joint law with the prescribed means can lower the polynomial value by
more than the dyadic deficiency bound. -/
theorem law_polynomial_lower_bound (L : ℕ) (μ : Law (Vertex (Coord L)))
    (hmean : ∀ i, μ.expect (fun v => vertexPoint v i) = means L i) (s : ℕ) :
    (L : ℝ) - ((s : ℝ) + 2 * (L : ℝ) / (2 : ℝ) ^ s) ≤
      μ.expect (fun v => polynomial L (vertexPoint v)) := by
  let a : Vertex (Coord L) → Fin L → Bool := fun v j => v (Sum.inl j)
  have ha (j : Fin L) : μ.expect (fun v => if a v j then 1 else 0) =
      1 / (2 : ℝ) ^ (j.val + 1) := by
    simpa [vertexPoint, means, blockCount, a] using hmean (Sum.inl j)
  have hd := dyadic_deficiency_bound μ a (failureCount L) (failureCount_nonneg L)
    ha (failureCount_expect L μ hmean) s
  have hscaled (j : Fin L) :
      μ.expect (fun v => vertexPoint v (Sum.inl j) * (blockCount L j : ℝ)) = 1 := by
    rw [μ.expect_mul_const, hmean]
    simp only [means]
    have hp : (blockCount L j : ℝ) ≠ 0 := by simp [blockCount]
    field_simp
  have hpoint (v : Vertex (Coord L)) :
      (∑ j, vertexPoint v (Sum.inl j) * (blockCount L j : ℝ)) -
        (∑ j, if a v j then min ((2 : ℝ) ^ (j.val + 1)) (failureCount L v) else 0) ≤
      polynomial L (vertexPoint v) := by
    convert polynomial_lower_bound L v using 1
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro j _
    simp only [vertexPoint, a, blockCount, Nat.cast_pow, Nat.cast_ofNat]
    split <;> ring
  have hp := μ.expect_mono hpoint
  rw [μ.expect_sub, μ.expect_sum] at hp
  simp only [hscaled, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    nsmul_eq_mul, mul_one] at hp
  linarith

end MultilinearGap
