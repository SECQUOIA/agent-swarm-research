import Formal.MultilinearGap.Termwise
import Formal.CubicGap.TermwiseUpper

namespace MultilinearGap

open CubicGap
noncomputable section

theorem polynomial_common_leaf (L : ℕ) (a : Fin L → ℝ) (z : ℝ) :
    polynomial L (Sum.elim a (fun _ => z)) =
      ∑ j, (blockCount L j : ℝ) * a j * z ^ blockSize L j := by
  simp [polynomial, monomial_support, block_card, mul_assoc]

theorem polynomial_law_upper (L : ℕ) (μ : Law (Vertex (Coord L)))
    (hmean : HasMeans μ (means L)) :
    μ.expect (fun v => polynomial L (vertexPoint v)) ≤ (L : ℝ) := by
  have h (v : Vertex (Coord L)) : polynomial L (vertexPoint v) ≤
      ∑ j, ∑ _b : Fin (blockCount L j), vertexPoint v (Sum.inl j) := by
    apply Finset.sum_le_sum
    intro j _
    apply Finset.sum_le_sum
    intro b _
    exact monomial_le_coordinate (support L j b)
      (by intro i _; simp only [vertexPoint]; split <;> norm_num) (by simp)
  have hh := μ.expect_mono h
  dsimp [HasMeans] at hmean
  simp only [Law.expect_sum, hmean, means] at hh
  have hlevel (j : Fin L) :
      ∑ _b : Fin (blockCount L j), 1 / (blockCount L j : ℝ) = 1 := by
    simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    have hp : (blockCount L j : ℝ) ≠ 0 := by dsimp [blockCount]; positivity
    field_simp
  simpa only [hlevel, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    nsmul_eq_mul, mul_one] using hh

def upperPoint (L : ℕ) (t : Bool) : Coord L → ℝ :=
  if t then Sum.elim
    (fun j => (1 / (blockCount L j : ℝ)) / (1 - 1 / (2 : ℝ)^L))
    (fun _ => 1) else fun _ => 0

theorem leaf_mean_pos (L : ℕ) (hL : 2 ≤ L) : 0 < 1 - 1 / (2 : ℝ)^L := by
  have hp : (1 : ℝ) < (2 : ℝ)^L := one_lt_pow₀ (by norm_num) (by omega)
  have hi : 1 / (2 : ℝ)^L < 1 := (div_lt_one (by positivity)).mpr hp
  linarith

/-- A two-point law of cube points attains all positive monomial upper bounds
at once. Its first atom has every leaf equal to one. -/
theorem polynomial_maximum (L : ℕ) (hL : 2 ≤ L) :
    IsGreatest (envelopeValues (polynomial L) (means L)) (L : ℝ) := by
  have hb := leaf_mean_pos L hL
  have hb0 : 1 - ((2 : ℝ)^L)⁻¹ ≠ 0 := by
    simpa only [one_div] using ne_of_gt hb
  have hb1 : 1 - 1 / (2 : ℝ)^L ≤ 1 := by
    have : 0 ≤ 1 / (2 : ℝ)^L := by positivity
    linarith
  let μ := upperMonomialLaw (1 - 1 / (2 : ℝ)^L) hb.le hb1
  have hy (t : Bool) : upperPoint L t ∈ cube (Coord L) := by
    cases t with
    | false => intro i; simp [upperPoint]
    | true =>
      intro i
      cases i with
      | inl j =>
        simp only [upperPoint, ↓reduceIte, Sum.elim_inl]
        exact ⟨by positivity, (div_le_one hb).mpr (anchor_le_leaf L (by omega) j)⟩
      | inr i => simp [upperPoint]
  have hmean (i : Coord L) : μ.expect (fun t => upperPoint L t i) = means L i := by
    cases i with
    | inl j =>
      simpa [μ, upperMonomialLaw, Law.expect, upperPoint, means] using
        mul_div_cancel₀ ((blockCount L j : ℝ)⁻¹) hb0
    | inr i => simp [μ, upperMonomialLaw, Law.expect, upperPoint, means]
  have hzero : polynomial L (upperPoint L false) = 0 := by
    simp [upperPoint, polynomial, monomial_support]
  have htrue : polynomial L (upperPoint L true) =
      (L : ℝ) / (1 - 1 / (2 : ℝ)^L) := by
    simp only [upperPoint, ↓reduceIte, polynomial_common_leaf, one_pow, mul_one]
    have hterm (j : Fin L) : (blockCount L j : ℝ) *
        (1 / (blockCount L j : ℝ) / (1 - 1 / (2 : ℝ)^L)) =
        1 / (1 - 1 / (2 : ℝ)^L) := by
      have hp : (blockCount L j : ℝ) ≠ 0 := by dsimp [blockCount]; positivity
      field_simp
    simp_rw [hterm]
    simp [div_eq_mul_inv]
  have hvalue : μ.expect (fun t => polynomial L (upperPoint L t)) = (L : ℝ) := by
    simpa [μ, upperMonomialLaw, Law.expect, hzero, htrue] using mul_div_cancel₀ (L : ℝ) hb0
  refine ⟨cube_law_attainment μ (polynomial L) (upperPoint L) (means L) L hy hmean hvalue, ?_⟩
  intro z hz
  obtain ⟨ν, hν, hval⟩ := (mem_cubeGraph_hull_iff (polynomial L)
    (polynomial_separatelyAffine L) (means L) z).mp hz
  rw [← hval]
  exact polynomial_law_upper L ν hν

theorem polynomial_at_means (L : ℕ) :
    polynomial L (means L) = ∑ j : Fin L, (1 - 1 / (2 : ℝ)^L)^blockSize L j := by
  have hm : means L = Sum.elim (fun j => 1 / (blockCount L j : ℝ))
      (fun _ => 1 - 1 / (2 : ℝ)^L) := by
    funext i
    cases i <;> rfl
  rw [hm, polynomial_common_leaf]
  apply Finset.sum_congr rfl
  intro j _
  have hp : (blockCount L j : ℝ) ≠ 0 := by dsimp [blockCount]; positivity
  field_simp

theorem polynomial_at_means_lt (L : ℕ) (hL : 2 ≤ L) :
    polynomial L (means L) < (L : ℝ) := by
  rw [polynomial_at_means]
  have hb := leaf_mean_pos L hL
  have hb1 : 1 - 1 / (2 : ℝ)^L < 1 := by
    have : 0 < 1 / (2 : ℝ)^L := by positivity
    linarith
  calc
    _ < ∑ _j : Fin L, (1 : ℝ) := by
      apply Finset.sum_lt_sum_of_nonempty
      · exact ⟨⟨0, by omega⟩, Finset.mem_univ _⟩
      · intro j _
        exact pow_lt_one₀ hb.le hb1 (by dsimp [blockSize]; positivity)
    _ = _ := by simp

end
end MultilinearGap
