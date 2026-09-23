import Mathlib

/-! An explicitly indexed directed acyclic multigraph. Edge indices distinguish
parallel edges, and vertex indices give a topological order. -/
namespace DAGSpectral

structure ExplicitDAG (v m : ℕ) where
  src : Fin m → Fin v
  dst : Fin m → Fin v
  forward : ∀ e, src e < dst e

namespace ExplicitDAG
variable {v m : ℕ} (G : ExplicitDAG v m)

/-- A path records actual edge identities in traversal order. -/
inductive Path (s : Fin v) : Fin v → List (Fin m) → Prop
  | nil : Path s s []
  | snoc {u : Fin v} {es : List (Fin m)} (h : Path s u es)
      (e : Fin m) (he : G.src e = u) : Path s (G.dst e) (es ++ [e])

variable {G}
theorem Path.start_le_end {s t : Fin v} {es : List (Fin m)} (h : G.Path s t es) :
    s ≤ t := by
  induction h with
  | nil => exact le_rfl
  | snoc h e he ih => exact le_trans ih (he ▸ le_of_lt (G.forward e))

theorem Path.length_bound {s t : Fin v} {es : List (Fin m)} (h : G.Path s t es) :
    es.length + s.val ≤ t.val := by
  induction h with
  | nil => simp
  | @snoc u es h e he ih =>
    have hf := G.forward e
    simp only [List.length_append, List.length_singleton]
    have hs : (G.src e).val = u.val := congrArg Fin.val he
    omega

theorem Path.length_le_vertices {s t : Fin v} {es : List (Fin m)}
    (h : G.Path s t es) : es.length ≤ v - 1 := by
  have := h.length_bound
  have := t.isLt
  omega

theorem Path.edge_between {s t : Fin v} {es : List (Fin m)} (h : G.Path s t es)
    {e : Fin m} (he : e ∈ es) : s ≤ G.src e ∧ G.dst e ≤ t := by
  induction h with
  | nil => simp at he
  | @snoc u es h f hf ih =>
    simp only [List.mem_append, List.mem_singleton] at he
    rcases he with he | rfl
    · obtain ⟨hs,ht⟩ := ih he
      exact ⟨hs, le_trans ht (hf ▸ le_of_lt (G.forward f))⟩
    · exact ⟨hf ▸ h.start_le_end, le_rfl⟩

theorem Path.nodup {s t : Fin v} {es : List (Fin m)} (h : G.Path s t es) :
    es.Nodup := by
  induction h with
  | nil => simp
  | @snoc u es h e he ih =>
    rw [List.nodup_append]
    refine ⟨ih, by simp, ?_⟩
    intro f hf g hg hfg
    simp only [List.mem_singleton] at hg
    subst g
    subst f
    have hh := (h.edge_between hf).2
    have hh' := G.forward e
    rw [he] at hh'
    exact (not_lt_of_ge hh) hh'

theorem Path.self_iff {s : Fin v} {es : List (Fin m)} :
    G.Path s s es ↔ es = [] := by
  constructor
  · intro h
    have hh := h.length_bound
    have : es.length = 0 := by omega
    exact List.length_eq_zero_iff.mp this
  · rintro rfl
    exact .nil

theorem Path.nil_iff {s t : Fin v} : G.Path s t [] ↔ s = t := by
  constructor
  · intro h
    have aux {a b : Fin v} {es : List (Fin m)} (hp : G.Path a b es) : es = [] → a = b := by
      induction hp with
      | nil => simp
      | snoc hp e he ih => simp
    exact aux h rfl
  · rintro rfl
    exact .nil

/-- Trial filtering leaves the original edge identities intact. -/
def AllowedPath (allowed : Fin m → Bool) (s t : Fin v) (es : List (Fin m)) : Prop :=
  G.Path s t es ∧ ∀ e ∈ es, allowed e = true

theorem AllowedPath.nil (allowed : Fin m → Bool) (s : Fin v) :
    G.AllowedPath allowed s s [] := ⟨.nil, by simp⟩

theorem AllowedPath.snoc {allowed : Fin m → Bool} {s u : Fin v} {es : List (Fin m)}
    (h : G.AllowedPath allowed s u es) (e : Fin m) (he : G.src e = u)
    (ha : allowed e = true) : G.AllowedPath allowed s (G.dst e) (es ++ [e]) := by
  refine ⟨h.1.snoc e he, ?_⟩
  intro f hf
  simp only [List.mem_append, List.mem_singleton] at hf
  rcases hf with hf | rfl
  · exact h.2 f hf
  · exact ha

end ExplicitDAG
end DAGSpectral
