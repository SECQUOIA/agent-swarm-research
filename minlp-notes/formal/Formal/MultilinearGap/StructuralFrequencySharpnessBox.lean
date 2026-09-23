import Formal.MultilinearGap.StructuralFrequencySharpness
import Formal.MultilinearGap.StructuralFrequencyBox

/-! Exact odd-cycle sharpness on every fixed positive aspect-ratio box. -/
namespace MultilinearGap.StructuralFrequencyCycle
open CubicGap
noncomputable section

/-- Every original factor of the cycle polynomial is bilinear. -/
theorem supports_card_two (k : ℕ) (s : Finset (Cycle k)) (hs : s ∈ supports k) :
    s.card = 2 := by
  obtain ⟨v, _, rfl⟩ := Finset.mem_image.mp hs
  exact support_card k v

/-- The actual physical hull gap is the cycle hull gap times the common
positive bilinear scaling factor. -/
theorem positiveBox_hullGap (k : ℕ) (rho : ℝ) (hrho : 1 ≤ rho) :
    boxHullGap (fun _ => 1) (fun _ => rho) (polynomial k)
      (boxPoint (fun _ => 1) (fun _ => rho) (meanPoint k)) =
      (rho - 1)^2 * ((k : ℝ) + 1) := by
  rw [polynomial, boxHullGap_bilinear rho hrho (supports k) (fun _ => 1)
    (supports_card_two k) (meanPoint k) (meanPoint_mem_cube k)]
  change _ * hullGap (polynomial k) (meanPoint k) = _
  rw [polynomial_hullGap]

/-- Every original term receives the same scaling, without adding supports. -/
theorem positiveBox_termwiseGap (k : ℕ) (rho : ℝ) (hrho : 1 ≤ rho) :
    boxTermwiseGap (supports k) (fun _ => 1) (fun _ => 1) (fun _ => rho)
      (boxPoint (fun _ => 1) (fun _ => rho) (meanPoint k)) =
      (rho - 1)^2 * ((2 * (k : ℝ) + 3) / 2) := by
  rw [boxTermwiseGap_bilinear rho hrho (supports k) (fun _ => 1)
    (supports_card_two k) (meanPoint k) (meanPoint_mem_cube k), polynomial_termwiseGap]

/-- Sharpness survives every fixed aspect ratio strictly greater than one. -/
theorem positiveBox_ratio (k : ℕ) (rho : ℝ) (hrho : 1 < rho) :
    boxTermwiseGap (supports k) (fun _ => 1) (fun _ => 1) (fun _ => rho)
      (boxPoint (fun _ => 1) (fun _ => rho) (meanPoint k)) /
    boxHullGap (fun _ => 1) (fun _ => rho) (polynomial k)
      (boxPoint (fun _ => 1) (fun _ => rho) (meanPoint k)) =
      (2 * (k : ℝ) + 3) / (2 * (k : ℝ) + 2) := by
  rw [positiveBox_termwiseGap k rho hrho.le, positiveBox_hullGap k rho hrho.le]
  have hscale : (rho - 1)^2 ≠ 0 := pow_ne_zero 2 (by linarith)
  rw [mul_div_mul_left _ _ hscale]
  have hk : (k : ℝ) + 1 ≠ 0 := by positivity
  have hk' : 2 * (k : ℝ) + 2 ≠ 0 := by positivity
  field_simp

end
end MultilinearGap.StructuralFrequencyCycle
