import Formal.ReciprocalAnchor.ManyFastEvaluation
import Formal.ReciprocalAnchor.ManyResults

/-! Executable exact rational membership in the actual many-leaf graph hull. -/
namespace ReciprocalAnchor.ManyLeaf

/-- The finite affine bounds, evaluated using exact rational arithmetic. -/
def rationalLinearBounds {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) : Prop :=
  a ≤ m ∧ m ≤ b ∧ ∀ j, 0 ≤ q j ∧ q j ≤ 1 ∧
    a * q j ≤ w j ∧ w j ≤ b * q j ∧
    a * (1 - q j) ≤ m - w j ∧ m - w j ≤ b * (1 - q j)

instance {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) :
    Decidable (rationalLinearBounds a b m q w) := by
  unfold rationalLinearBounds
  infer_instance

theorem rationalLinearBounds_cast {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) :
    rationalLinearBounds a b m q w ↔
      LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) := by
  unfold rationalLinearBounds LinearBounds
  dsimp only
  norm_cast

/-- A total Boolean checker. Correctness assumes the source domain `0 < a < b`. -/
def rationalMembership {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) : Bool :=
  decide (rationalLinearBounds a b m q w ∧
    FastEnvelope.fastLowerMoment a b m q w ≤ t ∧ t ≤ (a + b - m) / (a * b))

theorem rationalMembership_correct {n : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (ha : 0 < a) (hab : a < b) :
    rationalMembership a b m t q w = true ↔
      point (m : ℝ) t (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) ∈ hull n a b := by
  rw [mem_hull_iff_bounds (by exact_mod_cast ha) (by exact_mod_cast hab)]
  simp only [rationalMembership, decide_eq_true_eq]
  rw [rationalLinearBounds_cast]
  have he := FastEnvelope.fastLowerMoment_eq (m := m) (q := q) (w := w) ha hab.le
  rw [← he]
  norm_cast

end ReciprocalAnchor.ManyLeaf
