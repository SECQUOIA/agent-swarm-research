import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Combinatorics.SimpleGraph.Acyclic
import Mathlib.Data.List.Infix
import Mathlib.Data.Finset.Card
import Mathlib.Tactic
import Formal.MultilinearGap.StructuralSharpness

/-!
# Rooted tree decompositions and the sharpness flower

A finite rooted tree is represented by a finite, prefix-closed set of words.
The empty word is its root and the parent of a nonempty word deletes its last
letter. Thus there is exactly one root-to-node path: the successive prefixes.
This representation is a tree, not a series-parallel graph certificate.

`RootedTreeDecomposition` requires vertex and edge coverage and the usual
connectedness of the bags containing each vertex. Connectedness is expressed
by a highest containing bag and all prefix intervals descending from it.
`HasTreewidthAtMost` uses the cardinality bound `width + 1` on every bag.

The flower incidence graph has a width-two decomposition, including at zero
leaves. No characterization of arbitrary width-two graphs as series-parallel
networks is claimed in this file.
-/

namespace MultilinearGap.StructuralTreewidth

variable {V : Type*} [DecidableEq V]

/-- A genuine rooted tree decomposition, with tree nodes encoded by words. -/
structure RootedTreeDecomposition (G : SimpleGraph V) (Label : Type*)
    [DecidableEq Label] where
  nodes : Finset (List Label)
  root_mem : [] ∈ nodes
  prefix_closed : ∀ ⦃s t⦄, t ∈ nodes → s.IsPrefix t → s ∈ nodes
  bag : List Label → Finset V
  vertex_covered : ∀ v, ∃ t ∈ nodes, v ∈ bag t
  edge_covered : ∀ ⦃v w⦄, G.Adj v w → ∃ t ∈ nodes, v ∈ bag t ∧ w ∈ bag t
  connected_bags : ∀ v, ∃ r ∈ nodes, v ∈ bag r ∧
    ∀ t ∈ nodes, v ∈ bag t → r.IsPrefix t ∧
      ∀ s, r.IsPrefix s → s.IsPrefix t → v ∈ bag s

/-- The usual bag-size formulation of a treewidth upper bound. -/
def HasTreewidthAtMost (G : SimpleGraph V) (width : ℕ) : Prop :=
  ∃ (Label : Type) (_ : DecidableEq Label) (D : RootedTreeDecomposition G Label),
    ∀ t ∈ D.nodes, (D.bag t).card ≤ width + 1

/-- Removing graph edges preserves the same tree decomposition. -/
def RootedTreeDecomposition.of_le {G H : SimpleGraph V} {Label : Type*}
    [DecidableEq Label] (D : RootedTreeDecomposition H Label) (h : G ≤ H) :
    RootedTreeDecomposition G Label :=
  { D with edge_covered := fun _ _ hvw => D.edge_covered (h hvw) }

omit [DecidableEq V] in
theorem HasTreewidthAtMost.mono {G H : SimpleGraph V} {width : ℕ}
    (h : G ≤ H) (hH : HasTreewidthAtMost H width) : HasTreewidthAtMost G width := by
  obtain ⟨L, hL, D, hb⟩ := hH
  exact ⟨L, hL, D.of_le h, hb⟩

/-- An injective vertex map can pull a decomposition back to a subgraph. -/
noncomputable def RootedTreeDecomposition.pullback {W : Type*} [Fintype V]
    {G : SimpleGraph V} {H : SimpleGraph W} {Label : Type*} [DecidableEq Label]
    (D : RootedTreeDecomposition H Label) (f : G →g H) :
    RootedTreeDecomposition G Label := by
  classical
  refine {
    nodes := D.nodes
    root_mem := D.root_mem
    prefix_closed := D.prefix_closed
    bag := fun t => Finset.univ.filter (fun v => f v ∈ D.bag t)
    vertex_covered := ?_
    edge_covered := ?_
    connected_bags := ?_
  }
  · intro v
    obtain ⟨t, ht, hv⟩ := D.vertex_covered (f v)
    exact ⟨t, ht, by simpa using hv⟩
  · intro v w h
    obtain ⟨t, ht, hv, hw⟩ := D.edge_covered (f.map_adj h)
    exact ⟨t, ht, by simpa using hv, by simpa using hw⟩
  · intro v
    obtain ⟨r, hr, hv, hall⟩ := D.connected_bags (f v)
    refine ⟨r, hr, by simpa using hv, ?_⟩
    intro t ht hv
    obtain ⟨hprefix, hinterval⟩ := hall t ht (by simpa using hv)
    exact ⟨hprefix, fun s h₁ h₂ => by simpa using hinterval s h₁ h₂⟩

omit [DecidableEq V] in
theorem HasTreewidthAtMost.of_injective_hom {W : Type*} [Finite V]
    {G : SimpleGraph V} {H : SimpleGraph W} {width : ℕ}
    (f : G →g H) (hf : Function.Injective f) (hH : HasTreewidthAtMost H width) :
    HasTreewidthAtMost G width := by
  classical
  let _ := Fintype.ofFinite V
  obtain ⟨L, hL, D, hb⟩ := hH
  refine ⟨L, hL, D.pullback f, fun t ht => le_trans ?_ (hb t ht)⟩
  apply Finset.card_le_card_of_injOn f
  · intro v hv
    exact (Finset.mem_filter.mp hv).2
  · exact hf.injOn

/-- A bipartite incidence graph with separately indexed variables and factors. -/
def incidenceGraph {I J : Type*} (incident : I → J → Prop) : SimpleGraph (I ⊕ J) where
  Adj v w := match v, w with
    | .inl i, .inr j => incident i j
    | .inr j, .inl i => incident i j
    | _, _ => False
  symm := ⟨by intro v w; cases v <;> cases w <;> simp⟩
  loopless := ⟨by intro v; cases v <;> simp⟩

/-- Deleting incidences deletes edges, while retaining the original variable
and factor indices. This covers deletion of fixed box coordinates. -/
theorem incidenceGraph_mono {I J : Type*} {R S : I → J → Prop}
    (h : ∀ i j, R i j → S i j) : incidenceGraph R ≤ incidenceGraph S := by
  intro v w hvw
  cases v <;> cases w <;> simp only [incidenceGraph] at hvw ⊢
  · exact h _ _ hvw
  · exact h _ _ hvw

theorem incidence_treewidth_mono {I J : Type*} {R S : I → J → Prop} {width : ℕ}
    (h : ∀ i j, R i j → S i j) (hS : HasTreewidthAtMost (incidenceGraph S) width) :
    HasTreewidthAtMost (incidenceGraph R) width :=
  hS.mono (incidenceGraph_mono h)

/-- Variables are the anchor `none` and the leaves `some i`; factors are the
large product `none` and the bilinear anchor-leaf terms `some i`. -/
def flowerIncidence (n : ℕ) : Option (Fin n) → Option (Fin n) → Prop
  | none, none => False
  | none, some _ => True
  | some _, none => True
  | some i, some j => i = j

abbrev FlowerVertex (n : ℕ) := Option (Fin n) ⊕ Option (Fin n)

def flowerGraph (n : ℕ) : SimpleGraph (FlowerVertex n) :=
  incidenceGraph (flowerIncidence n)

def flowerNodes (n : ℕ) : Finset (List (Fin n)) :=
  {[]} ∪ Finset.univ.image (fun i => [i]) ∪ Finset.univ.image (fun i => [i, i])

@[simp] theorem mem_flowerNodes {n : ℕ} {t : List (Fin n)} :
    t ∈ flowerNodes n ↔ t = [] ∨ (∃ i, t = [i]) ∨ ∃ i, t = [i, i] := by
  simp only [flowerNodes, Finset.mem_union, Finset.mem_singleton, Finset.mem_image,
    Finset.mem_univ, true_and]
  constructor
  · rintro ((h | ⟨i, hi⟩) | ⟨i, hi⟩)
    · exact Or.inl h
    · exact Or.inr (Or.inl ⟨i, hi.symm⟩)
    · exact Or.inr (Or.inr ⟨i, hi.symm⟩)
  · rintro (h | ⟨i, hi⟩ | ⟨i, hi⟩)
    · exact Or.inl (Or.inl h)
    · exact Or.inl (Or.inr ⟨i, hi.symm⟩)
    · exact Or.inr ⟨i, hi.symm⟩

def flowerBag {n : ℕ} : List (Fin n) → Finset (FlowerVertex n)
  | [] => {.inl none, .inr none}
  | [i] => {.inl none, .inr none, .inl (some i)}
  | i :: _ :: _ => {.inl none, .inl (some i), .inr (some i)}

private theorem prefix_singleton_cases {α : Type*} {s : List α} {i : α}
    (h : s.IsPrefix [i]) : s = [] ∨ s = [i] := by
  simpa [List.prefix_cons_iff] using h

private theorem prefix_double_cases {α : Type*} {s : List α} {i : α}
    (h : s.IsPrefix [i, i]) : s = [] ∨ s = [i] ∨ s = [i, i] := by
  simp only [List.prefix_cons_iff, List.prefix_nil] at h
  rcases h with rfl | ⟨s, rfl, rfl | ⟨s, rfl, rfl⟩⟩ <;> simp

theorem flowerNodes_prefix_closed {n : ℕ} {s t : List (Fin n)}
    (ht : t ∈ flowerNodes n) (h : s.IsPrefix t) : s ∈ flowerNodes n := by
  rcases mem_flowerNodes.mp ht with rfl | ⟨i, rfl⟩ | ⟨i, rfl⟩
  · have := List.prefix_nil.mp h; simp [this]
  · rcases prefix_singleton_cases h with rfl | rfl <;> simp
  · rcases prefix_double_cases h with rfl | rfl | rfl <;> simp

theorem flower_vertex_covered (n : ℕ) (v : FlowerVertex n) :
    ∃ t ∈ flowerNodes n, v ∈ flowerBag t := by
  rcases v with (_ | i) | (_ | i)
  · exact ⟨[], by simp, by simp [flowerBag]⟩
  · exact ⟨[i], by simp, by simp [flowerBag]⟩
  · exact ⟨[], by simp, by simp [flowerBag]⟩
  · exact ⟨[i, i], by simp, by simp [flowerBag]⟩

theorem flower_edge_covered (n : ℕ) {v w : FlowerVertex n}
    (h : (flowerGraph n).Adj v w) :
    ∃ t ∈ flowerNodes n, v ∈ flowerBag t ∧ w ∈ flowerBag t := by
  rcases v with (_ | i) | (_ | i) <;>
    rcases w with (_ | j) | (_ | j) <;>
    simp only [flowerGraph, incidenceGraph, flowerIncidence] at h
  all_goals solve
  | contradiction
  | (refine ⟨[j, j], ?_, ?_⟩ <;> simp_all [flowerBag])
  | (refine ⟨[i, i], ?_, ?_⟩ <;> simp_all [flowerBag])
  | (refine ⟨[j], ?_, ?_⟩ <;> simp_all [flowerBag])
  | (refine ⟨[i], ?_, ?_⟩ <;> simp_all [flowerBag])

theorem flower_connected_bags (n : ℕ) (v : FlowerVertex n) :
    ∃ r ∈ flowerNodes n, v ∈ flowerBag r ∧
      ∀ t ∈ flowerNodes n, v ∈ flowerBag t → r.IsPrefix t ∧
        ∀ s, r.IsPrefix s → s.IsPrefix t → v ∈ flowerBag s := by
  rcases v with (_ | i) | (_ | i)
  · refine ⟨[], by simp, by simp [flowerBag], ?_⟩
    intro t ht hv
    refine ⟨by simp, ?_⟩
    intro s _ hs
    rcases mem_flowerNodes.mp (flowerNodes_prefix_closed ht hs) with
      rfl | ⟨j, rfl⟩ | ⟨j, rfl⟩ <;> simp [flowerBag]
  · refine ⟨[i], by simp, by simp [flowerBag], ?_⟩
    intro t ht hv
    rcases mem_flowerNodes.mp ht with rfl | ⟨j, rfl⟩ | ⟨j, rfl⟩
    · simp [flowerBag] at hv
    · simp only [flowerBag, Finset.mem_insert, Finset.mem_singleton,
        Sum.inl.injEq, Option.some_ne_none, Sum.inl_ne_inr, false_or,
        Option.some.injEq] at hv
      subst j
      refine ⟨by simp, ?_⟩
      intro s hi hs
      have : s = [i] := hs.eq_of_length_le hi.length_le
      simp [this, flowerBag]
    · simp only [flowerBag, Finset.mem_insert, Finset.mem_singleton,
        Sum.inl.injEq, Option.some_ne_none, Sum.inl_ne_inr, false_or,
        Option.some.injEq, or_false] at hv
      subst j
      refine ⟨by simp, ?_⟩
      intro s hi hs
      rcases prefix_double_cases hs with rfl | rfl | rfl
      · simp at hi
      · simp [flowerBag]
      · simp [flowerBag]
  · refine ⟨[], by simp, by simp [flowerBag], ?_⟩
    intro t ht hv
    refine ⟨by simp, ?_⟩
    intro s _ hs
    rcases mem_flowerNodes.mp ht with rfl | ⟨j, rfl⟩ | ⟨j, rfl⟩
    · have := List.prefix_nil.mp hs; simp [this, flowerBag]
    · rcases prefix_singleton_cases hs with rfl | rfl <;> simp [flowerBag]
    · simp [flowerBag] at hv
  · refine ⟨[i, i], by simp, by simp [flowerBag], ?_⟩
    intro t ht hv
    rcases mem_flowerNodes.mp ht with rfl | ⟨j, rfl⟩ | ⟨j, rfl⟩
    · simp [flowerBag] at hv
    · simp [flowerBag] at hv
    · simp only [flowerBag, Finset.mem_insert, Finset.mem_singleton,
        Sum.inr_ne_inl, false_or, Sum.inr.injEq, Option.some.injEq] at hv
      subst j
      refine ⟨by simp, ?_⟩
      intro s hi hs
      have : s = [i, i] := hs.eq_of_length_le hi.length_le
      simp [this, flowerBag]

def flowerDecomposition (n : ℕ) :
    RootedTreeDecomposition (flowerGraph n) (Fin n) where
  nodes := flowerNodes n
  root_mem := by simp
  prefix_closed := fun _ _ => flowerNodes_prefix_closed
  bag := flowerBag
  vertex_covered := flower_vertex_covered n
  edge_covered := fun _ _ => flower_edge_covered n
  connected_bags := flower_connected_bags n

theorem flowerBag_card_le_three {n : ℕ} (t : List (Fin n)) :
    (flowerBag t).card ≤ 3 := by
  cases t with
  | nil => simp [flowerBag]
  | cons i t =>
    cases t with
    | nil => simp [flowerBag]
    | cons j t => simp [flowerBag]

/-- The sharpness family's actual variable-factor incidence graph has
treewidth at most two. -/
theorem flower_hasTreewidthAtMost_two (n : ℕ) :
    HasTreewidthAtMost (flowerGraph n) 2 :=
  ⟨Fin n, inferInstance, flowerDecomposition n,
    fun t _ => flowerBag_card_le_three t⟩

/-- The named factor corresponds to the actual monomial scope. -/
def flowerFactorScope (n : ℕ) : Option (Fin n) → Finset (Option (Fin n))
  | none => StructuralSharpness.leafSupport n
  | some i => StructuralSharpness.pairSupport i

@[simp] theorem flowerIncidence_iff_mem {n : ℕ} (i j : Option (Fin n)) :
    flowerIncidence n i j ↔ i ∈ flowerFactorScope n j := by
  cases i <;> cases j <;>
    simp [flowerIncidence, flowerFactorScope, StructuralSharpness.leafSupport,
      StructuralSharpness.pairSupport]

theorem flowerFactorScope_injective (n : ℕ) :
    Function.Injective (flowerFactorScope n) := by
  intro i j h
  cases i with
  | none =>
    cases j with
    | none => rfl
    | some j => exact False.elim (StructuralSharpness.leafSupport_not_pair j h)
  | some i =>
    cases j with
    | none => exact False.elim (StructuralSharpness.leafSupport_not_pair i h.symm)
    | some j => exact congrArg some (StructuralSharpness.pairSupport_injective h)

def flowerFactorMap (n : ℕ) (j : Option (Fin n)) :
    {s // s ∈ StructuralSharpness.supports n} :=
  ⟨flowerFactorScope n j, by
    cases j <;> simp [flowerFactorScope, StructuralSharpness.supports]⟩

theorem flowerFactorMap_bijective (n : ℕ) : Function.Bijective (flowerFactorMap n) := by
  constructor
  · intro i j h
    exact flowerFactorScope_injective n (congrArg Subtype.val h)
  · rintro ⟨s, hs⟩
    simp only [StructuralSharpness.supports, Finset.mem_insert, Finset.mem_image,
      Finset.mem_univ, true_and] at hs
    rcases hs with rfl | ⟨i, rfl⟩
    · exact ⟨none, rfl⟩
    · exact ⟨some i, rfl⟩

noncomputable def flowerFactorEquiv (n : ℕ) :
    Option (Fin n) ≃ {s // s ∈ StructuralSharpness.supports n} :=
  Equiv.ofBijective (flowerFactorMap n) (flowerFactorMap_bijective n)

/-- Incidence graph whose factors are the actual distinct scopes used in the
verified polynomial, rather than auxiliary names for the factors. -/
def flowerSupportGraph (n : ℕ) :
    SimpleGraph (Option (Fin n) ⊕ {s // s ∈ StructuralSharpness.supports n}) :=
  incidenceGraph fun i s => i ∈ s.val

noncomputable def flowerSupportHom (n : ℕ) : flowerSupportGraph n →g flowerGraph n where
  toFun := Sum.map id (flowerFactorEquiv n).symm
  map_rel' := by
    intro v w h
    cases v with
    | inl i =>
      cases w with
      | inl j => exact False.elim h
      | inr s =>
        change flowerIncidence n i ((flowerFactorEquiv n).symm s)
        rw [flowerIncidence_iff_mem]
        have hs := congrArg Subtype.val ((flowerFactorEquiv n).apply_symm_apply s)
        change flowerFactorScope n ((flowerFactorEquiv n).symm s) = s.val at hs
        simpa only [hs] using (show i ∈ s.val from h)
    | inr s =>
      cases w with
      | inl i =>
        change flowerIncidence n i ((flowerFactorEquiv n).symm s)
        rw [flowerIncidence_iff_mem]
        have hs := congrArg Subtype.val ((flowerFactorEquiv n).apply_symm_apply s)
        change flowerFactorScope n ((flowerFactorEquiv n).symm s) = s.val at hs
        simpa only [hs] using (show i ∈ s.val from h)
      | inr t => exact False.elim h

theorem flowerSupportHom_injective (n : ℕ) : Function.Injective (flowerSupportHom n) := by
  exact Sum.map_injective.mpr ⟨Function.injective_id, (flowerFactorEquiv n).symm.injective⟩

theorem flower_supports_treewidth_le_two (n : ℕ) :
    HasTreewidthAtMost (flowerSupportGraph n) 2 := by
  classical
  exact (flower_hasTreewidthAtMost_two n).of_injective_hom
    (flowerSupportHom n) (flowerSupportHom_injective n)

omit [DecidableEq V] in
/-- Width one excludes every cycle. Choose the deepest highest bag of a cycle
vertex: both of its distinct cycle neighbors must occupy that same bag. -/
theorem HasTreewidthAtMost.isAcyclic {G : SimpleGraph V}
    (hG : HasTreewidthAtMost G 1) : G.IsAcyclic := by
  classical
  obtain ⟨L, hL, D, hcard⟩ := hG
  choose root hroot hmem hinterval using D.connected_bags
  intro u p hp
  obtain ⟨v, hv, hmax⟩ := Finset.exists_max_image p.support.toFinset
    (fun x => (root x).length) ⟨u, by simp⟩
  have hvp : v ∈ p.support := List.mem_toFinset.mp hv
  let q := p.rotate v hvp
  have hq : q.IsCycle := hp.rotate hvp
  have neighbors : ∀ w, w ∈ q.support → G.Adj v w → w ∈ D.bag (root v) := by
    intro w hw hvw
    obtain ⟨s, hs, hvs, hws⟩ := D.edge_covered hvw
    obtain ⟨hvp, _⟩ := hinterval v s hs hvs
    obtain ⟨hwp, hwinterval⟩ := hinterval w s hs hws
    apply hwinterval (root v) _ hvp
    apply List.prefix_of_prefix_length_le hwp hvp
    apply hmax w
    exact List.mem_toFinset.mpr ((p.mem_support_rotate_iff v _).mp hw)
  have ha := neighbors q.snd (q.getVert_mem_support 1) (q.adj_snd hq.not_nil)
  have hb := neighbors q.penultimate (q.getVert_mem_support (q.length - 1))
    (q.adj_penultimate hq.not_nil).symm
  have hsubset : {v, q.snd, q.penultimate} ⊆ D.bag (root v) := by
    intro x hx
    simp only [Finset.mem_insert, Finset.mem_singleton] at hx
    rcases hx with rfl | rfl | rfl
    · exact hmem x
    · exact ha
    · exact hb
  have hthree : ({v, q.snd, q.penultimate} : Finset V).card = 3 := by
    simp [(q.adj_snd hq.not_nil).ne, (q.adj_penultimate hq.not_nil).ne.symm,
      hq.snd_ne_penultimate]
  have := (Finset.card_le_card hsubset).trans (hcard (root v) (hroot v))
  omega

end MultilinearGap.StructuralTreewidth
