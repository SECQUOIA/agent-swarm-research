import Formal.LowerBounds
import Formal.UpperBounds
import Formal.CountArithmetic
import Formal.PolynomialFamily

/-! Final, unconditional minimum-count statements for the degree-32 family.

`HasBinaryLift` permits arbitrary convex lifts, so its lower bound is stronger
than the manuscript's polyhedral-binary lower bound. The rational affine upper
constructions also establish the minima in the rational MILP class.
-/
namespace ExactCounts

/-- Exact minimum over every convex integer lift, with no bound on integer ranges. -/
theorem integer_count_exact (n : ℕ) : IsLeast {p | HasIntegerLift n p} n :=
  ⟨integer_upper n, fun _ h => integer_lower_bound h⟩

/-- The same integer minimum is attained by a rational MILP. -/
theorem rational_integer_count_exact (n : ℕ) :
    IsLeast {p | HasRationalIntegerLift n p} n :=
  ⟨rational_integer_upper n, fun _ h => integer_lower_bound h.toHasIntegerLift⟩

/-- Complete characterization of feasible binary counts for arbitrary convex lifts. -/
theorem binary_lift_iff {n p : ℕ} :
    HasBinaryLift n p ↔ binaryCount n ≤ p :=
  ⟨fun h => binaryCount_le_iff.mpr (binary_lower_bound h),
    fun h => binary_upper (binaryCount_le_iff.mp h)⟩

/-- The same characterization already holds for finite rational linear systems. -/
theorem rational_binary_lift_iff {n p : ℕ} :
    HasRationalBinaryLift n p ↔ binaryCount n ≤ p :=
  ⟨fun h => binary_lift_iff.mp h.toHasBinaryLift,
    fun h => rational_binary_upper (binaryCount_le_iff.mp h)⟩

theorem binary_count_exact (n : ℕ) :
    IsLeast {p | HasBinaryLift n p} (binaryCount n) :=
  ⟨binary_lift_iff.mpr le_rfl, fun _ h => binary_lift_iff.mp h⟩

theorem rational_binary_count_exact (n : ℕ) :
    IsLeast {p | HasRationalBinaryLift n p} (binaryCount n) :=
  ⟨rational_binary_lift_iff.mpr le_rfl, fun _ h => rational_binary_lift_iff.mp h⟩

/-- The manuscript's logarithmic binary count, attained within rational MILP. -/
theorem rational_binary_count_logarithmic (n : ℕ) :
    IsLeast {p | HasRationalBinaryLift n p} ⌈(n : ℝ) * Real.logb 2 3⌉₊ := by
  rw [← binaryCount_eq_natCeil]
  exact rational_binary_count_exact n

/-- Both exact counts, rational realizations, and an explicit linear-size integer lift. -/
theorem exact_box_counts (n : ℕ) :
    IsLeast {p | HasIntegerLift n p} n ∧
    IsLeast {p | HasBinaryLift n p} (binaryCount n) ∧
    IsLeast {p | HasRationalIntegerLift n p} n ∧
    IsLeast {p | HasRationalBinaryLift n p} (binaryCount n) ∧
    (binaryCount n : ℤ) = ⌈(n : ℝ) * Real.logb 2 3⌉ ∧
    (∃ rows : Fin (13 * n) → RationalAffine n n (n * 3),
      Admissible (rationalPolyhedron rows) (IntegerCodes n)) :=
  ⟨integer_count_exact n, binary_count_exact n, rational_integer_count_exact n,
    rational_binary_count_exact n, binaryCount_eq_intCeil n, integer_upper_linear_size n⟩

/-- The separation is strict in every positive input dimension. -/
theorem strict_count_separation {n : ℕ} (hn : 1 ≤ n) :
    HasRationalIntegerLift n n ∧ ¬ HasBinaryLift n n := by
  refine ⟨rational_integer_upper n, ?_⟩
  intro h
  exact (not_le_of_gt (lt_binaryCount hn)) (binary_lift_iff.mp h)

end ExactCounts
