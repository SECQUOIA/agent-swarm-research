import CertifiedMinlp.Discrete

/-! Executable rational solution validation, finite incumbent selection, and
unrestricted objective bounds from checked discrete certificates. -/
namespace CertifiedMinlp.Discrete
open scoped BigOperators

variable {n : ℕ}

def rationalValue (c : Fin n → ℚ) (x : Fin n → ℚ) : ℚ := ∑ i, c i * x i

def realPoint (x : Fin n → ℚ) : Fin n → ℝ := fun i => x i

def objective (c : Fin n → ℚ) (x : Fin n → ℝ) : ℝ := ∑ i, (c i : ℝ) * x i

def rationalHolds (r : Row n) (x : Fin n → ℚ) : Bool :=
  match r.kind with
  | .le => decide (rationalValue r.coeff x ≤ r.rhs)
  | .ge => decide (r.rhs ≤ rationalValue r.coeff x)
  | .eq => decide (rationalValue r.coeff x = r.rhs)

def checkSolution (master : List (Row n)) (ints : Fin n → Bool)
    (x : Fin n → ℚ) : Bool :=
  decide (∀ i, ints i = true → x i = (⌊x i⌋ : ℚ)) && master.all (fun r => rationalHolds r x)

lemma rationalValue_cast (c : Fin n → ℚ) (x : Fin n → ℚ) :
    (rationalValue c x : ℝ) = objective c (realPoint x) := by
  simp [rationalValue, objective, realPoint]

theorem rationalHolds_sound {r : Row n} {x : Fin n → ℚ}
    (h : rationalHolds r x = true) : Holds r (realPoint x) := by
  have hv : value r (realPoint x) = (rationalValue r.coeff x : ℝ) :=
    (rationalValue_cast _ _).symm
  cases hk : r.kind <;> simp only [rationalHolds, hk, decide_eq_true_eq] at h <;>
    simp only [Holds, hk, Rel, hv] <;> exact_mod_cast h

theorem checkSolution_sound {master : List (Row n)} {ints : Fin n → Bool}
    {x : Fin n → ℚ} (h : checkSolution master ints x = true) :
    realPoint x ∈ masterFeasible master ints := by
  obtain ⟨hi, hm⟩ := Bool.and_eq_true_iff.mp h
  constructor
  · intro i hflag
    refine ⟨⌊x i⌋, ?_⟩
    have hx := of_decide_eq_true hi i hflag
    change (x i : ℝ) = (⌊x i⌋ : ℝ)
    exact_mod_cast hx
  · intro r hr
    exact rationalHolds_sound (List.all_eq_true.mp hm r hr)

/-- Empty lists have no incumbent. A nonempty list is searched by exact comparisons. -/
def bestSolution (c : Fin n → ℚ) : List (Fin n → ℚ) → Option (Fin n → ℚ)
  | [] => none
  | x :: xs => match bestSolution c xs with
    | none => some x
    | some y => some (if rationalValue c x ≤ rationalValue c y then x else y)

theorem bestSolution_spec (c : Fin n → ℚ) (xs : List (Fin n → ℚ)) :
    (bestSolution c xs = none ↔ xs = []) ∧
    ∀ x, bestSolution c xs = some x →
      x ∈ xs ∧ ∀ y ∈ xs, rationalValue c x ≤ rationalValue c y := by
  induction xs with
  | nil => simp [bestSolution]
  | cons a xs ih =>
    cases hb : bestSolution c xs with
    | none =>
      have hx : xs = [] := ih.1.mp hb
      subst xs
      simp [bestSolution]
    | some b =>
      obtain ⟨hmem, hmin⟩ := ih.2 b hb
      constructor
      · simp [bestSolution, hb]
      · intro x hx
        simp only [bestSolution, hb, Option.some.injEq] at hx
        by_cases hab : rationalValue c a ≤ rationalValue c b
        · simp only [hab, if_true] at hx
          subst x
          refine ⟨by simp, ?_⟩
          intro y hy
          rcases List.mem_cons.mp hy with rfl | hy
          · exact le_rfl
          · exact hab.trans (hmin y hy)
        · simp only [hab, if_false] at hx
          subst x
          refine ⟨by simp [hmem], ?_⟩
          intro y hy
          rcases List.mem_cons.mp hy with rfl | hy
          · exact le_of_lt (lt_of_not_ge hab)
          · exact hmin y hy

def lowerBoundRow (c : Fin n → ℚ) (β : ℚ) : Row n := ⟨c, β, .ge⟩

def solutionCutoff (c : Fin n → ℚ) (solutions : List (Fin n → ℚ)) : Option (Row n) :=
  (bestSolution c solutions).map (fun x => ⟨c, rationalValue c x, .le⟩)

def checkBound (master : List (Row n)) (ints : Fin n → Bool)
    (c : Fin n → ℚ) (β : ℚ) (solutions : List (Fin n → ℚ))
    (steps : List (Step n)) : Bool :=
  solutions.all (checkSolution master ints) &&
  check master ints (solutionCutoff c solutions) steps &&
  (steps.map Step.entry).any (fun e => decide (e.deps = ∅) && dominates e.row (lowerBoundRow c β))

/-- All provided solutions and all derivation rows are checked. The optional
cutoff comes from the least objective value in that finite solution list. -/
theorem checked_bound {master : List (Row n)} {ints : Fin n → Bool}
    {c : Fin n → ℚ} {β : ℚ} {solutions : List (Fin n → ℚ)} {steps : List (Step n)}
    (h : checkBound master ints c β solutions steps = true) :
    CertifiedMinlp.LowerBoundOn (masterFeasible master ints) (objective c) β := by
  obtain ⟨hc, he⟩ := Bool.and_eq_true_iff.mp h
  obtain ⟨hsol, hc⟩ := Bool.and_eq_true_iff.mp hc
  obtain ⟨e, hemem, hetest⟩ := List.any_eq_true.mp he
  obtain ⟨hdeps, hdom⟩ := Bool.and_eq_true_iff.mp hetest
  have hd := of_decide_eq_true hdeps
  cases hb : bestSolution c solutions with
  | none =>
    have hc' : check master ints none steps = true := by simpa [solutionCutoff, hb] using hc
    exact checked_assumption_free (fun _ hx => hx.2) (fun _ hx => hx.1)
      (by simp) hc' hemem hd hdom
  | some incumbent =>
    have hm := (bestSolution_spec c solutions).2 incumbent hb |>.1
    have hi := checkSolution_sound (List.all_eq_true.mp hsol incumbent hm)
    apply CertifiedMinlp.incumbent_cutoff_lifting _ _ (realPoint incumbent) _ hi
    intro x hx hxcut
    let S : Set (Fin n → ℝ) := {x | x ∈ masterFeasible master ints ∧
      objective c x ≤ objective c (realPoint incumbent)}
    have hcut : ∀ r, solutionCutoff c solutions = some r → ∀ y ∈ S, Holds r y := by
      intro r hr y hy
      have hr' : (⟨c, rationalValue c incumbent, .le⟩ : Row n) = r := by
        simpa [solutionCutoff, hb] using hr
      subst r
      change objective c y ≤ (rationalValue c incumbent : ℝ)
      rw [rationalValue_cast]
      exact hy.2
    exact checked_assumption_free (S := S) (fun _ hy => hy.1.2) (fun _ hy => hy.1.1)
      hcut hc hemem hd hdom x ⟨hx, hxcut⟩

def checkInfeasible (master : List (Row n)) (ints : Fin n → Bool)
    (steps : List (Step n)) : Bool :=
  check master ints none steps &&
  (steps.map Step.entry).any (fun e => decide (e.deps = ∅) && contradictory e.row)

theorem checked_infeasible {master : List (Row n)} {ints : Fin n → Bool}
    {steps : List (Step n)} (h : checkInfeasible master ints steps = true) :
    masterFeasible master ints = ∅ := by
  obtain ⟨hc, he⟩ := Bool.and_eq_true_iff.mp h
  obtain ⟨e, hemem, hetest⟩ := List.any_eq_true.mp he
  obtain ⟨hdeps, hcontra⟩ := Bool.and_eq_true_iff.mp hetest
  apply Set.eq_empty_iff_forall_notMem.mpr
  intro x hx
  have he := check_sound (S := masterFeasible master ints)
    (fun _ hx => hx.2) (fun _ hx => hx.1) (by simp) hc e hemem x hx
    (by simp [Assumptions, of_decide_eq_true hdeps])
  exact contradictory_sound hcontra he

/-- Maximization uses the same checker after negating the objective. -/
theorem checked_max_bound {master : List (Row n)} {ints : Fin n → Bool}
    {c : Fin n → ℚ} {β : ℚ} {solutions : List (Fin n → ℚ)} {steps : List (Step n)}
    (h : checkBound master ints (fun i => -c i) β solutions steps = true) :
    ∀ x ∈ masterFeasible master ints, objective c x ≤ -(β : ℝ) := by
  intro x hx
  have hh := checked_bound h x hx
  have hv : objective (fun i => -c i) x = -objective c x := by
    simp [objective, Finset.sum_neg_distrib]
  rw [hv] at hh
  linarith

end CertifiedMinlp.Discrete
