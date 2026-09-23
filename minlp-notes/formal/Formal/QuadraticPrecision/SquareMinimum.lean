import Formal.QuadraticPrecision.SquareLift
import Formal.QuadraticPrecision.PrecisionArithmetic

/-! Exact least counts, including equality at the error threshold. -/
namespace QuadraticPrecision
noncomputable section

theorem squareWidth_sq (p : ℕ) : (squareWidth p)^2 = (1 / 4 : ℝ)^p := by
  unfold squareWidth
  rw [← pow_mul, Nat.mul_comm p 2, pow_mul]
  norm_num

theorem square_binary_feasible_iff {ε : ℝ} (hε : 0 < ε) (p : ℕ) :
    HasBinaryGraphLift unitIntervalDomain squareOne ε p ↔ squarePrecisionCount ε ≤ p := by
  constructor
  · intro h
    exact square_graph_count_lower hε h.toInteger
  · intro h
    have hupper := square_hasBinaryGraphLift p
    have herr := (squarePrecisionCount_le_iff hε p).mp h
    rw [← squareWidth_sq] at herr
    exact hupper.mono_error herr

theorem square_integer_feasible_iff {ε : ℝ} (hε : 0 < ε) (p : ℕ) :
    HasGraphLift unitIntervalDomain squareOne ε p ↔ squarePrecisionCount ε ≤ p :=
  ⟨square_graph_count_lower hε,
    fun h => ((square_binary_feasible_iff hε p).mpr h).toInteger⟩

theorem square_binary_minimum {ε : ℝ} (hε : 0 < ε) :
    IsMinimumCount (HasBinaryGraphLift unitIntervalDomain squareOne ε)
      (squarePrecisionCount ε) :=
  ⟨(square_binary_feasible_iff hε _).mpr le_rfl,
    fun p hp => (square_binary_feasible_iff hε p).mp hp⟩

theorem square_integer_minimum {ε : ℝ} (hε : 0 < ε) :
    IsMinimumCount (HasGraphLift unitIntervalDomain squareOne ε)
      (squarePrecisionCount ε) :=
  ⟨(square_integer_feasible_iff hε _).mpr le_rfl,
    fun p hp => (square_integer_feasible_iff hε p).mp hp⟩

theorem square_no_exact_integer_lift (p : ℕ) :
    ¬HasGraphLift unitIntervalDomain squareOne 0 p := by
  intro h
  have hb := square_graph_integer_lower h
  have : 0 < (1 / 4 : ℝ)^p / 4 := by positivity
  linarith

end
end QuadraticPrecision
