import Formal.NetworkSimplex.ThresholdThreeCompleteness
import Formal.NetworkSimplex.ThresholdBranchValidity

/-! Source-only finite grouping for real data and completeness of original branches. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators

/-- A present direction has an attaining original row of minimum right-hand side. -/
theorem source_minimum {R N : Type*} [Finite R] (A : R → N) (b : R → ℝ)
    (i : N) (h : ∃ r, A r = i) :
    ∃ r, A r = i ∧ ∀ s, A s = i → b r ≤ b s := by
  classical
  let _ : Fintype R := Fintype.ofFinite R
  let fiber := Finset.univ.filter fun r => A r = i
  have hn : fiber.Nonempty := by
    obtain ⟨r, hr⟩ := h
    exact ⟨r, by simp [fiber, hr]⟩
  obtain ⟨r, hr, hmin⟩ := Finset.exists_min_image fiber b hn
  exact ⟨r, (Finset.mem_filter.mp hr).2, fun s hs => hmin s (by simp [fiber, hs])⟩

/-- Expanding every combination of attaining source rows is exact, even when
some directions are absent. Zero directions are checked as scalar inequalities. -/
theorem source_branches_sufficient {R C N : Type*} [Finite R] [Nonempty R]
    [Finite C] [Fintype N] {m : ℕ}
    (A : R → Fin m → ℝ) (b : R → ℝ) (normal : N → Fin m → ℝ)
    (weight : C → N → ℝ)
    (hcover : ∀ r, A r = 0 ∨ ∃ i, A r = normal i)
    (complete : ∀ rhs : N → Option ℝ, PartialCircuitTests weight rhs →
      ∃ x : Fin m → ℝ, ∀ i t, rhs i = some t → ∑ j, normal i j * x j ≤ t)
    (hzero : ∀ r, A r = 0 → 0 ≤ b r)
    (hbranch : ∀ c (rows : N → R),
      (∀ i, weight c i ≠ 0 → A (rows i) = normal i) →
      0 ≤ ∑ i, weight c i * b (rows i)) :
    ∃ x : Fin m → ℝ, ∀ r, ∑ j, A r j * x j ≤ b r := by
  classical
  let present (i : N) : Prop := ∃ r, A r = normal i
  have hm (i : N) (h : present i) := source_minimum A b (normal i) h
  let chosen (i : N) : R :=
    if h : present i then (hm i h).choose else Classical.choice inferInstance
  have hs (i : N) (h : present i) :
      A (chosen i) = normal i ∧ ∀ s, A s = normal i → b (chosen i) ≤ b s := by
    simp only [chosen, dif_pos h]
    exact (hm i h).choose_spec
  let rhs (i : N) : Option ℝ := if present i then some (b (chosen i)) else none
  have ht : PartialCircuitTests weight rhs := by
    intro c hc
    have hp (i : N) (hi : weight c i ≠ 0) : present i := by
      by_contra hn
      exact hi (hc i (by simp [rhs, hn]))
    have hb := hbranch c chosen (fun i hi => (hs i (hp i hi)).1)
    have he (i : N) : weight c i * (rhs i).getD 0 = weight c i * b (chosen i) := by
      by_cases hn : present i
      · simp [rhs, hn]
      · simp [rhs, hn, hc i (by simp [rhs, hn])]
    simpa only [he] using hb
  obtain ⟨x, hx⟩ := complete rhs ht
  refine ⟨x, fun r => ?_⟩
  rcases hcover r with hz | ⟨i, hi⟩
  · simpa [hz] using hzero r hz
  · have hp : present i := ⟨r, hi⟩
    rw [hi]
    exact (hx i _ (by simp [rhs, hp])).trans ((hs i hp).2 r hi)

end NetworkSimplex.Threshold

namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open NetworkSimplex.Threshold

/-- All nonzero reduced directions occur in the eleven-direction library. -/
theorem three_normal_cover (n : ProfileNormal 3) :
    normalVector n = 0 ∨ ∃ i, normalVector n = ThreeStateCircuits.normal i := by
  revert n
  decide

/-- The complete original-row branch family, with no added box rows. -/
def ThreeSourceTests {I : Type*} (D : ReductionData 3 I) : Prop :=
  (∀ r, normalVector (D.rowNormal r) = 0 → 0 ≤ D.rowRhs r) ∧
    ∀ c r, ThreeBranch D c r →
      0 ≤ ∑ k, (ThreeStateCircuits.weight c k : ℝ) * D.rowRhs (r k)

theorem three_source_tests_iff_profile {I : Type*} [Finite I] (D : ReductionData 3 I) :
    ThreeSourceTests D ↔ ∃ x, D.ReducedProfile x := by
  classical
  let _ : Fintype I := Fintype.ofFinite I
  let _ : Nonempty (ProfileRow 3 I) := ⟨.totalLower⟩
  constructor
  · rintro ⟨hz, hb⟩
    have hc (r : ProfileRow 3 I) :
        (fun j => (normalVector (D.rowNormal r) j : ℝ)) = 0 ∨
          ∃ i, (fun j => (normalVector (D.rowNormal r) j : ℝ)) =
            fun j => (ThreeStateCircuits.normal i j : ℝ) := by
      rcases three_normal_cover (D.rowNormal r) with h | ⟨i, h⟩
      · left; funext j; simp [h]
      · right; exact ⟨i, by rw [h]⟩
    obtain ⟨x, hx⟩ := source_branches_sufficient
      (fun r j => (normalVector (D.rowNormal r) j : ℝ)) D.rowRhs
      (fun i j => (ThreeStateCircuits.normal i j : ℝ))
      (fun c i => (ThreeStateCircuits.weight c i : ℝ)) hc
      (fun rhs ht => (three_partial_feasible_iff rhs).mpr ht)
      (fun r h => hz r (by
        funext j
        have hh : (normalVector (D.rowNormal r) j : ℝ) = 0 := congrFun h j
        exact_mod_cast hh))
      (fun c rows h => hb c rows (by
        intro i hi
        have hh := h i (by exact_mod_cast hi)
        funext j
        have hj := congrFun hh j
        exact_mod_cast hj))
    refine ⟨x, (D.rows_iff_reducedProfile x).mp ?_⟩
    intro r
    simpa only [profileNormal_value_eq_dot] using hx r
  · rintro ⟨x, hx⟩
    have hr := (D.rows_iff_reducedProfile x).mpr hx
    refine ⟨?_, fun c rows h => h.nonneg_of_rows D c rows x hr⟩
    intro r hz
    have hh := hr r
    simpa [profileNormal_value_eq_dot, hz] using hh

/-- The source-only branch description is exact in the original graph coordinates. -/
theorem three_mem_hull_iff_source_tests {L : ℕ} (D : ReductionData 3 (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    D.graphPoint ∈ convexHull ℝ D.graph ↔ D.OriginalDomain ∧ ThreeSourceTests D := by
  rw [D.mem_hull_iff, three_source_tests_iff_profile]
  rw [D.exists_fullProfile_iff_rows hc hh]
  exact and_congr_right fun _ => exists_congr fun x => D.rows_iff_reducedProfile x

end NetworkSimplex.Chain.Threshold
