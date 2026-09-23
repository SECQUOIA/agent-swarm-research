import Formal.NetworkSimplex.GroupedProfile
import Formal.NetworkSimplex.FiveTests

namespace NetworkSimplex.Chain.ReductionData

noncomputable section

variable {I : Type*} [Fintype I]

def twoTests (D : ReductionData 2 I) : Prop :=
  FiveTests (-D.grouped (.negativeSingleton 0)) (D.grouped (.subset {0}))
    (-D.grouped (.negativeSingleton 1)) (D.grouped (.subset {1}))
    (-D.grouped .negativeTotal) (D.grouped (.subset Finset.univ))

theorem grouped_two_iff (D : ReductionData 2 I) (x : Fin 2 → ℝ) :
    (∀ n, n.value x ≤ D.grouped n) ↔
      0 ≤ D.grouped (.subset ∅) ∧
      Hexagon (-D.grouped (.negativeSingleton 0)) (D.grouped (.subset {0}))
        (-D.grouped (.negativeSingleton 1)) (D.grouped (.subset {1}))
        (-D.grouped .negativeTotal) (D.grouped (.subset Finset.univ)) (x 0) (x 1) := by
  constructor
  · intro h
    have h0 := h (.subset ∅)
    have h1 := h (.subset {0})
    have h2 := h (.subset {1})
    have h3 := h (.subset Finset.univ)
    have h4 := h (.negativeSingleton 0)
    have h5 := h (.negativeSingleton 1)
    have h6 := h .negativeTotal
    simp only [ProfileNormal.value, Finset.sum_empty, Finset.sum_singleton,
      Fin.sum_univ_two] at h0 h1 h2 h3 h4 h5 h6
    exact ⟨h0, by unfold Hexagon; exact ⟨by linarith, h1, by linarith, h2,
      by linarith, h3⟩⟩
  · rintro ⟨h0, h1, h2, h3, h4, h5, h6⟩ n
    cases n with
    | subset s =>
        have hs : s = ∅ ∨ s = {0} ∨ s = {1} ∨ s = Finset.univ := by
          have hall : ∀ s : Finset (Fin 2),
              s = ∅ ∨ s = {0} ∨ s = {1} ∨ s = Finset.univ := by decide +kernel
          exact hall s
        rcases hs with rfl | rfl | rfl | rfl
        · simpa [ProfileNormal.value] using h0
        · simpa [ProfileNormal.value] using h2
        · simpa [ProfileNormal.value] using h4
        · simpa [ProfileNormal.value, Fin.sum_univ_two] using h6
    | negativeSingleton j =>
        fin_cases j
        · simpa [ProfileNormal.value] using neg_le_neg h1
        · simpa [ProfileNormal.value] using neg_le_neg h3
    | negativeTotal =>
        simp only [ProfileNormal.value, Fin.sum_univ_two]
        linarith

/-- Every repeated-row group and the zero rows are accounted for in the five-test oracle. -/
theorem two_tests_iff_reducedProfile (D : ReductionData 2 I) :
    (0 ≤ D.grouped (.subset ∅) ∧ D.twoTests) ↔ ∃ x, D.ReducedProfile x := by
  constructor
  · rintro ⟨h0, htests⟩
    obtain ⟨x, y, hxy⟩ := (five_tests_iff_feasible _ _ _ _ _ _).mp htests
    refine ⟨![x, y], (D.grouped_iff_reducedProfile _).mp ?_⟩
    exact (D.grouped_two_iff _).mpr ⟨h0, hxy⟩
  · rintro ⟨x, hx⟩
    obtain ⟨h0, hxy⟩ := (D.grouped_two_iff x).mp ((D.grouped_iff_reducedProfile x).mpr hx)
    exact ⟨h0, (five_tests_iff_feasible _ _ _ _ _ _).mpr ⟨x 0, x 1, hxy⟩⟩

/-- The five tests decide the full profile before residual elimination. -/
theorem two_tests_iff_fullProfile (D : ReductionData 2 I)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    (0 ≤ D.grouped (.subset ∅) ∧ D.twoTests) ↔ ∃ w, D.FullProfile w := by
  rw [D.exists_fullProfile_iff_rows hc hh]
  exact (D.two_tests_iff_reducedProfile).trans
    (exists_congr fun x => (D.rows_iff_reducedProfile x).symm)

end
end NetworkSimplex.Chain.ReductionData
