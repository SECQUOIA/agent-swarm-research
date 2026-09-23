import Formal.NetworkSimplex.ThresholdCoefficientBound
import Formal.NetworkSimplex.ThresholdPreprocessCriterion
import Formal.NetworkSimplex.ThresholdRowOccurrences
import Formal.NetworkSimplex.ThresholdBranchValidity

/-! Determinant coefficient bounds for literal original-coordinate source branches. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open NetworkSimplex.Threshold

/-- The coefficients being bounded belong to the actual affine source expressions. -/
theorem sourceBranch_coefficient_bound {I : Type*} [DecidableEq I] {m s : ℕ}
    (D : ReductionData m I) (rows : Fin s → ProfileRow m I) (p : Fin s → ℕ)
    (hs : s ≤ m + 1) (hp : ∀ i, p i ≤ delta01 m)
    (z : Coordinate m I) (hz : FlowOrProduct z) :
    |∑ i, (p i : ℤ) * rowCoefficient D (rows i) z| ≤
      ((m + 1) * delta01 m : ℕ) := by
  apply weighted_coefficient_abs_le p (fun i => rowCoefficient D (rows i) z)
    (by simpa using hs) hp
  intro i
  have h := row_flow_product_unit D (rows i) z hz
  have ha : |rowCoefficient D (rows i) z| ≤ 1 := abs_le.mpr h
  rw [← Int.natCast_natAbs] at ha
  exact_mod_cast ha

/-- Every branch selected by an actual compiled circuit has the advertised bound. -/
theorem compiledBranch_coefficient_bound {I : Type*} [DecidableEq I] {m N : ℕ}
    (D : ReductionData m I) (A : Matrix (Fin N) (Fin m) ℤ) (hA : RowSignedZeroOne A)
    (c : CompiledCircuit m N) (hc : c ∈ preprocessCircuits A)
    (rows : Fin (c.candidate.size.val + 1) → ProfileRow m I)
    (z : Coordinate m I) (hz : FlowOrProduct z) :
    |∑ i, (c.weight i : ℤ) * rowCoefficient D (rows i) z| ≤
      ((m + 1) * delta01 m : ℕ) :=
  sourceBranch_coefficient_bound D rows c.weight (by omega)
    (fun i => (preprocessCircuits_sound A hA hc).1 i |>.2) z hz

/-- A fixed integer cancellation branch is valid at every point in the original hull. -/
theorem sourceBranch_nonneg_of_hull {L m s : ℕ} (D : ReductionData m (Fin L))
    (rows : Fin s → ProfileRow m (Fin L)) (p : Fin s → ℕ)
    (hcancel : ∀ j, ∑ i, (p i : ℤ) * normalVector (D.rowNormal (rows i)) j = 0)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (h : D.graphPoint ∈ convexHull ℝ D.graph) :
    0 ≤ ∑ i, (p i : ℝ) * D.rowRhs (rows i) := by
  obtain ⟨x, hx⟩ := (D.exists_fullProfile_iff_rows hc hh).mp ((D.mem_hull_iff.mp h).2)
  exact integer_cancel_valid (fun r => normalVector (D.rowNormal r)) D.rowRhs rows p
    hcancel (x := x) (fun r => by
      simpa only [← profileNormal_value_eq_dot] using hx r)

/-- Zero-normal source rows also satisfy the general coefficient bound. -/
theorem sourceRow_coefficient_bound {I : Type*} [DecidableEq I] {m : ℕ}
    (D : ReductionData m I) (r : ProfileRow m I) (z : Coordinate m I)
    (hz : FlowOrProduct z) :
    |rowCoefficient D r z| ≤ ((m + 1) * delta01 m : ℕ) := by
  have hunit := abs_le.mpr (row_flow_product_unit D r z hz)
  have hbound : 1 ≤ (m + 1) * delta01 m :=
    (one_le_delta01 m).trans (Nat.le_mul_of_pos_left _ (by omega))
  exact hunit.trans (by exact_mod_cast hbound)

end NetworkSimplex.Chain.Threshold
