import QipmFormal.Refresh.Core
import QipmFormal.Refresh.Counting
import QipmFormal.Refresh.LeastSquares

/-!
# Pathwise residual-certified refresh: manuscript theorem

The cost used by the checkpoint recurrence is the actual least-squares
relative residual. The stored vector at a time that never becomes a
checkpoint is irrelevant. Accuracy is required only at realized checkpoints.
All systems and vectors describe one realized path, so the theorem makes
no independence or nonadaptivity assumption.
-/

namespace QipmFormal.Refresh

noncomputable section
open scoped BigOperators

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The scalar selected when testing the vector stored at checkpoint `s`. -/
def reuseScalar (H : ℕ → E ≃L[ℝ] E) (f stored : ℕ → E) (s t : ℕ) : ℝ :=
  scalarLeastSquares (H t (stored s)) (f t)

/-- The actual relative residual of the best scalar multiple of the stored vector. -/
def reuseCost (H : ℕ → E ≃L[ℝ] E) (f stored : ℕ → E) (s t : ℕ) : ℝ :=
  ‖H t (reuseScalar H f stored s t • stored s) - f t‖ / ‖f t‖

theorem reuseCost_le_candidate (H : ℕ → E ≃L[ℝ] E) (f stored : ℕ → E)
    (s t : ℕ) (a : ℝ) :
    reuseCost H f stored s t ≤ ‖H t (a • stored s) - f t‖ / ‖f t‖ := by
  unfold reuseCost reuseScalar
  simp only [map_smul]
  exact div_le_div_of_nonneg_right
    (scalarLeastSquares_minimizes (H t (stored s)) (f t) a) (norm_nonneg _)

theorem reuseCost_bound (H : ℕ → E ≃L[ℝ] E) (f stored : ℕ → E)
    (s t : ℕ) (hf : ∀ j, j ≤ t → f j ≠ 0) (hst : s ≤ t) (epsilon G : ℝ)
    (haccuracy : ‖H s (stored s) - f s‖ / ‖f s‖ ≤ epsilon)
    (hgain : ∀ j, s ≤ j → j ≤ t →
      ‖(normalizedOperator H f t).comp (normalizedInverse H f j)‖ ≤ G) :
    reuseCost H f stored s t ≤
      G * (epsilon + ∑ j ∈ Finset.Ico s t, stepVariation H f j) := by
  exact (reuseCost_le_candidate H f stored s t
    (solutionNorm H f t / solutionNorm H f s)).trans
      (candidate_residual_bound_on H f s t hf hst (stored s) epsilon G haccuracy hgain)

/-- The manuscript's headline inequality for the actual sequential policy.
`refreshCount` includes the solve at time zero. The gain is required through
the current test even when that test fails and triggers a new solve. -/
theorem paper_refresh_bound (H : ℕ → E ≃L[ℝ] E) (f stored : ℕ → E)
    (T : ℕ) (hf : ∀ t, t ≤ T → f t ≠ 0) (epsilon eta G : ℝ)
    (hG : 0 < G) (heta : 0 < eta) (hepsilon : epsilon ≤ eta / (2 * G))
    (haccuracy : ∀ t ≤ T,
      let s := checkpoint (reuseCost H f stored) eta t
      ‖H s (stored s) - f s‖ / ‖f s‖ ≤ epsilon)
    (hgain : ∀ t < T, ∀ j,
      checkpoint (reuseCost H f stored) eta t ≤ j → j ≤ t + 1 →
      ‖(normalizedOperator H f (t + 1)).comp (normalizedInverse H f j)‖ ≤ G) :
    (refreshCount (reuseCost H f stored) eta T : ℝ) ≤
      1 + 2 * G * (∑ j ∈ Finset.range T, stepVariation H f j) / eta := by
  apply refresh_count_bound hG heta hepsilon
  · intro j _
    exact norm_nonneg _
  · intro t ht
    exact reuseCost_bound H f stored _ (t + 1) (fun j hj => hf j (by omega))
      ((checkpoint_le _ _ t).trans (Nat.le_succ t)) epsilon G
      (haccuracy t (Nat.le_of_lt ht)) (hgain t ht)

end

end QipmFormal.Refresh
