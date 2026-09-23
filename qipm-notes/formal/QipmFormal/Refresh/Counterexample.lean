import QipmFormal.Refresh.Paper

/-!
# Safe acceptance alone does not control refresh counts

A conservative test may reject every cached vector even though the true
minimum residual is zero. This satisfies acceptance safety but violates the
claimed count at zero projective variation. It explains the correction to
the archived feasible-OSS reuse note.
-/

namespace QipmFormal.Refresh.Counterexample

noncomputable section
open scoped BigOperators

def identitySystems : ℕ → ℝ ≃L[ℝ] ℝ := fun _ => ContinuousLinearEquiv.refl ℝ ℝ

def unitRhs : ℕ → ℝ := fun _ => 1

theorem unitRhs_ne_zero (t : ℕ) : unitRhs t ≠ 0 := by simp [unitRhs]

theorem constant_stepVariation (j : ℕ) : stepVariation identitySystems unitRhs j = 0 := by
  simp [stepVariation, ray, solutionNorm, solution, identitySystems, unitRhs]

theorem constant_reuseCost (s t : ℕ) : reuseCost identitySystems unitRhs unitRhs s t = 0 := by
  simp [reuseCost, reuseScalar, scalarLeastSquares, identitySystems, unitRhs]

theorem constant_checkpoint_residual (t : ℕ) :
    ‖identitySystems t (unitRhs t) - unitRhs t‖ / ‖unitRhs t‖ = 0 := by
  simp [identitySystems]

theorem constant_cross_gain (t j : ℕ) :
    ‖(normalizedOperator identitySystems unitRhs t).comp
      (normalizedInverse identitySystems unitRhs j)‖ ≤ 1 := by
  simp [normalizedOperator, normalizedInverse, solutionNorm, solution, identitySystems, unitRhs]

/-- The proxy reports 2 at threshold 1, forcing a solve at every test. -/
theorem rejecting_proxy_count (T : ℕ) :
    refreshCount (fun _ _ => 2) 1 T = T + 1 := by
  induction T with
  | zero => rfl
  | succ n ih => simp [refreshCount, ih]

/-- Safe acceptance does not imply the refresh bound, even for a constant
one-dimensional identity system with exact stored solutions. -/
theorem safe_acceptance_only_counterexample (T : ℕ) (hT : 0 < T) :
    (∀ s t : ℕ, (2 : ℝ) ≤ 1 → reuseCost identitySystems unitRhs unitRhs s t ≤ 1) ∧
      (refreshCount (fun _ _ => 2) 1 T : ℝ) >
        1 + 2 * 1 * (∑ j ∈ Finset.range T, stepVariation identitySystems unitRhs j) / 1 := by
  constructor
  · intro s t _
    rw [constant_reuseCost]
    norm_num
  · simp only [constant_stepVariation, Finset.sum_const_zero, mul_zero, zero_div, add_zero]
    rw [rejecting_proxy_count]
    exact_mod_cast (show 1 < T + 1 by omega)

end

end QipmFormal.Refresh.Counterexample
