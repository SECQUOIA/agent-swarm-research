import Formal.QuadraticAggregation.Model

/-!
# Equivalent sequence formulation of asymptotic hyperplane convexity

The source note asks for a strictly increasing sequence of good levels tending
 to positive infinity. The model uses the equivalent unbounded-level property.
-/

open Filter Set

namespace QuadraticAggregation

/-- Every unbounded set of real numbers contains a strictly increasing sequence
that tends to positive infinity. -/
theorem exists_strictMono_tendsto_atTop_of_unbounded {P : ℝ → Prop}
    (h : ∀ R : ℝ, ∃ s, R < s ∧ P s) :
    ∃ s : ℕ → ℝ, StrictMono s ∧ Tendsto s atTop atTop ∧ ∀ k, P (s k) := by
  classical
  choose f hf hP using h
  let s : ℕ → ℝ := Nat.rec (f 0) (fun k sk => f (max sk (k + 1 : ℝ)))
  have hzero : s 0 = f 0 := rfl
  have hsucc (k : ℕ) : s (k + 1) = f (max (s k) (k + 1 : ℝ)) := rfl
  have hbound (k : ℕ) : (k : ℝ) < s k := by
    cases k with
    | zero => simpa only [hzero, Nat.cast_zero] using hf 0
    | succ k =>
      rw [hsucc, Nat.cast_add, Nat.cast_one]
      exact lt_of_le_of_lt (le_max_right _ _) (hf _)
  refine ⟨s, strictMono_nat_of_lt_succ ?_, ?_, ?_⟩
  · intro k
    rw [hsucc]
    exact lt_of_le_of_lt (le_max_left _ _) (hf _)
  · exact tendsto_atTop_mono (fun k => (hbound k).le) tendsto_natCast_atTop_atTop
  · intro k
    cases k with
    | zero => exact hP 0
    | succ k => exact hP _

variable {n m : ℕ}

/-- The sequence formulation from the source note, including strict increase. -/
def System.AsymptoticHCSequence (D : System n m) : Prop :=
  ∀ α : Vec n, α ≠ 0 → ∃ s : ℕ → ℝ,
    StrictMono s ∧ Tendsto s atTop atTop ∧
      ∀ k, Convex ℝ (D.homEval '' hyperplane α (s k))

theorem System.asymptoticHC_iff_sequence (D : System n m) :
    D.AsymptoticHC ↔ D.AsymptoticHCSequence := by
  constructor
  · intro h α hα
    exact exists_strictMono_tendsto_atTop_of_unbounded (h α hα)
  · intro h α hα R
    obtain ⟨s, _, hs, hc⟩ := h α hα
    obtain ⟨k, hk⟩ := ((tendsto_atTop.1 hs) (R + 1)).exists
    exact ⟨s k, by linarith, hc k⟩

end QuadraticAggregation
