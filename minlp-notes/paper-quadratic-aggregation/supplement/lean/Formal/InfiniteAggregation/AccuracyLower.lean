import Formal.InfiniteAggregation.AccuracyModel
import Formal.InfiniteAggregation.AccuracyConstants
import Formal.InfiniteAggregation.AccuracyLowerGap
import Formal.InfiniteAggregation.AccuracyLowerPigeonhole
import Formal.InfiniteAggregation.AccuracyLowerLipschitz

/-! The uniform lower bound for arbitrary finite families of actual good cuts.

The proof uses `N + 1` equally spaced witnesses. A discriminant estimate shows
that one cut can exclude at most one witness. This gives a slightly stronger
rational constant than the logarithmic covering argument in the source note.
-/

noncomputable section
namespace InfiniteAggregation

/-- Every admissible family of at most `N` inequalities admits an actual Gram
witness separated from every point of the closed hull in Euclidean distance. -/
theorem accuracy_lower_witness {r N : ℕ} (hr : 2 ≤ r) (hN : 1 ≤ N)
    (W : Finset Weight) (hW : admissibleFamily r W) (hcard : W.card ≤ N) :
    ∃ x ∈ relaxation W, ∀ y ∈ closedRegion r,
      1 / (2000 * (N : ℝ) ^ 2) ≤ euclideanDist x y := by
  have hNp : 0 < N := by omega
  have hNr : (1 : ℝ) ≤ N := by exact_mod_cast hN
  let η : ℝ := 1 / (400 * (N : ℝ) ^ 2)
  have hη : 0 ≤ η := by dsimp [η]; positivity
  have hηlt : η < 1 / 10 := by
    dsimp [η]
    apply (div_lt_iff₀ (by positivity)).2
    nlinarith
  let slack (w : Weight) (i : Fin (N + 1)) : ℝ :=
    (1 / 10) * (-w 0 / accuracyGrid N i - w 1 * accuracyGrid N i + w 2) + w 2 * η
  obtain ⟨i, hi⟩ := exists_unviolated_of_card_le W hcard (fun w i => 0 < slack w i) (by
    intro w hw i j hi hj
    have hK := ((good_iff_goodCone hr w).1 (hW w hw)).1
    by_contra hij
    have hgap := positive_perturbed_slacks_gap (hK.1 0) (hK.1 1) (hK.1 2) hK.2
      (accuracyGrid_mem_Icc hNp i) (accuracyGrid_mem_Icc hNp j) hNr
      (by simpa [slack, η, div_eq_mul_inv] using hi)
      (by simpa [slack, η, div_eq_mul_inv] using hj)
    exact (not_lt_of_ge (accuracyGrid_separated hNp hij)) hgap)
  let τ := accuracyGrid N i
  have hτ : τ ∈ Set.Icc (1 : ℝ) 2 := accuracyGrid_mem_Icc hNp i
  have ht : 0 < τ := by linarith [hτ.1]
  obtain ⟨hp, hdet⟩ := perturbed_gram_bounds hτ hη hηlt
  obtain ⟨u, v, hu, hv, huv⟩ := gram_realization hr hp hdet.le
  let x : Var r := (u, v)
  have hx : x ∈ relaxation W := by
    intro w hw
    rw [perturbed_aggregate_formula w hu hv huv]
    exact le_of_not_gt (hi w hw)
  have hxu : qnorm x.1 ≤ 1 := by
    change qnorm u ≤ 1
    rw [hu]
    have : 0 ≤ (1 / 10 : ℝ) / τ := by positivity
    linarith
  have hxv : qnorm x.2 ≤ 1 := by
    change qnorm v ≤ 1
    rw [hv]
    nlinarith
  have hval : aggregate (rayWeight τ) x = 2 * η := by
    rw [perturbed_aggregate_formula (rayWeight τ) hu hv huv]
    simp [rayWeight]
    field_simp
    ring
  refine ⟨x, hx, ?_⟩
  intro y hy
  have hyh : y ∈ closure (convexHull ℝ (feasible r)) := by
    rwa [closure_convexHull_feasible_eq_closedRegion hr]
  have hyval := goodCone_closedHull_valid (rayWeight_goodCone ht) (rayWeight_ne_zero τ) hyh
  have hD : 0 ≤ euclideanDist x y := dist_nonneg
  have hd := euclideanDist_sq x y
  have hdu : qnorm (x.1 - y.1) ≤ euclideanDist x y ^ 2 := by
    linarith [qnorm_nonneg (x.2 - y.2)]
  have hdv : qnorm (x.2 - y.2) ≤ euclideanDist x y ^ 2 := by
    linarith [qnorm_nonneg (x.1 - y.1)]
  have hlip := accuracy_ray_lipschitz hτ x y hD hxu hxv hy.1 hy.2.1 hdu hdv
  have hdiff := le_abs_self (aggregate (rayWeight τ) x - aggregate (rayWeight τ) y)
  rw [hval] at hlip hdiff
  have hsep : η / 5 ≤ euclideanDist x y := by linarith
  have heq : η / 5 = 1 / (2000 * (N : ℝ) ^ 2) := by dsimp [η]; ring
  rwa [heq] at hsep

/-- A stronger rational lower bound, valid also for unbounded relaxations. -/
theorem rational_lower_le_hausdorffError {r N : ℕ} (hr : 2 ≤ r) (hN : 1 ≤ N)
    (W : Finset Weight) (hW : admissibleFamily r W) (hcard : W.card ≤ N) :
    ENNReal.ofReal (1 / (2000 * (N : ℝ) ^ 2)) ≤ hausdorffError r W := by
  obtain ⟨x, hx, hsep⟩ := accuracy_lower_witness hr hN W hW hcard
  exact le_hausdorffError_of_witness hx hsep

/-- The source lower constant for every arbitrary admissible cut family. -/
theorem accuracy_lower_le_hausdorffError {r N : ℕ} (hr : 2 ≤ r) (hN : 1 ≤ N)
    (W : Finset Weight) (hW : admissibleFamily r W) (hcard : W.card ≤ N) :
    ENNReal.ofReal (accuracyLowerBound N) ≤ hausdorffError r W :=
  (ENNReal.ofReal_le_ofReal (accuracyLowerBound_le_rational_plain (by omega))).trans
    (rational_lower_le_hausdorffError hr hN W hW hcard)

/-- The source's exact lower constant bounds the infimum over all good cut families. -/
theorem accuracy_lower_le_optimalError {r N : ℕ} (hr : 2 ≤ r) (hN : 1 ≤ N) :
    ENNReal.ofReal (accuracyLowerBound N) ≤ optimalError r N := by
  apply le_optimalError
  intro W hW hcard
  exact accuracy_lower_le_hausdorffError hr hN W hW hcard

end InfiniteAggregation
