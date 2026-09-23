import Formal.NetworkSimplex.GroupedProfile
import Formal.NetworkSimplex.ThreeState

/-! The sixteen tests applied to the actual grouped three-coordinate profile. -/

namespace NetworkSimplex.Chain.ReductionData

noncomputable section

variable {I : Type*} [Fintype I]

/-- Bounds computed as minima of all matching original rows and redundant box rows. -/
def threeBounds (D : ReductionData 3 I) : ThreeStateBounds where
  l1 := -D.grouped (.negativeSingleton 0)
  l2 := -D.grouped (.negativeSingleton 1)
  l3 := -D.grouped (.negativeSingleton 2)
  ls := -D.grouped .negativeTotal
  u1 := D.grouped (.subset {0})
  u2 := D.grouped (.subset {1})
  u3 := D.grouped (.subset {2})
  u12 := D.grouped (.subset {0, 1})
  u13 := D.grouped (.subset {0, 2})
  u23 := D.grouped (.subset {1, 2})
  us := D.grouped (.subset Finset.univ)

private theorem subsets_three (s : Finset (Fin 3)) :
    s = ∅ ∨ s = {0} ∨ s = {1} ∨ s = {2} ∨ s = {0, 1} ∨
      s = {0, 2} ∨ s = {1, 2} ∨ s = Finset.univ := by
  revert s
  decide +kernel

theorem grouped_three_iff (D : ReductionData 3 I) (x : Fin 3 → ℝ) :
    (∀ n, n.value x ≤ D.grouped n) ↔
      0 ≤ D.grouped (.subset ∅) ∧ D.threeBounds.Feasible (x 0) (x 1) (x 2) := by
  constructor
  · intro h
    refine ⟨by simpa [ProfileNormal.value] using h (.subset ∅), ?_⟩
    have hl1 := h (.negativeSingleton 0)
    have hl2 := h (.negativeSingleton 1)
    have hl3 := h (.negativeSingleton 2)
    have hls := h .negativeTotal
    have hu1 := h (.subset {0})
    have hu2 := h (.subset {1})
    have hu3 := h (.subset {2})
    have hu12 := h (.subset {0, 1})
    have hu13 := h (.subset {0, 2})
    have hu23 := h (.subset {1, 2})
    have hus := h (.subset Finset.univ)
    simp [ProfileNormal.value, Fin.sum_univ_succ] at hl1 hl2 hl3 hls hu1 hu2 hu3 hu12 hu13 hu23 hus
    unfold ThreeStateBounds.Feasible threeBounds
    and_intros <;> linarith
  · rintro ⟨hz, h⟩ n
    rcases h with ⟨hl1, hu1, hl2, hu2, hl3, hu3, hu12, hu13, hu23, hls, hus⟩
    simp only [threeBounds] at hl1 hu1 hl2 hu2 hl3 hu3 hu12 hu13 hu23 hls hus
    cases n with
    | subset s =>
        rcases subsets_three s with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
        all_goals simp [ProfileNormal.value, Fin.sum_univ_succ]
        all_goals linarith
    | negativeSingleton j =>
        fin_cases j
        · simpa [ProfileNormal.value] using neg_le_neg hl1
        · simpa [ProfileNormal.value] using neg_le_neg hl2
        · simpa [ProfileNormal.value] using neg_le_neg hl3
    | negativeTotal =>
        simp [ProfileNormal.value, Fin.sum_univ_succ]
        linarith

/-- Exact three-dimensional profile feasibility: the scalar zero-row check and
sixteen fixed inequalities; no missing normal directions are assumed present. -/
theorem three_tests_iff_reducedProfile (D : ReductionData 3 I) :
    (0 ≤ D.grouped (.subset ∅) ∧ D.threeBounds.SixteenTests) ↔
      ∃ x, D.ReducedProfile x := by
  constructor
  · rintro ⟨hz, ht⟩
    obtain ⟨x, y, z, h⟩ := D.threeBounds.tests_imply_feasible ht
    refine ⟨![x, y, z], (D.grouped_iff_reducedProfile _).mp ?_⟩
    exact (D.grouped_three_iff _).mpr ⟨hz, h⟩
  · rintro ⟨x, hx⟩
    obtain ⟨hz, h⟩ := (D.grouped_three_iff x).mp ((D.grouped_iff_reducedProfile x).mpr hx)
    exact ⟨hz, ThreeStateBounds.feasible_implies_tests h⟩

/-- The same finite tests decide the full chain profile before residual elimination. -/
theorem three_tests_iff_fullProfile (D : ReductionData 3 I)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    (0 ≤ D.grouped (.subset ∅) ∧ D.threeBounds.SixteenTests) ↔
      ∃ w, D.FullProfile w := by
  rw [D.exists_fullProfile_iff_rows hc hh]
  exact (D.three_tests_iff_reducedProfile).trans
    (exists_congr fun x => (D.rows_iff_reducedProfile x).symm)

end
end NetworkSimplex.Chain.ReductionData
