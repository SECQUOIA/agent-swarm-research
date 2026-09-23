import Formal.NetworkSimplex.Disaggregation

namespace NetworkSimplex

noncomputable section

def OriginalSimplex {m : ℕ} (y : Fin m → ℝ) : Prop :=
  (∀ j, 0 ≤ y j) ∧ ∑ j, y j ≤ 1

def residualWeights {m : ℕ} (y : Fin m → ℝ) : Fin (m + 1) → ℝ :=
  Fin.cons (1 - ∑ j, y j) y

theorem residualWeights_simplex {m : ℕ} (y : Fin m → ℝ) :
    Simplex (residualWeights y) ↔ OriginalSimplex y := by
  constructor
  · rintro ⟨h, _⟩
    refine ⟨fun j => h j.succ, ?_⟩
    have hz := h 0
    change 0 ≤ 1 - ∑ j, y j at hz
    linarith
  · rintro ⟨hy, hs⟩
    constructor
    · intro j
      refine Fin.cases ?_ (fun i => hy i) j
      change 0 ≤ 1 - ∑ j, y j
      linarith
    · simp [residualWeights, Fin.sum_univ_succ]

theorem residualWeights_reconstruct {m : ℕ} (w : Fin (m + 1) → ℝ)
    (hw : Simplex w) : residualWeights (fun j => w j.succ) = w := by
  funext j
  refine Fin.cases ?_ (fun _ => rfl) j
  have h := hw.2
  rw [Fin.sum_univ_succ] at h
  change 1 - ∑ j : Fin m, w j.succ = w 0
  linarith

abbrev OriginalPoint (E O : Type*) (m : ℕ) := (E → ℝ) × ((Fin m → ℝ) × (O → ℝ))

def liftPoint {E O : Type*} {m : ℕ} (p : OriginalPoint E O m) : Point E (Fin (m + 1)) O :=
  (p.1, residualWeights p.2.1, p.2.2)

def projectPoint {E O : Type*} {m : ℕ} (p : Point E (Fin (m + 1)) O) : OriginalPoint E O m :=
  (p.1, (fun j => p.2.1 j.succ), p.2.2)

theorem project_lift {E O : Type*} {m : ℕ} (p : OriginalPoint E O m) :
    projectPoint (liftPoint p) = p := rfl

theorem liftPoint_affine {E O : Type*} {m : ℕ} (p q : OriginalPoint E O m)
    (r s : ℝ) (hrs : r + s = 1) :
    liftPoint (r • p + s • q) = r • liftPoint p + s • liftPoint q := by
  apply Prod.ext
  · rfl
  · apply Prod.ext
    · funext j
      refine Fin.cases ?_ (fun _ => rfl) j
      change 1 - ∑ j, (r * p.2.1 j + s * q.2.1 j) =
        r * (1 - ∑ j, p.2.1 j) + s * (1 - ∑ j, q.2.1 j)
      simp only [Finset.sum_add_distrib, ← Finset.mul_sum]
      nlinarith only [hrs]
    · rfl

def OriginalGraph {E V O : Type*} {m : ℕ}
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (label : O → Fin m) : Set (OriginalPoint E O m) :=
  {p | OriginalSimplex p.2.1 ∧ Flow A b u 1 p.1 ∧
    ∀ o, p.2.2 o = p.1 (arc o) * p.2.1 (label o)}

theorem graph_lift_iff {E V O : Type*} {m : ℕ}
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (label : O → Fin m) (p : OriginalPoint E O m) :
    liftPoint p ∈ Graph A b u arc (fun o => (label o).succ) ↔
      p ∈ OriginalGraph A b u arc label := by
  change (Simplex (residualWeights p.2.1) ∧ Flow A b u 1 p.1 ∧ _) ↔ _
  rw [residualWeights_simplex]
  rfl

theorem graph_project {E V O : Type*} {m : ℕ}
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (label : O → Fin m) {p : Point E (Fin (m + 1)) O}
    (h : p ∈ Graph A b u arc (fun o => (label o).succ)) :
    projectPoint p ∈ OriginalGraph A b u arc label := by
  refine ⟨⟨fun j => h.1.1 j.succ, ?_⟩, h.2.1, h.2.2⟩
  have hw := h.1.2
  rw [Fin.sum_univ_succ] at hw
  have hz := h.1.1 0
  change ∑ j : Fin m, p.2.1 j.succ ≤ 1
  linarith

/-- Adding the residual coordinate preserves exactly the original sparse-product hull. -/
theorem original_hull_iff_lift {E V O : Type*} {m : ℕ}
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (label : O → Fin m) (p : OriginalPoint E O m) :
    p ∈ convexHull ℝ (OriginalGraph A b u arc label) ↔
      liftPoint p ∈ convexHull ℝ (Graph A b u arc (fun o => (label o).succ)) := by
  constructor
  · intro hp
    apply (convexHull_min (t := {q : OriginalPoint E O m |
      liftPoint q ∈ convexHull ℝ (Graph A b u arc (fun o => (label o).succ))}) ?_ ?_) hp
    · intro q hq
      exact subset_convexHull ℝ _ ((graph_lift_iff A b u arc label q).mpr hq)
    · intro x hx y hy r s hr hs hrs
      change liftPoint (r • x + s • y) ∈
        convexHull ℝ (Graph A b u arc (fun o => (label o).succ))
      rw [liftPoint_affine x y r s hrs]
      exact (convex_convexHull ℝ _) hx hy hr hs hrs
  · intro hp
    have h : ∀ q ∈ convexHull ℝ (Graph A b u arc (fun o => (label o).succ)),
        projectPoint q ∈ convexHull ℝ (OriginalGraph A b u arc label) := by
      apply convexHull_min (t := {q : Point E (Fin (m + 1)) O |
        projectPoint q ∈ convexHull ℝ (OriginalGraph A b u arc label)})
      · intro q hq
        exact subset_convexHull ℝ _ (graph_project A b u arc label hq)
      · intro x hx y hy r s hr hs hrs
        exact (convex_convexHull ℝ _) hx hy hr hs hrs
    exact h _ hp

/-- The original-coordinate statement, retaining the residual state's capacity bounds. -/
theorem original_mem_hull_iff {E V O : Type*} {m : ℕ}
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (label : O → Fin m) (p : OriginalPoint E O m) :
    p ∈ convexHull ℝ (OriginalGraph A b u arc label) ↔
      OriginalSimplex p.2.1 ∧ ∃ f : Fin (m + 1) → E → ℝ,
        (∀ k, Flow A b u (residualWeights p.2.1 k) (f k)) ∧
        (∑ k, f k) = p.1 ∧ ∀ o, f (label o).succ (arc o) = p.2.2 o := by
  rw [original_hull_iff_lift, mem_convexHull_graph_iff]
  change (Simplex (residualWeights p.2.1) ∧ _) ↔ _
  rw [residualWeights_simplex]
  rfl

end
end NetworkSimplex
