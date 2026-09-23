import Mathlib.Data.Finset.Prod
import Mathlib.Tactic

/-!
# Two-terminal coloring states

Kernel verification of the active/blocking parity invariant under arbitrary
series and parallel composition. Signatures record terminal colors and all
possible parities of monochromatic terminal paths, including factor endpoints.

This file proves the finite signature rules. `StructuralTreewidthNetworkSound`
and `StructuralTreewidthPieceColoring` supply their actual graph interpretations;
the passage from a tree decomposition to pieces is proved separately.
-/
namespace MultilinearGap.StructuralTreewidth

/-- False denotes a variable vertex, true a factor vertex. -/
abbrev VertexType := Bool

/-- Variable-terminal colors are canonically false and have no semantic meaning. -/
structure Signature where
  leftColor : Bool
  rightColor : Bool
  pathsFalse : Finset Bool
  pathsTrue : Finset Bool
  deriving DecidableEq

def pathSet (s : Signature) (c : Bool) : Finset Bool :=
  if c then s.pathsTrue else s.pathsFalse

/-- Reversing terminals leaves the set of terminal-path parities unchanged. -/
def Signature.reverse (s : Signature) : Signature :=
  ⟨s.rightColor, s.leftColor, s.pathsFalse, s.pathsTrue⟩

@[simp] theorem pathSet_reverse (s : Signature) (c : Bool) :
    pathSet s.reverse c = pathSet s c := rfl

@[simp] theorem Signature.reverse_reverse (s : Signature) : s.reverse.reverse = s := rfl

/-- Exactly color `c` has paths, all of parity `p`. -/
def active (l r : Bool) (c p : Bool) : Signature :=
  ⟨l && c, r && c, if c then ∅ else {p}, if c then {p} else ∅⟩

/-- Prescribed factor-terminal colors, with no monochromatic terminal path. -/
def blocked (l r : Bool) (c : Bool) : Signature := ⟨l && c, r && c, ∅, ∅⟩

def distinct (c : Bool) : Signature := ⟨c, !c, ∅, ∅⟩

def needsBlocking (l r direct p : Bool) : Bool :=
  if l == r then if l then p else !p else !direct

/-- All alternatives required by one parity in the analytic invariant. -/
def required (l r direct p : Bool) : Finset Signature :=
  {active l r false p, active l r true p} ∪
    (if needsBlocking l r direct p then {blocked l r false, blocked l r true} else ∅) ∪
    (if l && r then {distinct false, distinct true} else ∅)

theorem required_reverse (l r direct p : Bool) :
    (required l r direct p).image Signature.reverse = required r l direct p := by
  cases l <;> cases r <;> cases direct <;> cases p <;> decide

/-- A direct terminal edge has mixed types and odd factor parity. -/
def Valid (l r direct p : Bool) : Prop := direct = true → l ≠ r ∧ p = true

instance (l r direct p : Bool) : Decidable (Valid l r direct p) :=
  inferInstanceAs (Decidable (direct = true → l ≠ r ∧ p = true))

/-- XOR of path parities, correcting the shared factor vertex. -/
def xorPaths (a b : Finset Bool) (middle : Bool) : Finset Bool :=
  (a ×ˢ b).image fun pq => xor (xor pq.1 pq.2) middle

def seriesSignature (middle : Bool) (a b : Signature) : Signature :=
  ⟨a.leftColor, b.rightColor,
    xorPaths a.pathsFalse b.pathsFalse middle, xorPaths a.pathsTrue b.pathsTrue middle⟩

def seriesStates (middle : Bool) (A B : Finset Signature) : Finset Signature :=
  ((A ×ˢ B).filter fun ab => ab.1.rightColor = ab.2.leftColor).image
    fun ab => seriesSignature middle ab.1 ab.2

/-- Excludes every odd cycle formed by monochromatic paths of the two children. -/
def parallelCompatible (l r : Bool) (a b : Signature) : Prop :=
  a.leftColor = b.leftColor ∧ a.rightColor = b.rightColor ∧
    ∀ c ∈ (Finset.univ : Finset Bool), ∀ p ∈ pathSet a c, ∀ q ∈ pathSet b c,
      xor (xor p q) (xor l r) = false

instance (l r : Bool) (a b : Signature) : Decidable (parallelCompatible l r a b) :=
  inferInstanceAs (Decidable (a.leftColor = b.leftColor ∧ a.rightColor = b.rightColor ∧
    ∀ c ∈ (Finset.univ : Finset Bool), ∀ p ∈ pathSet a c, ∀ q ∈ pathSet b c,
      xor (xor p q) (xor l r) = false))

def parallelSignature (a b : Signature) : Signature :=
  ⟨a.leftColor, a.rightColor, a.pathsFalse ∪ b.pathsFalse, a.pathsTrue ∪ b.pathsTrue⟩

def parallelStates (l r : Bool) (A B : Finset Signature) : Finset Signature :=
  ((A ×ˢ B).filter fun ab => parallelCompatible l r ab.1 ab.2).image
    fun ab => parallelSignature ab.1 ab.2

def parallelParity (l r d₁ d₂ p₁ p₂ : Bool) : Bool :=
  if l == r then if l then p₁ && p₂ else p₁ || p₂
  else if d₁ then p₁ else if d₂ then p₂ else p₁

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Exhausting the seven Boolean parameters checks 128 finite composition cases.
/-- All series cases, including endpoint colors and the shared-factor correction. -/
theorem required_series (l m r d₁ d₂ p₁ p₂ : Bool)
    (h₁ : Valid l m d₁ p₁) (h₂ : Valid m r d₂ p₂) :
    required l r false (xor (xor p₁ p₂) m) ⊆
      seriesStates m (required l m d₁ p₁) (required m r d₂ p₂) := by
  revert h₁ h₂
  cases l <;> cases m <;> cases r <;> cases d₁ <;> cases d₂ <;>
    cases p₁ <;> cases p₂ <;> decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Each Boolean case reduces finite sets of complete endpoint/path signatures.
/-- All parallel cases, excluding duplicate direct terminal edges. -/
theorem required_parallel (l r d₁ d₂ p₁ p₂ : Bool)
    (h₁ : Valid l r d₁ p₁) (h₂ : Valid l r d₂ p₂)
    (hsimple : (d₁ && d₂) = false) :
    required l r (d₁ || d₂) (parallelParity l r d₁ d₂ p₁ p₂) ⊆
      parallelStates l r (required l r d₁ p₁) (required l r d₂ p₂) := by
  revert h₁ h₂ hsimple
  cases l <;> cases r <;> cases d₁ <;> cases d₂ <;>
    cases p₁ <;> cases p₂ <;> decide

theorem parallel_valid (l r d₁ d₂ p₁ p₂ : Bool)
    (h₁ : Valid l r d₁ p₁) (h₂ : Valid l r d₂ p₂) :
    Valid l r (d₁ || d₂) (parallelParity l r d₁ d₂ p₁ p₂) := by
  revert h₁ h₂
  cases l <;> cases r <;> cases d₁ <;> cases d₂ <;>
    cases p₁ <;> cases p₂ <;> decide

/-- Recursive network syntax with endpoint types and the direct-edge indicator. -/
inductive Network : VertexType → VertexType → Bool → Type
  | edgeVF : Network false true true
  | edgeFV : Network true false true
  | series {l m r d₁ d₂ : Bool} : Network l m d₁ → Network m r d₂ → Network l r false
  | parallel {l r d₁ d₂ : Bool} : (d₁ && d₂) = false →
      Network l r d₁ → Network l r d₂ → Network l r (d₁ || d₂)

def Network.states {l r direct : Bool} : Network l r direct → Finset Signature
  | .edgeVF => required false true true true
  | .edgeFV => required true false true true
  | .series (m := m) a b => seriesStates m a.states b.states
  | .parallel (l := l) (r := r) _ a b => parallelStates l r a.states b.states

private theorem seriesStates_mono {m : Bool} {A B A' B' : Finset Signature}
    (hA : A ⊆ A') (hB : B ⊆ B') : seriesStates m A B ⊆ seriesStates m A' B' := by
  apply Finset.image_subset_image
  apply Finset.filter_subset_filter
  exact Finset.product_subset_product hA hB

private theorem parallelStates_mono {l r : Bool} {A B A' B' : Finset Signature}
    (hA : A ⊆ A') (hB : B ⊆ B') : parallelStates l r A B ⊆ parallelStates l r A' B' := by
  apply Finset.image_subset_image
  apply Finset.filter_subset_filter
  exact Finset.product_subset_product hA hB

/-- Every network admits the entire invariant, for one color-independent parity. -/
theorem Network.invariant {l r direct : Bool} (N : Network l r direct) :
    ∃ p, Valid l r direct p ∧ required l r direct p ⊆ N.states := by
  induction N with
  | edgeVF => exact ⟨true, by decide, Finset.Subset.refl _⟩
  | edgeFV => exact ⟨true, by decide, Finset.Subset.refl _⟩
  | @series l m r d₁ d₂ a b ih₁ ih₂ =>
    obtain ⟨p₁, h₁, hp₁⟩ := ih₁
    obtain ⟨p₂, h₂, hp₂⟩ := ih₂
    refine ⟨xor (xor p₁ p₂) m, by simp [Valid], ?_⟩
    exact (required_series l m r d₁ d₂ p₁ p₂ h₁ h₂).trans
      (seriesStates_mono hp₁ hp₂)
  | @parallel l r d₁ d₂ hsimple a b ih₁ ih₂ =>
    obtain ⟨p₁, h₁, hp₁⟩ := ih₁
    obtain ⟨p₂, h₂, hp₂⟩ := ih₂
    refine ⟨parallelParity l r d₁ d₂ p₁ p₂, parallel_valid l r d₁ d₂ p₁ p₂ h₁ h₂, ?_⟩
    exact (required_parallel l r d₁ d₂ p₁ p₂ h₁ h₂ hsimple).trans
      (parallelStates_mono hp₁ hp₂)

/-- No number of recursive compositions exhausts the available signatures. -/
theorem Network.states_nonempty {l r direct : Bool} (N : Network l r direct) :
    N.states.Nonempty := by
  obtain ⟨p, _, hp⟩ := N.invariant
  refine ⟨active l r false p, hp ?_⟩
  simp [required]

end MultilinearGap.StructuralTreewidth
