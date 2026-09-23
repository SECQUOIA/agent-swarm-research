import Formal.AffineShear
import Formal.MonotonePolynomial

/-! The monotone family and the quantitative separation stated in the exact-count note. -/
namespace ExactCounts
noncomputable section

/-- The shear at 56 is exactly the specified monotone polynomial graph. -/
theorem shearedGraph_monotone {n : ℕ} (x : Fin n → ℝ) :
    ShearedGraph 56 x = fun i => ![x i, monotoneLeftValue (x i), rightValue (x i)] := by
  rfl

/-- The entire monotone variant, including its rational linear-size realization. -/
theorem monotone_exact_box_counts (n : ℕ) :
    ConvexOn ℝ (Set.Icc 0 1) monotoneLeftValue ∧
    ConvexOn ℝ (Set.Icc 0 1) rightValue ∧
    MonotoneOn monotoneLeftValue (Set.Icc 0 1) ∧
    MonotoneOn rightValue (Set.Icc 0 1) ∧
    monotoneLeftPoly.natDegree = 32 ∧ rightPoly.natDegree = 32 ∧
    IsLeast {p | HasShearedLift (n := n) 56 (IntegerCodes p)} n ∧
    IsLeast {p | HasShearedLift (n := n) 56 (BinaryCodes p)} (binaryCount n) ∧
    IsLeast {p | HasClosedShearedLift (n := n) 56 (IntegerCodes p)} n ∧
    IsLeast {p | HasClosedShearedLift (n := n) 56 (BinaryCodes p)} (binaryCount n) ∧
    IsLeast {p | HasRationalShearedLift (n := n) 56 (IntegerCodes p)} n ∧
    IsLeast {p | HasRationalShearedLift (n := n) 56 (BinaryCodes p)} (binaryCount n) ∧
    (∃ rows : Fin (13 * n) → RationalAffine n n (n * 3),
      ShearedAdmissible 56 (rationalPolyhedron rows) (IntegerCodes n)) := by
  obtain ⟨hi, hb, hci, hcb, hri, hrb⟩ := sheared_exact_counts 56 n
  exact ⟨monotoneLeftValue_convex, rightValue_convex, monotoneLeftValue_monotone,
    rightValue_monotone, monotoneLeftPoly_natDegree, rightPoly_natDegree,
    hi, hb, hci, hcb, hri, hrb, sheared_integer_linear_size 56 n⟩

/-- The one-input example requires one general integer and two binary coordinates. -/
theorem one_input_exact_counts :
    IsLeast {p | HasIntegerLift 1 p} 1 ∧ IsLeast {p | HasBinaryLift 1 p} 2 := by
  simpa using And.intro (integer_count_exact 1) (binary_count_exact 1)

/-- Exact additive gap between the two minima, with subtraction in the integers. -/
theorem count_gap_formula (n : ℕ) :
    (binaryCount n : ℤ) - n = ⌈(n : ℝ) * Real.logb 2 3⌉ - n := by
  rw [binaryCount_eq_intCeil]

/-- The gap differs from n(log₂ 3 − 1) by less than one. -/
theorem count_gap_linear_bounds (n : ℕ) :
    (n : ℝ) * (Real.logb 2 3 - 1) ≤ (binaryCount n : ℝ) - n ∧
    (binaryCount n : ℝ) - n < (n : ℝ) * (Real.logb 2 3 - 1) + 1 := by
  have he : (binaryCount n : ℝ) = (⌈(n : ℝ) * Real.logb 2 3⌉ : ℤ) := by
    exact_mod_cast binaryCount_eq_intCeil n
  rw [he]
  have hl := Int.le_ceil ((n : ℝ) * Real.logb 2 3)
  have hu := Int.ceil_lt_add_one ((n : ℝ) * Real.logb 2 3)
  constructor <;> nlinarith

/-- A positive linear slope, rather than only strict separation at each dimension. -/
theorem count_gap_slope_pos : 0 < Real.logb 2 3 - 1 := by
  have h : Real.logb (2 : ℝ) 2 < Real.logb 2 3 :=
    Real.logb_lt_logb (by norm_num) (by norm_num) (by norm_num)
  norm_num at h ⊢
  linarith

end
end ExactCounts
