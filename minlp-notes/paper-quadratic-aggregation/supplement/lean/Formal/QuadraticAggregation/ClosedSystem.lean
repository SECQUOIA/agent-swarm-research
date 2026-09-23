import Formal.QuadraticAggregation.Headline

/-!
# Closed quadratic systems

A nonconstant convex aggregate bounds the closed feasible hull as well as the
strict feasible hull. With strict feasibility and asymptotic hyperplane
convexity, both hulls are proper exactly when a certificate exists.
-/

open Matrix Set
open scoped BigOperators

namespace QuadraticAggregation
variable {n m : ℕ}

/-- A convex quadratic has a convex nonpositive sublevel set. -/
theorem quadratic_nonpos_convex (A : Mat n) (b : Vec n) (c : ℝ)
    (hA : A.PosSemidef) : Convex ℝ {x | q A x + 2 * (b ⬝ᵥ x) + c ≤ 0} := by
  intro x hx y hy s t hs ht hst
  change q A (s • x + t • y) + 2 * (b ⬝ᵥ (s • x + t • y)) + c ≤ 0
  have hnonneg : 0 ≤ (x - y) ⬝ᵥ (A *ᵥ (x - y)) := by
    simpa using hA.dotProduct_mulVec_nonneg (x - y)
  have hid : q A (s • x + t • y) + 2 * (b ⬝ᵥ (s • x + t • y)) + c =
      s * (q A x + 2 * (b ⬝ᵥ x) + c) +
      t * (q A y + 2 * (b ⬝ᵥ y) + c) -
      s * t * ((x - y) ⬝ᵥ (A *ᵥ (x - y))) := by
    simp only [q, Matrix.mulVec_add, Matrix.mulVec_smul, add_dotProduct,
      dotProduct_add, smul_dotProduct, dotProduct_smul, Matrix.mulVec_sub,
      sub_dotProduct, dotProduct_sub, smul_eq_mul]
    have ht' : t = 1 - s := by linarith
    rw [ht']
    ring
  rw [hid]
  exact sub_nonpos.mpr (le_trans
    (add_nonpos (mul_nonpos_of_nonneg_of_nonpos hs hx)
      (mul_nonpos_of_nonneg_of_nonpos ht hy))
    (mul_nonneg (mul_nonneg hs ht) hnonneg))

/-- A nonconstant PSD quadratic cannot be nonpositive everywhere. The shift
by one reduces this to the strict certificate theorem already proved. -/
theorem quadratic_nonpos_ne_univ (A : Mat n) (b : Vec n) (c : ℝ)
    (hA : A.PosSemidef) (hab : A ≠ 0 ∨ b ≠ 0) :
    {x | q A x + 2 * (b ⬝ᵥ x) + c ≤ 0} ≠ Set.univ := by
  let D : System n 1 := ⟨fun _ => A, fun _ => by simpa [Matrix.IsSymm] using hA.isHermitian,
    fun _ => b, fun _ => c - 1⟩
  have hcert : D.Certificate (fun _ => 1) := by
    refine ⟨fun _ => zero_le_one, ?_, ?_, ?_⟩
    · intro h
      have := congrFun h 0
      norm_num at this
    · simpa [System.aggA, D] using hA
    · simpa [System.aggA, System.aggB, D] using hab
  intro hall
  apply hcert.convexHull_ne_univ
  apply Set.eq_univ_of_forall
  intro x
  apply subset_convexHull ℝ D.feasible
  intro i
  have hx : q A x + 2 * (b ⬝ᵥ x) + c ≤ 0 := by
    change x ∈ {x | q A x + 2 * (b ⬝ᵥ x) + c ≤ 0}
    rw [hall]
    trivial
  change q A x + 2 * (b ⬝ᵥ x) + (c - 1) < 0
  linarith

/-- Every nonpositive quadratic sublevel set is closed, whether or not the
quadratic is convex. -/
theorem quadratic_nonpos_isClosed (A : Mat n) (b : Vec n) (c : ℝ) :
    IsClosed {x | q A x + 2 * (b ⬝ᵥ x) + c ≤ 0} := by
  apply isClosed_le _ continuous_const
  unfold q Matrix.mulVec dotProduct
  fun_prop

/-- A nonconstant PSD quadratic is unbounded above. This includes both a
nonzero quadratic part and a zero quadratic part with nonzero linear part. -/
theorem quadratic_unbounded_above (A : Mat n) (b : Vec n) (c : ℝ)
    (hA : A.PosSemidef) (hab : A ≠ 0 ∨ b ≠ 0) :
    ∀ r : ℝ, ∃ x, r < q A x + 2 * (b ⬝ᵥ x) + c := by
  intro r
  by_contra! h
  apply quadratic_nonpos_ne_univ A b (c - r) hA hab
  apply Set.eq_univ_of_forall
  intro x
  change q A x + 2 * (b ⬝ᵥ x) + (c - r) ≤ 0
  linarith [h x]

namespace System

/-- Every strict feasible point is closed feasible. -/
theorem feasible_subset_closedFeasible (D : System n m) :
    D.feasible ⊆ D.closedFeasible := fun _ hx i => (hx i).le

/-- Nonnegative aggregation preserves closed inequalities. -/
theorem agg_eval_nonpos (D : System n m) {w : Vec m} (hw : ∀ i, 0 ≤ w i)
    {x : Vec n} (hx : x ∈ D.closedFeasible) :
    q (D.aggA w) x + 2 * (D.aggB w ⬝ᵥ x) + D.aggC w ≤ 0 := by
  rw [← D.agg_eval]
  exact Finset.sum_nonpos fun i _ => mul_nonpos_of_nonneg_of_nonpos (hw i) (hx i)

/-- A nonnegative PSD aggregation contains the entire closed feasible hull
in its quadratic sublevel set. Nontriviality is unnecessary for containment. -/
theorem closed_convexHull_subset_aggregate (D : System n m) {w : Vec m}
    (hw : ∀ i, 0 ≤ w i) (hA : (D.aggA w).PosSemidef) :
    convexHull ℝ D.closedFeasible ⊆
      {x | q (D.aggA w) x + 2 * (D.aggB w ⬝ᵥ x) + D.aggC w ≤ 0} :=
  convexHull_min (fun _ hx => D.agg_eval_nonpos hw hx)
    (quadratic_nonpos_convex _ _ _ hA)

/-- The certificate implication for the closed hull requires neither strict
feasibility nor hidden hyperplane convexity. -/
theorem Certificate.closed_convexHull_ne_univ {D : System n m} {w : Vec m}
    (hw : D.Certificate w) : convexHull ℝ D.closedFeasible ≠ Set.univ := by
  have hsub := D.closed_convexHull_subset_aggregate hw.1 hw.2.2.1
  intro hall
  apply quadratic_nonpos_ne_univ _ _ _ hw.2.2.1 hw.2.2.2
  exact Set.eq_univ_of_forall fun x => hsub (hall.symm ▸ Set.mem_univ x)

/-- Corollary 1: strict feasibility and asymptotic hyperplane convexity give
an exact certificate for a proper closed feasible hull. -/
theorem closed_proper_hull_iff_certificate (D : System n m)
    (hS : D.feasible.Nonempty) (hHC : D.AsymptoticHC) :
    convexHull ℝ D.closedFeasible ≠ Set.univ ↔ ∃ w, D.Certificate w := by
  refine ⟨fun hp => D.exists_certificate_of_proper hS hHC ?_,
    fun ⟨_, hw⟩ => hw.closed_convexHull_ne_univ⟩
  intro hall
  apply hp
  exact Set.eq_univ_of_forall fun x =>
    convexHull_mono D.feasible_subset_closedFeasible (hall.symm ▸ Set.mem_univ x)

/-- Under the hypotheses of Corollary 1, strict and closed hulls are proper
at the same time. This does not assert that either hull is closed. -/
theorem strict_proper_hull_iff_closed (D : System n m)
    (hS : D.feasible.Nonempty) (hHC : D.AsymptoticHC) :
    convexHull ℝ D.feasible ≠ Set.univ ↔ convexHull ℝ D.closedFeasible ≠ Set.univ :=
  (D.proper_hull_iff_certificate hS hHC).trans
    (D.closed_proper_hull_iff_certificate hS hHC).symm

theorem closed_proper_hull_iff_certificate_of_hhc (D : System n m)
    (hS : D.feasible.Nonempty) (hHC : D.HHC) :
    convexHull ℝ D.closedFeasible ≠ Set.univ ↔ ∃ w, D.Certificate w :=
  D.closed_proper_hull_iff_certificate hS hHC.asymptoticHC

/-- Corollary 1 in its whole-space form. -/
theorem closed_hull_eq_univ_iff_strict (D : System n m)
    (hS : D.feasible.Nonempty) (hHC : D.AsymptoticHC) :
    convexHull ℝ D.closedFeasible = Set.univ ↔ convexHull ℝ D.feasible = Set.univ := by
  simpa only [not_not] using not_congr (D.strict_proper_hull_iff_closed hS hHC).symm

theorem closed_hull_eq_univ_iff_strict_of_hhc (D : System n m)
    (hS : D.feasible.Nonempty) (hHC : D.HHC) :
    convexHull ℝ D.closedFeasible = Set.univ ↔ convexHull ℝ D.feasible = Set.univ :=
  D.closed_hull_eq_univ_iff_strict hS hHC.asymptoticHC

end System
end QuadraticAggregation
