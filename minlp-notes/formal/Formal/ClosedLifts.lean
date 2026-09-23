import Formal.UpperBounds
import Formal.CountArithmetic
import Formal.LowerBounds

/-! Requiring the lifted convex set to be closed leaves both exact counts unchanged. -/
namespace ExactCounts

variable {n p q : ℕ}

namespace RationalAffine

/-- Every expression in the rational affine syntax is a continuous real function. -/
theorem continuous_eval (e : RationalAffine n p q) : Continuous e.eval := by
  induction e with
  | const r => exact continuous_const
  | visible i j =>
    exact (continuous_apply j).comp ((continuous_apply i).comp continuous_fst)
  | code i => exact (continuous_apply i).comp (continuous_fst.comp continuous_snd)
  | aux i => exact (continuous_apply i).comp (continuous_snd.comp continuous_snd)
  | add e f he hf => exact he.add hf
  | scale r e he => exact continuous_const.mul he

end RationalAffine

/-- Arbitrary intersections of closed rational affine half-spaces are closed. -/
theorem rationalPolyhedron_isClosed {ι : Type} (rows : ι → RationalAffine n p q) :
    IsClosed (rationalPolyhedron rows) := by
  have he : rationalPolyhedron rows = ⋂ i, {y | (rows i).eval y ≤ 0} := by
    ext y
    simp [rationalPolyhedron]
  rw [he]
  exact isClosed_iInter (fun i => isClosed_le (rows i).continuous_eval continuous_const)

/-- A graph representation using a closed convex lifted set and integer coordinates. -/
def HasClosedIntegerLift (n p : ℕ) : Prop :=
  ∃ q, ∃ C : Set (Ambient n p q),
    Convex ℝ C ∧ IsClosed C ∧ Admissible C (IntegerCodes p)

/-- A graph representation using a closed convex lifted set and binary coordinates. -/
def HasClosedBinaryLift (n p : ℕ) : Prop :=
  ∃ q, ∃ C : Set (Ambient n p q),
    Convex ℝ C ∧ IsClosed C ∧ Admissible C (BinaryCodes p)

theorem HasClosedIntegerLift.toHasIntegerLift (h : HasClosedIntegerLift n p) :
    HasIntegerLift n p := by
  obtain ⟨q, C, hc, _, ha⟩ := h
  exact ⟨q, C, hc, ha⟩

theorem HasClosedBinaryLift.toHasBinaryLift (h : HasClosedBinaryLift n p) :
    HasBinaryLift n p := by
  obtain ⟨q, C, hc, _, ha⟩ := h
  exact ⟨q, C, hc, ha⟩

theorem HasRationalIntegerLift.toHasClosedIntegerLift (h : HasRationalIntegerLift n p) :
    HasClosedIntegerLift n p := by
  obtain ⟨q, r, rows, ha⟩ := h
  exact ⟨q, rationalPolyhedron rows, rationalPolyhedron_convex rows,
    rationalPolyhedron_isClosed rows, ha⟩

theorem HasRationalBinaryLift.toHasClosedBinaryLift (h : HasRationalBinaryLift n p) :
    HasClosedBinaryLift n p := by
  obtain ⟨q, r, rows, ha⟩ := h
  exact ⟨q, rationalPolyhedron rows, rationalPolyhedron_convex rows,
    rationalPolyhedron_isClosed rows, ha⟩

/-- The least integer dimension remains exactly the input dimension under closedness. -/
theorem closed_integer_exact_count (n : ℕ) : IsLeast {p | HasClosedIntegerLift n p} n := by
  constructor
  · exact (rational_integer_upper n).toHasClosedIntegerLift
  · intro p hp
    exact integer_lower_bound hp.toHasIntegerLift

/-- Closed convex binary lifts exist exactly when there are enough distinct binary words. -/
theorem closed_binary_lift_iff : HasClosedBinaryLift n p ↔ binaryCount n ≤ p := by
  constructor
  · intro h
    exact binaryCount_le_iff.mpr (binary_lower_bound h.toHasBinaryLift)
  · intro h
    exact (rational_binary_upper (binaryCount_le_iff.mp h)).toHasClosedBinaryLift

/-- The least binary dimension is unchanged when the lifted set must be closed. -/
theorem closed_binary_exact_count (n : ℕ) :
    IsLeast {p | HasClosedBinaryLift n p} (binaryCount n) := by
  constructor
  · exact closed_binary_lift_iff.mpr le_rfl
  · intro p hp
    exact closed_binary_lift_iff.mp hp

end ExactCounts
