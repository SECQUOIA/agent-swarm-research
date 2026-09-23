import Formal.DAGSpectral.Graph

/-! A computable check of the supplied vertex ordering. No acyclicity certificate
is trusted: every edge is checked against its actual endpoints. -/
namespace DAGSpectral

/-- Validate a graph whose vertex indices are claimed to be a topological order. -/
def checkDAG {v m : ℕ} (src dst : Fin m → Fin v) : Option (ExplicitDAG v m) :=
  if h : ∀ e, src e < dst e then some ⟨src, dst, h⟩ else none

theorem checkDAG_sound {v m : ℕ} {src dst : Fin m → Fin v} {G : ExplicitDAG v m}
    (h : checkDAG src dst = some G) :
    G.src = src ∧ G.dst = dst ∧ ∀ e, src e < dst e := by
  unfold checkDAG at h
  split_ifs at h with hf
  · cases h
    exact ⟨rfl, rfl, hf⟩

theorem checkDAG_complete {v m : ℕ} (src dst : Fin m → Fin v)
    (h : ∀ e, src e < dst e) :
    checkDAG src dst = some ⟨src, dst, h⟩ := by simp [checkDAG, h]

theorem checkDAG_reject_iff {v m : ℕ} (src dst : Fin m → Fin v) :
    checkDAG src dst = none ↔ ∃ e, dst e ≤ src e := by
  simp [checkDAG]

/-- A supplied permutation is applied to endpoints before the same finite check. -/
def checkDAGWithOrder {v m : ℕ} (src dst : Fin m → Fin v) (order : Equiv.Perm (Fin v)) :
    Option (ExplicitDAG v m) := checkDAG (order ∘ src) (order ∘ dst)

theorem checkDAGWithOrder_sound {v m : ℕ} {src dst : Fin m → Fin v}
    {order : Equiv.Perm (Fin v)} {G : ExplicitDAG v m}
    (h : checkDAGWithOrder src dst order = some G) :
    G.src = order ∘ src ∧ G.dst = order ∘ dst ∧ ∀ e, order (src e) < order (dst e) :=
  checkDAG_sound h

theorem checkDAGWithOrder_complete {v m : ℕ} (src dst : Fin m → Fin v)
    (order : Equiv.Perm (Fin v)) (h : ∀ e, order (src e) < order (dst e)) :
    checkDAGWithOrder src dst order = some ⟨order ∘ src, order ∘ dst, h⟩ :=
  checkDAG_complete _ _ h

end DAGSpectral
