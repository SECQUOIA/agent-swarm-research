import Formal.NetworkSimplex.ThresholdRows
import Formal.NetworkSimplex.ProfileHull

/-! Validity of the literal three-state circuit branches for the original chain hull. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators

theorem profileNormal_value_eq_dot {m : ℕ} (n : ProfileNormal m) (x : Fin m → ℝ) :
    n.value x = ∑ j, (normalVector n j : ℝ) * x j := by
  cases n with
  | subset s => simp [ProfileNormal.value, normalVector, Finset.sum_ite_mem]
  | negativeSingleton k => simp [ProfileNormal.value, normalVector]
  | negativeTotal => simp [ProfileNormal.value, normalVector, Finset.sum_neg_distrib]

theorem ThreeBranch.nonneg_of_rows {I : Type*} (D : ReductionData 3 I)
    (c : Fin 16) (r : Fin 11 → ProfileRow 3 I) (hbranch : ThreeBranch D c r)
    (x : Fin 3 → ℝ) (hx : ∀ r, (D.rowNormal r).value x ≤ D.rowRhs r) :
    0 ≤ ∑ k, (ThreeStateCircuits.weight c k : ℝ) * D.rowRhs (r k) := by
  have heq : (∑ k, (ThreeStateCircuits.weight c k : ℝ) * (D.rowNormal (r k)).value x) = 0 := by
    simp_rw [profileNormal_value_eq_dot, Finset.mul_sum]
    rw [Finset.sum_comm]
    have hz (j : Fin 3) :
        (∑ k, (ThreeStateCircuits.weight c k : ℝ) *
          (normalVector (D.rowNormal (r k)) j : ℝ)) = 0 := by
      have hs : (∑ k, ThreeStateCircuits.weight c k *
          normalVector (D.rowNormal (r k)) j) = 0 := by
        calc
          _ = ∑ k, ThreeStateCircuits.weight c k * ThreeStateCircuits.normal k j := by
            apply Finset.sum_congr rfl
            intro k _
            by_cases hk : ThreeStateCircuits.weight c k = 0
            · simp [hk]
            · rw [hbranch k hk]
          _ = 0 := ThreeStateCircuits.normal_cancellation c j
      exact_mod_cast hs
    simp_rw [← mul_assoc, ← Finset.sum_mul, hz, zero_mul]
    simp
  rw [← heq]
  apply Finset.sum_le_sum
  intro k _
  exact mul_le_mul_of_nonneg_left (hx (r k)) (by
    exact_mod_cast ThreeStateCircuits.weight_nonnegative c k)

theorem ThreeBranch.nonneg_of_hull {L : ℕ} (D : ReductionData 3 (Fin L))
    (c : Fin 16) (r : Fin 11 → ProfileRow 3 (Fin L)) (hbranch : ThreeBranch D c r)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (h : D.graphPoint ∈ convexHull ℝ D.graph) :
    0 ≤ ∑ k, (ThreeStateCircuits.weight c k : ℝ) * D.rowRhs (r k) := by
  obtain ⟨x, hx⟩ := (D.exists_fullProfile_iff_rows hc hh).mp ((D.mem_hull_iff.mp h).2)
  exact hbranch.nonneg_of_rows D c r x hx

end NetworkSimplex.Chain.Threshold
