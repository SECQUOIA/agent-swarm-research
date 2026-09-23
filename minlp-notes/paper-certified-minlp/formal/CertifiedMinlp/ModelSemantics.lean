import CertifiedMinlp.Transfer
import Mathlib.Data.EReal.Basic
import Mathlib.Data.Fin.Tuple.Basic

/-! Model normalization, extended-real bounds, and explicit auxiliary coordinates.
The extra coordinates are an unrestricted epigraph value and a fixed one. -/
namespace CertifiedMinlp
open scoped BigOperators

theorem normalized_upper_row (g u : ℝ) : g - u ≤ 0 ↔ g ≤ u := sub_nonpos

theorem normalized_lower_row (g l : ℝ) : l - g ≤ 0 ↔ l ≤ g := sub_nonpos

/-- The extended-real optimum also represents an empty feasible set correctly. -/
noncomputable def extendedOptimum {X : Type*} (F : Set X) (f : X → ℝ) : EReal :=
  ⨅ x ∈ F, (f x : EReal)

theorem extendedOptimum_lower {X : Type*} (F : Set X) (f : X → ℝ) (β : ℝ)
    (h : LowerBoundOn F f β) : (β : EReal) ≤ extendedOptimum F f := by
  exact le_iInf fun x => le_iInf fun hx => EReal.coe_le_coe_iff.mpr (h x hx)

theorem extendedOptimum_empty {X : Type*} (f : X → ℝ) :
    extendedOptimum ∅ f = ⊤ := by simp [extendedOptimum]

theorem extendedOptimum_le_witness {X : Type*} (F : Set X) (f : X → ℝ)
    (x : X) (hx : x ∈ F) : extendedOptimum F f ≤ (f x : EReal) := by
  exact iInf_le_of_le x (iInf_le_of_le hx le_rfl)

theorem primal_enclosure_gap {X : Type*} (F : Set X) (f : X → ℝ) (β U : ℝ)
    (x : X) (hlower : LowerBoundOn F f β) (hx : x ∈ F) (hupper : f x ≤ U) :
    0 ≤ U - sInf (f '' F) ∧ U - sInf (f '' F) ≤ U - β := by
  obtain ⟨hb, hw, _, _⟩ := primal_infimum_bounds F f β U x hlower hx hupper
  exact ⟨sub_nonneg.mpr (hw.trans hupper), sub_le_sub_left hb U⟩

def extendedPoint {n : ℕ} (x : Fin n → ℝ) (t : ℝ) : Fin (n + 2) → ℝ :=
  Fin.snoc (Fin.snoc x t) 1

def extendedCoefficients {n : ℕ} (a : Fin n → ℝ) (epigraph constant : ℝ) :
    Fin (n + 2) → ℝ := Fin.snoc (Fin.snoc a epigraph) constant

def originalPoint {n : ℕ} (y : Fin (n + 2) → ℝ) : Fin n → ℝ :=
  fun i => y i.castSucc.castSucc

@[simp] theorem originalPoint_extendedPoint {n : ℕ} (x : Fin n → ℝ) (t : ℝ) :
    originalPoint (extendedPoint x t) = x := by
  funext i
  simp [originalPoint, extendedPoint]

@[simp] theorem extendedPoint_epigraph {n : ℕ} (x : Fin n → ℝ) (t : ℝ) :
    extendedPoint x t (Fin.last n).castSucc = t := by simp [extendedPoint]

@[simp] theorem extendedPoint_constant {n : ℕ} (x : Fin n → ℝ) (t : ℝ) :
    extendedPoint x t (Fin.last (n + 1)) = 1 := by simp [extendedPoint]

theorem dot_extendedPoint {n : ℕ} (a x : Fin n → ℝ) (ae ac t : ℝ) :
    dot (extendedCoefficients a ae ac) (extendedPoint x t) = dot a x + ae * t + ac := by
  simp [dot, extendedCoefficients, extendedPoint, Fin.sum_univ_castSucc]

theorem affine_objective_constant_once {n : ℕ} (a x : Fin n → ℝ) (c t : ℝ) :
    dot (extendedCoefficients a 0 c) (extendedPoint x t) = affine a c x := by
  simp [dot_extendedPoint, affine]

theorem epigraph_objective_preserved {n : ℕ} (x : Fin n → ℝ) (f : ℝ) :
    dot (extendedCoefficients (fun _ => 0) 1 0) (extendedPoint x f) = f := by
  rw [dot_extendedPoint]
  simp [dot]

theorem epigraph_graph_row {n : ℕ} (h : (Fin n → ℝ) → ℝ) (x : Fin n → ℝ) :
    h (originalPoint (extendedPoint x (h x))) -
      extendedPoint x (h x) (Fin.last n).castSucc = 0 := by simp

end CertifiedMinlp
