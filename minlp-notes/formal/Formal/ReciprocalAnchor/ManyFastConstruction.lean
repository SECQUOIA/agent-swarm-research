import Formal.ReciprocalAnchor.ManySortCost
import Formal.ReciprocalAnchor.ManyParallelLines
import Formal.ReciprocalAnchor.ManyStackGeometry

/-! Complete rational envelope-stack construction and its charged operation bound. -/
namespace ReciprocalAnchor.ManyLeaf.FastEnvelope

/-- Sort, remove parallel lines, and build the envelope stack. The charge counts
one unit per sorting/deduplication rational comparison and twelve units per
stack position tested. A `Redundant` test contains at most four comparisons,
three subtractions, three multiplications and one addition (eleven operations),
so twelve units is a uniform upper charge, including terminal positions.
This is an arithmetic-operation charge, not a bit-operation count. -/
def buildStack (input : List Line) : List Line × ℕ :=
  let sorted := countedSort Line.slope input
  let distinct := parallelDedup sorted.1
  let result := scan distinct.1 []
  (result.1, sorted.2 + distinct.2 + 12 * result.2)

theorem push_length (c : Line) (stack : List Line) :
    (push c stack).1.length ≤ stack.length + 1 := by
  induction stack using push.induct c with
  | case1 b a rest hr ih =>
    rw [push, if_pos hr]
    simp only [List.length_cons] at *
    omega
  | case2 b a rest hr => simp [push, hr]
  | case3 stack hr =>
    cases stack with
    | nil => simp [push]
    | cons b rest =>
      cases rest with
      | nil => simp [push]
      | cons a rest => exact False.elim (hr b a rest rfl)

theorem scan_length (input stack : List Line) :
    (scan input stack).1.length ≤ input.length + stack.length := by
  induction input generalizing stack with
  | nil => simp [scan]
  | cons c cs ih =>
    simp only [scan, List.length_cons]
    have hi := ih (push c stack).1
    have hp := push_length c stack
    omega

theorem buildStack_valueReal (input : List Line) (x : ℝ) :
    valueReal (buildStack input).1 x = valueReal input x := by
  simp only [buildStack, scan_valueReal, valueReal, parallelDedup_valueReal]
  rw [max_eq_left (valueReal_nonneg _ x)]
  exact valueReal_perm (countedSort_spec Line.slope input).1 x

theorem buildStack_good (input : List Line) : Good (buildStack input).1 := by
  apply scan_good _ []
  · exact parallelDedup_strict _ (countedSort_spec Line.slope input).2.1
  · trivial
  · simp

theorem buildStack_length (input : List Line) :
    (buildStack input).1.length ≤ input.length := by
  have hs := (countedSort_spec Line.slope input).1.length_eq
  have hd := (parallelDedup_members_cost (countedSort Line.slope input).1).2.1
  have hc := scan_length (parallelDedup (countedSort Line.slope input).1).1 []
  simp only [List.length_nil, Nat.add_zero] at hc
  exact hc.trans (hd.trans hs.le)

theorem buildStack_cost (input : List Line) :
    (buildStack input).2 ≤ input.length * (input.length.log2 + 27) := by
  obtain ⟨hp, _, hs⟩ := countedSort_spec Line.slope input
  obtain ⟨_, hd, hc⟩ := parallelDedup_members_cost (countedSort Line.slope input).1
  have ht := scan_cost_le (parallelDedup (countedSort Line.slope input).1).1
  rw [hp.length_eq] at hd hc
  simp only [buildStack]
  nlinarith

/-- The constructed stack is geometrically valid, has no more than N lines,
preserves the envelope at every real argument, and has O(N log N) charge. -/
theorem buildStack_spec (input : List Line) :
    Good (buildStack input).1 ∧
    (buildStack input).1.length ≤ input.length ∧
    (∀ x : ℝ, valueReal (buildStack input).1 x = valueReal input x) ∧
    (buildStack input).2 ≤ input.length * (input.length.log2 + 27) :=
  ⟨buildStack_good input, buildStack_length input, buildStack_valueReal input,
    buildStack_cost input⟩

end ReciprocalAnchor.ManyLeaf.FastEnvelope
