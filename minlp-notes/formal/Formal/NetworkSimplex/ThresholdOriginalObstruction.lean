import Formal.NetworkSimplex.ThresholdObstruction
import Formal.NetworkSimplex.ThresholdFace
import Formal.NetworkSimplex.ThresholdSection

/-! The coefficient-two section in actual original coordinates, with four explicit labels. -/
namespace NetworkSimplex.Chain.ThresholdObstruction
open scoped BigOperators
noncomputable section

abbrev Obs := Observation classes (fun _ => False)
noncomputable instance : Fintype Obs := Fintype.ofFinite Obs

/-- The two free coordinates are individual observed products, without scaling. -/
def obsU : Obs := ⟨(a 0, 3), by simp [Selected, a, classes, observesA]⟩
def obsV : Obs := ⟨(a 1, 1), by simp [Selected, a, classes, observesA]⟩

def originalObstructionGraph :=
  OriginalGraph (incidence 4) (demand 4) (fun _ => 1)
    (fun o : Obs => o.val.1) (fun o => o.val.2)

theorem section_original_hull_iff {U V : ℝ} (h : Near U V) :
    sectionPoint U V ∈ convexHull ℝ originalObstructionGraph ↔ 3 / 32 ≤ 2 * U + V := by
  unfold originalObstructionGraph
  rw [original_hull_iff_full_of_sum_one _ _ _ _ _ _ (by
    change (∑ _ : Fin 4, (1 / 4 : ℝ)) = 1
    norm_num)]
  exact section_hull_iff h

/-- An arbitrary affine row in the original flow, simplex and observed-product coordinates. -/
structure OriginalRow where
  constant : ℝ
  flow : ChainArc 4 → ℝ
  weight : Fin 4 → ℝ
  product : Obs → ℝ

def OriginalRow.eval (r : OriginalRow) (p : OriginalPoint (ChainArc 4) Obs 4) : ℝ :=
  r.constant + (∑ e, r.flow e * p.1 e) +
    (∑ j, r.weight j * p.2.1 j) + ∑ o, r.product o * p.2.2 o

theorem section_product (u v : ℝ) (o : Obs) :
    (sectionPoint (1 / 32 + u) (1 / 32 + v)).2.2 o =
      (sectionPoint (1 / 32) (1 / 32)).2.2 o +
        (if o = obsU then u else 0) + (if o = obsV then v else 0) := by
  rcases o with ⟨⟨e, j⟩, ho⟩
  rcases e with ⟨i, flag⟩ | z
  · cases flag
    · fin_cases i <;> fin_cases j <;>
        simp [sectionPoint, chainPoint, pack, observedA, obsU, obsV, a,
          Selected, classes, observesA, Obs, Observation, Subtype.ext_iff, reduceCtorEq] at ho ⊢
    · fin_cases i <;> fin_cases j <;> simp [Selected, classes, observesB, reduceCtorEq] at ho
  · exact ho.elim

/-- Restriction preserves exactly the original coefficients on the two free products. -/
theorem OriginalRow.eval_section (r : OriginalRow) (u v : ℝ) :
    r.eval (sectionPoint (1 / 32 + u) (1 / 32 + v)) =
      r.eval (sectionPoint (1 / 32) (1 / 32)) + r.product obsU * u + r.product obsV * v := by
  unfold OriginalRow.eval
  simp_rw [section_product]
  simp only [mul_add, Finset.sum_add_distrib, mul_ite, mul_zero]
  simp only [Finset.sum_ite_eq', Finset.mem_univ, ↓reduceIte]
  simp only [sectionPoint, chainPoint]
  ring

/-- This original-coordinate hull has no unit-product description, even with
arbitrary flow/simplex coefficients and any additional affine equations. -/
theorem no_original_unit_description {ι κ : Type*} (rows : ι → OriginalRow)
    (eqs : κ → OriginalRow)
    (hunit : ∀ i o, UnitCoefficient ((rows i).product o)) :
    ¬ (∀ p, p ∈ convexHull ℝ originalObstructionGraph ↔
      (∀ i, 0 ≤ (rows i).eval p) ∧ (∀ j, (eqs j).eval p = 0)) := by
  intro hd
  apply local_halfplane_not_unit_description (ε := (1 / 128 : ℝ)) (by norm_num)
    (fun i => (rows i).product obsU) (fun i => (rows i).product obsV)
    (fun i => (rows i).eval (sectionPoint (1 / 32) (1 / 32)))
    (fun j => (eqs j).product obsU) (fun j => (eqs j).product obsV)
    (fun j => (eqs j).eval (sectionPoint (1 / 32) (1 / 32)))
    (fun i => hunit i _) (fun i => hunit i _)
  intro u v hu hv
  have hn : Near (1 / 32 + u) (1 / 32 + v) := by simpa [Near] using And.intro hu hv
  have hh := section_original_hull_iff hn
  rw [hd] at hh
  simp only [OriginalRow.eval_section] at hh
  exact hh.trans (by constructor <;> intro h <;> linarith)

/-- Any valid affine equation has zero coefficients on both free products. -/
theorem valid_equation_free_coefficients (r : OriginalRow)
    (h : ∀ p ∈ convexHull ℝ originalObstructionGraph, r.eval p = 0) :
    r.product obsU = 0 ∧ r.product obsV = 0 := by
  have he := local_halfplane_equation_zero (ε := (1 / 128 : ℝ)) (by norm_num)
    (A := r.product obsU) (B := r.product obsV)
    (c := r.eval (sectionPoint (1 / 32) (1 / 32))) (by
      intro u v hu hv hh
      rw [← r.eval_section]
      apply h
      apply (section_original_hull_iff (by simpa [Near] using And.intro hu hv)).mpr
      linarith)
  exact ⟨he.1, he.2.1⟩

/-- Every finite affine description contains a row with the unavoidable ratio two.
The previous theorem proves invariance under all valid affine-hull equations. -/
theorem finite_description_ratio {ι κ : Type*} [Finite ι] (rows : ι → OriginalRow)
    (eqs : κ → OriginalRow)
    (h : ∀ p, p ∈ convexHull ℝ originalObstructionGraph ↔
      (∀ i, 0 ≤ (rows i).eval p) ∧ (∀ j, (eqs j).eval p = 0)) :
    ∃ i, ∃ t : ℝ, 0 < t ∧ (rows i).product obsU = 2 * t ∧
      (rows i).product obsV = t := by
  have hd := local_halfplane_description_positive_multiple (ε := (1 / 128 : ℝ)) (by norm_num)
    (fun i => (rows i).product obsU) (fun i => (rows i).product obsV)
    (fun i => (rows i).eval (sectionPoint (1 / 32) (1 / 32)))
    (fun j => (eqs j).product obsU) (fun j => (eqs j).product obsV)
    (fun j => (eqs j).eval (sectionPoint (1 / 32) (1 / 32))) (by
      intro u v hu hv
      have hn : Near (1 / 32 + u) (1 / 32 + v) := by simpa [Near] using And.intro hu hv
      have hh := section_original_hull_iff hn
      rw [h] at hh
      simp only [OriginalRow.eval_section] at hh
      exact hh.trans (by constructor <;> intro h <;> linarith))
  obtain ⟨i, t, ht, _, hU, hV⟩ := hd
  exact ⟨i, t, ht, hU, hV⟩

end
end NetworkSimplex.Chain.ThresholdObstruction
