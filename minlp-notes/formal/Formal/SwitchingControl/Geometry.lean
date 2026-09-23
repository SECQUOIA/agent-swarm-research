import Mathlib
import Formal.SwitchingControl.Finite
import Formal.SwitchingControl.Profile

namespace SwitchingControl.Geometry

/-- Between consecutive integers, only the two endpoints have error below one. -/
theorem abs_sub_lt_one_iff {a : ℝ} {f k : ℤ}
    (hlo : (f : ℝ) < a) (hhi : a < (f : ℝ) + 1) :
    |a - (k : ℝ)| < 1 ↔ k = f ∨ k = f + 1 := by
  constructor
  · intro h
    obtain ⟨h1, h2⟩ := abs_lt.mp h
    have hf : f - 1 < k := by exact_mod_cast (show (f : ℝ) - 1 < k by linarith)
    have hk : k < f + 2 := by exact_mod_cast (show (k : ℝ) < f + 2 by linarith)
    omega
  · rintro (rfl | rfl) <;> rw [abs_lt] <;> push_cast <;> constructor <;> linarith

/-- Closed floor intervals suffice for the non-strict error bound. -/
theorem abs_sub_le_one {a : ℝ} {f k : ℕ}
    (hlo : (f : ℝ) ≤ a) (hhi : a ≤ (f : ℝ) + 1)
    (hk : k = f ∨ k = f + 1) : |a - (k : ℝ)| ≤ 1 := by
  rcases hk with rfl | rfl <;> rw [abs_le] <;> push_cast <;> constructor <;> linarith

/-- Prefix floors of the canonical exceptional seven-cell chamber. -/
def badFloors : Fin 7 → Fin 3 → ℕ :=
  ![![0, 0, 0], ![1, 0, 0], ![1, 1, 0], ![1, 1, 1],
    ![2, 1, 1], ![2, 1, 1], ![2, 1, 2]]

/-- Three schedules used to repair the exceptional chamber. -/
def repairWord : Fin 3 → Fin 7 → Fin 3 :=
  ![![1, 2, 0, 0, 0, 2, 2], ![0, 0, 2, 1, 1, 2, 2], ![0, 0, 1, 1, 2, 2, 0]]

def prefixCount (w : Fin 7 → Fin 3) (j : Fin 7) (i : Fin 3) : ℕ :=
  (Finset.univ.filter fun k : Fin 7 => k ≤ j ∧ w k = i).card

def switchCount (w : Fin 7 → Fin 3) : ℕ :=
  (Finset.univ.filter fun k : Fin 6 => w k.castSucc ≠ w k.succ).card

/-- Each repair is a schedule with at most three switches. -/
theorem repair_switches : ∀ r, switchCount (repairWord r) ≤ 3 := by decide

/-- Each repair misses just its indicated floor coordinate. -/
theorem repair_membership : ∀ (r : Fin 3) (j : Fin 7) (i : Fin 3),
    (j.val = r.val + 1 ∧ i = r ∧ prefixCount (repairWord r) j i = 0) ∨
    (prefixCount (repairWord r) j i = badFloors j i ∨
      prefixCount (repairWord r) j i = badFloors j i + 1) := by decide

/-- Conservation and monotonicity bound one of the three exceptional coordinates. -/
theorem one_small_coordinate (A : Fin 7 → Fin 3 → ℝ)
    (h0 : A 1 0 ≤ A 3 0) (h1 : A 2 1 ≤ A 3 1)
    (hsum : A 3 0 + A 3 1 + A 3 2 = 4) :
    A 1 0 ≤ 4 / 3 ∨ A 2 1 ≤ 4 / 3 ∨ A 3 2 ≤ 4 / 3 := by
  by_contra h
  push Not at h
  linarith

/-- The repair argument applies throughout the closed exceptional chamber. -/
theorem exceptional_repair (A : Fin 7 → Fin 3 → ℝ)
    (hfloor : ∀ j i, (badFloors j i : ℝ) ≤ A j i ∧
      A j i ≤ (badFloors j i : ℝ) + 1)
    (h0 : A 1 0 ≤ A 3 0) (h1 : A 2 1 ≤ A 3 1)
    (hsum : A 3 0 + A 3 1 + A 3 2 = 4) :
    ∃ r : Fin 3, switchCount (repairWord r) ≤ 3 ∧
      ∀ j i, |A j i - (prefixCount (repairWord r) j i : ℝ)| ≤ 4 / 3 := by
  have hsmall : ∃ r : Fin 3, A ⟨r.val + 1, by omega⟩ r ≤ 4 / 3 := by
    rcases one_small_coordinate A h0 h1 hsum with h | h | h
    · exact ⟨0, h⟩
    · exact ⟨1, h⟩
    · exact ⟨2, h⟩
  obtain ⟨r, hr⟩ := hsmall
  refine ⟨r, repair_switches r, ?_⟩
  intro j i
  rcases repair_membership r j i with ⟨hj, hi, hz⟩ | hk
  · subst i
    have jeq : j = ⟨r.val + 1, by omega⟩ := Fin.ext hj
    rw [hz, Nat.cast_zero, sub_zero,
      abs_of_nonneg (le_trans (Nat.cast_nonneg _) (hfloor j r).1)]
    simpa only [jeq] using hr
  · exact le_trans (abs_sub_le_one (hfloor j i).1 (hfloor j i).2 hk) (by norm_num)

/-- Relabeling modes preserves prefix counts. -/
theorem prefixCount_relabel (e : Equiv.Perm (Fin 3)) (w : Fin 7 → Fin 3)
    (j : Fin 7) (i : Fin 3) :
    prefixCount (e ∘ w) j (e i) = prefixCount w j i := by
  simp [prefixCount]

/-- Relabeling modes preserves the switch budget. -/
theorem switchCount_relabel (e : Equiv.Perm (Fin 3)) (w : Fin 7 → Fin 3) :
    switchCount (e ∘ w) = switchCount w := by
  simp [switchCount]

/-- All mode permutations of the exceptional chamber admit the same bound. -/
theorem exceptional_repair_permuted (A : Fin 7 → Fin 3 → ℝ)
    (e : Equiv.Perm (Fin 3))
    (hfloor : ∀ j i, (badFloors j i : ℝ) ≤ A j (e i) ∧
      A j (e i) ≤ (badFloors j i : ℝ) + 1)
    (h0 : A 1 (e 0) ≤ A 3 (e 0)) (h1 : A 2 (e 1) ≤ A 3 (e 1))
    (hsum : A 3 (e 0) + A 3 (e 1) + A 3 (e 2) = 4) :
    ∃ w : Fin 7 → Fin 3, switchCount w ≤ 3 ∧
      ∀ j i, |A j i - (prefixCount w j i : ℝ)| ≤ 4 / 3 := by
  obtain ⟨r, hs, hr⟩ := exceptional_repair (fun j i => A j (e i)) hfloor h0 h1 hsum
  refine ⟨e ∘ repairWord r, ?_, ?_⟩
  · simpa only [switchCount_relabel] using hs
  · intro j i
    obtain ⟨k, rfl⟩ := e.surjective i
    simpa only [prefixCount_relabel] using hr j k

/-- The finite checker's floor membership implies the real endpoint error bound. -/
theorem fits_discrepancy_le_one {n : ℕ} (A : Profile n)
    (f : Fin n → Fin 3 → ℕ) (w : Finite.Word)
    (hfit : Finite.Fits (List.ofFn f) w)
    (hfloor : ∀ j i, (f j i : ℝ) ≤ A j i ∧ A j i ≤ (f j i : ℝ) + 1) :
    w.length = n ∧ ∀ j : Fin n, ∀ i,
      |A j i - (Finite.countPrefix w (j.val + 1) i : ℝ)| ≤ 1 := by
  refine ⟨by simpa using hfit.1.symm, ?_⟩
  intro j i
  have h := hfit.2 ⟨j.val, by simp⟩ i
  have h' : f j i ≤ Finite.countPrefix w (j.val + 1) i ∧
      Finite.countPrefix w (j.val + 1) i ≤ f j i + 1 := by simpa using h
  apply abs_sub_le_one (hfloor j i).1 (hfloor j i).2
  omega

/-- List and array representations of the repair schedules have the same counts. -/
theorem repair_list_counts : ∀ (e : Equiv.Perm (Fin 3)) (r : Fin 3) (j : Fin 7) (i : Fin 3),
    Finite.countPrefix (List.ofFn (e ∘ repairWord r)) (j.val + 1) i =
      prefixCount (e ∘ repairWord r) j i := by decide

/-- List and array representations have the same number of switches. -/
theorem repair_list_switches : ∀ (e : Equiv.Perm (Fin 3)) (r : Fin 3),
    Finite.switches (List.ofFn (e ∘ repairWord r)) = switchCount (e ∘ repairWord r) := by decide

/-- The exceptional-chamber bound in the finite checker's list representation. -/
theorem exceptional_repair_list (A : Profile 7) (e : Equiv.Perm (Fin 3))
    (hfloor : ∀ j i, (badFloors j i : ℝ) ≤ A j (e i) ∧
      A j (e i) ≤ (badFloors j i : ℝ) + 1)
    (h0 : A 1 (e 0) ≤ A 3 (e 0)) (h1 : A 2 (e 1) ≤ A 3 (e 1))
    (hsum : A 3 (e 0) + A 3 (e 1) + A 3 (e 2) = 4) :
    ∃ w : Finite.Word, w.length = 7 ∧ Finite.switches w ≤ 3 ∧
      ∀ j : Fin 7, ∀ i, |A j i - (Finite.countPrefix w (j.val + 1) i : ℝ)| ≤ 4 / 3 := by
  obtain ⟨r, hs, hr⟩ := exceptional_repair (fun j i => A j (e i)) hfloor h0 h1 hsum
  refine ⟨List.ofFn (e ∘ repairWord r), by simp, ?_, ?_⟩
  · simpa only [repair_list_switches, switchCount_relabel] using hs
  · intro j i
    obtain ⟨k, rfl⟩ := e.surjective i
    simpa only [repair_list_counts, prefixCount_relabel] using hr j k

/-- The six exceptional histories are precisely relabelings of the canonical floor array. -/
theorem exceptional_orbit (h : Finite.History) (hh : h ∈ Finite.exceptional) :
    ∃ e : Equiv.Perm (Fin 3),
      h = List.ofFn (fun j : Fin 7 => fun i => badFloors j (e.symm i)) := by
  simp only [Finite.exceptional, List.mem_cons, List.not_mem_nil, or_false] at hh
  rcases hh with rfl | rfl | rfl | rfl | rfl | rfl
  · exact ⟨Equiv.refl _, by decide⟩
  · exact ⟨Equiv.swap 1 2, by decide⟩
  · exact ⟨Equiv.swap 0 1, by decide⟩
  · exact ⟨(Equiv.swap 0 1).trans (Equiv.swap 1 2), by decide⟩
  · exact ⟨(Equiv.swap 1 2).trans (Equiv.swap 0 1), by decide⟩
  · exact ⟨Equiv.swap 0 2, by decide⟩

/-- Membership in the checker's exceptional list supplies the required mode permutation. -/
theorem exceptional_floor_permutation (f : Fin 7 → Fin 3 → ℕ)
    (hf : List.ofFn f ∈ Finite.exceptional) :
    ∃ e : Equiv.Perm (Fin 3), ∀ j i, f j (e i) = badFloors j i := by
  obtain ⟨e, he⟩ := exceptional_orbit _ hf
  have heq : f = (fun j : Fin 7 => fun i => badFloors j (e.symm i)) :=
    List.ofFn_injective he
  refine ⟨e, ?_⟩
  intro j i
  simp [heq]

end SwitchingControl.Geometry
