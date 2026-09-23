import Formal.QuadraticAggregation.ShorModel
import Formal.QuadraticAggregation.ShorConeSeparation

/-!
# Strict semidefinite alternative and whole-space Shor projections

Open-set separation proves the converse without a closedness assumption on the
linear image of the PSD cone. In fact, triviality of every convex aggregation
and one strictly feasible point give a strictly feasible PSD slack at every point.
-/

open scoped BigOperators Matrix
open Set Finset

namespace QuadraticAggregation
namespace System

variable {n m : ℕ}

/-- A strict semidefinite alternative for the covariance slack at a fixed point. -/
theorem strict_shor_alternative (D : System n m) (x : Vec n)
    (hmiss : ¬ ∃ Y : Mat n, Y.PosSemidef ∧
      ∀ i, D.eval x i + tracePair (D.A i) Y < 0) :
    ∃ w : Vec m, (∀ i, 0 ≤ w i) ∧ w ≠ 0 ∧ (D.aggA w).PosSemidef ∧
      0 ≤ ∑ i, w i * D.eval x i := by
  classical
  let C : Set (Vec m) := {z | ∃ Y : Mat n, Y.PosSemidef ∧
    z = fun i => D.eval x i + tracePair (D.A i) Y}
  have hc : Convex ℝ C := by
    rintro z ⟨Y, hY, rfl⟩ z' ⟨Y', hY', rfl⟩ a b ha hb hab
    refine ⟨a • Y + b • Y', (hY.smul ha).add (hY'.smul hb), ?_⟩
    ext i
    simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, tracePair_add_right,
      tracePair_smul_right]
    nlinarith [congrArg (fun r : ℝ => r * D.eval x i) hab]
  have hne : C.Nonempty := ⟨D.eval x, 0, Matrix.PosSemidef.zero, by simp⟩
  have hm : ∀ z ∈ C, ¬ ∀ i, z i < 0 := by
    rintro z ⟨Y, hY, rfl⟩ hi
    exact hmiss ⟨Y, hY, hi⟩
  obtain ⟨w, hw, hw0, hsep⟩ := exists_nonnegative_separator hc hne hm
  have hall (Y : Mat n) (hY : Y.PosSemidef) :
      0 ≤ (∑ i, w i * D.eval x i) + tracePair (D.aggA w) Y := by
    have h := hsep _ ⟨Y, hY, rfl⟩
    simpa only [mul_add, Finset.sum_add_distrib, ← D.tracePair_aggA] using h
  have hbase : 0 ≤ ∑ i, w i * D.eval x i := by simpa using hall 0 Matrix.PosSemidef.zero
  have hq (v : Vec n) : 0 ≤ q (D.aggA w) v := by
    by_contra hneg
    have hneg' : q (D.aggA w) v < 0 := lt_of_not_ge hneg
    let t : ℝ := ((∑ i, w i * D.eval x i) + 1) / (- q (D.aggA w) v)
    have ht : 0 ≤ t := div_nonneg (by linarith) (by linarith)
    have h := hall (t • outer v) ((outer_posSemidef v).smul ht)
    rw [tracePair_smul_right, tracePair_outer] at h
    have he : t * (- q (D.aggA w) v) = (∑ i, w i * D.eval x i) + 1 :=
      div_mul_cancel₀ _ (ne_of_gt (neg_pos.mpr hneg'))
    nlinarith
  exact ⟨w, hw, hw0, Matrix.posSemidef_iff_dotProduct_mulVec.mpr
    ⟨Matrix.isHermitian_iff_isSymm.mpr (D.aggA_isSymm w), by simpa [q] using hq⟩, hbase⟩

/-- No nontrivial convex certificate implies strict feasibility of every Shor fiber.
Only strict feasibility of the original system is assumed; HHC is unnecessary. -/
theorem exists_strict_shor_slack (D : System n m) (hne : D.feasible.Nonempty)
    (hn : ¬ ∃ w, D.Certificate w) (x : Vec n) :
    ∃ Y : Mat n, Y.PosSemidef ∧ ∀ i, D.eval x i + tracePair (D.A i) Y < 0 := by
  classical
  by_contra hm
  obtain ⟨w, hw, hw0, hA, hx⟩ := D.strict_shor_alternative x hm
  have htrivial : D.aggA w = 0 ∧ D.aggB w = 0 := by
    by_contra! hab
    exact hn ⟨w, hw, hw0, hA, by tauto⟩
  have hc := D.trivial_aggC_neg hw hw0 htrivial.1 htrivial.2 hne
  rw [D.agg_eval, htrivial.1, htrivial.2] at hx
  simp only [q_zero_matrix, zero_dotProduct, mul_zero, zero_add] at hx
  linarith

/-- The converse direction of Lemma 4, without any hidden-convexity hypothesis. -/
theorem shorProjection_eq_univ_of_no_certificate (D : System n m)
    (hne : D.feasible.Nonempty) (hn : ¬ ∃ w, D.Certificate w) :
    D.shorProjection = Set.univ := by
  apply Set.eq_univ_of_forall
  intro x
  obtain ⟨Y, hY, hi⟩ := D.exists_strict_shor_slack hne hn x
  exact ⟨Y, hY, fun i => (hi i).le⟩

end System
end QuadraticAggregation
