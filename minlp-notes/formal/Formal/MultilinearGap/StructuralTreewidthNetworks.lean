import Formal.MultilinearGap.StructuralTreewidthStates
import Formal.MultilinearGap.StructuralTreewidthGluing
import Mathlib.Combinatorics.SimpleGraph.Maps
import Mathlib.Combinatorics.SimpleGraph.Operations
import Mathlib.Tactic

/-!
# Concrete graph embeddings for two-terminal composition

All graphs use natural-number vertices, with terminals 0 and 1. The embeddings
below identify exactly the common terminal in series composition and exactly
the two terminals in parallel composition. Unused vertices are isolated. This
provides concrete graph operations independently of the finite signature rules.
-/
namespace MultilinearGap.StructuralTreewidth

private def seriesLeftFn : ℕ → ℕ
  | 0 => 0
  | 1 => 2
  | n + 2 => 2 * n + 5

private def seriesRightFn : ℕ → ℕ
  | 0 => 2
  | 1 => 1
  | n + 2 => 2 * n + 6

private def parallelLeftFn : ℕ → ℕ
  | 0 => 0
  | 1 => 1
  | n + 2 => 2 * n + 4

private def parallelRightFn : ℕ → ℕ
  | 0 => 0
  | 1 => 1
  | n + 2 => 2 * n + 5

private theorem seriesLeft_injective : Function.Injective seriesLeftFn := by
  intro i j h
  rcases i with _ | (_ | i) <;> rcases j with _ | (_ | j) <;>
    simp only [seriesLeftFn] at h ⊢ <;> omega

private theorem seriesRight_injective : Function.Injective seriesRightFn := by
  intro i j h
  rcases i with _ | (_ | i) <;> rcases j with _ | (_ | j) <;>
    simp only [seriesRightFn] at h ⊢ <;> omega

private theorem parallelLeft_injective : Function.Injective parallelLeftFn := by
  intro i j h
  rcases i with _ | (_ | i) <;> rcases j with _ | (_ | j) <;>
    simp only [parallelLeftFn] at h ⊢ <;> omega

private theorem parallelRight_injective : Function.Injective parallelRightFn := by
  intro i j h
  rcases i with _ | (_ | i) <;> rcases j with _ | (_ | j) <;>
    simp only [parallelRightFn] at h ⊢ <;> omega

def seriesLeft : ℕ ↪ ℕ := ⟨seriesLeftFn, seriesLeft_injective⟩
def seriesRight : ℕ ↪ ℕ := ⟨seriesRightFn, seriesRight_injective⟩
def parallelLeft : ℕ ↪ ℕ := ⟨parallelLeftFn, parallelLeft_injective⟩
def parallelRight : ℕ ↪ ℕ := ⟨parallelRightFn, parallelRight_injective⟩

@[simp] theorem seriesLeft_zero : seriesLeft 0 = 0 := rfl
@[simp] theorem seriesLeft_one : seriesLeft 1 = 2 := rfl
@[simp] theorem seriesRight_zero : seriesRight 0 = 2 := rfl
@[simp] theorem seriesRight_one : seriesRight 1 = 1 := rfl
@[simp] theorem parallelLeft_zero : parallelLeft 0 = 0 := rfl
@[simp] theorem parallelLeft_one : parallelLeft 1 = 1 := rfl
@[simp] theorem parallelRight_zero : parallelRight 0 = 0 := rfl
@[simp] theorem parallelRight_one : parallelRight 1 = 1 := rfl

/-- Series children meet only at the identified sink/source. -/
theorem series_intersection (i j : ℕ) :
    seriesLeft i = seriesRight j ↔ i = 1 ∧ j = 0 := by
  rcases i with _ | (_ | i) <;> rcases j with _ | (_ | j) <;>
    simp [seriesLeft, seriesRight, Function.Embedding.coeFn_mk,
      seriesLeftFn, seriesRightFn]
  all_goals omega

/-- Parallel children meet precisely at their common terminals. -/
theorem parallel_intersection (i j : ℕ) :
    parallelLeft i = parallelRight j ↔ (i = 0 ∧ j = 0) ∨ (i = 1 ∧ j = 1) := by
  rcases i with _ | (_ | i) <;> rcases j with _ | (_ | j) <;>
    simp [parallelLeft, parallelRight, Function.Embedding.coeFn_mk,
      parallelLeftFn, parallelRightFn]
  all_goals omega

open scoped Classical in
/-- Glue vertex labels along compatible embedded pieces; isolated vertices get false. -/
noncomputable def glueLabels (f g : ℕ ↪ ℕ) (a b : ℕ → Bool) (x : ℕ) : Bool :=
  if h : ∃ i, f i = x then a h.choose
  else if h : ∃ j, g j = x then b h.choose else false

@[simp] theorem glueLabels_left (f g : ℕ ↪ ℕ) (a b : ℕ → Bool) (i : ℕ) :
    glueLabels f g a b (f i) = a i := by
  classical
  have h : ∃ j, f j = f i := ⟨i, rfl⟩
  simp only [glueLabels, dif_pos h]
  exact congrArg a (f.injective h.choose_spec)

/-- Agreement at identified vertices is the only requirement for the second piece. -/
theorem glueLabels_right (f g : ℕ ↪ ℕ) (a b : ℕ → Bool)
    (hcompat : ∀ i j, f i = g j → a i = b j) (j : ℕ) :
    glueLabels f g a b (g j) = b j := by
  classical
  unfold glueLabels
  split_ifs with h h'
  · exact hcompat h.choose j h.choose_spec
  · exact congrArg b (g.injective h'.choose_spec)
  · exact False.elim (h' ⟨j, rfl⟩)

theorem series_labels_compatible {a b : ℕ → Bool} (h : a 1 = b 0) :
    ∀ i j, seriesLeft i = seriesRight j → a i = b j := by
  intro i j hij
  obtain ⟨rfl, rfl⟩ := (series_intersection i j).mp hij
  exact h

theorem parallel_labels_compatible {a b : ℕ → Bool}
    (h₀ : a 0 = b 0) (h₁ : a 1 = b 1) :
    ∀ i j, parallelLeft i = parallelRight j → a i = b j := by
  intro i j hij
  rcases (parallel_intersection i j).mp hij with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
  · exact h₀
  · exact h₁

/-- Concrete series composition. -/
def seriesGraph (G H : SimpleGraph ℕ) : SimpleGraph ℕ :=
  G.map seriesLeft ⊔ H.map seriesRight

/-- Concrete parallel composition. -/
def parallelGraph (G H : SimpleGraph ℕ) : SimpleGraph ℕ :=
  G.map parallelLeft ⊔ H.map parallelRight

/-- An embedded edge joining the two series pieces must meet at vertex 2. -/
theorem series_meet_only_at (G H : SimpleGraph ℕ) {a b c : ℕ}
    (h₁ : (G.map seriesLeft).Adj a b) (h₂ : (H.map seriesRight).Adj b c) : b = 2 := by
  obtain ⟨i, j, _, _, hj⟩ := (SimpleGraph.map_adj _ _ _ _).mp h₁
  obtain ⟨k, t, _, hk, _⟩ := (SimpleGraph.map_adj _ _ _ _).mp h₂
  have := (series_intersection j k).mp (hj.trans hk.symm)
  simpa [this.1] using hj.symm

/-- The analogous shared-vertex fact for parallel composition. -/
theorem parallel_meet_only_at (G H : SimpleGraph ℕ) {a b c : ℕ}
    (h₁ : (G.map parallelLeft).Adj a b) (h₂ : (H.map parallelRight).Adj b c) :
    b = 0 ∨ b = 1 := by
  obtain ⟨i, j, _, _, hj⟩ := (SimpleGraph.map_adj _ _ _ _).mp h₁
  obtain ⟨k, t, _, hk, _⟩ := (SimpleGraph.map_adj _ _ _ _).mp h₂
  rcases (parallel_intersection j k).mp (hj.trans hk.symm) with ⟨rfl, _⟩ | ⟨rfl, _⟩
  · exact Or.inl (by simpa using hj.symm)
  · exact Or.inr (by simpa using hj.symm)

/-- Both endpoint types and all internal factor types are preserved by composition. -/
theorem bipartite_glue (G H : SimpleGraph ℕ) (f g : ℕ ↪ ℕ) (a b : ℕ → Bool)
    (ha : ∀ i j, G.Adj i j → a i ≠ a j)
    (hb : ∀ i j, H.Adj i j → b i ≠ b j)
    (hc : ∀ i j, f i = g j → a i = b j) :
    ∀ u v, (G.map f ⊔ H.map g).Adj u v →
      glueLabels f g a b u ≠ glueLabels f g a b v := by
  intro u v huv
  rcases huv with huv | huv
  · obtain ⟨i, j, hij, rfl, rfl⟩ := (SimpleGraph.map_adj _ _ _ _).mp huv
    simpa using ha i j hij
  · obtain ⟨i, j, hij, rfl, rfl⟩ := (SimpleGraph.map_adj _ _ _ _).mp huv
    simpa [glueLabels_right f g a b hc] using hb i j hij

/-- Embed the two vertices of the base edge as the distinguished terminals. -/
def edgeEmbedding : Bool ↪ ℕ := ⟨fun b => if b then 1 else 0, by decide⟩

@[simp] theorem edgeEmbedding_false : edgeEmbedding false = 0 := rfl
@[simp] theorem edgeEmbedding_true : edgeEmbedding true = 1 := rfl

/-- Natural-number realization of the two-terminal network syntax. -/
def Network.graph {l r d : Bool} : Network l r d → SimpleGraph ℕ
  | .edgeVF => TreewidthGraph.edgeGraph.map edgeEmbedding
  | .edgeFV => TreewidthGraph.edgeGraph.map edgeEmbedding
  | .series a b => seriesGraph a.graph b.graph
  | .parallel _ a b => parallelGraph a.graph b.graph

/-- The type of each vertex in the concrete network graph. -/
noncomputable def Network.factor {l r d : Bool} : Network l r d → ℕ → Bool
  | .edgeVF => fun n => n == 1
  | .edgeFV => fun n => n == 0
  | .series a b => glueLabels seriesLeft seriesRight a.factor b.factor
  | .parallel _ a b => glueLabels parallelLeft parallelRight a.factor b.factor

@[simp] theorem Network.factor_zero {l r d : Bool} (N : Network l r d) :
    N.factor 0 = l := by
  induction N with
  | edgeVF => rfl
  | edgeFV => rfl
  | series a b ih₁ ih₂ =>
    change glueLabels seriesLeft seriesRight a.factor b.factor (seriesLeft 0) = _
    rw [glueLabels_left]
    exact ih₁
  | parallel h a b ih₁ ih₂ =>
    change glueLabels parallelLeft parallelRight a.factor b.factor (parallelLeft 0) = _
    rw [glueLabels_left]
    exact ih₁

@[simp] theorem Network.factor_one {l r d : Bool} (N : Network l r d) :
    N.factor 1 = r := by
  induction N with
  | edgeVF => rfl
  | edgeFV => rfl
  | @series l m r d₁ d₂ a b ih₁ ih₂ =>
    change glueLabels seriesLeft seriesRight a.factor b.factor (seriesRight 1) = r
    rw [glueLabels_right _ _ _ _ (series_labels_compatible (by simp [ih₁]))]
    exact ih₂
  | parallel h a b ih₁ ih₂ =>
    change glueLabels parallelLeft parallelRight a.factor b.factor (parallelLeft 1) = _
    rw [glueLabels_left]
    exact ih₁

/-- Every realized network is bipartite with precisely its declared vertex types. -/
theorem Network.bipartite {l r d : Bool} (N : Network l r d) :
    ∀ u v, N.graph.Adj u v → N.factor u ≠ N.factor v := by
  induction N with
  | edgeVF =>
    intro u v huv
    obtain ⟨i, j, hij, rfl, rfl⟩ := (SimpleGraph.map_adj _ _ _ _).mp huv
    cases i <;> cases j <;> simp_all [Network.factor, TreewidthGraph.edgeGraph]
  | edgeFV =>
    intro u v huv
    obtain ⟨i, j, hij, rfl, rfl⟩ := (SimpleGraph.map_adj _ _ _ _).mp huv
    cases i <;> cases j <;> simp_all [Network.factor, TreewidthGraph.edgeGraph]
  | series a b ih₁ ih₂ =>
    exact bipartite_glue _ _ _ _ _ _ ih₁ ih₂ (series_labels_compatible (by simp))
  | parallel h a b ih₁ ih₂ =>
    exact bipartite_glue _ _ _ _ _ _ ih₁ ih₂ (parallel_labels_compatible (by simp) (by simp))

end MultilinearGap.StructuralTreewidth

namespace MultilinearGap.TreewidthGraph

open StructuralTreewidth

variable {V : Type*} {H K : SimpleGraph V} {s t : V}

/-- The exact path signature, including its cycle condition, is preserved by
parallel graph composition. The separation hypothesis concerns actual edges. -/
theorem realizesSignature_parallel (factor color : V → Bool) (hst : s ≠ t)
    (hsep : MeetOnlyAtPair H K s t) {a b : Signature}
    (ha : RealizesSignature factor color H s t a)
    (hb : RealizesSignature factor color K s t b)
    (hc : parallelCompatible (factor s) (factor t) a b) :
    RealizesSignature factor color (H ⊔ K) s t (parallelSignature a b) := by
  refine ⟨good_union_at_pair hst hsep factor color ha.1 hb.1 ?_, ha.2.1, ha.2.2.1, ?_⟩
  · intro p q hp hq c hpc hqc
    have hpa := (ha.2.2.2 c _).mpr ⟨p, hp, hpc, rfl⟩
    have hpb := (hb.2.2.2 c _).mpr ⟨q, hq, hqc, rfl⟩
    have hxor := hc.2.2 c (Finset.mem_univ _) _ hpa _ hpb
    have hzero : ∀ (x y : ZMod 2) (l r : Bool),
        Bool.xor (Bool.xor (parityBit x) (parityBit y)) (Bool.xor l r) = false →
        x + y = (if l then 1 else 0) + (if r then 1 else 0) := by decide
    exact hzero _ _ _ _ hxor
  · intro c bit
    have hset : bit ∈ pathSet (parallelSignature a b) c ↔
        bit ∈ pathSet a c ∨ bit ∈ pathSet b c := by
      cases c <;> simp [pathSet, parallelSignature]
    rw [hset]
    constructor
    · intro h
      rcases h with h | h
      · obtain ⟨p, hp, hm, hb⟩ := (ha.2.2.2 c bit).mp h
        refine ⟨p.mapLe le_sup_left, hp.mapLe _, ?_, ?_⟩
        · simpa [Monochromatic] using hm
        · simpa [pathParity] using hb
      · obtain ⟨p, hp, hm, hb⟩ := (hb.2.2.2 c bit).mp h
        refine ⟨p.mapLe le_sup_right, hp.mapLe _, ?_, ?_⟩
        · simpa [Monochromatic] using hm
        · simpa [pathParity] using hb
    · rintro ⟨p, hp, hm, hbit⟩
      rcases parallel_path_edges_in_one_piece hsep p hp with he | he
      · left
        apply (ha.2.2.2 c bit).mpr
        refine ⟨p.transfer H he, hp.transfer he, ?_, ?_⟩
        · simpa [Monochromatic] using hm
        · simpa [pathParity] using hbit
      · right
        apply (hb.2.2.2 c bit).mpr
        refine ⟨p.transfer K he, hp.transfer he, ?_, ?_⟩
        · simpa [Monochromatic] using hm
        · simpa [pathParity] using hbit

/-- The exact path signature is preserved by series graph composition. -/
theorem realizesSignature_series {m : V} (factor color : V → Bool)
    (hsep : MeetOnlyAt H K m) (hst : s ≠ t) (hsm : s ≠ m) (hmt : m ≠ t)
    (hs : ∀ x, ¬ K.Adj s x) (ht : ∀ x, ¬ H.Adj t x) {a b : Signature}
    (ha : RealizesSignature factor color H s m a)
    (hb : RealizesSignature factor color K m t b) :
    RealizesSignature factor color (H ⊔ K) s t (seriesSignature (factor m) a b) := by
  refine ⟨good_union_at_vertex hsep factor color ha.1 hb.1,
    ha.2.1, hb.2.2.1, ?_⟩
  intro c bit
  have hset : bit ∈ pathSet (seriesSignature (factor m) a b) c ↔
      ∃ x ∈ pathSet a c, ∃ y ∈ pathSet b c,
        Bool.xor (Bool.xor x y) (factor m) = bit := by
    cases c <;> simp [pathSet, seriesSignature, xorPaths, Finset.mem_image] <;> tauto
  rw [hset]
  constructor
  · rintro ⟨x, hx, y, hy, hxy⟩
    obtain ⟨p, hp, hmp, hpx⟩ := (ha.2.2.2 c x).mp hx
    obtain ⟨q, hq, hmq, hqy⟩ := (hb.2.2.2 c y).mp hy
    refine ⟨(p.mapLe le_sup_left).append (q.mapLe le_sup_right),
      series_append_isPath hsep p q hp hq hsm hmt, ?_, ?_⟩
    · rw [monochromatic_append]
      simpa [Monochromatic] using And.intro hmp hmq
    · rw [pathParity_append_bit]
      simpa [pathParity] using (congrArg₂
        (fun x y => Bool.xor (Bool.xor x y) (factor m)) hpx hqy).trans hxy
  · rintro ⟨p, hp, hm, hbit⟩
    obtain ⟨q, r, hq, hr, hqe, hre, hqr⟩ :=
      series_path_decomposition hsep hst hsm hmt hs ht p hp
    have hmono : Monochromatic factor color c q ∧ Monochromatic factor color c r := by
      rw [← monochromatic_append, hqr]
      exact hm
    refine ⟨parityBit (pathParity factor q), ?_, parityBit (pathParity factor r), ?_, ?_⟩
    · apply (ha.2.2.2 c _).mpr
      refine ⟨q.transfer H hqe, hq.transfer hqe, ?_, ?_⟩
      · simpa [Monochromatic] using hmono.1
      · simp [pathParity]
    · apply (hb.2.2.2 c _).mpr
      refine ⟨r.transfer K hre, hr.transfer hre, ?_, ?_⟩
      · simpa [Monochromatic] using hmono.2
      · simp [pathParity]
    · rw [← pathParity_append_bit, hqr]
      exact hbit

end MultilinearGap.TreewidthGraph
