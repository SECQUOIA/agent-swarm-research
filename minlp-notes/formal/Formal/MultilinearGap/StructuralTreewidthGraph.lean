import Formal.MultilinearGap.StructuralTreewidthStates
import Mathlib.Combinatorics.SimpleGraph.Paths
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

/-!
# Walk semantics for the one-sided series-parallel coloring invariant

Terminal-path parity counts both endpoints. Cycle parity omits the repeated
initial vertex. These conventions imply the shared-vertex correction in series
composition and the two-terminal correction in parallel composition. This file
proves these identities for actual `SimpleGraph.Walk`s; it does not assert a
series-parallel decomposition theorem.
-/

namespace MultilinearGap.TreewidthGraph

variable {V : Type*} {G : SimpleGraph V} {u v w : V}

/-- `true` marks a factor vertex, the side of the graph that receives colors. -/
def factorWeight (factor : V → Bool) (x : V) : ZMod 2 := if factor x then 1 else 0

/-- Factor-vertex parity along a terminal walk, including both terminals. -/
def pathParity (factor : V → Bool) (p : G.Walk u v) : ZMod 2 :=
  (p.support.map (factorWeight factor)).sum

/-- Factor-vertex parity with the initial vertex omitted. For a simple cycle,
this counts each vertex exactly once. -/
def cycleParity (factor : V → Bool) (p : G.Walk u u) : ZMod 2 :=
  (p.support.tail.map (factorWeight factor)).sum

/-- All factor vertices on the walk, including endpoints, have color `c`. -/
def Monochromatic (factor color : V → Bool) (c : Bool) (p : G.Walk u v) : Prop :=
  ∀ x ∈ p.support, factor x = true → color x = c

/-- Every monochromatic-factor simple cycle has even factor-vertex count. -/
def Good (factor color : V → Bool) (G : SimpleGraph V) : Prop :=
  ∀ (u : V) (p : G.Walk u u), p.IsCycle →
    ∀ c, Monochromatic factor color c p → cycleParity factor p = 0

lemma pathParity_eq_start_add_tail (factor : V → Bool) (p : G.Walk u v) :
    pathParity factor p = factorWeight factor u +
      (p.support.tail.map (factorWeight factor)).sum := by
  exact (congrArg (fun l : List V => (l.map (factorWeight factor)).sum)
    p.cons_tail_support).symm

/-- Series composition counts the shared vertex only once. -/
theorem pathParity_append (factor : V → Bool) (p : G.Walk u v) (q : G.Walk v w) :
    pathParity factor (p.append q) =
      pathParity factor p + pathParity factor q - factorWeight factor v := by
  rw [pathParity, SimpleGraph.Walk.support_append, List.map_append, List.sum_append]
  rw [pathParity_eq_start_add_tail factor q]
  unfold pathParity
  ring

@[simp] theorem pathParity_reverse (factor : V → Bool) (p : G.Walk u v) :
    pathParity factor p.reverse = pathParity factor p := by
  simp [pathParity, List.map_reverse]

/-- Closing two terminal paths removes one copy of each terminal. -/
theorem cycleParity_append (factor : V → Bool) (p : G.Walk u v) (q : G.Walk v u) :
    cycleParity factor (p.append q) =
      pathParity factor p + pathParity factor q -
        factorWeight factor u - factorWeight factor v := by
  unfold cycleParity
  rw [SimpleGraph.Walk.tail_support_append, List.map_append, List.sum_append]
  rw [pathParity_eq_start_add_tail factor p, pathParity_eq_start_add_tail factor q]
  ring

/-- Parallel paths use the two-terminal correction when closed into a walk. -/
theorem cycleParity_append_reverse (factor : V → Bool)
    (p q : G.Walk u v) :
    cycleParity factor (p.append q.reverse) =
      pathParity factor p + pathParity factor q -
        factorWeight factor u - factorWeight factor v := by
  rw [cycleParity_append, pathParity_reverse]

@[simp] theorem monochromatic_append (factor color : V → Bool) (c : Bool)
    (p : G.Walk u v) (q : G.Walk v w) :
    Monochromatic factor color c (p.append q) ↔
      Monochromatic factor color c p ∧ Monochromatic factor color c q := by
  simp only [Monochromatic, SimpleGraph.Walk.mem_support_append_iff]
  grind

@[simp] theorem monochromatic_reverse (factor color : V → Bool) (c : Bool)
    (p : G.Walk u v) :
    Monochromatic factor color c p.reverse ↔ Monochromatic factor color c p := by
  simp [Monochromatic]

/-- Any factor terminal fixes the color of a monochromatic terminal path. -/
theorem monochromatic_start (factor color : V → Bool) (c : Bool)
    (p : G.Walk u v) (hp : Monochromatic factor color c p) (hu : factor u = true) :
    color u = c := hp u p.start_mem_support hu

theorem monochromatic_end (factor color : V → Bool) (c : Bool)
    (p : G.Walk u v) (hp : Monochromatic factor color c p) (hv : factor v = true) :
    color v = c := hp v p.end_mem_support hv

/-- Distinctly colored factor terminals block every monochromatic path. -/
theorem no_monochromatic_of_distinct_factor_terminals
    (factor color : V → Bool) (p : G.Walk u v)
    (hu : factor u = true) (hv : factor v = true) (hc : color u ≠ color v) :
    ∀ c, ¬ Monochromatic factor color c p := by
  intro c hp
  exact hc ((monochromatic_start factor color c p hp hu).trans
    (monochromatic_end factor color c p hp hv).symm)

/-- Swapping colors preserves monochromatic walks, with their colors swapped. -/
@[simp] theorem monochromatic_swap (factor color : V → Bool) (c : Bool)
    (p : G.Walk u v) :
    Monochromatic factor (fun x => !(color x)) (!c) p ↔
      Monochromatic factor color c p := by
  simp [Monochromatic]

/-- This swap is the operation used to match an articulation vertex. -/
theorem good_swap (factor color : V → Bool) (h : Good factor color G) :
    Good factor (fun x => !(color x)) G := by
  intro x p hp c hc
  apply h x p hp (!c)
  intro y hy hf
  have hh := hc y hy hf
  cases c <;> cases he : color y <;> simp_all

/-- Exact compatibility test preventing odd cycles between parallel paths. -/
theorem parallel_cycle_even_iff (factor : V → Bool) (p q : G.Walk u v) :
    cycleParity factor (p.append q.reverse) = 0 ↔
      pathParity factor p + pathParity factor q =
        factorWeight factor u + factorWeight factor v := by
  rw [cycleParity_append_reverse]
  constructor <;> intro h <;> linear_combination h

/-- The parity sum is exactly the number of factor vertices, modulo two. -/
lemma factorWeight_sum_eq_count (factor : V → Bool) (xs : List V) :
    (xs.map (factorWeight factor)).sum = ((xs.filter factor).length : ZMod 2) := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
    cases hx : factor x <;> simp [factorWeight, hx, ih, add_comm]

theorem cycleParity_eq_count (factor : V → Bool) (p : G.Walk u u) :
    cycleParity factor p = ((p.support.tail.filter factor).length : ZMod 2) :=
  factorWeight_sum_eq_count factor p.support.tail

theorem cycleParity_zero_iff_even (factor : V → Bool) (p : G.Walk u u) :
    cycleParity factor p = 0 ↔ Even (p.support.tail.filter factor).length := by
  rw [cycleParity_eq_count, ZMod.natCast_eq_zero_iff_even]

/-- For simple cycles the list being counted has no repeated factor vertices. -/
theorem cycle_factor_support_nodup (factor : V → Bool) (p : G.Walk u u)
    (hp : p.IsCycle) : (p.support.tail.filter factor).Nodup :=
  hp.support_nodup.filter _

/-- Convert arithmetic modulo two to the Boolean convention of the state table. -/
def parityBit (a : ZMod 2) : Bool := decide (a = 1)

lemma parityBit_correction : ∀ (a b : ZMod 2) (t : Bool),
    parityBit (a + b - (if t then 1 else 0)) =
      Bool.xor (Bool.xor (parityBit a) (parityBit b)) t := by decide

lemma parityBit_two_corrections : ∀ (a b : ZMod 2) (s t : Bool),
    parityBit (a + b - (if s then 1 else 0) - (if t then 1 else 0)) =
      Bool.xor (Bool.xor (parityBit a) (parityBit b)) (Bool.xor s t) := by decide

lemma parityBit_eq_false : ∀ a : ZMod 2, parityBit a = false ↔ a = 0 := by decide

/-- Boolean XOR form of the series-composition equation. -/
theorem pathParity_append_bit (factor : V → Bool) (p : G.Walk u v)
    (q : G.Walk v w) :
    parityBit (pathParity factor (p.append q)) =
      Bool.xor (Bool.xor (parityBit (pathParity factor p))
        (parityBit (pathParity factor q))) (factor v) := by
  rw [pathParity_append]
  exact parityBit_correction _ _ _

/-- Boolean XOR form of the parallel-composition cycle test. -/
theorem parallel_cycle_even_iff_xor (factor : V → Bool) (p q : G.Walk u v) :
    cycleParity factor (p.append q.reverse) = 0 ↔
      Bool.xor (Bool.xor (parityBit (pathParity factor p))
        (parityBit (pathParity factor q))) (Bool.xor (factor u) (factor v)) = false := by
  rw [← parityBit_eq_false, cycleParity_append_reverse]
  simp only [factorWeight, parityBit_two_corrections]

/-- A good coloring can be made to match either color at a chosen articulation
vertex. Only a global color swap is needed. -/
theorem exists_good_matching_vertex (factor color : V → Bool)
    (h : Good factor color G) (x : V) (c : Bool) :
    ∃ color' : V → Bool, Good factor color' G ∧ color' x = c := by
  by_cases hx : color x = c
  · exact ⟨color, h, hx⟩
  · refine ⟨fun y => !(color y), good_swap factor color h, ?_⟩
    cases hc : color x <;> cases c <;> simp_all

/-- A bipartite edge has one factor endpoint, so the base terminal-path parity
is odd. -/
theorem pathParity_edge (factor : V → Bool) (h : G.Adj u v)
    (hb : factor u ≠ factor v) :
    pathParity factor (.cons h .nil) = 1 := by
  cases hu : factor u <;> cases hv : factor v <;>
    simp_all [pathParity, factorWeight]

/-- Exact interpretation of a state by a coloring of an actual graph. Path sets
record all simple terminal paths; the coloring must satisfy the cycle condition. -/
def RealizesSignature (factor color : V → Bool) (G : SimpleGraph V)
    (u v : V) (s : StructuralTreewidth.Signature) : Prop :=
  Good factor color G ∧
  s.leftColor = (factor u && color u) ∧
  s.rightColor = (factor v && color v) ∧
  ∀ c b, b ∈ StructuralTreewidth.pathSet s c ↔
    ∃ p : G.Walk u v, p.IsPath ∧ Monochromatic factor color c p ∧
      parityBit (pathParity factor p) = b

/-- The graph with just the two distinct terminal vertices and their edge. -/
abbrev edgeGraph : SimpleGraph Bool := ⊤

def edgeWalk : edgeGraph.Walk false true := .cons (by decide) .nil

lemma edgeWalk_isPath : edgeWalk.IsPath := by
  simp [edgeWalk, SimpleGraph.Walk.isPath_def]

lemma edgeGraph_path_unique (p : edgeGraph.Walk false true) (hp : p.IsPath) :
    p = edgeWalk := by
  have hlen := hp.length_lt
  cases p with
  | cons h q =>
    cases q with
    | nil => rfl
    | cons h' q =>
      simp only [SimpleGraph.Walk.length_cons, Fintype.card_bool] at hlen
      omega

lemma edgeGraph_good (factor color : Bool → Bool) : Good factor color edgeGraph := by
  intro x p hp c hc
  have hmax := hp.support_nodup.length_le_card
  have hmin := hp.three_le_length
  simp only [List.length_tail, SimpleGraph.Walk.length_support, Fintype.card_bool] at hmax
  omega

/-- The type marking for either orientation of the bipartite base edge. -/
def edgeFactor (left : Bool) (x : Bool) : Bool := if x then !left else left

/-- Each required active signature of either oriented base edge has a genuine
good coloring realizing exactly its recorded monochromatic path parities. -/
theorem edge_realizes_active (left c : Bool) :
    RealizesSignature (edgeFactor left) (fun _ => c) edgeGraph false true
      (StructuralTreewidth.active left (!left) c true) := by
  refine ⟨edgeGraph_good _ _, ?_, ?_, ?_⟩
  · simp [StructuralTreewidth.active, edgeFactor]
  · simp [StructuralTreewidth.active, edgeFactor]
  · intro d b
    constructor
    · intro hb
      refine ⟨edgeWalk, edgeWalk_isPath, ?_, ?_⟩
      · cases left <;> cases c <;> cases d <;> cases b <;>
          simp_all [StructuralTreewidth.pathSet, StructuralTreewidth.active,
            Monochromatic, edgeWalk, edgeFactor]
      · cases left <;> cases c <;> cases d <;> cases b <;>
          simp_all [StructuralTreewidth.pathSet, StructuralTreewidth.active,
            pathParity, factorWeight, edgeWalk, edgeFactor, parityBit]
    · rintro ⟨p, hp, hm, hb⟩
      obtain rfl := edgeGraph_path_unique p hp
      cases left <;> cases c <;> cases d <;> cases b <;>
        simp_all [StructuralTreewidth.pathSet, StructuralTreewidth.active,
          Monochromatic, pathParity, factorWeight, edgeWalk, edgeFactor, parityBit]

/-- Values on variable vertices have no effect on monochromatic-factor walks. -/
theorem monochromatic_congr_color (factor color color' : V → Bool)
    (h : ∀ x, factor x = true → color x = color' x) (c : Bool) (p : G.Walk u v) :
    Monochromatic factor color c p ↔ Monochromatic factor color' c p := by
  constructor <;> intro hm x hx hf
  · rw [← h x hf]
    exact hm x hx hf
  · rw [h x hf]
    exact hm x hx hf

/-- Canonical false colors on the uncolored side simplify graph gluing. -/
theorem realizesSignature_normalize (factor color : V → Bool)
    {s : StructuralTreewidth.Signature} (h : RealizesSignature factor color G u v s) :
    RealizesSignature factor (fun x => factor x && color x) G u v s := by
  have hc : ∀ x, factor x = true → color x = (factor x && color x) := by
    intro x hx
    simp [hx]
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro x p hp c hm
    exact h.1 x p hp c ((monochromatic_congr_color _ _ _ hc c p).mpr hm)
  · simpa [Bool.and_assoc] using h.2.1
  · simpa [Bool.and_assoc] using h.2.2.1
  · intro c b
    rw [h.2.2.2 c b]
    simp_rw [monochromatic_congr_color _ _ _ hc]

end MultilinearGap.TreewidthGraph
