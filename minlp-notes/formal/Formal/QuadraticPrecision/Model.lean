import Mathlib.Analysis.Convex.Combination
import Mathlib.Topology.Instances.Real.Lemmas
import Mathlib.Tactic

/-! Scalar convex integer lifts. The carrier need not be closed, and its integer
coordinates and real coefficients are unrestricted. -/
namespace QuadraticPrecision

abbrev Input (n : ℕ) := Fin n → ℝ
abbrev LiftPoint (n p q : ℕ) := Input n × ℝ × (Fin q → ℝ) × (Fin p → ℝ)

structure ConvexIntegerLift (n p q : ℕ) where
  carrier : Set (LiftPoint n p q)
  convex_carrier : Convex ℝ carrier

namespace ConvexIntegerLift
variable {n p q : ℕ}

def sectionAt (L : ConvexIntegerLift n p q) (z : Fin p → ℝ) : Set (Input n × ℝ) :=
  {v | ∃ a : Fin q → ℝ, (v.1, v.2, a, z) ∈ L.carrier}

def relaxation (L : ConvexIntegerLift n p q) : Set (Input n × ℝ) :=
  {v | ∃ z : Fin p → ℤ, v ∈ L.sectionAt (fun i => (z i : ℝ))}

theorem section_mix (L : ConvexIntegerLift n p q)
    {z z' : Fin p → ℝ} {v v' : Input n × ℝ}
    (hv : v ∈ L.sectionAt z) (hv' : v' ∈ L.sectionAt z')
    {a b : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (hab : a + b = 1) :
    a • v + b • v' ∈ L.sectionAt (a • z + b • z') := by
  obtain ⟨u, hu⟩ := hv
  obtain ⟨u', hu'⟩ := hv'
  exact ⟨a • u + b • u', L.convex_carrier hu hu' ha hb hab⟩

theorem convex_sectionAt (L : ConvexIntegerLift n p q) (z : Fin p → ℝ) :
    Convex ℝ (L.sectionAt z) := by
  intro v hv v' hv' a b ha hb hab
  have h := L.section_mix hv hv' ha hb hab
  simpa only [← add_smul, hab, one_smul] using h

/-- A finite convex combination of sections lies in the section at the same
combination of real indices. -/
theorem section_sum (L : ConvexIntegerLift n p q) {ι : Type*} [Fintype ι]
    (w : ι → ℝ) (hw : ∀ i, 0 ≤ w i) (hsum : ∑ i, w i = 1)
    (v : ι → Input n × ℝ) (z : ι → Fin p → ℝ)
    (hv : ∀ i, v i ∈ L.sectionAt (z i)) :
    (∑ i, w i • v i) ∈ L.sectionAt (∑ i, w i • z i) := by
  classical
  choose u hu using hv
  refine ⟨∑ i, w i • u i, ?_⟩
  have h := L.convex_carrier.sum_mem (t := Finset.univ)
    (fun i _ => hw i) hsum (fun i _ => hu i)
  convert h using 1
  simp [← prod_mk_sum]

/-- The finite-mixture obstruction requires only that the averaged integer
index is integral; the individual integer indices may be arbitrarily large. -/
theorem integral_mixture (L : ConvexIntegerLift n p q) {ι : Type*} [Fintype ι]
    (w : ι → ℝ) (hw : ∀ i, 0 ≤ w i) (hsum : ∑ i, w i = 1)
    (v : ι → Input n × ℝ) (z : ι → Fin p → ℤ)
    (hv : ∀ i, v i ∈ L.sectionAt (fun j => (z i j : ℝ)))
    (zbar : Fin p → ℤ)
    (hint : (∑ i, w i • (fun j => (z i j : ℝ))) = fun j => (zbar j : ℝ)) :
    (∑ i, w i • v i) ∈ L.relaxation := by
  refine ⟨zbar, ?_⟩
  rw [← hint]
  exact L.section_sum w hw hsum v _ hv

end ConvexIntegerLift

/-- Both graph containment and vertical soundness, including the input domain. -/
def IsGraphRelaxation {n : ℕ} (D : Set (Input n)) (f : Input n → ℝ) (ε : ℝ)
    (R : Set (Input n × ℝ)) : Prop :=
  (∀ x ∈ D, (x, f x) ∈ R) ∧
  ∀ v ∈ R, v.1 ∈ D ∧ |v.2 - f v.1| ≤ ε

/-- Contains the entire epigraph, including its unbounded output direction. -/
def IsEpigraphRelaxation {n : ℕ} (D : Set (Input n)) (f : Input n → ℝ) (ε : ℝ)
    (R : Set (Input n × ℝ)) : Prop :=
  (∀ x ∈ D, ∀ w, f x ≤ w → (x, w) ∈ R) ∧
  ∀ v ∈ R, v.1 ∈ D ∧ f v.1 - ε ≤ v.2

/-- Contains the entire hypograph, including its unbounded output direction. -/
def IsHypographRelaxation {n : ℕ} (D : Set (Input n)) (f : Input n → ℝ) (ε : ℝ)
    (R : Set (Input n × ℝ)) : Prop :=
  (∀ x ∈ D, ∀ w, w ≤ f x → (x, w) ∈ R) ∧
  ∀ v ∈ R, v.1 ∈ D ∧ v.2 ≤ f v.1 + ε

/-- The number of continuous coordinates is arbitrary but finite. -/
def HasGraphLift {n : ℕ} (D : Set (Input n)) (f : Input n → ℝ) (ε : ℝ) (p : ℕ) : Prop :=
  ∃ q, ∃ L : ConvexIntegerLift n p q, IsGraphRelaxation D f ε L.relaxation

def HasEpigraphLift {n : ℕ} (D : Set (Input n)) (f : Input n → ℝ) (ε : ℝ) (p : ℕ) : Prop :=
  ∃ q, ∃ L : ConvexIntegerLift n p q, IsEpigraphRelaxation D f ε L.relaxation

def HasHypographLift {n : ℕ} (D : Set (Input n)) (f : Input n → ℝ) (ε : ℝ) (p : ℕ) : Prop :=
  ∃ q, ∃ L : ConvexIntegerLift n p q, IsHypographRelaxation D f ε L.relaxation

end QuadraticPrecision
