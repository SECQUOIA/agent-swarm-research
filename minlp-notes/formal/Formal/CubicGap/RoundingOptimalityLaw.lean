import Formal.CubicGap.RoundingOptimality
import Formal.CubicGap.RoundingLaws
import Formal.CubicGap.RoundingUpper

/-! The fixed-mixture obstruction evaluated on actual finite binary laws. -/
namespace CubicGap
namespace RoundingOptimality
open MultilinearGap MeasureTheory Set
noncomputable section

/-- A uniform deficiency fraction for a fixed weighted combination of the three
actual laws, over every pair and triple in every finite cube. -/
def FixedMixtureGuarantee (w r v α : ℝ) : Prop :=
  ∀ (n : ℕ) (x : Fin n → ℝ) (hx : x ∈ cube (Fin n))
    (s : Finset (Fin n)) (i : Fin n),
    i ∈ s → (∀ j ∈ s, x i ≤ x j) → (s.card = 2 ∨ s.card = 3) →
    α * hullGap (monomial s) x ≤
      w * (x i - (orientationLaw x).expect (fun z => monomial s (vertexPoint z))) + 
      r * (x i - (bernoulliLaw x hx).expect (fun z => monomial s (vertexPoint z))) + 
      v * (x i - (biasedHighLaw x hx).expect (fun z => monomial s (vertexPoint z)))

private theorem orientation_triple_moment (x : Fin 3 → ℝ) :
    (orientationLaw x).expect (fun z => monomial {0, 1, 2} (vertexPoint z)) =
      ∫ t in (0 : ℝ)..1, orientationProbability (x 0) t * 
        orientationProbability (x 1) t * orientationProbability (x 2) t := by
  rw [orientationLaw_expect_monomial]
  simp [monomial, mul_assoc]

private theorem triple_sorted_min (x : Fin 3 → ℝ) (h01 : x 0 ≤ x 1)
    (h12 : x 1 ≤ x 2) : ∀ j ∈ ({0, 1, 2} : Finset (Fin 3)), x 0 ≤ x j := by
  intro j _
  fin_cases j
  · exact le_rfl
  · exact h01
  · exact h01.trans h12

/-- Evaluation of the actual three laws on every member of the one-low curve. -/
theorem oneLow_law_normalized (t : ℝ) (ht : 0 < t) (ht8 : t ≤ 1 / 8) :
    let x := oneLowPoint t
    let hx := oneLowPoint_cube t ht ht8
    let H := hullGap (monomial ({0, 1, 2} : Finset (Fin 3))) x
    0 < H ∧
    (x 0 - (orientationLaw x).expect (fun z => monomial {0, 1, 2} (vertexPoint z))) / H = 3 / 8 ∧
    (x 0 - (bernoulliLaw x hx).expect (fun z => monomial {0, 1, 2} (vertexPoint z))) / H =
      t - t ^ 3 / 2 ∧
    (x 0 - (biasedHighLaw x hx).expect (fun z => monomial {0, 1, 2} (vertexPoint z))) / H =
      3 / 4 := by
  dsimp only
  let x := oneLowPoint t
  have hx := oneLowPoint_cube t ht ht8
  have hsort := oneLowPoint_sorted t ht ht8
  have h01 : x 0 ≤ x 1 := hsort.1
  have h12 : x 1 ≤ x 2 := le_rfl
  have hgap := triple_hullGap x hx 0 1 2 (by decide) (by decide) (by decide) h01 h12
  have ho := orientation_integral_one_low (hx 0) (hx 1) (hx 2) hsort.2.1 hsort.2.2 h12
  have hb := integral_biasedHigh_triple_one_low (hx 0) (hx 1) (hx 2) h12 hsort.2.1 hsort.2.2
  have hi := independentRounding_triple_deficiency x hx 0 1 2 (by decide) (by decide) (by decide)
  have hsum : 2 - x 1 - x 2 = t ^ 2 + t ^ 2 := by simp [x, oneLowPoint]; ring
  have hfail : 1 - x 1 = t ^ 2 := by simp [x, oneLowPoint]
  have hfail' : 1 - x 2 = t ^ 2 := by simp [x, oneLowPoint]
  have hzero : x 0 = t := rfl
  rw [hsum, hzero] at hgap
  have hpos : 0 < min t (t ^ 2 + t ^ 2) := lt_min ht (by positivity)
  change 0 < hullGap (monomial {0, 1, 2}) x ∧ _
  rw [hgap]
  refine ⟨hpos, ?_, ?_, ?_⟩
  · rw [orientation_triple_moment, ho, hfail, hfail']
    simp only [oneLowPoint, Matrix.cons_val_zero]
    convert (oneLow_normalized_formulas t ht ht8).1 using 1
    ring
  · rw [hi, hzero]
    convert (oneLow_normalized_formulas t ht ht8).2.1 using 1
    dsimp [x, oneLowPoint]
    ring
  · rw [biasedHighLaw_expect_triple _ _ (by decide : (0 : Fin 3) ≠ 1)
      (by decide : (0 : Fin 3) ≠ 2) (by decide : (1 : Fin 3) ≠ 2), hb,
      hfail, hfail']
    simp only [oneLowPoint, Matrix.cons_val_zero]
    convert (oneLow_normalized_formulas t ht ht8).2.2 using 1
    ring

/-- Evaluation of the actual three laws on every member of the all-high curve. -/
theorem allHigh_law_normalized (t : ℝ) (ht : 0 < t) (ht8 : t ≤ 1 / 8) :
    let x := allHighPoint t
    let hx := allHighPoint_cube t ht ht8
    let H := hullGap (monomial ({0, 1, 2} : Finset (Fin 3))) x
    0 < H ∧
    (x 0 - (orientationLaw x).expect (fun z => monomial {0, 1, 2} (vertexPoint z))) / H = 3 / 8 ∧
    (x 0 - (bernoulliLaw x hx).expect (fun z => monomial {0, 1, 2} (vertexPoint z))) / H =
      (1 / 2 + t) - (1 / 2 + t) ^ 2 / 4 ∧
    (x 0 - (biasedHighLaw x hx).expect (fun z => monomial {0, 1, 2} (vertexPoint z))) / H =
      3 / 8 := by
  dsimp only
  let x := allHighPoint t
  have hx := allHighPoint_cube t ht ht8
  have hsort := allHighPoint_sorted t ht ht8
  have h01 : x 0 ≤ x 1 := hsort.2
  have h12 : x 1 ≤ x 2 := le_rfl
  have hgap := triple_hullGap x hx 0 1 2 (by decide) (by decide) (by decide) h01 h12
  have ho := orientation_integral_all_high (hx 0) (hx 1) (hx 2) hsort.1 h01 h12
  have hb := integral_biasedHigh_triple_high (hx 0) (hx 1) (hx 2) h01 h12 hsort.1
  have hi := independentRounding_triple_deficiency x hx 0 1 2 (by decide) (by decide) (by decide)
  have hsum : 2 - x 1 - x 2 = 1 / 2 + t := by simp [x, allHighPoint]; ring
  have hfail : 1 - x 1 = (1 / 2 + t) / 2 := by simp [x, allHighPoint]
  have hfail' : 1 - x 2 = (1 / 2 + t) / 2 := by simp [x, allHighPoint]
  have hzero : x 0 = 1 / 2 + t := rfl
  rw [hsum, hzero, min_self] at hgap
  have hpos : 0 < 1 / 2 + t := by linarith
  change 0 < hullGap (monomial {0, 1, 2}) x ∧ _
  rw [hgap]
  refine ⟨hpos, ?_, ?_, ?_⟩
  · rw [orientation_triple_moment, ho, hfail, hfail']
    simp only [allHighPoint, Matrix.cons_val_zero]
    field_simp
    ring
  · rw [hi, hzero]
    change ((1 / 2 + t) * (1 - (1 - (1 / 2 + t) / 2) *
      (1 - (1 / 2 + t) / 2))) / (1 / 2 + t) = _
    field_simp
    ring
  · rw [biasedHighLaw_expect_triple _ _ (by decide : (0 : Fin 3) ≠ 1)
      (by decide : (0 : Fin 3) ≠ 2) (by decide : (1 : Fin 3) ≠ 2), hb,
      hfail, hfail']
    simp only [allHighPoint, Matrix.cons_val_zero]
    field_simp
    ring

/-- The bilinear boundary configuration supplies the first mixture constraint. -/
theorem fixedMixture_bilinear_constraint (w r v α : ℝ)
    (h : FixedMixtureGuarantee w r v α) : α ≤ w / 2 + r / 2 := by
  let x : Fin 2 → ℝ := fun _ => 1 / 2
  have hx : x ∈ cube (Fin 2) := by intro i; norm_num [x]
  have hg := h 2 x hx {0, 1} 0 (by simp) (by intro i _; exact le_rfl)
    (Or.inl (by decide))
  have hgap := pair_hullGap x hx 0 1 (by decide) (le_rfl)
  have ho := orientation_integral_pair (hx 0) (hx 1) (le_rfl)
  have hb := integral_biasedHigh_pair_low (hx 0) (le_rfl) (show x 1 ≤ 1 / 2 from le_rfl)
  have hi := independentRounding_pair_deficiency x hx 0 1 (by decide)
  rw [hgap, orientationLaw_expect_pair x 0 1 (by decide), ho, hi,
    biasedHighLaw_expect_pair x hx (by decide : (0 : Fin 2) ≠ 1), hb] at hg
  norm_num [x] at hg
  linarith

/-- Every uniform guarantee satisfies the two constraints obtained from actual
positive-gap cubic configurations and their proved limits. -/
theorem fixedMixture_limit_constraints (w r v α : ℝ)
    (h : FixedMixtureGuarantee w r v α) :
    α ≤ 3 * w / 8 + 3 * v / 4 ∧ α ≤ 3 * w / 8 + 7 * r / 16 + 3 * v / 8 := by
  apply limit_constraints w r v α
  · intro n
    let t := smallParameter n
    obtain ⟨ht, ht8⟩ := smallParameter_bounds n
    let x := oneLowPoint t
    have hx := oneLowPoint_cube t ht ht8
    have hsort := oneLowPoint_sorted t ht ht8
    have hg := h 3 x hx {0, 1, 2} 0 (by simp)
      (triple_sorted_min x hsort.1 le_rfl) (Or.inr (by decide))
    obtain ⟨hp, ho, hi, hb⟩ := oneLow_law_normalized t ht ht8
    have hd := div_le_div_of_nonneg_right hg hp.le
    dsimp only [x] at hd
    simp only [add_div, mul_div_assoc, ho, hi, hb, div_self hp.ne', mul_one] at hd
    nlinarith [hd]
  · intro n
    let t := smallParameter n
    obtain ⟨ht, ht8⟩ := smallParameter_bounds n
    let x := allHighPoint t
    have hx := allHighPoint_cube t ht ht8
    have hsort := allHighPoint_sorted t ht ht8
    have hg := h 3 x hx {0, 1, 2} 0 (by simp)
      (triple_sorted_min x hsort.2 le_rfl) (Or.inr (by decide))
    obtain ⟨hp, ho, hi, hb⟩ := allHigh_law_normalized t ht ht8
    have hd := div_le_div_of_nonneg_right hg hp.le
    dsimp only [x] at hd
    simp only [add_div, mul_div_assoc, ho, hi, hb, div_self hp.ne', mul_one] at hd
    nlinarith [hd]

/-- The advertised weights attain the uniform fraction in the very same predicate
used for the optimality obstruction. -/
theorem optimal_mixture_guarantee :
    FixedMixtureGuarantee (18 / 31) (6 / 31) (7 / 31) (12 / 31) := by
  intro n x hx s i hi hmin hcard
  have hs : s.card ≤ 3 := by rcases hcard with h | h <;> omega
  have h := cubicRoundingLaw_support_deficiency s x hx hs
  rw [monomialUpper_eq_anchor s x i hi hmin, cubicRoundingLaw_expect] at h
  nlinarith [h]

/-- No fixed mixture of the actual O/I/B laws can guarantee more than `12/31`
of the monomial graph-hull width uniformly, even just on pairs and triples. -/
theorem fixed_mixture_optimal_bound (w r v α : ℝ) (hsum : w + r + v = 1)
    (h : FixedMixtureGuarantee w r v α) : α ≤ 12 / 31 := by
  obtain ⟨hone, hhigh⟩ := fixedMixture_limit_constraints w r v α h
  exact weighted_obstruction w r v α hsum (fixedMixture_bilinear_constraint w r v α h)
    hone hhigh

/-- The optimal fixed weights are uniquely `18/31`, `6/31`, and `7/31`. -/
theorem fixed_mixture_optimal_weights_unique (w r v : ℝ) (hsum : w + r + v = 1)
    (h : FixedMixtureGuarantee w r v (12 / 31)) :
    w = 18 / 31 ∧ r = 6 / 31 ∧ v = 7 / 31 := by
  obtain ⟨hone, hhigh⟩ := fixedMixture_limit_constraints w r v (12 / 31) h
  exact optimal_weights_unique w r v hsum (fixedMixture_bilinear_constraint w r v (12 / 31) h)
    hone hhigh

/-- The exact optimum over nonnegative normalized weights is attained and equals `12/31`. -/
theorem fixed_mixture_optimum :
    IsGreatest {α : ℝ | ∃ w r v : ℝ, 0 ≤ w ∧ 0 ≤ r ∧ 0 ≤ v ∧
      w + r + v = 1 ∧ FixedMixtureGuarantee w r v α} (12 / 31) := by
  constructor
  · exact ⟨18 / 31, 6 / 31, 7 / 31, by norm_num, by norm_num, by norm_num,
      by norm_num, optimal_mixture_guarantee⟩
  · rintro α ⟨w, r, v, _, _, _, hsum, h⟩
    exact fixed_mixture_optimal_bound w r v α hsum h

end
end RoundingOptimality
end CubicGap
