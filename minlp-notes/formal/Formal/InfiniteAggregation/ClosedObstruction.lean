import Formal.InfiniteAggregation.Witness

/-! # Finite closed aggregation families miss points outside the closed hull

A positive perturbation of an omitted-ray witness preserves every strict
inequality in a finite family, while violating a valid closed inequality.
-/

open Set Filter
open scoped Topology

noncomputable section
namespace InfiniteAggregation

/-- A finite family of strict affine slacks survives a common positive perturbation. -/
theorem finite_slack_perturbation {ι : Type*} [Finite ι]
    (a b : ι → ℝ) (ha : ∀ i, a i < 0) {δ : ℝ} (hδ : 0 < δ) :
    ∃ η : ℝ, 0 < η ∧ η < δ ∧ ∀ i, a i + b i * η < 0 := by
  have hall : ∀ᶠ η : ℝ in 𝓝 0, ∀ i, a i + b i * η < 0 := by
    apply Filter.eventually_all.mpr
    intro i
    have hc : ContinuousAt (fun η : ℝ => a i + b i * η) 0 := by fun_prop
    exact hc.eventually_lt continuousAt_const (by simpa using ha i)
  obtain ⟨ε, hε, hball⟩ := Metric.eventually_nhds_iff.mp hall
  let η := min ε δ / 2
  have hη : 0 < η := by dsimp [η]; positivity
  have hηε : η < ε := by dsimp [η]; linarith [min_le_left ε δ]
  have hηδ : η < δ := by dsimp [η]; linarith [min_le_right ε δ]
  refine ⟨η, hη, hηδ, hball ?_⟩
  simpa [Real.dist_eq, abs_of_pos hη] using hηε

/-- Decreasing the inner product slightly keeps the witness Gram matrix positive definite. -/
theorem perturbed_gram_bounds {τ η : ℝ} (hτ : τ ∈ Icc (1 : ℝ) 2)
    (hη : 0 ≤ η) (hη' : η < 1 / 10) :
    0 < 1 - (1 / 10) / τ ∧ (2 / 5 - η) ^ 2 < (1 - (1 / 10) / τ) * (1 - (1 / 10) * τ) := by
  have ht : 0 < τ := lt_of_lt_of_le (by norm_num) hτ.1
  have hp : 4 / 5 ≤ 1 - (1 / 10) / τ := by
    have : (1 / 10) / τ ≤ (1 / 5 : ℝ) := (div_le_iff₀ ht).mpr (by linarith [hτ.1])
    linarith
  have hq : 4 / 5 ≤ 1 - (1 / 10) * τ := by linarith [hτ.2]
  have hpq : (4 / 5 : ℝ) * (4 / 5) ≤ (1 - (1 / 10) / τ) * (1 - (1 / 10) * τ) :=
    mul_le_mul hp hq (by norm_num) (by linarith)
  constructor
  · linarith
  · have hc : (2 / 5 - η) ^ 2 ≤ (2 / 5 : ℝ) ^ 2 := by nlinarith
    nlinarith

/-- The aggregate value at a perturbed witness is an affine function of the perturbation. -/
theorem perturbed_aggregate_formula {r : ℕ} (w : Weight) {τ η : ℝ}
    {x : Var r} (hp : qnorm x.1 = 1 - (1 / 10) / τ)
    (hq : qnorm x.2 = 1 - (1 / 10) * τ) (hc : dot x.1 x.2 = 2 / 5 - η) :
    aggregate w x = (1 / 10) * (-w 0 / τ - w 1 * τ + w 2) + w 2 * η := by
  rw [aggregate_formula, hp, hq, hc]
  ring

/-- Every good-cone aggregate is nonpositive on the closed convex hull. -/
theorem goodCone_closedHull_valid {r : ℕ} {w : Weight}
    (hK : GoodCone w) (hne : w ≠ 0) {x : Var r}
    (hx : x ∈ closure (convexHull ℝ (feasible r))) : aggregate w x ≤ 0 := by
  apply closure_minimal (t := {y : Var r | aggregate w y ≤ 0}) ?_
    (isClosed_le (continuous_aggregate w) continuous_const) hx
  intro y hy
  exact (goodCone_hull_valid hK hne hy).le

/-- Every finite family in the good cone admits a point strictly satisfying the
family that lies outside the closed convex hull. -/
theorem finite_goodCone_closed_obstruction {r : ℕ} (hr : 2 ≤ r)
    {W : Set Weight} (hW : W.Finite)
    (hgood : ∀ w ∈ W, GoodCone w ∧ w ≠ 0) :
    ∃ x : Var r, (∀ w ∈ W, aggregate w x < 0) ∧
      x ∉ closure (convexHull ℝ (feasible r)) := by
  obtain ⟨τ, hτ, homit⟩ := exists_omitted_ray hW
  have ht : 0 < τ := lt_of_lt_of_le (by norm_num) hτ.1
  have : Finite W := hW.to_subtype
  have hslack (w : W) : (1 / 10 : ℝ) * (-(w.1 0) / τ - w.1 1 * τ + w.1 2) < 0 := by
    obtain ⟨hK, hne⟩ := hgood w.1 w.2
    have hle := ray_slack_nonpos (hK.1 0) (hK.1 1) (hK.1 2) hK.2 ht
    have hneq : -(w.1 0) / τ - w.1 1 * τ + w.1 2 ≠ 0 := by
      intro hz
      exact homit w.1 w.2 ((ray_slack_eq_iff hK.1 hne hK.2 ht).mp hz)
    exact mul_neg_of_pos_of_neg (by norm_num) (lt_of_le_of_ne hle hneq)
  obtain ⟨η, hη, hηlt, hslackη⟩ := finite_slack_perturbation
    (fun w : W => (1 / 10 : ℝ) * (-(w.1 0) / τ - w.1 1 * τ + w.1 2))
    (fun w : W => w.1 2) hslack (δ := 1 / 10) (by norm_num)
  have hb := perturbed_gram_bounds hτ hη.le hηlt
  obtain ⟨u, v, hp, hq, hc⟩ := gram_realization hr hb.1 hb.2.le
  refine ⟨(u, v), ?_, ?_⟩
  · intro w hw
    rw [perturbed_aggregate_formula w hp hq hc]
    exact hslackη ⟨w, hw⟩
  · intro hx
    have hvalid := goodCone_closedHull_valid (rayWeight_goodCone ht)
      (rayWeight_ne_zero τ) hx
    have hval : aggregate (rayWeight τ) (u, v) = 2 * η := by
      rw [perturbed_aggregate_formula (rayWeight τ) hp hq hc]
      simp [rayWeight]
      field_simp
      ring
    rw [hval] at hvalid
    linarith

/-- The non-strict inequalities from a finite good-cone family cannot describe
the closed convex hull. -/
theorem no_finite_goodCone_closed_description {r : ℕ} (hr : 2 ≤ r)
    {W : Set Weight} (hW : W.Finite)
    (hgood : ∀ w ∈ W, GoodCone w ∧ w ≠ 0) :
    closure (convexHull ℝ (feasible r)) ≠
      {x : Var r | ∀ w ∈ W, aggregate w x ≤ 0} := by
  obtain ⟨x, hfamily, hout⟩ := finite_goodCone_closed_obstruction hr hW hgood
  intro heq
  apply hout
  rw [heq]
  intro w hw
  exact (hfamily w hw).le


end InfiniteAggregation
