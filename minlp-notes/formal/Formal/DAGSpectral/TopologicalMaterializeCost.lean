import Formal.DAGSpectral.TopologicalPath

/-! Materialize reordered endpoints from one cached topological list.
The counter measures the executed index scans and endpoint copies. The separate
Kahn bound counts incoming-edge tests; neither count is advertised as the full
bit cost of raw-graph preprocessing. -/
namespace DAGSpectral

/-- An explicit equality scan implementing first-occurrence list indexing. -/
def topologicalIndexScan {α : Type*} [DecidableEq α] (x : α) : List α → ℕ × ℕ
  | [] => (0, 1)
  | y :: ys => if x = y then (0, 1) else
      let rest := topologicalIndexScan x ys
      (rest.1 + 1, rest.2 + 1)

@[simp] theorem topologicalIndexScan_value {α : Type*} [DecidableEq α] (x : α) (xs : List α) :
    (topologicalIndexScan x xs).1 = xs.idxOf x := by
  induction xs with
  | nil => simp [topologicalIndexScan]
  | cons y ys ih =>
    simp only [topologicalIndexScan]
    split_ifs with h
    · subst y; simp
    · simp [Ne.symm h, ih]

theorem topologicalIndexScan_cost {α : Type*} [DecidableEq α] (x : α) (xs : List α) :
    (topologicalIndexScan x xs).2 ≤ xs.length + 1 := by
  induction xs with
  | nil => simp [topologicalIndexScan]
  | cons y ys ih =>
    simp only [topologicalIndexScan, List.length_cons]
    split_ifs <;> simp_all

/-- Execute both endpoint index scans for each listed edge. -/
def topologicalEndpointScan {v m : ℕ} (xs : List (Fin v)) (src dst : Fin m → Fin v) :
    List (Fin m) → List (ℕ × ℕ) × ℕ
  | [] => ([], 1)
  | e :: es =>
    let s := topologicalIndexScan (src e) xs
    let t := topologicalIndexScan (dst e) xs
    let rest := topologicalEndpointScan xs src dst es
    ((s.1, t.1) :: rest.1, s.2 + t.2 + rest.2 + 1)

@[simp] theorem topologicalEndpointScan_value {v m : ℕ} (xs : List (Fin v))
    (src dst : Fin m → Fin v) (es : List (Fin m)) :
    (topologicalEndpointScan xs src dst es).1 =
      es.map (fun e => (xs.idxOf (src e), xs.idxOf (dst e))) := by
  induction es with
  | nil => rfl
  | cons e es ih => simp [topologicalEndpointScan, ih]

theorem topologicalEndpointScan_cost {v m : ℕ} (xs : List (Fin v))
    (src dst : Fin m → Fin v) (es : List (Fin m)) :
    (topologicalEndpointScan xs src dst es).2 ≤
      es.length * (2 * (xs.length + 1) + 1) + 1 := by
  induction es with
  | nil => simp [topologicalEndpointScan]
  | cons e es ih =>
    have hs := topologicalIndexScan_cost (src e) xs
    have ht := topologicalIndexScan_cost (dst e) xs
    simp only [topologicalEndpointScan, List.length_cons]
    nlinarith

theorem topological_materialization_scan_bound {v m : ℕ} (src dst : Fin m → Fin v)
    (ha : RawAcyclic src dst) :
    (topologicalEndpointScan (topologicalList src dst) src dst (List.finRange m)).2 ≤
      m * (2 * (v + 1) + 1) + 1 := by
  simpa only [List.length_finRange, topologicalList_length src dst ha] using
    topologicalEndpointScan_cost (topologicalList src dst) src dst (List.finRange m)

/-- Explicit cached endpoint vectors. The topological list is computed before
forming the endpoint closures, so later endpoint access does not rerun Kahn. -/
def materializedTopologicalGraph {v m : ℕ} (src dst : Fin m → Fin v)
    (ha : RawAcyclic src dst) : ExplicitDAG v m :=
  let xs := topologicalList src dst
  let rank : Fin v → Fin v := fun x => ⟨(topologicalIndexScan x xs).1, by
    rw [topologicalIndexScan_value]
    exact lt_of_lt_of_eq (List.idxOf_lt_length_iff.mpr (topologicalList_mem src dst ha x))
      (topologicalList_length src dst ha)⟩
  let endpoints := Vector.ofFn (fun e : Fin m => (rank (src e), rank (dst e)))
  { src := fun e => (endpoints.get e).1
    dst := fun e => (endpoints.get e).2
    forward := by
      intro e
      simp only [endpoints, Vector.get_ofFn]
      change (topologicalIndexScan (src e) xs).1 < (topologicalIndexScan (dst e) xs).1
      simp only [topologicalIndexScan_value]
      exact topologicalOrder_forward src dst ha e }

theorem materializedTopologicalGraph_eq {v m : ℕ} (src dst : Fin m → Fin v)
    (ha : RawAcyclic src dst) :
    materializedTopologicalGraph src dst ha = topologicallyOrderedGraph src dst ha := by
  have heq : ∀ G H : ExplicitDAG v m, G.src = H.src → G.dst = H.dst → G = H := by
    intro G H hs hd
    cases G
    cases H
    cases hs
    cases hd
    rfl
  apply heq <;> funext e <;> apply Fin.ext <;>
    simp [materializedTopologicalGraph, topologicallyOrderedGraph, topologicalOrder]

end DAGSpectral
