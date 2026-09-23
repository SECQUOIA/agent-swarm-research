import Formal.DAGSpectral.TopologicalSortCost

namespace DAGSpectral
variable {v m : ℕ}

/-- Raw paths do not assume that the input's vertex numbers are topological. -/
inductive RawPath (src dst : Fin m → Fin v) (s : Fin v) :
    Fin v → List (Fin m) → Prop
  | nil : RawPath src dst s s []
  | snoc {u : Fin v} {es : List (Fin m)} (h : RawPath src dst s u es)
      (e : Fin m) (he : src e = u) : RawPath src dst s (dst e) (es ++ [e])

/-- Construct the ordered graph, preserving every original edge identity. -/
def topologicallyOrderedGraph (src dst : Fin m → Fin v) (ha : RawAcyclic src dst) :
    ExplicitDAG v m where
  src := topologicalOrder src dst ha ∘ src
  dst := topologicalOrder src dst ha ∘ dst
  forward := topologicalOrder_forward src dst ha

theorem RawPath.toOrdered {src dst : Fin m → Fin v} (ha : RawAcyclic src dst)
    {s t : Fin v} {es : List (Fin m)} (hp : RawPath src dst s t es) :
    (topologicallyOrderedGraph src dst ha).Path
      (topologicalOrder src dst ha s) (topologicalOrder src dst ha t) es := by
  induction hp with
  | nil => exact .nil
  | @snoc u es hp e he ih =>
    exact ih.snoc e (congrArg (topologicalOrder src dst ha) he)

theorem orderedPath_toRaw {src dst : Fin m → Fin v} (ha : RawAcyclic src dst)
    {a b : Fin v} {es : List (Fin m)}
    (hp : (topologicallyOrderedGraph src dst ha).Path a b es) :
    RawPath src dst ((topologicalOrder src dst ha).symm a)
      ((topologicalOrder src dst ha).symm b) es := by
  induction hp with
  | nil => exact .nil
  | @snoc u es hp e he ih =>
    have hsrc : src e = (topologicalOrder src dst ha).symm u := by
      apply (topologicalOrder src dst ha).injective
      simpa only [Equiv.apply_symm_apply, topologicallyOrderedGraph,
        Function.comp_apply] using he
    simpa only [topologicallyOrderedGraph, Function.comp_apply, Equiv.symm_apply_apply] using
      ih.snoc e hsrc

theorem rawPath_iff_ordered {src dst : Fin m → Fin v} (ha : RawAcyclic src dst)
    {s t : Fin v} {es : List (Fin m)} :
    RawPath src dst s t es ↔ (topologicallyOrderedGraph src dst ha).Path
      (topologicalOrder src dst ha s) (topologicalOrder src dst ha t) es := by
  constructor
  · exact RawPath.toOrdered ha
  · intro hp
    simpa only [Equiv.symm_apply_apply] using orderedPath_toRaw ha hp

theorem rawPath_length_bound {src dst : Fin m → Fin v} (ha : RawAcyclic src dst)
    {s t : Fin v} {es : List (Fin m)} (hp : RawPath src dst s t es) :
    es.length ≤ v - 1 := (hp.toOrdered ha).length_le_vertices

theorem rawPath_nodup {src dst : Fin m → Fin v} (ha : RawAcyclic src dst)
    {s t : Fin v} {es : List (Fin m)} (hp : RawPath src dst s t es) : es.Nodup :=
  (hp.toOrdered ha).nodup

end DAGSpectral
