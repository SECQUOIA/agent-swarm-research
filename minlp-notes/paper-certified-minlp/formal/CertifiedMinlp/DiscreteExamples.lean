import CertifiedMinlp.DiscreteSolutions

/-! Kernel-evaluated boundary examples for the structured derivation checker. -/
namespace CertifiedMinlp.Discrete.Examples

private def row (a b : ℚ) (kind : Kind) : Row 1 := ⟨fun _ => a, b, kind⟩
private def step (r : Row 1) (deps : Finset ℕ) (assumption : Bool)
    (reason : Reason) : Step 1 := ⟨⟨r, deps, assumption⟩, reason⟩
private def ints : Fin 1 → Bool := fun _ => true
private def master : List (Row 1) := [row 1 (1 / 2) .ge]

/-- Split at zero: the left branch contradicts x ≥ 1/2; the right gives x ≥ 1. -/
def splitProof : List (Step 1) :=
  [step (row 1 (1 / 2) .ge) ∅ false (.original 0),
   step (row 1 0 .le) {1} true .assume,
   step (row 1 1 .ge) {2} true .assume,
   step (row 0 (1 / 2) .ge) {1} false (.combine .ge [(1, 0), (-1, 1)]),
   step (row 1 1 .ge) ∅ false (.unsplit 1 2 3 2)]

theorem split_accepted : check master ints none splitProof = true := by decide +kernel

theorem reversed_split_accepted : check master ints none
    (splitProof.take 4 ++ [step (row 1 1 .ge) ∅ false (.unsplit 2 1 2 3)]) = true := by
  decide +kernel

/-- The same bound follows by integer rounding. -/
theorem integer_rounding_accepted : check master ints none
    [step (row 1 (1 / 2) .ge) ∅ false (.original 0),
     step (row 1 1 .ge) ∅ false (.round .ge [(1, 0)])] = true := by decide +kernel

theorem continuous_rounding_rejected : check master (fun _ => false) none
    [step (row 1 (1 / 2) .ge) ∅ false (.original 0),
     step (row 1 1 .ge) ∅ false (.round .ge [(1, 0)])] = false := by decide +kernel

theorem equality_rounding_rejected : rounded ints (row 1 1 .eq) = none := by decide +kernel

/-- Checking continues after an already valid assumption-free bound. -/
theorem bad_later_row_rejected : check master ints none
    (splitProof ++ [step (row 0 0 .le) ∅ false (.combine .le [(0, 99)])]) = false := by
  decide +kernel

theorem self_reference_rejected : check master ints none
    [step (row 1 0 .ge) ∅ false (.combine .ge [(1, 0)])] = false := by decide +kernel

/-- A branch proof using both assumptions retains the other branch's index. -/
def crossBranchPrefix : List (Step 1) :=
  [step (row 1 0 .le) {0} true .assume,
   step (row 1 1 .ge) {1} true .assume,
   step (row 0 1 .ge) {0, 1} false (.combine .ge [(1, 1), (-1, 0)])]

theorem cross_dependency_retained : check ([] : List (Row 1)) ints none
    (crossBranchPrefix ++ [step (row 1 1 .ge) {1} false (.unsplit 0 1 2 1)]) = true := by
  decide +kernel

theorem cross_dependency_erasure_rejected : check ([] : List (Row 1)) ints none
    (crossBranchPrefix ++ [step (row 1 1 .ge) ∅ false (.unsplit 0 1 2 1)]) = false := by
  decide +kernel

/-- A syntactically present zero term contributes no assumptions. -/
theorem zero_multiplier_drops_dependency : check master ints none
    [step (row 1 (1 / 2) .ge) ∅ false (.original 0),
     step (row 1 0 .le) {1} true .assume,
     step (row 1 (1 / 2) .ge) ∅ false (.combine .ge [(1, 0), (0, 1)])] = true := by
  decide +kernel

theorem solution_without_incumbent_rejected : check master ints none
    [step (row 1 1 .le) ∅ false .solution] = false := by decide +kernel

/-- All finite incumbents are validated even if the proof does not use them. -/
theorem checked_bound_accepted :
    checkBound master ints (fun _ => 1) 1 [fun _ => 2, fun _ => 1] splitProof = true := by
  decide +kernel

theorem fractional_incumbent_rejected :
    checkBound master ints (fun _ => 1) 1 [fun _ => 1 / 2] splitProof = false := by
  decide +kernel

theorem infeasible_incumbent_rejected :
    checkBound master ints (fun _ => 1) 1 [fun _ => 0] splitProof = false := by
  decide +kernel

theorem minimum_incumbent_cutoff :
    solutionCutoff (fun _ : Fin 1 => 1) [fun _ => 2, fun _ => 1] =
      some (row 1 1 .le) := by decide +kernel

theorem strict_incumbent_cutoff_rejected :
    check master ints (solutionCutoff (fun _ => 1) [fun _ => 1])
      [step (row 1 0 .le) ∅ false .solution] = false := by decide +kernel

/-- A later valid row with unused assumptions cannot hide an earlier bound. -/
theorem earlier_bound_survives_later_assumption :
    checkBound master ints (fun _ => 1) 1 []
      (splitProof ++ [step (row 1 (-1) .le) {5} true .assume]) = true := by
  decide +kernel

/-- This example invokes the general checker theorem on actual accepted data. -/
theorem integer_half_bound :
    CertifiedMinlp.LowerBoundOn (masterFeasible master ints) (objective (fun _ => 1)) 1 := by
  simpa using checked_bound (β := 1) checked_bound_accepted

end CertifiedMinlp.Discrete.Examples
