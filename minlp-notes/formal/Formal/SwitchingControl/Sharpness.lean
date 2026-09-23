import Formal.SwitchingControl.Results
import Formal.SwitchingControl.SevenWitness

/-! Exact grid minimax values: universal upper bounds and valid matching inputs. -/
namespace SwitchingControl

/-- An exact minimax value, expressed directly by a uniform upper guarantee
and one valid input attaining the matching lower bound against every schedule. -/
def ExactGridValue (n budget : ℕ) (E : ℝ) : Prop :=
  (∀ A : Profile n, ValidProfile A → HasSchedule A budget E) ∧
  ∃ A : Profile n, ValidProfile A ∧
    ∀ w : Finite.Word, w.length = n → Finite.switches w ≤ budget →
      ∃ j i, E ≤ |A j i - (Finite.countPrefix w (j.val + 1) i : ℝ)|

/-- The endpoint profile of the pure alternating five-cell input. -/
def fiveSharpProfile : Profile 5 :=
  ![![1,0,0], ![1,1,0], ![2,1,0], ![2,2,0], ![3,2,0]]

/-- The endpoint profile of the pure alternating six-cell input. -/
def sixSharpProfile : Profile 6 :=
  ![![1,0,0], ![1,1,0], ![2,1,0], ![2,2,0], ![3,2,0], ![3,3,0]]

/-- The rational seven-cell relaxed input, viewed over the real numbers. -/
noncomputable def sevenSharpProfile : Profile 7 := fun j i => (SevenWitness.target j i : ℝ) / 3

theorem fiveSharpProfile_valid : ValidProfile fiveSharpProfile := by
  constructor
  · intro j i; fin_cases j <;> fin_cases i <;> norm_num [fiveSharpProfile]
  · intro j i hj; fin_cases j <;> fin_cases i <;> norm_num [fiveSharpProfile] at *
  · intro j k i hjk
    change j.val ≤ k.val at hjk
    fin_cases j <;> fin_cases k <;> fin_cases i <;> norm_num [fiveSharpProfile] at *
  · intro j; fin_cases j <;> norm_num [fiveSharpProfile, Fin.sum_univ_succ]

theorem sixSharpProfile_valid : ValidProfile sixSharpProfile := by
  constructor
  · intro j i; fin_cases j <;> fin_cases i <;> norm_num [sixSharpProfile]
  · intro j i hj; fin_cases j <;> fin_cases i <;> norm_num [sixSharpProfile] at *
  · intro j k i hjk
    change j.val ≤ k.val at hjk
    fin_cases j <;> fin_cases k <;> fin_cases i <;> norm_num [sixSharpProfile] at *
  · intro j; fin_cases j <;> norm_num [sixSharpProfile, Fin.sum_univ_succ]

theorem sevenSharpProfile_valid : ValidProfile sevenSharpProfile := by
  constructor
  · intro j i
    fin_cases j <;> fin_cases i <;> norm_num [sevenSharpProfile, SevenWitness.target]
  · intro j i hj
    fin_cases j <;> fin_cases i <;> norm_num [sevenSharpProfile, SevenWitness.target] at *
  · intro j k i hjk
    change j.val ≤ k.val at hjk
    fin_cases j <;> fin_cases k <;> fin_cases i <;>
      norm_num [sevenSharpProfile, SevenWitness.target] at *
  · intro j
    fin_cases j <;> norm_num [sevenSharpProfile, SevenWitness.target, Fin.sum_univ_succ]

private theorem fiveSharpProfile_eq : ∀ j i,
    fiveSharpProfile j i = (SevenWitness.count (SevenWitness.alternating 5) j i : ℝ) := by
  have hc : ∀ j i, SevenWitness.count (SevenWitness.alternating 5) j i =
      (![![1,0,0], ![1,1,0], ![2,1,0], ![2,2,0], ![3,2,0]] j i : ℕ) := by
    decide +kernel
  intro j i
  rw [hc]
  fin_cases j <;> fin_cases i <;> norm_num [fiveSharpProfile]

private theorem sixSharpProfile_eq : ∀ j i,
    sixSharpProfile j i = (SevenWitness.count (SevenWitness.alternating 6) j i : ℝ) := by
  have hc : ∀ j i, SevenWitness.count (SevenWitness.alternating 6) j i =
      (![![1,0,0], ![1,1,0], ![2,1,0], ![2,2,0], ![3,2,0], ![3,3,0]] j i : ℕ) := by
    decide +kernel
  intro j i
  rw [hc]
  fin_cases j <;> fin_cases i <;> norm_num [sixSharpProfile]

/-- The two word representations agree on all quantities used here. -/
def RepresentationsAgree (n : ℕ) : Prop :=
  ∀ w : SevenWitness.Word n,
    Finite.switches (List.ofFn w) = SevenWitness.switches w ∧
    ∀ (j : Fin n) (i : Fin 3),
      Finite.countPrefix (List.ofFn w) (j.val + 1) i = SevenWitness.count w j i

/-- Symbolic prefix-count identities hold for arbitrary letters on each grid. -/
private theorem small_representations (n : ℕ) (hn : n = 5 ∨ n = 6 ∨ n = 7) :
    RepresentationsAgree n := by
  rcases hn with rfl | rfl | rfl
  all_goals
    intro w
    constructor
    · simp [List.ofFn_succ, Finite.switches, SevenWitness.switches,
        Fin.sum_univ_succ, add_assoc]
    · intro j i
      unfold SevenWitness.count
      rw [Finset.card_eq_sum_ones, Finset.sum_filter]
      simp only [Fin.sum_univ_succ]
      fin_cases j <;>
        simp [Finite.countPrefix, List.ofFn_succ, List.count_cons, add_assoc] <;> omega

/-- Every list of the prescribed length comes from an array of that length. -/
private theorem exists_array {n : ℕ} (w : Finite.Word) (hw : w.length = n) :
    ∃ v : SevenWitness.Word n, List.ofFn v = w := by
  subst n
  exact ⟨w.get, List.ofFn_get w⟩

theorem five_profile_lower (w : Finite.Word) (hlen : w.length = 5)
    (hswitch : Finite.switches w ≤ 2) :
    ∃ j : Fin 5, ∃ i : Fin 3,
      (1 : ℝ) ≤ |fiveSharpProfile j i - (Finite.countPrefix w (j.val + 1) i : ℝ)| := by
  obtain ⟨v, rfl⟩ := exists_array w hlen
  obtain ⟨hs, hc⟩ := small_representations 5 (by omega) v
  obtain ⟨j, i, he⟩ := SevenWitness.five_real_lower v (hs ▸ hswitch)
  exact ⟨j, i, by rw [fiveSharpProfile_eq, hc]; exact he⟩

theorem five_grid_exact : ExactGridValue 5 2 1 :=
  ⟨five_cells, fiveSharpProfile, fiveSharpProfile_valid, five_profile_lower⟩

theorem six_profile_lower (w : Finite.Word) (hlen : w.length = 6)
    (hswitch : Finite.switches w ≤ 3) :
    ∃ j : Fin 6, ∃ i : Fin 3,
      (1 : ℝ) ≤ |sixSharpProfile j i - (Finite.countPrefix w (j.val + 1) i : ℝ)| := by
  obtain ⟨v, rfl⟩ := exists_array w hlen
  obtain ⟨hs, hc⟩ := small_representations 6 (by omega) v
  obtain ⟨j, i, he⟩ := SevenWitness.six_real_lower v (hs ▸ hswitch)
  exact ⟨j, i, by rw [sixSharpProfile_eq, hc]; exact he⟩

theorem six_grid_exact : ExactGridValue 6 3 1 :=
  ⟨six_cells, sixSharpProfile, sixSharpProfile_valid, six_profile_lower⟩

theorem seven_profile_lower (w : Finite.Word) (hlen : w.length = 7)
    (hswitch : Finite.switches w ≤ 3) :
    ∃ j : Fin 7, ∃ i : Fin 3,
      ((4 / 3) : ℝ) ≤ |sevenSharpProfile j i - (Finite.countPrefix w (j.val + 1) i : ℝ)| := by
  obtain ⟨v, rfl⟩ := exists_array w hlen
  obtain ⟨hs, hc⟩ := small_representations 7 (by omega) v
  obtain ⟨j, i, he⟩ := SevenWitness.real_lower v (hs ▸ hswitch)
  exact ⟨j, i, by rw [hc]; exact he⟩

theorem seven_grid_exact : ExactGridValue 7 3 (4 / 3) :=
  ⟨seven_cells, sevenSharpProfile, sevenSharpProfile_valid, seven_profile_lower⟩

end SwitchingControl
