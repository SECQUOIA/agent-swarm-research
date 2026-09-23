import Formal.SwitchingControl.ResultsCore
import Formal.SwitchingControl.Certificates

namespace SwitchingControl

theorem five_strict {A : Profile 5} (hA : ValidProfile A) (hs : StrictProfile A) :
    HasSchedule A 2 1 :=
  schedule_of_solvable hA hs (Finite.five_cover _ (strict_history (by decide) hA hs))

theorem six_strict {A : Profile 6} (hA : ValidProfile A) (hs : StrictProfile A) :
    HasSchedule A 3 1 :=
  schedule_of_solvable hA hs (Finite.six_cover _ (strict_history (by decide) hA hs))

theorem seven_strict {A : Profile 7} (hA : ValidProfile A) (hs : StrictProfile A) :
    HasSchedule A 3 (4 / 3) := by
  rcases Finite.seven_cover _ (strict_history (by decide) hA hs) with hg | hb
  · obtain ⟨w, hw, hs, he⟩ := schedule_of_solvable hA hs hg
    exact ⟨w, hw, hs, fun j i => (he j i).trans (by norm_num)⟩
  · obtain ⟨e, he⟩ := Geometry.exceptional_floor_permutation (floors A) hb
    apply Geometry.exceptional_repair_list A e
    · intro j i
      have hf := strict_floor_bounds hA hs j (e i)
      rw [he j i] at hf
      exact ⟨hf.1.le, hf.2.le⟩
    · exact (hA.increments 1 3 (e 0) (by decide)).1
    · exact (hA.increments 2 3 (e 1) (by decide)).1
    · have hc := hA.conservation 3
      have hp : ∑ i, A 3 (e i) = ∑ i, A 3 i := Equiv.sum_comp e _
      have hh := hp.trans hc
      norm_num [Fin.sum_univ_succ, add_assoc] at hh ⊢
      exact hh

/-- Every five-cell relaxed control has a two-switch schedule of error at most one. -/
theorem five_cells (A : Profile 5) (hA : ValidProfile A) : HasSchedule A 2 1 :=
  extend_to_boundary (by decide) 1 (fun _ => five_strict) A hA

/-- Every six-cell relaxed control has a three-switch schedule of error at most one. -/
theorem six_cells (A : Profile 6) (hA : ValidProfile A) : HasSchedule A 3 1 :=
  extend_to_boundary (by decide) 1 (fun _ => six_strict) A hA

/-- Every seven-cell relaxed control has a three-switch schedule of error at most four thirds. -/
theorem seven_cells (A : Profile 7) (hA : ValidProfile A) : HasSchedule A 3 (4 / 3) :=
  extend_to_boundary (by decide) (4 / 3) (fun _ => seven_strict) A hA

end SwitchingControl
