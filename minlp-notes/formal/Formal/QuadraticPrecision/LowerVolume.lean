import Formal.QuadraticPrecision.LowerContact
open MeasureTheory
open scoped BigOperators
namespace QuadraticPrecision

/-- The finite parity cover gives an actual volume obstruction for any convex
integer lift, with no regularity requirements on the lift carrier. -/
theorem graph_quadratic_volume_bound {d p : ℕ} {D : Set (Input d)}
    (hD : IsCompact D) (M : Matrix (Fin d) (Fin d) ℝ) (hM : M.IsSymm)
    (hdet : M.det ≠ 0) (a : Fin d → ℝ) (b ε : ℝ) (hε : 0 ≤ ε)
    (h : HasGraphLift D (quadraticPolynomial M a b) ε p) :
    volume D ≤ ENNReal.ofReal ((2:ℝ)^p * ((2:ℝ)^d *
      (12 * Real.sqrt d * ε)^((d:ℝ)/2) / Real.sqrt |M.det|)) := by
  obtain ⟨S,hc,_,hcover,he⟩ := graph_quadratic_parity_cover hD M a b ε h
  calc
    volume D ≤ volume (⋃ α, S α) := measure_mono hcover
    _ ≤ ∑ α, volume (S α) := measure_iUnion_fintype_le volume S
    _ ≤ ∑ _α : ParityCode p, ENNReal.ofReal ((2:ℝ)^d *
        (12 * Real.sqrt d * ε)^((d:ℝ)/2) / Real.sqrt |M.det|) := by
      apply Finset.sum_le_sum
      intro α _
      have heq : 3 * Real.sqrt d * (4*ε) = 12 * Real.sqrt d * ε := by ring
      simpa only [heq] using contact_volume_bound M hM hdet (hc α)
        (by positivity : 0 ≤ 4*ε) (he α)
    _ = _ := by
      rw [Finset.sum_const, Finset.card_univ, card_parityCode, nsmul_eq_mul]
      rw [← ENNReal.ofReal_natCast, ← ENNReal.ofReal_mul (by positivity)]
      simp
end QuadraticPrecision
