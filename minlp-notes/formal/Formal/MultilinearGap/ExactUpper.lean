import Formal.MultilinearGap.Lower
import Formal.MultilinearGap.Upper

/-! A sharp finite dual bound for the dyadic family. -/
namespace MultilinearGap

open CubicGap
open scoped BigOperators

/-- The selected capped value has a shifted-cap certificate. -/
theorem selected_min_certificate (a : Bool) (b c r : ℝ) (hcb : c ≤ b) :
    (if a then min b r else 0) ≤ min b r - min c r + (if a then c else 0) := by
  cases a with
  | false =>
    simp only [Bool.false_eq_true, ↓reduceIte, add_zero]
    exact sub_nonneg.mpr (min_le_min_right r hcb)
  | true => simp only [↓reduceIte]; linarith [min_le_left c r]

/-- Shifted caps telescope; only the final `s` caps remain. -/
theorem dyadic_exact_pointwise (L s : ℕ) (hs : s ≤ L) (a : ℕ → Bool)
    (r : ℝ) (hr : 0 ≤ r) :
    (∑ j ∈ Finset.range L, if a j then min ((2 : ℝ) ^ (j + 1)) r else 0) ≤
      (s : ℝ) * r + ∑ j ∈ Finset.range (L - s), if a (j + s) then (2 : ℝ) ^ (j + 1) else 0 := by
  let f : ℕ → ℝ := fun j => min ((2 : ℝ) ^ (j + 1)) r
  have hsmall : (∑ j ∈ Finset.range s, if a j then f j else 0) ≤
      ∑ j ∈ Finset.range s, f j := by
    apply Finset.sum_le_sum
    intro j _
    split
    · exact le_rfl
    · exact le_min (by positivity) hr
  have hlarge : (∑ j ∈ Finset.range (L - s), if a (j + s) then f (j + s) else 0) ≤
      ∑ j ∈ Finset.range (L - s), (f (j + s) - f j +
        (if a (j + s) then (2 : ℝ) ^ (j + 1) else 0)) := by
    apply Finset.sum_le_sum
    intro j _
    apply selected_min_certificate
    exact pow_le_pow_right₀ (by norm_num) (by omega)
  have hsplit (g : ℕ → ℝ) : ∑ j ∈ Finset.range L, g j =
      (∑ j ∈ Finset.range s, g j) + ∑ j ∈ Finset.range (L - s), g (j + s) := by
    conv_lhs => rw [← Nat.add_sub_of_le hs]
    rw [Finset.sum_range_add]
    simp only [Nat.add_comm]
  have hsplit' : ∑ j ∈ Finset.range L, f j =
      (∑ j ∈ Finset.range (L - s), f j) + ∑ j ∈ Finset.range s, f (j + (L - s)) := by
    conv_lhs => rw [← Nat.sub_add_cancel hs]
    rw [Finset.sum_range_add]
    simp only [Nat.add_comm]
  have hend : (∑ j ∈ Finset.range s, f (j + (L - s))) ≤ (s : ℝ) * r := by
    calc
      _ ≤ ∑ _j ∈ Finset.range s, r := Finset.sum_le_sum fun _ _ => min_le_right _ _
      _ = _ := by simp
  rw [hsplit]
  dsimp only [f] at hsmall hlarge hsplit' hend
  have hsum := add_le_add hsmall hlarge
  simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib] at hsum
  have htel := hsplit f
  dsimp only [f] at htel
  linarith

/-- The sharp dual bound holds for every finite law with the prescribed
activation means and mean deficiency one. -/
theorem dyadic_exact_deficiency_bound {Ω : Type*} [Fintype Ω] (L s : ℕ) (hs : s ≤ L)
    (μ : Law Ω) (a : Ω → ℕ → Bool) (r : Ω → ℝ) (hr : ∀ ω, 0 ≤ r ω)
    (ha : ∀ j, j < L → μ.expect (fun ω => if a ω j then 1 else 0) =
      1 / (2 : ℝ) ^ (j + 1)) (hmean : μ.expect r = 1) :
    μ.expect (fun ω => ∑ j ∈ Finset.range L,
      if a ω j then min ((2 : ℝ) ^ (j + 1)) (r ω) else 0) ≤
      (s : ℝ) + (L - s : ℕ) / (2 : ℝ) ^ s := by
  have hscale (j : ℕ) (hj : j ∈ Finset.range (L - s)) :
      μ.expect (fun ω => if a ω (j + s) then (2 : ℝ) ^ (j + 1) else 0) =
      1 / (2 : ℝ) ^ s := by
    have hjL : j + s < L := by have := Finset.mem_range.mp hj; omega
    have heq : (fun ω => if a ω (j + s) then (2 : ℝ) ^ (j + 1) else 0) =
        (fun ω => (if a ω (j + s) then 1 else 0) * (2 : ℝ) ^ (j + 1)) := by
      funext ω
      split <;> simp_all
    rw [heq, μ.expect_mul_const, ha _ hjL]
    rw [show j + s + 1 = (j + 1) + s by omega, pow_add]
    field_simp
  have h := μ.expect_mono (fun ω => dyadic_exact_pointwise L s hs (a ω) (r ω) (hr ω))
  simp only [μ.expect_add, μ.expect_const_mul, hmean, mul_one] at h
  have hc : (∑ j ∈ Finset.range (L - s),
      μ.expect (fun ω => if a ω (j + s) then (2 : ℝ) ^ (j + 1) else 0)) =
      (L - s : ℕ) / (2 : ℝ) ^ s := by
    rw [Finset.sum_congr rfl hscale]
    simp [div_eq_mul_inv]
  have hfinite (g : ℕ → Ω → ℝ) (n : ℕ) :
      μ.expect (fun ω => ∑ j ∈ Finset.range n, g j ω) =
        ∑ j ∈ Finset.range n, μ.expect (g j) := by
    simp only [Law.expect, Finset.mul_sum]
    rw [Finset.sum_comm]
  simp only [hfinite] at h ⊢
  rw [hc] at h
  exact h

/-- The exact finite dual certificate bounds every feasible polynomial mean. -/
theorem law_polynomial_exact_lower_bound (L s : ℕ) (hs : s ≤ L)
    (μ : Law (Vertex (Coord L)))
    (hmean : ∀ i, μ.expect (fun v => vertexPoint v i) = means L i) :
    (L : ℝ) - ((s : ℝ) + (L - s : ℕ) / (2 : ℝ) ^ s) ≤
      μ.expect (fun v => polynomial L (vertexPoint v)) := by
  let a : Vertex (Coord L) → ℕ → Bool := fun v j => if h : j < L then v (Sum.inl ⟨j, h⟩) else false
  have ha (j : ℕ) (hj : j < L) : μ.expect (fun v => if a v j then 1 else 0) =
      1 / (2 : ℝ) ^ (j + 1) := by
    simpa [vertexPoint, means, blockCount, a, hj] using hmean (Sum.inl ⟨j, hj⟩)
  have hd := dyadic_exact_deficiency_bound L s hs μ a (failureCount L)
    (failureCount_nonneg L) ha (failureCount_expect L μ hmean)
  have hsum (v : Vertex (Coord L)) :
      (∑ j ∈ Finset.range L, if a v j then min ((2 : ℝ) ^ (j + 1)) (failureCount L v) else 0) =
      ∑ j : Fin L, if v (Sum.inl j) then min ((2 : ℝ) ^ (j.val + 1)) (failureCount L v) else 0 := by
    rw [← Fin.sum_univ_eq_sum_range]
    apply Finset.sum_congr rfl
    intro j _
    simp [a, j.isLt]
  simp_rw [hsum] at hd
  have hscaled (j : Fin L) :
      μ.expect (fun v => vertexPoint v (Sum.inl j) * (blockCount L j : ℝ)) = 1 := by
    rw [μ.expect_mul_const, hmean]
    simp only [means]
    have hp : (blockCount L j : ℝ) ≠ 0 := by simp [blockCount]
    field_simp
  have hpoint (v : Vertex (Coord L)) :
      (∑ j, vertexPoint v (Sum.inl j) * (blockCount L j : ℝ)) -
        (∑ j, if v (Sum.inl j) then min ((2 : ℝ) ^ (j.val + 1)) (failureCount L v) else 0) ≤
      polynomial L (vertexPoint v) := by
    convert polynomial_lower_bound L v using 1
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro j _
    simp only [vertexPoint, blockCount, Nat.cast_pow, Nat.cast_ofNat]
    split <;> ring
  have hp := μ.expect_mono hpoint
  rw [μ.expect_sub, μ.expect_sum] at hp
  simp only [hscaled, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    nsmul_eq_mul, mul_one] at hp
  linarith

/-- A sharp finite upper bound for the actual continuous graph-hull gap. -/
theorem hullGap_exact_upper_bound (L s : ℕ) (hL : 2 ≤ L) (hs : s ≤ L) :
    hullGap (polynomial L) (means L) ≤ (s : ℝ) + (L - s : ℕ) / (2 : ℝ) ^ s := by
  apply hullGap_le_of_laws (polynomial L) (polynomial_separatelyAffine L) (means L)
    (L : ℝ) _ (polynomial_maximum L hL)
  intro μ hmean
  exact law_polynomial_exact_lower_bound L s hs μ hmean

end MultilinearGap
