import Formal.MultilinearGap.StructuralFrequencyBox
import Formal.MultilinearGap.StructuralFactorGaps

/-! Transfer of cardinality-factor bounds to original monomials on boxes.
Fixed coordinates are removed only from the count support. Every original
monomial remains one factor, including empty and duplicate scopes. -/
namespace MultilinearGap
open CubicGap
noncomputable section
variable {I J : Type*} [Fintype I] [DecidableEq I] [Fintype J]

/-- The coordinates of an original scope that vary on the physical box. -/
def varyingBoxSupport (l u : I → ℝ) (s : Finset I) : Finset I :=
  s.filter fun i => l i ≠ u i

omit [Fintype I] [DecidableEq I] in
/-- A common aspect ratio is required only on coordinates that vary. -/
theorem monomial_commonAspect_varying_vertex (l u : I → ℝ) (s : Finset I)
    (rho a : ℝ) (hr : ∀ i ∈ varyingBoxSupport l u s, u i = rho * l i)
    (v : Vertex I) :
    a * monomial s (boxPoint l u (vertexPoint v)) =
      commonAspectSequence rho l a s (countOn (varyingBoxSupport l u s) v) := by
  classical
  have he (i : I) (hi : i ∈ s) : boxPoint l u (vertexPoint v) i =
      l i * (if l i ≠ u i ∧ v i = true then rho else 1) := by
    by_cases hfix : l i = u i
    · simp [boxPoint, ← hfix]
    · have hu := hr i (Finset.mem_filter.mpr ⟨hi, hfix⟩)
      by_cases hv : v i = true
      · rw [if_pos ⟨hfix, hv⟩]
        simp [boxPoint, vertexPoint, hv, hu, mul_comm]
      · rw [if_neg (fun h => hv h.2)]
        simp [boxPoint, vertexPoint, hv]
  rw [monomial, Finset.prod_congr rfl he, Finset.prod_mul_distrib,
    Finset.prod_ite, Finset.prod_const, Finset.prod_const_one, mul_one]
  have hs : (s.filter fun i => l i ≠ u i ∧ v i = true) =
      (varyingBoxSupport l u s).filter (fun i => v i = true) := by
    ext i
    simp [varyingBoxSupport, and_assoc]
  rw [hs]
  unfold commonAspectSequence countOn
  ring

omit [Fintype I] [DecidableEq I] in
/-- Each normalized physical factor is a discrete-convex count table. -/
theorem commonAspectSequence_convexCountTable (rho : ℝ) (hrho : 0 ≤ rho)
    (l : I → ℝ) (hl : ∀ i, 0 ≤ l i) (a : ℝ) (ha : 0 ≤ a)
    (s : Finset I) (d : ℕ) : ConvexCountTable (commonAspectSequence rho l a s) d := by
  intro k _
  have h := commonAspectSequence_convex rho hrho l hl a ha s k
  linarith

omit [Fintype I] [DecidableEq I] in
/-- The scalar gap of a weighted physical factor sum is at most the sum of
its original factor gaps, including boxes with fixed coordinates. -/
theorem boxHullGap_factorSum_monomial_le [Finite I]
    (support : J → Finset I) (a : J → ℝ) (ha : ∀ j, 0 ≤ a j)
    (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    boxHullGap l u (factorSum fun j y => a j * monomial (support j) y) x ≤
      ∑ j, a j * boxHullGap l u (monomial (support j)) x := by
  classical
  let := Fintype.ofFinite I
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint l u hlu x hx
  let f : J → (I → ℝ) → ℝ := fun j q => a j * monomial (support j) (boxPoint l u q)
  have hf (j : J) : SeparatelyAffine (f j) := by
    intro q i t
    have h := separatelyAffine_box_monomial l u (support j) q i t
    dsimp only at h
    dsimp [f]
    rw [h]
    ring
  rw [boxHullGap_eq_of_mem l u hlu _ p hp]
  calc
    _ = hullGap (factorSum f) p := rfl
    _ ≤ ∑ j, hullGap (f j) p := hullGap_factorSum_le f hf p hp
    _ = _ := by
      apply Finset.sum_congr rfl
      intro j _
      rw [boxHullGap_eq_of_mem l u hlu _ p hp]
      exact hullGap_scale _ (separatelyAffine_box_monomial l u (support j)) p hp (a j) (ha j)

/-- Reuse any proved cardinality-factor bound on the original physical
monomials. Ratios may differ between supports; shared varying coordinates
force compatible ratios. Fixed coordinates, ratio one, and zero weights are
included. The displayed bound premise is solely a reusable transfer interface. -/
theorem commonAspect_original_box_transfer
    (support : J → Finset I) (a : J → ℝ) (ha : ∀ j, 0 ≤ a j)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (rho : J → ℝ) (hrho : ∀ j, 0 ≤ rho j)
    (hr : ∀ j i, i ∈ varyingBoxSupport l u (support j) → u i = rho j * l i)
    (C : ℝ)
    (hbound : ∀ (f : J → (I → ℝ) → ℝ) (φ : J → ℕ → ℝ),
      (∀ j, SeparatelyAffine (f j)) →
      (∀ j, ConvexCountTable (φ j) (varyingBoxSupport l u (support j)).card) →
      (∀ j v, f j (vertexPoint v) = φ j (countOn (varyingBoxSupport l u (support j)) v)) →
      ∀ p ∈ cube I, (∑ j, hullGap (f j) p) ≤ C * hullGap (factorSum f) p)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    (∑ j, a j * boxHullGap l u (monomial (support j)) x) ≤
      C * boxHullGap l u (factorSum fun j y => a j * monomial (support j) y) x := by
  classical
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint l u hlu x hx
  let f : J → (I → ℝ) → ℝ := fun j q => a j * monomial (support j) (boxPoint l u q)
  let φ : J → ℕ → ℝ := fun j => commonAspectSequence (rho j) l (a j) (support j)
  have hf (j : J) : SeparatelyAffine (f j) := by
    intro q i t
    have h := separatelyAffine_box_monomial l u (support j) q i t
    dsimp [f]
    dsimp only at h
    rw [h]
    ring
  have hφ (j : J) : ConvexCountTable (φ j) (varyingBoxSupport l u (support j)).card :=
    commonAspectSequence_convexCountTable _ (hrho j) l hl _ (ha j) _ _
  have hv (j : J) (v : Vertex I) :
      f j (vertexPoint v) = φ j (countOn (varyingBoxSupport l u (support j)) v) :=
    monomial_commonAspect_varying_vertex l u (support j) (rho j) (a j) (hr j) v
  have hb := hbound f φ hf hφ hv p hp
  have hlocal (j : J) : a j * boxHullGap l u (monomial (support j)) (boxPoint l u p) =
      hullGap (f j) p := by
    rw [boxHullGap_eq_of_mem l u hlu _ p hp]
    exact (hullGap_scale _ (separatelyAffine_box_monomial l u (support j)) p hp (a j) (ha j)).symm
  simp_rw [hlocal]
  rw [boxHullGap_eq_of_mem l u hlu _ p hp]
  exact hb

end
end MultilinearGap
