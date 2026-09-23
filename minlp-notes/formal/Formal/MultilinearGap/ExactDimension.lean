import Formal.MultilinearGap.Suprema
import Formal.MultilinearGap.Padding

/-! Exactly `n` coordinates and at most `n` coordinates give the same attainable
gap ratios, because unused coordinates preserve both actual envelope widths. -/
namespace MultilinearGap
open CubicGap
noncomputable section

def exactDimensionRatios (n : ℕ) : Set ℝ := {r | ∃ (I : Type) (hI : Fintype I)
    (hEq : DecidableEq I),
  letI := hI
  letI := hEq
  ∃ (S : Finset (Finset I)) (a : Finset I → ℝ) (x : I → ℝ),
    Fintype.card I = n ∧ (∀ s ∈ S, 0 ≤ a s) ∧ x ∈ cube I ∧
      0 < hullGap (supportPolynomial S a) x ∧
      r = weightedTermwiseGap S a x / hullGap (supportPolynomial S a) x}

theorem exactDimensionRatios_eq (n : ℕ) : exactDimensionRatios n = dimensionRatios n := by
  ext r
  constructor
  · rintro ⟨I, hI, hEq, S, a, x, hcard, ha, hx, hpos, hr⟩
    exact ⟨I, hI, hEq, S, a, x, hcard.le, ha, hx, hpos, hr⟩
  · rintro ⟨I, hI, hEq, S, a, x, hcard, ha, hx, hpos, hr⟩
    let _ := hI
    let _ := hEq
    let J := Fin (n - Fintype.card I)
    refine ⟨I ⊕ J, inferInstance, inferInstance, padSupports S, padCoefficient a,
      padPoint x, padded_card n hcard, padSupports_nonnegative S a ha,
      padPoint_mem_cube x hx, ?_, ?_⟩
    · simpa only [padSupports_hullGap] using hpos
    · simpa only [padSupports_hullGap, padSupports_weightedTermwiseGap] using hr

end
end MultilinearGap
