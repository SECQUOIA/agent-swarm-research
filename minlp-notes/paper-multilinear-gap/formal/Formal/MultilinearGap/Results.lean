import Formal.MultilinearGap.Upper
import Formal.MultilinearGap.Lower
import Formal.MultilinearGap.Growth

/-! The positive-coefficient uniform-gap conjecture fails already on the unit
cube with distinct squarefree monomials and every coefficient equal to one. -/
namespace MultilinearGap

open CubicGap
noncomputable section

theorem envelope_lower_bound (L s : ℕ) (z : ℝ)
    (hz : z ∈ envelopeValues (polynomial L) (means L)) :
    (L : ℝ) - ((s : ℝ) + 2 * (L : ℝ) / (2 : ℝ)^s) ≤ z := by
  obtain ⟨μ, hmean, hvalue⟩ := (mem_cubeGraph_hull_iff (polynomial L)
    (polynomial_separatelyAffine L) (means L) z).mp hz
  rw [← hvalue]
  exact law_polynomial_lower_bound L μ hmean s

/-- This weaker bound suffices for unboundedness; no exact lower envelope or
asymptotic formula is assumed. -/
theorem hullGap_bound (L : ℕ) (hL : 2 ≤ L) (s : ℕ) :
    hullGap (polynomial L) (means L) ≤
      (s : ℝ) + 2 * (L : ℝ) / (2 : ℝ)^s := by
  exact hullGap_le_of_laws (polynomial L) (polynomial_separatelyAffine L)
    (means L) L _ (polynomial_maximum L hL)
    (fun μ hmean => law_polynomial_lower_bound L μ hmean s)

theorem hullGap_positive (L : ℕ) (hL : 2 ≤ L) :
    0 < hullGap (polynomial L) (means L) := by
  apply hullGap_pos_of_graph_lt (polynomial L) (means L) (means_mem_cube L) L
    (polynomial_maximum L hL)
  · exact ⟨(L : ℝ) - (0 + 2 * (L : ℝ) / (2 : ℝ)^0),
      fun z hz => by simpa only [Nat.cast_zero] using envelope_lower_bound L 0 z hz⟩
  · exact polynomial_at_means_lt L hL

/-- Every proposed constant is exceeded by an explicit family member, using
the actual termwise and continuous graph-hull gaps. -/
theorem unbounded_gap_ratio (C : ℝ) :
    ∃ L : ℕ, 2 ≤ L ∧ 0 < hullGap (polynomial L) (means L) ∧
      C < termwiseGap (supports L) (means L) / hullGap (polynomial L) (means L) := by
  obtain ⟨L, s, hL, hlarge⟩ := exists_levels (max C 0)
  have hpos := hullGap_positive L hL
  refine ⟨L, hL, hpos, (lt_div_iff₀ hpos).mpr ?_⟩
  rw [termwiseGap_eq L (by omega)]
  calc
    C * hullGap (polynomial L) (means L) ≤
        max C 0 * hullGap (polynomial L) (means L) :=
      mul_le_mul_of_nonneg_right (le_max_left _ _) hpos.le
    _ ≤ max C 0 * ((s : ℝ) + 2 * (L : ℝ) / (2 : ℝ)^s) :=
      mul_le_mul_of_nonneg_left (hullGap_bound L hL s) (le_max_right _ _)
    _ < (L : ℝ) := hlarge

/-- Even the subclass with coefficient one on each distinct squarefree support
has no uniform term-by-term versus convex-hull gap bound on unit cubes. -/
theorem no_uniform_positive_multilinear_bound :
    ¬ ∃ C : ℝ, ∀ (I : Type) [Fintype I] [DecidableEq I]
      (S : Finset (Finset I)) (x : I → ℝ), x ∈ cube I →
      0 < hullGap (supportPolynomial S (fun _ => 1)) x →
      termwiseGap S x ≤ C * hullGap (supportPolynomial S (fun _ => 1)) x := by
  rintro ⟨C, hC⟩
  obtain ⟨L, hL, hpos, hratio⟩ := unbounded_gap_ratio C
  have hbound := hC (Coord L) (supports L) (means L) (means_mem_cube L)
    (by rw [← polynomial_eq_supportPolynomial]; exact hpos)
  rw [← polynomial_eq_supportPolynomial] at hbound
  have hstrict := (lt_div_iff₀ hpos).mp hratio
  linarith

end
end MultilinearGap
