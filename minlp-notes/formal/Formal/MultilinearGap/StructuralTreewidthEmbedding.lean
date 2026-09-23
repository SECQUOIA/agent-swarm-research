import Formal.MultilinearGap.StructuralTreewidthGraph
import Mathlib.Combinatorics.SimpleGraph.Operations

/-! Preservation of exact coloring signatures under injective graph embeddings. -/

namespace MultilinearGap.TreewidthGraph

variable {V W : Type*} {G : SimpleGraph V}

/-- The canonical graph map, with its vertex function definitionally the embedding. -/
abbrev embeddingHom (f : V ↪ W) (G : SimpleGraph V) : G →g G.map f where
  toFun := f
  map_rel' := fun h => SimpleGraph.map_adj_apply.mpr h

/-- A walk in a mapped graph between embedded vertices comes from a child walk. -/
theorem exists_walk_map (f : V ↪ W) {u v : V}
    (p : (G.map f).Walk (f u) (f v)) :
    ∃ q : G.Walk u v, q.map (embeddingHom f G) = p := by
  have aux : ∀ {a b} (p : (G.map f).Walk a b) (u v : V)
      (hu : f u = a) (hv : f v = b),
      ∃ q : G.Walk u v, (q.map (embeddingHom f G)).copy hu hv = p := by
    intro a b p
    induction p with
    | @nil a =>
      intro u v hu hv
      have huv : u = v := f.injective (hu.trans hv.symm)
      subst v
      subst a
      exact ⟨.nil, rfl⟩
    | @cons a b c hab p ih =>
      intro u v hu hv
      obtain ⟨x, y, hxy, hxa, hyb⟩ := (SimpleGraph.map_adj f G a b).mp hab
      have hxu : x = u := f.injective (hxa.trans hu.symm)
      subst x
      obtain ⟨q, hq⟩ := ih y v hyb hv
      subst a
      subst b
      subst c
      exact ⟨.cons hxy q, by simpa using congrArg (SimpleGraph.Walk.cons hab) hq⟩
  exact aux p u v rfl rfl

@[simp] theorem pathParity_map_embedding (f : V ↪ W) (factor : V → Bool)
    (F : W → Bool) (hf : ∀ x, F (f x) = factor x) {u v : V} (p : G.Walk u v) :
    pathParity F (p.map (embeddingHom f G)) = pathParity factor p := by
  simp [pathParity, List.map_map, Function.comp_def, factorWeight, hf]
  rfl

@[simp] theorem cycleParity_map_embedding (f : V ↪ W) (factor : V → Bool)
    (F : W → Bool) (hf : ∀ x, F (f x) = factor x) {u : V} (p : G.Walk u u) :
    cycleParity F (p.map (embeddingHom f G)) = cycleParity factor p := by
  simp [cycleParity, ← List.map_tail, List.map_map, Function.comp_def, factorWeight, hf]
  rfl

@[simp] theorem monochromatic_map_embedding (f : V ↪ W) (factor color : V → Bool)
    (F C : W → Bool) (hf : ∀ x, F (f x) = factor x)
    (hc : ∀ x, C (f x) = color x) {u v : V} (p : G.Walk u v) (c : Bool) :
    Monochromatic F C c (p.map (embeddingHom f G)) ↔
      Monochromatic factor color c p := by
  simp [Monochromatic, hf, hc]

/-- Isolated ambient vertices cannot create new cycles after embedding. -/
theorem good_map_embedding (f : V ↪ W) (factor color : V → Bool)
    (F C : W → Bool) (hf : ∀ x, F (f x) = factor x)
    (hc : ∀ x, C (f x) = color x) (hgood : Good factor color G) :
    Good F C (G.map f) := by
  intro x p hp c hm
  have hx : ∃ u, f u = x := by
    cases p with
    | nil => exact (hp.ne_nil rfl).elim
    | cons h q =>
      obtain ⟨u, v, huv, hu, hv⟩ := (SimpleGraph.map_adj f G _ _).mp h
      exact ⟨u, hu⟩
  obtain ⟨u, rfl⟩ := hx
  obtain ⟨q, rfl⟩ := exists_walk_map f p
  rw [cycleParity_map_embedding f factor F hf]
  exact hgood u q hp.of_map c ((monochromatic_map_embedding f factor color F C hf hc q c).mp hm)

/-- Exact simple-path sets and the good-cycle condition survive an injective relabeling. -/
theorem realizesSignature_map_embedding (f : V ↪ W) (factor color : V → Bool)
    (F C : W → Bool) (hf : ∀ x, F (f x) = factor x)
    (hc : ∀ x, C (f x) = color x) {u v : V} {s : StructuralTreewidth.Signature}
    (h : RealizesSignature factor color G u v s) :
    RealizesSignature F C (G.map f) (f u) (f v) s := by
  refine ⟨good_map_embedding f factor color F C hf hc h.1, ?_, ?_, ?_⟩
  · simpa [hf, hc] using h.2.1
  · simpa [hf, hc] using h.2.2.1
  · intro c b
    rw [h.2.2.2 c b]
    constructor
    · rintro ⟨p, hp, hm, hb⟩
      refine ⟨p.map (embeddingHom f G), hp.map f.injective, ?_, ?_⟩
      · exact (monochromatic_map_embedding f factor color F C hf hc p c).mpr hm
      · simpa only [pathParity_map_embedding f factor F hf] using hb
    · rintro ⟨p, hp, hm, hb⟩
      obtain ⟨q, rfl⟩ := exists_walk_map f p
      refine ⟨q, hp.of_map, ?_, ?_⟩
      · exact (monochromatic_map_embedding f factor color F C hf hc q c).mp hm
      · simpa only [pathParity_map_embedding f factor F hf] using hb

/-- Reversing terminals preserves the exact simple-path parity sets. -/
theorem RealizesSignature.reverse {factor color : V → Bool} {u v : V}
    {s : StructuralTreewidth.Signature} (h : RealizesSignature factor color G u v s) :
    RealizesSignature factor color G v u s.reverse := by
  refine ⟨h.1, h.2.2.1, h.2.1, ?_⟩
  intro c b
  rw [StructuralTreewidth.pathSet_reverse, h.2.2.2 c b]
  constructor
  · rintro ⟨p, hp, hm, hb⟩
    exact ⟨p.reverse, hp.reverse, (monochromatic_reverse ..).mpr hm, by simpa using hb⟩
  · rintro ⟨p, hp, hm, hb⟩
    exact ⟨p.reverse, hp.reverse, (monochromatic_reverse ..).mpr hm, by simpa using hb⟩

/-- Every actual bipartite edge realizes its active odd signature. -/
theorem edge_realizesSignature (factor : V → Bool) (u v : V)
    (htype : factor u ≠ factor v) (c : Bool) :
    RealizesSignature factor (fun _ => c) (SimpleGraph.edge u v) u v
      (StructuralTreewidth.active (factor u) (factor v) c true) := by
  classical
  have huv : u ≠ v := fun h => htype (congrArg factor h)
  let f : Bool ↪ V := ⟨fun x => if x then v else u, by
    intro x y h
    cases x <;> cases y <;> simp_all⟩
  have hf0 : f false = u := rfl
  have hf1 : f true = v := rfl
  have htype' : (!factor u) = factor v :=
    (show ∀ a b : Bool, a ≠ b → (!a) = b by decide) _ _ htype
  have hf : ∀ x, factor (f x) = edgeFactor (factor u) x := by
    intro x
    cases x
    · rfl
    · exact htype'.symm
  have hmap : edgeGraph.map f = SimpleGraph.edge u v := by
    ext x y
    constructor
    · intro hxy
      obtain ⟨a, b, hab, rfl, rfl⟩ := (SimpleGraph.map_adj f edgeGraph x y).mp hxy
      cases a <;> cases b
      · exact (hab rfl).elim
      · exact (SimpleGraph.edge_adj u v _ _).mpr ⟨Or.inl ⟨rfl, rfl⟩, huv⟩
      · exact (SimpleGraph.edge_adj u v _ _).mpr ⟨Or.inr ⟨rfl, rfl⟩, huv.symm⟩
      · exact (hab rfl).elim
    · intro hxy
      rcases (SimpleGraph.edge_adj u v x y).mp hxy with ⟨h | h, _⟩
      · obtain ⟨rfl, rfl⟩ := h
        exact (SimpleGraph.map_adj f edgeGraph _ _).mpr ⟨false, true, by decide, rfl, rfl⟩
      · obtain ⟨rfl, rfl⟩ := h
        exact (SimpleGraph.map_adj f edgeGraph _ _).mpr ⟨true, false, by decide, rfl, rfl⟩
  have h := realizesSignature_map_embedding f (edgeFactor (factor u)) (fun _ => c)
    factor (fun _ => c) hf (fun _ => rfl) (edge_realizes_active (factor u) c)
  rw [hmap] at h
  change RealizesSignature factor (fun _ => c) (SimpleGraph.edge u v) u v
    (StructuralTreewidth.active (factor u) (!(factor u)) c true) at h
  rwa [htype'] at h

end MultilinearGap.TreewidthGraph
