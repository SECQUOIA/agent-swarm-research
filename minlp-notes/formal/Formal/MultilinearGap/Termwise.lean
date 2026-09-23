import Formal.MultilinearGap.Construction
import Formal.MultilinearGap.Monomial
import Formal.MultilinearGap.EnvelopeBounds

namespace MultilinearGap

open CubicGap

noncomputable section

/-- The distinct squarefree terms of the dyadic family. -/
def supports (L : ℕ) : Finset (Finset (Coord L)) :=
  Finset.univ.image (fun p : (j : Fin L) × Fin (blockCount L j) => support L p.1 p.2)

theorem sum_supports (L : ℕ) (f : Finset (Coord L) → ℝ) :
    ∑ s ∈ supports L, f s = ∑ j, ∑ b, f (support L j b) := by
  rw [supports, Finset.sum_image (fun _ _ _ _ h => support_injective L h)]
  exact Fintype.sum_sigma _

/-- Every distinct term has coefficient one. -/
theorem polynomial_eq_supportPolynomial (L : ℕ) :
    polynomial L = supportPolynomial (supports L) (fun _ => 1) := by
  funext x
  simp only [supportPolynomial, one_mul]
  exact (sum_supports L (fun s => monomial s x)).symm

theorem blockSize_mul_failure (L : ℕ) (j : Fin L) :
    (blockSize L j : ℝ) * (1 / (2 : ℝ)^L) = 1 / (blockCount L j : ℝ) := by
  have hcount : (blockCount L j : ℝ) ≠ 0 := by unfold blockCount; positivity
  have hsize : (blockSize L j : ℝ) ≠ 0 := by unfold blockSize; positivity
  have hproduct : (blockCount L j : ℝ) * (blockSize L j : ℝ) = (2 : ℝ)^L := by
    exact_mod_cast blockCount_mul_blockSize L j
  rw [← hproduct]
  field_simp

theorem support_monomial_minimum (L : ℕ) (j : Fin L)
    (b : Fin (blockCount L j)) :
    IsLeast (envelopeValues (monomial (support L j b)) (means L)) 0 := by
  apply monomial_minimum_zero_of_anchor (support L j b) (means L)
    (means_mem_cube L) (Sum.inl j) (by simp) (1 / (2 : ℝ)^L) (by positivity)
  · rw [support_erase_anchor_card]
    exact (blockSize_mul_failure L j).symm
  · intro i hi
    rcases Finset.mem_erase.mp hi with ⟨hne, hi⟩
    cases i with
    | inl k =>
      have hk : k = j := by simpa using hi
      subst k
      exact (hne rfl).elim
    | inr i => rfl
  · rw [support_erase_anchor_card, blockSize_mul_failure]
    exact (means_mem_cube L (Sum.inl j)).2

theorem anchor_le_leaf (L : ℕ) (hL : 1 ≤ L) (j : Fin L) :
    1 / (blockCount L j : ℝ) ≤ 1 - 1 / (2 : ℝ)^L := by
  have hc : (2 : ℝ) ≤ (blockCount L j : ℝ) := by
    unfold blockCount
    exact_mod_cast (Nat.pow_le_pow_right (by decide : 1 ≤ 2) (by omega : 1 ≤ j.val+1))
  have hn : (2 : ℝ) ≤ (2 : ℝ)^L := by
    simpa using (pow_le_pow_right₀ (by norm_num : (1 : ℝ) ≤ 2) hL)
  have ha : 1 / (blockCount L j : ℝ) ≤ 1 / 2 :=
    one_div_le_one_div_of_le (by norm_num) hc
  have hb : 1 / (2 : ℝ)^L ≤ 1 / 2 :=
    one_div_le_one_div_of_le (by norm_num) hn
  linarith

theorem support_monomial_maximum (L : ℕ) (hL : 1 ≤ L) (j : Fin L)
    (b : Fin (blockCount L j)) :
    IsGreatest (envelopeValues (monomial (support L j b)) (means L))
      (1 / (blockCount L j : ℝ)) := by
  apply monomial_maximum_of_min_coordinate (support L j b) (means L)
    (means_mem_cube L) (Sum.inl j) (by simp)
  intro i hi
  cases i with
  | inl k =>
    have hk : k = j := by simpa using hi
    subst k
    exact le_rfl
  | inr i => exact anchor_le_leaf L hL j

theorem support_monomial_gap (L : ℕ) (hL : 1 ≤ L) (j : Fin L)
    (b : Fin (blockCount L j)) :
    hullGap (monomial (support L j b)) (means L) = 1 / (blockCount L j : ℝ) := by
  rw [hullGap, (support_monomial_maximum L hL j b).csSup_eq,
    (support_monomial_minimum L j b).csInf_eq, sub_zero]

/-- Each scale contributes exactly one to the term-by-term gap. -/
theorem termwiseGap_eq (L : ℕ) (hL : 1 ≤ L) :
    termwiseGap (supports L) (means L) = (L : ℝ) := by
  rw [termwiseGap, sum_supports]
  simp_rw [support_monomial_gap L hL]
  have hc (j : Fin L) : (blockCount L j : ℝ) ≠ 0 := by unfold blockCount; positivity
  simp [hc]

end
end MultilinearGap
