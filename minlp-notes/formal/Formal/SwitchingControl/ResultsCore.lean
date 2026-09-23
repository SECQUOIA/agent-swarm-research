import Formal.SwitchingControl.Profile
import Formal.SwitchingControl.History
import Formal.SwitchingControl.Geometry
import Formal.SwitchingControl.Boundary
import Formal.SwitchingControl.Schedules

/-! Uniform endpoint guarantees for every relaxed profile, including boundaries. -/
namespace SwitchingControl

/-- A word has the correct length, respects the switch budget, and meets all endpoint errors. -/
def HasSchedule {n : ℕ} (A : Profile n) (budget : ℕ) (E : ℝ) : Prop :=
  ∃ w : Finite.Word, w.length = n ∧ Finite.switches w ≤ budget ∧
    ∀ j i, |A j i - (Finite.countPrefix w (j.val + 1) i : ℝ)| ≤ E

theorem strict_history {n : ℕ} (hn : 0 < n) {A : Profile n}
    (hA : ValidProfile A) (hs : StrictProfile A) :
    List.ofFn (floors A) ∈ Finite.histories n := by
  apply Finite.finite_row_history_mem hn
  · intro j hj
    funext i
    have hi := initial_floors hA hs j hj i
    fin_cases i <;> exact hi
  · exact fun j k hjk i => floor_increment hA j k hjk i
  · intro j
    simpa [Fin.sum_univ_succ, add_assoc] using floor_sum_cases hA hs j

theorem schedule_of_solvable {n budget : ℕ} {A : Profile n}
    (hA : ValidProfile A) (hs : StrictProfile A)
    (hc : Finite.Solvable budget (List.ofFn (floors A))) : HasSchedule A budget 1 := by
  obtain ⟨w, hfit, hsw⟩ := hc
  obtain ⟨hlen, he⟩ := Geometry.fits_discrepancy_le_one A (floors A) w hfit
    (fun j i => ⟨(strict_floor_bounds hA hs j i).1.le,
      (strict_floor_bounds hA hs j i).2.le⟩)
  exact ⟨w, hlen, hsw, he⟩

/-- A strict-profile theorem extends to every valid profile on these grids. -/
theorem extend_to_boundary {n budget : ℕ} (hn : n ≤ 7) (E : ℝ)
    (hstrict : ∀ A : Profile n, ValidProfile A → StrictProfile A → HasSchedule A budget E)
    (A : Profile n) (hA : ValidProfile A) : HasSchedule A budget E := by
  classical
  let W := {w : {w : Finite.Word // w.length = n} // Finite.switches w.val ≤ budget}
  let x : (Fin n × Fin 3) → ℝ := fun c => A c.1 c.2
  let y : (Fin n × Fin 3) → ℝ := fun c => baseline n c.1 c.2
  let count : W → (Fin n × Fin 3) → ℝ :=
    fun w c => Finite.countPrefix w.val.val (c.1.val + 1) c.2
  have hbound : ∀ ε : ℝ, 0 < ε → ε < 1 →
      (∀ c (z : ℤ), Boundary.interpolate x y ε c ≠ z) →
      ∃ w : W, ∀ c, |Boundary.interpolate x y ε c - count w c| ≤ E := by
    intro ε hε hε1 hs
    obtain ⟨w, hlen, hsw, he⟩ := hstrict
      (fun j i => (1 - ε) * A j i + ε * baseline n j i)
      (valid_interpolate hA (baseline_valid n) hε.le hε1.le)
      (fun j i z => hs (j, i) z)
    exact ⟨⟨⟨w, hlen⟩, hsw⟩, fun c => he c.1 c.2⟩
  obtain ⟨w, hw⟩ := Boundary.extend_strict_bound x y count n E
    (fun c => profile_bounded hA c.1 c.2)
    (fun c => profile_bounded (baseline_valid n) c.1 c.2)
    (fun c z => baseline_strict hn c.1 c.2 z) hbound
  exact ⟨w.val.val, w.val.property, w.property, fun j i => hw (j, i)⟩

end SwitchingControl
