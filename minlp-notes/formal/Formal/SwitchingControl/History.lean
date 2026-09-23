import Formal.SwitchingControl.Finite

namespace SwitchingControl.Finite

/-- The Boolean records whether the sum of the three fractional parts is two. -/
def deficit (s : Bool) : ℕ := if s then 2 else 1

/-- The transition list contains every coordinate increment compatible with the row sums. -/
theorem transitions_complete (s t : Bool) (d : Triple)
    (hd : ∀ i, d i ≤ 1)
    (hs : d 0 + d 1 + d 2 + deficit t = deficit s + 1) :
    (t, d) ∈ transitions s := by
  have heq : d = ![d 0, d 1, d 2] := by
    funext i
    fin_cases i <;> rfl
  have h0 := hd 0
  have h1 := hd 1
  have h2 := hd 2
  rw [heq]
  generalize d 0 = a at *
  generalize d 1 = b at *
  generalize d 2 = c at *
  interval_cases a <;> interval_cases b <;> interval_cases c <;>
    cases s <;> cases t <;>
    simp_all [deficit, transitions, unit, zero, funext_iff, Fin.forall_fin_succ]

/-- Coordinatewise monotonicity turns floor differences into natural increments. -/
theorem next_transition (s t : Bool) (x y : Triple)
    (hm : ∀ i, x i ≤ y i ∧ y i ≤ x i + 1)
    (hs : y 0 + y 1 + y 2 + deficit t = x 0 + x 1 + x 2 + deficit s + 1) :
    (t, fun i => y i - x i) ∈ transitions s := by
  apply transitions_complete
  · intro i
    have := hm i
    omega
  · have := hm 0
    have := hm 1
    have := hm 2
    omega

/-- Any prescribed sequence of legal transitions occurs in the recursive enumeration. -/
theorem trace_mem (n : ℕ) (f : Fin (n + 1) → Triple) (s : Fin (n + 1) → Bool)
    (h : History) (hlast : h.getLastD zero = f 0)
    (ht : ∀ j : Fin n,
      (s j.succ, fun i => f j.succ i - f j.castSucc i) ∈ transitions (s j.castSucc))
    (hm : ∀ j : Fin n, ∀ i, f j.castSucc i ≤ f j.succ i) :
    h ++ List.ofFn (fun j : Fin n => f j.succ) ∈ historiesFrom n (s 0) h := by
  induction n generalizing h with
  | zero => simp [historiesFrom]
  | succ n ih =>
    let d : Triple := fun i => f 1 i - f 0 i
    have hadd : add (h.getLastD zero) d = f 1 := by
      funext i
      rw [hlast]
      exact Nat.add_sub_of_le (hm 0 i)
    have hext : extend h d = h ++ [f 1] := by unfold extend; rw [hadd]
    apply List.mem_flatMap.mpr
    refine ⟨(s 1, d), ht 0, ?_⟩
    have hp := ih (fun j => f j.succ) (fun j => s j.succ) (extend h d) ?_ ?_ ?_
    · simpa [List.ofFn_succ, hext, List.append_assoc] using hp
    · simp [hext]
    · intro j
      exact ht j.succ
    · intro j i
      exact hm j.succ i

/-- Every monotone strict-floor profile is among the finite histories checked by the kernel. -/
theorem finite_row_history_mem {N : ℕ} (hN : 0 < N) (f : Fin N → Triple)
    (hzero : ∀ j : Fin N, j.val = 0 → f j = zero)
    (hm : ∀ j k : Fin N, k.val = j.val + 1 → ∀ i,
      f j i ≤ f k i ∧ f k i ≤ f j i + 1)
    (hs : ∀ j : Fin N,
      f j 0 + f j 1 + f j 2 + 1 = j.val + 1 ∨
      f j 0 + f j 1 + f j 2 + 2 = j.val + 1) :
    List.ofFn f ∈ histories N := by
  obtain ⟨n, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : N ≠ 0)
  let s : Fin (n + 1) → Bool := fun j => decide (f j 0 + f j 1 + f j 2 + 2 = j.val + 1)
  have hsum (j : Fin (n + 1)) :
      f j 0 + f j 1 + f j 2 + deficit (s j) = j.val + 1 := by
    rcases hs j with hj | hj
    · have hn : ¬ (f j 0 + f j 1 + f j 2 + 2 = j.val + 1) := by omega
      simpa only [s, hn, decide_false, deficit, Bool.false_eq_true, if_false] using hj
    · simp only [s, hj, decide_true, deficit, if_true]
  have hs0 : s 0 = false := by
    have hz := hzero 0 rfl
    simp [s, hz, zero]
  have hp := trace_mem n f s [zero] ?_ ?_ ?_
  · simpa [histories, hs0, List.ofFn_succ, hzero 0 rfl] using hp
  · simp [hzero 0 rfl]
  · intro j
    apply next_transition
    · exact hm j.castSucc j.succ rfl
    · have h0 := hsum j.castSucc
      have h1 := hsum j.succ
      simp only [Fin.val_succ, Fin.val_castSucc] at h0 h1
      omega
  · intro j i
    exact (hm j.castSucc j.succ rfl i).1

end SwitchingControl.Finite
