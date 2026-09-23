import Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected
import Mathlib.Combinatorics.SimpleGraph.Paths
import Mathlib.Algebra.Ring.Parity

/-! A graph whose simple cycles have even length has a proper Boolean coloring. -/
namespace MultilinearGap.StructuralEvenCycle
open SimpleGraph
noncomputable section
variable {V : Type*} {G : SimpleGraph V}

/-- Removing repeated vertices preserves length parity when every simple cycle
is even. The removed closed segment is a simple cycle or a two-edge return. -/
theorem bypass_length_mod_two [DecidableEq V]
    (heven : ∀ v (p : G.Walk v v), p.IsCycle → Even p.length)
    {u v : V} (p : G.Walk u v) : p.bypass.length % 2 = p.length % 2 := by
  induction p with
  | nil => simp [Walk.bypass]
  | @cons u w v huw p ih =>
    by_cases hs : u ∈ p.bypass.support
    · have hpath := p.bypass_isPath.takeUntil hs
      have hpos : 0 < (p.bypass.takeUntil u hs).length := by
        by_contra hn
        have hn' : (p.bypass.takeUntil u hs).Nil := Walk.length_eq_zero_iff.mp (by omega)
        exact huw.ne hn'.eq.symm
      have hloop : Even ((p.bypass.takeUntil u hs).length + 1) := by
        by_cases hl : 3 ≤ (p.bypass.takeUntil u hs).length + 1
        · apply heven u ((p.bypass.takeUntil u hs).cons huw)
          apply Walk.isCycle_iff_isPath_tail_and_le_length.mpr
          exact ⟨by simpa using hpath, by simpa using hl⟩
        · have : (p.bypass.takeUntil u hs).length + 1 = 2 := by omega
          rw [this]
          exact ⟨1, rfl⟩
      have hsum := congrArg Walk.length (p.bypass.take_spec hs)
      simp only [Walk.length_append] at hsum
      have hmod := Nat.even_iff.mp hloop
      simp only [Walk.bypass, dif_pos hs, Walk.length_cons]
      omega
    · simp only [Walk.bypass, dif_neg hs, Walk.length_cons]
      omega

/-- Every closed walk is even, allowing repeated edges and immediate returns. -/
theorem closed_walk_even
    (heven : ∀ v (p : G.Walk v v), p.IsCycle → Even p.length)
    (u : V) (p : G.Walk u u) : Even p.length := by
  classical
  have h := bypass_length_mod_two heven p
  have hz : p.bypass.length = 0 :=
    Walk.length_eq_zero_iff.mpr (Walk.isPath_iff_nil.mp p.bypass_isPath)
  apply Nat.even_iff.mpr
  omega

/-- Paths between the same endpoints have the same length parity. -/
theorem walk_length_mod_two
    (heven : ∀ v (p : G.Walk v v), p.IsCycle → Even p.length)
    {u v : V} (p q : G.Walk u v) : p.length % 2 = q.length % 2 := by
  have h := Nat.even_iff.mp (closed_walk_even heven u (p.append q.reverse))
  simp only [Walk.length_append, Walk.length_reverse] at h
  omega

/-- Pick one root in each component and color by the parity of a walk from it.
The even-cycle hypothesis makes that parity independent of the chosen walk. -/
theorem exists_bool_coloring (G : SimpleGraph V)
    (heven : ∀ v (p : G.Walk v v), p.IsCycle → Even p.length) :
    ∃ color : V → Bool, ∀ {u v}, G.Adj u v → color u ≠ color v := by
  classical
  let root (v : V) := (G.connectedComponentMk v).out
  have hr (v : V) : G.Reachable (root v) v :=
    ConnectedComponent.exact (Quot.out_eq (G.connectedComponentMk v))
  let path (v : V) : G.Walk (root v) v := Classical.choice (hr v)
  refine ⟨fun v => decide ((path v).length % 2 = 0), ?_⟩
  intro u v huv hc
  have hroot : root u = root v :=
    congrArg Quot.out (ConnectedComponent.sound huv.reachable)
  have hp := walk_length_mod_two heven ((path u).concat huv)
    ((path v).copy hroot.symm rfl)
  simp only [Walk.length_concat, Walk.length_copy] at hp
  have hc' : (path u).length % 2 = 0 ↔ (path v).length % 2 = 0 :=
    decide_eq_decide.mp hc
  omega

end
end MultilinearGap.StructuralEvenCycle
