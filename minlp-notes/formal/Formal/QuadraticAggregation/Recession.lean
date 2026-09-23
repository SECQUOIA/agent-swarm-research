import Formal.QuadraticAggregation.Model

/-!
# Negative quadratic recession directions

A direction where every leading quadratic form is negative forces the convex
hull of the strict feasible set to fill the ambient space. The proof perturbs
the two homogeneous points `(v, 0)` and `(-v, 0)`, dehomogenizes them, and takes
their midpoint.
-/

open scoped BigOperators Matrix Topology
open Set Filter

namespace QuadraticAggregation

variable {n m : ℕ}

namespace System

/-- A common strict negative direction of the leading forms implies a full
convex hull, without any hidden-convexity assumption. -/
theorem convexHull_eq_univ_of_negative_recession (D : System n m) {v : Vec n}
    (hv : ∀ i, q (D.A i) v < 0) : convexHull ℝ D.feasible = univ := by
  apply Set.eq_univ_of_forall
  intro x
  have hp : ∀ᶠ t : ℝ in 𝓝 0, ∀ i, D.homEval (t • x + v, t) i < 0 := by
    apply Filter.eventually_all.mpr
    intro i
    have hc : Continuous (fun t : ℝ => D.homEval (t • x + v, t) i) := by
      exact (continuous_apply i).comp (D.continuous_homEval.comp (by fun_prop))
    exact hc.continuousAt.eventually_lt continuousAt_const (by simpa using hv i)
  have hm : ∀ᶠ t : ℝ in 𝓝 0, ∀ i, D.homEval (t • x - v, t) i < 0 := by
    apply Filter.eventually_all.mpr
    intro i
    have hc : Continuous (fun t : ℝ => D.homEval (t • x - v, t) i) := by
      exact (continuous_apply i).comp (D.continuous_homEval.comp (by fun_prop))
    exact hc.continuousAt.eventually_lt continuousAt_const (by
      simpa [homEval, q, Matrix.mulVec_neg] using hv i)
  have ht : ∀ᶠ t : ℝ in 𝓝[>] 0,
      t ∈ Ioi (0 : ℝ) ∧ (∀ i, D.homEval (t • x + v, t) i < 0) ∧
        (∀ i, D.homEval (t • x - v, t) i < 0) :=
    (show ∀ᶠ t : ℝ in 𝓝[>] 0, t ∈ Ioi (0 : ℝ) from self_mem_nhdsWithin).and
      ((hp.and hm).filter_mono nhdsWithin_le_nhds)
  obtain ⟨t, ht, htp, htm⟩ := ht.exists
  have ht0 : t ≠ 0 := ne_of_gt ht
  have hconv := (convex_convexHull ℝ D.feasible)
    (subset_convexHull ℝ D.feasible (D.dehomogenize_mem ht0 htp))
    (subset_convexHull ℝ D.feasible (D.dehomogenize_mem ht0 htm))
    (show (0 : ℝ) ≤ 1 / 2 by norm_num)
    (show (0 : ℝ) ≤ 1 / 2 by norm_num)
    (show (1 : ℝ) / 2 + 1 / 2 = 1 by norm_num)
  convert hconv using 1
  ext j
  simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
  field_simp
  ring

/-- A proper convex hull rules out every common strict negative leading
direction. -/
theorem no_negative_recession (D : System n m)
    (hproper : convexHull ℝ D.feasible ≠ univ) :
    ∀ v : Vec n, ¬ ∀ i, q (D.A i) v < 0 := by
  intro v hv
  exact hproper (D.convexHull_eq_univ_of_negative_recession hv)

end System
end QuadraticAggregation
