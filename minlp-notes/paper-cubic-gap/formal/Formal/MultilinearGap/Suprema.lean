import Formal.MultilinearGap.GeneralGaps
import Formal.MultilinearGap.LowerAsymptotics

/-! Worst-case gap ratios range over all finite dimensions and nonnegative
coefficients, using actual continuous graph-hull widths. -/
namespace MultilinearGap

open CubicGap
noncomputable section

def degreeRatios (d : ℕ) : Set ℝ := {r | ∃ (I : Type) (hI : Fintype I)
    (hEq : DecidableEq I),
  letI := hI
  letI := hEq
  ∃ (S : Finset (Finset I)) (a : Finset I → ℝ) (x : I → ℝ),
    (∀ s ∈ S, 0 ≤ a s) ∧ (∀ s ∈ S, s.card ≤ d) ∧ x ∈ cube I ∧
      0 < hullGap (supportPolynomial S a) x ∧
      r = weightedTermwiseGap S a x / hullGap (supportPolynomial S a) x}

/-- Dimension allowance; padding by unused coordinates gives the equivalent
convention of requiring exactly `n` coordinates. -/
def dimensionRatios (n : ℕ) : Set ℝ := {r | ∃ (I : Type) (hI : Fintype I)
    (hEq : DecidableEq I),
  letI := hI
  letI := hEq
  ∃ (S : Finset (Finset I)) (a : Finset I → ℝ) (x : I → ℝ),
    Fintype.card I ≤ n ∧ (∀ s ∈ S, 0 ≤ a s) ∧ x ∈ cube I ∧
      0 < hullGap (supportPolynomial S a) x ∧
      r = weightedTermwiseGap S a x / hullGap (supportPolynomial S a) x}

def degreeSupremum (d : ℕ) : ℝ := sSup (degreeRatios d)
def dimensionSupremum (n : ℕ) : ℝ := sSup (dimensionRatios n)

theorem degreeRatios_mono : Monotone degreeRatios := by
  intro d e hde r hr
  obtain ⟨I, hI, hEq, S, a, x, ha, hdeg, hx, hpos, hr⟩ := hr
  exact ⟨I, hI, hEq, S, a, x, ha, fun s hs => (hdeg s hs).trans hde, hx, hpos, hr⟩

theorem dimensionRatios_mono : Monotone dimensionRatios := by
  intro n m hnm r hr
  obtain ⟨I, hI, hEq, S, a, x, hcard, ha, hx, hpos, hr⟩ := hr
  exact ⟨I, hI, hEq, S, a, x, hcard.trans hnm, ha, hx, hpos, hr⟩

theorem dimensionRatios_subset_degreeRatios (n : ℕ) :
    dimensionRatios n ⊆ degreeRatios n := by
  rintro r ⟨I, hI, hEq, S, a, x, hcard, ha, hx, hpos, hr⟩
  let _ := hI
  let _ := hEq
  exact ⟨I, hI, hEq, S, a, x, ha,
    fun s _ => (Finset.card_le_univ s).trans hcard, hx, hpos, hr⟩

def CubeDegreeBound (d : ℕ) (U : ℝ) : Prop :=
  ∀ (I : Type) [Fintype I] [DecidableEq I]
    (S : Finset (Finset I)) (a : Finset I → ℝ) (x : I → ℝ),
    (∀ s ∈ S, 0 ≤ a s) → (∀ s ∈ S, s.card ≤ d) → x ∈ cube I →
      weightedTermwiseGap S a x ≤ U * hullGap (supportPolynomial S a) x

theorem degreeRatios_le {d : ℕ} {U : ℝ} (hU : CubeDegreeBound d U)
    {r : ℝ} (hr : r ∈ degreeRatios d) : r ≤ U := by
  obtain ⟨I, hI, hEq, S, a, x, ha, hdeg, hx, hpos, rfl⟩ := hr
  let _ := hI
  let _ := hEq
  exact (div_le_iff₀ hpos).mpr (hU I S a x ha hdeg hx)

theorem degreeRatios_bddAbove {d : ℕ} {U : ℝ} (hU : CubeDegreeBound d U) :
    BddAbove (degreeRatios d) := ⟨U, fun _ hr => degreeRatios_le hU hr⟩

theorem witness_ratio_mem_dimensionRatios (n : ℕ) (hn : 8 ≤ n) :
    termwiseGap (supports (witnessLevels n)) (means (witnessLevels n)) /
      hullGap (polynomial (witnessLevels n)) (means (witnessLevels n)) ∈ dimensionRatios n := by
  refine ⟨Coord (witnessLevels n), inferInstance, inferInstance,
    supports (witnessLevels n), fun _ => 1, means (witnessLevels n),
    witness_dimension_le n (by omega), by simp, means_mem_cube _, ?_, ?_⟩
  · rw [← polynomial_eq_supportPolynomial]
    exact hullGap_positive _ (witnessLevels_ge_two n hn)
  · rw [← polynomial_eq_supportPolynomial]
    simp [weightedTermwiseGap, termwiseGap]

theorem dimensionRatios_nonempty (n : ℕ) (hn : 8 ≤ n) :
    (dimensionRatios n).Nonempty := ⟨_, witness_ratio_mem_dimensionRatios n hn⟩

theorem degreeRatios_nonempty (n : ℕ) (hn : 8 ≤ n) :
    (degreeRatios n).Nonempty :=
  (dimensionRatios_nonempty n hn).mono (dimensionRatios_subset_degreeRatios n)

theorem suprema_bounds (n : ℕ) (hn : 8 ≤ n) (U : ℝ) (hU : CubeDegreeBound n U) :
    lowerComparison n ≤ dimensionSupremum n ∧
      dimensionSupremum n ≤ degreeSupremum n ∧ degreeSupremum n ≤ U := by
  have hbd := degreeRatios_bddAbove hU
  have hbn : BddAbove (dimensionRatios n) := hbd.mono (dimensionRatios_subset_degreeRatios n)
  refine ⟨?_, ?_, ?_⟩
  · exact (lowerComparison_le_ratio n hn).trans
      (le_csSup hbn (witness_ratio_mem_dimensionRatios n hn))
  · exact csSup_le (dimensionRatios_nonempty n hn)
      (fun r hr => le_csSup hbd (dimensionRatios_subset_degreeRatios n hr))
  · exact csSup_le (degreeRatios_nonempty n hn) (fun _ hr => degreeRatios_le hU hr)

end
end MultilinearGap
