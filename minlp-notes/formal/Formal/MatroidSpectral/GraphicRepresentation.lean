import Mathlib.Combinatorics.SimpleGraph.Acyclic
import Mathlib.LinearAlgebra.LinearIndependent.Defs
import Mathlib.Algebra.BigOperators.Group.Finset.Piecewise

/-! Rational oriented incidence vectors and their graph-theoretic span.

The span criterion below uses actual walk reachability. In particular it does
not define forests in terms of linear independence.
-/
namespace MatroidSpectral.Graphic
open scoped BigOperators
open SimpleGraph

variable {V : Type*} [DecidableEq V]

def edgeVector (u v : V) : V → ℚ := Pi.single u 1 - Pi.single v 1

theorem edgeVector_self (u : V) : edgeVector u u = 0 := by simp [edgeVector]

theorem edgeVector_reverse (u v : V) : edgeVector v u = -edgeVector u v := by
  simp [edgeVector, neg_sub]

theorem edgeVector_add (u v w : V) : edgeVector u v + edgeVector v w = edgeVector u w := by
  simp [edgeVector]

def edgeSpan (G : SimpleGraph V) : Submodule ℚ (V → ℚ) :=
  Submodule.span ℚ {x | ∃ u v, G.Adj u v ∧ x = edgeVector u v}

theorem adj_vector_mem (G : SimpleGraph V) {u v : V} (h : G.Adj u v) :
    edgeVector u v ∈ edgeSpan G :=
  Submodule.subset_span ⟨u, v, h, rfl⟩

theorem reachable_vector_mem (G : SimpleGraph V) {u v : V} (h : G.Reachable u v) :
    edgeVector u v ∈ edgeSpan G := by
  obtain ⟨w⟩ := h
  induction w with
  | nil => simp [edgeVector_self]
  | @cons u v w huv p ih =>
      rw [← edgeVector_add u v w]
      exact (edgeSpan G).add_mem (adj_vector_mem G huv) ih

variable [Fintype V]

noncomputable def componentSum (G : SimpleGraph V) (u : V) : (V → ℚ) →ₗ[ℚ] ℚ := by
  classical
  exact
    { toFun := fun x => ∑ v, if G.Reachable u v then x v else 0
      map_add' := by
        intro x y
        simp only [Pi.add_apply, ← Finset.sum_add_distrib]
        apply Finset.sum_congr rfl
        intro v _
        split_ifs <;> simp
      map_smul' := by intro a x; simp [Finset.mul_sum, mul_ite] }

open Classical in
@[simp] theorem componentSum_single (G : SimpleGraph V) (u v : V) :
    componentSum G u (Pi.single v 1) = if G.Reachable u v then 1 else 0 := by
  classical
  change (∑ x, if G.Reachable u x then (Pi.single v (1 : ℚ)) x else 0) = _
  rw [Finset.sum_eq_single v]
  · simp
  · intro b _ hb
    simp [hb]
  · simp

theorem componentSum_adj (G : SimpleGraph V) (u : V) {v w : V} (h : G.Adj v w) :
    componentSum G u (edgeVector v w) = 0 := by
  classical
  have hr : G.Reachable u v ↔ G.Reachable u w :=
    ⟨fun hv => hv.trans h.reachable, fun hw => hw.trans h.symm.reachable⟩
  simp [edgeVector, hr]

theorem edgeSpan_le_componentKernel (G : SimpleGraph V) (u : V) :
    edgeSpan G ≤ LinearMap.ker (componentSum G u) := by
  apply Submodule.span_le.mpr
  rintro x ⟨v, w, h, rfl⟩
  exact componentSum_adj G u h

omit [Fintype V] in
theorem vector_mem_iff_reachable [Finite V] (G : SimpleGraph V) (u v : V) :
    edgeVector u v ∈ edgeSpan G ↔ G.Reachable u v := by
  classical
  let := Fintype.ofFinite V
  refine ⟨fun h => ?_, reachable_vector_mem G⟩
  have hz := edgeSpan_le_componentKernel G u h
  by_contra hn
  have he : componentSum G u (edgeVector u v) = 0 := hz
  simp [edgeVector, hn] at he

end MatroidSpectral.Graphic
