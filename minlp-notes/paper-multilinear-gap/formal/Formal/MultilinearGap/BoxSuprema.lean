import Formal.MultilinearGap.BoxTransfer
import Formal.MultilinearGap.ExactDimension

/-! Worst-case ratios on all finite nonnegative boxes, with degree bounded and
with dimension fixed exactly. The gaps refer to the original continuous graph
hulls and original term-by-term relaxation. -/
namespace MultilinearGap

open CubicGap
noncomputable section

/-- All ratios in degree at most `d`, over every finite nonnegative box. -/
def boxDegreeRatios (d : ℕ) : Set ℝ := {r | ∃ (I : Type) (hI : Fintype I)
    (hEq : DecidableEq I),
  letI := hI
  letI := hEq
  ∃ (S : Finset (Finset I)) (a : Finset I → ℝ) (l u x : I → ℝ),
    (∀ s ∈ S, 0 ≤ a s) ∧ (∀ s ∈ S, s.card ≤ d) ∧
      (∀ i, 0 ≤ l i) ∧ (∀ i, l i ≤ u i) ∧ x ∈ coordinateBox l u ∧
      0 < boxHullGap l u (supportPolynomial S a) x ∧
      r = boxTermwiseGap S a l u x / boxHullGap l u (supportPolynomial S a) x}

/-- All ratios in exactly `n` coordinates, over every finite nonnegative box. -/
def boxDimensionRatios (n : ℕ) : Set ℝ := {r | ∃ (I : Type) (hI : Fintype I)
    (hEq : DecidableEq I),
  letI := hI
  letI := hEq
  ∃ (S : Finset (Finset I)) (a : Finset I → ℝ) (l u x : I → ℝ),
    Fintype.card I = n ∧ (∀ s ∈ S, 0 ≤ a s) ∧
      (∀ i, 0 ≤ l i) ∧ (∀ i, l i ≤ u i) ∧ x ∈ coordinateBox l u ∧
      0 < boxHullGap l u (supportPolynomial S a) x ∧
      r = boxTermwiseGap S a l u x / boxHullGap l u (supportPolynomial S a) x}

def boxDegreeSupremum (d : ℕ) : ℝ := sSup (boxDegreeRatios d)
def boxDimensionSupremum (n : ℕ) : ℝ := sSup (boxDimensionRatios n)

/-- A unit cube is one of the allowed nonnegative boxes. -/
theorem degreeRatios_subset_boxDegreeRatios (d : ℕ) :
    degreeRatios d ⊆ boxDegreeRatios d := by
  rintro r ⟨I, hI, hEq, S, a, x, ha, hd, hx, hpos, hr⟩
  exact ⟨I, hI, hEq, S, a, fun _ => 0, fun _ => 1, x, ha, hd,
    by simp, by simp, hx, hpos, hr⟩

theorem exactDimensionRatios_subset_boxDimensionRatios (n : ℕ) :
    exactDimensionRatios n ⊆ boxDimensionRatios n := by
  rintro r ⟨I, hI, hEq, S, a, x, hc, ha, hx, hpos, hr⟩
  exact ⟨I, hI, hEq, S, a, fun _ => 0, fun _ => 1, x, hc, ha,
    by simp, by simp, hx, hpos, hr⟩

theorem dimensionRatios_subset_boxDimensionRatios (n : ℕ) :
    dimensionRatios n ⊆ boxDimensionRatios n := by
  rw [← exactDimensionRatios_eq n]
  exact exactDimensionRatios_subset_boxDimensionRatios n

theorem boxDimensionRatios_subset_boxDegreeRatios (n : ℕ) :
    boxDimensionRatios n ⊆ boxDegreeRatios n := by
  rintro r ⟨I, hI, hEq, S, a, l, u, x, hc, ha, hl, hlu, hx, hpos, hr⟩
  let _ := hI
  let _ := hEq
  exact ⟨I, hI, hEq, S, a, l, u, x, ha,
    fun s _ => (Finset.card_le_univ s).trans_eq hc, hl, hlu, hx, hpos, hr⟩

/-- The cube upper bound applies to every ratio on an original nonnegative box. -/
theorem boxDegreeRatios_le {d : ℕ} {U : ℝ} (hU : CubeDegreeBound d U)
    {r : ℝ} (hr : r ∈ boxDegreeRatios d) : r ≤ U := by
  obtain ⟨I, hI, hEq, S, a, l, u, x, ha, hd, hl, hlu, hx, hpos, rfl⟩ := hr
  let _ := hI
  let _ := hEq
  apply (div_le_iff₀ hpos).mpr
  exact degree_gap_bound_on_box d U (fun S a ha hd x hx => hU I S a x ha hd hx)
    S a ha hd l u hl hlu x hx

theorem boxDegreeRatios_bddAbove {d : ℕ} {U : ℝ} (hU : CubeDegreeBound d U) :
    BddAbove (boxDegreeRatios d) := ⟨U, fun _ hr => boxDegreeRatios_le hU hr⟩

theorem boxDimensionRatios_nonempty (n : ℕ) (hn : 8 ≤ n) :
    (boxDimensionRatios n).Nonempty :=
  (dimensionRatios_nonempty n hn).mono (dimensionRatios_subset_boxDimensionRatios n)

theorem boxDegreeRatios_nonempty (n : ℕ) (hn : 8 ≤ n) :
    (boxDegreeRatios n).Nonempty :=
  (degreeRatios_nonempty n hn).mono (degreeRatios_subset_boxDegreeRatios n)

/-- The lower construction and transferred cube upper bound sandwich both
original all-box suprema, using exactly `n` coordinates for the dimension bound. -/
theorem box_suprema_bounds (n : ℕ) (hn : 8 ≤ n) (U : ℝ) (hU : CubeDegreeBound n U) :
    lowerComparison n ≤ boxDimensionSupremum n ∧
      boxDimensionSupremum n ≤ boxDegreeSupremum n ∧ boxDegreeSupremum n ≤ U := by
  have hbd := boxDegreeRatios_bddAbove hU
  have hbn : BddAbove (boxDimensionRatios n) :=
    hbd.mono (boxDimensionRatios_subset_boxDegreeRatios n)
  refine ⟨?_, ?_, ?_⟩
  · exact (lowerComparison_le_ratio n hn).trans
      (le_csSup hbn (dimensionRatios_subset_boxDimensionRatios n
        (witness_ratio_mem_dimensionRatios n hn)))
  · exact csSup_le (boxDimensionRatios_nonempty n hn)
      (fun r hr => le_csSup hbd (boxDimensionRatios_subset_boxDegreeRatios n hr))
  · exact csSup_le (boxDegreeRatios_nonempty n hn) (fun _ hr => boxDegreeRatios_le hU hr)

end
end MultilinearGap
